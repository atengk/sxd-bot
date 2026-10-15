"""神仙道招财神符/摇钱树免费福利自动化任务 (Mod 76)

自动查询每日免费招财次数，只消耗免费次数领取铜钱，严禁消耗非绑定元宝（零元宝防御红线）。

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


class FreeMoneyTreeTask(BaseTask):
    """免费招财神符任务

    @author Ateng
    @since 2026-10-15
    """

    name = "FreeMoneyTreeTask"
    interval_sec = 0.0  # 单次执行

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行招财神符免费次数巡检...")

        try:
            # 1. 查询招财神符状态 (Mod 76, Act 0)
            req_76 = PacketBuilder(mod=76, act=0).build()
            resp_bytes = await client.request(req_76, timeout_sec=5.0)

            reader = ByteArrayReader(resp_bytes)
            # 解析招财神符状态
            # 通常首字节为免费剩余次数 (free_times)
            if reader.remaining >= 1:
                free_times = reader.read_uint8()
                ingot_cost = reader.read_uint16() if reader.remaining >= 2 else 999

                logger.info("招财神符状态: 免费剩余次数=%d, 下次所需元宝=%d", free_times, ingot_cost)

                # 2. 严格零元宝安全红线防御
                if free_times > 0 and ingot_cost == 0:
                    logger.info("检测到存在免费招财次数，正在执行免费招财...")
                    claim_req = PacketBuilder(mod=76, act=1).build()
                    await client.send_packet(claim_req)
                    return TaskResult.success(f"成功领取免费招财，剩余免费次数: {free_times - 1}")
                else:
                    logger.info("无免费招财次数或需要消耗元宝，触发安全拦截并跳过")
                    return TaskResult.skipped("无可用免费招财次数，安全跳过")
            else:
                logger.info("招财神符状态应答为空，跳过执行")
                return TaskResult.skipped("招财神符应答载荷不足")

        except Exception as exc:
            logger.warning("招财神符巡检异常: %s", exc)
            return TaskResult.failed(f"招财神符执行失败: {exc}")
