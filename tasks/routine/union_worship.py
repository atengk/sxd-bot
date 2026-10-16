"""神仙道仙盟上香自动化任务 (Mod 419: Mod_SaUnionWorship_Base)

对接官方微端仙盟上香祈福协议，向神坛敬奉白檀香以换取仙盟贡献度与祝福，
严格遵守零元宝安全红线 (锁定 type=0 免费/铜钱白檀香，绝不元宝敬香)。

@author Ateng
@since 2026-10-16
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)

# Mod 419 常量
COIN = 0
INGOT = 1
SUCCESS = 2
NO_COIN = 3
NO_INGOT = 4
NO_TIME = 5
ITEM_PACK_FULL = 6
JOIN_TODAY = 7
FAILED = 8


class UnionWorshipTask(BaseTask):
    """仙盟上香自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "UnionWorshipTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行仙盟免费/铜钱档白檀香敬奉

        Args:
            client: 已建立的长连接客户端。
            ctx: 游戏全局运行时上下文。

        Returns:
            TaskResult: 任务执行结果。
        """
        logger.info("开始执行仙盟上香 (SaUnionWorship) 巡检流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过仙盟上香任务")

        # 仙盟系统通常要求较高等级且已加入仙盟
        if ctx.player.level < 100:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达仙盟开启门槛 (100级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"worship": False})

        worshipped = False
        try:
            # 1. 打开仙盟上香面板同步数据 (Mod 419, Act 1: open_panel)
            req_panel = PacketBuilder(mod=419, act=1).build()
            resp_panel = await client.request(req_panel, timeout_sec=2.0)
            if not resp_panel or len(resp_panel) < 4:
                return TaskResult.skipped("仙盟上香面板状态未就绪或未加入仙盟，安全跳过")

            logger.info("仙盟上香面板同步成功 (回包长度: %d 字节)", len(resp_panel))

            # 2. 严格零元宝：锁定 COIN=0 档位白檀香敬香 (Mod 419, Act 2: worship, type=0)
            req_worship = PacketBuilder(mod=419, act=2).write_uint8(COIN).build()
            resp_worship = await client.request(req_worship, timeout_sec=2.0)
            if resp_worship and len(resp_worship) >= 1:
                status = resp_worship[0]
                if status == SUCCESS:
                    worshipped = True
                    logger.info("成功为仙盟敬奉白檀香！获得仙盟贡献与祝福 (零元宝)")
                elif status in (NO_TIME, FAILED):
                    logger.info("今日仙盟已敬过香或无剩余次数 (状态码: %d)", status)
                else:
                    logger.info("仙盟敬香返回状态码: %d", status)

            msg = f"仙盟上香流水线完成: 敬香状态={'成功完成' if worshipped else '今日已上香/已达成'} (零元宝)"
            logger.info(msg)
            return TaskResult.success(msg, data={"worshipped": worshipped})

        except TimeoutError:
            msg = "仙盟上香服务响应超时，安全跳过防断连"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"timeout": True})
        except Exception as exc:
            logger.warning("仙盟上香流水线执行异常: %s", exc)
            return TaskResult.skipped(f"仙盟上香异常跳过: {exc}")
