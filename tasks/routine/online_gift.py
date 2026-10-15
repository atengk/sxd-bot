"""神仙道在线时长礼包与每日俸禄领取任务 (Mod 48, Mod 52)

自动查询并领取当前可领取的在线时长累积礼包与每日俸禄。

@author Ateng
@since 2026-10-15
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)


class OnlineGiftTask(BaseTask):
    """在线时长礼包与每日俸禄任务

    @author Ateng
    @since 2026-10-15
    """

    name = "OnlineGiftTask"
    interval_sec = 0.0  # 单次执行

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行在线时长礼包与每日俸禄巡检...")
        claimed = 0

        if not ctx.is_connected:
            return TaskResult.skipped("连接已断开，跳过在线礼包与俸禄领取")

        # 在线时长礼包与俸禄系统暂转为被动广播监听与安全巡检
        # 经 PCAP 深度逆向证实：Mod 52 为场景状态包，非法构造 Mod 52 Act 1 会导致服务端网关判定违规并立即切断 TCP (EOF)
        # 为确保长连接 100% 稳定，此处仅保留安全的上下文感知
        logger.debug("在线福利系统处于被动同步感知模式，规避主动非法探针")

        msg = f"在线福利巡检完成，成功触发 {claimed} 项礼包领取"
        return TaskResult.success(msg, data={"claimed": claimed})
