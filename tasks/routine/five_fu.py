"""神仙道寻仙五福临门每日福利自动化任务 (Mod 68: Mod_FindImmortal_Base)

对接官方微端寻仙五福临门子系统协议，自动同步每日免费祈福次数与阶段，
智能执行开始祈福与收官领奖流水线，严格遵守零元宝安全红线 (绝不元宝改运)。

@author Ateng
@since 2026-10-17
"""

import asyncio
import logging
from typing import Any, Dict

from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)

# Mod 68 寻仙系统常量
MOD_FIND_IMMORTAL = 68

# 动作协议标识
ACT_OPEN_FIVE_BLESSINGS = 10
ACT_START_BLESS = 11
ACT_CONTINUE_BLESS = 12
ACT_END_BLESS = 13
ACT_IS_FIVE_BLESSINGS_OPEN = 14

# 状态码
SUCCESS = 0
NOT_ENOUGH_COIN = 1
HAVE_NOT_NUMBER = 2
GOADING = 3
NOT_ENOUGH_INGOT = 4
FAILED = 5
HAVE_NOT_FIND = 6
NO_ENOUGTH_FAME = 7
NOT_ENOUGH_NUMBER = 8
ALREADY_START = 9
EXCHANGE_FUN_NOT_OPEN = 10
NOT_START = 11
YES = 12
NO = 13


class FiveFuTask(BaseTask):
    """寻仙五福临门每日福利自动化任务

    @author Ateng
    @since 2026-10-17
    """

    name = "FiveFuTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行寻仙五福临门免费祈福与福利收割

        Args:
            client: 已建立的长连接客户端。
            ctx: 游戏全局运行时上下文。

        Returns:
            TaskResult: 任务执行结果。
        """
        logger.info("开始执行五福临门 (FiveFu / Mod 68) 日常福利巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过五福临门任务")

        try:
            # 1. 探测五福临门系统开放状态 (Mod 68, Act 14: is_five_blessings_open)
            try:
                req_open_probe = PacketBuilder(mod=MOD_FIND_IMMORTAL, act=ACT_IS_FIVE_BLESSINGS_OPEN).build()
                resp_open_probe = await client.request(req_open_probe, timeout_sec=2.0)
                logger.info("五福临门开放状态探测回包: %s", resp_open_probe.hex() if resp_open_probe else "None")
                if resp_open_probe and len(resp_open_probe) > 0 and resp_open_probe[0] == NO:
                    msg = "五福临门当前未开放 (is_five_blessings_open=NO)，安全跳过"
                    logger.info(msg)
                    return TaskResult.skipped(msg, data={"active": False, "is_open": False})
            except Exception as probe_err:
                logger.debug("五福临门开放探测异常: %s", probe_err)

            # 2. 查询五福临门面板概况 (Mod 68, Act 10: open_five_blessings)
            req_panel = PacketBuilder(mod=MOD_FIND_IMMORTAL, act=ACT_OPEN_FIVE_BLESSINGS).build()
            resp_panel = await client.request(req_panel, timeout_sec=2.5)
            logger.info("五福临门面板回包: %s (长度: %d 字节)", resp_panel.hex() if resp_panel else "None", len(resp_panel) if resp_panel else 0)
            if not resp_panel or len(resp_panel) < 3:
                return TaskResult.skipped("五福临门面板响应为空，安全跳过", data={"active": False})

            reader = ByteArrayReader(resp_panel)
            bless_number = reader.read_int16()
            stage = reader.read_uint8()
            logger.info("五福临门面板同步成功: 剩余免费祈福次数=%d, 当前阶段=%d", bless_number, stage)

            rounds_done = 0
            claimed_pending = False

            # 3. 若有未结算收官的旧阶段 (stage > 0)，先行执行收官领奖防丢失
            if stage > 0:
                logger.info("检测到未领取的五福临门祈福奖励 (阶段: %d)，执行收官领取...", stage)
                req_claim = PacketBuilder(mod=MOD_FIND_IMMORTAL, act=ACT_END_BLESS).build()
                resp_claim = await client.request(req_claim, timeout_sec=2.0)
                if resp_claim and len(resp_claim) > 0 and resp_claim[0] == SUCCESS:
                    claimed_pending = True
                    logger.info("已成功结算并领取上一轮五福临门遗留奖励！")
                stage = 0

            # 4. 循环消耗剩余免费祈福次数 (零元宝安全闭环)
            while bless_number > 0:
                logger.info("开始执行第 %d 次五福临门免费祈福 (剩余: %d 次)...", rounds_done + 1, bless_number)
                req_start = PacketBuilder(mod=MOD_FIND_IMMORTAL, act=ACT_START_BLESS).build()
                resp_start = await client.request(req_start, timeout_sec=2.5)
                if not resp_start or len(resp_start) == 0:
                    logger.warning("五福临门祈福请求无响应，终止后续轮次")
                    break

                res_code = resp_start[0]
                if res_code == SUCCESS:
                    rounds_done += 1
                    bless_number -= 1

                    # 祈福成功后，直接收官领取本轮奖励 (Mod 68, Act 13: end_bless，严禁改运消耗元宝)
                    req_end = PacketBuilder(mod=MOD_FIND_IMMORTAL, act=ACT_END_BLESS).build()
                    resp_end = await client.request(req_end, timeout_sec=2.0)
                    if resp_end and len(resp_end) > 0 and resp_end[0] == SUCCESS:
                        logger.info("第 %d 轮五福临门祈福奖励结算并领取成功！(零元宝)", rounds_done)
                    else:
                        logger.info("第 %d 轮五福临门已完成祈福 (零元宝)", rounds_done)

                elif res_code in (HAVE_NOT_NUMBER, NOT_ENOUGH_NUMBER):
                    logger.info("今日五福临门免费祈福次数已全部耗尽")
                    break
                elif res_code == NOT_ENOUGH_INGOT:
                    logger.warning("五福临门需要元宝，触发零元宝熔断！立即终止后续操作")
                    break
                else:
                    logger.warning("五福临门祈福返回状态异常 (状态码: %d)，安全中止", res_code)
                    break

                await asyncio.sleep(0.3)

            msg = (
                f"五福临门流水线完成: 成功执行免费祈福 {rounds_done} 轮"
                f"{'，补领遗留奖励 1 次' if claimed_pending else ''} (严格零元宝)"
            )
            logger.info(msg)
            return TaskResult.success(
                msg,
                data={
                    "active": True,
                    "rounds_done": rounds_done,
                    "claimed_pending": claimed_pending,
                    "remaining_free": bless_number,
                },
            )

        except TimeoutError:
            msg = "五福临门网关交互超时，安全跳过防断连"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"active": False, "timeout": True})
        except Exception as exc:
            logger.warning("五福临门流水线异常: %s", exc)
            return TaskResult.skipped(f"五福临门异常跳过: {exc}")
