"""全景态势只读遥测、背包快照与元宝安全审计 API 测试套件

测试覆盖:
1. GET /api/accounts/{alias}/telemetry 离线保底与持久化资产数据返回
2. 100 格背包物品快照及其金/紫/蓝/白品质标签只读序列化
3. GET /api/accounts/{alias}/assistant 小助手日常任务与活跃度宝箱数据
4. GET /api/accounts/{alias}/audit-logs 7日资产走势与零元宝风控审计记录
5. 针对不存在账号的 404 安全拦截
6. Token 门禁在遥测与审计路由上的鉴权防护

@author Ateng
@since 2026-10-16
"""

import json
import os
import shutil
import tempfile
import time
import unittest
from starlette.testclient import TestClient

from storage.config_db import ConfigDatabase, AccountRecord
from storage.player_db import (
    PlayerDatabase,
    PlayerProfileRecord,
    InventoryItemRecord,
    ModuleStateRecord,
    AuditLogRecord,
)
from web.app import create_app
from web.session_manager import AccountSessionManager


class TestWebTelemetryAndAudit(unittest.TestCase):
    """全景遥测、背包快照与审计 API 测试集"""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="sxd_test_telemetry_")
        self.config_db_path = os.path.join(self.test_dir, "config.sqlite")
        self.config_db = ConfigDatabase(db_path=self.config_db_path, auto_bootstrap=False)
        self.session_manager = AccountSessionManager(db=self.config_db)

        # 1. 预置两个账号
        self.acc1 = AccountRecord(
            alias="主号",
            platform="fengwanyx",
            username="player_main",
            password="pass_main",
            server="s813",
            server_id=813,
            enabled=True,
            hosting_enabled=True,
        )
        self.acc2 = AccountRecord(
            alias="小号",
            platform="static",
            username="player_alt",
            password="pass_alt",
            server="s814",
            server_id=814,
            enabled=True,
            hosting_enabled=False,
        )
        self.config_db.add_account(self.acc1)
        self.config_db.add_account(self.acc2)

        # 2. 为主号创建私有 PlayerDatabase 并预置测试数据
        self.player_db_path = os.path.join(self.test_dir, "storage_813_1001.db")
        self.player_db = PlayerDatabase(server_id=813, player_id=1001, db_path=self.player_db_path)
        self.session_manager.set_player_db("主号", self.player_db)

        # 预置角色档案
        self.profile = PlayerProfileRecord(
            player_id=1001,
            nickname="神威剑仙",
            level=128,
            coins=182490120,
            ingots=36800,
            power=185,
            fame=1250000,
            vip_level=5,
            town_id=1,
            updated_at=time.time(),
        )
        self.player_db.upsert_player_profile(self.profile)

        # 预置伙伴列表快照 (Mod 5)
        self.player_db.set_module_state(
            ModuleStateRecord(
                module_id=5,
                state_key="role_list",
                payload={
                    "roles": [
                        {
                            "role_id": 1,
                            "name": "神威剑仙",
                            "level": 128,
                            "is_deployed": True,
                            "health": 50000,
                            "max_health": 50000,
                            "role_job": "武圣",
                            "realm_level": 5,
                        },
                        {
                            "role_id": 2,
                            "name": "将臣",
                            "level": 125,
                            "is_deployed": True,
                            "health": 48000,
                            "max_health": 48000,
                            "role_job": "将星",
                            "realm_level": 4,
                        },
                    ]
                },
            )
        )

        # 预置背包道具 (含金/紫/蓝/白品质)
        items = [
            InventoryItemRecord(grid_id=1, item_id=3001, count=10, item_type=2, props={"name": "节日自选礼包盒", "quality": "gold"}),
            InventoryItemRecord(grid_id=2, item_id=2003, count=5, item_type=2, props={"name": "高级经验丹", "quality": "purple"}),
            InventoryItemRecord(grid_id=3, item_id=1002, count=20, item_type=2, props={"name": "中级体力丹", "quality": "blue"}),
            InventoryItemRecord(grid_id=4, item_id=501, count=99, item_type=3, props={"name": "象牙", "quality": "white"}),
        ]
        self.player_db.upsert_inventory_items(items)

        # 预置小助手日常进度快照 (Mod 52)
        self.player_db.set_module_state(
            ModuleStateRecord(
                module_id=52,
                state_key="assistant_info",
                payload={
                    "current_liveness": 75,
                    "max_liveness": 100,
                    "items": [
                        {"item_id": 1, "name": "招财神符", "completed_count": 1, "total_quota": 1, "is_completed": True},
                        {"item_id": 2, "name": "帮派祭神", "completed_count": 1, "total_quota": 1, "is_completed": True},
                        {"item_id": 8, "name": "竞技场", "completed_count": 5, "total_quota": 10, "is_completed": False},
                    ],
                    "boxes": [
                        {"box_id": 1, "required_liveness": 20, "status": 4, "status_desc": "已领取"},
                        {"box_id": 2, "required_liveness": 40, "status": 4, "status_desc": "已领取"},
                        {"box_id": 3, "required_liveness": 60, "status": 4, "status_desc": "已领取"},
                        {"box_id": 4, "required_liveness": 80, "status": 2, "status_desc": "未达标"},
                        {"box_id": 5, "required_liveness": 100, "status": 2, "status_desc": "未达标"},
                    ],
                },
            )
        )

        # 预置高危元宝操作审计记录
        self.player_db.add_audit_log(
            AuditLogRecord(
                module_id=28,
                action_id=4,
                action_name="buy_challenge_times",
                allow_ingot=False,
                details={"reason": "零元宝安全红线熔断拦截"},
            )
        )
        self.player_db.add_audit_log(
            AuditLogRecord(
                module_id=24,
                action_id=5,
                action_name="world_boss_ingot_inspire",
                allow_ingot=False,
                details={"reason": "只读模式跳过"},
            )
        )

        os.environ.pop("SXD_WEB_TOKEN", None)
        self.app = create_app(db=self.config_db, session_manager=self.session_manager)
        self.client = TestClient(self.app)

    def tearDown(self) -> None:
        os.environ.pop("SXD_WEB_TOKEN", None)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_get_telemetry_with_persisted_data(self) -> None:
        """测试获取主号全景遥测：角色资产、参战伙伴与只读背包网格"""
        resp = self.client.get("/api/accounts/主号/telemetry")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        # 验证核心角色画像
        self.assertEqual(data["alias"], "主号")
        self.assertEqual(data["nickname"], "神威剑仙")
        self.assertEqual(data["level"], 128)
        self.assertEqual(data["vip_level"], 5)
        self.assertEqual(data["coins"], 182490120)
        self.assertEqual(data["ingots"], 36800)
        self.assertEqual(data["power"], 185)
        self.assertEqual(data["fame"], 1250000)

        # 验证参战伙伴
        roles = data["roles"]
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0]["name"], "神威剑仙")
        self.assertEqual(roles[1]["name"], "将臣")

        # 验证只读背包物品与品质标识
        inv = data["inventory"]
        self.assertEqual(len(inv), 4)
        gold_item = next(i for i in inv if i["item_id"] == 3001)
        self.assertEqual(gold_item["quality"], "gold")
        self.assertEqual(gold_item["count"], 10)

        purple_item = next(i for i in inv if i["item_id"] == 2003)
        self.assertEqual(purple_item["quality"], "purple")

        blue_item = next(i for i in inv if i["item_id"] == 1002)
        self.assertEqual(blue_item["quality"], "blue")

        white_item = next(i for i in inv if i["item_id"] == 501)
        self.assertEqual(white_item["quality"], "white")

    def test_get_telemetry_offline_defaults(self) -> None:
        """测试对于尚无本地私有库的小号，返回平滑优雅的默认保底遥测"""
        resp = self.client.get("/api/accounts/小号/telemetry")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["alias"], "小号")
        self.assertGreaterEqual(data["level"], 1)
        self.assertIsInstance(data["roles"], list)
        self.assertIsInstance(data["inventory"], list)

    def test_get_telemetry_not_found(self) -> None:
        """测试获取不存在账号的遥测返回 404"""
        resp = self.client.get("/api/accounts/不存在账号/telemetry")
        self.assertEqual(resp.status_code, 404)

    def test_get_assistant_with_data(self) -> None:
        """测试获取小助手日常进度与活跃度宝箱"""
        resp = self.client.get("/api/accounts/主号/assistant")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["alias"], "主号")
        self.assertEqual(data["current_liveness"], 75)
        self.assertEqual(data["max_liveness"], 100)
        self.assertEqual(len(data["items"]), 3)
        self.assertEqual(len(data["boxes"]), 5)

        box1 = next(b for b in data["boxes"] if b["box_id"] == 1)
        self.assertEqual(box1["status_desc"], "已领取")

    def test_get_assistant_offline_defaults(self) -> None:
        """测试对于尚无小助手快照的账号返回全量日常清单默认结构"""
        resp = self.client.get("/api/accounts/小号/assistant")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["alias"], "小号")
        self.assertEqual(data["current_liveness"], 0)
        self.assertGreaterEqual(len(data["items"]), 5)
        self.assertEqual(len(data["boxes"]), 5)

    def test_get_audit_logs(self) -> None:
        """测试获取 7 日资产走势与零元宝风控审计记录"""
        resp = self.client.get("/api/accounts/主号/audit-logs")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["alias"], "主号")

        # 验证 7 日资产走势
        history = data["asset_history"]
        self.assertEqual(len(history), 7)
        self.assertIn("date", history[0])
        self.assertIn("coins", history[0])
        self.assertIn("ingots", history[0])

        # 验证高危元宝操作审计记录
        audits = data["audit_records"]
        self.assertGreaterEqual(len(audits), 2)
        first_audit = audits[0]
        self.assertIn("action_name", first_audit)
        self.assertFalse(first_audit["allow_ingot"])

    def test_token_gate_on_telemetry(self) -> None:
        """测试 Token 门禁在只读遥测路由上的安全防护"""
        os.environ["SXD_WEB_TOKEN"] = "telemetry_guard_token"
        app = create_app(db=self.config_db, session_manager=self.session_manager)
        client = TestClient(app)

        # 1. 未授权请求 -> 401
        self.assertEqual(client.get("/api/accounts/主号/telemetry").status_code, 401)
        self.assertEqual(client.get("/api/accounts/主号/assistant").status_code, 401)
        self.assertEqual(client.get("/api/accounts/主号/audit-logs").status_code, 401)

        # 2. 携带有效 Token -> 200
        headers = {"Authorization": "Bearer telemetry_guard_token"}
        self.assertEqual(client.get("/api/accounts/主号/telemetry", headers=headers).status_code, 200)
        self.assertEqual(client.get("/api/accounts/主号/assistant", headers=headers).status_code, 200)
        self.assertEqual(client.get("/api/accounts/主号/audit-logs", headers=headers).status_code, 200)


if __name__ == "__main__":
    unittest.main()
