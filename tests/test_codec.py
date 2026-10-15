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
        writer.write_int8(-42)
        writer.write_uint8(200)
        writer.write_int16(-1234)
        writer.write_uint16(54321)
        writer.write_int32(-100000)
        writer.write_uint32(3000000000)
        writer.write_int64(9876543210123)

        raw = writer.to_bytes()
        reader = ByteArrayReader(raw)

        self.assertEqual(reader.read_int8(), -42)
        self.assertEqual(reader.read_uint8(), 200)
        self.assertEqual(reader.read_int16(), -1234)
        self.assertEqual(reader.read_uint16(), 54321)
        self.assertEqual(reader.read_int32(), -100000)
        self.assertEqual(reader.read_uint32(), 3000000000)
        self.assertEqual(reader.read_int64(), 9876543210123)
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

    def test_pcap_real_turn1_hex_compliance(self) -> None:
        # 对照 PCAP Stream 18 Turn 1 真实报文数据切片
        hex_data = (
            "000000680000000000066b6f6e6779750020623437373635393362623834386537623634"
            "6638386139386465623431613863000a31373932303635333835000966656e6777616e79"
            "7800000000000062b40160000006e796afe78ea9000570635f77640100066b6f6e677975"
        )
        raw_bytes = bytes.fromhex(hex_data)

        fsm = FrameFSM()
        fsm.feed(raw_bytes)
        frames = fsm.extract_frames()

        self.assertEqual(len(frames), 1)
        payload, is_zlib = frames[0]
        self.assertFalse(is_zlib)

        mod, act = struct.unpack(">HH", payload[:4])
        self.assertEqual(mod, 0)
        self.assertEqual(act, 0)

        # 验证能完全反序列化为 PlayerLoginReq
        login_req = PlayerLoginReq.decode(payload[4:])
        self.assertEqual(login_req.username, "kongyu")
        self.assertEqual(login_req.hash_code, "b4776593bb848e7b64f88a98deb41a8c")
        self.assertEqual(login_req.time, "1792065385")
        self.assertEqual(login_req.platform, "fengwanyx")
        self.assertEqual(login_req.server_id, 25268)


if __name__ == "__main__":
    unittest.main()
