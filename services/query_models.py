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
