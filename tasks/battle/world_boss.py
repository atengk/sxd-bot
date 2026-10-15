"""神仙道世界 Boss 定时参战与挂机复活自动化任务 (Mod 24, WorldBoss)

支持每日定时世界 Boss (擎天木/赤炎兽/刀疤兔) 时段感知接入、阅历免费鼓舞增强战力、
阵亡免费复活重返战场与秒战结算，严格遵守零元宝安全原则 (不元宝鼓舞，不元宝加速复活)。

@author Ateng
@since 2026-10-15
"""

import asyncio
from datetime import datetime
import logging
from typing import Dict, Any, List, Optional
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)


class WorldBossTask(BaseTask):
    """世界 Boss 定时参战自动化任务

    @author Ateng
    @since 2026-10-15
    """

    name = "WorldBossTask"
    interval_sec = 0.0  # 单次巡检，亦可由调度器在活动时段定时唤醒

    # 官方世界 Boss 标准时段 (小时, 分钟起止)
    ACTIVE_WINDOWS = [
        (10, 0, 10, 30),  # 上午场 10:00 - 10:30 (擎天木)
        (15, 30, 16, 0),  # 下午场 15:30 - 16:00 (赤炎兽)
    ]

    def __init__(self, force_check: bool = False) -> None:
        """初始化世界 Boss 任务

        Args:
            force_check: 是否无视时段强制探测世界 Boss 战场状态。
        """
        self.force_check = force_check

    def _is_in_boss_time(self) -> bool:
        """判断当前时间是否处于世界 Boss 开放时段"""
        now = datetime.now()
        current_minute = now.hour * 60 + now.minute
        for sh, sm, eh, em in self.ACTIVE_WINDOWS:
            start_m = sh * 60 + sm
            end_m = eh * 60 + em
            if start_m <= current_minute <= end_m:
                return True
        return False

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行世界 Boss (WorldBoss) 活动状态巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过世界 Boss 任务")

        # 1. 前置时间守卫拦截：非活动时段安全跳过，杜绝空发报文导致网关断连
        if not self.force_check and not self._is_in_boss_time():
            now_str = datetime.now().strftime("%H:%M")
            msg = f"当前时间 ({now_str}) 非世界 Boss 开放时段 (10:00-10:30 / 15:30-16:00)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"in_event": False})

        # 等级防御：世界 Boss 开启门槛
        if ctx.player.level < 25:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达世界 Boss 门槛 (25级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"in_event": False})

        fights_done = 0
        inspires_done = 0

        try:
            # 2. 免费阅历鼓舞战力 (Mod 24, Act 15: strengthen_combat, 严格阅历/零元宝)
            try:
                req_inspire = PacketBuilder(mod=24, act=15).build()
                resp_inspire = await client.request(req_inspire, timeout_sec=2.0)
                if len(resp_inspire) >= 2:
                    inspires_done += 1
                    logger.info("阅历免费鼓舞执行成功！战力获得加成")
            except Exception as exc:
                logger.debug("阅历鼓舞暂未开放或已达上限: %s", exc)

            # 3. 发起战斗挑战 Boss (Mod 24, Act 14: fight_world_boss)
            try:
                req_fight = PacketBuilder(mod=24, act=14).build()
                resp_fight = await client.request(req_fight, timeout_sec=3.0)
                if len(resp_fight) >= 2:
                    fights_done += 1
                    logger.info("世界 Boss 参战攻击成功！获得巨额声望与伤害贡献 (报文长度: %d 字节)", len(resp_fight))

                    # 4. 阵亡免费复活 (Mod 24, Act 13: super_reborn, 免费/等待CD)
                    await asyncio.sleep(0.5)
                    try:
                        req_reborn = PacketBuilder(mod=24, act=13).build()
                        await client.request(req_reborn, timeout_sec=1.5)
                        logger.info("世界 Boss 免费重生复活成功")
                    except Exception:
                        pass
                else:
                    logger.info("世界 Boss 暂未刷新或已被击杀结算")
            except Exception as exc:
                logger.info("世界 Boss 参战探测: %s", exc)

            status_msg = "已参战并完成战斗结算" if fights_done > 0 else "当前世界 Boss 处于未开始或已结束状态"
            msg = f"世界 Boss 巡检完成: {status_msg} (鼓舞: {inspires_done}次, 参战: {fights_done}次)"
            logger.info(msg)
            return TaskResult.success(msg, data={"fights_done": fights_done, "inspires_done": inspires_done})

        except Exception as exc:
            logger.info("世界 Boss 任务安全跳过: %s", exc)
            return TaskResult.skipped(f"世界 Boss 任务跳过: {exc}")
