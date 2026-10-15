"""神仙道 Web 自动化登录与网关凭据提取模块

实现完整的 3 步全自动 Web 登录流程：
1. 请求 member 站点 login.php 完成账号鉴权，获取 Session 与 Cookie。
2. 请求 play.php 获取区服入场参数集 (regdate, pi, hash, time, non_kid 等)。
3. 请求目标区服 index_wd.php 换取最新的动态网关 IP、Port 与长连接 Token Hash。

@author Ateng
@since 2026-10-15
"""

import http.cookiejar
import json
import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any
import urllib.request
import urllib.parse
from json import JSONDecoder

logger = logging.getLogger(__name__)


@dataclass
class GatewayCredentials:
    """网关鉴权与连接凭据模型

    @author Ateng
    @since 2026-10-15
    """

    server_host: str
    server_port: int
    player_name: str
    hash_code: str
    time: str
    platform: str
    server_id: int
    nickname: str = ""


class WebAuthFetcher:
    """Web 自动化鉴权调度器

    @author Ateng
    @since 2026-10-15
    """

    @classmethod
    def auto_login(
        cls,
        username: str,
        password: str,
        server: str = "s813",
        app: str = "sxd",
        timeout_sec: float = 10.0,
    ) -> Optional[GatewayCredentials]:
        """全自动执行账号登录与网关令牌换取

        Args:
            username: 平台账号用户名。
            password: 账号密码。
            server: 目标游戏区服代号 (例如 's813')。
            app: 游戏标识 (默认为 'sxd')。
            timeout_sec: 各步骤网络超时秒数。

        Returns:
            若全流程成功返回包含最新 Token 的 GatewayCredentials，否则返回 None。
        """
        cookie_jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

        try:
            # 步骤 1: 平台账号鉴权登录
            logger.info("执行 Web 登录步骤 1: 账号凭据鉴权 (%s)...", username)
            login_params = urllib.parse.urlencode({
                "password": password,
                "captcha": "",
                "app": app,
                "username": username,
            })
            login_url = f"http://member.fengwanyx.3fangyuan.com//api/account/login.php?{login_params}"
            req1 = urllib.request.Request(login_url, headers={
                "User-Agent": "Shockwave Flash",
                "x-flash-version": "10,2,153,1",
            })

            with opener.open(req1, timeout=timeout_sec) as resp1:
                res_body1 = resp1.read().decode("utf-8", errors="replace")
                data1 = json.loads(res_body1)
                if not data1.get("username"):
                    logger.error("Web 登录步骤 1 失败，返回值: %s", res_body1)
                    return None

            logger.info("Web 登录步骤 1 成功，已获取用户会话 Cookie")

            # 步骤 2: 获取区服入场参数 (play.php)
            logger.info("执行 Web 登录步骤 2: 拉取区服 %s 入场参数...", server)
            play_params = urllib.parse.urlencode({
                "app": app,
                "server": server,
                "username": username,
            })
            play_url = f"http://member.fengwanyx.3fangyuan.com//api/account/play.php?{play_params}"
            req2 = urllib.request.Request(play_url, headers={
                "User-Agent": "Shockwave Flash",
                "x-flash-version": "10,2,153,1",
            })

            with opener.open(req2, timeout=timeout_sec) as resp2:
                res_body2 = resp2.read().decode("utf-8", errors="replace")
                data2 = json.loads(res_body2)
                if "hash" not in data2 or "time" not in data2:
                    logger.error("Web 登录步骤 2 失败，未能获取入场 hash: %s", res_body2)
                    return None

            logger.info("Web 登录步骤 2 成功，获取临时入场参数")

            # 步骤 3: 向大区主站换取最终网关 IP 与最新 Socket Token (index_wd.php)
            logger.info("执行 Web 登录步骤 3: 换取目标区服 Socket 网关凭据...")
            index_query = urllib.parse.urlencode(data2)
            index_url = f"http://{server}.sxd.fengwanyx.com/index_wd.php?{index_query}"
            req3 = urllib.request.Request(index_url, headers={
                "User-Agent": "Shockwave Flash",
                "x-flash-version": "10,2,153,1",
            })

            with opener.open(req3, timeout=timeout_sec) as resp3:
                res_body3 = resp3.read().decode("utf-8", errors="replace")

            # 从页面响应中提取 JSON
            start_idx = res_body3.find('{"code":1')
            if start_idx == -1:
                logger.error("Web 登录步骤 3 失败，页面中未发现成功状态 JSON: %s", res_body3[:300])
                return None

            obj, _ = JSONDecoder().raw_decode(res_body3[start_idx:])
            gw_data = obj.get("data", {})

            creds = GatewayCredentials(
                server_host=gw_data.get("ip", "9x656.sxdweb.xd.com"),
                server_port=int(gw_data.get("port", 8381)),
                player_name=gw_data.get("player_name", username),
                hash_code=gw_data.get("hash_code", ""),
                time=str(gw_data.get("time", "")),
                platform="fengwanyx",
                server_id=25268,
                nickname="梦一场",
            )

            logger.info(
                "全自动 Web 登录成功！获取动态网关: %s:%d, 用户: %s, 会话时间戳: %s",
                creds.server_host,
                creds.server_port,
                creds.player_name,
                creds.time,
            )
            return creds

        except Exception as exc:
            logger.error("全自动 Web 登录流程异常: %s", exc)
            return None

    @staticmethod
    def from_config_dict(conf: Dict[str, Any]) -> GatewayCredentials:
        """从本地配置字典中装载凭据 (静态备用模式)"""
        static_c = conf.get("static_credentials", {})
        return GatewayCredentials(
            server_host=static_c.get("server_host", "9x656.sxdweb.xd.com"),
            server_port=int(static_c.get("server_port", 8381)),
            player_name=static_c.get("player_name", ""),
            hash_code=static_c.get("hash_code", ""),
            time=str(static_c.get("time", "")),
            platform=static_c.get("platform", "fengwanyx"),
            server_id=int(static_c.get("server_id", 25268)),
            nickname=static_c.get("nickname", ""),
        )
