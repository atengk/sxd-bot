"""神仙道 Item 模块协议代码契约 (Mod 2)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_Item_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class ItemConstants:
    """Item 模块业务状态与行为常量"""

    ACTION_FAILED = 143
    ACTION_SUCCESS = 20
    ALREADY_HAVE = 162
    ALREADY_MARRY = 213
    AMAGIC_EQUIP = 204
    AMAGIC_SPIRIT = 205
    ARMOR_FUN_NOT_OPEN = 72
    ARTIFACT = 202
    ARTIFACT_NOT_OPEN = 113
    ATTRIBUTE_GOD_STONE = 198
    AWAKE_NO_OPEN = 80
    BAI_LIAN_QIAN_KUN_TWO_UNOPEN = 99
    BAI_LIAN_QIAN_KUN_UNOPEN = 90
    BECOME_IMMORTAL_FUN_NOT_OPEN = 63
    BLOODLINE = 191
    BLOODLINE_FUN_NOT_OPEN = 64
    BLOOD_ESSENCE = 7
    BOOK_ERROR = 216
    BUY_NUMBER_LIMIT = 185
    CAN_JUAN_PACK_FULL = 76
    CARD_SOUL_FUN_NOT_OPEN = 73
    CHANGE_CARD_NOT_OPEN = 109
    CHAOSVOID_FUN_NOT_OPEN = 54
    CHAOS_ITEM_PACK_FULL = 59
    CHAOS_LING_YE = 15
    CHAOS_MONSTER_PACK_FULL = 58
    CHAOS_NO_OPEN = 95
    CHAOS_VOID = 189
    CHILDREN_COUNT_LIMIT = 98
    CHILDREN_FUNCTION_UNOPEN = 97
    COINS = 3
    DANCE_ACTION_NOT_OPEN = 106
    DAO_YUAN = 16
    DAO_YUAN_CAN_NOT_GET = 67
    DESTINY_SWORD = 203
    DEVILEXPEDITION_NOT_OPEN = 122
    DRAGONBALL = 13
    DRAGONBALL_FUN_NOT_OPEN = 55
    DRAGONBALL_NO_FREE_GRID = 57
    DRAGONBALL_VOW_FUN_NOT_OPEN = 56
    DRAG_FAILED = 182
    DRAG_SUCCESS = 180
    DRAG_TO_BAG = 178
    DRAG_TO_FURNACE = 179
    EIGHTIMMORTALS_NOT_OPEN = 111
    ELIXIR_SOUL_NOT_OPEN = 107
    END_TIME = 48
    EQUIP = 186
    EQUIPMENT_NOT_IN_BODY = 159
    ERROR_COOL_TIME = 119
    ERROR_PARAM = 230
    EUDEMONS_FUN_NOT_OPENED = 130
    EXISTS_NICK_NAME = 208
    EXPLOIT = 17
    FAILED = 153
    FAILED_TOWN = 93
    FAILURE = 224
    FALLING = 155
    FAME = 4
    FATE = 188
    FATE_FUN_NOT_OPEN = 53
    FATE_INN_NOT_UPGRADE = 100
    FATE_PACK_FULL = 207
    FA_FANG = 169
    FA_GONG = 166
    FA_XIANG_NO_OPEN = 114
    FIND_IMMORTAL_FUN_NOT_OPEN = 51
    FISHING_NOT_OPEN = 79
    FIVE_BLESSINGS_FUN_NOT_OPEN = 77
    FIVE_ELEMENTS_FUN_NOT_OPEN = 74
    FIVE_ELEMENTS_STONE = 192
    FLOP_GAME_FUN_NOT_OPEN = 71
    FORBID = 212
    FORBIDDEN_NICKNAME = 210
    FUN_NOT_OPEN = 25
    GIFT_ID = 12
    GOLDEN_DAN = 193
    GRID_ID_ERROR = 219
    GRID_MAX_LIMIT = 220
    HAS_ACTIVATED_TOMB_ARTIFACTS = 138
    HAS_NO_CHENG_NIAN_CHILD = 105
    HAVE_JEWEL = 32
    HAVE_NO_ROLE_CAN_TO_SAGE = 66
    HAVE_SOUL = 31
    HOLDING = 156
    HORSE_SKILL = 199
    HORSE_SKILL_NOT_OPEN = 103
    INGOT = 2
    INSUFFICIENT_CARD = 150
    INSUFFICIENT_COIN = 147
    INSUFFICIENT_INGOT = 24
    INSUFFICIENT_YUPAI = 183
    IN_CAMP_WAR = 43
    IN_FACTION_WAR = 44
    IN_HEROES_WAR = 45
    IS_DAY_FALL = 133
    ITEM_ERROR = 215
    ITEM_ID = 19
    ITEM_LIST_REFRESHED = 151
    ITEM_LOCK = 144
    ITEM_NO_EXIST = 152
    JEWEL_FUN_NOT_OPEN = 75
    JOB_NOT_MATCH = 42
    JOB_STRENGTHEN = 200
    JOB_STRENGTHEN_NOT_OPEN = 110
    JUE_FANG = 170
    JUE_GONG = 167
    JULING_FUN_NO_OPEN = 81
    JUYUAN = 194
    JUYUAN_NO_OPEN = 86
    LINK_FATE_NO_OPEN = 84
    LINK_FATE_STONE_PACK_FULL = 85
    LIU_DAO_LUN_HUI_NOT_OPEN = 121
    LOST_DEPLOY_FUN_NOT_OPEN = 78
    LUN_HUN_NO_OPEN = 87
    MAGICARRAY_NO_OPEN = 124
    MAGIC_ARMS = 190
    MAGIC_ARMS_FUN_NOT_OPEN = 65
    MAGIC_WEAPON_NOT_OPEN = 102
    MAIN_ROLE_REBIRTH_NO_OPEN = 123
    MAIN_ROLE_SAINT_NO_OPEN = 94
    MATERIAL_NOT_ENOUGH = 22
    MAX_BUY_COUNT_LIMIT = 225
    MIRACLE_FIGHTERS = 196
    MIRACLE_FIGHTERS_TWO = 201
    MOUNT_FUN_NOT_OPEN = 52
    MOUNT_OR_SUIT_NO_OPEN = 89
    MOUNT_RUNE_FUNCTION_UNOPEN = 88
    MYSTIC_CAPTURE_NOT_OPEN = 139
    NIMBUS = 14
    NO = 1
    NOENOUGH_GRID = 184
    NOSUITEROLELEVEL = 160
    NOT_AWARD_ID = 222
    NOT_CHARGE_NUM = 134
    NOT_ELIXIR_ITEM = 26
    NOT_ELIXIR_VALUE = 27
    NOT_ENOUGH_ACTIVITY = 135
    NOT_ENOUGH_CHIP = 128
    NOT_ENOUGH_COIN = 116
    NOT_ENOUGH_DAY_COUNT = 175
    NOT_ENOUGH_EXPERIENCE = 115
    NOT_ENOUGH_FATE_GRID = 46
    NOT_ENOUGH_FIVE_ELEMENTS_PACK = 70
    NOT_ENOUGH_GRID = 41
    NOT_ENOUGH_ITEM = 171
    NOT_ENOUGH_LEVEL = 28
    NOT_ENOUGH_ONVERT_RES = 140
    NOT_ENOUGH_SOUL_GRID = 47
    NOT_ENOUGH_STATE_POINT = 174
    NOT_ENOUGH_STATE_POINT_LV = 177
    NOT_ENOUGH_TODAY_RECHARGE_INGOT = 120
    NOT_ENOUGH_VALUE = 132
    NOT_ENOUGH_VIP_LEVEL = 158
    NOT_ENOUGTH_EXP_ITEM = 129
    NOT_FRIEND = 223
    NOT_GAIN_GIFT = 131
    NOT_GRID = 172
    NOT_HAVE_ZHANG_MA_ZI = 68
    NOT_INVITE_ROLE = 60
    NOT_SELECTED = 206
    NOT_SUPERGIFT = 214
    NOUPGRADEQUEUE = 163
    NOVIPLEVEL = 164
    NO_ENOUGH = 226
    NO_ENOUGH_RESOURCE = 218
    NO_SUITE_EQUIP_TYPE = 35
    NO_SUITE_ROLE_JOB = 37
    NO_SUITE_ROLE_LEVEL = 36
    NO_THIS_DANCE = 104
    NO_TRANS_TIMES = 227
    NO_USE = 176
    NO_USE_AVATAR_CARD = 21
    NPC_ITEM_NO_EXIST = 149
    OPEN_NOT_ENOUGH_LEVEL = 118
    OPEN_NOT_ENOUGH_VIP_LEVEL = 117
    ORANGE_EQUIP = 187
    ORANGE_EQUIPMENT_FUN_NOT_OPEN = 91
    PACK_FULL = 23
    PAGE_ONE_LOCK = 221
    PARTNER_SOUL_ARRAY_NOT_OPEN = 141
    PARTNER_SOUL_NOT_OPEN = 101
    PLAYER_GRID_NO_EXIST = 29
    PLAYER_ROLE_NOT_EXIST = 34
    POWER = 10
    POWERFAME = 18
    POWER_FAME_NO_OPEN = 82
    PU_FANG = 168
    PU_GONG = 165
    RAISING = 154
    RECENTLY_CAN_BE_USED = 62
    RECYCLE_ITEM_EXPIRED = 146
    RECYCLE_ITEM_NO_EXIST = 145
    REFINE_POOL_UNOPEN = 92
    ROLE_NO_REJOIN = 61
    ROLE_POS_EQUI_EMPTY = 39
    ROLE_USED_ITEM = 69
    ROLL_CAKE_FUN_NOT_OPEN = 50
    SANT_WEAPON = 197
    SEAL_SOUL_NO_OPEN = 96
    SKILL = 8
    SKILL_BOOK_PACK_FULL = 217
    SOURCE_GRID_EMPTY = 30
    STATE_POINT = 6
    STONE = 5
    SUCCESS = 161
    TACTICS_NOT_OPEN = 108
    THE_SAME_NICK_NAME = 209
    TIAN_SHU_NO_OPEN = 83
    TIME_LIMIT = 126
    TODAY_HAS_USED = 136
    TOMB_ARTIFACTS_FUN_NO_OPEN = 137
    TOOLONG_NICKNAME = 211
    TOWER_FUN_NOT_OPEN = 49
    TOWN_NPC_ERROR = 173
    TYPE_ERROR = 229
    UNSUITED = 148
    UNUSABLE_ITEM = 40
    UN_AVALIABLE_GRID = 38
    WAIT_TO_USE = 125
    WAREHOUSE_FULL = 33
    WISH_BOX_NOT_EXIST = 228
    WRONG_ITEM = 181
    XIAN_LING = 9
    XU_YUAN_LI_JUAN_CANT_USE = 127
    YES = 0
    YIN_YANG_HALL_NOT_OPEN = 112
    YUPAI_NUMBER = 11
    YU_BAO = 195
    ZENG_FU_SHI_NOT_ENOUGHT = 142
    ZERO_CD_TIME = 157

@dataclass
class ItemGetItemBasicalInfosReq(BasePacket):
    """Item.get_item_basical_infos 请求封包 (Mod 2, Act 1)"""

    field_0: List[int]

    def __init__(self, field_0: List[int]) -> None:
        super().__init__(mod=2, act=1)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 复杂类型字段 field_0: ['IntUtil']
        writer.write_json(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetItemBasicalInfosReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_json()
        return cls(f_0)

@dataclass
class ItemGetItemBasicalInfosResp(BasePacket):
    """Item.get_item_basical_infos 应答封包 (Mod 2, Act 1)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, str]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, str]) -> None:
        super().__init__(mod=2, act=1)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetItemBasicalInfosResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemGetEmptyGridNumberReq(BasePacket):
    """Item.get_empty_grid_number 请求封包 (Mod 2, Act 2)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=2)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetEmptyGridNumberReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemGetEmptyGridNumberResp(BasePacket):
    """Item.get_empty_grid_number 应答封包 (Mod 2, Act 2)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=2)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetEmptyGridNumberResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemGetAllPlayerItemInfosReq(BasePacket):
    """Item.get_all_player_item_infos 请求封包 (Mod 2, Act 3)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=3)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetAllPlayerItemInfosReq":
        return cls()

@dataclass
class ItemGetAllPlayerItemInfosResp(BasePacket):
    """Item.get_all_player_item_infos 应答封包 (Mod 2, Act 3)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=3)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetAllPlayerItemInfosResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemChangeItemInfoSendToClientReq(BasePacket):
    """Item.change_item_info_send_to_client 请求封包 (Mod 2, Act 4)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=4)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemChangeItemInfoSendToClientReq":
        return cls()

@dataclass
class ItemChangeItemInfoSendToClientResp(BasePacket):
    """Item.change_item_info_send_to_client 应答封包 (Mod 2, Act 4)"""

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

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int, field_9: int, field_10: int, field_11: int, field_12: int, field_13: int, field_14: int, field_15: int, field_16: int, field_17: int, field_18: int, field_19: int, field_20: int) -> None:
        super().__init__(mod=2, act=4)
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

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int32(self.field_7)
        writer.write_int32(self.field_8)
        writer.write_int8(self.field_9)
        writer.write_int32(self.field_10)
        writer.write_int32(self.field_11)
        writer.write_int8(self.field_12)
        writer.write_int16(self.field_13)
        writer.write_int16(self.field_14)
        writer.write_int8(self.field_15)
        writer.write_int32(self.field_16)
        writer.write_int32(self.field_17)
        writer.write_int32(self.field_18)
        writer.write_int64(self.field_19)
        writer.write_int32(self.field_20)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemChangeItemInfoSendToClientResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        f_6 = reader.read_int32()
        f_7 = reader.read_int32()
        f_8 = reader.read_int32()
        f_9 = reader.read_int8()
        f_10 = reader.read_int32()
        f_11 = reader.read_int32()
        f_12 = reader.read_int8()
        f_13 = reader.read_int16()
        f_14 = reader.read_int16()
        f_15 = reader.read_int8()
        f_16 = reader.read_int32()
        f_17 = reader.read_int32()
        f_18 = reader.read_int32()
        f_19 = reader.read_int64()
        f_20 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11, f_12, f_13, f_14, f_15, f_16, f_17, f_18, f_19, f_20)

@dataclass
class ItemOpenNotifyReq(BasePacket):
    """Item.open_notify 请求封包 (Mod 2, Act 5)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=5)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemOpenNotifyReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemOpenNotifyResp(BasePacket):
    """Item.open_notify 应答封包 (Mod 2, Act 5)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=5)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemOpenNotifyResp":
        return cls()

@dataclass
class ItemGetPlayerGiftAllInfoReq(BasePacket):
    """Item.get_player_gift_all_info 请求封包 (Mod 2, Act 6)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=6)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerGiftAllInfoReq":
        return cls()

@dataclass
class ItemGetPlayerGiftAllInfoResp(BasePacket):
    """Item.get_player_gift_all_info 应答封包 (Mod 2, Act 6)"""

    field_0: Tuple[int, int, str, str, Tuple[int, int, int]]

    def __init__(self, field_0: Tuple[int, int, str, str, Tuple[int, int, int]]) -> None:
        super().__init__(mod=2, act=6)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerGiftAllInfoResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemGetFactureReelDataReq(BasePacket):
    """Item.get_facture_reel_data 请求封包 (Mod 2, Act 21)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=21)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetFactureReelDataReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class ItemGetFactureReelDataResp(BasePacket):
    """Item.get_facture_reel_data 应答封包 (Mod 2, Act 21)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: Tuple[int, int, str, int, int]
    field_5: int
    field_6: int
    field_7: int
    field_8: int
    field_9: int
    field_10: int
    field_11: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: Tuple[int, int, str, int, int], field_5: int, field_6: int, field_7: int, field_8: int, field_9: int, field_10: int, field_11: int) -> None:
        super().__init__(mod=2, act=21)
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
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        # 写入动态列表 field_4 (元素数 + 记录项)
        writer.write_uint16(len(self.field_4))
        for item_4 in self.field_4:
            writer.write_json(item_4)
        writer.write_int32(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int32(self.field_7)
        writer.write_int8(self.field_8)
        writer.write_int8(self.field_9)
        writer.write_int32(self.field_10)
        writer.write_int32(self.field_11)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetFactureReelDataResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        # 读取动态列表 f_4
        cnt_4 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_4 = []
        for _ in range(cnt_4):
            f_4.append(reader.read_json())
        f_5 = reader.read_int32()
        f_6 = reader.read_int32()
        f_7 = reader.read_int32()
        f_8 = reader.read_int8()
        f_9 = reader.read_int8()
        f_10 = reader.read_int32()
        f_11 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11)

@dataclass
class ItemGetPlayerRoleElixirDataReq(BasePacket):
    """Item.get_player_role_elixir_data 请求封包 (Mod 2, Act 22)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=22)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerRoleElixirDataReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemGetPlayerRoleElixirDataResp(BasePacket):
    """Item.get_player_role_elixir_data 应答封包 (Mod 2, Act 22)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=22)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerRoleElixirDataResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemAvatarCardOffReq(BasePacket):
    """Item.avatar_card_off 请求封包 (Mod 2, Act 25)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=25)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemAvatarCardOffReq":
        return cls()

@dataclass
class ItemAvatarCardOffResp(BasePacket):
    """Item.avatar_card_off 应答封包 (Mod 2, Act 25)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=25)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemAvatarCardOffResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemPlayerUseGridReelReq(BasePacket):
    """Item.player_use_grid_reel 请求封包 (Mod 2, Act 27)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=2, act=27)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int8(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerUseGridReelReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class ItemPlayerUseGridReelResp(BasePacket):
    """Item.player_use_grid_reel 应答封包 (Mod 2, Act 27)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=27)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        # 写入动态列表 field_3 (元素数 + 记录项)
        writer.write_uint16(len(self.field_3))
        for item_3 in self.field_3:
            writer.write_json(item_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerUseGridReelResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        # 读取动态列表 f_3
        cnt_3 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_3 = []
        for _ in range(cnt_3):
            f_3.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class ItemPlayerUseGridElixirReq(BasePacket):
    """Item.player_use_grid_elixir 请求封包 (Mod 2, Act 28)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=28)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerUseGridElixirReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemPlayerUseGridElixirResp(BasePacket):
    """Item.player_use_grid_elixir 应答封包 (Mod 2, Act 28)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=28)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerUseGridElixirResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemPlayerGetSuperGiftReq(BasePacket):
    """Item.player_get_super_gift 请求封包 (Mod 2, Act 29)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=29)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerGetSuperGiftReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemPlayerGetSuperGiftResp(BasePacket):
    """Item.player_get_super_gift 应答封包 (Mod 2, Act 29)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=29)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerGetSuperGiftResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemGetPlayerRoleElixirRecordReq(BasePacket):
    """Item.get_player_role_elixir_record 请求封包 (Mod 2, Act 30)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=30)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerRoleElixirRecordReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemGetPlayerRoleElixirRecordResp(BasePacket):
    """Item.get_player_role_elixir_record 应答封包 (Mod 2, Act 30)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int, int]]
    field_2: Tuple[int, int, int]
    field_3: int
    field_4: int
    field_5: int
    field_6: int

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int, int]], field_2: Tuple[int, int, int], field_3: int, field_4: int, field_5: int, field_6: int) -> None:
        super().__init__(mod=2, act=30)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5
        self.field_6 = field_6

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int32(self.field_6)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerRoleElixirRecordResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_json())
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        f_6 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6)

@dataclass
class ItemPlayerUseIngotElixirReq(BasePacket):
    """Item.player_use_ingot_elixir 请求封包 (Mod 2, Act 31)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=31)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerUseIngotElixirReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemPlayerUseIngotElixirResp(BasePacket):
    """Item.player_use_ingot_elixir 应答封包 (Mod 2, Act 31)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=31)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerUseIngotElixirResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemGetPlayerPackItemListReq(BasePacket):
    """Item.get_player_pack_item_list 请求封包 (Mod 2, Act 41)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=41)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerPackItemListReq":
        return cls()

@dataclass
class ItemGetPlayerPackItemListResp(BasePacket):
    """Item.get_player_pack_item_list 应答封包 (Mod 2, Act 41)"""

    field_0: int
    field_1: int
    field_2: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]
    field_3: int
    field_4: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: int, field_2: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int], field_3: int, field_4: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=41)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int32(self.field_1)
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        writer.write_int16(self.field_3)
        # 写入动态列表 field_4 (元素数 + 记录项)
        writer.write_uint16(len(self.field_4))
        for item_4 in self.field_4:
            writer.write_json(item_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerPackItemListResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int32()
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_json())
        f_3 = reader.read_int16()
        # 读取动态列表 f_4
        cnt_4 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_4 = []
        for _ in range(cnt_4):
            f_4.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class ItemGetPlayerWarehouseGridsReq(BasePacket):
    """Item.get_player_warehouse_grids 请求封包 (Mod 2, Act 42)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=42)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerWarehouseGridsReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemGetPlayerWarehouseGridsResp(BasePacket):
    """Item.get_player_warehouse_grids 应答封包 (Mod 2, Act 42)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=42)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int32(self.field_2)
        # 写入动态列表 field_3 (元素数 + 记录项)
        writer.write_uint16(len(self.field_3))
        for item_3 in self.field_3:
            writer.write_json(item_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerWarehouseGridsResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int16()
        f_2 = reader.read_int32()
        # 读取动态列表 f_3
        cnt_3 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_3 = []
        for _ in range(cnt_3):
            f_3.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class ItemGetRoleEquipListReq(BasePacket):
    """Item.get_role_equip_list 请求封包 (Mod 2, Act 43)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=43)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetRoleEquipListReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemGetRoleEquipListResp(BasePacket):
    """Item.get_role_equip_list 应答封包 (Mod 2, Act 43)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=43)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetRoleEquipListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemChangePackItemGridReq(BasePacket):
    """Item.change_pack_item_grid 请求封包 (Mod 2, Act 44)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=44)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemChangePackItemGridReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class ItemChangePackItemGridResp(BasePacket):
    """Item.change_pack_item_grid 应答封包 (Mod 2, Act 44)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=44)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemChangePackItemGridResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemChangeWarehouseItemGridReq(BasePacket):
    """Item.change_warehouse_item_grid 请求封包 (Mod 2, Act 45)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=45)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemChangeWarehouseItemGridReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class ItemChangeWarehouseItemGridResp(BasePacket):
    """Item.change_warehouse_item_grid 应答封包 (Mod 2, Act 45)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=45)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemChangeWarehouseItemGridResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemDropPackGridItemReq(BasePacket):
    """Item.drop_pack_grid_item 请求封包 (Mod 2, Act 46)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=46)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemDropPackGridItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        return cls(f_0)

@dataclass
class ItemDropPackGridItemResp(BasePacket):
    """Item.drop_pack_grid_item 应答封包 (Mod 2, Act 46)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=46)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemDropPackGridItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemDropWarehouseGridItemReq(BasePacket):
    """Item.drop_warehouse_grid_item 请求封包 (Mod 2, Act 47)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=47)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemDropWarehouseGridItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        return cls(f_0)

@dataclass
class ItemDropWarehouseGridItemResp(BasePacket):
    """Item.drop_warehouse_grid_item 应答封包 (Mod 2, Act 47)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=47)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemDropWarehouseGridItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemMoveWarehouseGridItemToPackReq(BasePacket):
    """Item.move_warehouse_grid_item_to_pack 请求封包 (Mod 2, Act 48)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=48)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMoveWarehouseGridItemToPackReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class ItemMoveWarehouseGridItemToPackResp(BasePacket):
    """Item.move_warehouse_grid_item_to_pack 应答封包 (Mod 2, Act 48)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=48)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMoveWarehouseGridItemToPackResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemMovePackGridItemToWarehouseReq(BasePacket):
    """Item.move_pack_grid_item_to_warehouse 请求封包 (Mod 2, Act 49)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=49)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMovePackGridItemToWarehouseReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class ItemMovePackGridItemToWarehouseResp(BasePacket):
    """Item.move_pack_grid_item_to_warehouse 应答封包 (Mod 2, Act 49)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=49)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMovePackGridItemToWarehouseResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemEquipPlayerRoleItemReq(BasePacket):
    """Item.equip_player_role_item 请求封包 (Mod 2, Act 50)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=2, act=50)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int16(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemEquipPlayerRoleItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int32()
        f_2 = reader.read_int16()
        return cls(f_0, f_1, f_2)

@dataclass
class ItemEquipPlayerRoleItemResp(BasePacket):
    """Item.equip_player_role_item 应答封包 (Mod 2, Act 50)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=50)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemEquipPlayerRoleItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemRemovePlayerRoleEquipmentReq(BasePacket):
    """Item.remove_player_role_equipment 请求封包 (Mod 2, Act 51)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=2, act=51)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int16(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemRemovePlayerRoleEquipmentReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int16()
        f_2 = reader.read_int16()
        return cls(f_0, f_1, f_2)

@dataclass
class ItemRemovePlayerRoleEquipmentResp(BasePacket):
    """Item.remove_player_role_equipment 应答封包 (Mod 2, Act 51)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=51)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemRemovePlayerRoleEquipmentResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemGetPlayerRoleEquipListReq(BasePacket):
    """Item.get_player_role_equip_list 请求封包 (Mod 2, Act 52)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=52)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerRoleEquipListReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemGetPlayerRoleEquipListResp(BasePacket):
    """Item.get_player_role_equip_list 应答封包 (Mod 2, Act 52)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=52)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerRoleEquipListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemPlayerUseGridItemReq(BasePacket):
    """Item.player_use_grid_item 请求封包 (Mod 2, Act 53)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=53)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerUseGridItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        return cls(f_0)

@dataclass
class ItemPlayerUseGridItemResp(BasePacket):
    """Item.player_use_grid_item 应答封包 (Mod 2, Act 53)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=53)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerUseGridItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemClassifyPackReq(BasePacket):
    """Item.classify_pack 请求封包 (Mod 2, Act 54)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=54)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 复杂类型字段 field_0: ['IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'ByteUtil', 'IntUtil', 'IntUtil', 'ByteUtil', 'ShortUtil', 'ShortUtil', 'ByteUtil', 'IntUtil']
        writer.write_json(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemClassifyPackReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_json()
        return cls(f_0)

@dataclass
class ItemClassifyPackResp(BasePacket):
    """Item.classify_pack 应答封包 (Mod 2, Act 54)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=54)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemClassifyPackResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemClassifyWarehouseReq(BasePacket):
    """Item.classify_warehouse 请求封包 (Mod 2, Act 55)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=55)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 复杂类型字段 field_0: ['IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'ByteUtil', 'IntUtil', 'IntUtil', 'ByteUtil', 'ShortUtil', 'ShortUtil', 'ByteUtil', 'IntUtil']
        writer.write_json(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemClassifyWarehouseReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_json()
        return cls(f_0)

@dataclass
class ItemClassifyWarehouseResp(BasePacket):
    """Item.classify_warehouse 应答封包 (Mod 2, Act 55)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=55)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemClassifyWarehouseResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemAddPackGridReq(BasePacket):
    """Item.add_pack_grid 请求封包 (Mod 2, Act 56)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=56)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemAddPackGridReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemAddPackGridResp(BasePacket):
    """Item.add_pack_grid 应答封包 (Mod 2, Act 56)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=2, act=56)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int16(self.field_2)
        writer.write_int16(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemAddPackGridResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int16()
        f_2 = reader.read_int16()
        f_3 = reader.read_int16()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class ItemAddWarehouseGridReq(BasePacket):
    """Item.add_warehouse_grid 请求封包 (Mod 2, Act 57)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=57)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemAddWarehouseGridReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemAddWarehouseGridResp(BasePacket):
    """Item.add_warehouse_grid 应答封包 (Mod 2, Act 57)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=2, act=57)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int16(self.field_2)
        writer.write_int16(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemAddWarehouseGridResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int16()
        f_2 = reader.read_int16()
        f_3 = reader.read_int16()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class ItemHasLevelGiftItemReq(BasePacket):
    """Item.has_level_gift_item 请求封包 (Mod 2, Act 58)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=58)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemHasLevelGiftItemReq":
        return cls()

@dataclass
class ItemHasLevelGiftItemResp(BasePacket):
    """Item.has_level_gift_item 应答封包 (Mod 2, Act 58)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=58)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemHasLevelGiftItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemHasMedicalItemReq(BasePacket):
    """Item.has_medical_item 请求封包 (Mod 2, Act 59)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=59)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemHasMedicalItemReq":
        return cls()

@dataclass
class ItemHasMedicalItemResp(BasePacket):
    """Item.has_medical_item 应答封包 (Mod 2, Act 59)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=2, act=59)
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
    def decode(cls, data: bytes) -> "ItemHasMedicalItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class ItemGetNpcItemListReq(BasePacket):
    """Item.get_npc_item_list 请求封包 (Mod 2, Act 71)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=71)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetNpcItemListReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemGetNpcItemListResp(BasePacket):
    """Item.get_npc_item_list 应答封包 (Mod 2, Act 71)"""

    field_0: int
    field_1: int
    field_2: List[int]

    def __init__(self, field_0: int, field_1: int, field_2: List[int]) -> None:
        super().__init__(mod=2, act=71)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_int32(item_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetNpcItemListResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_int32())
        return cls(f_0, f_1, f_2)

@dataclass
class ItemGetNpcRecycleItemListReq(BasePacket):
    """Item.get_npc_recycle_item_list 请求封包 (Mod 2, Act 72)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=72)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetNpcRecycleItemListReq":
        return cls()

@dataclass
class ItemGetNpcRecycleItemListResp(BasePacket):
    """Item.get_npc_recycle_item_list 应答封包 (Mod 2, Act 72)"""

    field_0: Tuple[int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=72)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetNpcRecycleItemListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemPlayerSellItemReq(BasePacket):
    """Item.player_sell_item 请求封包 (Mod 2, Act 73)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=73)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerSellItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        return cls(f_0)

@dataclass
class ItemPlayerSellItemResp(BasePacket):
    """Item.player_sell_item 应答封包 (Mod 2, Act 73)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]
    field_2: Tuple[int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int], field_2: Tuple[int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=73)
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
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerSellItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_json())
        return cls(f_0, f_1, f_2)

@dataclass
class ItemPlayerBuyBackItemReq(BasePacket):
    """Item.player_buy_back_item 请求封包 (Mod 2, Act 74)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=74)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerBuyBackItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class ItemPlayerBuyBackItemResp(BasePacket):
    """Item.player_buy_back_item 应答封包 (Mod 2, Act 74)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]
    field_2: Tuple[int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int], field_2: Tuple[int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=74)
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
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerBuyBackItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_json())
        return cls(f_0, f_1, f_2)

@dataclass
class ItemPlayerBuyNpcItemReq(BasePacket):
    """Item.player_buy_npc_item 请求封包 (Mod 2, Act 75)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=2, act=75)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int16(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerBuyNpcItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int16()
        return cls(f_0, f_1, f_2)

@dataclass
class ItemPlayerBuyNpcItemResp(BasePacket):
    """Item.player_buy_npc_item 应答封包 (Mod 2, Act 75)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=75)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerBuyNpcItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemLuckyShopItemListReq(BasePacket):
    """Item.lucky_shop_item_list 请求封包 (Mod 2, Act 76)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=76)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemLuckyShopItemListReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemLuckyShopItemListResp(BasePacket):
    """Item.lucky_shop_item_list 应答封包 (Mod 2, Act 76)"""

    field_0: Tuple[int, int]
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: Tuple[int, int], field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=2, act=76)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemLuckyShopItemListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class ItemLuckyShopRecordListReq(BasePacket):
    """Item.lucky_shop_record_list 请求封包 (Mod 2, Act 77)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=77)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemLuckyShopRecordListReq":
        return cls()

@dataclass
class ItemLuckyShopRecordListResp(BasePacket):
    """Item.lucky_shop_record_list 应答封包 (Mod 2, Act 77)"""

    field_0: Tuple[int, str, int, int]

    def __init__(self, field_0: Tuple[int, str, int, int]) -> None:
        super().__init__(mod=2, act=77)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemLuckyShopRecordListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemBuyLuckyShopItemReq(BasePacket):
    """Item.buy_lucky_shop_item 请求封包 (Mod 2, Act 78)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=78)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemBuyLuckyShopItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemBuyLuckyShopItemResp(BasePacket):
    """Item.buy_lucky_shop_item 应答封包 (Mod 2, Act 78)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=78)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemBuyLuckyShopItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemRefreshLuckyShopReq(BasePacket):
    """Item.refresh_lucky_shop 请求封包 (Mod 2, Act 79)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=79)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemRefreshLuckyShopReq":
        return cls()

@dataclass
class ItemRefreshLuckyShopResp(BasePacket):
    """Item.refresh_lucky_shop 应答封包 (Mod 2, Act 79)"""

    field_0: int
    field_1: Tuple[int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int]) -> None:
        super().__init__(mod=2, act=79)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemRefreshLuckyShopResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemPlayerBuyEquipItemReq(BasePacket):
    """Item.player_buy_equip_item 请求封包 (Mod 2, Act 80)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=2, act=80)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int16(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerBuyEquipItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int16()
        return cls(f_0, f_1, f_2)

@dataclass
class ItemPlayerBuyEquipItemResp(BasePacket):
    """Item.player_buy_equip_item 应答封包 (Mod 2, Act 80)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=2, act=80)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int64(self.field_2)
        writer.write_int32(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerBuyEquipItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int64()
        f_3 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class ItemGetEquipmentListReq(BasePacket):
    """Item.get_equipment_list 请求封包 (Mod 2, Act 91)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=91)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetEquipmentListReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemGetEquipmentListResp(BasePacket):
    """Item.get_equipment_list 应答封包 (Mod 2, Act 91)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=91)
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
    def decode(cls, data: bytes) -> "ItemGetEquipmentListResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemEquipUpgradeStatReq(BasePacket):
    """Item.equip_upgrade_stat 请求封包 (Mod 2, Act 92)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=92)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemEquipUpgradeStatReq":
        return cls()

@dataclass
class ItemEquipUpgradeStatResp(BasePacket):
    """Item.equip_upgrade_stat 应答封包 (Mod 2, Act 92)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=2, act=92)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_uint8(self.field_1)
        writer.write_int8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemEquipUpgradeStatResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_uint8()
        f_2 = reader.read_int8()
        return cls(f_0, f_1, f_2)

@dataclass
class ItemClearUpgradeCdTimeReq(BasePacket):
    """Item.clear_upgrade_cd_time 请求封包 (Mod 2, Act 94)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=94)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemClearUpgradeCdTimeReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemClearUpgradeCdTimeResp(BasePacket):
    """Item.clear_upgrade_cd_time 应答封包 (Mod 2, Act 94)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=94)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemClearUpgradeCdTimeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemOpenUpgradeOpportunityReq(BasePacket):
    """Item.open_upgrade_opportunity 请求封包 (Mod 2, Act 95)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=95)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemOpenUpgradeOpportunityReq":
        return cls()

@dataclass
class ItemOpenUpgradeOpportunityResp(BasePacket):
    """Item.open_upgrade_opportunity 应答封包 (Mod 2, Act 95)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=2, act=95)
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
    def decode(cls, data: bytes) -> "ItemOpenUpgradeOpportunityResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class ItemEquipUpgradeStatListReq(BasePacket):
    """Item.equip_upgrade_stat_list 请求封包 (Mod 2, Act 96)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=96)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemEquipUpgradeStatListReq":
        return cls()

@dataclass
class ItemEquipUpgradeStatListResp(BasePacket):
    """Item.equip_upgrade_stat_list 应答封包 (Mod 2, Act 96)"""

    field_0: int
    field_1: Tuple[int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int]) -> None:
        super().__init__(mod=2, act=96)
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
    def decode(cls, data: bytes) -> "ItemEquipUpgradeStatListResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemPlayerReelNeedItemReq(BasePacket):
    """Item.player_reel_need_item 请求封包 (Mod 2, Act 97)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=97)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerReelNeedItemReq":
        return cls()

@dataclass
class ItemPlayerReelNeedItemResp(BasePacket):
    """Item.player_reel_need_item 应答封包 (Mod 2, Act 97)"""

    field_0: Tuple[int, int, int, int, int]
    field_1: Tuple[int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int], field_1: Tuple[int, int]) -> None:
        super().__init__(mod=2, act=97)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerReelNeedItemResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemPlayerEquipUseReelReq(BasePacket):
    """Item.player_equip_use_reel 请求封包 (Mod 2, Act 98)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int) -> None:
        super().__init__(mod=2, act=98)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerEquipUseReelReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5)

@dataclass
class ItemPlayerEquipUseReelResp(BasePacket):
    """Item.player_equip_use_reel 应答封包 (Mod 2, Act 98)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=98)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        # 写入动态列表 field_3 (元素数 + 记录项)
        writer.write_uint16(len(self.field_3))
        for item_3 in self.field_3:
            writer.write_json(item_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerEquipUseReelResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        # 读取动态列表 f_3
        cnt_3 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_3 = []
        for _ in range(cnt_3):
            f_3.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class ItemGetPlayerItemFactureReelDataReq(BasePacket):
    """Item.get_player_item_facture_reel_data 请求封包 (Mod 2, Act 100)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=100)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerItemFactureReelDataReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemGetPlayerItemFactureReelDataResp(BasePacket):
    """Item.get_player_item_facture_reel_data 应答封包 (Mod 2, Act 100)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: Tuple[int, int, str, int, int]
    field_5: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: Tuple[int, int, str, int, int], field_5: int) -> None:
        super().__init__(mod=2, act=100)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        # 写入动态列表 field_4 (元素数 + 记录项)
        writer.write_uint16(len(self.field_4))
        for item_4 in self.field_4:
            writer.write_json(item_4)
        writer.write_int32(self.field_5)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerItemFactureReelDataResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        # 读取动态列表 f_4
        cnt_4 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_4 = []
        for _ in range(cnt_4):
            f_4.append(reader.read_json())
        f_5 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5)

@dataclass
class ItemPermanentCleanItemUpdateCdReq(BasePacket):
    """Item.permanent_clean_item_update_cd 请求封包 (Mod 2, Act 101)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=101)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemPermanentCleanItemUpdateCdReq":
        return cls()

@dataclass
class ItemPermanentCleanItemUpdateCdResp(BasePacket):
    """Item.permanent_clean_item_update_cd 应答封包 (Mod 2, Act 101)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=101)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPermanentCleanItemUpdateCdResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemGetPermanentCleanItemUpdateCdReq(BasePacket):
    """Item.get_permanent_clean_item_update_cd 请求封包 (Mod 2, Act 102)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=102)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPermanentCleanItemUpdateCdReq":
        return cls()

@dataclass
class ItemGetPermanentCleanItemUpdateCdResp(BasePacket):
    """Item.get_permanent_clean_item_update_cd 应答封包 (Mod 2, Act 102)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=102)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPermanentCleanItemUpdateCdResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemNotifySuperGiftItemsReq(BasePacket):
    """Item.notify_super_gift_items 请求封包 (Mod 2, Act 103)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=103)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemNotifySuperGiftItemsReq":
        return cls()

@dataclass
class ItemNotifySuperGiftItemsResp(BasePacket):
    """Item.notify_super_gift_items 应答封包 (Mod 2, Act 103)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int
    field_8: Tuple[int, int, int]
    field_9: Tuple[int, int]
    field_10: Tuple[int, int]
    field_11: List[int]
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
    field_24: Tuple[int, int]
    field_25: Tuple[int, int]
    field_26: int
    field_27: Tuple[int, int]
    field_28: Tuple[int, int]
    field_29: int
    field_30: int
    field_31: Tuple[int, int]
    field_32: Tuple[int, int]

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: Tuple[int, int, int], field_9: Tuple[int, int], field_10: Tuple[int, int], field_11: List[int], field_12: int, field_13: int, field_14: int, field_15: int, field_16: int, field_17: int, field_18: int, field_19: int, field_20: int, field_21: int, field_22: int, field_23: int, field_24: Tuple[int, int], field_25: Tuple[int, int], field_26: int, field_27: Tuple[int, int], field_28: Tuple[int, int], field_29: int, field_30: int, field_31: Tuple[int, int], field_32: Tuple[int, int]) -> None:
        super().__init__(mod=2, act=103)
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

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int32(self.field_7)
        # 写入动态列表 field_8 (元素数 + 记录项)
        writer.write_uint16(len(self.field_8))
        for item_8 in self.field_8:
            writer.write_json(item_8)
        # 写入动态列表 field_9 (元素数 + 记录项)
        writer.write_uint16(len(self.field_9))
        for item_9 in self.field_9:
            writer.write_json(item_9)
        # 写入动态列表 field_10 (元素数 + 记录项)
        writer.write_uint16(len(self.field_10))
        for item_10 in self.field_10:
            writer.write_json(item_10)
        # 写入动态列表 field_11 (元素数 + 记录项)
        writer.write_uint16(len(self.field_11))
        for item_11 in self.field_11:
            writer.write_int32(item_11)
        writer.write_int8(self.field_12)
        writer.write_int32(self.field_13)
        writer.write_int16(self.field_14)
        writer.write_int16(self.field_15)
        writer.write_int16(self.field_16)
        writer.write_int16(self.field_17)
        writer.write_int16(self.field_18)
        writer.write_int16(self.field_19)
        writer.write_int16(self.field_20)
        writer.write_int32(self.field_21)
        writer.write_int16(self.field_22)
        writer.write_int16(self.field_23)
        # 写入动态列表 field_24 (元素数 + 记录项)
        writer.write_uint16(len(self.field_24))
        for item_24 in self.field_24:
            writer.write_json(item_24)
        # 写入动态列表 field_25 (元素数 + 记录项)
        writer.write_uint16(len(self.field_25))
        for item_25 in self.field_25:
            writer.write_json(item_25)
        writer.write_int16(self.field_26)
        # 写入动态列表 field_27 (元素数 + 记录项)
        writer.write_uint16(len(self.field_27))
        for item_27 in self.field_27:
            writer.write_json(item_27)
        # 写入动态列表 field_28 (元素数 + 记录项)
        writer.write_uint16(len(self.field_28))
        for item_28 in self.field_28:
            writer.write_json(item_28)
        writer.write_int16(self.field_29)
        writer.write_int32(self.field_30)
        # 写入动态列表 field_31 (元素数 + 记录项)
        writer.write_uint16(len(self.field_31))
        for item_31 in self.field_31:
            writer.write_json(item_31)
        # 写入动态列表 field_32 (元素数 + 记录项)
        writer.write_uint16(len(self.field_32))
        for item_32 in self.field_32:
            writer.write_json(item_32)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemNotifySuperGiftItemsResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        f_6 = reader.read_int32()
        f_7 = reader.read_int32()
        # 读取动态列表 f_8
        cnt_8 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_8 = []
        for _ in range(cnt_8):
            f_8.append(reader.read_json())
        # 读取动态列表 f_9
        cnt_9 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_9 = []
        for _ in range(cnt_9):
            f_9.append(reader.read_json())
        # 读取动态列表 f_10
        cnt_10 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_10 = []
        for _ in range(cnt_10):
            f_10.append(reader.read_json())
        # 读取动态列表 f_11
        cnt_11 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_11 = []
        for _ in range(cnt_11):
            f_11.append(reader.read_int32())
        f_12 = reader.read_int8()
        f_13 = reader.read_int32()
        f_14 = reader.read_int16()
        f_15 = reader.read_int16()
        f_16 = reader.read_int16()
        f_17 = reader.read_int16()
        f_18 = reader.read_int16()
        f_19 = reader.read_int16()
        f_20 = reader.read_int16()
        f_21 = reader.read_int32()
        f_22 = reader.read_int16()
        f_23 = reader.read_int16()
        # 读取动态列表 f_24
        cnt_24 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_24 = []
        for _ in range(cnt_24):
            f_24.append(reader.read_json())
        # 读取动态列表 f_25
        cnt_25 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_25 = []
        for _ in range(cnt_25):
            f_25.append(reader.read_json())
        f_26 = reader.read_int16()
        # 读取动态列表 f_27
        cnt_27 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_27 = []
        for _ in range(cnt_27):
            f_27.append(reader.read_json())
        # 读取动态列表 f_28
        cnt_28 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_28 = []
        for _ in range(cnt_28):
            f_28.append(reader.read_json())
        f_29 = reader.read_int16()
        f_30 = reader.read_int32()
        # 读取动态列表 f_31
        cnt_31 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_31 = []
        for _ in range(cnt_31):
            f_31.append(reader.read_json())
        # 读取动态列表 f_32
        cnt_32 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_32 = []
        for _ in range(cnt_32):
            f_32.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11, f_12, f_13, f_14, f_15, f_16, f_17, f_18, f_19, f_20, f_21, f_22, f_23, f_24, f_25, f_26, f_27, f_28, f_29, f_30, f_31, f_32)

@dataclass
class ItemChangeAttackItemReq(BasePacket):
    """Item.change_attack_item 请求封包 (Mod 2, Act 104)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=2, act=104)
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
    def decode(cls, data: bytes) -> "ItemChangeAttackItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class ItemChangeAttackItemResp(BasePacket):
    """Item.change_attack_item 应答封包 (Mod 2, Act 104)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=104)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemChangeAttackItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemChangeAttackInfoReq(BasePacket):
    """Item.change_attack_info 请求封包 (Mod 2, Act 105)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=105)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemChangeAttackInfoReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemChangeAttackInfoResp(BasePacket):
    """Item.change_attack_info 应答封包 (Mod 2, Act 105)"""

    field_0: Tuple[int, int]

    def __init__(self, field_0: Tuple[int, int]) -> None:
        super().__init__(mod=2, act=105)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemChangeAttackInfoResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemGetSoulReq(BasePacket):
    """Item.get_soul 请求封包 (Mod 2, Act 106)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=106)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetSoulReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemGetSoulResp(BasePacket):
    """Item.get_soul 应答封包 (Mod 2, Act 106)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=106)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetSoulResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemGetTheItemNumReq(BasePacket):
    """Item.get_the_item_num 请求封包 (Mod 2, Act 107)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=107)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetTheItemNumReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemGetTheItemNumResp(BasePacket):
    """Item.get_the_item_num 应答封包 (Mod 2, Act 107)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=107)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetTheItemNumResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemCanChangeListReq(BasePacket):
    """Item.can_change_list 请求封包 (Mod 2, Act 108)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=108)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemCanChangeListReq":
        return cls()

@dataclass
class ItemCanChangeListResp(BasePacket):
    """Item.can_change_list 应答封包 (Mod 2, Act 108)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=108)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemCanChangeListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemGetGoldOilReq(BasePacket):
    """Item.get_gold_oil 请求封包 (Mod 2, Act 109)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=109)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetGoldOilReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemGetGoldOilResp(BasePacket):
    """Item.get_gold_oil 应答封包 (Mod 2, Act 109)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=109)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetGoldOilResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemCanUseGoldInfoReq(BasePacket):
    """Item.can_use_gold_info 请求封包 (Mod 2, Act 110)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=110)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemCanUseGoldInfoReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemCanUseGoldInfoResp(BasePacket):
    """Item.can_use_gold_info 应答封包 (Mod 2, Act 110)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=110)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemCanUseGoldInfoResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemUseGoldOilReq(BasePacket):
    """Item.use_gold_oil 请求封包 (Mod 2, Act 111)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=2, act=111)
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
    def decode(cls, data: bytes) -> "ItemUseGoldOilReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class ItemUseGoldOilResp(BasePacket):
    """Item.use_gold_oil 应答封包 (Mod 2, Act 111)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=111)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemUseGoldOilResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemTakeOffClothesReq(BasePacket):
    """Item.take_off_clothes 请求封包 (Mod 2, Act 112)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=112)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemTakeOffClothesReq":
        return cls()

@dataclass
class ItemTakeOffClothesResp(BasePacket):
    """Item.take_off_clothes 应答封包 (Mod 2, Act 112)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=112)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemTakeOffClothesResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemSwapCardReq(BasePacket):
    """Item.swap_card 请求封包 (Mod 2, Act 113)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=113)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemSwapCardReq":
        return cls()

@dataclass
class ItemSwapCardResp(BasePacket):
    """Item.swap_card 应答封包 (Mod 2, Act 113)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=113)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemSwapCardResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemTianDiYuPaiReq(BasePacket):
    """Item.tian_di_yu_pai 请求封包 (Mod 2, Act 114)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=114)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemTianDiYuPaiReq":
        return cls()

@dataclass
class ItemTianDiYuPaiResp(BasePacket):
    """Item.tian_di_yu_pai 应答封包 (Mod 2, Act 114)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=114)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemTianDiYuPaiResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemOpenFurnaceReq(BasePacket):
    """Item.open_furnace 请求封包 (Mod 2, Act 121)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=121)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemOpenFurnaceReq":
        return cls()

@dataclass
class ItemOpenFurnaceResp(BasePacket):
    """Item.open_furnace 应答封包 (Mod 2, Act 121)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=121)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemOpenFurnaceResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemDragFurnaceItemReq(BasePacket):
    """Item.drag_furnace_item 请求封包 (Mod 2, Act 122)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=122)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemDragFurnaceItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemDragFurnaceItemResp(BasePacket):
    """Item.drag_furnace_item 应答封包 (Mod 2, Act 122)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=122)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemDragFurnaceItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemGetYupaiInfoReq(BasePacket):
    """Item.get_yupai_info 请求封包 (Mod 2, Act 123)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=123)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetYupaiInfoReq":
        return cls()

@dataclass
class ItemGetYupaiInfoResp(BasePacket):
    """Item.get_yupai_info 应答封包 (Mod 2, Act 123)"""

    field_0: Tuple[int, int]

    def __init__(self, field_0: Tuple[int, int]) -> None:
        super().__init__(mod=2, act=123)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetYupaiInfoResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemGetYupaiNpcItemListReq(BasePacket):
    """Item.get_yupai_npc_item_list 请求封包 (Mod 2, Act 124)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=124)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetYupaiNpcItemListReq":
        return cls()

@dataclass
class ItemGetYupaiNpcItemListResp(BasePacket):
    """Item.get_yupai_npc_item_list 应答封包 (Mod 2, Act 124)"""

    field_0: List[int]
    field_1: List[int]
    field_2: List[int]
    field_3: Tuple[int, int]

    def __init__(self, field_0: List[int], field_1: List[int], field_2: List[int], field_3: Tuple[int, int]) -> None:
        super().__init__(mod=2, act=124)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_int32(item_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_int32(item_1)
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_int32(item_2)
        # 写入动态列表 field_3 (元素数 + 记录项)
        writer.write_uint16(len(self.field_3))
        for item_3 in self.field_3:
            writer.write_json(item_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetYupaiNpcItemListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_int32())
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_int32())
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_int32())
        # 读取动态列表 f_3
        cnt_3 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_3 = []
        for _ in range(cnt_3):
            f_3.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class ItemPlayerBuyYupaiNpcItemReq(BasePacket):
    """Item.player_buy_yupai_npc_item 请求封包 (Mod 2, Act 125)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=2, act=125)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int16(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerBuyYupaiNpcItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int16()
        f_2 = reader.read_int16()
        return cls(f_0, f_1, f_2)

@dataclass
class ItemPlayerBuyYupaiNpcItemResp(BasePacket):
    """Item.player_buy_yupai_npc_item 应答封包 (Mod 2, Act 125)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=125)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerBuyYupaiNpcItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemGetGiftDecipheKeyReq(BasePacket):
    """Item.get_gift_deciphe_key 请求封包 (Mod 2, Act 126)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=126)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetGiftDecipheKeyReq":
        return cls()

@dataclass
class ItemGetGiftDecipheKeyResp(BasePacket):
    """Item.get_gift_deciphe_key 应答封包 (Mod 2, Act 126)"""

    field_0: Tuple[int, str]

    def __init__(self, field_0: Tuple[int, str]) -> None:
        super().__init__(mod=2, act=126)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetGiftDecipheKeyResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemReplacePlayerRoleEquipReq(BasePacket):
    """Item.replace_player_role_equip 请求封包 (Mod 2, Act 127)"""

    field_0: int
    field_1: int
    field_2: List[int]

    def __init__(self, field_0: int, field_1: int, field_2: List[int]) -> None:
        super().__init__(mod=2, act=127)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        # 复杂类型字段 field_2: ['UByteUtil']
        writer.write_json(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemReplacePlayerRoleEquipReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_json()
        return cls(f_0, f_1, f_2)

@dataclass
class ItemReplacePlayerRoleEquipResp(BasePacket):
    """Item.replace_player_role_equip 应答封包 (Mod 2, Act 127)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=127)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemReplacePlayerRoleEquipResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemGetPlayerRoleReplaceInfoReq(BasePacket):
    """Item.get_player_role_replace_info 请求封包 (Mod 2, Act 128)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=128)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerRoleReplaceInfoReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemGetPlayerRoleReplaceInfoResp(BasePacket):
    """Item.get_player_role_replace_info 应答封包 (Mod 2, Act 128)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: List[int]
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

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: List[int], field_5: int, field_6: int, field_7: int, field_8: int, field_9: int, field_10: int, field_11: int, field_12: int, field_13: int, field_14: int, field_15: int, field_16: int, field_17: int, field_18: int, field_19: int, field_20: int, field_21: int) -> None:
        super().__init__(mod=2, act=128)
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

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int8(self.field_1)
        writer.write_int8(self.field_2)
        writer.write_int32(self.field_3)
        # 写入动态列表 field_4 (元素数 + 记录项)
        writer.write_uint16(len(self.field_4))
        for item_4 in self.field_4:
            writer.write_int32(item_4)
        writer.write_int8(self.field_5)
        writer.write_int8(self.field_6)
        writer.write_int16(self.field_7)
        writer.write_int8(self.field_8)
        writer.write_int8(self.field_9)
        writer.write_int32(self.field_10)
        writer.write_int8(self.field_11)
        writer.write_int32(self.field_12)
        writer.write_int32(self.field_13)
        writer.write_int8(self.field_14)
        writer.write_int8(self.field_15)
        writer.write_int32(self.field_16)
        writer.write_int32(self.field_17)
        writer.write_int32(self.field_18)
        writer.write_int8(self.field_19)
        writer.write_int32(self.field_20)
        writer.write_int32(self.field_21)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerRoleReplaceInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int8()
        f_2 = reader.read_int8()
        f_3 = reader.read_int32()
        # 读取动态列表 f_4
        cnt_4 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_4 = []
        for _ in range(cnt_4):
            f_4.append(reader.read_int32())
        f_5 = reader.read_int8()
        f_6 = reader.read_int8()
        f_7 = reader.read_int16()
        f_8 = reader.read_int8()
        f_9 = reader.read_int8()
        f_10 = reader.read_int32()
        f_11 = reader.read_int8()
        f_12 = reader.read_int32()
        f_13 = reader.read_int32()
        f_14 = reader.read_int8()
        f_15 = reader.read_int8()
        f_16 = reader.read_int32()
        f_17 = reader.read_int32()
        f_18 = reader.read_int32()
        f_19 = reader.read_int8()
        f_20 = reader.read_int32()
        f_21 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11, f_12, f_13, f_14, f_15, f_16, f_17, f_18, f_19, f_20, f_21)

@dataclass
class ItemPlayerRoleCanReplaceInfoReq(BasePacket):
    """Item.player_role_can_replace_info 请求封包 (Mod 2, Act 129)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=129)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerRoleCanReplaceInfoReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemPlayerRoleCanReplaceInfoResp(BasePacket):
    """Item.player_role_can_replace_info 应答封包 (Mod 2, Act 129)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: List[int]
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

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: List[int], field_5: int, field_6: int, field_7: int, field_8: int, field_9: int, field_10: int, field_11: int, field_12: int, field_13: int, field_14: int, field_15: int, field_16: int, field_17: int, field_18: int, field_19: int, field_20: int, field_21: int) -> None:
        super().__init__(mod=2, act=129)
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

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int8(self.field_1)
        writer.write_int8(self.field_2)
        writer.write_int32(self.field_3)
        # 写入动态列表 field_4 (元素数 + 记录项)
        writer.write_uint16(len(self.field_4))
        for item_4 in self.field_4:
            writer.write_int32(item_4)
        writer.write_int8(self.field_5)
        writer.write_int8(self.field_6)
        writer.write_int16(self.field_7)
        writer.write_int8(self.field_8)
        writer.write_int8(self.field_9)
        writer.write_int32(self.field_10)
        writer.write_int8(self.field_11)
        writer.write_int32(self.field_12)
        writer.write_int32(self.field_13)
        writer.write_int8(self.field_14)
        writer.write_int8(self.field_15)
        writer.write_int32(self.field_16)
        writer.write_int32(self.field_17)
        writer.write_int32(self.field_18)
        writer.write_int8(self.field_19)
        writer.write_int32(self.field_20)
        writer.write_int32(self.field_21)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerRoleCanReplaceInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int8()
        f_2 = reader.read_int8()
        f_3 = reader.read_int32()
        # 读取动态列表 f_4
        cnt_4 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_4 = []
        for _ in range(cnt_4):
            f_4.append(reader.read_int32())
        f_5 = reader.read_int8()
        f_6 = reader.read_int8()
        f_7 = reader.read_int16()
        f_8 = reader.read_int8()
        f_9 = reader.read_int8()
        f_10 = reader.read_int32()
        f_11 = reader.read_int8()
        f_12 = reader.read_int32()
        f_13 = reader.read_int32()
        f_14 = reader.read_int8()
        f_15 = reader.read_int8()
        f_16 = reader.read_int32()
        f_17 = reader.read_int32()
        f_18 = reader.read_int32()
        f_19 = reader.read_int8()
        f_20 = reader.read_int32()
        f_21 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11, f_12, f_13, f_14, f_15, f_16, f_17, f_18, f_19, f_20, f_21)

@dataclass
class ItemLargeUseGridItemReq(BasePacket):
    """Item.large_use_grid_item 请求封包 (Mod 2, Act 130)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=130)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemLargeUseGridItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemLargeUseGridItemResp(BasePacket):
    """Item.large_use_grid_item 应答封包 (Mod 2, Act 130)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=130)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemLargeUseGridItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemUseSetNicknameItemReq(BasePacket):
    """Item.use_set_nickname_item 请求封包 (Mod 2, Act 131)"""

    field_0: int
    field_1: str
    field_2: int

    def __init__(self, field_0: int, field_1: str, field_2: int) -> None:
        super().__init__(mod=2, act=131)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_uint8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemUseSetNicknameItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_uint8()
        return cls(f_0, f_1, f_2)

@dataclass
class ItemUseSetNicknameItemResp(BasePacket):
    """Item.use_set_nickname_item 应答封包 (Mod 2, Act 131)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]
    field_2: str

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int], field_2: str) -> None:
        super().__init__(mod=2, act=131)
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
        writer.write_utf(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemUseSetNicknameItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        f_2 = reader.read_utf()
        return cls(f_0, f_1, f_2)

@dataclass
class ItemUseSetRoleItemReq(BasePacket):
    """Item.use_set_role_item 请求封包 (Mod 2, Act 132)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=132)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemUseSetRoleItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemUseSetRoleItemResp(BasePacket):
    """Item.use_set_role_item 应答封包 (Mod 2, Act 132)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=132)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemUseSetRoleItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemPlayerUseSingleItemReq(BasePacket):
    """Item.player_use_single_item 请求封包 (Mod 2, Act 133)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=133)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerUseSingleItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        return cls(f_0)

@dataclass
class ItemPlayerUseSingleItemResp(BasePacket):
    """Item.player_use_single_item 应答封包 (Mod 2, Act 133)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=133)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerUseSingleItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemNotifyItemAttrPlusReq(BasePacket):
    """Item.notify_item_attr_plus 请求封包 (Mod 2, Act 134)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=134)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemNotifyItemAttrPlusReq":
        return cls()

@dataclass
class ItemNotifyItemAttrPlusResp(BasePacket):
    """Item.notify_item_attr_plus 应答封包 (Mod 2, Act 134)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int) -> None:
        super().__init__(mod=2, act=134)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int16(self.field_2)
        writer.write_int16(self.field_3)
        writer.write_int16(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemNotifyItemAttrPlusResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int16()
        f_3 = reader.read_int16()
        f_4 = reader.read_int16()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class ItemGetPlayerHomeWarehouseGridsReq(BasePacket):
    """Item.get_player_home_warehouse_grids 请求封包 (Mod 2, Act 135)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=135)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerHomeWarehouseGridsReq":
        return cls()

@dataclass
class ItemGetPlayerHomeWarehouseGridsResp(BasePacket):
    """Item.get_player_home_warehouse_grids 应答封包 (Mod 2, Act 135)"""

    field_0: int
    field_1: int
    field_2: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: int, field_2: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=135)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int16(self.field_1)
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerHomeWarehouseGridsResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int16()
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_json())
        return cls(f_0, f_1, f_2)

@dataclass
class ItemMoveHomeWarehouseGridItemToPackReq(BasePacket):
    """Item.move_home_warehouse_grid_item_to_pack 请求封包 (Mod 2, Act 136)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=136)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMoveHomeWarehouseGridItemToPackReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class ItemMoveHomeWarehouseGridItemToPackResp(BasePacket):
    """Item.move_home_warehouse_grid_item_to_pack 应答封包 (Mod 2, Act 136)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=136)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMoveHomeWarehouseGridItemToPackResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemMovePackGridItemToHomeWarehouseReq(BasePacket):
    """Item.move_pack_grid_item_to_home_warehouse 请求封包 (Mod 2, Act 137)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=137)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMovePackGridItemToHomeWarehouseReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class ItemMovePackGridItemToHomeWarehouseResp(BasePacket):
    """Item.move_pack_grid_item_to_home_warehouse 应答封包 (Mod 2, Act 137)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=137)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMovePackGridItemToHomeWarehouseResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemClassifyHomeWarehouseReq(BasePacket):
    """Item.classify_home_warehouse 请求封包 (Mod 2, Act 148)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=148)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 复杂类型字段 field_0: ['IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'ByteUtil', 'IntUtil', 'IntUtil', 'ByteUtil', 'ShortUtil', 'ShortUtil', 'ByteUtil', 'IntUtil']
        writer.write_json(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemClassifyHomeWarehouseReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_json()
        return cls(f_0)

@dataclass
class ItemClassifyHomeWarehouseResp(BasePacket):
    """Item.classify_home_warehouse 应答封包 (Mod 2, Act 148)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=148)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemClassifyHomeWarehouseResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemChangeHomeWarehouseItemGridReq(BasePacket):
    """Item.change_home_warehouse_item_grid 请求封包 (Mod 2, Act 149)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=149)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemChangeHomeWarehouseItemGridReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class ItemChangeHomeWarehouseItemGridResp(BasePacket):
    """Item.change_home_warehouse_item_grid 应答封包 (Mod 2, Act 149)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=149)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemChangeHomeWarehouseItemGridResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemDropHomeWarehouseGridItemReq(BasePacket):
    """Item.drop_home_warehouse_grid_item 请求封包 (Mod 2, Act 150)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=150)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemDropHomeWarehouseGridItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        return cls(f_0)

@dataclass
class ItemDropHomeWarehouseGridItemResp(BasePacket):
    """Item.drop_home_warehouse_grid_item 应答封包 (Mod 2, Act 150)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=150)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemDropHomeWarehouseGridItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemPlayerUseRandomItemReq(BasePacket):
    """Item.player_use_random_item 请求封包 (Mod 2, Act 151)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=151)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerUseRandomItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemPlayerUseRandomItemResp(BasePacket):
    """Item.player_use_random_item 应答封包 (Mod 2, Act 151)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]
    field_2: int

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int], field_2: int) -> None:
        super().__init__(mod=2, act=151)
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
    def decode(cls, data: bytes) -> "ItemPlayerUseRandomItemResp":
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
class ItemGetPlayerSupergiftWarehouseGridsReq(BasePacket):
    """Item.get_player_supergift_warehouse_grids 请求封包 (Mod 2, Act 152)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=152)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerSupergiftWarehouseGridsReq":
        return cls()

@dataclass
class ItemGetPlayerSupergiftWarehouseGridsResp(BasePacket):
    """Item.get_player_supergift_warehouse_grids 应答封包 (Mod 2, Act 152)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=152)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerSupergiftWarehouseGridsResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemMoveSupergiftWarehouseGridItemToPackReq(BasePacket):
    """Item.move_supergift_warehouse_grid_item_to_pack 请求封包 (Mod 2, Act 153)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=153)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMoveSupergiftWarehouseGridItemToPackReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class ItemMoveSupergiftWarehouseGridItemToPackResp(BasePacket):
    """Item.move_supergift_warehouse_grid_item_to_pack 应答封包 (Mod 2, Act 153)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=153)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMoveSupergiftWarehouseGridItemToPackResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemMovePackGridItemToSupergiftWarehouseReq(BasePacket):
    """Item.move_pack_grid_item_to_supergift_warehouse 请求封包 (Mod 2, Act 154)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=154)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMovePackGridItemToSupergiftWarehouseReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class ItemMovePackGridItemToSupergiftWarehouseResp(BasePacket):
    """Item.move_pack_grid_item_to_supergift_warehouse 应答封包 (Mod 2, Act 154)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=154)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMovePackGridItemToSupergiftWarehouseResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemClassifySupergiftWarehouseReq(BasePacket):
    """Item.classify_supergift_warehouse 请求封包 (Mod 2, Act 155)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=155)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 复杂类型字段 field_0: ['IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'ByteUtil', 'IntUtil', 'IntUtil', 'ByteUtil', 'ShortUtil', 'ShortUtil', 'ByteUtil', 'IntUtil']
        writer.write_json(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemClassifySupergiftWarehouseReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_json()
        return cls(f_0)

@dataclass
class ItemClassifySupergiftWarehouseResp(BasePacket):
    """Item.classify_supergift_warehouse 应答封包 (Mod 2, Act 155)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=155)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemClassifySupergiftWarehouseResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemChangeSupergiftWarehouseItemGridReq(BasePacket):
    """Item.change_supergift_warehouse_item_grid 请求封包 (Mod 2, Act 156)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=156)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemChangeSupergiftWarehouseItemGridReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class ItemChangeSupergiftWarehouseItemGridResp(BasePacket):
    """Item.change_supergift_warehouse_item_grid 应答封包 (Mod 2, Act 156)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=156)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemChangeSupergiftWarehouseItemGridResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemUseDingJiJiNengShuZiXuanBaoReq(BasePacket):
    """Item.use_ding_ji_ji_neng_shu_zi_xuan_bao 请求封包 (Mod 2, Act 157)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=157)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemUseDingJiJiNengShuZiXuanBaoReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemUseDingJiJiNengShuZiXuanBaoResp(BasePacket):
    """Item.use_ding_ji_ji_neng_shu_zi_xuan_bao 应答封包 (Mod 2, Act 157)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=157)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemUseDingJiJiNengShuZiXuanBaoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemExpandPageTwoGridReq(BasePacket):
    """Item.expand_page_two_grid 请求封包 (Mod 2, Act 158)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=158)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemExpandPageTwoGridReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        return cls(f_0)

@dataclass
class ItemExpandPageTwoGridResp(BasePacket):
    """Item.expand_page_two_grid 应答封包 (Mod 2, Act 158)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=158)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int16(self.field_2)
        # 写入动态列表 field_3 (元素数 + 记录项)
        writer.write_uint16(len(self.field_3))
        for item_3 in self.field_3:
            writer.write_json(item_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemExpandPageTwoGridResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int16()
        f_2 = reader.read_int16()
        # 读取动态列表 f_3
        cnt_3 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_3 = []
        for _ in range(cnt_3):
            f_3.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class ItemPlayerUseGridItemNeedChooseReq(BasePacket):
    """Item.player_use_grid_item_need_choose 请求封包 (Mod 2, Act 159)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=159)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerUseGridItemNeedChooseReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        return cls(f_0)

@dataclass
class ItemPlayerUseGridItemNeedChooseResp(BasePacket):
    """Item.player_use_grid_item_need_choose 应答封包 (Mod 2, Act 159)"""

    field_0: int
    field_1: Tuple[int, int, int]
    field_2: int

    def __init__(self, field_0: int, field_1: Tuple[int, int, int], field_2: int) -> None:
        super().__init__(mod=2, act=159)
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
    def decode(cls, data: bytes) -> "ItemPlayerUseGridItemNeedChooseResp":
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
class ItemUseChooseBoxReq(BasePacket):
    """Item.use_choose_box 请求封包 (Mod 2, Act 160)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=160)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemUseChooseBoxReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemUseChooseBoxResp(BasePacket):
    """Item.use_choose_box 应答封包 (Mod 2, Act 160)"""

    field_0: int
    field_1: Tuple[int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int]) -> None:
        super().__init__(mod=2, act=160)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemUseChooseBoxResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemGetYunNiangItemsReq(BasePacket):
    """Item.get_yun_niang_items 请求封包 (Mod 2, Act 161)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=161)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetYunNiangItemsReq":
        return cls()

@dataclass
class ItemGetYunNiangItemsResp(BasePacket):
    """Item.get_yun_niang_items 应答封包 (Mod 2, Act 161)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int]
    field_2: Tuple[int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int], field_2: Tuple[int, int]) -> None:
        super().__init__(mod=2, act=161)
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
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetYunNiangItemsResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_json())
        return cls(f_0, f_1, f_2)

@dataclass
class ItemBuyYunNiangItemReq(BasePacket):
    """Item.buy_yun_niang_item 请求封包 (Mod 2, Act 162)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=162)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemBuyYunNiangItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemBuyYunNiangItemResp(BasePacket):
    """Item.buy_yun_niang_item 应答封包 (Mod 2, Act 162)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=162)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        # 写入动态列表 field_3 (元素数 + 记录项)
        writer.write_uint16(len(self.field_3))
        for item_3 in self.field_3:
            writer.write_json(item_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemBuyYunNiangItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        # 读取动态列表 f_3
        cnt_3 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_3 = []
        for _ in range(cnt_3):
            f_3.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class ItemGetPlayerFriendshipWarehouseGridsReq(BasePacket):
    """Item.get_player_friendship_warehouse_grids 请求封包 (Mod 2, Act 163)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=163)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerFriendshipWarehouseGridsReq":
        return cls()

@dataclass
class ItemGetPlayerFriendshipWarehouseGridsResp(BasePacket):
    """Item.get_player_friendship_warehouse_grids 应答封包 (Mod 2, Act 163)"""

    field_0: int
    field_1: int
    field_2: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: int, field_2: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=163)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int16(self.field_1)
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerFriendshipWarehouseGridsResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int16()
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_json())
        return cls(f_0, f_1, f_2)

@dataclass
class ItemMoveFriendshipWarehouseGridItemToPackReq(BasePacket):
    """Item.move_friendship_warehouse_grid_item_to_pack 请求封包 (Mod 2, Act 164)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=164)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMoveFriendshipWarehouseGridItemToPackReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class ItemMoveFriendshipWarehouseGridItemToPackResp(BasePacket):
    """Item.move_friendship_warehouse_grid_item_to_pack 应答封包 (Mod 2, Act 164)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=164)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMoveFriendshipWarehouseGridItemToPackResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemMovePackGridItemToFriendshipWarehouseReq(BasePacket):
    """Item.move_pack_grid_item_to_friendship_warehouse 请求封包 (Mod 2, Act 165)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=165)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMovePackGridItemToFriendshipWarehouseReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class ItemMovePackGridItemToFriendshipWarehouseResp(BasePacket):
    """Item.move_pack_grid_item_to_friendship_warehouse 应答封包 (Mod 2, Act 165)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=165)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMovePackGridItemToFriendshipWarehouseResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemClassifyFriendshipWarehouseReq(BasePacket):
    """Item.classify_friendship_warehouse 请求封包 (Mod 2, Act 166)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=166)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 复杂类型字段 field_0: ['IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'IntUtil', 'ByteUtil', 'IntUtil', 'IntUtil', 'ByteUtil', 'ShortUtil', 'ShortUtil', 'ByteUtil', 'IntUtil']
        writer.write_json(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemClassifyFriendshipWarehouseReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_json()
        return cls(f_0)

@dataclass
class ItemClassifyFriendshipWarehouseResp(BasePacket):
    """Item.classify_friendship_warehouse 应答封包 (Mod 2, Act 166)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=166)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemClassifyFriendshipWarehouseResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemChangeFriendshipWarehouseItemGridReq(BasePacket):
    """Item.change_friendship_warehouse_item_grid 请求封包 (Mod 2, Act 167)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=167)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemChangeFriendshipWarehouseItemGridReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class ItemChangeFriendshipWarehouseItemGridResp(BasePacket):
    """Item.change_friendship_warehouse_item_grid 应答封包 (Mod 2, Act 167)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=167)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemChangeFriendshipWarehouseItemGridResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemDropFriendshipWarehouseGridItemReq(BasePacket):
    """Item.drop_friendship_warehouse_grid_item 请求封包 (Mod 2, Act 168)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=168)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemDropFriendshipWarehouseGridItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        return cls(f_0)

@dataclass
class ItemDropFriendshipWarehouseGridItemResp(BasePacket):
    """Item.drop_friendship_warehouse_grid_item 应答封包 (Mod 2, Act 168)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=168)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemDropFriendshipWarehouseGridItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemPlayerRefreshGridItemNeedChooseReq(BasePacket):
    """Item.player_refresh_grid_item_need_choose 请求封包 (Mod 2, Act 169)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=169)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerRefreshGridItemNeedChooseReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        return cls(f_0)

@dataclass
class ItemPlayerRefreshGridItemNeedChooseResp(BasePacket):
    """Item.player_refresh_grid_item_need_choose 应答封包 (Mod 2, Act 169)"""

    field_0: int
    field_1: Tuple[int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int]) -> None:
        super().__init__(mod=2, act=169)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerRefreshGridItemNeedChooseResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemPlayerBatchGridItemReq(BasePacket):
    """Item.player_batch_grid_item 请求封包 (Mod 2, Act 170)"""

    field_0: List[int]

    def __init__(self, field_0: List[int]) -> None:
        super().__init__(mod=2, act=170)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 复杂类型字段 field_0: ['IntUtil']
        writer.write_json(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerBatchGridItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_json()
        return cls(f_0)

@dataclass
class ItemPlayerBatchGridItemResp(BasePacket):
    """Item.player_batch_grid_item 应答封包 (Mod 2, Act 170)"""

    field_0: int
    field_1: List[int]
    field_2: Tuple[int, int]

    def __init__(self, field_0: int, field_1: List[int], field_2: Tuple[int, int]) -> None:
        super().__init__(mod=2, act=170)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_int32(item_1)
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerBatchGridItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_int32())
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_json())
        return cls(f_0, f_1, f_2)

@dataclass
class ItemElixirTransformPanelReq(BasePacket):
    """Item.elixir_transform_panel 请求封包 (Mod 2, Act 171)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=171)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemElixirTransformPanelReq":
        return cls()

@dataclass
class ItemElixirTransformPanelResp(BasePacket):
    """Item.elixir_transform_panel 应答封包 (Mod 2, Act 171)"""

    field_0: int
    field_1: Tuple[int, int, int]
    field_2: int

    def __init__(self, field_0: int, field_1: Tuple[int, int, int], field_2: int) -> None:
        super().__init__(mod=2, act=171)
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
    def decode(cls, data: bytes) -> "ItemElixirTransformPanelResp":
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
class ItemElixirTransformReq(BasePacket):
    """Item.elixir_transform 请求封包 (Mod 2, Act 172)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=172)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemElixirTransformReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemElixirTransformResp(BasePacket):
    """Item.elixir_transform 应答封包 (Mod 2, Act 172)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=172)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemElixirTransformResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemGetPearlPrivilegeInfoReq(BasePacket):
    """Item.get_pearl_privilege_info 请求封包 (Mod 2, Act 173)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=173)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPearlPrivilegeInfoReq":
        return cls()

@dataclass
class ItemGetPearlPrivilegeInfoResp(BasePacket):
    """Item.get_pearl_privilege_info 应答封包 (Mod 2, Act 173)"""

    field_0: Tuple[int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=173)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPearlPrivilegeInfoResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemExchangePearlPrivilegeReq(BasePacket):
    """Item.exchange_pearl_privilege 请求封包 (Mod 2, Act 174)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=174)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemExchangePearlPrivilegeReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        return cls(f_0)

@dataclass
class ItemExchangePearlPrivilegeResp(BasePacket):
    """Item.exchange_pearl_privilege 应答封包 (Mod 2, Act 174)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=2, act=174)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemExchangePearlPrivilegeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemGetMemoryItemInfoReq(BasePacket):
    """Item.get_memory_item_info 请求封包 (Mod 2, Act 175)"""

    def __init__(self) -> None:
        super().__init__(mod=2, act=175)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetMemoryItemInfoReq":
        return cls()

@dataclass
class ItemGetMemoryItemInfoResp(BasePacket):
    """Item.get_memory_item_info 应答封包 (Mod 2, Act 175)"""

    field_0: Tuple[int, int]

    def __init__(self, field_0: Tuple[int, int]) -> None:
        super().__init__(mod=2, act=175)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetMemoryItemInfoResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class ItemSelectWishBoxTypeReq(BasePacket):
    """Item.select_wish_box_type 请求封包 (Mod 2, Act 176)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=176)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemSelectWishBoxTypeReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemSelectWishBoxTypeResp(BasePacket):
    """Item.select_wish_box_type 应答封包 (Mod 2, Act 176)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=176)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemSelectWishBoxTypeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class ItemMingWenChangePanelReq(BasePacket):
    """Item.ming_wen_change_panel 请求封包 (Mod 2, Act 177)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=177)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMingWenChangePanelReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class ItemMingWenChangePanelResp(BasePacket):
    """Item.ming_wen_change_panel 应答封包 (Mod 2, Act 177)"""

    field_0: int
    field_1: Tuple[int, int, int, Tuple[int, int]]

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, Tuple[int, int]]) -> None:
        super().__init__(mod=2, act=177)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMingWenChangePanelResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class ItemMingWenChangeReq(BasePacket):
    """Item.ming_wen_change 请求封包 (Mod 2, Act 178)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=2, act=178)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMingWenChangeReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class ItemMingWenChangeResp(BasePacket):
    """Item.ming_wen_change 应答封包 (Mod 2, Act 178)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=2, act=178)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMingWenChangeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)
