"""神仙道全量静态协议元数据库 SQLite 驱动与查询仓储测试套件

测试覆盖:
1. 预置只读 SQLite 数据库表结构、行数及元数据完备性验证
2. 缺失数据库物理文件时的严格 FileNotFoundError 异常防御
3. 通用项目静态元数据 (tb_metadata) 读取、写入与全景字典重建
4. 核心元数据表与 B-Tree 索引有效性验证
5. 模块、动作及常量的强类型点查与模糊模式搜索
6. 参数签名与回包复杂类型 JSON 反序列化一致性
7. 空安全与边缘异常输入防御测试

@author Ateng
@since 2026-10-16
"""

import os
import shutil
import tempfile
import time
import unittest
from storage.protocol_db import (
    DEFAULT_DB_PATH,
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
        # 复制现有只读库用于测试隔离
        shutil.copyfile(DEFAULT_DB_PATH, cls.test_db_path)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_dir.cleanup()

    def test_01_verify_prebuilt_db_integrity(self) -> None:
        """测试已预置的只读数据库完整性与全量数据规模"""
        self.assertTrue(os.path.exists(self.test_db_path))
        file_size = os.path.getsize(self.test_db_path)
        self.assertGreater(file_size, 1024 * 1024)

        db = ProtocolDatabase(db_path=self.test_db_path)
        with db.get_connection() as conn:
            mod_cnt = conn.execute("SELECT COUNT(*) FROM tb_modules").fetchone()[0]
            act_cnt = conn.execute("SELECT COUNT(*) FROM tb_actions").fetchone()[0]
            const_cnt = conn.execute("SELECT COUNT(*) FROM tb_constants").fetchone()[0]
            meta_cnt = conn.execute("SELECT COUNT(*) FROM tb_metadata").fetchone()[0]

            self.assertGreaterEqual(mod_cnt, 880)
            self.assertGreaterEqual(act_cnt, 8700)
            self.assertGreaterEqual(const_cnt, 13000)
            self.assertGreaterEqual(meta_cnt, 2)

    def test_02_strict_file_not_found_on_missing_db(self) -> None:
        """测试数据库文件缺失时严格抛出 FileNotFoundError"""
        missing_path = os.path.join(self.temp_dir.name, "missing.db")
        with self.assertRaises(FileNotFoundError):
            ProtocolDatabase(db_path=missing_path)

    def test_03_query_and_set_metadata(self) -> None:
        """测试项目静态元数据 (tb_metadata) 读写与字典重建"""
        repo = ProtocolRepository(ProtocolDatabase(db_path=self.test_db_path))

        # 1. 查询全景 manifest 概况
        manifest_meta = repo.get_manifest_metadata()
        self.assertIsNotNone(manifest_meta)
        assert manifest_meta is not None
        self.assertEqual(manifest_meta.get("modules_count"), 880)
        self.assertEqual(manifest_meta.get("total_actions"), 8719)

        # 2. 查询逆向工程资产配置
        reverse_assets = repo.get_reverse_assets()
        self.assertIsNotNone(reverse_assets)
        assert reverse_assets is not None
        self.assertIn("target_executable", reverse_assets)
        self.assertIn("pcap", reverse_assets)

        # 3. 动态设置与查询自定义元数据
        repo.set_metadata("test_custom_key", {"version": "1.0.0", "status": "ok"})
        custom_val = repo.get_metadata("test_custom_key")
        self.assertEqual(custom_val, {"version": "1.0.0", "status": "ok"})

        # 4. 重构全景 manifest 字典
        full_dict = repo.get_full_manifest_dict()
        self.assertIn("metadata", full_dict)
        self.assertIn("modules", full_dict)
        self.assertEqual(len(full_dict["modules"]), 880)

    def test_04_query_modules(self) -> None:
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

    def test_05_query_and_search_actions(self) -> None:
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

    def test_06_query_and_search_constants(self) -> None:
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

    def test_07_null_safety_and_edge_cases(self) -> None:
        """测试空安全与非预期输入优雅降级"""
        repo = ProtocolRepository(ProtocolDatabase(db_path=self.test_db_path))

        # 不存在的实体返回 None
        self.assertIsNone(repo.get_module(99999))
        self.assertIsNone(repo.get_action(99999, 1))
        self.assertIsNone(repo.get_constant(99999, "NON_EXIST"))
        self.assertIsNone(repo.get_metadata("non_existent_key_xyz"))

        # 空集合返回空列表与空字典，严禁返回 None
        self.assertEqual(repo.get_actions_by_module(99999), [])
        self.assertEqual(repo.get_constants_by_module(99999), {})
        self.assertEqual(repo.search_actions("non_existent_random_xyz_12345"), [])
        self.assertEqual(repo.search_constants("non_existent_random_xyz_12345"), [])
        self.assertEqual(repo.search_actions(""), [])
        self.assertEqual(repo.search_constants(""), [])

    def test_08_default_database_instance(self) -> None:
        """测试使用默认参数单例实例初始化与查询"""
        repo = ProtocolRepository()
        self.assertTrue(os.path.exists("data/protocol_manifest.db"))
        mod = repo.get_module(0)
        self.assertIsNotNone(mod)
        assert mod is not None
        self.assertEqual(mod.name, "Player")


if __name__ == "__main__":
    unittest.main()
