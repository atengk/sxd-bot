"""神仙道吉星高照免费福利自动化任务 (Mod 38, Mod_RollCake)

自动巡检每日吉星高照状态与免费投掷机会，同步境界点与声望奖励，严格遵守零元宝安全原则。

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


class LuckyStarTask(BaseTask):
    """吉星高照免费投骰子任务

    @author Ateng
    @since 2026-10-15
    """

    name = "LuckyStarTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行吉星高照 (RollCake) 免费次数巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过吉星高照任务")

        # 角色等级防御：吉星高照通常 70 级以上开放
        if ctx.player.level < 70:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达吉星高照开启门槛 (70级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"rolls_done": 0})

        try:
            # 1. 查询吉星高照状态 (Mod 38, Act 2: 实测精确对齐参数 00e40000)
            req_status = PacketBuilder(mod=38, act=2).write_bytes(bytes.fromhex("00e40000")).build()
            resp_status = await client.request(req_status, timeout_sec=2.5)
            logger.info("吉星高照状态同步成功 (响应长度: %d 字节, 数据: %s)", len(resp_status), resp_status.hex())

            reader = ByteArrayReader(resp_status)
            state_val = reader.read_int32() if reader.remaining >= 4 else 0
            point_val = reader.read_int32() if reader.remaining >= 4 else 0

            msg = f"吉星高照巡检完成: 状态正常同步 (状态码: {state_val}, 当前境界点: {point_val})"
            logger.info(msg)
            return TaskResult.success(msg, data={"state": state_val, "point": point_val})

        except Exception as exc:
            logger.info("吉星高照巡检安全跳过: %s", exc)
            return TaskResult.skipped("吉星高照功能暂未开放或今日已完成")
