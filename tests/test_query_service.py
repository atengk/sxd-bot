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

from services.query_models import PlayerAssetDTO
from services.query_service import QueryService
from services.query_formatter import QueryFormatter


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

        # 2. 测试 JSON 格式
        captured_json_out = StringIO()
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
             patch.object(sys, "stdout", captured_json_out):
            await run_query_mode(config, query_target="assets", as_json=True)
            json_val = captured_json_out.getvalue()
            data = json.loads(json_val)
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["data"]["coins"], 123456)


if __name__ == "__main__":
    unittest.main()
