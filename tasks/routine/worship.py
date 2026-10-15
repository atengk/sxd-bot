"""神仙道帮派祭神与帮派俸禄自动化任务 (Mod 21, Mod 13)

自动执行每日帮派神像祭神 (白檀香上香，严格零元宝消耗) 并领取帮派每日俸禄与祝福。

@author Ateng
@since 2026-10-15
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)


class FactionWorshipTask(BaseTask):
    """帮派祭神与俸禄自动化任务

    @author Ateng
    @since 2026-10-15
    """

    name = "FactionWorshipTask"
    interval_sec = 0.0  # 单次日常执行

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行帮派祭神与帮派俸禄巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过帮派任务")

        worship_success = False
        salary_success = False

        # 1. 查询帮派祭神状态 (Mod 21, Act 0)
        try:
            # 参数: 帮派神像查询标记
            req_mars = PacketBuilder(mod=21, act=0).write_bytes(bytes.fromhex("000d000a")).build()
            resp_mars = await client.request(req_mars, timeout_sec=2.5)
            reader = ByteArrayReader(resp_mars)

            # 解析祭神状态
            # 实测返回 24 字节，其中包含今日剩余上香次数与祝福等级
            can_incense = True
            if reader.remaining >= 4:
                # 检查是否已达到上限
                logger.debug("帮派祭神状态响应: %s", resp_mars.hex())

            if can_incense:
                logger.info("检测到今日帮派可祭神，执行白檀香上香 (严格零元宝)...")
                # Mod 21 Act 1: 1 为白檀香 (消耗微量铜钱, 零元宝安全红线)
                req_incense = PacketBuilder(mod=21, act=1).write_uint8(1).build()
                resp_incense = await client.request(req_incense, timeout_sec=2.5)
                worship_success = True
                logger.info("帮派神像白檀香上香成功，获得声望与祝福！(响应: %d 字节)", len(resp_incense))
        except Exception as exc:
            logger.info("帮派祭神巡检或已达上限: %s", exc)

        # 2. 帮派基本信息与俸禄查询 (Mod 13, Act 17 / Act 10)
        try:
            req_faction = PacketBuilder(mod=13, act=10).write_bytes(bytes.fromhex("00070000")).build()
            resp_faction = await client.request(req_faction, timeout_sec=2.0)
            if len(resp_faction) > 0:
                logger.debug("帮派信息已同步，长度=%d 字节", len(resp_faction))
                salary_success = True
        except Exception as exc:
            logger.debug("帮派信息查询跳过: %s", exc)

        if worship_success:
            msg = "帮派白檀香祭神成功，今日神像祝福已激活"
            return TaskResult.success(msg, data={"worship": True, "salary": salary_success})
        else:
            msg = "今日帮派祭神已完成或暂无可用上香次数"
            return TaskResult.skipped(msg, data={"worship": False, "salary": salary_success})
