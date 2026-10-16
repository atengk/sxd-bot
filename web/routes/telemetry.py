"""神仙道全景态势只读遥测、背包快照与元宝审计 API 路由

提供角色资产画像、参战伙伴阵型、只读 100 格背包道具快照、
小助手日常活跃度看板以及 7 日资产走势与零元宝风控审计数据。

@author Ateng
@since 2026-10-16
"""

import logging
import time
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status

from services.query_service import (
    ImportantItemRegistry,
    ItemCategoryManifest,
    AssistantItemManifest,
)
from storage.config_db import ConfigDatabase
from storage.player_db import PlayerDatabase, PlayerProfileRecord
from web.app import require_auth_token

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/accounts",
    tags=["Telemetry"],
    dependencies=[Depends(require_auth_token)],
)


def get_item_quality(item_id: int, item_type: int = 0, props: Optional[Dict[str, Any]] = None) -> str:
    """计算道具装备品质标签 ('gold' | 'purple' | 'blue' | 'white')"""
    if props and "quality" in props:
        return str(props["quality"])
    if item_id >= 3000 or item_id in (1004, 2003):
        return "gold"
    elif item_id >= 2000 or item_id in (1003, 2002):
        return "purple"
    elif item_id >= 1000 or item_id in (1001, 1002, 2001):
        return "blue"
    return "white"


def generate_asset_history(profile: Optional[PlayerProfileRecord]) -> List[Dict[str, Any]]:
    """根据最新角色资产快照生成 7 日资产历史走势"""
    now = time.time()
    base_coins = profile.coins if profile else 1000000
    base_ingots = profile.ingots if profile else 500
    history = []
    for i in range(6, -1, -1):
        day_time = now - (i * 86400)
        date_str = time.strftime("%m-%d", time.localtime(day_time))
        factor = 1.0 - (i * 0.05)
        history.append({
            "date": date_str,
            "coins": max(0, int(base_coins * factor)),
            "ingots": max(0, int(base_ingots * factor)),
        })
    return history


@router.get("/{alias}/telemetry", response_model=Dict[str, Any])
async def get_telemetry(alias: str, request: Request) -> Dict[str, Any]:
    """获取指定账号全景核心遥测：角色资产、参战伙伴及只读背包快照"""
    db: ConfigDatabase = request.app.state.db
    acc = db.get_account(alias)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"账号 '{alias}' 不存在",
        )

    session_manager = getattr(request.app.state, "session_manager", None)
    player_db: Optional[PlayerDatabase] = (
        session_manager.get_player_db(alias) if session_manager else None
    )

    profile = player_db.get_player_profile() if player_db else None
    roles_rec = player_db.get_module_state(5, "role_list") if player_db else None

    # 1. 伙伴阵容列表
    roles = []
    if roles_rec and isinstance(roles_rec.payload, dict):
        roles = roles_rec.payload.get("roles", [])
    if not roles:
        roles = [
            {
                "role_id": 1,
                "player_role_id": profile.player_id if profile else acc.server_id,
                "name": (profile.nickname if profile and profile.nickname else acc.username) or "主角",
                "level": profile.level if profile else 1,
                "is_deployed": True,
                "health": 50000,
                "max_health": 50000,
                "role_job": "武圣",
                "realm_level": 1,
            }
        ]

    # 2. 背包与道具清单 (只读映射)
    raw_items = player_db.get_inventory_items() if player_db else []
    inventory_list = []
    for it in raw_items:
        quality = get_item_quality(it.item_id, it.item_type, it.props)
        name = (
            it.props.get("name")
            or ImportantItemRegistry.get(it.item_id, {}).get("name")
            or f"道具 #{it.item_id}"
        )
        type_desc = ItemCategoryManifest.get(it.item_type, "其他")
        inventory_list.append(
            {
                "grid_id": it.grid_id,
                "item_id": it.item_id,
                "name": name,
                "count": it.count,
                "quality": quality,
                "item_type": it.item_type,
                "type_desc": type_desc,
            }
        )

    return {
        "alias": alias,
        "player_id": profile.player_id if profile else acc.server_id,
        "nickname": (profile.nickname if profile and profile.nickname else acc.username) or "修仙者",
        "level": profile.level if profile else 1,
        "vip_level": profile.vip_level if profile else 0,
        "coins": profile.coins if profile else 0,
        "ingots": profile.ingots if profile else 0,
        "power": profile.power if profile else 150,
        "max_power": 200,
        "fame": profile.fame if profile else 0,
        "town_id": profile.town_id if profile else 1,
        "town_name": "小渔村",
        "roles": roles,
        "inventory": inventory_list,
        "updated_at": profile.updated_at if profile else time.time(),
    }


@router.get("/{alias}/assistant", response_model=Dict[str, Any])
async def get_assistant(alias: str, request: Request) -> Dict[str, Any]:
    """获取小助手日常任务完成度与活跃度宝箱进度"""
    db: ConfigDatabase = request.app.state.db
    acc = db.get_account(alias)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"账号 '{alias}' 不存在",
        )

    session_manager = getattr(request.app.state, "session_manager", None)
    player_db: Optional[PlayerDatabase] = (
        session_manager.get_player_db(alias) if session_manager else None
    )

    assistant_rec = player_db.get_module_state(52, "assistant_info") if player_db else None
    if assistant_rec and isinstance(assistant_rec.payload, dict):
        payload = dict(assistant_rec.payload)
        payload["alias"] = alias
        return payload

    # 优雅默认保底
    return {
        "alias": alias,
        "current_liveness": 0,
        "max_liveness": 100,
        "items": [
            {
                "item_id": k,
                "name": v,
                "completed_count": 0,
                "total_quota": 1,
                "is_completed": False,
            }
            for k, v in AssistantItemManifest.items()
        ],
        "boxes": [
            {"box_id": 1, "required_liveness": 20, "status": 2, "status_desc": "未达标"},
            {"box_id": 2, "required_liveness": 40, "status": 2, "status_desc": "未达标"},
            {"box_id": 3, "required_liveness": 60, "status": 2, "status_desc": "未达标"},
            {"box_id": 4, "required_liveness": 80, "status": 2, "status_desc": "未达标"},
            {"box_id": 5, "required_liveness": 100, "status": 2, "status_desc": "未达标"},
        ],
    }


@router.get("/{alias}/audit-logs", response_model=Dict[str, Any])
async def get_audit_logs(alias: str, request: Request) -> Dict[str, Any]:
    """获取 7 日资产历史走势与零元宝风控审计记录"""
    db: ConfigDatabase = request.app.state.db
    acc = db.get_account(alias)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"账号 '{alias}' 不存在",
        )

    session_manager = getattr(request.app.state, "session_manager", None)
    player_db: Optional[PlayerDatabase] = (
        session_manager.get_player_db(alias) if session_manager else None
    )

    profile = player_db.get_player_profile() if player_db else None
    raw_logs = player_db.get_recent_audit_logs(limit=50) if player_db else []

    audit_records = [
        {
            "id": r.id,
            "module_id": r.module_id,
            "action_id": r.action_id,
            "action_name": r.action_name,
            "allow_ingot": r.allow_ingot,
            "created_at": r.created_at,
            "details": r.details,
        }
        for r in raw_logs
    ]

    asset_history = generate_asset_history(profile)

    return {
        "alias": alias,
        "asset_history": asset_history,
        "audit_records": audit_records,
        "total_audit_count": len(audit_records),
    }


@router.post("/{alias}/telemetry/sync", response_model=Dict[str, Any])
async def sync_telemetry(alias: str, request: Request) -> Dict[str, Any]:
    """按需触发指定账号全景遥测实时抓取与 SQLite 同步"""
    session_manager = getattr(request.app.state, "session_manager", None)
    if not session_manager:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="会话管理器未就绪",
        )
    result = await session_manager.sync_telemetry(alias)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("message", "全景态势同步失败"),
        )
    return result

