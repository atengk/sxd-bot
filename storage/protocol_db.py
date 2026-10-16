"""神仙道全量静态协议元数据库 SQLite 驱动与查询仓储

集中纳管 880 模块、8,719 个 Action 及 13,765 个常量的静态元数据与项目静态配置 (tb_metadata)，
提供开箱即用的只读 SQLite 连接与毫秒级强类型仓储接口。

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
    """协议字典 SQLite 数据库连接与自检引擎

    @author Ateng
    @since 2026-10-16
    """

    def __init__(
        self,
        db_path: Optional[str] = None,
        json_path: Optional[str] = None,
        manifest_path: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        candidate = db_path
        if not candidate and json_path and json_path.endswith(".db"):
            candidate = json_path
        if not candidate and manifest_path and manifest_path.endswith(".db"):
            candidate = manifest_path

        self.db_path = candidate or DEFAULT_DB_PATH
        self._ensure_exists()

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

    def _ensure_exists(self) -> None:
        """严格自检数据库完整性，若不存在直接抛出明确异常"""
        if not os.path.exists(self.db_path) or os.path.getsize(self.db_path) == 0:
            raise FileNotFoundError(
                f"协议字典数据库未找到或为空: {self.db_path}。该文件由 Git 仓库直接纳管，请检查数据完整性。"
            )
        logger.debug("协议字典数据库验证成功: %s", self.db_path)


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

    get_all_modules = list_modules

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

    def get_metadata(self, key: str) -> Optional[Any]:
        """查询项目通用静态元数据 (自动尝试解析 JSON)"""
        with self.db.connect() as conn:
            cursor = conn.execute("SELECT value FROM tb_metadata WHERE key = ?", (key,))
            row = cursor.fetchone()
            if row is None:
                return None
            raw = row["value"]
            try:
                return json.loads(raw)
            except (ValueError, TypeError):
                return raw

    def set_metadata(self, key: str, value: Any) -> None:
        """写入或更新项目通用静态元数据"""
        val_str = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value)
        with self.db.connect() as conn:
            with conn:
                conn.execute(
                    "CREATE TABLE IF NOT EXISTS tb_metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
                )
                conn.execute(
                    "INSERT OR REPLACE INTO tb_metadata (key, value) VALUES (?, ?)",
                    (key, val_str),
                )

    def get_reverse_assets(self) -> Optional[Dict[str, Any]]:
        """获取逆向工程资产配置元数据"""
        return self.get_metadata("reverse_assets")

    def get_manifest_metadata(self) -> Optional[Dict[str, Any]]:
        """获取协议全景元数据概况信息"""
        return self.get_metadata("manifest_metadata")

    def get_full_manifest_dict(self) -> Dict[str, Any]:
        """按需重构全量协议清单字典 (用于兼容需要旧版全景结构的工具与测试)"""
        meta = self.get_manifest_metadata() or {}
        modules: Dict[str, Any] = {}
        for m in self.list_modules():
            actions: Dict[str, Any] = {}
            for a in self.get_actions_by_module(m.module_id):
                actions[str(a.action_id)] = {
                    "action": a.action_id,
                    "name": a.name,
                    "request": a.request_types,
                    "response": a.response_types,
                }
            constants = self.get_constants_by_module(m.module_id)
            modules[str(m.module_id)] = {
                "module": m.module_id,
                "module_id": m.module_id,
                "name": m.name,
                "class_name": f"Mod_{m.name}_Base",
                "actions": actions,
                "constants": constants,
            }
        return {"metadata": meta, "modules": modules}

