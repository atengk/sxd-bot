"""神仙道 Town 模块协议代码契约 (Mod 1)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_Town_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class TownConstants:
    """Town 模块业务状态与行为常量"""

    BECOME_IMMORTAL = 10
    FAILED = 1
    FALSE = 12
    FINISHED_PRACTICE = 6
    FULL = 2
    NOT_ENOUGH_INGOT = 3
    NOT_IMMORTAL = 9
    OFF_PRACTICE = 5
    ON_PRACTICE = 4
    SUCCESS = 0
    TOWN_FAILURE = 14
    TOWN_HIDDEN = 7
    TOWN_NOHIDDEN = 8
    TOWN_SUCCESS = 13
    TRUE = 11

@dataclass
class TownEnterTownReq(BasePacket):
    """Town.enter_town 请求封包 (Mod 1, Act 0)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=1, act=0)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownEnterTownReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class TownEnterTownResp(BasePacket):
    """Town.enter_town 应答封包 (Mod 1, Act 0)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: Tuple[int, int, int, int]
    field_5: str
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
    field_16: str
    field_17: int
    field_18: int
    field_19: int
    field_20: int
    field_21: int
    field_22: List[int]
    field_23: int
    field_24: List[int]
    field_25: int
    field_26: int
    field_27: int
    field_28: int
    field_29: int
    field_30: int
    field_31: str
    field_32: int
    field_33: int
    field_34: str
    field_35: int
    field_36: int
    field_37: int
    field_38: int
    field_39: int
    field_40: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: Tuple[int, int, int, int], field_5: str, field_6: int, field_7: int, field_8: int, field_9: int, field_10: int, field_11: int, field_12: int, field_13: int, field_14: int, field_15: int, field_16: str, field_17: int, field_18: int, field_19: int, field_20: int, field_21: int, field_22: List[int], field_23: int, field_24: List[int], field_25: int, field_26: int, field_27: int, field_28: int, field_29: int, field_30: int, field_31: str, field_32: int, field_33: int, field_34: str, field_35: int, field_36: int, field_37: int, field_38: int, field_39: int, field_40: int) -> None:
        super().__init__(mod=1, act=0)
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

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        # 写入动态列表 field_4 (元素数 + 记录项)
        writer.write_uint16(len(self.field_4))
        for item_4 in self.field_4:
            writer.write_json(item_4)
        writer.write_utf(self.field_5)
        writer.write_int16(self.field_6)
        writer.write_int16(self.field_7)
        writer.write_int32(self.field_8)
        writer.write_int32(self.field_9)
        writer.write_int8(self.field_10)
        writer.write_int32(self.field_11)
        writer.write_int32(self.field_12)
        writer.write_uint8(self.field_13)
        writer.write_int8(self.field_14)
        writer.write_int32(self.field_15)
        writer.write_utf(self.field_16)
        writer.write_int8(self.field_17)
        writer.write_int16(self.field_18)
        writer.write_int32(self.field_19)
        writer.write_int32(self.field_20)
        writer.write_int8(self.field_21)
        # 写入动态列表 field_22 (元素数 + 记录项)
        writer.write_uint16(len(self.field_22))
        for item_22 in self.field_22:
            writer.write_int32(item_22)
        writer.write_uint8(self.field_23)
        # 写入动态列表 field_24 (元素数 + 记录项)
        writer.write_uint16(len(self.field_24))
        for item_24 in self.field_24:
            writer.write_int32(item_24)
        writer.write_uint8(self.field_25)
        writer.write_int16(self.field_26)
        writer.write_uint8(self.field_27)
        writer.write_int16(self.field_28)
        writer.write_int8(self.field_29)
        writer.write_int16(self.field_30)
        writer.write_utf(self.field_31)
        writer.write_int32(self.field_32)
        writer.write_int16(self.field_33)
        writer.write_utf(self.field_34)
        writer.write_int32(self.field_35)
        writer.write_int32(self.field_36)
        writer.write_int8(self.field_37)
        writer.write_int8(self.field_38)
        writer.write_int32(self.field_39)
        writer.write_int32(self.field_40)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownEnterTownResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        # 读取动态列表 f_4
        cnt_4 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_4 = []
        for _ in range(cnt_4):
            f_4.append(reader.read_json())
        f_5 = reader.read_utf()
        f_6 = reader.read_int16()
        f_7 = reader.read_int16()
        f_8 = reader.read_int32()
        f_9 = reader.read_int32()
        f_10 = reader.read_int8()
        f_11 = reader.read_int32()
        f_12 = reader.read_int32()
        f_13 = reader.read_uint8()
        f_14 = reader.read_int8()
        f_15 = reader.read_int32()
        f_16 = reader.read_utf()
        f_17 = reader.read_int8()
        f_18 = reader.read_int16()
        f_19 = reader.read_int32()
        f_20 = reader.read_int32()
        f_21 = reader.read_int8()
        # 读取动态列表 f_22
        cnt_22 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_22 = []
        for _ in range(cnt_22):
            f_22.append(reader.read_int32())
        f_23 = reader.read_uint8()
        # 读取动态列表 f_24
        cnt_24 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_24 = []
        for _ in range(cnt_24):
            f_24.append(reader.read_int32())
        f_25 = reader.read_uint8()
        f_26 = reader.read_int16()
        f_27 = reader.read_uint8()
        f_28 = reader.read_int16()
        f_29 = reader.read_int8()
        f_30 = reader.read_int16()
        f_31 = reader.read_utf()
        f_32 = reader.read_int32()
        f_33 = reader.read_int16()
        f_34 = reader.read_utf()
        f_35 = reader.read_int32()
        f_36 = reader.read_int32()
        f_37 = reader.read_int8()
        f_38 = reader.read_int8()
        f_39 = reader.read_int32()
        f_40 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11, f_12, f_13, f_14, f_15, f_16, f_17, f_18, f_19, f_20, f_21, f_22, f_23, f_24, f_25, f_26, f_27, f_28, f_29, f_30, f_31, f_32, f_33, f_34, f_35, f_36, f_37, f_38, f_39, f_40)

@dataclass
class TownLeaveTownReq(BasePacket):
    """Town.leave_town 请求封包 (Mod 1, Act 1)"""

    def __init__(self) -> None:
        super().__init__(mod=1, act=1)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TownLeaveTownReq":
        return cls()

@dataclass
class TownLeaveTownResp(BasePacket):
    """Town.leave_town 应答封包 (Mod 1, Act 1)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=1, act=1)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownLeaveTownResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class TownMoveToReq(BasePacket):
    """Town.move_to 请求封包 (Mod 1, Act 2)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=1, act=2)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int16(self.field_2)
        writer.write_int16(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownMoveToReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        f_2 = reader.read_int16()
        f_3 = reader.read_int16()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class TownMoveToResp(BasePacket):
    """Town.move_to 应答封包 (Mod 1, Act 2)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int) -> None:
        super().__init__(mod=1, act=2)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int16(self.field_2)
        writer.write_int16(self.field_3)
        writer.write_int16(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownMoveToResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int16()
        f_2 = reader.read_int16()
        f_3 = reader.read_int16()
        f_4 = reader.read_int16()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class TownGetPlayersReq(BasePacket):
    """Town.get_players 请求封包 (Mod 1, Act 3)"""

    def __init__(self) -> None:
        super().__init__(mod=1, act=3)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TownGetPlayersReq":
        return cls()

@dataclass
class TownGetPlayersResp(BasePacket):
    """Town.get_players 应答封包 (Mod 1, Act 3)"""

    field_0: Tuple[int, int, int, Tuple[int, int, int, int], str, int, int, int, int, int, int, int, int, int, int, str, int, int, int, int, int, int, int, int, int, int, str, int, int, str, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, Tuple[int, int, int, int], str, int, int, int, int, int, int, int, int, int, int, str, int, int, int, int, int, int, int, int, int, int, str, int, int, str, int, int, int, int, int, int]) -> None:
        super().__init__(mod=1, act=3)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownGetPlayersResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class TownPlayerFollowRoleChangeReq(BasePacket):
    """Town.player_follow_role_change 请求封包 (Mod 1, Act 4)"""

    def __init__(self) -> None:
        super().__init__(mod=1, act=4)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TownPlayerFollowRoleChangeReq":
        return cls()

@dataclass
class TownPlayerFollowRoleChangeResp(BasePacket):
    """Town.player_follow_role_change 应答封包 (Mod 1, Act 4)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: str
    field_5: int
    field_6: int
    field_7: str
    field_8: int
    field_9: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: str, field_5: int, field_6: int, field_7: str, field_8: int, field_9: int) -> None:
        super().__init__(mod=1, act=4)
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
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int16(self.field_2)
        writer.write_int16(self.field_3)
        writer.write_utf(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int16(self.field_6)
        writer.write_utf(self.field_7)
        writer.write_int32(self.field_8)
        writer.write_int32(self.field_9)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownPlayerFollowRoleChangeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int16()
        f_3 = reader.read_int16()
        f_4 = reader.read_utf()
        f_5 = reader.read_int32()
        f_6 = reader.read_int16()
        f_7 = reader.read_utf()
        f_8 = reader.read_int32()
        f_9 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9)

@dataclass
class TownPlayerCountReq(BasePacket):
    """Town.player_count 请求封包 (Mod 1, Act 5)"""

    def __init__(self) -> None:
        super().__init__(mod=1, act=5)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TownPlayerCountReq":
        return cls()

@dataclass
class TownPlayerCountResp(BasePacket):
    """Town.player_count 应答封包 (Mod 1, Act 5)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=1, act=5)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownPlayerCountResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class TownPlayerFollowSettingChangeReq(BasePacket):
    """Town.player_follow_setting_change 请求封包 (Mod 1, Act 6)"""

    def __init__(self) -> None:
        super().__init__(mod=1, act=6)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TownPlayerFollowSettingChangeReq":
        return cls()

@dataclass
class TownPlayerFollowSettingChangeResp(BasePacket):
    """Town.player_follow_setting_change 应答封包 (Mod 1, Act 6)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=1, act=6)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownPlayerFollowSettingChangeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class TownPlayTownVideoReq(BasePacket):
    """Town.play_town_video 请求封包 (Mod 1, Act 7)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=1, act=7)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownPlayTownVideoReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class TownPlayTownVideoResp(BasePacket):
    """Town.play_town_video 应答封包 (Mod 1, Act 7)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=1, act=7)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownPlayTownVideoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class TownNotifyPlayerHaveFollowSettingReq(BasePacket):
    """Town.notify_player_have_follow_setting 请求封包 (Mod 1, Act 8)"""

    def __init__(self) -> None:
        super().__init__(mod=1, act=8)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TownNotifyPlayerHaveFollowSettingReq":
        return cls()

@dataclass
class TownNotifyPlayerHaveFollowSettingResp(BasePacket):
    """Town.notify_player_have_follow_setting 应答封包 (Mod 1, Act 8)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=1, act=8)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownNotifyPlayerHaveFollowSettingResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class TownNotifyImageChangeReq(BasePacket):
    """Town.notify_image_change 请求封包 (Mod 1, Act 9)"""

    def __init__(self) -> None:
        super().__init__(mod=1, act=9)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TownNotifyImageChangeReq":
        return cls()

@dataclass
class TownNotifyImageChangeResp(BasePacket):
    """Town.notify_image_change 应答封包 (Mod 1, Act 9)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: str

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: str) -> None:
        super().__init__(mod=1, act=9)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int8(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_utf(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownNotifyImageChangeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int8()
        f_2 = reader.read_int32()
        f_3 = reader.read_utf()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class TownNotifyDanceActionReq(BasePacket):
    """Town.notify_dance_action 请求封包 (Mod 1, Act 10)"""

    def __init__(self) -> None:
        super().__init__(mod=1, act=10)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TownNotifyDanceActionReq":
        return cls()

@dataclass
class TownNotifyDanceActionResp(BasePacket):
    """Town.notify_dance_action 应答封包 (Mod 1, Act 10)"""

    field_0: List[int]
    field_1: int
    field_2: int
    field_3: str
    field_4: int

    def __init__(self, field_0: List[int], field_1: int, field_2: int, field_3: str, field_4: int) -> None:
        super().__init__(mod=1, act=10)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_int32(item_0)
        writer.write_int32(self.field_1)
        writer.write_int8(self.field_2)
        writer.write_utf(self.field_3)
        writer.write_int32(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownNotifyDanceActionResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_int32())
        f_1 = reader.read_int32()
        f_2 = reader.read_int8()
        f_3 = reader.read_utf()
        f_4 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class TownPlayerChaosMonsterFollowChangeReq(BasePacket):
    """Town.player_chaos_monster_follow_change 请求封包 (Mod 1, Act 11)"""

    def __init__(self) -> None:
        super().__init__(mod=1, act=11)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TownPlayerChaosMonsterFollowChangeReq":
        return cls()

@dataclass
class TownPlayerChaosMonsterFollowChangeResp(BasePacket):
    """Town.player_chaos_monster_follow_change 应答封包 (Mod 1, Act 11)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=1, act=11)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownPlayerChaosMonsterFollowChangeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class TownPlayerDragonBallFollowSettingChangeReq(BasePacket):
    """Town.player_dragon_ball_follow_setting_change 请求封包 (Mod 1, Act 12)"""

    def __init__(self) -> None:
        super().__init__(mod=1, act=12)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TownPlayerDragonBallFollowSettingChangeReq":
        return cls()

@dataclass
class TownPlayerDragonBallFollowSettingChangeResp(BasePacket):
    """Town.player_dragon_ball_follow_setting_change 应答封包 (Mod 1, Act 12)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=1, act=12)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownPlayerDragonBallFollowSettingChangeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class TownPlayerSupremeVipPrefixChangeReq(BasePacket):
    """Town.player_supreme_vip_prefix_change 请求封包 (Mod 1, Act 13)"""

    def __init__(self) -> None:
        super().__init__(mod=1, act=13)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TownPlayerSupremeVipPrefixChangeReq":
        return cls()

@dataclass
class TownPlayerSupremeVipPrefixChangeResp(BasePacket):
    """Town.player_supreme_vip_prefix_change 应答封包 (Mod 1, Act 13)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=1, act=13)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownPlayerSupremeVipPrefixChangeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)
