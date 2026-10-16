"""神仙道 WorldBoss 模块协议代码契约 (Mod 24)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_WorldBoss_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class WorldbossConstants:
    """WorldBoss 模块业务状态与行为常量"""

    ACTION_FAILED = 1
    ACTION_SUCCESS = 0
    COMBAT_LIMIT = 9
    DEATH_STATUS = 5
    MAX_TIMES = 7
    MISSION_OVER = 3
    NOT_BEGIN = 2
    NOT_ENOUGH_INGOT = 6
    NOT_ENOUGH_SKILL = 8
    WORLD_BOSS_DEAD = 4

@dataclass
class WorldbossGetWorldBossListReq(BasePacket):
    """WorldBoss.get_world_boss_list 请求封包 (Mod 24, Act 0)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=24, act=0)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossGetWorldBossListReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class WorldbossGetWorldBossListResp(BasePacket):
    """WorldBoss.get_world_boss_list 应答封包 (Mod 24, Act 0)"""

    field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int]

    def __init__(self, field_0: Tuple[int, int, int, int, int, int, int, int, int, int, int]) -> None:
        super().__init__(mod=24, act=0)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossGetWorldBossListResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class WorldbossGetWorldBossDataReq(BasePacket):
    """WorldBoss.get_world_boss_data 请求封包 (Mod 24, Act 1)"""

    def __init__(self) -> None:
        super().__init__(mod=24, act=1)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossGetWorldBossDataReq":
        return cls()

@dataclass
class WorldbossGetWorldBossDataResp(BasePacket):
    """WorldBoss.get_world_boss_data 应答封包 (Mod 24, Act 1)"""

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

    def __init__(self, field_0: int, field_1: int, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int, field_9: int, field_10: int, field_11: int) -> None:
        super().__init__(mod=24, act=1)
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

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int8(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int32(self.field_7)
        writer.write_int64(self.field_8)
        writer.write_int64(self.field_9)
        writer.write_int32(self.field_10)
        writer.write_int32(self.field_11)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossGetWorldBossDataResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int8()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        f_6 = reader.read_int32()
        f_7 = reader.read_int32()
        f_8 = reader.read_int64()
        f_9 = reader.read_int64()
        f_10 = reader.read_int32()
        f_11 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11)

@dataclass
class WorldbossFightWorldBossReq(BasePacket):
    """WorldBoss.fight_world_boss 请求封包 (Mod 24, Act 2)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=24, act=2)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossFightWorldBossReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class WorldbossFightWorldBossResp(BasePacket):
    """WorldBoss.fight_world_boss 应答封包 (Mod 24, Act 2)"""

    field_0: int
    field_1: int
    field_2: Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int]
    field_3: Tuple[int, int]
    field_4: int

    def __init__(self, field_0: int, field_1: int, field_2: Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int], field_3: Tuple[int, int], field_4: int) -> None:
        super().__init__(mod=24, act=2)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_uint8(self.field_1)
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        # 写入动态列表 field_3 (元素数 + 记录项)
        writer.write_uint16(len(self.field_3))
        for item_3 in self.field_3:
            writer.write_json(item_3)
        writer.write_int32(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossFightWorldBossResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_uint8()
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
        f_4 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class WorldbossClearDeathCdReq(BasePacket):
    """WorldBoss.clear_death_cd 请求封包 (Mod 24, Act 3)"""

    def __init__(self) -> None:
        super().__init__(mod=24, act=3)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossClearDeathCdReq":
        return cls()

@dataclass
class WorldbossClearDeathCdResp(BasePacket):
    """WorldBoss.clear_death_cd 应答封包 (Mod 24, Act 3)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=24, act=3)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossClearDeathCdResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class WorldbossGetDefeatRecordListReq(BasePacket):
    """WorldBoss.get_defeat_record_list 请求封包 (Mod 24, Act 4)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=24, act=4)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossGetDefeatRecordListReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class WorldbossGetDefeatRecordListResp(BasePacket):
    """WorldBoss.get_defeat_record_list 应答封包 (Mod 24, Act 4)"""

    field_0: int
    field_1: Tuple[int, str, int]

    def __init__(self, field_0: int, field_1: Tuple[int, str, int]) -> None:
        super().__init__(mod=24, act=4)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossGetDefeatRecordListResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        return cls(f_0, f_1)

@dataclass
class WorldbossResetDeathCdReq(BasePacket):
    """WorldBoss.reset_death_cd 请求封包 (Mod 24, Act 5)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=24, act=5)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossResetDeathCdReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class WorldbossResetDeathCdResp(BasePacket):
    """WorldBoss.reset_death_cd 应答封包 (Mod 24, Act 5)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=24, act=5)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossResetDeathCdResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class WorldbossSuperRebornReq(BasePacket):
    """WorldBoss.super_reborn 请求封包 (Mod 24, Act 6)"""

    def __init__(self) -> None:
        super().__init__(mod=24, act=6)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossSuperRebornReq":
        return cls()

@dataclass
class WorldbossSuperRebornResp(BasePacket):
    """WorldBoss.super_reborn 应答封包 (Mod 24, Act 6)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=24, act=6)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_uint8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossSuperRebornResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_uint8()
        return cls(f_0, f_1)

@dataclass
class WorldbossStrengthenCombatReq(BasePacket):
    """WorldBoss.strengthen_combat 请求封包 (Mod 24, Act 7)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=24, act=7)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossStrengthenCombatReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class WorldbossStrengthenCombatResp(BasePacket):
    """WorldBoss.strengthen_combat 应答封包 (Mod 24, Act 7)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=24, act=7)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int8(self.field_1)
        writer.write_uint8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossStrengthenCombatResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int8()
        f_2 = reader.read_uint8()
        return cls(f_0, f_1, f_2)

@dataclass
class WorldbossSelectFactionBossTimeReq(BasePacket):
    """WorldBoss.select_faction_boss_time 请求封包 (Mod 24, Act 8)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=24, act=8)
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
    def decode(cls, data: bytes) -> "WorldbossSelectFactionBossTimeReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int8()
        f_2 = reader.read_int8()
        return cls(f_0, f_1, f_2)

@dataclass
class WorldbossSelectFactionBossTimeResp(BasePacket):
    """WorldBoss.select_faction_boss_time 应答封包 (Mod 24, Act 8)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=24, act=8)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int8(self.field_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossSelectFactionBossTimeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int8()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class WorldbossOpenWorldBossReq(BasePacket):
    """WorldBoss.open_world_boss 请求封包 (Mod 24, Act 9)"""

    def __init__(self) -> None:
        super().__init__(mod=24, act=9)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossOpenWorldBossReq":
        return cls()

@dataclass
class WorldbossOpenWorldBossResp(BasePacket):
    """WorldBoss.open_world_boss 应答封包 (Mod 24, Act 9)"""

    field_0: int
    field_1: str
    field_2: int

    def __init__(self, field_0: int, field_1: str, field_2: int) -> None:
        super().__init__(mod=24, act=9)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossOpenWorldBossResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_utf()
        f_2 = reader.read_int8()
        return cls(f_0, f_1, f_2)

@dataclass
class WorldbossCloseWorldBossReq(BasePacket):
    """WorldBoss.close_world_boss 请求封包 (Mod 24, Act 10)"""

    def __init__(self) -> None:
        super().__init__(mod=24, act=10)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossCloseWorldBossReq":
        return cls()

@dataclass
class WorldbossCloseWorldBossResp(BasePacket):
    """WorldBoss.close_world_boss 应答封包 (Mod 24, Act 10)"""

    field_0: int
    field_1: str
    field_2: int
    field_3: Tuple[int, str, int]

    def __init__(self, field_0: int, field_1: str, field_2: int, field_3: Tuple[int, str, int]) -> None:
        super().__init__(mod=24, act=10)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int64(self.field_2)
        # 写入动态列表 field_3 (元素数 + 记录项)
        writer.write_uint16(len(self.field_3))
        for item_3 in self.field_3:
            writer.write_json(item_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossCloseWorldBossResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_utf()
        f_2 = reader.read_int64()
        # 读取动态列表 f_3
        cnt_3 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_3 = []
        for _ in range(cnt_3):
            f_3.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class WorldbossDefeatWorldBossReq(BasePacket):
    """WorldBoss.defeat_world_boss 请求封包 (Mod 24, Act 11)"""

    def __init__(self) -> None:
        super().__init__(mod=24, act=11)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossDefeatWorldBossReq":
        return cls()

@dataclass
class WorldbossDefeatWorldBossResp(BasePacket):
    """WorldBoss.defeat_world_boss 应答封包 (Mod 24, Act 11)"""

    field_0: int
    field_1: str
    field_2: int
    field_3: int
    field_4: str
    field_5: int
    field_6: int
    field_7: Tuple[int, str, int]

    def __init__(self, field_0: int, field_1: str, field_2: int, field_3: int, field_4: str, field_5: int, field_6: int, field_7: Tuple[int, str, int]) -> None:
        super().__init__(mod=24, act=11)
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
        writer.write_int8(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_utf(self.field_4)
        writer.write_int64(self.field_5)
        writer.write_int32(self.field_6)
        # 写入动态列表 field_7 (元素数 + 记录项)
        writer.write_uint16(len(self.field_7))
        for item_7 in self.field_7:
            writer.write_json(item_7)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossDefeatWorldBossResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_utf()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        f_4 = reader.read_utf()
        f_5 = reader.read_int64()
        f_6 = reader.read_int32()
        # 读取动态列表 f_7
        cnt_7 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_7 = []
        for _ in range(cnt_7):
            f_7.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7)

@dataclass
class WorldbossHurtWorldBossReq(BasePacket):
    """WorldBoss.hurt_world_boss 请求封包 (Mod 24, Act 12)"""

    def __init__(self) -> None:
        super().__init__(mod=24, act=12)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossHurtWorldBossReq":
        return cls()

@dataclass
class WorldbossHurtWorldBossResp(BasePacket):
    """WorldBoss.hurt_world_boss 应答封包 (Mod 24, Act 12)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=24, act=12)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int64(self.field_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossHurtWorldBossResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int64()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class WorldbossPlayerDeathCdReq(BasePacket):
    """WorldBoss.player_death_cd 请求封包 (Mod 24, Act 13)"""

    def __init__(self) -> None:
        super().__init__(mod=24, act=13)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossPlayerDeathCdReq":
        return cls()

@dataclass
class WorldbossPlayerDeathCdResp(BasePacket):
    """WorldBoss.player_death_cd 应答封包 (Mod 24, Act 13)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=24, act=13)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossPlayerDeathCdResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class WorldbossUpdateWorldBossPositionReq(BasePacket):
    """WorldBoss.update_world_boss_position 请求封包 (Mod 24, Act 14)"""

    def __init__(self) -> None:
        super().__init__(mod=24, act=14)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossUpdateWorldBossPositionReq":
        return cls()

@dataclass
class WorldbossUpdateWorldBossPositionResp(BasePacket):
    """WorldBoss.update_world_boss_position 应答封包 (Mod 24, Act 14)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=24, act=14)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossUpdateWorldBossPositionResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class WorldbossPlayerWorldBossBuffReq(BasePacket):
    """WorldBoss.player_world_boss_buff 请求封包 (Mod 24, Act 15)"""

    def __init__(self) -> None:
        super().__init__(mod=24, act=15)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossPlayerWorldBossBuffReq":
        return cls()

@dataclass
class WorldbossPlayerWorldBossBuffResp(BasePacket):
    """WorldBoss.player_world_boss_buff 应答封包 (Mod 24, Act 15)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=24, act=15)
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
    def decode(cls, data: bytes) -> "WorldbossPlayerWorldBossBuffResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int8()
        f_2 = reader.read_int8()
        return cls(f_0, f_1, f_2)

@dataclass
class WorldbossFactionBossTimeListReq(BasePacket):
    """WorldBoss.faction_boss_time_list 请求封包 (Mod 24, Act 16)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=24, act=16)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossFactionBossTimeListReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class WorldbossFactionBossTimeListResp(BasePacket):
    """WorldBoss.faction_boss_time_list 应答封包 (Mod 24, Act 16)"""

    field_0: int
    field_1: int
    field_2: Tuple[int, int, int, int]

    def __init__(self, field_0: int, field_1: int, field_2: Tuple[int, int, int, int]) -> None:
        super().__init__(mod=24, act=16)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int8(self.field_1)
        # 写入动态列表 field_2 (元素数 + 记录项)
        writer.write_uint16(len(self.field_2))
        for item_2 in self.field_2:
            writer.write_json(item_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossFactionBossTimeListResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int8()
        # 读取动态列表 f_2
        cnt_2 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_2 = []
        for _ in range(cnt_2):
            f_2.append(reader.read_json())
        return cls(f_0, f_1, f_2)

@dataclass
class WorldbossSetRobotReq(BasePacket):
    """WorldBoss.set_robot 请求封包 (Mod 24, Act 17)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=24, act=17)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossSetRobotReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class WorldbossSetRobotResp(BasePacket):
    """WorldBoss.set_robot 应答封包 (Mod 24, Act 17)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=24, act=17)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossSetRobotResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class WorldbossWorldBossLowHealthReq(BasePacket):
    """WorldBoss.world_boss_low_health 请求封包 (Mod 24, Act 18)"""

    def __init__(self) -> None:
        super().__init__(mod=24, act=18)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossWorldBossLowHealthReq":
        return cls()

@dataclass
class WorldbossWorldBossLowHealthResp(BasePacket):
    """WorldBoss.world_boss_low_health 应答封包 (Mod 24, Act 18)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=24, act=18)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossWorldBossLowHealthResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class WorldbossGetRobotStatuReq(BasePacket):
    """WorldBoss.get_robot_statu 请求封包 (Mod 24, Act 19)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=24, act=19)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossGetRobotStatuReq":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class WorldbossGetRobotStatuResp(BasePacket):
    """WorldBoss.get_robot_statu 应答封包 (Mod 24, Act 19)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=24, act=19)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorldbossGetRobotStatuResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)
