"""神仙道数据查询控制台看板格式化与 JSON 导出引擎

提供美化对齐的控制台 ANSI 矩阵看板渲染与标准 JSON 序列化输出。

@author Ateng
@since 2026-10-16
"""

import json
from typing import Any, Dict, List
from services.query_models import PlayerAssetDTO, RoleDTO, AssistantDailyDTO


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

    @staticmethod
    def format_roles_table(roles: List[RoleDTO]) -> str:
        """格式化参战伙伴阵容看板表格"""
        lines = [
            "=" * 72,
            "              神仙道参战伙伴阵容看板 (Battle Roles)",
            "=" * 72,
            f" {'ID':<4} | {'伙伴名称':<12} | {'等级':<6} | {'参战状态':<10} | {'生命值 / 上限':<20}",
            "-" * 72,
        ]
        if not roles:
            lines.append("  (暂无出战伙伴数据)")
        else:
            for r in roles:
                deploy_str = "主力出战" if r.is_deployed else "备战待命"
                hp_str = f"{r.health:,} / {r.max_health:,}" if r.max_health > 0 else "-"
                lines.append(
                    f" {r.role_id:<4} | {r.name:<12} | Lv.{r.level:<3} | {deploy_str:<10} | {hp_str:<20}"
                )
        lines.append("=" * 72)
        lines.append(f"  阵容统计 : 共有 {len(roles)} 位伙伴出战/待命")
        return "\n".join(lines)

    @staticmethod
    def format_roles_json(roles: List[RoleDTO]) -> str:
        """导出伙伴阵容为标准 JSON 字符串"""
        payload = {
            "status": "success",
            "type": "roles",
            "total": len(roles),
            "data": [r.to_dict() for r in roles],
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

    @staticmethod
    def format_assistant_table(dto: AssistantDailyDTO) -> str:
        """格式化小助手今日日常进度与活跃度看板表格"""
        lines = [
            "=" * 72,
            "            小助手今日日常进度与活跃度看板 (Daily Assistant)",
            "=" * 72,
            f"  今日活跃度进度 : {dto.current_liveness} / {dto.max_liveness} 点",
            "-" * 72,
            f" {'ID':<4} | {'玩法名称':<16} | {'完成进度':<12} | {'状态':<10}",
            "-" * 72,
        ]
        if not dto.items:
            lines.append("  (暂无日常玩法数据)")
        else:
            for item in dto.items:
                status_str = "已达成" if item.is_completed else "未达成"
                progress_str = f"{item.completed_count} / {item.total_quota}"
                lines.append(
                    f" {item.item_id:<4} | {item.name:<16} | {progress_str:<12} | {status_str:<10}"
                )
        lines.append("-" * 72)
        lines.append("  今日活跃度宝箱进度:")
        if not dto.boxes:
            lines.append("    (暂无宝箱档位数据)")
        else:
            for box in dto.boxes:
                lines.append(f"    第 {box.box_id} 档 ({box.required_liveness}点): [{box.status_desc}]")
        lines.append("=" * 72)
        return "\n".join(lines)

    @staticmethod
    def format_assistant_json(dto: AssistantDailyDTO) -> str:
        """导出小助手日常态势为标准 JSON 字符串"""
        payload = {
            "status": "success",
            "type": "assistant",
            "data": dto.to_dict(),
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

