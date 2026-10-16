"""Sprint 2 高产出日常资源流单元测试套件

全面覆盖：
1. 仙府药园土地解包、成熟单倍收获、自动播种与仙令礼包探测 (Mod 13)
2. 吉星高照免费次数解包、存量领奖结算与绝对零元宝熔断保护 (Mod 38)
3. 齐天大圣偷桃一键批量摘桃海量经验与神龙日常喂养 (Mod 40, Mod 100)
4. 喜从天降与通商主面板资产、最新行情走势指数同步 (Mod 41)

@author Ateng
@since 2026-10-16
"""

import unittest
from unittest.mock import AsyncMock, MagicMock
from core.context import GameContext
from network.client import SXDClient
from tasks.base import TaskStatus
from tasks.routine.farm import FarmTask
from tasks.routine.lucky_star import LuckyStarTask
from tasks.routine.peach_pet import PeachAndPetTask
from tasks.routine.traders import TradersTask


class TestSprint2Routine(unittest.IsolatedAsyncioTestCase):
    """Sprint 2 高产出日常任务测试套件

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

    # ==================== 1. 仙府药园 (Mod 13) 测试 ====================

    def test_farm_decode_farmlands(self) -> None:
        """测试新版土地数据解包 (Mod 13, Act 21)"""
        task = FarmTask()
        # 构造实测 82 字节的模拟载荷 (4 块土地: 10, 11, 12, 8)
        # 土地 10: 空地 (herbs_id=0, time=0)
        # 土地 11: 成熟 (herbs_id=169, time=0)
        # 土地 12: 生长中 (herbs_id=175, time=1200)
        # 土地 8: 空地 (herbs_id=0, time=0)
        raw = bytearray()
        raw.extend((4).to_bytes(2, "big"))  # count = 4
        # land 10
        raw.extend((10).to_bytes(4, "big"))
        raw.extend((0).to_bytes(4, "big"))
        raw.extend((0).to_bytes(4, "big"))
        raw.extend(bytes([1, 1, 0, 0, 0, 0, 0]))
        # land 11
        raw.extend((11).to_bytes(4, "big"))
        raw.extend((169).to_bytes(4, "big"))
        raw.extend((0).to_bytes(4, "big"))
        raw.extend(bytes([1, 1, 0, 0, 0, 0, 0]))
        # land 12
        raw.extend((12).to_bytes(4, "big"))
        raw.extend((175).to_bytes(4, "big"))
        raw.extend((1200).to_bytes(4, "big"))
        raw.extend(bytes([1, 1, 0, 0, 0, 0, 0]))
        # land 8
        raw.extend((8).to_bytes(4, "big"))
        raw.extend((0).to_bytes(4, "big"))
        raw.extend((0).to_bytes(4, "big"))
        raw.extend(bytes([1, 1, 0, 0, 0, 0, 0]))

        lands = task._decode_farmlands(bytes(raw))
        self.assertEqual(len(lands), 4)

        self.assertEqual(lands[0]["farmland_id"], 10)
        self.assertTrue(lands[0]["is_empty"])
        self.assertFalse(lands[0]["is_mature"])

        self.assertEqual(lands[1]["farmland_id"], 11)
        self.assertFalse(lands[1]["is_empty"])
        self.assertTrue(lands[1]["is_mature"])

        self.assertEqual(lands[2]["farmland_id"], 12)
        self.assertFalse(lands[2]["is_empty"])
        self.assertFalse(lands[2]["is_mature"])
        self.assertEqual(lands[2]["farmland_time"], 1200)

        self.assertEqual(lands[3]["farmland_id"], 8)
        self.assertTrue(lands[3]["is_empty"])

    async def test_farm_execute_harvest_and_plant(self) -> None:
        """测试药园执行流：单倍收获成熟作物，自动补种经验仙草"""
        task = FarmTask()

        raw_lands = bytearray()
        raw_lands.extend((2).to_bytes(2, "big"))  # count = 2
        # land 10: 成熟待收
        raw_lands.extend((10).to_bytes(4, "big"))
        raw_lands.extend((169).to_bytes(4, "big"))
        raw_lands.extend((0).to_bytes(4, "big"))
        raw_lands.extend(bytes([1, 1, 0, 0, 0, 0, 0]))
        # land 11: 空地待播种
        raw_lands.extend((11).to_bytes(4, "big"))
        raw_lands.extend((0).to_bytes(4, "big"))
        raw_lands.extend((0).to_bytes(4, "big"))
        raw_lands.extend(bytes([1, 1, 0, 0, 0, 0, 0]))

        async def mock_request(packet, timeout_sec=3.0):
            if packet.mod == 13 and packet.act == 21:
                return bytes(raw_lands)
            if packet.mod == 13 and packet.act == 25:
                # harvest success
                return bytes([8]) + bytes(10)
            if packet.mod == 13 and packet.act == 24:
                # plant success
                return bytes([8]) + bytes(26)
            if packet.mod == 13 and packet.act == 19:
                return bytes([1])  # 有未领礼包
            if packet.mod == 13 and packet.act == 20:
                return bytes([0, 1])  # 成功领奖
            return b""

        self.client.request = AsyncMock(side_effect=mock_request)

        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertEqual(result.data["harvested_count"], 1)
        self.assertEqual(result.data["planted_count"], 1)
        self.assertTrue(result.data["xianling_claimed"])

    # ==================== 2. 吉星高照 (Mod 38) 测试 ====================

    async def test_lucky_star_guardrail_zero_free_times(self) -> None:
        """测试吉星高照强前置安全卫语句：免费次数为 0 立即 SKIPPED，坚决不消耗元宝"""
        task = LuckyStarTask()

        # 免费次数为 0 时的 Mod 38, Act 2 回包
        raw_count = bytearray()
        raw_count.extend((0).to_bytes(2, "big"))       # free_times = 0
        raw_count.extend((2403).to_bytes(2, "big"))    # points = 2403
        raw_count.extend((6022).to_bytes(4, "big"))    # extra_points = 6022

        async def mock_request(packet, timeout_sec=2.5):
            if packet.mod == 38 and packet.act == 2:
                return bytes(raw_count)
            if packet.mod == 38 and packet.act == 4:
                return bytes([4])  # NO_RECORD
            return b""

        self.client.request = AsyncMock(side_effect=mock_request)

        result = await task.execute(self.client, self.ctx)
        # 必须触发安全跳过
        self.assertEqual(result.status, TaskStatus.SKIPPED)
        self.assertIn("零元宝安全熔断", result.message)
        self.assertEqual(result.data["free_times"], 0)
        self.assertEqual(result.data["rolls_done"], 0)

    async def test_lucky_star_execution_with_free_rolls(self) -> None:
        """测试吉星高照在有免费次数时执行投掷与领奖入库"""
        task = LuckyStarTask()

        free_count = 2

        async def mock_request(packet, timeout_sec=2.5):
            nonlocal free_count
            if packet.mod == 38 and packet.act == 2:
                raw = bytearray()
                raw.extend((free_count).to_bytes(2, "big"))
                raw.extend((2403).to_bytes(2, "big"))
                raw.extend((6022).to_bytes(4, "big"))
                return bytes(raw)
            if packet.mod == 38 and packet.act == 6:
                return bytes([0])  # is_auto = 0
            if packet.mod == 38 and packet.act == 4:
                return bytes([0])  # SUCCESS
            return b""

        self.client.request = AsyncMock(side_effect=mock_request)
        self.client.send_packet = AsyncMock()

        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertIn("吉星高照流水线完成", result.message)

    # ==================== 3. 齐天大圣偷桃 (Mod 40) 测试 ====================

    async def test_peach_and_pet_batch_harvest(self) -> None:
        """测试齐天大圣一键批量偷桃与神龙培养"""
        task = PeachAndPetTask()

        async def mock_request(packet, timeout_sec=2.5):
            if packet.mod == 40 and packet.act == 3:
                return bytes.fromhex("2f040100")
            if packet.mod == 40 and packet.act == 4:
                return bytes.fromhex("05010001010098968000000064")
            if packet.mod == 40 and packet.act == 5:
                # [1B 0=SUCCESS] + [4B extra] + [4B exp (10,000,000)]
                return bytes([0]) + (0).to_bytes(4, "big") + (10000000).to_bytes(4, "big")
            if packet.mod == 40 and packet.act == 6:
                return bytes([0])
            if packet.mod == 100 and packet.act == 29:
                return bytes([1])  # 神龙喂养成功
            return b""

        self.client.request = AsyncMock(side_effect=mock_request)

        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertEqual(result.data["peaches"], 1)
        self.assertEqual(result.data["exp"], 10000000)
        self.assertTrue(result.data["pet_fed"])

    # ==================== 4. 喜从天降与通商 (Mod 41) 测试 ====================

    async def test_traders_panel_and_trend_sync(self) -> None:
        """测试喜从天降/通商主面板数据与行情趋势同步"""
        task = TradersTask()

        # 模拟 239 字节主面板数据
        raw_panel = bytearray(239)
        raw_panel[0:4] = (1).to_bytes(4, "big")       # status = 1
        raw_panel[4:8] = (6295).to_bytes(4, "big")    # tokens = 6295
        raw_panel[8:12] = (64000).to_bytes(4, "big")  # max_tokens = 64000

        async def mock_request(packet, timeout_sec=2.5):
            if packet.mod == 41 and packet.act == 0:
                return bytes(raw_panel)
            if packet.mod == 41 and packet.act == 2:
                return (22722).to_bytes(4, "big") + (100).to_bytes(4, "big")
            if packet.mod == 41 and packet.act == 4:
                return (1).to_bytes(4, "big")
            if packet.mod == 41 and packet.act == 5:
                return bytes(8)
            return b""

        self.client.request = AsyncMock(side_effect=mock_request)

        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertTrue(result.data["panel_synced"])
        self.assertEqual(result.data["tokens"], 6295)
        self.assertEqual(result.data["trend_index"], 1)


if __name__ == "__main__":
    unittest.main()
