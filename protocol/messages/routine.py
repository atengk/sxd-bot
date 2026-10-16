"""神仙道高频日常福利与资源运转全系模块数据契约 (Mod 13, 22, 30, 21, 38, 41, 76)

涵盖:
- Mod 13: 仙府药园与草药种植 (Mod_Farm_Base)
- Mod 22: 猎命系统与命格管理 (Mod_Fate_Base)
- Mod 30: 西天取经与使者护送 (Mod_TakeBible_Base)
- Mod 21: 仙履奇缘每日答题 (Mod_TravelEvent_Base)
- Mod 38: 吉星高照骰子投掷 (Mod_RollCake_Base)
- Mod 41: 帮派祭神关公上香 (Mod_WorshipMars_Base)
- Mod 76: 仙女献舞/共舞福利 (Mod_Dance_Base)

严格落实 [SAFE_READ], [ROUTINE_FREE], [HAZARDOUS_INGOT] 三级安全红线守卫。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Any
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter


# ==============================================================================
# Mod 13: 仙府药园 (Mod_Farm_Base)
# ==============================================================================

@dataclass
class FarmGetFarmlandInfoListReq(BasePacket):
    """获取药园地块列表信息请求 (Mod 13, Act 0) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=13, act=0)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "FarmGetFarmlandInfoListReq":
        return cls()


@dataclass
class FarmGetPlayerRoleInfoListReq(BasePacket):
    """获取可种植伙伴角色列表请求 (Mod 13, Act 1) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=13, act=1)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "FarmGetPlayerRoleInfoListReq":
        return cls()


@dataclass
class FarmPlantHerbsReq(BasePacket):
    """在指定地块播种草药 (Mod 13, Act 5) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    farmland_id: int
    role_id: int
    herbs_type: int = 0

    def __init__(self, farmland_id: int, role_id: int, herbs_type: int = 0) -> None:
        super().__init__(mod=13, act=5)
        self.farmland_id = farmland_id
        self.role_id = role_id
        self.herbs_type = herbs_type

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.farmland_id)
        writer.write_int32(self.role_id)
        writer.write_uint8(self.herbs_type)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmPlantHerbsReq":
        reader = ByteArrayReader(data)
        fid = reader.read_int32() if reader.remaining >= 4 else 0
        rid = reader.read_int32() if reader.remaining >= 4 else 0
        htype = reader.read_uint8() if reader.remaining >= 1 else 0
        return cls(farmland_id=fid, role_id=rid, herbs_type=htype)


@dataclass
class FarmHarvestReq(BasePacket):
    """收获已成熟草药地块 (Mod 13, Act 6) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    farmland_id: int

    def __init__(self, farmland_id: int) -> None:
        super().__init__(mod=13, act=6)
        self.farmland_id = farmland_id

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.farmland_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmHarvestReq":
        reader = ByteArrayReader(data)
        fid = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(farmland_id=fid)


@dataclass
class FarmHarvestResp(BasePacket):
    """收获草药结算回执 (Mod 13, Act 6) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    result_code: int
    gain_exp: int = 0
    gain_coins: int = 0

    def __init__(self, result_code: int, gain_exp: int = 0, gain_coins: int = 0) -> None:
        super().__init__(mod=13, act=6)
        self.result_code = result_code
        self.gain_exp = gain_exp
        self.gain_coins = gain_coins

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.result_code)
        writer.write_int64(self.gain_exp)
        writer.write_int32(self.gain_coins)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmHarvestResp":
        reader = ByteArrayReader(data)
        code = reader.read_uint8() if reader.remaining >= 1 else 1
        exp = reader.read_int64() if reader.remaining >= 8 else 0
        coins = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(result_code=code, gain_exp=exp, gain_coins=coins)


@dataclass
class FarmGetXianLingGiftReq(BasePacket):
    """领取仙府药园仙令每日免费礼包 (Mod 13, Act 20) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=13, act=20)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "FarmGetXianLingGiftReq":
        return cls()


@dataclass
class FarmBuyCoinTreeReq(BasePacket):
    """消耗元宝购买摇钱树聚宝次数 (Mod 13, Act 25) - [HAZARDOUS_INGOT]

    前置安全红线守卫拦截。

    @author Ateng
    @since 2026-10-16
    """

    count: int = 1
    allow_ingot: bool = False

    def __init__(self, count: int = 1, allow_ingot: bool = False) -> None:
        super().__init__(mod=13, act=25)
        if not allow_ingot:
            raise PermissionError("[HAZARDOUS_INGOT] buy_coin_tree_count 涉及元宝扣除，已触发安全熔断保护！若确认执行请显式设置 allow_ingot=True")
        self.count = count
        self.allow_ingot = allow_ingot

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint16(self.count)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FarmBuyCoinTreeReq":
        reader = ByteArrayReader(data)
        cnt = reader.read_uint16() if reader.remaining >= 2 else 1
        return cls(count=cnt, allow_ingot=True)


# ==============================================================================
# Mod 22: 猎命系统 (Mod_Fate_Base)
# ==============================================================================

@dataclass
class FateGetFateNpcReq(BasePacket):
    """获取当前点亮的猎命师 NPC 状态 (Mod 22, Act 0) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=22, act=0)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "FateGetFateNpcReq":
        return cls()


@dataclass
class FateGetTempFateReq(BasePacket):
    """获取临时猎命槽命格列表 (Mod 22, Act 1) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=22, act=1)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "FateGetTempFateReq":
        return cls()


@dataclass
class FatePickupFateReq(BasePacket):
    """将临时命格拾取到正式背包 (Mod 22, Act 2) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    temp_fate_id: int

    def __init__(self, temp_fate_id: int) -> None:
        super().__init__(mod=22, act=2)
        self.temp_fate_id = temp_fate_id

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.temp_fate_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FatePickupFateReq":
        reader = ByteArrayReader(data)
        tid = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(temp_fate_id=tid)


@dataclass
class FateSaleTempFateReq(BasePacket):
    """一键变卖临时命格槽内的厄运灰命 (Mod 22, Act 3) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=22, act=3)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "FateSaleTempFateReq":
        return cls()


@dataclass
class FateGetBagListReq(BasePacket):
    """获取正式命格背包列表 (Mod 22, Act 4) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=22, act=4)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "FateGetBagListReq":
        return cls()


@dataclass
class FateGetRoleFateListReq(BasePacket):
    """获取角色已穿戴的命格列表 (Mod 22, Act 6) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    role_id: int

    def __init__(self, role_id: int) -> None:
        super().__init__(mod=22, act=6)
        self.role_id = role_id

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.role_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateGetRoleFateListReq":
        reader = ByteArrayReader(data)
        rid = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(role_id=rid)


@dataclass
class FateWearOnReq(BasePacket):
    """将命格穿戴到指定角色的命格槽位 (Mod 22, Act 7) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    player_role_id: int
    fate_id: int
    grid_id: int

    def __init__(self, player_role_id: int, fate_id: int, grid_id: int) -> None:
        super().__init__(mod=22, act=7)
        self.player_role_id = player_role_id
        self.fate_id = fate_id
        self.grid_id = grid_id

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.player_role_id)
        writer.write_int32(self.fate_id)
        writer.write_uint8(self.grid_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateWearOnReq":
        reader = ByteArrayReader(data)
        pid = reader.read_int32() if reader.remaining >= 4 else 0
        fid = reader.read_int32() if reader.remaining >= 4 else 0
        gid = reader.read_uint8() if reader.remaining >= 1 else 0
        return cls(player_role_id=pid, fate_id=fid, grid_id=gid)


@dataclass
class FateAppointFateNpcReq(BasePacket):
    """点击猎命师猎取命格 (Mod 22, Act 11) - [ROUTINE_FREE]

    npc_id 1~5 对应周一仙至姜子牙，仅允许铜钱猎命；若为高级元宝直召姜子牙需熔断。

    @author Ateng
    @since 2026-10-16
    """

    npc_id: int
    allow_ingot: bool = False

    def __init__(self, npc_id: int, allow_ingot: bool = False) -> None:
        super().__init__(mod=22, act=11)
        # npc_id=5 为姜子牙，若通过元宝直接点亮姜子牙属于高危操作
        self.npc_id = npc_id
        self.allow_ingot = allow_ingot

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.npc_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "FateAppointFateNpcReq":
        reader = ByteArrayReader(data)
        nid = reader.read_uint8() if reader.remaining >= 1 else 1
        return cls(npc_id=nid)


@dataclass
class FateBuyBagGridReq(BasePacket):
    """消耗元宝扩充命格背包格子 (Mod 22, Act 5) - [HAZARDOUS_INGOT]

    前置安全红线守卫拦截。

    @author Ateng
    @since 2026-10-16
    """

    allow_ingot: bool = False

    def __init__(self, allow_ingot: bool = False) -> None:
        super().__init__(mod=22, act=5)
        if not allow_ingot:
            raise PermissionError("[HAZARDOUS_INGOT] buy_bag_grid 涉及元宝扣除，已触发安全熔断保护！若确认执行请显式设置 allow_ingot=True")
        self.allow_ingot = allow_ingot

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "FateBuyBagGridReq":
        return cls(allow_ingot=True)


# ==============================================================================
# Mod 30: 西天取经 (Mod_TakeBible_Base)
# ==============================================================================

@dataclass
class TakeBibleOpenReq(BasePacket):
    """打开西天取经主大厅界面 (Mod 30, Act 0) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=30, act=0)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "TakeBibleOpenReq":
        return cls()


@dataclass
class TakeBibleGetInfoReq(BasePacket):
    """查询西天取经今日剩余次数与冷却 (Mod 30, Act 2) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=30, act=2)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "TakeBibleGetInfoReq":
        return cls()


@dataclass
class TakeBibleRefreshReq(BasePacket):
    """刷新取经使者等级 (Mod 30, Act 12) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=30, act=12)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "TakeBibleRefreshReq":
        return cls()


@dataclass
class TakeBibleStartReq(BasePacket):
    """发起西天取经启程护送 (Mod 30, Act 10) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=30, act=10)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "TakeBibleStartReq":
        return cls()


@dataclass
class TakeBibleRobReq(BasePacket):
    """打劫其他玩家护送的取经队伍 (Mod 30, Act 14) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    target_player_id: int

    def __init__(self, target_player_id: int) -> None:
        super().__init__(mod=30, act=14)
        self.target_player_id = target_player_id

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.target_player_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TakeBibleRobReq":
        reader = ByteArrayReader(data)
        pid = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(target_player_id=pid)


@dataclass
class TakeBibleQuicklyReq(BasePacket):
    """消耗元宝极速完成西天取经 (Mod 30, Act 11) - [HAZARDOUS_INGOT]

    前置安全红线守卫拦截。

    @author Ateng
    @since 2026-10-16
    """

    allow_ingot: bool = False

    def __init__(self, allow_ingot: bool = False) -> None:
        super().__init__(mod=30, act=11)
        if not allow_ingot:
            raise PermissionError("[HAZARDOUS_INGOT] take_bible_quickly 涉及元宝扣除，已触发安全熔断保护！若确认执行请显式设置 allow_ingot=True")
        self.allow_ingot = allow_ingot

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "TakeBibleQuicklyReq":
        return cls(allow_ingot=True)


@dataclass
class TakeBibleCallRuLaiReq(BasePacket):
    """消耗海量元宝直接召唤如来佛祖 (Mod 30, Act 13) - [HAZARDOUS_INGOT]

    前置安全红线守卫拦截。

    @author Ateng
    @since 2026-10-16
    """

    allow_ingot: bool = False

    def __init__(self, allow_ingot: bool = False) -> None:
        super().__init__(mod=30, act=13)
        if not allow_ingot:
            raise PermissionError("[HAZARDOUS_INGOT] call_ru_lai 涉及高额元宝扣除，已触发安全熔断保护！若确认执行请显式设置 allow_ingot=True")
        self.allow_ingot = allow_ingot

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "TakeBibleCallRuLaiReq":
        return cls(allow_ingot=True)


# ==============================================================================
# Mod 21: 仙履奇缘 (Mod_TravelEvent_Base)
# ==============================================================================

@dataclass
class TravelEventGetInfoReq(BasePacket):
    """查询仙履奇缘今日剩余答题次数 (Mod 21, Act 0) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=21, act=0)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "TravelEventGetInfoReq":
        return cls()


@dataclass
class TravelEventGetQuestionReq(BasePacket):
    """获取当前奇缘事件题目与选项 (Mod 21, Act 1) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=21, act=1)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "TravelEventGetQuestionReq":
        return cls()


@dataclass
class TravelEventAnswerReq(BasePacket):
    """提交仙履奇缘答题选择 (Mod 21, Act 2) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    event_id: int
    answer_index: int

    def __init__(self, event_id: int, answer_index: int) -> None:
        super().__init__(mod=21, act=2)
        self.event_id = event_id
        self.answer_index = answer_index

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.event_id)
        writer.write_uint8(self.answer_index)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "TravelEventAnswerReq":
        reader = ByteArrayReader(data)
        eid = reader.read_int32() if reader.remaining >= 4 else 0
        idx = reader.read_uint8() if reader.remaining >= 1 else 0
        return cls(event_id=eid, answer_index=idx)


@dataclass
class TravelEventCancelCdReq(BasePacket):
    """消耗元宝秒清仙履奇缘答题 CD (Mod 21, Act 3) - [HAZARDOUS_INGOT]

    前置安全红线守卫拦截。

    @author Ateng
    @since 2026-10-16
    """

    allow_ingot: bool = False

    def __init__(self, allow_ingot: bool = False) -> None:
        super().__init__(mod=21, act=3)
        if not allow_ingot:
            raise PermissionError("[HAZARDOUS_INGOT] cancel_cd 涉及元宝扣除，已触发安全熔断保护！若确认执行请显式设置 allow_ingot=True")
        self.allow_ingot = allow_ingot

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "TravelEventCancelCdReq":
        return cls(allow_ingot=True)


# ==============================================================================
# Mod 38: 吉星高照 (Mod_RollCake_Base)
# ==============================================================================

@dataclass
class RollCakeGetCountReq(BasePacket):
    """查询吉星高照今日剩余投掷次数 (Mod 38, Act 2) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=38, act=2)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "RollCakeGetCountReq":
        return cls()


@dataclass
class RollCakeRollReq(BasePacket):
    """发起吉星高照 6 颗骰子投掷 (Mod 38, Act 0) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=38, act=0)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "RollCakeRollReq":
        return cls()


@dataclass
class RollCakeGetAwardReq(BasePacket):
    """收获当前吉星投掷对应的境界点奖励 (Mod 38, Act 4) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=38, act=4)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "RollCakeGetAwardReq":
        return cls()


@dataclass
class RollCakeRerollReq(BasePacket):
    """改运重掷特定骰子 (Mod 38, Act 3) - [HAZARDOUS_INGOT]

    若超出每日免费改运次数将消耗元宝，因此未显式设置 allow_ingot 时拦截。

    @author Ateng
    @since 2026-10-16
    """

    allow_ingot: bool = False

    def __init__(self, allow_ingot: bool = False) -> None:
        super().__init__(mod=38, act=3)
        if not allow_ingot:
            raise PermissionError("[HAZARDOUS_INGOT] reroll 存在消耗元宝改运风险，已触发安全熔断保护！若确认执行请显式设置 allow_ingot=True")
        self.allow_ingot = allow_ingot

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "RollCakeRerollReq":
        return cls(allow_ingot=True)


# ==============================================================================
# Mod 41: 帮派祭神 (Mod_WorshipMars_Base)
# ==============================================================================

@dataclass
class WorshipMarsInfoReq(BasePacket):
    """查询关圣帝君像与今日祭神状态 (Mod 41, Act 0) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=41, act=0)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "WorshipMarsInfoReq":
        return cls()


@dataclass
class WorshipMarsRemainTimesReq(BasePacket):
    """查询今日剩余上香次数 (Mod 41, Act 4) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=41, act=4)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "WorshipMarsRemainTimesReq":
        return cls()


@dataclass
class WorshipMarsIncenseReq(BasePacket):
    """向关公像上香祈福 (Mod 41, Act 1) - [ROUTINE_FREE / HAZARDOUS_INGOT]

    上香类型:
    - 1: 白檀香 (消耗 100 阅历，零元宝放行)
    - 2: 苏合香 (消耗 30 元宝，高危熔断拦截)
    - 3: 天木香 (消耗 90 元宝，高危熔断拦截)

    @author Ateng
    @since 2026-10-16
    """

    incense_type: int = 1
    allow_ingot: bool = False

    def __init__(self, incense_type: int = 1, allow_ingot: bool = False) -> None:
        super().__init__(mod=41, act=1)
        if incense_type in (2, 3) and not allow_ingot:
            raise PermissionError(f"[HAZARDOUS_INGOT] 帮派祭神选择了元宝付费香 (type={incense_type})，已触发零元宝熔断保护！若确认执行请显式设置 allow_ingot=True")
        self.incense_type = incense_type
        self.allow_ingot = allow_ingot

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint8(self.incense_type)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "WorshipMarsIncenseReq":
        reader = ByteArrayReader(data)
        itype = reader.read_uint8() if reader.remaining >= 1 else 1
        return cls(incense_type=itype, allow_ingot=True)


# ==============================================================================
# Mod 76: 仙女献舞/共舞 (Mod_Dance_Base)
# ==============================================================================

@dataclass
class DanceGetInfoReq(BasePacket):
    """获取仙女献舞每日福利状态 (Mod 76, Act 0) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=76, act=0)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "DanceGetInfoReq":
        return cls()


@dataclass
class DanceStartReq(BasePacket):
    """开启仙女共舞福利 (Mod 76, Act 1) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=76, act=1)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "DanceStartReq":
        return cls()


@dataclass
class DanceReceiveAwardReq(BasePacket):
    """领取仙女献舞声望与奖励 (Mod 76, Act 2) - [ROUTINE_FREE]

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self) -> None:
        super().__init__(mod=76, act=2)

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "DanceReceiveAwardReq":
        return cls()
