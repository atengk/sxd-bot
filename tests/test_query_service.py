"""神仙道数据查询服务与态势感知看板单元测试套件

测试驱动开发 (TDD) 验证：
1. PlayerAssetDTO 领域模型与序列化
2. QueryService.query_player_assets 只读协议反序列化与上下文同步
3. 即查即存机制与 SQLite 角色画像持久化
4. QueryFormatter 控制台表格看板渲染与 JSON 格式化导出
5. 零元宝安全不变量与只读边界验证

@author Ateng
@since 2026-10-16
"""

import json
import os
import shutil
import tempfile
import unittest
from unittest.mock import AsyncMock, MagicMock

from core.context import GameContext
from network.client import SXDClient
from protocol.packet import ByteArrayWriter
from storage.player_db import PlayerDatabase

from services.query_models import (
    PlayerAssetDTO,
    RoleDTO,
    AssistantDailyDTO,
    AssistantDailyItemDTO,
    AssistantLivenessBoxDTO,
    InventoryItemDTO,
    PackSummaryDTO,
    FullTelemetryDTO,
)

from services.query_service import QueryService
from services.query_formatter import QueryFormatter
from protocol.messages.role import RoleGetRoleListReq, RoleGetRoleListResp
from protocol.messages.assistant import AssistantInfoReq, AssistantInfoResp
from protocol.messages.item import ItemGetPlayerPackItemListReq, ItemGetPlayerPackItemListResp



class TestQueryService(unittest.IsolatedAsyncioTestCase):
    """数据查询服务与态势看板单元测试

    @author Ateng
    @since 2026-10-16
    """

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.ctx = GameContext()
        self.ctx.set_connected(True)
        self.ctx.update_login_success(player_id=8888)
        self.ctx.update_player_info(
            nickname="剑仙李逍遥",
            player_id=8888,
            level=120,
            coins=50000000,
            ingots=9999,
            power=180,
            fame=125000,
            vip_level=6,
            town_id=29,
            mission_key=854,
        )

        self.client = MagicMock(spec=SXDClient)
        self.client.context = self.ctx
        self.player_db = PlayerDatabase(server_id=1, player_id=8888, base_dir=self.temp_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _build_mock_player_info_payload(self) -> bytes:
        """构造 Mod 0 Act 2 官方 44 字段二进制响应测试桩"""
        writer = ByteArrayWriter()
        writer.write_utf("剑仙李逍遥")        # Field 0: nickname
        writer.write_int32(120)               # Field 1: level
        writer.write_int32(9999)              # Field 2: ingots
        writer.write_int64(50000000)          # Field 3: coins
        writer.write_int64(1000000)           # Field 4: health
        writer.write_int64(1000000)           # Field 5: max_health
        writer.write_int32(180)               # Field 6: power
        writer.write_int64(1234567)           # Field 7: exp
        writer.write_int64(2000000)           # Field 8: max_exp
        writer.write_int32(29)                # Field 9: town_map_id
        for _ in range(4):                    # Field 10-13
            writer.write_int32(0)
        writer.write_int32(6)                 # Field 14: vip_level
        for _ in range(4):                    # Field 15-18
            writer.write_int32(0)
        writer.write_int8(1)                  # Field 19: camp_id
        writer.write_int32(0)                 # Field 20: townKey
        writer.write_int32(125000)            # Field 21: fame
        for _ in range(7):                    # Field 22-28
            writer.write_int32(0)
        writer.write_int32(854)               # Field 29: mission_key
        return writer.to_bytes()

    # ==================== 1. PlayerAssetDTO 模型测试 ====================

    def test_player_asset_dto_to_dict(self) -> None:
        """验证 PlayerAssetDTO 序列化正确性"""
        dto = PlayerAssetDTO(
            player_id=123,
            nickname="太白金星",
            level=300,
            coins=100000000,
            ingots=888,
            power=200,
            fame=300000,
            vip_level=12,
            town_id=29,
            town_name="大理城",
            mission_key=900,
        )
        data = dto.to_dict()
        self.assertEqual(data["player_id"], 123)
        self.assertEqual(data["nickname"], "太白金星")
        self.assertEqual(data["level"], 300)
        self.assertEqual(data["coins"], 100000000)
        self.assertEqual(data["ingots"], 888)
        self.assertEqual(data["power"], 200)
        self.assertEqual(data["fame"], 300000)
        self.assertEqual(data["town_name"], "大理城")

    # ==================== 2. QueryService 基础资产查询与解包 ====================

    async def test_query_player_assets_with_live_response(self) -> None:
        """验证 QueryService 发送只读请求并正确解析组装 DTO"""
        mock_payload = self._build_mock_player_info_payload()
        self.client.request = AsyncMock(return_value=mock_payload)

        service = QueryService(self.client, self.ctx, self.player_db)
        dto = await service.query_player_assets()

        self.assertEqual(dto.player_id, 8888)
        self.assertEqual(dto.nickname, "剑仙李逍遥")
        self.assertEqual(dto.level, 120)
        self.assertEqual(dto.coins, 50000000)
        self.assertEqual(dto.ingots, 9999)
        self.assertEqual(dto.power, 180)
        self.assertEqual(dto.fame, 125000)
        self.assertEqual(dto.vip_level, 6)
        self.assertEqual(dto.town_id, 29)
        self.assertEqual(dto.mission_key, 854)

        # 断言 client.request 发送的是 Mod 0 Act 2 只读包
        self.client.request.assert_called_once()
        req_pkt = self.client.request.call_args[0][0]
        self.assertEqual(req_pkt.mod, 0)
        self.assertEqual(req_pkt.act, 2)

    # ==================== 3. 即查即存机制与 SQLite 缓存落盘 ====================

    async def test_query_player_assets_sqlite_persistence(self) -> None:
        """验证查询动作自动将数据同步至本地 SQLite 数据库"""
        mock_payload = self._build_mock_player_info_payload()
        self.client.request = AsyncMock(return_value=mock_payload)

        service = QueryService(self.client, self.ctx, self.player_db)
        await service.query_player_assets()

        # 从数据库中读取校验
        profile = self.player_db.get_player_profile()
        self.assertIsNotNone(profile)
        self.assertEqual(profile.player_id, 8888)
        self.assertEqual(profile.nickname, "剑仙李逍遥")
        self.assertEqual(profile.level, 120)
        self.assertEqual(profile.coins, 50000000)
        self.assertEqual(profile.ingots, 9999)
        self.assertEqual(profile.power, 180)

    # ==================== 4. 看板格式化渲染引擎测试 ====================

    def test_query_formatter_table_and_json(self) -> None:
        """验证 QueryFormatter 输出美化看板与 JSON 契约"""
        dto = PlayerAssetDTO(
            player_id=8888,
            nickname="剑仙李逍遥",
            level=120,
            coins=50000000,
            ingots=9999,
            power=180,
            fame=125000,
            vip_level=6,
            town_id=29,
            town_name="大理城",
            mission_key=854,
        )

        # 1. 验证控制台表格
        table_output = QueryFormatter.format_assets_table(dto)
        self.assertIn("神仙道角色全景资产看板", table_output)
        self.assertIn("剑仙李逍遥", table_output)
        self.assertIn("50,000,000", table_output)
        self.assertIn("9,999", table_output)
        self.assertIn("180 / 200", table_output)

        # 2. 验证 JSON 导出
        json_output = QueryFormatter.format_assets_json(dto)
        parsed = json.loads(json_output)
        self.assertEqual(parsed["status"], "success")
        self.assertEqual(parsed["type"], "assets")
        self.assertEqual(parsed["data"]["coins"], 50000000)
        self.assertEqual(parsed["data"]["ingots"], 9999)

    # ==================== 5. 零元宝安全不变量与超时容错 ====================

    async def test_query_timeout_fallback_to_context(self) -> None:
        """验证当服务端网络超时时，优雅退避至现有上下文而不崩溃"""
        self.client.request = AsyncMock(side_effect=TimeoutError("网络超时"))

        service = QueryService(self.client, self.ctx, self.player_db)
        # 应正常返回上下文中的保底数据，绝不抛出未处理异常
        dto = await service.query_player_assets()
        self.assertEqual(dto.player_id, 8888)
        self.assertEqual(dto.nickname, "剑仙李逍遥")
        self.assertEqual(dto.coins, 50000000)

    # ==================== 6. CLI run_query_mode 端到端生命周期 ====================

    async def test_run_query_mode_assets_table_and_json(self) -> None:
        """验证 main.py run_query_mode 完整执行生命周期与格式化输出"""
        from io import StringIO
        import sys
        from unittest.mock import patch
        from main import run_query_mode

        config = {
            "auth_mode": "static",
            "server": {"host": "127.0.0.1", "port": 8000},
            "credentials": {
                "player_name": "test_user",
                "hash_code": "abc",
                "time": "123",
                "platform": "test",
                "server_id": 1,
            },
        }

        # 模拟标准输出捕获
        captured_out = StringIO()
        with patch.object(SXDClient, "connect", new=AsyncMock(return_value=True)), \
             patch.object(SXDClient, "disconnect", new=AsyncMock(return_value=None)), \
             patch("main.LoginTask.execute", new=AsyncMock(return_value=MagicMock(is_success=True))), \
             patch.object(QueryService, "query_player_assets", new=AsyncMock(return_value=PlayerAssetDTO(
                 player_id=8888,
                 nickname="李逍遥",
                 level=100,
                 coins=123456,
                 ingots=888,
                 power=150,
             ))), \
             patch.object(sys, "stdout", captured_out):
            # 1. 测试表格看板
            await run_query_mode(config, query_target="assets", as_json=False)
            table_val = captured_out.getvalue()
            self.assertIn("神仙道角色全景资产看板", table_val)
            self.assertIn("李逍遥", table_val)

        # ==================== 7. 伙伴系统 (Role: Mod 5) 编解码与查询测试 ====================

    def _build_mock_role_list_payload(self) -> bytes:
        """构造 Mod 5 Act 2 get_role_list 二进制应答桩"""
        writer = ByteArrayWriter()
        # 15 个头部字段
        for _ in range(7):
            writer.write_int32(0)
        writer.write_utf("")  # string 1
        writer.write_utf("")  # string 2
        writer.write_int32(0) # int 1
        writer.write_int8(0)  # byte 1
        writer.write_int8(0)  # byte 2
        writer.write_int8(0)  # byte 3
        writer.write_int16(0) # short 1
        writer.write_int16(0) # short 2

        # 角色数组：长度 2
        writer.write_uint16(2)

        # 角色 1: 主角
        writer.write_utf("剑仙李逍遥")        # 0: name
        writer.write_int32(1)                 # 1: role_id
        writer.write_int32(101)               # 2: player_role_id
        writer.write_int64(1000)              # 3: exp
        writer.write_int64(2000)              # 4: max_exp
        writer.write_int16(120)               # 5: level
        writer.write_int8(0)                  # 6: deploy_state (0=DEPLOY)
        writer.write_int16(1)                 # 7: order
        writer.write_int64(800000)            # 8: health
        writer.write_int64(800000)            # 9: max_health

        # 角色 2: 伙伴小仙女
        writer.write_utf("小仙女")            # 0: name
        writer.write_int32(2)                 # 1: role_id
        writer.write_int32(102)               # 2: player_role_id
        writer.write_int64(500)               # 3: exp
        writer.write_int64(1000)              # 4: max_exp
        writer.write_int16(110)               # 5: level
        writer.write_int8(0)                  # 6: deploy_state (0=DEPLOY)
        writer.write_int16(2)                 # 7: order
        writer.write_int64(500000)            # 8: health
        writer.write_int64(500000)            # 9: max_health

        return writer.to_bytes()

    def test_role_dto_to_dict(self) -> None:
        """验证 RoleDTO 字典序列化"""
        role = RoleDTO(
            role_id=1,
            player_role_id=101,
            name="剑仙李逍遥",
            level=120,
            is_deployed=True,
            health=800000,
            max_health=800000,
            role_job="武圣",
            realm_level=5,
        )
        d = role.to_dict()
        self.assertEqual(d["name"], "剑仙李逍遥")
        self.assertEqual(d["level"], 120)
        self.assertTrue(d["is_deployed"])
        self.assertEqual(d["health"], 800000)

    async def test_query_roles_service(self) -> None:
        """验证 QueryService.query_roles 只读发包与 DTO 映射"""
        mock_payload = self._build_mock_role_list_payload()
        self.client.request = AsyncMock(return_value=mock_payload)

        service = QueryService(self.client, self.ctx, self.player_db)
        roles = await service.query_roles()

        self.assertEqual(len(roles), 2)
        r1, r2 = roles[0], roles[1]
        self.assertEqual(r1.name, "剑仙李逍遥")
        self.assertEqual(r1.level, 120)
        self.assertTrue(r1.is_deployed)
        self.assertEqual(r2.name, "小仙女")
        self.assertEqual(r2.level, 110)

        # 验证发包目标为 Mod 5 Act 2
        req = self.client.request.call_args[0][0]
        self.assertEqual(req.mod, 5)
        self.assertEqual(req.act, 2)

    def test_query_formatter_roles_table_and_json(self) -> None:
        """验证 QueryFormatter 输出伙伴阵容看板与 JSON"""
        roles = [
            RoleDTO(role_id=1, player_role_id=101, name="剑仙李逍遥", level=120, is_deployed=True, health=800000, max_health=800000),
            RoleDTO(role_id=2, player_role_id=102, name="小仙女", level=110, is_deployed=True, health=500000, max_health=500000),
        ]
        table = QueryFormatter.format_roles_table(roles)
        self.assertIn("参战伙伴阵容看板", table)
        self.assertIn("剑仙李逍遥", table)
        self.assertIn("小仙女", table)
        self.assertIn("主力出战", table)

        json_str = QueryFormatter.format_roles_json(roles)
        data = json.loads(json_str)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["type"], "roles")
        self.assertEqual(len(data["data"]), 2)

    async def test_run_query_mode_roles(self) -> None:
        """验证 main.py run_query_mode query_target='roles'"""
        from io import StringIO
        import sys
        from unittest.mock import patch
        from main import run_query_mode

        config = {
            "auth_mode": "static",
            "server": {"host": "127.0.0.1", "port": 8000},
            "credentials": {"player_name": "test_user", "server_id": 1},
        }

        captured_out = StringIO()
        with patch.object(SXDClient, "connect", new=AsyncMock(return_value=True)), \
             patch.object(SXDClient, "disconnect", new=AsyncMock(return_value=None)), \
             patch("main.LoginTask.execute", new=AsyncMock(return_value=MagicMock(is_success=True))), \
             patch.object(QueryService, "query_roles", new=AsyncMock(return_value=[
                 RoleDTO(role_id=1, name="巨灵神", level=100, is_deployed=True),
             ])), \
             patch.object(sys, "stdout", captured_out):
            await run_query_mode(config, query_target="roles", as_json=False)
            output = captured_out.getvalue()
            self.assertIn("参战伙伴阵容看板", output)
            self.assertIn("巨灵神", output)


    # ==================== 8. 小助手 (Assistant: Mod 52) 编解码与矩阵测试 ====================

    def _build_mock_assistant_info_payload(self) -> bytes:
        """构造 Mod 52 Act 0 info 二进制应答桩"""
        writer = ByteArrayWriter()
        # List 0: 日常条目列表 (长度 3: 招财, 祭神, 未知玩法999)
        writer.write_uint16(3)

        # 条目 1: 招财神符 (ID=1)
        writer.write_int32(1)  # item_id
        writer.write_int32(1)  # completed_count
        writer.write_uint16(1) # sub array len
        writer.write_int32(1)  # quota = 1

        # 条目 2: 帮派祭神 (ID=2)
        writer.write_int32(2)  # item_id
        writer.write_int32(0)  # completed_count
        writer.write_uint16(1)
        writer.write_int32(1)  # quota = 1

        # 条目 3: 未知新玩法 (ID=999)
        writer.write_int32(999) # item_id
        writer.write_int32(3)   # completed_count
        writer.write_uint16(1)
        writer.write_int32(5)   # quota = 5

        # List 1: 活跃度宝箱列表 (长度 3)
        writer.write_uint16(3)

        # 宝箱 1: 第 1 档 (20 活跃度，已领取 status=4)
        writer.write_int32(1)  # box_id
        writer.write_int32(20) # required_liveness
        writer.write_int32(4)  # status

        # 宝箱 2: 第 2 档 (40 活跃度，可领取 status=0)
        writer.write_int32(2)  # box_id
        writer.write_int32(40) # required_liveness
        writer.write_int32(0)  # status

        # 宝箱 3: 第 3 档 (60 活跃度，未达标 status=2)
        writer.write_int32(3)  # box_id
        writer.write_int32(60) # required_liveness
        writer.write_int32(2)  # status

        return writer.to_bytes()

    def test_assistant_dto_to_dict(self) -> None:
        """验证 AssistantDailyDTO 字典序列化"""
        item = AssistantDailyItemDTO(item_id=1, name="招财神符", completed_count=1, total_quota=1, is_completed=True)
        box = AssistantLivenessBoxDTO(box_id=1, required_liveness=20, status=4, status_desc="已领取")
        dto = AssistantDailyDTO(current_liveness=50, max_liveness=100, items=[item], boxes=[box])

        d = dto.to_dict()
        self.assertEqual(d["current_liveness"], 50)
        self.assertEqual(len(d["items"]), 1)
        self.assertEqual(d["items"][0]["name"], "招财神符")
        self.assertTrue(d["items"][0]["is_completed"])
        self.assertEqual(len(d["boxes"]), 1)
        self.assertEqual(d["boxes"][0]["status_desc"], "已领取")

    async def test_query_assistant_service_and_graceful_fallback(self) -> None:
        """验证 QueryService.query_assistant 解析、未知 ID 优雅降级与 SQLite 快照落盘"""
        mock_payload = self._build_mock_assistant_info_payload()
        self.client.request = AsyncMock(return_value=mock_payload)

        service = QueryService(self.client, self.ctx, self.player_db)
        dto = await service.query_assistant()

        self.assertEqual(len(dto.items), 3)
        self.assertEqual(dto.items[0].name, "招财神符")
        self.assertTrue(dto.items[0].is_completed)

        self.assertEqual(dto.items[1].name, "帮派祭神")
        self.assertFalse(dto.items[1].is_completed)

        # 核心防线验证：未知 ID=999 优雅回退为未知玩法，绝不抛出 KeyError
        self.assertEqual(dto.items[2].name, "未知玩法 #999")
        self.assertEqual(dto.items[2].completed_count, 3)
        self.assertEqual(dto.items[2].total_quota, 5)

        # 验证宝箱状态
        self.assertEqual(len(dto.boxes), 3)
        self.assertEqual(dto.boxes[0].status_desc, "已领取")
        self.assertEqual(dto.boxes[1].status_desc, "可领取")
        self.assertEqual(dto.boxes[2].status_desc, "未达标")

        # 验证 SQLite 模块快照落盘
        state = self.player_db.get_module_state(module_id=52, state_key="assistant_info")
        self.assertIsNotNone(state)
        self.assertIn("items", state.payload)
        self.assertEqual(len(state.payload["items"]), 3)

    def test_query_formatter_assistant_table_and_json(self) -> None:
        """验证 QueryFormatter 输出小助手矩阵表格与 JSON"""
        item = AssistantDailyItemDTO(item_id=1, name="招财神符", completed_count=1, total_quota=1, is_completed=True)
        box = AssistantLivenessBoxDTO(box_id=1, required_liveness=20, status=4, status_desc="已领取")
        dto = AssistantDailyDTO(current_liveness=50, max_liveness=100, items=[item], boxes=[box])

        table = QueryFormatter.format_assistant_table(dto)
        self.assertIn("小助手今日日常进度与活跃度看板", table)
        self.assertIn("招财神符", table)
        self.assertIn("已达成", table)
        self.assertIn("第 1 档 (20点): [已领取]", table)

        json_str = QueryFormatter.format_assistant_json(dto)
        data = json.loads(json_str)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["type"], "assistant")
        self.assertEqual(data["data"]["current_liveness"], 50)

    async def test_run_query_mode_assistant(self) -> None:
        """验证 main.py run_query_mode query_target='assistant'"""
        from io import StringIO
        import sys
        from unittest.mock import patch
        from main import run_query_mode

        config = {
            "auth_mode": "static",
            "server": {"host": "127.0.0.1", "port": 8000},
            "credentials": {"player_name": "test_user", "server_id": 1},
        }

        captured_out = StringIO()
        with patch.object(SXDClient, "connect", new=AsyncMock(return_value=True)), \
             patch.object(SXDClient, "disconnect", new=AsyncMock(return_value=None)), \
             patch("main.LoginTask.execute", new=AsyncMock(return_value=MagicMock(is_success=True))), \
             patch.object(QueryService, "query_assistant", new=AsyncMock(return_value=AssistantDailyDTO(
                 current_liveness=80,
                 items=[AssistantDailyItemDTO(item_id=1, name="招财神符", completed_count=1, total_quota=1, is_completed=True)],
                 boxes=[],
             ))), \
             patch.object(sys, "stdout", captured_out):
            await run_query_mode(config, query_target="assistant", as_json=False)
            output = captured_out.getvalue()
            self.assertIn("小助手今日日常进度与活跃度看板", output)
            self.assertIn("招财神符", output)


    # ==================== 9. 主背包与随身仓库 (Item / Pack: Mod 2) 盘点测试 ====================

    def _build_mock_pack_payload(self) -> bytes:
        """构造 Mod 2 Act 41 get_player_pack_item_list 二进制应答桩"""
        writer = ByteArrayWriter()
        # field_0: 背包总格数 (48)
        writer.write_int16(48)
        # field_1: 背包空余格数 (4格，处于空间紧张预警状态 < 5)
        writer.write_int32(4)

        # field_2: 主背包物品列表 (3 件)
        writer.write_uint16(3)
        # 物品 1: 初级体力丹 (ID=1001, 数量=3, item_type=2 消耗品, grid_id=1)
        writer.write_json([1, 1001, 1, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # 物品 2: 高级体力丹 (ID=1003, 数量=1, item_type=2 消耗品, grid_id=2)
        writer.write_json([2, 1003, 2, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # 物品 3: 普通装备 (ID=8888, 数量=1, item_type=1 装备, grid_id=3)
        writer.write_json([3, 8888, 3, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        # field_3: 随身仓库总格数 (36)
        writer.write_int16(36)

        # field_4: 随身仓库物品列表 (1 件)
        writer.write_uint16(1)
        # 物品 4: 中级经验丹 (ID=2002, 数量=2, item_type=2 消耗品, grid_id=1)
        writer.write_json([4, 2002, 1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        return writer.to_bytes()

    def test_pack_dto_to_dict(self) -> None:
        """验证 InventoryItemDTO 与 PackSummaryDTO 字典序列化"""
        item = InventoryItemDTO(
            grid_id=1,
            item_id=1001,
            name="初级体力丹",
            count=3,
            item_type=2,
            type_desc="战略消耗",
            potential_power=150,
            potential_exp=0,
            is_strategic=True,
        )
        dto = PackSummaryDTO(
            pack_capacity=48,
            pack_used=44,
            pack_empty=4,
            warehouse_capacity=36,
            warehouse_used=12,
            warehouse_empty=24,
            is_space_low=True,
            total_potential_power=150,
            total_potential_exp=0,
            category_counts={"战略消耗": 3, "装备": 1},
            strategic_items=[item],
            items=[item],
            warehouse_items=[],
        )

        d = dto.to_dict()
        self.assertEqual(d["pack_capacity"], 48)
        self.assertEqual(d["pack_empty"], 4)
        self.assertTrue(d["is_space_low"])
        self.assertEqual(d["total_potential_power"], 150)
        self.assertEqual(len(d["strategic_items"]), 1)
        self.assertEqual(d["strategic_items"][0]["name"], "初级体力丹")
        self.assertEqual(d["strategic_items"][0]["potential_power"], 150)

    async def test_query_pack_service_and_storage_persistence(self) -> None:
        """验证 QueryService.query_pack 战略消耗品收益折算、大类聚合、空间预警与 SQLite 持久化"""
        mock_payload = self._build_mock_pack_payload()
        self.client.request = AsyncMock(return_value=mock_payload)

        service = QueryService(self.client, self.ctx, self.player_db)
        dto = await service.query_pack()

        # 1. 验证容量与预警状态
        self.assertEqual(dto.pack_capacity, 48)
        self.assertEqual(dto.pack_empty, 4)
        self.assertEqual(dto.pack_used, 44)
        self.assertTrue(dto.is_space_low)  # 剩余 4 格 < 5，预警激活
        self.assertEqual(dto.warehouse_capacity, 36)

        # 2. 验证战略消耗品识别与收益折算 (初级体力丹 3*50=150, 高级体力丹 1*200=200 => 350; 中级经验丹 2*50000=100000)
        self.assertEqual(dto.total_potential_power, 350)
        self.assertEqual(dto.total_potential_exp, 100000)
        self.assertEqual(len(dto.strategic_items), 3)

        # 3. 验证未识别道具大类聚合
        self.assertEqual(dto.category_counts.get("装备", 0), 1)

        # 4. 验证即查即存与 SQLite tb_inventory 落盘
        stored_items = self.player_db.get_inventory_items()
        self.assertEqual(len(stored_items), 3)  # 主背包 3 件物品写入 tb_inventory
        self.assertEqual(stored_items[0].item_id, 1001)
        self.assertEqual(stored_items[0].count, 3)

        # 验证子系统状态快照
        state = self.player_db.get_module_state(module_id=2, state_key="pack_summary")
        self.assertIsNotNone(state)
        self.assertEqual(state.payload["total_potential_power"], 350)

        # 5. 坚守只读防线：只发起 Mod 2 Act 41 请求，绝无使用道具或开启格子写操作
        self.assertEqual(self.client.request.await_count, 1)
        called_packet = self.client.request.await_args[0][0]
        self.assertEqual(called_packet.mod, 2)
        self.assertEqual(called_packet.act, 41)

    def test_query_formatter_pack_table_and_json(self) -> None:
        """验证 QueryFormatter 输出背包盘点表格与 JSON"""
        item = InventoryItemDTO(
            grid_id=1,
            item_id=1001,
            name="初级体力丹",
            count=3,
            item_type=2,
            type_desc="战略消耗",
            potential_power=150,
            is_strategic=True,
        )
        dto = PackSummaryDTO(
            pack_capacity=48,
            pack_used=44,
            pack_empty=4,
            warehouse_capacity=36,
            warehouse_used=12,
            warehouse_empty=24,
            is_space_low=True,
            total_potential_power=350,
            total_potential_exp=100000,
            category_counts={"战略消耗": 3, "装备": 1},
            strategic_items=[item],
            items=[item],
            warehouse_items=[],
        )

        table = QueryFormatter.format_pack_table(dto)
        self.assertIn("神仙道主背包与随身仓库盘点看板", table)
        self.assertIn("空间紧张", table)
        self.assertIn("初级体力丹", table)
        self.assertIn("+350 点", table)

        json_str = QueryFormatter.format_pack_json(dto)
        data = json.loads(json_str)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["type"], "pack")
        self.assertTrue(data["data"]["is_space_low"])
        self.assertEqual(data["data"]["total_potential_power"], 350)

    async def test_run_query_mode_pack(self) -> None:
        """验证 main.py run_query_mode query_target='pack'"""
        from io import StringIO
        import sys
        from unittest.mock import patch
        from main import run_query_mode

        config = {
            "auth_mode": "static",
            "server": {"host": "127.0.0.1", "port": 8000},
            "credentials": {"player_name": "test_user", "server_id": 1},
        }

        captured_out = StringIO()
        with patch.object(SXDClient, "connect", new=AsyncMock(return_value=True)), \
             patch.object(SXDClient, "disconnect", new=AsyncMock(return_value=None)), \
             patch("main.LoginTask.execute", new=AsyncMock(return_value=MagicMock(is_success=True))), \
             patch.object(QueryService, "query_pack", new=AsyncMock(return_value=PackSummaryDTO(
                 pack_capacity=48,
                 pack_used=44,
                 pack_empty=4,
                 is_space_low=True,
                 total_potential_power=350,
                 strategic_items=[InventoryItemDTO(name="高级体力丹", count=1, potential_power=200)],
             ))), \
             patch.object(sys, "stdout", captured_out):
            await run_query_mode(config, query_target="pack", as_json=False)
            output = captured_out.getvalue()
            self.assertIn("神仙道主背包与随身仓库盘点看板", output)
            self.assertIn("高级体力丹", output)


    # ==================== 10. 全景综合态势大看板 (--query all) 测试 ====================

    def test_full_telemetry_dto_to_dict(self) -> None:
        """验证 FullTelemetryDTO 聚合实体与字典序列化"""
        assets = PlayerAssetDTO(player_id=8888, nickname="全景大侠", level=100)
        roles = [RoleDTO(role_id=1, name="巨灵神", level=90)]
        assistant = AssistantDailyDTO(current_liveness=60)
        pack = PackSummaryDTO(pack_capacity=48, pack_empty=5)

        dto = FullTelemetryDTO(
            assets=assets,
            roles=roles,
            assistant=assistant,
            pack=pack,
            errors={"test_module": "网络超时"},
        )

        d = dto.to_dict()
        self.assertIn("assets", d)
        self.assertEqual(d["assets"]["nickname"], "全景大侠")
        self.assertEqual(len(d["roles"]), 1)
        self.assertEqual(d["roles"][0]["name"], "巨灵神")
        self.assertEqual(d["assistant"]["current_liveness"], 60)
        self.assertEqual(d["pack"]["pack_capacity"], 48)
        self.assertIn("test_module", d["errors"])

    async def test_query_all_service_success(self) -> None:
        """验证 QueryService.query_all 全链路成功聚合四大子系统数据"""
        service = QueryService(self.client, self.ctx, self.player_db)
        mock_asset = PlayerAssetDTO(player_id=8888, nickname="逍遥剑仙", level=120)
        mock_roles = [RoleDTO(role_id=1, name="巨灵神", level=100)]
        mock_assistant = AssistantDailyDTO(current_liveness=80)
        mock_pack = PackSummaryDTO(pack_capacity=48, pack_used=40, pack_empty=8)

        service.query_player_assets = AsyncMock(return_value=mock_asset)
        service.query_roles = AsyncMock(return_value=mock_roles)
        service.query_assistant = AsyncMock(return_value=mock_assistant)
        service.query_pack = AsyncMock(return_value=mock_pack)

        telemetry = await service.query_all()
        self.assertEqual(telemetry.assets.nickname, "逍遥剑仙")
        self.assertEqual(len(telemetry.roles), 1)
        self.assertEqual(telemetry.assistant.current_liveness, 80)
        self.assertEqual(telemetry.pack.pack_capacity, 48)
        self.assertEqual(len(telemetry.errors), 0)

    async def test_query_all_service_graceful_degradation(self) -> None:
        """验证 QueryService.query_all 单模块超时异常时的优雅降级与错误隔离"""
        service = QueryService(self.client, self.ctx, self.player_db)
        mock_asset = PlayerAssetDTO(player_id=8888, nickname="坚韧修士", level=100)
        mock_roles = [RoleDTO(role_id=1, name="小师妹", level=80)]
        mock_pack = PackSummaryDTO(pack_capacity=48, pack_empty=10)

        service.query_player_assets = AsyncMock(return_value=mock_asset)
        service.query_roles = AsyncMock(return_value=mock_roles)
        # 模拟小助手服务出现网络超时异常
        service.query_assistant = AsyncMock(side_effect=TimeoutError("小助手服务端无响应"))
        service.query_pack = AsyncMock(return_value=mock_pack)

        # 核心防线验证：单点故障绝不导致 query_all 崩溃，未故障模块正常交付
        telemetry = await service.query_all()
        self.assertEqual(telemetry.assets.nickname, "坚韧修士")
        self.assertEqual(len(telemetry.roles), 1)
        self.assertIsNone(telemetry.assistant)  # 异常模块降级为空
        self.assertEqual(telemetry.pack.pack_capacity, 48)
        self.assertIn("assistant", telemetry.errors)
        self.assertIn("小助手服务端无响应", telemetry.errors["assistant"])

    def test_query_formatter_all_table_and_json(self) -> None:
        """验证 QueryFormatter 输出综合大看板表格与 JSON"""
        assets = PlayerAssetDTO(player_id=8888, nickname="综合大侠", level=120, coins=1000000, ingots=888)
        roles = [RoleDTO(role_id=1, name="九凤", level=110, is_deployed=True)]
        assistant = AssistantDailyDTO(current_liveness=75)
        pack = PackSummaryDTO(pack_capacity=48, pack_empty=6, total_potential_power=200)

        # 1. 正常完整看板
        dto = FullTelemetryDTO(assets=assets, roles=roles, assistant=assistant, pack=pack)
        table = QueryFormatter.format_all_table(dto)
        self.assertIn("神仙道全景综合态势大看板", table)
        self.assertIn("综合大侠", table)
        self.assertIn("九凤", table)
        self.assertIn("今日活跃度进度 : 75", table)
        self.assertIn("主背包容量", table)

        # 2. 存在模块降级时的看板容错展示
        dto_degraded = FullTelemetryDTO(
            assets=assets,
            roles=roles,
            assistant=None,
            pack=pack,
            errors={"assistant": "网络超时"},
        )
        table_degraded = QueryFormatter.format_all_table(dto_degraded)
        self.assertIn("神仙道全景综合态势大看板", table_degraded)
        self.assertIn("[小助手板块暂不可用: 网络超时]", table_degraded)

        # 3. JSON 格式化导出
        json_str = QueryFormatter.format_all_json(dto)
        data = json.loads(json_str)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["type"], "all")
        self.assertIn("assets", data["data"])
        self.assertIn("roles", data["data"])

    async def test_run_query_mode_all_and_invalid_target(self) -> None:
        """验证 main.py run_query_mode query_target='all' 与非法参数防御"""
        from io import StringIO
        import sys
        from unittest.mock import patch
        from main import run_query_mode

        config = {
            "auth_mode": "static",
            "server": {"host": "127.0.0.1", "port": 8000},
            "credentials": {"player_name": "test_user", "server_id": 1},
        }

        # 1. 验证 query_target="all"
        captured_out = StringIO()
        with patch.object(SXDClient, "connect", new=AsyncMock(return_value=True)), \
             patch.object(SXDClient, "disconnect", new=AsyncMock(return_value=None)), \
             patch("main.LoginTask.execute", new=AsyncMock(return_value=MagicMock(is_success=True))), \
             patch.object(QueryService, "query_all", new=AsyncMock(return_value=FullTelemetryDTO(
                 assets=PlayerAssetDTO(player_id=8888, nickname="综合验收员"),
                 roles=[],
                 assistant=None,
                 pack=None,
             ))), \
             patch.object(sys, "stdout", captured_out):
            await run_query_mode(config, query_target="all", as_json=False)
            output = captured_out.getvalue()
            self.assertIn("神仙道全景综合态势大看板", output)
            self.assertIn("综合验收员", output)

        # 2. 验证非法 query_target 防御与提示
        captured_err = StringIO()
        with patch.object(SXDClient, "connect", new=AsyncMock(return_value=True)), \
             patch.object(SXDClient, "disconnect", new=AsyncMock(return_value=None)), \
             patch("main.LoginTask.execute", new=AsyncMock(return_value=MagicMock(is_success=True))), \
             patch("main.logger.warning") as mock_warn:
            await run_query_mode(config, query_target="invalid_target", as_json=False)
            mock_warn.assert_called()


if __name__ == "__main__":
    unittest.main()


