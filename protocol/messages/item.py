"""神仙道背包与物品资产模块数据契约 (Mod 2: Mod_Item_Base)

定义背包格子查询、一键智能整理、杂物变卖与元宝解锁格位的强类型契约模型。
严格落实 [SAFE_READ], [ROUTINE_FREE], [HAZARDOUS_INGOT] 安全红线守卫。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter


class ItemConstants:
    """Mod_Item_Base 官方业务状态常量"""
    ACTION_SUCCESS = 20
    ACTION_FAILED = 143
    FAILED = 153
    SUCCESS = 0
    COINS = 3
    FAME = 4
    INGOT = 5
    GRID_ID_ERROR = 219
    GRID_MAX_LIMIT = 220
    NOT_ENOUGH_INGOT = 221


@dataclass
class ItemGetEmptyGridNumberReq(BasePacket):
    """查询主背包剩余可用空格数量 (Mod 2, Act 2) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=2, act=2)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetEmptyGridNumberReq":
        return cls()


@dataclass
class ItemGetEmptyGridNumberResp(BasePacket):
    """查询主背包剩余空格应答 (Mod 2, Act 2) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    empty_count: int

    def __init__(self, empty_count: int) -> None:
        super().__init__(mod=2, act=2)
        self.empty_count = empty_count

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.empty_count)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetEmptyGridNumberResp":
        reader = ByteArrayReader(data)
        cnt = reader.read_int16() if reader.remaining >= 2 else 0
        return cls(empty_count=cnt)


@dataclass
class ItemGetAllPlayerItemInfosReq(BasePacket):
    """获取玩家全部背包与穿戴物品快照 (Mod 2, Act 3) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=2, act=3)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetAllPlayerItemInfosReq":
        return cls()


@dataclass
class ItemClassifyPackReq(BasePacket):
    """一键主背包智能自动整理归纳 (Mod 2, Act 52) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=2, act=52)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "ItemClassifyPackReq":
        return cls()


@dataclass
class ItemClassifyPackResp(BasePacket):
    """一键主背包整理应答 (Mod 2, Act 52) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    result_code: int

    def __init__(self, result_code: int) -> None:
        super().__init__(mod=2, act=52)
        self.result_code = result_code

    @property
    def is_success(self) -> bool:
        return self.result_code == ItemConstants.ACTION_SUCCESS

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.result_code)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemClassifyPackResp":
        reader = ByteArrayReader(data)
        code = reader.read_uint8() if reader.remaining >= 1 else ItemConstants.ACTION_FAILED
        return cls(result_code=code)


@dataclass
class ItemClassifyWarehouseReq(BasePacket):
    """一键随身仓库智能自动整理归纳 (Mod 2, Act 53) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=2, act=53)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "ItemClassifyWarehouseReq":
        return cls()


@dataclass
class ItemSellItemReq(BasePacket):
    """变卖背包指定物品换取铜钱 (Mod 2, Act 58) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    player_item_id: int

    def __init__(self, player_item_id: int) -> None:
        super().__init__(mod=2, act=58)
        self.player_item_id = player_item_id

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.player_item_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemSellItemReq":
        reader = ByteArrayReader(data)
        item_id = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(player_item_id=item_id)


@dataclass
class ItemSellItemResp(BasePacket):
    """变卖物品应答 (Mod 2, Act 58) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    result_code: int
    return_coins: int = 0

    def __init__(self, result_code: int, return_coins: int = 0) -> None:
        super().__init__(mod=2, act=58)
        self.result_code = result_code
        self.return_coins = return_coins

    @property
    def is_success(self) -> bool:
        return self.result_code == ItemConstants.ACTION_SUCCESS

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.result_code)
        writer.write_int32(self.return_coins)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemSellItemResp":
        reader = ByteArrayReader(data)
        code = reader.read_uint8() if reader.remaining >= 1 else ItemConstants.ACTION_FAILED
        coins = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(result_code=code, return_coins=coins)


@dataclass
class ItemAddPackGridReq(BasePacket):
    """消耗元宝开启主背包格子 (Mod 2, Act 54) - [HAZARDOUS_INGOT]

    强制前置安全红线守卫拦截，防止未经授权意外扣除元宝。

    @author Ateng
    @since 2026-10-16
    """

    grid_count: int
    allow_ingot: bool = False

    def __init__(self, grid_count: int, allow_ingot: bool = False) -> None:
        super().__init__(mod=2, act=54)
        if not allow_ingot:
            raise PermissionError("[HAZARDOUS_INGOT] add_pack_grid 涉及元宝扣除，已触发安全熔断保护！若确认执行请显式设置 allow_ingot=True")
        self.grid_count = grid_count
        self.allow_ingot = allow_ingot

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.grid_count)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemAddPackGridReq":
        reader = ByteArrayReader(data)
        cnt = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(grid_count=cnt, allow_ingot=True)
