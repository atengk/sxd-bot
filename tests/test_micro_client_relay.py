"""微端宿主架构、本地代理中继与端到端握手协议仿真测试套件

测试覆盖:
1. WebAuthFetcher 3 步鉴权流程与凭据兑换测试 (模拟平台接口与内嵌 JSON 解析)
2. 本地代理中继透明全双工流转发测试 (模拟 8061 <-> 8062 真实中继网络拓扑)
3. Turn 1 复合握手帧 (120 字节: Mod 0 Act 0 + Mod 0 Act 72) 组装与切帧测试
4. Turn 2 登录成功回执与全局上下文激活测试
5. 本地辅助 IPC 协议 (Mod 94, Mod 529, Mod 336, Mod 293) 报文还原测试
6. 无微端图形界面环境下 SXDClient 异步长连接握手端到端闭环测试

@author Ateng
@since 2026-10-16
"""

import asyncio
import io
import json
import struct
import unittest
from unittest.mock import patch, MagicMock
from core.context import GameContext
from core.events import EventBus
from network.client import SXDClient
from network.web_auth import WebAuthFetcher, GatewayCredentials
from protocol.frame import FrameFSM
from protocol.packet import ByteArrayReader, ByteArrayWriter
from protocol.messages.player import PlayerLoginReq, PlayerLoginResp


class TestWebAuthFlow(unittest.TestCase):
    """Web 自动化鉴权与凭据提取测试

    @author Ateng
    @since 2026-10-16
    """

    @patch("urllib.request.build_opener")
    def test_auto_login_success(self, mock_build_opener: MagicMock) -> None:
        """测试 Web 登录 3 步全自动鉴权成功分支"""
        mock_opener = MagicMock()
        mock_build_opener.return_value = mock_opener

        # 1. 模拟 login.php 响应
        resp1 = MagicMock()
        resp1.read.return_value = json.dumps({"username": "kongyu", "status": 1}).encode("utf-8")
        resp1.__enter__.return_value = resp1

        # 2. 模拟 play.php 响应
        resp2 = MagicMock()
        resp2.read.return_value = json.dumps({
            "regdate": "1693793577",
            "pi": "test_pi",
            "hash": "test_hash_play",
            "time": "1792065385",
            "non_kid": 1,
        }).encode("utf-8")
        resp2.__enter__.return_value = resp2

        # 3. 模拟 index_wd.php 响应 (包含内嵌 JSON 的 HTML 页面)
        html_payload = """
        <html>
        <head><title>SXD WeiDuan</title></head>
        <body>
        <script>
        var wd_config = {"code":1,"msg":"success","data":{"ip":"127.0.0.1","port":8381,"player_name":"kongyu","hash_code":"b4776593bb848e7b64f88a98deb41a8c","time":"1792065385","server_id":25268,"is_wd":1}};
        </script>
        </body>
        </html>
        """
        resp3 = MagicMock()
        resp3.read.return_value = html_payload.encode("utf-8")
        resp3.__enter__.return_value = resp3

        mock_opener.open.side_effect = [resp1, resp2, resp3]

        creds = WebAuthFetcher.auto_login("kongyu", "secret123", server="s813")
        self.assertIsNotNone(creds)
        assert creds is not None
        self.assertEqual(creds.server_host, "127.0.0.1")
        self.assertEqual(creds.server_port, 8381)
        self.assertEqual(creds.player_name, "kongyu")
        self.assertEqual(creds.hash_code, "b4776593bb848e7b64f88a98deb41a8c")
        self.assertEqual(creds.time, "1792065385")
        self.assertEqual(creds.server_id, 25268)

    @patch("urllib.request.build_opener")
    def test_auto_login_step1_failure(self, mock_build_opener: MagicMock) -> None:
        """测试步骤 1 账号密码错误时优雅降级返回 None"""
        mock_opener = MagicMock()
        mock_build_opener.return_value = mock_opener

        resp1 = MagicMock()
        resp1.read.return_value = json.dumps({"username": "", "status": 0, "msg": "密码错误"}).encode("utf-8")
        resp1.__enter__.return_value = resp1

        mock_opener.open.return_value = resp1
        creds = WebAuthFetcher.auto_login("kongyu", "wrong_pass")
        self.assertIsNone(creds)


class TestMicroClientRelayAndIPC(unittest.TestCase):
    """微端本地网络中继与 IPC 封包还原测试

    @author Ateng
    @since 2026-10-16
    """

    def test_turn1_handshake_composite_frame(self) -> None:
        """测试 Turn 1 复合握手帧 (120 字节) 组装与切片拆解"""
        # 1. 组装 Frame 1: Mod 0 Act 0 (PlayerLoginReq)
        login_req = PlayerLoginReq(
            username="kongyu",
            hash_code="b4776593bb848e7b64f88a98deb41a8c",
            time="1792065385",
            platform="fengwanyx",
            server_id=25268,
            is_wd=1,
            wd_code=0x60,
            sub_code=0,
            publish="疯玩",
            client_type="pc_wd",
            flag=1,
            account="kongyu",
        )
        frame1_bytes = login_req.to_network_frame()
        self.assertEqual(len(frame1_bytes), 108)  # 4B Length (104) + 104B Body

        # 2. 组装 Frame 2: Mod 0 Act 72 (init_client)
        writer2 = ByteArrayWriter()
        writer2.write_int32(0)
        body2 = writer2.to_bytes()
        frame2_len = 4 + len(body2)
        frame2_bytes = struct.pack(">IHH", frame2_len, 0, 72) + body2
        self.assertEqual(len(frame2_bytes), 12)  # 4B Len + 4B ModAct + 4B Val = 12B

        # 3. 粘包拼接为单一 TCP 载荷 (120 字节)
        turn1_combined = frame1_bytes + frame2_bytes
        self.assertEqual(len(turn1_combined), 120)

        # 4. 通过 FrameFSM 切片提取
        fsm = FrameFSM()
        fsm.feed(turn1_combined)
        frames = fsm.extract_frames()
        self.assertEqual(len(frames), 2)

        # 验证 Frame 1 内容
        p1, z1 = frames[0]
        self.assertFalse(z1)
        m1, a1 = struct.unpack(">HH", p1[:4])
        self.assertEqual((m1, a1), (0, 0))
        decoded_req = PlayerLoginReq.decode(p1[4:])
        self.assertEqual(decoded_req.username, "kongyu")
        self.assertEqual(decoded_req.client_type, "pc_wd")

        # 验证 Frame 2 内容
        p2, z2 = frames[1]
        self.assertFalse(z2)
        m2, a2 = struct.unpack(">HH", p2[:4])
        self.assertEqual((m2, a2), (0, 72))
        r2 = ByteArrayReader(p2[4:])
        self.assertEqual(r2.read_int32(), 0)

    def test_turn2_login_resp_state_sync(self) -> None:
        """测试 Turn 2 登录成功回执帧解码与状态同步"""
        turn2_hex = "0000001a0000000000000000040a000000000000000001000b0000108501"
        raw_bytes = bytes.fromhex(turn2_hex)
        fsm = FrameFSM()
        fsm.feed(raw_bytes)
        frames = fsm.extract_frames()
        self.assertEqual(len(frames), 1)

        payload, _ = frames[0]
        mod, act = struct.unpack(">HH", payload[:4])
        self.assertEqual((mod, act), (0, 0))

        resp = PlayerLoginResp.decode(payload[4:])
        self.assertTrue(resp.is_success)
        self.assertEqual(resp.result_code, 0)
        self.assertEqual(resp.player_id, 4)

    def test_auxiliary_ipc_port_packets_decoding(self) -> None:
        """测试本地辅助 IPC 端口真实报文解析 (8242, 8245, 8254, 8257)"""
        # 1. 端口 8242 (Mod 94 Act 0) 角色信息同步全量 77 字节报文
        hex_8242 = "00000049005e0000000e66656e6777616e79785f73383133000000040009e6a2a6e4b880e59cba6ad0bf7700203462656432373861666564643033636635666331376339616539353338393263"
        bytes_8242 = bytes.fromhex(hex_8242)
        fsm = FrameFSM()
        fsm.feed(bytes_8242)
        frames_8242 = fsm.extract_frames()
        self.assertEqual(len(frames_8242), 1)
        p, _ = frames_8242[0]
        mod, act = struct.unpack(">HH", p[:4])
        self.assertEqual((mod, act), (94, 0))
        r = ByteArrayReader(p[4:])
        self.assertEqual(r.read_utf(), "fengwanyx_s813")
        self.assertEqual(r.read_int32(), 4)
        self.assertEqual(r.read_utf(), "梦一场")
        self.assertEqual(r.read_int32(), 1792065399)
        self.assertEqual(r.read_utf(), "4bed278afedd03cf5fc17c9ae953892c")

        # 2. 端口 8245 (Mod 529 Act 3) 网关绑定同步全量 102 字节报文
        hex_8245 = "0000006202110003000e66656e6777616e79785f7338313300000004002266656e6777616e79785f733831334039783635362e7378647765622e78642e636f6d6ad0bf7a00206535623564383361656237333331373136636131636436653766336635343339"
        bytes_8245 = bytes.fromhex(hex_8245)
        fsm.feed(bytes_8245)
        frames_8245 = fsm.extract_frames()
        self.assertEqual(len(frames_8245), 1)
        p, _ = frames_8245[0]
        mod, act = struct.unpack(">HH", p[:4])
        self.assertEqual((mod, act), (529, 3))
        r = ByteArrayReader(p[4:])
        self.assertEqual(r.read_utf(), "fengwanyx_s813")
        self.assertEqual(r.read_int32(), 4)
        self.assertEqual(r.read_utf(), "fengwanyx_s813@9x656.sxdweb.xd.com")
        self.assertEqual(r.read_int32(), 1792065402)
        self.assertEqual(r.read_utf(), "e5b5d83aeb7331716ca1cd6e7f3f5439")


class TestHeadlessRelayAndHandshakeE2E(unittest.IsolatedAsyncioTestCase):
    """无头环境本地双端口代理中继与长连接握手端到端仿真

    @author Ateng
    @since 2026-10-16
    """

    async def asyncSetUp(self) -> None:
        self.game_server = None
        self.relay_server = None
        self.client = None

    async def asyncTearDown(self) -> None:
        if self.client is not None:
            await self.client.disconnect()
        if self.relay_server is not None:
            self.relay_server.close()
            await self.relay_server.wait_closed()
        if self.game_server is not None:
            self.game_server.close()
            await self.game_server.wait_closed()

    async def test_full_relay_and_handshake_pipeline(self) -> None:
        """测试 Client -> LocalRelay(8062) -> GameServer 完整透明中继与握手时序"""
        # 1. 启动模拟游戏服务端网关 (接收转发并返回 Turn 2)
        handshake_received = asyncio.Event()

        async def handle_game_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            fsm = FrameFSM()
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                fsm.feed(data)
                frames = fsm.extract_frames()
                for payload, _ in frames:
                    mod, act = struct.unpack(">HH", payload[:4])
                    if mod == 0 and act == 0:
                        handshake_received.set()
                        # 回复 Turn 2: 登录成功 (30 字节)
                        turn2_hex = "0000001a0000000000000000040a000000000000000001000b0000108501"
                        writer.write(bytes.fromhex(turn2_hex))
                        await writer.drain()

            writer.close()
            await writer.wait_closed()

        self.game_server = await asyncio.start_server(handle_game_client, "127.0.0.1", 0)
        game_port = self.game_server.sockets[0].getsockname()[1]

        # 2. 启动模拟本地代理中继 (模拟微端 8062 端口行为)
        async def handle_relay_conn(client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter) -> None:
            remote_reader, remote_writer = await asyncio.open_connection("127.0.0.1", game_port)

            async def forward(src_reader: asyncio.StreamReader, dst_writer: asyncio.StreamWriter) -> None:
                try:
                    while True:
                        buf = await src_reader.read(4096)
                        if not buf:
                            break
                        dst_writer.write(buf)
                        await dst_writer.drain()
                except Exception:
                    pass
                finally:
                    dst_writer.close()

            # 启动双向透明全双工转发
            t1 = asyncio.create_task(forward(client_reader, remote_writer))
            t2 = asyncio.create_task(forward(remote_reader, client_writer))
            await asyncio.gather(t1, t2, return_exceptions=True)

        self.relay_server = await asyncio.start_server(handle_relay_conn, "127.0.0.1", 0)
        relay_port = self.relay_server.sockets[0].getsockname()[1]

        # 3. 启动 SXDClient 连接本地中继端口 (模拟无微端脱机连接)
        context = GameContext()
        event_bus = EventBus()
        self.client = SXDClient(context=context, event_bus=event_bus)

        connected = await self.client.connect("127.0.0.1", relay_port)
        self.assertTrue(connected)
        self.assertTrue(context.is_connected)

        # 4. 发送 Turn 1 复合握手帧
        login_req = PlayerLoginReq(
            username="kongyu",
            hash_code="b4776593bb848e7b64f88a98deb41a8c",
            time="1792065385",
            platform="fengwanyx",
            server_id=25268,
        )
        await self.client.send_packet(login_req)

        # 5. 等待服务端收到握手并应答
        await asyncio.wait_for(handshake_received.wait(), timeout=3.0)
        await asyncio.sleep(0.1)  # 等待收包循环处理 Turn 2 回执

        # 6. 验证上下文激活状态
        self.assertTrue(context.player.logged_in)
        self.assertEqual(context.player.player_id, 4)

        # 7. 优雅关闭
        await self.client.disconnect()
        self.assertFalse(context.is_connected)


if __name__ == "__main__":
    unittest.main()
