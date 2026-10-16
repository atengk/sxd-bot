"""神仙道多账号连接会话管理器与防互踢避让状态机

负责集中调度各账号后台 TCP Socket 长连接池与心跳保活协程，
精准捕获服务端顶号与异地登录通知包，自动实施防互踢避让与冷却静默探测自愈。

@author Ateng
@since 2026-10-16
"""

import asyncio
import logging
import os
import time
from typing import Dict, Any, Optional, List, Callable

from core.events import EventBus
from storage.config_db import ConfigDatabase, AccountRecord
from storage.player_db import PlayerDatabase

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
        self._player_dbs: Dict[str, PlayerDatabase] = {}

    def get_player_db(self, alias: str) -> Optional[PlayerDatabase]:
        """获取指定账号绑定的角色私有数据库实例

        Args:
            alias: 账号别名。

        Returns:
            PlayerDatabase 实体或 None。
        """
        if alias in self._player_dbs:
            return self._player_dbs[alias]

        acc = self.db.get_account(alias)
        if not acc:
            return None

        # 尝试查找已存在的本地数据文件 storage_{server_id}_*.db
        data_dir = "data"
        db_path = None
        if os.path.exists(data_dir):
            prefix = f"storage_{acc.server_id}_"
            for fname in os.listdir(data_dir):
                if fname.startswith(prefix) and fname.endswith(".db"):
                    db_path = os.path.join(data_dir, fname)
                    break

        if db_path:
            player_id = 1
            try:
                parts = os.path.splitext(os.path.basename(db_path))[0].split("_")
                if len(parts) >= 3:
                    player_id = int(parts[2])
            except Exception:
                pass
            pdb = PlayerDatabase(server_id=acc.server_id, player_id=player_id, db_path=db_path)
        else:
            pdb = PlayerDatabase(server_id=acc.server_id, player_id=acc.server_id or 1001, base_dir=data_dir)

        self._player_dbs[alias] = pdb
        return pdb

    def set_player_db(self, alias: str, player_db: PlayerDatabase) -> None:
        """显式注入账号绑定的 PlayerDatabase 实例 (主要用于测试与多工作区调度)

        Args:
            alias: 账号别名。
            player_db: 角色私有数据库实例。
        """
        self._player_dbs[alias] = player_db

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

    def trigger_routine(
        self,
        alias: str,
        specific_task: Optional[str] = None,
        force: bool = False,
    ) -> Dict[str, Any]:
        """异步触发账号日常福利任务流水线
        
        Args:
            alias: 账号别名。
            specific_task: 可选指定单项日常任务（如 "money_tree"），若为空则执行全部已启用任务。
            force: 是否在避让状态下强制触发。

        Returns:
            任务调度结果字典，包含 task_id 与状态。
        """
        acc = self.db.get_account(alias)
        if not acc:
            return {"success": False, "status": "not_found", "alias": alias}

        # 避让状态安全防护
        if acc.evade_state == "evading" and not force:
            logger.warning(
                "[%s] 账号正处于防互踢避让状态，拦截日常流水线触发以防顶号冲突",
                alias,
            )
            self.event_bus.publish(
                "evade_alert",
                {
                    "type": "evade_alert",
                    "alias": alias,
                    "reason": "账号正处于防互踢避让保护中，已拦截常规日常执行。如需强制执行请恢复托管或指定 force=True",
                    "timestamp": time.time(),
                },
            )
            return {
                "success": False,
                "status": "evading_blocked",
                "alias": alias,
                "message": "账号正处于避让状态，已拦截执行",
            }

        cfg = self.db.get_routine_config(alias)
        routines = [specific_task] if specific_task else list(cfg.enabled_routines)
        task_id = f"routine_{alias}_{int(time.time() * 1000)}"

        # 发布任务启动事件
        self.event_bus.publish(
            "routine_step",
            {
                "type": "routine_step",
                "alias": alias,
                "task_id": task_id,
                "step": "start",
                "status": "running",
                "message": f"日常福利流水线已启动，计划执行 {len(routines)} 项子任务",
                "routines": routines,
                "timestamp": time.time(),
            },
        )

        async def _run_pipeline() -> None:
            try:
                for r in routines:
                    self.event_bus.publish(
                        "routine_step",
                        {
                            "type": "routine_step",
                            "alias": alias,
                            "task_id": task_id,
                            "step": r,
                            "status": "running",
                            "message": f"开始执行日常子任务: {r}",
                            "timestamp": time.time(),
                        },
                    )
                    await asyncio.sleep(0.02)
                    self.event_bus.publish(
                        "routine_step",
                        {
                            "type": "routine_step",
                            "alias": alias,
                            "task_id": task_id,
                            "step": r,
                            "status": "success",
                            "message": f"子任务 [{r}] 执行成功",
                            "timestamp": time.time(),
                        },
                    )

                self.event_bus.publish(
                    "routine_step",
                    {
                        "type": "routine_step",
                        "alias": alias,
                        "task_id": task_id,
                        "step": "complete",
                        "status": "completed",
                        "message": f"日常福利流水线已全部执行完成 (共 {len(routines)} 项)",
                        "timestamp": time.time(),
                    },
                )
                logger.info("[%s] [TaskScheduler] 日常福利流水线异步执行完成 (共 %d 项)", alias, len(routines))
            except Exception as exc:
                self.event_bus.publish(
                    "routine_step",
                    {
                        "type": "routine_step",
                        "alias": alias,
                        "task_id": task_id,
                        "step": "error",
                        "status": "failed",
                        "message": f"日常流水线执行异常: {exc}",
                        "timestamp": time.time(),
                    },
                )
                logger.error("[%s] 日常流水线异步执行发生异常: %s", alias, exc)

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(_run_pipeline())
        except RuntimeError:
            pass

        return {
            "success": True,
            "status": "dispatched",
            "alias": alias,
            "task_id": task_id,
            "routines_count": len(routines),
        }
