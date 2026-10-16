"""神仙道回忆之境里程碑奖励自动化任务 (Mod 526: Mod_MemoryZone_Base)

对接官方微端回忆之境协议，自动同步剧情篇章通关星级，
一键提取各章节未领取的绑定奖励，严格遵守零元宝安全红线 (绝不元宝回溯)。

@author Ateng
@since 2026-10-16
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)

# Mod 526 常量
SUCCESS = 0
FAILED = 1
MAX_TIMES = 2
NO_INGOT = 3


class MemoryZoneTask(BaseTask):
    """回忆之境里程碑奖励自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "MemoryZoneTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行回忆之境章节星级同步与奖励提取

        Args:
            client: 已建立的长连接客户端。
            ctx: 游戏全局运行时上下文。

        Returns:
            TaskResult: 任务执行结果。
        """
        logger.info("开始执行回忆之境 (MemoryZone) 奖励巡检流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过回忆之境任务")

        # 回忆之境通常 120 级以上开放
        if ctx.player.level < 120:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达回忆之境门槛 (120级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"claimed_zones": 0})

        claimed_zones = 0
        total_zones = 0

        try:
            # 1. 查询回忆之境主面板与篇章星级列表 (Mod 526, Act 1: main_panel)
            req_main = PacketBuilder(mod=526, act=1).build()
            resp_main = await client.request(req_main, timeout_sec=2.5)
            if not resp_main or len(resp_main) < 3:
                return TaskResult.skipped("回忆之境面板数据为空，安全跳过")

            reader = ByteArrayReader(resp_main)
            _status = reader.read_uint8()
            zone_count = reader.read_uint16()
            total_zones = zone_count
            logger.info("回忆之境面板同步成功，包含篇章数: %d 卷", zone_count)

            # 2. 遍历各已通关篇章尝试领取绑定奖励 (Mod 526, Act 3: get_bind_award)
            for _ in range(zone_count):
                if reader.remaining < 16:
                    break
                zone_id = reader.read_int32()
                stars = reader.read_int32()
                max_stars = reader.read_int32()
                state = reader.read_int32()

                # 只有未领取状态 (state == 0) 才发起领取请求，已领取篇章安全跳过防断连
                if stars > 0 and state == 0:
                    try:
                        req_award = PacketBuilder(mod=526, act=3).write_int32(zone_id).build()
                        resp_award = await client.request(req_award, timeout_sec=2.0)
                        if resp_award and len(resp_award) >= 1 and resp_award[0] == SUCCESS:
                            claimed_zones += 1
                            logger.info("成功领取回忆之境 [篇章ID=%d] 绑定里程碑大礼包！(星级: %d/%d)", zone_id, stars, max_stars)
                    except Exception as z_err:
                        logger.debug("章节 %d 奖励领取跳过: %s", zone_id, z_err)
                else:
                    logger.debug("回忆之境篇章 [ID=%d] 奖励已领取或未达标 (星级: %d/%d, 状态: %d)", zone_id, stars, max_stars, state)

            msg = f"回忆之境流水线完成: 巡检章节 {total_zones} 卷，成功提取绑定大奖 {claimed_zones} 项 (零元宝)"
            logger.info(msg)
            return TaskResult.success(msg, data={"total_zones": total_zones, "claimed_zones": claimed_zones})

        except TimeoutError:
            msg = "回忆之境接口响应超时，安全跳过防断连"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"timeout": True})
        except Exception as exc:
            logger.warning("回忆之境流水线执行异常: %s", exc)
            return TaskResult.skipped(f"回忆之境异常跳过: {exc}")
