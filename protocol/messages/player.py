"""神仙道玩家与核心登录模块数据契约 (Mod 0)

定义玩家登录请求、登录应答及基础属性响应的强类型序列化模型。

@author Ateng
@since 2026-10-15
"""

from dataclasses import dataclass
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

    @author Ateng
    @since 2026-10-15
    """

    result_code: int
    raw_extra: bytes

    def __init__(self, result_code: int, raw_extra: bytes) -> None:
        super().__init__(mod=0, act=0)
        self.result_code = result_code
        self.raw_extra = raw_extra

    @classmethod
    def decode(cls, data: bytes) -> "PlayerLoginResp":
        reader = ByteArrayReader(data)
        result_code = reader.read_uint8() if reader.remaining >= 1 else 0
        extra = reader.read_bytes()
        return cls(result_code=result_code, raw_extra=extra)

    @property
    def is_success(self) -> bool:
        return self.result_code == 0


@dataclass
class PlayerInfoResp(BasePacket):
    """角色基础属性同步应答 (Mod 0, Act 2)

    @author Ateng
    @since 2026-10-15
    """

    nickname: str
    player_id: int
    level: int = 1
    coins: int = 0
    ingots: int = 0
    raw_payload: bytes = b""

    def __init__(
        self,
        nickname: str,
        player_id: int,
        level: int = 1,
        coins: int = 0,
        ingots: int = 0,
        raw_payload: bytes = b"",
    ) -> None:
        super().__init__(mod=0, act=2)
        self.nickname = nickname
        self.player_id = player_id
        self.level = level
        self.coins = coins
        self.ingots = ingots
        self.raw_payload = raw_payload

    @classmethod
    def decode(cls, data: bytes) -> "PlayerInfoResp":
        reader = ByteArrayReader(data)
        nickname = reader.read_utf() if reader.remaining >= 2 else ""
        player_id = reader.read_int32() if reader.remaining >= 4 else 0
        coins = reader.read_int32() if reader.remaining >= 4 else 0
        ingots = reader.read_int32() if reader.remaining >= 4 else 0
        exp = reader.read_int64() if reader.remaining >= 8 else 0

        # 从属性扩展区中探测角色真实等级
        level = 1
        rem_bytes = data[len(data) - reader.remaining :]
        for offset in (16, 24, 0, 2):
            if offset + 2 <= len(rem_bytes):
                cand = int.from_bytes(rem_bytes[offset : offset + 2], "big")
                if 20 <= cand <= 250:
                    level = cand
                    break

        return cls(
            nickname=nickname,
            player_id=player_id,
            level=level,
            coins=coins,
            ingots=ingots,
            raw_payload=data,
        )
