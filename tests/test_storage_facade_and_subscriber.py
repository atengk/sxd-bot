"""神仙道统一存储门面 GameStorage 与 EventBus 切面集成测试

测试用例覆盖:
1. GameStorage 门面初始化与全系强类型领域仓储 (protocol, player, inventory, module_state, battles, audits)
2. PlayerRepository 与 InventoryRepository 业务查询与状态增删改查
3. ModuleStateRepository 半结构化快照读写与默认值容错
4. BattleRecordRepository 战报胜率统计与 AuditLogRepository 审计追溯
5. 原生 SQL 执行逃生接口 (storage.query / storage.execute)
6. SqliteStorageSubscriber 与 EventBus 端到端全链路联动:
   - Mod 0 Act 2: 角色基础属性同步
   - Mod 0 Act 3: 角色属性动态更新
   - Mod 2 Act 3: 背包物品全量同步
   - Mod 4 Act 2: 关卡怪物战斗结算
   - Mod 13 Act 0 / Act 6: 药园地块与收获回执
   - Mod 28 Act 13: 竞技场剩余挑战次数
   - 高危元宝操作审计流水入库

@author Ateng
@since 2026-10-16
"""

import asyncio
import os
import shutil
import tempfile
import unittest

from core.context import GameContext
from core.events import EventBus
from protocol.contracts.mod_13_farm import FarmGetFarmlandinfoListResp
from protocol.contracts.mod_2_item import ItemGetAllPlayerItemInfosResp
from protocol.messages.battle import (
    MissionFightMonsterResp,
    SuperSportGetChallengeTimesResp,
)
from protocol.messages.player import (
    PlayerInfoResp,
    PlayerUpdatePlayerDataResp,
)
from protocol.messages.routine import FarmHarvestResp
from protocol.packet import ByteArrayWriter
from storage.facade import (
    AssetRepository,
    AuditLogRepository,
    BattleRecordRepository,
    GameStorage,
    InventoryRepository,
    ModuleStateRepository,
    PlayerRepository,
)
from storage.player_db import (
    AssetTransactionRecord,
    AuditLogRecord,
    BattleRecord,
    InventoryItemRecord,
    ModuleStateRecord,
    PlayerProfileRecord,
)
from storage.subscriber import SqliteStorageSubscriber


class TestStorageFacadeAndSubscriber(unittest.TestCase):
    """统一存储门面与 EventBus 切面自动化集成测试套件

    @author Ateng
    @since 2026-10-16
    """

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="sxd_test_facade_")
        self.server_id = 999
        self.player_id = 88888
        self.context = GameContext()
        self.storage = GameStorage(
            server_id=self.server_id,
            player_id=self.player_id,
            base_dir=self.test_dir,
            auto_start_worker=True,
            flush_interval=0.01,
        )
        self.event_bus = EventBus()
        self.subscriber = SqliteStorageSubscriber(
            worker=self.storage.worker,
            player_db=self.storage.player_db,
            player_id=self.player_id,
            context=self.context,
        )
        self.subscriber.attach_to_event_bus(self.event_bus)

    def tearDown(self) -> None:
        self.storage.close()
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _encode_player_info(
        self,
        nickname: str = "太上仙人",
        level: int = 90,
        coins: int = 1000000,
        ingots: int = 500,
        power: int = 200,
    ) -> bytes:
        """辅助打包 Mod 0 Act 2 官方契约二进制报文"""
        writer = ByteArrayWriter()
        writer.write_utf(nickname)
        writer.write_int32(level)
        writer.write_int32(ingots)
        writer.write_int64(coins)
        writer.write_int64(10000)  # health
        writer.write_int64(10000)  # max_health
        writer.write_int32(power)
        writer.write_int64(50000)  # exp
        writer.write_int64(100000) # max_exp
        writer.write_int32(1)      # town_map_id
        for _ in range(4):
            writer.write_int32(0)
        writer.write_int32(0)      # vip_level
        for _ in range(4):
            writer.write_int32(0)
        writer.write_int8(1)       # camp_id
        writer.write_int32(0)      # townKey
        writer.write_int32(0)      # fame
        for _ in range(7):
            writer.write_int32(0)
        writer.write_int32(10)     # mission_key
        return writer.to_bytes()

    def test_01_facade_structure_and_repositories(self) -> None:
        """测试 GameStorage 门面子仓储挂载与静态协议检索能力"""
        self.assertIsInstance(self.storage.player, PlayerRepository)
        self.assertIsInstance(self.storage.inventory, InventoryRepository)
        self.assertIsInstance(self.storage.module_state, ModuleStateRepository)
        self.assertIsInstance(self.storage.battles, BattleRecordRepository)
        self.assertIsInstance(self.storage.audits, AuditLogRepository)
        self.assertIsInstance(self.storage.assets, AssetRepository)

        # 验证静态协议字典仓储已就绪
        modules = self.storage.protocol.list_modules()
        self.assertGreater(len(modules), 800)
        action = self.storage.protocol.get_action(0, 0)
        self.assertIsNotNone(action)
        assert action is not None
        self.assertEqual(action.name, "login")

    def test_02_player_repository_crud(self) -> None:
        """测试 PlayerRepository 角色档案保存与局部属性增量更新"""
        self.assertIsNone(self.storage.player.get_profile())

        # 保存角色基础信息
        initial = PlayerProfileRecord(
            player_id=self.player_id,
            nickname="昆仑散仙",
            level=60,
            coins=100000,
            ingots=500,
            power=120,
        )
        self.storage.player.upsert_profile(initial)

        prof = self.storage.player.get_profile()
        self.assertIsNotNone(prof)
        assert prof is not None
        self.assertEqual(prof.nickname, "昆仑散仙")
        self.assertEqual(prof.level, 60)
        self.assertEqual(prof.power, 120)

        # 局部更新属性
        updated = self.storage.player.update_stats(level=65, power=100, fame=2000)
        self.assertIsNotNone(updated)
        assert updated is not None
        self.assertEqual(updated.level, 65)
        self.assertEqual(updated.power, 100)
        self.assertEqual(updated.fame, 2000)
        self.assertEqual(updated.nickname, "昆仑散仙")

    def test_03_inventory_repository_crud(self) -> None:
        """测试 InventoryRepository 背包资产增删查与统计"""
        self.assertEqual(self.storage.inventory.count(), 0)
        self.assertEqual(self.storage.inventory.get_items(), [])

        items = [
            InventoryItemRecord(grid_id=1, item_id=2001, count=1, item_type=1, props={"name": "太虚神甲"}),
            InventoryItemRecord(grid_id=2, item_id=3002, count=99, item_type=2, props={"name": "凝气丹"}),
            InventoryItemRecord(grid_id=3, item_id=2001, count=1, item_type=1, props={"name": "太虚神甲备用"}),
        ]
        self.storage.inventory.upsert_items(items)

        self.assertEqual(self.storage.inventory.count(), 3)
        item_1 = self.storage.inventory.get_item_by_grid(1)
        self.assertIsNotNone(item_1)
        assert item_1 is not None
        self.assertEqual(item_1.props["name"], "太虚神甲")

        # 按模板 ID 检索
        found = self.storage.inventory.find_items_by_id(2001)
        self.assertEqual(len(found), 2)
        self.assertEqual([i.grid_id for i in found], [1, 3])

        # 移除与清空
        self.storage.inventory.remove_item(2)
        self.assertEqual(self.storage.inventory.count(), 2)

        self.storage.inventory.clear()
        self.assertEqual(self.storage.inventory.count(), 0)

    def test_04_module_state_and_battle_stats(self) -> None:
        """测试 ModuleStateRepository 与 BattleRecordRepository 领域聚合能力"""
        # 1. 模块状态默认值与点查
        self.assertIsNone(self.storage.module_state.get_payload(13, "herbs"))
        self.assertEqual(self.storage.module_state.get_payload(13, "herbs", default=[]), [])

        self.storage.module_state.save_payload(13, "herbs", [{"plot": 1, "seed": "九叶灵芝"}])
        payload = self.storage.module_state.get_payload(13, "herbs")
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["seed"], "九叶灵芝")

        # 2. 战报统计与胜率
        self.assertEqual(self.storage.battles.get_win_rate(), 0.0)
        self.storage.battles.add_record(BattleRecord(mission_id=1, is_win=True, exp_gain=100))
        self.storage.battles.add_record(BattleRecord(mission_id=2, is_win=True, exp_gain=120))
        self.storage.battles.add_record(BattleRecord(mission_id=3, is_win=False, exp_gain=10))

        self.assertEqual(self.storage.battles.count(), 3)
        self.assertAlmostEqual(self.storage.battles.get_win_rate(), 2.0 / 3.0, places=4)

    def test_05_raw_sql_query_and_execute_escape_hatch(self) -> None:
        """测试 storage.query 与 storage.execute 原生 SQL 逃生通道"""
        # 写入测试数据
        self.storage.player.upsert_profile(
            PlayerProfileRecord(player_id=self.player_id, nickname="逃生测试者", level=120, coins=888888)
        )

        # 1. 执行原生只读查询
        rows = self.storage.query("SELECT nickname, level, coins FROM tb_player_profile WHERE player_id = ?", (self.player_id,))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["nickname"], "逃生测试者")
        self.assertEqual(rows[0]["level"], 120)
        self.assertEqual(rows[0]["coins"], 888888)

        # 2. 执行原生更新写入
        affected = self.storage.execute(
            "UPDATE tb_player_profile SET level = ? WHERE player_id = ?",
            (125, self.player_id),
        )
        self.assertEqual(affected, 1)

        prof = self.storage.player.get_profile()
        self.assertIsNotNone(prof)
        assert prof is not None
        self.assertEqual(prof.level, 125)

    def test_06_eventbus_player_info_and_update_stream(self) -> None:
        """测试 EventBus 下发角色信息与增量变更广播自动切面入库"""
        loop = asyncio.new_event_loop()
        try:
            async def emit_and_drain(mod: int, act: int, payload: bytes) -> None:
                await self.event_bus.emit(mod, act, payload)
                await asyncio.sleep(0.01)

            # 1. 模拟网络层解出 Mod 0 Act 2 封包 (PlayerInfoResp)
            resp_info = PlayerInfoResp(
                nickname="全自动剑客",
                player_id=self.player_id,
                level=80,
                coins=500000,
                ingots=1200,
                power=200,
                town_map_id=29,
                vip_level=3,
                fame=8888,
            )
            # 构造原始编码 (利用 ByteArrayWriter 打包)
            writer = ByteArrayWriter()
            writer.write_utf(resp_info.nickname)
            writer.write_int32(resp_info.level)
            writer.write_int32(resp_info.ingots)
            writer.write_int64(resp_info.coins)
            writer.write_int64(10000)  # health
            writer.write_int64(10000)  # max_health
            writer.write_int32(resp_info.power)
            writer.write_int64(50000)  # exp
            writer.write_int64(100000) # max_exp
            writer.write_int32(resp_info.town_map_id)
            for _ in range(4):
                writer.write_int32(0)
            writer.write_int32(resp_info.vip_level)
            for _ in range(4):
                writer.write_int32(0)
            writer.write_int8(1) # camp_id
            writer.write_int32(0) # townKey
            writer.write_int32(resp_info.fame)
            for _ in range(7):
                writer.write_int32(0)
            writer.write_int32(10) # mission_key

            info_payload = writer.to_bytes()

            # 2. 模拟网络层 emit Mod 0 Act 2
            loop.run_until_complete(emit_and_drain(0, 2, info_payload))
            self.storage.flush()

            # 验证角色档案已自动持久化落盘
            prof = self.storage.player.get_profile()
            self.assertIsNotNone(prof)
            assert prof is not None
            self.assertEqual(prof.nickname, "全自动剑客")
            self.assertEqual(prof.level, 80)
            self.assertEqual(prof.coins, 500000)
            self.assertEqual(prof.ingots, 1200)
            self.assertEqual(prof.power, 200)
            self.assertEqual(prof.town_id, 29)

            # 3. 模拟网络层 emit Mod 0 Act 3 (属性增量更新广播: 等级升到 81, 体力变为 195, 元宝变为 1250)
            upd_resp = PlayerUpdatePlayerDataResp(
                updates={
                    18: 81,   # level
                    19: 1250, # ingots
                    23: 195,  # power
                }
            )
            loop.run_until_complete(emit_and_drain(0, 3, upd_resp.encode_payload()))
            self.storage.flush()

            # 验证增量更新生效
            prof_updated = self.storage.player.get_profile()
            self.assertIsNotNone(prof_updated)
            assert prof_updated is not None
            self.assertEqual(prof_updated.level, 81)
            self.assertEqual(prof_updated.ingots, 1250)
            self.assertEqual(prof_updated.power, 195)
            self.assertEqual(prof_updated.coins, 500000)  # 原属性依然保留
        finally:
            loop.close()

    def test_07_eventbus_battle_and_subsystem_stream(self) -> None:
        """测试 EventBus 下发战斗战报与子系统快照自动切面入库"""
        loop = asyncio.new_event_loop()
        try:
            async def emit_and_drain(mod: int, act: int, payload: bytes) -> None:
                await self.event_bus.emit(mod, act, payload)
                await asyncio.sleep(0.01)

            # 1. 模拟普通副本怪物战斗结算 Mod 4 Act 2
            battle_resp = MissionFightMonsterResp(
                result_code=0,
                is_win=True,
                exp_gain=8800,
                coins_gain=4500,
            )
            loop.run_until_complete(emit_and_drain(4, 2, battle_resp.encode_payload()))
            self.storage.flush()

            recent_battles = self.storage.battles.get_recent(limit=10)
            self.assertEqual(len(recent_battles), 1)
            self.assertTrue(recent_battles[0].is_win)
            self.assertEqual(recent_battles[0].exp_gain, 8800)
            self.assertEqual(recent_battles[0].coins_gain, 4500)

            # 2. 模拟药园收获回执 Mod 13 Act 6
            harvest_resp = FarmHarvestResp(result_code=8, gain_exp=15000, gain_coins=30000)
            loop.run_until_complete(emit_and_drain(13, 6, harvest_resp.encode_payload()))
            self.storage.flush()

            harvest_state = self.storage.module_state.get_payload(13, "last_harvest")
            self.assertIsNotNone(harvest_state)
            self.assertEqual(harvest_state["gain_exp"], 15000)
            self.assertEqual(harvest_state["gain_coins"], 30000)

            # 3. 模拟竞技场挑战次数 Mod 28 Act 13
            sport_resp = SuperSportGetChallengeTimesResp(free_times=7)
            loop.run_until_complete(emit_and_drain(28, 13, sport_resp.encode_payload()))
            self.storage.flush()

            sport_state = self.storage.module_state.get_payload(28, "challenge_times")
            self.assertIsNotNone(sport_state)
            self.assertEqual(sport_state["free_times"], 7)

            # 4. 模拟背包全量物品同步 Mod 2 Act 3
            item_writer = ByteArrayWriter()
            item_writer.write_uint16(2)
            # Item 1: grid_id=1, item_id=101, item_type=1, count=5
            item_writer.write_json([1, 101, 1, 0, 0, 0, 0, 0, 0, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            # Item 2: grid_id=2, item_id=202, item_type=2, count=99
            item_writer.write_json([2, 202, 2, 0, 0, 0, 0, 0, 0, 2, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            loop.run_until_complete(emit_and_drain(2, 3, item_writer.to_bytes()))
            self.storage.flush()

            inv_items = self.storage.inventory.get_items()
            self.assertEqual(len(inv_items), 2)
            self.assertEqual(inv_items[0].grid_id, 1)
            self.assertEqual(inv_items[0].item_id, 101)
            self.assertEqual(inv_items[0].count, 5)
            self.assertEqual(inv_items[1].grid_id, 2)
            self.assertEqual(inv_items[1].item_id, 202)
            self.assertEqual(inv_items[1].count, 99)
        finally:
            loop.close()

    def test_08_hazardous_ingot_audit_trail(self) -> None:
        """测试高危元宝操作审计流水感知与查询追溯"""
        self.subscriber.record_hazardous_audit(
            module_id=28,
            action_id=4,
            action_name="buy_challenge_times",
            allow_ingot=True,
            details={"cost_ingots": 20, "times": 1},
        )
        self.subscriber.record_hazardous_audit(
            module_id=24,
            action_id=5,
            action_name="world_boss_ingot_inspire",
            allow_ingot=True,
            details={"boss_id": 1, "cost_ingots": 10},
        )
        self.storage.flush()

        audits = self.storage.audits.get_recent(limit=10)
        self.assertEqual(len(audits), 2)
        self.assertEqual(audits[0].action_name, "world_boss_ingot_inspire")
        self.assertEqual(audits[0].details["cost_ingots"], 10)
        self.assertTrue(audits[0].allow_ingot)
        self.assertEqual(audits[1].action_name, "buy_challenge_times")

    def test_09_subscriber_asset_transaction_and_offline_change(self) -> None:
        """测试 Subscriber 捕获日常任务变动归因与上线微端差额记录"""
        loop = asyncio.new_event_loop()
        try:
            async def emit_and_drain(mod: int, act: int, payload: bytes) -> None:
                await self.event_bus.emit(mod, act, payload)
                await asyncio.sleep(0.01)

            # 1. 初始化角色上线基础画像
            info_payload1 = self._encode_player_info(coins=1000000, ingots=500)
            loop.run_until_complete(emit_and_drain(0, 2, info_payload1))
            self.storage.flush()

            # 2. 模拟任务执行上下文: farm
            self.context.set_active_task("farm")
            upd_coin = PlayerUpdatePlayerDataResp(
                updates={20: 1080000}  # 铜钱增加 80,000
            )
            loop.run_until_complete(emit_and_drain(0, 3, upd_coin.encode_payload()))
            self.context.clear_active_task()
            self.storage.flush()

            # 验证流水与归因
            txs = self.storage.assets.get_recent_transactions(limit=10)
            self.assertEqual(len(txs), 1)
            self.assertEqual(txs[0].asset_type, "coin")
            self.assertEqual(txs[0].change_type, "income")
            self.assertEqual(txs[0].amount, 80000)
            self.assertEqual(txs[0].balance_after, 1080000)
            self.assertEqual(txs[0].reason, "仙府药园收获")

            # 3. 模拟微端/外部变动 (例如微端离线消耗 50 元宝，并产出 20,000 铜钱)
            info_payload2 = self._encode_player_info(coins=1100000, ingots=450)
            loop.run_until_complete(emit_and_drain(0, 2, info_payload2))
            self.storage.flush()

            # 验证外部差额流水生成
            all_txs = self.storage.assets.get_recent_transactions(limit=10)
            self.assertEqual(len(all_txs), 3)

            # 最新的两条为微端外部变动
            external_txs = [t for t in all_txs if t.reason == "微端/外部变动"]
            self.assertEqual(len(external_txs), 2)

            ingot_tx = [t for t in external_txs if t.asset_type == "ingot"][0]
            self.assertEqual(ingot_tx.change_type, "expense")
            self.assertEqual(ingot_tx.amount, 50)
            self.assertEqual(ingot_tx.balance_after, 450)

            coin_tx = [t for t in external_txs if t.asset_type == "coin"][0]
            self.assertEqual(coin_tx.change_type, "income")
            self.assertEqual(coin_tx.amount, 20000)
            self.assertEqual(coin_tx.balance_after, 1100000)

            # 4. 验证今日汇总
            today = self.storage.assets.get_today_summary()
            self.assertIsNotNone(today)
            assert today is not None
            self.assertEqual(today.closing_coins, 1100000)
            self.assertEqual(today.coins_income, 100000)  # 80000 + 20000
            self.assertEqual(today.closing_ingots, 450)
            self.assertEqual(today.ingots_expense, 50)
        finally:
            loop.close()


if __name__ == "__main__":
    unittest.main()

