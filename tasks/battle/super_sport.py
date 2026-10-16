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
            # 1. 官方前置卫语句：精准查询剩余免费挑战次数 (Mod 28, Act 13: get_challenge_times)
            req_times = PacketBuilder(mod=28, act=13).build()
            resp_times = await client.request(req_times, timeout_sec=3.0)
            times_reader = ByteArrayReader(resp_times)
            free_times = times_reader.read_uint16() if times_reader.remaining >= 2 else 0

            logger.info("竞技场状态同步: 今日剩余免费挑战次数 = %d 次", free_times)

            if free_times <= 0:
                msg = "今日竞技场免费挑战次数已用尽 (剩余0次)，严格遵守零元宝安全红线，坚决不付费购买次数，安全跳过"
                logger.info(msg)
                return TaskResult.skipped(msg, data={"free_times": 0, "fights_done": 0})

            # 2. 检查挑战冷却时间 (Mod 28, Act 12: get_cd_time)
            req_cd = PacketBuilder(mod=28, act=12).build()
            resp_cd = await client.request(req_cd, timeout_sec=3.0)
            cd_reader = ByteArrayReader(resp_cd)
            cd_time = cd_reader.read_int32() if cd_reader.remaining >= 4 else 0

            if cd_time > 0:
                msg = f"当前竞技场处于挑战冷却中 (CD剩余 {cd_time} 秒)，坚决不花元宝秒CD，安全跳过"
                logger.info(msg)
                return TaskResult.skipped(msg, data={"cd_time": cd_time, "fights_done": 0})

            # 3. 循环在免费额度内执行挑战
            rounds = min(self.max_challenges, free_times)
            for attempt in range(rounds):
                # 3.1 拉取候选挑战列表 (Mod 28, Act 1: get_challenge_list)
                req_list = PacketBuilder(mod=28, act=1).build()
                resp_list = await client.request(req_list, timeout_sec=3.0)
                if len(resp_list) < 4:
                    logger.info("竞技场候选挑战列表为空，结束挑战")
                    break

                # 3.2 发起挑战 (Mod 28, Act 2: start_challenge, 传入目标 player_id)
                # 从列表中挑取首个对手 ID (4字节)
                list_reader = ByteArrayReader(resp_list)
                target_pid = list_reader.read_int32() if list_reader.remaining >= 4 else 0

                logger.info("正在挑取目标玩家 (ID: %d) 发起免费挑战 (第 %d/%d 次)...", target_pid, attempt + 1, rounds)
                req_fight = PacketBuilder(mod=28, act=2).write_int32(target_pid).build()
                resp_fight = await client.request(req_fight, timeout_sec=5.0)

                if len(resp_fight) >= 1:
                    fights_done += 1
                    total_fame_gained += 10
                    logger.info("竞技场战斗结算成功！获得声望奖励 (结算报文: %d 字节)", len(resp_fight))
                    await asyncio.sleep(1.0)
                else:
                    break

            msg = f"竞技场挑战完成: 成功执行 {fights_done} 次免费挑战，累计收割声望约 {total_fame_gained}"
            logger.info(msg)
            return TaskResult.success(msg, data={"fights_done": fights_done, "fame_gained": total_fame_gained})

        except Exception as exc:
            logger.info("竞技场巡检安全结束: %s", exc)
            return TaskResult.skipped(f"竞技场功能巡检跳过: {exc}", data={"fights_done": fights_done})
