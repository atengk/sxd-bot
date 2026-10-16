"""神仙道数据查询控制台看板格式化与 JSON 导出引擎

提供美化对齐的控制台 ANSI 矩阵看板渲染与标准 JSON 序列化输出。

@author Ateng
@since 2026-10-16
"""

import json
from typing import Any, Dict, List
from services.query_models import (
    PlayerAssetDTO,
    RoleDTO,
    AssistantDailyDTO,
    PackSummaryDTO,
    FullTelemetryDTO,
)




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

    @staticmethod
    def format_pack_table(dto: PackSummaryDTO) -> str:
        """格式化主背包与随身仓库盘点看板表格"""
        warn_str = "[警告: 背包空间紧张，建议变卖杂物]" if dto.is_space_low else "[空间充裕]"
        lines = [
            "=" * 72,
            "            神仙道主背包与随身仓库盘点看板 (Pack & Inventory)",
            "=" * 72,
            f"  主背包容量 : {dto.pack_used} / {dto.pack_capacity} 格 (剩余 {dto.pack_empty} 空格) {warn_str}",
            f"  随身仓库   : {dto.warehouse_used} / {dto.warehouse_capacity} 格 (剩余 {dto.warehouse_empty} 空格)",
            f"  战略总储备 : 可补充体力: +{dto.total_potential_power} 点 | 潜在经验: +{dto.total_potential_exp:,} 点",
            "-" * 72,
            "  【核心战略消耗品与礼包汇总】",
            f"   {'名称':<16} | {'数量':<8} | {'类型':<10} | {'潜在收益折算':<20}",
            "-" * 72,
        ]
        if not dto.strategic_items:
            lines.append("   (暂无核心战略消耗品或礼包)")
        else:
            for it in dto.strategic_items:
                benefits = []
                if it.potential_power > 0:
                    benefits.append(f"体力 +{it.potential_power} 点")
                if it.potential_exp > 0:
                    benefits.append(f"经验 +{it.potential_exp:,} 点")
                benefit_str = ", ".join(benefits) if benefits else "-"
                lines.append(
                    f"   {it.name:<16} | {it.count:<8} | {it.type_desc:<10} | {benefit_str:<20}"
                )
        lines.append("-" * 72)
        lines.append("  【物品大类宏观分布】")
        cat_parts = [f"{k}: {v} 件" for k, v in dto.category_counts.items()]
        cat_str = " | ".join(cat_parts) if cat_parts else "暂无物品"
        lines.append(f"   {cat_str}")
        lines.append("=" * 72)
        return "\n".join(lines)

    @staticmethod
    def format_pack_json(dto: PackSummaryDTO) -> str:
        """导出背包与随身仓库盘点数据为标准 JSON 字符串"""
        payload = {
            "status": "success",
            "type": "pack",
            "data": dto.to_dict(),
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

    @staticmethod
    def format_all_table(dto: FullTelemetryDTO) -> str:
        """格式化全景综合态势大看板表格"""
        lines = [
            "=" * 76,
            "              神仙道全景综合态势大看板 (Full Telemetry)",
            "=" * 76,
        ]

        # 1. 基础资产板块
        if dto.assets:
            lines.append("【一、角色全景资产概况】")
            lines.append(f"  角色昵称: {dto.assets.nickname or '已登录角色'} (ID: {dto.assets.player_id}) | Lv.{dto.assets.level} (VIP {dto.assets.vip_level})")
            lines.append(f"  持有财富: 铜钱 {dto.assets.coins:,} | 绑定元宝 {dto.assets.ingots:,} [受最高安全防护]")
            lines.append(f"  行动体力: {dto.assets.power} / {dto.assets.max_power} 点 | 角色声望: {dto.assets.fame:,}")
            lines.append("-" * 76)
        elif "assets" in dto.errors:
            lines.append(f"  [资产板块暂不可用: {dto.errors['assets']}]")
            lines.append("-" * 76)

        # 2. 参战伙伴阵容板块
        if dto.roles:
            lines.append("【二、参战伙伴阵容态势】")
            role_strs = []
            for r in dto.roles:
                deploy = "出战" if r.is_deployed else "待命"
                role_strs.append(f"{r.name} (Lv.{r.level}, {deploy})")
            lines.append("  阵容: " + " | ".join(role_strs))
            lines.append("-" * 76)
        elif "roles" in dto.errors:
            lines.append(f"  [伙伴板块暂不可用: {dto.errors['roles']}]")
            lines.append("-" * 76)
        else:
            lines.append("【二、参战伙伴阵容态势】")
            lines.append("  (暂无出战伙伴数据)")
            lines.append("-" * 76)

        # 3. 小助手日常矩阵与活跃度板块
        if dto.assistant:
            lines.append("【三、小助手日常进度与活跃度】")
            lines.append(f"  今日活跃度进度 : {dto.assistant.current_liveness} / {dto.assistant.max_liveness} 点")
            comp_cnt = sum(1 for it in dto.assistant.items if it.is_completed)
            lines.append(f"  日常玩法完成度 : 已达成 {comp_cnt} / {len(dto.assistant.items)} 项")
            if dto.assistant.boxes:
                box_strs = [f"第{b.box_id}档({b.required_liveness}点):[{b.status_desc}]" for b in dto.assistant.boxes]
                lines.append("  宝箱状态 : " + " | ".join(box_strs))
            lines.append("-" * 76)
        elif "assistant" in dto.errors:
            lines.append(f"  [小助手板块暂不可用: {dto.errors['assistant']}]")
            lines.append("-" * 76)

        # 4. 背包与仓库战略储备板块
        if dto.pack:
            lines.append("【四、主背包与随身仓库盘点】")
            warn_str = "[空间紧张]" if dto.pack.is_space_low else "[空间充裕]"
            lines.append(f"  主背包容量 : {dto.pack.pack_used} / {dto.pack.pack_capacity} 格 (剩余 {dto.pack.pack_empty} 空格) {warn_str}")
            lines.append(f"  随身仓库   : {dto.pack.warehouse_used} / {dto.pack.warehouse_capacity} 格 (剩余 {dto.pack.warehouse_empty} 空格)")
            lines.append(f"  战略总储备 : 可补充体力: +{dto.pack.total_potential_power} 点 | 潜在经验: +{dto.pack.total_potential_exp:,} 点")
            if dto.pack.category_counts:
                cat_str = " | ".join(f"{k}: {v}件" for k, v in dto.pack.category_counts.items())
                lines.append(f"  大类统计   : {cat_str}")
            lines.append("=" * 76)
        elif "pack" in dto.errors:
            lines.append(f"  [背包板块暂不可用: {dto.errors['pack']}]")
            lines.append("=" * 76)
        else:
            lines.append("=" * 76)

        return "\n".join(lines)

    @staticmethod
    def format_all_json(dto: FullTelemetryDTO) -> str:
        """导出全景综合态势数据为标准 JSON 字符串"""
        payload = {
            "status": "success",
            "type": "all",
            "data": dto.to_dict(),
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)



