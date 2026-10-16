"""神仙道多账号连接会话管理器与真机长连接托管引擎

负责集中调度各账号后台 TCP Socket 长连接池与心跳保活协程，
编排真实 35 项日常福利流水线，并在执行完毕后自动触发全景态势即查即存与实时刷报；
精准捕获服务端顶号与异地登录通知包，自动实施防互踢避让与冷却静默探测自愈。

@author Ateng
@since 2026-10-16
"""

import asyncio
import logging
import os
import time
from typing import Dict, Any, Optional, List, Callable

from core.context import GameContext
from core.config import AccountConfig
from core.events import EventBus
from network.client import SXDClient
from network.web_auth import WebAuthFetcher, GatewayCredentials
from protocol.builder import PacketBuilder
from services.query_service import QueryService
from storage.config_db import ConfigDatabase, AccountRecord
from storage.player_db import PlayerDatabase

from tasks.routine.login import LoginTask
from tasks.routine.heartbeat import HeartbeatTask
from tasks.routine.signin import DailySignInTask
from tasks.routine.money_tree import FreeMoneyTreeTask
from tasks.routine.online_gift import OnlineGiftTask
from tasks.routine.worship import FactionWorshipTask
from tasks.routine.faction_roll import FactionRollCakeTask
from tasks.routine.lucky_star import LuckyStarTask
from tasks.routine.farm import FarmTask
from tasks.routine.peach_pet import PeachAndPetTask
from tasks.routine.fate import FateHuntTask
from tasks.routine.take_bible import TakeBibleTask
from tasks.battle.hero_mission import HeroMissionSweepTask
from tasks.battle.normal_mission import NormalMissionSweepTask
from tasks.battle.multi_mission import MultiMissionTask
from tasks.battle.super_sport import SuperSportTask
from tasks.battle.world_boss import WorldBossTask
from tasks.routine.travel_event import TravelEventTask
from tasks.routine.item_clean import ItemCleanTask
from tasks.routine.traders import TradersTask
from tasks.routine.fishing import FishingTask
from tasks.battle.tower import TowerTask
from tasks.routine.email import EmailTask
from tasks.routine.ask_fairy import AskFairyTask
from tasks.routine.touch_stone import GoldenTouchStoneTask
from tasks.routine.weekend import WeekendRevelryTask
from tasks.routine.assistant import AssistantTask
from tasks.routine.practice import PracticeTask
from tasks.routine.hunt_demon import HuntDemonTask
from tasks.routine.five_elements import FiveElementsTask
from tasks.routine.five_fu import FiveFuTask
from tasks.routine.nimbus import NimbusTask
from tasks.routine.link_fate import LinkFateTask
from tasks.routine.home import HomeTask
from tasks.routine.union_worship import UnionWorshipTask
from tasks.routine.memory_zone import MemoryZoneTask

logger = logging.getLogger(__name__)

# 35 项日常与战斗自动化任务构造器映射字典
ROUTINE_TASK_BUILDERS: Dict[str, Callable[[], Any]] = {
    "signin": lambda: DailySignInTask(),
    "money_tree": lambda: FreeMoneyTreeTask(),
    "worship": lambda: FactionWorshipTask(),
    "faction_roll": lambda: FactionRollCakeTask(),
    "lucky_star": lambda: LuckyStarTask(),
    "farm": lambda: FarmTask(),
    "peach_pet": lambda: PeachAndPetTask(),
    "traders": lambda: TradersTask(),
    "fishing": lambda: FishingTask(),
    "fish": lambda: FishingTask(),
    "tower": lambda: TowerTask(),
    "six_paths_tower": lambda: TowerTask(),
    "fate": lambda: FateHuntTask(),
    "take_bible": lambda: TakeBibleTask(),
    "travel": lambda: TravelEventTask(),
    "travel_event": lambda: TravelEventTask(),
    "item_clean": lambda: ItemCleanTask(),
    "clean": lambda: ItemCleanTask(),
    "hero_mission": lambda: HeroMissionSweepTask(),
    "normal_mission": lambda: NormalMissionSweepTask(),
    "sweep": lambda: NormalMissionSweepTask(),
    "multi_mission": lambda: MultiMissionTask(),
    "seal_satan": lambda: MultiMissionTask(),
    "sport": lambda: SuperSportTask(),
    "super_sport": lambda: SuperSportTask(),
    "arena": lambda: SuperSportTask(),
    "boss": lambda: WorldBossTask(),
    "world_boss": lambda: WorldBossTask(),
    "online_gift": lambda: OnlineGiftTask(),
    "email": lambda: EmailTask(),
    "mail": lambda: EmailTask(),
    "ask_fairy": lambda: AskFairyTask(),
    "fairy": lambda: AskFairyTask(),
    "wen_ling": lambda: AskFairyTask(),
    "touch_stone": lambda: GoldenTouchStoneTask(),
    "stone": lambda: GoldenTouchStoneTask(),
    "weekend": lambda: WeekendRevelryTask(),
    "assistant": lambda: AssistantTask(is_post_routine=False),
    "practice": lambda: PracticeTask(),
    "hunt_demon": lambda: HuntDemonTask(),
    "demon": lambda: HuntDemonTask(),
    "five_elements": lambda: FiveElementsTask(),
    "five": lambda: FiveElementsTask(),
    "five_fu": lambda: FiveFuTask(),
    "fu": lambda: FiveFuTask(),
    "nimbus": lambda: NimbusTask(),
    "ling": lambda: NimbusTask(),
    "link_fate": lambda: LinkFateTask(),
    "fate_box": lambda: LinkFateTask(),
    "home": lambda: HomeTask(),
    "marry_home": lambda: HomeTask(),
    "union_worship": lambda: UnionWorshipTask(),
    "worship_union": lambda: UnionWorshipTask(),
    "memory_zone": lambda: MemoryZoneTask(),
    "memory": lambda: MemoryZoneTask(),
}


class AccountSessionManager:
    """账号长连接会话与防互踢避让状态机中心

    @author Ateng
    @since 2026-10-16
    """

    def __init__(
        self,
        db: ConfigDatabase,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        """初始化会话管理器

        Args:
            db: SQLite 配置仓储实例。
            event_bus: 全局事件总线（若未传入则默认实例化全局 EventBus）。
        """
        self.db = db
        self.event_bus = event_bus or EventBus()
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._silent_probes: Dict[str, float] = {}
        self._player_dbs: Dict[str, PlayerDatabase] = {}
        self._hosting_tasks: Dict[str, asyncio.Task] = {}
        self._account_locks: Dict[str, asyncio.Lock] = {}

    def _get_account_lock(self, alias: str) -> asyncio.Lock:
        """获取账号独占异步锁，避免并发网络发包冲突"""
        if alias not in self._account_locks:
            self._account_locks[alias] = asyncio.Lock()
        return self._account_locks[alias]

    def get_player_db(self, alias: str) -> Optional[PlayerDatabase]:
        """获取指定账号绑定的角色私有数据库实例

        Args:
            alias: 账号别名。

        Returns:
            PlayerDatabase 实体或 None。
        """
        if alias in self._player_dbs:
            return self._player_dbs[alias]

        acc = self.db.get_account(alias)
        if not acc:
            return None

        data_dir = "data"
        # 1. 若账号已记录确切的 player_id (> 0)，严格精准匹配
        if acc.player_id and acc.player_id > 0:
            target_file = f"storage_{acc.server_id}_{acc.player_id}.db"
            db_path = os.path.join(data_dir, target_file)
            pdb = PlayerDatabase(server_id=acc.server_id, player_id=acc.player_id, db_path=db_path)
            self._player_dbs[alias] = pdb
            return pdb

        # 2. 若尚未持久化 player_id，通过已知映射精准分配并持久化，坚决避开 _0.db 碰撞
        known_pid = 4 if alias in ("大号", "kongyu") else (5 if alias in ("小号", "kongling") else 0)
        if known_pid > 0:
            self.db.update_account_player_id(alias, known_pid)
            target_file = f"storage_{acc.server_id}_{known_pid}.db"
            db_path = os.path.join(data_dir, target_file)
            pdb = PlayerDatabase(server_id=acc.server_id, player_id=known_pid, db_path=db_path)
            self._player_dbs[alias] = pdb
            return pdb

        # 3. 兜底分配
        pdb = PlayerDatabase(server_id=acc.server_id, player_id=acc.server_id or 1001, base_dir=data_dir)
        self._player_dbs[alias] = pdb
        return pdb

    def set_player_db(self, alias: str, player_db: PlayerDatabase) -> None:
        """显式注入账号绑定的 PlayerDatabase 实例 (主要用于测试与多工作区调度)

        Args:
            alias: 账号别名。
            player_db: 角色私有数据库实例。
        """
        self._player_dbs[alias] = player_db

    def get_session_info(self, alias: str) -> Dict[str, Any]:
        """获取账号当前会话运行状态

        Args:
            alias: 账号别名。

        Returns:
            字典包含连接状态、避让状态与心跳时戳。
        """
        acc = self.db.get_account(alias)
        if not acc:
            return {
                "connection_status": "disconnected",
                "evade_state": "none",
                "evade_since": 0.0,
                "hosting_enabled": False,
                "last_heartbeat": 0.0,
            }

        session = self._sessions.get(alias, {})
        client = session.get("client")
        is_conn = client is not None and getattr(client.context, "is_connected", False)

        if acc.evade_state == "evading":
            conn_status = "disconnected"
        elif is_conn:
            conn_status = "connected"
        elif alias in self._hosting_tasks and not self._hosting_tasks[alias].done():
            conn_status = session.get("connection_status", "connecting")
        else:
            conn_status = "disconnected"

        evade_reason = session.get("evade_reason")
        if not evade_reason and acc.evade_state == "evading":
            evade_reason = "微端登录让位"
        evade_probe_at = session.get("evade_probe_at", 0.0)
        if not evade_probe_at and acc.evade_state == "evading":
            evade_probe_at = acc.evade_since + 3600.0

        return {
            "connection_status": conn_status,
            "evade_state": acc.evade_state,
            "evade_since": acc.evade_since,
            "evade_reason": evade_reason or "",
            "evade_probe_at": evade_probe_at,
            "hosting_enabled": acc.hosting_enabled,
            "last_heartbeat": session.get("last_heartbeat", 0.0),
        }

    def get_client(self, alias: str) -> Optional[SXDClient]:
        """获取账号当前活跃的长连接客户端实例"""
        return self._sessions.get(alias, {}).get("client")

    def get_context(self, alias: str) -> Optional[GameContext]:
        """获取账号当前活跃的运行时上下文实例"""
        return self._sessions.get(alias, {}).get("context")

    async def clean_inventory(
        self,
        alias: str,
        target_empty: int = 5,
        force_all: bool = True,
    ) -> Dict[str, Any]:
        """异步执行指定账号的四阶背包自理流水线

        Args:
            alias: 账号别名。
            target_empty: 目标预留空格数量。
            force_all: 是否强制四阶深度全清。

        Returns:
            执行结果字典。
        """
        lock = self._get_account_lock(alias)
        async with lock:
            session = self._sessions.get(alias, {})
            client = session.get("client")
            ctx = session.get("context")
            if not client or not ctx or not ctx.is_connected:
                return {"success": False, "message": f"账号 '{alias}' 当前未处于有效在线托管连接状态，无法操作背包"}

            from tasks.routine.item_clean import ItemCleanTask
            task = ItemCleanTask(target_empty=target_empty, force_all=force_all)
            res = await task.execute(client, ctx)

            # 触发最新态势感知
            pdb = self.get_player_db(alias)
            if pdb:
                try:
                    query_srv = QueryService(client=client, context=ctx, player_db=pdb)
                    await query_srv.query_all(timeout_sec=3.0)
                    self.event_bus.publish(
                        "telemetry_updated",
                        {"type": "telemetry_updated", "alias": alias, "timestamp": time.time()},
                    )
                except Exception as q_exc:
                    logger.debug("清包后态势刷新异常: %s", q_exc)

            return {
                "success": res.is_success,
                "alias": alias,
                "message": res.message,
                "data": res.data or {},
            }

    async def use_all_inventory(self, alias: str) -> Dict[str, Any]:
        """批量打开或使用指定账号背包内的所有宝箱、丹药与可用消耗品 (不存仓、不丢弃)

        Args:
            alias: 账号别名。

        Returns:
            执行结果字典。
        """
        lock = self._get_account_lock(alias)
        async with lock:
            session = self._sessions.get(alias, {})
            client = session.get("client")
            ctx = session.get("context")
            if not client or not ctx or not ctx.is_connected:
                return {"success": False, "message": f"账号 '{alias}' 当前未处于有效在线托管连接状态，无法操作背包"}

            from tasks.routine.item_clean import ItemCleanTask
            task = ItemCleanTask(target_empty=100, force_all=True, use_only=True)
            res = await task.execute(client, ctx)

            # 触发最新态势感知
            pdb = self.get_player_db(alias)
            if pdb:
                try:
                    query_srv = QueryService(client=client, context=ctx, player_db=pdb)
                    await query_srv.query_all(timeout_sec=3.0)
                    self.event_bus.publish(
                        "telemetry_updated",
                        {"type": "telemetry_updated", "alias": alias, "timestamp": time.time()},
                    )
                except Exception as q_exc:
                    logger.debug("使用道具后态势刷新异常: %s", q_exc)

            return {
                "success": res.is_success,
                "alias": alias,
                "message": res.message,
                "data": res.data or {},
            }

    def start_hosting(self, alias: str) -> bool:
        """为指定账号开启真实长连接托管与心跳保活

        Args:
            alias: 账号别名。

        Returns:
            是否成功开启托管。
        """
        acc = self.db.get_account(alias)
        if not acc or not acc.enabled:
            return False

        self.db.set_hosting_state(alias, True)
        if alias not in self._sessions:
            self._sessions[alias] = {}
        self._sessions[alias]["connection_status"] = "connecting"
        self._sessions[alias]["hosting_enabled"] = True
        self._sessions[alias]["last_heartbeat"] = time.time()

        # 取消已有的工作协程
        if alias in self._hosting_tasks and not self._hosting_tasks[alias].done():
            self._hosting_tasks[alias].cancel()

        # 启动后台真实常驻长连接守护协程
        try:
            loop = asyncio.get_running_loop()
            task = loop.create_task(self._hosting_worker(alias))
            self._hosting_tasks[alias] = task
        except RuntimeError:
            pass

        self.event_bus.publish(
            "HOSTING_STARTED",
            {"alias": alias, "timestamp": time.time()},
        )
        self.event_bus.publish(
            "ACCOUNT_CONNECTING",
            {"type": "ACCOUNT_CONNECTING", "alias": alias, "timestamp": time.time()},
        )
        logger.info("[%s] 长连接托管已启动 (正在连入游戏网关...)", alias)
        return True

    def start_all_hosting(self) -> int:
        """为所有启用托管且处于激活状态的账号拉起长连接常驻守护协程

        Returns:
            成功拉起托管的账号数量。
        """
        count = 0
        accounts = self.db.list_accounts()
        for acc in accounts:
            if acc.enabled and acc.hosting_enabled:
                if self.start_hosting(acc.alias):
                    count += 1
        logger.info("全员长连接常驻守护就绪，共拉起 %d 个账号的自主托管协程", count)
        return count

    def stop_hosting(self, alias: str) -> bool:
        """主动暂停/停止指定账号的长连接托管

        Args:
            alias: 账号别名。

        Returns:
            是否成功停止托管。
        """
        self.db.set_hosting_state(alias, False)
        if alias in self._sessions:
            self._sessions[alias]["connection_status"] = "disconnected"
            self._sessions[alias]["hosting_enabled"] = False
            active_client = self._sessions[alias].pop("client", None)
            if active_client:
                try:
                    active_client.abort()
                except Exception:
                    pass

        if alias in self._hosting_tasks and not self._hosting_tasks[alias].done():
            self._hosting_tasks[alias].cancel()

        self.event_bus.publish(
            "HOSTING_STOPPED",
            {"alias": alias, "timestamp": time.time()},
        )
        self.event_bus.publish(
            "ACCOUNT_DISCONNECTED",
            {"type": "ACCOUNT_DISCONNECTED", "alias": alias, "timestamp": time.time()},
        )
        logger.info("[%s] 长连接托管已停止", alias)
        return True

    async def _run_patrol_internal(self, alias: str) -> None:
        """常驻周期自愈巡检：药园收种、点金助友、防体力溢出扫荡与全景态势即查即存"""
        lock = self._get_account_lock(alias)
        async with lock:
            session = self._sessions.get(alias, {})
            client = session.get("client")
            ctx = session.get("context")
            if not (client and client.context.is_connected and ctx):
                return
            try:
                # 1. 仙府药园收获与补种
                from tasks.routine.farm import FarmTask
                await FarmTask().execute(client, ctx)
                # 2. 点金助友
                from tasks.routine.touch_stone import GoldenTouchStoneTask
                await GoldenTouchStoneTask().execute(client, ctx)
                # 3. 体力防溢出自动扫荡 (若当前体力 >= 5 则消耗体力)
                if ctx.player.power >= 5:
                    from tasks.battle.normal_mission import NormalMissionSweepTask
                    await NormalMissionSweepTask().execute(client, ctx)
                # 4. 小助手活跃度领奖
                from tasks.routine.assistant import AssistantTask
                await AssistantTask().execute(client, ctx)
                # 5. 全景态势即查即存与推流
                pdb = self.get_player_db(alias)
                if pdb:
                    query_srv = QueryService(client=client, context=ctx, player_db=pdb)
                    await query_srv.query_all(timeout_sec=3.0)
                    self.event_bus.publish(
                        "telemetry_updated",
                        {"type": "telemetry_updated", "alias": alias, "timestamp": time.time()},
                    )
            except Exception as e:
                logger.warning("[%s] 周期自愈巡检非致命异常: %s", alias, e)

    async def _safe_trigger_routine_async(self, alias: str) -> None:
        """异步下发日常流水线调度 (供跨天自动清盘调用)"""
        try:
            self.trigger_routine(alias)
        except Exception as e:
            logger.error("[%s] 跨天流水线自主调度异常: %s", alias, e)

    async def _hosting_worker(self, alias: str) -> None:
        """后台常驻 Socket 长连接保活、分层双轨自愈巡检与协议通知监听协程"""
        logger.info("[%s] 长连接常驻自愈守护协程已启动", alias)
        lock = self._get_account_lock(alias)
        backoff_idx = 0
        backoff_intervals = [5.0, 15.0, 30.0, 60.0]
        last_patrol_time = time.time()
        last_routine_day = time.strftime("%Y-%m-%d", time.localtime())

        while True:
            try:
                acc = self.db.get_account(alias)
                if not acc or not acc.hosting_enabled or not acc.enabled:
                    logger.info("[%s] 托管状态未启用或账号禁用，常驻协程退出", alias)
                    break

                if acc.evade_state == "evading":
                    self._sessions.setdefault(alias, {})["connection_status"] = "disconnected"
                    await asyncio.sleep(5.0)
                    self.check_silent_probes()
                    continue

                account_cfg = AccountConfig(
                    alias=acc.alias,
                    username=acc.username,
                    password=acc.password,
                    server=acc.server,
                    server_id=acc.server_id,
                    server_host=acc.server_host,
                    server_port=acc.server_port,
                    enabled=acc.enabled,
                    platform=acc.platform,
                )

                creds = WebAuthFetcher.resolve_credentials(account_cfg)
                if not creds:
                    delay = backoff_intervals[min(backoff_idx, len(backoff_intervals) - 1)]
                    backoff_idx += 1
                    logger.warning("[%s] 无法解析网关认证凭据，退避 %.1f 秒后重试...", alias, delay)
                    self._sessions.setdefault(alias, {})["connection_status"] = "disconnected"
                    await asyncio.sleep(delay)
                    continue

                ctx = GameContext()
                client = SXDClient(context=ctx, event_bus=self.event_bus)
                self._sessions.setdefault(alias, {})["client"] = client

                # 挂载顶号协议监听 (Mod 100 Act 22 或 Mod 0 Act 15)
                async def _on_packet(mod: int, act: int, payload: bytes) -> None:
                    self.handle_protocol_notification(alias, mod, act)

                self.event_bus.subscribe_all(_on_packet)

                connected = await client.connect(creds.server_host, creds.server_port, timeout_sec=8.0)
                if not connected:
                    delay = backoff_intervals[min(backoff_idx, len(backoff_intervals) - 1)]
                    backoff_idx += 1
                    logger.warning("[%s] 连接网关 %s:%d 失败，退避 %.1f 秒后重试...", alias, creds.server_host, creds.server_port, delay)
                    self._sessions.setdefault(alias, {})["connection_status"] = "disconnected"
                    self.event_bus.publish(
                        "ACCOUNT_DISCONNECTED",
                        {"type": "ACCOUNT_DISCONNECTED", "alias": alias, "timestamp": time.time()},
                    )
                    await asyncio.sleep(delay)
                    continue

                # 登录握手
                login_task = LoginTask(creds)
                login_res = await login_task.execute(client, ctx)
                if not login_res.is_success:
                    delay = backoff_intervals[min(backoff_idx, len(backoff_intervals) - 1)]
                    backoff_idx += 1
                    logger.warning("[%s] 托管登录认证失败: %s，退避 %.1f 秒后重试...", alias, login_res.message, delay)
                    self._sessions.setdefault(alias, {})["connection_status"] = "disconnected"
                    self.event_bus.publish(
                        "ACCOUNT_DISCONNECTED",
                        {"type": "ACCOUNT_DISCONNECTED", "alias": alias, "timestamp": time.time()},
                    )
                    await client.disconnect()
                    await asyncio.sleep(delay)
                    continue

                # 成功连入，重置退避
                backoff_idx = 0

                # 登记会话
                self._sessions.setdefault(alias, {})
                self._sessions[alias]["connection_status"] = "connected"
                self._sessions[alias]["client"] = client
                self._sessions[alias]["context"] = ctx
                self._sessions[alias]["last_heartbeat"] = time.time()
                self._sessions[alias]["hosting_enabled"] = True

                # 广播 SSE 实时连接就绪通知
                self.event_bus.publish(
                    "ACCOUNT_CONNECTED",
                    {
                        "type": "ACCOUNT_CONNECTED",
                        "alias": alias,
                        "player_id": ctx.player.player_id,
                        "nickname": ctx.player.nickname,
                        "level": ctx.player.level,
                        "timestamp": time.time(),
                    },
                )

                # 持久化真实角色 player_id 并精准初始化私有数据库
                if ctx.player.player_id > 0:
                    self.db.update_account_player_id(alias, ctx.player.player_id)
                pdb = PlayerDatabase(server_id=creds.server_id, player_id=ctx.player.player_id, base_dir="data")
                self.set_player_db(alias, pdb)

                try:
                    query_srv = QueryService(client=client, context=ctx, player_db=pdb)
                    await query_srv.query_all(timeout_sec=3.0)
                    self.event_bus.publish(
                        "telemetry_updated",
                        {"type": "telemetry_updated", "alias": alias, "timestamp": time.time()},
                    )
                except Exception as q_exc:
                    logger.warning("[%s] 托管初次态势感知同步异常 (非致命): %s", alias, q_exc)

                logger.info("[%s] 长连接常驻托管就绪，角色: %s (Lv.%d)", alias, ctx.player.nickname, ctx.player.level)

                # 分层双轨守护主循环：心跳保活 + 周期自愈巡检 + 跨天清盘
                heartbeat_pkt = PacketBuilder(mod=0, act=1).build()
                while client.context.is_connected:
                    acc_cur = self.db.get_account(alias)
                    if not acc_cur or not acc_cur.hosting_enabled or acc_cur.evade_state == "evading":
                        break

                    now = time.time()
                    # 1. 高频保活轨：发送心跳
                    async with lock:
                        try:
                            await client.send_packet(heartbeat_pkt)
                            self._sessions[alias]["last_heartbeat"] = now
                        except Exception as hb_exc:
                            logger.warning("[%s] 心跳包发送失败: %s", alias, hb_exc)
                            break

                    # 2. 跨天清盘轨：每日 00:05 跨天自动触发全套 35 项日常福利
                    curr_day = time.strftime("%Y-%m-%d", time.localtime(now))
                    curr_hm = time.strftime("%H:%M", time.localtime(now))
                    if curr_day != last_routine_day and curr_hm >= "00:05":
                        logger.info("[%s] 检测到自然日跨天 (%s)，自动触发全员全量日常福利清盘流水线...", alias, curr_day)
                        last_routine_day = curr_day
                        try:
                            loop = asyncio.get_running_loop()
                            loop.create_task(self._safe_trigger_routine_async(alias))
                        except Exception as tr_err:
                            logger.warning("[%s] 跨天流水线启动异常: %s", alias, tr_err)

                    # 3. 中频巡检轨：默认每 3 分钟 (180 秒) 自动巡检药园/助友/防体力溢出/全景态势同步
                    elif now - last_patrol_time >= 180.0:
                        last_patrol_time = now
                        logger.info("[%s] 触发常驻周期巡检 (药园收获补种 / 帮派助友 / 防体力溢出 / 全景态势同步)...", alias)
                        try:
                            loop = asyncio.get_running_loop()
                            loop.create_task(self._run_patrol_internal(alias))
                        except Exception as pt_err:
                            logger.warning("[%s] 周期巡检启动异常: %s", alias, pt_err)

                    await asyncio.sleep(15.0)
                    self.check_silent_probes()

                self._sessions[alias]["connection_status"] = "disconnected"
                self._sessions[alias].pop("client", None)
                await client.disconnect()
                self.event_bus.publish(
                    "ACCOUNT_DISCONNECTED",
                    {"type": "ACCOUNT_DISCONNECTED", "alias": alias, "timestamp": time.time()},
                )

                # 4. 零容忍服从避让：非避让模式下的异常断开 (收到服务端 EOF/Reset)，坚决不自动重连抢线，立即触发防互踢避让
                acc_now = self.db.get_account(alias)
                if acc_now and acc_now.hosting_enabled and acc_now.enabled and acc_now.evade_state != "evading":
                    logger.warning(
                        "[%s] 托管长连接非正常断开 (收到服务端 EOF/Reset)，零容忍立即触发防互踢避让以保护微端玩家！",
                        alias,
                    )
                    self.trigger_evade(alias, reason="微端登录让位 (EOF断开)", probe_delay_sec=3600.0)
                    continue

            except asyncio.CancelledError:
                logger.info("[%s] 托管工作协程安全取消", alias)
                active_client = self._sessions.get(alias, {}).pop("client", None)
                if active_client:
                    try:
                        active_client.abort()
                    except Exception:
                        pass
                break
            except Exception as exc:
                logger.error("[%s] 托管工作协程异常: %s", alias, exc, exc_info=True)
                self._sessions.setdefault(alias, {})["connection_status"] = "disconnected"
                await asyncio.sleep(10.0)

    def trigger_evade(
        self,
        alias: str,
        reason: str = "duplicate_login",
        probe_delay_sec: float = 3600.0,
    ) -> None:
        """捕获到玩家自登或顶号包，触发防互踢避让 (底层强杀连接以瞬间让位)

        Args:
            alias: 账号别名。
            reason: 触发原因描述。
            probe_delay_sec: 静默探测冷却时长 (秒)。
        """
        now = time.time()
        # 0. 避让联动关停长连接托管开关，保证界面行为与物理状态严格一致
        self.db.set_hosting_state(alias, False)
        self.db.set_evade_state(alias, evade_state="evading", evade_since=now)

        if alias not in self._sessions:
            self._sessions[alias] = {}
        self._sessions[alias]["hosting_enabled"] = False
        self._sessions[alias]["connection_status"] = "disconnected"
        self._sessions[alias]["evade_reason"] = reason
        self._sessions[alias]["evade_probe_at"] = now + probe_delay_sec

        # 1. 若存在活跃 client，底层通过 transport.abort() 瞬间强杀以释放网关会话
        active_client = self._sessions[alias].pop("client", None)
        if active_client:
            try:
                active_client.abort()
            except Exception as e:
                logger.warning("[%s] 强杀活跃连接异常: %s", alias, e)

        # 2. 立即取消当前常驻守护协程，杜绝后台重试与抢线
        if alias in self._hosting_tasks and not self._hosting_tasks[alias].done():
            self._hosting_tasks[alias].cancel()
            self._hosting_tasks.pop(alias, None)

        # 调度静默探测
        self._silent_probes[alias] = now + probe_delay_sec

        self.event_bus.publish(
            "ACCOUNT_EVADED",
            {
                "type": "ACCOUNT_EVADED",
                "alias": alias,
                "reason": reason,
                "timestamp": now,
                "probe_delay_sec": probe_delay_sec,
            },
        )
        self.event_bus.publish(
            "ACCOUNT_DISCONNECTED",
            {
                "type": "ACCOUNT_DISCONNECTED",
                "alias": alias,
                "timestamp": now,
            },
        )
        self.event_bus.publish(
            "evade_alert",
            {
                "type": "evade_alert",
                "alias": alias,
                "reason": f"触发防互踢避让 (原因: {reason})，长连接已主动断开让位！",
                "timestamp": now,
            },
        )
        logger.warning(
            "[%s] 触发防互踢避让 (原因: %s)，已联动关闭长连接托管！静默探测将于 %.1fs 后就绪",
            alias,
            reason,
            probe_delay_sec,
        )

    def resume_hosting(self, alias: str) -> bool:
        """玩家手动点击【打完了·恢复托管】或静默探测确认离线后自愈恢复

        Args:
            alias: 账号别名。

        Returns:
            是否成功恢复托管。
        """
        acc = self.db.get_account(alias)
        if not acc:
            return False

        # 1. 强制设为开启托管并重置避让状态
        self.db.set_hosting_state(alias, True)
        self.db.set_evade_state(alias, evade_state="none", evade_since=0.0)
        self._silent_probes.pop(alias, None)

        self._sessions.setdefault(alias, {})
        self._sessions[alias]["hosting_enabled"] = True
        self._sessions[alias]["connection_status"] = "connecting"
        self._sessions[alias]["evade_state"] = "none"

        # 2. 重新建立长连接托管
        if acc.enabled:
            self.start_hosting(alias)

        self.event_bus.publish(
            "ACCOUNT_CONNECTING",
            {"type": "ACCOUNT_CONNECTING", "alias": alias, "timestamp": time.time()},
        )
        self.event_bus.publish(
            "ACCOUNT_RESUMED",
            {"type": "ACCOUNT_RESUMED", "alias": alias, "timestamp": time.time()},
        )
        logger.info("[%s] 避让状态已解除，已成功恢复在线托管 (正在握手)...", alias)
        return True

    def evade_all(self, reason: str = "用户手动全员避让", probe_delay_sec: float = 3600.0) -> int:
        """一键全员防互踢避让 (强制断开全部在线长连接)

        Args:
            reason: 避让原因描述。
            probe_delay_sec: 静默探测冷却时长 (秒)。

        Returns:
            成功触发避让的账号数量。
        """
        count = 0
        accounts = self.db.list_accounts()
        for acc in accounts:
            if acc.enabled:
                self.trigger_evade(acc.alias, reason=reason, probe_delay_sec=probe_delay_sec)
                count += 1
        logger.info("已完成全员防互踢避让操作，共计避让 %d 个账号", count)
        return count

    def resume_all(self) -> int:
        """一键全员退出避让并恢复在线托管 (全员强制拉起)

        Returns:
            成功恢复在线托管的账号数量。
        """
        count = 0
        accounts = self.db.list_accounts()
        for acc in accounts:
            if acc.enabled:
                if self.resume_hosting(acc.alias):
                    count += 1
        logger.info("已完成全员避让恢复操作，共计恢复 %d 个账号", count)
        return count

    def check_silent_probes(self) -> List[str]:
        """轮询并执行到达冷却时间的静默探测自愈

        Returns:
            自愈恢复托管的账号别名列表。
        """
        now = time.time()
        resumed: List[str] = []
        due_aliases = [
            alias
            for alias, due_time in list(self._silent_probes.items())
            if now >= due_time
        ]

        for alias in due_aliases:
            logger.info("[%s] 静默探测冷却已满，正在探测玩家游戏会话...", alias)
            self.resume_hosting(alias)
            resumed.append(alias)

        return resumed

    def handle_protocol_notification(
        self,
        alias: str,
        module_id: int,
        action_id: int,
    ) -> bool:
        """协议包监听钩子，自动识别异地登录包 (Mod 100 Act 22 或 Mod 0 Act 15)

        Args:
            alias: 账号别名。
            module_id: 协议模块编号。
            action_id: 协议动作编号。

        Returns:
            若为顶号通知并触发了避让则返回 True，否则返回 False。
        """
        if (module_id == 100 and action_id == 22) or (module_id == 0 and action_id == 15):
            self.trigger_evade(
                alias,
                reason=f"Mod {module_id} Act {action_id} (another_login_notify)",
            )
            return True
        return False

    def trigger_routine(
        self,
        alias: str,
        specific_task: Optional[str] = None,
        force: bool = False,
    ) -> Dict[str, Any]:
        """异步触发账号日常福利任务流水线 (真正网络 Socket 驱动与即查即存)

        Args:
            alias: 账号别名。
            specific_task: 可选指定单项日常任务（如 "money_tree"），若为空则执行全部已启用任务。
            force: 是否在避让状态下强制触发。

        Returns:
            任务调度结果字典，包含 task_id 与状态。
        """
        acc = self.db.get_account(alias)
        if not acc:
            return {"success": False, "status": "not_found", "alias": alias}

        # 避让状态安全防护
        if acc.evade_state == "evading" and not force:
            logger.warning(
                "[%s] 账号正处于防互踢避让状态，拦截日常流水线触发以防顶号冲突",
                alias,
            )
            self.event_bus.publish(
                "evade_alert",
                {
                    "type": "evade_alert",
                    "alias": alias,
                    "reason": "账号正处于防互踢避让保护中，已拦截常规日常执行。如需强制执行请恢复托管或指定 force=True",
                    "timestamp": time.time(),
                },
            )
            return {
                "success": False,
                "status": "evading_blocked",
                "alias": alias,
                "message": "账号正处于避让状态，已拦截执行",
            }

        cfg = self.db.get_routine_config(alias)
        if specific_task:
            routines = [specific_task]
        else:
            # 过滤掉非独立单次日常任务 (login 与 heartbeat 属于会话底层机制)
            routines = [r for r in cfg.enabled_routines if r not in ("login", "heartbeat")]

        task_id = f"routine_{alias}_{int(time.time() * 1000)}"

        # 发布任务启动事件
        self.event_bus.publish(
            "routine_step",
            {
                "type": "routine_step",
                "alias": alias,
                "task_id": task_id,
                "step": "start",
                "status": "running",
                "message": f"日常福利流水线已启动，计划执行 {len(routines)} 项子任务",
                "routines": routines,
                "timestamp": time.time(),
            },
        )

        async def _run_pipeline() -> None:
            lock = self._get_account_lock(alias)
            async with lock:
                temp_client = False
                client: Optional[SXDClient] = None
                ctx: Optional[GameContext] = None

                try:
                    # 1. 优先复用当前活跃托管长连接；若无则创建临时无头连接
                    session = self._sessions.get(alias, {})
                    active_client = session.get("client")
                    active_ctx = session.get("context")

                    if active_client and active_client.context.is_connected and active_ctx:
                        client = active_client
                        ctx = active_ctx
                        logger.info("[%s] 复用当前活跃的托管 Socket 长连接执行日常流水线", alias)
                    else:
                        temp_client = True
                        account_cfg = AccountConfig(
                            alias=acc.alias,
                            username=acc.username,
                            password=acc.password,
                            server=acc.server,
                            server_id=acc.server_id,
                            server_host=acc.server_host,
                            server_port=acc.server_port,
                            enabled=acc.enabled,
                            platform=acc.platform,
                        )
                        creds = WebAuthFetcher.resolve_credentials(account_cfg)
                        if not creds:
                            self.event_bus.publish(
                                "routine_step",
                                {
                                    "type": "routine_step",
                                    "alias": alias,
                                    "task_id": task_id,
                                    "step": "auth",
                                    "status": "failed",
                                    "message": "无法解析账号凭据或缺少关键认证信息，终止执行",
                                    "timestamp": time.time(),
                                },
                            )
                            return

                        ctx = GameContext()
                        client = SXDClient(context=ctx, event_bus=self.event_bus)

                        self.event_bus.publish(
                            "routine_step",
                            {
                                "type": "routine_step",
                                "alias": alias,
                                "task_id": task_id,
                                "step": "connect",
                                "status": "running",
                                "message": f"正在建立与游戏网关的连接 ({creds.server_host}:{creds.server_port})...",
                                "timestamp": time.time(),
                            },
                        )

                        connected = await client.connect(creds.server_host, creds.server_port, timeout_sec=8.0)
                        if not connected:
                            self.event_bus.publish(
                                "routine_step",
                                {
                                    "type": "routine_step",
                                    "alias": alias,
                                    "task_id": task_id,
                                    "step": "connect",
                                    "status": "failed",
                                    "message": f"无法建立与游戏网关的连接 ({creds.server_host}:{creds.server_port})",
                                    "timestamp": time.time(),
                                },
                            )
                            return

                        login_task = LoginTask(creds)
                        login_res = await login_task.execute(client, ctx)
                        if not login_res.is_success:
                            self.event_bus.publish(
                                "routine_step",
                                {
                                    "type": "routine_step",
                                    "alias": alias,
                                    "task_id": task_id,
                                    "step": "login",
                                    "status": "failed",
                                    "message": f"游戏登录认证失败: {login_res.message}",
                                    "timestamp": time.time(),
                                },
                            )
                            await client.disconnect()
                            return

                        # 持久化真实角色 player_id 并精准初始化私有数据库
                        if ctx.player.player_id > 0:
                            self.db.update_account_player_id(alias, ctx.player.player_id)
                        pdb = PlayerDatabase(server_id=creds.server_id, player_id=ctx.player.player_id, base_dir="data")
                        self.set_player_db(alias, pdb)

                    # 2. 依次调度执行各子任务
                    for r in routines:
                        # 断网级联熔断保护：若底层 Socket 已断开，立即紧急终止后续调度
                        if not (client and client.context.is_connected):
                            logger.warning("[%s] 底层网络连接已中断，紧急熔断终止后续日常调度 (中断于任务: %s)", alias, r)
                            self.event_bus.publish(
                                "routine_step",
                                {
                                    "type": "routine_step",
                                    "alias": alias,
                                    "task_id": task_id,
                                    "step": r,
                                    "status": "failed",
                                    "message": f"底层网络连接中断，触发熔断保护，终止后续日常调度",
                                    "timestamp": time.time(),
                                },
                            )
                            break

                        self.event_bus.publish(
                            "routine_step",
                            {
                                "type": "routine_step",
                                "alias": alias,
                                "task_id": task_id,
                                "step": r,
                                "status": "running",
                                "message": f"开始执行日常子任务: {r}",
                                "timestamp": time.time(),
                            },
                        )

                        builder = ROUTINE_TASK_BUILDERS.get(r)
                        if builder:
                            task_instance = builder()
                            res = await task_instance.execute(client, ctx)
                            step_status = "success" if res.is_success else "failed"
                            step_msg = f"子任务 [{r}] 执行{'成功' if res.is_success else '未完成'}: {res.message or '完成'}"
                            self.event_bus.publish(
                                "routine_step",
                                {
                                    "type": "routine_step",
                                    "alias": alias,
                                    "task_id": task_id,
                                    "step": r,
                                    "status": step_status,
                                    "message": step_msg,
                                    "timestamp": time.time(),
                                },
                            )
                        else:
                            self.event_bus.publish(
                                "routine_step",
                                {
                                    "type": "routine_step",
                                    "alias": alias,
                                    "task_id": task_id,
                                    "step": r,
                                    "status": "success",
                                    "message": f"子任务 [{r}] 暂无额外动作，跳过",
                                    "timestamp": time.time(),
                                },
                            )

                        await asyncio.sleep(0.3)

                    # 3. 日常收官：全景态势即查即存与实时刷报
                    self.event_bus.publish(
                        "routine_step",
                        {
                            "type": "routine_step",
                            "alias": alias,
                            "task_id": task_id,
                            "step": "sync",
                            "status": "running",
                            "message": "日常福利流水线已执行完毕，正在同步全景资产与角色态势...",
                            "timestamp": time.time(),
                        },
                    )

                    player_db = self.get_player_db(alias)
                    if player_db and client and client.context.is_connected and ctx:
                        try:
                            query_srv = QueryService(client=client, context=ctx, player_db=player_db)
                            await query_srv.query_all(timeout_sec=3.0)
                            self.event_bus.publish(
                                "telemetry_updated",
                                {
                                    "type": "telemetry_updated",
                                    "alias": alias,
                                    "timestamp": time.time(),
                                },
                            )
                        except Exception as q_exc:
                            logger.warning("[%s] 态势感知同步发生异常: %s", alias, q_exc)

                    self.event_bus.publish(
                        "routine_step",
                        {
                            "type": "routine_step",
                            "alias": alias,
                            "task_id": task_id,
                            "step": "complete",
                            "status": "completed",
                            "message": f"日常福利流水线全部执行完成 (共 {len(routines)} 项)，最新资产与态势已实时存盘！",
                            "timestamp": time.time(),
                        },
                    )
                    logger.info("[%s] [TaskScheduler] 日常福利流水线真实异步执行完成 (共 %d 项)", alias, len(routines))

                except Exception as exc:
                    self.event_bus.publish(
                        "routine_step",
                        {
                            "type": "routine_step",
                            "alias": alias,
                            "task_id": task_id,
                            "step": "error",
                            "status": "failed",
                            "message": f"日常流水线执行异常: {exc}",
                            "timestamp": time.time(),
                        },
                    )
                    logger.error("[%s] 日常流水线异步执行发生异常: %s", alias, exc, exc_info=True)
                finally:
                    if temp_client and client:
                        await client.disconnect()

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(_run_pipeline())
        except RuntimeError:
            pass

        return {
            "success": True,
            "status": "dispatched",
            "alias": alias,
            "task_id": task_id,
            "routines_count": len(routines),
        }

    async def sync_telemetry(self, alias: str) -> Dict[str, Any]:
        """按需触发指定账号的全景资产态势即查即存并推流通知

        Args:
            alias: 账号别名。

        Returns:
            同步执行结果字典。
        """
        acc = self.db.get_account(alias)
        if not acc:
            return {"success": False, "message": f"账号 '{alias}' 不存在"}

        lock = self._get_account_lock(alias)
        async with lock:
            session = self._sessions.get(alias, {})
            client = session.get("client")
            ctx = session.get("context")
            temp_client = False

            try:
                if not (client and client.context.is_connected and ctx):
                    temp_client = True
                    account_cfg = AccountConfig(
                        alias=acc.alias,
                        username=acc.username,
                        password=acc.password,
                        server=acc.server,
                        server_id=acc.server_id,
                        server_host=acc.server_host,
                        server_port=acc.server_port,
                        enabled=acc.enabled,
                        platform=acc.platform,
                    )
                    creds = WebAuthFetcher.resolve_credentials(account_cfg)
                    if not creds:
                        return {"success": False, "message": "无法解析账号凭据或缺少关键认证信息"}

                    ctx = GameContext()
                    client = SXDClient(context=ctx, event_bus=self.event_bus)
                    connected = await client.connect(creds.server_host, creds.server_port, timeout_sec=8.0)
                    if not connected:
                        return {"success": False, "message": "无法连接游戏网关"}

                    login_task = LoginTask(creds)
                    login_res = await login_task.execute(client, ctx)
                    if not login_res.is_success:
                        await client.disconnect()
                        return {"success": False, "message": f"登录失败: {login_res.message}"}

                if ctx.player.player_id > 0:
                    self.db.update_account_player_id(alias, ctx.player.player_id)
                pdb = PlayerDatabase(server_id=acc.server_id, player_id=ctx.player.player_id, base_dir="data")
                self.set_player_db(alias, pdb)

                query_srv = QueryService(client=client, context=ctx, player_db=pdb)
                await query_srv.query_all(timeout_sec=3.0)

                self.event_bus.publish(
                    "telemetry_updated",
                    {"type": "telemetry_updated", "alias": alias, "timestamp": time.time()},
                )
                return {
                    "success": True,
                    "alias": alias,
                    "message": "全景资产态势同步完成，最新数据已入库！",
                    "player_id": ctx.player.player_id,
                    "nickname": ctx.player.nickname,
                    "coins": ctx.player.coins,
                    "ingots": ctx.player.ingots,
                    "power": ctx.player.power,
                }
            except Exception as e:
                logger.error("[%s] 态势感知同步异常: %s", alias, e)
                return {"success": False, "message": str(e)}
            finally:
                if temp_client and client:
                    await client.disconnect()

