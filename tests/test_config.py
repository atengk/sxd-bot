"""配置管理与多账号解析单元测试 (Unit Tests for Configuration & Multi-Account)

验证精简配置文件结构、多账号调度过滤、Docker 环境变量展开与旧版格式兼容。

@author Ateng
@since 2026-10-16
"""

import json
import os
import unittest
from unittest.mock import patch, MagicMock

from core.config import AccountConfig, SettingsConfig, AppConfig, ConfigManager, expand_env_vars
from network.web_auth import WebAuthFetcher, GatewayCredentials


class TestConfigManager(unittest.TestCase):
    """配置管理与多账号解析测试用例集"""

    def setUp(self) -> None:
        """清理测试可能干扰的环境变量"""
        self.cleanup_keys = [
            "SXD_USERNAME",
            "SXD_PASSWORD",
            "SXD_SERVER",
            "SXD_ALIAS",
            "SXD_PLATFORM",
            "SXD_ACCOUNTS_JSON",
            "TEST_VAR_A",
            "TEST_VAR_B",
        ]
        for key in self.cleanup_keys:
            os.environ.pop(key, None)

    def tearDown(self) -> None:
        """还原测试环境变量"""
        for key in self.cleanup_keys:
            os.environ.pop(key, None)

    def test_expand_env_vars_with_default(self) -> None:
        """验证环境变量占位符替换与默认值回退"""
        os.environ["TEST_VAR_A"] = "real_value_a"

        # 1. 存在环境变量
        res1 = expand_env_vars("${TEST_VAR_A}")
        self.assertEqual(res1, "real_value_a")

        # 2. 存在环境变量且带有默认值
        res2 = expand_env_vars("${TEST_VAR_A:-fallback_val}")
        self.assertEqual(res2, "real_value_a")

        # 3. 不存在环境变量，回退默认值
        res3 = expand_env_vars("${TEST_VAR_B:-fallback_b}")
        self.assertEqual(res3, "fallback_b")

        # 4. 不存在环境变量且无默认值
        res4 = expand_env_vars("${TEST_VAR_B}")
        self.assertEqual(res4, "")

        # 5. 字典与列表递归替换
        nested = {
            "name": "${TEST_VAR_A}",
            "list": ["item_${TEST_VAR_B:-default_b}", 123],
            "sub": {"val": "${TEST_VAR_A}"},
        }
        res_nested = expand_env_vars(nested)
        self.assertEqual(res_nested["name"], "real_value_a")
        self.assertEqual(res_nested["list"][0], "item_default_b")
        self.assertEqual(res_nested["list"][1], 123)
        self.assertEqual(res_nested["sub"]["val"], "real_value_a")

    def test_multi_account_loading_and_filtering(self) -> None:
        """验证标准多账号配置加载与启用过滤"""
        raw = {
            "settings": {
                "heartbeat_interval_sec": 5.0,
                "enable_heartbeat": True,
            },
            "accounts": [
                {
                    "alias": "主号",
                    "username": "user1",
                    "password": "mock_password_1",
                    "server": "s813",
                    "enabled": True,
                    "platform": "fengwanyx",
                },
                {
                    "alias": "小号",
                    "username": "user2",
                    "password": "mock_password_2",
                    "server": "s814",
                    "enabled": False,
                    "platform": "fengwanyx",
                },
                {
                    "alias": "直连号",
                    "username": "user3",
                    "server": "s815",
                    "enabled": True,
                    "server_host": "10.0.0.1",
                    "server_port": 8381,
                },
            ],
        }

        app_config = ConfigManager.load_from_dict(raw)
        self.assertEqual(len(app_config.accounts), 3)

        # 过滤已启用账号
        enabled = app_config.enabled_accounts
        self.assertEqual(len(enabled), 2)
        self.assertEqual([a.username for a in enabled], ["user1", "user3"])

        # 按 alias 与 username 检索账号
        acc_main = app_config.find_account("主号")
        self.assertIsNotNone(acc_main)
        self.assertEqual(acc_main.username, "user1")
        self.assertEqual(acc_main.display_name, "主号 (user1)")

        acc_alt = app_config.find_account("user2")
        self.assertIsNotNone(acc_alt)
        self.assertEqual(acc_alt.alias, "小号")

        self.assertIsNone(app_config.find_account("non_existent"))

    def test_docker_zero_config_via_env(self) -> None:
        """验证 Docker 容器环境下单账号通过环境变量零配置直启"""
        os.environ["SXD_USERNAME"] = "docker_hero"
        os.environ["SXD_PASSWORD"] = "docker_secret"
        os.environ["SXD_SERVER"] = "s999"
        os.environ["SXD_ALIAS"] = "容器号"

        # 传入不存在的配置文件路径
        app_config = ConfigManager.load(config_path="non_existent_config.json")

        self.assertEqual(len(app_config.accounts), 1)
        acc = app_config.accounts[0]
        self.assertEqual(acc.username, "docker_hero")
        self.assertEqual(acc.password, "docker_secret")
        self.assertEqual(acc.server, "s999")
        self.assertEqual(acc.alias, "容器号")
        self.assertTrue(acc.enabled)

    def test_docker_multi_account_json_injection(self) -> None:
        """验证 Docker 环境变量 SXD_ACCOUNTS_JSON 批量注入多账号"""
        accounts_payload = [
            {"alias": "云端1号", "username": "cloud_u1", "password": "p1", "server": "s1"},
            {"alias": "云端2号", "username": "cloud_u2", "password": "p2", "server": "s2"},
        ]
        os.environ["SXD_ACCOUNTS_JSON"] = json.dumps(accounts_payload)

        app_config = ConfigManager.load(config_path=None)
        self.assertEqual(len(app_config.accounts), 2)
        self.assertEqual(app_config.accounts[0].alias, "云端1号")
        self.assertEqual(app_config.accounts[1].alias, "云端2号")

    def test_legacy_single_account_compatibility(self) -> None:
        """验证旧版单账号 config.json 结构向下兼容无缝映射"""
        legacy_raw = {
            "auth_mode": "static",
            "static_credentials": {
                "server_host": "192.168.1.100",
                "server_port": 8888,
                "player_name": "legacy_player",
                "hash_code": "legacy_hash",
                "time": "1700000000",
                "platform": "legacy_plat",
                "server_id": 9999,
            },
            "automation": {
                "enable_heartbeat": True,
                "heartbeat_interval_sec": 4.0,
            },
        }

        app_config = ConfigManager.load_from_dict(legacy_raw)
        self.assertEqual(len(app_config.accounts), 1)
        acc = app_config.accounts[0]
        self.assertEqual(acc.username, "legacy_player")
        self.assertEqual(acc.server_host, "192.168.1.100")
        self.assertEqual(acc.server_port, 8888)
        self.assertEqual(acc.server_id, 9999)
        self.assertEqual(acc.hash_code, "legacy_hash")
        self.assertEqual(acc.time, "1700000000")
        self.assertEqual(acc.platform, "legacy_plat")
        self.assertEqual(app_config.settings.heartbeat_interval_sec, 4.0)

    def test_resolve_credentials_static_and_dynamic(self) -> None:
        """验证 WebAuthFetcher.resolve_credentials 动态登录与静态直连回退"""
        # 1. 静态直连账号
        static_acc = AccountConfig(
            alias="测试直连",
            username="static_user",
            server_host="127.0.0.1",
            server_port=8080,
            platform="test_plat",
            server_id=1234,
            hash_code="h_code",
            time="t_stamp",
        )
        creds = WebAuthFetcher.resolve_credentials(static_acc)
        self.assertIsNotNone(creds)
        self.assertEqual(creds.server_host, "127.0.0.1")
        self.assertEqual(creds.server_port, 8080)
        self.assertEqual(creds.player_name, "static_user")
        self.assertEqual(creds.server_id, 1234)
        self.assertEqual(creds.hash_code, "h_code")

        # 2. 动态 Web 认证账号 (Mock auto_login)
        dyn_acc = AccountConfig(
            alias="动态号",
            username="dyn_user",
            password="dyn_password",
            server="s813",
        )
        mock_gateway = GatewayCredentials(
            server_host="gateway.sxd.com",
            server_port=8381,
            player_name="dyn_user",
            hash_code="dyn_token",
            time="1700000001",
            platform="fengwanyx",
            server_id=25268,
        )
        with patch.object(WebAuthFetcher, "auto_login", return_value=mock_gateway) as mock_login:
            dyn_creds = WebAuthFetcher.resolve_credentials(dyn_acc)
            self.assertIsNotNone(dyn_creds)
            self.assertEqual(dyn_creds.server_host, "gateway.sxd.com")
            self.assertEqual(dyn_creds.hash_code, "dyn_token")
            mock_login.assert_called_once_with(
                username="dyn_user",
                password="dyn_password",
                server="s813",
                platform="fengwanyx",
            )


if __name__ == "__main__":
    unittest.main()
