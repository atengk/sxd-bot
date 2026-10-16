"""神仙道角色城镇打坐与挂机练功自动化任务 (Mod 0: Player.start_practice)

在日常主线任务结束后或守护空闲时，指令角色进入打坐挂机练功状态，保障离线与空闲收益。

@author Ateng
@since 2026-10-16
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)


class PracticeTask(BaseTask):
    """城镇挂机打坐练功任务

    @author Ateng
    @since 2026-10-16
    """

    name = "PracticeTask"
    interval_sec = 0.0  # 单次流水线收官任务

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行角色挂机打坐练功指令"""
        logger.info("开始执行角色城镇挂机打坐与练功状态设置...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于有效长连接状态，跳过练功任务")

        try:
            # 发送角色打坐练功指令 (Mod 0, Act 36: start_practice)
            req_practice = PacketBuilder(mod=0, act=36).build()
            await client.send_packet(req_practice)
            logger.info("已成功向服务端提交角色打坐练功挂机指令 (Mod 0, Act 36)")

            msg = "角色打坐练功状态已激活，持续累积挂机经验"
            return TaskResult.success(msg, data={"practice_active": True})

        except Exception as exc:
            logger.warning("激活打坐练功异常 (安全跳过): %s", exc)
            return TaskResult.skipped(f"激活打坐练功跳过: {exc}")
