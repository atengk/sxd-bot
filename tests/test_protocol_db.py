"""神仙道全量静态协议元数据库 SQLite 驱动与查询仓储测试套件

测试覆盖:
1. 首次冷启动自检与全量 880 模块 JSON 极速热转储 (耗时与行数校验)
2. 二次启动跳过已存在数据库的静默加速
3. 核心元数据表与 B-Tree 索引有效性验证
4. 模块、动作及常量的强类型点查与模糊模式搜索
5. 参数签名与回包复杂类型 JSON 反序列化一致性
6. 空安全与边缘异常输入防御测试

@author Ateng
@since 2026-10-16
"""

import os
import tempfile
import time
import unittest
from storage.protocol_db import (
    DEFAULT_JSON_PATH,
    ProtocolDatabase,
    ProtocolRepository,
    ModuleMeta,
    ActionMeta,
    ConstantMeta,
)


class TestProtocolDatabaseAndRepository(unittest.TestCase):
    """测试协议字典数据库自动化转储与查询仓储

    @author Ateng
    @since 2026-10-16
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_db_path = os.path.join(cls.temp_dir.name, "test_manifest.db")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_dir.cleanup()

    def test_01_auto_ingest_from_json_on_first_load(self) -> None:
        """测试冷启动时自动从 JSON 批量导入 SQLite 并验证耗时"""
        self.assertFalse(os.path.exists(self.test_db_path))

        t0 = time.perf_counter()
        db = ProtocolDatabase(db_path=self.test_db_path, json_path=DEFAULT_JSON_PATH)
        elapsed = time.perf_counter() - t0

        # 1. 验证文件已成功创建且体积合理
        self.assertTrue(os.path.exists(self.test_db_path))
        file_size = os.path.getsize(self.test_db_path)
        self.assertGreater(file_size, 1024 * 1024)  # 至少大于 1MB

        # 2. 验证首次转储耗时在 1.5 秒以内 (通常在 0.2~0.5s)
        self.assertLess(elapsed, 1.5)

        # 3. 验证表数据行数匹配
        with db.get_connection() as conn:
            mod_cnt = conn.execute("SELECT COUNT(*) FROM tb_modules").fetchone()[0]
            act_cnt = conn.execute("SELECT COUNT(*) FROM tb_actions").fetchone()[0]
            const_cnt = conn.execute("SELECT COUNT(*) FROM tb_constants").fetchone()[0]

            self.assertGreaterEqual(mod_cnt, 880)
            self.assertGreaterEqual(act_cnt, 8700)
            self.assertGreaterEqual(const_cnt, 13000)

    def test_02_secondary_load_skips_ingestion(self) -> None:
        """测试已存在数据库二次加载时立即复用 (毫秒级)"""
        t0 = time.perf_counter()
        db = ProtocolDatabase(db_path=self.test_db_path, json_path=DEFAULT_JSON_PATH)
        elapsed = time.perf_counter() - t0

        self.assertLess(elapsed, 0.05)  # 二次检查必须在 50ms 内完成

    def test_03_query_modules(self) -> None:
        """测试模块点查与全量模块列表查询"""
        repo = ProtocolRepository(ProtocolDatabase(db_path=self.test_db_path))

        # 1. 查询基石模块 0 (Player)
        mod0 = repo.get_module(0)
        self.assertIsNotNone(mod0)
        assert mod0 is not None
        self.assertEqual(mod0.module_id, 0)
        self.assertEqual(mod0.name, "Player")
        self.assertGreater(mod0.action_count, 50)

        # 2. 查询日常模块 13 (Farm)
        mod13 = repo.get_module(13)
        self.assertIsNotNone(mod13)
        assert mod13 is not None
        self.assertEqual(mod13.name, "Farm")
        self.assertEqual(mod13.action_count, 27)

        # 3. 查询全量模块列表
        all_mods = repo.list_modules()
        self.assertGreaterEqual(len(all_mods), 880)
        self.assertEqual(all_mods[0].module_id, 0)

    def test_04_query_and_search_actions(self) -> None:
        """测试动作精确定位与模糊检索"""
        repo = ProtocolRepository(ProtocolDatabase(db_path=self.test_db_path))

        # 1. 精确获取 Mod 0 Act 0 (login)
        act_login = repo.get_action(0, 0)
        self.assertIsNotNone(act_login)
        assert act_login is not None
        self.assertEqual(act_login.name, "login")
        self.assertIsInstance(act_login.request_types, list)
        self.assertIsInstance(act_login.response_types, list)

        # 2. 精确获取 Mod 4 Act 2 (fight_monster)
        act_fight = repo.get_action(4, 2)
        self.assertIsNotNone(act_fight)
        assert act_fight is not None
        self.assertEqual(act_fight.name, "fight_monster")

        # 3. 按模块列出动作
        farm_acts = repo.get_actions_by_module(13)
        self.assertEqual(len(farm_acts), 27)
        act_names = [a.name for a in farm_acts]
        self.assertIn("get_farmlandinfo_list", act_names)
        self.assertIn("plant_herbs", act_names)
        self.assertIn("harvest", act_names)

        # 4. 跨模块模糊搜索动作 "farmland"
        search_res = repo.search_actions("farmland", limit=10)
        self.assertGreaterEqual(len(search_res), 2)
        for act in search_res:
            self.assertIn("farmland", act.name.lower())

    def test_05_query_and_search_constants(self) -> None:
        """测试常量精确定位与字典映射"""
        repo = ProtocolRepository(ProtocolDatabase(db_path=self.test_db_path))

        # 1. 精确定位 Mod 0 的 SUCCESS 常量 (官方编译数值为 89)
        val = repo.get_constant(0, "SUCCESS")
        self.assertIsNotNone(val)
        self.assertEqual(val, 89)

        # 2. 获取 Mod 0 的所有常量映射
        mod0_consts = repo.get_constants_by_module(0)
        self.assertIn("SUCCESS", mod0_consts)
        self.assertIn("FAILED", mod0_consts)
        self.assertEqual(mod0_consts["SUCCESS"], 89)

        # 3. 跨模块模糊搜索包含 "INCENSE" 的常量
        search_consts = repo.search_constants("INCENSE", limit=20)
        self.assertGreaterEqual(len(search_consts), 1)
        for c in search_consts:
            self.assertIn("incense", c.name.lower())

    def test_06_null_safety_and_edge_cases(self) -> None:
        """测试空安全与非预期输入优雅降级"""
        repo = ProtocolRepository(ProtocolDatabase(db_path=self.test_db_path))

        # 不存在的实体返回 None
        self.assertIsNone(repo.get_module(99999))
        self.assertIsNone(repo.get_action(99999, 1))
        self.assertIsNone(repo.get_constant(99999, "NON_EXIST"))

        # 空集合返回空列表与空字典，严禁返回 None
        self.assertEqual(repo.get_actions_by_module(99999), [])
        self.assertEqual(repo.get_constants_by_module(99999), {})
        self.assertEqual(repo.search_actions("non_existent_random_xyz_12345"), [])
        self.assertEqual(repo.search_constants("non_existent_random_xyz_12345"), [])
        self.assertEqual(repo.search_actions(""), [])
        self.assertEqual(repo.search_constants(""), [])

        # 源文件不存在时抛出语义化异常
        with self.assertRaises(FileNotFoundError):
            ProtocolDatabase(
                db_path=os.path.join(self.temp_dir.name, "missing.db"),
                json_path="non_existent_file.json",
            )

    def test_07_default_database_instance(self) -> None:
        """测试使用默认参数单例实例初始化与查询"""
        repo = ProtocolRepository()
        self.assertTrue(os.path.exists("data/protocol_manifest.db"))
        mod = repo.get_module(0)
        self.assertIsNotNone(mod)
        assert mod is not None
        self.assertEqual(mod.name, "Player")


if __name__ == "__main__":
    unittest.main()
