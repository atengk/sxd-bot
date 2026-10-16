"""神仙道异步长连接网络客户端与串行命令管理引擎

负责维持与服务端网关的 asyncio TCP Socket 长连接、滑动窗口收包循环、串行命令锁以及请求-应答 Future 匹配唤醒。

@author Ateng
@since 2026-10-15
"""

import asyncio
import logging
import struct
from typing import Optional, Dict, List, Tuple
from core.context import GameContext
from core.events import EventBus
from protocol.frame import FrameFSM
from protocol.packet import BasePacket, ByteArrayReader
from protocol.messages.player import PlayerLoginResp, PlayerInfoResp

logger = logging.getLogger(__name__)


class SXDClient:
    """神仙道无头异步 TCP 客户端

    @author Ateng
    @since 2026-10-15
    """

    def __init__(self, context: Optional[GameContext] = None, event_bus: Optional[EventBus] = None) -> None:
        self.context = context or GameContext()
        self.event_bus = event_bus or EventBus()
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._frame_fsm = FrameFSM()
        self._running = False
        self._read_task: Optional[asyncio.Task] = None
        self._request_lock = asyncio.Lock()
        self._pending_futures: Dict[Tuple[int, int], List[asyncio.Future]] = {}

    async def connect(self, host: str, port: int, timeout_sec: float = 8.0) -> bool:
        """建立至目标游戏服务端的 TCP 异步长连接

        Args:
            host: 目标服务器 IP 或域名。
            port: 目标端口号。
            timeout_sec: 连接超时时间。

        Returns:
            若建立成功返回 True，否则返回 False。
        """
        try:
            logger.info("正在建立与神仙道网关的 TCP 连接: %s:%d", host, port)
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=timeout_sec,
            )
            self._running = True
            self.context.set_connected(True)
            self._read_task = asyncio.create_task(self._read_loop())
            logger.info("TCP 连接建立成功，接收调度协程已启动")
            return True
        except Exception as exc:
            logger.error("TCP 连接失败 [%s:%d]: %s", host, port, exc)
            self.context.set_connected(False)
            return False

    async def disconnect(self) -> None:
        """优雅关闭长连接并释放资源"""
        self._running = False
        self.context.set_connected(False)

        if self._writer is not None:
            try:
                self._writer.close()
                await self._writer.wait_closed()
            except Exception:
                pass
            self._writer = None

        current_task = asyncio.current_task()
        if self._read_task is not None and self._read_task != current_task:
            self._read_task.cancel()
            try:
                await self._read_task
            except (asyncio.CancelledError, Exception):
                pass
            self._read_task = None

        # 唤醒所有挂起的 Future 并抛出连接中断异常
        for key, futures in self._pending_futures.items():
            for fut in futures:
                if not fut.done():
                    fut.set_exception(ConnectionResetError("TCP 连接已主动关闭"))
        self._pending_futures.clear()
        self._frame_fsm.clear()
        logger.info("TCP 长连接已完全关闭并重置状态")

    def abort(self) -> None:
        """强杀 TCP 连接 (发送 TCP RST 报文)，瞬间从 OS 层面终结连接以避让真机玩家"""
        self._running = False
        self.context.set_connected(False)
        if self._writer is not None:
            try:
                transport = self._writer.transport
                if transport is not None:
                    transport.abort()
            except Exception:
                pass
            self._writer = None

        if self._read_task is not None and not self._read_task.done():
            self._read_task.cancel()
            self._read_task = None

        for key, futures in self._pending_futures.items():
            for fut in futures:
                if not fut.done():
                    fut.set_exception(ConnectionResetError("TCP 连接已被底层强杀"))
        self._pending_futures.clear()
        self._frame_fsm.clear()
        logger.warning("TCP 长连接已被底层强杀 (transport.abort) 并瞬间重置状态")

    async def send_packet(self, packet: BasePacket) -> None:
        """向服务端发送单向指令封包 (不等待回复)

        Args:
            packet: 实现了 to_network_frame 的数据包实例。
        """
        if not self._running or self._writer is None:
            raise ConnectionError("当前未处于已连接状态，无法发送数据包")

        frame_bytes = packet.to_network_frame()
        self._writer.write(frame_bytes)
        await self._writer.drain()
        logger.debug("已发送网络帧 [Mod=%d, Act=%d], 长度=%d", packet.mod, packet.act, len(frame_bytes))

    async def request(
        self,
        packet: BasePacket,
        timeout_sec: float = 5.0,
        response_mod_act: Optional[Tuple[int, int]] = None,
    ) -> bytes:
        """串行管道化发送业务请求并等待对应回复载荷

        Args:
            packet: 待发送的数据包实例。
            timeout_sec: 等待应答超时秒数。
            response_mod_act: 期待的目标应答 (Mod, Act)，若未指定则默认与发送端相同。

        Returns:
            服务端回复的二进制 Payload 载荷字节。
        """
        target_key = response_mod_act or (packet.mod, packet.act)

        # 1. 串行命令锁防乱序
        async with self._request_lock:
            loop = asyncio.get_running_loop()
            fut: asyncio.Future[bytes] = loop.create_future()

            if target_key not in self._pending_futures:
                self._pending_futures[target_key] = []
            self._pending_futures[target_key].append(fut)

            # 2. 发送请求报文
            try:
                await self.send_packet(packet)
                # 3. 挂起等待结果
                return await asyncio.wait_for(fut, timeout=timeout_sec)
            except asyncio.TimeoutError:
                logger.warning("请求应答超时 [Mod=%d, Act=%d], 超时设定=%.1fs", target_key[0], target_key[1], timeout_sec)
                raise TimeoutError(f"等待响应超时: Mod={target_key[0]}, Act={target_key[1]}")
            finally:
                if target_key in self._pending_futures and fut in self._pending_futures[target_key]:
                    self._pending_futures[target_key].remove(fut)

    async def _read_loop(self) -> None:
        """底层异步持续收包循环"""
        while self._running and self._reader is not None:
            try:
                chunk = await self._reader.read(4096)
                if not chunk:
                    if self._running:
                        logger.warning("服务端主动断开 TCP 套接字通道 (EOF)")
                    else:
                        logger.debug("TCP 套接字读取通道已安全优雅结束 (EOF)")
                    break

                self._frame_fsm.feed(chunk)
                frames = self._frame_fsm.extract_frames()

                for payload, is_compressed in frames:
                    if len(payload) < 4:
                        continue

                    # 1. 解析首部 Mod 与 Act
                    mod, act = struct.unpack(">HH", payload[:4])
                    body_payload = payload[4:]

                    logger.debug("收到下行封包: Mod=%d, Act=%d (zlib=%s, 载荷=%d B)", mod, act, is_compressed, len(body_payload))

                    # 2. 状态上下文自动同步钩子
                    self._sync_context(mod, act, body_payload)

                    # 3. 优先匹配待决应答 Future
                    key = (mod, act)
                    if key in self._pending_futures and self._pending_futures[key]:
                        matched_fut = self._pending_futures[key].pop(0)
                        if not matched_fut.done():
                            matched_fut.set_result(body_payload)

                    # 4. 向事件总线派发广播
                    await self.event_bus.emit(mod, act, body_payload)

            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.error("收包循环捕获异常: %s", exc)
                break

        await self.disconnect()

    def _sync_context(self, mod: int, act: int, body: bytes) -> None:
        """网络下行包静默状态感知同步"""
        try:
            if mod == 0 and act == 0:
                resp = PlayerLoginResp.decode(body)
                if resp.is_success:
                    self.context.update_login_success(resp.player_id)
                    logger.info("收到登录成功应答，玩家ID=%d，已自动激活全局上下文 logged_in 状态", resp.player_id)
            elif mod == 0 and act == 2:
                resp = PlayerInfoResp.decode(body)
                self.context.update_player_info(
                    nickname=resp.nickname,
                    player_id=self.context.player.player_id,
                    level=resp.level,
                    coins=resp.coins,
                    ingots=resp.ingots,
                    power=resp.power,
                    fame=resp.fame,
                    vip_level=resp.vip_level,
                    town_id=resp.town_map_id,
                    mission_key=resp.mission_key,
                )
                logger.info(
                    "玩家基础属性已同步 (官方契约): 昵称='%s', 等级=%d, 铜钱=%d, 元宝=%d, 体力=%d, 城镇ID=%d",
                    resp.nickname,
                    resp.level,
                    resp.coins,
                    resp.ingots,
                    resp.power,
                    resp.town_map_id,
                )
            elif mod == 0 and act == 3:
                # 角色属性变更广播 (Mod_Player_Base.update_player_data)
                # 报文格式: [2B Count] + N * [1B PropID + 8B Value]
                if len(body) >= 2:
                    cnt = int.from_bytes(body[:2], "big")
                    if len(body) >= 2 + cnt * 9:
                        for i in range(cnt):
                            prop_id = body[2 + i * 9]
                            val = int.from_bytes(body[3 + i * 9 : 11 + i * 9], "big")
                            if prop_id == 18:
                                self.context.update_level(val)
                                logger.info("玩家等级更新: %d 级", val)
                            elif prop_id == 19:
                                old_ingots = self.context.player.ingots
                                diff = val - old_ingots
                                self.context.update_ingots(val)
                                if old_ingots > 0 and diff != 0:
                                    logger.info("玩家元宝更新: 当前总额 %d (变动 %+d)", val, diff)
                                else:
                                    logger.info("玩家元宝更新: 当前总额 %d", val)
                            elif prop_id == 20:
                                old_coins = self.context.player.coins
                                diff = val - old_coins
                                self.context.update_coins(val)
                                if old_coins > 0 and diff != 0:
                                    logger.info("玩家铜钱更新: 当前总额 %d (变动 %+d)", val, diff)
                                else:
                                    logger.info("玩家铜钱更新: 当前总额 %d", val)
                            elif prop_id in (23, 77):
                                old_power = self.context.player.power
                                diff = val - old_power
                                self.context.update_power(val)
                                if old_power >= 0 and diff != 0:
                                    logger.info("玩家体力更新: 当前剩余 %d 点 (变动 %+d)", val, diff)
                                else:
                                    logger.info("玩家体力更新: 当前剩余 %d 点", val)
                            elif prop_id == 37:
                                self.context.update_fame(val)
                            elif prop_id == 39:
                                self.context.update_vip(val)
        except Exception as exc:
            logger.warning("解析并同步状态上下文异常 [Mod=%d, Act=%d]: %s", mod, act, exc)
