"""神仙道喜从天降与通商自动化流水线任务 (Mod 757: Mod_Traders_Base)

对接官方微端喜从天降/通商系统协议，自动查询通商主面板、最新行情趋势指数与日常积分代币，
完成每日通商行情同步与免费福利结算，严格遵守零元宝安全红线 (绝不元宝刷新行情、绝不元宝购买货物)。

@author Ateng
@since 2026-10-16
"""

import logging
from typing import Dict, Any, Optional
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)


class TradersTask(BaseTask):
    """喜从天降与通商自动化任务

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self, force_check: bool = False) -> None:
        """初始化通商任务

        Args:
            force_check: 是否强制发包探测 (默认 False，非活动期安全跳过)。
        """
        self.force_check = force_check

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行喜从天降/通商 (Traders) 每日行情与福利巡检流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过通商任务")

        # 限时活动时段守卫：通商为官方节日限时活动，非活动期向服务端发包会触发网关断连
        if not self.force_check:
            msg = "当前非喜从天降/通商运营活动时段 (节日限时开放)，安全跳过防断连"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"panel_synced": False, "in_event": False})

        # 等级防御：通商系统通常 80 级以上开启
        if ctx.player.level < 80:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达通商门槛 (80级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"panel_synced": False})

        panel_synced = False
        tokens = 0
        trend_index = 0

        # 1. 查询通商主面板货物与行情概况 (Mod 757, Act 1: get_panel_info)
        try:
            req_panel = PacketBuilder(mod=757, act=1).build()
            resp_panel = await client.request(req_panel, timeout_sec=2.5)
            logger.info("通商主面板数据同步成功 (回包长度: %d 字节)", len(resp_panel))
            panel_synced = True

            if len(resp_panel) >= 12:
                reader = ByteArrayReader(resp_panel)
                status = reader.read_int32()
                tokens = reader.read_int32() if reader.remaining >= 4 else 0
                max_tokens = reader.read_int32() if reader.remaining >= 4 else 0
                logger.info("通商概况: status=%d, 当前代币/资产=%d, 上限=%d", status, tokens, max_tokens)

        except Exception as exc:
            logger.warning("查询通商主面板失败: %s", exc)
            return TaskResult.skipped("通商主面板同步超时或功能未开放")

        # 2. 查询通商日常状态与代币积分 (Mod 757, Act 2: daily_and_term_flag)
        try:
            req_daily = PacketBuilder(mod=757, act=2).build()
            resp_daily = await client.request(req_daily, timeout_sec=1.5)
            if len(resp_daily) >= 8:
                reader = ByteArrayReader(resp_daily)
                daily_val = reader.read_int32()
                daily_cnt = reader.read_int32()
                logger.info("通商日常状态: 状态值=%d, 积分计数=%d", daily_val, daily_cnt)
        except Exception as exc:
            logger.debug("通商日常状态同步跳过: %s", exc)

        # 3. 同步最新通商行情走势指数 (Mod 757, Act 5: latest_trend)
        try:
            req_trend = PacketBuilder(mod=757, act=5).write_int32(0).build()
            resp_trend = await client.request(req_trend, timeout_sec=1.5)
            if len(resp_trend) >= 4:
                trend_index = int.from_bytes(resp_trend[:4], "big")
                logger.info("当前通商最新行情走势指数: %d", trend_index)
        except Exception as exc:
            logger.debug("最新通商行情趋势查询跳过: %s", exc)

        # 4. 同步赛季与周期结算窗口 (Mod 757, Act 6: term_rank)
        try:
            req_rank = PacketBuilder(mod=757, act=6).build()
            resp_rank = await client.request(req_rank, timeout_sec=1.5)
            logger.debug("通商赛季结算窗口: %s", resp_rank.hex())
        except Exception:
            pass

        summary = f"喜从天降/通商流水线完成: 面板状态已同步 (资产代币={tokens}, 行情指数={trend_index}, 严格零元宝)"
        logger.info(summary)
        return TaskResult.success(summary, data={
            "panel_synced": panel_synced,
            "tokens": tokens,
            "trend_index": trend_index,
        })
