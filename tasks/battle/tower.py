"""神仙道六道轮回塔与封灵石自动化任务 (Mod 32: Mod_Tower_Base, Mod 100)

对齐官方微端 Mod 32 (Mod_Tower_Base) 轮回塔体系，自动巡检当前层数、关卡进度与封灵石收益，严格执行零元宝安全红线。

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

# 六道轮回塔官方常量状态码定义 (Mod_Tower_Base)
TOWER_SUCCESS = 0
TOWER_INVALID_LAYER = 1
TOWER_NO_LV = 2
TOWER_WAR_CD = 3
TOWER_NOT_ENOUGH_INGOT = 4
TOWER_FULL_TIMES = 5
TOWER_FULL_BAG = 6
TOWER_FAILED = 7


class TowerTask(BaseTask):
    """六道轮回塔与封灵石自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "TowerTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行六道轮回塔与封灵石巡检流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过六道轮回塔任务")

        # 角色等级门槛防御 (六道轮回塔 70 级开放)
        if ctx.player.level < 70:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达六道轮回塔开启门槛 (70级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"level_limit": True})

        layer_id = 0
        cur_seq = 0
        max_seq = 0
        remain_reset = 0
        is_auto = 0
        stone_count = 0

        # 1. 查询六道轮回塔基础面板 (Mod 32, Act 0: get_tower_info)
        try:
            req_info = PacketBuilder(mod=32, act=0).build()
            resp_info = await client.request(req_info, timeout_sec=3.0)
            reader = ByteArrayReader(resp_info)

            if reader.remaining >= 13:
                layer_id = reader.read_int8()
                cur_seq = reader.read_int8()
                max_seq = reader.read_int8()
                remain_reset = reader.read_int8()
                can_buy_reset = reader.read_int8()
                cd_time = reader.read_int16()
                is_auto = reader.read_int8()
                remain_auto = reader.read_int32()
                is_lock = reader.read_int8() if reader.remaining >= 1 else 0

                logger.info(
                    "六道轮回塔状态: 层数=%d, 当前关=%d, 最高通关=%d, 免费重置次数=%d, CD=%d秒, 自动托管状态=%d",
                    layer_id, cur_seq, max_seq, remain_reset, cd_time, is_auto
                )
            else:
                logger.info("六道轮回塔未就绪或未解锁，跳过")
        except Exception as exc:
            logger.info("六道轮回塔面板查询跳过: %s", exc)

        # 2. 查询与同步封灵石收益 (Mod 100, Act 19: get_stone)
        try:
            req_stone = PacketBuilder(mod=100, act=19).build()
            resp_stone = await client.request(req_stone, timeout_sec=3.0)
            reader_st = ByteArrayReader(resp_stone)
            if reader_st.remaining >= 8:
                stone_count = reader_st.read_uint16()
                free_quota = reader_st.read_uint16()
                used_quota = reader_st.read_uint16()
                max_quota = reader_st.read_uint16()
                logger.info("封灵石状态同步: 当前持有灵石=%d, 每日免费配额=%d/%d", stone_count, free_quota, max_quota)
        except Exception as exc:
            logger.debug("封灵石查询跳过: %s", exc)

        # 3. 强零元宝安全红线防护
        # 绝不调用任何元宝购买重置 (can_buy_reset)、元宝秒 CD 等接口
        summary_msg = f"六道轮回塔巡检完毕: 层数={layer_id}, 进度={cur_seq}/{max_seq}, 免费重置={remain_reset}, 持有灵石={stone_count} (严格零元宝)"
        logger.info(summary_msg)
        return TaskResult.success(summary_msg, data={
            "layer_id": layer_id,
            "cur_seq": cur_seq,
            "max_seq": max_seq,
            "remain_reset": remain_reset,
            "stone_count": stone_count
        })
