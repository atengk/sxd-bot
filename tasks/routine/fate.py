"""神仙道猎命与命格整理自动化任务 (Mod 22: Mod_Fate_Base)

自动查询猎命 NPC 状态，一键卖出厄运与灰色命格换取铜钱，一键拾取高阶有益命格至命格背包，严格遵守零元宝安全原则。

@author Ateng
@since 2026-10-15
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)


class FateHuntTask(BaseTask):
    """猎命与命格整理自动化任务

    @author Ateng
    @since 2026-10-15
    """

    name = "FateHuntTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行猎命系统与命格背包巡检流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过猎命任务")

        # 角色等级门槛检查 (猎命通常 20 级以上开启)
        if ctx.player.level < 20:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达猎命门槛 (20级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"active": False})

        # 1. 查询猎命 NPC 状态 (Mod 22, Act 0: get_fate_npc)
        try:
            req_npc = PacketBuilder(mod=22, act=0).build()
            resp_npc = await client.request(req_npc, timeout_sec=2.5)
            logger.info("猎命系统状态同步成功 (响应长度: %d 字节)", len(resp_npc))

            # 2. 查询临时命格背包 (Mod 22, Act 1: get_temp_fate)
            req_temp = PacketBuilder(mod=22, act=1).build()
            resp_temp = await client.request(req_temp, timeout_sec=2.5)
            from protocol.packet import ByteArrayReader
            reader = ByteArrayReader(resp_temp)
            temp_count = reader.read_uint16() if reader.remaining >= 2 else 0

            if temp_count == 0:
                logger.info("当前临时命格背包为空 (待整理数量: 0)，安全跳过卖出与拾取操作")
            else:
                logger.info("检测到待整理临时命格: %d 个，开始分类整理...", temp_count)
                temp_fates = []
                for _ in range(temp_count):
                    if reader.remaining >= 10:
                        tf_id = reader.read_int64()
                        f_id = reader.read_int16()
                        temp_fates.append((tf_id, f_id))

                # 灰色/厄运命格通常 fate_id == 1
                grey_ids = [tf_id for tf_id, f_id in temp_fates if f_id <= 1]
                useful_ids = [tf_id for tf_id, f_id in temp_fates if f_id > 1]

                # 3. 卖出厄运命格 (Mod 22, Act 3: sale_temp_fate)
                if grey_ids:
                    builder_sale = PacketBuilder(mod=22, act=3).write_uint16(len(grey_ids))
                    for gid in grey_ids:
                        builder_sale.write_int64(gid)
                    await client.send_packet(builder_sale.build())
                    logger.info("已提交一键卖出 %d 个灰色/厄运命格指令，回收铜钱", len(grey_ids))

                # 4. 拾取有用命格 (Mod 22, Act 2: pickup_fate)
                if useful_ids:
                    builder_pickup = PacketBuilder(mod=22, act=2).write_uint16(len(useful_ids))
                    for uid in useful_ids:
                        builder_pickup.write_int64(uid)
                    await client.send_packet(builder_pickup.build())
                    logger.info("已提交一键拾取 %d 个高阶命格入背包指令", len(useful_ids))

            msg = f"猎命系统巡检完成: 状态已同步 ({len(resp_npc)} 字节)，临时命格整理完毕 (初始待整理: {temp_count})"
            logger.info(msg)
            return TaskResult.success(msg, data={"fate_synced": True, "temp_count": temp_count})

        except Exception as exc:
            logger.info("猎命系统巡检跳过: %s", exc)
            return TaskResult.skipped(f"猎命系统暂未解锁或处于静默状态: {exc}")

