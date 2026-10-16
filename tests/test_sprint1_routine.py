"""Sprint 1 基础日常福利与帮派白檀香祭神离线单元测试

覆盖 FactionWorshipTask (Mod 21)、DailySignInTask (Mod 42, 127) 与 OnlineGiftTask (Mod 0)。
严格验证零元宝安全熔断逻辑与大端二进制编解码。

@author Ateng
@since 2026-10-16
"""

import unittest
from unittest.mock import AsyncMock
from core.context import GameContext
from tasks.routine.worship import FactionWorshipTask, INCENSE_SANDALWOOD
from tasks.routine.signin import DailySignInTask
from tasks.routine.online_gift import OnlineGiftTask
from protocol.builder import PacketBuilder


class TestSprint1RoutineTasks(unittest.IsolatedAsyncioTestCase):
    """Sprint 1 日常福利任务测试套件

    @author Ateng
    @since 2026-10-16
    """

    def setUp(self):
        self.ctx = GameContext()
        self.ctx.set_connected(True)
        self.mock_client = AsyncMock()

    async def test_worship_mars_success(self):
        """测试帮派祭神：剩余次数 > 0 时，成功发送白檀香上香"""
        task = FactionWorshipTask()
        # 模拟 Mod 21 Act 0 回包 24 字节 (free_times=1, max_times=5, god_level=10)
        status_resp_payload = PacketBuilder(mod=21, act=0) \
            .write_int32(0) \
            .write_int32(10) \
            .write_int32(0) \
            .write_int32(0) \
            .write_int32(1) \
            .write_int32(5) \
            .build() \
            .encode_payload()

        # 模拟上香成功回包
        incense_resp = bytes.fromhex("0000000101")

        self.mock_client.request.side_effect = [status_resp_payload, incense_resp]

        result = await task.execute(self.mock_client, self.ctx)
        self.assertTrue(result.success)
        self.assertEqual(result.data.get("incense_type"), INCENSE_SANDALWOOD)

        # 验证发送的上香请求内容
        self.assertEqual(self.mock_client.request.call_count, 2)
        incense_req_sent = self.mock_client.request.call_args_list[1][0][0]
        # 校验 DynamicPacket 属性
        self.assertEqual(incense_req_sent.mod, 21)
        self.assertEqual(incense_req_sent.act, 1)
        self.assertEqual(incense_req_sent.payload, bytes([0x01]))  # 白檀香

    async def test_worship_mars_zero_ingot_guardrail(self):
        """测试帮派祭神：剩余次数 == 0 时，触发零元宝熔断，坚决不上香"""
        task = FactionWorshipTask()
        # 模拟 Mod 21 Act 0 回包 (free_times=0)
        status_resp_payload = PacketBuilder(mod=21, act=0) \
            .write_int32(0) \
            .write_int32(10) \
            .write_int32(0) \
            .write_int32(0) \
            .write_int32(0) \
            .write_int32(5) \
            .build() \
            .encode_payload()

        self.mock_client.request.return_value = status_resp_payload

        result = await task.execute(self.mock_client, self.ctx)
        self.assertTrue(result.skipped)
        self.assertIn("零元宝熔断", result.message)

        # 确保只执行了状态查询，绝对没有发送上香请求
        self.assertEqual(self.mock_client.request.call_count, 1)

    async def test_daily_sign_in_flow(self):
        """测试签到与七日礼包：未签到时触发签到，针对可领取的七日礼包发送领取"""
        task = DailySignInTask()

        # 模拟 Mod 42 Act 0 回包 (signed_days=5, is_signed=0: 未签到, 时间戳 8B)
        sign42_payload = PacketBuilder(mod=42, act=0) \
            .write_uint16(5) \
            .write_uint8(0) \
            .write_int64(1792100000) \
            .build() \
            .encode_payload()

        # 模拟 Mod 42 Act 2 签到成功回包
        sign42_do_resp = bytes.fromhex("01")

        # 模拟 Mod 127 Act 0 七日礼包列表回包 (2 项：项 1 已领，项 2 未领)
        sign127_payload = PacketBuilder(mod=127, act=0) \
            .write_uint16(2) \
            .write_uint16(101).write_uint8(1) \
            .write_uint16(102).write_uint8(0) \
            .build() \
            .encode_payload()

        self.mock_client.request.side_effect = [sign42_payload, sign42_do_resp, sign127_payload]

        result = await task.execute(self.mock_client, self.ctx)
        self.assertTrue(result.success)
        # 应触发常规签到 1 次 + 七日礼包 1 次 = 2 项
        self.assertEqual(result.data.get("claimed_count"), 2)

        # 验证发送的七日礼包领取指令 (Mod 127, Act 2, item_idx=2)
        self.assertEqual(self.mock_client.send_packet.call_count, 1)
        pkt_sent = self.mock_client.send_packet.call_args[0][0]
        self.assertEqual(pkt_sent.mod, 127)
        self.assertEqual(pkt_sent.act, 2)
        self.assertEqual(pkt_sent.payload, bytes([0x00, 0x02]))  # item_idx = 2

    async def test_online_gift_flow(self):
        """测试在线礼包与俸禄：发送微端专享、在线时长与每日俸禄"""
        task = OnlineGiftTask()
        result = await task.execute(self.mock_client, self.ctx)

        self.assertTrue(result.success)
        self.assertEqual(result.data.get("claimed"), 3)
        self.assertEqual(self.mock_client.send_packet.call_count, 3)

        calls = [c[0][0] for c in self.mock_client.send_packet.call_args_list]
        # Mod 0 Act 39 (微端礼包)
        self.assertEqual(calls[0].mod, 0)
        self.assertEqual(calls[0].act, 39)
        # Mod 0 Act 46 (在线时长)
        self.assertEqual(calls[1].mod, 0)
        self.assertEqual(calls[1].act, 46)
        # Mod 0 Act 22 (阵营俸禄)
        self.assertEqual(calls[2].mod, 0)
        self.assertEqual(calls[2].act, 22)


if __name__ == "__main__":
    unittest.main()
