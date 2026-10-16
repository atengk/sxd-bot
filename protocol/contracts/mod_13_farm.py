"""神仙道 Farm 模块协议代码契约 (Mod 13)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_Farm_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class FarmConstants:
    """Farm 模块业务状态与行为常量"""

    CAN_NOT_UP = 29
    COIN_HERBS = 3
    ERROR = 33
    EXP_HERBS = 2
    FAILED = 30
    INVITE = 6
    IS_DOUBLE = 14
    IS_MAIN_ROLE = 19
    IS_PLANT = 28
    IS_TOP_HERBS = 11
    ITEM_PACK_FULL = 34
    LIMIT_NUM = 25
    NOINVITE = 7
    NOT_ENOUGH_INGOT = 10
    NOT_ENOUGTH_COIN = 31
    NOT_ENOUGTH_INGOT = 32
    NOT_PLAYER_ROLE = 18
    NO_DOUBLE = 15
    NO_ENOUGHT_COIN_TREE_COUNT = 12
    NO_ENOUGHT_XIANLING_TREE_COUNT = 13
    NO_ENOUGTH_TIMES = 26
    NO_INGOT = 24
    NO_PLANT = 1
    NO_REMAIN = 23
    NO_VIP = 27
    PACK_FULL = 16
    PASS = 21
    PLANT = 0
    REACH_MAX_LAND_COUNT = 17
    REMAIN = 22
    ROLE_LEVEL = 20
    SUCCESS = 8
    TOP_HERBS = 9
    WAR = 5
    XIANLING_HERBS = 4

@dataclass
class FarmGetFarmlandinfoListReq(BasePacket):
    """Farm.get_farmlandinfo_list 请求封包 (Mod 13, Act 0)"""

    def __init__(self) -> None:
        super().__init__(mod=13, act=0)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FarmGetFarmlandinfoListReq":
        return cls()

@dataclass
class FarmGetFarmlandinfoListResp(BasePacket):
    """Farm.get_farmlandinfo_list 应答封包 (Mod 13, Act 0)"""

    field_0: Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int]
    field_1: int
    field_2: int

    def __init__(self, field_0: Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int], field_1: int, field_2: int) -> None:
        super().__init__(mod=13, act=0)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmGetFarmlandinfoListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class FarmGetPlayerRoleinfoListReq(BasePacket):
    """Farm.get_player_roleinfo_list 请求封包 (Mod 13, Act 1)"""

    def __init__(self) -> None:
        super().__init__(mod=13, act=1)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FarmGetPlayerRoleinfoListReq":
        return cls()

@dataclass
class FarmGetPlayerRoleinfoListResp(BasePacket):
    """Farm.get_player_roleinfo_list 应答封包 (Mod 13, Act 1)"""

    field_0: Tuple[int, str, str, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, str, str, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=13, act=1)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmGetPlayerRoleinfoListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class FarmGetHerbsSeedReq(BasePacket):
    """Farm.get_herbs_seed 请求封包 (Mod 13, Act 2)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=2)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmGetHerbsSeedReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FarmGetHerbsSeedResp(BasePacket):
    """Farm.get_herbs_seed 应答封包 (Mod 13, Act 2)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=13, act=2)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_uint8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmGetHerbsSeedResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_uint8()
        return cls(f_0, f_1, f_2)

@dataclass
class FarmRefreshHerbsSeedReq(BasePacket):
    """Farm.refresh_herbs_seed 请求封包 (Mod 13, Act 3)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=3)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmRefreshHerbsSeedReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FarmRefreshHerbsSeedResp(BasePacket):
    """Farm.refresh_herbs_seed 应答封包 (Mod 13, Act 3)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=13, act=3)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_uint8(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmRefreshHerbsSeedResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_uint8()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class FarmGetTopHerbsSeedReq(BasePacket):
    """Farm.get_top_herbs_seed 请求封包 (Mod 13, Act 4)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=4)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmGetTopHerbsSeedReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FarmGetTopHerbsSeedResp(BasePacket):
    """Farm.get_top_herbs_seed 应答封包 (Mod 13, Act 4)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=13, act=4)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_uint8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmGetTopHerbsSeedResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_uint8()
        return cls(f_0, f_1, f_2)

@dataclass
class FarmPlantHerbsReq(BasePacket):
    """Farm.plant_herbs 请求封包 (Mod 13, Act 5)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=13, act=5)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_uint8(self.field_2)
        writer.write_int8(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmPlantHerbsReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_uint8()
        f_3 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class FarmPlantHerbsResp(BasePacket):
    """Farm.plant_herbs 应答封包 (Mod 13, Act 5)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: str
    field_4: str
    field_5: int
    field_6: int
    field_7: int
    field_8: int
    field_9: int
    field_10: int
    field_11: int
    field_12: int
    field_13: int
    field_14: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: str, field_4: str, field_5: int, field_6: int, field_7: int, field_8: int, field_9: int, field_10: int, field_11: int, field_12: int, field_13: int, field_14: int) -> None:
        super().__init__(mod=13, act=5)
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

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_utf(self.field_3)
        writer.write_utf(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int64(self.field_6)
        writer.write_int64(self.field_7)
        writer.write_int32(self.field_8)
        writer.write_int32(self.field_9)
        writer.write_int32(self.field_10)
        writer.write_int32(self.field_11)
        writer.write_uint8(self.field_12)
        writer.write_uint8(self.field_13)
        writer.write_int8(self.field_14)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmPlantHerbsResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_utf()
        f_4 = reader.read_utf()
        f_5 = reader.read_int32()
        f_6 = reader.read_int64()
        f_7 = reader.read_int64()
        f_8 = reader.read_int32()
        f_9 = reader.read_int32()
        f_10 = reader.read_int32()
        f_11 = reader.read_int32()
        f_12 = reader.read_uint8()
        f_13 = reader.read_uint8()
        f_14 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11, f_12, f_13, f_14)

@dataclass
class FarmHarvestReq(BasePacket):
    """Farm.harvest 请求封包 (Mod 13, Act 6)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=13, act=6)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_uint8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmHarvestReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_uint8()
        return cls(f_0, f_1)

@dataclass
class FarmHarvestResp(BasePacket):
    """Farm.harvest 应答封包 (Mod 13, Act 6)"""

    field_0: int
    field_1: str
    field_2: str
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int
    field_8: int

    def __init__(self, field_0: int, field_1: str, field_2: str, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int) -> None:
        super().__init__(mod=13, act=6)
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
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_int64(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int32(self.field_7)
        writer.write_uint8(self.field_8)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmHarvestResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_int64()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        f_6 = reader.read_int32()
        f_7 = reader.read_int32()
        f_8 = reader.read_uint8()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8)

@dataclass
class FarmReclamationReq(BasePacket):
    """Farm.reclamation 请求封包 (Mod 13, Act 7)"""

    def __init__(self) -> None:
        super().__init__(mod=13, act=7)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FarmReclamationReq":
        return cls()

@dataclass
class FarmReclamationResp(BasePacket):
    """Farm.reclamation 应答封包 (Mod 13, Act 7)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=13, act=7)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmReclamationResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class FarmCheckRoleStateReq(BasePacket):
    """Farm.check_role_state 请求封包 (Mod 13, Act 8)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=13, act=8)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_uint8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmCheckRoleStateReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_uint8()
        return cls(f_0, f_1)

@dataclass
class FarmCheckRoleStateResp(BasePacket):
    """Farm.check_role_state 应答封包 (Mod 13, Act 8)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=8)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmCheckRoleStateResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FarmHarvestCheckRemainExpReq(BasePacket):
    """Farm.harvest_check_remain_exp 请求封包 (Mod 13, Act 9)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=9)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmHarvestCheckRemainExpReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FarmHarvestCheckRemainExpResp(BasePacket):
    """Farm.harvest_check_remain_exp 应答封包 (Mod 13, Act 9)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=13, act=9)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_uint8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmHarvestCheckRemainExpResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_uint8()
        return cls(f_0, f_1)

@dataclass
class FarmGetSimpleFarmlandinfoReq(BasePacket):
    """Farm.get_simple_farmlandinfo 请求封包 (Mod 13, Act 10)"""

    def __init__(self) -> None:
        super().__init__(mod=13, act=10)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FarmGetSimpleFarmlandinfoReq":
        return cls()

@dataclass
class FarmGetSimpleFarmlandinfoResp(BasePacket):
    """Farm.get_simple_farmlandinfo 应答封包 (Mod 13, Act 10)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=13, act=10)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmGetSimpleFarmlandinfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class FarmClearFarmlandCdReq(BasePacket):
    """Farm.clear_farmland_cd 请求封包 (Mod 13, Act 11)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=11)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmClearFarmlandCdReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FarmClearFarmlandCdResp(BasePacket):
    """Farm.clear_farmland_cd 应答封包 (Mod 13, Act 11)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=11)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmClearFarmlandCdResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FarmBuyCoinTreeCountInfoReq(BasePacket):
    """Farm.buy_coin_tree_count_info 请求封包 (Mod 13, Act 12)"""

    def __init__(self) -> None:
        super().__init__(mod=13, act=12)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FarmBuyCoinTreeCountInfoReq":
        return cls()

@dataclass
class FarmBuyCoinTreeCountInfoResp(BasePacket):
    """Farm.buy_coin_tree_count_info 应答封包 (Mod 13, Act 12)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=13, act=12)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmBuyCoinTreeCountInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class FarmBuyCoinTreeCountReq(BasePacket):
    """Farm.buy_coin_tree_count 请求封包 (Mod 13, Act 13)"""

    def __init__(self) -> None:
        super().__init__(mod=13, act=13)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FarmBuyCoinTreeCountReq":
        return cls()

@dataclass
class FarmBuyCoinTreeCountResp(BasePacket):
    """Farm.buy_coin_tree_count 应答封包 (Mod 13, Act 13)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=13, act=13)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmBuyCoinTreeCountResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class FarmCoinTreeCountNotifyReq(BasePacket):
    """Farm.coin_tree_count_notify 请求封包 (Mod 13, Act 14)"""

    def __init__(self) -> None:
        super().__init__(mod=13, act=14)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FarmCoinTreeCountNotifyReq":
        return cls()

@dataclass
class FarmCoinTreeCountNotifyResp(BasePacket):
    """Farm.coin_tree_count_notify 应答封包 (Mod 13, Act 14)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=14)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmCoinTreeCountNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FarmIngotForFarmlandReq(BasePacket):
    """Farm.ingot_for_farmland 请求封包 (Mod 13, Act 15)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=15)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmIngotForFarmlandReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FarmIngotForFarmlandResp(BasePacket):
    """Farm.ingot_for_farmland 应答封包 (Mod 13, Act 15)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=15)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmIngotForFarmlandResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FarmUpFarmlandLevelReq(BasePacket):
    """Farm.up_farmland_level 请求封包 (Mod 13, Act 16)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=16)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmUpFarmlandLevelReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FarmUpFarmlandLevelResp(BasePacket):
    """Farm.up_farmland_level 应答封包 (Mod 13, Act 16)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=16)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmUpFarmlandLevelResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FarmXianlingTreeCountNotifyReq(BasePacket):
    """Farm.xianling_tree_count_notify 请求封包 (Mod 13, Act 17)"""

    def __init__(self) -> None:
        super().__init__(mod=13, act=17)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FarmXianlingTreeCountNotifyReq":
        return cls()

@dataclass
class FarmXianlingTreeCountNotifyResp(BasePacket):
    """Farm.xianling_tree_count_notify 应答封包 (Mod 13, Act 17)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=17)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmXianlingTreeCountNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FarmXianlingTreeCountInfoReq(BasePacket):
    """Farm.xianling_tree_count_info 请求封包 (Mod 13, Act 18)"""

    def __init__(self) -> None:
        super().__init__(mod=13, act=18)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FarmXianlingTreeCountInfoReq":
        return cls()

@dataclass
class FarmXianlingTreeCountInfoResp(BasePacket):
    """Farm.xianling_tree_count_info 应答封包 (Mod 13, Act 18)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=13, act=18)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmXianlingTreeCountInfoResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class FarmIsPlayerGetXianLingGiftReq(BasePacket):
    """Farm.is_player_get_xian_ling_gift 请求封包 (Mod 13, Act 19)"""

    def __init__(self) -> None:
        super().__init__(mod=13, act=19)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FarmIsPlayerGetXianLingGiftReq":
        return cls()

@dataclass
class FarmIsPlayerGetXianLingGiftResp(BasePacket):
    """Farm.is_player_get_xian_ling_gift 应答封包 (Mod 13, Act 19)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=19)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmIsPlayerGetXianLingGiftResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class FarmPlayerGetXianLingGiftReq(BasePacket):
    """Farm.player_get_xian_ling_gift 请求封包 (Mod 13, Act 20)"""

    def __init__(self) -> None:
        super().__init__(mod=13, act=20)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FarmPlayerGetXianLingGiftReq":
        return cls()

@dataclass
class FarmPlayerGetXianLingGiftResp(BasePacket):
    """Farm.player_get_xian_ling_gift 应答封包 (Mod 13, Act 20)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=13, act=20)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmPlayerGetXianLingGiftResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class FarmGetNewFarmlandinfoListReq(BasePacket):
    """Farm.get_new_farmlandinfo_list 请求封包 (Mod 13, Act 21)"""

    def __init__(self) -> None:
        super().__init__(mod=13, act=21)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FarmGetNewFarmlandinfoListReq":
        return cls()

@dataclass
class FarmGetNewFarmlandinfoListResp(BasePacket):
    """Farm.get_new_farmlandinfo_list 应答封包 (Mod 13, Act 21)"""

    field_0: Tuple[int, int, int, int, int, Tuple[int, int, int]]
    field_1: int

    def __init__(self, field_0: Tuple[int, int, int, int, int, Tuple[int, int, int]], field_1: int) -> None:
        super().__init__(mod=13, act=21)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmGetNewFarmlandinfoListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class FarmNewFarmlandHerbsListReq(BasePacket):
    """Farm.new_farmland_herbs_list 请求封包 (Mod 13, Act 22)"""

    def __init__(self) -> None:
        super().__init__(mod=13, act=22)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "FarmNewFarmlandHerbsListReq":
        return cls()

@dataclass
class FarmNewFarmlandHerbsListResp(BasePacket):
    """Farm.new_farmland_herbs_list 应答封包 (Mod 13, Act 22)"""

    field_0: Tuple[int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int]) -> None:
        super().__init__(mod=13, act=22)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmNewFarmlandHerbsListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class FarmBuyNewHerbsReq(BasePacket):
    """Farm.buy_new_herbs 请求封包 (Mod 13, Act 23)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=23)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmBuyNewHerbsReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FarmBuyNewHerbsResp(BasePacket):
    """Farm.buy_new_herbs 应答封包 (Mod 13, Act 23)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=23)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmBuyNewHerbsResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class FarmPlantNewHerbsReq(BasePacket):
    """Farm.plant_new_herbs 请求封包 (Mod 13, Act 24)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=13, act=24)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmPlantNewHerbsReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class FarmPlantNewHerbsResp(BasePacket):
    """Farm.plant_new_herbs 应答封包 (Mod 13, Act 24)"""

    field_0: int
    field_1: int
    field_2: int
    field_3: int
    field_4: Tuple[int, int, int]

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: Tuple[int, int, int]) -> None:
        super().__init__(mod=13, act=24)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        # 写入动态列表 field_4 (元素数 + 记录项)
        writer.write_uint16(len(self.field_4))
        for item_4 in self.field_4:
            writer.write_json(item_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmPlantNewHerbsResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        # 读取动态列表 f_4
        cnt_4 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_4 = []
        for _ in range(cnt_4):
            f_4.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class FarmHarvestNewReq(BasePacket):
    """Farm.harvest_new 请求封包 (Mod 13, Act 25)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=25)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmHarvestNewReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FarmHarvestNewResp(BasePacket):
    """Farm.harvest_new 应答封包 (Mod 13, Act 25)"""

    field_0: int
    field_1: Tuple[int, int, int]
    field_2: int

    def __init__(self, field_0: int, field_1: Tuple[int, int, int], field_2: int) -> None:
        super().__init__(mod=13, act=25)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmHarvestNewResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class FarmNewClearFarmlandCdReq(BasePacket):
    """Farm.new_clear_farmland_cd 请求封包 (Mod 13, Act 26)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=26)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmNewClearFarmlandCdReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class FarmNewClearFarmlandCdResp(BasePacket):
    """Farm.new_clear_farmland_cd 应答封包 (Mod 13, Act 26)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=13, act=26)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmNewClearFarmlandCdResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)
