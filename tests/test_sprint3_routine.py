"""Sprint 3 进阶玩法与副本深水区单元测试套件

全面覆盖：
1. 深海捕鱼达人状态查询、免费捕鱼与绝对零元宝熔断保护 (Mod 217)
2. 帮派吉星高照免费投掷循环、点数解析与七星封魔探查 (Mod 10, Mod 21)
3. 六道轮回塔层数解包、关卡进度与封灵石收益同步 (Mod 32, Mod 100)

@author Ateng
@since 2026-10-16
"""

import unittest
from unittest.mock import AsyncMock, MagicMock
from core.context import GameContext
from network.client import SXDClient
from tasks.base import TaskStatus
from tasks.routine.fishing import FishingTask
from tasks.routine.faction_roll import FactionRollCakeTask
from tasks.battle.tower import TowerTask


class TestSprint3Routine(unittest.IsolatedAsyncioTestCase):
    """Sprint 3 进阶玩法自动化单元测试

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
            coins=10000000,
            ingots=39806,
            power=100,
            fame=50000,
            vip_level=10,
            town_id=29,
            mission_key=100,
        )
        self.client = MagicMock(spec=SXDClient)

    # ==================== 1. 深海捕鱼 (Mod 217) 测试 ====================

    async def test_fishing_zero_fishhook_guardrail(self) -> None:
        """测试鱼叉耗尽时触发强前置熔断 (零元宝保护)"""
        task = FishingTask()
        # Mod 217 Act 0 返回 4 字节: 0 支鱼叉
        self.client.request = AsyncMock(return_value=(0).to_bytes(4, "big"))

        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SKIPPED)
        self.assertIn("零元宝熔断", res.message)
        self.assertEqual(res.data["fishhook_count"], 0)
        # 验证仅发起查询，绝不发起付费或额外捕鱼
        self.assertEqual(self.client.request.call_count, 1)

    async def test_fishing_execute_success(self) -> None:
        """测试持有鱼叉时成功执行免费撒网捕鱼"""
        task = FishingTask()

        # 模拟调用序列:
        # 1. Act 0: 剩余鱼叉 2 支
        # 2. Act 1: 捕鱼 1 (成功, 状态码 0, 鱼种 101, 奖励 5000)
        # 3. Act 1: 捕鱼 2 (成功, 状态码 0, 鱼种 102, 奖励 6000)
        resp_info = (2).to_bytes(4, "big")
        resp_fish1 = bytes([0]) + (101).to_bytes(4, "big") + (5000).to_bytes(4, "big")
        resp_fish2 = bytes([0]) + (102).to_bytes(4, "big") + (6000).to_bytes(4, "big")

        self.client.request = AsyncMock(side_effect=[resp_info, resp_fish1, resp_fish2])

        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SUCCESS)
        self.assertEqual(res.data["fished_count"], 2)
        self.assertEqual(self.client.request.call_count, 3)

    # ==================== 2. 帮派吉星与进阶活动 (Mod 10, Mod 0) 测试 ====================

    async def test_faction_roll_cake_flow(self) -> None:
        """测试帮派吉星循环投掷、积分同步与七星封魔探查"""
        task = FactionRollCakeTask()

        # 模拟报文序列:
        # 1. Mod 10 Act 44: 帮派吉星剩余投掷次数 1 次
        resp_rolls = bytes([1])

        # 2. Mod 10 Act 46: 投掷吉星回执 (19 字节)
        # 0x20(SUCCESS), score=5, total_score=100, my_score=20, count=6, [1,1,2,6,4,2], remain=0
        resp_roll_result = bytes.fromhex("20050000006400000014000601010206040200")

        # 3. Mod 10 Act 45: 同步面板回执
        resp_cake_info = bytes.fromhex("00000014000000640000000000")

        # 4. Mod 10 Act 32: 七星封魔状态 (s_state=1, j_state=0)
        resp_satan = bytes([1, 0, 0, 0, 0, 0, 0, 0, 0, 7])

        # 5. Mod 10 Act 28: 加入封魔回执
        resp_join = bytes([0])

        # 6. Mod 0 Act 22: 阵营俸禄回执
        resp_salary = bytes([0])

        self.client.request = AsyncMock(side_effect=[
            resp_rolls,
            resp_roll_result,
            resp_cake_info,
            resp_satan,
            resp_join,
            resp_salary
        ])

        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SUCCESS)
        self.assertEqual(res.data["roll_cake_rolls"], 1)
        self.assertTrue(res.data["seal_satan_joined"])
        self.assertTrue(res.data["salary"])
        self.assertEqual(self.client.request.call_count, 6)

    # ==================== 3. 六道轮回塔与封灵石 (Mod 32, Mod 100) 测试 ====================

    async def test_tower_level_gate(self) -> None:
        """测试未达 70 级门槛时的安全拦截防御"""
        task = TowerTask()
        low_ctx = GameContext()
        low_ctx.set_connected(True)
        low_ctx.update_player_info(nickname="小萌新", player_id=99, level=50)

        res = await task.execute(self.client, low_ctx)
        self.assertEqual(res.status, TaskStatus.SKIPPED)
        self.assertIn("未达六道轮回塔开启门槛", res.message)

    async def test_tower_status_and_stone(self) -> None:
        """测试六道轮回塔面板状态解包与封灵石收益同步"""
        task = TowerTask()

        # 1. Mod 32 Act 0: 轮回塔面板 (13 字节实测数据: 190c19140600000d0000352c0c)
        resp_tower = bytes.fromhex("190c19140600000d0000352c0c")

        # 2. Mod 100 Act 21: 封灵石状态 (8 字节实测数据: 0036003600140018)
        resp_stone = bytes.fromhex("0036003600140018")

        self.client.request = AsyncMock(side_effect=[resp_tower, resp_stone])

        res = await task.execute(self.client, self.ctx)
        self.assertEqual(res.status, TaskStatus.SUCCESS)
        self.assertEqual(res.data["layer_id"], 25)
        self.assertEqual(res.data["cur_seq"], 12)
        self.assertEqual(res.data["max_seq"], 25)
        self.assertEqual(res.data["remain_reset"], 20)
        self.assertEqual(res.data["stone_count"], 54)
        self.assertEqual(self.client.request.call_count, 2)


if __name__ == "__main__":
    unittest.main()
