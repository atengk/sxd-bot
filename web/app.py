"""神仙道 Web 控制台 FastAPI 核心接入服务

提供系统健康度探针、Token 访问门禁拦截与内嵌轻量单页静态资源托管。

@author Ateng
@since 2026-10-16
"""

import logging
import os
import time
from typing import Optional, Dict, Any

from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from storage.config_db import ConfigDatabase

logger = logging.getLogger(__name__)

security_bearer = HTTPBearer(auto_error=False)


class TokenVerifyReq(BaseModel):
    """Token 验证请求体模型

    @author Ateng
    @since 2026-10-16
    """

    token: str = ""


def get_configured_web_token(db: Optional[ConfigDatabase]) -> str:
    """获取系统当前生效的 Web 访问 Token

    优先级: 环境变量 SXD_WEB_TOKEN > SQLite tb_system_settings 中的 web_token。

    Args:
        db: 可选的 ConfigDatabase 实例。

    Returns:
        生效的 Token 字符串，若未设置则返回空字符串。
    """
    env_token = os.environ.get("SXD_WEB_TOKEN", "").strip()
    if env_token:
        return env_token
    if db is not None:
        try:
            return db.get_setting("web_token", "").strip()
        except Exception as e:
            logger.warning("从 SQLite 读取 web_token 失败: %s", e)
    return ""


def require_auth_token(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
) -> bool:
    """FastAPI 访问门禁依赖项

    当系统配置了访问 Token 时，请求必须携带有效的 Bearer Token 或 ?token= 查询参数；
    若未设置 Token，则默认免密放行。

    Args:
        request: HTTP 请求对象。
        credentials: 从 Authorization 头提取的 Bearer 凭证。

    Returns:
        验证通过返回 True。

    Raises:
        HTTPException: 401 Unauthorized 未经授权。
    """
    db: Optional[ConfigDatabase] = getattr(request.app.state, "db", None)
    expected_token = get_configured_web_token(db)
    if not expected_token:
        return True

    supplied_token = ""
    if credentials and credentials.credentials:
        supplied_token = credentials.credentials.strip()
    elif "token" in request.query_params:
        supplied_token = request.query_params["token"].strip()

    if supplied_token == expected_token:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="未授权访问: 缺少有效 Web 访问口令",
        headers={"WWW-Authenticate": "Bearer"},
    )


def create_app(
    db: Optional[ConfigDatabase] = None,
    static_dir: Optional[str] = None,
    routers: Optional[list] = None,
    session_manager: Optional[Any] = None,
) -> FastAPI:
    """构造并初始化 FastAPI 应用实例

    Args:
        db: SQLite 配置仓储实例（若为 None 则默认初始化 data/config.sqlite）。
        static_dir: 静态资源目录路径（若为 None 则默认读取 web/static）。
        routers: 待注册的外部 APIRouter 列表。
        session_manager: 可选的长连接会话管理器实例。

    Returns:
        已挂载路由与静态资源的 FastAPI 应用对象。
    """
    from web.session_manager import AccountSessionManager
    from web.routes.accounts import router as accounts_router
    from web.routes.routines import router as routines_router
    from web.routes.events import router as events_router
    from web.routes.telemetry import router as telemetry_router
    from web.logging_bridge import attach_log_bridge

    app = FastAPI(
        title="神仙道无头协议自动化控制台",
        description="现代化神仙道自动化 Web 管理后台与多账号调度 API",
        version="1.1.1",
    )

    app.state.start_time = time.time()
    app.state.db = db if db is not None else ConfigDatabase()
    app.state.session_manager = (
        session_manager
        if session_manager is not None
        else AccountSessionManager(db=app.state.db)
    )

    # 挂载受管日志桥接器至当前 session_manager 的 event_bus (防范日志风暴，限定业务日志器)
    if hasattr(app.state.session_manager, "event_bus"):
        app.state.log_bridge = attach_log_bridge(
            app.state.session_manager.event_bus,
            logger_name="sxd_bot",
        )

    # 启动钩子：服务启动自动拉起全量启用账号的长连接常驻自愈守护
    @app.on_event("startup")
    async def on_startup() -> None:
        sm = getattr(app.state, "session_manager", None)
        if sm and hasattr(sm, "start_all_hosting"):
            sm.start_all_hosting()

    # 1. 注册健康检查探针 (无需鉴权)
    @app.get("/api/health", tags=["System"])
    async def health_check() -> Dict[str, Any]:
        """服务健康检查接口"""
        accounts = app.state.db.list_accounts() if app.state.db else []
        uptime = time.time() - app.state.start_time
        return {
            "status": "ok",
            "uptime_sec": round(uptime, 2),
            "accounts_count": len(accounts),
        }

    # 2. 注册口令验证接口
    @app.post("/api/auth/verify", tags=["Auth"])
    async def verify_token(req: TokenVerifyReq) -> Dict[str, Any]:
        """验证客户端传入的口令是否合法"""
        expected_token = get_configured_web_token(app.state.db)
        if not expected_token:
            return {"valid": True, "token_required": False}

        if req.token.strip() == expected_token:
            return {"valid": True, "token_required": True}

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="口令错误，请重新输入",
        )

    # 3. 注册多账号管理业务路由器
    app.include_router(accounts_router)

    # 4. 注册 35 项日常任务配置与流水线触发路由器
    app.include_router(routines_router)

    # 5. 注册 SSE 实时事件与日志推送路由器
    app.include_router(events_router)

    # 6. 注册全景遥测、100格背包快照与元宝审计路由器
    app.include_router(telemetry_router)

    # 4. 注册额外外部业务路由器
    if routers:
        for r in routers:
            app.include_router(r)

    # 5. 挂载内嵌单页静态资源 (必须位于所有 API 路由注册之后)
    target_static = static_dir or os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(target_static):
        app.mount("/", StaticFiles(directory=target_static, html=True), name="static")
    else:
        logger.warning("未找到静态资源目录: %s，根路径将无法托管静态单页", target_static)

    return app


