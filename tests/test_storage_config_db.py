"""SQLite 配置仓储与无感种子迁移测试套件 (Unit Tests for SQLite Config Store)

验证:
1. 数据库自检建表与 WAL 模式初始化 (tb_accounts, tb_routine_configs, tb_system_settings)
2. 账号强类型 CRUD (add, get, list, update, delete)
3. 账号长连接托管状态 (hosting_enabled) 与防互踢避让状态 (evade_state) 更新
4. 账号级独立 35 项日常子任务配置与元宝安全阈值存取
5. 系统级键值设置存取 (tb_system_settings)
6. 初次启动无感从 config.json 种子数据自动迁移
7. 桥接导出为 AppConfig 对象

@author Ateng
@since 2026-10-16
"""

import json
import os
import shutil
import tempfile
import time
import unittest

from storage.config_db import (
    AccountRecord,
    ConfigDatabase,
    RoutineConfigRecord,
    SystemSettingRecord,
    ALL_ROUTINES,
)


class TestConfigDatabase(unittest.TestCase):
    """SQLite 配置仓储单元测试用例"""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="sxd_test_config_db_")
        self.db_path = os.path.join(self.test_dir, "test_config.sqlite")
        self.seed_json_path = os.path.join(self.test_dir, "seed_config.json")

    def tearDown(self) -> None:
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def _get_db(self, auto_bootstrap: bool = False, seed_json_path: Optional[str] = None) -> ConfigDatabase:
        return ConfigDatabase(
            db_path=self.db_path,
            seed_json_path=seed_json_path,
            auto_bootstrap=auto_bootstrap,
        )

    def test_schema_initialization(self) -> None:
        """测试数据库初次创建、表结构初始化与 WAL 模式"""
        db = self._get_db()
        self.assertTrue(os.path.exists(self.db_path))

        with db.connect() as conn:
            cursor = conn.cursor()
            # 验证 WAL 模式
            cursor.execute("PRAGMA journal_mode;")
            mode = cursor.fetchone()[0]
            self.assertEqual(mode.lower(), "wal")

            # 验证三张核心表已就绪
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = {row[0] for row in cursor.fetchall()}
            self.assertIn("tb_accounts", tables)
            self.assertIn("tb_routine_configs", tables)
            self.assertIn("tb_system_settings", tables)

    def test_account_crud(self) -> None:
        """测试账号的新增、查询、列表、更新与删除"""
        db = self._get_db()

        acc1 = AccountRecord(
            alias="主号",
            platform="fengwanyx",
            username="player1",
            password="pass1_secret",
            server="s138",
            server_id=25268,
            enabled=True,
            hosting_enabled=True,
        )
        acc2 = AccountRecord(
            alias="小号1",
            platform="static",
            username="player2",
            password="pass2_secret",
            server="s140",
            server_id=25270,
            server_host="127.0.0.1",
            server_port=8080,
            enabled=False,
            hosting_enabled=False,
        )

        # 1. 新增
        self.assertTrue(db.add_account(acc1))
        self.assertTrue(db.add_account(acc2))

        # 2. 查询单个
        fetched1 = db.get_account("主号")
        self.assertIsNotNone(fetched1)
        self.assertEqual(fetched1.alias, "主号")
        self.assertEqual(fetched1.username, "player1")
        self.assertEqual(fetched1.password, "pass1_secret")
        self.assertEqual(fetched1.server, "s138")
        self.assertTrue(fetched1.enabled)
        self.assertTrue(fetched1.hosting_enabled)

        # 3. 列表查询
        all_accs = db.list_accounts()
        self.assertEqual(len(all_accs), 2)

        enabled_accs = db.list_accounts(enabled_only=True)
        self.assertEqual(len(enabled_accs), 1)
        self.assertEqual(enabled_accs[0].alias, "主号")

        # 4. 更新
        fetched1.password = "new_pass"
        fetched1.server = "s139"
        self.assertTrue(db.update_account(fetched1))
        updated = db.get_account("主号")
        self.assertEqual(updated.password, "new_pass")
        self.assertEqual(updated.server, "s139")

        # 5. 删除
        self.assertTrue(db.delete_account("小号1"))
        self.assertIsNone(db.get_account("小号1"))
        self.assertEqual(len(db.list_accounts()), 1)

    def test_hosting_and_evade_state(self) -> None:
        """测试在线托管开关与防互踢避让状态流转"""
        db = self._get_db()
        acc = AccountRecord(alias="测试号", username="tester", server="s813")
        db.add_account(acc)

        # 托管状态切换
        db.set_hosting_state("测试号", False)
        f = db.get_account("测试号")
        self.assertFalse(f.hosting_enabled)

        db.set_hosting_state("测试号", True)
        f = db.get_account("测试号")
        self.assertTrue(f.hosting_enabled)

        # 避让状态流转
        now = time.time()
        db.set_evade_state("测试号", evade_state="evading", evade_since=now)
        f = db.get_account("测试号")
        self.assertEqual(f.evade_state, "evading")
        self.assertAlmostEqual(f.evade_since, now, places=1)

        # 恢复托管
        db.set_evade_state("测试号", evade_state="none", evade_since=0.0)
        f = db.get_account("测试号")
        self.assertEqual(f.evade_state, "none")
        self.assertEqual(f.evade_since, 0.0)

    def test_routine_config_storage(self) -> None:
        """测试账号级独立 35 项日常任务开关与元宝安全红线"""
        db = self._get_db()
        acc = AccountRecord(alias="日常号", username="routine_user")
        db.add_account(acc)

        # 默认日常配置检查
        default_cfg = db.get_routine_config("日常号")
        self.assertEqual(default_cfg.alias, "日常号")
        self.assertEqual(default_cfg.allowed_ingots, 0)
        self.assertEqual(set(default_cfg.enabled_routines), set(ALL_ROUTINES))

        # 修改为仅开启药园和招财神符
        custom_routines = ["farm", "money_tree"]
        updated_cfg = RoutineConfigRecord(
            alias="日常号",
            allowed_ingots=50,
            enabled_routines=custom_routines,
        )
        self.assertTrue(db.save_routine_config(updated_cfg))

        saved_cfg = db.get_routine_config("日常号")
        self.assertEqual(saved_cfg.allowed_ingots, 50)
        self.assertEqual(saved_cfg.enabled_routines, ["farm", "money_tree"])

    def test_system_settings_storage(self) -> None:
        """测试系统级键值配置 (Token, 端口等)"""
        db = self._get_db()

        # 默认取空或指定默认值
        self.assertEqual(db.get_setting("web_token"), "")
        self.assertEqual(db.get_setting("web_port", default="8000"), "8000")

        # 设置与读取
        self.assertTrue(db.set_setting("web_token", "secret123"))
        self.assertEqual(db.get_setting("web_token"), "secret123")

        # 更新覆盖
        self.assertTrue(db.set_setting("web_token", "secret456"))
        self.assertEqual(db.get_setting("web_token"), "secret456")

    def test_bootstrap_from_json(self) -> None:
        """测试首次启动自动从 config.json 无感导入数据"""
        seed_data = {
            "settings": {
                "heartbeat_interval_sec": 4.0,
                "enable_heartbeat": True,
                "enable_auto_routine": True,
            },
            "accounts": [
                {
                    "alias": "种子主号",
                    "username": "seed_user_1",
                    "password": "seed_pass_1",
                    "server": "s138",
                    "platform": "fengwanyx",
                    "enabled": True,
                },
                {
                    "alias": "种子小号",
                    "username": "seed_user_2",
                    "password": "seed_pass_2",
                    "server": "s140",
                    "platform": "static",
                    "server_host": "10.0.0.1",
                    "server_port": 8888,
                    "enabled": False,
                },
            ],
        }
        with open(self.seed_json_path, "w", encoding="utf-8") as f:
            json.dump(seed_data, f, ensure_ascii=False)

        # 传入 seed_json_path 初始化 ConfigDatabase
        db = ConfigDatabase(
            db_path=self.db_path,
            seed_json_path=self.seed_json_path,
            auto_bootstrap=True,
        )

        accounts = db.list_accounts()
        self.assertEqual(len(accounts), 2)

        main_acc = db.get_account("种子主号")
        self.assertIsNotNone(main_acc)
        self.assertEqual(main_acc.username, "seed_user_1")
        self.assertTrue(main_acc.enabled)

        alt_acc = db.get_account("种子小号")
        self.assertIsNotNone(alt_acc)
        self.assertEqual(alt_acc.server_host, "10.0.0.1")
        self.assertEqual(alt_acc.server_port, 8888)
        self.assertFalse(alt_acc.enabled)

        # 验证默认日常配置也被初始化
        routine_cfg = db.get_routine_config("种子主号")
        self.assertEqual(routine_cfg.allowed_ingots, 0)
        self.assertEqual(set(routine_cfg.enabled_routines), set(ALL_ROUTINES))

        # 验证重复实例化不会覆盖或重复插入
        db2 = ConfigDatabase(
            db_path=self.db_path,
            seed_json_path=self.seed_json_path,
            auto_bootstrap=True,
        )
        self.assertEqual(len(db2.list_accounts()), 2)

    def test_to_app_config_bridge(self) -> None:
        """测试将 SQLite 配置仓储数据桥接导出为 AppConfig 对象"""
        db = self._get_db()
        db.add_account(
            AccountRecord(
                alias="桥接号",
                username="bridge_user",
                password="pwd",
                server="s813",
                enabled=True,
            )
        )

        app_config = db.to_app_config()
        self.assertEqual(len(app_config.accounts), 1)
        self.assertEqual(app_config.accounts[0].alias, "桥接号")
        self.assertEqual(app_config.accounts[0].username, "bridge_user")
        self.assertEqual(len(app_config.enabled_accounts), 1)



if __name__ == "__main__":
    unittest.main()
