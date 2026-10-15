"""神仙道玩家登录握手与基础角色初始化自动化任务

发送 Mod 0 Act 0 登录凭据，校验返回结果并拉取角色基础数据。

@author Ateng
@since 2026-10-15
"""

import asyncio
import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from network.web_auth import GatewayCredentials
from protocol.messages.player import PlayerLoginReq, PlayerLoginResp, PlayerInfoResp
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)


class LoginTask(BaseTask):
    """登录与初始化握手任务

    @author Ateng
    @since 2026-10-15
    """

    name = "LoginTask"
    interval_sec = 0.0  # 单次执行

    def __init__(self, creds: GatewayCredentials) -> None:
        self.creds = creds

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("执行登录任务: 角色用户名='%s', 平台='%s'", self.creds.player_name, self.creds.platform)

        # 1. 组装并发送登录请求 (Mod 0, Act 0)
        login_req = PlayerLoginReq(
            username=self.creds.player_name,
            hash_code=self.creds.hash_code,
            time=self.creds.time,
            platform=self.creds.platform,
            server_id=self.creds.server_id,
            account=self.creds.player_name,
        )

        try:
            resp_bytes = await client.request(login_req, timeout_sec=6.0)
            login_resp = PlayerLoginResp.decode(resp_bytes)

            if not login_resp.is_success:
                return TaskResult.failed(f"登录握手被服务器拒绝，错误码: {login_resp.result_code}")

            logger.info("登录握手成功！按真实协议时序推进前置初始化链...")

            # 2. 发送前置环境初始化 (Mod 0, Act 72)
            pkt_72 = PacketBuilder(mod=0, act=72).write_int32(0).build()
            await client.send_packet(pkt_72)

            # 3. 发送版本/客户端校验 (Mod 0, Act 99)
            pkt_99 = PacketBuilder(mod=0, act=99).write_int32(72).build()
            await client.send_packet(pkt_99)

            # 4. 获取角色基础信息 (Mod 0, Act 2)
            pkt_2 = PacketBuilder(mod=0, act=2).write_int32(99).build()
            await client.send_packet(pkt_2)
            # 等待服务端回传基础属性完成上下文中等级/财富同步
            await asyncio.sleep(0.5)

            return TaskResult.success("登录与角色基础初始化完成")

        except Exception as exc:
            logger.error("登录任务执行异常: %s", exc)
            return TaskResult.failed(f"登录执行失败: {exc}")
