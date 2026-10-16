"""神仙道高频日常福利与资源运转全系模块契约与真实抓包还原测试套件

测试覆盖:
1. Mod 13 仙府药园常规播种、收获及摇钱树 [HAZARDOUS_INGOT] 元宝熔断
2. Mod 22 猎命系统命格拾取、变卖灰命、穿戴及扩包 [HAZARDOUS_INGOT] 元宝熔断
3. Mod 30 西天取经常规护送、打劫及加速到达/召唤如来 [HAZARDOUS_INGOT] 元宝熔断
4. Mod 21 仙履奇缘每日答题及清除 CD [HAZARDOUS_INGOT] 元宝熔断
5. Mod 38 吉星高照骰子投掷及付费改运 [HAZARDOUS_INGOT] 元宝熔断
6. Mod 41 帮派祭神白檀香免费放行与苏合香/天木香 [HAZARDOUS_INGOT] 元宝熔断
7. Mod 76 仙女献舞/共舞福利领取
8. 基于 2026-10-15 真实微端进程抓包数据的 12 组报文帧深度还原与一致性校验

@author Ateng
@since 2026-10-16
"""

import struct
import unittest
from protocol.frame import FrameFSM
from protocol.messages.routine import (
    FarmGetFarmlandInfoListReq,
    FarmGetPlayerRoleInfoListReq,
    FarmPlantHerbsReq,
    FarmHarvestReq,
    FarmHarvestResp,
    FarmGetXianLingGiftReq,
    FarmBuyCoinTreeReq,
    FateGetFateNpcReq,
    FateGetTempFateReq,
    FatePickupFateReq,
    FateSaleTempFateReq,
    FateGetBagListReq,
    FateGetRoleFateListReq,
    FateWearOnReq,
    FateAppointFateNpcReq,
    FateBuyBagGridReq,
    TakeBibleOpenReq,
    TakeBibleGetInfoReq,
    TakeBibleRefreshReq,
    TakeBibleStartReq,
    TakeBibleRobReq,
    TakeBibleQuicklyReq,
    TakeBibleCallRuLaiReq,
    TravelEventGetInfoReq,
    TravelEventGetQuestionReq,
    TravelEventAnswerReq,
    TravelEventCancelCdReq,
    RollCakeGetCountReq,
    RollCakeRollReq,
    RollCakeGetAwardReq,
    RollCakeRerollReq,
    WorshipMarsInfoReq,
    WorshipMarsRemainTimesReq,
    WorshipMarsIncenseReq,
    DanceGetInfoReq,
    DanceStartReq,
    DanceReceiveAwardReq,
)


class TestRoutineModules(unittest.TestCase):
    """测试日常福利全系模块数据契约与元宝熔断防御

    @author Ateng
    @since 2026-10-16
    """

    def test_farm_routine_and_ingot_guardrails(self) -> None:
        """测试 Mod 13 仙府药园常规流转与摇钱树元宝拦截"""
        # 1. 常规请求与应答编解码
        list_req = FarmGetFarmlandInfoListReq()
        self.assertEqual((list_req.mod, list_req.act), (13, 0))

        role_req = FarmGetPlayerRoleInfoListReq()
        self.assertEqual((role_req.mod, role_req.act), (13, 1))

        plant_req = FarmPlantHerbsReq(farmland_id=2, role_id=1001, herbs_type=1)
        self.assertEqual((plant_req.mod, plant_req.act), (13, 5))
        decoded_plant = FarmPlantHerbsReq.decode(plant_req.encode_payload())
        self.assertEqual(decoded_plant.farmland_id, 2)
        self.assertEqual(decoded_plant.role_id, 1001)
        self.assertEqual(decoded_plant.herbs_type, 1)

        harvest_req = FarmHarvestReq(farmland_id=2)
        self.assertEqual((harvest_req.mod, harvest_req.act), (13, 6))
        decoded_harvest = FarmHarvestReq.decode(harvest_req.encode_payload())
        self.assertEqual(decoded_harvest.farmland_id, 2)

        harvest_resp = FarmHarvestResp(result_code=0, gain_exp=88000, gain_coins=50000)
        decoded_resp = FarmHarvestResp.decode(harvest_resp.encode_payload())
        self.assertEqual(decoded_resp.result_code, 0)
        self.assertEqual(decoded_resp.gain_exp, 88000)
        self.assertEqual(decoded_resp.gain_coins, 50000)

        gift_req = FarmGetXianLingGiftReq()
        self.assertEqual((gift_req.mod, gift_req.act), (13, 20))

        # 2. 摇钱树元宝熔断拦截
        with self.assertRaises(PermissionError) as ctx:
            FarmBuyCoinTreeReq(count=5)
        self.assertIn("[HAZARDOUS_INGOT]", str(ctx.exception))
        self.assertIn("buy_coin_tree_count", str(ctx.exception))

        # 3. 显式授权后放行
        allowed_tree = FarmBuyCoinTreeReq(count=5, allow_ingot=True)
        self.assertTrue(allowed_tree.allow_ingot)
        self.assertEqual(allowed_tree.count, 5)

    def test_fate_routine_and_ingot_guardrails(self) -> None:
        """测试 Mod 22 猎命系统命格拾取、变卖与扩充背包熔断"""
        npc_req = FateGetFateNpcReq()
        self.assertEqual((npc_req.mod, npc_req.act), (22, 0))

        temp_req = FateGetTempFateReq()
        self.assertEqual((temp_req.mod, temp_req.act), (22, 1))

        pickup_req = FatePickupFateReq(temp_fate_id=501)
        self.assertEqual((pickup_req.mod, pickup_req.act), (22, 2))
        decoded_pickup = FatePickupFateReq.decode(pickup_req.encode_payload())
        self.assertEqual(decoded_pickup.temp_fate_id, 501)

        sale_req = FateSaleTempFateReq()
        self.assertEqual((sale_req.mod, sale_req.act), (22, 3))

        bag_req = FateGetBagListReq()
        self.assertEqual((bag_req.mod, bag_req.act), (22, 4))

        wear_req = FateWearOnReq(player_role_id=1, fate_id=999, grid_id=3)
        self.assertEqual((wear_req.mod, wear_req.act), (22, 7))
        decoded_wear = FateWearOnReq.decode(wear_req.encode_payload())
        self.assertEqual(decoded_wear.player_role_id, 1)
        self.assertEqual(decoded_wear.fate_id, 999)
        self.assertEqual(decoded_wear.grid_id, 3)

        # 扩充背包格子元宝熔断拦截
        with self.assertRaises(PermissionError) as ctx:
            FateBuyBagGridReq()
        self.assertIn("[HAZARDOUS_INGOT]", str(ctx.exception))
        self.assertIn("buy_bag_grid", str(ctx.exception))

        allowed_bag = FateBuyBagGridReq(allow_ingot=True)
        self.assertTrue(allowed_bag.allow_ingot)

    def test_take_bible_routine_and_ingot_guardrails(self) -> None:
        """测试 Mod 30 西天取经免费启程与元宝秒速/召唤如来熔断"""
        open_req = TakeBibleOpenReq()
        self.assertEqual((open_req.mod, open_req.act), (30, 0))

        info_req = TakeBibleGetInfoReq()
        self.assertEqual((info_req.mod, info_req.act), (30, 2))

        refresh_req = TakeBibleRefreshReq()
        self.assertEqual((refresh_req.mod, refresh_req.act), (30, 12))

        start_req = TakeBibleStartReq()
        self.assertEqual((start_req.mod, start_req.act), (30, 10))

        rob_req = TakeBibleRobReq(target_player_id=7788)
        self.assertEqual((rob_req.mod, rob_req.act), (30, 14))
        decoded_rob = TakeBibleRobReq.decode(rob_req.encode_payload())
        self.assertEqual(decoded_rob.target_player_id, 7788)

        # 秒速到达元宝熔断拦截
        with self.assertRaises(PermissionError) as ctx1:
            TakeBibleQuicklyReq()
        self.assertIn("[HAZARDOUS_INGOT]", str(ctx1.exception))
        self.assertIn("take_bible_quickly", str(ctx1.exception))

        # 召唤如来元宝熔断拦截
        with self.assertRaises(PermissionError) as ctx2:
            TakeBibleCallRuLaiReq()
        self.assertIn("[HAZARDOUS_INGOT]", str(ctx2.exception))
        self.assertIn("call_ru_lai", str(ctx2.exception))

        allowed_quick = TakeBibleQuicklyReq(allow_ingot=True)
        self.assertTrue(allowed_quick.allow_ingot)

        allowed_rulai = TakeBibleCallRuLaiReq(allow_ingot=True)
        self.assertTrue(allowed_rulai.allow_ingot)

    def test_travel_event_routine_and_ingot_guardrails(self) -> None:
        """测试 Mod 21 仙履奇缘答题流转与秒清 CD 元宝拦截"""
        info_req = TravelEventGetInfoReq()
        self.assertEqual((info_req.mod, info_req.act), (21, 0))

        q_req = TravelEventGetQuestionReq()
        self.assertEqual((q_req.mod, q_req.act), (21, 1))

        ans_req = TravelEventAnswerReq(event_id=12, answer_index=0)
        self.assertEqual((ans_req.mod, ans_req.act), (21, 2))
        decoded_ans = TravelEventAnswerReq.decode(ans_req.encode_payload())
        self.assertEqual(decoded_ans.event_id, 12)
        self.assertEqual(decoded_ans.answer_index, 0)

        # 秒清 CD 拦截
        with self.assertRaises(PermissionError) as ctx:
            TravelEventCancelCdReq()
        self.assertIn("[HAZARDOUS_INGOT]", str(ctx.exception))
        self.assertIn("cancel_cd", str(ctx.exception))

        allowed_cd = TravelEventCancelCdReq(allow_ingot=True)
        self.assertTrue(allowed_cd.allow_ingot)

    def test_roll_cake_routine_and_ingot_guardrails(self) -> None:
        """测试 Mod 38 吉星高照骰子投掷与元宝改运熔断"""
        count_req = RollCakeGetCountReq()
        self.assertEqual((count_req.mod, count_req.act), (38, 2))

        roll_req = RollCakeRollReq()
        self.assertEqual((roll_req.mod, roll_req.act), (38, 0))

        award_req = RollCakeGetAwardReq()
        self.assertEqual((award_req.mod, award_req.act), (38, 4))

        # 元宝改运拦截
        with self.assertRaises(PermissionError) as ctx:
            RollCakeRerollReq()
        self.assertIn("[HAZARDOUS_INGOT]", str(ctx.exception))
        self.assertIn("reroll", str(ctx.exception))

        allowed_reroll = RollCakeRerollReq(allow_ingot=True)
        self.assertTrue(allowed_reroll.allow_ingot)

    def test_worship_mars_incense_guardrails(self) -> None:
        """测试 Mod 41 帮派祭神白檀香放行与苏合香/天木香元宝熔断"""
        info_req = WorshipMarsInfoReq()
        self.assertEqual((info_req.mod, info_req.act), (41, 0))

        remain_req = WorshipMarsRemainTimesReq()
        self.assertEqual((remain_req.mod, remain_req.act), (41, 4))

        # 白檀香 (type=1) 零元宝 -> 正常放行
        free_incense = WorshipMarsIncenseReq(incense_type=1)
        self.assertEqual(free_incense.incense_type, 1)
        self.assertFalse(free_incense.allow_ingot)
        self.assertEqual((free_incense.mod, free_incense.act), (41, 1))

        # 苏合香 (type=2, 30 元宝) -> 必须抛出 PermissionError
        with self.assertRaises(PermissionError) as ctx1:
            WorshipMarsIncenseReq(incense_type=2)
        self.assertIn("[HAZARDOUS_INGOT]", str(ctx1.exception))
        self.assertIn("type=2", str(ctx1.exception))

        # 天木香 (type=3, 90 元宝) -> 必须抛出 PermissionError
        with self.assertRaises(PermissionError) as ctx2:
            WorshipMarsIncenseReq(incense_type=3)
        self.assertIn("[HAZARDOUS_INGOT]", str(ctx2.exception))
        self.assertIn("type=3", str(ctx2.exception))

        # 显式授权后可构造苏合香与天木香
        allowed_suhe = WorshipMarsIncenseReq(incense_type=2, allow_ingot=True)
        self.assertEqual(allowed_suhe.incense_type, 2)
        self.assertTrue(allowed_suhe.allow_ingot)

        allowed_tianmu = WorshipMarsIncenseReq(incense_type=3, allow_ingot=True)
        self.assertEqual(allowed_tianmu.incense_type, 3)
        self.assertTrue(allowed_tianmu.allow_ingot)

    def test_dance_welfare_flow(self) -> None:
        """测试 Mod 76 仙女献舞/共舞福利领取契约"""
        info_req = DanceGetInfoReq()
        self.assertEqual((info_req.mod, info_req.act), (76, 0))

        start_req = DanceStartReq()
        self.assertEqual((start_req.mod, start_req.act), (76, 1))

        award_req = DanceReceiveAwardReq()
        self.assertEqual((award_req.mod, award_req.act), (76, 2))


class TestRealWorldPcapRoutineFrames(unittest.TestCase):
    """基于 2026-10-15 真实微端抓包报文的真机还原测试

    @author Ateng
    @since 2026-10-16
    """

    def test_real_farm_frames_from_pcap(self) -> None:
        """测试真实抓包中的药园相关帧 (Mod 13 Act 0, Act 10, Act 19, Act 20)"""
        # Mod 13 Act 0: get_farmlandinfo_list (8 字节帧)
        hex_13_0 = "00000008000d000001b10002"
        fsm = FrameFSM()
        fsm.feed(bytes.fromhex(hex_13_0))
        frames = fsm.extract_frames()
        self.assertEqual(len(frames), 1)
        p, _ = frames[0]
        mod, act = struct.unpack(">HH", p[:4])
        self.assertEqual((mod, act), (13, 0))

        # Mod 13 Act 10: get_simple_farmlandinfo (8 字节帧)
        hex_13_10 = "00000008000d000a00070000"
        fsm.feed(bytes.fromhex(hex_13_10))
        frames = fsm.extract_frames()
        self.assertEqual(len(frames), 1)
        p, _ = frames[0]
        mod, act = struct.unpack(">HH", p[:4])
        self.assertEqual((mod, act), (13, 10))

        # Mod 13 Act 19: is_player_get_xian_ling_gift (8 字节帧)
        hex_13_19 = "00000008000d001300c50001"
        fsm.feed(bytes.fromhex(hex_13_19))
        frames = fsm.extract_frames()
        self.assertEqual(len(frames), 1)
        p, _ = frames[0]
        mod, act = struct.unpack(">HH", p[:4])
        self.assertEqual((mod, act), (13, 19))

        # Mod 13 Act 20: player_get_xian_ling_gift (8 字节帧)
        hex_13_20 = "00000008000d0014002a0011"
        fsm.feed(bytes.fromhex(hex_13_20))
        frames = fsm.extract_frames()
        self.assertEqual(len(frames), 1)
        p, _ = frames[0]
        mod, act = struct.unpack(">HH", p[:4])
        self.assertEqual((mod, act), (13, 20))

    def test_real_travel_and_roll_cake_frames_from_pcap(self) -> None:
        """测试真实抓包中的仙履奇缘与吉星高照帧 (Mod 21 Act 0, Mod 38 Act 2)"""
        # Mod 21 Act 0: get_activity_info (8 字节帧)
        hex_21_0 = "0000000800150000000d000a"
        fsm = FrameFSM()
        fsm.feed(bytes.fromhex(hex_21_0))
        frames = fsm.extract_frames()
        self.assertEqual(len(frames), 1)
        p, _ = frames[0]
        mod, act = struct.unpack(">HH", p[:4])
        self.assertEqual((mod, act), (21, 0))

        # Mod 38 Act 2: get_count (8 字节帧)
        hex_38_2 = "000000080026000200e40000"
        fsm.feed(bytes.fromhex(hex_38_2))
        frames = fsm.extract_frames()
        self.assertEqual(len(frames), 1)
        p, _ = frames[0]
        mod, act = struct.unpack(">HH", p[:4])
        self.assertEqual((mod, act), (38, 2))

    def test_real_fate_and_worship_mars_frames_from_pcap(self) -> None:
        """测试真实抓包中的猎命与祭神帧 (Mod 22 Act 6/30, Mod 41 Act 0/2/4/5)"""
        fsm = FrameFSM()

        # Mod 22 Act 6: get_role_fate_list (12 字节帧)
        hex_22_6 = "0000000c001600060000002000650001"
        fsm.feed(bytes.fromhex(hex_22_6))
        frames = fsm.extract_frames()
        self.assertEqual(len(frames), 1)
        p, _ = frames[0]
        mod, act = struct.unpack(">HH", p[:4])
        self.assertEqual((mod, act), (22, 6))

        # Mod 22 Act 30: get_fate_inn_upgrade_flag (12 字节帧)
        hex_22_30 = "0000000c0016001e000000040002002b"
        fsm.feed(bytes.fromhex(hex_22_30))
        frames = fsm.extract_frames()
        self.assertEqual(len(frames), 1)
        p, _ = frames[0]
        mod, act = struct.unpack(">HH", p[:4])
        self.assertEqual((mod, act), (22, 30))

        # Mod 41 Act 0: mars_info (8 字节帧)
        hex_41_0 = "000000080029000002700001"
        fsm.feed(bytes.fromhex(hex_41_0))
        frames = fsm.extract_frames()
        self.assertEqual(len(frames), 1)
        p, _ = frames[0]
        mod, act = struct.unpack(">HH", p[:4])
        self.assertEqual((mod, act), (41, 0))

        # Mod 41 Act 4: get_remain_incense_times (8 字节帧)
        hex_41_4 = "00000008002900040088000a"
        fsm.feed(bytes.fromhex(hex_41_4))
        frames = fsm.extract_frames()
        self.assertEqual(len(frames), 1)
        p, _ = frames[0]
        mod, act = struct.unpack(">HH", p[:4])
        self.assertEqual((mod, act), (41, 4))


if __name__ == "__main__":
    unittest.main()
