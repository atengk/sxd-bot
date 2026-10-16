"""神仙道 TakeBible 模块协议代码契约 (Mod 30)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_TakeBible_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class TakebibleConstants:
    """TakeBible 模块业务状态与行为常量"""

    APPLY_PROTECT = 34
    ARRIVAL = 28
    BAI_LONG_MA = 0
    BEROB = 32
    BE_MONSTER_ROB = 31
    BE_ROB_ALL = 21
    CANCEL_APPLY = 13
    CLOSE = 5
    FRIEND_APPROVE_APPLY = 29
    FRIEND_REJECT_APPLY = 30
    FULL_PROTECT_TIMES = 10
    FULL_ROB_TIMES = 19
    FULL_TAKE_BIBLE_TIMES = 17
    HAVE_CD_TIME = 20
    INVALID_PLAYER_ID = 9
    INVALID_TYPE = 35
    KILL_ALL = 37
    KILL_ONE = 36
    KILL_ONE_NO_AWARD = 38
    NEW_TAKE_BIBLE = 26
    NOT_ENOUGH_INGOT = 15
    NOT_ONLINE = 11
    OPEN = 7
    OPEN_FOR_CALL = 6
    PROTECT_BEROB = 33
    PROTECT_STATUS = 14
    QUICKLY = 27
    REQUEST_VIP = 16
    REROB = 18
    ROB = 24
    SHA_WU_JING = 1
    SUCCESS = 8
    SUN_WU_KONG = 3
    TAKE_BIBLE = 25
    TAKE_BIBLE_STATUS = 12
    TANGSENG_BE_ROB_ALL = 23
    TANGSENG_FULL_ROB_TIMES = 22
    TANG_SENG = 4
    ZHU_BA_JIE = 2

@dataclass
class TakebibleOpenTakeBibleReq(BasePacket):
    """TakeBible.open_take_bible 请求封包 (Mod 30, Act 0)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=0)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleOpenTakeBibleReq":
        return cls()

@dataclass
class TakebibleOpenTakeBibleResp(BasePacket):
    """TakeBible.open_take_bible 应答封包 (Mod 30, Act 0)"""

    field_0: Tuple[int, int, int, int, int, int, int, int]
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int
    field_8: int

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int], field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int) -> None:
        super().__init__(mod=30, act=0)
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
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        writer.write_int32(self.field_1)
        writer.write_int8(self.field_2)
        writer.write_int8(self.field_3)
        writer.write_int8(self.field_4)
        writer.write_int8(self.field_5)
        writer.write_int8(self.field_6)
        writer.write_uint8(self.field_7)
        writer.write_int32(self.field_8)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleOpenTakeBibleResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        f_1 = reader.read_int32()
        f_2 = reader.read_int8()
        f_3 = reader.read_int8()
        f_4 = reader.read_int8()
        f_5 = reader.read_int8()
        f_6 = reader.read_int8()
        f_7 = reader.read_uint8()
        f_8 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8)

@dataclass
class TakebibleCloseTakeBibleReq(BasePacket):
    """TakeBible.close_take_bible 请求封包 (Mod 30, Act 1)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=1)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleCloseTakeBibleReq":
        return cls()

@dataclass
class TakebibleCloseTakeBibleResp(BasePacket):
    """TakeBible.close_take_bible 应答封包 (Mod 30, Act 1)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=1)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleCloseTakeBibleResp":
        return cls()

@dataclass
class TakebibleGetTakeBibleInfoReq(BasePacket):
    """TakeBible.get_take_bible_info 请求封包 (Mod 30, Act 2)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=2)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleGetTakeBibleInfoReq":
        return cls()

@dataclass
class TakebibleGetTakeBibleInfoResp(BasePacket):
    """TakeBible.get_take_bible_info 应答封包 (Mod 30, Act 2)"""

    field_0: Tuple[int, int, int, int]
    field_1: Tuple[int, str, int, int, int]
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: str
    field_8: int

    def __init__(self, field_0: Tuple[int, int, int, int], field_1: Tuple[int, str, int, int, int], field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: str, field_8: int) -> None:
        super().__init__(mod=30, act=2)
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
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        writer.write_int8(self.field_2)
        writer.write_int8(self.field_3)
        writer.write_int16(self.field_4)
        writer.write_int8(self.field_5)
        writer.write_uint8(self.field_6)
        writer.write_utf(self.field_7)
        writer.write_int8(self.field_8)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleGetTakeBibleInfoResp":
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
        f_2 = reader.read_int8()
        f_3 = reader.read_int8()
        f_4 = reader.read_int16()
        f_5 = reader.read_int8()
        f_6 = reader.read_uint8()
        f_7 = reader.read_utf()
        f_8 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8)

@dataclass
class TakebibleApplyFriendReq(BasePacket):
    """TakeBible.apply_friend 请求封包 (Mod 30, Act 3)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=30, act=3)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleApplyFriendReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class TakebibleApplyFriendResp(BasePacket):
    """TakeBible.apply_friend 应答封包 (Mod 30, Act 3)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=30, act=3)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleApplyFriendResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class TakebibleCancelApplyFriendReq(BasePacket):
    """TakeBible.cancel_apply_friend 请求封包 (Mod 30, Act 4)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=4)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleCancelApplyFriendReq":
        return cls()

@dataclass
class TakebibleCancelApplyFriendResp(BasePacket):
    """TakeBible.cancel_apply_friend 应答封包 (Mod 30, Act 4)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=4)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleCancelApplyFriendResp":
        return cls()

@dataclass
class TakebibleApproveApplyReq(BasePacket):
    """TakeBible.approve_apply 请求封包 (Mod 30, Act 5)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=30, act=5)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleApproveApplyReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class TakebibleApproveApplyResp(BasePacket):
    """TakeBible.approve_apply 应答封包 (Mod 30, Act 5)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=30, act=5)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleApproveApplyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class TakebibleRejectApplyReq(BasePacket):
    """TakeBible.reject_apply 请求封包 (Mod 30, Act 6)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=30, act=6)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleRejectApplyReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class TakebibleRejectApplyResp(BasePacket):
    """TakeBible.reject_apply 应答封包 (Mod 30, Act 6)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=6)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleRejectApplyResp":
        return cls()

@dataclass
class TakebibleBuyProtectionReq(BasePacket):
    """TakeBible.buy_protection 请求封包 (Mod 30, Act 7)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=7)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleBuyProtectionReq":
        return cls()

@dataclass
class TakebibleBuyProtectionResp(BasePacket):
    """TakeBible.buy_protection 应答封包 (Mod 30, Act 7)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=30, act=7)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleBuyProtectionResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class TakebibleRefreshReq(BasePacket):
    """TakeBible.refresh 请求封包 (Mod 30, Act 8)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=8)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleRefreshReq":
        return cls()

@dataclass
class TakebibleRefreshResp(BasePacket):
    """TakeBible.refresh 应答封包 (Mod 30, Act 8)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=30, act=8)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_uint8(self.field_1)
        writer.write_int16(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleRefreshResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_uint8()
        f_2 = reader.read_int16()
        return cls(f_0, f_1, f_2)

@dataclass
class TakebibleGetPlayerTakeBibleReq(BasePacket):
    """TakeBible.get_player_take_bible 请求封包 (Mod 30, Act 9)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=30, act=9)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleGetPlayerTakeBibleReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class TakebibleGetPlayerTakeBibleResp(BasePacket):
    """TakeBible.get_player_take_bible 应答封包 (Mod 30, Act 9)"""

    field_0: int
    field_1: str
    field_2: int
    field_3: int
    field_4: int
    field_5: str
    field_6: int
    field_7: int
    field_8: int
    field_9: int
    field_10: int
    field_11: str

    def __init__(self, field_0: int, field_1: str, field_2: int, field_3: int, field_4: int, field_5: str, field_6: int, field_7: int, field_8: int, field_9: int, field_10: int, field_11: str) -> None:
        super().__init__(mod=30, act=9)
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
        writer.write_utf(self.field_1)
        writer.write_int16(self.field_2)
        writer.write_int8(self.field_3)
        writer.write_int8(self.field_4)
        writer.write_utf(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int16(self.field_7)
        writer.write_int32(self.field_8)
        writer.write_int16(self.field_9)
        writer.write_int8(self.field_10)
        writer.write_utf(self.field_11)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleGetPlayerTakeBibleResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int16()
        f_3 = reader.read_int8()
        f_4 = reader.read_int8()
        f_5 = reader.read_utf()
        f_6 = reader.read_int32()
        f_7 = reader.read_int16()
        f_8 = reader.read_int32()
        f_9 = reader.read_int16()
        f_10 = reader.read_int8()
        f_11 = reader.read_utf()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11)

@dataclass
class TakebibleStartTakeBibleReq(BasePacket):
    """TakeBible.start_take_bible 请求封包 (Mod 30, Act 10)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=10)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleStartTakeBibleReq":
        return cls()

@dataclass
class TakebibleStartTakeBibleResp(BasePacket):
    """TakeBible.start_take_bible 应答封包 (Mod 30, Act 10)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=30, act=10)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleStartTakeBibleResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class TakebibleRobReq(BasePacket):
    """TakeBible.rob 请求封包 (Mod 30, Act 11)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=30, act=11)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleRobReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class TakebibleRobResp(BasePacket):
    """TakeBible.rob 应答封包 (Mod 30, Act 11)"""

    field_0: int
    field_1: int
    field_2: str
    field_3: int
    field_4: int
    field_5: int
    field_6: Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int]
    field_7: int
    field_8: int

    def __init__(self, field_0: int, field_1: int, field_2: str, field_3: int, field_4: int, field_5: int, field_6: Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int], field_7: int, field_8: int) -> None:
        super().__init__(mod=30, act=11)
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
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int16(self.field_4)
        writer.write_int32(self.field_5)
        # 写入动态列表 field_6 (元素数 + 记录项)
        writer.write_uint16(len(self.field_6))
        for item_6 in self.field_6:
            writer.write_json(item_6)
        writer.write_int8(self.field_7)
        writer.write_int8(self.field_8)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleRobResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_utf()
        f_3 = reader.read_int32()
        f_4 = reader.read_int16()
        f_5 = reader.read_int32()
        # 读取动态列表 f_6
        cnt_6 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_6 = []
        for _ in range(cnt_6):
            f_6.append(reader.read_json())
        f_7 = reader.read_int8()
        f_8 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8)

@dataclass
class TakebibleNotifyReq(BasePacket):
    """TakeBible.notify 请求封包 (Mod 30, Act 12)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=12)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleNotifyReq":
        return cls()

@dataclass
class TakebibleNotifyResp(BasePacket):
    """TakeBible.notify 应答封包 (Mod 30, Act 12)"""

    field_0: int
    field_1: Tuple[int, str, int, str, int, int, int]
    field_2: Tuple[int, str, int]
    field_3: Tuple[int, int, int, int, int, int, int, int]
    field_4: Tuple[int, int, int]
    field_5: List[int]
    field_6: List[int]

    def __init__(self, field_0: int, field_1: Tuple[int, str, int, str, int, int, int], field_2: Tuple[int, str, int], field_3: Tuple[int, int, int, int, int, int, int, int], field_4: Tuple[int, int, int], field_5: List[int], field_6: List[int]) -> None:
        super().__init__(mod=30, act=12)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5
        self.field_6 = field_6

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
            writer.write_int32(item_5)
        # 写入动态列表 field_6 (元素数 + 记录项)
        writer.write_uint16(len(self.field_6))
        for item_6 in self.field_6:
            writer.write_int32(item_6)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleNotifyResp":
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
            f_5.append(reader.read_int32())
        # 读取动态列表 f_6
        cnt_6 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_6 = []
        for _ in range(cnt_6):
            f_6.append(reader.read_int32())
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6)

@dataclass
class TakebibleNotifyGlobalReq(BasePacket):
    """TakeBible.notify_global 请求封包 (Mod 30, Act 13)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=13)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleNotifyGlobalReq":
        return cls()

@dataclass
class TakebibleNotifyGlobalResp(BasePacket):
    """TakeBible.notify_global 应答封包 (Mod 30, Act 13)"""

    field_0: int
    field_1: Tuple[str, int]
    field_2: Tuple[str, str, int]
    field_3: Tuple[int, str, int, int]

    def __init__(self, field_0: int, field_1: Tuple[str, int], field_2: Tuple[str, str, int], field_3: Tuple[int, str, int, int]) -> None:
        super().__init__(mod=30, act=13)
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
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        # 写入动态列表 field_3 (元素数 + 记录项)
        writer.write_uint16(len(self.field_3))
        for item_3 in self.field_3:
            writer.write_json(item_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleNotifyGlobalResp":
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
        # 读取动态列表 f_3
        cnt_3 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_3 = []
        for _ in range(cnt_3):
            f_3.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class TakebibleQuicklyReq(BasePacket):
    """TakeBible.quickly 请求封包 (Mod 30, Act 14)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=30, act=14)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleQuicklyReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class TakebibleQuicklyResp(BasePacket):
    """TakeBible.quickly 应答封包 (Mod 30, Act 14)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=30, act=14)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleQuicklyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class TakebibleGetTakeBibleUpdataDataReq(BasePacket):
    """TakeBible.get_take_bible_updata_data 请求封包 (Mod 30, Act 15)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=15)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleGetTakeBibleUpdataDataReq":
        return cls()

@dataclass
class TakebibleGetTakeBibleUpdataDataResp(BasePacket):
    """TakeBible.get_take_bible_updata_data 应答封包 (Mod 30, Act 15)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=30, act=15)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleGetTakeBibleUpdataDataResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class TakebibleGetRobTakeBibleCdTimeReq(BasePacket):
    """TakeBible.get_rob_take_bible_cd_time 请求封包 (Mod 30, Act 16)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=16)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleGetRobTakeBibleCdTimeReq":
        return cls()

@dataclass
class TakebibleGetRobTakeBibleCdTimeResp(BasePacket):
    """TakeBible.get_rob_take_bible_cd_time 应答封包 (Mod 30, Act 16)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=30, act=16)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleGetRobTakeBibleCdTimeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class TakebibleClearRobTakeBibleCdTimeReq(BasePacket):
    """TakeBible.clear_rob_take_bible_cd_time 请求封包 (Mod 30, Act 17)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=17)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleClearRobTakeBibleCdTimeReq":
        return cls()

@dataclass
class TakebibleClearRobTakeBibleCdTimeResp(BasePacket):
    """TakeBible.clear_rob_take_bible_cd_time 应答封包 (Mod 30, Act 17)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=30, act=17)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleClearRobTakeBibleCdTimeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class TakebibleBuyBlessReq(BasePacket):
    """TakeBible.buy_bless 请求封包 (Mod 30, Act 18)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=18)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleBuyBlessReq":
        return cls()

@dataclass
class TakebibleBuyBlessResp(BasePacket):
    """TakeBible.buy_bless 应答封包 (Mod 30, Act 18)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=30, act=18)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleBuyBlessResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class TakebibleGetPlayerTakeBibleMonsterReq(BasePacket):
    """TakeBible.get_player_take_bible_monster 请求封包 (Mod 30, Act 21)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=30, act=21)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleGetPlayerTakeBibleMonsterReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class TakebibleGetPlayerTakeBibleMonsterResp(BasePacket):
    """TakeBible.get_player_take_bible_monster 应答封包 (Mod 30, Act 21)"""

    field_0: int
    field_1: str
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int

    def __init__(self, field_0: int, field_1: str, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int) -> None:
        super().__init__(mod=30, act=21)
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
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int8(self.field_2)
        writer.write_int8(self.field_3)
        writer.write_int8(self.field_4)
        writer.write_int8(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int16(self.field_7)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleGetPlayerTakeBibleMonsterResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int8()
        f_3 = reader.read_int8()
        f_4 = reader.read_int8()
        f_5 = reader.read_int8()
        f_6 = reader.read_int32()
        f_7 = reader.read_int16()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7)

@dataclass
class TakebibleNotifyKillMonsterReq(BasePacket):
    """TakeBible.notify_kill_monster 请求封包 (Mod 30, Act 22)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=22)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleNotifyKillMonsterReq":
        return cls()

@dataclass
class TakebibleNotifyKillMonsterResp(BasePacket):
    """TakeBible.notify_kill_monster 应答封包 (Mod 30, Act 22)"""

    field_0: int
    field_1: str
    field_2: int
    field_3: str
    field_4: int

    def __init__(self, field_0: int, field_1: str, field_2: int, field_3: str, field_4: int) -> None:
        super().__init__(mod=30, act=22)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_utf(self.field_3)
        writer.write_int8(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleNotifyKillMonsterResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_utf()
        f_2 = reader.read_int32()
        f_3 = reader.read_utf()
        f_4 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class TakebibleGetRecentRobPlayerReq(BasePacket):
    """TakeBible.get_recent_rob_player 请求封包 (Mod 30, Act 23)"""

    def __init__(self) -> None:
        super().__init__(mod=30, act=23)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleGetRecentRobPlayerReq":
        return cls()

@dataclass
class TakebibleGetRecentRobPlayerResp(BasePacket):
    """TakeBible.get_recent_rob_player 应答封包 (Mod 30, Act 23)"""

    field_0: List[int]

    def __init__(self, field_0: List[int]) -> None:
        super().__init__(mod=30, act=23)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_int32(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakebibleGetRecentRobPlayerResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_int32())
        return cls(f_0)
