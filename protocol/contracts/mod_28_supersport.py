"""神仙道 SuperSport 模块协议代码契约 (Mod 28)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_SuperSport_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class SupersportConstants:
    """SuperSport 模块业务状态与行为常量"""

    AWARD_TOP = 13
    END_AWARD = 8
    FULL_BUY_TIMES = 6
    HAVE_CD_TIME = 3
    INVALID_RANKING = 1
    KILL_WIN_TOP = 10
    NOT_ENOUGH_CHALLENGE_TIMES = 2
    NOT_ENOUGH_INGOT = 5
    NOT_IN_CHALLENGE_TIME = 4
    RANKING_TOP = 11
    START_AWARD = 7
    SUCCESS = 0
    UPDATE_RANKING_TOP = 12
    WIN_TOP = 9

@dataclass
class SupersportOpenSuperSportReq(BasePacket):
    """SuperSport.open_super_sport 请求封包 (Mod 28, Act 0)"""

    def __init__(self) -> None:
        super().__init__(mod=28, act=0)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "SupersportOpenSuperSportReq":
        return cls()

@dataclass
class SupersportOpenSuperSportResp(BasePacket):
    """SuperSport.open_super_sport 应答封包 (Mod 28, Act 0)"""

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
    field_11: int
    field_12: Tuple[int, int, int, int, str, int, int]
    field_13: Tuple[int, int, int, str, int, str, int, int, int, str, int]

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int, field_9: int, field_10: int, field_11: int, field_12: Tuple[int, int, int, int, str, int, int], field_13: Tuple[int, int, int, str, int, str, int, int, int, str, int]) -> None:
        super().__init__(mod=28, act=0)
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

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int16(self.field_3)
        writer.write_int16(self.field_4)
        writer.write_int16(self.field_5)
        writer.write_int16(self.field_6)
        writer.write_int32(self.field_7)
        writer.write_int32(self.field_8)
        writer.write_int32(self.field_9)
        writer.write_int32(self.field_10)
        writer.write_int32(self.field_11)
        # 写入动态列表 field_12 (元素数 + 记录项)
        writer.write_uint16(len(self.field_12))
        for item_12 in self.field_12:
            writer.write_json(item_12)
        # 写入动态列表 field_13 (元素数 + 记录项)
        writer.write_uint16(len(self.field_13))
        for item_13 in self.field_13:
            writer.write_json(item_13)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SupersportOpenSuperSportResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int16()
        f_2 = reader.read_int32()
        f_3 = reader.read_int16()
        f_4 = reader.read_int16()
        f_5 = reader.read_int16()
        f_6 = reader.read_int16()
        f_7 = reader.read_int32()
        f_8 = reader.read_int32()
        f_9 = reader.read_int32()
        f_10 = reader.read_int32()
        f_11 = reader.read_int32()
        # 读取动态列表 f_12
        cnt_12 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_12 = []
        for _ in range(cnt_12):
            f_12.append(reader.read_json())
        # 读取动态列表 f_13
        cnt_13 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_13 = []
        for _ in range(cnt_13):
            f_13.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11, f_12, f_13)

@dataclass
class SupersportGetChallengeListReq(BasePacket):
    """SuperSport.get_challenge_list 请求封包 (Mod 28, Act 1)"""

    def __init__(self) -> None:
        super().__init__(mod=28, act=1)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "SupersportGetChallengeListReq":
        return cls()

@dataclass
class SupersportGetChallengeListResp(BasePacket):
    """SuperSport.get_challenge_list 应答封包 (Mod 28, Act 1)"""

    field_0: Tuple[int, int, int, int, str, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, str, int, int]) -> None:
        super().__init__(mod=28, act=1)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SupersportGetChallengeListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class SupersportStartChallengeReq(BasePacket):
    """SuperSport.start_challenge 请求封包 (Mod 28, Act 2)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=28, act=2)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SupersportStartChallengeReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class SupersportStartChallengeResp(BasePacket):
    """SuperSport.start_challenge 应答封包 (Mod 28, Act 2)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: Tuple[int, int, int, int, int, Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int], Tuple[int, int]]

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: Tuple[int, int, int, int, int, Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int], Tuple[int, int]]) -> None:
        super().__init__(mod=28, act=2)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int32(self.field_2)
        # 写入动态列表 field_3 (元素数 + 记录项)
        writer.write_uint16(len(self.field_3))
        for item_3 in self.field_3:
            writer.write_json(item_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SupersportStartChallengeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int16()
        f_2 = reader.read_int32()
        # 读取动态列表 f_3
        cnt_3 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_3 = []
        for _ in range(cnt_3):
            f_3.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class SupersportClearCdTimeReq(BasePacket):
    """SuperSport.clear_cd_time 请求封包 (Mod 28, Act 3)"""

    def __init__(self) -> None:
        super().__init__(mod=28, act=3)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "SupersportClearCdTimeReq":
        return cls()

@dataclass
class SupersportClearCdTimeResp(BasePacket):
    """SuperSport.clear_cd_time 应答封包 (Mod 28, Act 3)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=28, act=3)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SupersportClearCdTimeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class SupersportBuyChallengeTimesReq(BasePacket):
    """SuperSport.buy_challenge_times 请求封包 (Mod 28, Act 4)"""

    def __init__(self) -> None:
        super().__init__(mod=28, act=4)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "SupersportBuyChallengeTimesReq":
        return cls()

@dataclass
class SupersportBuyChallengeTimesResp(BasePacket):
    """SuperSport.buy_challenge_times 应答封包 (Mod 28, Act 4)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=28, act=4)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int16(self.field_2)
        writer.write_int16(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SupersportBuyChallengeTimesResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int16()
        f_2 = reader.read_int16()
        f_3 = reader.read_int16()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class SupersportNotifyNewSportWarReportReq(BasePacket):
    """SuperSport.notify_new_sport_war_report 请求封包 (Mod 28, Act 5)"""

    def __init__(self) -> None:
        super().__init__(mod=28, act=5)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "SupersportNotifyNewSportWarReportReq":
        return cls()

@dataclass
class SupersportNotifyNewSportWarReportResp(BasePacket):
    """SuperSport.notify_new_sport_war_report 应答封包 (Mod 28, Act 5)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int
    field_8: int
    field_9: str
    field_10: int
    field_11: str
    field_12: int
    field_13: int
    field_14: int
    field_15: str
    field_16: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int, field_9: str, field_10: int, field_11: str, field_12: int, field_13: int, field_14: int, field_15: str, field_16: int) -> None:
        super().__init__(mod=28, act=5)
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
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int16(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int8(self.field_7)
        writer.write_int32(self.field_8)
        writer.write_utf(self.field_9)
        writer.write_int32(self.field_10)
        writer.write_utf(self.field_11)
        writer.write_int32(self.field_12)
        writer.write_int32(self.field_13)
        writer.write_int32(self.field_14)
        writer.write_utf(self.field_15)
        writer.write_int32(self.field_16)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SupersportNotifyNewSportWarReportResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        f_5 = reader.read_int16()
        f_6 = reader.read_int32()
        f_7 = reader.read_int8()
        f_8 = reader.read_int32()
        f_9 = reader.read_utf()
        f_10 = reader.read_int32()
        f_11 = reader.read_utf()
        f_12 = reader.read_int32()
        f_13 = reader.read_int32()
        f_14 = reader.read_int32()
        f_15 = reader.read_utf()
        f_16 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11, f_12, f_13, f_14, f_15, f_16)

@dataclass
class SupersportNotifyReq(BasePacket):
    """SuperSport.notify 请求封包 (Mod 28, Act 6)"""

    def __init__(self) -> None:
        super().__init__(mod=28, act=6)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "SupersportNotifyReq":
        return cls()

@dataclass
class SupersportNotifyResp(BasePacket):
    """SuperSport.notify 应答封包 (Mod 28, Act 6)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=28, act=6)
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
    def decode(cls, data: bytes) -> "SupersportNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class SupersportCloseSuperSportReq(BasePacket):
    """SuperSport.close_super_sport 请求封包 (Mod 28, Act 7)"""

    def __init__(self) -> None:
        super().__init__(mod=28, act=7)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "SupersportCloseSuperSportReq":
        return cls()

@dataclass
class SupersportCloseSuperSportResp(BasePacket):
    """SuperSport.close_super_sport 应答封包 (Mod 28, Act 7)"""

    def __init__(self) -> None:
        super().__init__(mod=28, act=7)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "SupersportCloseSuperSportResp":
        return cls()

@dataclass
class SupersportGetPlayerWarReportReq(BasePacket):
    """SuperSport.get_player_war_report 请求封包 (Mod 28, Act 8)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=28, act=8)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SupersportGetPlayerWarReportReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class SupersportGetPlayerWarReportResp(BasePacket):
    """SuperSport.get_player_war_report 应答封包 (Mod 28, Act 8)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: int
    field_5: Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int]
    field_6: Tuple[int, int]

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int], field_6: Tuple[int, int]) -> None:
        super().__init__(mod=28, act=8)
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
        # 写入动态列表 field_5 (元素数 + 记录项)
        writer.write_uint16(len(self.field_5))
        for item_5 in self.field_5:
            writer.write_json(item_5)
        # 写入动态列表 field_6 (元素数 + 记录项)
        writer.write_uint16(len(self.field_6))
        for item_6 in self.field_6:
            writer.write_json(item_6)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SupersportGetPlayerWarReportResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
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
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6)

@dataclass
class SupersportGetRankingTopReq(BasePacket):
    """SuperSport.get_ranking_top 请求封包 (Mod 28, Act 9)"""

    def __init__(self) -> None:
        super().__init__(mod=28, act=9)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "SupersportGetRankingTopReq":
        return cls()

@dataclass
class SupersportGetRankingTopResp(BasePacket):
    """SuperSport.get_ranking_top 应答封包 (Mod 28, Act 9)"""

    field_0: Tuple[int, int, int, str, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, str, int, int, int, int]) -> None:
        super().__init__(mod=28, act=9)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SupersportGetRankingTopResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class SupersportNotifyUpdateWinTopReq(BasePacket):
    """SuperSport.notify_update_win_top 请求封包 (Mod 28, Act 10)"""

    def __init__(self) -> None:
        super().__init__(mod=28, act=10)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "SupersportNotifyUpdateWinTopReq":
        return cls()

@dataclass
class SupersportNotifyUpdateWinTopResp(BasePacket):
    """SuperSport.notify_update_win_top 应答封包 (Mod 28, Act 10)"""

    field_0: int
    field_1: str
    field_2: int

    def __init__(self, field_0: int, field_1: str, field_2: int) -> None:
        super().__init__(mod=28, act=10)
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
    def decode(cls, data: bytes) -> "SupersportNotifyUpdateWinTopResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class SupersportNotifyGlobalReq(BasePacket):
    """SuperSport.notify_global 请求封包 (Mod 28, Act 11)"""

    def __init__(self) -> None:
        super().__init__(mod=28, act=11)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "SupersportNotifyGlobalReq":
        return cls()

@dataclass
class SupersportNotifyGlobalResp(BasePacket):
    """SuperSport.notify_global 应答封包 (Mod 28, Act 11)"""

    field_0: int
    field_1: Tuple[int, str, int]
    field_2: Tuple[int, str, int, str, int]
    field_3: Tuple[int, str, int, str]
    field_4: Tuple[int, str, int]
    field_5: Tuple[int, int, str, int, int]

    def __init__(self, field_0: int, field_1: Tuple[int, str, int], field_2: Tuple[int, str, int, str, int], field_3: Tuple[int, str, int, str], field_4: Tuple[int, str, int], field_5: Tuple[int, int, str, int, int]) -> None:
        super().__init__(mod=28, act=11)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5

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
            writer.write_json(item_5)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SupersportNotifyGlobalResp":
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
            f_5.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3, f_4, f_5)

@dataclass
class SupersportGetCdTimeReq(BasePacket):
    """SuperSport.get_cd_time 请求封包 (Mod 28, Act 12)"""

    def __init__(self) -> None:
        super().__init__(mod=28, act=12)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "SupersportGetCdTimeReq":
        return cls()

@dataclass
class SupersportGetCdTimeResp(BasePacket):
    """SuperSport.get_cd_time 应答封包 (Mod 28, Act 12)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=28, act=12)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SupersportGetCdTimeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class SupersportGetChallengeTimesReq(BasePacket):
    """SuperSport.get_challenge_times 请求封包 (Mod 28, Act 13)"""

    def __init__(self) -> None:
        super().__init__(mod=28, act=13)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "SupersportGetChallengeTimesReq":
        return cls()

@dataclass
class SupersportGetChallengeTimesResp(BasePacket):
    """SuperSport.get_challenge_times 应答封包 (Mod 28, Act 13)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=28, act=13)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "SupersportGetChallengeTimesResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)
