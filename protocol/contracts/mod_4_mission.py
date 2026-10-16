"""神仙道 Mission 模块协议代码契约 (Mod 4)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_Mission_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class MissionConstants:
    """Mission 模块业务状态与行为常量"""

    ADDON_STUNT = 1
    ALREADY_GOT = 42
    AWARD_BOX_NO_OPEN = 20
    BACK_ATTACK = 6
    BE_ADDON_STUNT = 3
    BE_STUNT = 2
    COIN = 26
    FAILED = 29
    FAILURE = 46
    HASCHALLENGED = 30
    INGOT = 27
    LESS_POWER = 18
    MAGIC_ATTACK = 7
    MISSION_ID_ERROR = 47
    MS_ALREADY_CLICK = 32
    MS_ALREADY_DO = 35
    MS_ERROR_MISSION = 31
    MS_FAILURE = 34
    MS_MONSTER = 37
    MS_NOBODY = 38
    MS_PAPER = 14
    MS_PLAYER = 36
    MS_SCISSOR = 12
    MS_STONE = 13
    MS_SUCCESS = 33
    NORMAL_ATTACK = 4
    NO_BOX_TO_OPEN = 39
    NO_ENOUGH_STAR = 41
    NO_TRUNK_MISSION = 40
    NO_TRUNK_MISSION_COMPLETE = 43
    NO_UNLOCK = 48
    PACK_FULL = 22
    PICKUP_FAILED = 24
    PICKUP_SUCCESS = 23
    PRE_ATTACK = 5
    PRE_TRUNK_MISSION_NO_COMPLETE = 21
    REFIGHT = 11
    REPICKUP = 25
    SCORE_A = 15
    SCORE_B = 16
    SCORE_C = 17
    SEC_CHANGE = 9
    SELF_STUNT = 0
    SKILL = 28
    STUNT_ATTACK = 8
    SUCCESS = 10
    TRUNK_ALREADY_FIGHT = 19
    ZHIXIAN_BUFF = 44
    ZHUXIAN_BUFF = 45

@dataclass
class MissionGetSectionsReq(BasePacket):
    """Mission.get_sections 请求封包 (Mod 4, Act 0)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=0)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetSectionsReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class MissionGetSectionsResp(BasePacket):
    """Mission.get_sections 应答封包 (Mod 4, Act 0)"""

    field_0: Tuple[int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int]) -> None:
        super().__init__(mod=4, act=0)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetSectionsResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class MissionEnterMissionReq(BasePacket):
    """Mission.enter_mission 请求封包 (Mod 4, Act 1)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=1)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionEnterMissionReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class MissionEnterMissionResp(BasePacket):
    """Mission.enter_mission 应答封包 (Mod 4, Act 1)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: List[int]
    field_7: List[int]

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: List[int], field_7: List[int]) -> None:
        super().__init__(mod=4, act=1)
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
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int8(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        # 写入动态列表 field_6 (元素数 + 记录项)
        writer.write_uint16(len(self.field_6))
        for item_6 in self.field_6:
            writer.write_int32(item_6)
        # 写入动态列表 field_7 (元素数 + 记录项)
        writer.write_uint16(len(self.field_7))
        for item_7 in self.field_7:
            writer.write_int32(item_7)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionEnterMissionResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int8()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        # 读取动态列表 f_6
        cnt_6 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_6 = []
        for _ in range(cnt_6):
            f_6.append(reader.read_int32())
        # 读取动态列表 f_7
        cnt_7 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_7 = []
        for _ in range(cnt_7):
            f_7.append(reader.read_int32())
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7)

@dataclass
class MissionFightMonsterReq(BasePacket):
    """Mission.fight_monster 请求封包 (Mod 4, Act 2)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=4, act=2)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int8(self.field_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionFightMonsterReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int8()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class MissionFightMonsterResp(BasePacket):
    """Mission.fight_monster 应答封包 (Mod 4, Act 2)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int]
    field_4: Tuple[int, int, int]
    field_5: Tuple[int, int]
    field_6: Tuple[int, int]
    field_7: Tuple[Tuple[str, Tuple[int, str, int, int, int, int, int, int, int, int, int, int, int, int, int, int]], Tuple[str, Tuple[int, str, int, int, int, int, int, int, int, int, int, int, int, int, int, int]]]
    field_8: int
    field_9: int
    field_10: int
    field_11: int
    field_12: int
    field_13: int
    field_14: Tuple[int, int]
    field_15: int
    field_16: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int], field_4: Tuple[int, int, int], field_5: Tuple[int, int], field_6: Tuple[int, int], field_7: Tuple[Tuple[str, Tuple[int, str, int, int, int, int, int, int, int, int, int, int, int, int, int, int]], Tuple[str, Tuple[int, str, int, int, int, int, int, int, int, int, int, int, int, int, int, int]]], field_8: int, field_9: int, field_10: int, field_11: int, field_12: int, field_13: int, field_14: Tuple[int, int], field_15: int, field_16: int) -> None:
        super().__init__(mod=4, act=2)
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

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int8(self.field_2)
        # 写入动态列表 field_3 (元素数 + 记录项)
        writer.write_uint16(len(self.field_3))
        for item_3 in self.field_3:
            writer.write_json(item_3)
        # 写入动态列表 field_4 (元素数 + 记录项)
        writer.write_uint16(len(self.field_4))
        for item_4 in self.field_4:
            writer.write_json(item_4)
        # 写入动态列表 field_5 (元素数 + 记录项)
        writer.write_uint16(len(self.field_5))
        for item_5 in self.field_5:
            writer.write_json(item_5)
        # 写入动态列表 field_6 (元素数 + 记录项)
        writer.write_uint16(len(self.field_6))
        for item_6 in self.field_6:
            writer.write_json(item_6)
        # 写入动态列表 field_7 (元素数 + 记录项)
        writer.write_uint16(len(self.field_7))
        for item_7 in self.field_7:
            writer.write_json(item_7)
        writer.write_int32(self.field_8)
        writer.write_uint8(self.field_9)
        writer.write_int16(self.field_10)
        writer.write_int16(self.field_11)
        writer.write_int32(self.field_12)
        writer.write_int32(self.field_13)
        # 写入动态列表 field_14 (元素数 + 记录项)
        writer.write_uint16(len(self.field_14))
        for item_14 in self.field_14:
            writer.write_json(item_14)
        writer.write_int16(self.field_15)
        writer.write_uint8(self.field_16)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionFightMonsterResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int8()
        # 读取动态列表 f_3
        cnt_3 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_3 = []
        for _ in range(cnt_3):
            f_3.append(reader.read_json())
        # 读取动态列表 f_4
        cnt_4 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_4 = []
        for _ in range(cnt_4):
            f_4.append(reader.read_json())
        # 读取动态列表 f_5
        cnt_5 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_5 = []
        for _ in range(cnt_5):
            f_5.append(reader.read_json())
        # 读取动态列表 f_6
        cnt_6 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_6 = []
        for _ in range(cnt_6):
            f_6.append(reader.read_json())
        # 读取动态列表 f_7
        cnt_7 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_7 = []
        for _ in range(cnt_7):
            f_7.append(reader.read_json())
        f_8 = reader.read_int32()
        f_9 = reader.read_uint8()
        f_10 = reader.read_int16()
        f_11 = reader.read_int16()
        f_12 = reader.read_int32()
        f_13 = reader.read_int32()
        # 读取动态列表 f_14
        cnt_14 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_14 = []
        for _ in range(cnt_14):
            f_14.append(reader.read_json())
        f_15 = reader.read_int16()
        f_16 = reader.read_uint8()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11, f_12, f_13, f_14, f_15, f_16)

@dataclass
class MissionRankMissionReq(BasePacket):
    """Mission.rank_mission 请求封包 (Mod 4, Act 3)"""

    def __init__(self) -> None:
        super().__init__(mod=4, act=3)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionRankMissionReq":
        return cls()

@dataclass
class MissionRankMissionResp(BasePacket):
    """Mission.rank_mission 应答封包 (Mod 4, Act 3)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: Tuple[int, int, int]
    field_8: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: Tuple[int, int, int], field_8: int) -> None:
        super().__init__(mod=4, act=3)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5
        self.field_6 = field_6
        self.field_7 = field_7
        self.field_8 = field_8

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_uint8(self.field_2)
        writer.write_int8(self.field_3)
        writer.write_int8(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int32(self.field_6)
        # 写入动态列表 field_7 (元素数 + 记录项)
        writer.write_uint16(len(self.field_7))
        for item_7 in self.field_7:
            writer.write_json(item_7)
        writer.write_int16(self.field_8)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionRankMissionResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        f_2 = reader.read_uint8()
        f_3 = reader.read_int8()
        f_4 = reader.read_int8()
        f_5 = reader.read_int32()
        f_6 = reader.read_int32()
        # 读取动态列表 f_7
        cnt_7 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_7 = []
        for _ in range(cnt_7):
            f_7.append(reader.read_json())
        f_8 = reader.read_int16()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8)

@dataclass
class MissionOpenBoxReq(BasePacket):
    """Mission.open_box 请求封包 (Mod 4, Act 4)"""

    def __init__(self) -> None:
        super().__init__(mod=4, act=4)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionOpenBoxReq":
        return cls()

@dataclass
class MissionOpenBoxResp(BasePacket):
    """Mission.open_box 应答封包 (Mod 4, Act 4)"""

    field_0: int
    field_1: int
    field_2: Tuple[int, int]
    field_3: int

    def __init__(self, field_0: int, field_1: int, field_2: Tuple[int, int], field_3: int) -> None:
        super().__init__(mod=4, act=4)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        writer.write_int16(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionOpenBoxResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_json())
        f_3 = reader.read_int16()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class MissionPickupAwardReq(BasePacket):
    """Mission.pickup_award 请求封包 (Mod 4, Act 5)"""

    def __init__(self) -> None:
        super().__init__(mod=4, act=5)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionPickupAwardReq":
        return cls()

@dataclass
class MissionPickupAwardResp(BasePacket):
    """Mission.pickup_award 应答封包 (Mod 4, Act 5)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=5)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionPickupAwardResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class MissionSignPlayMissionVideoReq(BasePacket):
    """Mission.sign_play_mission_video 请求封包 (Mod 4, Act 6)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=6)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionSignPlayMissionVideoReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class MissionSignPlayMissionVideoResp(BasePacket):
    """Mission.sign_play_mission_video 应答封包 (Mod 4, Act 6)"""

    def __init__(self) -> None:
        super().__init__(mod=4, act=6)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionSignPlayMissionVideoResp":
        return cls()

@dataclass
class MissionGetMonsterStrategyListReq(BasePacket):
    """Mission.get_monster_strategy_list 请求封包 (Mod 4, Act 7)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=7)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetMonsterStrategyListReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class MissionGetMonsterStrategyListResp(BasePacket):
    """Mission.get_monster_strategy_list 应答封包 (Mod 4, Act 7)"""

    field_0: int
    field_1: Tuple[str, int, int, str]

    def __init__(self, field_0: int, field_1: Tuple[str, int, int, str]) -> None:
        super().__init__(mod=4, act=7)
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
    def decode(cls, data: bytes) -> "MissionGetMonsterStrategyListResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class MissionGetPlayerWarReportReq(BasePacket):
    """Mission.get_player_war_report 请求封包 (Mod 4, Act 8)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=8)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetPlayerWarReportReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class MissionGetPlayerWarReportResp(BasePacket):
    """Mission.get_player_war_report 应答封包 (Mod 4, Act 8)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int]
    field_4: Tuple[int, int, int]
    field_5: Tuple[int, int]
    field_6: Tuple[int, int]
    field_7: Tuple[Tuple[str, Tuple[int, str, int, int, int, int, int, int, int, int, int, int, int, int, int, int]], Tuple[str, Tuple[int, str, int, int, int, int, int, int, int, int, int, int, int, int, int, int]]]
    field_8: int
    field_9: int
    field_10: int
    field_11: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int], field_4: Tuple[int, int, int], field_5: Tuple[int, int], field_6: Tuple[int, int], field_7: Tuple[Tuple[str, Tuple[int, str, int, int, int, int, int, int, int, int, int, int, int, int, int, int]], Tuple[str, Tuple[int, str, int, int, int, int, int, int, int, int, int, int, int, int, int, int]]], field_8: int, field_9: int, field_10: int, field_11: int) -> None:
        super().__init__(mod=4, act=8)
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
        writer.write_int8(self.field_2)
        # 写入动态列表 field_3 (元素数 + 记录项)
        writer.write_uint16(len(self.field_3))
        for item_3 in self.field_3:
            writer.write_json(item_3)
        # 写入动态列表 field_4 (元素数 + 记录项)
        writer.write_uint16(len(self.field_4))
        for item_4 in self.field_4:
            writer.write_json(item_4)
        # 写入动态列表 field_5 (元素数 + 记录项)
        writer.write_uint16(len(self.field_5))
        for item_5 in self.field_5:
            writer.write_json(item_5)
        # 写入动态列表 field_6 (元素数 + 记录项)
        writer.write_uint16(len(self.field_6))
        for item_6 in self.field_6:
            writer.write_json(item_6)
        # 写入动态列表 field_7 (元素数 + 记录项)
        writer.write_uint16(len(self.field_7))
        for item_7 in self.field_7:
            writer.write_json(item_7)
        writer.write_int32(self.field_8)
        writer.write_uint8(self.field_9)
        writer.write_int16(self.field_10)
        writer.write_int16(self.field_11)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetPlayerWarReportResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int8()
        # 读取动态列表 f_3
        cnt_3 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_3 = []
        for _ in range(cnt_3):
            f_3.append(reader.read_json())
        # 读取动态列表 f_4
        cnt_4 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_4 = []
        for _ in range(cnt_4):
            f_4.append(reader.read_json())
        # 读取动态列表 f_5
        cnt_5 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_5 = []
        for _ in range(cnt_5):
            f_5.append(reader.read_json())
        # 读取动态列表 f_6
        cnt_6 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_6 = []
        for _ in range(cnt_6):
            f_6.append(reader.read_json())
        # 读取动态列表 f_7
        cnt_7 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_7 = []
        for _ in range(cnt_7):
            f_7.append(reader.read_json())
        f_8 = reader.read_int32()
        f_9 = reader.read_uint8()
        f_10 = reader.read_int16()
        f_11 = reader.read_int16()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11)

@dataclass
class MissionRandomItemReq(BasePacket):
    """Mission.random_item 请求封包 (Mod 4, Act 9)"""

    def __init__(self) -> None:
        super().__init__(mod=4, act=9)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionRandomItemReq":
        return cls()

@dataclass
class MissionRandomItemResp(BasePacket):
    """Mission.random_item 应答封包 (Mod 4, Act 9)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=4, act=9)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionRandomItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class MissionFetchRandomItemReq(BasePacket):
    """Mission.fetch_random_item 请求封包 (Mod 4, Act 10)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=10)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionFetchRandomItemReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class MissionFetchRandomItemResp(BasePacket):
    """Mission.fetch_random_item 应答封包 (Mod 4, Act 10)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=4, act=10)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionFetchRandomItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class MissionGetSpecialResultReq(BasePacket):
    """Mission.get_special_result 请求封包 (Mod 4, Act 11)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=11)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetSpecialResultReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class MissionGetSpecialResultResp(BasePacket):
    """Mission.get_special_result 应答封包 (Mod 4, Act 11)"""

    field_0: int
    field_1: Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int]
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int], field_2: int, field_3: int) -> None:
        super().__init__(mod=4, act=11)
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
        writer.write_int32(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetSpecialResultResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class MissionIsSpecialSceneReq(BasePacket):
    """Mission.is_special_scene 请求封包 (Mod 4, Act 12)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=12)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionIsSpecialSceneReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class MissionIsSpecialSceneResp(BasePacket):
    """Mission.is_special_scene 应答封包 (Mod 4, Act 12)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=12)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionIsSpecialSceneResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class MissionClickMissionItemElementReq(BasePacket):
    """Mission.click_mission_item_element 请求封包 (Mod 4, Act 13)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=4, act=13)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionClickMissionItemElementReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class MissionClickMissionItemElementResp(BasePacket):
    """Mission.click_mission_item_element 应答封包 (Mod 4, Act 13)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=13)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionClickMissionItemElementResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class MissionFirstTieSecondWinReq(BasePacket):
    """Mission.first_tie_second_win 请求封包 (Mod 4, Act 14)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=4, act=14)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_uint8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionFirstTieSecondWinReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_uint8()
        return cls(f_0, f_1, f_2)

@dataclass
class MissionFirstTieSecondWinResp(BasePacket):
    """Mission.first_tie_second_win 应答封包 (Mod 4, Act 14)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=4, act=14)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_uint8(self.field_1)
        writer.write_uint8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionFirstTieSecondWinResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_uint8()
        f_2 = reader.read_uint8()
        return cls(f_0, f_1, f_2)

@dataclass
class MissionOpenBoxDirectlyReq(BasePacket):
    """Mission.open_box_directly 请求封包 (Mod 4, Act 15)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=15)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionOpenBoxDirectlyReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class MissionOpenBoxDirectlyResp(BasePacket):
    """Mission.open_box_directly 应答封包 (Mod 4, Act 15)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: Tuple[int, int]
    field_4: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: Tuple[int, int], field_4: int) -> None:
        super().__init__(mod=4, act=15)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        # 写入动态列表 field_3 (元素数 + 记录项)
        writer.write_uint16(len(self.field_3))
        for item_3 in self.field_3:
            writer.write_json(item_3)
        writer.write_int16(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionOpenBoxDirectlyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        # 读取动态列表 f_3
        cnt_3 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_3 = []
        for _ in range(cnt_3):
            f_3.append(reader.read_json())
        f_4 = reader.read_int16()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class MissionPickupTrunkMissionAwardDirectlyReq(BasePacket):
    """Mission.pickup_trunk_mission_award_directly 请求封包 (Mod 4, Act 16)"""

    def __init__(self) -> None:
        super().__init__(mod=4, act=16)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionPickupTrunkMissionAwardDirectlyReq":
        return cls()

@dataclass
class MissionPickupTrunkMissionAwardDirectlyResp(BasePacket):
    """Mission.pickup_trunk_mission_award_directly 应答封包 (Mod 4, Act 16)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=16)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionPickupTrunkMissionAwardDirectlyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class MissionGetStarAwardReq(BasePacket):
    """Mission.get_star_award 请求封包 (Mod 4, Act 17)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=4, act=17)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetStarAwardReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class MissionGetStarAwardResp(BasePacket):
    """Mission.get_star_award 应答封包 (Mod 4, Act 17)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=17)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetStarAwardResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class MissionGetStarAwardInfoReq(BasePacket):
    """Mission.get_star_award_info 请求封包 (Mod 4, Act 18)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=18)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetStarAwardInfoReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class MissionGetStarAwardInfoResp(BasePacket):
    """Mission.get_star_award_info 应答封包 (Mod 4, Act 18)"""

    field_0: List[int]

    def __init__(self, field_0: List[int]) -> None:
        super().__init__(mod=4, act=18)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_int8(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetStarAwardInfoResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_int8())
        return cls(f_0)

@dataclass
class MissionGetStarCountReq(BasePacket):
    """Mission.get_star_count 请求封包 (Mod 4, Act 19)"""

    def __init__(self) -> None:
        super().__init__(mod=4, act=19)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetStarCountReq":
        return cls()

@dataclass
class MissionGetStarCountResp(BasePacket):
    """Mission.get_star_count 应答封包 (Mod 4, Act 19)"""

    field_0: Tuple[int, int]

    def __init__(self, field_0: Tuple[int, int]) -> None:
        super().__init__(mod=4, act=19)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetStarCountResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class MissionGetCompleteMaxInfoReq(BasePacket):
    """Mission.get_complete_max_info 请求封包 (Mod 4, Act 20)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=20)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetCompleteMaxInfoReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class MissionGetCompleteMaxInfoResp(BasePacket):
    """Mission.get_complete_max_info 应答封包 (Mod 4, Act 20)"""

    field_0: int
    field_1: str
    field_2: int

    def __init__(self, field_0: int, field_1: str, field_2: int) -> None:
        super().__init__(mod=4, act=20)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetCompleteMaxInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class MissionGetMissionCompleteInfoReq(BasePacket):
    """Mission.get_mission_complete_info 请求封包 (Mod 4, Act 21)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=21)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetMissionCompleteInfoReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class MissionGetMissionCompleteInfoResp(BasePacket):
    """Mission.get_mission_complete_info 应答封包 (Mod 4, Act 21)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=4, act=21)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetMissionCompleteInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int16()
        f_2 = reader.read_int8()
        return cls(f_0, f_1, f_2)

@dataclass
class MissionShowBuffReq(BasePacket):
    """Mission.show_buff 请求封包 (Mod 4, Act 22)"""

    def __init__(self) -> None:
        super().__init__(mod=4, act=22)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionShowBuffReq":
        return cls()

@dataclass
class MissionShowBuffResp(BasePacket):
    """Mission.show_buff 应答封包 (Mod 4, Act 22)"""

    field_0: Tuple[int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int]) -> None:
        super().__init__(mod=4, act=22)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionShowBuffResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class MissionUpdateBuffReq(BasePacket):
    """Mission.update_buff 请求封包 (Mod 4, Act 23)"""

    def __init__(self) -> None:
        super().__init__(mod=4, act=23)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionUpdateBuffReq":
        return cls()

@dataclass
class MissionUpdateBuffResp(BasePacket):
    """Mission.update_buff 应答封包 (Mod 4, Act 23)"""

    field_0: Tuple[int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int]) -> None:
        super().__init__(mod=4, act=23)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionUpdateBuffResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class MissionGetHirePartnerInfoReq(BasePacket):
    """Mission.get_hire_partner_info 请求封包 (Mod 4, Act 24)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=24)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetHirePartnerInfoReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class MissionGetHirePartnerInfoResp(BasePacket):
    """Mission.get_hire_partner_info 应答封包 (Mod 4, Act 24)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=4, act=24)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetHirePartnerInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class MissionGetSectBuffActiveFlagReq(BasePacket):
    """Mission.get_sect_buff_active_flag 请求封包 (Mod 4, Act 25)"""

    def __init__(self) -> None:
        super().__init__(mod=4, act=25)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetSectBuffActiveFlagReq":
        return cls()

@dataclass
class MissionGetSectBuffActiveFlagResp(BasePacket):
    """Mission.get_sect_buff_active_flag 应答封包 (Mod 4, Act 25)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=25)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionGetSectBuffActiveFlagResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class MissionAutoHeroFightMonsterReq(BasePacket):
    """Mission.auto_hero_fight_monster 请求封包 (Mod 4, Act 26)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=4, act=26)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionAutoHeroFightMonsterReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class MissionAutoHeroFightMonsterResp(BasePacket):
    """Mission.auto_hero_fight_monster 应答封包 (Mod 4, Act 26)"""

    field_0: int
    field_1: int
    field_2: Tuple[int, int]

    def __init__(self, field_0: int, field_1: int, field_2: Tuple[int, int]) -> None:
        super().__init__(mod=4, act=26)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int8(self.field_1)
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionAutoHeroFightMonsterResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int8()
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_json())
        return cls(f_0, f_1, f_2)
