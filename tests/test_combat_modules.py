"""神仙道核心战斗与副本挑战全系模块契约与安全守卫单元测试

验证 Mod 4 (副本), Mod 25 (练功扫荡), Mod 28 (竞技场), Mod 24 (世界 Boss) 的
编解码精确性、免元宝日常流程与 [HAZARDOUS_INGOT] 元宝扣除安全熔断机制。

@author Ateng
@since 2026-10-16
"""

import unittest
from protocol.messages.battle import (
    MissionEnterMissionReq,
    MissionFightMonsterReq,
    MissionFightMonsterResp,
    MissionPracticeGetInfoReq,
    MissionPracticeStartReq,
    MissionPracticeQuicklyReq,
    MissionPracticeCancelReq,
    SuperSportGetChallengeTimesReq,
    SuperSportGetChallengeTimesResp,
    SuperSportGetChallengeListReq,
    SuperSportStartChallengeReq,
    SuperSportBuyChallengeTimesReq,
    SuperSportClearCdTimeReq,
    WorldBossGetDataReq,
    WorldBossFightReq,
    WorldBossInspireReq,
    WorldBossIngotInspireReq,
)


class TestCombatModules(unittest.TestCase):
    """测试战斗与副本挑战协议模型与元宝安全熔断守卫

    @author Ateng
    @since 2026-10-16
    """

    def test_mission_enter_and_fight_encode_decode(self) -> None:
        """测试 Mod 4 普通副本关卡进入与怪物挑战请求编解码"""
        enter_req = MissionEnterMissionReq(mission_id=101)
        self.assertEqual(enter_req.mod, 4)
        self.assertEqual(enter_req.act, 1)
        encoded_enter = enter_req.encode_payload()
        decoded_enter = MissionEnterMissionReq.decode(encoded_enter)
        self.assertEqual(decoded_enter.mission_id, 101)

        fight_req = MissionFightMonsterReq(mission_id=101, monster_team_id=2001)
        self.assertEqual(fight_req.mod, 4)
        self.assertEqual(fight_req.act, 2)
        encoded_fight = fight_req.encode_payload()
        decoded_fight = MissionFightMonsterReq.decode(encoded_fight)
        self.assertEqual(decoded_fight.mission_id, 101)
        self.assertEqual(decoded_fight.monster_team_id, 2001)

    def test_mission_fight_monster_resp_decode(self) -> None:
        """测试 Mod 4 副本怪物战斗结算应答编解码"""
        resp = MissionFightMonsterResp(
            result_code=0,
            is_win=True,
            exp_gain=125000,
            coins_gain=3200,
        )
        encoded = resp.encode_payload()
        decoded = MissionFightMonsterResp.decode(encoded)
        self.assertEqual(decoded.result_code, 0)
        self.assertTrue(decoded.is_win)
        self.assertEqual(decoded.exp_gain, 125000)
        self.assertEqual(decoded.coins_gain, 3200)

    def test_mission_practice_routine_free_flow(self) -> None:
        """测试 Mod 25 免元宝极速秒扫荡全流程契约"""
        info_req = MissionPracticeGetInfoReq(mission_id=88)
        self.assertEqual(info_req.mod, 25)
        self.assertEqual(info_req.act, 0)
        decoded_info = MissionPracticeGetInfoReq.decode(info_req.encode_payload())
        self.assertEqual(decoded_info.mission_id, 88)

        # 全额体力扫荡 (count=0, auto_sale=1)
        start_req = MissionPracticeStartReq(mission_id=88, count=0, auto_sale=1)
        self.assertEqual(start_req.mod, 25)
        self.assertEqual(start_req.act, 1)
        decoded_start = MissionPracticeStartReq.decode(start_req.encode_payload())
        self.assertEqual(decoded_start.mission_id, 88)
        self.assertEqual(decoded_start.count, 0)
        self.assertEqual(decoded_start.auto_sale, 1)

        # 官方微端免费秒完成特权 (times=0)
        quick_req = MissionPracticeQuicklyReq(times=0)
        self.assertEqual(quick_req.mod, 25)
        self.assertEqual(quick_req.act, 3)
        decoded_quick = MissionPracticeQuicklyReq.decode(quick_req.encode_payload())
        self.assertEqual(decoded_quick.times, 0)

        cancel_req = MissionPracticeCancelReq()
        self.assertEqual(cancel_req.mod, 25)
        self.assertEqual(cancel_req.act, 2)
        self.assertEqual(cancel_req.encode_payload(), b"")

    def test_supersport_routine_free_and_ranking_flow(self) -> None:
        """测试 Mod 28 竞技场免费次数查询与对手挑战请求"""
        times_req = SuperSportGetChallengeTimesReq()
        self.assertEqual(times_req.mod, 28)
        self.assertEqual(times_req.act, 13)

        times_resp = SuperSportGetChallengeTimesResp(free_times=15)
        decoded_times = SuperSportGetChallengeTimesResp.decode(times_resp.encode_payload())
        self.assertEqual(decoded_times.free_times, 15)

        list_req = SuperSportGetChallengeListReq()
        self.assertEqual(list_req.mod, 28)
        self.assertEqual(list_req.act, 1)

        challenge_req = SuperSportStartChallengeReq(player_id=123456)
        self.assertEqual(challenge_req.mod, 28)
        self.assertEqual(challenge_req.act, 2)
        decoded_challenge = SuperSportStartChallengeReq.decode(challenge_req.encode_payload())
        self.assertEqual(decoded_challenge.player_id, 123456)

    def test_supersport_hazardous_ingot_guardrails(self) -> None:
        """测试 Mod 28 元宝购买挑战次数与秒 CD 触发 [HAZARDOUS_INGOT] 安全熔断"""
        # 默认未经授权购买挑战次数 -> 必须触发 PermissionError 熔断
        with self.assertRaises(PermissionError) as ctx1:
            SuperSportBuyChallengeTimesReq(times=5)
        self.assertIn("[HAZARDOUS_INGOT]", str(ctx1.exception))
        self.assertIn("buy_challenge_times", str(ctx1.exception))

        # 显式授权后正常构造与编解码
        req_buy_allowed = SuperSportBuyChallengeTimesReq(times=5, allow_ingot=True)
        self.assertEqual(req_buy_allowed.times, 5)
        self.assertTrue(req_buy_allowed.allow_ingot)
        decoded_buy = SuperSportBuyChallengeTimesReq.decode(req_buy_allowed.encode_payload())
        self.assertEqual(decoded_buy.times, 5)
        self.assertTrue(decoded_buy.allow_ingot)

        # 默认未经授权清除 CD -> 必须触发 PermissionError 熔断
        with self.assertRaises(PermissionError) as ctx2:
            SuperSportClearCdTimeReq()
        self.assertIn("[HAZARDOUS_INGOT]", str(ctx2.exception))
        self.assertIn("clear_cd_time", str(ctx2.exception))

        # 显式授权后正常构造与编解码
        req_cd_allowed = SuperSportClearCdTimeReq(allow_ingot=True)
        self.assertTrue(req_cd_allowed.allow_ingot)
        decoded_cd = SuperSportClearCdTimeReq.decode(req_cd_allowed.encode_payload())
        self.assertTrue(decoded_cd.allow_ingot)

    def test_world_boss_routine_free_and_ingot_guardrails(self) -> None:
        """测试 Mod 24 世界 Boss 阅历免费鼓舞与元宝鼓舞安全熔断"""
        # 安全查询
        data_req = WorldBossGetDataReq(boss_id=1)
        self.assertEqual(data_req.mod, 24)
        self.assertEqual(data_req.act, 1)
        decoded_data = WorldBossGetDataReq.decode(data_req.encode_payload())
        self.assertEqual(decoded_data.boss_id, 1)

        # 发起进攻
        fight_req = WorldBossFightReq(boss_id=1)
        self.assertEqual(fight_req.mod, 24)
        self.assertEqual(fight_req.act, 2)
        decoded_fight = WorldBossFightReq.decode(fight_req.encode_payload())
        self.assertEqual(decoded_fight.boss_id, 1)

        # 阅历免费鼓舞
        free_inspire = WorldBossInspireReq(boss_id=1)
        self.assertEqual(free_inspire.mod, 24)
        self.assertEqual(free_inspire.act, 4)
        decoded_free = WorldBossInspireReq.decode(free_inspire.encode_payload())
        self.assertEqual(decoded_free.boss_id, 1)

        # 元宝鼓舞熔断拦截
        with self.assertRaises(PermissionError) as ctx:
            WorldBossIngotInspireReq(boss_id=1)
        self.assertIn("[HAZARDOUS_INGOT]", str(ctx.exception))
        self.assertIn("ingot_inspire", str(ctx.exception))

        # 显式授权元宝鼓舞
        allowed_inspire = WorldBossIngotInspireReq(boss_id=1, allow_ingot=True)
        self.assertEqual(allowed_inspire.boss_id, 1)
        self.assertTrue(allowed_inspire.allow_ingot)
        decoded_ingot = WorldBossIngotInspireReq.decode(allowed_inspire.encode_payload())
        self.assertEqual(decoded_ingot.boss_id, 1)
        self.assertTrue(decoded_ingot.allow_ingot)


if __name__ == "__main__":
    unittest.main()
