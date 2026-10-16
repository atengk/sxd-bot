"""平台鉴权适配器包导出 (Platform Auth Package)

@author Ateng
@since 2026-10-16
"""

from network.platforms.base import BasePlatformAuthProvider
from network.platforms.fengwan import FengwanAuthProvider
from network.platforms.static import StaticAuthProvider
from network.platforms.registry import PlatformAuthRegistry

__all__ = [
    "BasePlatformAuthProvider",
    "FengwanAuthProvider",
    "StaticAuthProvider",
    "PlatformAuthRegistry",
]
