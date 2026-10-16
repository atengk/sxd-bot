"""神仙道 Fate 模块协议代码契约 (Mod 22)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_Fate_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class FateConstants:
    """Fate 模块业务状态与行为常量"""

    BAG_FULL = 1
    BAG_TO_ROLE = 17
    CANT_MERGE = 20
    CANT_TAICHU_QIANLI = 21
    FAILD = 43
    FAILED = 4
    FALSE = 39
    FATE_CAN_EXCHANGE = 25
    FATE_CAN_PICK_UP = 3
    FATE_PACK_FULL = 33
    FULL_BUY_TIMES = 24
    FULL_TEMP_BAG = 13
    FUNCTION_NO_OPEN = 36
    HAVE_SAME_TYPE_FATE = 7
    HAVE_WEAR_ON = 8
    INVALID_FATE_NPC_ID = 12
    INVALID_GRID = 2
    INVALID_LEVEL = 10
    INVALID_NPC_ID = 23
    INVALID_POSITION = 9
    IN_BAG = 15
    IS_LOCKED = 11
    LIMILT_NUM = 42
    MAX_BAG_NUMBER = 6
    MAX_LEVEL = 19
    NOT_BREAKTHROUGHS = 41
    NOT_ENOUGH_COIN = 14
    NOT_ENOUGH_COINS = 37
    NOT_ENOUGH_COUNT = 27
    NOT_ENOUGH_INGOT = 5
    NOT_ENOUGH_LEVEL = 26
    NOT_ENOUGH_MING_GONG = 40
    NO_ENOUGH_BAGS = 30
    NO_ENOUGH_COINS = 31
    NO_ENOUGH_LEVEL = 32
    NO_MERGE_ENOUGH_LEVEL = 22
    ON_ROLE = 16
    PLAYER_CANCEL = 34
    PURPLE = 28
    ROLE_TO_BAG = 18
    SUCCESS = 0
    TRUE = 38
    UPGRADED_ALL = 35
    YELLOW = 29

@dataclass
class FateGetFateNpcReq(BasePacket):
    """Fate.get_fate_npc 请求封包 (Mod 22, Act 0)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=0)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateGetFateNpcReq":
        return cls()

@dataclass
class FateGetFateNpcResp(BasePacket):
    """Fate.get_fate_npc 应答封包 (Mod 22, Act 0)"""

    field_0: int
    field_1: Tuple[int, int, int, int, int]
    field_2: int

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, int, int], field_2: int) -> None:
        super().__init__(mod=22, act=0)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateGetFateNpcResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class FateGetTempFateReq(BasePacket):
    """Fate.get_temp_fate 请求封包 (Mod 22, Act 1)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=1)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateGetTempFateReq":
        return cls()

@dataclass
class FateGetTempFateResp(BasePacket):
    """Fate.get_temp_fate 应答封包 (Mod 22, Act 1)"""

    field_0: Tuple[int, int]

    def __init__(self, field_0: Tuple[int, int]) -> None:
        super().__init__(mod=22, act=1)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateGetTempFateResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class FatePickupFateReq(BasePacket):
    """Fate.pickup_fate 请求封包 (Mod 22, Act 2)"""

    field_0: List[int]

    def __init__(self, field_0: List[int]) -> None:
        super().__init__(mod=22, act=2)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 复杂类型字段 field_0: ['LongUtil']
        writer.write_json(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FatePickupFateReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_json()
        return cls(f_0)

@dataclass
class FatePickupFateResp(BasePacket):
    """Fate.pickup_fate 应答封包 (Mod 22, Act 2)"""

    field_0: int
    field_1: List[int]

    def __init__(self, field_0: int, field_1: List[int]) -> None:
        super().__init__(mod=22, act=2)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_int64(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FatePickupFateResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_int64())
        return cls(f_0, f_1)

@dataclass
class FateSaleTempFateReq(BasePacket):
    """Fate.sale_temp_fate 请求封包 (Mod 22, Act 3)"""

    field_0: List[int]

    def __init__(self, field_0: List[int]) -> None:
        super().__init__(mod=22, act=3)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 复杂类型字段 field_0: ['LongUtil']
        writer.write_json(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateSaleTempFateReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_json()
        return cls(f_0)

@dataclass
class FateSaleTempFateResp(BasePacket):
    """Fate.sale_temp_fate 应答封包 (Mod 22, Act 3)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=3)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateSaleTempFateResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateGetBagListReq(BasePacket):
    """Fate.get_bag_list 请求封包 (Mod 22, Act 4)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=4)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateGetBagListReq":
        return cls()

@dataclass
class FateGetBagListResp(BasePacket):
    """Fate.get_bag_list 应答封包 (Mod 22, Act 4)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, List[int], int, int]
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: Tuple[int, int]
    field_7: int
    field_8: int
    field_9: int
    field_10: Tuple[int, int, Tuple[int, int]]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, List[int], int, int], field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: Tuple[int, int], field_7: int, field_8: int, field_9: int, field_10: Tuple[int, int, Tuple[int, int]]) -> None:
        super().__init__(mod=22, act=4)
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

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        # 写入动态列表 field_6 (元素数 + 记录项)
        writer.write_uint16(len(self.field_6))
        for item_6 in self.field_6:
            writer.write_json(item_6)
        writer.write_int8(self.field_7)
        writer.write_int8(self.field_8)
        writer.write_int32(self.field_9)
        # 写入动态列表 field_10 (元素数 + 记录项)
        writer.write_uint16(len(self.field_10))
        for item_10 in self.field_10:
            writer.write_json(item_10)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateGetBagListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        # 读取动态列表 f_6
        cnt_6 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_6 = []
        for _ in range(cnt_6):
            f_6.append(reader.read_json())
        f_7 = reader.read_int8()
        f_8 = reader.read_int8()
        f_9 = reader.read_int32()
        # 读取动态列表 f_10
        cnt_10 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_10 = []
        for _ in range(cnt_10):
            f_10.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10)

@dataclass
class FateBuyBagGridReq(BasePacket):
    """Fate.buy_bag_grid 请求封包 (Mod 22, Act 5)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=5)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateBuyBagGridReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FateBuyBagGridResp(BasePacket):
    """Fate.buy_bag_grid 应答封包 (Mod 22, Act 5)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=5)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateBuyBagGridResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateGetRoleFateListReq(BasePacket):
    """Fate.get_role_fate_list 请求封包 (Mod 22, Act 6)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=6)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateGetRoleFateListReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FateGetRoleFateListResp(BasePacket):
    """Fate.get_role_fate_list 应答封包 (Mod 22, Act 6)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, List[int], int, int]
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, List[int], int, int], field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int) -> None:
        super().__init__(mod=22, act=6)
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
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        writer.write_int32(self.field_1)
        writer.write_int8(self.field_2)
        writer.write_int8(self.field_3)
        writer.write_int8(self.field_4)
        writer.write_int8(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int8(self.field_7)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateGetRoleFateListResp":
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
        f_6 = reader.read_int32()
        f_7 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7)

@dataclass
class FateWearOnReq(BasePacket):
    """Fate.wear_on 请求封包 (Mod 22, Act 7)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=22, act=7)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateWearOnReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int8()
        return cls(f_0, f_1, f_2)

@dataclass
class FateWearOnResp(BasePacket):
    """Fate.wear_on 应答封包 (Mod 22, Act 7)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=22, act=7)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateWearOnResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class FateDiscardFateReq(BasePacket):
    """Fate.discard_fate 请求封包 (Mod 22, Act 8)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=8)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateDiscardFateReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FateDiscardFateResp(BasePacket):
    """Fate.discard_fate 应答封包 (Mod 22, Act 8)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=8)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateDiscardFateResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateAppointFateNpcReq(BasePacket):
    """Fate.appoint_fate_npc 请求封包 (Mod 22, Act 9)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=9)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateAppointFateNpcReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class FateAppointFateNpcResp(BasePacket):
    """Fate.appoint_fate_npc 应答封包 (Mod 22, Act 9)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=22, act=9)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int8(self.field_2)
        writer.write_int64(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateAppointFateNpcResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int16()
        f_2 = reader.read_int8()
        f_3 = reader.read_int64()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class FateWearOffFateReq(BasePacket):
    """Fate.wear_off_fate 请求封包 (Mod 22, Act 10)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=22, act=10)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateWearOffFateReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class FateWearOffFateResp(BasePacket):
    """Fate.wear_off_fate 应答封包 (Mod 22, Act 10)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=10)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateWearOffFateResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateChangeFateGridReq(BasePacket):
    """Fate.change_fate_grid 请求封包 (Mod 22, Act 12)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=22, act=12)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateChangeFateGridReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class FateChangeFateGridResp(BasePacket):
    """Fate.change_fate_grid 应答封包 (Mod 22, Act 12)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=12)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateChangeFateGridResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateMergeReq(BasePacket):
    """Fate.merge 请求封包 (Mod 22, Act 13)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=22, act=13)
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
    def decode(cls, data: bytes) -> "FateMergeReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_uint8()
        return cls(f_0, f_1, f_2)

@dataclass
class FateMergeResp(BasePacket):
    """Fate.merge 应答封包 (Mod 22, Act 13)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int
    field_8: int
    field_9: List[int]
    field_10: int
    field_11: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int, field_9: List[int], field_10: int, field_11: int) -> None:
        super().__init__(mod=22, act=13)
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
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int16(self.field_2)
        writer.write_int8(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int8(self.field_6)
        writer.write_int32(self.field_7)
        writer.write_int8(self.field_8)
        # 写入动态列表 field_9 (元素数 + 记录项)
        writer.write_uint16(len(self.field_9))
        for item_9 in self.field_9:
            writer.write_int16(item_9)
        writer.write_int32(self.field_10)
        writer.write_int16(self.field_11)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateMergeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int16()
        f_3 = reader.read_int8()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        f_6 = reader.read_int8()
        f_7 = reader.read_int32()
        f_8 = reader.read_int8()
        # 读取动态列表 f_9
        cnt_9 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_9 = []
        for _ in range(cnt_9):
            f_9.append(reader.read_int16())
        f_10 = reader.read_int32()
        f_11 = reader.read_int16()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11)

@dataclass
class FateChangePositionReq(BasePacket):
    """Fate.change_position 请求封包 (Mod 22, Act 14)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=22, act=14)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateChangePositionReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class FateChangePositionResp(BasePacket):
    """Fate.change_position 应答封包 (Mod 22, Act 14)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=14)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateChangePositionResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateGetPlayerRoleFatePowerReq(BasePacket):
    """Fate.get_player_role_fate_power 请求封包 (Mod 22, Act 15)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=15)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateGetPlayerRoleFatePowerReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FateGetPlayerRoleFatePowerResp(BasePacket):
    """Fate.get_player_role_fate_power 应答封包 (Mod 22, Act 15)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=15)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateGetPlayerRoleFatePowerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FateGetMergeDataReq(BasePacket):
    """Fate.get_merge_data 请求封包 (Mod 22, Act 16)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=22, act=16)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateGetMergeDataReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int16()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class FateGetMergeDataResp(BasePacket):
    """Fate.get_merge_data 应答封包 (Mod 22, Act 16)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=16)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateGetMergeDataResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        return cls(f_0)

@dataclass
class FateMergeAllInBagReq(BasePacket):
    """Fate.merge_all_in_bag 请求封包 (Mod 22, Act 17)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=17)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateMergeAllInBagReq":
        return cls()

@dataclass
class FateMergeAllInBagResp(BasePacket):
    """Fate.merge_all_in_bag 应答封包 (Mod 22, Act 17)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=17)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateMergeAllInBagResp":
        return cls()

@dataclass
class FateBuyFateNpcReq(BasePacket):
    """Fate.buy_fate_npc 请求封包 (Mod 22, Act 18)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=18)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateBuyFateNpcReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class FateBuyFateNpcResp(BasePacket):
    """Fate.buy_fate_npc 应答封包 (Mod 22, Act 18)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=18)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateBuyFateNpcResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateExchangeFateReq(BasePacket):
    """Fate.exchange_fate 请求封包 (Mod 22, Act 19)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=19)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateExchangeFateReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        return cls(f_0)

@dataclass
class FateExchangeFateResp(BasePacket):
    """Fate.exchange_fate 应答封包 (Mod 22, Act 19)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=19)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateExchangeFateResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateGetScrapAmountReq(BasePacket):
    """Fate.get_scrap_amount 请求封包 (Mod 22, Act 20)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=20)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateGetScrapAmountReq":
        return cls()

@dataclass
class FateGetScrapAmountResp(BasePacket):
    """Fate.get_scrap_amount 应答封包 (Mod 22, Act 20)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=22, act=20)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateGetScrapAmountResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class FateMergeAllNormalInBagReq(BasePacket):
    """Fate.merge_all_normal_in_bag 请求封包 (Mod 22, Act 21)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=21)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateMergeAllNormalInBagReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateMergeAllNormalInBagResp(BasePacket):
    """Fate.merge_all_normal_in_bag 应答封包 (Mod 22, Act 21)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=21)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateMergeAllNormalInBagResp":
        return cls()

@dataclass
class FateExchangeUnknowFireReq(BasePacket):
    """Fate.exchange_unknow_fire 请求封包 (Mod 22, Act 22)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=22)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateExchangeUnknowFireReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FateExchangeUnknowFireResp(BasePacket):
    """Fate.exchange_unknow_fire 应答封包 (Mod 22, Act 22)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=22)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateExchangeUnknowFireResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateGetFateCatSkillReq(BasePacket):
    """Fate.get_fate_cat_skill 请求封包 (Mod 22, Act 23)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=23)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateGetFateCatSkillReq":
        return cls()

@dataclass
class FateGetFateCatSkillResp(BasePacket):
    """Fate.get_fate_cat_skill 应答封包 (Mod 22, Act 23)"""

    field_0: int
    field_1: int
    field_2: List[int]

    def __init__(self, field_0: int, field_1: int, field_2: List[int]) -> None:
        super().__init__(mod=22, act=23)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int16(self.field_1)
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_int32(item_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateGetFateCatSkillResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int16()
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_int32())
        return cls(f_0, f_1, f_2)

@dataclass
class FateUseFateCatSkillReq(BasePacket):
    """Fate.use_fate_cat_skill 请求封包 (Mod 22, Act 24)"""

    field_0: List[int]

    def __init__(self, field_0: List[int]) -> None:
        super().__init__(mod=22, act=24)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 复杂类型字段 field_0: ['IntUtil']
        writer.write_json(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateUseFateCatSkillReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_json()
        return cls(f_0)

@dataclass
class FateUseFateCatSkillResp(BasePacket):
    """Fate.use_fate_cat_skill 应答封包 (Mod 22, Act 24)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=24)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateUseFateCatSkillResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateCrazyFateReq(BasePacket):
    """Fate.crazy_fate 请求封包 (Mod 22, Act 25)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=25)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateCrazyFateReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FateCrazyFateResp(BasePacket):
    """Fate.crazy_fate 应答封包 (Mod 22, Act 25)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=25)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateCrazyFateResp":
        return cls()

@dataclass
class FateCancelCrazyFateReq(BasePacket):
    """Fate.cancel_crazy_fate 请求封包 (Mod 22, Act 26)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=26)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateCancelCrazyFateReq":
        return cls()

@dataclass
class FateCancelCrazyFateResp(BasePacket):
    """Fate.cancel_crazy_fate 应答封包 (Mod 22, Act 26)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=26)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateCancelCrazyFateResp":
        return cls()

@dataclass
class FateNotifyCrazyFateResultReq(BasePacket):
    """Fate.notify_crazy_fate_result 请求封包 (Mod 22, Act 27)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=27)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateNotifyCrazyFateResultReq":
        return cls()

@dataclass
class FateNotifyCrazyFateResultResp(BasePacket):
    """Fate.notify_crazy_fate_result 应答封包 (Mod 22, Act 27)"""

    field_0: int
    field_1: List[int]
    field_2: int
    field_3: int
    field_4: int

    def __init__(self, field_0: int, field_1: List[int], field_2: int, field_3: int, field_4: int) -> None:
        super().__init__(mod=22, act=27)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_int16(item_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateNotifyCrazyFateResultResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_int16())
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class FateGetUpgradeFateNpcIdReq(BasePacket):
    """Fate.get_upgrade_fate_npc_id 请求封包 (Mod 22, Act 28)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=28)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateGetUpgradeFateNpcIdReq":
        return cls()

@dataclass
class FateGetUpgradeFateNpcIdResp(BasePacket):
    """Fate.get_upgrade_fate_npc_id 应答封包 (Mod 22, Act 28)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=22, act=28)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateGetUpgradeFateNpcIdResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class FateUpgradeFateNpcReq(BasePacket):
    """Fate.upgrade_fate_npc 请求封包 (Mod 22, Act 29)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=29)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateUpgradeFateNpcReq":
        return cls()

@dataclass
class FateUpgradeFateNpcResp(BasePacket):
    """Fate.upgrade_fate_npc 应答封包 (Mod 22, Act 29)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=22, act=29)
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
    def decode(cls, data: bytes) -> "FateUpgradeFateNpcResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class FateGetFateInnUpgradeFlagReq(BasePacket):
    """Fate.get_fate_inn_upgrade_flag 请求封包 (Mod 22, Act 30)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=30)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateGetFateInnUpgradeFlagReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FateGetFateInnUpgradeFlagResp(BasePacket):
    """Fate.get_fate_inn_upgrade_flag 应答封包 (Mod 22, Act 30)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=30)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateGetFateInnUpgradeFlagResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateGetMingGongInfoReq(BasePacket):
    """Fate.get_ming_gong_info 请求封包 (Mod 22, Act 31)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=31)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateGetMingGongInfoReq":
        return cls()

@dataclass
class FateGetMingGongInfoResp(BasePacket):
    """Fate.get_ming_gong_info 应答封包 (Mod 22, Act 31)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=22, act=31)
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
    def decode(cls, data: bytes) -> "FateGetMingGongInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class FateExchangeMingGongReq(BasePacket):
    """Fate.exchange_ming_gong 请求封包 (Mod 22, Act 32)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=32)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateExchangeMingGongReq":
        return cls()

@dataclass
class FateExchangeMingGongResp(BasePacket):
    """Fate.exchange_ming_gong 应答封包 (Mod 22, Act 32)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=22, act=32)
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
    def decode(cls, data: bytes) -> "FateExchangeMingGongResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class FateBreakthroughsFateReq(BasePacket):
    """Fate.breakthroughs_fate 请求封包 (Mod 22, Act 33)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=33)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateBreakthroughsFateReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FateBreakthroughsFateResp(BasePacket):
    """Fate.breakthroughs_fate 应答封包 (Mod 22, Act 33)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=22, act=33)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int8(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateBreakthroughsFateResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int8()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class FateExchangeMingGongScrapReq(BasePacket):
    """Fate.exchange_ming_gong_scrap 请求封包 (Mod 22, Act 34)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=34)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateExchangeMingGongScrapReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FateExchangeMingGongScrapResp(BasePacket):
    """Fate.exchange_ming_gong_scrap 应答封包 (Mod 22, Act 34)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=22, act=34)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateExchangeMingGongScrapResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class FateFateLockReq(BasePacket):
    """Fate.fate_lock 请求封包 (Mod 22, Act 35)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=35)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateFateLockReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FateFateLockResp(BasePacket):
    """Fate.fate_lock 应答封包 (Mod 22, Act 35)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=35)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateFateLockResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateFateUnlockReq(BasePacket):
    """Fate.fate_unlock 请求封包 (Mod 22, Act 36)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=36)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateFateUnlockReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FateFateUnlockResp(BasePacket):
    """Fate.fate_unlock 应答封包 (Mod 22, Act 36)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=36)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateFateUnlockResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateUnlockFateReq(BasePacket):
    """Fate.unlock_fate 请求封包 (Mod 22, Act 37)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=22, act=37)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateUnlockFateReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class FateUnlockFateResp(BasePacket):
    """Fate.unlock_fate 应答封包 (Mod 22, Act 37)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=22, act=37)
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
    def decode(cls, data: bytes) -> "FateUnlockFateResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class FateNewCrazyFateReq(BasePacket):
    """Fate.new_crazy_fate 请求封包 (Mod 22, Act 38)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=38)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateNewCrazyFateReq":
        return cls()

@dataclass
class FateNewCrazyFateResp(BasePacket):
    """Fate.new_crazy_fate 应答封包 (Mod 22, Act 38)"""

    field_0: int
    field_1: List[int]
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: List[int], field_2: int, field_3: int) -> None:
        super().__init__(mod=22, act=38)
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
            writer.write_int16(item_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateNewCrazyFateResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_int16())
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class FateSetFateMergeSettingReq(BasePacket):
    """Fate.set_fate_merge_setting 请求封包 (Mod 22, Act 39)"""

    field_0: Tuple[int, int]

    def __init__(self, field_0: Tuple[int, int]) -> None:
        super().__init__(mod=22, act=39)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 复杂类型字段 field_0: ['ByteUtil', 'ByteUtil']
        writer.write_json(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateSetFateMergeSettingReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_json()
        return cls(f_0)

@dataclass
class FateSetFateMergeSettingResp(BasePacket):
    """Fate.set_fate_merge_setting 应答封包 (Mod 22, Act 39)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=39)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateSetFateMergeSettingResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateChangeTaichuAutoMergeStateReq(BasePacket):
    """Fate.change_taichu_auto_merge_state 请求封包 (Mod 22, Act 40)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=40)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateChangeTaichuAutoMergeStateReq":
        return cls()

@dataclass
class FateChangeTaichuAutoMergeStateResp(BasePacket):
    """Fate.change_taichu_auto_merge_state 应答封包 (Mod 22, Act 40)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=40)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateChangeTaichuAutoMergeStateResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FateClassifyWareReq(BasePacket):
    """Fate.classify_ware 请求封包 (Mod 22, Act 41)"""

    def __init__(self) -> None:
        super().__init__(mod=22, act=41)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FateClassifyWareReq":
        return cls()

@dataclass
class FateClassifyWareResp(BasePacket):
    """Fate.classify_ware 应答封包 (Mod 22, Act 41)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=22, act=41)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateClassifyWareResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)
