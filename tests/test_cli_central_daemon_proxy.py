"""CLI 中央服务代理模式 (Central Daemon Proxy) 单元测试套件

测试驱动开发 (TDD) 覆盖:
1. DaemonProxy 探针健康检查 (is_alive 判定在线与离线)
2. DaemonProxy 只读查询代理 (assets, roles, assistant, pack, all) 避免双 Socket 冲突
3. DaemonProxy 日常流水线远程调度触发 (trigger_routine)
4. Daemon 离线状态或 --no-proxy 时的自动降级 (Fallback 到本地 SQLite 仓储)
5. CLI web 子命令参数解析与 Uvicorn 启动集成
6. main.py 对 Central Daemon Proxy 的透明路由接入

@author Ateng
@since 2026-10-16
"""

import json
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch, MagicMock

import httpx

from cli.daemon_proxy import DaemonProxy
from storage.config_db import ConfigDatabase, AccountRecord


class TestCLICentralDaemonProxy(unittest.TestCase):
    """CLI 中央服务代理与全量回归测试集"""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="sxd_test_proxy_")
        self.db_path = os.path.join(self.test_dir, "test_config.sqlite")
        self.db = ConfigDatabase(db_path=self.db_path, auto_bootstrap=False)
        self.acc1 = AccountRecord(
            alias="主号",
            platform="fengwanyx",
            username="player_main",
            password="pass_main",
            server="s813",
            enabled=True,
            hosting_enabled=True,
        )
        self.db.add_account(self.acc1)

    def tearDown(self) -> None:
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_daemon_proxy_is_alive_online(self) -> None:
        """测试 DaemonProxy 在服务端 200 OK 时正确判定在线"""
        proxy = DaemonProxy(base_url="http://127.0.0.1:8000")
        with patch("httpx.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"status": "ok", "uptime_sec": 12.3}
            mock_get.return_value = mock_resp

            self.assertTrue(proxy.is_alive())
            mock_get.assert_called_once_with(
                "http://127.0.0.1:8000/api/health",
                timeout=1.0,
            )

    def test_daemon_proxy_is_alive_offline(self) -> None:
        """测试 DaemonProxy 在连接拒绝或超时时正确判定离线"""
        proxy = DaemonProxy(base_url="http://127.0.0.1:8000")
        with patch("httpx.get", side_effect=httpx.ConnectError("Connection refused")):
            self.assertFalse(proxy.is_alive())

        with patch("httpx.get", side_effect=httpx.TimeoutException("Timeout")):
            self.assertFalse(proxy.is_alive())

    def test_daemon_proxy_query_assets_telemetry(self) -> None:
        """测试通过 DaemonProxy 代理查询角色资产画像，避免双 Socket 冲突"""
        proxy = DaemonProxy(base_url="http://127.0.0.1:8000", token="test_token")
        mock_telemetry_payload = {
            "alias": "主号",
            "player_id": 1001,
            "nickname": "神威剑仙",
            "level": 128,
            "vip_level": 6,
            "coins": 182490120,
            "ingots": 36800,
            "power": 185,
            "max_power": 200,
            "fame": 824000,
            "town_id": 1,
            "town_name": "小渔村",
            "roles": [
                {
                    "role_id": 1,
                    "name": "神威剑仙",
                    "level": 128,
                    "is_deployed": True,
                    "health": 50000,
                    "max_health": 50000,
                }
            ],
            "inventory": [
                {
                    "grid_id": 0,
                    "item_id": 3001,
                    "name": "真·万寿无疆",
                    "count": 1,
                    "quality": "gold",
                    "type_desc": "命格",
                }
            ],
        }

        with patch("httpx.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = mock_telemetry_payload
            mock_get.return_value = mock_resp

            data = proxy.query_telemetry("主号")
            self.assertIsNotNone(data)
            self.assertEqual(data["nickname"], "神威剑仙")
            self.assertEqual(data["coins"], 182490120)

            # 验证请求携带了 Token 鉴权头
            mock_get.assert_called_once()
            args, kwargs = mock_get.call_args
            self.assertEqual(args[0], "http://127.0.0.1:8000/api/accounts/主号/telemetry")
            self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test_token")

    def test_daemon_proxy_query_assistant(self) -> None:
        """测试通过 DaemonProxy 代理查询小助手活跃度数据"""
        proxy = DaemonProxy(base_url="http://127.0.0.1:8000")
        mock_assistant_payload = {
            "alias": "主号",
            "current_liveness": 110,
            "max_liveness": 140,
            "items": [
                {
                    "item_id": 1,
                    "name": "仙府药园",
                    "completed_count": 1,
                    "total_quota": 1,
                    "is_completed": True,
                }
            ],
            "boxes": [
                {"box_id": 1, "required_liveness": 20, "status": 1, "status_desc": "已领取"}
            ],
        }

        with patch("httpx.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = mock_assistant_payload
            mock_get.return_value = mock_resp

            data = proxy.query_assistant("主号")
            self.assertIsNotNone(data)
            self.assertEqual(data["current_liveness"], 110)
            self.assertEqual(len(data["items"]), 1)

    def test_daemon_proxy_trigger_routine(self) -> None:
        """测试通过 DaemonProxy 远程调度触发账号日常流水线"""
        proxy = DaemonProxy(base_url="http://127.0.0.1:8000")
        with patch("httpx.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {
                "success": True,
                "status": "dispatched",
                "task_id": "routine_主号_1729080000",
                "alias": "主号",
            }
            mock_post.return_value = mock_resp

            res = proxy.trigger_routine("主号", force=False)
            self.assertTrue(res.get("success"))
            self.assertEqual(res.get("status"), "dispatched")

            mock_post.assert_called_once_with(
                "http://127.0.0.1:8000/api/accounts/主号/routine/trigger",
                json={"force": False},
                headers={},
                timeout=5.0,
            )

    def test_cli_query_formatter_rendering(self) -> None:
        """测试代理返回数据经过 DTO 转换后与 QueryFormatter 渲染一致性"""
        proxy = DaemonProxy()
        telemetry_raw = {
            "alias": "主号",
            "player_id": 1001,
            "nickname": "神威剑仙",
            "level": 128,
            "vip_level": 6,
            "coins": 182490120,
            "ingots": 36800,
            "power": 185,
            "max_power": 200,
            "fame": 824000,
            "town_id": 1,
            "town_name": "小渔村",
            "roles": [
                {
                    "role_id": 1,
                    "name": "神威剑仙",
                    "level": 128,
                    "is_deployed": True,
                    "health": 50000,
                    "max_health": 50000,
                    "role_job": "武圣",
                }
            ],
            "inventory": [
                {
                    "grid_id": 0,
                    "item_id": 3001,
                    "name": "真·万寿无疆",
                    "count": 1,
                    "quality": "gold",
                    "type_desc": "命格",
                }
            ],
        }

        # 1. 验证转换为 PlayerAssetDTO
        asset_dto = proxy.convert_to_asset_dto(telemetry_raw)
        self.assertEqual(asset_dto.coins, 182490120)
        self.assertEqual(asset_dto.nickname, "神威剑仙")

        # 2. 验证转换为 RoleDTO 列表
        roles_dto = proxy.convert_to_roles_dto(telemetry_raw)
        self.assertEqual(len(roles_dto), 1)
        self.assertEqual(roles_dto[0].name, "神威剑仙")

        # 3. 验证转换为 PackSummaryDTO
        pack_dto = proxy.convert_to_pack_dto(telemetry_raw)
        self.assertEqual(pack_dto.pack_used, 1)

    def test_cli_web_command_parsing(self) -> None:
        """测试 CLI 命令行解析 web 子命令并启动 Uvicorn"""
        from cli.__main__ import build_parser

        parser = build_parser()
        args = parser.parse_args(["web", "--host", "0.0.0.0", "--port", "8888"])
        self.assertEqual(args.command, "web")
        self.assertEqual(args.host, "0.0.0.0")
        self.assertEqual(args.port, 8888)

    def test_cli_fallback_to_sqlite_when_offline(self) -> None:
        """测试当 Daemon 离线时，CLI 可从本地 SQLite 数据库独立加载账号"""
        from cli.daemon_proxy import resolve_account_from_storage

        # 确保从指定的 sqlite 库中读取主号
        acc = resolve_account_from_storage(alias="主号", db_path=self.db_path)
        self.assertIsNotNone(acc)
        self.assertEqual(acc.alias, "主号")
        self.assertEqual(acc.username, "player_main")

    def test_main_py_web_subcommand_dispatch(self) -> None:
        """测试 main.py web 子命令能正确拦截并调度 run_web_server"""
        import sys
        from main import main as main_entry

        orig_argv = sys.argv
        sys.argv = ["main.py", "web", "--port", "9090"]
        try:
            with patch("cli.__main__.run_web_server") as mock_web_server:
                main_entry()
                mock_web_server.assert_called_once()
                args = mock_web_server.call_args[0][0]
                self.assertEqual(args.port, 9090)
        finally:
            sys.argv = orig_argv

    def test_main_py_proxy_mode_when_daemon_online(self) -> None:
        """测试 main.py 在守护进程在线时，-q 查询自动走 DaemonProxy 代理"""
        import sys
        from main import main as main_entry

        orig_argv = sys.argv
        sys.argv = ["main.py", "-q", "assets", "-a", "主号"]
        try:
            with patch("cli.daemon_proxy.DaemonProxy.is_alive", return_value=True):
                with patch("cli.__main__.handle_query_command") as mock_handle_query:
                    main_entry()
                    mock_handle_query.assert_called_once_with(
                        query_target="assets",
                        alias="主号",
                        as_json=False,
                        no_proxy=False,
                        config_path="config/config.json",
                    )
        finally:
            sys.argv = orig_argv


if __name__ == "__main__":
    unittest.main()
