"""神仙道 Player 模块协议代码契约 (Mod 0)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_Player_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class PlayerConstants:
    """Player 模块业务状态与行为常量"""

    ACTION_FAILED = 100
    ACTION_SUCCESS = 97
    AGAINST_WALLOWS = 3
    ALREADY_GET = 98
    BAG_FULL = 110
    BLOODLINE_ESSENCE = 55
    BLUE_YUPAI = 52
    BUY_NUMBER = 47
    CAMP_ERR = 90
    CAMP_SALARY = 76
    CANCEL_PRACTICE = 105
    CANT_CHANGE_CAMP = 91
    CAN_INCENSE_COUNT = 41
    CAN_JUAN_DUST = 59
    CAN_NOT_BACK_TIMES = 107
    CAN_NOT_UP_HEALTH_JOIN_CAMP_WAR = 83
    CHARGE_BACK_EFFECT = 117
    DAOYUAN = 58
    DISABLE_LOGIN = 6
    DUPLICATED_NICKNAME = 16
    ERROR = 111
    EXPLOIT = 60
    EXTRA_POWER = 77
    FAILD = 121
    FAILED = 1
    FALSE = 120
    FAME = 37
    FAME_LEVEL = 38
    FINISHED_PRACTICE = 104
    FINISH_DAY_QUEST = 85
    FIRST_TIME = 2
    FISHHOOK = 63
    FORBIDDEN_NICKNAME = 15
    FREE_MEDICAL = 75
    FULL_BUY_TIMES = 88
    FUNCTION_LOCK = 123
    GET_ONLINE_GIFT = 82
    GM_LOGIN = 8
    GREEN_YUPAI = 51
    HEAD_PORTRAIT = 65
    HEAD_RIM = 68
    HEALTH_UP_MEDICAL = 73
    HEALTH_UP_MEDICAL_EMPTY = 74
    HEALTH_UP_SYS = 72
    HIDE_ALL_EFFECT = 12
    HIDE_SUSTAINTED_EFFECT = 13
    IDCARDISUSE = 92
    INTERNET_BAR_POWER = 79
    IP_LOGIN_LIMIT = 7
    KID_FES_PLAY_TIME_NOT_ENOUGTH = 122
    KID_LOGIN_CONTROL = 4
    KID_PLAY_TIME_NOT_ENOUGTH = 5
    MAGIC_BREATH = 61
    MAX_EXTRA_POWER = 78
    MAX_HERO_MISSION_LOCK = 48
    MAX_INTERNET_BAR_POWER = 80
    MAX_MISSION_LOCK = 44
    MOUNT_RUNE = 64
    MUSIC_SET = 112
    NO = 10
    NOT_BUY_TRAIL = 118
    NOT_ENOUGH_INGOT = 87
    NOT_JOIN_CAMP = 99
    NO_INGOT = 106
    ONE_WARNING = 93
    ONLINE_GIFT = 81
    PACK_FULL = 101
    PLAYER_AVATAR = 31
    PLAYER_AVATAR_CD = 32
    PLAYER_CAMP_ID = 36
    PLAYER_CD_TIME = 40
    PLAYER_COINS = 20
    PLAYER_DAY_QUEST = 84
    PLAYER_EXPERIENCE = 25
    PLAYER_FUNCTION = 34
    PLAYER_HEALTH = 21
    PLAYER_INGOT = 19
    PLAYER_INIT_MEDICAL = 28
    PLAYER_LEVEL = 18
    PLAYER_MAX_EXPERIENCE = 26
    PLAYER_MAX_HEALTH = 22
    PLAYER_MAX_POWER = 24
    PLAYER_MEDICAL = 27
    PLAYER_PACK_EMPTY_NUM = 33
    PLAYER_POWER = 23
    PLAYER_QUEST_STATE = 35
    PLAYER_RECHARGE_VOUCHER = 69
    PLAYER_ROLE_LEVEL = 70
    PLAYER_SKILL = 42
    PLAYER_TOWN_KEY = 71
    PLAYER_TRANSPORT = 29
    PLAYER_TRANSPORT_BUFF_TIME = 30
    PLAYER_XIAN_LING = 49
    POWER_CRYSTAL = 66
    PURPLE_YUPAI = 53
    QUEST_GIFT_BAG = 43
    ROLE_SCRAP = 56
    SET_FAILED = 109
    SET_SUCCESS = 108
    SHOW_ALL_EFFECT = 11
    SHOW_MOUNT_TRAIL = 116
    SHOW_SUIT_TRAIL = 115
    SIMPLE_EFFECT = 14
    SPEAKER = 62
    START_PRACTICE = 103
    STATE_POINT = 45
    SUCCEED = 0
    SUCCESS = 89
    SUPER_TOWN_LEVLE = 57
    TANG_YUAN = 86
    TIMEUP = 96
    TOOLONG_NICKNAME = 17
    TOTAL_STATE_POINT = 46
    TRUE = 119
    TWO_WARNING = 94
    UI_TYPE = 114
    UPDATE_PRACTICE = 102
    VIP_LEVEL = 39
    WARNING = 95
    WAR_SET = 113
    WHITE_YU_PAI = 50
    XIU_WEI_LING_SHU_LEVEL = 67
    YELLOW_YUPAI = 54
    YES = 9

@dataclass
class PlayerLoginReq(BasePacket):
    """Player.login 请求封包 (Mod 0, Act 0)"""

    field_0: str
    field_1: str
    field_2: str
    field_3: str
    field_4: int
    field_5: str
    field_6: int
    field_7: int
    field_8: str
    field_9: str
    field_10: int
    field_11: str

    def __init__(self, field_0: str, field_1: str, field_2: str, field_3: str, field_4: int, field_5: str, field_6: int, field_7: int, field_8: str, field_9: str, field_10: int, field_11: str) -> None:
        super().__init__(mod=0, act=0)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5
        self.field_6 = field_6
        self.field_7 = field_7
        self.field_8 = field_8
        self.field_9 = field_9
        self.field_10 = field_10
        self.field_11 = field_11

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_utf(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_utf(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int8(self.field_7)
        writer.write_utf(self.field_8)
        writer.write_utf(self.field_9)
        writer.write_int8(self.field_10)
        writer.write_utf(self.field_11)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerLoginReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_utf()
        f_4 = reader.read_int32()
        f_5 = reader.read_utf()
        f_6 = reader.read_int32()
        f_7 = reader.read_int8()
        f_8 = reader.read_utf()
        f_9 = reader.read_utf()
        f_10 = reader.read_int8()
        f_11 = reader.read_utf()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11)

@dataclass
class PlayerLoginResp(BasePacket):
    """Player.login 应答封包 (Mod 0, Act 0)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int
    field_8: int
    field_9: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int, field_9: int) -> None:
        super().__init__(mod=0, act=0)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5
        self.field_6 = field_6
        self.field_7 = field_7
        self.field_8 = field_8
        self.field_9 = field_9

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_uint8(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int8(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int8(self.field_6)
        writer.write_uint8(self.field_7)
        writer.write_int32(self.field_8)
        writer.write_int8(self.field_9)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerLoginResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_uint8()
        f_3 = reader.read_int32()
        f_4 = reader.read_int8()
        f_5 = reader.read_int32()
        f_6 = reader.read_int8()
        f_7 = reader.read_uint8()
        f_8 = reader.read_int32()
        f_9 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9)

@dataclass
class PlayerPlayerFirstInitReq(BasePacket):
    """Player.player_first_init 请求封包 (Mod 0, Act 1)"""

    field_0: int
    field_1: str

    def __init__(self, field_0: int, field_1: str) -> None:
        super().__init__(mod=0, act=1)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerFirstInitReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        return cls(f_0, f_1)

@dataclass
class PlayerPlayerFirstInitResp(BasePacket):
    """Player.player_first_init 应答封包 (Mod 0, Act 1)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=1)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerFirstInitResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerGetPlayerInfoReq(BasePacket):
    """Player.get_player_info 请求封包 (Mod 0, Act 2)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=2)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerInfoReq":
        return cls()

@dataclass
class PlayerGetPlayerInfoResp(BasePacket):
    """Player.get_player_info 应答封包 (Mod 0, Act 2)"""

    field_0: str
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int
    field_8: int
    field_9: int
    field_10: int
    field_11: int
    field_12: int
    field_13: int
    field_14: int
    field_15: int
    field_16: int
    field_17: int
    field_18: int
    field_19: int
    field_20: int
    field_21: int
    field_22: int
    field_23: int
    field_24: int
    field_25: int
    field_26: int
    field_27: int
    field_28: int
    field_29: int
    field_30: int
    field_31: int
    field_32: int
    field_33: int
    field_34: int
    field_35: str
    field_36: str
    field_37: int
    field_38: int
    field_39: int
    field_40: int
    field_41: int
    field_42: int
    field_43: int

    def __init__(self, field_0: str, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int, field_9: int, field_10: int, field_11: int, field_12: int, field_13: int, field_14: int, field_15: int, field_16: int, field_17: int, field_18: int, field_19: int, field_20: int, field_21: int, field_22: int, field_23: int, field_24: int, field_25: int, field_26: int, field_27: int, field_28: int, field_29: int, field_30: int, field_31: int, field_32: int, field_33: int, field_34: int, field_35: str, field_36: str, field_37: int, field_38: int, field_39: int, field_40: int, field_41: int, field_42: int, field_43: int) -> None:
        super().__init__(mod=0, act=2)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5
        self.field_6 = field_6
        self.field_7 = field_7
        self.field_8 = field_8
        self.field_9 = field_9
        self.field_10 = field_10
        self.field_11 = field_11
        self.field_12 = field_12
        self.field_13 = field_13
        self.field_14 = field_14
        self.field_15 = field_15
        self.field_16 = field_16
        self.field_17 = field_17
        self.field_18 = field_18
        self.field_19 = field_19
        self.field_20 = field_20
        self.field_21 = field_21
        self.field_22 = field_22
        self.field_23 = field_23
        self.field_24 = field_24
        self.field_25 = field_25
        self.field_26 = field_26
        self.field_27 = field_27
        self.field_28 = field_28
        self.field_29 = field_29
        self.field_30 = field_30
        self.field_31 = field_31
        self.field_32 = field_32
        self.field_33 = field_33
        self.field_34 = field_34
        self.field_35 = field_35
        self.field_36 = field_36
        self.field_37 = field_37
        self.field_38 = field_38
        self.field_39 = field_39
        self.field_40 = field_40
        self.field_41 = field_41
        self.field_42 = field_42
        self.field_43 = field_43

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int64(self.field_3)
        writer.write_int64(self.field_4)
        writer.write_int64(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int64(self.field_7)
        writer.write_int64(self.field_8)
        writer.write_int32(self.field_9)
        writer.write_int32(self.field_10)
        writer.write_int32(self.field_11)
        writer.write_int32(self.field_12)
        writer.write_int32(self.field_13)
        writer.write_int32(self.field_14)
        writer.write_int32(self.field_15)
        writer.write_int32(self.field_16)
        writer.write_int32(self.field_17)
        writer.write_int32(self.field_18)
        writer.write_int8(self.field_19)
        writer.write_int32(self.field_20)
        writer.write_int32(self.field_21)
        writer.write_int32(self.field_22)
        writer.write_int32(self.field_23)
        writer.write_int32(self.field_24)
        writer.write_int32(self.field_25)
        writer.write_int32(self.field_26)
        writer.write_int8(self.field_27)
        writer.write_int32(self.field_28)
        writer.write_int32(self.field_29)
        writer.write_int8(self.field_30)
        writer.write_int32(self.field_31)
        writer.write_int32(self.field_32)
        writer.write_int32(self.field_33)
        writer.write_int8(self.field_34)
        writer.write_utf(self.field_35)
        writer.write_utf(self.field_36)
        writer.write_int32(self.field_37)
        writer.write_int32(self.field_38)
        writer.write_int32(self.field_39)
        writer.write_int32(self.field_40)
        writer.write_int32(self.field_41)
        writer.write_int32(self.field_42)
        writer.write_int32(self.field_43)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int64()
        f_4 = reader.read_int64()
        f_5 = reader.read_int64()
        f_6 = reader.read_int32()
        f_7 = reader.read_int64()
        f_8 = reader.read_int64()
        f_9 = reader.read_int32()
        f_10 = reader.read_int32()
        f_11 = reader.read_int32()
        f_12 = reader.read_int32()
        f_13 = reader.read_int32()
        f_14 = reader.read_int32()
        f_15 = reader.read_int32()
        f_16 = reader.read_int32()
        f_17 = reader.read_int32()
        f_18 = reader.read_int32()
        f_19 = reader.read_int8()
        f_20 = reader.read_int32()
        f_21 = reader.read_int32()
        f_22 = reader.read_int32()
        f_23 = reader.read_int32()
        f_24 = reader.read_int32()
        f_25 = reader.read_int32()
        f_26 = reader.read_int32()
        f_27 = reader.read_int8()
        f_28 = reader.read_int32()
        f_29 = reader.read_int32()
        f_30 = reader.read_int8()
        f_31 = reader.read_int32()
        f_32 = reader.read_int32()
        f_33 = reader.read_int32()
        f_34 = reader.read_int8()
        f_35 = reader.read_utf()
        f_36 = reader.read_utf()
        f_37 = reader.read_int32()
        f_38 = reader.read_int32()
        f_39 = reader.read_int32()
        f_40 = reader.read_int32()
        f_41 = reader.read_int32()
        f_42 = reader.read_int32()
        f_43 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11, f_12, f_13, f_14, f_15, f_16, f_17, f_18, f_19, f_20, f_21, f_22, f_23, f_24, f_25, f_26, f_27, f_28, f_29, f_30, f_31, f_32, f_33, f_34, f_35, f_36, f_37, f_38, f_39, f_40, f_41, f_42, f_43)

@dataclass
class PlayerUpdatePlayerDataReq(BasePacket):
    """Player.update_player_data 请求封包 (Mod 0, Act 3)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=3)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerUpdatePlayerDataReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerUpdatePlayerDataResp(BasePacket):
    """Player.update_player_data 应答封包 (Mod 0, Act 3)"""

    field_0: Tuple[int, int]

    def __init__(self, field_0: Tuple[int, int]) -> None:
        super().__init__(mod=0, act=3)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerUpdatePlayerDataResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class PlayerUpdatePlayerDataForTownReq(BasePacket):
    """Player.update_player_data_for_town 请求封包 (Mod 0, Act 4)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=4)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerUpdatePlayerDataForTownReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerUpdatePlayerDataForTownResp(BasePacket):
    """Player.update_player_data_for_town 应答封包 (Mod 0, Act 4)"""

    field_0: Tuple[int, int, int]

    def __init__(self, field_0: Tuple[int, int, int]) -> None:
        super().__init__(mod=0, act=4)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerUpdatePlayerDataForTownResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class PlayerBuyPowerReq(BasePacket):
    """Player.buy_power 请求封包 (Mod 0, Act 5)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=5)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerBuyPowerReq":
        return cls()

@dataclass
class PlayerBuyPowerResp(BasePacket):
    """Player.buy_power 应答封包 (Mod 0, Act 5)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=0, act=5)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_uint8(self.field_2)
        writer.write_int8(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerBuyPowerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int16()
        f_2 = reader.read_uint8()
        f_3 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class PlayerGetPlayerFunctionReq(BasePacket):
    """Player.get_player_function 请求封包 (Mod 0, Act 6)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=6)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerFunctionReq":
        return cls()

@dataclass
class PlayerGetPlayerFunctionResp(BasePacket):
    """Player.get_player_function 应答封包 (Mod 0, Act 6)"""

    field_0: Tuple[int, int]

    def __init__(self, field_0: Tuple[int, int]) -> None:
        super().__init__(mod=0, act=6)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerFunctionResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class PlayerSignPlayPlayerFunctionReq(BasePacket):
    """Player.sign_play_player_function 请求封包 (Mod 0, Act 7)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=7)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSignPlayPlayerFunctionReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerSignPlayPlayerFunctionResp(BasePacket):
    """Player.sign_play_player_function 应答封包 (Mod 0, Act 7)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=7)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSignPlayPlayerFunctionResp":
        return cls()

@dataclass
class PlayerSetPlayerCampReq(BasePacket):
    """Player.set_player_camp 请求封包 (Mod 0, Act 8)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=8)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSetPlayerCampReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerSetPlayerCampResp(BasePacket):
    """Player.set_player_camp 应答封包 (Mod 0, Act 8)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=8)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSetPlayerCampResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerReceivePlayerDelayNotifyMessageReq(BasePacket):
    """Player.receive_player_delay_notify_message 请求封包 (Mod 0, Act 9)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=9)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerReceivePlayerDelayNotifyMessageReq":
        return cls()

@dataclass
class PlayerReceivePlayerDelayNotifyMessageResp(BasePacket):
    """Player.receive_player_delay_notify_message 应答封包 (Mod 0, Act 9)"""

    field_0: Tuple[str, int]

    def __init__(self, field_0: Tuple[str, int]) -> None:
        super().__init__(mod=0, act=9)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerReceivePlayerDelayNotifyMessageResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class PlayerValidateIdCardReq(BasePacket):
    """Player.validate_id_card 请求封包 (Mod 0, Act 10)"""

    field_0: str

    def __init__(self, field_0: str) -> None:
        super().__init__(mod=0, act=10)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerValidateIdCardReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        return cls(f_0)

@dataclass
class PlayerValidateIdCardResp(BasePacket):
    """Player.validate_id_card 应答封包 (Mod 0, Act 10)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=10)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerValidateIdCardResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerAgainstWallowsNotifyReq(BasePacket):
    """Player.against_wallows_notify 请求封包 (Mod 0, Act 11)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=11)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerAgainstWallowsNotifyReq":
        return cls()

@dataclass
class PlayerAgainstWallowsNotifyResp(BasePacket):
    """Player.against_wallows_notify 应答封包 (Mod 0, Act 11)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=11)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerAgainstWallowsNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerGetPlayerCampSalaryReq(BasePacket):
    """Player.get_player_camp_salary 请求封包 (Mod 0, Act 20)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=20)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerCampSalaryReq":
        return cls()

@dataclass
class PlayerGetPlayerCampSalaryResp(BasePacket):
    """Player.get_player_camp_salary 应答封包 (Mod 0, Act 20)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=0, act=20)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerCampSalaryResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class PlayerServerTimeReq(BasePacket):
    """Player.server_time 请求封包 (Mod 0, Act 22)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=22)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerServerTimeReq":
        return cls()

@dataclass
class PlayerServerTimeResp(BasePacket):
    """Player.server_time 应答封包 (Mod 0, Act 22)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=22)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerServerTimeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerGetBuyPowerDataReq(BasePacket):
    """Player.get_buy_power_data 请求封包 (Mod 0, Act 23)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=23)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetBuyPowerDataReq":
        return cls()

@dataclass
class PlayerGetBuyPowerDataResp(BasePacket):
    """Player.get_buy_power_data 应答封包 (Mod 0, Act 23)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=0, act=23)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetBuyPowerDataResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int16()
        f_2 = reader.read_int8()
        return cls(f_0, f_1, f_2)

@dataclass
class PlayerGetOtherPlayerInfoReq(BasePacket):
    """Player.get_other_player_info 请求封包 (Mod 0, Act 24)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=24)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetOtherPlayerInfoReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerGetOtherPlayerInfoResp(BasePacket):
    """Player.get_other_player_info 应答封包 (Mod 0, Act 24)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=0, act=24)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_uint8(self.field_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetOtherPlayerInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_uint8()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class PlayerPlayerGetOnlineGiftReq(BasePacket):
    """Player.player_get_online_gift 请求封包 (Mod 0, Act 30)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=30)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerGetOnlineGiftReq":
        return cls()

@dataclass
class PlayerPlayerGetOnlineGiftResp(BasePacket):
    """Player.player_get_online_gift 应答封包 (Mod 0, Act 30)"""

    field_0: int
    field_1: Tuple[int, int, int]
    field_2: int

    def __init__(self, field_0: int, field_1: Tuple[int, int, int], field_2: int) -> None:
        super().__init__(mod=0, act=30)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerGetOnlineGiftResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class PlayerGetPlayerCurrentOnlineGiftReq(BasePacket):
    """Player.get_player_current_online_gift 请求封包 (Mod 0, Act 31)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=31)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerCurrentOnlineGiftReq":
        return cls()

@dataclass
class PlayerGetPlayerCurrentOnlineGiftResp(BasePacket):
    """Player.get_player_current_online_gift 应答封包 (Mod 0, Act 31)"""

    field_0: int
    field_1: Tuple[int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int]) -> None:
        super().__init__(mod=0, act=31)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerCurrentOnlineGiftResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class PlayerGetAfficheListReq(BasePacket):
    """Player.get_affiche_list 请求封包 (Mod 0, Act 35)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=35)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetAfficheListReq":
        return cls()

@dataclass
class PlayerGetAfficheListResp(BasePacket):
    """Player.get_affiche_list 应答封包 (Mod 0, Act 35)"""

    field_0: Tuple[int, str]

    def __init__(self, field_0: Tuple[int, str]) -> None:
        super().__init__(mod=0, act=35)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetAfficheListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class PlayerStartPracticeReq(BasePacket):
    """Player.start_practice 请求封包 (Mod 0, Act 36)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=36)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerStartPracticeReq":
        return cls()

@dataclass
class PlayerStartPracticeResp(BasePacket):
    """Player.start_practice 应答封包 (Mod 0, Act 36)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=36)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerStartPracticeResp":
        return cls()

@dataclass
class PlayerGetPracticeDataReq(BasePacket):
    """Player.get_practice_data 请求封包 (Mod 0, Act 37)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=37)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPracticeDataReq":
        return cls()

@dataclass
class PlayerGetPracticeDataResp(BasePacket):
    """Player.get_practice_data 应答封包 (Mod 0, Act 37)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int) -> None:
        super().__init__(mod=0, act=37)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5
        self.field_6 = field_6
        self.field_7 = field_7

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int64(self.field_4)
        writer.write_int8(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int32(self.field_7)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPracticeDataResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        f_4 = reader.read_int64()
        f_5 = reader.read_int8()
        f_6 = reader.read_int32()
        f_7 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7)

@dataclass
class PlayerSignFinishedPracticeReq(BasePacket):
    """Player.sign_finished_practice 请求封包 (Mod 0, Act 38)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=38)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSignFinishedPracticeReq":
        return cls()

@dataclass
class PlayerSignFinishedPracticeResp(BasePacket):
    """Player.sign_finished_practice 应答封包 (Mod 0, Act 38)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=38)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSignFinishedPracticeResp":
        return cls()

@dataclass
class PlayerCancelPracticeReq(BasePacket):
    """Player.cancel_practice 请求封包 (Mod 0, Act 39)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=39)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerCancelPracticeReq":
        return cls()

@dataclass
class PlayerCancelPracticeResp(BasePacket):
    """Player.cancel_practice 应答封包 (Mod 0, Act 39)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=39)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerCancelPracticeResp":
        return cls()

@dataclass
class PlayerPracticeNotifyReq(BasePacket):
    """Player.practice_notify 请求封包 (Mod 0, Act 40)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=40)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPracticeNotifyReq":
        return cls()

@dataclass
class PlayerPracticeNotifyResp(BasePacket):
    """Player.practice_notify 应答封包 (Mod 0, Act 40)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=0, act=40)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPracticeNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class PlayerGetPlayerWarCdTimeReq(BasePacket):
    """Player.get_player_war_cd_time 请求封包 (Mod 0, Act 41)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=41)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerWarCdTimeReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerGetPlayerWarCdTimeResp(BasePacket):
    """Player.get_player_war_cd_time 应答封包 (Mod 0, Act 41)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=41)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerWarCdTimeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerGetGameAssistantInfoReq(BasePacket):
    """Player.get_game_assistant_info 请求封包 (Mod 0, Act 42)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=42)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetGameAssistantInfoReq":
        return cls()

@dataclass
class PlayerGetGameAssistantInfoResp(BasePacket):
    """Player.get_game_assistant_info 应答封包 (Mod 0, Act 42)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int
    field_8: int
    field_9: int
    field_10: int
    field_11: int
    field_12: int
    field_13: int
    field_14: int
    field_15: int
    field_16: int
    field_17: int
    field_18: int
    field_19: int
    field_20: int
    field_21: int
    field_22: int
    field_23: int
    field_24: int
    field_25: int
    field_26: int
    field_27: int
    field_28: int
    field_29: int
    field_30: int
    field_31: int
    field_32: int
    field_33: Tuple[int, int, int, int]
    field_34: Tuple[int, int, int, int]

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int, field_9: int, field_10: int, field_11: int, field_12: int, field_13: int, field_14: int, field_15: int, field_16: int, field_17: int, field_18: int, field_19: int, field_20: int, field_21: int, field_22: int, field_23: int, field_24: int, field_25: int, field_26: int, field_27: int, field_28: int, field_29: int, field_30: int, field_31: int, field_32: int, field_33: Tuple[int, int, int, int], field_34: Tuple[int, int, int, int]) -> None:
        super().__init__(mod=0, act=42)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5
        self.field_6 = field_6
        self.field_7 = field_7
        self.field_8 = field_8
        self.field_9 = field_9
        self.field_10 = field_10
        self.field_11 = field_11
        self.field_12 = field_12
        self.field_13 = field_13
        self.field_14 = field_14
        self.field_15 = field_15
        self.field_16 = field_16
        self.field_17 = field_17
        self.field_18 = field_18
        self.field_19 = field_19
        self.field_20 = field_20
        self.field_21 = field_21
        self.field_22 = field_22
        self.field_23 = field_23
        self.field_24 = field_24
        self.field_25 = field_25
        self.field_26 = field_26
        self.field_27 = field_27
        self.field_28 = field_28
        self.field_29 = field_29
        self.field_30 = field_30
        self.field_31 = field_31
        self.field_32 = field_32
        self.field_33 = field_33
        self.field_34 = field_34

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int64(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int64(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int32(self.field_7)
        writer.write_int32(self.field_8)
        writer.write_int32(self.field_9)
        writer.write_int32(self.field_10)
        writer.write_int32(self.field_11)
        writer.write_int32(self.field_12)
        writer.write_int32(self.field_13)
        writer.write_int32(self.field_14)
        writer.write_int32(self.field_15)
        writer.write_int32(self.field_16)
        writer.write_int32(self.field_17)
        writer.write_int32(self.field_18)
        writer.write_int32(self.field_19)
        writer.write_int32(self.field_20)
        writer.write_int32(self.field_21)
        writer.write_int32(self.field_22)
        writer.write_int32(self.field_23)
        writer.write_int32(self.field_24)
        writer.write_int32(self.field_25)
        writer.write_int32(self.field_26)
        writer.write_int32(self.field_27)
        writer.write_int32(self.field_28)
        writer.write_int32(self.field_29)
        writer.write_int32(self.field_30)
        writer.write_int32(self.field_31)
        writer.write_int32(self.field_32)
        # 写入动态列表 field_33 (元素数 + 记录项)
        writer.write_uint16(len(self.field_33))
        for item_33 in self.field_33:
            writer.write_json(item_33)
        # 写入动态列表 field_34 (元素数 + 记录项)
        writer.write_uint16(len(self.field_34))
        for item_34 in self.field_34:
            writer.write_json(item_34)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetGameAssistantInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int64()
        f_2 = reader.read_int32()
        f_3 = reader.read_int64()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        f_6 = reader.read_int32()
        f_7 = reader.read_int32()
        f_8 = reader.read_int32()
        f_9 = reader.read_int32()
        f_10 = reader.read_int32()
        f_11 = reader.read_int32()
        f_12 = reader.read_int32()
        f_13 = reader.read_int32()
        f_14 = reader.read_int32()
        f_15 = reader.read_int32()
        f_16 = reader.read_int32()
        f_17 = reader.read_int32()
        f_18 = reader.read_int32()
        f_19 = reader.read_int32()
        f_20 = reader.read_int32()
        f_21 = reader.read_int32()
        f_22 = reader.read_int32()
        f_23 = reader.read_int32()
        f_24 = reader.read_int32()
        f_25 = reader.read_int32()
        f_26 = reader.read_int32()
        f_27 = reader.read_int32()
        f_28 = reader.read_int32()
        f_29 = reader.read_int32()
        f_30 = reader.read_int32()
        f_31 = reader.read_int32()
        f_32 = reader.read_int32()
        # 读取动态列表 f_33
        cnt_33 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_33 = []
        for _ in range(cnt_33):
            f_33.append(reader.read_json())
        # 读取动态列表 f_34
        cnt_34 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_34 = []
        for _ in range(cnt_34):
            f_34.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11, f_12, f_13, f_14, f_15, f_16, f_17, f_18, f_19, f_20, f_21, f_22, f_23, f_24, f_25, f_26, f_27, f_28, f_29, f_30, f_31, f_32, f_33, f_34)

@dataclass
class PlayerSendIngotReceiveShowVipReq(BasePacket):
    """Player.send_ingot_receive_show_vip 请求封包 (Mod 0, Act 43)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=43)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSendIngotReceiveShowVipReq":
        return cls()

@dataclass
class PlayerSendIngotReceiveShowVipResp(BasePacket):
    """Player.send_ingot_receive_show_vip 应答封包 (Mod 0, Act 43)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=43)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSendIngotReceiveShowVipResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerAgainstWallowsInfoReq(BasePacket):
    """Player.against_wallows_info 请求封包 (Mod 0, Act 44)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=44)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerAgainstWallowsInfoReq":
        return cls()

@dataclass
class PlayerAgainstWallowsInfoResp(BasePacket):
    """Player.against_wallows_info 应答封包 (Mod 0, Act 44)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=0, act=44)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_uint8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerAgainstWallowsInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_uint8()
        return cls(f_0, f_1)

@dataclass
class PlayerGetLastPlayerVersionReq(BasePacket):
    """Player.get_last_player_version 请求封包 (Mod 0, Act 45)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=45)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetLastPlayerVersionReq":
        return cls()

@dataclass
class PlayerGetLastPlayerVersionResp(BasePacket):
    """Player.get_last_player_version 应答封包 (Mod 0, Act 45)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=45)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetLastPlayerVersionResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerGetWarningAfficheReq(BasePacket):
    """Player.get_warning_affiche 请求封包 (Mod 0, Act 46)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=46)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetWarningAfficheReq":
        return cls()

@dataclass
class PlayerGetWarningAfficheResp(BasePacket):
    """Player.get_warning_affiche 应答封包 (Mod 0, Act 46)"""

    field_0: str

    def __init__(self, field_0: str) -> None:
        super().__init__(mod=0, act=46)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetWarningAfficheResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        return cls(f_0)

@dataclass
class PlayerBackTimesReq(BasePacket):
    """Player.back_times 请求封包 (Mod 0, Act 47)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=47)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerBackTimesReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerBackTimesResp(BasePacket):
    """Player.back_times 应答封包 (Mod 0, Act 47)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=0, act=47)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerBackTimesResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class PlayerPlayerInfoContrastReq(BasePacket):
    """Player.player_info_contrast 请求封包 (Mod 0, Act 48)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=48)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerInfoContrastReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerPlayerInfoContrastResp(BasePacket):
    """Player.player_info_contrast 应答封包 (Mod 0, Act 48)"""

    field_0: Tuple[int, int, str, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, str, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=0, act=48)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerInfoContrastResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class PlayerPlayerConsumeAlertSetInfoReq(BasePacket):
    """Player.player_consume_alert_set_info 请求封包 (Mod 0, Act 49)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=49)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerConsumeAlertSetInfoReq":
        return cls()

@dataclass
class PlayerPlayerConsumeAlertSetInfoResp(BasePacket):
    """Player.player_consume_alert_set_info 应答封包 (Mod 0, Act 49)"""

    field_0: Tuple[int, int]

    def __init__(self, field_0: Tuple[int, int]) -> None:
        super().__init__(mod=0, act=49)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerConsumeAlertSetInfoResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class PlayerPlayerConsumeAlertSetReq(BasePacket):
    """Player.player_consume_alert_set 请求封包 (Mod 0, Act 50)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=0, act=50)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerConsumeAlertSetReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class PlayerPlayerConsumeAlertSetResp(BasePacket):
    """Player.player_consume_alert_set 应答封包 (Mod 0, Act 50)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=50)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerConsumeAlertSetResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerGetPlayerInfoByUsernameReq(BasePacket):
    """Player.get_player_info_by_username 请求封包 (Mod 0, Act 51)"""

    field_0: str

    def __init__(self, field_0: str) -> None:
        super().__init__(mod=0, act=51)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerInfoByUsernameReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        return cls(f_0)

@dataclass
class PlayerGetPlayerInfoByUsernameResp(BasePacket):
    """Player.get_player_info_by_username 应答封包 (Mod 0, Act 51)"""

    field_0: int
    field_1: int
    field_2: str

    def __init__(self, field_0: int, field_1: int, field_2: str) -> None:
        super().__init__(mod=0, act=51)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_utf(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerInfoByUsernameResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_utf()
        return cls(f_0, f_1, f_2)

@dataclass
class PlayerPlayerFollowSettingReq(BasePacket):
    """Player.player_follow_setting 请求封包 (Mod 0, Act 52)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=52)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerFollowSettingReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerPlayerFollowSettingResp(BasePacket):
    """Player.player_follow_setting 应答封包 (Mod 0, Act 52)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=0, act=52)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerFollowSettingResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class PlayerIsWeichengnianReq(BasePacket):
    """Player.is_weichengnian 请求封包 (Mod 0, Act 53)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=53)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerIsWeichengnianReq":
        return cls()

@dataclass
class PlayerIsWeichengnianResp(BasePacket):
    """Player.is_weichengnian 应答封包 (Mod 0, Act 53)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=53)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerIsWeichengnianResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class PlayerSetCustomPannelReq(BasePacket):
    """Player.set_custom_pannel 请求封包 (Mod 0, Act 54)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=54)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSetCustomPannelReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerSetCustomPannelResp(BasePacket):
    """Player.set_custom_pannel 应答封包 (Mod 0, Act 54)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=0, act=54)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSetCustomPannelResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class PlayerPcClientGiftInfoReq(BasePacket):
    """Player.pc_client_gift_info 请求封包 (Mod 0, Act 55)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=55)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPcClientGiftInfoReq":
        return cls()

@dataclass
class PlayerPcClientGiftInfoResp(BasePacket):
    """Player.pc_client_gift_info 应答封包 (Mod 0, Act 55)"""

    field_0: int
    field_1: Tuple[int, int]
    field_2: int
    field_3: Tuple[int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int], field_2: int, field_3: Tuple[int, int]) -> None:
        super().__init__(mod=0, act=55)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        writer.write_int8(self.field_2)
        # 写入动态列表 field_3 (元素数 + 记录项)
        writer.write_uint16(len(self.field_3))
        for item_3 in self.field_3:
            writer.write_json(item_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPcClientGiftInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        f_2 = reader.read_int8()
        # 读取动态列表 f_3
        cnt_3 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_3 = []
        for _ in range(cnt_3):
            f_3.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class PlayerReceiveClientGiftReq(BasePacket):
    """Player.receive_client_gift 请求封包 (Mod 0, Act 56)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=56)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerReceiveClientGiftReq":
        return cls()

@dataclass
class PlayerReceiveClientGiftResp(BasePacket):
    """Player.receive_client_gift 应答封包 (Mod 0, Act 56)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=56)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerReceiveClientGiftResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerNotifyHaveClientGiftReq(BasePacket):
    """Player.notify_have_client_gift 请求封包 (Mod 0, Act 57)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=57)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerNotifyHaveClientGiftReq":
        return cls()

@dataclass
class PlayerNotifyHaveClientGiftResp(BasePacket):
    """Player.notify_have_client_gift 应答封包 (Mod 0, Act 57)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=57)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerNotifyHaveClientGiftResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class PlayerGamebangPlayerStatusReq(BasePacket):
    """Player.gamebang_player_status 请求封包 (Mod 0, Act 58)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=58)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGamebangPlayerStatusReq":
        return cls()

@dataclass
class PlayerGamebangPlayerStatusResp(BasePacket):
    """Player.gamebang_player_status 应答封包 (Mod 0, Act 58)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=58)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGamebangPlayerStatusResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class PlayerSetPlayerSettingReq(BasePacket):
    """Player.set_player_setting 请求封包 (Mod 0, Act 59)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=0, act=59)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSetPlayerSettingReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class PlayerSetPlayerSettingResp(BasePacket):
    """Player.set_player_setting 应答封包 (Mod 0, Act 59)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=59)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSetPlayerSettingResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerPlayerOpenNewGameFunctionReq(BasePacket):
    """Player.player_open_new_game_function 请求封包 (Mod 0, Act 60)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=60)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerOpenNewGameFunctionReq":
        return cls()

@dataclass
class PlayerPlayerOpenNewGameFunctionResp(BasePacket):
    """Player.player_open_new_game_function 应答封包 (Mod 0, Act 60)"""

    field_0: List[int]

    def __init__(self, field_0: List[int]) -> None:
        super().__init__(mod=0, act=60)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_int16(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerOpenNewGameFunctionResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_int16())
        return cls(f_0)

@dataclass
class PlayerPlayerGetInternetBarOnlineGiftReq(BasePacket):
    """Player.player_get_internet_bar_online_gift 请求封包 (Mod 0, Act 61)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=61)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerGetInternetBarOnlineGiftReq":
        return cls()

@dataclass
class PlayerPlayerGetInternetBarOnlineGiftResp(BasePacket):
    """Player.player_get_internet_bar_online_gift 应答封包 (Mod 0, Act 61)"""

    field_0: int
    field_1: Tuple[int, int]
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: Tuple[int, int], field_2: int, field_3: int) -> None:
        super().__init__(mod=0, act=61)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        writer.write_int32(self.field_2)
        writer.write_int8(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerGetInternetBarOnlineGiftResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        f_2 = reader.read_int32()
        f_3 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class PlayerGetPlayerCurrentInternetBarOnlineGiftReq(BasePacket):
    """Player.get_player_current_internet_bar_online_gift 请求封包 (Mod 0, Act 62)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=62)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerCurrentInternetBarOnlineGiftReq":
        return cls()

@dataclass
class PlayerGetPlayerCurrentInternetBarOnlineGiftResp(BasePacket):
    """Player.get_player_current_internet_bar_online_gift 应答封包 (Mod 0, Act 62)"""

    field_0: int
    field_1: int
    field_2: Tuple[int, int]

    def __init__(self, field_0: int, field_1: int, field_2: Tuple[int, int]) -> None:
        super().__init__(mod=0, act=62)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int32(self.field_1)
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerCurrentInternetBarOnlineGiftResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int32()
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_json())
        return cls(f_0, f_1, f_2)

@dataclass
class PlayerSetInStTownReq(BasePacket):
    """Player.set_in_st_town 请求封包 (Mod 0, Act 63)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=63)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSetInStTownReq":
        return cls()

@dataclass
class PlayerSetInStTownResp(BasePacket):
    """Player.set_in_st_town 应答封包 (Mod 0, Act 63)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=63)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSetInStTownResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerIsInStTownReq(BasePacket):
    """Player.is_in_st_town 请求封包 (Mod 0, Act 64)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=64)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerIsInStTownReq":
        return cls()

@dataclass
class PlayerIsInStTownResp(BasePacket):
    """Player.is_in_st_town 应答封包 (Mod 0, Act 64)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=64)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerIsInStTownResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class PlayerSuperTownLevelInfoReq(BasePacket):
    """Player.super_town_level_info 请求封包 (Mod 0, Act 65)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=65)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSuperTownLevelInfoReq":
        return cls()

@dataclass
class PlayerSuperTownLevelInfoResp(BasePacket):
    """Player.super_town_level_info 应答封包 (Mod 0, Act 65)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=0, act=65)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSuperTownLevelInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class PlayerCompareWarPowerReq(BasePacket):
    """Player.compare_war_power 请求封包 (Mod 0, Act 66)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=66)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerCompareWarPowerReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerCompareWarPowerResp(BasePacket):
    """Player.compare_war_power 应答封包 (Mod 0, Act 66)"""

    field_0: Tuple[str, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[str, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=0, act=66)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerCompareWarPowerResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class PlayerOperationActivityTimeListReq(BasePacket):
    """Player.operation_activity_time_list 请求封包 (Mod 0, Act 67)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=67)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerOperationActivityTimeListReq":
        return cls()

@dataclass
class PlayerOperationActivityTimeListResp(BasePacket):
    """Player.operation_activity_time_list 应答封包 (Mod 0, Act 67)"""

    field_0: Tuple[int, Tuple[int, int], int, int]

    def __init__(self, field_0: Tuple[int, Tuple[int, int], int, int]) -> None:
        super().__init__(mod=0, act=67)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerOperationActivityTimeListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class PlayerIsTestServerReq(BasePacket):
    """Player.is_test_server 请求封包 (Mod 0, Act 68)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=68)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerIsTestServerReq":
        return cls()

@dataclass
class PlayerIsTestServerResp(BasePacket):
    """Player.is_test_server 应答封包 (Mod 0, Act 68)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=68)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerIsTestServerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerCheckFunctionOpenReq(BasePacket):
    """Player.check_function_open 请求封包 (Mod 0, Act 69)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=69)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerCheckFunctionOpenReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerCheckFunctionOpenResp(BasePacket):
    """Player.check_function_open 应答封包 (Mod 0, Act 69)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=69)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerCheckFunctionOpenResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerPlayerUiListReq(BasePacket):
    """Player.player_ui_list 请求封包 (Mod 0, Act 70)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=70)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerUiListReq":
        return cls()

@dataclass
class PlayerPlayerUiListResp(BasePacket):
    """Player.player_ui_list 应答封包 (Mod 0, Act 70)"""

    field_0: List[int]
    field_1: int

    def __init__(self, field_0: List[int], field_1: int) -> None:
        super().__init__(mod=0, act=70)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_int32(item_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerUiListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_int32())
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class PlayerSetPlayerUiReq(BasePacket):
    """Player.set_player_ui 请求封包 (Mod 0, Act 71)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=71)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSetPlayerUiReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerSetPlayerUiResp(BasePacket):
    """Player.set_player_ui 应答封包 (Mod 0, Act 71)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=71)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSetPlayerUiResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerGetPlayerMissionLoadingInterfaceIdReq(BasePacket):
    """Player.get_player_mission_loading_interface_id 请求封包 (Mod 0, Act 72)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=72)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerMissionLoadingInterfaceIdReq":
        return cls()

@dataclass
class PlayerGetPlayerMissionLoadingInterfaceIdResp(BasePacket):
    """Player.get_player_mission_loading_interface_id 应答封包 (Mod 0, Act 72)"""

    field_0: int
    field_1: List[int]

    def __init__(self, field_0: int, field_1: List[int]) -> None:
        super().__init__(mod=0, act=72)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_int32(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerMissionLoadingInterfaceIdResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_int32())
        return cls(f_0, f_1)

@dataclass
class PlayerSetPlayerMissionLoadingInterfaceIdReq(BasePacket):
    """Player.set_player_mission_loading_interface_id 请求封包 (Mod 0, Act 73)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=73)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSetPlayerMissionLoadingInterfaceIdReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerSetPlayerMissionLoadingInterfaceIdResp(BasePacket):
    """Player.set_player_mission_loading_interface_id 应答封包 (Mod 0, Act 73)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=73)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSetPlayerMissionLoadingInterfaceIdResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerAwardItemNotifyReq(BasePacket):
    """Player.award_item_notify 请求封包 (Mod 0, Act 74)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=74)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerAwardItemNotifyReq":
        return cls()

@dataclass
class PlayerAwardItemNotifyResp(BasePacket):
    """Player.award_item_notify 应答封包 (Mod 0, Act 74)"""

    field_0: Tuple[int, int]

    def __init__(self, field_0: Tuple[int, int]) -> None:
        super().__init__(mod=0, act=74)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerAwardItemNotifyResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class PlayerHeartReq(BasePacket):
    """Player.heart 请求封包 (Mod 0, Act 75)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=75)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerHeartReq":
        return cls()

@dataclass
class PlayerHeartResp(BasePacket):
    """Player.heart 应答封包 (Mod 0, Act 75)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=75)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerHeartResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class PlayerCustomerServiceInfoReq(BasePacket):
    """Player.customer_service_info 请求封包 (Mod 0, Act 76)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=76)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerCustomerServiceInfoReq":
        return cls()

@dataclass
class PlayerCustomerServiceInfoResp(BasePacket):
    """Player.customer_service_info 应答封包 (Mod 0, Act 76)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=0, act=76)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int8(self.field_1)
        writer.write_int64(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerCustomerServiceInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int8()
        f_2 = reader.read_int64()
        return cls(f_0, f_1, f_2)

@dataclass
class PlayerSetGetCustomerServiceGiftReq(BasePacket):
    """Player.set_get_customer_service_gift 请求封包 (Mod 0, Act 77)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=77)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSetGetCustomerServiceGiftReq":
        return cls()

@dataclass
class PlayerSetGetCustomerServiceGiftResp(BasePacket):
    """Player.set_get_customer_service_gift 应答封包 (Mod 0, Act 77)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=77)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerSetGetCustomerServiceGiftResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerKidLoginNotifyReq(BasePacket):
    """Player.kid_login_notify 请求封包 (Mod 0, Act 78)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=78)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerKidLoginNotifyReq":
        return cls()

@dataclass
class PlayerKidLoginNotifyResp(BasePacket):
    """Player.kid_login_notify 应答封包 (Mod 0, Act 78)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=78)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerKidLoginNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerGetPlayerLockReq(BasePacket):
    """Player.get_player_lock 请求封包 (Mod 0, Act 79)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=79)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerLockReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class PlayerGetPlayerLockResp(BasePacket):
    """Player.get_player_lock 应答封包 (Mod 0, Act 79)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=79)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetPlayerLockResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerGetChargeBackEffectListReq(BasePacket):
    """Player.get_charge_back_effect_list 请求封包 (Mod 0, Act 80)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=80)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetChargeBackEffectListReq":
        return cls()

@dataclass
class PlayerGetChargeBackEffectListResp(BasePacket):
    """Player.get_charge_back_effect_list 应答封包 (Mod 0, Act 80)"""

    field_0: Tuple[int, int, int]

    def __init__(self, field_0: Tuple[int, int, int]) -> None:
        super().__init__(mod=0, act=80)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetChargeBackEffectListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class PlayerPlayerChaosMonsterFollowSettingReq(BasePacket):
    """Player.player_chaos_monster_follow_setting 请求封包 (Mod 0, Act 81)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=81)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerChaosMonsterFollowSettingReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        return cls(f_0)

@dataclass
class PlayerPlayerChaosMonsterFollowSettingResp(BasePacket):
    """Player.player_chaos_monster_follow_setting 应答封包 (Mod 0, Act 81)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=0, act=81)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerChaosMonsterFollowSettingResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class PlayerPlayerDragonBallFollowSettingReq(BasePacket):
    """Player.player_dragon_ball_follow_setting 请求封包 (Mod 0, Act 82)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=82)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerDragonBallFollowSettingReq":
        return cls()

@dataclass
class PlayerPlayerDragonBallFollowSettingResp(BasePacket):
    """Player.player_dragon_ball_follow_setting 应答封包 (Mod 0, Act 82)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=0, act=82)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerPlayerDragonBallFollowSettingResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class PlayerGetHeadInfoReq(BasePacket):
    """Player.get_head_info 请求封包 (Mod 0, Act 83)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=83)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetHeadInfoReq":
        return cls()

@dataclass
class PlayerGetHeadInfoResp(BasePacket):
    """Player.get_head_info 应答封包 (Mod 0, Act 83)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=0, act=83)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerGetHeadInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class PlayerOfficialAccountPanelShowFlagReq(BasePacket):
    """Player.official_account_panel_show_flag 请求封包 (Mod 0, Act 84)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=84)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerOfficialAccountPanelShowFlagReq":
        return cls()

@dataclass
class PlayerOfficialAccountPanelShowFlagResp(BasePacket):
    """Player.official_account_panel_show_flag 应答封包 (Mod 0, Act 84)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=0, act=84)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerOfficialAccountPanelShowFlagResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class PlayerJiekouTestReq(BasePacket):
    """Player.jiekou_test 请求封包 (Mod 0, Act 99)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=99)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerJiekouTestReq":
        return cls()

@dataclass
class PlayerJiekouTestResp(BasePacket):
    """Player.jiekou_test 应答封包 (Mod 0, Act 99)"""

    def __init__(self) -> None:
        super().__init__(mod=0, act=99)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "PlayerJiekouTestResp":
        return cls()
