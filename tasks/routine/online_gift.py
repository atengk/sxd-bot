"""神仙道在线时长礼包、微端礼包与每日俸禄领取任务 (Mod 0)

自动查询并领取当前可领取的在线时长累积礼包、微端专享礼包与每日阵营俸禄。严格遵守零元宝消耗安全原则。

@author Ateng
@since 2026-10-15
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)


class OnlineGiftTask(BaseTask):
    """在线时长礼包、微端礼包与阵营俸禄任务

    @author Ateng
    @since 2026-10-15
    """

    name = "OnlineGiftTask"
    interval_sec = 0.0  # 单次执行

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行在线时长礼包、微端礼包与每日俸禄巡检...")
        claimed = 0

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过在线礼包与俸禄领取")

        # 1. 领取微端专享每日礼包 (Mod 0, Act 39: receive_client_gift)
        try:
            logger.info("发送微端专享每日礼包领取指令 (Mod 0, Act 39)...")
            pkt_client_gift = PacketBuilder(mod=0, act=39).write_int32(0).build()
            await client.send_packet(pkt_client_gift)
            claimed += 1
            logger.info("微端专享每日礼包指令已成功发送")
        except Exception as exc:
            logger.warning("微端专享礼包领取异常: %s", exc)

        # 2. 领取在线时长累积礼包 (Mod 0, Act 46: player_get_online_gift)
        try:
            logger.info("发送在线时长累积礼包领取指令 (Mod 0, Act 46)...")
            pkt_online_gift = PacketBuilder(mod=0, act=46).write_int32(0).build()
            await client.send_packet(pkt_online_gift)
            claimed += 1
            logger.info("在线时长累积礼包指令已成功发送")
        except Exception as exc:
            logger.warning("在线时长礼包领取异常: %s", exc)

        # 3. 领取阵营/帮派每日俸禄 (Mod 0, Act 22: get_player_camp_salary)
        try:
            logger.info("发送阵营/帮派每日俸禄领取指令 (Mod 0, Act 22)...")
            # 经 Stream 18 真实抓包印证：微端发送 4 字节标识 00010000
            pkt_salary = PacketBuilder(mod=0, act=22).write_bytes(bytes.fromhex("00010000")).build()
            await client.send_packet(pkt_salary)
            claimed += 1
            logger.info("阵营/帮派每日俸禄领取指令已成功发送")
        except Exception as exc:
            logger.warning("阵营俸禄领取异常: %s", exc)

        msg = f"在线福利与每日俸禄巡检完成，成功触发 {claimed} 项福利领取"
        logger.info(msg)
        return TaskResult.success(msg, data={"claimed": claimed})
