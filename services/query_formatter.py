"""神仙道数据查询控制台看板格式化与 JSON 导出引擎

提供美化对齐的控制台 ANSI 矩阵看板渲染与标准 JSON 序列化输出。

@author Ateng
@since 2026-10-16
"""

import json
from typing import Any, Dict
from services.query_models import PlayerAssetDTO


class QueryFormatter:
    """查询看板格式化引擎

    @author Ateng
    @since 2026-10-16
    """

    @staticmethod
    def format_assets_table(dto: PlayerAssetDTO) -> str:
        """格式化玩家基础资产看板表格"""
        lines = [
            "=" * 64,
            "            神仙道角色全景资产看板 (Player Assets)",
            "=" * 64,
            f"  角色昵称 : {dto.nickname or '已登录角色'} (ID: {dto.player_id})",
            f"  角色等级 : Lv.{dto.level} (VIP {dto.vip_level})",
            f"  当前所在 : 城镇 ID #{dto.town_id}" + (f" ({dto.town_name})" if dto.town_name else ""),
            f"  最高关卡 : 副本 Mission Key #{dto.mission_key}",
            "-" * 64,
            f"  持有铜钱 : {dto.coins:,} 铜钱",
            f"  绑定元宝 : {dto.ingots:,} 元宝 [受最高安全防护]",
            f"  行动体力 : {dto.power} / {dto.max_power} 点",
            f"  角色声望 : {dto.fame:,} 声望",
            f"  经验数值 : {dto.experience:,} / {dto.max_experience:,}",
            "=" * 64,
        ]
        return "\n".join(lines)

    @staticmethod
    def format_assets_json(dto: PlayerAssetDTO) -> str:
        """导出为格式化 JSON 字符串"""
        payload = {
            "status": "success",
            "type": "assets",
            "data": dto.to_dict(),
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)
