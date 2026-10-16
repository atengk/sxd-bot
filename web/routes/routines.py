"""神仙道 35 项日常任务配置与流水线触发 API 路由

提供账号级独立日常子任务开关查询与持久化修改，
以及异步任务调度引擎手工触发与进度广播。

@author Ateng
@since 2026-10-16
"""

import logging
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from storage.config_db import ConfigDatabase, RoutineConfigRecord, ALL_ROUTINES
from web.app import require_auth_token

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/accounts",
    tags=["Routines"],
    dependencies=[Depends(require_auth_token)],
)


class RoutineConfigUpdateReq(BaseModel):
    """日常任务开关与元宝安全阈值更新请求

    @author Ateng
    @since 2026-10-16
    """

    allowed_ingots: Optional[int] = Field(default=0, ge=0, description="允许消耗的元宝上限")
    enabled_routines: List[str] = Field(default_factory=list, description="启用的日常子任务名称列表")


class RoutineTriggerReq(BaseModel):
    """日常流水线触发请求参数

    @author Ateng
    @since 2026-10-16
    """

    specific_task: Optional[str] = Field(default=None, description="指定单独执行的子任务标识")
    force: bool = Field(default=False, description="是否强制执行（绕过避让状态）")


@router.get("/{alias}/routine-config", response_model=Dict[str, Any])
async def get_routine_config(alias: str, request: Request) -> Dict[str, Any]:
    """获取指定账号的 35 项日常子任务开关及元宝配置"""
    db: ConfigDatabase = request.app.state.db
    acc = db.get_account(alias)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"账号 '{alias}' 不存在",
        )

    cfg = db.get_routine_config(alias)
    return {
        "alias": cfg.alias,
        "allowed_ingots": cfg.allowed_ingots,
        "enabled_routines": cfg.enabled_routines,
        "all_routines": list(ALL_ROUTINES),
        "updated_at": cfg.updated_at,
    }


@router.put("/{alias}/routine-config", response_model=Dict[str, Any])
async def update_routine_config(
    alias: str,
    req: RoutineConfigUpdateReq,
    request: Request,
) -> Dict[str, Any]:
    """更新指定账号的 35 项日常子任务开关及元宝安全红线"""
    db: ConfigDatabase = request.app.state.db
    acc = db.get_account(alias)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"账号 '{alias}' 不存在",
        )

    record = RoutineConfigRecord(
        alias=alias,
        allowed_ingots=req.allowed_ingots if req.allowed_ingots is not None else 0,
        enabled_routines=req.enabled_routines,
    )

    success = db.save_routine_config(record)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="保存日常任务配置失败",
        )

    return {
        "success": True,
        "alias": alias,
        "allowed_ingots": record.allowed_ingots,
        "enabled_count": len(record.enabled_routines),
        "updated_at": record.updated_at,
    }


@router.post("/{alias}/routine/trigger", response_model=Dict[str, Any])
async def trigger_routine(
    alias: str,
    request: Request,
    req: Optional[RoutineTriggerReq] = None,
) -> Dict[str, Any]:
    """手工异步触发指定账号的自动化日常流水线"""
    db: ConfigDatabase = request.app.state.db
    acc = db.get_account(alias)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"账号 '{alias}' 不存在",
        )

    session_manager = getattr(request.app.state, "session_manager", None)
    if not session_manager:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="会话管理器未就绪",
        )

    specific_task = req.specific_task if req else None
    force = req.force if req else False

    result = session_manager.trigger_routine(
        alias=alias,
        specific_task=specific_task,
        force=force,
    )
    return result
