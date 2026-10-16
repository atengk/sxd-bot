"""神仙道五行日常整理自动化任务 (Mod 168: Mod_FiveElements_Base)

对接官方微端五行真气系统协议，自动查询五行装备与晶石背包状态，
执行每日五行背包自动化梳理整理，严格遵守零破坏性原则 (不擅自升级/吞噬晶石)。

@author Ateng
@since 2026-10-16
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)

# Mod 168 常量
SUCCESS = 9


class FiveElementsTask(BaseTask):
    """五行日常整理自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "FiveElementsTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行五行系统日常同步与背包梳理

        Args:
            client: 已建立的长连接客户端。
            ctx: 游戏全局运行时上下文。

        Returns:
            TaskResult: 任务执行结果。
        """
        logger.info("开始执行五行系统 (FiveElements) 日常整理巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过五行任务")

        if ctx.player.level < 100:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达五行开启门槛 (100级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"cleaned": False})

        cleaned = False
        equip_count = 0
        try:
            # 1. 查询当前五行背包装备列表 (Mod 168, Act 0: get_pack_five_elements_equip_list)
            req_list = PacketBuilder(mod=168, act=0).build()
            resp_list = await client.request(req_list, timeout_sec=2.5)
            if resp_list and len(resp_list) >= 2:
                equip_count = (resp_list[0] << 8) | resp_list[1]
                logger.info("五行背包数据同步成功，包含 %d 件五行资产", equip_count)

            # 2. 触发五行背包一键归类与整理 (Mod 168, Act 10: clean_up_pack)
            req_clean = PacketBuilder(mod=168, act=10).build()
            resp_clean = await client.request(req_clean, timeout_sec=2.0)
            if resp_clean and len(resp_clean) >= 1 and resp_clean[0] == SUCCESS:
                cleaned = True
                logger.info("五行背包与晶石槽位自动化整理完成！")

            summary = f"五行系统巡检完成: 资产已同步 (存量 {equip_count} 件)，背包整理={'成功' if cleaned else '已跳过'}"
            logger.info(summary)
            return TaskResult.success(summary, data={"cleaned": cleaned, "equip_count": equip_count})

        except Exception as exc:
            logger.warning("五行日常流水线执行异常: %s", exc)
            return TaskResult.skipped(f"五行任务异常跳过: {exc}")
