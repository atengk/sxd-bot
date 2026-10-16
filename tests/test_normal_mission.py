"""神仙道普通副本极速扫荡与体力清空任务单元测试

测试 NormalMissionSweepTask 的等级门槛、体力消耗计算、前置卫语句跳过与协议交互序列。

@author Ateng
@since 2026-10-15
"""

import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock
from core.context import GameContext
from network.client import SXDClient
from tasks.base import TaskStatus
from tasks.battle.normal_mission import NormalMissionSweepTask


class TestNormalMissionSweepTask(unittest.IsolatedAsyncioTestCase):
    """普通副本扫荡流水线单元测试"""

    def setUp(self) -> None:
        self.ctx = GameContext()
        self.client = MagicMock(spec=SXDClient)
        self.client.context = self.ctx
        self.client.send_packet = AsyncMock()
        self.client.request = AsyncMock()

    async def test_skip_when_disconnected(self) -> None:
        """断开连接时安全跳过"""
        self.ctx.set_connected(False)
        task = NormalMissionSweepTask()
        res = await task.execute(self.client, self.ctx)

        self.assertEqual(res.status, TaskStatus.SKIPPED)
        self.assertIn("未处于有效长连接状态", res.message)

    async def test_skip_when_low_level(self) -> None:
        """角色等级未达门槛 (10级) 时安全跳过"""
        self.ctx.set_connected(True)
        self.ctx.player.level = 8
        task = NormalMissionSweepTask()
        res = await task.execute(self.client, self.ctx)

        self.assertEqual(res.status, TaskStatus.SKIPPED)
        self.assertIn("未达普通副本扫荡门槛", res.message)

    async def test_skip_when_not_enough_power(self) -> None:
        """体力不足 5 点时安全跳过"""
        self.ctx.set_connected(True)
        self.ctx.player.level = 50
        self.ctx.update_power(3)  # 仅剩 3 点体力

        task = NormalMissionSweepTask()
        res = await task.execute(self.client, self.ctx)

        self.assertEqual(res.status, TaskStatus.SKIPPED)
        self.assertIn("当前体力不足以扫荡一次普通副本", res.message)

    async def test_successful_sweep_flow(self) -> None:
        """体力充足时正常执行官方扫荡流水线并同步体力清空"""
        self.ctx.set_connected(True)
        self.ctx.player.level = 300
        self.ctx.update_power(52)  # 52 点体力

        # 模拟扫荡与极速完成响应
        async def mock_request(pkt, timeout_sec=5.0) -> bytes:
            if getattr(pkt, "mod", None) == 25 and getattr(pkt, "act", None) == 3:
                # 极速秒完成触发时扣减体力至 2 点
                self.ctx.update_power(2)
                return b"\x00\x00"
            return b"\x00\x00\x00\x00"

        self.client.request.side_effect = mock_request

        task = NormalMissionSweepTask(target_mission_id=854)
        res = await task.execute(self.client, self.ctx)

        self.assertEqual(res.status, TaskStatus.SUCCESS)
        self.assertEqual(res.data["swept_loops"], 1)
        self.assertEqual(res.data["consumed_power"], 50)
        self.assertEqual(self.ctx.player.power, 2)
        self.assertIn("普通副本扫荡任务完成", res.message)

    async def test_skip_when_reaching_min_power_reserve(self) -> None:
        """当体力低于保留阈值时安全跳过"""
        self.ctx.set_connected(True)
        self.ctx.player.level = 80
        self.ctx.update_power(20)

        # 设置保留阈值为 20 点
        task = NormalMissionSweepTask(min_power_reserve=20)
        res = await task.execute(self.client, self.ctx)

        self.assertEqual(res.status, TaskStatus.SKIPPED)
        self.assertIn("当前体力不足以扫荡一次普通副本", res.message)


class TestContextPowerSync(unittest.TestCase):
    """上下文体力同步逻辑测试"""

    def test_sync_power_from_mod0_act3_broadcast(self) -> None:
        client = SXDClient()
        # 构造 Mod 0 Act 3 广播载荷: Count=1, PropID=23, Value=120
        # [2B Count=1] + [1B PropID=23] + [8B Value=120]
        body = b"\x00\x01\x17\x00\x00\x00\x00\x00\x00\x00\x78"
        client._sync_context(mod=0, act=3, body=body)

        self.assertEqual(client.context.player.power, 120)


if __name__ == "__main__":
    unittest.main()
