"""神仙道全量静态协议元数据库 SQLite 驱动与查询仓储

负责将 880 模块、8,719 个 Action 及 13,765 个常量的静态元数据
在首次冷启动时自动转储为只读 SQLite 数据库，并提供毫秒级全文检索与实体点查仓储接口。

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
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Iterator

logger = logging.getLogger(__name__)

DEFAULT_DB_PATH = os.path.join("data", "protocol_manifest.db")
DEFAULT_JSON_PATH = os.path.join("protocol", "manifest", "all_modules_manifest.json")


@dataclass
class ModuleMeta:
    """协议模块元数据实体

    @author Ateng
    @since 2026-10-16
    """

    module_id: int
    name: str
    action_count: int = 0
    constant_count: int = 0


@dataclass
class ActionMeta:
    """协议动作元数据实体

    @author Ateng
    @since 2026-10-16
    """

    module_id: int
    action_id: int
    name: str
    request_types: List[Any] = field(default_factory=list)
    response_types: List[Any] = field(default_factory=list)


@dataclass
class ConstantMeta:
    """协议常量元数据实体

    @author Ateng
    @since 2026-10-16
    """

    module_id: int
    name: str
    value: int


class ProtocolDatabase:
    """协议字典 SQLite 数据库连接与自检转储引擎

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self, db_path: Optional[str] = None, json_path: Optional[str] = None) -> None:
        self.db_path = db_path or DEFAULT_DB_PATH
        self.json_path = json_path or DEFAULT_JSON_PATH
        self._ensure_ingested()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        """获取安全的受管数据库连接 (上下文退出时自动关闭物理句柄)"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def get_connection(self) -> Iterator[sqlite3.Connection]:
        """获取安全受管数据库连接别名"""
        return self.connect()

    def _ensure_ingested(self) -> None:
        """自检数据库完整性，若不存在则自动执行一次性热转储"""
        if os.path.exists(self.db_path) and os.path.getsize(self.db_path) > 0:
            logger.debug("协议字典数据库已存在: %s", self.db_path)
            return

        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"协议元数据源 JSON 文件未找到: {self.json_path}")

        logger.info("首次初始化协议字典数据库，正在从 JSON 热转储: %s -> %s", self.json_path, self.db_path)
        t0 = time.perf_counter()

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        modules_data = data.get("modules", {})

        conn = sqlite3.connect(self.db_path)
        try:
            with conn:
                # 1. 创建核心元数据表与 B-Tree 索引
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tb_modules (
                        module_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        action_count INTEGER NOT NULL DEFAULT 0,
                        constant_count INTEGER NOT NULL DEFAULT 0
                    )
                    """
                )
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tb_actions (
                        module_id INTEGER NOT NULL,
                        action_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        request_types TEXT NOT NULL,
                        response_types TEXT NOT NULL,
                        PRIMARY KEY (module_id, action_id)
                    )
                    """
                )
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tb_constants (
                        module_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        value INTEGER NOT NULL,
                        PRIMARY KEY (module_id, name)
                    )
                    """
                )
                conn.execute("CREATE INDEX IF NOT EXISTS idx_actions_name ON tb_actions(name)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_actions_mod ON tb_actions(module_id)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_constants_name ON tb_constants(name)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_constants_mod ON tb_constants(module_id)")

                # 2. 批量组装导入批次数据
                mod_rows = []
                act_rows = []
                const_rows = []

                for mod_key, mod_info in modules_data.items():
                    mod_id = int(mod_info.get("module", mod_key))
                    mod_name = mod_info.get("name", "")
                    actions = mod_info.get("actions", {})
                    constants = mod_info.get("constants", {})

                    mod_rows.append((mod_id, mod_name, len(actions), len(constants)))

                    for act_key, act_info in actions.items():
                        act_id = int(act_info.get("action", act_key))
                        act_name = act_info.get("name", "")
                        req_json = json.dumps(act_info.get("request", []))
                        resp_json = json.dumps(act_info.get("response", []))
                        act_rows.append((mod_id, act_id, act_name, req_json, resp_json))

                    for const_name, const_val in constants.items():
                        const_rows.append((mod_id, str(const_name), int(const_val)))

                # 3. 高性能批量事务写入
                conn.executemany(
                    "INSERT OR REPLACE INTO tb_modules VALUES (?, ?, ?, ?)",
                    mod_rows,
                )
                conn.executemany(
                    "INSERT OR REPLACE INTO tb_actions VALUES (?, ?, ?, ?, ?)",
                    act_rows,
                )
                conn.executemany(
                    "INSERT OR REPLACE INTO tb_constants VALUES (?, ?, ?)",
                    const_rows,
                )

            elapsed = time.perf_counter() - t0
            logger.info(
                "协议字典转储完成: %d 模块, %d 动作, %d 常量, 耗时 %.3f 秒",
                len(mod_rows),
                len(act_rows),
                len(const_rows),
                elapsed,
            )
        finally:
            conn.close()


class ProtocolRepository:
    """协议元数据查询仓储服务

    提供模块、动作、常量的强类型点查、模糊检索与参数签名提取接口。

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self, db: Optional[ProtocolDatabase] = None) -> None:
        self.db = db or ProtocolDatabase()

    def get_module(self, module_id: int) -> Optional[ModuleMeta]:
        """根据模块编号查询模块元数据"""
        with self.db.connect() as conn:
            cursor = conn.execute(
                "SELECT module_id, name, action_count, constant_count FROM tb_modules WHERE module_id = ?",
                (module_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return ModuleMeta(
                module_id=row["module_id"],
                name=row["name"],
                action_count=row["action_count"],
                constant_count=row["constant_count"],
            )

    def list_modules(self) -> List[ModuleMeta]:
        """列出所有已纳管的协议模块"""
        with self.db.connect() as conn:
            cursor = conn.execute(
                "SELECT module_id, name, action_count, constant_count FROM tb_modules ORDER BY module_id ASC"
            )
            return [
                ModuleMeta(
                    module_id=r["module_id"],
                    name=r["name"],
                    action_count=r["action_count"],
                    constant_count=r["constant_count"],
                )
                for r in cursor.fetchall()
            ]

    def get_action(self, module_id: int, action_id: int) -> Optional[ActionMeta]:
        """查询指定模块内的特定动作定义"""
        with self.db.connect() as conn:
            cursor = conn.execute(
                "SELECT module_id, action_id, name, request_types, response_types FROM tb_actions WHERE module_id = ? AND action_id = ?",
                (module_id, action_id),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return ActionMeta(
                module_id=row["module_id"],
                action_id=row["action_id"],
                name=row["name"],
                request_types=json.loads(row["request_types"]),
                response_types=json.loads(row["response_types"]),
            )

    def get_actions_by_module(self, module_id: int) -> List[ActionMeta]:
        """获取指定模块下所有动作定义列表"""
        with self.db.connect() as conn:
            cursor = conn.execute(
                "SELECT module_id, action_id, name, request_types, response_types FROM tb_actions WHERE module_id = ? ORDER BY action_id ASC",
                (module_id,),
            )
            return [
                ActionMeta(
                    module_id=r["module_id"],
                    action_id=r["action_id"],
                    name=r["name"],
                    request_types=json.loads(r["request_types"]),
                    response_types=json.loads(r["response_types"]),
                )
                for r in cursor.fetchall()
            ]

    def search_actions(self, keyword: str, limit: int = 50) -> List[ActionMeta]:
        """按动作名称模糊搜索动作定义"""
        if not keyword:
            return []
        pattern = f"%{keyword}%"
        with self.db.connect() as conn:
            cursor = conn.execute(
                "SELECT module_id, action_id, name, request_types, response_types FROM tb_actions WHERE name LIKE ? ORDER BY module_id ASC, action_id ASC LIMIT ?",
                (pattern, limit),
            )
            return [
                ActionMeta(
                    module_id=r["module_id"],
                    action_id=r["action_id"],
                    name=r["name"],
                    request_types=json.loads(r["request_types"]),
                    response_types=json.loads(r["response_types"]),
                )
                for r in cursor.fetchall()
            ]

    def get_constant(self, module_id: int, name: str) -> Optional[int]:
        """查询特定模块下的常量数值"""
        with self.db.connect() as conn:
            cursor = conn.execute(
                "SELECT value FROM tb_constants WHERE module_id = ? AND name = ?",
                (module_id, name),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return int(row["value"])

    def get_constants_by_module(self, module_id: int) -> Dict[str, int]:
        """获取指定模块的所有常量字典映射"""
        with self.db.connect() as conn:
            cursor = conn.execute(
                "SELECT name, value FROM tb_constants WHERE module_id = ? ORDER BY name ASC",
                (module_id,),
            )
            return {r["name"]: int(r["value"]) for r in cursor.fetchall()}

    def search_constants(self, keyword: str, limit: int = 50) -> List[ConstantMeta]:
        """按常量标识符模糊搜索常量"""
        if not keyword:
            return []
        pattern = f"%{keyword}%"
        with self.db.connect() as conn:
            cursor = conn.execute(
                "SELECT module_id, name, value FROM tb_constants WHERE name LIKE ? ORDER BY module_id ASC, name ASC LIMIT ?",
                (pattern, limit),
            )
            return [
                ConstantMeta(
                    module_id=r["module_id"],
                    name=r["name"],
                    value=int(r["value"]),
                )
                for r in cursor.fetchall()
            ]
