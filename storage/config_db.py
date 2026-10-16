"""神仙道集中式 SQLite 配置仓储与动态实体数据持久化引擎

集中纳管多账号凭据、账号级独立 35 项日常子任务开关、元宝安全红线与系统运行参数，
支持 WAL 模式高并发读写，提供初次从 config.json 种子数据的无感自动迁移。

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

from core.config import AccountConfig, AppConfig, SettingsConfig, ConfigManager

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_DB_PATH = os.path.join("data", "config.sqlite")
DEFAULT_SEED_JSON_PATH = os.path.join("config", "config.json")

# 35 项标准自动化与日常任务名录
ALL_ROUTINES: List[str] = [
    "login",
    "heartbeat",
    "signin",
    "money_tree",
    "online_gift",
    "worship",
    "faction_roll",
    "lucky_star",
    "farm",
    "peach_pet",
    "fate",
    "take_bible",
    "hero_mission",
    "normal_mission",
    "arena",
    "six_paths_tower",
    "traders",
    "fishing",
    "seal_satan",
    "touch_stone",
    "ask_fairy",
    "weekend",
    "email",
    "item_clean",
    "hunt_demon",
    "five_elements",
    "five_fu",
    "nimbus",
    "link_fate",
    "home",
    "union_worship",
    "memory_zone",
    "assistant",
    "travel_event",
    "practice",
]


@dataclass
class AccountRecord:
    """平台账号持久化实体

    @author Ateng
    @since 2026-10-16
    """

    alias: str
    platform: str = "fengwanyx"
    username: str = ""
    password: str = ""
    server: str = "s813"
    server_id: int = 25268
    server_host: Optional[str] = None
    server_port: Optional[int] = None
    player_id: int = 0
    enabled: bool = True
    hosting_enabled: bool = True
    evade_state: str = "none"  # "none" | "evading"
    evade_since: float = 0.0
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def to_account_config(self) -> AccountConfig:
        """转换为内存态 AccountConfig 领域对象"""
        return AccountConfig(
            alias=self.alias,
            username=self.username,
            password=self.password,
            server=self.server,
            server_id=self.server_id,
            server_host=self.server_host,
            server_port=self.server_port,
            enabled=self.enabled,
            platform=self.platform,
        )


@dataclass
class RoutineConfigRecord:
    """账号级独立日常任务配置与元宝安全红线

    @author Ateng
    @since 2026-10-16
    """

    alias: str
    allowed_ingots: int = 0
    enabled_routines: List[str] = field(default_factory=lambda: list(ALL_ROUTINES))
    updated_at: float = field(default_factory=time.time)


@dataclass
class SystemSettingRecord:
    """系统级键值参数实体

    @author Ateng
    @since 2026-10-16
    """

    key: str
    value: str = ""
    updated_at: float = field(default_factory=time.time)


class ConfigDatabase:
    """SQLite 配置仓储与自愈管理中心

    @author Ateng
    @since 2026-10-16
    """

    def __init__(
        self,
        db_path: Optional[str] = None,
        seed_json_path: Optional[str] = None,
        auto_bootstrap: bool = True,
    ) -> None:
        """初始化配置仓储并执行模式自检与种子迁移

        Args:
            db_path: SQLite 数据库物理存储路径。
            seed_json_path: 首次冷启时的 JSON 种子路径，若传入空字符串或 None 且 auto_bootstrap=False 则不执行迁移。
            auto_bootstrap: 是否在首次启动表为空时自动尝试从种子文件迁移。
        """
        self.db_path = db_path or DEFAULT_CONFIG_DB_PATH
        if seed_json_path is not None:
            self.seed_json_path = seed_json_path
        else:
            self.seed_json_path = DEFAULT_SEED_JSON_PATH if auto_bootstrap else ""
        self.auto_bootstrap = auto_bootstrap

        self._ensure_db_dir()
        self._init_schema()
        if self.auto_bootstrap and self.seed_json_path:
            self._auto_bootstrap_if_empty()


    def _ensure_db_dir(self) -> None:
        """确保数据库文件父目录存在"""
        db_dir = os.path.dirname(os.path.abspath(self.db_path))
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        """获取启用 WAL 模式且行映射为 Row 的受管数据库连接"""
        conn = sqlite3.connect(self.db_path, timeout=5.0)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA synchronous = NORMAL;")
            conn.execute("PRAGMA busy_timeout = 5000;")
            conn.execute("PRAGMA foreign_keys = ON;")
            yield conn
        finally:
            conn.close()

    def _init_schema(self) -> None:
        """初始化核心表结构索引"""
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS tb_accounts (
                    alias TEXT PRIMARY KEY,
                    platform TEXT NOT NULL DEFAULT 'fengwanyx',
                    username TEXT NOT NULL DEFAULT '',
                    password TEXT NOT NULL DEFAULT '',
                    server TEXT NOT NULL DEFAULT 's813',
                    server_id INTEGER NOT NULL DEFAULT 25268,
                    server_host TEXT,
                    server_port INTEGER,
                    player_id INTEGER NOT NULL DEFAULT 0,
                    enabled INTEGER NOT NULL DEFAULT 1,
                    hosting_enabled INTEGER NOT NULL DEFAULT 1,
                    evade_state TEXT NOT NULL DEFAULT 'none',
                    evade_since REAL NOT NULL DEFAULT 0.0,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL
                );

                CREATE TABLE IF NOT EXISTS tb_routine_configs (
                    alias TEXT PRIMARY KEY,
                    allowed_ingots INTEGER NOT NULL DEFAULT 0,
                    enabled_routines_json TEXT NOT NULL DEFAULT '[]',
                    updated_at REAL NOT NULL,
                    FOREIGN KEY (alias) REFERENCES tb_accounts(alias) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS tb_system_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL DEFAULT '',
                    updated_at REAL NOT NULL
                );
                """
            )
            try:
                conn.execute("ALTER TABLE tb_accounts ADD COLUMN player_id INTEGER NOT NULL DEFAULT 0;")
            except sqlite3.OperationalError:
                pass
            try:
                # 迁移升级：若存量已启用账号存在 hosting_enabled 为 0 的，默认全量置为 1 开启长连接
                conn.execute("UPDATE tb_accounts SET hosting_enabled = 1 WHERE enabled = 1 AND hosting_enabled = 0;")
            except sqlite3.OperationalError:
                pass
            conn.commit()

    def _auto_bootstrap_if_empty(self) -> None:
        """若数据库无任何账号且种子 JSON 存在，自动执行无感迁移"""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(1) FROM tb_accounts;")
            count = cursor.fetchone()[0]
            if count == 0 and os.path.exists(self.seed_json_path):
                logger.info(
                    "配置仓储 tb_accounts 为空，检测到种子文件 %s，正在执行自动引导迁移...",
                    self.seed_json_path,
                )
                self.bootstrap_from_json(self.seed_json_path)

    def bootstrap_from_json(self, json_path: str) -> int:
        """从 JSON 配置文件导入账号与日常设置

        Args:
            json_path: 种子 JSON 配置文件路径。

        Returns:
            成功导入的账号数量。
        """
        if not os.path.exists(json_path):
            return 0

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except Exception as e:
            logger.error("读取种子配置文件失败: %s", e)
            return 0

        app_config = ConfigManager.load_from_dict(raw_data)
        imported_count = 0

        for acc in app_config.accounts:
            record = AccountRecord(
                alias=acc.alias,
                platform=acc.platform,
                username=acc.username,
                password=acc.password,
                server=acc.server,
                server_id=acc.server_id,
                server_host=acc.server_host,
                server_port=acc.server_port,
                enabled=acc.enabled,
                hosting_enabled=acc.enabled,
            )
            routine_record = RoutineConfigRecord(
                alias=acc.alias,
                allowed_ingots=0,
                enabled_routines=list(ALL_ROUTINES),
            )
            if self.add_account(record, routine_record):
                imported_count += 1

        logger.info("种子数据迁移完成，共纳管 %d 个平台账号", imported_count)
        return imported_count

    # -------------------------------------------------------------------------
    # 账号实体 CRUD
    # -------------------------------------------------------------------------

    def add_account(
        self,
        account: AccountRecord,
        routine_config: Optional[RoutineConfigRecord] = None,
    ) -> bool:
        """新增账号记录及对应的日常任务配置

        Args:
            account: 账号实体。
            routine_config: 可选的日常任务定制，若未提供则默认全开且零元宝。

        Returns:
            是否添加成功。
        """
        now = time.time()
        created_at = account.created_at or now
        updated_at = account.updated_at or now

        routines = routine_config or RoutineConfigRecord(
            alias=account.alias,
            allowed_ingots=0,
            enabled_routines=list(ALL_ROUTINES),
            updated_at=now,
        )

        with self.connect() as conn:
            try:
                # 1. 写入 tb_accounts
                conn.execute(
                    """
                    INSERT INTO tb_accounts (
                        alias, platform, username, password, server, server_id,
                        server_host, server_port, player_id, enabled, hosting_enabled,
                        evade_state, evade_since, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        account.alias,
                        account.platform,
                        account.username,
                        account.password,
                        account.server,
                        account.server_id,
                        account.server_host,
                        account.server_port,
                        account.player_id,
                        1 if account.enabled else 0,
                        1 if account.hosting_enabled else 0,
                        account.evade_state,
                        account.evade_since,
                        created_at,
                        updated_at,
                    ),
                )
                # 2. 写入关联的 tb_routine_configs
                conn.execute(
                    """
                    INSERT OR REPLACE INTO tb_routine_configs (
                        alias, allowed_ingots, enabled_routines_json, updated_at
                    ) VALUES (?, ?, ?, ?);
                    """,
                    (
                        routines.alias,
                        routines.allowed_ingots,
                        json.dumps(routines.enabled_routines, ensure_ascii=False),
                        now,
                    ),
                )
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                logger.warning("账号别名 %s 已存在，插入被拒绝", account.alias)
                return False

    def get_account(self, alias: str) -> Optional[AccountRecord]:
        """根据别名精确获取单个账号实体

        Args:
            alias: 账号别名。

        Returns:
            账号实体或 None。
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tb_accounts WHERE alias = ?;", (alias,))
            row = cursor.fetchone()
            if not row:
                return None
            return self._row_to_account(row)

    def list_accounts(self, enabled_only: bool = False) -> List[AccountRecord]:
        """查询全量或仅已启用的账号列表

        Args:
            enabled_only: 是否仅返回 enabled=1 的账号。

        Returns:
            账号实体列表（无匹配时保证返回空列表）。
        """
        sql = "SELECT * FROM tb_accounts"
        params: Tuple[Any, ...] = ()
        if enabled_only:
            sql += " WHERE enabled = 1"
        sql += " ORDER BY created_at ASC;"

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [self._row_to_account(row) for row in rows]

    def update_account(self, account: AccountRecord) -> bool:
        """更新账号主体信息

        Args:
            account: 待更新的账号对象。

        Returns:
            是否更新成功。
        """
        now = time.time()
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE tb_accounts SET
                    platform = ?,
                    username = ?,
                    password = ?,
                    server = ?,
                    server_id = ?,
                    server_host = ?,
                    server_port = ?,
                    player_id = ?,
                    enabled = ?,
                    hosting_enabled = ?,
                    evade_state = ?,
                    evade_since = ?,
                    updated_at = ?
                WHERE alias = ?;
                """,
                (
                    account.platform,
                    account.username,
                    account.password,
                    account.server,
                    account.server_id,
                    account.server_host,
                    account.server_port,
                    account.player_id,
                    1 if account.enabled else 0,
                    1 if account.hosting_enabled else 0,
                    account.evade_state,
                    account.evade_since,
                    now,
                    account.alias,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0

    def update_account_player_id(self, alias: str, player_id: int) -> bool:
        """记录或更新账号绑定的真实游戏角色 Player ID

        Args:
            alias: 账号别名。
            player_id: 游戏内角色唯一 ID。

        Returns:
            是否更新成功。
        """
        now = time.time()
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tb_accounts SET player_id = ?, updated_at = ? WHERE alias = ?;",
                (player_id, now, alias),
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_account(self, alias: str) -> bool:
        """根据别名删除账号（级联删除日常配置）

        Args:
            alias: 账号别名。

        Returns:
            是否删除成功。
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tb_accounts WHERE alias = ?;", (alias,))
            conn.commit()
            return cursor.rowcount > 0

    def rename_account_alias(self, old_alias: str, new_alias: str) -> bool:
        """重命名账号别名并级联更新关联日常配置

        Args:
            old_alias: 原账号别名。
            new_alias: 新账号别名。

        Returns:
            是否重命名成功。
        """
        if old_alias == new_alias:
            return True
        with self.connect() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM tb_accounts WHERE alias = ?;", (new_alias,))
                if cursor.fetchone():
                    logger.warning("目标账号别名 '%s' 已存在，重命名被拒绝", new_alias)
                    return False

                cursor.execute("PRAGMA foreign_keys = OFF;")
                cursor.execute(
                    "UPDATE tb_routine_configs SET alias = ? WHERE alias = ?;",
                    (new_alias, old_alias),
                )
                cursor.execute(
                    "UPDATE tb_accounts SET alias = ?, updated_at = ? WHERE alias = ?;",
                    (new_alias, time.time(), old_alias),
                )
                cursor.execute("PRAGMA foreign_keys = ON;")
                conn.commit()
                return cursor.rowcount > 0
            except Exception as e:
                logger.error("重命名账号别名失败 [%s -> %s]: %s", old_alias, new_alias, e)
                return False


    def set_hosting_state(self, alias: str, hosting_enabled: bool) -> bool:
        """更新长连接托管开关状态

        Args:
            alias: 账号别名。
            hosting_enabled: 是否启用后台托管长连接。

        Returns:
            是否修改成功。
        """
        now = time.time()
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE tb_accounts SET
                    hosting_enabled = ?,
                    updated_at = ?
                WHERE alias = ?;
                """,
                (1 if hosting_enabled else 0, now, alias),
            )
            conn.commit()
            return cursor.rowcount > 0

    def set_evade_state(
        self,
        alias: str,
        evade_state: str,
        evade_since: Optional[float] = None,
    ) -> bool:
        """更新防互踢避让状态

        Args:
            alias: 账号别名。
            evade_state: 状态值 ("none" | "evading")。
            evade_since: 避让开始时间戳（若未指定且状态为 evading 则取当前时间）。

        Returns:
            是否更新成功。
        """
        now = time.time()
        since = evade_since if evade_since is not None else (now if evade_state == "evading" else 0.0)

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE tb_accounts SET
                    evade_state = ?,
                    evade_since = ?,
                    updated_at = ?
                WHERE alias = ?;
                """,
                (evade_state, since, now, alias),
            )
            conn.commit()
            return cursor.rowcount > 0

    # -------------------------------------------------------------------------
    # 账号级 35 项日常子任务配置
    # -------------------------------------------------------------------------

    def get_routine_config(self, alias: str) -> RoutineConfigRecord:
        """获取账号级独立日常配置（未配置则返回全开默认值）

        Args:
            alias: 账号别名。

        Returns:
            RoutineConfigRecord 实体。
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tb_routine_configs WHERE alias = ?;", (alias,))
            row = cursor.fetchone()
            if not row:
                return RoutineConfigRecord(
                    alias=alias,
                    allowed_ingots=0,
                    enabled_routines=list(ALL_ROUTINES),
                )

            try:
                routines = json.loads(row["enabled_routines_json"])
            except Exception:
                routines = list(ALL_ROUTINES)

            return RoutineConfigRecord(
                alias=row["alias"],
                allowed_ingots=row["allowed_ingots"],
                enabled_routines=routines,
                updated_at=row["updated_at"],
            )

    def save_routine_config(self, config: RoutineConfigRecord) -> bool:
        """持久化保存账号独立日常配置

        Args:
            config: 日常配置实体。

        Returns:
            是否保存成功。
        """
        now = time.time()
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO tb_routine_configs (
                    alias, allowed_ingots, enabled_routines_json, updated_at
                ) VALUES (?, ?, ?, ?)
                ON CONFLICT(alias) DO UPDATE SET
                    allowed_ingots = excluded.allowed_ingots,
                    enabled_routines_json = excluded.enabled_routines_json,
                    updated_at = excluded.updated_at;
                """,
                (
                    config.alias,
                    config.allowed_ingots,
                    json.dumps(config.enabled_routines, ensure_ascii=False),
                    now,
                ),
            )
            conn.commit()
            return True

    # -------------------------------------------------------------------------
    # 系统级键值设置
    # -------------------------------------------------------------------------

    def get_setting(self, key: str, default: str = "") -> str:
        """获取系统参数值

        Args:
            key: 参数键。
            default: 默认回退值。

        Returns:
            配置值字符串。
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM tb_system_settings WHERE key = ?;", (key,))
            row = cursor.fetchone()
            if not row or row["value"] is None:
                return default
            return str(row["value"])

    def set_setting(self, key: str, value: str) -> bool:
        """设置系统参数值

        Args:
            key: 参数键。
            value: 参数值。

        Returns:
            是否设置成功。
        """
        now = time.time()
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO tb_system_settings (key, value, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = excluded.updated_at;
                """,
                (key, value, now),
            )
            conn.commit()
            return True

    # -------------------------------------------------------------------------
    # 辅助与向后兼容转换
    # -------------------------------------------------------------------------

    def to_app_config(self) -> AppConfig:
        """将当前数据库全量账号与配置转换为内存态 AppConfig 对象"""
        accounts = self.list_accounts()
        account_configs = [acc.to_account_config() for acc in accounts]

        heartbeat_interval = float(self.get_setting("heartbeat_interval_sec", "3.0"))
        enable_heartbeat = self.get_setting("enable_heartbeat", "true").lower() == "true"
        enable_auto_routine = self.get_setting("enable_auto_routine", "true").lower() == "true"

        settings = SettingsConfig(
            heartbeat_interval_sec=heartbeat_interval,
            enable_heartbeat=enable_heartbeat,
            enable_auto_routine=enable_auto_routine,
        )

        return AppConfig(settings=settings, accounts=account_configs)

    def _row_to_account(self, row: sqlite3.Row) -> AccountRecord:
        """将 sqlite3.Row 转换为强类型 AccountRecord"""
        return AccountRecord(
            alias=row["alias"],
            platform=row["platform"],
            username=row["username"],
            password=row["password"],
            server=row["server"],
            server_id=row["server_id"],
            server_host=row["server_host"],
            server_port=row["server_port"],
            player_id=row["player_id"] if "player_id" in row.keys() else 0,
            enabled=bool(row["enabled"]),
            hosting_enabled=bool(row["hosting_enabled"]),
            evade_state=row["evade_state"],
            evade_since=row["evade_since"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
