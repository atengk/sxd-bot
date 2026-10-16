"""神仙道角色私有 SQLite 数据库、异步工作线程与 FIFO 滚动淘汰测试套件

测试覆盖:
1. 角色私有数据库物理隔离与 WAL 高并发模式建表校验
2. 角色画像、背包装备、子系统 JSON 快照读写一致性
3. 战报流水与高危元宝审计记录 FIFO 自动滚动淘汰 (边界测试)
4. 多角色、多区服独立数据库完全物理隔离无干扰
5. StorageWorker 后台专职写入线程批量入库与优雅停机
6. WAL 模式下高频并发读写无数据库锁冲突 (Zero Database Locked)

@author Ateng
@since 2026-10-16
"""

import os
import tempfile
import threading
import time
import unittest
from storage.player_db import (
    PlayerDatabase,
    PlayerProfileRecord,
    InventoryItemRecord,
    ModuleStateRecord,
    BattleRecord,
    AuditLogRecord,
)
from storage.worker import StorageWorker, StorageTask


class TestPlayerDatabaseAndWorker(unittest.TestCase):
    """测试角色私有数据库与后台写入工作线程

    @author Ateng
    @since 2026-10-16
    """

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = self.temp_dir.name
        self.db = PlayerDatabase(server_id=813, player_id=1001, base_dir=self.base_dir)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_01_database_init_and_wal_mode(self) -> None:
        """测试角色私有库初始化并验证 WAL 模式与 5 张核心表"""
        self.assertTrue(os.path.exists(self.db.db_path))

        with self.db.connect() as conn:
            # 1. 验证 WAL 模式
            mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
            self.assertEqual(mode.lower(), "wal")

            # 2. 验证 5 张核心表存在
            tables = [
                r[0]
                for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
            ]
            self.assertIn("tb_player_profile", tables)
            self.assertIn("tb_inventory", tables)
            self.assertIn("tb_module_state", tables)
            self.assertIn("tb_battle_records", tables)
            self.assertIn("tb_audit_log", tables)

    def test_02_player_profile_upsert_and_query(self) -> None:
        """测试角色画像属性持久化与覆盖更新"""
        # 初始为空
        self.assertIsNone(self.db.get_player_profile())

        # 插入初始数据
        p1 = PlayerProfileRecord(
            player_id=1001,
            nickname="剑破苍穹",
            level=85,
            coins=5000000,
            ingots=1200,
            power=180,
            fame=120000,
            vip_level=6,
            town_id=10,
        )
        self.db.upsert_player_profile(p1)

        queried1 = self.db.get_player_profile()
        self.assertIsNotNone(queried1)
        assert queried1 is not None
        self.assertEqual(queried1.nickname, "剑破苍穹")
        self.assertEqual(queried1.level, 85)
        self.assertEqual(queried1.coins, 5000000)
        self.assertEqual(queried1.ingots, 1200)

        # 覆盖更新 (升到 86 级，消耗体力)
        p2 = PlayerProfileRecord(
            player_id=1001,
            nickname="剑破苍穹",
            level=86,
            coins=5200000,
            ingots=1200,
            power=175,
            fame=120500,
            vip_level=6,
            town_id=10,
        )
        self.db.upsert_player_profile(p2)

        queried2 = self.db.get_player_profile()
        self.assertIsNotNone(queried2)
        assert queried2 is not None
        self.assertEqual(queried2.level, 86)
        self.assertEqual(queried2.power, 175)

    def test_03_inventory_items_crud(self) -> None:
        """测试背包装备物品批量更新、查询与删除"""
        self.assertEqual(self.db.get_inventory_items(), [])

        items = [
            InventoryItemRecord(grid_id=1, item_id=101, count=1, item_type=1, props={"name": "太白飞剑", "enhance": 10}),
            InventoryItemRecord(grid_id=2, item_id=205, count=99, item_type=2, props={"name": "九品灵芝草"}),
            InventoryItemRecord(grid_id=3, item_id=301, count=5, item_type=3, props={"name": "天蚕丝"}),
        ]
        self.db.upsert_inventory_items(items)

        current_items = self.db.get_inventory_items()
        self.assertEqual(len(current_items), 3)
        self.assertEqual(current_items[0].props["name"], "太白飞剑")
        self.assertEqual(current_items[1].count, 99)

        # 移除第 2 格道具
        self.db.remove_inventory_item(grid_id=2)
        remaining = self.db.get_inventory_items()
        self.assertEqual(len(remaining), 2)
        self.assertEqual([i.grid_id for i in remaining], [1, 3])

    def test_04_module_state_json_snapshots(self) -> None:
        """测试子系统半结构化 JSON 状态快照保存与点查"""
        # 1. 模拟保存药园地块快照 (Mod 13)
        farm_state = ModuleStateRecord(
            module_id=13,
            state_key="plots",
            payload={
                "plots_count": 3,
                "plots": [
                    {"plot_id": 1, "herbs_type": 1, "is_ready": True},
                    {"plot_id": 2, "herbs_type": 0, "is_ready": False},
                ],
            },
        )
        self.db.set_module_state(farm_state)

        queried_farm = self.db.get_module_state(13, "plots")
        self.assertIsNotNone(queried_farm)
        assert queried_farm is not None
        self.assertEqual(queried_farm.payload["plots_count"], 3)
        self.assertTrue(queried_farm.payload["plots"][0]["is_ready"])

        # 2. 查询不存在的状态返回 None
        self.assertIsNone(self.db.get_module_state(13, "non_existent"))

    def test_05_fifo_rolling_eviction_retention(self) -> None:
        """测试战斗记录与审计日志达到阈值时的 FIFO 自动滚动淘汰"""
        # 1. 连续插入 25 条战报，设置 max_records=10
        for i in range(1, 26):
            rec = BattleRecord(
                mission_id=100 + i,
                is_win=(i % 2 == 0),
                exp_gain=1000 * i,
                coins_gain=500 * i,
                payload={"turn": i},
            )
            self.db.add_battle_record(rec, max_records=10)

        # 验证仅保留最新 10 条 (mission_id 应当为 116 至 125)
        recent_battles = self.db.get_recent_battle_records(limit=50)
        self.assertEqual(len(recent_battles), 10)
        self.assertEqual(recent_battles[0].mission_id, 125)  # 最新在最前
        self.assertEqual(recent_battles[-1].mission_id, 116)

        # 2. 连续插入 15 条元宝审计记录，设置 max_records=5
        for i in range(1, 16):
            audit = AuditLogRecord(
                module_id=28,
                action_id=4,
                action_name="buy_challenge_times",
                allow_ingot=True,
                details={"times": i, "cost": i * 10},
            )
            self.db.add_audit_log(audit, max_records=5)

        recent_audits = self.db.get_recent_audit_logs(limit=50)
        self.assertEqual(len(recent_audits), 5)
        self.assertEqual(recent_audits[0].details["times"], 15)
        self.assertEqual(recent_audits[-1].details["times"], 11)

    def test_06_multi_player_physical_isolation(self) -> None:
        """测试不同角色及不同服务器独立建库且完全隔离"""
        db_p1 = PlayerDatabase(server_id=813, player_id=1001, base_dir=self.base_dir)
        db_p2 = PlayerDatabase(server_id=813, player_id=1002, base_dir=self.base_dir)

        # 分别写入不同昵称和等级
        db_p1.upsert_player_profile(PlayerProfileRecord(player_id=1001, nickname="角色一", level=50))
        db_p2.upsert_player_profile(PlayerProfileRecord(player_id=1002, nickname="角色二", level=90))

        # 验证互不干扰
        p1 = db_p1.get_player_profile()
        p2 = db_p2.get_player_profile()
        self.assertIsNotNone(p1)
        self.assertIsNotNone(p2)
        assert p1 is not None and p2 is not None
        self.assertEqual(p1.nickname, "角色一")
        self.assertEqual(p1.level, 50)
        self.assertEqual(p2.nickname, "角色二")
        self.assertEqual(p2.level, 90)

        # 磁盘上生成了两个独立的文件
        self.assertTrue(os.path.exists(db_p1.db_path))
        self.assertTrue(os.path.exists(db_p2.db_path))
        self.assertNotEqual(db_p1.db_path, db_p2.db_path)

    def test_07_storage_worker_pipeline(self) -> None:
        """测试 StorageWorker 后台专职写入线程批量入库与优雅关机"""
        worker = StorageWorker(self.db, batch_size=10, flush_interval=0.02)
        worker.start()
        self.assertTrue(worker.is_running)

        # 异步非阻塞提交各类任务
        worker.submit_profile(PlayerProfileRecord(player_id=1001, nickname="异步战神", level=77))
        worker.submit_inventory([
            InventoryItemRecord(grid_id=10, item_id=888, count=1, props={"desc": "玄武战甲"}),
        ])
        worker.submit_module_state(ModuleStateRecord(module_id=22, state_key="fate_bag", payload={"bag_size": 20}))
        worker.submit_battle_record(BattleRecord(mission_id=88, is_win=True, exp_gain=6666))
        worker.submit_audit_log(AuditLogRecord(module_id=24, action_id=5, action_name="ingot_inspire", allow_ingot=True))

        # 刷新并优雅关机
        worker.flush()
        worker.stop()
        self.assertFalse(worker.is_running)

        # 验证数据库中均已成功持久化
        prof = self.db.get_player_profile()
        self.assertIsNotNone(prof)
        assert prof is not None
        self.assertEqual(prof.nickname, "异步战神")

        inv = self.db.get_inventory_items()
        self.assertEqual(len(inv), 1)
        self.assertEqual(inv[0].props["desc"], "玄武战甲")

        fate = self.db.get_module_state(22, "fate_bag")
        self.assertIsNotNone(fate)
        assert fate is not None
        self.assertEqual(fate.payload["bag_size"], 20)

        battles = self.db.get_recent_battle_records()
        self.assertEqual(len(battles), 1)
        self.assertEqual(battles[0].mission_id, 88)

        audits = self.db.get_recent_audit_logs()
        self.assertEqual(len(audits), 1)
        self.assertEqual(audits[0].action_name, "ingot_inspire")

    def test_08_concurrent_wal_reads_and_writes(self) -> None:
        """测试 WAL 模式下后台高频写入与前台并发读取无锁死 (Zero Database Locked)"""
        worker = StorageWorker(self.db, batch_size=5, flush_interval=0.01)
        worker.start()

        write_count = 50
        errors = []

        # 1. 提交 50 条后台写任务
        for i in range(write_count):
            worker.submit_battle_record(
                BattleRecord(mission_id=i, is_win=True, exp_gain=i * 10)
            )

        # 2. 前台并发线程同时执行 100 次读操作
        def reader_task() -> None:
            try:
                for _ in range(100):
                    _ = self.db.get_player_profile()
                    _ = self.db.get_recent_battle_records(limit=10)
                    time.sleep(0.001)
            except Exception as e:
                errors.append(e)

        reader_thread = threading.Thread(target=reader_task)
        reader_thread.start()
        reader_thread.join()

        worker.flush()
        worker.stop()

        # 验证无任何异常产生 (WAL 读写并发无锁争用)
        self.assertEqual(errors, [])
        all_battles = self.db.get_recent_battle_records(limit=100)
        self.assertEqual(len(all_battles), write_count)


if __name__ == "__main__":
    unittest.main()
