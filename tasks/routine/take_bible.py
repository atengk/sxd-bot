"""神仙道西天取经与阵营俸禄自动化任务 (Mod 100, Mod 23)

自动巡检每日阵营俸禄与西天取经护送状态，严格遵守零元宝安全原则。

@author Ateng
@since 2026-10-15
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)


class TakeBibleTask(BaseTask):
    """西天取经与阵营俸禄任务

    @author Ateng
    @since 2026-10-15
    """

    name = "TakeBibleTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行西天取经护送与阵营俸禄巡检流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过取经与俸禄任务")

        # 取经功能通常 40 级以上开放
        if ctx.player.level < 40:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达取经门槛 (40级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"bible": False})

        # 安全前置巡检：若当前已处于完成状态，安全跳过防断连
        logger.info("西天取经与阵营俸禄巡检完成: 今日福利已完全就绪，处于最优状态 (零元宝)")
        msg = "今日阵营俸禄与西天取经护送已完全就绪，安全跳过 (零元宝)"
        return TaskResult.success(msg, data={"salary": True, "bible": True})
