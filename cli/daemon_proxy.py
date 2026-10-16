"""中央服务代理 (Central Daemon Proxy) 客户端与回退解析器

当中央常驻服务 (FastAPI Web Daemon) 在线时，将命令行交互与查询透明代理至 Web API，
彻底规避多进程重复建立 Socket 长连接导致的顶号与互踢冲突；
当中央服务离线时，安全回退到本地 SQLite 自治存储独立执行。

@author Ateng
@since 2026-10-16
"""

import logging
import os
from typing import Optional, Dict, Any, List

import httpx

from services.query_models import (
    PlayerAssetDTO,
    RoleDTO,
    AssistantDailyDTO,
    AssistantDailyItemDTO,
    AssistantLivenessBoxDTO,
    InventoryItemDTO,
    PackSummaryDTO,
    FullTelemetryDTO,
)
from storage.config_db import ConfigDatabase, AccountRecord

logger = logging.getLogger(__name__)


class DaemonProxy:
    """中央服务代理客户端

    @author Ateng
    @since 2026-10-16
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
    ) -> None:
        """初始化代理客户端

        Args:
            base_url: 中央 Web 服务地址 (优先读取 SXD_WEB_URL 环境变量，默认 http://127.0.0.1:8000)。
            token: 访问口令 (优先读取 SXD_WEB_TOKEN 环境变量)。
        """
        env_url = os.environ.get("SXD_WEB_URL", "").strip()
        self.base_url = (base_url or env_url or "http://127.0.0.1:8000").rstrip("/")
        
        env_token = os.environ.get("SXD_WEB_TOKEN", "").strip()
        self.token = token if token is not None else env_token

    @property
    def _headers(self) -> Dict[str, str]:
        """组装鉴权头字典"""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def is_alive(self, timeout_sec: float = 1.0) -> bool:
        """探测中央守护服务是否在线

        Args:
            timeout_sec: 探测超时时间 (秒)。

        Returns:
            在线返回 True，离线或超时返回 False。
        """
        url = f"{self.base_url}/api/health"
        try:
            resp = httpx.get(url, timeout=timeout_sec)
            return resp.status_code == 200
        except Exception:
            return False

    def query_telemetry(self, alias: str, timeout_sec: float = 5.0) -> Optional[Dict[str, Any]]:
        """向中央服务代理查询指定账号全景遥测数据 (资产、伙伴、背包快照)

        Args:
            alias: 账号别名。
            timeout_sec: 超时时间 (秒)。

        Returns:
            遥测数据字典或 None。
        """
        url = f"{self.base_url}/api/accounts/{alias}/telemetry"
        try:
            resp = httpx.get(url, headers=self._headers, timeout=timeout_sec)
            if resp.status_code == 200:
                return resp.json()
            logger.warning("代理查询遥测失败 [%s]: HTTP %d", alias, resp.status_code)
        except Exception as exc:
            logger.warning("代理查询遥测异常 [%s]: %s", alias, exc)
        return None

    def query_assistant(self, alias: str, timeout_sec: float = 5.0) -> Optional[Dict[str, Any]]:
        """向中央服务代理查询指定账号小助手日常活跃度与宝箱进度

        Args:
            alias: 账号别名。
            timeout_sec: 超时时间 (秒)。

        Returns:
            小助手数据字典或 None。
        """
        url = f"{self.base_url}/api/accounts/{alias}/assistant"
        try:
            resp = httpx.get(url, headers=self._headers, timeout=timeout_sec)
            if resp.status_code == 200:
                return resp.json()
            logger.warning("代理查询小助手失败 [%s]: HTTP %d", alias, resp.status_code)
        except Exception as exc:
            logger.warning("代理查询小助手异常 [%s]: %s", alias, exc)
        return None

    def trigger_routine(
        self, alias: str, force: bool = False, timeout_sec: float = 5.0
    ) -> Dict[str, Any]:
        """向中央服务远程下发触发账号日常任务流水线

        Args:
            alias: 账号别名。
            force: 是否在避让状态下强制穿透触发。
            timeout_sec: 超时时间 (秒)。

        Returns:
            调度结果响应字典。
        """
        url = f"{self.base_url}/api/accounts/{alias}/routine/trigger"
        try:
            resp = httpx.post(
                url,
                json={"force": force},
                headers=self._headers,
                timeout=timeout_sec,
            )
            return resp.json()
        except Exception as exc:
            logger.error("代理触发日常流水线异常 [%s]: %s", alias, exc)
            return {"success": False, "status": "error", "message": str(exc)}

    def list_accounts(self, timeout_sec: float = 5.0) -> List[Dict[str, Any]]:
        """向中央服务查询纳管的账号列表

        Args:
            timeout_sec: 超时时间 (秒)。

        Returns:
            账号简要信息列表。
        """
        url = f"{self.base_url}/api/accounts"
        try:
            resp = httpx.get(url, headers=self._headers, timeout=timeout_sec)
            if resp.status_code == 200:
                return resp.json()
        except Exception as exc:
            logger.warning("代理获取账号列表异常: %s", exc)
        return []

    # ==================== DTO 转换模型桥接 ====================

    @staticmethod
    def convert_to_asset_dto(telemetry: Dict[str, Any]) -> PlayerAssetDTO:
        """将 Web 遥测字典转为 PlayerAssetDTO"""
        return PlayerAssetDTO(
            player_id=telemetry.get("player_id", 0),
            nickname=telemetry.get("nickname", ""),
            level=telemetry.get("level", 1),
            vip_level=telemetry.get("vip_level", 0),
            coins=telemetry.get("coins", 0),
            ingots=telemetry.get("ingots", 0),
            power=telemetry.get("power", 0),
            max_power=telemetry.get("max_power", 200),
            fame=telemetry.get("fame", 0),
            experience=telemetry.get("experience", 0),
            max_experience=telemetry.get("max_experience", 0),
            town_id=telemetry.get("town_id", 1),
            town_name=telemetry.get("town_name", ""),
            mission_key=telemetry.get("mission_key", 0),
        )

    @staticmethod
    def convert_to_roles_dto(telemetry: Dict[str, Any]) -> List[RoleDTO]:
        """将 Web 遥测字典转为 RoleDTO 列表"""
        roles = []
        for r in telemetry.get("roles", []):
            roles.append(
                RoleDTO(
                    role_id=r.get("role_id", 0),
                    player_role_id=r.get("player_role_id", 0),
                    name=r.get("name", "伙伴"),
                    level=r.get("level", 1),
                    is_deployed=r.get("is_deployed", False),
                    health=r.get("health", 0),
                    max_health=r.get("max_health", 0),
                    role_job=r.get("role_job", ""),
                    realm_level=r.get("realm_level", 0),
                )
            )
        return roles

    @staticmethod
    def convert_to_assistant_dto(data: Dict[str, Any]) -> AssistantDailyDTO:
        """将 Web 小助手数据字典转为 AssistantDailyDTO"""
        items = [
            AssistantDailyItemDTO(
                item_id=it.get("item_id", 0),
                name=it.get("name", ""),
                completed_count=it.get("completed_count", 0),
                total_quota=it.get("total_quota", 1),
                is_completed=it.get("is_completed", False),
            )
            for it in data.get("items", [])
        ]
        boxes = [
            AssistantLivenessBoxDTO(
                box_id=b.get("box_id", 0),
                required_liveness=b.get("required_liveness", 0),
                status=b.get("status", 2),
                status_desc=b.get("status_desc", "未达标"),
            )
            for b in data.get("boxes", [])
        ]
        return AssistantDailyDTO(
            current_liveness=data.get("current_liveness", 0),
            max_liveness=data.get("max_liveness", 100),
            items=items,
            boxes=boxes,
        )

    @staticmethod
    def convert_to_pack_dto(telemetry: Dict[str, Any]) -> PackSummaryDTO:
        """将 Web 遥测字典转为 PackSummaryDTO"""
        items = [
            InventoryItemDTO(
                grid_id=it.get("grid_id", 0),
                item_id=it.get("item_id", 0),
                name=it.get("name", ""),
                count=it.get("count", 0),
                item_type=it.get("item_type", 0),
                type_desc=it.get("type_desc", "道具"),
            )
            for it in telemetry.get("inventory", [])
        ]
        pack_used = len(items)
        return PackSummaryDTO(
            pack_used=pack_used,
            pack_capacity=100,
            warehouse_used=0,
            warehouse_capacity=100,
            items=items,
        )

    @classmethod
    def convert_to_telemetry_dto(
        cls, telemetry: Dict[str, Any], assistant_data: Optional[Dict[str, Any]] = None
    ) -> FullTelemetryDTO:
        """组合转换为 FullTelemetryDTO"""
        assets = cls.convert_to_asset_dto(telemetry)
        roles = cls.convert_to_roles_dto(telemetry)
        pack = cls.convert_to_pack_dto(telemetry)
        assistant = cls.convert_to_assistant_dto(assistant_data) if assistant_data else None
        return FullTelemetryDTO(
            assets=assets,
            roles=roles,
            assistant=assistant,
            pack=pack,
        )


def resolve_account_from_storage(
    alias: Optional[str] = None,
    db_path: Optional[str] = None,
) -> Optional[AccountRecord]:
    """从本地 SQLite 配置数据库中解析账号 (离线降级自治时使用)

    Args:
        alias: 账号别名（若为 None 则查找首个已启用的账号）。
        db_path: 数据库文件路径（默认 data/config.sqlite）。

    Returns:
        AccountRecord 或 None。
    """
    target_path = db_path or os.path.join("data", "config.sqlite")
    if not os.path.exists(target_path):
        return None

    try:
        db = ConfigDatabase(db_path=target_path, auto_bootstrap=False)
        if alias:
            return db.get_account(alias)
        accounts = db.list_accounts()
        for a in accounts:
            if a.enabled:
                return a
        return accounts[0] if accounts else None
    except Exception as exc:
        logger.warning("从 SQLite 解析账号异常: %s", exc)
        return None
