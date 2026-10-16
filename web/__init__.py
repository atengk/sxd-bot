"""神仙道 Web 控制台与 HTTP/SSE 管理服务

包含 FastAPI 接入层、常驻连接池状态机、Token 门禁与内嵌轻量单页静态资源。

@author Ateng
@since 2026-10-16
"""

from web.app import create_app

__all__ = ["create_app"]
