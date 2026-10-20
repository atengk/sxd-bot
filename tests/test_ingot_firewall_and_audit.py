"""出站元宝安全防火墙、双轨审计与仙桃任务回归单元测试套件

测试覆盖：
1. IngotFirewall 规则引擎针对高危出站指令与动态载荷的阻断与放行判定
2. SXDClient 网络层物理阻断、INGOT_BLOCKED 事件广播与底层套接字零下发
3. SqliteStorageSubscriber 双轨审计：事前拦截审计与事后差额审计完整落库
4. PeachAndPetTask 摘仙桃任务彻底清除 Mod 40 Act 6 召唤白猿的零元宝安全性

@author Ateng
@since 2026-10-20
"""

import asyncio
import os
import tempfile
import time
import unittest
from unittest.mock import AsyncMock, MagicMock

from core.context import GameContext
from core.events import EventBus
from core.security import IngotFirewall, IngotSecurityException
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import BasePacket
from storage.player_db import PlayerDatabase, PlayerProfileRecord
from storage.subscriber import SqliteStorageSubscriber
from storage.worker import StorageWorker
from tasks.routine.peach_pet import PeachAndPetTask


class TestIngotFirewall(unittest.TestCase):
    """出站元宝安全防火墙规则判定单元测试

    @author Ateng
    @since 2026-10-20
    """

    def test_unconditional_hazardous_actions_blocked(self) -> None:
        """测试无条件高危元宝操作黑名单默认强阻断"""
        # 1. 仙桃召唤白猿 (Mod 40, Act 6)
        pkt_call_peach = PacketBuilder(mod=40, act=6).build()
        is_safe, action, reason = IngotFirewall.check_egress(pkt_call_peach, allow_ingot=False)
        self.assertFalse(is_safe)
        self.assertIn("召唤白猿", action)

        # 2. 竞技场购买次数 (Mod 28, Act 4)
        pkt_buy_sport = PacketBuilder(mod=28, act=4).build()
        is_safe, action, reason = IngotFirewall.check_egress(pkt_buy_sport, allow_ingot=False)
        self.assertFalse(is_safe)
        self.assertIn("竞技场", action)

        # 3. 药园开地 (Mod 13, Act 3)
        pkt_farm_open = PacketBuilder(mod=13, act=3).build()
        is_safe, action, reason = IngotFirewall.check_egress(pkt_farm_open, allow_ingot=False)
        self.assertFalse(is_safe)
        self.assertIn("药园", action)

    def test_unconditional_hazardous_actions_with_allow_ingot(self) -> None:
        """测试显式授权 allow_ingot=True 时放行无条件高危指令"""
        pkt_call_peach = PacketBuilder(mod=40, act=6).build()
        is_safe, action, reason = IngotFirewall.check_egress(pkt_call_peach, allow_ingot=True)
        self.assertTrue(is_safe)

    def test_conditional_worship_mars_incense(self) -> None:
        """测试帮派祭神白檀香 (铜钱) 放行，苏合香/天木香 (元宝) 阻断"""
        # 白檀香: type=1 (4 字节大端整数)
        pkt_sandalwood = PacketBuilder(mod=41, act=1).write_int32(1).build()
        is_safe, _, _ = IngotFirewall.check_egress(pkt_sandalwood, allow_ingot=False)
        self.assertTrue(is_safe)

        # 苏合香: type=2 (消耗元宝)
        pkt_suhe = PacketBuilder(mod=41, act=1).write_int32(2).build()
        is_safe, action, reason = IngotFirewall.check_egress(pkt_suhe, allow_ingot=False)
        self.assertFalse(is_safe)
        self.assertIn("元宝上香", action)

        # 天木香: type=3 (消耗元宝)
        pkt_tianmu = PacketBuilder(mod=41, act=1).write_int32(3).build()
        is_safe, action, reason = IngotFirewall.check_egress(pkt_tianmu, allow_ingot=False)
        self.assertFalse(is_safe)
        self.assertIn("元宝上香", action)

    def test_conditional_feed_pet(self) -> None:
        """测试神龙培养 feed_type=0 (铜钱) 放行，非 0 阻断"""
        pkt_free = PacketBuilder(mod=48, act=2).write_uint8(0).build()
        is_safe, _, _ = IngotFirewall.check_egress(pkt_free, allow_ingot=False)
        self.assertTrue(is_safe)

        pkt_ingot = PacketBuilder(mod=48, act=2).write_uint8(1).build()
        is_safe, action, _ = IngotFirewall.check_egress(pkt_ingot, allow_ingot=False)
        self.assertFalse(is_safe)
        self.assertIn("神龙元宝培养", action)

    def test_conditional_world_boss_inspire(self) -> None:
        """测试世界Boss阅历鼓舞 (type=1) 放行，元宝鼓舞阻断"""
        pkt_skill = PacketBuilder(mod=24, act=7).write_uint8(1).build()
        is_safe, _, _ = IngotFirewall.check_egress(pkt_skill, allow_ingot=False)
        self.assertTrue(is_safe)

        pkt_ingot = PacketBuilder(mod=24, act=7).write_uint8(2).build()
        is_safe, action, _ = IngotFirewall.check_egress(pkt_ingot, allow_ingot=False)
        self.assertFalse(is_safe)
        self.assertIn("世界Boss元宝鼓舞", action)

    def test_safe_read_and_routine_packets(self) -> None:
        """测试安全查询与日常普通数据包正常放行"""
        pkt_heartbeat = PacketBuilder(mod=0, act=22).build()
        is_safe, _, _ = IngotFirewall.check_egress(pkt_heartbeat, allow_ingot=False)
        self.assertTrue(is_safe)

        pkt_farm_info = PacketBuilder(mod=13, act=0).build()
        is_safe, _, _ = IngotFirewall.check_egress(pkt_farm_info, allow_ingot=False)
        self.assertTrue(is_safe)

        pkt_peach_info = PacketBuilder(mod=40, act=0).build()
        is_safe, _, _ = IngotFirewall.check_egress(pkt_peach_info, allow_ingot=False)
        self.assertTrue(is_safe)


class TestClientEgressFirewallIntegration(unittest.IsolatedAsyncioTestCase):
    """SXDClient 网络层出站防火墙集成测试

    @author Ateng
    @since 2026-10-20
    """

    async def asyncSetUp(self) -> None:
        self.context = GameContext()
        self.context.set_connected(True)
        self.event_bus = EventBus()
        self.client = SXDClient(context=self.context, event_bus=self.event_bus)
        self.client._running = True

        # 模拟底层 Socket 写入器
        self.mock_writer = MagicMock()
        self.mock_writer.write = MagicMock()
        self.mock_writer.drain = AsyncMock()
        self.client._writer = self.mock_writer

    async def test_send_packet_blocks_hazardous_egress(self) -> None:
        """测试 send_packet 拦截高危出站并广播 INGOT_BLOCKED 事件且不写入底层 Socket"""
        events_captured = []

        def on_blocked(data):
            events_captured.append(data)

        self.event_bus.subscribe_event("INGOT_BLOCKED", on_blocked)

        hazardous_pkt = PacketBuilder(mod=40, act=6).build()
        with self.assertRaises(IngotSecurityException) as ctx:
            await self.client.send_packet(hazardous_pkt, allow_ingot=False)

        self.assertIn("仙桃召唤白猿", str(ctx.exception))
        # 验证底层 Socket 绝对零下发
        self.mock_writer.write.assert_not_called()
        # 验证事件捕获
        self.assertEqual(len(events_captured), 1)
        self.assertEqual(events_captured[0]["module_id"], 40)
        self.assertEqual(events_captured[0]["action_id"], 6)

    async def test_request_blocks_hazardous_egress(self) -> None:
        """测试 request 拦截高危指令，不挂起也不写入 Socket"""
        hazardous_pkt = PacketBuilder(mod=28, act=4).build()
        with self.assertRaises(IngotSecurityException):
            await self.client.request(hazardous_pkt, allow_ingot=False)

        self.mock_writer.write.assert_not_called()
        self.assertEqual(len(self.client._pending_futures), 0)

    async def test_send_packet_allows_safe_packet(self) -> None:
        """测试普通安全指令正常写入底层 Socket"""
        safe_pkt = PacketBuilder(mod=0, act=22).build()
        await self.client.send_packet(safe_pkt, allow_ingot=False)
        self.mock_writer.write.assert_called_once()


class TestDualTrackAuditStorageIntegration(unittest.TestCase):
    """持久化切面双轨元宝审计落库集成测试

    @author Ateng
    @since 2026-10-20
    """

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_audit.db")
        self.player_db = PlayerDatabase(db_path=self.db_path, player_id=8888, server_id="s813")
        self.worker = StorageWorker(db=self.player_db)
        self.worker.start()

        self.context = GameContext()
        self.context.set_connected(True)
        self.context.update_player_info(
            nickname="审计测试号",
            player_id=8888,
            level=100,
            coins=1000000,
            ingots=5000,
        )
        self.event_bus = EventBus()
        self.subscriber = SqliteStorageSubscriber(
            worker=self.worker,
            player_db=self.player_db,
            player_id=8888,
            context=self.context,
        )
        self.subscriber.attach_to_event_bus(self.event_bus)

        # 预先持久化初始角色画像形成基线
        self.player_db.upsert_player_profile(
            PlayerProfileRecord(
                player_id=8888,
                nickname="审计测试号",
                level=100,
                coins=1000000,
                ingots=5000,
            )
        )

    def tearDown(self) -> None:
        self.worker.stop()
        self.temp_dir.cleanup()

    def test_pre_egress_firewall_audit(self) -> None:
        """测试事前拦截轨：收到 INGOT_BLOCKED 事件后正确生成审计记录入库"""
        self.context.set_active_task("peach_pet")
        self.event_bus.publish(
            "INGOT_BLOCKED",
            {
                "module_id": 40,
                "action_id": 6,
                "action_name": "仙桃召唤白猿(100元宝)",
                "reason": "出站防火墙拦截高危元宝操作: 仙桃召唤白猿(100元宝)",
                "timestamp": time.time(),
            },
        )
        self.worker.flush()

        logs = self.player_db.get_recent_audit_logs(limit=10)
        self.assertGreaterEqual(len(logs), 1)
        target_log = logs[0]
        self.assertEqual(target_log.module_id, 40)
        self.assertEqual(target_log.action_id, 6)
        self.assertIn("[防火墙拦截]", target_log.action_name)
        self.assertFalse(target_log.allow_ingot)
        self.assertEqual(target_log.details.get("stage"), "pre_egress_firewall")
        self.assertEqual(target_log.details.get("active_task"), "peach_pet")

    def test_post_egress_delta_audit(self) -> None:
        """测试事后差额轨：下行动态属性广播元宝减少强制入库审计流水"""
        self.context.set_active_task("farm")
        # 构造 Mod 0 Act 3 (PlayerUpdatePlayerDataResp) 载荷: 属性 19 (元宝) 减少 100 (5000 -> 4900)
        from protocol.messages.player import PlayerUpdatePlayerDataResp
        payload = PlayerUpdatePlayerDataResp(updates={19: 4900}).encode_payload()

        # 触发下行广播
        asyncio.run(self.subscriber._on_update_player_data(0, 3, payload))
        self.worker.flush()

        logs = self.player_db.get_recent_audit_logs(limit=10)
        self.assertGreaterEqual(len(logs), 1)
        target_log = logs[0]
        self.assertEqual(target_log.module_id, 0)
        self.assertEqual(target_log.action_id, 3)
        self.assertIn("[元宝消耗]", target_log.action_name)
        self.assertFalse(target_log.allow_ingot)
        self.assertEqual(target_log.details.get("stage"), "post_egress_delta")
        self.assertEqual(target_log.details.get("delta"), -100)
        self.assertEqual(target_log.details.get("previous_balance"), 5000)
        self.assertEqual(target_log.details.get("current_balance"), 4900)
        self.assertEqual(target_log.details.get("active_task"), "farm")

    def test_peach_pet_task_never_sends_call_peach(self) -> None:
        """测试 PeachAndPetTask 执行时绝不发送 Mod 40 Act 6 (零元宝保证)"""
        task = PeachAndPetTask()
        sent_mod_acts = []

        mock_client = MagicMock()
        mock_client.context = self.context

        async def fake_request(packet, timeout_sec=2.0):
            sent_mod_acts.append((packet.mod, packet.act))
            # 模拟 Mod 40 Act 3 (仙桃面板)
            if packet.mod == 40 and packet.act == 3:
                return bytes([0] * 10)
            # 模拟 Mod 40 Act 4 (偷桃进度)
            if packet.mod == 40 and packet.act == 4:
                return bytes([0] * 15)
            # 模拟 Mod 40 Act 5 (一键批量摘仙桃) 响应: 9 字节 [0=SUCCESS] + [4B extra] + [4B exp=1000]
            if packet.mod == 40 and packet.act == 5:
                w = ByteArrayWriter()
                w.write_uint8(0).write_int32(0).write_int32(1000)
                return w.to_bytes()
            # 模拟 Mod 48 Act 2 (神龙喂养) 响应: 1 字节 SUCCESS=0
            if packet.mod == 48 and packet.act == 2:
                return bytes([0])
            return b""

        mock_client.request = AsyncMock(side_effect=fake_request)

        result = asyncio.run(task.execute(mock_client, self.context))
        self.assertTrue(result.is_success)

        # 验证发送的协议动作列表，确保绝不包含 (40, 6)
        self.assertNotIn((40, 6), sent_mod_acts)
        # 验证包含 (40, 3), (40, 4), (40, 5), (48, 2)
        expected_subset = {(40, 3), (40, 4), (40, 5), (48, 2)}
        self.assertTrue(expected_subset.issubset(set(sent_mod_acts)))


if __name__ == "__main__":
    unittest.main()
