"""神仙道统一仓储查询门面与领域仓储接口

为上层业务决策引擎与查询提供统一门面入口 (GameStorage)，
整合静态协议字典仓储 (storage.protocol)、角色档案仓储 (storage.player)、
背包资产仓储 (storage.inventory)、子系统状态快照仓储 (storage.module_state)、
战报流水仓储 (storage.battles) 及元宝审计仓储 (storage.audits)，
并提供原生 SQL 执行逃生接口 (storage.query / storage.execute)。

@author Ateng
@since 2026-10-16
"""

import json
import logging
from typing import Any, Dict, List, Optional

from storage.player_db import (
    AuditLogRecord,
    BattleRecord,
    InventoryItemRecord,
    ModuleStateRecord,
    PlayerDatabase,
    PlayerProfileRecord,
)
from storage.protocol_db import ProtocolDatabase, ProtocolRepository
from storage.worker import StorageWorker

logger = logging.getLogger(__name__)


class PlayerRepository:
    """角色基础与高阶属性领域仓储

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self, db: PlayerDatabase, worker: Optional[StorageWorker] = None) -> None:
        self.db = db
        self.worker = worker

    def get_profile(self) -> Optional[PlayerProfileRecord]:
        """获取当前角色最新持久化档案"""
        return self.db.get_player_profile()

    def upsert_profile(self, profile: PlayerProfileRecord, async_write: bool = False) -> None:
        """保存或覆盖角色档案

        Args:
            profile: 角色档案实体。
            async_write: 是否通过后台异步写入队列执行。
        """
        if async_write and self.worker is not None:
            self.worker.submit_profile(profile)
        else:
            self.db.upsert_player_profile(profile)

    def update_stats(self, **kwargs: Any) -> Optional[PlayerProfileRecord]:
        """局部增量更新角色属性字段并立即落盘

        Args:
            kwargs: 待更新属性 (如 level, coins, ingots, power, fame, vip_level, town_id)。

        Returns:
            更新后的角色完整档案。
        """
        # 1. 读取既有档案或初始化缺省档案
        profile = self.get_profile()
        if profile is None:
            profile = PlayerProfileRecord(player_id=self.db.player_id)

        # 2. 动态更新属性值
        for key, value in kwargs.items():
            if hasattr(profile, key):
                current_attr = getattr(profile, key)
                if current_attr is not None and not isinstance(value, type(current_attr)):
                    try:
                        value = type(current_attr)(value)
                    except (ValueError, TypeError):
                        pass
                setattr(profile, key, value)

        # 3. 同步持久化并返回最新状态
        self.db.upsert_player_profile(profile)
        return profile


class InventoryRepository:
    """背包资产与道具装备领域仓储

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self, db: PlayerDatabase, worker: Optional[StorageWorker] = None) -> None:
        self.db = db
        self.worker = worker

    def get_items(self) -> List[InventoryItemRecord]:
        """获取当前背包全部物品列表"""
        return self.db.get_inventory_items()

    def get_item_by_grid(self, grid_id: int) -> Optional[InventoryItemRecord]:
        """按背包格位编号点查物品"""
        items = self.get_items()
        for item in items:
            if item.grid_id == grid_id:
                return item
        return None

    def find_items_by_id(self, item_id: int) -> List[InventoryItemRecord]:
        """按物品模板 ID 查询全部匹配槽位列表"""
        with self.db.connect() as conn:
            cursor = conn.execute(
                "SELECT grid_id, item_id, count, item_type, props_json "
                "FROM tb_inventory WHERE item_id = ? ORDER BY grid_id ASC",
                (item_id,),
            )
            return [
                InventoryItemRecord(
                    grid_id=r["grid_id"],
                    item_id=r["item_id"],
                    count=r["count"],
                    item_type=r["item_type"],
                    props=json.loads(r["props_json"]),
                )
                for r in cursor.fetchall()
            ]

    def upsert_items(self, items: List[InventoryItemRecord], async_write: bool = False) -> None:
        """批量保存或更新背包物品"""
        if not items:
            return
        if async_write and self.worker is not None:
            self.worker.submit_inventory(items)
        else:
            self.db.upsert_inventory_items(items)

    def upsert_item(self, item: InventoryItemRecord, async_write: bool = False) -> None:
        """保存单件背包物品"""
        self.upsert_items([item], async_write=async_write)

    def remove_item(self, grid_id: int) -> None:
        """从背包中移除指定格位的物品"""
        self.db.remove_inventory_item(grid_id)

    def count(self) -> int:
        """获取当前背包已占用格子总数"""
        with self.db.connect() as conn:
            cursor = conn.execute("SELECT COUNT(*) AS cnt FROM tb_inventory")
            row = cursor.fetchone()
            return int(row["cnt"]) if row else 0

    def clear(self) -> None:
        """清空背包所有物品"""
        with self.db.connect() as conn:
            conn.execute("DELETE FROM tb_inventory")
            conn.commit()


class ModuleStateRepository:
    """各功能子系统半结构化快照领域仓储

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self, db: PlayerDatabase, worker: Optional[StorageWorker] = None) -> None:
        self.db = db
        self.worker = worker

    def get_state(self, module_id: int, state_key: str) -> Optional[ModuleStateRecord]:
        """获取指定模块与键名的快照记录"""
        return self.db.get_module_state(module_id, state_key)

    def get_payload(self, module_id: int, state_key: str, default: Optional[Any] = None) -> Any:
        """读取快照载荷有效字典，不存在则返回缺省值"""
        rec = self.get_state(module_id, state_key)
        if rec is None:
            return default
        return rec.payload

    def set_state(self, state: ModuleStateRecord, async_write: bool = False) -> None:
        """保存模块状态快照"""
        if async_write and self.worker is not None:
            self.worker.submit_module_state(state)
        else:
            self.db.set_module_state(state)

    def save_payload(
        self,
        module_id: int,
        state_key: str,
        payload: Any,
        async_write: bool = False,
    ) -> None:
        """便捷保存指定模块与键名的载荷字典"""
        rec = ModuleStateRecord(module_id=module_id, state_key=state_key, payload=payload)
        self.set_state(rec, async_write=async_write)

    def get_all_states(self, module_id: int) -> List[ModuleStateRecord]:
        """获取特定模块下的所有状态快照记录"""
        with self.db.connect() as conn:
            cursor = conn.execute(
                "SELECT module_id, state_key, payload_json "
                "FROM tb_module_state WHERE module_id = ? ORDER BY state_key ASC",
                (module_id,),
            )
            return [
                ModuleStateRecord(
                    module_id=r["module_id"],
                    state_key=r["state_key"],
                    payload=json.loads(r["payload_json"]),
                )
                for r in cursor.fetchall()
            ]


class BattleRecordRepository:
    """战斗结算流水与战报领域仓储

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self, db: PlayerDatabase, worker: Optional[StorageWorker] = None) -> None:
        self.db = db
        self.worker = worker

    def get_recent(self, limit: int = 50) -> List[BattleRecord]:
        """按时间倒序获取最新战报记录"""
        return self.db.get_recent_battle_records(limit=limit)

    def add_record(
        self,
        record: BattleRecord,
        async_write: bool = False,
        max_records: int = 1000,
    ) -> None:
        """添加战斗记录并维持 FIFO 滚动淘汰"""
        if async_write and self.worker is not None:
            self.worker.submit_battle_record(record)
        else:
            self.db.add_battle_record(record, max_records=max_records)

    def count(self) -> int:
        """获取战报总记录数"""
        with self.db.connect() as conn:
            cursor = conn.execute("SELECT COUNT(*) AS cnt FROM tb_battle_records")
            row = cursor.fetchone()
            return int(row["cnt"]) if row else 0

    def get_win_rate(self, limit: int = 100) -> float:
        """计算近期战斗胜率 (0.0 ~ 1.0)"""
        recent = self.get_recent(limit=limit)
        if not recent:
            return 0.0
        wins = sum(1 for r in recent if r.is_win)
        return float(wins) / len(recent)


class AuditLogRepository:
    """高危元宝操作审计日志领域仓储

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self, db: PlayerDatabase, worker: Optional[StorageWorker] = None) -> None:
        self.db = db
        self.worker = worker

    def get_recent(self, limit: int = 50) -> List[AuditLogRecord]:
        """按时间倒序获取最新审计日志"""
        return self.db.get_recent_audit_logs(limit=limit)

    def add_log(
        self,
        log: AuditLogRecord,
        async_write: bool = False,
        max_records: int = 1000,
    ) -> None:
        """追加审计日志并维持 FIFO 滚动淘汰"""
        if async_write and self.worker is not None:
            self.worker.submit_audit_log(log)
        else:
            self.db.add_audit_log(log, max_records=max_records)

    def count(self) -> int:
        """获取审计日志总记录数"""
        with self.db.connect() as conn:
            cursor = conn.execute("SELECT COUNT(*) AS cnt FROM tb_audit_log")
            row = cursor.fetchone()
            return int(row["cnt"]) if row else 0


class GameStorage:
    """神仙道统一存储门面系统

    统一整合静态协议元数据字典仓储与动态角色私有库，
    向业务侧暴露强类型领域仓储接口与原生 SQL 逃生通道。

    @author Ateng
    @since 2026-10-16
    """

    def __init__(
        self,
        server_id: int,
        player_id: int,
        base_dir: Optional[str] = None,
        manifest_path: Optional[str] = None,
        auto_start_worker: bool = True,
        batch_size: int = 50,
        flush_interval: float = 0.05,
    ) -> None:
        self.server_id = server_id
        self.player_id = player_id

        # 1. 初始化静态只读协议元数据字典仓储
        target_db = manifest_path if manifest_path and manifest_path.endswith(".db") else None
        self.protocol_db = ProtocolDatabase(db_path=target_db)
        self.protocol = ProtocolRepository(self.protocol_db)

        # 2. 初始化角色私有 SQLite 动态数据库与后台写入工作线程
        self.player_db = PlayerDatabase(server_id=server_id, player_id=player_id, base_dir=base_dir)
        self.worker = StorageWorker(
            db=self.player_db,
            batch_size=batch_size,
            flush_interval=flush_interval,
        )

        # 3. 装配领域强类型子仓储
        self.player = PlayerRepository(self.player_db, self.worker)
        self.inventory = InventoryRepository(self.player_db, self.worker)
        self.module_state = ModuleStateRepository(self.player_db, self.worker)
        self.battles = BattleRecordRepository(self.player_db, self.worker)
        self.audits = AuditLogRepository(self.player_db, self.worker)

        # 4. 按需启动后台写入线程
        if auto_start_worker:
            self.worker.start()

    def start(self) -> None:
        """启动后台专职写入线程"""
        self.worker.start()

    def flush(self) -> None:
        """立即将后台写入管道中的待入库数据批量刷盘"""
        self.worker.flush()

    def stop(self) -> None:
        """安全停止后台写入线程并确保所有队列数据已持久化"""
        self.worker.stop()

    def close(self) -> None:
        """优雅关闭存储门面并释放后台线程资源"""
        self.stop()

    def query(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """在角色私有库上执行原生 SQL 查询逃生接口 (只读)

        Args:
            sql: 原生 SELECT 语句。
            params: 参数绑定元组。

        Returns:
            以字典形式组织的行记录列表。
        """
        with self.player_db.connect() as conn:
            cursor = conn.execute(sql, params)
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def execute(self, sql: str, params: tuple = ()) -> int:
        """在角色私有库上执行原生 SQL 修改接口 (写入)

        Args:
            sql: 原生 INSERT/UPDATE/DELETE 语句。
            params: 参数绑定元组。

        Returns:
            受影响的数据行数。
        """
        with self.player_db.connect() as conn:
            cursor = conn.execute(sql, params)
            conn.commit()
            return cursor.rowcount

    def __enter__(self) -> "GameStorage":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
