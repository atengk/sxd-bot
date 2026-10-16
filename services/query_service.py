"""神仙道数据查询与态势感知领域服务 (Query Service)

编排纯只读协议动作，提取玩家全景资产、伙伴阵型、日常进度并执行即查即存。

@author Ateng
@since 2026-10-16
"""

import logging
from typing import Optional, List
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.messages.player import PlayerInfoResp
from protocol.messages.role import RoleGetRoleListReq, RoleGetRoleListResp
from services.query_models import PlayerAssetDTO, RoleDTO
from storage.player_db import PlayerDatabase, PlayerProfileRecord, ModuleStateRecord

logger = logging.getLogger(__name__)


class QueryService:
    """无状态数据查询与态势感知服务

    @author Ateng
    @since 2026-10-16
    """

    def __init__(
        self,
        client: SXDClient,
        context: GameContext,
        player_db: Optional[PlayerDatabase] = None,
    ) -> None:
        self.client = client
        self.context = context
        self.player_db = player_db

    async def query_player_assets(self, timeout_sec: float = 3.0) -> PlayerAssetDTO:
        """查询玩家全景核心资产 (Mod 0, Act 2: get_player_info)

        发起只读状态请求，提取基础属性，更新上下文并写入本地 SQLite 仓储。

        Args:
            timeout_sec: 网络请求等待超时秒数。

        Returns:
            玩家资产强类型数据传输对象。
        """
        logger.info("正在查询角色基础全景资产 (Mod 0, Act 2: get_player_info)...")

        # 1. 发起只读请求 (Mod 0 Act 2)
        try:
            req_pkt = PacketBuilder(mod=0, act=2).build()
            resp_bytes = await self.client.request(req_pkt, timeout_sec=timeout_sec)
            if resp_bytes:
                info = PlayerInfoResp.decode(resp_bytes)
                self.context.update_player_info(
                    nickname=info.nickname,
                    player_id=self.context.player.player_id,
                    level=info.level,
                    coins=info.coins,
                    ingots=info.ingots,
                    power=info.power,
                    fame=info.fame,
                    vip_level=info.vip_level,
                    town_id=info.town_map_id,
                    mission_key=info.mission_key,
                )
        except Exception as exc:
            logger.warning("发包拉取 Mod 0 Act 2 异常或降级使用当前上下文: %s", exc)

        # 2. 从上下文组装 DTO
        p = self.context.player
        t = self.context.town
        dto = PlayerAssetDTO(
            player_id=p.player_id,
            nickname=p.nickname,
            level=p.level,
            coins=p.coins,
            ingots=p.ingots,
            power=p.power,
            max_power=200,
            fame=p.fame,
            vip_level=p.vip_level,
            town_id=t.town_id,
            town_name=t.town_name,
            mission_key=p.mission_key,
        )

        # 3. 即查即存：持久化更新本地 SQLite 数据库
        if self.player_db:
            try:
                rec = PlayerProfileRecord(
                    player_id=dto.player_id,
                    nickname=dto.nickname,
                    level=dto.level,
                    coins=dto.coins,
                    ingots=dto.ingots,
                    power=dto.power,
                    fame=dto.fame,
                    vip_level=dto.vip_level,
                    town_id=dto.town_id,
                    updated_at=dto.updated_at,
                )
                self.player_db.upsert_player_profile(rec)
                logger.debug("角色核心资产已成功持久化至本地 SQLite (player_id=%d)", dto.player_id)
            except Exception as e:
                logger.warning("本地 SQLite 资产快照写入失败 (非致命): %s", e)

        return dto

    async def query_roles(self, timeout_sec: float = 3.0) -> List[RoleDTO]:
        """查询参战伙伴与阵容列表 (Mod 5, Act 2: get_role_list)

        发起只读状态请求，提取上阵与主力伙伴详细信息，并同步持久化至本地 SQLite 快照。

        @author Ateng
        @since 2026-10-16

        Args:
            timeout_sec: 网络请求等待超时秒数。

        Returns:
            参战伙伴 DTO 列表。
        """
        logger.info("正在查询参战伙伴与阵型数据 (Mod 5, Act 2: get_role_list)...")
        roles_dto: List[RoleDTO] = []

        try:
            req_pkt = RoleGetRoleListReq(player_id=self.context.player.player_id)
            resp_bytes = await self.client.request(req_pkt, timeout_sec=timeout_sec)
            if resp_bytes:
                resp = RoleGetRoleListResp.decode(resp_bytes)
                for r in resp.roles:
                    roles_dto.append(
                        RoleDTO(
                            role_id=r.role_id,
                            player_role_id=r.player_role_id,
                            name=r.name,
                            level=r.level,
                            is_deployed=r.is_deployed,
                            health=r.health,
                            max_health=r.max_health,
                            role_job=r.role_job,
                            realm_level=r.realm_level,
                            raw_props=r.raw_props,
                        )
                    )
        except Exception as exc:
            logger.warning("发包拉取 Mod 5 Act 2 伙伴列表异常: %s", exc)

        # 若未成功获取任何伙伴且主角在上下文中，回退添加主角自身保底
        if not roles_dto and self.context.player.player_id > 0:
            roles_dto.append(
                RoleDTO(
                    role_id=1,
                    player_role_id=self.context.player.player_id,
                    name=self.context.player.nickname or "主角",
                    level=self.context.player.level,
                    is_deployed=True,
                )
            )

        # 即查即存：持久化写入本地 SQLite tb_module_state 表 (module_id=5, state_key="role_list")
        if self.player_db:
            try:
                rec = ModuleStateRecord(
                    module_id=5,
                    state_key="role_list",
                    payload={"roles": [r.to_dict() for r in roles_dto]},
                )
                self.player_db.set_module_state(rec)
                logger.debug("伙伴列表快照已成功持久化至本地 SQLite (roles_count=%d)", len(roles_dto))
            except Exception as e:
                logger.warning("本地 SQLite 伙伴快照写入失败 (非致命): %s", e)

        return roles_dto
