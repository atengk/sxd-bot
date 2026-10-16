"""神仙道参战伙伴与角色阵型模块数据契约 (Mod 5: Mod_Role_Base)

定义伙伴列表查询、阵型参战状态与多实体反序列化强类型契约模型。
严格落实 [SAFE_READ] 只读安全红线。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter


class RoleConstants:
    """Mod_Role_Base 官方业务常量"""

    DEPLOY = 0
    NODEPLOY = 1
    REPLACE = 2
    YES = 3
    NO = 4
    SUCCEED = 5
    FAILED = 6
    IS_MAIN_ROLE = 15
    IS_FOLLOW_ROLE = 16


@dataclass
class RoleItem:
    """单个参战伙伴详细属性实体

    @author Ateng
    @since 2026-10-16
    """

    name: str = ""
    role_id: int = 0
    player_role_id: int = 0
    exp: int = 0
    max_exp: int = 0
    level: int = 1
    deploy_state: int = 0
    order: int = 0
    health: int = 0
    max_health: int = 0
    role_job: str = ""
    realm_level: int = 0
    raw_props: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_deployed(self) -> bool:
        """是否为主力上阵状态"""
        return self.deploy_state == RoleConstants.DEPLOY


@dataclass
class RoleGetRoleListReq(BasePacket):
    """查询角色伙伴列表请求 (Mod 5, Act 2) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    player_id: int = 0

    def __init__(self, player_id: int = 0) -> None:
        super().__init__(mod=5, act=2)
        self.player_id = player_id

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        writer.write_int32(self.player_id)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "RoleGetRoleListReq":
        reader = ByteArrayReader(data)
        pid = reader.read_int32() if reader.remaining >= 4 else 0
        return cls(player_id=pid)


@dataclass
class RoleGetRoleListResp(BasePacket):
    """伙伴列表应答封包 (Mod 5, Act 2) - [SAFE_READ]

    @author Ateng
    @since 2026-10-16
    """

    roles: List[RoleItem] = field(default_factory=list)
    raw_payload: bytes = b""

    def __init__(self, roles: Optional[List[RoleItem]] = None, raw_payload: bytes = b"") -> None:
        super().__init__(mod=5, act=2)
        self.roles = roles or []
        self.raw_payload = raw_payload

    def encode_payload(self) -> bytes:
        writer = ByteArrayWriter()
        # 15 个头部字段
        for _ in range(7):
            writer.write_int32(0)
        writer.write_utf("")
        writer.write_utf("")
        writer.write_int32(0)
        writer.write_int8(0)
        writer.write_int8(0)
        writer.write_int8(0)
        writer.write_int16(0)
        writer.write_int16(0)

        # 写入角色列表
        writer.write_uint16(len(self.roles))
        for r in self.roles:
            writer.write_utf(r.name)
            writer.write_int32(r.role_id)
            writer.write_int32(r.player_role_id)
            writer.write_int64(r.exp)
            writer.write_int64(r.max_exp)
            writer.write_int16(r.level)
            writer.write_int8(r.deploy_state)
            writer.write_int16(r.order)
            writer.write_int64(r.health)
            writer.write_int64(r.max_health)
        return writer.to_bytes()

    @classmethod
    def decode(cls, data: bytes) -> "RoleGetRoleListResp":
        reader = ByteArrayReader(data)
        roles: List[RoleItem] = []

        try:
            # 1. 尝试跳过 15 个头部字段 (共 7*4 + 2*utf + 4 + 3*1 + 2*2)
            # 前 7 个 int32 (28 字节)
            for _ in range(7):
                if reader.remaining >= 4:
                    reader.read_int32()
            # 2 个 string
            if reader.remaining >= 2:
                reader.read_utf()
            if reader.remaining >= 2:
                reader.read_utf()
            # 1 个 int32
            if reader.remaining >= 4:
                reader.read_int32()
            # 3 个 int8
            for _ in range(3):
                if reader.remaining >= 1:
                    reader.read_int8()
            # 2 个 int16
            for _ in range(2):
                if reader.remaining >= 2:
                    reader.read_int16()

            # 2. 读取角色列表总数
            if reader.remaining >= 2:
                count = reader.read_uint16()
                for _ in range(count):
                    if reader.remaining < 4:
                        break
                    name = reader.read_utf() if reader.remaining >= 2 else ""
                    role_id = reader.read_int32() if reader.remaining >= 4 else 0
                    player_role_id = reader.read_int32() if reader.remaining >= 4 else 0
                    exp = reader.read_int64() if reader.remaining >= 8 else 0
                    max_exp = reader.read_int64() if reader.remaining >= 8 else 0
                    level = reader.read_int16() if reader.remaining >= 2 else 1
                    deploy_state = reader.read_int8() if reader.remaining >= 1 else 0
                    order = reader.read_int16() if reader.remaining >= 2 else 0
                    health = reader.read_int64() if reader.remaining >= 8 else 0
                    max_health = reader.read_int64() if reader.remaining >= 8 else 0

                    roles.append(
                        RoleItem(
                            name=name,
                            role_id=role_id,
                            player_role_id=player_role_id,
                            exp=exp,
                            max_exp=max_exp,
                            level=level,
                            deploy_state=deploy_state,
                            order=order,
                            health=health,
                            max_health=max_health,
                        )
                    )
        except Exception:
            pass

        return cls(roles=roles, raw_payload=data)
