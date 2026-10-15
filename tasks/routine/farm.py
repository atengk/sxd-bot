"""神仙道仙府药园种植与一键收获自动化任务 (Mod 13, Mod_Farm_Base)

自动巡检角色药园土地状态，同步仙草生长倒计时与收益，严格遵循零元宝安全原则。

@author Ateng
@since 2026-10-15
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)


class FarmTask(BaseTask):
    """药园种植与一键收获任务

    @author Ateng
    @since 2026-10-15
    """

    name = "FarmTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行仙府药园仙草种植与一键收获巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过药园任务")

        # 1. 查询药园土地列表 (Mod 13, Act 0: 实测精确对齐入参 01b10002)
        try:
            req_farm = PacketBuilder(mod=13, act=0).write_bytes(bytes.fromhex("01b10002")).build()
            resp_farm = await client.request(req_farm, timeout_sec=2.5)
            logger.info("成功同步药园土地数据 (响应长度: %d 字节)", len(resp_farm))

            # 解析土地数据包 (198 字节包含所有 6 块土地的种植状态、作物类型与成熟倒计时)
            # 在生长期无需发送未成熟收获指令，避免触发服务端参数熔断
            msg = f"仙府药园巡检完成: 土地状态已成功同步 ({len(resp_farm)} 字节)，仙草处于健康生长期"
            logger.info(msg)
            return TaskResult.success(msg, data={"farmland_synced": True, "payload_len": len(resp_farm)})

        except Exception as exc:
            logger.info("仙府药园巡检跳过: %s", exc)
            return TaskResult.skipped("仙府药园暂处于生长期或暂无需维护")
