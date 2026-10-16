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
) -> FastAPI:
    """构造并初始化 FastAPI 应用实例

    Args:
        db: SQLite 配置仓储实例（若为 None 则默认初始化 data/config.sqlite）。
        static_dir: 静态资源目录路径（若为 None 则默认读取 web/static）。
        routers: 待注册的 APIRouter 列表（在挂载根路径静态资源前完成注册）。

    Returns:
        已挂载路由与静态资源的 FastAPI 应用对象。
    """
    app = FastAPI(
        title="神仙道无头协议自动化控制台",
        description="现代化神仙道自动化 Web 管理后台与多账号调度 API",
        version="1.0.0",
    )

    app.state.start_time = time.time()
    app.state.db = db if db is not None else ConfigDatabase()

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

    # 3. 注册外部业务路由器
    if routers:
        for r in routers:
            app.include_router(r)

    # 4. 挂载内嵌单页静态资源 (必须位于所有 API 路由注册之后)
    target_static = static_dir or os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(target_static):
        app.mount("/", StaticFiles(directory=target_static, html=True), name="static")
    else:
        logger.warning("未找到静态资源目录: %s，根路径将无法托管静态单页", target_static)

    return app

