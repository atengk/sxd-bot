"""静态直连与通用兜底鉴权适配器 (Static & Direct Auth Provider)

用于心动官服及其他尚未逆向全自动登录的第三方平台，通过用户抓包提供的静态网关直连。

@author Ateng
@since 2026-10-16
"""

import logging
from typing import Optional, TYPE_CHECKING

from network.platforms.base import BasePlatformAuthProvider

if TYPE_CHECKING:
    from core.config import AccountConfig
    from network.web_auth import GatewayCredentials

logger = logging.getLogger("static_auth")


class StaticAuthProvider(BasePlatformAuthProvider):
    """静态直连鉴权适配器 (通用兜底)"""

    @property
    def platform_name(self) -> str:
        return "static"

    def auto_login(self, account: "AccountConfig", timeout_sec: float = 10.0) -> Optional["GatewayCredentials"]:
        """根据配置中的静态网关信息组装凭据"""
        from network.web_auth import GatewayCredentials

        if account.server_host and account.server_port:
            logger.info("[%s] 采用静态网关直连配置: %s:%d (平台: %s)", account.display_name, account.server_host, int(account.server_port), account.platform)
            return GatewayCredentials(
                server_host=account.server_host,
                server_port=int(account.server_port),
                player_name=account.username,
                hash_code=account.hash_code,
                time=account.time,
                platform=account.platform,
                server_id=account.server_id,
                nickname=account.alias or account.username,
            )

        logger.warning("[%s] 静态平台鉴权模式要求配置 server_host 与 server_port，当前账号未提供", account.display_name)
        return None
