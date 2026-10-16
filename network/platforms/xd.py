"""心动官方平台鉴权提供方 (XD Platform Auth Provider)

基于微端网络抓包逆向还原心动官网 (www.xd.com) 完整鉴权链路：
1. 请求 users/loginService 换取官网登录 Session 与用户 ID；
2. 请求 games/play 换取目标双线大区入场签名；
3. 请求大区主站 index_wd.php 换取最新的长连接网关 IP、Port 与握手 Hash。

@author Ateng
@since 2026-10-16
"""

import http.cookiejar
import json
import logging
from json import JSONDecoder
from typing import Optional, TYPE_CHECKING
import urllib.parse
import urllib.request

from network.platforms.base import BasePlatformAuthProvider

if TYPE_CHECKING:
    from core.config import AccountConfig
    from network.web_auth import GatewayCredentials

logger = logging.getLogger("platform_auth_xd")


class XDPlatformAuthProvider(BasePlatformAuthProvider):
    """心动官方平台鉴权提供方
    
    @author Ateng
    @since 2026-10-16
    """

    @property
    def platform_name(self) -> str:
        return "xd"

    def auto_login(self, account: "AccountConfig", timeout_sec: float = 10.0) -> Optional["GatewayCredentials"]:
        """执行心动官方微端全流程自动登录与网关令牌换取"""
        from network.web_auth import GatewayCredentials

        username = (account.username or "").strip()
        password = (account.password or "").strip()
        server = (account.server or "S3542").strip()

        if not username or not password:
            logger.warning("[%s] 心动官服登录失败: 用户名或密码为空", account.display_name)
            return None

        # 规范化大区标识 (如 '3542' -> 'S3542', 's3542' -> 'S3542')
        if not server.upper().startswith("S"):
            xd_server = f"S{server}"
        else:
            xd_server = server.upper()

        cookie_jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

        try:
            # 1. 心动官网账号鉴权
            logger.info("[%s] 执行心动官网登录步骤 1: 验证账号身份...", account.display_name)
            login_params = urllib.parse.urlencode({
                "data[User][username]": username,
                "data[User][password]": password,
                "data[User][site]": "xd",
                "data[User][remember_me]": "false",
                "app": "sxd",
                "history_amount": 0,
                "captcha_identifier": 0,
                "captcha": "",
                "twoauth": 1,
                "open_twoauth": "true",
            })
            login_url = f"https://www.xd.com/users/loginService?{login_params}"
            req1 = urllib.request.Request(login_url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                "Referer": "https://www.xd.com/",
            })

            with opener.open(req1, timeout=timeout_sec) as resp1:
                res_body1 = resp1.read().decode("utf-8", errors="replace")
                data1 = json.loads(res_body1)
                user_id = str(data1.get("user") or data1.get("id") or "")
                if not user_id:
                    error_msg = data1.get("msg") or data1.get("error") or "用户凭据无效"
                    logger.error("[%s] 心动官网登录步骤 1 失败: %s", account.display_name, error_msg)
                    return None

            logger.info("[%s] 心动官网登录步骤 1 成功，获取用户 UID: %s", account.display_name, user_id)

            # 2. 获取大区直连入场参数 (games/play)
            logger.info("[%s] 执行心动官网登录步骤 2: 拉取区服 %s 入场票据...", account.display_name, xd_server)
            play_url = f"https://www.xd.com/games/play?app=sxd&server={xd_server}&redirect=false"
            req2 = urllib.request.Request(play_url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                "Referer": "https://www.xd.com/",
            })

            with opener.open(req2, timeout=timeout_sec) as resp2:
                res_body2 = resp2.read().decode("utf-8", errors="replace").strip()
                if res_body2.startswith('"') and res_body2.endswith('"'):
                    res_body2 = json.loads(res_body2)

                qs_dict = urllib.parse.parse_qs(res_body2)
                ticket_data = {k: v[0] for k, v in qs_dict.items()}
                if "hash" not in ticket_data or "time" not in ticket_data:
                    logger.error("[%s] 心动官网登录步骤 2 失败，未获取入场 hash: %s", account.display_name, res_body2)
                    return None

            logger.info("[%s] 心动官网登录步骤 2 成功，获取区服临时票据", account.display_name)

            # 3. 向大区微端入口换取最终 TCP 网关与会话 Hash (index_wd.php)
            logger.info("[%s] 执行心动官网登录步骤 3: 换取目标区服 Socket 网关凭据...", account.display_name)
            server_lower = xd_server.lower()
            index_query = urllib.parse.urlencode(ticket_data)
            index_url = f"http://{server_lower}.sxd.xd.com/index_wd.php?{index_query}&format="
            req3 = urllib.request.Request(index_url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
            })

            with opener.open(req3, timeout=timeout_sec) as resp3:
                res_body3 = resp3.read().decode("utf-8", errors="replace")

            start_idx = res_body3.find('{"code":1')
            if start_idx != -1:
                obj, _ = JSONDecoder().raw_decode(res_body3[start_idx:])
            else:
                obj = json.loads(res_body3)

            gw_data = obj.get("data", {})
            server_host = gw_data.get("ip") or f"{server_lower}.sxd.xd.com"
            server_port = int(gw_data.get("port", 8475))
            player_name = str(gw_data.get("player_name", user_id))
            hash_code = str(gw_data.get("hash_code", ""))
            time_str = str(gw_data.get("time", ticket_data.get("time", "")))

            # 提取区服数字编号
            raw_sid = gw_data.get("server_id", 3542)
            try:
                if isinstance(raw_sid, str):
                    digits = "".join(filter(str.isdigit, raw_sid))
                    numeric_sid = int(digits) if digits else 3542
                else:
                    numeric_sid = int(raw_sid)
            except Exception:
                numeric_sid = 3542

            if not hash_code:
                logger.error("[%s] 心动官网登录步骤 3 失败，未解析到有效 hash_code: %s", account.display_name, res_body3[:300])
                return None

            creds = GatewayCredentials(
                server_host=server_host,
                server_port=server_port,
                player_name=player_name,
                hash_code=hash_code,
                time=time_str,
                platform="xd",
                server_id=numeric_sid,
                nickname=gw_data.get("nickname", ""),
            )
            logger.info("[%s] 心动官服登录与网关令牌换取全部成功: %s:%d (角色: %s)", account.display_name, server_host, server_port, player_name)
            return creds

        except Exception as e:
            logger.error("[%s] 心动官服自动登录网络异常: %s", account.display_name, e, exc_info=True)
            return None
