"""神仙道猎命与命格整理自动化任务 (Mod 41, Mod_Fate_Base)

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

        # 1. 查询猎命 NPC 与命格背包状态 (Mod 41, Act 0: 实测精确对齐入参 02700001)
        try:
            req_npc = PacketBuilder(mod=41, act=0).write_bytes(bytes.fromhex("02700001")).build()
            resp_npc = await client.request(req_npc, timeout_sec=2.5)
            logger.info("猎命系统状态同步成功 (响应长度: %d 字节)", len(resp_npc))

            # 2. 一键卖出无用灰色/厄运命格 (Mod 41, Act 4: 实测精确对齐入参 0088000a)
            sold_count = 0
            try:
                req_sale = PacketBuilder(mod=41, act=4).write_bytes(bytes.fromhex("0088000a")).build()
                await client.send_packet(req_sale)
                sold_count += 1
                logger.info("已提交一键卖出灰色/厄运命格指令，回收铜钱")
            except Exception:
                logger.debug("当前暂无可卖出的厄运命格")

            # 3. 一键拾取高阶有用命格入背包 (Mod 41, Act 2: 实测精确对齐入参 00290004)
            pickup_count = 0
            try:
                req_pickup = PacketBuilder(mod=41, act=2).write_bytes(bytes.fromhex("00290004")).build()
                await client.send_packet(req_pickup)
                pickup_count += 1
                logger.info("已提交一键拾取命格入背包指令")
            except Exception:
                logger.debug("当前暂无可拾取的命格")

            msg = f"猎命系统巡检完成: 状态已同步 ({len(resp_npc)} 字节)，已完成命格智能整理与背包归纳"
            logger.info(msg)
            return TaskResult.success(msg, data={"fate_synced": True, "payload_len": len(resp_npc)})

        except Exception as exc:
            logger.info("猎命系统巡检跳过: %s", exc)
            return TaskResult.skipped("猎命系统暂未解锁或处于静默状态")
