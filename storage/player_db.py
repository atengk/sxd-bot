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


@dataclass
class AssetTransactionRecord:
    """元宝与铜钱资产收支流水实体

    @author Ateng
    @since 2026-10-19
    """

    asset_type: str  # 'coin' | 'ingot'
    change_type: str  # 'income' | 'expense'
    amount: int
    balance_after: int
    reason: str
    created_at: float = field(default_factory=time.time)
    id: Optional[int] = None


@dataclass
class DailyAssetSummaryRecord:
    """每日资产汇总财务实体

    @author Ateng
    @since 2026-10-19
    """

    stat_date: str  # 'YYYY-MM-DD'
    opening_coins: int = 0
    closing_coins: int = 0
    coins_income: int = 0
    coins_expense: int = 0
    opening_ingots: int = 0
    closing_ingots: int = 0
    ingots_income: int = 0
    ingots_expense: int = 0
    updated_at: float = field(default_factory=time.time)


MAX_ASSET_TRANSACTION_RECORDS = 2000


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

                # 7. 元宝与铜钱资产收支流水明细表 (FIFO 滚动淘汰上限 2,000)
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tb_asset_transaction (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        asset_type TEXT NOT NULL,
                        change_type TEXT NOT NULL,
                        amount INTEGER NOT NULL,
                        balance_after INTEGER NOT NULL,
                        reason TEXT NOT NULL,
                        created_at REAL NOT NULL
                    )
                    """
                )
                conn.execute("CREATE INDEX IF NOT EXISTS idx_asset_tx_created_at ON tb_asset_transaction(created_at)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_asset_tx_type ON tb_asset_transaction(asset_type)")

                # 8. 每日资产汇总表 (永久保留，按自然日聚合收支与期初/期末)
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tb_daily_asset_summary (
                        stat_date TEXT PRIMARY KEY,
                        opening_coins INTEGER NOT NULL DEFAULT 0,
                        closing_coins INTEGER NOT NULL DEFAULT 0,
                        coins_income INTEGER NOT NULL DEFAULT 0,
                        coins_expense INTEGER NOT NULL DEFAULT 0,
                        opening_ingots INTEGER NOT NULL DEFAULT 0,
                        closing_ingots INTEGER NOT NULL DEFAULT 0,
                        ingots_income INTEGER NOT NULL DEFAULT 0,
                        ingots_expense INTEGER NOT NULL DEFAULT 0,
                        updated_at REAL NOT NULL
                    )
                    """
                )
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

    def record_asset_transaction(
        self,
        rec: AssetTransactionRecord,
        max_records: int = MAX_ASSET_TRANSACTION_RECORDS,
    ) -> None:
        """记录一条资产收支流水，执行 FIFO 淘汰并即时增量更新每日汇总表 (Stream-driven Upsert)

        Args:
            rec: 资产收支流水实体。
            max_records: 明细表最大保留条数 (FIFO 淘汰门槛)。
        """
        stat_date = time.strftime("%Y-%m-%d", time.localtime(rec.created_at))
        with self.connect() as conn:
            with conn:
                # 1. 写入明细流水表
                cursor = conn.execute(
                    """
                    INSERT INTO tb_asset_transaction (asset_type, change_type, amount, balance_after, reason, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (rec.asset_type, rec.change_type, rec.amount, rec.balance_after, rec.reason, rec.created_at),
                )
                rec.id = cursor.lastrowid

                # 2. 明细流水表 FIFO 自动滚动淘汰
                conn.execute(
                    """
                    DELETE FROM tb_asset_transaction
                    WHERE id NOT IN (
                        SELECT id FROM tb_asset_transaction ORDER BY id DESC LIMIT ?
                    )
                    """,
                    (max_records,),
                )

                # 3. 每日资产汇总表增量累加与期末结余刷新
                row = conn.execute(
                    "SELECT * FROM tb_daily_asset_summary WHERE stat_date = ?", (stat_date,)
                ).fetchone()

                if row is None:
                    # 尝试继承前序最近一天的期末结余作为期初基准
                    prev_row = conn.execute(
                        "SELECT closing_coins, closing_ingots FROM tb_daily_asset_summary WHERE stat_date < ? ORDER BY stat_date DESC LIMIT 1",
                        (stat_date,),
                    ).fetchone()

                    # 读取当前全量画像兜底
                    prof_row = conn.execute(
                        "SELECT coins, ingots FROM tb_player_profile WHERE player_id = ?",
                        (self.player_id,),
                    ).fetchone()
                    fallback_coins = prof_row["coins"] if prof_row else 0
                    fallback_ingots = prof_row["ingots"] if prof_row else 0

                    base_coins = prev_row["closing_coins"] if prev_row else fallback_coins
                    base_ingots = prev_row["closing_ingots"] if prev_row else fallback_ingots

                    if rec.asset_type == "coin":
                        op_coins = (
                            rec.balance_after - rec.amount
                            if rec.change_type == "income"
                            else rec.balance_after + rec.amount
                        )
                        cl_coins = rec.balance_after
                        c_in = rec.amount if rec.change_type == "income" else 0
                        c_ex = rec.amount if rec.change_type == "expense" else 0
                        op_ingots = base_ingots
                        cl_ingots = base_ingots
                        i_in = 0
                        i_ex = 0
                    else:
                        op_ingots = (
                            rec.balance_after - rec.amount
                            if rec.change_type == "income"
                            else rec.balance_after + rec.amount
                        )
                        cl_ingots = rec.balance_after
                        i_in = rec.amount if rec.change_type == "income" else 0
                        i_ex = rec.amount if rec.change_type == "expense" else 0
                        op_coins = base_coins
                        cl_coins = base_coins
                        c_in = 0
                        c_ex = 0

                    conn.execute(
                        """
                        INSERT INTO tb_daily_asset_summary (
                            stat_date, opening_coins, closing_coins, coins_income, coins_expense,
                            opening_ingots, closing_ingots, ingots_income, ingots_expense, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (stat_date, op_coins, cl_coins, c_in, c_ex, op_ingots, cl_ingots, i_in, i_ex, rec.created_at),
                    )
                else:
                    if rec.asset_type == "coin":
                        c_in_delta = rec.amount if rec.change_type == "income" else 0
                        c_ex_delta = rec.amount if rec.change_type == "expense" else 0
                        if (
                            row["opening_coins"] == 0
                            and row["closing_coins"] == 0
                            and row["coins_income"] == 0
                            and row["coins_expense"] == 0
                        ):
                            op_coin_val = (
                                rec.balance_after - rec.amount
                                if rec.change_type == "income"
                                else rec.balance_after + rec.amount
                            )
                            conn.execute(
                                """
                                UPDATE tb_daily_asset_summary
                                SET opening_coins = ?,
                                    closing_coins = ?,
                                    coins_income = coins_income + ?,
                                    coins_expense = coins_expense + ?,
                                    updated_at = ?
                                WHERE stat_date = ?
                                """,
                                (op_coin_val, rec.balance_after, c_in_delta, c_ex_delta, rec.created_at, stat_date),
                            )
                        else:
                            conn.execute(
                                """
                                UPDATE tb_daily_asset_summary
                                SET closing_coins = ?,
                                    coins_income = coins_income + ?,
                                    coins_expense = coins_expense + ?,
                                    updated_at = ?
                                WHERE stat_date = ?
                                """,
                                (rec.balance_after, c_in_delta, c_ex_delta, rec.created_at, stat_date),
                            )
                    else:
                        i_in_delta = rec.amount if rec.change_type == "income" else 0
                        i_ex_delta = rec.amount if rec.change_type == "expense" else 0
                        if (
                            row["opening_ingots"] == 0
                            and row["closing_ingots"] == 0
                            and row["ingots_income"] == 0
                            and row["ingots_expense"] == 0
                        ):
                            op_ingot_val = (
                                rec.balance_after - rec.amount
                                if rec.change_type == "income"
                                else rec.balance_after + rec.amount
                            )
                            conn.execute(
                                """
                                UPDATE tb_daily_asset_summary
                                SET opening_ingots = ?,
                                    closing_ingots = ?,
                                    ingots_income = ingots_income + ?,
                                    ingots_expense = ingots_expense + ?,
                                    updated_at = ?
                                WHERE stat_date = ?
                                """,
                                (op_ingot_val, rec.balance_after, i_in_delta, i_ex_delta, rec.created_at, stat_date),
                            )
                        else:
                            conn.execute(
                                """
                                UPDATE tb_daily_asset_summary
                                SET closing_ingots = ?,
                                    ingots_income = ingots_income + ?,
                                    ingots_expense = ingots_expense + ?,
                                    updated_at = ?
                                WHERE stat_date = ?
                                """,
                                (rec.balance_after, i_in_delta, i_ex_delta, rec.created_at, stat_date),
                            )

    def get_recent_asset_transactions(
        self,
        limit: int = 50,
        asset_type: Optional[str] = None,
        stat_date: Optional[str] = None,
    ) -> List[AssetTransactionRecord]:
        """获取最近资产收支流水明细

        Args:
            limit: 最大返回条数。
            asset_type: 可选币种过滤 ('coin' | 'ingot')。
            stat_date: 可选自然日过滤 ('YYYY-MM-DD')。

        Returns:
            资产流水记录列表 (按时间降序)。
        """
        sql = "SELECT id, asset_type, change_type, amount, balance_after, reason, created_at FROM tb_asset_transaction WHERE 1=1"
        params: List[Any] = []
        if asset_type:
            sql += " AND asset_type = ?"
            params.append(asset_type)
        if stat_date:
            try:
                start_ts = time.mktime(time.strptime(f"{stat_date} 00:00:00", "%Y-%m-%d %H:%M:%S"))
                end_ts = start_ts + 86400.0
                sql += " AND created_at >= ? AND created_at < ?"
                params.extend([start_ts, end_ts])
            except (ValueError, TypeError):
                pass

        sql += " ORDER BY id DESC LIMIT ?"
        params.append(limit)

        with self.connect() as conn:
            cursor = conn.execute(sql, tuple(params))
            return [
                AssetTransactionRecord(
                    id=r["id"],
                    asset_type=r["asset_type"],
                    change_type=r["change_type"],
                    amount=r["amount"],
                    balance_after=r["balance_after"],
                    reason=r["reason"],
                    created_at=r["created_at"],
                )
                for r in cursor.fetchall()
            ]

    def get_daily_asset_summaries(self, days: int = 7) -> List[DailyAssetSummaryRecord]:
        """获取最近 N 日的每日资产汇总 (按日期升序排列，便于前端走势图绘制)

        Args:
            days: 历史天数。

        Returns:
            每日资产汇总列表 (按日期升序)。
        """
        with self.connect() as conn:
            cursor = conn.execute(
                """
                SELECT stat_date, opening_coins, closing_coins, coins_income, coins_expense,
                       opening_ingots, closing_ingots, ingots_income, ingots_expense, updated_at
                FROM tb_daily_asset_summary
                ORDER BY stat_date DESC LIMIT ?
                """,
                (days,),
            )
            rows = cursor.fetchall()
            records = [
                DailyAssetSummaryRecord(
                    stat_date=r["stat_date"],
                    opening_coins=r["opening_coins"],
                    closing_coins=r["closing_coins"],
                    coins_income=r["coins_income"],
                    coins_expense=r["coins_expense"],
                    opening_ingots=r["opening_ingots"],
                    closing_ingots=r["closing_ingots"],
                    ingots_income=r["ingots_income"],
                    ingots_expense=r["ingots_expense"],
                    updated_at=r["updated_at"],
                )
                for r in rows
            ]
            records.reverse()
            return records

    def get_today_asset_summary(self) -> Optional[DailyAssetSummaryRecord]:
        """获取当天的每日资产汇总快照

        Returns:
            今日汇总实体，若今日尚无收支变动则返回 None。
        """
        today_str = time.strftime("%Y-%m-%d")
        with self.connect() as conn:
            row = conn.execute(
                """
                SELECT stat_date, opening_coins, closing_coins, coins_income, coins_expense,
                       opening_ingots, closing_ingots, ingots_income, ingots_expense, updated_at
                FROM tb_daily_asset_summary WHERE stat_date = ?
                """,
                (today_str,),
            ).fetchone()
            if row is None:
                return None
            return DailyAssetSummaryRecord(
                stat_date=row["stat_date"],
                opening_coins=row["opening_coins"],
                closing_coins=row["closing_coins"],
                coins_income=row["coins_income"],
                coins_expense=row["coins_expense"],
                opening_ingots=row["opening_ingots"],
                closing_ingots=row["closing_ingots"],
                ingots_income=row["ingots_income"],
                ingots_expense=row["ingots_expense"],
                updated_at=row["updated_at"],
            )

    def save_daily_asset_summary(self, summary: DailyAssetSummaryRecord) -> None:
        """保存或更新单日资产汇总快照 (支持期初结存初始化与增量修正)

        Args:
            summary: 每日资产汇总记录实体。
        """
        now = time.time()
        with self.connect() as conn:
            with conn:
                conn.execute(
                    """
                    INSERT INTO tb_daily_asset_summary (
                        stat_date, opening_coins, closing_coins, coins_income, coins_expense,
                        opening_ingots, closing_ingots, ingots_income, ingots_expense, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(stat_date) DO UPDATE SET
                        opening_coins = CASE WHEN excluded.opening_coins > 0 THEN excluded.opening_coins ELSE tb_daily_asset_summary.opening_coins END,
                        closing_coins = excluded.closing_coins,
                        coins_income = excluded.coins_income,
                        coins_expense = excluded.coins_expense,
                        opening_ingots = CASE WHEN excluded.opening_ingots > 0 THEN excluded.opening_ingots ELSE tb_daily_asset_summary.opening_ingots END,
                        closing_ingots = excluded.closing_ingots,
                        ingots_income = excluded.ingots_income,
                        ingots_expense = excluded.ingots_expense,
                        updated_at = excluded.updated_at
                    """,
                    (
                        summary.stat_date,
                        summary.opening_coins,
                        summary.closing_coins,
                        summary.coins_income,
                        summary.coins_expense,
                        summary.opening_ingots,
                        summary.closing_ingots,
                        summary.ingots_income,
                        summary.ingots_expense,
                        now,
                    ),
                )


