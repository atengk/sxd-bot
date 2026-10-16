"""神仙道数据查询与态势感知强类型领域模型 (Query DTO Models)

定义全景资产看板、伙伴阵型与日常完成度等结构化数据传输对象。

@author Ateng
@since 2026-10-16
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import time


@dataclass
class PlayerAssetDTO:
    """玩家角色全景资产传输模型

    @author Ateng
    @since 2026-10-16
    """

    player_id: int = 0
    nickname: str = ""
    level: int = 1
    coins: int = 0
    ingots: int = 0
    power: int = 0
    max_power: int = 200
    experience: int = 0
    max_experience: int = 0
    fame: int = 0
    vip_level: int = 0
    town_id: int = 0
    town_name: str = ""
    mission_key: int = 0
    updated_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        """序列化为标准字典"""
        return {
            "player_id": self.player_id,
            "nickname": self.nickname,
            "level": self.level,
            "coins": self.coins,
            "ingots": self.ingots,
            "power": self.power,
            "max_power": self.max_power,
            "experience": self.experience,
            "max_experience": self.max_experience,
            "fame": self.fame,
            "vip_level": self.vip_level,
            "town_id": self.town_id,
            "town_name": self.town_name,
            "mission_key": self.mission_key,
            "updated_at": self.updated_at,
        }


@dataclass
class RoleDTO:
    """参战伙伴数据传输模型

    @author Ateng
    @since 2026-10-16
    """

    role_id: int = 0
    player_role_id: int = 0
    name: str = ""
    level: int = 1
    is_deployed: bool = True
    health: int = 0
    max_health: int = 0
    role_job: str = ""
    realm_level: int = 0
    raw_props: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """序列化为标准字典"""
        return {
            "role_id": self.role_id,
            "player_role_id": self.player_role_id,
            "name": self.name,
            "level": self.level,
            "is_deployed": self.is_deployed,
            "health": self.health,
            "max_health": self.max_health,
            "role_job": self.role_job,
            "realm_level": self.realm_level,
        }


@dataclass
class AssistantDailyItemDTO:
    """小助手单项日常任务传输模型

    @author Ateng
    @since 2026-10-16
    """

    item_id: int = 0
    name: str = ""
    completed_count: int = 0
    total_quota: int = 0
    is_completed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """序列化为标准字典"""
        return {
            "item_id": self.item_id,
            "name": self.name,
            "completed_count": self.completed_count,
            "total_quota": self.total_quota,
            "is_completed": self.is_completed,
        }


@dataclass
class AssistantLivenessBoxDTO:
    """小助手每日活跃度宝箱传输模型

    @author Ateng
    @since 2026-10-16
    """

    box_id: int = 0
    required_liveness: int = 0
    status: int = 0
    status_desc: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """序列化为标准字典"""
        return {
            "box_id": self.box_id,
            "required_liveness": self.required_liveness,
            "status": self.status,
            "status_desc": self.status_desc,
        }


@dataclass
class AssistantDailyDTO:
    """小助手今日日常态势与活跃度看板传输模型

    @author Ateng
    @since 2026-10-16
    """

    current_liveness: int = 0
    max_liveness: int = 100
    items: List[AssistantDailyItemDTO] = field(default_factory=list)
    boxes: List[AssistantLivenessBoxDTO] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """序列化为标准字典"""
        return {
            "current_liveness": self.current_liveness,
            "max_liveness": self.max_liveness,
            "items": [it.to_dict() for it in self.items],
            "boxes": [bx.to_dict() for bx in self.boxes],
        }


@dataclass
class InventoryItemDTO:
    """背包/随身仓库单项物品传输模型

    @author Ateng
    @since 2026-10-16
    """

    grid_id: int = 0
    item_id: int = 0
    name: str = ""
    count: int = 1
    item_type: int = 0
    type_desc: str = ""
    potential_power: int = 0
    potential_exp: int = 0
    is_strategic: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """序列化为标准字典"""
        return {
            "grid_id": self.grid_id,
            "item_id": self.item_id,
            "name": self.name,
            "count": self.count,
            "item_type": self.item_type,
            "type_desc": self.type_desc,
            "potential_power": self.potential_power,
            "potential_exp": self.potential_exp,
            "is_strategic": self.is_strategic,
        }


@dataclass
class PackSummaryDTO:
    """主背包与随身仓库全局盘点传输模型

    @author Ateng
    @since 2026-10-16
    """

    pack_capacity: int = 0
    pack_used: int = 0
    pack_empty: int = 0
    warehouse_capacity: int = 0
    warehouse_used: int = 0
    warehouse_empty: int = 0
    is_space_low: bool = False
    total_potential_power: int = 0
    total_potential_exp: int = 0
    category_counts: Dict[str, int] = field(default_factory=dict)
    strategic_items: List[InventoryItemDTO] = field(default_factory=list)
    items: List[InventoryItemDTO] = field(default_factory=list)
    warehouse_items: List[InventoryItemDTO] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """序列化为标准字典"""
        return {
            "pack_capacity": self.pack_capacity,
            "pack_used": self.pack_used,
            "pack_empty": self.pack_empty,
            "warehouse_capacity": self.warehouse_capacity,
            "warehouse_used": self.warehouse_used,
            "warehouse_empty": self.warehouse_empty,
            "is_space_low": self.is_space_low,
            "total_potential_power": self.total_potential_power,
            "total_potential_exp": self.total_potential_exp,
            "category_counts": self.category_counts,
            "strategic_items": [it.to_dict() for it in self.strategic_items],
            "items": [it.to_dict() for it in self.items],
            "warehouse_items": [it.to_dict() for it in self.warehouse_items],
        }


@dataclass
class FullTelemetryDTO:
    """神仙道全景综合态势传输模型

    聚合玩家资产、参战伙伴、小助手日常矩阵、背包与仓库战略储备以及各子模块错误隔离记录。

    @author Ateng
    @since 2026-10-16
    """

    assets: Optional[PlayerAssetDTO] = None
    roles: List[RoleDTO] = field(default_factory=list)
    assistant: Optional[AssistantDailyDTO] = None
    pack: Optional[PackSummaryDTO] = None
    errors: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """序列化为标准全景字典"""
        return {
            "assets": self.assets.to_dict() if self.assets else None,
            "roles": [r.to_dict() for r in self.roles],
            "assistant": self.assistant.to_dict() if self.assistant else None,
            "pack": self.pack.to_dict() if self.pack else None,
            "errors": self.errors,
        }



