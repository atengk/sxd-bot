"""神仙道无头协议自动化 CLI 与中央服务代理模块

提供 CLI 命令行交互、Central Daemon Proxy 代理派发与 FastAPI Web 常驻服务拉起。

@author Ateng
@since 2026-10-16
"""

from cli.daemon_proxy import DaemonProxy

__all__ = ["DaemonProxy"]
