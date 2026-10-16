"""神仙道每日签到与七日登录福利领取任务 (Mod 42, Mod 127)

自动查询常规每日签到与七日连续登录福利状态，针对未达成的免费档位发送领取指令。严格遵守零元宝消耗安全原则。

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

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过签到与登录福利任务")

        # 1. 常规每日签到巡检与执行 (Mod 42: Mod_SignIn_Base)
        try:
            # 1.1 查询签到状态 (Mod 42, Act 0: get_sign_in_info)
            req_42 = PacketBuilder(mod=42, act=0).build()
            resp_42 = await client.request(req_42, timeout_sec=3.0)
            reader42 = ByteArrayReader(resp_42)

            if reader42.remaining >= 3:
                signed_days = reader42.read_uint16()
                is_signed = reader42.read_uint8()  # 1: 今日已签到, 0: 未签到
                logger.info("常规签到状态: 累计已签到=%d 天, 今日状态=%s", signed_days, "已签到" if is_signed == 1 else "未签到")

                # 1.2 执行签到 (Mod 42, Act 2: player_sign_in)
                if is_signed == 0:
                    logger.info("检测到今日常规签到未完成，正在执行签到...")
                    do_sign = PacketBuilder(mod=42, act=2).build()
                    resp_sign = await client.request(do_sign, timeout_sec=3.0)
                    claimed_count += 1
                    logger.info("每日签到成功！(响应载荷 %d 字节)", len(resp_sign))
                else:
                    logger.info("今日常规签到已完成，无需重复签到")
            else:
                logger.warning("常规签到回包异常，长度不足 3 字节: %s", resp_42.hex())

        except Exception as exc:
            logger.warning("常规每日签到巡检异常: %s", exc)

        # 2. 七日登录/连续登录豪华福利巡检 (Mod 127: Mod_SignInTwo_Base)
        try:
            # 2.1 查询七日登录奖励列表 (Mod 127, Act 0: get_player_sign_in_info_two)
            req_127 = PacketBuilder(mod=127, act=0).build()
            resp_127 = await client.request(req_127, timeout_sec=3.0)
            reader127 = ByteArrayReader(resp_127)

            if reader127.remaining >= 2:
                total_items = reader127.read_uint16()
                logger.info("七日登录福利列表项目数: %d 项", total_items)

                for item_idx in range(1, total_items + 1):
                    if reader127.remaining < 3:
                        break
                    award_id = reader127.read_uint16()
                    status = reader127.read_uint8()  # 0: 可领取, 1: 已领取, 2: 未达成

                    if status == 0:
                        logger.info("检测到第 %d 项登录福利 (奖励ID=%d) 可领取，正在领取...", item_idx, award_id)
                        claim_pkt = PacketBuilder(mod=127, act=2).write_uint16(item_idx).build()
                        await client.send_packet(claim_pkt)
                        claimed_count += 1
                        logger.info("第 %d 项登录福利领取指令已发出", item_idx)
            else:
                logger.debug("七日登录福利暂无活动或回包为空")

        except Exception as exc:
            logger.warning("七日登录福利查询/领取异常: %s", exc)

        msg = f"签到与登录福利巡检完毕，共触发/完成 {claimed_count} 项福利领取"
        logger.info(msg)
        return TaskResult.success(msg, data={"claimed_count": claimed_count})
