"""神仙道世界问答限时抢答与自愈题库自动化任务 (Mod 164 & Mod 6)

监听 Mod 164 服务端下行广播，捕获 1 分钟告警激活世界频道发言静默保护，
收到题目推送后毫秒级检索本地题库并向 Mod 6 世界频道发起零延迟抢答，
并在答题结算广播中自动学习并写回新题答案，支持 5 分钟超时看门狗安全熔断。

@author Ateng
@since 2026-10-17
"""

import asyncio
import json
import logging
import os
import re
from typing import Dict, Any, List, Optional, Tuple

from core.context import GameContext
from core.events import EventBus
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader
from tasks.base import BaseTask, TaskResult

logger = logging.getLogger(__name__)

# Mod 164 动作编号
ACT_NOTIFY_ALARM = 0       # notify_answer_will_begin_after_one_minute
ACT_NOTIFY_QUESTION = 1    # notify_question
ACT_NOTIFY_RESULT = 2      # notify_result_and_award_player_list

# Mod 6 动作与频道常量
MOD_CHAT = 6
ACT_CHAT_WITH_PLAYERS = 0
CHAT_CHANNEL_WORLD = 1     # 世界频道

DEFAULT_BANK_PATH = os.path.join("data", "world_answer_bank.json")


class WorldAnswerBank:
    """世界问答本地题库匹配与自愈持久化引擎

    @author Ateng
    @since 2026-10-17
    """

    def __init__(self, file_path: str = DEFAULT_BANK_PATH) -> None:
        """初始化题库引擎

        Args:
            file_path: 题库文件物理路径。
        """
        self.file_path = file_path
        self._questions: List[Dict[str, Any]] = []
        self._lock = asyncio.Lock()
        self.load()

    def load(self) -> None:
        """从本地 JSON 文件加载题库数据"""
        if not os.path.exists(self.file_path):
            logger.warning("题库文件不存在: %s，将初始化为空题库", self.file_path)
            self._questions = []
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = json.load(f)
                self._questions = content.get("questions", [])
            logger.debug("世界问答题库加载成功，共 %d 道题目", len(self._questions))
        except Exception as exc:
            logger.error("世界问答题库加载失败: %s", exc)
            self._questions = []

    def _normalize_text(self, text: str) -> str:
        """归一化题目文本，去除标点符号与空白字符"""
        return re.sub(r"[^\w\u4e00-\u9fa5]", "", text)

    def match_answer(self, question: str, expected_length: int) -> Optional[str]:
        """依据题目文本与字数硬约束检索最佳答案

        Args:
            question: 服务端推送的原始题目字符串。
            expected_length: 官方提示的答案字数约束。

        Returns:
            若成功匹配返回答案字符串，未命中则返回 None。
        """
        if not question:
            return None

        norm_q = self._normalize_text(question)

        # 1. 优先执行全文本精准匹配与字数校验
        for item in self._questions:
            item_q = self._normalize_text(item.get("question", ""))
            item_ans = item.get("answer", "")
            item_len = item.get("length", len(item_ans))

            if expected_length > 0 and item_len != expected_length:
                continue

            if norm_q and norm_q == item_q:
                logger.info("精准命中题库题目: '%s' -> 答案: '%s'", question, item_ans)
                return item_ans

        # 2. 次选执行关键词重合度模糊匹配 (仅在字数吻合的候选中比对)
        best_candidate: Optional[str] = None
        highest_score = 0

        for item in self._questions:
            item_ans = item.get("answer", "")
            item_len = item.get("length", len(item_ans))
            if expected_length > 0 and item_len != expected_length:
                continue

            keywords = item.get("keywords", [])
            score = 0
            for kw in keywords:
                if kw and kw in norm_q:
                    score += len(kw)

            # 也比对原题干的重合字符数
            item_q = self._normalize_text(item.get("question", ""))
            common_chars = sum(1 for ch in norm_q if ch in item_q)
            score += common_chars

            if score > highest_score and score >= 4:
                highest_score = score
                best_candidate = item_ans

        if best_candidate:
            logger.info("模糊命中题库候选: '%s' (匹配分: %d) -> 答案: '%s'", question, highest_score, best_candidate)
            return best_candidate

        logger.warning("未命中题库题目: '%s' (要求字数: %d)", question, expected_length)
        return None

    def learn_answer(self, question: str, expected_length: int, answer: str) -> bool:
        """自愈学习：将服务端广播的真实正确答案录入题库并持久化

        Args:
            question: 题目文本。
            expected_length: 答案字数。
            answer: 官方公布的正确答案。

        Returns:
            若新增学习成功返回 True，若已存在返回 False。
        """
        if not question or not answer:
            return False

        norm_q = self._normalize_text(question)

        # 1. 检查是否已收录
        for item in self._questions:
            if self._normalize_text(item.get("question", "")) == norm_q:
                # 若答案有变动则更新
                if item.get("answer") != answer:
                    item["answer"] = answer
                    item["length"] = len(answer)
                    self._save_atomic()
                    logger.info("题库已修正题目答案: '%s' -> '%s'", question, answer)
                    return True
                return False

        # 2. 提取关键词并追加新条目
        # 简单提取 2 字及以上的连续汉字作为关键词
        raw_words = re.findall(r"[\u4e00-\u9fa5]{2,}", question)
        keywords = list(dict.fromkeys(raw_words))[:4]

        new_entry = {
            "question": question,
            "keywords": keywords,
            "answer": answer,
            "length": expected_length if expected_length > 0 else len(answer),
        }
        self._questions.append(new_entry)
        self._save_atomic()
        logger.info("自愈学习成功收录新题目: '%s' -> 答案: '%s' (长度: %d)", question, answer, new_entry["length"])
        return True

    def _save_atomic(self) -> None:
        """原子写入磁盘保存题库，防止并发写损坏"""
        os.makedirs(os.path.dirname(os.path.abspath(self.file_path)), exist_ok=True)
        temp_file = f"{self.file_path}.tmp"
        payload = {
            "_meta": {
                "description": "神仙道世界问答本地题库 (World Answer Bank)",
                "total_questions": len(self._questions),
            },
            "questions": self._questions,
        }
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            os.replace(temp_file, self.file_path)
            logger.debug("题库持久化保存成功 (共 %d 题)", len(self._questions))
        except Exception as exc:
            logger.error("题库持久化写入失败: %s", exc)
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except OSError:
                    pass


class WorldAnswerTask(BaseTask):
    """神仙道世界问答限时抢答自动化任务

    @author Ateng
    @since 2026-10-17
    """

    name = "WorldAnswerTask"
    interval_sec = 0.0  # 依托网络事件与看门狗触发

    def __init__(
        self,
        bank: Optional[WorldAnswerBank] = None,
        watchdog_timeout_sec: float = 300.0,
    ) -> None:
        """初始化世界问答任务

        Args:
            bank: 题库匹配与自愈实例。
            watchdog_timeout_sec: 独立任务执行最大看门狗超时时间 (默认 5 分钟)。
        """
        self.bank = bank or WorldAnswerBank()
        self.watchdog_timeout_sec = watchdog_timeout_sec

        # 运行时状态感知
        self.is_silenced: bool = False
        self.last_question: str = ""
        self.last_expected_length: int = 0
        self.submitted_answer: Optional[str] = None
        self.official_answer: Optional[str] = None
        self.is_my_answer_awarded: bool = False
        self.award_rank: Optional[int] = None
        self.award_players: List[Tuple[int, str, int]] = []
        self.total_correct_count: int = 0

        self._completion_future: Optional[asyncio.Future] = None

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行世界问答监听与抢答流水线

        Args:
            client: 具备请求发送与长连接能力的客户端。
            ctx: 当前全局上下文只读状态池。

        Returns:
            TaskResult 任务执行状态与战报结果。
        """
        logger.info("开始部署世界问答 (World Answer) 事件监听流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过世界问答任务")

        # 1. 注册 Mod 164 事件总线监听器
        loop = asyncio.get_running_loop()
        self._completion_future = loop.create_future()

        event_bus = client.event_bus

        async def _on_alarm_event(mod: int, act: int, payload: bytes) -> None:
            self._handle_alarm(payload)

        async def _on_question_event(mod: int, act: int, payload: bytes) -> None:
            await self._handle_question(client, payload)

        async def _on_result_event(mod: int, act: int, payload: bytes) -> None:
            self._handle_result(ctx, payload)

        event_bus.subscribe(164, ACT_NOTIFY_ALARM, _on_alarm_event)
        event_bus.subscribe(164, ACT_NOTIFY_QUESTION, _on_question_event)
        event_bus.subscribe(164, ACT_NOTIFY_RESULT, _on_result_event)

        logger.info("已成功订阅 Mod 164 问答全系广播 (Act 0 告警, Act 1 题目, Act 2 结算)")

        # 2. 启动 5 分钟超时看门狗挂起等待答题流程结束
        try:
            logger.info("进入世界问答看门狗等待窗口 (最大等待时间: %.1fs)...", self.watchdog_timeout_sec)
            await asyncio.wait_for(self._completion_future, timeout=self.watchdog_timeout_sec)
        except asyncio.TimeoutError:
            logger.warning("世界问答看门狗超时 (%.1fs 未收到出题或结算)，优雅退出", self.watchdog_timeout_sec)
            return TaskResult.skipped(
                f"在等待窗口 ({int(self.watchdog_timeout_sec)}s) 内未检测到世界问答活动广播",
                data={"submitted_answer": self.submitted_answer, "timed_out": True},
            )
        finally:
            # 3. 清理事件监听器，保持总线干净无泄漏
            self._cleanup_listeners(event_bus, _on_alarm_event, _on_question_event, _on_result_event)

        # 4. 汇总战报输出
        msg = self._build_summary_message()
        logger.info(msg)

        return TaskResult.success(
            msg,
            data={
                "question": self.last_question,
                "expected_length": self.last_expected_length,
                "submitted_answer": self.submitted_answer,
                "official_answer": self.official_answer,
                "is_awarded": self.is_my_answer_awarded,
                "rank": self.award_rank,
                "total_correct": self.total_correct_count,
            },
        )

    def _handle_alarm(self, payload: bytes) -> None:
        """处理 1 分钟倒计时前置告警 (Act 0)"""
        reader = ByteArrayReader(payload)
        countdown = reader.read_int32() if reader.remaining >= 4 else 60
        self.is_silenced = True
        logger.info("【世界问答】收到系统出题告警！将在 1 分钟后正式出题 (倒计时: %d 秒)，已激活世界频道发言静默保护", countdown)

    async def _handle_question(self, client: SXDClient, payload: bytes) -> None:
        """处理题目广播并实施极限抢答 (Act 1)"""
        try:
            reader = ByteArrayReader(payload)
            question = reader.read_utf() if reader.remaining >= 2 else ""
            expected_length = reader.read_int8() if reader.remaining >= 1 else 0

            self.last_question = question
            self.last_expected_length = expected_length
            logger.info("【世界问答】收到正式题目广播: '%s' | 要求字数: %d 字", question, expected_length)

            # 1. 毫秒级匹配题库
            matched_ans = self.bank.match_answer(question, expected_length)
            if not matched_ans:
                logger.info("【世界问答】题库未收录本题，答题阶段采取静默防御 (不乱猜乱发，等待结算自动学习)")
                return

            self.submitted_answer = matched_ans

            # 2. 组装 Mod 6 世界频道发送封包实施零延迟抢答
            chat_packet = (
                PacketBuilder(mod=MOD_CHAT, act=ACT_CHAT_WITH_PLAYERS)
                .write_uint8(CHAT_CHANNEL_WORLD)   # 频道: 世界
                .write_utf(matched_ans)            # 答案消息
                .write_utf("")                     # 目标玩家 (无)
                .write_utf("")                     # 校验令牌 (无)
                .build()
            )

            # 3. 瞬间抢发
            await client.send_packet(chat_packet)
            logger.info("【世界问答】零延迟极限抢答已发出！世界频道文本: '%s' (字数: %d)", matched_ans, len(matched_ans))

        except Exception as exc:
            logger.error("【世界问答】题目处理与抢答异常: %s", exc)

    def _handle_result(self, ctx: GameContext, payload: bytes) -> None:
        """处理结算广播与自学习 (Act 2)"""
        try:
            reader = ByteArrayReader(payload)
            official_answer = reader.read_utf() if reader.remaining >= 2 else ""
            self.official_answer = official_answer

            # 读取前十名获奖玩家名单
            player_cnt = reader.read_uint16() if reader.remaining >= 2 else 0
            award_list: List[Tuple[int, str, int]] = []
            for _ in range(player_cnt):
                if reader.remaining < 4:
                    break
                pid = reader.read_int32()
                pname = reader.read_utf() if reader.remaining >= 2 else ""
                rank = reader.read_int8() if reader.remaining >= 1 else 0
                award_list.append((pid, pname, rank))

            total_correct = reader.read_int32() if reader.remaining >= 4 else len(award_list)

            self.award_players = award_list
            self.total_correct_count = total_correct

            logger.info("【世界问答】收到官方结算广播！正确答案: '%s' | 答对玩家总数: %d | 前十上榜数: %d",
                        official_answer, total_correct, len(award_list))

            # 1. 检查自身是否荣登前十名
            my_pid = ctx.player.player_id
            for pid, pname, rank in award_list:
                if pid == my_pid:
                    self.is_my_answer_awarded = True
                    self.award_rank = rank
                    logger.info("恭喜！本角色荣登世界问答全服排行榜第 %d 名 (斩获智多星礼包)！", rank)
                    break

            # 2. 触发自愈学习：若题目库尚未收录或答案不准确，自动追加持久化
            if self.last_question and official_answer:
                self.bank.learn_answer(self.last_question, self.last_expected_length, official_answer)

        except Exception as exc:
            logger.error("【世界问答】结算广播解析异常: %s", exc)
        finally:
            self.is_silenced = False
            if self._completion_future and not self._completion_future.done():
                self._completion_future.set_result(True)

    def _cleanup_listeners(
        self,
        event_bus: EventBus,
        on_alarm: Any,
        on_question: Any,
        on_result: Any,
    ) -> None:
        """清理已订阅的监听器句柄"""
        if (164, ACT_NOTIFY_ALARM) in event_bus._listeners:
            event_bus._listeners[(164, ACT_NOTIFY_ALARM)] = [
                h for h in event_bus._listeners[(164, ACT_NOTIFY_ALARM)] if h != on_alarm
            ]
        if (164, ACT_NOTIFY_QUESTION) in event_bus._listeners:
            event_bus._listeners[(164, ACT_NOTIFY_QUESTION)] = [
                h for h in event_bus._listeners[(164, ACT_NOTIFY_QUESTION)] if h != on_question
            ]
        if (164, ACT_NOTIFY_RESULT) in event_bus._listeners:
            event_bus._listeners[(164, ACT_NOTIFY_RESULT)] = [
                h for h in event_bus._listeners[(164, ACT_NOTIFY_RESULT)] if h != on_result
            ]

    def _build_summary_message(self) -> str:
        """构建战报字符串"""
        if self.is_my_answer_awarded:
            return (
                f"世界问答圆满成功！正确答案: '{self.official_answer}'，"
                f"角色荣登全服第 {self.award_rank} 名，成功夺得智多星礼包奖励！"
            )
        elif self.submitted_answer:
            return (
                f"世界问答抢答完毕。提交答案: '{self.submitted_answer}'，"
                f"官方答案: '{self.official_answer}' (全服答对共 {self.total_correct_count} 人)。"
            )
        else:
            return (
                f"世界问答巡检完毕。题目: '{self.last_question}'，"
                f"官方答案: '{self.official_answer}' (未收录生题已自动反哺题库)。"
            )
