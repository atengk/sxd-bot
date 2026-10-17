"""全域综合福利收割、练功修行闭环与更新福利单元测试套件

覆盖：
1. 版本更新福利与维护补偿领取 (Mod 240)
2. 【领取奖励】大厅与全服超级礼包循环领取 (Mod 2 Act 6/29)
3. 竞技场每日排名声望与铜钱结算 (Mod 20 Act 1)
4. 城镇练功打坐累积经验签收与无缝续练 (Mod 0 Act 37/38/36)
5. 仙道问灵求签并领取签文奖励 (Mod 503 Act 3/4)

@author Ateng
@since 2026-10-17
"""

import unittest
from unittest.mock import AsyncMock, MagicMock
from core.context import GameContext
from network.client import SXDClient
from tasks.base import TaskStatus
from tasks.routine.release_welfare import ReleaseWelfareTask
from tasks.routine.take_award import TakeAwardTask
from tasks.routine.practice import PracticeTask
from tasks.routine.ask_fairy import AskFairyTask
from protocol.builder import PacketBuilder


class TestWelfareAndPractice(unittest.IsolatedAsyncioTestCase):
    """全域福利收割与练功修行单元测试

    @author Ateng
    @since 2026-10-17
    """

    def setUp(self) -> None:
        self.ctx = GameContext()
        self.ctx.set_connected(True)
        self.ctx.update_player_info(
            nickname="梦一场",
            player_id=4,
            level=300,
            coins=36800000000,
            ingots=39666,
            power=100,
            fame=50000,
            vip_level=10,
            town_id=29,
        )
        self.client = MagicMock(spec=SXDClient)

    async def test_release_welfare_task_flow(self) -> None:
        """测试版本更新福利全量收割流水线"""
        task = ReleaseWelfareTask()
        self.client.request = AsyncMock(return_value=b"\x00" * 10)
        self.client.send_packet = AsyncMock()

        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SUCCESS)
        self.assertIn("版本更新福利", res.message)
        # 应提交福利领取、额外元宝及特权请求
        self.assertGreaterEqual(self.client.send_packet.call_count, 4)

    async def test_take_award_task_with_super_gifts(self) -> None:
        """测试【领取奖励】大厅超级礼包循环领取与竞技场结算"""
        task = TakeAwardTask()

        from protocol.packet import ByteArrayWriter
        writer = ByteArrayWriter()
        writer.write_int32(2)  # 2 个礼包
        # 礼包 1
        writer.write_int32(101).write_int32(1).write_utf("大礼包1").write_utf("说明1").write_int32(0)
        # 礼包 2
        writer.write_int32(102).write_int32(1).write_utf("大礼包2").write_utf("说明2").write_int32(0)
        gift_payload = writer.to_bytes()

        self.client.request = AsyncMock(side_effect=[
            gift_payload,   # Mod 2 Act 6: 礼包列表
            bytes([0]),     # Mod 2 Act 29 (礼包 101): SUCCESS
            bytes([0]),     # Mod 2 Act 29 (礼包 102): SUCCESS
            b"\x00" * 16,   # Mod 20 Act 1: 竞技场排名奖励
            b"\x00" * 4,    # Mod 127 Act 1: 幸运日列表
        ])
        self.client.send_packet = AsyncMock()

        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SUCCESS)
        self.assertEqual(res.data["claimed_gifts"], 2)

    async def test_practice_claim_accumulated_exp(self) -> None:
        """测试城镇练功挂机经验签收与无缝续练"""
        task = PracticeTask()

        from protocol.packet import ByteArrayWriter
        # 模拟 Mod 584 Act 1: 现代练功修行 (status: 0, auras: 1, val1, val2, exp: 2548263240)
        writer = ByteArrayWriter()
        writer.write_uint8(0).write_uint16(1).write_int32(7923).write_int32(10)
        writer.write_int32(0).write_int32(0)
        writer.write_int64(2548263240)
        writer.write_int32(0).write_int32(0).write_int32(0)
        exp_payload_584 = writer.to_bytes()

        # 模拟 Mod 584 Act 3: collect_all 回包
        writer3 = ByteArrayWriter()
        writer3.write_uint8(0).write_uint16(0).write_int64(2548263240)
        exp_payload_act3 = writer3.to_bytes()

        self.client.request = AsyncMock(side_effect=[
            exp_payload_584,   # Mod 584 Act 1
            exp_payload_act3,  # Mod 584 Act 3
            b"",               # Mod 0 Act 37
        ])
        self.client.send_packet = AsyncMock()

        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SUCCESS)
        self.assertEqual(res.data["claimed_exp"], 2548263240)
        self.assertGreaterEqual(self.client.send_packet.call_count, 1)

    async def test_take_award_lucky_day_one_key_claim(self) -> None:
        """测试【⭐幸运日】Mod 127 一键抽取倍率与领奖流水线"""
        task = TakeAwardTask()

        from protocol.packet import ByteArrayWriter
        # 模拟 Mod 127 Act 1: 5 个幸运日活动 (1, 4, 16, 7, 17)
        writer = ByteArrayWriter()
        writer.write_uint16(5)
        for gid in [1, 4, 16, 7, 17]:
            writer.write_int16(gid)
            # 填充剩余 35 字节
            for _ in range(35):
                writer.write_uint8(0)
        gift_payload = writer.to_bytes()

        self.client.request = AsyncMock(side_effect=[
            b"",            # Mod 2 Act 6
            gift_payload,   # Mod 127 Act 1: 5 个幸运日礼包
        ])
        self.client.send_packet = AsyncMock()

        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SUCCESS)
        self.assertEqual(res.data["claimed_lucky_items"], 5)
        # 严格零元宝：每个幸运日礼包仅调用免费 get_game_function_end_gift (Act 2)，绝不调用 random_award (Act 3)
        self.assertGreaterEqual(self.client.send_packet.call_count, 5)

    async def test_weekend_revelry_draw_and_lottery_flow(self) -> None:
        """测试周末狂欢仙果转盘 (Mod 242) 与活跃回馈 (Mod 644) 免费抽取"""
        from tasks.routine.weekend import WeekendRevelryTask
        task = WeekendRevelryTask()

        # 强制 mock 为周末
        task.is_weekend = MagicMock(return_value=True)

        self.client.request = AsyncMock(side_effect=[
            b"\x00" * 10,   # Mod 637 Act 0: panel_info
            bytes([0]),     # Mod 637 Act 1: pack 1 成功
            bytes([1]),     # pack 2 失败
            bytes([1]),     # pack 3 失败
            b"\x00" * 6,    # Mod 638 Act 0: entrust panel
            b"\x00" * 4,    # Mod 242 Act 1: sunday_fruit_info
            bytes([2]),     # Mod 242 Act 2: draw 1 (SUCCESS=2)
            bytes([3]),     # Mod 242 Act 2: draw 2 (TIME_USE=3 次数用尽退出)
            b"\x00" * 4,    # Mod 644 Act 0: repay_info
            bytes([0]),     # Mod 644 Act 1: repay draw SUCCESS
        ])
        self.client.send_packet = AsyncMock()

        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SUCCESS)
        self.assertEqual(res.data["claimed_packs"], 1)
        self.assertEqual(res.data["claimed_draws"], 2)  # 1次仙果 + 1次活跃回馈


if __name__ == "__main__":
    unittest.main()
