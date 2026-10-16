"""神仙道深海捕鱼自动化任务 (Mod 217: Mod_Fish_Base)

对齐官方微端 Mod 217 (Mod_Fish_Base) 捕鱼达人协议，自动巡检鱼叉数量并执行免费深海捕鱼，严格执行零元宝安全红线。

@author Ateng
@since 2026-10-16
"""

import logging
from typing import Dict, Any
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader
from tasks.base import BaseTask, TaskResult

logger = logging.getLogger(__name__)


class FishingTask(BaseTask):
    """深海捕鱼自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "FishingTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行深海捕鱼自动化巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过捕鱼任务")

        # 1. 查询当前可用鱼叉数量 (Mod 217, Act 0: get_player_fishhook)
        fishhook_count = 0
        try:
            req_info = PacketBuilder(mod=217, act=0).build()
            resp_info = await client.request(req_info, timeout_sec=3.0)
            reader = ByteArrayReader(resp_info)
            if reader.remaining >= 4:
                fishhook_count = reader.read_int32()
            logger.info("深海捕鱼状态查询完成: 剩余可用鱼叉=%d 支", fishhook_count)
        except Exception as exc:
            logger.warning("查询深海捕鱼鱼叉状态异常: %s", exc)
            return TaskResult.failed(f"捕鱼状态查询异常: {exc}")

        # 2. 强安全前置卫语句 (绝对零元宝安全红线)
        if fishhook_count <= 0:
            msg = "今日免费鱼叉已耗尽 (可用=0)，触发零元宝熔断保护，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"fishhook_count": 0, "fished_count": 0})

        # 3. 循环执行免费捕鱼 (Mod 217, Act 1: do_fishing)
        fished_success = 0
        while fishhook_count > 0:
            try:
                logger.info("正在执行免费撒网捕鱼 (当前剩余鱼叉=%d)...", fishhook_count)
                req_fish = PacketBuilder(mod=217, act=1).build()
                resp_fish = await client.request(req_fish, timeout_sec=3.0)
                reader_fish = ByteArrayReader(resp_fish)

                if reader_fish.remaining >= 1:
                    result_code = reader_fish.read_uint8()
                    if result_code == 0:  # SUCCESS
                        fish_type = reader_fish.read_int32() if reader_fish.remaining >= 4 else 0
                        reward = reader_fish.read_int32() if reader_fish.remaining >= 4 else 0
                        fished_success += 1
                        logger.info("捕鱼成功! 鱼种ID=%d, 结算奖励=%d", fish_type, reward)
                    else:
                        logger.info("捕鱼完成或背包配额限制 (状态码: %d)", result_code)
                        break
                else:
                    break

                fishhook_count -= 1
            except Exception as exc:
                logger.warning("执行深海捕鱼过程中出现异常: %s", exc)
                break

        summary_msg = f"深海捕鱼执行完毕: 成功捕鱼 {fished_success} 次，剩余鱼叉 {fishhook_count} 支 (严格零元宝)"
        logger.info(summary_msg)
        return TaskResult.success(summary_msg, data={"fishhook_count": fishhook_count, "fished_count": fished_success})
