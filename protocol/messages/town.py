"""神仙道城镇与场景寻路模块数据契约 (Mod 1: Mod_Town_Base)

定义进入城镇、离开城镇、场景寻路移动与同屏在线玩家拉取的强类型契约模型。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter


class TownConstants:
    """Mod_Town_Base 官方业务状态常量"""
    SUCCESS = 0
    FAILED = 1
    FULL = 2
    NOT_ENOUGH_INGOT = 3
    ON_PRACTICE = 4
    OFF_PRACTICE = 5
    FINISHED_PRACTICE = 6
    TOWN_HIDDEN = 7
    TOWN_NOHIDDEN = 8
    NOT_IMMORTAL = 9
    BECOME_IMMORTAL = 10
    TRUE = 11
    FALSE = 12
    TOWN_SUCCESS = 13
    TOWN_FAILURE = 14


@dataclass
class TownEnterTownReq(BasePacket):
    """进入指定城镇场景请求 (Mod 1, Act 0) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    town_id: int

    def __init__(self, town_id: int) -> None:
        super().__init__(mod=1, act=0)
        self.town_id = town_id

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.town_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownEnterTownReq":
        reader = ByteArrayReader(data)
        town_id = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(town_id=town_id)


@dataclass
class TownEnterTownResp(BasePacket):
    """进入城镇场景应答 (Mod 1, Act 0) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    result_code: int
    town_id: int = 0
    raw_payload: bytes = b""

    def __init__(self, result_code: int, town_id: int = 0, raw_payload: bytes = b"") -> None:
        super().__init__(mod=1, act=0)
        self.result_code = result_code
        self.town_id = town_id
        self.raw_payload = raw_payload

    @property
    def is_success(self) -> bool:
        return self.result_code == TownConstants.SUCCESS

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.result_code)
        writer.write_int32(self.town_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownEnterTownResp":
        reader = ByteArrayReader(data)
        result_code = reader.read_uint8() if reader.remaining >= 1 else 1
        town_id = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(result_code=result_code, town_id=town_id, raw_payload=data)


@dataclass
class TownLeaveTownReq(BasePacket):
    """离开当前城镇场景请求 (Mod 1, Act 1) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=1, act=1)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "TownLeaveTownReq":
        return cls()


@dataclass
class TownMoveToReq(BasePacket):
    """在城镇场景中寻路移动请求 (Mod 1, Act 2) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    src_x: int
    src_y: int
    dst_x: int
    dst_y: int

    def __init__(self, src_x: int, src_y: int, dst_x: int, dst_y: int) -> None:
        super().__init__(mod=1, act=2)
        self.src_x = src_x
        self.src_y = src_y
        self.dst_x = dst_x
        self.dst_y = dst_y

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.src_x)
        writer.write_int16(self.src_y)
        writer.write_int16(self.dst_x)
        writer.write_int16(self.dst_y)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownMoveToReq":
        reader = ByteArrayReader(data)
        sx = reader.read_int16() if reader.remaining >= 2 else 0
        sy = reader.read_int16() if reader.remaining >= 2 else 0
        dx = reader.read_int16() if reader.remaining >= 2 else 0
        dy = reader.read_int16() if reader.remaining >= 2 else 0
        return cls(src_x=sx, src_y=sy, dst_x=dx, dst_y=dy)


@dataclass
class TownMoveToResp(BasePacket):
    """场景寻路移动广播应答 (Mod 1, Act 2) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    player_id: int
    src_x: int
    src_y: int
    dst_x: int
    dst_y: int

    def __init__(self, player_id: int, src_x: int, src_y: int, dst_x: int, dst_y: int) -> None:
        super().__init__(mod=1, act=2)
        self.player_id = player_id
        self.src_x = src_x
        self.src_y = src_y
        self.dst_x = dst_x
        self.dst_y = dst_y

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.player_id)
        writer.write_int16(self.src_x)
        writer.write_int16(self.src_y)
        writer.write_int16(self.dst_x)
        writer.write_int16(self.dst_y)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TownMoveToResp":
        reader = ByteArrayReader(data)
        pid = reader.read_int32() if reader.remaining >= 4 else 0
        sx = reader.read_int16() if reader.remaining >= 2 else 0
        sy = reader.read_int16() if reader.remaining >= 2 else 0
        dx = reader.read_int16() if reader.remaining >= 2 else 0
        dy = reader.read_int16() if reader.remaining >= 2 else 0
        return cls(player_id=pid, src_x=sx, src_y=sy, dst_x=dx, dst_y=dy)


@dataclass
class TownGetPlayersReq(BasePacket):
    """拉取城镇同屏玩家列表请求 (Mod 1, Act 3) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=1, act=3)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "TownGetPlayersReq":
        return cls()
