"""神仙道数据查询与态势感知领域服务 (Query Service)

编排纯只读协议动作，提取玩家全景资产、伙伴阵型、日常进度并执行即查即存。

@author Ateng
@since 2026-10-16
"""

import logging
from typing import Optional, List, Dict, Any
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.messages.player import PlayerInfoResp
from protocol.messages.role import RoleGetRoleListReq, RoleGetRoleListResp
from protocol.messages.assistant import AssistantInfoReq, AssistantInfoResp
from protocol.messages.item import ItemGetPlayerPackItemListReq, ItemGetPlayerPackItemListResp
from services.query_models import (
    PlayerAssetDTO,
    RoleDTO,
    AssistantDailyDTO,
    AssistantDailyItemDTO,
    AssistantLivenessBoxDTO,
    InventoryItemDTO,
    PackSummaryDTO,
)
from storage.player_db import (
    PlayerDatabase,
    PlayerProfileRecord,
    ModuleStateRecord,
    InventoryItemRecord,
)

logger = logging.getLogger(__name__)

ImportantItemRegistry: Dict[int, Dict[str, Any]] = {
    1001: {"name": "初级体力丹", "category": "战略消耗", "power": 50, "exp": 0},
    1002: {"name": "中级体力丹", "category": "战略消耗", "power": 100, "exp": 0},
    1003: {"name": "高级体力丹", "category": "战略消耗", "power": 200, "exp": 0},
    1004: {"name": "特级体力丹", "category": "战略消耗", "power": 500, "exp": 0},
    2001: {"name": "初级经验丹", "category": "战略消耗", "power": 0, "exp": 10000},
    2002: {"name": "中级经验丹", "category": "战略消耗", "power": 0, "exp": 50000},
    2003: {"name": "高级经验丹", "category": "战略消耗", "power": 0, "exp": 200000},
    3001: {"name": "节日自选礼包盒", "category": "战略礼包", "power": 0, "exp": 0, "is_gift": True},
    3002: {"name": "活跃度宝箱", "category": "战略礼包", "power": 0, "exp": 0, "is_gift": True},
    3003: {"name": "仙令自选福袋", "category": "战略礼包", "power": 0, "exp": 0, "is_gift": True},
}

ItemCategoryManifest: Dict[int, str] = {
    1: "装备",
    2: "消耗品",
    3: "材料",
    4: "任务道具",
    5: "命格/灵石",
    6: "符印/法宝",
}

AssistantItemManifest: Dict[int, str] = {
    1: "招财神符",
    2: "帮派祭神",
    3: "吉星高照",
    4: "仙府药园",
    5: "摘仙桃",
    6: "喜从天降",
    7: "吹鱼/钓鱼",
    8: "竞技场",
    9: "多人副本",
    10: "日常活跃/其他",
    11: "生肖重置",
    12: "送花/结缘",
    13: "仙道问灵",
    14: "点金石",
    15: "护送取经",
}


def _format_box_status(status: int) -> str:
    """转换活跃度宝箱状态码为可读状态文本"""
    if status == 0:
        return "可领取"
    elif status == 4:
        return "已领取"
    elif status == 2:
        return "未达标"
    elif status == 1:
        return "VIP不足"
    elif status == 3:
        return "背包已满"
    else:
        return f"状态({status})"




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

    async def query_assistant(self, timeout_sec: float = 3.0) -> AssistantDailyDTO:
        """查询小助手日常任务进度与活跃度看板 (Mod 52, Act 0: info)

        发起只读状态请求，提取日常条目完成度与活跃度宝箱状态，并持久化写入 SQLite。

        @author Ateng
        @since 2026-10-16

        Args:
            timeout_sec: 网络请求等待超时秒数。

        Returns:
            小助手日常态势强类型数据传输对象。
        """
        logger.info("正在查询小助手日常进度与活跃度 (Mod 52, Act 0: info)...")
        items_dto: List[AssistantDailyItemDTO] = []
        boxes_dto: List[AssistantLivenessBoxDTO] = []
        current_liveness = 0

        try:
            req_pkt = AssistantInfoReq()
            resp_bytes = await self.client.request(req_pkt, timeout_sec=timeout_sec)
            if resp_bytes:
                resp = AssistantInfoResp.decode(resp_bytes)
                for it in resp.items:
                    name = AssistantItemManifest.get(it.item_id, f"未知玩法 #{it.item_id}")
                    total_quota = it.quota_list[0] if it.quota_list else 1
                    is_completed = it.completed_count >= total_quota
                    items_dto.append(
                        AssistantDailyItemDTO(
                            item_id=it.item_id,
                            name=name,
                            completed_count=it.completed_count,
                            total_quota=total_quota,
                            is_completed=is_completed,
                        )
                    )

                for bx in resp.boxes:
                    status_desc = _format_box_status(bx.status)
                    boxes_dto.append(
                        AssistantLivenessBoxDTO(
                            box_id=bx.box_id,
                            required_liveness=bx.required_liveness,
                            status=bx.status,
                            status_desc=status_desc,
                        )
                    )
        except Exception as exc:
            logger.warning("发包拉取 Mod 52 Act 0 小助手数据异常: %s", exc)

        dto = AssistantDailyDTO(
            current_liveness=current_liveness,
            max_liveness=100,
            items=items_dto,
            boxes=boxes_dto,
        )

        # 即查即存：持久化写入本地 SQLite tb_module_state 表 (module_id=52, state_key="assistant_info")
        if self.player_db:
            try:
                rec = ModuleStateRecord(
                    module_id=52,
                    state_key="assistant_info",
                    payload=dto.to_dict(),
                )
                self.player_db.set_module_state(rec)
                logger.debug("小助手日常快照已成功持久化至本地 SQLite (items_count=%d)", len(items_dto))
            except Exception as e:
                logger.warning("本地 SQLite 小助手快照写入失败 (非致命): %s", e)

        return dto


    async def query_pack(self, timeout_sec: float = 3.0) -> PackSummaryDTO:
        """查询主背包与随身仓库道具盘点看板 (Mod 2, Act 41: get_player_pack_item_list)

        发起只读状态请求，统计主背包与仓库格位占用、空间预警、核心战略消耗品收益折算，
        并将提取到的道具列表同步落盘至本地 SQLite tb_inventory 表。

        @author Ateng
        @since 2026-10-16

        Args:
            timeout_sec: 网络请求等待超时秒数。

        Returns:
            主背包与随身仓库全局盘点强类型传输对象。
        """
        logger.info("正在查询主背包与随身仓库物品列表 (Mod 2, Act 41: get_player_pack_item_list)...")

        pack_capacity = 0
        pack_empty = 0
        warehouse_capacity = 0
        raw_pack_items: List[Any] = []
        raw_wh_items: List[Any] = []

        try:
            req_pkt = ItemGetPlayerPackItemListReq()
            resp_bytes = await self.client.request(req_pkt, timeout_sec=timeout_sec)
            if resp_bytes:
                resp = ItemGetPlayerPackItemListResp.decode(resp_bytes)
                pack_capacity = resp.pack_capacity
                pack_empty = resp.pack_empty_grids
                warehouse_capacity = resp.warehouse_capacity
                raw_pack_items = resp.pack_items
                raw_wh_items = resp.warehouse_items
        except Exception as exc:
            logger.warning("发包拉取 Mod 2 Act 41 背包道具数据异常: %s", exc)

        pack_used = max(0, pack_capacity - pack_empty) if pack_capacity > 0 else len(raw_pack_items)
        is_space_low = pack_empty < 5

        def _parse_raw_item(raw: Any) -> Optional[InventoryItemDTO]:
            if not isinstance(raw, (list, tuple)) or len(raw) < 3:
                return None
            player_item_id = int(raw[0])
            item_id = int(raw[1])
            grid_id = int(raw[2])
            item_type = int(raw[9]) if len(raw) > 9 else 0
            count = int(raw[10]) if len(raw) > 10 else 1

            if item_id in ImportantItemRegistry:
                meta = ImportantItemRegistry[item_id]
                name = meta["name"]
                type_desc = meta["category"]
                power = meta.get("power", 0) * count
                exp = meta.get("exp", 0) * count
                is_strategic = True
            else:
                name = f"道具 #{item_id}"
                type_desc = ItemCategoryManifest.get(item_type, "普通杂物")
                power = 0
                exp = 0
                is_strategic = False

            return InventoryItemDTO(
                grid_id=grid_id,
                item_id=item_id,
                name=name,
                count=max(1, count),
                item_type=item_type,
                type_desc=type_desc,
                potential_power=power,
                potential_exp=exp,
                is_strategic=is_strategic,
            )

        items_dto: List[InventoryItemDTO] = []
        strategic_items: List[InventoryItemDTO] = []
        category_counts: Dict[str, int] = {}

        total_potential_power = 0
        total_potential_exp = 0

        # 1. 解析主背包物品
        for raw in raw_pack_items:
            it = _parse_raw_item(raw)
            if it:
                items_dto.append(it)
                category_counts[it.type_desc] = category_counts.get(it.type_desc, 0) + 1
                if it.is_strategic:
                    strategic_items.append(it)
                    total_potential_power += it.potential_power
                    total_potential_exp += it.potential_exp

        # 2. 解析随身仓库物品
        wh_items_dto: List[InventoryItemDTO] = []
        for raw in raw_wh_items:
            it = _parse_raw_item(raw)
            if it:
                wh_items_dto.append(it)
                if it.is_strategic:
                    strategic_items.append(it)
                    total_potential_power += it.potential_power
                    total_potential_exp += it.potential_exp

        warehouse_used = len(wh_items_dto)
        warehouse_empty = max(0, warehouse_capacity - warehouse_used)

        dto = PackSummaryDTO(
            pack_capacity=pack_capacity,
            pack_used=pack_used,
            pack_empty=pack_empty,
            warehouse_capacity=warehouse_capacity,
            warehouse_used=warehouse_used,
            warehouse_empty=warehouse_empty,
            is_space_low=is_space_low,
            total_potential_power=total_potential_power,
            total_potential_exp=total_potential_exp,
            category_counts=category_counts,
            strategic_items=strategic_items,
            items=items_dto,
            warehouse_items=wh_items_dto,
        )

        # 3. 即查即存：持久化写入本地 SQLite tb_inventory 与 tb_module_state 表
        if self.player_db:
            try:
                inv_records = [
                    InventoryItemRecord(
                        grid_id=it.grid_id,
                        item_id=it.item_id,
                        count=it.count,
                        item_type=it.item_type,
                        props={"name": it.name, "type_desc": it.type_desc},
                    )
                    for it in items_dto
                ]
                self.player_db.upsert_inventory_items(inv_records)

                rec = ModuleStateRecord(
                    module_id=2,
                    state_key="pack_summary",
                    payload=dto.to_dict(),
                )
                self.player_db.set_module_state(rec)
                logger.debug("背包物品快照已成功持久化至本地 SQLite (items_count=%d)", len(items_dto))
            except Exception as e:
                logger.warning("本地 SQLite 背包快照写入失败 (非致命): %s", e)

        return dto


