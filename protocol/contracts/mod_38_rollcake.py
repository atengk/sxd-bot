"""神仙道 RollCake 模块协议代码契约 (Mod 38)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_RollCake_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class RollcakeConstants:
    """RollCake 模块业务状态与行为常量"""

    FAILURE = 1
    HAVE_RECORD = 5
    NOT_ENOUGH_INGOT = 2
    NO_CHANG_LUCK_TIMES = 3
    NO_RECORD = 4
    SUCCESS = 0

@dataclass
class RollcakeRollReq(BasePacket):
    """RollCake.roll 请求封包 (Mod 38, Act 0)"""

    def __init__(self) -> None:
        super().__init__(mod=38, act=0)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "RollcakeRollReq":
        return cls()

@dataclass
class RollcakeRollResp(BasePacket):
    """RollCake.roll 应答封包 (Mod 38, Act 0)"""

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
        super().__init__(mod=38, act=0)
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
        writer.write_int8(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int8(self.field_3)
        writer.write_int8(self.field_4)
        writer.write_int8(self.field_5)
        writer.write_int8(self.field_6)
        writer.write_int8(self.field_7)
        writer.write_int8(self.field_8)
        writer.write_int32(self.field_9)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "RollcakeRollResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int8()
        f_2 = reader.read_int32()
        f_3 = reader.read_int8()
        f_4 = reader.read_int8()
        f_5 = reader.read_int8()
        f_6 = reader.read_int8()
        f_7 = reader.read_int8()
        f_8 = reader.read_int8()
        f_9 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9)

@dataclass
class RollcakeGetCountReq(BasePacket):
    """RollCake.get_count 请求封包 (Mod 38, Act 2)"""

    def __init__(self) -> None:
        super().__init__(mod=38, act=2)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "RollcakeGetCountReq":
        return cls()

@dataclass
class RollcakeGetCountResp(BasePacket):
    """RollCake.get_count 应答封包 (Mod 38, Act 2)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=38, act=2)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int8(self.field_1)
        writer.write_int8(self.field_2)
        writer.write_int32(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "RollcakeGetCountResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int8()
        f_2 = reader.read_int8()
        f_3 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class RollcakeRerollReq(BasePacket):
    """RollCake.reroll 请求封包 (Mod 38, Act 3)"""

    def __init__(self) -> None:
        super().__init__(mod=38, act=3)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "RollcakeRerollReq":
        return cls()

@dataclass
class RollcakeRerollResp(BasePacket):
    """RollCake.reroll 应答封包 (Mod 38, Act 3)"""

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

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int, field_9: int, field_10: int) -> None:
        super().__init__(mod=38, act=3)
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
        writer.write_uint8(self.field_0)
        writer.write_int8(self.field_1)
        writer.write_int8(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int8(self.field_4)
        writer.write_int8(self.field_5)
        writer.write_int8(self.field_6)
        writer.write_int8(self.field_7)
        writer.write_int8(self.field_8)
        writer.write_int8(self.field_9)
        writer.write_int32(self.field_10)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "RollcakeRerollResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int8()
        f_2 = reader.read_int8()
        f_3 = reader.read_int32()
        f_4 = reader.read_int8()
        f_5 = reader.read_int8()
        f_6 = reader.read_int8()
        f_7 = reader.read_int8()
        f_8 = reader.read_int8()
        f_9 = reader.read_int8()
        f_10 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10)

@dataclass
class RollcakeGetAwardReq(BasePacket):
    """RollCake.get_award 请求封包 (Mod 38, Act 4)"""

    def __init__(self) -> None:
        super().__init__(mod=38, act=4)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "RollcakeGetAwardReq":
        return cls()

@dataclass
class RollcakeGetAwardResp(BasePacket):
    """RollCake.get_award 应答封包 (Mod 38, Act 4)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=38, act=4)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "RollcakeGetAwardResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class RollcakeGetStateReq(BasePacket):
    """RollCake.get_state 请求封包 (Mod 38, Act 5)"""

    def __init__(self) -> None:
        super().__init__(mod=38, act=5)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "RollcakeGetStateReq":
        return cls()

@dataclass
class RollcakeGetStateResp(BasePacket):
    """RollCake.get_state 应答封包 (Mod 38, Act 5)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int
    field_8: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int) -> None:
        super().__init__(mod=38, act=5)
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
        writer.write_int8(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int8(self.field_3)
        writer.write_int8(self.field_4)
        writer.write_int8(self.field_5)
        writer.write_int8(self.field_6)
        writer.write_int8(self.field_7)
        writer.write_int8(self.field_8)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "RollcakeGetStateResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int8()
        f_2 = reader.read_int32()
        f_3 = reader.read_int8()
        f_4 = reader.read_int8()
        f_5 = reader.read_int8()
        f_6 = reader.read_int8()
        f_7 = reader.read_int8()
        f_8 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8)

@dataclass
class RollcakeIsAutoReq(BasePacket):
    """RollCake.is_auto 请求封包 (Mod 38, Act 6)"""

    def __init__(self) -> None:
        super().__init__(mod=38, act=6)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "RollcakeIsAutoReq":
        return cls()

@dataclass
class RollcakeIsAutoResp(BasePacket):
    """RollCake.is_auto 应答封包 (Mod 38, Act 6)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=38, act=6)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "RollcakeIsAutoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class RollcakeSetAutoReq(BasePacket):
    """RollCake.set_auto 请求封包 (Mod 38, Act 7)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=38, act=7)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "RollcakeSetAutoReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class RollcakeSetAutoResp(BasePacket):
    """RollCake.set_auto 应答封包 (Mod 38, Act 7)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=38, act=7)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "RollcakeSetAutoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)
