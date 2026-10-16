"""神仙道配置管理与多账号实体模型

支持配置文件读取、多账号配置、Docker 环境变量动态注入与占位符展开。
全面兼容存量单账号配置格式，实现无缝平滑升级。

@author Ateng
@since 2026-10-16
"""

import json
import logging
import os
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_ENV_VAR_PATTERN = re.compile(r"\$\{([A-Za-z0-9_]+)(?::-([^}]*))?\}")


def expand_env_vars(data: Any) -> Any:
    """递归展开配置中的环境变量占位符 (${VAR_NAME} 或 ${VAR_NAME:-default})
    
    Args:
        data: 输入的配置数据对象 (字符串、字典、列表或原始标量)。

    Returns:
        替换后的配置数据对象。
    """
    if isinstance(data, str):
        def _replace_match(match: re.Match) -> str:
            var_name = match.group(1)
            default_val = match.group(2) if match.group(2) is not None else ""
            return os.environ.get(var_name, default_val)

        return _ENV_VAR_PATTERN.sub(_replace_match, data)
    elif isinstance(data, dict):
        return {k: expand_env_vars(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [expand_env_vars(item) for item in data]
    return data


@dataclass
class AccountConfig:
    """平台账号配置实体
    
    @author Ateng
    @since 2026-10-16
    """

    username: str
    password: str = ""
    server: str = "s813"
    alias: str = ""
    enabled: bool = True
    platform: str = "fengwanyx"
    server_host: Optional[str] = None
    server_port: Optional[int] = None
    server_id: int = 25268
    hash_code: str = ""
    time: str = ""

    def __post_init__(self) -> None:
        if not self.alias:
            self.alias = self.username or "default"

    @property
    def display_name(self) -> str:
        """获取用于日志与看板展示的账号名称"""
        if self.alias and self.alias != self.username:
            return f"{self.alias} ({self.username})"
        return self.username or self.alias or "未命名账号"

    def to_dict(self) -> Dict[str, Any]:
        """将账号配置导出为标准字典结构"""
        d: Dict[str, Any] = {
            "alias": self.alias,
            "username": self.username,
            "password": self.password,
            "server": self.server,
            "enabled": self.enabled,
            "platform": self.platform,
        }
        if self.server_host:
            d["server_host"] = self.server_host
        if self.server_port:
            d["server_port"] = self.server_port
        if self.server_id != 25268:
            d["server_id"] = self.server_id
        if self.hash_code:
            d["hash_code"] = self.hash_code
        if self.time:
            d["time"] = self.time
        return d


@dataclass
class SettingsConfig:
    """全局通用自动化与网络参数设置
    
    @author Ateng
    @since 2026-10-16
    """

    heartbeat_interval_sec: float = 3.0
    enable_heartbeat: bool = True
    enable_auto_routine: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """将设置导出为字典"""
        return {
            "heartbeat_interval_sec": self.heartbeat_interval_sec,
            "enable_heartbeat": self.enable_heartbeat,
            "enable_auto_routine": self.enable_auto_routine,
        }


@dataclass
class AppConfig:
    """应用顶层聚合配置模型
    
    @author Ateng
    @since 2026-10-16
    """

    settings: SettingsConfig = field(default_factory=SettingsConfig)
    accounts: List[AccountConfig] = field(default_factory=list)

    def get_enabled_accounts(self) -> List[AccountConfig]:
        """获取所有已启用的账号列表
        
        Returns:
            启用的账号列表，若无则返回空列表。
        """
        return [acc for acc in self.accounts if acc.enabled]

    @property
    def enabled_accounts(self) -> List[AccountConfig]:
        """获取所有已启用的账号列表属性"""
        return self.get_enabled_accounts()

    def find_account(self, identifier: str) -> Optional[AccountConfig]:
        """根据 alias 或 username 查找账号
        
        Args:
            identifier: 账号别名或平台用户名。

        Returns:
            匹配的账号配置，未找到则返回 None。
        """
        for acc in self.accounts:
            if acc.alias == identifier or acc.username == identifier:
                return acc
        return None

    def to_dict(self) -> Dict[str, Any]:
        """导出全量配置字典"""
        return {
            "settings": self.settings.to_dict(),
            "accounts": [acc.to_dict() for acc in self.accounts],
        }


class ConfigManager:
    """配置加载与生命周期管理器
    
    负责合并文件配置、系统环境变量与 Docker 注入参数，实现平滑降级与向下兼容。
    
    @author Ateng
    @since 2026-10-16
    """

    @classmethod
    def load_from_dict(cls, raw_config: Dict[str, Any]) -> AppConfig:
        """从字典对象解析应用配置 (包含环境变量展开与向后兼容)
        
        Args:
            raw_config: 原始配置字典。

        Returns:
            AppConfig 对象。
        """
        expanded = expand_env_vars(raw_config) if raw_config else {}
        settings_dict = expanded.get("settings") or expanded.get("automation") or {}
        settings = SettingsConfig(
            heartbeat_interval_sec=float(settings_dict.get("heartbeat_interval_sec", 3.0)),
            enable_heartbeat=bool(settings_dict.get("enable_heartbeat", True)),
            enable_auto_routine=bool(settings_dict.get("enable_auto_routine", True)),
        )

        accounts: List[AccountConfig] = []
        if "accounts" in expanded and isinstance(expanded["accounts"], list):
            for item in expanded["accounts"]:
                if isinstance(item, dict):
                    accounts.append(
                        AccountConfig(
                            alias=str(item.get("alias", "")),
                            username=str(item.get("username", "")),
                            password=str(item.get("password", "")),
                            server=str(item.get("server", "s813")),
                            enabled=bool(item.get("enabled", True)),
                            platform=str(item.get("platform", "fengwanyx")),
                            server_host=item.get("server_host"),
                            server_port=int(item["server_port"]) if item.get("server_port") else None,
                            server_id=int(item["server_id"]) if item.get("server_id") else 25268,
                            hash_code=str(item.get("hash_code", "")),
                            time=str(item.get("time", "")),
                        )
                    )

        # 向下兼容旧版单账号配置 (web_auth / static_credentials / credentials / server)
        if not accounts:
            web_conf = expanded.get("web_auth", {})
            static_c = expanded.get("static_credentials", {})
            srv_conf = expanded.get("server", {})
            cred_conf = expanded.get("credentials", {})

            uname = web_conf.get("username") or static_c.get("player_name") or cred_conf.get("player_name", "")
            pwd = web_conf.get("password", "")
            srv = web_conf.get("server", "s813")
            plat = static_c.get("platform", "fengwanyx")

            server_host = static_c.get("server_host")
            server_port = int(static_c["server_port"]) if static_c.get("server_port") else None
            server_id = int(static_c.get("server_id", 25268))
            hash_code = str(static_c.get("hash_code", ""))
            time_val = str(static_c.get("time", ""))

            if not server_host and isinstance(srv_conf, dict):
                server_host = srv_conf.get("host")
                server_port = int(srv_conf["port"]) if srv_conf.get("port") else None

            if uname or server_host:
                accounts.append(
                    AccountConfig(
                        alias="默认账号",
                        username=uname or "default_user",
                        password=pwd,
                        server=srv,
                        enabled=True,
                        platform=plat,
                        server_host=server_host,
                        server_port=server_port,
                        server_id=server_id,
                        hash_code=hash_code,
                        time=time_val,
                    )
                )

        return AppConfig(settings=settings, accounts=accounts)

    @classmethod
    def load(cls, config_path: Optional[str] = "config/config.json") -> AppConfig:
        """从指定路径或环境变量装载全量应用配置
        
        解析优先级:
        1. 优先读取并解析配置文件 (若存在) 并展开 ${VAR} 占位符；
        2. 若提供了 SXD_ACCOUNTS_JSON 环境变量，则合并或覆盖账号列表；
        3. 若无配置文件且检测到单账号 Docker 环境变量 (SXD_USERNAME, SXD_PASSWORD)，自动合成为单账号配置；
        4. 向下兼容旧版 config.json (web_auth / static_credentials 结构)。

        Args:
            config_path: 配置文件相对或绝对路径，默认为 'config/config.json'。

        Returns:
            组装完整的 AppConfig 对象。
        """
        raw_config: Dict[str, Any] = {}

        # 1. 尝试读取文件配置
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    raw_content = json.load(f)
                    raw_config = expand_env_vars(raw_content)
                    logger.debug("已成功读取并展开配置文件: %s", config_path)
            except Exception as exc:
                logger.warning("读取配置文件 %s 异常: %s", config_path, exc)

        app_config = cls.load_from_dict(raw_config)

        # 2. 环境变量覆盖/注入多账号 (SXD_ACCOUNTS_JSON)
        env_accounts_json = os.environ.get("SXD_ACCOUNTS_JSON")
        if env_accounts_json:
            try:
                parsed_json = json.loads(env_accounts_json)
                if isinstance(parsed_json, list):
                    for item in parsed_json:
                        if isinstance(item, dict):
                            app_config.accounts.append(
                                AccountConfig(
                                    alias=str(item.get("alias", "")),
                                    username=str(item.get("username", "")),
                                    password=str(item.get("password", "")),
                                    server=str(item.get("server", "s813")),
                                    enabled=bool(item.get("enabled", True)),
                                    platform=str(item.get("platform", "fengwanyx")),
                                    server_host=item.get("server_host"),
                                    server_port=int(item["server_port"]) if item.get("server_port") else None,
                                )
                            )
                    logger.info("已成功通过环境变量 SXD_ACCOUNTS_JSON 注入 %d 个账号", len(parsed_json))
            except Exception as e:
                logger.warning("解析 SXD_ACCOUNTS_JSON 环境变量失败: %s", e)

        # 3. Docker 单账号零配置直启 (环境变量兜底: SXD_USERNAME, SXD_PASSWORD)
        env_user = os.environ.get("SXD_USERNAME")
        env_pass = os.environ.get("SXD_PASSWORD")
        if env_user and not any(acc.username == env_user for acc in app_config.accounts):
            app_config.accounts.append(
                AccountConfig(
                    alias=os.environ.get("SXD_ALIAS", env_user),
                    username=env_user,
                    password=env_pass or "",
                    server=os.environ.get("SXD_SERVER", "s813"),
                    enabled=True,
                    platform=os.environ.get("SXD_PLATFORM", "fengwanyx"),
                )
            )
            logger.info("已通过系统环境变量 (SXD_USERNAME) 自动生成运行时账号实体: %s", env_user)

        return app_config
