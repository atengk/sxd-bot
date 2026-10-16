"""神仙道聚灵日常自动化任务 (Mod 104: Mod_Nimbus_Base)

对接官方微端聚灵协议，自动查询灵气存量与可用免费聚灵配额，
仅在存在免费次数时调用基础聚灵，严格遵守零元宝安全红线 (绝不元宝聚灵)。

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

# Mod 104 常量
SUCCESS = 0
FAILED = 1
NO_ENOUGH_INGOT = 2
NO_ENOUGH_LEVEL = 3
NO_ENOUGH_TIME = 4


class NimbusTask(BaseTask):
    """聚灵日常自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "NimbusTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行每日免费聚灵

        Args:
            client: 已建立的长连接客户端。
            ctx: 游戏全局运行时上下文。

        Returns:
            TaskResult: 任务执行结果。
        """
        logger.info("开始执行每日聚灵 (Nimbus) 巡检流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过聚灵任务")

        if ctx.player.level < 90:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达聚灵门槛 (90级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"nimbus": 0})

        try:
            # 1. 查询聚灵面板基础信息 (Mod 104, Act 0: nimbus_info)
            req_info = PacketBuilder(mod=104, act=0).build()
            resp_info = await client.request(req_info, timeout_sec=2.5)
            if not resp_info or len(resp_info) < 6:
                return TaskResult.skipped("聚灵面板状态同步不完整，安全跳过")

            reader = ByteArrayReader(resp_info)
            total_nimbus = reader.read_int32()
            free_times = reader.read_uint16()
            logger.info("聚灵面板同步成功: 当前灵气总值=%d, 剩余免费聚灵次数=%d", total_nimbus, free_times)

            # 2. 强前置零元宝卫语句：若免费次数已耗尽，坚决跳过
            if free_times <= 0:
                msg = f"今日聚灵免费次数已耗尽 (剩余 0 次)，零元宝安全熔断 (当前灵气: {total_nimbus})"
                logger.info(msg)
                return TaskResult.success(msg, data={"free_times": 0, "total_nimbus": total_nimbus, "gathered": False})

            # 3. 执行免费聚灵 (Mod 104, Act 1: gather_nimbus, type=0)
            req_gather = PacketBuilder(mod=104, act=1).write_int8(0).build()
            resp_gather = await client.request(req_gather, timeout_sec=2.0)
            gathered = False
            if resp_gather and len(resp_gather) >= 1:
                status = resp_gather[0]
                if status == SUCCESS:
                    gathered = True
                    logger.info("成功执行每日免费聚灵！获得海量灵气资产 (零元宝)")
                elif status in (NO_ENOUGH_INGOT, NO_ENOUGH_TIME):
                    logger.info("聚灵免费次数已用尽或元宝卫语句拦截 (状态码: %d)", status)

            msg = f"聚灵流水线完成: 聚灵操作={'成功' if gathered else '未执行/已耗尽'}, 当前灵气={total_nimbus}"
            logger.info(msg)
            return TaskResult.success(msg, data={"total_nimbus": total_nimbus, "gathered": gathered})

        except TimeoutError:
            msg = "聚灵服务响应超时，安全跳过防断连"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"timeout": True})
        except Exception as exc:
            logger.warning("聚灵流水线执行异常: %s", exc)
            return TaskResult.skipped(f"聚灵异常跳过: {exc}")
