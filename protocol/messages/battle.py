"""神仙道核心战斗与副本挑战全系模块数据契约 (Mod 4, 25, 28, 24)

涵盖:
- Mod 4: 普通副本剧情与怪物战斗 (Mod_Mission_Base)
- Mod 25: 副本练功与极速秒扫荡 (Mod_MissionPractice_Base)
- Mod 28: 竞技场天梯冲榜与软柿子对决 (Mod_SuperSport_Base)
- Mod 24: 世界 Boss 定时参战与阅历鼓舞 (Mod_WorldBoss_Base)

严格落实 [SAFE_READ], [ROUTINE_FREE], [HAZARDOUS_INGOT] 三级安全红线守卫。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Any
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter


# ==============================================================================
# Mod 4: 普通副本 (Mod_Mission_Base)
# ==============================================================================

@dataclass
class MissionEnterMissionReq(BasePacket):
    """进入副本关卡请求 (Mod 4, Act 1) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    mission_id: int

    def __init__(self, mission_id: int) -> None:
        super().__init__(mod=4, act=1)
        self.mission_id = mission_id

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.mission_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionEnterMissionReq":
        reader = ByteArrayReader(data)
        mid = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(mission_id=mid)


@dataclass
class MissionFightMonsterReq(BasePacket):
    """发起怪物战斗请求 (Mod 4, Act 2) - [ROUTINE_FREE]

    每次挑战消耗 5 点体力。

    @author Ateng
    @since 2026-10-16
    """

    mission_id: int
    monster_team_id: int

    def __init__(self, mission_id: int, monster_team_id: int) -> None:
        super().__init__(mod=4, act=2)
        self.mission_id = mission_id
        self.monster_team_id = monster_team_id

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.mission_id)
        writer.write_int32(self.monster_team_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionFightMonsterReq":
        reader = ByteArrayReader(data)
        mid = reader.read_int32() if reader.remaining >= 4 else 0
        tid = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(mission_id=mid, monster_team_id=tid)


@dataclass
class MissionFightMonsterResp(BasePacket):
    """怪物战斗结算应答 (Mod 4, Act 2) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    result_code: int
    is_win: bool = False
    exp_gain: int = 0
    coins_gain: int = 0
    raw_payload: bytes = b""

    def __init__(
        self,
        result_code: int,
        is_win: bool = False,
        exp_gain: int = 0,
        coins_gain: int = 0,
        raw_payload: bytes = b"",
    ) -> None:
        super().__init__(mod=4, act=2)
        self.result_code = result_code
        self.is_win = is_win
        self.exp_gain = exp_gain
        self.coins_gain = coins_gain
        self.raw_payload = raw_payload

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.result_code)
        writer.write_bool(self.is_win)
        writer.write_int64(self.exp_gain)
        writer.write_int32(self.coins_gain)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionFightMonsterResp":
        reader = ByteArrayReader(data)
        code = reader.read_uint8() if reader.remaining >= 1 else 1
        win = reader.read_bool() if reader.remaining >= 1 else False
        exp = reader.read_int64() if reader.remaining >= 8 else 0
        coins = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(result_code=code, is_win=win, exp_gain=exp, coins_gain=coins, raw_payload=data)


# ==============================================================================
# Mod 25: 副本练功与极速扫荡 (Mod_MissionPractice_Base)
# ==============================================================================

@dataclass
class MissionPracticeGetInfoReq(BasePacket):
    """查询关卡扫荡信息 (Mod 25, Act 0) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    mission_id: int

    def __init__(self, mission_id: int) -> None:
        super().__init__(mod=25, act=0)
        self.mission_id = mission_id

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.mission_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionPracticeGetInfoReq":
        reader = ByteArrayReader(data)
        mid = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(mission_id=mid)


@dataclass
class MissionPracticeStartReq(BasePacket):
    """启动关卡扫荡请求 (Mod 25, Act 1) - [ROUTINE_FREE]

    count=0 表示一次性全额消耗剩余体力扫荡到底；auto_sale=1 自动变卖杂物。

    @author Ateng
    @since 2026-10-16
    """

    mission_id: int
    count: int = 0
    auto_sale: int = 1

    def __init__(self, mission_id: int, count: int = 0, auto_sale: int = 1) -> None:
        super().__init__(mod=25, act=1)
        self.mission_id = mission_id
        self.count = count
        self.auto_sale = auto_sale

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.mission_id)
        writer.write_uint16(self.count)
        writer.write_uint8(self.auto_sale)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionPracticeStartReq":
        reader = ByteArrayReader(data)
        mid = reader.read_int32() if reader.remaining >= 4 else 0
        cnt = reader.read_uint16() if reader.remaining >= 2 else 0
        sale = reader.read_uint8() if reader.remaining >= 1 else 1
        return cls(mission_id=mid, count=cnt, auto_sale=sale)


@dataclass
class MissionPracticeQuicklyReq(BasePacket):
    """免元宝极速秒完成扫荡 (Mod 25, Act 3) - [ROUTINE_FREE]

    times=0 表示官方微端特权免费秒结算所有剩余轮次。

    @author Ateng
    @since 2026-10-16
    """

    times: int = 0

    def __init__(self, times: int = 0) -> None:
        super().__init__(mod=25, act=3)
        self.times = times

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint16(self.times)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionPracticeQuicklyReq":
        reader = ByteArrayReader(data)
        t = reader.read_uint16() if reader.remaining >= 2 else 0
        return cls(times=t)


@dataclass
class MissionPracticeCancelReq(BasePacket):
    """取消练功扫荡请求 (Mod 25, Act 2) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=25, act=2)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "MissionPracticeCancelReq":
        return cls()


# ==============================================================================
# Mod 28: 竞技场天梯 (Mod_SuperSport_Base)
# ==============================================================================

@dataclass
class SuperSportGetChallengeTimesReq(BasePacket):
    """查询竞技场剩余免费挑战次数 (Mod 28, Act 13) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=28, act=13)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "SuperSportGetChallengeTimesReq":
        return cls()


@dataclass
class SuperSportGetChallengeTimesResp(BasePacket):
    """竞技场剩余挑战次数应答 (Mod 28, Act 13) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    free_times: int

    def __init__(self, free_times: int) -> None:
        super().__init__(mod=28, act=13)
        self.free_times = free_times

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint16(self.free_times)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SuperSportGetChallengeTimesResp":
        reader = ByteArrayReader(data)
        times = reader.read_uint16() if reader.remaining >= 2 else 0
        return cls(free_times=times)


@dataclass
class SuperSportGetChallengeListReq(BasePacket):
    """拉取候选挑战对手列表请求 (Mod 28, Act 1) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=28, act=1)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "SuperSportGetChallengeListReq":
        return cls()


@dataclass
class SuperSportStartChallengeReq(BasePacket):
    """发起竞技场对手挑战 (Mod 28, Act 2) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    player_id: int

    def __init__(self, player_id: int) -> None:
        super().__init__(mod=28, act=2)
        self.player_id = player_id

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.player_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SuperSportStartChallengeReq":
        reader = ByteArrayReader(data)
        pid = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(player_id=pid)


@dataclass
class SuperSportBuyChallengeTimesReq(BasePacket):
    """消耗元宝购买额外竞技场挑战次数 (Mod 28, Act 4) - [HAZARDOUS_INGOT]

    前置安全红线守卫拦截。

    @author Ateng
    @since 2026-10-16
    """

    times: int = 1
    allow_ingot: bool = False

    def __init__(self, times: int = 1, allow_ingot: bool = False) -> None:
        super().__init__(mod=28, act=4)
        if not allow_ingot:
            raise PermissionError("[HAZARDOUS_INGOT] buy_challenge_times 涉及元宝扣除，已触发安全熔断保护！若确认执行请显式设置 allow_ingot=True")
        self.times = times
        self.allow_ingot = allow_ingot

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint16(self.times)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SuperSportBuyChallengeTimesReq":
        reader = ByteArrayReader(data)
        t = reader.read_uint16() if reader.remaining >= 2 else 1
        return cls(times=t, allow_ingot=True)


@dataclass
class SuperSportClearCdTimeReq(BasePacket):
    """消耗元宝秒清竞技场冷却时间 (Mod 28, Act 3) - [HAZARDOUS_INGOT]

    前置安全红线守卫拦截。

    @author Ateng
    @since 2026-10-16
    """

    allow_ingot: bool = False

    def __init__(self, allow_ingot: bool = False) -> None:
        super().__init__(mod=28, act=3)
        if not allow_ingot:
            raise PermissionError("[HAZARDOUS_INGOT] clear_cd_time 涉及元宝扣除，已触发安全熔断保护！若确认执行请显式设置 allow_ingot=True")
        self.allow_ingot = allow_ingot

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "SuperSportClearCdTimeReq":
        return cls(allow_ingot=True)


# ==============================================================================
# Mod 24: 世界 Boss (Mod_WorldBoss_Base)
# ==============================================================================

@dataclass
class WorldBossGetDataReq(BasePacket):
    """获取世界 Boss 战场数据与生命值 (Mod 24, Act 1: get_world_boss_data) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=24, act=1)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "WorldBossGetDataReq":
        return cls()


@dataclass
class WorldBossFightReq(BasePacket):
    """向世界 Boss 发起一次战斗挑战 (Mod 24, Act 2: fight_world_boss) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    boss_type: int = 1

    def __init__(self, boss_type: int = 1) -> None:
        super().__init__(mod=24, act=2)
        self.boss_type = boss_type

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.boss_type)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldBossFightReq":
        reader = ByteArrayReader(data)
        btype = reader.read_uint8() if reader.remaining >= 1 else 1
        return cls(boss_type=btype)


@dataclass
class WorldBossInspireReq(BasePacket):
    """消耗角色阅历免费鼓舞攻击力 (Mod 24, Act 7: strengthen_combat) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    inspire_type: int = 1

    def __init__(self, inspire_type: int = 1) -> None:
        super().__init__(mod=24, act=7)
        self.inspire_type = inspire_type

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.inspire_type)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldBossInspireReq":
        reader = ByteArrayReader(data)
        itype = reader.read_uint8() if reader.remaining >= 1 else 1
        return cls(inspire_type=itype)


@dataclass
class WorldBossIngotInspireReq(BasePacket):
    """消耗元宝 100% 成功直接鼓舞世界 Boss (Mod 24, Act 7: strengthen_combat) - [HAZARDOUS_INGOT]

    前置安全红线守卫拦截。

    @author Ateng
    @since 2026-10-16
    """

    inspire_type: int = 2
    allow_ingot: bool = False

    def __init__(self, inspire_type: int = 2, allow_ingot: bool = False) -> None:
        super().__init__(mod=24, act=7)
        if not allow_ingot:
            raise PermissionError("[HAZARDOUS_INGOT] ingot_inspire 涉及元宝扣除，已触发安全熔断保护！若确认执行请显式设置 allow_ingot=True")
        self.inspire_type = inspire_type
        self.allow_ingot = allow_ingot

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.inspire_type)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldBossIngotInspireReq":
        reader = ByteArrayReader(data)
        itype = reader.read_uint8() if reader.remaining >= 1 else 2
        return cls(inspire_type=itype, allow_ingot=True)
