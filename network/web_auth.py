"""神仙道 Web 自动化登录与网关凭据提取模块

实现完整的 3 步全自动 Web 登录流程：
1. 请求 member 站点 login.php 完成账号鉴权，获取 Session 与 Cookie。
2. 请求 play.php 获取区服入场参数集 (regdate, pi, hash, time, non_kid 等)。
3. 请求目标区服 index_wd.php 换取最新的动态网关 IP、Port 与长连接 Token Hash。

@author Ateng
@since 2026-10-15
"""

import http.cookiejar
import json
import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any
import urllib.request
import urllib.parse
from json import JSONDecoder

logger = logging.getLogger(__name__)


@dataclass
class GatewayCredentials:
    """网关鉴权与连接凭据模型

    @author Ateng
    @since 2026-10-15
    """

    server_host: str
    server_port: int
    player_name: str
    hash_code: str
    time: str
    platform: str
    server_id: int
    nickname: str = ""


class WebAuthFetcher:
    """Web 自动化鉴权调度器

    @author Ateng
    @since 2026-10-15
    """

    @classmethod
    def auto_login(
        cls,
        username: str,
        password: str,
        server: str = "s813",
        app: str = "sxd",
        timeout_sec: float = 10.0,
        platform: str = "fengwanyx",
    ) -> Optional[GatewayCredentials]:
        """全自动执行指定平台的账号登录与网关令牌换取

        Args:
            username: 平台账号用户名。
            password: 账号密码。
            server: 目标游戏区服代号 (例如 's813')。
            app: 游戏标识 (默认为 'sxd')。
            timeout_sec: 各步骤网络超时秒数。
            platform: 渠道平台标识 (如 'fengwanyx', 'xd', '360')。

        Returns:
            若全流程成功返回包含最新 Token 的 GatewayCredentials，否则返回 None。
        """
        from core.config import AccountConfig
        from network.platforms.registry import PlatformAuthRegistry

        acc = AccountConfig(
            alias=username,
            username=username,
            password=password,
            server=server,
            platform=platform,
        )
        provider = PlatformAuthRegistry.get(platform)
        return provider.auto_login(acc, timeout_sec=timeout_sec)

    @staticmethod
    def resolve_credentials(account: Any) -> Optional[GatewayCredentials]:
        """根据 AccountConfig 自动解析网关凭据 (动态派发至平台 Provider，失败时回退静态网关)"""
        from core.config import AccountConfig
        from network.platforms.registry import PlatformAuthRegistry

        if not isinstance(account, AccountConfig):
            account = AccountConfig(
                alias=str(account.get("alias", "") if isinstance(account, dict) else ""),
                username=str(account.get("username", "") if isinstance(account, dict) else ""),
                password=str(account.get("password", "") if isinstance(account, dict) else ""),
                server=str(account.get("server", "s813") if isinstance(account, dict) else "s813"),
                platform=str(account.get("platform", "fengwanyx") if isinstance(account, dict) else "fengwanyx"),
                server_host=account.get("server_host") if isinstance(account, dict) else None,
                server_port=account.get("server_port") if isinstance(account, dict) else None,
                server_id=int(account.get("server_id", 25268)) if isinstance(account, dict) else 25268,
                hash_code=str(account.get("hash_code", "") if isinstance(account, dict) else ""),
                time=str(account.get("time", "") if isinstance(account, dict) else ""),
            )

        # 1. 若具备用户名与密码，通过注册表调用对应平台的 Provider 自动登录
        if account.username and account.password:
            logger.info("采用平台 [%s] 自动化登录流程换取新鲜令牌 (用户: %s, 区服: %s)...", account.platform, account.username, account.server)
            creds = WebAuthFetcher.auto_login(
                username=account.username,
                password=account.password,
                server=account.server,
                platform=account.platform,
            )
            if creds:
                return creds
            logger.warning("平台 [%s] 全自动登录失败，检查是否有静态网关配置兜底...", account.platform)

        # 2. 静态直连网关兜底 (适用于未逆向自动登录的平台或纯静态直连)
        if account.server_host and account.server_port:
            logger.info("采用静态网关直连配置: %s:%d (平台: %s)", account.server_host, int(account.server_port), account.platform)
            return GatewayCredentials(
                server_host=account.server_host,
                server_port=int(account.server_port),
                player_name=account.username,
                hash_code=str(account.hash_code),
                time=str(account.time),
                platform=account.platform,
                server_id=int(account.server_id),
                nickname=account.alias or account.username,
            )

        return None

    @staticmethod
    def from_config_dict(conf: Dict[str, Any]) -> GatewayCredentials:
        """从本地配置字典中装载凭据 (静态备用模式)"""
        static_c = conf.get("static_credentials", {})
        return GatewayCredentials(
            server_host=static_c.get("server_host", "9x656.sxdweb.xd.com"),
            server_port=int(static_c.get("server_port", 8381)),
            player_name=static_c.get("player_name", ""),
            hash_code=static_c.get("hash_code", ""),
            time=str(static_c.get("time", "")),
            platform=static_c.get("platform", "fengwanyx"),
            server_id=int(static_c.get("server_id", 25268)),
            nickname=static_c.get("nickname", ""),
        )

