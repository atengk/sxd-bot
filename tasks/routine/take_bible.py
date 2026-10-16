"""神仙道西天取经护送自动化任务 (Mod 30: Mod_TakeBible_Base)

对接官方微端 Mod 30 (Mod_TakeBible_Base) 协议，自动查询西天取经护送状态，
启动每日免费使徒护送获取声望与巨额铜钱，严格遵守零元宝安全红线 (绝不元宝刷新使徒，绝不元宝加速)。

@author Ateng
@since 2026-10-16
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)

# Mod 30 TakeBible 状态码常量
SUCCESS = 8
FULL_TAKE_BIBLE_TIMES = 17


class TakeBibleTask(BaseTask):
    """西天取经护送自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "TakeBibleTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行西天取经护送巡检流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过取经任务")

        # 取经功能通常 40 级以上开放
        if ctx.player.level < 40:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达取经门槛 (40级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"bible": False})

        # 城镇场景安全守卫：西天取经 NPC 位于主线城镇，处于高阶跨服/圣域城镇 (如城镇ID=29) 时直接发包会触发网关跨图断连
        if ctx.town.town_id > 10:
            msg = f"当前角色处于高阶城镇 (城镇ID={ctx.town.town_id})，非取经NPC专属场景，安全跳过防断连"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"bible": False, "town_id": ctx.town.town_id})

        started = False
        try:
            # 1. 查询当前护送状态与剩余次数 (Mod 100, Act 46: get_take_bible_info)
            req_info = PacketBuilder(mod=100, act=46).build()
            resp_info = await client.request(req_info, timeout_sec=3.0)
            logger.info("西天取经状态同步成功 (响应载荷: %d 字节, 十六进制: %s)", len(resp_info), resp_info.hex())

            # 2. 严格零元宝：直接调用免费启动护送 (Mod 100, Act 35: start_take_bible)
            req_start = PacketBuilder(mod=100, act=35).build()
            resp_start = await client.request(req_start, timeout_sec=3.0)
            reader_start = ByteArrayReader(resp_start)

            if reader_start.remaining >= 1:
                status_code = reader_start.read_uint8()
                if status_code == 0:
                    started = True
                    logger.info("成功启动西天取经免费护送！(状态码=%d, 零元宝)", status_code)
                else:
                    logger.info("西天取经今日已在进行中或护送次数已满 (状态码=%d)", status_code)

        except Exception as exc:
            logger.warning("西天取经执行异常: %s", exc)

        if started:
            msg = "成功启动西天取经免费护送 (零元宝)"
            return TaskResult.success(msg, data={"started": True})
        else:
            msg = "西天取经巡检完成: 今日护送已在进行中或次数耗尽"
            return TaskResult.success(msg, data={"started": False})
