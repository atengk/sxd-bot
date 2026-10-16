"""神仙道猎妖日常自动化任务 (Mod 105: Mod_HuntDemon_Base)

对接官方微端猎妖协议，自动查询每日免费猎妖次数并全额猎捕妖兽，
严格遵守零元宝安全红线 (参数硬编码 auto_buy=0，绝不元宝购买挑战次数)。

@author Ateng
@since 2026-10-16
"""

import asyncio
import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)

# Mod 105 常量
SUCCESS = 5
PACK_FULL = 6
NO_ENOUGH_INGOT = 7
NO_ENOUGH_COIN = 8
NO_ENOUGH_TIMES = 9


class HuntDemonTask(BaseTask):
    """猎妖日常自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "HuntDemonTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行每日免费猎妖挑战

        Args:
            client: 已建立的长连接客户端。
            ctx: 游戏全局运行时上下文。

        Returns:
            TaskResult: 任务执行结果。
        """
        logger.info("开始执行每日猎妖 (HuntDemon) 巡检流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过猎妖任务")

        if ctx.player.level < 80:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达猎妖门槛 (80级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"hunts_done": 0})

        # 1. 打开猎妖面板同步剩余免费次数 (Mod 105, Act 1: open_hunt_demon)
        free_times = 0
        try:
            req_open = PacketBuilder(mod=105, act=1).write_int8(1).build()
            resp_open = await client.request(req_open, timeout_sec=2.5)
            if len(resp_open) >= 3:
                reader = ByteArrayReader(resp_open)
                _type = reader.read_int8()
                free_times = reader.read_int8()
                max_times = reader.read_int8()
                logger.info("猎妖面板同步成功: 剩余免费次数=%d, 上限=%d", free_times, max_times)
        except Exception as exc:
            logger.warning("查询猎妖面板失败: %s", exc)
            return TaskResult.skipped(f"猎妖面板同步失败: {exc}")

        # 2. 强前置零元宝安全卫语句：若免费次数已耗尽，坚决跳过
        if free_times <= 0:
            msg = "今日猎妖免费挑战次数已用尽 (剩余 0 次)，零元宝安全熔断"
            logger.info(msg)
            return TaskResult.success(msg, data={"free_times": 0, "hunts_done": 0})

        # 3. 循环消耗每日免费猎妖次数 (严格 auto_buy=0 绝不消耗元宝)
        hunts_done = 0
        try:
            while free_times > 0 and hunts_done < 10:
                # Mod 105, Act 2: hunt_demon(type=1, auto_buy=0)
                req_hunt = PacketBuilder(mod=105, act=2).write_int8(1).write_int8(0).build()
                resp_hunt = await client.request(req_hunt, timeout_sec=2.5)
                if not resp_hunt:
                    break

                status = resp_hunt[0]
                if status == SUCCESS:
                    hunts_done += 1
                    free_times -= 1
                    logger.info("第 %d 次免费猎妖击杀成功！已获得铜钱、材料与历练 (零元宝)", hunts_done)
                    await asyncio.sleep(0.3)
                elif status in (NO_ENOUGH_TIMES, NO_ENOUGH_INGOT):
                    logger.info("猎妖次数或条件已耗尽 (状态码: %d)，安全中止", status)
                    break
                elif status == PACK_FULL:
                    logger.warning("背包已满，猎妖安全提前中止")
                    break
                else:
                    logger.info("猎妖返回状态码: %d，终止循环", status)
                    break

        except Exception as exc:
            logger.warning("猎妖循环执行异常收尾: %s", exc)

        summary = f"每日猎妖流水线完成: 成功猎杀妖兽 {hunts_done} 次 (零元宝)"
        logger.info(summary)
        return TaskResult.success(summary, data={"hunts_done": hunts_done, "free_times_left": free_times})
