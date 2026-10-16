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
NOT_ENOUGH_INGOT = 15


class TakeBibleTask(BaseTask):
    """西天取经护送自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "TakeBibleTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行西天取经日常护送任务

        Args:
            client: 已建立的长连接客户端。
            ctx: 游戏全局运行时上下文。

        Returns:
            TaskResult: 任务执行结果。
        """
        logger.info("开始执行西天取经护送巡检流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过取经任务")

        # 取经功能通常 40 级以上开放
        if ctx.player.level < 40:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达取经门槛 (40级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"bible": False})

        started = False
        try:
            # 1. 查询当前护送状态与剩余次数 (Mod 30, Act 2: get_take_bible_info)
            req_info = PacketBuilder(mod=30, act=2).build()
            resp_info = await client.request(req_info, timeout_sec=2.5)
            logger.info("西天取经状态同步成功 (响应载荷: %d 字节, 十六进制: %s)", len(resp_info), resp_info.hex()[:40])

            # 2. 严格零元宝：直接调用免费启动护送 (Mod 30, Act 10: start_take_bible)
            req_start = PacketBuilder(mod=30, act=10).build()
            resp_start = await client.request(req_start, timeout_sec=2.0)
            if resp_start and len(resp_start) >= 1:
                status = resp_start[0]
                if status == SUCCESS:
                    started = True
                    logger.info("西天取经护送成功启程！将收获巨额铜钱与声望奖励 (零元宝)")
                elif status == FULL_TAKE_BIBLE_TIMES:
                    logger.info("今日西天取经免费护送次数已用尽")
                else:
                    logger.info("取经启动返回状态码: %d", status)

            msg = f"西天取经巡检完成: 取经状态={'已启动' if started else '就绪/无免费配额'} (零元宝)"
            logger.info(msg)
            return TaskResult.success(msg, data={"started": started, "bible": True})

        except TimeoutError:
            # 处于圣域城镇或非活动开放窗口时服务端不回包，安全优雅降级
            msg = "当前城镇或时段西天取经服务暂未就绪，安全跳过防断连"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"bible": False, "timeout": True})

        except Exception as exc:
            logger.warning("西天取经流水线执行异常: %s", exc)
            return TaskResult.skipped(f"西天取经异常跳过: {exc}")
