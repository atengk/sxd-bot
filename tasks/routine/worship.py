"""神仙道帮派祭神与神像上香自动化任务 (Mod 21)

自动执行每日帮派神像祭神 (白檀香上香，严格零元宝消耗) 并获取帮派祝福与声望。

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

# 贡品常量定义 (严格遵守零元宝红线)
INCENSE_SANDALWOOD = 1  # 白檀香 (消耗微量铜钱, 零元宝, 声望+100, 帮派贡献+10)
INCENSE_SUHE = 2        # 苏合香 (消耗元宝, 坚决禁止使用)
INCENSE_TIANMU = 3      # 天木香 (消耗大额元宝, 坚决禁止使用)


class FactionWorshipTask(BaseTask):
    """帮派祭神白檀香自动化任务

    @author Ateng
    @since 2026-10-15
    """

    name = "FactionWorshipTask"
    interval_sec = 0.0  # 单次日常执行

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行帮派祭神巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过帮派祭神任务")

        # 1. 查询帮派神像状态 (Mod 21, Act 0: mars_info)
        try:
            req_mars = PacketBuilder(mod=21, act=0).build()
            resp_mars = await client.request(req_mars, timeout_sec=3.0)
            reader = ByteArrayReader(resp_mars)

            if reader.remaining < 24:
                return TaskResult.skipped("帮派神像响应报文长度不足，可能尚未加入帮派")

            _reserve0 = reader.read_int32()
            god_level = reader.read_int32()
            _reserve1 = reader.read_int32()
            _reserve2 = reader.read_int32()
            free_times = reader.read_int32()
            max_times = reader.read_int32()

            logger.info("帮派神像状态: 神像等级=%d, 今日剩余祭神次数=%d/%d", god_level, free_times, max_times)

            # 2. 强前置卫语句: 零元宝安全熔断
            if free_times <= 0:
                msg = f"今日帮派祭神次数已耗尽 ({free_times}/{max_times})，触发零元宝熔断，跳过上香"
                logger.info(msg)
                return TaskResult.skipped(msg, data={"god_level": god_level, "free_times": free_times, "incense_type": 0})

            # 3. 执行白檀香上香 (Mod 21, Act 1: incense)
            logger.info("检测到今日剩余免费祭神次数 > 0，执行白檀香上香 (严格硬编码为 1, 零元宝)...")
            incense_pkt = PacketBuilder(mod=21, act=1).write_uint8(INCENSE_SANDALWOOD).build()
            incense_resp = await client.request(incense_pkt, timeout_sec=3.0)

            msg = f"帮派神像白檀香上香成功！(响应载荷 {len(incense_resp)} 字节)"
            logger.info(msg)
            return TaskResult.success(msg, data={"god_level": god_level, "incense_type": INCENSE_SANDALWOOD})

        except Exception as exc:
            logger.warning("帮派祭神巡检异常: %s", exc)
            return TaskResult.failed(f"帮派祭神执行失败: {exc}")
