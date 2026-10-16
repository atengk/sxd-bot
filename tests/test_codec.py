"""神仙道二进制协议编解码、分帧与契约往返单元测试

对照 PCAP 捕获的真实流量特征对 ByteArray 序列化、FrameFSM 状态机与 Dataclass 契约进行严格自检。

@author Ateng
@since 2026-10-15
"""

import struct
import unittest
import zlib
from protocol.frame import FrameFSM
from protocol.packet import ByteArrayReader, ByteArrayWriter, BasePacket
from protocol.builder import PacketBuilder
from protocol.messages.player import PlayerLoginReq, PlayerLoginResp, PlayerInfoResp
from protocol.messages.heartbeat import HeartbeatPkt


class TestByteArrayCodec(unittest.TestCase):
    """ByteArray 基础类型与 writeUTF 编解码测试"""

    def test_primitive_types_roundtrip(self) -> None:
        writer = ByteArrayWriter()
        writer.write_bool(True)
        writer.write_bool(False)
        writer.write_int8(-42)
        writer.write_uint8(200)
        writer.write_int16(-1234)
        writer.write_uint16(54321)
        writer.write_int32(-100000)
        writer.write_uint32(3000000000)
        writer.write_int64(9876543210123)
        writer.write_float(3.14159)
        writer.write_double(1234567.890123)
        writer.write_json({"status": "ok", "items": [1, 2, 3], "nested": {"key": "value"}})

        raw = writer.to_bytes()
        reader = ByteArrayReader(raw)

        self.assertTrue(reader.read_bool())
        self.assertFalse(reader.read_bool())
        self.assertEqual(reader.read_int8(), -42)
        self.assertEqual(reader.read_uint8(), 200)
        self.assertEqual(reader.read_int16(), -1234)
        self.assertEqual(reader.read_uint16(), 54321)
        self.assertEqual(reader.read_int32(), -100000)
        self.assertEqual(reader.read_uint32(), 3000000000)
        self.assertEqual(reader.read_int64(), 9876543210123)
        self.assertAlmostEqual(reader.read_float(), 3.14159, places=4)
        self.assertAlmostEqual(reader.read_double(), 1234567.890123, places=5)
        self.assertEqual(reader.read_json(), {"status": "ok", "items": [1, 2, 3], "nested": {"key": "value"}})
        self.assertEqual(reader.remaining, 0)

    def test_write_read_utf(self) -> None:
        writer = ByteArrayWriter()
        writer.write_utf("kongyu")
        writer.write_utf("神仙道微端测试")
        writer.write_utf("")

        raw = writer.to_bytes()
        reader = ByteArrayReader(raw)

        self.assertEqual(reader.read_utf(), "kongyu")
        self.assertEqual(reader.read_utf(), "神仙道微端测试")
        self.assertEqual(reader.read_utf(), "")
        self.assertEqual(reader.remaining, 0)


class TestFrameFSM(unittest.TestCase):
    """TCP 滑动窗口分帧状态机测试"""

    def test_uncompressed_frame_extraction(self) -> None:
        fsm = FrameFSM()
        body = b"\x00\x00\x00\x48\x00\x00\x00\x00"  # Mod 0 Act 72
        frame = struct.pack(">I", len(body)) + body

        fsm.feed(frame)
        extracted = fsm.extract_frames()

        self.assertEqual(len(extracted), 1)
        payload, is_compressed = extracted[0]
        self.assertEqual(payload, body)
        self.assertFalse(is_compressed)
        self.assertEqual(fsm.buffer_size, 0)

    def test_zlib_compressed_frame_extraction(self) -> None:
        fsm = FrameFSM()
        original_body = b"\x00\x14\x00\x57" + "公告：欢迎来到神仙道世界".encode("utf-8")
        compressed_body = zlib.compress(original_body)
        frame = struct.pack(">I", len(compressed_body)) + compressed_body

        fsm.feed(frame)
        extracted = fsm.extract_frames()

        self.assertEqual(len(extracted), 1)
        payload, is_compressed = extracted[0]
        self.assertEqual(payload, original_body)
        self.assertTrue(is_compressed)

    def test_fragmented_packet_stream(self) -> None:
        fsm = FrameFSM()
        body = b"hello_sxd_stream_test"
        frame = struct.pack(">I", len(body)) + body

        # 模拟分 3 次 TCP 分片到达
        fsm.feed(frame[:3])
        self.assertEqual(len(fsm.extract_frames()), 0)

        fsm.feed(frame[3:10])
        self.assertEqual(len(fsm.extract_frames()), 0)

        fsm.feed(frame[10:])
        extracted = fsm.extract_frames()
        self.assertEqual(len(extracted), 1)
        self.assertEqual(extracted[0][0], body)


class TestPacketModels(unittest.TestCase):
    """业务数据契约模型往返测试"""

    def test_player_login_req_serialization(self) -> None:
        req = PlayerLoginReq(
            username="test_user",
            hash_code="b4776593bb848e7b64f88a98deb41a8c",
            time="1792065385",
            platform="fengwanyx",
            server_id=25268,
        )

        frame_bytes = req.to_network_frame()
        self.assertGreater(len(frame_bytes), 4)

        payload_len = struct.unpack(">I", frame_bytes[:4])[0]
        self.assertEqual(payload_len, len(frame_bytes) - 4)

        mod, act = struct.unpack(">HH", frame_bytes[4:8])
        self.assertEqual(mod, 0)
        self.assertEqual(act, 0)

        # 解码并校验字段一致性
        decoded = PlayerLoginReq.decode(frame_bytes[8:])
        self.assertEqual(decoded.username, "test_user")
        self.assertEqual(decoded.hash_code, "b4776593bb848e7b64f88a98deb41a8c")
        self.assertEqual(decoded.server_id, 25268)

    def test_pipelined_multi_frame_extraction(self) -> None:
        """测试在单个 TCP 报文中粘连多个独立物理帧的切片还原 (Stream 18 Turn 1 全量 120 字节)"""
        full_turn1_hex = (
            "000000680000000000066b6f6e6779750020623437373635393362623834386537623634"
            "6638386139386465623431613863000a31373932303635333835000966656e6777616e79"
            "7800000000000062b40160000006e796afe78ea9000570635f77640100066b6f6e677975"
            "000000080000004800000000"
        )
        raw_bytes = bytes.fromhex(full_turn1_hex)
        fsm = FrameFSM()
        fsm.feed(raw_bytes)
        frames = fsm.extract_frames()

        self.assertEqual(len(frames), 2)
        
        # 帧 1: Mod 0 Act 0 (login_req)
        frame1_payload, is_zlib1 = frames[0]
        self.assertFalse(is_zlib1)
        mod1, act1 = struct.unpack(">HH", frame1_payload[:4])
        self.assertEqual(mod1, 0)
        self.assertEqual(act1, 0)
        login_req = PlayerLoginReq.decode(frame1_payload[4:])
        self.assertEqual(login_req.username, "kongyu")
        self.assertEqual(login_req.server_id, 25268)

        # 帧 2: Mod 0 Act 72 (init_client)
        frame2_payload, is_zlib2 = frames[1]
        self.assertFalse(is_zlib2)
        mod2, act2 = struct.unpack(">HH", frame2_payload[:4])
        self.assertEqual(mod2, 0)
        self.assertEqual(act2, 72)
        reader2 = ByteArrayReader(frame2_payload[4:])
        self.assertEqual(reader2.read_int32(), 0)

    def test_dual_mode_zlib_decompression(self) -> None:
        """测试顶层直出模式与 Payload 级压缩模式的双模式自适应解压"""
        fsm = FrameFSM()
        
        # 1. 顶层直出模式 (Top-Level Zlib)
        top_original = b"\x00\x14\x00\x57\x00\x05hello"
        top_compressed = zlib.compress(top_original)
        top_frame = struct.pack(">I", len(top_compressed)) + top_compressed
        fsm.feed(top_frame)
        res1 = fsm.extract_frames()
        self.assertEqual(len(res1), 1)
        self.assertEqual(res1[0][0], top_original)
        self.assertTrue(res1[0][1])

        # 2. 载荷级压缩模式 (Payload-Level Zlib)
        header = b"\x00\x14\x00\x57"
        body = b"\x00\x05world"
        body_compressed = zlib.compress(body)
        payload_frame_body = header + body_compressed
        payload_frame = struct.pack(">I", len(payload_frame_body)) + payload_frame_body
        fsm.feed(payload_frame)
        res2 = fsm.extract_frames()
        self.assertEqual(len(res2), 1)
        self.assertEqual(res2[0][0], header + body)
        self.assertTrue(res2[0][1])

    def test_pcap_real_turn2_login_resp_compliance(self) -> None:
        """测试 Stream 18 Turn 2 登录成功回执帧 (30字节, 官方 10 字段契约)"""
        turn2_hex = "0000001a0000000000000000040a000000000000000001000b0000108501"
        raw_bytes = bytes.fromhex(turn2_hex)
        fsm = FrameFSM()
        fsm.feed(raw_bytes)
        frames = fsm.extract_frames()

        self.assertEqual(len(frames), 1)
        payload, is_zlib = frames[0]
        self.assertFalse(is_zlib)
        mod, act = struct.unpack(">HH", payload[:4])
        self.assertEqual(mod, 0)
        self.assertEqual(act, 0)

        # 对照 Mod_Player_Base.login.response 官方 10 个字段序列化契约
        reader = ByteArrayReader(payload[4:])
        status = reader.read_uint8()     # [0] UByteUtil: 状态码 0=成功
        field2 = reader.read_int32()     # [1] IntUtil: 4
        field3 = reader.read_uint8()     # [2] UByteUtil: 10
        field4 = reader.read_int32()     # [3] IntUtil: 0
        field5 = reader.read_int8()      # [4] ByteUtil: 0
        field6 = reader.read_int32()     # [5] IntUtil: 1
        field7 = reader.read_int8()      # [6] ByteUtil: 0
        field8 = reader.read_uint8()     # [7] UByteUtil: 11
        field9 = reader.read_int32()     # [8] IntUtil: 4229 (0x1085)
        field10 = reader.read_int8()     # [9] ByteUtil: 1

        self.assertEqual(status, 0)
        self.assertEqual(field2, 4)
        self.assertEqual(field3, 10)
        self.assertEqual(field4, 0)
        self.assertEqual(field5, 0)
        self.assertEqual(field6, 1)
        self.assertEqual(field7, 0)
        self.assertEqual(field8, 11)
        self.assertEqual(field9, 4229)
        self.assertEqual(field10, 1)
        self.assertEqual(reader.remaining, 0)

    def test_player_info_resp_official_decoding(self) -> None:
        """测试 Mod 0 Act 2 官方 44 字段解包契约"""
        from protocol.packet import ByteArrayWriter
        writer = ByteArrayWriter()
        writer.write_utf("梦一场")     # 0: nickname
        writer.write_int32(300)        # 1: level
        writer.write_int32(40096)      # 2: ingots
        writer.write_int64(36807665882)# 3: coins
        writer.write_int64(9180049)    # 4: health
        writer.write_int64(9180049)    # 5: max_health
        writer.write_int32(138)        # 6: power
        writer.write_int64(1000)       # 7: exp
        writer.write_int64(2000)       # 8: max_exp
        writer.write_int32(29)         # 9: town_map_id
        # 10 ~ 13 (4 ints)
        for _ in range(4): writer.write_int32(0)
        writer.write_int32(10)         # 14: vip_level
        # 15 ~ 18 (4 ints)
        for _ in range(4): writer.write_int32(0)
        writer.write_int8(1)           # 19: camp_id
        writer.write_int32(0)          # 20: townKey
        writer.write_int32(50000)      # 21: fame
        # 22 ~ 28 (7 ints)
        for _ in range(7): writer.write_int32(0)
        writer.write_int32(854)        # 29: mission_key

        resp = PlayerInfoResp.decode(writer.to_bytes())
        self.assertEqual(resp.nickname, "梦一场")
        self.assertEqual(resp.level, 300)
        self.assertEqual(resp.ingots, 40096)
        self.assertEqual(resp.coins, 36807665882)
        self.assertEqual(resp.power, 138)
        self.assertEqual(resp.town_map_id, 29)
        self.assertEqual(resp.vip_level, 10)
        self.assertEqual(resp.camp_id, 1)
        self.assertEqual(resp.fame, 50000)
        self.assertEqual(resp.mission_key, 854)


if __name__ == "__main__":
    unittest.main()
