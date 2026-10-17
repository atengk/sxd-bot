"""神仙道猎妖日常自动化任务 (Mod 105: Mod_HuntDemon_Base)

对接官方微端猎妖协议，自动查询每日免费猎妖次数与铜钱猎妖次数，
双轨推进：优先消耗每日 5 次免费猎妖，随后消耗每日 15 次铜钱猎妖，
严格遵守零元宝安全红线 (参数硬编码 auto_buy=0，绝不元宝购买挑战次数)，
并内置背包满安全熔断与铜钱防破产安全底线拦截。

@author Ateng
@since 2026-10-17
"""

import asyncio
import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)

# Mod 105 常量与动作模式 (对齐官方 ActionScript 反编译底层契约)
HUNT_MODE_FREE = 0  # 免费猎妖 (sendFreeFun)
HUNT_MODE_COIN = 1  # 铜钱猎妖 (sendCommonFun)
HUNT_MODE_INGOT = 2  # 元宝猎妖 (sendIngotFun，严禁调用)

SUCCESS = 5
PACK_FULL = 6
NO_ENOUGH_INGOT = 7
NO_ENOUGH_COIN = 8
NO_ENOUGH_TIMES = 9
FIND_IMMORTAL_NUM_FULL = 10

# 铜钱猎妖防破产底线（角色铜钱若低于此阈值，则跳过铜钱猎妖以保护资产安全）
MIN_COIN_THRESHOLD = 500_000


class HuntDemonTask(BaseTask):
    """猎妖日常自动化任务

    @author Ateng
    @since 2026-10-17
    """

    name = "HuntDemonTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行每日猎妖巡检流水线 (双轨：优先免费猎妖，后置铜钱猎妖)

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
            return TaskResult.skipped(
                msg,
                data={
                    "hunts_done": 0,
                    "total_hunts": 0,
                    "free_hunts_done": 0,
                    "coin_hunts_done": 0,
                },
            )

        # 1. 打开猎妖面板同步剩余免费次数与铜钱次数 (Mod 105, Act 1: open_hunt_demon)
        # 官方响应结构: [Byte free_times, Byte coin_times, Byte ingot_times, Short need_ingot, ...]
        free_times = 0
        coin_times = 0
        ingot_times = 0
        need_ingot = 0
        try:
            # Mod 105, Act 1: open_hunt_demon(type: Byte = 0)
            req_open = PacketBuilder(mod=105, act=1).write_int8(0).build()
            resp_open = await client.request(req_open, timeout_sec=2.5)
            if len(resp_open) >= 5:
                reader = ByteArrayReader(resp_open)
                free_times = reader.read_int8()
                coin_times = reader.read_int8()
                ingot_times = reader.read_int8()
                need_ingot = reader.read_int16()
                logger.info(
                    "猎妖面板同步成功: 剩余免费次数=%d, 剩余可用铜钱次数=%d, 剩余元宝次数=%d (需元宝=%d)",
                    free_times,
                    coin_times,
                    ingot_times,
                    need_ingot,
                )
            elif len(resp_open) >= 2:
                reader = ByteArrayReader(resp_open)
                free_times = reader.read_int8()
                coin_times = reader.read_int8()
                logger.info(
                    "猎妖面板同步成功 (紧凑格式): 剩余免费次数=%d, 剩余可用铜钱次数=%d",
                    free_times,
                    coin_times,
                )
            else:
                logger.warning("猎妖面板回包长度异常: %d 字节", len(resp_open))
                return TaskResult.skipped(f"猎妖面板回包长度不足 ({len(resp_open)} 字节)")
        except Exception as exc:
            logger.warning("查询猎妖面板失败: %s", exc)
            return TaskResult.skipped(f"猎妖面板同步失败: {exc}")

        # 2. 强前置零元宝安全卫语句：若免费次数与铜钱次数均已耗尽，坚决跳过
        if free_times <= 0 and coin_times <= 0:
            msg = f"今日猎妖免费与铜钱挑战次数已全部用尽 (免费={free_times}, 铜钱={coin_times})，零元宝安全熔断"
            logger.info(msg)
            return TaskResult.success(
                msg,
                data={
                    "hunts_done": 0,
                    "total_hunts": 0,
                    "free_hunts_done": 0,
                    "coin_hunts_done": 0,
                    "free_times_left": free_times,
                    "coin_times_left": coin_times,
                },
            )

        free_hunts_done = 0
        coin_hunts_done = 0
        pack_full = False

        # 3. 第一阶段：循环消耗每日免费猎妖次数 (type=0, auto_buy=0 严格绝不消耗元宝)
        if free_times > 0:
            logger.info("开始执行第一阶段：免费猎妖 (剩余可用 %d 次)...", free_times)
            try:
                while free_times > 0 and free_hunts_done < 10:
                    # Mod 105, Act 2: hunt_demon(type=0, auto_buy=0)
                    req_hunt = (
                        PacketBuilder(mod=105, act=2)
                        .write_int8(HUNT_MODE_FREE)
                        .write_int8(0)
                        .build()
                    )
                    resp_hunt = await client.request(req_hunt, timeout_sec=2.5)
                    if not resp_hunt:
                        break

                    status = resp_hunt[0]
                    if status == SUCCESS:
                        free_hunts_done += 1
                        free_times -= 1
                        logger.info(
                            "第 %d 次免费猎妖击杀成功！已获得铜钱、材料与历练 (严格零元宝)",
                            free_hunts_done,
                        )
                        await asyncio.sleep(0.3)
                    elif status == PACK_FULL:
                        logger.warning("背包已满，猎妖安全提前中止")
                        pack_full = True
                        break
                    elif status in (NO_ENOUGH_TIMES, NO_ENOUGH_INGOT):
                        logger.info("免费猎妖次数已耗尽或需元宝 (状态码: %d)，结束免费阶段", status)
                        break
                    else:
                        logger.info("免费猎妖返回状态码: %d，终止免费阶段", status)
                        break
            except Exception as exc:
                logger.warning("免费猎妖循环执行异常: %s", exc)

        # 4. 第二阶段：循环消耗每日铜钱猎妖次数 (type=1, auto_buy=0，需前置检查铜钱存量防破产)
        if not pack_full and coin_times > 0:
            if ctx.player.coins < MIN_COIN_THRESHOLD:
                logger.info(
                    "当前角色铜钱 (%d) 低于猎妖安全底线 (%d)，安全跳过铜钱猎妖以防破产",
                    ctx.player.coins,
                    MIN_COIN_THRESHOLD,
                )
            else:
                logger.info(
                    "开始执行第二阶段：铜钱猎妖 (剩余可用 %d 次, 当前铜钱=%d)...",
                    coin_times,
                    ctx.player.coins,
                )
                try:
                    while coin_times > 0 and coin_hunts_done < 25:
                        # 动态检查铜钱余额
                        if ctx.player.coins < MIN_COIN_THRESHOLD:
                            logger.info(
                                "铜钱余额 (%d) 已接近安全阈值 (%d)，提前中止铜钱猎妖",
                                ctx.player.coins,
                                MIN_COIN_THRESHOLD,
                            )
                            break

                        # Mod 105, Act 2: hunt_demon(type=1, auto_buy=0)
                        req_hunt = (
                            PacketBuilder(mod=105, act=2)
                            .write_int8(HUNT_MODE_COIN)
                            .write_int8(0)
                            .build()
                        )
                        resp_hunt = await client.request(req_hunt, timeout_sec=2.5)
                        if not resp_hunt:
                            break

                        status = resp_hunt[0]
                        if status == SUCCESS:
                            coin_hunts_done += 1
                            coin_times -= 1
                            logger.info(
                                "第 %d 次铜钱猎妖击杀成功！已获得材料与历练 (严格零元宝)",
                                coin_hunts_done,
                            )
                            await asyncio.sleep(0.3)
                        elif status == NO_ENOUGH_COIN:
                            logger.info("角色铜钱不足 (状态码: 8)，中止铜钱猎妖")
                            break
                        elif status == PACK_FULL:
                            logger.warning("背包已满，铜钱猎妖安全提前中止")
                            pack_full = True
                            break
                        elif status in (NO_ENOUGH_TIMES, NO_ENOUGH_INGOT):
                            logger.info("铜钱猎妖次数已耗尽或需元宝 (状态码: %d)，安全中止", status)
                            break
                        elif status == FIND_IMMORTAL_NUM_FULL:
                            logger.info("寻仙次数达到上限 (状态码: 10)，安全中止铜钱猎妖")
                            break
                        else:
                            logger.info("铜钱猎妖返回状态码: %d，终止循环", status)
                            break
                except Exception as exc:
                    logger.warning("铜钱猎妖循环执行异常: %s", exc)

        total_hunts = free_hunts_done + coin_hunts_done
        summary = (
            f"每日猎妖流水线完成: 成功猎杀 {total_hunts} 次 "
            f"(免费 {free_hunts_done} 次, 铜钱 {coin_hunts_done} 次, 严格零元宝)"
        )
        logger.info(summary)
        return TaskResult.success(
            summary,
            data={
                "hunts_done": total_hunts,
                "total_hunts": total_hunts,
                "free_hunts_done": free_hunts_done,
                "coin_hunts_done": coin_hunts_done,
                "free_times_left": free_times,
                "coin_times_left": coin_times,
                "pack_full": pack_full,
            },
        )

