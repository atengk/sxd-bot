"""神仙道心跳保活循环自动化任务

定期向服务端发送 Mod 0 Act 75 (Player.heart) 心跳帧，维持 TCP Socket 长连接活性，防止超时断线。

@author Ateng
@since 2026-10-15
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.messages.heartbeat import HeartbeatPkt

logger = logging.getLogger(__name__)


class HeartbeatTask(BaseTask):
    """心跳保活循环任务

    @author Ateng
    @since 2026-10-15
    """

    name = "HeartbeatTask"

    def __init__(self, interval_sec: float = 3.0) -> None:
        self.interval_sec = interval_sec
        self._seq = 0

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        if not ctx.is_connected:
            return TaskResult.skipped("连接已断开，跳过本次心跳发送")

        self._seq = (self._seq + 1) & 0xFF
        pkt = HeartbeatPkt(seq=self._seq)

        try:
            await client.send_packet(pkt)
            logger.debug("心跳保活包发送成功: seq=%d", self._seq)
            return TaskResult.success(f"心跳发送成功 seq={self._seq}")
        except Exception as exc:
            logger.warning("心跳保活包发送失败: %s", exc)
            return TaskResult.failed(f"心跳异常: {exc}")
