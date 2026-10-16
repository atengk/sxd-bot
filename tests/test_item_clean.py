"""背包四阶梯度自理流水线与物品清理任务单元测试套件

测试用例覆盖:
1. 背包四阶梯度执行流程 (整理 -> 使用消耗品 -> 存入仓库 -> 变卖/丢弃)
2. 目标空闲格位满足时前置早退 (Early Exit, 默认 ≥ 5 格)
3. 自选宝箱跳过保护 (避免不可逆自选损失)
4. 核心战略资产与紫金装备防变卖防丢弃保护 (PROTECTED_ITEM_IDS)
5. 体力丹使用门槛限制 (当前体力 ≥ 100 时禁止无端消耗溢出)
6. 强制全清模式 (force_all=True) 执行到极致

@author Ateng
@since 2026-10-16
"""

import unittest
from unittest.mock import AsyncMock, MagicMock
from tasks.routine.item_clean import ItemCleanTask, PROTECTED_ITEM_IDS
from protocol.messages.item import (
    ItemConstants,
    ItemClassifyPackReq,
    ItemGetPlayerPackItemListResp,
    ItemPlayerUseGridItemReq,
    ItemMovePackGridItemToWarehouseReq,
    ItemSellItemReq,
    ItemSellItemResp,
    ItemDropPackGridItemReq,
)
from core.context import GameContext
from services.query_service import ImportantItemRegistry


class TestItemCleanTask(unittest.IsolatedAsyncioTestCase):
    """测试背包四阶梯度自理流水线安全与业务逻辑"""

    def setUp(self) -> None:
        self.mock_client = MagicMock()
        self.mock_client.send_packet = AsyncMock()
        self.mock_client.request = AsyncMock()

        self.mock_ctx = MagicMock(spec=GameContext)
        self.mock_ctx.is_connected = True
        self.mock_ctx.player = MagicMock()
        self.mock_ctx.player.power = 50

    async def test_early_exit_when_enough_empty_grids(self) -> None:
        """测试初始背包剩余空格充足 (≥ 5 格) 时无须繁琐清理，快速前置退出"""
        # 背包容量 48，已用 38，剩余 10 格空闲
        pack_items = [[i, 100, i] + [0] * 18 for i in range(1, 39)]
        pack_resp = ItemGetPlayerPackItemListResp(
            pack_capacity=48,
            pack_empty_grids=10,
            pack_items=pack_items,
            warehouse_capacity=48,
            warehouse_items=[],
        )
        self.mock_client.request.return_value = pack_resp.encode_payload()

        task = ItemCleanTask(target_empty=5, force_all=False)
        result = await task.execute(self.mock_client, self.mock_ctx)

        self.assertTrue(result.is_success)
        self.assertIn("可用空间充足", result.message)
        self.assertEqual(self.mock_client.send_packet.call_count, 0)

    async def test_stage1_classify_pack_resolves_space(self) -> None:
        """测试第一阶整理背包后若已满足目标空格，则提前退出"""
        full_items = [[i, 100, i] + [0] * 18 for i in range(1, 49)]
        init_resp = ItemGetPlayerPackItemListResp(
            pack_capacity=48,
            pack_empty_grids=0,
            pack_items=full_items,
            warehouse_capacity=48,
            warehouse_items=[],
        )
        after_items = [[i, 100, i] + [0] * 18 for i in range(1, 43)]
        after_resp = ItemGetPlayerPackItemListResp(
            pack_capacity=48,
            pack_empty_grids=6,
            pack_items=after_items,
            warehouse_capacity=48,
            warehouse_items=[],
        )

        self.mock_client.request.side_effect = [
            init_resp.encode_payload(),
            after_resp.encode_payload(),
        ]

        task = ItemCleanTask(target_empty=5, force_all=False)
        result = await task.execute(self.mock_client, self.mock_ctx)

        self.assertTrue(result.is_success)
        self.assertIn("第 1 阶整理归纳后背包空间达标", result.message)
        self.assertEqual(self.mock_client.send_packet.call_count, 1)
        sent_pkt = self.mock_client.send_packet.call_args[0][0]
        self.assertIsInstance(sent_pkt, ItemClassifyPackReq)

    async def test_stage2_use_all_consumables_including_selective_box_and_stamina(self) -> None:
        """测试第二阶使用所有宝箱与消耗品：无视体力阈值全部吃满体力丹，自选宝箱默认开第一项"""
        item_exp = [1, 2001, 1] + [0] * 6 + [2] + [0] * 11
        item_power = [2, 1001, 2] + [0] * 6 + [2] + [0] * 11
        item_selective = [3, 8888, 3] + [0] * 6 + [2] + [0] * 11
        item_consumable = [4, 9999, 4] + [0] * 6 + [2] + [0] * 11

        full_items = [item_exp, item_power, item_selective, item_consumable] + [
            [i, 100, i] + [0] * 18 for i in range(5, 49)
        ]

        init_resp = ItemGetPlayerPackItemListResp(
            pack_capacity=48,
            pack_empty_grids=0,
            pack_items=full_items,
            warehouse_capacity=48,
            warehouse_items=[],
        )
        after_classify_resp = init_resp
        after_use_resp = ItemGetPlayerPackItemListResp(
            pack_capacity=48,
            pack_empty_grids=6,
            pack_items=[[i, 100, i] + [0] * 18 for i in range(7, 49)],
            warehouse_capacity=48,
            warehouse_items=[],
        )

        self.mock_client.request.side_effect = [
            init_resp.encode_payload(),
            after_classify_resp.encode_payload(),
            after_use_resp.encode_payload(),
        ]

        # 玩家体力设为 120 (>= 100)，新规范下体力丹依然强制全部使用
        self.mock_ctx.player.power = 120

        # 在全局注册表中注入自选宝箱属性并在测试完成后复原
        ImportantItemRegistry[8888] = {"is_selective": True, "name": "战略自选礼盒"}
        try:
            task = ItemCleanTask(target_empty=5, force_all=False)
            result = await task.execute(self.mock_client, self.mock_ctx)
        finally:
            ImportantItemRegistry.pop(8888, None)

        self.assertTrue(result.is_success)
        self.assertIn("第 2 阶开箱与使用后背包空间达标", result.message)

        used_grid_ids = [
            call.args[0].grid_id
            for call in self.mock_client.send_packet.call_args_list
            if isinstance(call.args[0], ItemPlayerUseGridItemReq)
        ]
        self.assertIn(1, used_grid_ids)
        self.assertIn(2, used_grid_ids)
        self.assertIn(3, used_grid_ids)
        self.assertIn(4, used_grid_ids)

    async def test_stage3_warehouse_transfer_when_space_available(self) -> None:
        """测试第三阶在仓库有空闲时，转存不可使用物品"""
        mat_item = [1, 5555, 1] + [0] * 6 + [0] + [3] + [0] * 11
        full_items = [mat_item] + [[i, 100, i] + [0] * 18 for i in range(2, 49)]

        init_resp = ItemGetPlayerPackItemListResp(
            pack_capacity=48,
            pack_empty_grids=0,
            pack_items=full_items,
            warehouse_capacity=48,
            warehouse_items=[[1, 10, 1] + [0] * 18] * 10,
        )
        after_classify = init_resp
        after_stage2 = init_resp
        after_stage3 = ItemGetPlayerPackItemListResp(
            pack_capacity=48,
            pack_empty_grids=5,
            pack_items=full_items[1:44],
            warehouse_capacity=48,
            warehouse_items=[],
        )

        self.mock_client.request.side_effect = [
            init_resp.encode_payload(),
            after_classify.encode_payload(),
            after_stage2.encode_payload(),
            after_stage3.encode_payload(),
        ]

        task = ItemCleanTask(target_empty=5, force_all=False)
        result = await task.execute(self.mock_client, self.mock_ctx)

        self.assertTrue(result.is_success)
        self.assertIn("第 3 阶存仓后背包空间达标", result.message)

        warehoused_grids = [
            call.args[0].pack_grid_id
            for call in self.mock_client.send_packet.call_args_list
            if isinstance(call.args[0], ItemMovePackGridItemToWarehouseReq)
        ]
        self.assertIn(1, warehoused_grids)

    async def test_stage4_warehouse_full_sells_and_drops_remaining(self) -> None:
        """测试第四阶仓满全丢 (Q4 B 模式)：仓库满后剩余物品先变卖换钱，无法变卖的彻底丢弃"""
        # 格位 1: 可变卖物品 (player_item_id=101)
        item1 = [101, 2001, 1] + [0] * 6 + [0] + [1] + [0] * 11
        # 格位 2: 无法变卖物品 (player_item_id=102, 变卖失败后执行丢弃)
        item2 = [102, 999999, 2] + [0] * 6 + [0] + [4] + [0] * 11

        init_resp = ItemGetPlayerPackItemListResp(
            pack_capacity=2,
            pack_empty_grids=0,
            pack_items=[item1, item2],
            warehouse_capacity=1,
            warehouse_items=[[1, 10, 1] + [0] * 18],
        )
        after_classify = init_resp
        after_stage2 = init_resp
        after_stage3 = init_resp
        sell_resp1 = ItemSellItemResp(result_code=ItemConstants.ACTION_SUCCESS, return_coins=500)
        sell_resp2 = ItemSellItemResp(result_code=ItemConstants.ACTION_FAILED, return_coins=0)
        final_resp = ItemGetPlayerPackItemListResp(
            pack_capacity=2,
            pack_empty_grids=2,
            pack_items=[],
            warehouse_capacity=1,
            warehouse_items=[[1, 10, 1] + [0] * 18],
        )

        self.mock_client.request.side_effect = [
            init_resp.encode_payload(),
            after_classify.encode_payload(),
            after_stage2.encode_payload(),
            after_stage3.encode_payload(),
            sell_resp1.encode_payload(),
            sell_resp2.encode_payload(),
            final_resp.encode_payload(),
        ]

        task = ItemCleanTask(target_empty=2, force_all=True)
        result = await task.execute(self.mock_client, self.mock_ctx)

        self.assertTrue(result.is_success)

        # 检查变卖请求已发出
        sold_player_item_ids = [
            call.args[0].player_item_id
            for call in self.mock_client.request.call_args_list
            if isinstance(call.args[0], ItemSellItemReq)
        ]
        self.assertIn(101, sold_player_item_ids)
        self.assertIn(102, sold_player_item_ids)

        # 检查 item2 变卖失败后被丢弃
        dropped_grids = [
            call.args[0].grid_id
            for call in self.mock_client.send_packet.call_args_list
            if isinstance(call.args[0], ItemDropPackGridItemReq)
        ]
        self.assertIn(2, dropped_grids)

    async def test_use_only_mode_does_not_warehouse_or_drop(self) -> None:
        """测试一键使用模式 (use_only=True)：仅开箱吃丹，绝不存仓和丢弃"""
        item_exp = [1, 2001, 1] + [0] * 6 + [2] + [0] * 11
        item_mat = [2, 5555, 2] + [0] * 6 + [0] + [3] + [0] * 11

        init_resp = ItemGetPlayerPackItemListResp(
            pack_capacity=48,
            pack_empty_grids=0,
            pack_items=[item_exp, item_mat],
            warehouse_capacity=48,
            warehouse_items=[],
        )
        after_classify = init_resp
        after_stage2 = ItemGetPlayerPackItemListResp(
            pack_capacity=48,
            pack_empty_grids=1,
            pack_items=[item_mat],
            warehouse_capacity=48,
            warehouse_items=[],
        )

        self.mock_client.request.side_effect = [
            init_resp.encode_payload(),
            after_classify.encode_payload(),
            after_stage2.encode_payload(),
        ]

        task = ItemCleanTask(target_empty=100, force_all=True, use_only=True)
        result = await task.execute(self.mock_client, self.mock_ctx)

        self.assertTrue(result.is_success)
        self.assertIn("一键使用背包物品完成", result.message)

        # 验证绝无存仓请求
        warehoused = [
            call.args[0]
            for call in self.mock_client.send_packet.call_args_list
            if isinstance(call.args[0], ItemMovePackGridItemToWarehouseReq)
        ]
        self.assertEqual(len(warehoused), 0)

        # 验证绝无丢弃请求
        dropped = [
            call.args[0]
            for call in self.mock_client.send_packet.call_args_list
            if isinstance(call.args[0], ItemDropPackGridItemReq)
        ]
        self.assertEqual(len(dropped), 0)


if __name__ == "__main__":
    unittest.main()

