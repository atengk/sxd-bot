"""神仙道五福临门节庆福利自动化任务 (Mod 400: Mod_FiveFu_Base)

对接官方微端五福临门活动协议，探测运营活动开放状态，
自动开启每日免费福卡礼包并合成大礼包，非活动期安全静默跳过 (零元宝消耗)。

@author Ateng
@since 2026-10-16
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)

# Mod 400 常量
SUCCESS = 0
PACK_FULL = 1
NOACTIVITY = 2


class FiveFuTask(BaseTask):
    """五福临门节庆福利自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "FiveFuTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行五福临门活动探测与福袋收割

        Args:
            client: 已建立的长连接客户端。
            ctx: 游戏全局运行时上下文。

        Returns:
            TaskResult: 任务执行结果。
        """
        logger.info("开始执行五福临门 (FiveFu) 运营活动巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过五福临门任务")

        try:
            # 1. 尝试开启每日福卡礼包 (Mod 400, Act 1: open_pack)
            req_open = PacketBuilder(mod=400, act=1).build()
            resp_open = await client.request(req_open, timeout_sec=2.0)
            if not resp_open or len(resp_open) == 0:
                return TaskResult.skipped("五福临门服务端未响应，安全跳过")

            status = resp_open[0]
            if status == NOACTIVITY:
                msg = "五福临门当前非活动开放时段，日常安全跳过"
                logger.info(msg)
                return TaskResult.skipped(msg, data={"active": False})

            opened = False
            composed = False
            if status == SUCCESS:
                opened = True
                logger.info("成功领取并开启今日免费五福礼包！")

                # 2. 尝试合成大五福 (Mod 400, Act 3: compose_fu)
                try:
                    req_compose = PacketBuilder(mod=400, act=3).build()
                    resp_compose = await client.request(req_compose, timeout_sec=2.0)
                    if resp_compose and resp_compose[0] == SUCCESS:
                        composed = True
                        logger.info("五福卡片已集齐，成功合成大五福并领取奖励！")
                        # 3. 尝试开启大五福礼包
                        await client.send_packet(PacketBuilder(mod=400, act=5).build())
                except Exception as comp_err:
                    logger.debug("合成五福跳过: %s", comp_err)

            msg = f"五福临门巡检完成: 活动进行中，开福卡={'成功' if opened else '已领过'}，五福合成={'成功' if composed else '卡片不足'}"
            logger.info(msg)
            return TaskResult.success(msg, data={"active": True, "opened": opened, "composed": composed})

        except TimeoutError:
            msg = "五福临门活动网关超时，安全跳过防断连"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"active": False, "timeout": True})
        except Exception as exc:
            logger.warning("五福临门流水线异常: %s", exc)
            return TaskResult.skipped(f"五福临门异常跳过: {exc}")
