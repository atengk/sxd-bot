"""神仙道 Dance 模块协议代码契约 (Mod 76)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_Dance_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class DanceConstants:
    """Dance 模块业务状态与行为常量"""

    ERROR = 1
    SUCCESS = 0

@dataclass
class DanceGetDanceInfoReq(BasePacket):
    """Dance.get_dance_info 请求封包 (Mod 76, Act 0)"""

    def __init__(self) -> None:
        super().__init__(mod=76, act=0)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "DanceGetDanceInfoReq":
        return cls()

@dataclass
class DanceGetDanceInfoResp(BasePacket):
    """Dance.get_dance_info 应答封包 (Mod 76, Act 0)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=76, act=0)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int8(self.field_1)
        writer.write_int8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "DanceGetDanceInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int8()
        f_2 = reader.read_int8()
        return cls(f_0, f_1, f_2)

@dataclass
class DanceStartDanceReq(BasePacket):
    """Dance.start_dance 请求封包 (Mod 76, Act 1)"""

    def __init__(self) -> None:
        super().__init__(mod=76, act=1)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "DanceStartDanceReq":
        return cls()

@dataclass
class DanceStartDanceResp(BasePacket):
    """Dance.start_dance 应答封包 (Mod 76, Act 1)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=76, act=1)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "DanceStartDanceResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class DanceReceiveAwardReq(BasePacket):
    """Dance.receive_award 请求封包 (Mod 76, Act 2)"""

    def __init__(self) -> None:
        super().__init__(mod=76, act=2)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "DanceReceiveAwardReq":
        return cls()

@dataclass
class DanceReceiveAwardResp(BasePacket):
    """Dance.receive_award 应答封包 (Mod 76, Act 2)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=76, act=2)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "DanceReceiveAwardResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class DanceNotifyStartDanceReq(BasePacket):
    """Dance.notify_start_dance 请求封包 (Mod 76, Act 3)"""

    def __init__(self) -> None:
        super().__init__(mod=76, act=3)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "DanceNotifyStartDanceReq":
        return cls()

@dataclass
class DanceNotifyStartDanceResp(BasePacket):
    """Dance.notify_start_dance 应答封包 (Mod 76, Act 3)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=76, act=3)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "DanceNotifyStartDanceResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class DanceNotifyDanceStatusReq(BasePacket):
    """Dance.notify_dance_status 请求封包 (Mod 76, Act 4)"""

    def __init__(self) -> None:
        super().__init__(mod=76, act=4)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "DanceNotifyDanceStatusReq":
        return cls()

@dataclass
class DanceNotifyDanceStatusResp(BasePacket):
    """Dance.notify_dance_status 应答封包 (Mod 76, Act 4)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=76, act=4)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "DanceNotifyDanceStatusResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class DanceGetActivityOpenTimestampReq(BasePacket):
    """Dance.get_activity_open_timestamp 请求封包 (Mod 76, Act 5)"""

    def __init__(self) -> None:
        super().__init__(mod=76, act=5)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "DanceGetActivityOpenTimestampReq":
        return cls()

@dataclass
class DanceGetActivityOpenTimestampResp(BasePacket):
    """Dance.get_activity_open_timestamp 应答封包 (Mod 76, Act 5)"""

    field_0: List[int]

    def __init__(self, field_0: List[int]) -> None:
        super().__init__(mod=76, act=5)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_int32(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "DanceGetActivityOpenTimestampResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_int32())
        return cls(f_0)
