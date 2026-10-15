"""神仙道只读全局状态上下文 (Single Source of Truth)

维护当前无头会话的核心游戏状态，包含角色基础信息、财富数值、当前所在城镇等。由底层网络收包循环自动驱动更新。

@author Ateng
@since 2026-10-15
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import time


@dataclass
class PlayerState:
    """玩家角色核心状态

    @author Ateng
    @since 2026-10-15
    """

    player_id: int = 0
    nickname: str = ""
    level: int = 1
    coins: int = 0
    ingots: int = 0
    vip_level: int = 0
    logged_in: bool = False
    last_login_time: float = 0.0


@dataclass
class TownState:
    """城镇与世界场景状态

    @author Ateng
    @since 2026-10-15
    """

    town_id: int = 0
    town_name: str = ""
    pos_x: int = 0
    pos_y: int = 0


class GameContext:
    """游戏上下文状态池

    @author Ateng
    @since 2026-10-15
    """

    def __init__(self) -> None:
        self.player = PlayerState()
        self.town = TownState()
        self.extra_props: Dict[str, Any] = {}
        self._connected: bool = False
        self._connection_start_time: float = 0.0

    @property
    def is_connected(self) -> bool:
        """是否处于有效 TCP 连接状态"""
        return self._connected

    def set_connected(self, connected: bool) -> None:
        """更新网络连接活性"""
        self._connected = connected
        if connected:
            self._connection_start_time = time.time()
        else:
            self.player.logged_in = False

    def update_login_success(self, player_id: int = 0) -> None:
        """标记登录鉴权成功"""
        self.player.logged_in = True
        self.player.last_login_time = time.time()
        if player_id > 0:
            self.player.player_id = player_id

    def update_player_info(
        self,
        nickname: str,
        player_id: int,
        level: int = 0,
        coins: int = 0,
        ingots: int = 0,
    ) -> None:
        """更新玩家基础角色信息"""
        if nickname:
            self.player.nickname = nickname
        if player_id > 0:
            self.player.player_id = player_id
        if level > 0:
            self.player.level = level
        if coins > 0:
            self.player.coins = coins
        if ingots > 0:
            self.player.ingots = ingots

    def update_town(self, town_id: int, pos_x: int = 0, pos_y: int = 0) -> None:
        """更新当前所在城镇"""
        self.town.town_id = town_id
        self.town.pos_x = pos_x
        self.town.pos_y = pos_y
