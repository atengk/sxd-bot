"""神仙道每日签到与登录福利领取任务 (Mod 127, Mod 42)

自动查询七日登录与每日签到奖励状态，针对未领取的免费档位发送领取指令。严格遵守零元宝消耗安全原则。

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


class DailySignInTask(BaseTask):
    """每日签到与七日登录福利任务

    @author Ateng
    @since 2026-10-15
    """

    name = "DailySignInTask"
    interval_sec = 0.0  # 单次执行

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行每日签到与登录福利巡检...")
        claimed_count = 0

        # 1. 查询七日登录奖励状态 (Mod 127, Act 0)
        try:
            req_127 = PacketBuilder(mod=127, act=0).write_uint16(5).write_uint16(5).build()
            resp_127_bytes = await client.request(req_127, timeout_sec=5.0)

            # 解析七日登录奖励列表
            reader = ByteArrayReader(resp_127_bytes)
            if reader.remaining >= 2:
                total_days = reader.read_uint16()
                for day_idx in range(1, total_days + 1):
                    if reader.remaining < 3:
                        break
                    _day_id = reader.read_uint16()
                    status = reader.read_uint8()  # 0: 可领取, 1: 已领取, 2: 未达成

                    if status == 0:
                        logger.info("检测到第 %d 天登录福利可领取，正在领取...", day_idx)
                        claim_pkt = PacketBuilder(mod=127, act=2).write_uint16(day_idx).build()
                        await client.send_packet(claim_pkt)
                        claimed_count += 1
                        logger.info("第 %d 天登录福利已发送领取指令", day_idx)

        except Exception as exc:
            logger.warning("七日登录福利查询/领取异常: %s", exc)

        # 2. 查询常规每日签到 (Mod 42, Act 0)
        try:
            req_42 = PacketBuilder(mod=42, act=0).build()
            resp_42_bytes = await client.request(req_42, timeout_sec=5.0)
            reader42 = ByteArrayReader(resp_42_bytes)
            # 若第一字节为可签到标记 (0 为可签到)
            if reader42.remaining >= 1:
                sign_status = reader42.read_uint8()
                if sign_status == 0:
                    logger.info("检测到今日常规签到未完成，正在签到...")
                    do_sign = PacketBuilder(mod=42, act=1).build()
                    await client.send_packet(do_sign)
                    claimed_count += 1
                    logger.info("每日签到指令已发送")
                else:
                    logger.info("今日常规签到已完成或暂不可领")
        except Exception as exc:
            logger.warning("每日签到查询/执行异常: %s", exc)

        msg = f"签到任务巡检完毕，共领取/签到 {claimed_count} 项福利"
        logger.info(msg)
        return TaskResult.success(msg, data={"claimed_count": claimed_count})
