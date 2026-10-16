"""神仙道 Assistant 模块协议代码契约 (Mod 52)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_Assistant_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class AssistantConstants:
    """Assistant 模块业务状态与行为常量"""

    FAILED = 5
    FIND_IMMORTAL_LIMIT = 7
    FISHHOOK_LIMIT = 6
    HAVE_DONE = 4
    NOT_ENOUGH_NUM = 2
    NOT_ENOUGH_VIP = 1
    PACK_FULL = 3
    SUCCESS = 0

@dataclass
class AssistantInfoReq(BasePacket):
    """Assistant.info 请求封包 (Mod 52, Act 0)"""

    def __init__(self) -> None:
        super().__init__(mod=52, act=0)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "AssistantInfoReq":
        return cls()

@dataclass
class AssistantInfoResp(BasePacket):
    """Assistant.info 应答封包 (Mod 52, Act 0)"""

    field_0: Tuple[int, int, List[int]]
    field_1: Tuple[int, int, int]

    def __init__(self, field_0: Tuple[int, int, List[int]], field_1: Tuple[int, int, int]) -> None:
        super().__init__(mod=52, act=0)
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
    def decode(cls, data: bytes) -> "AssistantInfoResp":
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
class AssistantGetAwardReq(BasePacket):
    """Assistant.get_award 请求封包 (Mod 52, Act 1)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=52, act=1)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "AssistantGetAwardReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class AssistantGetAwardResp(BasePacket):
    """Assistant.get_award 应答封包 (Mod 52, Act 1)"""

    field_0: int
    field_1: Tuple[int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int]) -> None:
        super().__init__(mod=52, act=1)
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
    def decode(cls, data: bytes) -> "AssistantGetAwardResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class AssistantCompleteNumberReq(BasePacket):
    """Assistant.complete_number 请求封包 (Mod 52, Act 2)"""

    def __init__(self) -> None:
        super().__init__(mod=52, act=2)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "AssistantCompleteNumberReq":
        return cls()

@dataclass
class AssistantCompleteNumberResp(BasePacket):
    """Assistant.complete_number 应答封包 (Mod 52, Act 2)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=52, act=2)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "AssistantCompleteNumberResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class AssistantOneKeyGetAwardReq(BasePacket):
    """Assistant.one_key_get_award 请求封包 (Mod 52, Act 3)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=52, act=3)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "AssistantOneKeyGetAwardReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class AssistantOneKeyGetAwardResp(BasePacket):
    """Assistant.one_key_get_award 应答封包 (Mod 52, Act 3)"""

    field_0: int
    field_1: Tuple[int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int]) -> None:
        super().__init__(mod=52, act=3)
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
    def decode(cls, data: bytes) -> "AssistantOneKeyGetAwardResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)
