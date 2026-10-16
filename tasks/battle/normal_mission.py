"""神仙道普通副本自动极速扫荡与体力清空任务 (Mod 25, Mod_MissionPractice_Base)

自动巡检角色剩余体力，选取最优普通关卡执行安全极速扫荡，严格遵守零元宝安全原则，杜绝体力自然溢出浪费。

@author Ateng
@since 2026-10-15
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)


class NormalMissionSweepTask(BaseTask):
    """普通副本自动扫荡与体力清空任务

    @author Ateng
    @since 2026-10-15
    """

    name = "NormalMissionSweepTask"
    interval_sec = 0.0  # 默认在单次流水线中执行；守护模式下由调度器或配置设置周期 (如 1800s)

    def __init__(
        self,
        target_mission_id: int = 854,
        target_town_id: int = 29,
        min_power_reserve: int = 0,
        interval_sec: float = 0.0,
    ) -> None:
        """初始化普通副本扫荡任务

        Args:
            target_mission_id: 优先扫荡的目标关卡 ID (默认 854 幽冥地府-白无常，支持配置指定)。
            target_town_id: 关卡所属城镇 ID (默认 29 大理城)。
            min_power_reserve: 预留最低体力值 (默认 0，消耗完全部体力)。
            interval_sec: 调度周期秒数 (守护模式下可配置)。
        """
        self.target_mission_id = target_mission_id
        self.target_town_id = target_town_id
        self.min_power_reserve = min_power_reserve
        self.interval_sec = interval_sec

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行普通副本扫荡流水线

        Args:
            client: 异步长连接客户端。
            ctx: 全局游戏上下文。

        Returns:
            任务执行结果对象。
        """
        logger.info("开始执行普通副本自动扫荡与体力清空流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于有效长连接状态，跳过副本扫荡")

        # 1. 检查角色等级门槛 (普通副本扫荡门槛通常为 10 级)
        if ctx.player.level < 10:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达普通副本扫荡门槛 (10级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"swept_rounds": 0})

        # 2. 检查体力 (若刚登录，微延时等待下行属性包完成解析)
        if ctx.player.power == 0:
            for _ in range(3):
                if ctx.player.power > 0:
                    break
                await asyncio.sleep(0.2)

        if ctx.player.power < 5 or ctx.player.power <= self.min_power_reserve:
            msg = f"当前体力不足以扫荡一次普通副本 (当前体力={ctx.player.power}, 预留={self.min_power_reserve}, 最少需5点)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"swept_rounds": 0, "power": ctx.player.power})

        initial_power = ctx.player.power
        logger.info("检测到可用体力 %d 点，开始按协议状态机执行副本扫荡清空...", initial_power)

        # 3. 如果当前所在城镇与目标关卡城镇不一致，同步传送至目标城镇 (Mod 1, Act 0: 单参数 town_id)
        if ctx.town.town_id > 0 and ctx.town.town_id != self.target_town_id:
            try:
                pkt_town = PacketBuilder(mod=1, act=0).write_int32(self.target_town_id).build()
                await client.send_packet(pkt_town)
                await asyncio.sleep(0.3)
            except Exception as exc:
                logger.warning("城镇切换异常 (尝试继续): %s", exc)

        # 3.5 前置背包空间自理守卫：若背包空格紧张 (< 5 格)，自动执行四阶自理流水线腾挪空间
        try:
            from tasks.routine.item_clean import ItemCleanTask
            clean_task = ItemCleanTask(target_empty=5)
            await clean_task.execute(client, ctx)
        except Exception as clean_err:
            logger.warning("扫荡前置背包清理守卫执行异常 (继续尝试扫荡): %s", clean_err)

        # 4. 循环执行全额扫荡与极速秒加速，直至体力耗尽 (< 5 点或到达保留阈值)
        loop_count = 0
        while ctx.player.power >= 5 and ctx.player.power > self.min_power_reserve:
            loop_count += 1
            power_before_round = ctx.player.power
            logger.info("--- 开始第 %d 轮清空体力极速扫荡 (当前体力: %d 点) ---", loop_count, power_before_round)

            # 4.1 查询关卡扫荡信息 (Mod 25, Act 0: write_int32(mission_id))
            pkt_info = PacketBuilder(mod=25, act=0).write_int32(self.target_mission_id).build()
            await client.send_packet(pkt_info)
            await asyncio.sleep(0.2)

            # 4.2 启动全额扫荡 (Mod 25, Act 1: mission_id[4B] + count=0[2B] + auto_sale=1[1B])
            # 官方规范: count=0 表示一次性全额消耗剩余体力挂机扫荡，auto_sale=1 自动变卖杂物
            pkt_start = (
                PacketBuilder(mod=25, act=1)
                .write_int32(self.target_mission_id)
                .write_uint16(0)
                .write_uint8(1)
                .build()
            )
            try:
                resp_bytes = await client.request(pkt_start, timeout_sec=5.0)
                if len(resp_bytes) >= 1:
                    code = resp_bytes[0]
                    if code == 1:
                        logger.warning("服务端提示体力不足 (NOT_ENOUGH_POWER)，结束扫荡")
                        break
                    elif code == 2:
                        logger.warning("服务端提示背包已满 (BAG_FULL)，结束扫荡")
                        break
            except Exception as exc:
                logger.warning("发送 start_practice 请求超时或异常: %s", exc)

            await asyncio.sleep(0.2)

            # 4.3 极速秒完成 (Mod 25, Act 3: times=0[2B])
            # 官方规范: 免元宝极速秒完成所有扫荡战斗，即刻结算经验与掉落
            pkt_quick = PacketBuilder(mod=25, act=3).write_uint16(0).build()
            try:
                await client.request(pkt_quick, timeout_sec=5.0)
            except Exception as exc:
                logger.warning("发送 quickly 加速请求异常: %s", exc)

            # 4.4 留出 1.5s 等待服务端连续推送战报、经验奖励与 Mod 0 Act 3 体力扣减广播
            await asyncio.sleep(1.5)

            # 若体力未扣减（可能关卡次数耗尽或异常），防御性跳出，防止死循环
            if ctx.player.power >= power_before_round:
                logger.info("本轮扫荡后体力未发生变动，可能已耗尽或关卡不可挑战，退出循环")
                break

        total_consumed = max(0, initial_power - ctx.player.power)
        msg = f"普通副本扫荡任务完成: 累计执行 {loop_count} 轮极速扫荡，消耗体力 {total_consumed} 点，剩余体力 {ctx.player.power} 点"
        logger.info(msg)
        return TaskResult.success(msg, data={"swept_loops": loop_count, "consumed_power": total_consumed, "final_power": ctx.player.power})
