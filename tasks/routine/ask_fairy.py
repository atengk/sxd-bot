"""神仙道仙道问灵每日求签与签文福利自动化任务 (Mod 503: Mod_AskFairy_Base)

支持角色满 100 级后每日免费仙道问灵、签文资产收集与活跃度累积，严格遵守自选商店零误触防线。

@author Ateng
@since 2026-10-16
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)


class AskFairyTask(BaseTask):
    """仙道问灵自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "AskFairyTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行每日仙道问灵流水线"""
        logger.info("开始执行仙道问灵 (AskFairy) 每日求签与活跃度巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于有效长连接状态，跳过问灵任务")

        # 1. 角色等级门槛检查 (问灵系统通常 100 级解锁)
        if ctx.player.level < 100:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达仙道问灵开启门槛 (100级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"level_ok": False})

        try:
            # 2. 查询问灵系统状态 (Mod 503, Act 0: get_recall_info)
            req_info = PacketBuilder(mod=503, act=0).build()
            resp_info = await client.request(req_info, timeout_sec=2.5)
            logger.info("仙道问灵系统状态同步成功 (响应长度: %d 字节)", len(resp_info))

            # 3. 执行每日免费问灵 1 次 (Mod 503, Act 3: do_ask_fairy)
            req_ask = PacketBuilder(mod=503, act=3).build()
            resp_ask = await client.request(req_ask, timeout_sec=2.5)
            ask_status = resp_ask[0] if resp_ask else 0

            if ask_status == 0:
                logger.info("今日免费仙道问灵成功！斩获新签文与活跃度奖励 (+5活跃度)")
            else:
                logger.info("今日免费仙道问灵已完成或处于冷却中 (状态码: %d)，安全跳过", ask_status)

            # 4. 尝试领取等级累积问灵奖励 (Mod 503, Act 7: gain_ask_level_award)
            try:
                req_lvl = PacketBuilder(mod=503, act=7).build()
                resp_lvl = await client.request(req_lvl, timeout_sec=2.0)
                logger.debug("问灵等级累积奖励检测响应: %s", resp_lvl.hex() if resp_lvl else "空")
            except Exception:
                logger.debug("暂无可领取的问灵等级阶梯奖励")

            msg = f"仙道问灵巡检完成: 状态已同步 ({len(resp_info)} 字节)，今日免费求签已执行 (状态: {ask_status})"
            logger.info(msg)
            return TaskResult.success(msg, data={"ask_status": ask_status})

        except Exception as exc:
            logger.warning("仙道问灵巡检异常 (安全跳过): %s", exc)
            return TaskResult.skipped(f"仙道问灵暂不可用: {exc}")
