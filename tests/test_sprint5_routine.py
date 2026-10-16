"""Sprint 5 高阶日常与圣域拓展任务单元测试套件

全面覆盖 10 大全新及升级模块：
1. 吉星高照自适应 VIP 托管与免费投掷 (Mod 38)
2. 西天取经 Mod 30 协议与优雅降级 (Mod 30)
3. 猎妖每日 10 次免费挑战与零元宝死锁 (Mod 105)
4. 五行装备同步与背包自动整理 (Mod 168)
5. 五福临门运营活动探测与福袋合成 (Mod 400)
6. 聚灵免费灵气汇聚与元宝卫语句 (Mod 104)
7. 缘魂宝箱批量开启与背包整理 (Mod 232)
8. 仙府家园全屋家具收益与蛋糕领取 (Mod 210)
9. 仙盟上香白檀香档位死锁与祈福 (Mod 419)
10. 回忆之境篇章通关星级与大礼包提取 (Mod 526)

@author Ateng
@since 2026-10-16
"""

import unittest
from unittest.mock import AsyncMock, MagicMock
from core.context import GameContext
from network.client import SXDClient
from tasks.base import TaskStatus
from tasks.routine.lucky_star import LuckyStarTask
from tasks.routine.take_bible import TakeBibleTask
from tasks.routine.hunt_demon import HuntDemonTask
from tasks.routine.five_elements import FiveElementsTask
from tasks.routine.five_fu import FiveFuTask
from tasks.routine.nimbus import NimbusTask
from tasks.routine.link_fate import LinkFateTask
from tasks.routine.home import HomeTask
from tasks.routine.union_worship import UnionWorshipTask
from tasks.routine.memory_zone import MemoryZoneTask


class TestSprint5Routine(unittest.IsolatedAsyncioTestCase):
    """Sprint 5 高阶日常自动化单元测试

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

    # ==================== 1. 吉星高照 (Mod 38) ====================

    async def test_lucky_star_auto_mode(self) -> None:
        """测试 VIP 自动托管模式下提取境界点"""
        task = LuckyStarTask()
        # get_count -> free:10, points:200, extra:6000; is_auto -> 1; get_award -> 0 (SUCCESS); final get_count
        count_bytes = (10).to_bytes(2, "big") + (200).to_bytes(2, "big") + (6000).to_bytes(4, "big")
        self.client.request = AsyncMock(side_effect=[
            count_bytes,       # Act 2: get_count
            bytes([1]),        # Act 6: is_auto = 1
            bytes([0]),        # Act 4: get_award SUCCESS
            count_bytes,       # Act 2: final get_count
        ])
        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertTrue(result.data["is_auto"])
        self.assertTrue(result.data["claimed_award"])

    async def test_lucky_star_zero_free_times(self) -> None:
        """测试免费次数用尽时安全熔断"""
        task = LuckyStarTask()
        count_bytes = (0).to_bytes(2, "big") + (0).to_bytes(2, "big") + (6000).to_bytes(4, "big")
        self.client.request = AsyncMock(side_effect=[
            count_bytes,       # Act 2
            bytes([0]),        # Act 6: is_auto = 0
            bytes([1]),        # Act 4: get_award no record
        ])
        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SKIPPED)
        self.assertEqual(result.data["free_times"], 0)

    # ==================== 2. 西天取经 (Mod 30) ====================

    async def test_take_bible_success(self) -> None:
        """测试西天取经启动护送"""
        task = TakeBibleTask()
        self.client.request = AsyncMock(side_effect=[
            bytes([8]) + b"\x00" * 30,  # Act 2: get_take_bible_info
            bytes([8]),                 # Act 10: start_take_bible SUCCESS
        ])
        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertTrue(result.data["started"])

    async def test_take_bible_timeout_degradation(self) -> None:
        """测试非活动场景超时优雅降级"""
        task = TakeBibleTask()
        self.client.request = AsyncMock(side_effect=TimeoutError())
        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SKIPPED)
        self.assertTrue(result.data["timeout"])

    # ==================== 3. 猎妖 (Mod 105) ====================

    async def test_hunt_demon_full_pipeline(self) -> None:
        """测试每日 10 次免费猎妖全额击杀"""
        task = HuntDemonTask()
        # open_hunt_demon: type=3, free=2, max=10
        open_resp = bytes([3, 2, 10, 0, 15]) + b"\x00" * 12
        # hunt_demon: status=5 (SUCCESS)
        hunt_resp = bytes([5]) + b"\x00" * 28
        self.client.request = AsyncMock(side_effect=[
            open_resp,
            hunt_resp,
            hunt_resp,
        ])
        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertEqual(result.data["hunts_done"], 2)

    # ==================== 4. 五行 (Mod 168) ====================

    async def test_five_elements_clean_up(self) -> None:
        """测试五行背包自动梳理整理"""
        task = FiveElementsTask()
        equip_resp = (5).to_bytes(2, "big") + b"\x00" * 50
        clean_resp = bytes([9])  # 9 = SUCCESS
        self.client.request = AsyncMock(side_effect=[equip_resp, clean_resp])
        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertTrue(result.data["cleaned"])
        self.assertEqual(result.data["equip_count"], 5)

    # ==================== 5. 五福临门 (Mod 400) ====================

    async def test_five_fu_inactive(self) -> None:
        """测试五福临门非活动期静默跳过"""
        task = FiveFuTask()
        self.client.request = AsyncMock(return_value=bytes([2]))  # 2 = NOACTIVITY
        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SKIPPED)
        self.assertFalse(result.data["active"])

    async def test_five_fu_active_compose(self) -> None:
        """测试五福临门活动期开福袋与合成"""
        task = FiveFuTask()
        self.client.request = AsyncMock(side_effect=[
            bytes([0]),  # open_pack SUCCESS
            bytes([0]),  # compose_fu SUCCESS
        ])
        self.client.send_packet = AsyncMock()
        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertTrue(result.data["active"])
        self.assertTrue(result.data["opened"])
        self.assertTrue(result.data["composed"])

    # ==================== 6. 聚灵 (Mod 104) ====================

    async def test_nimbus_gather_free(self) -> None:
        """测试免费聚灵天地灵气"""
        task = NimbusTask()
        # nimbus_info: total=21000, free=1
        info_resp = (21000).to_bytes(4, "big") + (1).to_bytes(2, "big") + b"\x00" * 8
        gather_resp = bytes([0]) + b"\x00" * 15  # SUCCESS
        self.client.request = AsyncMock(side_effect=[info_resp, gather_resp])
        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertTrue(result.data["gathered"])
        self.assertEqual(result.data["total_nimbus"], 21000)

    # ==================== 7. 缘魂宝箱 (Mod 232) ====================

    async def test_link_fate_open_boxes(self) -> None:
        """测试批量一键开启免费缘魂宝箱"""
        task = LinkFateTask()
        # get_link_fate_box: 1 kind, box_id=3937, count=35
        box_resp = (1).to_bytes(2, "big") + (3937).to_bytes(4, "big") + (35).to_bytes(4, "big") + b"\x00" * 6
        open_resp = bytes([5]) + b"\x00" * 30  # 5 = SUCCESS
        self.client.request = AsyncMock(side_effect=[box_resp, open_resp])
        self.client.send_packet = AsyncMock()
        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertEqual(result.data["opened_boxes"], 35)

    # ==================== 8. 仙府家园 (Mod 210) ====================

    async def test_home_furniture_and_cake(self) -> None:
        """测试家园每日蛋糕赠礼提取"""
        task = HomeTask()
        self.client.request = AsyncMock(side_effect=[
            bytes([1]),                                # Act 0: has_home = 1
            bytes([0]) + b"\x00" * 8,                  # Act 19: get_cake SUCCESS
        ])
        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertTrue(result.data["has_home"])
        self.assertTrue(result.data["cake"])

    # ==================== 9. 仙盟上香 (Mod 419) ====================

    async def test_union_worship_coin(self) -> None:
        """测试仙盟白檀香祈福"""
        task = UnionWorshipTask()
        panel_resp = b"\x00" * 44
        worship_resp = bytes([2]) + b"\x00" * 8  # 2 = SUCCESS
        self.client.request = AsyncMock(side_effect=[panel_resp, worship_resp])
        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertTrue(result.data["worshipped"])

    # ==================== 10. 回忆之境 (Mod 526) ====================

    async def test_memory_zone_milestone_claim(self) -> None:
        """测试回忆之境篇章通关奖励提取"""
        task = MemoryZoneTask()
        # main_panel: status=0, zones=1, zone_id=1, stars=6, max_stars=6, state=0 (未领取)
        main_resp = bytes([0]) + (1).to_bytes(2, "big") + (1).to_bytes(4, "big") + (6).to_bytes(4, "big") + (6).to_bytes(4, "big") + (0).to_bytes(4, "big")
        award_resp = bytes([0]) + b"\x00" * 8  # 0 = SUCCESS
        self.client.request = AsyncMock(side_effect=[main_resp, award_resp])
        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertEqual(result.data["claimed_zones"], 1)
        self.assertEqual(result.data["total_zones"], 1)


if __name__ == "__main__":
    unittest.main()
