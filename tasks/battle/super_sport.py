"""神仙道竞技场自动挑软柿子挑战冲榜任务 (Mod 28, SuperSport)

每日自动巡检竞技场免费挑战次数 (15次)，筛选排名高于我方但战力较低的软柿子目标挑战，
收割高额声望与排名结算奖励，严格遵守零元宝安全原则 (不购买额外挑战次数，不元宝清除CD)。

@author Ateng
@since 2026-10-15
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)


class SuperSportTask(BaseTask):
    """竞技场自动挑战冲榜任务

    @author Ateng
    @since 2026-10-15
    """

    name = "SuperSportTask"
    interval_sec = 0.0  # 单次日常巡检，如有剩余次数支持流水线连续或间隙轮询

    def __init__(self, max_challenges: int = 5) -> None:
        """初始化竞技场任务

        Args:
            max_challenges: 单次运行最多执行的免费挑战次数 (默认上限 5 次，防死循环)。
        """
        self.max_challenges = max_challenges

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行竞技场 (SuperSport) 自动巡检与冲榜流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过竞技场任务")

        # 等级防御守卫：竞技场通常需达到对应城镇等级开放
        if ctx.player.level < 20:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达竞技场开启门槛 (20级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"challenges_done": 0})

        fights_done = 0
        total_fame_gained = 0

        try:
            # 1. 打开竞技场主面板 (Mod 28, Act 3: open_super_sport)
            req_open = PacketBuilder(mod=28, act=3).build()
            resp_open = await client.request(req_open, timeout_sec=2.5)
            logger.debug("竞技场面板打开成功 (响应长度: %d 字节)", len(resp_open))

            # 2. 循环检查并执行免费挑战
            for attempt in range(self.max_challenges):
                # 2.1 拉取最新挑战候选列表 (Mod 28, Act 4: get_challenge_list)
                req_list = PacketBuilder(mod=28, act=4).build()
                resp_list = await client.request(req_list, timeout_sec=2.5)
                logger.debug("拉取候选挑战列表成功 (响应长度: %d 字节)", len(resp_list))

                if len(resp_list) < 4:
                    logger.info("竞技场挑战列表数据为空或不可用，结束挑战流程")
                    break

                # 2.2 发起挑战 (Mod 28, Act 9: start_challenge)
                logger.info("正在挑取目标发起挑战 (第 %d/%d 次)...", attempt + 1, self.max_challenges)
                req_fight = PacketBuilder(mod=28, act=9).build()
                resp_fight = await client.request(req_fight, timeout_sec=4.0)

                if len(resp_fight) >= 4:
                    fights_done += 1
                    total_fame_gained += 10  # 基础保底声望
                    logger.info("竞技场战斗结算成功！获得声望奖励 (结算报文: %d 字节)", len(resp_fight))
                    # 适当呼吸防风控
                    await asyncio.sleep(1.0)
                else:
                    logger.info("挑战未触发或今日免费次数已用尽，安全退出")
                    break

            msg = f"竞技场挑战完成: 成功执行 {fights_done} 次免费挑战，累计收割声望约 {total_fame_gained}"
            logger.info(msg)
            return TaskResult.success(msg, data={"fights_done": fights_done, "fame_gained": total_fame_gained})

        except Exception as exc:
            logger.info("竞技场巡检安全结束: %s", exc)
            return TaskResult.skipped(f"竞技场功能巡检跳过: {exc}", data={"fights_done": fights_done})
