"""神仙道 MissionPractice 模块协议代码契约 (Mod 25)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_MissionPractice_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class MissionpracticeConstants:
    """MissionPractice 模块业务状态与行为常量"""

    BAG_FULL = 2
    IN_PRACTICE = 3
    NEW_WAR_REPORT = 5
    NOT_ENOUGH_INGOT = 4
    NOT_ENOUGH_POWER = 1
    RANK_REPORT = 6
    SUCCESS = 0
    UPDATE_TIME = 7

@dataclass
class MissionpracticeGetPracticeInfoReq(BasePacket):
    """MissionPractice.get_practice_info 请求封包 (Mod 25, Act 0)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=25, act=0)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeGetPracticeInfoReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class MissionpracticeGetPracticeInfoResp(BasePacket):
    """MissionPractice.get_practice_info 应答封包 (Mod 25, Act 0)"""

    field_0: int
    field_1: Tuple[int, int, int]
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: Tuple[int, int, int], field_2: int, field_3: int) -> None:
        super().__init__(mod=25, act=0)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        writer.write_int8(self.field_2)
        writer.write_int64(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeGetPracticeInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        f_2 = reader.read_int8()
        f_3 = reader.read_int64()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class MissionpracticeStartPracticeReq(BasePacket):
    """MissionPractice.start_practice 请求封包 (Mod 25, Act 1)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=25, act=1)
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
    def decode(cls, data: bytes) -> "MissionpracticeStartPracticeReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int16()
        f_2 = reader.read_int8()
        return cls(f_0, f_1, f_2)

@dataclass
class MissionpracticeStartPracticeResp(BasePacket):
    """MissionPractice.start_practice 应答封包 (Mod 25, Act 1)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=25, act=1)
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
    def decode(cls, data: bytes) -> "MissionpracticeStartPracticeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class MissionpracticeCancelPracticeReq(BasePacket):
    """MissionPractice.cancel_practice 请求封包 (Mod 25, Act 2)"""

    def __init__(self) -> None:
        super().__init__(mod=25, act=2)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeCancelPracticeReq":
        return cls()

@dataclass
class MissionpracticeCancelPracticeResp(BasePacket):
    """MissionPractice.cancel_practice 应答封包 (Mod 25, Act 2)"""

    def __init__(self) -> None:
        super().__init__(mod=25, act=2)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeCancelPracticeResp":
        return cls()

@dataclass
class MissionpracticeQuicklyReq(BasePacket):
    """MissionPractice.quickly 请求封包 (Mod 25, Act 3)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=25, act=3)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeQuicklyReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        return cls(f_0)

@dataclass
class MissionpracticeQuicklyResp(BasePacket):
    """MissionPractice.quickly 应答封包 (Mod 25, Act 3)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=25, act=3)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeQuicklyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class MissionpracticeNotifyReq(BasePacket):
    """MissionPractice.notify 请求封包 (Mod 25, Act 4)"""

    def __init__(self) -> None:
        super().__init__(mod=25, act=4)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeNotifyReq":
        return cls()

@dataclass
class MissionpracticeNotifyResp(BasePacket):
    """MissionPractice.notify 应答封包 (Mod 25, Act 4)"""

    field_0: int
    field_1: Tuple[int, int, int, Tuple[int, int], Tuple[int, int], int]
    field_2: Tuple[int, int, int, Tuple[int, int], Tuple[int, int], int, int, int, int, int, int]
    field_3: int
    field_4: int

    def __init__(self, field_0: int, field_1: Tuple[int, int, int, Tuple[int, int], Tuple[int, int], int], field_2: Tuple[int, int, int, Tuple[int, int], Tuple[int, int], int, int, int, int, int, int], field_3: int, field_4: int) -> None:
        super().__init__(mod=25, act=4)
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
            writer.write_json(item_1)
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeNotifyResp":
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
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class MissionpracticeGetContinuePracticeInfoReq(BasePacket):
    """MissionPractice.get_continue_practice_info 请求封包 (Mod 25, Act 5)"""

    def __init__(self) -> None:
        super().__init__(mod=25, act=5)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeGetContinuePracticeInfoReq":
        return cls()

@dataclass
class MissionpracticeGetContinuePracticeInfoResp(BasePacket):
    """MissionPractice.get_continue_practice_info 应答封包 (Mod 25, Act 5)"""

    field_0: int
    field_1: Tuple[int, int, int]
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int
    field_8: int

    def __init__(self, field_0: int, field_1: Tuple[int, int, int], field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int) -> None:
        super().__init__(mod=25, act=5)
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
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        writer.write_int8(self.field_2)
        writer.write_int64(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int16(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int32(self.field_7)
        writer.write_int8(self.field_8)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeGetContinuePracticeInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        f_2 = reader.read_int8()
        f_3 = reader.read_int64()
        f_4 = reader.read_int32()
        f_5 = reader.read_int16()
        f_6 = reader.read_int32()
        f_7 = reader.read_int32()
        f_8 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8)

@dataclass
class MissionpracticeContinuePracticeReq(BasePacket):
    """MissionPractice.continue_practice 请求封包 (Mod 25, Act 6)"""

    def __init__(self) -> None:
        super().__init__(mod=25, act=6)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeContinuePracticeReq":
        return cls()

@dataclass
class MissionpracticeContinuePracticeResp(BasePacket):
    """MissionPractice.continue_practice 应答封包 (Mod 25, Act 6)"""

    def __init__(self) -> None:
        super().__init__(mod=25, act=6)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeContinuePracticeResp":
        return cls()

@dataclass
class MissionpracticeSetAutoSaleItemReq(BasePacket):
    """MissionPractice.set_auto_sale_item 请求封包 (Mod 25, Act 7)"""

    def __init__(self) -> None:
        super().__init__(mod=25, act=7)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeSetAutoSaleItemReq":
        return cls()

@dataclass
class MissionpracticeSetAutoSaleItemResp(BasePacket):
    """MissionPractice.set_auto_sale_item 应答封包 (Mod 25, Act 7)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=25, act=7)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeSetAutoSaleItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class MissionpracticeCancelAutoSaleItemReq(BasePacket):
    """MissionPractice.cancel_auto_sale_item 请求封包 (Mod 25, Act 8)"""

    def __init__(self) -> None:
        super().__init__(mod=25, act=8)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeCancelAutoSaleItemReq":
        return cls()

@dataclass
class MissionpracticeCancelAutoSaleItemResp(BasePacket):
    """MissionPractice.cancel_auto_sale_item 应答封包 (Mod 25, Act 8)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=25, act=8)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "MissionpracticeCancelAutoSaleItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)
