"""神仙道缘魂宝箱自动化开启任务 (Mod 232: Mod_LinkFate_Base)

对接官方微端缘魂宝箱协议，自动查询角色积攒的各类免费缘魂宝箱，
执行一键批量开箱与缘魂背包自动归类整理，严格遵守零元宝安全红线 (绝不元宝购买金色缘魂宝箱)。

@author Ateng
@since 2026-10-16
"""

import asyncio
import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)

# Mod 232 常量
SUCCESS = 5
FAILED = 10
PACK_FULL = 16
NO_ENOUGH_INGOT = 20
NOT_ENOUGH_BOX = 22


class LinkFateTask(BaseTask):
    """缘魂宝箱自动化开启与整理任务

    @author Ateng
    @since 2026-10-16
    """

    name = "LinkFateTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行缘魂宝箱批量开启与背包整理

        Args:
            client: 已建立的长连接客户端。
            ctx: 游戏全局运行时上下文。

        Returns:
            TaskResult: 任务执行结果。
        """
        logger.info("开始执行缘魂宝箱 (LinkFate) 批量开启与背包整理流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过缘魂宝箱任务")

        if ctx.player.level < 110:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达缘魂系统门槛 (110级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"opened_boxes": 0})

        total_opened = 0
        try:
            # 1. 查询存量缘魂宝箱列表 (Mod 232, Act 30: get_link_fate_box)
            req_boxes = PacketBuilder(mod=232, act=30).build()
            resp_boxes = await client.request(req_boxes, timeout_sec=2.5)
            if not resp_boxes or len(resp_boxes) < 2:
                return TaskResult.skipped("缘魂宝箱数据同步异常，安全跳过")

            reader = ByteArrayReader(resp_boxes)
            kind_count = reader.read_uint16()
            boxes_to_open = []
            for _ in range(kind_count):
                if reader.remaining < 8:
                    break
                box_id = reader.read_int32()
                box_count = reader.read_int32()
                if box_count > 0:
                    boxes_to_open.append((box_id, box_count))

            logger.info("缘魂宝箱同步完成，待开启宝箱类型数: %d 项", len(boxes_to_open))

            # 2. 依次遍历并批量一键开启所有免费存量宝箱 (Mod 232, Act 34: one_key_open_box)
            for box_id, count in boxes_to_open:
                try:
                    # 单次最多开 50 个防服务端报文过大
                    batch = min(count, 50)
                    req_open = PacketBuilder(mod=232, act=34).write_int32(box_id).write_int32(batch).build()
                    resp_open = await client.request(req_open, timeout_sec=2.5)
                    if resp_open and len(resp_open) >= 1 and resp_open[0] == SUCCESS:
                        total_opened += batch
                        logger.info("成功开启缘魂宝箱 [ID=%d] 共 %d 个！获得大量缘魂石 (零元宝)", box_id, batch)
                        await asyncio.sleep(0.3)
                    elif resp_open and resp_open[0] == PACK_FULL:
                        logger.warning("缘魂背包空间已满，提前中止开箱")
                        break
                except Exception as open_err:
                    logger.debug("开箱单项异常: %s", open_err)

            # 3. 自动整理与分类缘魂背包 (Mod 232, Act 14: classify_pack_grid)
            try:
                req_sort = PacketBuilder(mod=232, act=14).build()
                await client.send_packet(req_sort)
                logger.info("缘魂背包网格自动化整理完成")
            except Exception:
                pass

            msg = f"缘魂宝箱流水线完成: 累计开启免费宝箱 {total_opened} 个，背包整理完成 (零元宝)"
            logger.info(msg)
            return TaskResult.success(msg, data={"opened_boxes": total_opened})

        except TimeoutError:
            msg = "缘魂宝箱接口超时，安全跳过防断连"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"timeout": True})
        except Exception as exc:
            logger.warning("缘魂宝箱流水线执行异常: %s", exc)
            return TaskResult.skipped(f"缘魂宝箱异常跳过: {exc}")
