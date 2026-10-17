"""神仙道 Notify 模块协议代码契约 (Mod 20)

由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 Mod_Notify_Base。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Any, List, Tuple, Optional
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter

class NotifyConstants:
    """Notify 模块业务状态与行为常量"""

    BACK_LOTTERY = 27
    CHANGE_MONEY = 6
    CHRISTMAS_SEND_GIFT = 35
    CLOSE = 20
    COIN = 14
    COINS = 0
    DOUBLE_TURNTABLE = 32
    DRAGONBALL_SACRIFICE = 17
    DRAGONBALL_WISH = 18
    DUN_HUANG = 31
    EXPLORE_FORBIDDEN = 22
    FACTION = 5
    FAME = 3
    FATE = 15
    GOLD_TOWER = 34
    ITEM = 1
    ITEM_DECIPHER = 7
    LONG_GONG = 29
    MAKE_SKILL_BOOK = 21
    MEMENTO_COIN_EXCHANGE = 28
    MOONLIGHT_BOX = 33
    MYSTIC_CAPURE = 8
    NINE_DOOR = 30
    OPEN = 19
    PARADE_START = 25
    READY_WEDDING = 23
    ROLE = 2
    RULAI_CLOSE = 10
    RULAI_OPEN = 11
    RULAI_OPEN_FOR_CALL = 9
    STATEPOINT = 13
    STATE_POINT_LV = 12
    TANG_SENG = 4
    WEDDING_END = 26
    WEDDING_START = 24
    XIANLING = 16

@dataclass
class NotifyMissionAwardReq(BasePacket):
    """Notify.mission_award 请求封包 (Mod 20, Act 0)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=0)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyMissionAwardReq":
        return cls()

@dataclass
class NotifyMissionAwardResp(BasePacket):
    """Notify.mission_award 应答封包 (Mod 20, Act 0)"""

    field_0: int
    field_1: str
    field_2: int
    field_3: int
    field_4: int
    field_5: int

    def __init__(self, field_0: int, field_1: str, field_2: int, field_3: int, field_4: int, field_5: int) -> None:
        super().__init__(mod=20, act=0)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyMissionAwardResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5)

@dataclass
class NotifyPkAwardReq(BasePacket):
    """Notify.pk_award 请求封包 (Mod 20, Act 1)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=1)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPkAwardReq":
        return cls()

@dataclass
class NotifyPkAwardResp(BasePacket):
    """Notify.pk_award 应答封包 (Mod 20, Act 1)"""

    field_0: int
    field_1: str
    field_2: int
    field_3: int
    field_4: int

    def __init__(self, field_0: int, field_1: str, field_2: int, field_3: int, field_4: int) -> None:
        super().__init__(mod=20, act=1)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_uint8(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPkAwardResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_uint8()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class NotifyCompleteReelProductionReq(BasePacket):
    """Notify.complete_reel_production 请求封包 (Mod 20, Act 2)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=2)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyCompleteReelProductionReq":
        return cls()

@dataclass
class NotifyCompleteReelProductionResp(BasePacket):
    """Notify.complete_reel_production 应答封包 (Mod 20, Act 2)"""

    field_0: int
    field_1: str
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int
    field_8: int

    def __init__(self, field_0: int, field_1: str, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int) -> None:
        super().__init__(mod=20, act=2)
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
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int8(self.field_7)
        writer.write_int8(self.field_8)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyCompleteReelProductionResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        f_6 = reader.read_int32()
        f_7 = reader.read_int8()
        f_8 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8)

@dataclass
class NotifyRoleNumNotifyReq(BasePacket):
    """Notify.role_num_notify 请求封包 (Mod 20, Act 10)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=10)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyRoleNumNotifyReq":
        return cls()

@dataclass
class NotifyRoleNumNotifyResp(BasePacket):
    """Notify.role_num_notify 应答封包 (Mod 20, Act 10)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=10)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyRoleNumNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class NotifyNewResearchNotifyReq(BasePacket):
    """Notify.new_research_notify 请求封包 (Mod 20, Act 11)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=11)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNewResearchNotifyReq":
        return cls()

@dataclass
class NotifyNewResearchNotifyResp(BasePacket):
    """Notify.new_research_notify 应答封包 (Mod 20, Act 11)"""

    field_0: Tuple[int, str]

    def __init__(self, field_0: Tuple[int, str]) -> None:
        super().__init__(mod=20, act=11)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNewResearchNotifyResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class NotifyNewPartnersNotifyReq(BasePacket):
    """Notify.new_partners_notify 请求封包 (Mod 20, Act 12)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=12)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNewPartnersNotifyReq":
        return cls()

@dataclass
class NotifyNewPartnersNotifyResp(BasePacket):
    """Notify.new_partners_notify 应答封包 (Mod 20, Act 12)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=12)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNewPartnersNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class NotifyNotifyGetGoodFateReq(BasePacket):
    """Notify.notify_get_good_fate 请求封包 (Mod 20, Act 13)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=13)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyGetGoodFateReq":
        return cls()

@dataclass
class NotifyNotifyGetGoodFateResp(BasePacket):
    """Notify.notify_get_good_fate 应答封包 (Mod 20, Act 13)"""

    field_0: int
    field_1: str
    field_2: int

    def __init__(self, field_0: int, field_1: str, field_2: int) -> None:
        super().__init__(mod=20, act=13)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int16(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyGetGoodFateResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int16()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyNotifyPlayerMissionPracticeStatusReq(BasePacket):
    """Notify.notify_player_mission_practice_status 请求封包 (Mod 20, Act 14)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=14)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyPlayerMissionPracticeStatusReq":
        return cls()

@dataclass
class NotifyNotifyPlayerMissionPracticeStatusResp(BasePacket):
    """Notify.notify_player_mission_practice_status 应答封包 (Mod 20, Act 14)"""

    field_0: int
    field_1: int

    def __init__(self, field_0: int, field_1: int) -> None:
        super().__init__(mod=20, act=14)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyPlayerMissionPracticeStatusResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class NotifyUpdatePlayerSuperGiftReq(BasePacket):
    """Notify.update_player_super_gift 请求封包 (Mod 20, Act 15)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=15)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdatePlayerSuperGiftReq":
        return cls()

@dataclass
class NotifyUpdatePlayerSuperGiftResp(BasePacket):
    """Notify.update_player_super_gift 应答封包 (Mod 20, Act 15)"""

    field_0: Tuple[int, int, int, str]

    def __init__(self, field_0: Tuple[int, int, int, str]) -> None:
        super().__init__(mod=20, act=15)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdatePlayerSuperGiftResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class NotifyChangeEquipReq(BasePacket):
    """Notify.change_equip 请求封包 (Mod 20, Act 16)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=16)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyChangeEquipReq":
        return cls()

@dataclass
class NotifyChangeEquipResp(BasePacket):
    """Notify.change_equip 应答封包 (Mod 20, Act 16)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=20, act=16)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyChangeEquipResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyUpdateLuckyShopItemReq(BasePacket):
    """Notify.update_lucky_shop_item 请求封包 (Mod 20, Act 17)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=17)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateLuckyShopItemReq":
        return cls()

@dataclass
class NotifyUpdateLuckyShopItemResp(BasePacket):
    """Notify.update_lucky_shop_item 应答封包 (Mod 20, Act 17)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=17)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateLuckyShopItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class NotifyBuyGoodStuffInLuckyShopReq(BasePacket):
    """Notify.buy_good_stuff_in_lucky_shop 请求封包 (Mod 20, Act 18)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=18)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyBuyGoodStuffInLuckyShopReq":
        return cls()

@dataclass
class NotifyBuyGoodStuffInLuckyShopResp(BasePacket):
    """Notify.buy_good_stuff_in_lucky_shop 应答封包 (Mod 20, Act 18)"""

    field_0: int
    field_1: str
    field_2: int

    def __init__(self, field_0: int, field_1: str, field_2: int) -> None:
        super().__init__(mod=20, act=18)
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
    def decode(cls, data: bytes) -> "NotifyBuyGoodStuffInLuckyShopResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyDisbandFactionNotifyReq(BasePacket):
    """Notify.disband_faction_notify 请求封包 (Mod 20, Act 19)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=19)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyDisbandFactionNotifyReq":
        return cls()

@dataclass
class NotifyDisbandFactionNotifyResp(BasePacket):
    """Notify.disband_faction_notify 应答封包 (Mod 20, Act 19)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=19)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyDisbandFactionNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class NotifyKickoutMemberNotifyReq(BasePacket):
    """Notify.kickout_member_notify 请求封包 (Mod 20, Act 20)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=20)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyKickoutMemberNotifyReq":
        return cls()

@dataclass
class NotifyKickoutMemberNotifyResp(BasePacket):
    """Notify.kickout_member_notify 应答封包 (Mod 20, Act 20)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=20)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyKickoutMemberNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class NotifyPlayerTakeBibleReq(BasePacket):
    """Notify.player_take_bible 请求封包 (Mod 20, Act 22)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=22)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPlayerTakeBibleReq":
        return cls()

@dataclass
class NotifyPlayerTakeBibleResp(BasePacket):
    """Notify.player_take_bible 应答封包 (Mod 20, Act 22)"""

    field_0: str
    field_1: int

    def __init__(self, field_0: str, field_1: int) -> None:
        super().__init__(mod=20, act=22)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_uint8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPlayerTakeBibleResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_uint8()
        return cls(f_0, f_1)

@dataclass
class NotifyPlayerTakeBibleBerobbedReq(BasePacket):
    """Notify.player_take_bible_berobbed 请求封包 (Mod 20, Act 23)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=23)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPlayerTakeBibleBerobbedReq":
        return cls()

@dataclass
class NotifyPlayerTakeBibleBerobbedResp(BasePacket):
    """Notify.player_take_bible_berobbed 应答封包 (Mod 20, Act 23)"""

    field_0: str
    field_1: str
    field_2: int

    def __init__(self, field_0: str, field_1: str, field_2: int) -> None:
        super().__init__(mod=20, act=23)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_uint8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPlayerTakeBibleBerobbedResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_uint8()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyGameTimerReq(BasePacket):
    """Notify.game_timer 请求封包 (Mod 20, Act 24)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=24)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyGameTimerReq":
        return cls()

@dataclass
class NotifyGameTimerResp(BasePacket):
    """Notify.game_timer 应答封包 (Mod 20, Act 24)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=24)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyGameTimerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class NotifySendFlowerReq(BasePacket):
    """Notify.send_flower 请求封包 (Mod 20, Act 25)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=25)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifySendFlowerReq":
        return cls()

@dataclass
class NotifySendFlowerResp(BasePacket):
    """Notify.send_flower 应答封包 (Mod 20, Act 25)"""

    field_0: str
    field_1: str
    field_2: int
    field_3: int
    field_4: int

    def __init__(self, field_0: str, field_1: str, field_2: int, field_3: int, field_4: int) -> None:
        super().__init__(mod=20, act=25)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int8(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifySendFlowerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        f_4 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class NotifyPassTowerReq(BasePacket):
    """Notify.pass_tower 请求封包 (Mod 20, Act 26)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=26)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPassTowerReq":
        return cls()

@dataclass
class NotifyPassTowerResp(BasePacket):
    """Notify.pass_tower 应答封包 (Mod 20, Act 26)"""

    field_0: str
    field_1: int
    field_2: int

    def __init__(self, field_0: str, field_1: int, field_2: int) -> None:
        super().__init__(mod=20, act=26)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_int8(self.field_1)
        writer.write_int8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPassTowerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_int8()
        f_2 = reader.read_int8()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyUpdateRulaiStatusReq(BasePacket):
    """Notify.update_rulai_status 请求封包 (Mod 20, Act 28)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=28)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateRulaiStatusReq":
        return cls()

@dataclass
class NotifyUpdateRulaiStatusResp(BasePacket):
    """Notify.update_rulai_status 应答封包 (Mod 20, Act 28)"""

    field_0: int
    field_1: Tuple[int, str]
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: Tuple[int, str], field_2: int, field_3: int) -> None:
        super().__init__(mod=20, act=28)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        # 写入动态列表 field_1 (元素数 + 记录项)
        writer.write_uint16(len(self.field_1))
        for item_1 in self.field_1:
            writer.write_json(item_1)
        writer.write_int32(self.field_2)
        writer.write_int16(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateRulaiStatusResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        # 读取动态列表 f_1
        cnt_1 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_1 = []
        for _ in range(cnt_1):
            f_1.append(reader.read_json())
        f_2 = reader.read_int32()
        f_3 = reader.read_int16()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class NotifyRollCakeReq(BasePacket):
    """Notify.roll_cake 请求封包 (Mod 20, Act 29)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=29)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyRollCakeReq":
        return cls()

@dataclass
class NotifyRollCakeResp(BasePacket):
    """Notify.roll_cake 应答封包 (Mod 20, Act 29)"""

    field_0: int
    field_1: str
    field_2: int

    def __init__(self, field_0: int, field_1: str, field_2: int) -> None:
        super().__init__(mod=20, act=29)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyRollCakeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int8()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyUpdateServerWarStepReq(BasePacket):
    """Notify.update_server_war_step 请求封包 (Mod 20, Act 30)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=30)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateServerWarStepReq":
        return cls()

@dataclass
class NotifyUpdateServerWarStepResp(BasePacket):
    """Notify.update_server_war_step 应答封包 (Mod 20, Act 30)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=30)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateServerWarStepResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class NotifyHaveNewServerWarReportReq(BasePacket):
    """Notify.have_new_server_war_report 请求封包 (Mod 20, Act 31)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=31)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewServerWarReportReq":
        return cls()

@dataclass
class NotifyHaveNewServerWarReportResp(BasePacket):
    """Notify.have_new_server_war_report 应答封包 (Mod 20, Act 31)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=31)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewServerWarReportResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class NotifyServerWarWinnerReq(BasePacket):
    """Notify.server_war_winner 请求封包 (Mod 20, Act 32)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=32)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyServerWarWinnerReq":
        return cls()

@dataclass
class NotifyServerWarWinnerResp(BasePacket):
    """Notify.server_war_winner 应答封包 (Mod 20, Act 32)"""

    field_0: int
    field_1: str
    field_2: str
    field_3: str

    def __init__(self, field_0: int, field_1: str, field_2: str, field_3: str) -> None:
        super().__init__(mod=20, act=32)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_utf(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyServerWarWinnerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_utf()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class NotifyWorldWarTopLoginReq(BasePacket):
    """Notify.world_war_top_login 请求封包 (Mod 20, Act 33)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=33)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyWorldWarTopLoginReq":
        return cls()

@dataclass
class NotifyWorldWarTopLoginResp(BasePacket):
    """Notify.world_war_top_login 应答封包 (Mod 20, Act 33)"""

    field_0: str

    def __init__(self, field_0: str) -> None:
        super().__init__(mod=20, act=33)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyWorldWarTopLoginResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        return cls(f_0)

@dataclass
class NotifyZodiacEntryNotifyReq(BasePacket):
    """Notify.zodiac_entry_notify 请求封包 (Mod 20, Act 34)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=34)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyZodiacEntryNotifyReq":
        return cls()

@dataclass
class NotifyZodiacEntryNotifyResp(BasePacket):
    """Notify.zodiac_entry_notify 应答封包 (Mod 20, Act 34)"""

    field_0: str
    field_1: int

    def __init__(self, field_0: str, field_1: int) -> None:
        super().__init__(mod=20, act=34)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyZodiacEntryNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class NotifyGetPetAnimalExpReq(BasePacket):
    """Notify.get_pet_animal_exp 请求封包 (Mod 20, Act 35)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=35)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyGetPetAnimalExpReq":
        return cls()

@dataclass
class NotifyGetPetAnimalExpResp(BasePacket):
    """Notify.get_pet_animal_exp 应答封包 (Mod 20, Act 35)"""

    field_0: str

    def __init__(self, field_0: str) -> None:
        super().__init__(mod=20, act=35)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyGetPetAnimalExpResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        return cls(f_0)

@dataclass
class NotifyStudyStuntNotifyReq(BasePacket):
    """Notify.study_stunt_notify 请求封包 (Mod 20, Act 36)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=36)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyStudyStuntNotifyReq":
        return cls()

@dataclass
class NotifyStudyStuntNotifyResp(BasePacket):
    """Notify.study_stunt_notify 应答封包 (Mod 20, Act 36)"""

    field_0: str
    field_1: int

    def __init__(self, field_0: str, field_1: int) -> None:
        super().__init__(mod=20, act=36)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_int16(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyStudyStuntNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_int16()
        return cls(f_0, f_1)

@dataclass
class NotifyFlowerWeekNumberOneReq(BasePacket):
    """Notify.flower_week_number_one 请求封包 (Mod 20, Act 37)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=37)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyFlowerWeekNumberOneReq":
        return cls()

@dataclass
class NotifyFlowerWeekNumberOneResp(BasePacket):
    """Notify.flower_week_number_one 应答封包 (Mod 20, Act 37)"""

    field_0: str

    def __init__(self, field_0: str) -> None:
        super().__init__(mod=20, act=37)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyFlowerWeekNumberOneResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        return cls(f_0)

@dataclass
class NotifyCatHuntGoldenBoxReq(BasePacket):
    """Notify.cat_hunt_golden_box 请求封包 (Mod 20, Act 38)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=38)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyCatHuntGoldenBoxReq":
        return cls()

@dataclass
class NotifyCatHuntGoldenBoxResp(BasePacket):
    """Notify.cat_hunt_golden_box 应答封包 (Mod 20, Act 38)"""

    field_0: str
    field_1: int
    field_2: int

    def __init__(self, field_0: str, field_1: int, field_2: int) -> None:
        super().__init__(mod=20, act=38)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyCatHuntGoldenBoxResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyUpdateWorldFactionWarStepReq(BasePacket):
    """Notify.update_world_faction_war_step 请求封包 (Mod 20, Act 39)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=39)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateWorldFactionWarStepReq":
        return cls()

@dataclass
class NotifyUpdateWorldFactionWarStepResp(BasePacket):
    """Notify.update_world_faction_war_step 应答封包 (Mod 20, Act 39)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=39)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateWorldFactionWarStepResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class NotifyUpdateWorldFactionWarTeamReq(BasePacket):
    """Notify.update_world_faction_war_team 请求封包 (Mod 20, Act 40)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=40)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateWorldFactionWarTeamReq":
        return cls()

@dataclass
class NotifyUpdateWorldFactionWarTeamResp(BasePacket):
    """Notify.update_world_faction_war_team 应答封包 (Mod 20, Act 40)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=40)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateWorldFactionWarTeamResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class NotifyWorldFactionWarWinnerReq(BasePacket):
    """Notify.world_faction_war_winner 请求封包 (Mod 20, Act 41)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=41)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyWorldFactionWarWinnerReq":
        return cls()

@dataclass
class NotifyWorldFactionWarWinnerResp(BasePacket):
    """Notify.world_faction_war_winner 应答封包 (Mod 20, Act 41)"""

    field_0: str
    field_1: str
    field_2: str

    def __init__(self, field_0: str, field_1: str, field_2: str) -> None:
        super().__init__(mod=20, act=41)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyWorldFactionWarWinnerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyHaveNewWorldFactionWarReportReq(BasePacket):
    """Notify.have_new_world_faction_war_report 请求封包 (Mod 20, Act 42)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=42)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewWorldFactionWarReportReq":
        return cls()

@dataclass
class NotifyHaveNewWorldFactionWarReportResp(BasePacket):
    """Notify.have_new_world_faction_war_report 应答封包 (Mod 20, Act 42)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=42)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewWorldFactionWarReportResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class NotifyWeekRankingReq(BasePacket):
    """Notify.week_ranking 请求封包 (Mod 20, Act 43)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=43)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyWeekRankingReq":
        return cls()

@dataclass
class NotifyWeekRankingResp(BasePacket):
    """Notify.week_ranking 应答封包 (Mod 20, Act 43)"""

    field_0: int
    field_1: str

    def __init__(self, field_0: int, field_1: str) -> None:
        super().__init__(mod=20, act=43)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_utf(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyWeekRankingResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_utf()
        return cls(f_0, f_1)

@dataclass
class NotifySpecialNotifyReq(BasePacket):
    """Notify.special_notify 请求封包 (Mod 20, Act 44)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=44)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifySpecialNotifyReq":
        return cls()

@dataclass
class NotifySpecialNotifyResp(BasePacket):
    """Notify.special_notify 应答封包 (Mod 20, Act 44)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=44)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifySpecialNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class NotifyFindImmortalFiveNotifyReq(BasePacket):
    """Notify.find_immortal_five_notify 请求封包 (Mod 20, Act 45)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=45)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyFindImmortalFiveNotifyReq":
        return cls()

@dataclass
class NotifyFindImmortalFiveNotifyResp(BasePacket):
    """Notify.find_immortal_five_notify 应答封包 (Mod 20, Act 45)"""

    field_0: int
    field_1: str
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int
    field_8: int

    def __init__(self, field_0: int, field_1: str, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int) -> None:
        super().__init__(mod=20, act=45)
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
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int8(self.field_2)
        writer.write_int8(self.field_3)
        writer.write_int16(self.field_4)
        writer.write_int16(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int16(self.field_7)
        writer.write_int16(self.field_8)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyFindImmortalFiveNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int8()
        f_3 = reader.read_int8()
        f_4 = reader.read_int16()
        f_5 = reader.read_int16()
        f_6 = reader.read_int32()
        f_7 = reader.read_int16()
        f_8 = reader.read_int16()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8)

@dataclass
class NotifyUnlockSpecialPartnerReq(BasePacket):
    """Notify.unlock_special_partner 请求封包 (Mod 20, Act 47)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=47)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUnlockSpecialPartnerReq":
        return cls()

@dataclass
class NotifyUnlockSpecialPartnerResp(BasePacket):
    """Notify.unlock_special_partner 应答封包 (Mod 20, Act 47)"""

    field_0: List[int]

    def __init__(self, field_0: List[int]) -> None:
        super().__init__(mod=20, act=47)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_int32(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUnlockSpecialPartnerResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_int32())
        return cls(f_0)

@dataclass
class NotifyWorldTopWarGiftHasWhiteTigerReq(BasePacket):
    """Notify.world_top_war_gift_has_white_tiger 请求封包 (Mod 20, Act 48)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=48)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyWorldTopWarGiftHasWhiteTigerReq":
        return cls()

@dataclass
class NotifyWorldTopWarGiftHasWhiteTigerResp(BasePacket):
    """Notify.world_top_war_gift_has_white_tiger 应答封包 (Mod 20, Act 48)"""

    field_0: int
    field_1: str

    def __init__(self, field_0: int, field_1: str) -> None:
        super().__init__(mod=20, act=48)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyWorldTopWarGiftHasWhiteTigerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        return cls(f_0, f_1)

@dataclass
class NotifyLuckyWheelAwardSevenMedicineReelReq(BasePacket):
    """Notify.lucky_wheel_award_seven_medicine_reel 请求封包 (Mod 20, Act 49)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=49)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyLuckyWheelAwardSevenMedicineReelReq":
        return cls()

@dataclass
class NotifyLuckyWheelAwardSevenMedicineReelResp(BasePacket):
    """Notify.lucky_wheel_award_seven_medicine_reel 应答封包 (Mod 20, Act 49)"""

    field_0: int
    field_1: str
    field_2: int

    def __init__(self, field_0: int, field_1: str, field_2: int) -> None:
        super().__init__(mod=20, act=49)
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
    def decode(cls, data: bytes) -> "NotifyLuckyWheelAwardSevenMedicineReelResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyUpdateServerFactionWarStepReq(BasePacket):
    """Notify.update_server_faction_war_step 请求封包 (Mod 20, Act 50)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=50)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateServerFactionWarStepReq":
        return cls()

@dataclass
class NotifyUpdateServerFactionWarStepResp(BasePacket):
    """Notify.update_server_faction_war_step 应答封包 (Mod 20, Act 50)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=50)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateServerFactionWarStepResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class NotifyHaveNewServerFactionWarReportReq(BasePacket):
    """Notify.have_new_server_faction_war_report 请求封包 (Mod 20, Act 51)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=51)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewServerFactionWarReportReq":
        return cls()

@dataclass
class NotifyHaveNewServerFactionWarReportResp(BasePacket):
    """Notify.have_new_server_faction_war_report 应答封包 (Mod 20, Act 51)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=51)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewServerFactionWarReportResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class NotifyServerFactionWarWinnerReq(BasePacket):
    """Notify.server_faction_war_winner 请求封包 (Mod 20, Act 52)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=52)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyServerFactionWarWinnerReq":
        return cls()

@dataclass
class NotifyServerFactionWarWinnerResp(BasePacket):
    """Notify.server_faction_war_winner 应答封包 (Mod 20, Act 52)"""

    field_0: str

    def __init__(self, field_0: str) -> None:
        super().__init__(mod=20, act=52)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyServerFactionWarWinnerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        return cls(f_0)

@dataclass
class NotifyIngotLuckWheelNotifyReq(BasePacket):
    """Notify.ingot_luck_wheel_notify 请求封包 (Mod 20, Act 53)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=53)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyIngotLuckWheelNotifyReq":
        return cls()

@dataclass
class NotifyIngotLuckWheelNotifyResp(BasePacket):
    """Notify.ingot_luck_wheel_notify 应答封包 (Mod 20, Act 53)"""

    field_0: int
    field_1: str
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: str, field_2: int, field_3: int) -> None:
        super().__init__(mod=20, act=53)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_int32(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyIngotLuckWheelNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int32()
        f_3 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class NotifyStudySigilStuntNotifyReq(BasePacket):
    """Notify.study_sigil_stunt_notify 请求封包 (Mod 20, Act 54)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=54)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyStudySigilStuntNotifyReq":
        return cls()

@dataclass
class NotifyStudySigilStuntNotifyResp(BasePacket):
    """Notify.study_sigil_stunt_notify 应答封包 (Mod 20, Act 54)"""

    field_0: int
    field_1: str
    field_2: int

    def __init__(self, field_0: int, field_1: str, field_2: int) -> None:
        super().__init__(mod=20, act=54)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int16(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyStudySigilStuntNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int16()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyGetGoodFateNotifyReq(BasePacket):
    """Notify.get_good_fate_notify 请求封包 (Mod 20, Act 55)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=55)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyGetGoodFateNotifyReq":
        return cls()

@dataclass
class NotifyGetGoodFateNotifyResp(BasePacket):
    """Notify.get_good_fate_notify 应答封包 (Mod 20, Act 55)"""

    field_0: int
    field_1: str

    def __init__(self, field_0: int, field_1: str) -> None:
        super().__init__(mod=20, act=55)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyGetGoodFateNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        return cls(f_0, f_1)

@dataclass
class NotifyNotifyUnlockExclArtiReq(BasePacket):
    """Notify.notify_unlock_excl_arti 请求封包 (Mod 20, Act 56)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=56)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyUnlockExclArtiReq":
        return cls()

@dataclass
class NotifyNotifyUnlockExclArtiResp(BasePacket):
    """Notify.notify_unlock_excl_arti 应答封包 (Mod 20, Act 56)"""

    field_0: str
    field_1: int

    def __init__(self, field_0: str, field_1: int) -> None:
        super().__init__(mod=20, act=56)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyUnlockExclArtiResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class NotifyNotifyChristmasActivityAwardReq(BasePacket):
    """Notify.notify_christmas_activity_award 请求封包 (Mod 20, Act 57)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=57)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyChristmasActivityAwardReq":
        return cls()

@dataclass
class NotifyNotifyChristmasActivityAwardResp(BasePacket):
    """Notify.notify_christmas_activity_award 应答封包 (Mod 20, Act 57)"""

    field_0: int
    field_1: int
    field_2: str
    field_3: int
    field_4: int

    def __init__(self, field_0: int, field_1: int, field_2: str, field_3: int, field_4: int) -> None:
        super().__init__(mod=20, act=57)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyChristmasActivityAwardResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_utf()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class NotifyNotifyPlayerChangeJobReq(BasePacket):
    """Notify.notify_player_change_job 请求封包 (Mod 20, Act 58)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=58)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyPlayerChangeJobReq":
        return cls()

@dataclass
class NotifyNotifyPlayerChangeJobResp(BasePacket):
    """Notify.notify_player_change_job 应答封包 (Mod 20, Act 58)"""

    field_0: int
    field_1: str
    field_2: int

    def __init__(self, field_0: int, field_1: str, field_2: int) -> None:
        super().__init__(mod=20, act=58)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int16(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyPlayerChangeJobResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int16()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyNotifyLanternFestivalAwardReq(BasePacket):
    """Notify.notify_lantern_festival_award 请求封包 (Mod 20, Act 59)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=59)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyLanternFestivalAwardReq":
        return cls()

@dataclass
class NotifyNotifyLanternFestivalAwardResp(BasePacket):
    """Notify.notify_lantern_festival_award 应答封包 (Mod 20, Act 59)"""

    field_0: int
    field_1: int
    field_2: str
    field_3: int
    field_4: int

    def __init__(self, field_0: int, field_1: int, field_2: str, field_3: int, field_4: int) -> None:
        super().__init__(mod=20, act=59)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyLanternFestivalAwardResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_utf()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class NotifyNotifyPlayerHuntDemonAwardReq(BasePacket):
    """Notify.notify_player_hunt_demon_award 请求封包 (Mod 20, Act 60)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=60)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyPlayerHuntDemonAwardReq":
        return cls()

@dataclass
class NotifyNotifyPlayerHuntDemonAwardResp(BasePacket):
    """Notify.notify_player_hunt_demon_award 应答封包 (Mod 20, Act 60)"""

    field_0: int
    field_1: str
    field_2: int

    def __init__(self, field_0: int, field_1: str, field_2: int) -> None:
        super().__init__(mod=20, act=60)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyPlayerHuntDemonAwardResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int8()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyUpdateTwinDragonsStepReq(BasePacket):
    """Notify.update_twin_dragons_step 请求封包 (Mod 20, Act 61)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=61)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateTwinDragonsStepReq":
        return cls()

@dataclass
class NotifyUpdateTwinDragonsStepResp(BasePacket):
    """Notify.update_twin_dragons_step 应答封包 (Mod 20, Act 61)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=61)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateTwinDragonsStepResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class NotifyHaveNewTwinDragonsReportReq(BasePacket):
    """Notify.have_new_twin_dragons_report 请求封包 (Mod 20, Act 62)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=62)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewTwinDragonsReportReq":
        return cls()

@dataclass
class NotifyHaveNewTwinDragonsReportResp(BasePacket):
    """Notify.have_new_twin_dragons_report 应答封包 (Mod 20, Act 62)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=62)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewTwinDragonsReportResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class NotifyTwinDragonsWinnerReq(BasePacket):
    """Notify.twin_dragons_winner 请求封包 (Mod 20, Act 63)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=63)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyTwinDragonsWinnerReq":
        return cls()

@dataclass
class NotifyTwinDragonsWinnerResp(BasePacket):
    """Notify.twin_dragons_winner 应答封包 (Mod 20, Act 63)"""

    field_0: int
    field_1: str
    field_2: str
    field_3: str

    def __init__(self, field_0: int, field_1: str, field_2: str, field_3: str) -> None:
        super().__init__(mod=20, act=63)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_utf(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyTwinDragonsWinnerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_utf()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class NotifyOpenStBossGiftNotifyReq(BasePacket):
    """Notify.open_st_boss_gift_notify 请求封包 (Mod 20, Act 64)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=64)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyOpenStBossGiftNotifyReq":
        return cls()

@dataclass
class NotifyOpenStBossGiftNotifyResp(BasePacket):
    """Notify.open_st_boss_gift_notify 应答封包 (Mod 20, Act 64)"""

    field_0: int
    field_1: str
    field_2: int

    def __init__(self, field_0: int, field_1: str, field_2: int) -> None:
        super().__init__(mod=20, act=64)
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
    def decode(cls, data: bytes) -> "NotifyOpenStBossGiftNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int32()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyNotifyUnlockSupernaturalReq(BasePacket):
    """Notify.notify_unlock_supernatural 请求封包 (Mod 20, Act 65)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=65)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyUnlockSupernaturalReq":
        return cls()

@dataclass
class NotifyNotifyUnlockSupernaturalResp(BasePacket):
    """Notify.notify_unlock_supernatural 应答封包 (Mod 20, Act 65)"""

    field_0: str
    field_1: int

    def __init__(self, field_0: str, field_1: int) -> None:
        super().__init__(mod=20, act=65)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_int32(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyUnlockSupernaturalResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_int32()
        return cls(f_0, f_1)

@dataclass
class NotifyStudyExclusiveSupernaturalNotifyReq(BasePacket):
    """Notify.study_exclusive_supernatural_notify 请求封包 (Mod 20, Act 66)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=66)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyStudyExclusiveSupernaturalNotifyReq":
        return cls()

@dataclass
class NotifyStudyExclusiveSupernaturalNotifyResp(BasePacket):
    """Notify.study_exclusive_supernatural_notify 应答封包 (Mod 20, Act 66)"""

    field_0: int
    field_1: str
    field_2: int

    def __init__(self, field_0: int, field_1: str, field_2: int) -> None:
        super().__init__(mod=20, act=66)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int16(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyStudyExclusiveSupernaturalNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int16()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyHaveNewNewTopWarReportReq(BasePacket):
    """Notify.have_new_new_top_war_report 请求封包 (Mod 20, Act 67)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=67)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewNewTopWarReportReq":
        return cls()

@dataclass
class NotifyHaveNewNewTopWarReportResp(BasePacket):
    """Notify.have_new_new_top_war_report 应答封包 (Mod 20, Act 67)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=67)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewNewTopWarReportResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class NotifyNewTopWarWinnerReq(BasePacket):
    """Notify.new_top_war_winner 请求封包 (Mod 20, Act 68)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=68)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNewTopWarWinnerReq":
        return cls()

@dataclass
class NotifyNewTopWarWinnerResp(BasePacket):
    """Notify.new_top_war_winner 应答封包 (Mod 20, Act 68)"""

    field_0: int
    field_1: str
    field_2: str
    field_3: str

    def __init__(self, field_0: int, field_1: str, field_2: str, field_3: str) -> None:
        super().__init__(mod=20, act=68)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_utf(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNewTopWarWinnerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_utf()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class NotifyCircleWarNotifyReq(BasePacket):
    """Notify.circle_war_notify 请求封包 (Mod 20, Act 69)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=69)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyCircleWarNotifyReq":
        return cls()

@dataclass
class NotifyCircleWarNotifyResp(BasePacket):
    """Notify.circle_war_notify 应答封包 (Mod 20, Act 69)"""

    field_0: str
    field_1: int

    def __init__(self, field_0: str, field_1: int) -> None:
        super().__init__(mod=20, act=69)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyCircleWarNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class NotifySacrificeDragonballNotifyReq(BasePacket):
    """Notify.sacrifice_dragonball_notify 请求封包 (Mod 20, Act 70)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=70)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifySacrificeDragonballNotifyReq":
        return cls()

@dataclass
class NotifySacrificeDragonballNotifyResp(BasePacket):
    """Notify.sacrifice_dragonball_notify 应答封包 (Mod 20, Act 70)"""

    field_0: str
    field_1: int
    field_2: int

    def __init__(self, field_0: str, field_1: int, field_2: int) -> None:
        super().__init__(mod=20, act=70)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_uint8(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifySacrificeDragonballNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_int32()
        f_2 = reader.read_uint8()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifySacrificeDragonballWorldChannelNotifyReq(BasePacket):
    """Notify.sacrifice_dragonball_world_channel_notify 请求封包 (Mod 20, Act 71)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=71)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifySacrificeDragonballWorldChannelNotifyReq":
        return cls()

@dataclass
class NotifySacrificeDragonballWorldChannelNotifyResp(BasePacket):
    """Notify.sacrifice_dragonball_world_channel_notify 应答封包 (Mod 20, Act 71)"""

    field_0: str
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: str, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=20, act=71)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_int32(self.field_2)
        writer.write_uint8(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifySacrificeDragonballWorldChannelNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_int32()
        f_2 = reader.read_int32()
        f_3 = reader.read_uint8()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class NotifyGamableLevel1NotifyReq(BasePacket):
    """Notify.gamable_level_1_notify 请求封包 (Mod 20, Act 72)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=72)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyGamableLevel1NotifyReq":
        return cls()

@dataclass
class NotifyGamableLevel1NotifyResp(BasePacket):
    """Notify.gamable_level_1_notify 应答封包 (Mod 20, Act 72)"""

    field_0: str

    def __init__(self, field_0: str) -> None:
        super().__init__(mod=20, act=72)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyGamableLevel1NotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        return cls(f_0)

@dataclass
class NotifyGamableResultNotifyReq(BasePacket):
    """Notify.gamable_result_notify 请求封包 (Mod 20, Act 73)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=73)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyGamableResultNotifyReq":
        return cls()

@dataclass
class NotifyGamableResultNotifyResp(BasePacket):
    """Notify.gamable_result_notify 应答封包 (Mod 20, Act 73)"""

    field_0: int
    field_1: int
    field_2: int

    def __init__(self, field_0: int, field_1: int, field_2: int) -> None:
        super().__init__(mod=20, act=73)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int16(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int16(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyGamableResultNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int16()
        f_1 = reader.read_int16()
        f_2 = reader.read_int16()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyPlayerStTakeBibleReq(BasePacket):
    """Notify.player_st_take_bible 请求封包 (Mod 20, Act 74)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=74)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPlayerStTakeBibleReq":
        return cls()

@dataclass
class NotifyPlayerStTakeBibleResp(BasePacket):
    """Notify.player_st_take_bible 应答封包 (Mod 20, Act 74)"""

    field_0: str
    field_1: str
    field_2: str
    field_3: int

    def __init__(self, field_0: str, field_1: str, field_2: str, field_3: int) -> None:
        super().__init__(mod=20, act=74)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_uint8(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPlayerStTakeBibleResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_uint8()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class NotifyPlayerStTakeBibleBerobbedReq(BasePacket):
    """Notify.player_st_take_bible_berobbed 请求封包 (Mod 20, Act 75)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=75)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPlayerStTakeBibleBerobbedReq":
        return cls()

@dataclass
class NotifyPlayerStTakeBibleBerobbedResp(BasePacket):
    """Notify.player_st_take_bible_berobbed 应答封包 (Mod 20, Act 75)"""

    field_0: str
    field_1: str
    field_2: str
    field_3: str
    field_4: str
    field_5: str
    field_6: int

    def __init__(self, field_0: str, field_1: str, field_2: str, field_3: str, field_4: str, field_5: str, field_6: int) -> None:
        super().__init__(mod=20, act=75)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5
        self.field_6 = field_6

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_utf(self.field_3)
        writer.write_utf(self.field_4)
        writer.write_utf(self.field_5)
        writer.write_uint8(self.field_6)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPlayerStTakeBibleBerobbedResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_utf()
        f_4 = reader.read_utf()
        f_5 = reader.read_utf()
        f_6 = reader.read_uint8()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6)

@dataclass
class NotifyUpdateStSupWarStepReq(BasePacket):
    """Notify.update_st_sup_war_step 请求封包 (Mod 20, Act 76)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=76)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateStSupWarStepReq":
        return cls()

@dataclass
class NotifyUpdateStSupWarStepResp(BasePacket):
    """Notify.update_st_sup_war_step 应答封包 (Mod 20, Act 76)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=76)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateStSupWarStepResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class NotifyHaveNewStSupWarReportReq(BasePacket):
    """Notify.have_new_st_sup_war_report 请求封包 (Mod 20, Act 77)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=77)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewStSupWarReportReq":
        return cls()

@dataclass
class NotifyHaveNewStSupWarReportResp(BasePacket):
    """Notify.have_new_st_sup_war_report 应答封包 (Mod 20, Act 77)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=77)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewStSupWarReportResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class NotifyStSupWarWinnerReq(BasePacket):
    """Notify.st_sup_war_winner 请求封包 (Mod 20, Act 78)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=78)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyStSupWarWinnerReq":
        return cls()

@dataclass
class NotifyStSupWarWinnerResp(BasePacket):
    """Notify.st_sup_war_winner 应答封包 (Mod 20, Act 78)"""

    field_0: int
    field_1: str
    field_2: str

    def __init__(self, field_0: int, field_1: str, field_2: str) -> None:
        super().__init__(mod=20, act=78)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyStSupWarWinnerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifyNotifyLuxurySeatReq(BasePacket):
    """Notify.notify_luxury_seat 请求封包 (Mod 20, Act 79)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=79)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyLuxurySeatReq":
        return cls()

@dataclass
class NotifyNotifyLuxurySeatResp(BasePacket):
    """Notify.notify_luxury_seat 应答封包 (Mod 20, Act 79)"""

    field_0: int
    field_1: int
    field_2: str
    field_3: str
    field_4: str

    def __init__(self, field_0: int, field_1: int, field_2: str, field_3: str, field_4: str) -> None:
        super().__init__(mod=20, act=79)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int8(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_utf(self.field_3)
        writer.write_utf(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyLuxurySeatResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int8()
        f_2 = reader.read_utf()
        f_3 = reader.read_utf()
        f_4 = reader.read_utf()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class NotifyHaveNewGodWarReportReq(BasePacket):
    """Notify.have_new_god_war_report 请求封包 (Mod 20, Act 80)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=80)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewGodWarReportReq":
        return cls()

@dataclass
class NotifyHaveNewGodWarReportResp(BasePacket):
    """Notify.have_new_god_war_report 应答封包 (Mod 20, Act 80)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=80)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewGodWarReportResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class NotifyGodWarWinnerReq(BasePacket):
    """Notify.god_war_winner 请求封包 (Mod 20, Act 81)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=81)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyGodWarWinnerReq":
        return cls()

@dataclass
class NotifyGodWarWinnerResp(BasePacket):
    """Notify.god_war_winner 应答封包 (Mod 20, Act 81)"""

    field_0: str
    field_1: str
    field_2: str

    def __init__(self, field_0: str, field_1: str, field_2: str) -> None:
        super().__init__(mod=20, act=81)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyGodWarWinnerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        return cls(f_0, f_1, f_2)

@dataclass
class NotifySkyLanternBlessGoldQualityReq(BasePacket):
    """Notify.sky_lantern_bless_gold_quality 请求封包 (Mod 20, Act 82)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=82)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifySkyLanternBlessGoldQualityReq":
        return cls()

@dataclass
class NotifySkyLanternBlessGoldQualityResp(BasePacket):
    """Notify.sky_lantern_bless_gold_quality 应答封包 (Mod 20, Act 82)"""

    field_0: str
    field_1: str
    field_2: str
    field_3: int
    field_4: int
    field_5: int
    field_6: int

    def __init__(self, field_0: str, field_1: str, field_2: str, field_3: int, field_4: int, field_5: int, field_6: int) -> None:
        super().__init__(mod=20, act=82)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5
        self.field_6 = field_6

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_uint8(self.field_3)
        writer.write_uint8(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int32(self.field_6)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifySkyLanternBlessGoldQualityResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_uint8()
        f_4 = reader.read_uint8()
        f_5 = reader.read_int32()
        f_6 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6)

@dataclass
class NotifyWarPowerChangeReq(BasePacket):
    """Notify.war_power_change 请求封包 (Mod 20, Act 83)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=83)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyWarPowerChangeReq":
        return cls()

@dataclass
class NotifyWarPowerChangeResp(BasePacket):
    """Notify.war_power_change 应答封包 (Mod 20, Act 83)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=83)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int64(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyWarPowerChangeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int64()
        return cls(f_0)

@dataclass
class NotifySkyLanternBlessTopOneReq(BasePacket):
    """Notify.sky_lantern_bless_top_one 请求封包 (Mod 20, Act 84)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=84)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifySkyLanternBlessTopOneReq":
        return cls()

@dataclass
class NotifySkyLanternBlessTopOneResp(BasePacket):
    """Notify.sky_lantern_bless_top_one 应答封包 (Mod 20, Act 84)"""

    field_0: str
    field_1: str
    field_2: str
    field_3: str
    field_4: str
    field_5: str

    def __init__(self, field_0: str, field_1: str, field_2: str, field_3: str, field_4: str, field_5: str) -> None:
        super().__init__(mod=20, act=84)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_utf(self.field_3)
        writer.write_utf(self.field_4)
        writer.write_utf(self.field_5)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifySkyLanternBlessTopOneResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_utf()
        f_4 = reader.read_utf()
        f_5 = reader.read_utf()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5)

@dataclass
class NotifyMakeChaosItemReq(BasePacket):
    """Notify.make_chaos_item 请求封包 (Mod 20, Act 85)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=85)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyMakeChaosItemReq":
        return cls()

@dataclass
class NotifyMakeChaosItemResp(BasePacket):
    """Notify.make_chaos_item 应答封包 (Mod 20, Act 85)"""

    field_0: str
    field_1: int
    field_2: int
    field_3: int

    def __init__(self, field_0: str, field_1: int, field_2: int, field_3: int) -> None:
        super().__init__(mod=20, act=85)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_int16(self.field_1)
        writer.write_int16(self.field_2)
        writer.write_int8(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyMakeChaosItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_int16()
        f_2 = reader.read_int16()
        f_3 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class NotifyNotifyTravelShopStatusReq(BasePacket):
    """Notify.notify_travel_shop_status 请求封包 (Mod 20, Act 86)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=86)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyTravelShopStatusReq":
        return cls()

@dataclass
class NotifyNotifyTravelShopStatusResp(BasePacket):
    """Notify.notify_travel_shop_status 应答封包 (Mod 20, Act 86)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=86)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyTravelShopStatusResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class NotifyNotifyPlayerNewGiftReq(BasePacket):
    """Notify.notify_player_new_gift 请求封包 (Mod 20, Act 87)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=87)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyPlayerNewGiftReq":
        return cls()

@dataclass
class NotifyNotifyPlayerNewGiftResp(BasePacket):
    """Notify.notify_player_new_gift 应答封包 (Mod 20, Act 87)"""

    field_0: int
    field_1: int
    field_2: str
    field_3: str
    field_4: Tuple[int, int, int]

    def __init__(self, field_0: int, field_1: int, field_2: str, field_3: str, field_4: Tuple[int, int, int]) -> None:
        super().__init__(mod=20, act=87)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_utf(self.field_3)
        # 写入动态列表 field_4 (元素数 + 记录项)
        writer.write_uint16(len(self.field_4))
        for item_4 in self.field_4:
            writer.write_json(item_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyPlayerNewGiftResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int32()
        f_2 = reader.read_utf()
        f_3 = reader.read_utf()
        # 读取动态列表 f_4
        cnt_4 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_4 = []
        for _ in range(cnt_4):
            f_4.append(reader.read_json())
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class NotifyChristmasHuntDemonNotifyReq(BasePacket):
    """Notify.christmas_hunt_demon_notify 请求封包 (Mod 20, Act 88)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=88)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyChristmasHuntDemonNotifyReq":
        return cls()

@dataclass
class NotifyChristmasHuntDemonNotifyResp(BasePacket):
    """Notify.christmas_hunt_demon_notify 应答封包 (Mod 20, Act 88)"""

    field_0: str
    field_1: int
    field_2: int
    field_3: int
    field_4: int

    def __init__(self, field_0: str, field_1: int, field_2: int, field_3: int, field_4: int) -> None:
        super().__init__(mod=20, act=88)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_uint8(self.field_1)
        writer.write_int16(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_uint8(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyChristmasHuntDemonNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_uint8()
        f_2 = reader.read_int16()
        f_3 = reader.read_int32()
        f_4 = reader.read_uint8()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class NotifyBecomeImmortalReq(BasePacket):
    """Notify.become_immortal 请求封包 (Mod 20, Act 89)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=89)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyBecomeImmortalReq":
        return cls()

@dataclass
class NotifyBecomeImmortalResp(BasePacket):
    """Notify.become_immortal 应答封包 (Mod 20, Act 89)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=89)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyBecomeImmortalResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class NotifyNotifyStBossDetectTitleReq(BasePacket):
    """Notify.notify_st_boss_detect_title 请求封包 (Mod 20, Act 90)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=90)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyStBossDetectTitleReq":
        return cls()

@dataclass
class NotifyNotifyStBossDetectTitleResp(BasePacket):
    """Notify.notify_st_boss_detect_title 应答封包 (Mod 20, Act 90)"""

    field_0: str

    def __init__(self, field_0: str) -> None:
        super().__init__(mod=20, act=90)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyStBossDetectTitleResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        return cls(f_0)

@dataclass
class NotifyLotusLampColorfulQualityReq(BasePacket):
    """Notify.lotus_lamp_colorful_quality 请求封包 (Mod 20, Act 91)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=91)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyLotusLampColorfulQualityReq":
        return cls()

@dataclass
class NotifyLotusLampColorfulQualityResp(BasePacket):
    """Notify.lotus_lamp_colorful_quality 应答封包 (Mod 20, Act 91)"""

    field_0: str
    field_1: int
    field_2: int
    field_3: int
    field_4: int

    def __init__(self, field_0: str, field_1: int, field_2: int, field_3: int, field_4: int) -> None:
        super().__init__(mod=20, act=91)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_uint8(self.field_1)
        writer.write_uint8(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyLotusLampColorfulQualityResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_uint8()
        f_2 = reader.read_uint8()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class NotifyWishTreeGoodQualityReq(BasePacket):
    """Notify.wish_tree_good_quality 请求封包 (Mod 20, Act 92)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=92)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyWishTreeGoodQualityReq":
        return cls()

@dataclass
class NotifyWishTreeGoodQualityResp(BasePacket):
    """Notify.wish_tree_good_quality 应答封包 (Mod 20, Act 92)"""

    field_0: str
    field_1: str
    field_2: str
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: str

    def __init__(self, field_0: str, field_1: str, field_2: str, field_3: int, field_4: int, field_5: int, field_6: int, field_7: str) -> None:
        super().__init__(mod=20, act=92)
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
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_uint8(self.field_3)
        writer.write_uint8(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_utf(self.field_7)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyWishTreeGoodQualityResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_uint8()
        f_4 = reader.read_uint8()
        f_5 = reader.read_int32()
        f_6 = reader.read_int32()
        f_7 = reader.read_utf()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7)

@dataclass
class NotifyNotifyCardMasterDrawReq(BasePacket):
    """Notify.notify_card_master_draw 请求封包 (Mod 20, Act 93)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=93)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyCardMasterDrawReq":
        return cls()

@dataclass
class NotifyNotifyCardMasterDrawResp(BasePacket):
    """Notify.notify_card_master_draw 应答封包 (Mod 20, Act 93)"""

    field_0: str
    field_1: int

    def __init__(self, field_0: str, field_1: int) -> None:
        super().__init__(mod=20, act=93)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_int8(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyCardMasterDrawResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_int8()
        return cls(f_0, f_1)

@dataclass
class NotifySuperPrizePoolNotifyReq(BasePacket):
    """Notify.super_prize_pool_notify 请求封包 (Mod 20, Act 94)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=94)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifySuperPrizePoolNotifyReq":
        return cls()

@dataclass
class NotifySuperPrizePoolNotifyResp(BasePacket):
    """Notify.super_prize_pool_notify 应答封包 (Mod 20, Act 94)"""

    field_0: str
    field_1: str
    field_2: str
    field_3: int

    def __init__(self, field_0: str, field_1: str, field_2: str, field_3: int) -> None:
        super().__init__(mod=20, act=94)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_int32(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifySuperPrizePoolNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class NotifyAwakeSkillBookNotifyReq(BasePacket):
    """Notify.awake_skill_book_notify 请求封包 (Mod 20, Act 95)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=95)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyAwakeSkillBookNotifyReq":
        return cls()

@dataclass
class NotifyAwakeSkillBookNotifyResp(BasePacket):
    """Notify.awake_skill_book_notify 应答封包 (Mod 20, Act 95)"""

    field_0: int
    field_1: str
    field_2: int
    field_3: int

    def __init__(self, field_0: int, field_1: str, field_2: int, field_3: int) -> None:
        super().__init__(mod=20, act=95)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int16(self.field_2)
        writer.write_int8(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyAwakeSkillBookNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_utf()
        f_2 = reader.read_int16()
        f_3 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class NotifyFireworkNotifyReq(BasePacket):
    """Notify.firework_notify 请求封包 (Mod 20, Act 96)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=96)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyFireworkNotifyReq":
        return cls()

@dataclass
class NotifyFireworkNotifyResp(BasePacket):
    """Notify.firework_notify 应答封包 (Mod 20, Act 96)"""

    field_0: str
    field_1: str
    field_2: str
    field_3: int
    field_4: int
    field_5: int

    def __init__(self, field_0: str, field_1: str, field_2: str, field_3: int, field_4: int, field_5: int) -> None:
        super().__init__(mod=20, act=96)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyFireworkNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5)

@dataclass
class NotifyMarryNotifyReq(BasePacket):
    """Notify.marry_notify 请求封包 (Mod 20, Act 97)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=97)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyMarryNotifyReq":
        return cls()

@dataclass
class NotifyMarryNotifyResp(BasePacket):
    """Notify.marry_notify 应答封包 (Mod 20, Act 97)"""

    field_0: int
    field_1: str
    field_2: str
    field_3: str
    field_4: str
    field_5: int

    def __init__(self, field_0: int, field_1: str, field_2: str, field_3: str, field_4: str, field_5: int) -> None:
        super().__init__(mod=20, act=97)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_utf(self.field_3)
        writer.write_utf(self.field_4)
        writer.write_int32(self.field_5)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyMarryNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_utf()
        f_4 = reader.read_utf()
        f_5 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5)

@dataclass
class NotifyChangeNotifyReq(BasePacket):
    """Notify.change_notify 请求封包 (Mod 20, Act 98)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=98)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyChangeNotifyReq":
        return cls()

@dataclass
class NotifyChangeNotifyResp(BasePacket):
    """Notify.change_notify 应答封包 (Mod 20, Act 98)"""

    field_0: str
    field_1: str

    def __init__(self, field_0: str, field_1: str) -> None:
        super().__init__(mod=20, act=98)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyChangeNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        return cls(f_0, f_1)

@dataclass
class NotifyLotteryTicketWinnerNotifyReq(BasePacket):
    """Notify.lottery_ticket_winner_notify 请求封包 (Mod 20, Act 99)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=99)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyLotteryTicketWinnerNotifyReq":
        return cls()

@dataclass
class NotifyLotteryTicketWinnerNotifyResp(BasePacket):
    """Notify.lottery_ticket_winner_notify 应答封包 (Mod 20, Act 99)"""

    field_0: str
    field_1: str
    field_2: str
    field_3: int

    def __init__(self, field_0: str, field_1: str, field_2: str, field_3: int) -> None:
        super().__init__(mod=20, act=99)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_int8(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyLotteryTicketWinnerNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class NotifyFiveBlessingsNotifyReq(BasePacket):
    """Notify.five_blessings_notify 请求封包 (Mod 20, Act 100)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=100)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyFiveBlessingsNotifyReq":
        return cls()

@dataclass
class NotifyFiveBlessingsNotifyResp(BasePacket):
    """Notify.five_blessings_notify 应答封包 (Mod 20, Act 100)"""

    field_0: int
    field_1: str
    field_2: int
    field_3: int
    field_4: int
    field_5: int
    field_6: int
    field_7: int
    field_8: int

    def __init__(self, field_0: int, field_1: str, field_2: int, field_3: int, field_4: int, field_5: int, field_6: int, field_7: int, field_8: int) -> None:
        super().__init__(mod=20, act=100)
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
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int8(self.field_2)
        writer.write_int64(self.field_3)
        writer.write_int32(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int32(self.field_6)
        writer.write_int32(self.field_7)
        writer.write_int32(self.field_8)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyFiveBlessingsNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_int8()
        f_3 = reader.read_int64()
        f_4 = reader.read_int32()
        f_5 = reader.read_int32()
        f_6 = reader.read_int32()
        f_7 = reader.read_int32()
        f_8 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8)

@dataclass
class NotifyFourAnniversaryBackLotteryNotifyReq(BasePacket):
    """Notify.four_anniversary_back_lottery_notify 请求封包 (Mod 20, Act 101)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=101)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyFourAnniversaryBackLotteryNotifyReq":
        return cls()

@dataclass
class NotifyFourAnniversaryBackLotteryNotifyResp(BasePacket):
    """Notify.four_anniversary_back_lottery_notify 应答封包 (Mod 20, Act 101)"""

    field_0: int
    field_1: str
    field_2: int
    field_3: int
    field_4: int

    def __init__(self, field_0: int, field_1: str, field_2: int, field_3: int, field_4: int) -> None:
        super().__init__(mod=20, act=101)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_int16(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int8(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyFourAnniversaryBackLotteryNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_utf()
        f_2 = reader.read_int16()
        f_3 = reader.read_int32()
        f_4 = reader.read_int8()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class NotifyUpdateStArenaStepReq(BasePacket):
    """Notify.update_st_arena_step 请求封包 (Mod 20, Act 102)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=102)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateStArenaStepReq":
        return cls()

@dataclass
class NotifyUpdateStArenaStepResp(BasePacket):
    """Notify.update_st_arena_step 应答封包 (Mod 20, Act 102)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=102)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateStArenaStepResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class NotifyStIndianaJonesBoxAwardReq(BasePacket):
    """Notify.st_indiana_jones_box_award 请求封包 (Mod 20, Act 103)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=103)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyStIndianaJonesBoxAwardReq":
        return cls()

@dataclass
class NotifyStIndianaJonesBoxAwardResp(BasePacket):
    """Notify.st_indiana_jones_box_award 应答封包 (Mod 20, Act 103)"""

    field_0: int
    field_1: str
    field_2: str
    field_3: str
    field_4: int
    field_5: int

    def __init__(self, field_0: int, field_1: str, field_2: str, field_3: str, field_4: int, field_5: int) -> None:
        super().__init__(mod=20, act=103)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_utf(self.field_3)
        writer.write_int16(self.field_4)
        writer.write_int32(self.field_5)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyStIndianaJonesBoxAwardResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_utf()
        f_4 = reader.read_int16()
        f_5 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5)

@dataclass
class NotifyWorldSkyLanternBlessGoldQualityReq(BasePacket):
    """Notify.world_sky_lantern_bless_gold_quality 请求封包 (Mod 20, Act 104)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=104)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyWorldSkyLanternBlessGoldQualityReq":
        return cls()

@dataclass
class NotifyWorldSkyLanternBlessGoldQualityResp(BasePacket):
    """Notify.world_sky_lantern_bless_gold_quality 应答封包 (Mod 20, Act 104)"""

    field_0: str
    field_1: str
    field_2: str
    field_3: int
    field_4: int
    field_5: int
    field_6: int

    def __init__(self, field_0: str, field_1: str, field_2: str, field_3: int, field_4: int, field_5: int, field_6: int) -> None:
        super().__init__(mod=20, act=104)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5
        self.field_6 = field_6

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_uint8(self.field_3)
        writer.write_uint8(self.field_4)
        writer.write_int32(self.field_5)
        writer.write_int32(self.field_6)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyWorldSkyLanternBlessGoldQualityResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_uint8()
        f_4 = reader.read_uint8()
        f_5 = reader.read_int32()
        f_6 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6)

@dataclass
class NotifyUpdateStUnionSixvsixStepReq(BasePacket):
    """Notify.update_st_union_sixvsix_step 请求封包 (Mod 20, Act 105)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=105)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateStUnionSixvsixStepReq":
        return cls()

@dataclass
class NotifyUpdateStUnionSixvsixStepResp(BasePacket):
    """Notify.update_st_union_sixvsix_step 应答封包 (Mod 20, Act 105)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=105)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateStUnionSixvsixStepResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        return cls(f_0)

@dataclass
class NotifyHaveNewStUnionSixvsixReportReq(BasePacket):
    """Notify.have_new_st_union_sixvsix_report 请求封包 (Mod 20, Act 106)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=106)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewStUnionSixvsixReportReq":
        return cls()

@dataclass
class NotifyHaveNewStUnionSixvsixReportResp(BasePacket):
    """Notify.have_new_st_union_sixvsix_report 应答封包 (Mod 20, Act 106)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=106)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHaveNewStUnionSixvsixReportResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class NotifyStUnionSixvsixWinnerReq(BasePacket):
    """Notify.st_union_sixvsix_winner 请求封包 (Mod 20, Act 107)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=107)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyStUnionSixvsixWinnerReq":
        return cls()

@dataclass
class NotifyStUnionSixvsixWinnerResp(BasePacket):
    """Notify.st_union_sixvsix_winner 应答封包 (Mod 20, Act 107)"""

    field_0: int
    field_1: str
    field_2: str
    field_3: str

    def __init__(self, field_0: int, field_1: str, field_2: str, field_3: str) -> None:
        super().__init__(mod=20, act=107)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_utf(self.field_3)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyStUnionSixvsixWinnerResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_utf()
        return cls(f_0, f_1, f_2, f_3)

@dataclass
class NotifyHideTreasureMapItemReq(BasePacket):
    """Notify.hide_treasure_map_item 请求封包 (Mod 20, Act 108)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=108)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHideTreasureMapItemReq":
        return cls()

@dataclass
class NotifyHideTreasureMapItemResp(BasePacket):
    """Notify.hide_treasure_map_item 应答封包 (Mod 20, Act 108)"""

    field_0: str
    field_1: str
    field_2: str
    field_3: int
    field_4: int

    def __init__(self, field_0: str, field_1: str, field_2: str, field_3: int, field_4: int) -> None:
        super().__init__(mod=20, act=108)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_int32(self.field_3)
        writer.write_int32(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyHideTreasureMapItemResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_int32()
        f_4 = reader.read_int32()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class NotifyPlayerSaTakeBibleReq(BasePacket):
    """Notify.player_sa_take_bible 请求封包 (Mod 20, Act 109)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=109)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPlayerSaTakeBibleReq":
        return cls()

@dataclass
class NotifyPlayerSaTakeBibleResp(BasePacket):
    """Notify.player_sa_take_bible 应答封包 (Mod 20, Act 109)"""

    field_0: str
    field_1: str
    field_2: str
    field_3: int
    field_4: int

    def __init__(self, field_0: str, field_1: str, field_2: str, field_3: int, field_4: int) -> None:
        super().__init__(mod=20, act=109)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_int8(self.field_3)
        writer.write_uint8(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPlayerSaTakeBibleResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_int8()
        f_4 = reader.read_uint8()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class NotifyPlayerSaTakeBibleBerobbedReq(BasePacket):
    """Notify.player_sa_take_bible_berobbed 请求封包 (Mod 20, Act 110)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=110)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPlayerSaTakeBibleBerobbedReq":
        return cls()

@dataclass
class NotifyPlayerSaTakeBibleBerobbedResp(BasePacket):
    """Notify.player_sa_take_bible_berobbed 应答封包 (Mod 20, Act 110)"""

    field_0: str
    field_1: str
    field_2: str
    field_3: str
    field_4: str
    field_5: str
    field_6: int
    field_7: int

    def __init__(self, field_0: str, field_1: str, field_2: str, field_3: str, field_4: str, field_5: str, field_6: int, field_7: int) -> None:
        super().__init__(mod=20, act=110)
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
        writer.write_utf(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_utf(self.field_3)
        writer.write_utf(self.field_4)
        writer.write_utf(self.field_5)
        writer.write_int8(self.field_6)
        writer.write_uint8(self.field_7)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyPlayerSaTakeBibleBerobbedResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        f_2 = reader.read_utf()
        f_3 = reader.read_utf()
        f_4 = reader.read_utf()
        f_5 = reader.read_utf()
        f_6 = reader.read_int8()
        f_7 = reader.read_uint8()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5, f_6, f_7)

@dataclass
class NotifyNotifySaLuxurySeatReq(BasePacket):
    """Notify.notify_sa_luxury_seat 请求封包 (Mod 20, Act 111)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=111)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifySaLuxurySeatReq":
        return cls()

@dataclass
class NotifyNotifySaLuxurySeatResp(BasePacket):
    """Notify.notify_sa_luxury_seat 应答封包 (Mod 20, Act 111)"""

    field_0: int
    field_1: int
    field_2: str
    field_3: str
    field_4: str

    def __init__(self, field_0: int, field_1: int, field_2: str, field_3: str, field_4: str) -> None:
        super().__init__(mod=20, act=111)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        writer.write_int8(self.field_1)
        writer.write_utf(self.field_2)
        writer.write_utf(self.field_3)
        writer.write_utf(self.field_4)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifySaLuxurySeatResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        f_1 = reader.read_int8()
        f_2 = reader.read_utf()
        f_3 = reader.read_utf()
        f_4 = reader.read_utf()
        return cls(f_0, f_1, f_2, f_3, f_4)

@dataclass
class NotifyNotifyActivityAwardReq(BasePacket):
    """Notify.notify_activity_award 请求封包 (Mod 20, Act 112)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=112)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyActivityAwardReq":
        return cls()

@dataclass
class NotifyNotifyActivityAwardResp(BasePacket):
    """Notify.notify_activity_award 应答封包 (Mod 20, Act 112)"""

    field_0: int
    field_1: int
    field_2: str
    field_3: Tuple[int, int]
    field_4: str
    field_5: str

    def __init__(self, field_0: int, field_1: int, field_2: str, field_3: Tuple[int, int], field_4: str, field_5: str) -> None:
        super().__init__(mod=20, act=112)
        self.field_0 = field_0
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3
        self.field_4 = field_4
        self.field_5 = field_5

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.field_0)
        writer.write_int32(self.field_1)
        writer.write_utf(self.field_2)
        # 写入动态列表 field_3 (元素数 + 记录项)
        writer.write_uint16(len(self.field_3))
        for item_3 in self.field_3:
            writer.write_json(item_3)
        writer.write_utf(self.field_4)
        writer.write_utf(self.field_5)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyActivityAwardResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_uint8()
        f_1 = reader.read_int32()
        f_2 = reader.read_utf()
        # 读取动态列表 f_3
        cnt_3 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_3 = []
        for _ in range(cnt_3):
            f_3.append(reader.read_json())
        f_4 = reader.read_utf()
        f_5 = reader.read_utf()
        return cls(f_0, f_1, f_2, f_3, f_4, f_5)

@dataclass
class NotifyUpdateNewServerWarStepReq(BasePacket):
    """Notify.update_new_server_war_step 请求封包 (Mod 20, Act 113)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=113)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateNewServerWarStepReq":
        return cls()

@dataclass
class NotifyUpdateNewServerWarStepResp(BasePacket):
    """Notify.update_new_server_war_step 应答封包 (Mod 20, Act 113)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=113)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyUpdateNewServerWarStepResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class NotifyNewHaveNewServerWarReportReq(BasePacket):
    """Notify.new_have_new_server_war_report 请求封包 (Mod 20, Act 114)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=114)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNewHaveNewServerWarReportReq":
        return cls()

@dataclass
class NotifyNewHaveNewServerWarReportResp(BasePacket):
    """Notify.new_have_new_server_war_report 应答封包 (Mod 20, Act 114)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=114)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int8(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNewHaveNewServerWarReportResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int8()
        return cls(f_0)

@dataclass
class NotifyZongziVoteCampVoteReq(BasePacket):
    """Notify.zongzi_vote_camp_vote 请求封包 (Mod 20, Act 115)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=115)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyZongziVoteCampVoteReq":
        return cls()

@dataclass
class NotifyZongziVoteCampVoteResp(BasePacket):
    """Notify.zongzi_vote_camp_vote 应答封包 (Mod 20, Act 115)"""

    field_0: Tuple[int, int]

    def __init__(self, field_0: Tuple[int, int]) -> None:
        super().__init__(mod=20, act=115)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 写入动态列表 field_0 (元素数 + 记录项)
        writer.write_uint16(len(self.field_0))
        for item_0 in self.field_0:
            writer.write_json(item_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyZongziVoteCampVoteResp":
        reader = ByteArrayReader(data)
        # 读取动态列表 f_0
        cnt_0 = reader.read_uint16() if reader.remaining >= 2 else 0
        f_0 = []
        for _ in range(cnt_0):
            f_0.append(reader.read_json())
        return cls(f_0)

@dataclass
class NotifyNotifyPlayerChargeReq(BasePacket):
    """Notify.notify_player_charge 请求封包 (Mod 20, Act 116)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=116)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyPlayerChargeReq":
        return cls()

@dataclass
class NotifyNotifyPlayerChargeResp(BasePacket):
    """Notify.notify_player_charge 应答封包 (Mod 20, Act 116)"""

    field_0: int

    def __init__(self, field_0: int) -> None:
        super().__init__(mod=20, act=116)
        self.field_0 = field_0

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.field_0)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyNotifyPlayerChargeResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_int32()
        return cls(f_0)

@dataclass
class NotifyFairyGameNotifyReq(BasePacket):
    """Notify.fairy_game_notify 请求封包 (Mod 20, Act 117)"""

    def __init__(self) -> None:
        super().__init__(mod=20, act=117)

    def encode_payload(self) -> bytes:
        return b''

    @classmethod
    def decode(cls, data: bytes) -> "NotifyFairyGameNotifyReq":
        return cls()

@dataclass
class NotifyFairyGameNotifyResp(BasePacket):
    """Notify.fairy_game_notify 应答封包 (Mod 20, Act 117)"""

    field_0: str
    field_1: str

    def __init__(self, field_0: str, field_1: str) -> None:
        super().__init__(mod=20, act=117)
        self.field_0 = field_0
        self.field_1 = field_1

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.field_0)
        writer.write_utf(self.field_1)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "NotifyFairyGameNotifyResp":
        reader = ByteArrayReader(data)
        f_0 = reader.read_utf()
        f_1 = reader.read_utf()
        return cls(f_0, f_1)
