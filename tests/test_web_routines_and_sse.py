"""35 项日常任务配置、流水线触发与 SSE 流式事件接口测试套件

测试覆盖:
1. GET /api/accounts/{alias}/routine-config 读取 35 项日常开关与元宝上限
2. PUT /api/accounts/{alias}/routine-config 保存日常开关定制
3. POST /api/accounts/{alias}/routine/trigger 异步分发日常流水线
4. 防互踢避让状态下触发日常的拦截与 force 强制穿透
5. GET /api/events SSE 流式连接建立与 connected 握手
6. GET /api/events?alias={alias} 单账号事件流过滤隔离
7. EventBusLogHandler 受管日志透明转译与 SSE 连通性
8. Token 门禁在日常配置与 SSE 路由上的安全校验

@author Ateng
@since 2026-10-16
"""

import json
import logging
import os
import shutil
import tempfile
import time
import unittest
from starlette.testclient import TestClient

from core.events import EventBus
from storage.config_db import ConfigDatabase, AccountRecord, ALL_ROUTINES
from web.app import create_app
from web.logging_bridge import EventBusLogHandler, attach_log_bridge, detach_log_bridge
from web.session_manager import AccountSessionManager


class TestWebRoutinesAndSSE(unittest.TestCase):
    """35 项日常配置、流水线触发与 SSE 测试集"""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="sxd_test_routines_")
        self.db_path = os.path.join(self.test_dir, "test_config.sqlite")
        self.db = ConfigDatabase(db_path=self.db_path, auto_bootstrap=False)
        self.event_bus = EventBus()
        self.session_manager = AccountSessionManager(db=self.db, event_bus=self.event_bus)

        # 预置两个账号
        self.acc1 = AccountRecord(
            alias="主号",
            platform="fengwanyx",
            username="player_main",
            password="pass_main",
            server="s813",
            enabled=True,
            hosting_enabled=True,
        )
        self.acc2 = AccountRecord(
            alias="打工小号",
            platform="static",
            username="player_alt",
            password="pass_alt",
            server="s814",
            enabled=True,
            hosting_enabled=True,
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

    def test_get_routine_config_defaults(self) -> None:
        """测试获取账号默认 35 项日常配置与零元宝上限"""
        resp = self.client.get("/api/accounts/主号/routine-config")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["alias"], "主号")
        self.assertEqual(data["allowed_ingots"], 0)
        self.assertEqual(len(data["enabled_routines"]), 35)
        self.assertEqual(len(data["all_routines"]), 35)
        self.assertIn("money_tree", data["enabled_routines"])
        self.assertIn("farm", data["enabled_routines"])

    def test_get_routine_config_not_found(self) -> None:
        """测试查询不存在账号的日常配置返回 404"""
        resp = self.client.get("/api/accounts/不存在账号/routine-config")
        self.assertEqual(resp.status_code, 404)

    def test_update_routine_config(self) -> None:
        """测试定制更新日常任务开关与元宝安全阈值"""
        payload = {
            "allowed_ingots": 100,
            "enabled_routines": ["signin", "money_tree", "farm"],
        }
        resp = self.client.put("/api/accounts/主号/routine-config", json=payload)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json().get("success"))
        self.assertEqual(resp.json().get("allowed_ingots"), 100)
        self.assertEqual(resp.json().get("enabled_count"), 3)

        # 数据库再读验证
        db_cfg = self.db.get_routine_config("主号")
        self.assertEqual(db_cfg.allowed_ingots, 100)
        self.assertEqual(db_cfg.enabled_routines, ["signin", "money_tree", "farm"])

        # GET 接口回读验证
        get_resp = self.client.get("/api/accounts/主号/routine-config")
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.json()["enabled_routines"], ["signin", "money_tree", "farm"])

    def test_update_routine_config_not_found(self) -> None:
        """测试更新不存在账号日常配置返回 404"""
        resp = self.client.put(
            "/api/accounts/不存在账号/routine-config",
            json={"allowed_ingots": 0, "enabled_routines": []},
        )
        self.assertEqual(resp.status_code, 404)

    def test_trigger_routine_pipeline(self) -> None:
        """测试手工异步触发单账号日常福利流水线"""
        resp = self.client.post("/api/accounts/主号/routine/trigger")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data.get("status"), "dispatched")
        self.assertEqual(data.get("alias"), "主号")
        self.assertTrue(data.get("task_id", "").startswith("routine_主号_"))

    def test_trigger_routine_evade_protection_and_force(self) -> None:
        """测试防互踢避让状态下的日常触发拦截与 force 强制穿透"""
        # 1. 模拟主号进入避让态
        self.session_manager.trigger_evade("主号", reason="player_online_test")

        # 2. 未携带 force 触发日常 -> 触发拦截保护
        resp_block = self.client.post("/api/accounts/主号/routine/trigger")
        self.assertEqual(resp_block.status_code, 200)
        block_data = resp_block.json()
        self.assertFalse(block_data.get("success"))
        self.assertEqual(block_data.get("status"), "evading_blocked")

        # 3. 携带 force=True 触发日常 -> 强制放行调度
        resp_force = self.client.post(
            "/api/accounts/主号/routine/trigger",
            json={"force": True},
        )
        self.assertEqual(resp_force.status_code, 200)
        force_data = resp_force.json()
        self.assertTrue(force_data.get("success"))
        self.assertEqual(force_data.get("status"), "dispatched")

    def test_trigger_routine_not_found(self) -> None:
        """测试触发不存在账号日常返回 404"""
        resp = self.client.post("/api/accounts/未知号/routine/trigger")
        self.assertEqual(resp.status_code, 404)

    def test_sse_stream_initial_connection(self) -> None:
        """测试 SSE 流连接建立并接收初始握手帧"""
        resp = self.client.get("/api/events?limit=1")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/event-stream", resp.headers.get("content-type", ""))
        self.assertIn("event: connected", resp.text)
        self.assertIn('"type": "connected"', resp.text)

    def test_sse_stream_alias_filtering(self) -> None:
        """测试 SSE 基于账号别名 ?alias={alias} 进行事件流精准过滤"""
        import threading
        def emit_events():
            # 等待 SSE 通道在 EventBus 上完成订阅注册
            for _ in range(100):
                if len(self.event_bus._global_app_listeners) > 0:
                    break
                time.sleep(0.01)
            time.sleep(0.02)
            # 1. 发布打工小号的事件 (应被过滤不推送)
            self.event_bus.publish(
                "routine_step",
                {"type": "routine_step", "alias": "打工小号", "message": "小号任务"},
            )
            # 2. 发布主号的事件 (应被正常接收)
            self.event_bus.publish(
                "routine_step",
                {"type": "routine_step", "alias": "主号", "message": "主号日常"},
            )

        t = threading.Thread(target=emit_events)
        t.start()

        resp = self.client.get("/api/events?alias=主号&limit=2&max_idle_sec=2.0")
        t.join()

        self.assertEqual(resp.status_code, 200)
        text = resp.text
        self.assertIn("event: connected", text)
        self.assertIn("主号日常", text)
        self.assertNotIn("小号任务", text)

    def test_logging_bridge_to_event_bus(self) -> None:
        """测试受管 Python 日志通过 EventBusLogHandler 转换为应用事件"""
        received = []
        self.event_bus.subscribe_event("log", lambda data: received.append(data))

        handler = attach_log_bridge(self.event_bus, logger_name="test_logger")
        try:
            test_log = logging.getLogger("test_logger")
            test_log.setLevel(logging.INFO)
            test_log.info("[主号] 招财神符收获 280,000 铜钱")

            self.assertGreaterEqual(len(received), 1)
            last_ev = received[-1]
            self.assertEqual(last_ev.get("alias"), "主号")
            self.assertEqual(last_ev.get("level"), "INFO")
            self.assertIn("招财神符收获", last_ev.get("message", ""))
        finally:
            detach_log_bridge(handler, logger_name="test_logger")

    def test_token_gate_on_routines_and_sse(self) -> None:
        """测试 Token 门禁在日常配置与 SSE 路由上的拦截"""
        os.environ["SXD_WEB_TOKEN"] = "token_vault_456"
        app = create_app(db=self.db, session_manager=self.session_manager)
        client = TestClient(app)

        # 1. routine-config 拦截
        r1 = client.get("/api/accounts/主号/routine-config")
        self.assertEqual(r1.status_code, 401)
        r2 = client.get(
            "/api/accounts/主号/routine-config",
            headers={"Authorization": "Bearer token_vault_456"},
        )
        self.assertEqual(r2.status_code, 200)

        # 2. SSE 拦截与 query token 放行
        r3 = client.get("/api/events?limit=1")
        self.assertEqual(r3.status_code, 401)

        r4 = client.get("/api/events?token=token_vault_456&limit=1")
        self.assertEqual(r4.status_code, 200)
        self.assertIn("event: connected", r4.text)


if __name__ == "__main__":
    unittest.main()
