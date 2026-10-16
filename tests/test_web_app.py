"""FastAPI Web 服务脚手架、Token 门禁与静态单页测试套件

测试用例覆盖:
1. 服务健康检查接口 /api/health
2. 静态单页挂载与 / 路由 HTML 响应
3. 免密模式下的鉴权验证 (/api/auth/verify)
4. Token 门禁配置生效 (通过 SXD_WEB_TOKEN 环境变量或 SQLite 配置仓储)
5. 错误 Token 拦截与 401 Unauthorized 防御
6. 正确 Bearer Token 验证与鉴权通过

@author Ateng
@since 2026-10-16
"""

import os
import shutil
import tempfile
import unittest
from starlette.testclient import TestClient

from storage.config_db import ConfigDatabase, AccountRecord
from web.app import create_app


class TestWebApp(unittest.TestCase):
    """FastAPI Web 接入层基础脚手架与鉴权门禁测试集"""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="sxd_test_web_")
        self.db_path = os.path.join(self.test_dir, "web_config.sqlite")
        self.db = ConfigDatabase(db_path=self.db_path, auto_bootstrap=False)
        self.db.add_account(
            AccountRecord(
                alias="主号",
                username="test_user",
                server="s813",
                enabled=True,
            )
        )
        # 清理可能干扰的环境变量
        os.environ.pop("SXD_WEB_TOKEN", None)

    def tearDown(self) -> None:
        os.environ.pop("SXD_WEB_TOKEN", None)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_health_check(self) -> None:
        """测试服务健康度探测接口"""
        app = create_app(db=self.db)
        client = TestClient(app)

        resp = client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get("status"), "ok")
        self.assertEqual(data.get("accounts_count"), 1)

    def test_static_index_serving(self) -> None:
        """测试内嵌单页静态资源在根路径 / 的托管"""
        app = create_app(db=self.db)
        client = TestClient(app)

        resp = client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/html", resp.headers.get("content-type", ""))
        self.assertIn("神仙道无头自动化控制台", resp.text)

    def test_auth_verify_when_no_token_required(self) -> None:
        """测试未配置 Token 时，免密模式的验证响应"""
        app = create_app(db=self.db)
        client = TestClient(app)

        resp = client.post("/api/auth/verify", json={"token": ""})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data.get("valid"))
        self.assertFalse(data.get("token_required"))

    def test_token_gate_from_env(self) -> None:
        """测试通过环境变量配置 SXD_WEB_TOKEN 的访问门禁拦截与验证"""
        os.environ["SXD_WEB_TOKEN"] = "admin_env_pass_123"
        app = create_app(db=self.db)
        client = TestClient(app)

        # 1. 错误口令 -> 401
        bad_resp = client.post("/api/auth/verify", json={"token": "wrong_password"})
        self.assertEqual(bad_resp.status_code, 401)

        # 2. 正确口令 -> 200
        ok_resp = client.post("/api/auth/verify", json={"token": "admin_env_pass_123"})
        self.assertEqual(ok_resp.status_code, 200)
        data = ok_resp.json()
        self.assertTrue(data.get("valid"))
        self.assertTrue(data.get("token_required"))

    def test_token_gate_from_sqlite_setting(self) -> None:
        """测试通过 SQLite 数据库 tb_system_settings 配置的 Token 门禁"""
        self.db.set_setting("web_token", "sqlite_secret_token_888")
        app = create_app(db=self.db)
        client = TestClient(app)

        # 1. 错误口令
        resp1 = client.post("/api/auth/verify", json={"token": "invalid"})
        self.assertEqual(resp1.status_code, 401)

        # 2. 正确口令
        resp2 = client.post("/api/auth/verify", json={"token": "sqlite_secret_token_888"})
        self.assertEqual(resp2.status_code, 200)
        self.assertTrue(resp2.json().get("valid"))

    def test_protected_route_dependency(self) -> None:
        """测试受保护路由使用 require_auth_token 依赖项的拦截行为"""
        from fastapi import Depends, APIRouter
        from web.app import require_auth_token

        os.environ["SXD_WEB_TOKEN"] = "guard_token_999"
        router = APIRouter()

        @router.get("/api/protected", dependencies=[Depends(require_auth_token)])
        async def protected_endpoint():
            return {"secret_data": "ok"}

        app = create_app(db=self.db, routers=[router])
        client = TestClient(app)


        # 1. 无凭证访问 -> 401
        res1 = client.get("/api/protected")
        self.assertEqual(res1.status_code, 401)

        # 2. 错误凭证 -> 401
        res2 = client.get("/api/protected", headers={"Authorization": "Bearer bad_token"})
        self.assertEqual(res2.status_code, 401)

        # 3. 正确 Bearer Header 访问 -> 200
        res3 = client.get("/api/protected", headers={"Authorization": "Bearer guard_token_999"})
        self.assertEqual(res3.status_code, 200)
        self.assertEqual(res3.json().get("secret_data"), "ok")

        # 4. 正确 query param 访问 -> 200
        res4 = client.get("/api/protected?token=guard_token_999")
        self.assertEqual(res4.status_code, 200)
        self.assertEqual(res4.json().get("secret_data"), "ok")


if __name__ == "__main__":
    unittest.main()

