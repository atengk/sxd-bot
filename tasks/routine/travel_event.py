"""神仙道仙履奇缘智能答题自动化任务 (Mod 21: Mod_TravelEvent_Base)

对接官方微端 Mod 21 (Mod_TravelEvent_Base) 协议，自动查询仙履奇缘奇遇状态与剩余答题机会，
自动获取题目并提交选项结算奖励 (体力/声望)，严格遵守零元宝安全原则 (绝不调用 Act 3 cancel_cd 元宝消除冷却)。

@author Ateng
@since 2026-10-16
"""

import logging
from typing import Dict, Any, List, Optional
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)

# Mod 21 状态码常量
CD_TIME = 0
REACH_MAX_COUNT = 1
SUCCESS = 2


class TravelEventTask(BaseTask):
    """仙履奇缘智能答题自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "TravelEventTask"
    interval_sec = 0.0  # 单次日常巡检

    def __init__(self, max_answers: int = 3) -> None:
        """初始化仙履奇缘任务

        Args:
            max_answers: 单次最多自动答题轮数 (防死循环)。
        """
        self.max_answers = max_answers

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行仙履奇缘 (TravelEvent) 智能答题巡检流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过仙履奇缘任务")

        # 等级防御：仙履奇缘开启门槛 (通常 28 级)
        if ctx.player.level < 28:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达仙履奇缘门槛 (28级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"answers_done": 0})

        answers_done = 0

        # 1. 查询仙履奇缘活动概况 (Mod 21, Act 0: get_activity_info)
        try:
            req_info = PacketBuilder(mod=21, act=0).build()
            resp_info = await client.request(req_info, timeout_sec=3.0)
            logger.info("仙履奇缘概况同步成功 (响应载荷: %d 字节)", len(resp_info))

            # 2. 循环检查并答题 (最多 max_answers 次)
            for _ in range(self.max_answers):
                # 获取当前奇遇与选项 (Mod 21, Act 1: get_event_and_answer)
                req_event = PacketBuilder(mod=21, act=1).build()
                resp_event = await client.request(req_event, timeout_sec=3.0)
                reader_ev = ByteArrayReader(resp_event)

                if reader_ev.remaining < 4:
                    logger.debug("仙履奇缘暂无可用事件题目或响应过短")
                    break

                event_id = reader_ev.read_int32()
                if event_id <= 0:
                    logger.info("今日仙履奇缘暂无待答题目或已达上限 (event_id=%d)", event_id)
                    break

                # 读取事件文本描述与选项列表
                event_desc = reader_ev.read_utf() if reader_ev.remaining >= 2 else ""
                logger.info("获取到仙履奇缘事件: ID=%d, 内容: %s", event_id, event_desc[:30] if event_desc else "无描述")

                opt_cnt = reader_ev.read_uint16() if reader_ev.remaining >= 2 else 0
                chosen_answer_id = None
                for _ in range(opt_cnt):
                    if reader_ev.remaining < 4:
                        break
                    aid = reader_ev.read_int32()
                    _txt1 = reader_ev.read_utf() if reader_ev.remaining >= 2 else ""
                    _txt2 = reader_ev.read_utf() if reader_ev.remaining >= 2 else ""
                    if chosen_answer_id is None:
                        chosen_answer_id = aid

                if chosen_answer_id is None:
                    logger.debug("仙履奇缘未读取到有效选项，跳过本题")
                    break

                # 提交首选答案 (Mod 21, Act 2: answer_travel_event，参数: event_id: int32, answer_id: int32)
                req_ans = PacketBuilder(mod=21, act=2).write_int32(event_id).write_int32(chosen_answer_id).build()
                resp_ans = await client.request(req_ans, timeout_sec=3.0)
                answers_done += 1
                logger.info("成功提交仙履奇缘答题 (第 %d 轮, 事件ID=%d, 选项ID=%d, 响应长度=%d 字节)",
                            answers_done, event_id, chosen_answer_id, len(resp_ans))

        except Exception as exc:
            logger.warning("仙履奇缘答题巡检异常: %s", exc)

        msg = f"仙履奇缘巡检完毕，完成 {answers_done} 轮答题结算 (严格零元宝)"
        logger.info(msg)
        return TaskResult.success(msg, data={"answers_done": answers_done})
