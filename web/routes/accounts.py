"""神仙道多账号在线管理与托管控制 API 路由

提供多账号 CRUD、在线托管开关、防互踢避让状态感知与一键手动恢复接口。

@author Ateng
@since 2026-10-16
"""

import logging
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from storage.config_db import ConfigDatabase, AccountRecord
from web.app import require_auth_token

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/accounts",
    tags=["Accounts"],
    dependencies=[Depends(require_auth_token)],
)


class AccountCreateReq(BaseModel):
    """账号创建请求体模型

    @author Ateng
    @since 2026-10-16
    """

    alias: str = Field(..., description="账号唯一别名")
    platform: str = Field(default="fengwanyx", description="联运平台类型")
    username: str = Field(default="", description="平台用户名")
    password: str = Field(default="", description="登录密码")
    server: str = Field(default="s813", description="游戏区服标识")
    server_id: int = Field(default=25268, description="游戏物理区服编号")
    server_host: Optional[str] = Field(default=None, description="直连网关主机")
    server_port: Optional[int] = Field(default=None, description="直连网关端口")
    enabled: bool = Field(default=True, description="是否启用自动化")
    hosting_enabled: bool = Field(default=True, description="是否开启长连接托管")


class AccountUpdateReq(BaseModel):
    """账号更新请求体模型

    @author Ateng
    @since 2026-10-16
    """

    platform: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    server: Optional[str] = None
    server_id: Optional[int] = None
    server_host: Optional[str] = None
    server_port: Optional[int] = None
    enabled: Optional[bool] = None
    hosting_enabled: Optional[bool] = None


class HostingToggleReq(BaseModel):
    """长连接托管开关请求体

    @author Ateng
    @since 2026-10-16
    """

    hosting_enabled: Optional[bool] = None


@router.get("", response_model=List[Dict[str, Any]])
async def list_accounts(request: Request) -> List[Dict[str, Any]]:
    """获取所有账号列表及其动态长连接和防互踢避让状态"""
    db: ConfigDatabase = request.app.state.db
    session_manager = request.app.state.session_manager
    accounts = db.list_accounts()

    results: List[Dict[str, Any]] = []
    for acc in accounts:
        session_info = session_manager.get_session_info(acc.alias) if session_manager else {}
        results.append(
            {
                "alias": acc.alias,
                "platform": acc.platform,
                "username": acc.username,
                "server": acc.server,
                "server_id": acc.server_id,
                "server_host": acc.server_host,
                "server_port": acc.server_port,
                "enabled": acc.enabled,
                "hosting_enabled": session_info.get("hosting_enabled", acc.hosting_enabled),
                "evade_state": session_info.get("evade_state", acc.evade_state),
                "evade_since": session_info.get("evade_since", acc.evade_since),
                "connection_status": session_info.get("connection_status", "disconnected"),
                "last_heartbeat": session_info.get("last_heartbeat", 0.0),
                "created_at": acc.created_at,
            }
        )
    return results


@router.post("", response_model=Dict[str, Any])
async def create_account(req: AccountCreateReq, request: Request) -> Dict[str, Any]:
    """创建新账号实体并持久化至 SQLite"""
    db: ConfigDatabase = request.app.state.db
    existing = db.get_account(req.alias)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"账号别名 '{req.alias}' 已存在，请使用其他别名",
        )

    record = AccountRecord(
        alias=req.alias,
        platform=req.platform,
        username=req.username,
        password=req.password,
        server=req.server,
        server_id=req.server_id,
        server_host=req.server_host,
        server_port=req.server_port,
        enabled=req.enabled,
        hosting_enabled=req.hosting_enabled,
    )

    success = db.add_account(record)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="保存账号失败",
        )

    session_manager = getattr(request.app.state, "session_manager", None)
    if session_manager and req.hosting_enabled and req.enabled:
        session_manager.start_hosting(req.alias)

    return {"success": True, "alias": req.alias}


@router.put("/{alias}", response_model=Dict[str, Any])
async def update_account(
    alias: str,
    req: AccountUpdateReq,
    request: Request,
) -> Dict[str, Any]:
    """更新指定账号的配置信息"""
    db: ConfigDatabase = request.app.state.db
    acc = db.get_account(alias)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"账号 '{alias}' 不存在",
        )

    if req.platform is not None:
        acc.platform = req.platform
    if req.username is not None:
        acc.username = req.username
    if req.password is not None and req.password != "":
        acc.password = req.password
    if req.server is not None:
        acc.server = req.server
    if req.server_id is not None:
        acc.server_id = req.server_id
    if req.server_host is not None:
        acc.server_host = req.server_host
    if req.server_port is not None:
        acc.server_port = req.server_port
    if req.enabled is not None:
        acc.enabled = req.enabled
    if req.hosting_enabled is not None:
        acc.hosting_enabled = req.hosting_enabled

    success = db.update_account(acc)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新账号失败",
        )

    return {"success": True, "alias": alias}


@router.delete("/{alias}", response_model=Dict[str, Any])
async def delete_account(alias: str, request: Request) -> Dict[str, Any]:
    """根据别名删除账号及其关联日常配置"""
    db: ConfigDatabase = request.app.state.db
    session_manager = getattr(request.app.state, "session_manager", None)
    if session_manager:
        session_manager.stop_hosting(alias)

    success = db.delete_account(alias)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"账号 '{alias}' 不存在",
        )

    return {"success": True, "alias": alias}


@router.post("/{alias}/hosting/toggle", response_model=Dict[str, Any])
async def toggle_hosting(
    alias: str,
    req: HostingToggleReq,
    request: Request,
) -> Dict[str, Any]:
    """切换指定账号的长连接托管状态"""
    db: ConfigDatabase = request.app.state.db
    session_manager = getattr(request.app.state, "session_manager", None)
    acc = db.get_account(alias)
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"账号 '{alias}' 不存在",
        )

    new_state = req.hosting_enabled if req.hosting_enabled is not None else not acc.hosting_enabled
    if session_manager:
        if new_state:
            session_manager.start_hosting(alias)
        else:
            session_manager.stop_hosting(alias)
    else:
        db.set_hosting_state(alias, new_state)

    return {"success": True, "alias": alias, "hosting_enabled": new_state}


@router.post("/{alias}/hosting/resume", response_model=Dict[str, Any])
async def resume_hosting(alias: str, request: Request) -> Dict[str, Any]:
    """玩家手动点击【打完了·恢复托管】，退出防互踢避让并重新连接"""
    session_manager = getattr(request.app.state, "session_manager", None)
    if not session_manager:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="会话管理器未就绪",
        )

    success = session_manager.resume_hosting(alias)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"账号 '{alias}' 不存在",
        )

    return {"success": True, "alias": alias, "evade_state": "none"}
