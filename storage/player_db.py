"""神仙道角色私有数据库与动态业务实体存储引擎

管理单个角色在特定区服的私有 SQLite 数据库 (storage_{server_id}_{player_id}.db)，
支持 WAL 模式高并发读写，涵盖角色画像、背包装备、子系统 JSON 快照、
战报历史与元宝风控审计流水，并实施 1,000 条 FIFO 自动滚动淘汰。

@author Ateng
@since 2026-10-16
"""

import json
import logging
import os
import sqlite3
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Iterator, Tuple

logger = logging.getLogger(__name__)

DEFAULT_DATA_DIR = "data"
MAX_FIFO_RECORDS = 1000


@dataclass
class PlayerProfileRecord:
    """角色基础属性持久化实体

    @author Ateng
    @since 2026-10-16
    """

    player_id: int
    nickname: str = ""
    level: int = 1
    coins: int = 0
    ingots: int = 0
    power: int = 0
    fame: int = 0
    vip_level: int = 0
    town_id: int = 0
    updated_at: float = field(default_factory=time.time)


@dataclass
class InventoryItemRecord:
    """背包装备与道具槽位实体

    @author Ateng
    @since 2026-10-16
    """

    grid_id: int
    item_id: int
    count: int = 1
    item_type: int = 0
    props: Dict[str, Any] = field(default_factory=dict)
    updated_at: float = field(default_factory=time.time)


@dataclass
class ModuleStateRecord:
    """子系统半结构化状态快照实体

    @author Ateng
    @since 2026-10-16
    """

    module_id: int
    state_key: str
    payload: Dict[str, Any] = field(default_factory=dict)
    updated_at: float = field(default_factory=time.time)


@dataclass
class BattleRecord:
    """关卡怪物战斗与战利品结算记录实体

    @author Ateng
    @since 2026-10-16
    """

    mission_id: int
    is_win: bool
    exp_gain: int = 0
    coins_gain: int = 0
    payload: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    id: Optional[int] = None


@dataclass
class AuditLogRecord:
    """元宝扣除与高危资产操作安全审计实体

    @author Ateng
    @since 2026-10-16
    """

    module_id: int
    action_id: int
    action_name: str
    allow_ingot: bool
    details: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    id: Optional[int] = None


class PlayerDatabase:
    """角色私有 SQLite 数据库引擎

    @author Ateng
    @since 2026-10-16
    """

    def __init__(
        self,
        server_id: int,
        player_id: int,
        base_dir: Optional[str] = None,
        db_path: Optional[str] = None,
    ) -> None:
        self.server_id = server_id
        self.player_id = player_id
        if db_path:
            self.db_path = db_path
        else:
            dir_path = base_dir or DEFAULT_DATA_DIR
            self.db_path = os.path.join(dir_path, f"storage_{server_id}_{player_id}.db")

        self._init_database()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        """获取安全的受管数据库连接 (离开上下文自动关闭物理句柄)"""
        conn = sqlite3.connect(self.db_path, timeout=5.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
        finally:
            conn.close()

    def get_connection(self) -> Iterator[sqlite3.Connection]:
        """获取安全受管数据库连接别名"""
        return self.connect()

    def _init_database(self) -> None:
        """初始化物理数据库目录、开启 WAL 模式并建表"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        try:
            with conn:
                # 1. 启用 WAL 高并发无锁读模式与短超时防御
                conn.execute("PRAGMA journal_mode = WAL;")
                conn.execute("PRAGMA synchronous = NORMAL;")
                conn.execute("PRAGMA busy_timeout = 5000;")

                # 2. 角色核心基础信息单行表
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tb_player_profile (
                        player_id INTEGER PRIMARY KEY,
                        nickname TEXT NOT NULL DEFAULT '',
                        level INTEGER NOT NULL DEFAULT 1,
                        coins INTEGER NOT NULL DEFAULT 0,
                        ingots INTEGER NOT NULL DEFAULT 0,
                        power INTEGER NOT NULL DEFAULT 0,
                        fame INTEGER NOT NULL DEFAULT 0,
                        vip_level INTEGER NOT NULL DEFAULT 0,
                        town_id INTEGER NOT NULL DEFAULT 0,
                        updated_at REAL NOT NULL
                    )
                    """
                )

                # 3. 角色背包与装备资产表
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tb_inventory (
                        grid_id INTEGER PRIMARY KEY,
                        item_id INTEGER NOT NULL,
                        count INTEGER NOT NULL DEFAULT 1,
                        item_type INTEGER NOT NULL DEFAULT 0,
                        props_json TEXT NOT NULL DEFAULT '{}',
                        updated_at REAL NOT NULL
                    )
                    """
                )
                conn.execute("CREATE INDEX IF NOT EXISTS idx_inventory_item_id ON tb_inventory(item_id)")

                # 4. 高频子系统半结构化最新快照表 (支持 json_extract 检索)
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tb_module_state (
                        module_id INTEGER NOT NULL,
                        state_key TEXT NOT NULL,
                        payload_json TEXT NOT NULL DEFAULT '{}',
                        updated_at REAL NOT NULL,
                        PRIMARY KEY (module_id, state_key)
                    )
                    """
                )

                # 5. 战斗挑战流水记录表 (FIFO 滚动淘汰上限 1,000)
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tb_battle_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        mission_id INTEGER NOT NULL,
                        is_win INTEGER NOT NULL DEFAULT 0,
                        exp_gain INTEGER NOT NULL DEFAULT 0,
                        coins_gain INTEGER NOT NULL DEFAULT 0,
                        created_at REAL NOT NULL,
                        payload_json TEXT NOT NULL DEFAULT '{}'
                    )
                    """
                )
                conn.execute("CREATE INDEX IF NOT EXISTS idx_battle_created_at ON tb_battle_records(created_at)")

                # 6. 元宝扣除与高危动作审计流水表 (FIFO 滚动淘汰上限 1,000)
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tb_audit_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        module_id INTEGER NOT NULL,
                        action_id INTEGER NOT NULL,
                        action_name TEXT NOT NULL,
                        allow_ingot INTEGER NOT NULL DEFAULT 0,
                        created_at REAL NOT NULL,
                        details_json TEXT NOT NULL DEFAULT '{}'
                    )
                    """
                )
                conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_created_at ON tb_audit_log(created_at)")
        finally:
            conn.close()

    # ==========================================================================
    # 读写底层操作 API (由仓储与写入 Worker 协同调度)
    # ==========================================================================

    def upsert_player_profile(self, profile: PlayerProfileRecord) -> None:
        """插入或更新角色核心属性"""
        with self.connect() as conn:
            with conn:
                conn.execute(
                    """
                    INSERT INTO tb_player_profile (player_id, nickname, level, coins, ingots, power, fame, vip_level, town_id, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(player_id) DO UPDATE SET
                        nickname = excluded.nickname,
                        level = excluded.level,
                        coins = excluded.coins,
                        ingots = excluded.ingots,
                        power = excluded.power,
                        fame = excluded.fame,
                        vip_level = excluded.vip_level,
                        town_id = excluded.town_id,
                        updated_at = excluded.updated_at
                    """,
                    (
                        profile.player_id,
                        profile.nickname,
                        profile.level,
                        profile.coins,
                        profile.ingots,
                        profile.power,
                        profile.fame,
                        profile.vip_level,
                        profile.town_id,
                        profile.updated_at,
                    ),
                )

    def get_player_profile(self) -> Optional[PlayerProfileRecord]:
        """获取当前角色的核心属性"""
        with self.connect() as conn:
            cursor = conn.execute(
                """
                SELECT player_id, nickname, level, coins, ingots, power, fame, vip_level, town_id, updated_at
                FROM tb_player_profile WHERE player_id = ?
                """,
                (self.player_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return PlayerProfileRecord(
                player_id=row["player_id"],
                nickname=row["nickname"],
                level=row["level"],
                coins=row["coins"],
                ingots=row["ingots"],
                power=row["power"],
                fame=row["fame"],
                vip_level=row["vip_level"],
                town_id=row["town_id"],
                updated_at=row["updated_at"],
            )

    def upsert_inventory_items(self, items: List[InventoryItemRecord]) -> None:
        """批量更新背包装备与道具"""
        if not items:
            return
        rows = [
            (i.grid_id, i.item_id, i.count, i.item_type, json.dumps(i.props), i.updated_at)
            for i in items
        ]
        with self.connect() as conn:
            with conn:
                conn.executemany(
                    """
                    INSERT INTO tb_inventory (grid_id, item_id, count, item_type, props_json, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(grid_id) DO UPDATE SET
                        item_id = excluded.item_id,
                        count = excluded.count,
                        item_type = excluded.item_type,
                        props_json = excluded.props_json,
                        updated_at = excluded.updated_at
                    """,
                    rows,
                )

    def get_inventory_items(self) -> List[InventoryItemRecord]:
        """获取当前背包装备全量列表"""
        with self.connect() as conn:
            cursor = conn.execute(
                "SELECT grid_id, item_id, count, item_type, props_json, updated_at FROM tb_inventory ORDER BY grid_id ASC"
            )
            return [
                InventoryItemRecord(
                    grid_id=r["grid_id"],
                    item_id=r["item_id"],
                    count=r["count"],
                    item_type=r["item_type"],
                    props=json.loads(r["props_json"]),
                    updated_at=r["updated_at"],
                )
                for r in cursor.fetchall()
            ]

    def remove_inventory_item(self, grid_id: int) -> None:
        """移除指定背包格子的道具"""
        with self.connect() as conn:
            with conn:
                conn.execute("DELETE FROM tb_inventory WHERE grid_id = ?", (grid_id,))

    def set_module_state(self, record: ModuleStateRecord) -> None:
        """写入或更新子系统状态快照"""
        with self.connect() as conn:
            with conn:
                conn.execute(
                    """
                    INSERT INTO tb_module_state (module_id, state_key, payload_json, updated_at)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(module_id, state_key) DO UPDATE SET
                        payload_json = excluded.payload_json,
                        updated_at = excluded.updated_at
                    """,
                    (record.module_id, record.state_key, json.dumps(record.payload), record.updated_at),
                )

    def get_module_state(self, module_id: int, state_key: str) -> Optional[ModuleStateRecord]:
        """读取子系统指定快照"""
        with self.connect() as conn:
            cursor = conn.execute(
                "SELECT module_id, state_key, payload_json, updated_at FROM tb_module_state WHERE module_id = ? AND state_key = ?",
                (module_id, state_key),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return ModuleStateRecord(
                module_id=row["module_id"],
                state_key=row["state_key"],
                payload=json.loads(row["payload_json"]),
                updated_at=row["updated_at"],
            )

    def add_battle_record(self, record: BattleRecord, max_records: int = MAX_FIFO_RECORDS) -> None:
        """插入一条战斗战报记录并执行 FIFO 滚动淘汰"""
        with self.connect() as conn:
            with conn:
                cursor = conn.execute(
                    """
                    INSERT INTO tb_battle_records (mission_id, is_win, exp_gain, coins_gain, created_at, payload_json)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record.mission_id,
                        1 if record.is_win else 0,
                        record.exp_gain,
                        record.coins_gain,
                        record.created_at,
                        json.dumps(record.payload),
                    ),
                )
                record.id = cursor.lastrowid

                # FIFO 滚动淘汰：保留最新的 max_records 条
                conn.execute(
                    """
                    DELETE FROM tb_battle_records
                    WHERE id NOT IN (
                        SELECT id FROM tb_battle_records ORDER BY id DESC LIMIT ?
                    )
                    """,
                    (max_records,),
                )

    def get_recent_battle_records(self, limit: int = 50) -> List[BattleRecord]:
        """获取最近发生的战斗战报流水"""
        with self.connect() as conn:
            cursor = conn.execute(
                """
                SELECT id, mission_id, is_win, exp_gain, coins_gain, created_at, payload_json
                FROM tb_battle_records ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            )
            return [
                BattleRecord(
                    id=r["id"],
                    mission_id=r["mission_id"],
                    is_win=bool(r["is_win"]),
                    exp_gain=r["exp_gain"],
                    coins_gain=r["coins_gain"],
                    created_at=r["created_at"],
                    payload=json.loads(r["payload_json"]),
                )
                for r in cursor.fetchall()
            ]

    def add_audit_log(self, log: AuditLogRecord, max_records: int = MAX_FIFO_RECORDS) -> None:
        """记录一条元宝高危操作审计并执行 FIFO 滚动淘汰"""
        with self.connect() as conn:
            with conn:
                cursor = conn.execute(
                    """
                    INSERT INTO tb_audit_log (module_id, action_id, action_name, allow_ingot, created_at, details_json)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        log.module_id,
                        log.action_id,
                        log.action_name,
                        1 if log.allow_ingot else 0,
                        log.created_at,
                        json.dumps(log.details),
                    ),
                )
                log.id = cursor.lastrowid

                # FIFO 滚动淘汰
                conn.execute(
                    """
                    DELETE FROM tb_audit_log
                    WHERE id NOT IN (
                        SELECT id FROM tb_audit_log ORDER BY id DESC LIMIT ?
                    )
                    """,
                    (max_records,),
                )

    def get_recent_audit_logs(self, limit: int = 50) -> List[AuditLogRecord]:
        """获取最近的高危元宝审计记录流水"""
        with self.connect() as conn:
            cursor = conn.execute(
                """
                SELECT id, module_id, action_id, action_name, allow_ingot, created_at, details_json
                FROM tb_audit_log ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            )
            return [
                AuditLogRecord(
                    id=r["id"],
                    module_id=r["module_id"],
                    action_id=r["action_id"],
                    action_name=r["action_name"],
                    allow_ingot=bool(r["allow_ingot"]),
                    created_at=r["created_at"],
                    details=json.loads(r["details_json"]),
                )
                for r in cursor.fetchall()
            ]
