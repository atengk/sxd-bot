"""神仙道 TravelEvent 模块协议代码契约 (Mod 21)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_TravelEvent_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class TraveleventConstants:
    """TravelEvent 模块业务状态与行为常量"""

    CD_TIME = 0
    COIN = 3
    EXP = 4
    FAME = 5
    NO_GET = 10
    NO_INGOT = 8
    PACKAGE_FULL = 9
    POWER = 6
    REACH_MAX_COUNT = 1
    SKILL = 7
    SUCCESS = 2

@dataclass
class TraveleventGetActivityInfoReq(BasePacket):
    """TravelEvent.get_activity_info 请求封包 (Mod 21, Act 0)"""

    def __init__(self) -> None:
        super().__init__(mod=21, act=0)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TraveleventGetActivityInfoReq":
        return cls()

@dataclass
class TraveleventGetActivityInfoResp(BasePacket):
    """TravelEvent.get_activity_info 应答封包 (Mod 21, Act 0)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int) -> None:
        super().__init__(mod=21, act=0)
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
    def decode(cls, data: bytes) -> "TraveleventGetActivityInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5)

@dataclass
class TraveleventGetEventAndAnswerReq(BasePacket):
    """TravelEvent.get_event_and_answer 请求封包 (Mod 21, Act 1)"""

    def __init__(self) -> None:
        super().__init__(mod=21, act=1)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TraveleventGetEventAndAnswerReq":
        return cls()

@dataclass
class TraveleventGetEventAndAnswerResp(BasePacket):
    """TravelEvent.get_event_and_answer 应答封包 (Mod 21, Act 1)"""

    field_0: int
    field_1: str
    field_2: Tuple[int, str, str]
    field_3: int
    field_4: int
    field_5: int
    field_6: int

    def __init__(self, field_0: int, field_1: str, field_2: Tuple[int, str, str], field_3: int, field_4: int, field_5: int, field_6: int) -> None:
        super().__init__(mod=21, act=1)
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
        writer.write_utf(self.field_1)
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        writer.write_uint8(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int32(self.field_6)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TraveleventGetEventAndAnswerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_json())
        f_3 = reader.read_uint8()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        f_6 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6)

@dataclass
class TraveleventAnswerTravelEventReq(BasePacket):
    """TravelEvent.answer_travel_event 请求封包 (Mod 21, Act 2)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=21, act=2)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TraveleventAnswerTravelEventReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class TraveleventAnswerTravelEventResp(BasePacket):
    """TravelEvent.answer_travel_event 应答封包 (Mod 21, Act 2)"""

    field_0: str
    field_1: Tuple[int, int]
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int

    def __init__(self, field_0: str, field_1: Tuple[int, int], field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int) -> None:
        super().__init__(mod=21, act=2)
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
        writer.write_utf(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int32(self.field_7)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TraveleventAnswerTravelEventResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        f_6 = reader.read_int32()
        f_7 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7)

@dataclass
class TraveleventCancelCdReq(BasePacket):
    """TravelEvent.cancel_cd 请求封包 (Mod 21, Act 3)"""

    def __init__(self) -> None:
        super().__init__(mod=21, act=3)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TraveleventCancelCdReq":
        return cls()

@dataclass
class TraveleventCancelCdResp(BasePacket):
    """TravelEvent.cancel_cd 应答封包 (Mod 21, Act 3)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=21, act=3)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TraveleventCancelCdResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class TraveleventLotteryDrawReq(BasePacket):
    """TravelEvent.lottery_draw 请求封包 (Mod 21, Act 4)"""

    def __init__(self) -> None:
        super().__init__(mod=21, act=4)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "TraveleventLotteryDrawReq":
        return cls()

@dataclass
class TraveleventLotteryDrawResp(BasePacket):
    """TravelEvent.lottery_draw 应答封包 (Mod 21, Act 4)"""

    field_0: int
    field_1: Tuple[int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, int]) -> None:
        super().__init__(mod=21, act=4)
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
    def decode(cls, data: bytes) -> "TraveleventLotteryDrawResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)
