"""领取奖励一键领取、周末狂欢抽取奖励与药园果园一体化单元测试套件

测试覆盖：
1. 【领取奖励】大厅 Mod 2 Act 6 (16位标准数组反序列化) 与 Act 29 超级礼包全量收割
2. 【周末狂欢】Mod 637 Act 0 面板同步与 Act 1 周六/周日/周一狂欢礼抽取奖励
3. 【我的药园】Mod 13 Act 0 经典土地巡检、伙伴匹配与经验仙草播种/收获
4. 【果园仙树】Mod 135 FairyTree 仙树铜钱与经验免费采摘闭环
严格遵循零元宝安全红线与 Clean Code 规范。

@author Ateng
@since 2026-10-17
"""

import unittest
from unittest.mock import AsyncMock, MagicMock
from core.context import GameContext
from network.client import SXDClient
from tasks.base import TaskStatus
from tasks.routine.take_award import TakeAwardTask
from tasks.routine.weekend import WeekendRevelryTask
from tasks.routine.farm import FarmTask
from protocol.packet import ByteArrayWriter


class TestAwardWeekendAndFarm(unittest.IsolatedAsyncioTestCase):
    """【领取奖励】一键领取、周末狂欢抽取与药园果园自动化测试

    @author Ateng
    @since 2026-10-17
    """

    def setUp(self) -> None:
        self.ctx = GameContext()
        self.ctx.set_connected(True)
        self.ctx.update_player_info(
            nickname="梦一场",
            player_id=4,
            level=300,
            coins=36800000000,
            ingots=39666,
            power=100,
            fame=50000,
            vip_level=10,
            town_id=29,
        )
        self.client = MagicMock(spec=SXDClient)

    async def test_take_award_uint16_array_decoding(self) -> None:
        """测试【领取奖励】标准 16 位数组反序列化并调用 Act 29 一键领取全部礼包"""
        task = TakeAwardTask()

        # 构造 Mod 2 Act 6 官方 16 位数组载荷 (3 个超级大礼包: 22115, 22116, 22117)
        writer = ByteArrayWriter()
        writer.write_uint16(3)  # 3 个礼包 (16位计数)

        # 礼包 1: 竞技场奖励
        writer.write_int32(22115).write_int32(1).write_utf("竞技场结算").write_utf("竞技场每日排名")
        writer.write_uint16(1).write_uint8(1).write_int32(101).write_int32(2000000)

        # 礼包 2: 周排行榜
        writer.write_int32(22116).write_int32(1).write_utf("周排行榜").write_utf("周声望奖励")
        writer.write_uint16(1).write_uint8(1).write_int32(102).write_int32(100000)

        # 礼包 3: 封印妖魔
        writer.write_int32(22117).write_int32(1).write_utf("封印妖魔").write_utf("妖魔击退")
        writer.write_uint16(0)  # 0 项内层道具

        gift_payload = writer.to_bytes()

        claimed_ids = []

        async def mock_req(packet, timeout_sec=2.0):
            if packet.mod == 2 and packet.act == 6:
                return gift_payload
            if packet.mod == 2 and packet.act == 29:
                from protocol.packet import ByteArrayReader
                reader = ByteArrayReader(packet.payload)
                gid = reader.read_int32()
                claimed_ids.append(gid)
                return bytes([161])  # SUCCESS
            if packet.mod == 127 and packet.act == 1:
                return b"\x00" * 4
            return b""

        self.client.request = AsyncMock(side_effect=mock_req)
        self.client.send_packet = AsyncMock()

        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertEqual(result.data["claimed_gifts"], 3)
        self.assertEqual(claimed_ids, [22115, 22116, 22117])

    async def test_weekend_revelry_prize_draw(self) -> None:
        """测试【周末狂欢】周六/周日抽取奖励流水线"""
        task = WeekendRevelryTask()

        # 模拟 Mod 637 Act 0 面板载荷 (58 字节标准结构)
        writer = ByteArrayWriter()
        writer.write_int32(1)   # cur_day = 1
        writer.write_uint16(3)  # 3 个档位
        # 档位 1: 周六狂欢礼 (pid=1, status=1 可领, need_ingot=0, pool_id=101)
        writer.write_int32(1).write_int32(1).write_int32(0).write_int32(101)
        # 档位 2: 周日狂欢礼 (pid=2, status=0 未到期, need_ingot=0, pool_id=102)
        writer.write_int32(2).write_int32(0).write_int32(0).write_int32(102)
        # 档位 3: 周一助力礼 (pid=3, status=0 未到期, need_ingot=0, pool_id=103)
        writer.write_int32(3).write_int32(0).write_int32(0).write_int32(103)
        writer.write_int32(0)
        panel_payload = writer.to_bytes()

        drawn_packs = []

        async def mock_req(packet, timeout_sec=2.0):
            if packet.mod == 637 and packet.act == 0:
                return panel_payload
            if packet.mod == 637 and packet.act == 1:
                from protocol.packet import ByteArrayReader
                reader = ByteArrayReader(packet.payload)
                pid = reader.read_int32()
                drawn_packs.append(pid)
                # 若是周六档位则返回 SUCCESS=0，其它返回 DAY_ERROR=4
                if pid == 1:
                    return bytes([0])
                return bytes([4])
            if packet.mod == 638 and packet.act == 0:
                return b""
            if packet.mod == 242 and packet.act == 1:
                return b"\x00" * 4
            if packet.mod == 242 and packet.act == 2:
                return bytes([3])  # TIME_USE
            if packet.mod == 644 and packet.act == 0:
                return b"\x00" * 4
            if packet.mod == 644 and packet.act == 1:
                return bytes([0])
            return b""

        self.client.request = AsyncMock(side_effect=mock_req)
        self.client.send_packet = AsyncMock()

        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertGreaterEqual(result.data["claimed_packs"], 1)
        self.assertIn(1, drawn_packs)

    async def test_farm_classic_and_orchard_fairy_tree(self) -> None:
        """测试【我的药园】经典土地收获补种与【果园】仙树免费采摘"""
        task = FarmTask()

        # 1. 构造 Mod 13 Act 0 经典土地载荷 (2 块土地: 1 块成熟待收，1 块空地待播)
        w_c = ByteArrayWriter()
        w_c.write_uint16(2)
        # 土地 1: 成熟待收 (lid=1, rid=1001, is_plant=1, grow_time=0)
        w_c.write_int32(1).write_int32(1001).write_utf("后羿").write_utf("金线草")
        w_c.write_int32(2).write_int64(100000).write_int64(0).write_int32(0).write_int32(12345).write_int32(1)
        w_c.write_uint8(1).write_uint8(1).write_int8(0)
        # 土地 2: 空地待播 (lid=2, rid=0, is_plant=0, grow_time=0)
        w_c.write_int32(2).write_int32(0).write_utf("").write_utf("")
        w_c.write_int32(0).write_int64(0).write_int64(0).write_int32(0).write_int32(0).write_int32(0)
        w_c.write_uint8(0).write_uint8(1).write_int8(0)
        classic_lands_payload = w_c.to_bytes()

        # 2. 构造 Mod 13 Act 1 伙伴列表 (伙伴 1002 飞卫，等级 290 < 主角 300)
        w_r = ByteArrayWriter()
        w_r.write_uint16(1)
        w_r.write_int32(1002).write_utf("飞卫").write_utf("飞羽").write_int32(290)
        w_r.write_bytes(b"\x00" * 29)
        roles_payload = w_r.to_bytes()

        actions_recorded = []

        async def mock_farm_req(packet, timeout_sec=2.0):
            actions_recorded.append((packet.mod, packet.act))
            # 经典药园
            if packet.mod == 13 and packet.act == 0:
                return classic_lands_payload
            if packet.mod == 13 and packet.act == 1:
                return roles_payload
            if packet.mod == 13 and packet.act == 6:  # harvest
                return bytes([8])
            if packet.mod == 13 and packet.act == 5:  # plant
                return bytes([8])
            # 新版药园跳过
            if packet.mod == 13 and packet.act == 21:
                return b""
            # 果园仙树 Mod 135
            if packet.mod == 135 and packet.act == 0:  # is_open
                return bytes([0])
            if packet.mod == 135 and packet.act == 3:  # coin
                return bytes([2])
            if packet.mod == 135 and packet.act == 4:  # expr
                return bytes([2])
            # 仙令礼包与摇钱树
            if packet.mod == 13 and packet.act == 19:
                return bytes([1])
            if packet.mod == 13 and packet.act == 20:
                return bytes([0, 1])
            if packet.mod == 13 and packet.act == 12:
                # used=0, free=1
                return (0).to_bytes(4, "big") + (1).to_bytes(4, "big") + (0).to_bytes(8, "big")
            if packet.mod == 13 and packet.act == 13:
                return bytes([8])
            return b""

        self.client.request = AsyncMock(side_effect=mock_farm_req)

        result = await task.execute(self.client, self.ctx)
        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertEqual(result.data["harvested_count"], 1)
        # 地块 1 收获后变为空闲，与原空地 2 一并即时补种 (planted_count=2)
        self.assertEqual(result.data["planted_count"], 2)
        self.assertEqual(result.data["fairy_tree_count"], 2)
        self.assertTrue(result.data["xianling_claimed"])

        # 验证经典药园与仙树关键指令均已下发
        self.assertIn((13, 6), actions_recorded)   # harvest
        self.assertIn((13, 5), actions_recorded)   # plant
        self.assertIn((135, 3), actions_recorded)  # fairy tree coin
        self.assertIn((135, 4), actions_recorded)  # fairy tree expr

    async def test_farm_coin_tree_auto_fallback_when_max_level(self) -> None:
        """测试【药园智能自适应】当伙伴全员满级时，自动从经验树切为发财树 (herbs_type=3)"""
        task = FarmTask(plant_type="auto")

        # 1 块空闲土地 (lid=1)
        w_c = ByteArrayWriter()
        w_c.write_uint16(1)
        w_c.write_int32(1).write_int32(0).write_utf("").write_utf("")
        w_c.write_int32(0).write_int64(0).write_int64(0).write_int32(0).write_int32(0).write_int32(0)
        w_c.write_uint8(0).write_uint8(1).write_int8(0)
        # 尾部: dew_count=0, max_lands=1
        w_c.write_int32(0).write_int32(1)
        lands_payload = w_c.to_bytes()

        # 伙伴列表：全部已达主角 300 级 (无待培养伙伴)
        w_r = ByteArrayWriter()
        w_r.write_uint16(2)
        w_r.write_int32(2001).write_utf("魔莫邪").write_utf("剑灵").write_int32(300)
        w_r.write_bytes(b"\x00" * 29)
        w_r.write_int32(2002).write_utf("后羿").write_utf("飞羽").write_int32(300)
        w_r.write_bytes(b"\x00" * 29)
        roles_payload = w_r.to_bytes()

        planted_packets = []

        async def mock_req(packet, timeout_sec=2.0):
            if packet.mod == 13 and packet.act == 0:
                return lands_payload
            if packet.mod == 13 and packet.act == 1:
                return roles_payload
            if packet.mod == 13 and packet.act == 5:
                from protocol.packet import ByteArrayReader
                r = ByteArrayReader(packet.payload)
                lid = r.read_int32()
                rid = r.read_int32()
                htype = r.read_uint8()
                is_double = r.read_int8()
                planted_packets.append((lid, rid, htype, is_double))
                return bytes([8])
            return b""

        self.client.request = AsyncMock(side_effect=mock_req)
        result = await task.execute(self.client, self.ctx)

        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertEqual(result.data["planted_count"], 1)
        self.assertIn("发财树", result.data["plant_type_desc"])
        self.assertEqual(len(planted_packets), 1)
        # 验证发财树: htype=3 (COIN_HERBS), rid=4 (ctx.player_id), is_double=0
        self.assertEqual(planted_packets[0], (1, 4, 3, 0))

    async def test_farm_dew_upgrade_lands_min_level_first(self) -> None:
        """测试【仙露升级土地】按最低等级优先升级且严格遵循零元宝预检与熔断"""
        task = FarmTask()

        # 3 块土地: #1 等级 1, #2 等级 0, #3 等级 0; 仙露存量 = 2
        w_c = ByteArrayWriter()
        w_c.write_uint16(3)
        # 土地 1: level=1, 已播种待长
        w_c.write_int32(1).write_int32(101).write_utf("").write_utf("")
        w_c.write_int32(2).write_int64(0).write_int64(0).write_int32(999).write_int32(0).write_int32(0)
        w_c.write_uint8(1).write_uint8(1).write_int8(0)
        # 土地 2: level=0, 已播种待长
        w_c.write_int32(2).write_int32(101).write_utf("").write_utf("")
        w_c.write_int32(2).write_int64(0).write_int64(0).write_int32(999).write_int32(0).write_int32(0)
        w_c.write_uint8(1).write_uint8(0).write_int8(0)
        # 土地 3: level=0, 已播种待长
        w_c.write_int32(3).write_int32(101).write_utf("").write_utf("")
        w_c.write_int32(2).write_int64(0).write_int64(0).write_int32(999).write_int32(0).write_int32(0)
        w_c.write_uint8(1).write_uint8(0).write_int8(0)
        # 尾部: dew_count=2
        w_c.write_int32(2).write_int32(3)
        lands_payload = w_c.to_bytes()

        upgraded_lands = []

        async def mock_req(packet, timeout_sec=2.0):
            if packet.mod == 13 and packet.act == 0:
                return lands_payload
            if packet.mod == 13 and packet.act == 15:  # ingot_for_farmland
                # 需 0 元宝
                return (0).to_bytes(4, "big")
            if packet.mod == 13 and packet.act == 16:  # up_farmland_level
                from protocol.packet import ByteArrayReader
                r = ByteArrayReader(packet.payload)
                lid = r.read_int32()
                upgraded_lands.append(lid)
                return bytes([8])  # SUCCESS
            return b""

        self.client.request = AsyncMock(side_effect=mock_req)
        result = await task.execute(self.client, self.ctx)

        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertEqual(result.data["upgraded_lands_count"], 2)
        # 仙露有 2 滴，优先升 0 级的土地 #2 和 #3，绝不优先升 1 级的土地 #1
        self.assertEqual(upgraded_lands, [2, 3])

    async def test_farm_dew_upgrade_zero_ingot_circuit_breaker(self) -> None:
        """测试【仙露升级土地】当预检需要消耗元宝时，立即触发熔断绝不扣除元宝"""
        task = FarmTask()

        w_c = ByteArrayWriter()
        w_c.write_uint16(1)
        w_c.write_int32(1).write_int32(0).write_utf("").write_utf("")
        w_c.write_int32(0).write_int64(0).write_int64(0).write_int32(0).write_int32(0).write_int32(0)
        w_c.write_uint8(0).write_uint8(0).write_int8(0)
        w_c.write_int32(1).write_int32(1)  # dew=1
        lands_payload = w_c.to_bytes()

        actions_sent = []

        async def mock_req(packet, timeout_sec=2.0):
            actions_sent.append((packet.mod, packet.act))
            if packet.mod == 13 and packet.act == 0:
                return lands_payload
            if packet.mod == 13 and packet.act == 15:
                # 返回需要消耗 100 元宝
                return (100).to_bytes(4, "big")
            if packet.mod == 13 and packet.act == 1:
                return (0).to_bytes(2, "big")
            if packet.mod == 13 and packet.act == 5:
                return bytes([8])
            return b""

        self.client.request = AsyncMock(side_effect=mock_req)
        result = await task.execute(self.client, self.ctx)

        self.assertEqual(result.status, TaskStatus.SUCCESS)
        self.assertEqual(result.data["upgraded_lands_count"], 0)
        # 验证因为元宝 > 0，坚决未下发 Act 16 (up_farmland_level)
        self.assertNotIn((13, 16), actions_sent)
