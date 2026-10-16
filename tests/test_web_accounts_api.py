"""多账号管理、长连接托管与防互踢避让接口测试套件

测试用例覆盖:
1. GET /api/accounts 账号列表与实时连接/避让状态读取
2. POST /api/accounts 账号创建与非法重复别名拦截
3. PUT /api/accounts/{alias} 账号凭据与区服信息更新
4. DELETE /api/accounts/{alias} 账号级联删除
5. POST /api/accounts/{alias}/hosting/toggle 长连接托管启停
6. 防互踢避让状态流转 (触发避让 -> 暂停重连 -> 标黄避让中 -> 恢复托管)
7. 静默探测恢复 (Silent Probe Recovery) 定时探活测试
8. Token 门禁在账号管理路由上的安全性拦截

@author Ateng
@since 2026-10-16
"""

import asyncio
import os
import shutil
import tempfile
import time
import unittest
from starlette.testclient import TestClient

from storage.config_db import ConfigDatabase, AccountRecord
from web.app import create_app
from web.session_manager import AccountSessionManager


class TestWebAccountsApi(unittest.TestCase):
    """多账号管理与防互踢避让 API 测试集"""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="sxd_test_accounts_")
        self.db_path = os.path.join(self.test_dir, "test_config.sqlite")
        self.db = ConfigDatabase(db_path=self.db_path, auto_bootstrap=False)
        self.session_manager = AccountSessionManager(db=self.db)

        # 预置两个账号
        self.acc1 = AccountRecord(
            alias="主号",
            platform="fengwanyx",
            username="player_main",
            password="secret_pass_1",
            server="s138",
            server_id=25268,
            enabled=True,
            hosting_enabled=True,
        )
        self.acc2 = AccountRecord(
            alias="打工小号",
            platform="static",
            username="player_alt",
            password="secret_pass_2",
            server="s140",
            server_id=25270,
            enabled=True,
            hosting_enabled=False,
        )
        self.db.add_account(self.acc1)
        self.db.add_account(self.acc2)

        os.environ.pop("SXD_WEB_TOKEN", None)
        self.app = create_app(db=self.db, session_manager=self.session_manager)
        self.client = TestClient(self.app)

    def tearDown(self) -> None:
        os.environ.pop("SXD_WEB_TOKEN", None)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_list_accounts(self) -> None:
        """测试获取全部账号列表与复合运行态"""
        resp = self.client.get("/api/accounts")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 2)
        
        main_item = next(item for item in data if item["alias"] == "主号")
        self.assertEqual(main_item["platform"], "fengwanyx")
        self.assertEqual(main_item["server"], "s138")
        self.assertTrue(main_item["hosting_enabled"])
        self.assertEqual(main_item["evade_state"], "none")

    def test_create_account(self) -> None:
        """测试创建新账号及重复别名拦截"""
        # 1. 成功创建
        payload = {
            "alias": "新挖矿号",
            "platform": "fengwanyx",
            "username": "miner_user",
            "password": "miner_pwd",
            "server": "s142",
            "enabled": True,
            "hosting_enabled": True,
        }
        resp = self.client.post("/api/accounts", json=payload)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json().get("success"))

        created = self.db.get_account("新挖矿号")
        self.assertIsNotNone(created)
        self.assertEqual(created.username, "miner_user")

        # 2. 重复别名创建 -> 400 Bad Request
        resp_dup = self.client.post("/api/accounts", json=payload)
        self.assertEqual(resp_dup.status_code, 400)

    def test_update_account(self) -> None:
        """测试更新现有账号"""
        update_payload = {
            "platform": "static",
            "username": "updated_user",
            "password": "updated_password",
            "server": "s139",
            "enabled": True,
            "hosting_enabled": True,
        }
        resp = self.client.put("/api/accounts/主号", json=update_payload)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json().get("success"))

        updated = self.db.get_account("主号")
        self.assertEqual(updated.username, "updated_user")
        self.assertEqual(updated.server, "s139")

    def test_delete_account(self) -> None:
        """测试删除账号"""
        resp = self.client.delete("/api/accounts/打工小号")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json().get("success"))
        self.assertIsNone(self.db.get_account("打工小号"))

    def test_toggle_hosting(self) -> None:
        """测试长连接托管开关接口"""
        # 关闭主号托管
        resp = self.client.post("/api/accounts/主号/hosting/toggle", json={"hosting_enabled": False})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.json().get("hosting_enabled"))
        self.assertFalse(self.db.get_account("主号").hosting_enabled)

        # 重新开启主号托管
        resp2 = self.client.post("/api/accounts/主号/hosting/toggle", json={"hosting_enabled": True})
        self.assertEqual(resp2.status_code, 200)
        self.assertTrue(resp2.json().get("hosting_enabled"))
        self.assertTrue(self.db.get_account("主号").hosting_enabled)

    def test_mutual_evade_and_resume_flow(self) -> None:
        """测试防互踢避让触发与一键手动恢复全流程"""
        # 1. 模拟收到异地登录通知包，触发防互踢避让
        self.session_manager.trigger_evade("主号", reason="Mod 100 Act 22 another_login_notify")
        
        # 验证数据库状态更新为 evading
        acc = self.db.get_account("主号")
        self.assertEqual(acc.evade_state, "evading")
        self.assertGreater(acc.evade_since, 0.0)

        # 验证 API 查询呈现避让中
        resp = self.client.get("/api/accounts")
        main_item = next(item for item in resp.json() if item["alias"] == "主号")
        self.assertEqual(main_item["evade_state"], "evading")

        # 2. 点击【打完了·恢复托管】接口
        resume_resp = self.client.post("/api/accounts/主号/hosting/resume")
        self.assertEqual(resume_resp.status_code, 200)
        self.assertTrue(resume_resp.json().get("success"))

        # 验证状态重置为 none
        acc_resumed = self.db.get_account("主号")
        self.assertEqual(acc_resumed.evade_state, "none")
        self.assertEqual(acc_resumed.evade_since, 0.0)

    def test_silent_probe_recovery(self) -> None:
        """测试静默探测恢复自愈逻辑"""
        # 设置一个微型探测延迟 (0.05 秒)
        self.session_manager.trigger_evade("主号", reason="test_evade", probe_delay_sec=0.05)
        self.assertEqual(self.db.get_account("主号").evade_state, "evading")

        # 等待静默探测触发并自愈
        time.sleep(0.1)
        self.session_manager.check_silent_probes()
        
        # 避让状态已自动恢复
        acc = self.db.get_account("主号")
        self.assertEqual(acc.evade_state, "none")

    def test_token_gate_on_accounts_api(self) -> None:
        """测试账号管理接口在 Token 门禁下的安全防御"""
        os.environ["SXD_WEB_TOKEN"] = "secure_token_123"
        app = create_app(db=self.db, session_manager=self.session_manager)
        client = TestClient(app)

        # 1. 无凭据请求 -> 401
        res1 = client.get("/api/accounts")
        self.assertEqual(res1.status_code, 401)

        # 2. 正确 Bearer Token -> 200
        res2 = client.get("/api/accounts", headers={"Authorization": "Bearer secure_token_123"})
        self.assertEqual(res2.status_code, 200)

    def test_account_test_login_endpoint(self) -> None:
        """测试 POST /api/accounts/test-login 探测端点"""
        from unittest.mock import patch
        from network.web_auth import GatewayCredentials

        # 1. 成功模拟
        mock_creds = GatewayCredentials(
            server_host="9x604.sxdweb.xd.com",
            server_port=8475,
            player_name="357260427",
            hash_code="mock_token_hash_123",
            time="1792151706",
            platform="xd",
            server_id=3542,
            nickname="剑仙",
        )
        with patch("network.web_auth.WebAuthFetcher.resolve_credentials", return_value=mock_creds):
            res = self.client.post(
                "/api/accounts/test-login",
                json={
                    "platform": "xd",
                    "username": "test_user",
                    "password": "test_password",
                    "server": "S3542",
                },
            )
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertTrue(data["success"])
            self.assertEqual(data["server_host"], "9x604.sxdweb.xd.com")
            self.assertEqual(data["player_name"], "357260427")

        # 2. 失败模拟
        with patch("network.web_auth.WebAuthFetcher.resolve_credentials", return_value=None):
            res_fail = self.client.post(
                "/api/accounts/test-login",
                json={
                    "platform": "xd",
                    "username": "bad_user",
                    "password": "wrong_password",
                    "server": "S3542",
                },
            )
            self.assertEqual(res_fail.status_code, 200)
            data_fail = res_fail.json()
            self.assertFalse(data_fail["success"])

    def test_evade_all_and_resume_all_endpoints(self) -> None:
        """测试 POST /api/accounts/evade/all 与 POST /api/accounts/resume/all 批量避让恢复"""
        # 1. 批量触发避让
        resp_evade = self.client.post("/api/accounts/evade/all")
        self.assertEqual(resp_evade.status_code, 200)
        evade_data = resp_evade.json()
        self.assertTrue(evade_data["success"])
        self.assertGreaterEqual(evade_data["evaded_count"], 1)

        # 2. 查询列表验证避让状态与倒计时字段
        resp_list = self.client.get("/api/accounts")
        self.assertEqual(resp_list.status_code, 200)
        items = resp_list.json()
        main_acc = next(acc for acc in items if acc["alias"] == "主号")
        self.assertEqual(main_acc["evade_state"], "evading")
        self.assertFalse(main_acc["hosting_enabled"])
        self.assertEqual(main_acc["evade_reason"], "用户手动全员避让")
        self.assertIsNotNone(main_acc["evade_probe_at"])

        # 3. 批量恢复托管
        resp_resume = self.client.post("/api/accounts/resume/all")
        self.assertEqual(resp_resume.status_code, 200)
        resume_data = resp_resume.json()
        self.assertTrue(resume_data["success"])
        self.assertGreaterEqual(resume_data["resumed_count"], 1)

        # 4. 再次验证状态已清除并恢复长连接托管开启
        resp_list2 = self.client.get("/api/accounts")
        items2 = resp_list2.json()
        main_acc2 = next(acc for acc in items2 if acc["alias"] == "主号")
        self.assertEqual(main_acc2["evade_state"], "none")
        self.assertTrue(main_acc2["hosting_enabled"])

    def test_single_account_evade_endpoint(self) -> None:
        """测试 POST /api/accounts/{alias}/hosting/evade 单账号主动避让"""
        resp = self.client.post("/api/accounts/主号/hosting/evade")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])

        info = self.session_manager.get_session_info("主号")
        self.assertEqual(info["evade_state"], "evading")
        self.assertEqual(info["evade_reason"], "用户手动避让")
        self.assertIsNotNone(info["evade_probe_at"])

    def test_single_account_inventory_clean_endpoint(self) -> None:
        """测试 POST /api/accounts/{alias}/inventory/clean 一键清理背包端点"""
        from unittest.mock import patch, AsyncMock

        mock_clean_res = {
            "success": True,
            "message": "背包四阶自理完成: 剩余 12 格 (使用 2 件, 存仓 3 件, 变卖 1 件)",
            "result": {"empty_grids": 12},
        }

        with patch.object(self.session_manager, "clean_inventory", new_callable=AsyncMock) as mock_clean:
            mock_clean.return_value = mock_clean_res

            resp = self.client.post(
                "/api/accounts/主号/inventory/clean",
                json={"target_empty": 5, "force_all": True},
            )
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertTrue(data["success"])
            self.assertIn("背包四阶自理完成", data["message"])
            mock_clean.assert_called_once_with(alias="主号", target_empty=5, force_all=True)

    def test_single_account_inventory_use_all_endpoint(self) -> None:
        """测试 POST /api/accounts/{alias}/inventory/use-all 一键使用背包物品端点"""
        from unittest.mock import patch, AsyncMock

        mock_use_res = {
            "success": True,
            "message": "一键使用消耗品与宝箱完毕: 剩余 8 格 (开箱/吃丹 5 件)",
            "data": {"empty_grids": 8, "items_used": 5},
        }

        with patch.object(self.session_manager, "use_all_inventory", new_callable=AsyncMock) as mock_use:
            mock_use.return_value = mock_use_res

            resp = self.client.post("/api/accounts/主号/inventory/use-all")
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertTrue(data["success"])
            self.assertIn("一键使用消耗品与宝箱完毕", data["message"])
            mock_use.assert_called_once_with(alias="主号")



if __name__ == "__main__":
    unittest.main()

