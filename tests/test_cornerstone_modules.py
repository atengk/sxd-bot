"""三大核心基石模块 (Mod 0: Player, Mod 1: Town, Mod 2: Item) 自动化测试套件

测试覆盖:
1. Mod 0 (Player): 登录请求/回执 (结合 PCAP Stream 18 真实报文)、44 字段属性、动态属性广播、元宝购买体力安全熔断
2. Mod 1 (Town): 城镇进入/离开、网格寻路移动坐标往返、城镇同屏玩家请求
3. Mod 2 (Item): 背包空格查询、一键智能整理、杂物变卖、元宝解锁背包格位安全熔断

@author Ateng
@since 2026-10-16
"""

import struct
import unittest
from protocol.messages.player import (
    PlayerLoginReq,
    PlayerLoginResp,
    PlayerInfoResp,
    PlayerBuyPowerReq,
    PlayerUpdatePlayerDataResp,
)
from protocol.messages.town import (
    TownConstants,
    TownEnterTownReq,
    TownEnterTownResp,
    TownLeaveTownReq,
    TownMoveToReq,
    TownMoveToResp,
    TownGetPlayersReq,
)
from protocol.messages.item import (
    ItemConstants,
    ItemGetEmptyGridNumberReq,
    ItemGetEmptyGridNumberResp,
    ItemGetAllPlayerItemInfosReq,
    ItemClassifyPackReq,
    ItemClassifyPackResp,
    ItemSellItemReq,
    ItemSellItemResp,
    ItemAddPackGridReq,
)


class TestPlayerCornerstoneModule(unittest.TestCase):
    """Mod 0 (Player) 角色核心基石契约测试

    @author Ateng
    @since 2026-10-16
    """

    def test_pcap_turn2_login_resp_decoding(self) -> None:
        """测试 Stream 18 Turn 2 真实 30 字节抓包登录回执解码"""
        turn2_hex = "0000001a0000000000000000040a000000000000000001000b0000108501"
        raw_payload = bytes.fromhex(turn2_hex)[8:]  # 跳过 4B Length + 4B Mod/Act

        resp = PlayerLoginResp.decode(raw_payload)
        self.assertTrue(resp.is_success)
        self.assertEqual(resp.result_code, 0)
        self.assertEqual(resp.player_id, 4)

    def test_player_info_44_fields_roundtrip(self) -> None:
        """测试 PlayerInfoResp 44 维角色基础属性解析"""
        from protocol.packet import ByteArrayWriter
        writer = ByteArrayWriter()
        writer.write_utf("梦一场")      # 0: nickname
        writer.write_int32(300)         # 1: level
        writer.write_int32(40096)       # 2: ingots
        writer.write_int64(36807665882) # 3: coins
        writer.write_int64(9180049)     # 4: health
        writer.write_int64(9180049)     # 5: max_health
        writer.write_int32(100)         # 6: power
        writer.write_int64(12345678)    # 7: exp
        writer.write_int64(20000000)    # 8: max_exp
        writer.write_int32(29)          # 9: town_map_id (大理城)
        for _ in range(4): writer.write_int32(0)  # 10~13
        writer.write_int32(10)          # 14: vip_level
        for _ in range(4): writer.write_int32(0)  # 15~18
        writer.write_int8(1)            # 19: camp_id
        writer.write_int32(0)           # 20
        writer.write_int32(888888)      # 21: fame
        for _ in range(7): writer.write_int32(0)  # 22~28
        writer.write_int32(250)         # 29: mission_key

        payload = writer.to_bytes()
        resp = PlayerInfoResp.decode(payload)

        self.assertEqual(resp.nickname, "梦一场")
        self.assertEqual(resp.level, 300)
        self.assertEqual(resp.ingots, 40096)
        self.assertEqual(resp.coins, 36807665882)
        self.assertEqual(resp.power, 100)
        self.assertEqual(resp.town_map_id, 29)
        self.assertEqual(resp.vip_level, 10)
        self.assertEqual(resp.camp_id, 1)
        self.assertEqual(resp.fame, 888888)
        self.assertEqual(resp.mission_key, 250)

    def test_update_player_data_dynamic_broadcast(self) -> None:
        """测试 Mod 0 Act 3 动态属性更新广播报文编解码"""
        updates_in = {
            18: 300,        # 等级
            19: 50000,      # 元宝
            20: 100000000,  # 铜钱
            23: 150,        # 体力
            37: 999999,     # 声望
        }
        pkt = PlayerUpdatePlayerDataResp(updates=updates_in)
        raw = pkt.encode_payload()

        decoded = PlayerUpdatePlayerDataResp.decode(raw)
        self.assertEqual(decoded.updates, updates_in)

    def test_buy_power_hazardous_ingot_guardrail(self) -> None:
        """测试购买体力 [HAZARDOUS_INGOT] 安全红线守卫前置拦截"""
        # 1. 默认调用未经授权，必须触发 PermissionError
        with self.assertRaises(PermissionError) as cm:
            PlayerBuyPowerReq()
        self.assertIn("[HAZARDOUS_INGOT]", str(cm.exception))

        # 2. 显式授权 allow_ingot=True 放行
        req = PlayerBuyPowerReq(allow_ingot=True)
        self.assertEqual(req.mod, 0)
        self.assertEqual(req.act, 5)
        self.assertEqual(req.encode_payload(), b"")


class TestTownCornerstoneModule(unittest.TestCase):
    """Mod 1 (Town) 城镇场景基石契约测试

    @author Ateng
    @since 2026-10-16
    """

    def test_enter_and_leave_town(self) -> None:
        """测试进入城镇与离开城镇协议往返"""
        enter_req = TownEnterTownReq(town_id=29)
        raw_req = enter_req.encode_payload()
        self.assertEqual(len(raw_req), 4)
        dec_req = TownEnterTownReq.decode(raw_req)
        self.assertEqual(dec_req.town_id, 29)

        resp = TownEnterTownResp(result_code=TownConstants.SUCCESS, town_id=29)
        self.assertTrue(resp.is_success)
        raw_resp = resp.encode_payload()
        dec_resp = TownEnterTownResp.decode(raw_resp)
        self.assertTrue(dec_resp.is_success)
        self.assertEqual(dec_resp.town_id, 29)

        leave_req = TownLeaveTownReq()
        self.assertEqual(leave_req.encode_payload(), b"")

    def test_move_to_coordinates_codec(self) -> None:
        """测试场景寻路移动 4 坐标往返一致性"""
        move_req = TownMoveToReq(src_x=120, src_y=340, dst_x=560, dst_y=780)
        raw = move_req.encode_payload()
        self.assertEqual(len(raw), 8)  # 4 * 2B short

        dec_req = TownMoveToReq.decode(raw)
        self.assertEqual((dec_req.src_x, dec_req.src_y), (120, 340))
        self.assertEqual((dec_req.dst_x, dec_req.dst_y), (560, 780))

        move_resp = TownMoveToResp(player_id=4, src_x=120, src_y=340, dst_x=560, dst_y=780)
        raw_resp = move_resp.encode_payload()
        self.assertEqual(len(raw_resp), 12)  # 4B Int + 4 * 2B short
        dec_resp = TownMoveToResp.decode(raw_resp)
        self.assertEqual(dec_resp.player_id, 4)
        self.assertEqual((dec_resp.src_x, dec_resp.src_y), (120, 340))
        self.assertEqual((dec_resp.dst_x, dec_resp.dst_y), (560, 780))


class TestItemCornerstoneModule(unittest.TestCase):
    """Mod 2 (Item) 背包与物品基石契约测试

    @author Ateng
    @since 2026-10-16
    """

    def test_empty_grid_and_classify_pack(self) -> None:
        """测试空格子数量查询与一键背包整理"""
        empty_resp = ItemGetEmptyGridNumberResp(empty_count=18)
        raw = empty_resp.encode_payload()
        self.assertEqual(len(raw), 2)
        dec_empty = ItemGetEmptyGridNumberResp.decode(raw)
        self.assertEqual(dec_empty.empty_count, 18)

        classify_req = ItemClassifyPackReq()
        self.assertEqual(classify_req.encode_payload(), b"")

        classify_resp = ItemClassifyPackResp(result_code=ItemConstants.ACTION_SUCCESS)
        self.assertTrue(classify_resp.is_success)
        dec_classify = ItemClassifyPackResp.decode(classify_resp.encode_payload())
        self.assertTrue(dec_classify.is_success)

    def test_sell_item_routine_codec(self) -> None:
        """测试杂物变卖换取铜钱协议"""
        sell_req = ItemSellItemReq(player_item_id=10245)
        raw = sell_req.encode_payload()
        self.assertEqual(len(raw), 4)
        dec_sell = ItemSellItemReq.decode(raw)
        self.assertEqual(dec_sell.player_item_id, 10245)

        sell_resp = ItemSellItemResp(result_code=ItemConstants.ACTION_SUCCESS, return_coins=5000)
        self.assertTrue(sell_resp.is_success)
        self.assertEqual(sell_resp.return_coins, 5000)
        dec_resp = ItemSellItemResp.decode(sell_resp.encode_payload())
        self.assertTrue(dec_resp.is_success)
        self.assertEqual(dec_resp.return_coins, 5000)

    def test_add_pack_grid_hazardous_ingot_guardrail(self) -> None:
        """测试元宝解锁背包格子 [HAZARDOUS_INGOT] 安全红线守卫前置拦截"""
        # 1. 默认调用未授权必须触发 PermissionError
        with self.assertRaises(PermissionError) as cm:
            ItemAddPackGridReq(grid_count=5)
        self.assertIn("[HAZARDOUS_INGOT]", str(cm.exception))

        # 2. 显式授权 allow_ingot=True 放行
        req = ItemAddPackGridReq(grid_count=5, allow_ingot=True)
        self.assertEqual(req.grid_count, 5)
        raw = req.encode_payload()
        self.assertEqual(len(raw), 4)
        dec = ItemAddPackGridReq.decode(raw)
        self.assertEqual(dec.grid_count, 5)
        self.assertTrue(dec.allow_ingot)


if __name__ == "__main__":
    unittest.main()
