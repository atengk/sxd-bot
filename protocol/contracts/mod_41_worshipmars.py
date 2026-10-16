"""神仙道 WorshipMars 模块协议代码契约 (Mod 41)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_WorshipMars_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class WorshipmarsConstants:
    """WorshipMars 模块业务状态与行为常量"""

    BLESSING_TIMES = 6
    COUNT_USED = 2
    EXP_ADD = 7
    INSUFFICIENT_INGOT = 3
    INSUFFICIENT_SKILL = 5
    NO_ENOUGTH_VIP = 4
    OFFERINGS_NO_EXIST = 1
    SUCCESS = 0

@dataclass
class WorshipmarsMarsInfoReq(BasePacket):
    """WorshipMars.mars_info 请求封包 (Mod 41, Act 0)"""

    def __init__(self) -> None:
        super().__init__(mod=41, act=0)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorshipmarsMarsInfoReq":
        return cls()

@dataclass
class WorshipmarsMarsInfoResp(BasePacket):
    """WorshipMars.mars_info 应答封包 (Mod 41, Act 0)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: Tuple[int, str, int, int, int]

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: Tuple[int, str, int, int, int]) -> None:
        super().__init__(mod=41, act=0)
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
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int8(self.field_5)
        # 写入动态列表 field_6 (元素数 + 记录项)
        writer.write_uint16(len(self.field_6))
        for item_6 in self.field_6:
            writer.write_json(item_6)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorshipmarsMarsInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        f_5 = reader.read_int8()
        # 读取动态列表 f_6
        cnt_6 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_6 = []
        for _ in range(cnt_6):
            f_6.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6)

@dataclass
class WorshipmarsIncenseReq(BasePacket):
    """WorshipMars.incense 请求封包 (Mod 41, Act 1)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=41, act=1)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorshipmarsIncenseReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class WorshipmarsIncenseResp(BasePacket):
    """WorshipMars.incense 应答封包 (Mod 41, Act 1)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=41, act=1)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorshipmarsIncenseResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class WorshipmarsGetBlessingTimesAndExpAddReq(BasePacket):
    """WorshipMars.get_blessing_times_and_exp_add 请求封包 (Mod 41, Act 2)"""

    def __init__(self) -> None:
        super().__init__(mod=41, act=2)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorshipmarsGetBlessingTimesAndExpAddReq":
        return cls()

@dataclass
class WorshipmarsGetBlessingTimesAndExpAddResp(BasePacket):
    """WorshipMars.get_blessing_times_and_exp_add 应答封包 (Mod 41, Act 2)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=41, act=2)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorshipmarsGetBlessingTimesAndExpAddResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class WorshipmarsBlessingTimesAndExpAddNotifyReq(BasePacket):
    """WorshipMars.blessing_times_and_exp_add_notify 请求封包 (Mod 41, Act 3)"""

    def __init__(self) -> None:
        super().__init__(mod=41, act=3)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorshipmarsBlessingTimesAndExpAddNotifyReq":
        return cls()

@dataclass
class WorshipmarsBlessingTimesAndExpAddNotifyResp(BasePacket):
    """WorshipMars.blessing_times_and_exp_add_notify 应答封包 (Mod 41, Act 3)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=41, act=3)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorshipmarsBlessingTimesAndExpAddNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class WorshipmarsGetRemainIncenseTimesReq(BasePacket):
    """WorshipMars.get_remain_incense_times 请求封包 (Mod 41, Act 4)"""

    def __init__(self) -> None:
        super().__init__(mod=41, act=4)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorshipmarsGetRemainIncenseTimesReq":
        return cls()

@dataclass
class WorshipmarsGetRemainIncenseTimesResp(BasePacket):
    """WorshipMars.get_remain_incense_times 应答封包 (Mod 41, Act 4)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=41, act=4)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorshipmarsGetRemainIncenseTimesResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class WorshipmarsQingmingActiveTimeListReq(BasePacket):
    """WorshipMars.qingming_active_time_list 请求封包 (Mod 41, Act 5)"""

    def __init__(self) -> None:
        super().__init__(mod=41, act=5)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorshipmarsQingmingActiveTimeListReq":
        return cls()

@dataclass
class WorshipmarsQingmingActiveTimeListResp(BasePacket):
    """WorshipMars.qingming_active_time_list 应答封包 (Mod 41, Act 5)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=41, act=5)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorshipmarsQingmingActiveTimeListResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)
