"""神仙道吉星高照免费福利自动化流水线任务 (Mod 38, Mod_RollCake_Base)

对接官方微端吉星高照协议，自动查询每日免费投掷次数与累计境界点，
自适应 VIP 托管状态（is_auto=1 时直接结算存量境界点，is_auto=0 时循环投掷），
严格遵守零元宝安全红线 (绝不元宝改命、绝不购买挑战次数)。

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

# Mod 38 常量
SUCCESS = 0
FAILURE = 1
NOT_ENOUGH_INGOT = 2
NO_CHANG_LUCK_TIMES = 3
NO_RECORD = 4
HAVE_RECORD = 5


class LuckyStarTask(BaseTask):
    """吉星高照免费投掷与奖励结算任务

    @author Ateng
    @since 2026-10-16
    """

    name = "LuckyStarTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行吉星高照日常巡检与奖励提取

        Args:
            client: 已建立的长连接客户端。
            ctx: 游戏全局运行时上下文。

        Returns:
            TaskResult: 任务执行结果。
        """
        logger.info("开始执行吉星高照 (RollCake) 免费投掷与奖励结算巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过吉星高照任务")

        # 角色等级防御：吉星高照通常 70 级以上开放
        if ctx.player.level < 70:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达吉星高照门槛 (70级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"rolls_done": 0})

        # 1. 查询吉星高照当前状态与剩余免费投掷次数 (Mod 38, Act 2: get_count)
        try:
            req_count = PacketBuilder(mod=38, act=2).build()
            resp_count = await client.request(req_count, timeout_sec=2.5)
            logger.info("吉星高照状态同步成功 (回包长度: %d 字节, 十六进制: %s)", len(resp_count), resp_count.hex())

            reader = ByteArrayReader(resp_count)
            free_times = reader.read_uint16() if reader.remaining >= 2 else 0
            points = reader.read_uint16() if reader.remaining >= 2 else 0
            extra_points = reader.read_uint32() if reader.remaining >= 4 else 0

            logger.info("吉星高照当前概况: 剩余免费投掷次数=%d, 当前积分=%d, 累计境界点=%d", free_times, points, extra_points)

        except Exception as exc:
            logger.warning("查询吉星高照状态失败: %s", exc)
            return TaskResult.skipped("吉星高照状态同步超时或功能未开放")

        # 2. 查询是否已开启自动吉星托管 (Mod 38, Act 6: is_auto)
        is_auto_active = False
        try:
            resp_auto = await client.request(PacketBuilder(mod=38, act=6).build(), timeout_sec=1.5)
            if len(resp_auto) > 0 and resp_auto[0] == 1:
                is_auto_active = True
                logger.info("吉星高照处于托管自动投掷状态 (is_auto=1)")
        except Exception:
            pass

        # 3. 检查并领取未结算的吉星奖励 (Mod 38, Act 4: get_award)
        claimed_existing_award = False
        try:
            req_award = PacketBuilder(mod=38, act=4).build()
            resp_award = await client.request(req_award, timeout_sec=1.5)
            if len(resp_award) > 0 and resp_award[0] == SUCCESS:
                claimed_existing_award = True
                logger.info("成功领取吉星高照存量奖励！境界点已自动入库")
        except Exception as exc:
            logger.debug("领取存量吉星奖励跳过: %s", exc)

        # 4. 强前置零元宝安全卫语句：若免费次数已耗尽，坚决跳过，绝对严禁消耗元宝！
        if free_times <= 0:
            msg = f"今日吉星高照免费投掷次数已用尽 (剩余 0 次)，零元宝安全熔断，绝不改命或购买挑战次数 (累计境界点: {extra_points})"
            logger.info(msg)
            return TaskResult.skipped(msg, data={
                "free_times": 0,
                "points": points,
                "extra_points": extra_points,
                "rolls_done": 0,
                "claimed_award": claimed_existing_award,
                "is_auto": is_auto_active,
            })

        # 5. 执行免费投掷循环 (严格零元宝，仅在未托管时手动发包)
        rolls_done = 0
        try:
            if is_auto_active:
                logger.info("吉星高照已处于系统托管自动投掷状态 (is_auto=1)，已自动结算，无需手动发包 (零断连)")
                rolls_done = free_times
            else:
                # 激活面板状态并执行手动免费投掷
                await client.send_packet(PacketBuilder(mod=38, act=5).build())
                while free_times > 0 and rolls_done < 10:
                    await client.send_packet(PacketBuilder(mod=38, act=0).build())
                    await asyncio.sleep(0.3)
                    await client.send_packet(PacketBuilder(mod=38, act=4).build())
                    rolls_done += 1
                    free_times -= 1
                    logger.info("第 %d 次免费吉星投掷完成并结算！", rolls_done)

            # 刷新最新结算点数
            final_resp = await client.request(PacketBuilder(mod=38, act=2).build(), timeout_sec=1.5)
            if len(final_resp) >= 8:
                reader = ByteArrayReader(final_resp)
                free_times = reader.read_uint16()
                points = reader.read_uint16()
                extra_points = reader.read_uint32()

        except Exception as roll_err:
            logger.info("吉星投掷安全收尾: %s", roll_err)

        summary = f"吉星高照流水线完成: 成功结算免费投掷, 最终累计境界点={extra_points} (零元宝)"
        logger.info(summary)
        return TaskResult.success(summary, data={
            "free_times": free_times,
            "points": points,
            "extra_points": extra_points,
            "rolls_done": rolls_done,
            "claimed_award": claimed_existing_award,
            "is_auto": is_auto_active,
        })
