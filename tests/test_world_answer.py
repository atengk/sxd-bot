"""神仙道世界问答 (World Answer) 题库检索、极限抢答与自愈学习单元测试套件

测试覆盖:
1. WorldAnswerBank 本地精准匹配、字数硬约束与关键词模糊匹配
2. WorldAnswerBank 自愈学习 (Self-Healing) 与原子持久化机制
3. Mod 164 二进制广播帧编解码 (Act 0 告警, Act 1 出题, Act 2 结算)
4. Mod 6 世界频道抢答封包构造规约
5. WorldAnswerTask 完整异步生命周期与 5 分钟超时看门狗测试

@author Ateng
@since 2026-10-17
"""

import asyncio
import json
import os
import shutil
import struct
import tempfile
import unittest
from unittest.mock import AsyncMock, MagicMock

from core.context import GameContext
from core.events import EventBus
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader, ByteArrayWriter
from tasks.routine.world_answer import (
    WorldAnswerBank,
    WorldAnswerTask,
    ACT_NOTIFY_ALARM,
    ACT_NOTIFY_QUESTION,
    ACT_NOTIFY_RESULT,
    MOD_CHAT,
    ACT_CHAT_WITH_PLAYERS,
    CHAT_CHANNEL_WORLD,
)


class TestWorldAnswerBank(unittest.TestCase):
    """题库匹配与自愈学习测试"""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        self.bank_file = os.path.join(self.test_dir, "test_bank.json")

        initial_data = {
            "_meta": {"description": "Unit Test Bank"},
            "questions": [
                {
                    "question": "孙悟空的大师傅是谁？",
                    "keywords": ["孙悟空", "大师傅"],
                    "answer": "菩提祖师",
                    "length": 4,
                },
                {
                    "question": "白龙马原来是哪里的三太子？",
                    "keywords": ["白龙马", "三太子"],
                    "answer": "西海",
                    "length": 2,
                },
                {
                    "question": "主角多少级开启封灵系统？",
                    "keywords": ["主角", "封灵", "等级"],
                    "answer": "70",
                    "length": 2,
                },
            ],
        }
        with open(self.bank_file, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, ensure_ascii=False)

        self.bank = WorldAnswerBank(self.bank_file)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_exact_match(self) -> None:
        """测试精准题干匹配"""
        ans = self.bank.match_answer("孙悟空的大师傅是谁？", 4)
        self.assertEqual(ans, "菩提祖师")

        ans_no_punct = self.bank.match_answer("孙悟空的大师傅是谁", 4)
        self.assertEqual(ans_no_punct, "菩提祖师")

    def test_length_constraint_filtering(self) -> None:
        """测试字数硬约束过滤 (字数不符坚决不匹配)"""
        ans = self.bank.match_answer("孙悟空的大师傅是谁？", 3)
        self.assertIsNone(ans)

    def test_fuzzy_keyword_match(self) -> None:
        """测试包含关键词的变体题目模糊匹配"""
        ans = self.bank.match_answer("请问西游记中孙悟空的大师傅叫什么名", 4)
        self.assertEqual(ans, "菩提祖师")

    def test_unmatched_question(self) -> None:
        """测试生题未收录返回 None"""
        ans = self.bank.match_answer("天王盖地虎的下一句是什么", 5)
        self.assertIsNone(ans)

    def test_self_healing_learning(self) -> None:
        """测试自愈学习并持久化写回磁盘"""
        new_q = "唐僧西天取经取得是什么经？"
        new_ans = "大乘真经"
        new_len = 4

        # 初始未收录
        self.assertIsNone(self.bank.match_answer(new_q, new_len))

        # 触发自愈学习
        learned = self.bank.learn_answer(new_q, new_len, new_ans)
        self.assertTrue(learned)

        # 验证内存已能命中
        self.assertEqual(self.bank.match_answer(new_q, new_len), new_ans)

        # 重新创建 Bank 实例验证磁盘物理持久化成功
        new_bank_instance = WorldAnswerBank(self.bank_file)
        self.assertEqual(new_bank_instance.match_answer(new_q, new_len), new_ans)


class TestWorldAnswerProtocol(unittest.TestCase):
    """二进制数据包序列化与编解码测试"""

    def test_mod164_act0_alarm_payload(self) -> None:
        """测试 Act 0 告警广播载荷解析"""
        writer = ByteArrayWriter()
        writer.write_int32(60)
        payload = writer.to_bytes()

        reader = ByteArrayReader(payload)
        countdown = reader.read_int32()
        self.assertEqual(countdown, 60)

    def test_mod164_act1_question_payload(self) -> None:
        """测试 Act 1 出题广播载荷解析"""
        writer = ByteArrayWriter()
        writer.write_utf("孙悟空的大师傅是谁？")
        writer.write_int8(4)
        payload = writer.to_bytes()

        reader = ByteArrayReader(payload)
        question = reader.read_utf()
        length = reader.read_int8()
        self.assertEqual(question, "孙悟空的大师傅是谁？")
        self.assertEqual(length, 4)

    def test_mod164_act2_result_payload(self) -> None:
        """测试 Act 2 结算与获奖榜单载荷解析"""
        writer = ByteArrayWriter()
        writer.write_utf("菩提祖师")
        writer.write_uint16(2)  # 2 位获奖者
        # 获奖者 1
        writer.write_int32(1001)
        writer.write_utf("齐天大圣")
        writer.write_int8(1)
        # 获奖者 2
        writer.write_int32(1002)
        writer.write_utf("二郎真君")
        writer.write_int8(2)
        # 答对总人数
        writer.write_int32(15)

        payload = writer.to_bytes()

        reader = ByteArrayReader(payload)
        ans = reader.read_utf()
        cnt = reader.read_uint16()
        players = []
        for _ in range(cnt):
            pid = reader.read_int32()
            pname = reader.read_utf()
            rank = reader.read_int8()
            players.append((pid, pname, rank))
        total = reader.read_int32()

        self.assertEqual(ans, "菩提祖师")
        self.assertEqual(cnt, 2)
        self.assertEqual(players[0], (1001, "齐天大圣", 1))
        self.assertEqual(players[1], (1002, "二郎真君", 2))
        self.assertEqual(total, 15)

    def test_mod6_act0_chat_packet_structure(self) -> None:
        """测试 Mod 6 世界频道抢答封包二进制结构"""
        packet = (
            PacketBuilder(mod=MOD_CHAT, act=ACT_CHAT_WITH_PLAYERS)
            .write_uint8(CHAT_CHANNEL_WORLD)
            .write_utf("菩提祖师")
            .write_utf("")
            .write_utf("")
            .build()
        )
        self.assertEqual(packet.mod, 6)
        self.assertEqual(packet.act, 0)

        reader = ByteArrayReader(packet.payload)
        channel = reader.read_uint8()
        msg = reader.read_utf()
        to_player = reader.read_utf()
        token = reader.read_utf()

        self.assertEqual(channel, CHAT_CHANNEL_WORLD)
        self.assertEqual(msg, "菩提祖师")
        self.assertEqual(to_player, "")
        self.assertEqual(token, "")


class TestWorldAnswerTaskLifecycle(unittest.IsolatedAsyncioTestCase):
    """WorldAnswerTask 异步生命周期集成测试"""

    async def asyncSetUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        self.bank_file = os.path.join(self.test_dir, "test_bank.json")
        with open(self.bank_file, "w", encoding="utf-8") as f:
            json.dump({
                "questions": [
                    {
                        "question": "二郎神身边的那条神犬叫什么？",
                        "keywords": ["二郎神", "神犬"],
                        "answer": "哮天犬",
                        "length": 3,
                    }
                ]
            }, f)
        self.bank = WorldAnswerBank(self.bank_file)

        self.ctx = GameContext()
        self.ctx.set_connected(True)
        self.ctx.player.player_id = 8888
        self.ctx.player.nickname = "太上老君"

        self.event_bus = EventBus()
        self.client = MagicMock(spec=SXDClient)
        self.client.event_bus = self.event_bus
        self.client.send_packet = AsyncMock()

    async def asyncTearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    async def test_successful_quiz_flow(self) -> None:
        """测试完整答题流水线：告警 -> 出题抢答 -> 结算上榜"""
        task = WorldAnswerTask(bank=self.bank, watchdog_timeout_sec=5.0)

        # 启动任务执行协程
        exec_coro = asyncio.create_task(task.execute(self.client, self.ctx))
        await asyncio.sleep(0.05)  # 等待监听器注册

        # 1. 模拟收到 1 分钟倒计时告警 (Act 0)
        alarm_writer = ByteArrayWriter()
        alarm_writer.write_int32(60)
        await self.event_bus.emit(164, ACT_NOTIFY_ALARM, alarm_writer.to_bytes())
        await asyncio.sleep(0.02)
        self.assertTrue(task.is_silenced)

        # 2. 模拟收到正式题目 (Act 1)
        q_writer = ByteArrayWriter()
        q_writer.write_utf("二郎神身边的那条神犬叫什么？")
        q_writer.write_int8(3)
        await self.event_bus.emit(164, ACT_NOTIFY_QUESTION, q_writer.to_bytes())
        await asyncio.sleep(0.02)

        # 验证抢发封包已被下发至 client.send_packet
        self.client.send_packet.assert_awaited_once()
        sent_packet = self.client.send_packet.call_args[0][0]
        self.assertEqual(sent_packet.mod, 6)
        self.assertEqual(sent_packet.act, 0)
        self.assertEqual(task.submitted_answer, "哮天犬")

        # 3. 模拟收到结算广播 (Act 2)，本角色荣登全服第 1 名
        res_writer = ByteArrayWriter()
        res_writer.write_utf("哮天犬")
        res_writer.write_uint16(1)
        res_writer.write_int32(8888)  # 匹配本号 player_id
        res_writer.write_utf("太上老君")
        res_writer.write_int8(1)      # 第 1 名
        res_writer.write_int32(8)

        await self.event_bus.emit(164, ACT_NOTIFY_RESULT, res_writer.to_bytes())

        # 等待任务退出
        result = await exec_coro
        self.assertTrue(result.is_success)
        self.assertTrue(task.is_my_answer_awarded)
        self.assertEqual(task.award_rank, 1)
        self.assertFalse(task.is_silenced)

    async def test_unmatched_and_self_healing_flow(self) -> None:
        """测试生题静默防御与结算后自愈学习流程"""
        task = WorldAnswerTask(bank=self.bank, watchdog_timeout_sec=5.0)

        exec_coro = asyncio.create_task(task.execute(self.client, self.ctx))
        await asyncio.sleep(0.05)

        # 1. 收到未收录的新题目
        q_writer = ByteArrayWriter()
        q_writer.write_utf("神雕侠侣中小龙女的丈夫是谁？")
        q_writer.write_int8(2)
        await self.event_bus.emit(164, ACT_NOTIFY_QUESTION, q_writer.to_bytes())
        await asyncio.sleep(0.02)

        # 静默防御，不调用 send_packet
        self.client.send_packet.assert_not_awaited()
        self.assertIsNone(task.submitted_answer)

        # 2. 收到官方结算广播
        res_writer = ByteArrayWriter()
        res_writer.write_utf("杨过")
        res_writer.write_uint16(0)
        res_writer.write_int32(0)
        await self.event_bus.emit(164, ACT_NOTIFY_RESULT, res_writer.to_bytes())

        result = await exec_coro
        self.assertTrue(result.is_success)

        # 验证新题目已被自愈学习收录至题库
        self.assertEqual(self.bank.match_answer("神雕侠侣中小龙女的丈夫是谁？", 2), "杨过")

    async def test_watchdog_timeout(self) -> None:
        """测试 5 分钟超时看门狗熔断 (未出题时安全退出)"""
        task = WorldAnswerTask(bank=self.bank, watchdog_timeout_sec=0.2)  # 测试微缩超时
        result = await task.execute(self.client, self.ctx)

        self.assertEqual(result.status.value, "skipped")
        self.assertTrue(result.data.get("timed_out"))


if __name__ == "__main__":
    unittest.main()
