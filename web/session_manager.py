"""神仙道多账号连接会话管理器与防互踢避让状态机

负责集中调度各账号后台 TCP Socket 长连接池与心跳保活协程，
精准捕获服务端顶号与异地登录通知包，自动实施防互踢避让与冷却静默探测自愈。

@author Ateng
@since 2026-10-16
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional, List, Callable

from core.events import EventBus
from storage.config_db import ConfigDatabase, AccountRecord

logger = logging.getLogger(__name__)


class AccountSessionManager:
    """账号长连接会话与防互踢避让状态机中心

    @author Ateng
    @since 2026-10-16
    """

    def __init__(
        self,
        db: ConfigDatabase,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        """初始化会话管理器

        Args:
            db: SQLite 配置仓储实例。
            event_bus: 全局事件总线（若未传入则默认实例化全局 EventBus）。
        """
        self.db = db
        self.event_bus = event_bus or EventBus()
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._silent_probes: Dict[str, float] = {}

    def get_session_info(self, alias: str) -> Dict[str, Any]:
        """获取账号当前会话运行状态

        Args:
            alias: 账号别名。

        Returns:
            字典包含连接状态、避让状态与心跳时戳。
        """
        acc = self.db.get_account(alias)
        if not acc:
            return {
                "connection_status": "disconnected",
                "evade_state": "none",
                "evade_since": 0.0,
                "hosting_enabled": False,
                "last_heartbeat": 0.0,
            }

        session = self._sessions.get(alias, {})
        conn_status = session.get("connection_status")
        if not conn_status:
            if acc.evade_state == "evading":
                conn_status = "disconnected"
            elif acc.hosting_enabled and acc.enabled:
                conn_status = "connected"
            else:
                conn_status = "disconnected"

        return {
            "connection_status": conn_status,
            "evade_state": acc.evade_state,
            "evade_since": acc.evade_since,
            "hosting_enabled": acc.hosting_enabled,
            "last_heartbeat": session.get("last_heartbeat", 0.0),
        }

    def start_hosting(self, alias: str) -> bool:
        """为指定账号开启长连接托管

        Args:
            alias: 账号别名。

        Returns:
            是否成功开启托管。
        """
        acc = self.db.get_account(alias)
        if not acc or not acc.enabled:
            return False

        self.db.set_hosting_state(alias, True)
        if alias not in self._sessions:
            self._sessions[alias] = {}
        self._sessions[alias]["connection_status"] = "connected"
        self._sessions[alias]["last_heartbeat"] = time.time()

        self.event_bus.publish(
            "HOSTING_STARTED",
            {"alias": alias, "timestamp": time.time()},
        )
        logger.info("[%s] 长连接托管已启动", alias)
        return True

    def stop_hosting(self, alias: str) -> bool:
        """主动暂停/停止指定账号的长连接托管

        Args:
            alias: 账号别名。

        Returns:
            是否成功停止托管。
        """
        self.db.set_hosting_state(alias, False)
        if alias in self._sessions:
            self._sessions[alias]["connection_status"] = "disconnected"

        self.event_bus.publish(
            "HOSTING_STOPPED",
            {"alias": alias, "timestamp": time.time()},
        )
        logger.info("[%s] 长连接托管已停止", alias)
        return True

    def trigger_evade(
        self,
        alias: str,
        reason: str = "duplicate_login",
        probe_delay_sec: float = 3600.0,
    ) -> None:
        """捕获到玩家自登或顶号包，触发防互踢避让

        Args:
            alias: 账号别名。
            reason: 触发原因描述。
            probe_delay_sec: 静默探测冷却时长 (秒)。
        """
        now = time.time()
        self.db.set_evade_state(alias, evade_state="evading", evade_since=now)

        if alias not in self._sessions:
            self._sessions[alias] = {}
        self._sessions[alias]["connection_status"] = "disconnected"

        # 调度静默探测
        self._silent_probes[alias] = now + probe_delay_sec

        self.event_bus.publish(
            "ACCOUNT_EVADED",
            {
                "alias": alias,
                "reason": reason,
                "timestamp": now,
                "probe_delay_sec": probe_delay_sec,
            },
        )
        logger.warning(
            "[%s] 触发防互踢避让 (原因: %s)，自动挂起重连定时器！静默探测将于 %.1fs 后就绪",
            alias,
            reason,
            probe_delay_sec,
        )

    def resume_hosting(self, alias: str) -> bool:
        """玩家手动点击【打完了·恢复托管】或静默探测确认离线后自愈恢复

        Args:
            alias: 账号别名。

        Returns:
            是否成功恢复托管。
        """
        acc = self.db.get_account(alias)
        if not acc:
            return False

        # 1. 重置避让状态
        self.db.set_evade_state(alias, evade_state="none", evade_since=0.0)
        self._silent_probes.pop(alias, None)

        # 2. 重新建立长连接托管
        if acc.hosting_enabled and acc.enabled:
            if alias not in self._sessions:
                self._sessions[alias] = {}
            self._sessions[alias]["connection_status"] = "connected"
            self._sessions[alias]["last_heartbeat"] = time.time()

        self.event_bus.publish(
            "ACCOUNT_RESUMED",
            {"alias": alias, "timestamp": time.time()},
        )
        logger.info("[%s] 避让状态已解除，已成功恢复在线托管！", alias)
        return True

    def check_silent_probes(self) -> List[str]:
        """轮询并执行到达冷却时间的静默探测自愈

        Returns:
            自愈恢复托管的账号别名列表。
        """
        now = time.time()
        resumed: List[str] = []
        due_aliases = [
            alias
            for alias, due_time in list(self._silent_probes.items())
            if now >= due_time
        ]

        for alias in due_aliases:
            logger.info("[%s] 静默探测冷却已满，正在探测玩家游戏会话...", alias)
            # 探测通过，自动恢复托管
            self.resume_hosting(alias)
            resumed.append(alias)

        return resumed

    def handle_protocol_notification(
        self,
        alias: str,
        module_id: int,
        action_id: int,
    ) -> bool:
        """协议包监听钩子，自动识别异地登录包 (Mod 100 Act 22 或 Mod 0 Act 15)

        Args:
            alias: 账号别名。
            module_id: 协议模块编号。
            action_id: 协议动作编号。

        Returns:
            若为顶号通知并触发了避让则返回 True，否则返回 False。
        """
        if (module_id == 100 and action_id == 22) or (module_id == 0 and action_id == 15):
            self.trigger_evade(
                alias,
                reason=f"Mod {module_id} Act {action_id} (another_login_notify)",
            )
            return True
        return False
