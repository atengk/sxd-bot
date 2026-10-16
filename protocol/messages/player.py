"""神仙道玩家与核心登录模块数据契约 (Mod 0)

定义玩家登录请求、登录应答及基础属性响应的强类型序列化模型。

@author Ateng
@since 2026-10-15
"""

from dataclasses import dataclass, field
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter


@dataclass
class PlayerLoginReq(BasePacket):
    """玩家登录请求封包 (Mod 0, Act 0)

    @author Ateng
    @since 2026-10-15
    """

    username: str
    hash_code: str
    time: str
    platform: str
    server_id: int
    is_wd: int = 1
    wd_code: int = 0x60
    sub_code: int = 0
    publish: str = "疯玩"
    client_type: str = "pc_wd"
    flag: int = 1
    account: str = ""

    def __init__(
        self,
        username: str,
        hash_code: str,
        time: str,
        platform: str,
        server_id: int,
        is_wd: int = 1,
        wd_code: int = 0x60,
        sub_code: int = 0,
        publish: str = "疯玩",
        client_type: str = "pc_wd",
        flag: int = 1,
        account: str = "",
    ) -> None:
        super().__init__(mod=0, act=0)
        self.username = username
        self.hash_code = hash_code
        self.time = time
        self.platform = platform
        self.server_id = server_id
        self.is_wd = is_wd
        self.wd_code = wd_code
        self.sub_code = sub_code
        self.publish = publish
        self.client_type = client_type
        self.flag = flag
        self.account = account or username

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(self.username)
        writer.write_utf(self.hash_code)
        writer.write_utf(self.time)
        writer.write_utf(self.platform)
        writer.write_int32(0)
        writer.write_int32(self.server_id)
        writer.write_uint8(self.is_wd)
        writer.write_uint8(self.wd_code)
        writer.write_uint8(self.sub_code)
        writer.write_utf(self.publish)
        writer.write_utf(self.client_type)
        writer.write_uint8(self.flag)
        writer.write_utf(self.account)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerLoginReq":
        reader = ByteArrayReader(data)
        username = reader.read_utf()
        hash_code = reader.read_utf()
        time_str = reader.read_utf()
        platform = reader.read_utf()
        _zero = reader.read_int32()
        server_id = reader.read_int32()
        is_wd = reader.read_uint8()
        wd_code = reader.read_uint8()
        sub_code = reader.read_uint8()
        publish = reader.read_utf()
        client_type = reader.read_utf()
        flag = reader.read_uint8()
        account = reader.read_utf()
        return cls(
            username=username,
            hash_code=hash_code,
            time=time_str,
            platform=platform,
            server_id=server_id,
            is_wd=is_wd,
            wd_code=wd_code,
            sub_code=sub_code,
            publish=publish,
            client_type=client_type,
            flag=flag,
            account=account,
        )


@dataclass
class PlayerLoginResp(BasePacket):
    """玩家登录结果应答封包 (Mod 0, Act 0)

    对照官方 ActionScript 契约:
    [0] result_code: UByte (0=SUCCEED)
    [1] player_id: Int (玩家唯一数字 ID)

    @author Ateng
    @since 2026-10-15
    """

    result_code: int
    player_id: int = 0
    raw_extra: bytes = b""

    def __init__(self, result_code: int, player_id: int = 0, raw_extra: bytes = b"") -> None:
        super().__init__(mod=0, act=0)
        self.result_code = result_code
        self.player_id = player_id
        self.raw_extra = raw_extra

    @classmethod
    def decode(cls, data: bytes) -> "PlayerLoginResp":
        reader = ByteArrayReader(data)
        result_code = reader.read_uint8() if reader.remaining >= 1 else 0
        player_id = reader.read_int32() if reader.remaining >= 4 else 0
        extra = reader.read_bytes()
        return cls(result_code=result_code, player_id=player_id, raw_extra=extra)

    @property
    def is_success(self) -> bool:
        return self.result_code == 0


@dataclass
class PlayerInfoResp(BasePacket):
    """角色基础属性同步应答 (Mod 0, Act 2)

    100% 对照官方 Flash Main.swf PlayerData.format_player_info 44 个标准字段解码:
    Field 0: nickname (String) - 角色昵称
    Field 1: level (Int) - 真实等级 (如 300 级)
    Field 2: ingots (Int) - 真实持有元宝
    Field 3: coins (Long) - 真实持有铜钱 (8 字节长整型)
    Field 4: health (Long) - 生命值
    Field 5: max_health (Long) - 最大生命值
    Field 6: power (Int) - 真实当前体力
    Field 7: experience (Long) - 当前角色经验
    Field 8: max_experience (Long) - 当前等级经验上限
    Field 9: town_map_id (Int) - 真实所在城镇地图 ID (如 29 大理城)
    Field 14: vip_level (Int) - VIP 等级
    Field 19: camp_id (Byte) - 阵营 ID
    Field 21: fame (Int) - 角色声望
    Field 29: mission_key (Int) - 当前已解锁最高副本关卡 ID

    @author Ateng
    @since 2026-10-15
    """

    nickname: str
    player_id: int = 0
    level: int = 1
    ingots: int = 0
    coins: int = 0
    health: int = 0
    max_health: int = 0
    power: int = 0
    experience: int = 0
    max_experience: int = 0
    town_map_id: int = 0
    vip_level: int = 0
    camp_id: int = 0
    fame: int = 0
    mission_key: int = 0
    raw_payload: bytes = b""

    @classmethod
    def decode(cls, data: bytes) -> "PlayerInfoResp":
        reader = ByteArrayReader(data)
        nickname = reader.read_utf() if reader.remaining >= 2 else ""
        level = reader.read_int32() if reader.remaining >= 4 else 1
        ingots = reader.read_int32() if reader.remaining >= 4 else 0
        coins = reader.read_int64() if reader.remaining >= 8 else 0
        health = reader.read_int64() if reader.remaining >= 8 else 0
        max_health = reader.read_int64() if reader.remaining >= 8 else 0
        power = reader.read_int32() if reader.remaining >= 4 else 0
        exp = reader.read_int64() if reader.remaining >= 8 else 0
        max_exp = reader.read_int64() if reader.remaining >= 8 else 0
        town_map_id = reader.read_int32() if reader.remaining >= 4 else 0

        # 跳过 10~13 (bossMapId, jihuisuoId, mounts, mountsCD: 共 4 个 4B Int)
        for _ in range(4):
            if reader.remaining >= 4:
                reader.read_int32()

        vip_level = reader.read_int32() if reader.remaining >= 4 else 0

        # 跳过 15~18 (avatar, avatarCD, mainPlayerRoleId, mainRoleId: 共 4 个 4B Int)
        for _ in range(4):
            if reader.remaining >= 4:
                reader.read_int32()

        camp_id = reader.read_int8() if reader.remaining >= 1 else 0

        # 跳过 20 (townKey: 4B Int)
        if reader.remaining >= 4:
            reader.read_int32()

        fame = reader.read_int32() if reader.remaining >= 4 else 0

        # 跳过 22~28
        for _ in range(7):
            if reader.remaining >= 4:
                reader.read_int32()

        mission_key = reader.read_int32() if reader.remaining >= 4 else 0

        return cls(
            nickname=nickname,
            player_id=0,
            level=level,
            ingots=ingots,
            coins=coins,
            health=health,
            max_health=max_health,
            power=power,
            experience=exp,
            max_experience=max_exp,
            town_map_id=town_map_id,
            vip_level=vip_level,
            camp_id=camp_id,
            fame=fame,
            mission_key=mission_key,
            raw_payload=data,
        )


@dataclass
class PlayerBuyPowerReq(BasePacket):
    """消耗元宝购买体力请求 (Mod 0, Act 5) - [HAZARDOUS_INGOT]

    强制前置安全红线守卫拦截，防止未经授权意外扣除元宝。

    @author Ateng
    @since 2026-10-16
    """

    allow_ingot: bool = False

    def __init__(self, allow_ingot: bool = False) -> None:
        super().__init__(mod=0, act=5)
        if not allow_ingot:
            raise PermissionError("[HAZARDOUS_INGOT] buy_power 涉及元宝扣除，已触发安全熔断保护！若确认执行请显式设置 allow_ingot=True")
        self.allow_ingot = allow_ingot

    def encode_payload(self) -> bytes:
        return b""

    @classmethod
    def decode(cls, data: bytes) -> "PlayerBuyPowerReq":
        return cls(allow_ingot=True)


@dataclass
class PlayerUpdatePlayerDataResp(BasePacket):
    """角色基础与高阶数值变更广播 (Mod 0, Act 3) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    updates: dict = field(default_factory=dict)

    def __init__(self, updates: Optional[dict] = None) -> None:
        super().__init__(mod=0, act=3)
        self.updates = updates or {}

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_uint16(len(self.updates))
        for prop_id, val in sorted(self.updates.items()):
            writer.write_uint8(prop_id)
            writer.write_int64(val)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "PlayerUpdatePlayerDataResp":
        reader = ByteArrayReader(data)
        count = reader.read_uint16() if reader.remaining >= 2 else 0
        updates = {}
        for _ in range(count):
            if reader.remaining < 9:
                break
            prop_id = reader.read_uint8()
            val = reader.read_int64()
            updates[prop_id] = val
        return cls(updates=updates)

