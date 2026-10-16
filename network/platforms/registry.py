"""平台鉴权适配器注册中心 (Platform Auth Registry)

负责管理各联运渠道平台的 Provider 实例，提供根据 platform 标识符动态派发鉴权。

@author Ateng
@since 2026-10-16
"""

import logging
from typing import Dict, Type, Optional

from network.platforms.base import BasePlatformAuthProvider
from network.platforms.fengwan import FengwanAuthProvider
from network.platforms.static import StaticAuthProvider
from network.platforms.xd import XDPlatformAuthProvider

logger = logging.getLogger("platform_registry")


class PlatformAuthRegistry:
    """平台鉴权适配器注册与分发中心"""

    _registry: Dict[str, BasePlatformAuthProvider] = {}
    _aliases: Dict[str, str] = {
        "fengwan": "fengwanyx",
        "fw": "fengwanyx",
        "direct": "static",
        "default": "fengwanyx",
        "xindong": "xd",
        "guanfu": "xd",
        "gf": "xd",
    }

    @classmethod
    def register(cls, provider: BasePlatformAuthProvider) -> None:
        """注册一个新的平台鉴权提供方"""
        cls._registry[provider.platform_name.lower()] = provider
        logger.debug("已注册平台鉴权适配器: %s", provider.platform_name)

    @classmethod
    def get(cls, platform: Optional[str]) -> BasePlatformAuthProvider:
        """获取指定平台的鉴权提供方 (未匹配时优雅回退至静态/疯玩)"""
        if not cls._registry:
            cls._init_defaults()

        plat_key = (platform or "fengwanyx").strip().lower()
        # 别名规范化
        canonical_key = cls._aliases.get(plat_key, plat_key)

        provider = cls._registry.get(canonical_key)
        if provider:
            return provider

        logger.warning("未找到平台 '%s' 的专用 Web 自动登录适配器，自动回退至静态直连模式", platform)
        return cls._registry.get("static", StaticAuthProvider())

    @classmethod
    def _init_defaults(cls) -> None:
        """初始化内置默认平台"""
        cls.register(FengwanAuthProvider())
        cls.register(StaticAuthProvider())
        cls.register(XDPlatformAuthProvider())


# 模块装载时自动初始化
PlatformAuthRegistry._init_defaults()
