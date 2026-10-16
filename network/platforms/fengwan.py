"""疯玩游戏平台鉴权适配器 (Fengwan Platform Auth Provider)

实现疯玩游戏 (fengwanyx) 平台专有的三步 Web 登录与网关 Token 换取流水线。

@author Ateng
@since 2026-10-16
"""

import http.cookiejar
import json
from json.decoder import JSONDecoder
import logging
import urllib.parse
import urllib.request
from typing import Optional, TYPE_CHECKING

from network.platforms.base import BasePlatformAuthProvider

if TYPE_CHECKING:
    from core.config import AccountConfig
    from network.web_auth import GatewayCredentials

logger = logging.getLogger("fengwan_auth")


class FengwanAuthProvider(BasePlatformAuthProvider):
    """疯玩游戏 (fengwanyx) 平台鉴权适配器"""

    @property
    def platform_name(self) -> str:
        return "fengwanyx"

    def auto_login(self, account: "AccountConfig", timeout_sec: float = 10.0) -> Optional["GatewayCredentials"]:
        """执行疯玩平台全自动登录并换取新鲜的 Socket 网关凭据

        包含 3 步标准流程：
        // 1. 平台账号凭据鉴权获取用户会话 Cookie
        // 2. 请求区服入场参数获取临时签名 hash 与时间戳
        // 3. 向大区主站换取最终网关 IP、端口与当次 Socket Token
        """
        from network.web_auth import GatewayCredentials

        username = account.username
        password = account.password
        server = account.server or "s813"
        app = "sxd"

        cookie_jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

        try:
            # 1. 平台账号鉴权登录
            logger.info("[%s] 执行疯玩平台登录步骤 1: 账号凭据鉴权 (%s)...", account.display_name, username)
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
                    logger.error("[%s] 疯玩平台登录步骤 1 失败，返回值: %s", account.display_name, res_body1)
                    return None

            logger.info("[%s] 疯玩平台登录步骤 1 成功，已获取用户会话 Cookie", account.display_name)

            # 2. 获取区服入场参数 (play.php)
            logger.info("[%s] 执行疯玩平台登录步骤 2: 拉取区服 %s 入场参数...", account.display_name, server)
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
                    logger.error("[%s] 疯玩平台登录步骤 2 失败，未能获取入场 hash: %s", account.display_name, res_body2)
                    return None

            logger.info("[%s] 疯玩平台登录步骤 2 成功，获取临时入场参数", account.display_name)

            # 3. 向大区主站换取最终网关 IP 与最新 Socket Token (index_wd.php)
            logger.info("[%s] 执行疯玩平台登录步骤 3: 换取目标区服 Socket 网关凭据...", account.display_name)
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
                logger.error("[%s] 疯玩平台登录步骤 3 失败，页面中未发现成功状态 JSON: %s", account.display_name, res_body3[:300])
                return None

            obj, _ = JSONDecoder().raw_decode(res_body3[start_idx:])
            gw_data = obj.get("data", {})

            # 安全解析 server_id (部分区服可能返回字符串如 'fengwanyx_s813')
            raw_sid = gw_data.get("server_id", 25268)
            try:
                sid_val = int(raw_sid)
            except (ValueError, TypeError):
                sid_val = 25268

            creds = GatewayCredentials(
                server_host=gw_data.get("ip", "9x656.sxdweb.xd.com"),
                server_port=int(gw_data.get("port", 8381)),
                player_name=gw_data.get("player_name", username),
                hash_code=gw_data.get("hash_code", ""),
                time=str(gw_data.get("time", "")),
                platform="fengwanyx",
                server_id=sid_val,
                nickname=account.alias or username,
            )

            logger.info(
                "[%s] 疯玩平台全自动登录成功！动态网关: %s:%d, 用户: %s, 时间戳: %s",
                account.display_name,
                creds.server_host,
                creds.server_port,
                creds.player_name,
                creds.time,
            )
            return creds

        except Exception as exc:
            logger.error("[%s] 疯玩平台全自动登录流程异常: %s", account.display_name, exc)
            return None
