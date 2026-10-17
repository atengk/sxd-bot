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
class ItemPlayerUseGridItemReq(BasePacket):
    """使用背包指定格位物品 (Mod 2, Act 53) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    grid_id: int

    def __init__(self, grid_id: int) -> None:
        super().__init__(mod=2, act=53)
        self.grid_id = grid_id

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.grid_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerUseGridItemReq":
        reader = ByteArrayReader(data)
        gid = reader.read_int16() if reader.remaining >= 2 else 0
        return cls(grid_id=gid)


@dataclass
class ItemPlayerUseGridItemResp(BasePacket):
    """使用背包物品应答 (Mod 2, Act 53) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    result_code: int

    def __init__(self, result_code: int) -> None:
        super().__init__(mod=2, act=53)
        self.result_code = result_code

    @property
    def is_success(self) -> bool:
        return self.result_code == ItemConstants.ACTION_SUCCESS or self.result_code == 0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.result_code)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemPlayerUseGridItemResp":
        reader = ByteArrayReader(data)
        code = reader.read_uint8() if reader.remaining >= 1 else ItemConstants.ACTION_FAILED
        return cls(result_code=code)


@dataclass
class ItemMovePackGridItemToWarehouseReq(BasePacket):
    """将背包格位物品移动存入随身仓库 (Mod 2, Act 49) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    pack_grid_id: int
    warehouse_grid_id: int = 0

    def __init__(self, pack_grid_id: int, warehouse_grid_id: int = 0) -> None:
        super().__init__(mod=2, act=49)
        self.pack_grid_id = pack_grid_id
        self.warehouse_grid_id = warehouse_grid_id

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.pack_grid_id)
        writer.write_int16(self.warehouse_grid_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemMovePackGridItemToWarehouseReq":
        reader = ByteArrayReader(data)
        pid = reader.read_int16() if reader.remaining >= 2 else 0
        wid = reader.read_int16() if reader.remaining >= 2 else 0
        return cls(pack_grid_id=pid, warehouse_grid_id=wid)


@dataclass
class ItemDropPackGridItemReq(BasePacket):
    """丢弃/销毁背包指定格位物品 (Mod 2, Act 46) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    grid_id: int

    def __init__(self, grid_id: int) -> None:
        super().__init__(mod=2, act=46)
        self.grid_id = grid_id

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.grid_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemDropPackGridItemReq":
        reader = ByteArrayReader(data)
        gid = reader.read_int16() if reader.remaining >= 2 else 0
        return cls(grid_id=gid)


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


@dataclass
class ItemGetPlayerPackItemListReq(BasePacket):
    """获取玩家主背包与随身仓库物品列表请求 (Mod 2, Act 41) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=2, act=41)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerPackItemListReq":
        return cls()


def _read_item_record(reader: ByteArrayReader) -> List[Any]:
    """读取 Mod 2 物品 21 字段强类型二进制记录项 (75 字节)"""
    record: List[Any] = []
    for _ in range(9):
        record.append(reader.read_int32())
    record.append(reader.read_int8())
    record.append(reader.read_int32())
    record.append(reader.read_int32())
    record.append(reader.read_int8())
    record.append(reader.read_int16())
    record.append(reader.read_int16())
    record.append(reader.read_int8())
    for _ in range(3):
        record.append(reader.read_int32())
    record.append(reader.read_int64())
    record.append(reader.read_int32())
    return record


def _write_item_record(writer: ByteArrayWriter, item: Any) -> None:
    """写入 Mod 2 物品 21 字段强类型二进制记录项 (75 字节)"""
    if isinstance(item, (list, tuple)):
        vals = list(item) + [0] * max(0, 21 - len(item))
        for i in range(9):
            writer.write_int32(int(vals[i]))
        writer.write_int8(int(vals[9]))
        writer.write_int32(int(vals[10]))
        writer.write_int32(int(vals[11]))
        writer.write_int8(int(vals[12]))
        writer.write_int16(int(vals[13]))
        writer.write_int16(int(vals[14]))
        writer.write_int8(int(vals[15]))
        for i in range(16, 19):
            writer.write_int32(int(vals[i]))
        writer.write_int64(int(vals[19]))
        writer.write_int32(int(vals[20]))
    else:
        writer.write_json(item)


@dataclass
class ItemGetPlayerPackItemListResp(BasePacket):
    """玩家主背包与随身仓库物品列表应答 (Mod 2, Act 41) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    pack_capacity: int = 0
    pack_empty_grids: int = 0
    pack_items: List[Any] = field(default_factory=list)
    warehouse_capacity: int = 0
    warehouse_items: List[Any] = field(default_factory=list)
    raw_payload: bytes = b""

    def __init__(
        self,
        pack_capacity: int = 0,
        pack_empty_grids: int = 0,
        pack_items: Optional[List[Any]] = None,
        warehouse_capacity: int = 0,
        warehouse_items: Optional[List[Any]] = None,
        raw_payload: bytes = b"",
    ) -> None:
        super().__init__(mod=2, act=41)
        self.pack_capacity = pack_capacity
        self.pack_empty_grids = pack_empty_grids
        self.pack_items = pack_items or []
        self.warehouse_capacity = warehouse_capacity
        self.warehouse_items = warehouse_items or []
        self.raw_payload = raw_payload

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.pack_capacity)
        writer.write_int32(self.pack_empty_grids)
        writer.write_uint16(len(self.pack_items))
        for item in self.pack_items:
            _write_item_record(writer, item)
        writer.write_int16(self.warehouse_capacity)
        writer.write_uint16(len(self.warehouse_items))
        for item in self.warehouse_items:
            _write_item_record(writer, item)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemGetPlayerPackItemListResp":
        reader = ByteArrayReader(data)
        pack_cap = 0
        empty_grids = 0
        pack_items: List[Any] = []
        wh_cap = 0
        wh_items: List[Any] = []

        try:
            if reader.remaining >= 2:
                pack_cap = reader.read_int16()
            if reader.remaining >= 4:
                empty_grids = reader.read_int32()
            if reader.remaining >= 2:
                cnt_pack = reader.read_uint16()
                for _ in range(cnt_pack):
                    if reader.remaining >= 75:
                        pack_items.append(_read_item_record(reader))
                    elif reader.remaining > 0:
                        try:
                            pack_items.append(reader.read_json())
                        except Exception:
                            break
                    else:
                        break
            if reader.remaining >= 2:
                wh_cap = reader.read_int16()
            if reader.remaining >= 2:
                cnt_wh = reader.read_uint16()
                for _ in range(cnt_wh):
                    if reader.remaining >= 75:
                        wh_items.append(_read_item_record(reader))
                    elif reader.remaining > 0:
                        try:
                            wh_items.append(reader.read_json())
                        except Exception:
                            break
                    else:
                        break
        except Exception:
            pass

        return cls(
            pack_capacity=pack_cap,
            pack_empty_grids=empty_grids,
            pack_items=pack_items,
            warehouse_capacity=wh_cap,
            warehouse_items=wh_items,
            raw_payload=data,
        )


@dataclass
class ItemChooseBoxReq(BasePacket):
    """自选礼盒选取选项并开启请求 (Mod 2, Act 160) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-17
    """

    grid_id: int
    choose_index: int = 1

    def __init__(self, grid_id: int, choose_index: int = 1) -> None:
        super().__init__(mod=2, act=160)
        self.grid_id = grid_id
        self.choose_index = choose_index

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.grid_id)
        writer.write_int32(self.choose_index)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "ItemChooseBoxReq":
        reader = ByteArrayReader(data)
        gid = reader.read_int16() if reader.remaining >= 2 else 0
        idx = reader.read_int32() if reader.remaining >= 4 else 1
        return cls(grid_id=gid, choose_index=idx)

