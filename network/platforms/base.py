"""多平台鉴权提供方抽象基类 (Base Platform Auth Provider)

定义各联运渠道平台转换为统一底层 Socket 网关凭据的核心契约。

@author Ateng
@since 2026-10-16
"""

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from core.config import AccountConfig
    from network.web_auth import GatewayCredentials


class BasePlatformAuthProvider(ABC):
    """平台鉴权适配器抽象基类

    负责将各平台私有的用户鉴权与选区逻辑，转换为心动底层标准的 Socket 网关凭据。
    """

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """获取当前适配器对应的平台主标识符 (如 'fengwanyx', 'xd', 'static')"""
        pass

    @abstractmethod
    def auto_login(self, account: "AccountConfig", timeout_sec: float = 10.0) -> Optional["GatewayCredentials"]:
        """执行平台全自动登录并换取新鲜的 Socket 网关凭据

        Args:
            account: 账号配置实体 (包含 username, password, server 等)。
            timeout_sec: 网络请求超时时间 (秒)。

        Returns:
            若全流程认证成功返回包含最新会话令牌的 GatewayCredentials，否则返回 None。
        """
        pass
