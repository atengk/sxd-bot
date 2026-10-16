"""神仙道小助手日常进度查询与活跃度宝箱全自动领取任务 (Mod 52: Mod_Assistant_Base)

支持前置状态同步查漏补缺，后置一键按阶梯提取活跃度宝箱 (体力、铜钱、经验与珍稀道具)。

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


class AssistantTask(BaseTask):
    """小助手与每日活跃度宝箱自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "AssistantTask"
    interval_sec = 0.0  # 单次日常巡检

    def __init__(self, is_post_routine: bool = True) -> None:
        """初始化小助手任务

        Args:
            is_post_routine: 是否为日常结束后的收官领取模式 (若为 False 则仅做前置状态同步)。
        """
        self.is_post_routine = is_post_routine

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行小助手状态同步与活跃度宝箱收割流水线"""
        logger.info("开始执行小助手 (Assistant) 与活跃度宝箱巡检流水线 (后置领取=%s)...", self.is_post_routine)

        if not ctx.is_connected:
            return TaskResult.skipped("未处于有效长连接状态，跳过小助手任务")

        try:
            # 1. 查询小助手面板全量状态与当前活跃度 (Mod 52, Act 0: info)
            req_info = PacketBuilder(mod=52, act=0).build()
            resp_info = await client.request(req_info, timeout_sec=2.5)
            logger.info("小助手面板数据同步成功 (响应载荷: %d 字节)", len(resp_info))

            claimed_boxes = 0

            # 2. 若处于后置收官阶段，依次遍历 5 个活跃度宝箱档位并全额收割 (Mod 52, Act 1: get_award)
            if self.is_post_routine:
                for box_id in range(1, 6):
                    try:
                        req_get = PacketBuilder(mod=52, act=1).write_int32(box_id).build()
                        resp_get = await client.request(req_get, timeout_sec=2.0)
                        if resp_get and len(resp_get) >= 1:
                            status = resp_get[0]
                            if status == 0:  # SUCCESS
                                claimed_boxes += 1
                                items_cnt = 0
                                if len(resp_get) >= 3:
                                    items_cnt = (resp_get[1] << 8) | resp_get[2]
                                logger.info("成功开启第 %d 档每日活跃度宝箱！包含 %d 项战利品", box_id, items_cnt)
                            elif status == 4:  # HAVE_DONE
                                logger.debug("第 %d 档活跃度宝箱今日已领取过", box_id)
                            elif status == 2:  # NOT_ENOUGH_NUM (活跃度未达标)
                                logger.debug("当前活跃度尚未达到第 %d 档阈值，后续档位跳过", box_id)
                                break
                            else:
                                logger.debug("第 %d 档宝箱返回状态: %d", box_id, status)
                    except Exception as e:
                        logger.debug("宝箱 %d 提取异常: %s", box_id, e)

            msg = f"小助手巡检完成: 状态已同步 ({len(resp_info)} 字节)，已领活跃度宝箱: {claimed_boxes} 个"
            logger.info(msg)
            return TaskResult.success(msg, data={"claimed_boxes": claimed_boxes, "info_len": len(resp_info)})

        except Exception as exc:
            logger.warning("小助手功能巡检异常 (安全跳过): %s", exc)
            return TaskResult.skipped(f"小助手暂不可用: {exc}")
