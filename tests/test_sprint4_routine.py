"""Sprint 4 邮件、仙道问灵、点金石、周末狂欢、小助手与练功单元测试套件

全面覆盖：
1. 系统邮件与停机维护/更新大礼包一键提取 (Mod 345)
2. 仙道问灵等级守卫与每日免费求签 (Mod 503)
3. 点金石点石成金与好友求助无损协助 (Mod 551)
4. 周末狂欢时段守卫、免费礼包与委托减负 (Mod 637 / Mod 638)
5. 小助手面板数据同步与阶梯活跃度宝箱提取 (Mod 52)
6. 城镇挂机打坐练功指令激活 (Mod 0 Act 36)

@author Ateng
@since 2026-10-16
"""

import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from core.context import GameContext
from network.client import SXDClient
from tasks.base import TaskStatus
from tasks.routine.email import EmailTask
from tasks.routine.ask_fairy import AskFairyTask
from tasks.routine.touch_stone import GoldenTouchStoneTask
from tasks.routine.weekend import WeekendRevelryTask
from tasks.routine.assistant import AssistantTask
from tasks.routine.practice import PracticeTask


class TestSprint4Routine(unittest.IsolatedAsyncioTestCase):
    """Sprint 4 进阶日常与福利收割单元测试

    @author Ateng
    @since 2026-10-16
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
            mission_key=100,
        )
        self.client = MagicMock(spec=SXDClient)

    # ==================== 1. 系统邮件 (Mod 345) 测试 ====================

    async def test_email_one_key_claim(self) -> None:
        """测试一键提取邮件附件与更新大礼包"""
        task = EmailTask()
        # Mock: is_have_new_email -> 1, get_email_info -> 2 封邮件, one_key_get_award -> 0 (成功)
        self.client.request = AsyncMock(side_effect=[
            bytes([1]),                                    # Act 5: 新邮件标识
            (2).to_bytes(2, "big") + b"\x00" * 20,         # Act 0: 邮件总数 2
            bytes([0]),                                    # Act 6: 一键提取成功
        ])

        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SUCCESS)
        self.assertEqual(res.data["email_count"], 2)
        self.assertEqual(res.data["claim_status"], 0)
        self.assertEqual(self.client.request.call_count, 3)

    # ==================== 2. 仙道问灵 (Mod 503) 测试 ====================

    async def test_ask_fairy_level_guardrail(self) -> None:
        """测试等级未达 100 级时安全跳过"""
        self.ctx.player.level = 80
        task = AskFairyTask()
        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SKIPPED)
        self.assertFalse(res.data["level_ok"])

    async def test_ask_fairy_free_inquiry_success(self) -> None:
        """测试 100 级以上每日免费仙道问灵"""
        self.ctx.player.level = 300
        task = AskFairyTask()
        self.client.request = AsyncMock(side_effect=[
            b"\x00" * 32,  # Act 0: recall_info
            bytes([0]),    # Act 3: do_ask_fairy 成功 (0)
            bytes([0]),    # Act 7: gain_ask_level_award
        ])

        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SUCCESS)
        self.assertEqual(res.data["ask_status"], 0)

    # ==================== 3. 点金石 (Mod 551) 测试 ====================

    async def test_golden_touch_stone_flow(self) -> None:
        """测试点石成金与好友求助协助流水线"""
        task = GoldenTouchStoneTask()
        self.client.request = AsyncMock(side_effect=[
            bytes([2]),                            # Act 0: status
            b"\x00" * 24,                          # Act 2: panel info
            bytes([0]),                            # Act 6: touch_stone 成功
            (1).to_bytes(4, "big") + (0).to_bytes(2, "big"),  # Act 1: share panel info (0好友)
        ])
        self.client.send_packet = AsyncMock()

        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SUCCESS)
        self.assertEqual(res.data["touch_done"], 1)

    # ==================== 4. 周末狂欢 (Mod 637 / Mod 638) 测试 ====================

    @patch("tasks.routine.weekend.WeekendRevelryTask.is_weekend", return_value=False)
    async def test_weekend_revelry_weekday_skip(self, mock_is_weekend: MagicMock) -> None:
        """测试工作日严格时段守卫防断连跳过"""
        task = WeekendRevelryTask()
        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SKIPPED)
        self.assertFalse(res.data["is_weekend"])

    @patch("tasks.routine.weekend.WeekendRevelryTask.is_weekend", return_value=True)
    async def test_weekend_revelry_weekend_claim(self, mock_is_weekend: MagicMock) -> None:
        """测试周末时段自动领取大礼包与委托减负"""
        task = WeekendRevelryTask()
        self.client.request = AsyncMock(side_effect=[
            b"\x00" * 16,                          # Act 0: panel_info
            bytes([0]),                            # Act 1: pack 1 成功
            bytes([1]),                            # Act 1: pack 2 失败/已领
            bytes([1]),                            # Act 1: pack 3 失败/已领
            (0).to_bytes(4, "big") + (0).to_bytes(2, "big"),  # Act 0: entrust panel (0委托)
        ])
        self.client.send_packet = AsyncMock()

        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SUCCESS)
        self.assertEqual(res.data["claimed_packs"], 1)

    # ==================== 5. 小助手 (Mod 52) 测试 ====================

    async def test_assistant_post_routine_boxes(self) -> None:
        """测试小助手活跃度达标后的阶梯宝箱领取"""
        task = AssistantTask(is_post_routine=True)
        self.client.request = AsyncMock(side_effect=[
            b"\x00" * 48,                          # Act 0: info
            bytes([0, 0, 5]) + b"\x00" * 10,       # Act 1 (box 1): SUCCESS (0) 5件道具
            bytes([2, 0, 0]),                      # Act 1 (box 2): NOT_ENOUGH_NUM (2) 活跃不足退出
        ])

        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SUCCESS)
        self.assertEqual(res.data["claimed_boxes"], 1)

    # ==================== 6. 挂机打坐练功 (Mod 0 Act 36) 测试 ====================

    async def test_practice_task(self) -> None:
        """测试挂机打坐指令发送"""
        task = PracticeTask()
        self.client.send_packet = AsyncMock()

        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SUCCESS)
        self.assertTrue(res.data["practice_active"])
        self.client.send_packet.assert_called_once()


if __name__ == "__main__":
    unittest.main()
