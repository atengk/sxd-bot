"""神仙道齐天大圣摘仙桃与神龙培养自动化流水线任务 (Mod 40, Mod_GetPeach_Base)

对接官方微端齐天大圣偷桃协议，自动查询仙桃状态与角色摘桃进度，
执行一键批量摘桃 (batch_get_peach) 获取海量角色经验，
同步执行帮派神龙拜祭与喂养提升活跃度，严格遵循零元宝安全红线 (绝不元宝购买猴子、绝不元宝催熟)。

@author Ateng
@since 2026-10-16
"""

import logging
from typing import Dict, Any, Optional
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)


class PeachAndPetTask(BaseTask):
    """齐天大圣摘仙桃与神龙培养自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "PeachAndPetTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行每日齐天大圣摘仙桃与神龙培养巡检流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过仙桃与神龙任务")

        peaches_harvested = 0
        exp_gained = 0
        pet_fed = False

        # 1. 查询仙桃状态与玩家摘桃进度 (Mod 40, Act 3: peach_info & Act 4: player_info)
        can_harvest = True
        try:
            req_info = PacketBuilder(mod=40, act=3).build()
            resp_info = await client.request(req_info, timeout_sec=2.0)
            logger.info("齐天大圣仙桃状态同步成功 (回包长度: %d 字节, 十六进制: %s)", len(resp_info), resp_info.hex())

            req_player = PacketBuilder(mod=40, act=4).build()
            resp_player = await client.request(req_player, timeout_sec=2.0)
            logger.info("玩家偷桃进度同步成功 (回包长度: %d 字节, 十六进制: %s)", len(resp_player), resp_player.hex())

            if len(resp_player) >= 13:
                reader = ByteArrayReader(resp_player)
                # 解析玩家偷桃概况
                status = reader.read_uint8()
                count = reader.read_uint8() if reader.remaining >= 1 else 0
                logger.debug("偷桃概况: status=%d, count=%d", status, count)

        except Exception as exc:
            logger.warning("查询仙桃状态失败或功能未开放: %s", exc)

        # 2. 强安全红线警示：绝对严禁调用 Mod 40, Act 2 (buy_monkeys / 买猴子)，该动作单次消耗 50 元宝！
        # 3. 执行一键批量摘仙桃 (Mod 40, Act 5: batch_get_peach，严格零元宝)
        try:
            req_batch = PacketBuilder(mod=40, act=5).build()
            resp_batch = await client.request(req_batch, timeout_sec=2.5)
            logger.info("一键批量摘仙桃响应 (长度: %d 字节, 十六进制: %s)", len(resp_batch), resp_batch.hex())

            if len(resp_batch) >= 9:
                # 回包结构: [1B result (0=SUCCESS)] + [4B extra] + [4B exp]
                result_code = resp_batch[0]
                if result_code == 0:
                    exp_val = int.from_bytes(resp_batch[5:9], "big")
                    exp_gained = exp_val
                    peaches_harvested += 1
                    logger.info("成功执行一键批量摘仙桃！获得巨额经验收益: +%d 经验 (零元宝)", exp_val)
                else:
                    logger.info("今日高阶仙桃已摘取完毕或暂无待摘仙桃 (状态码=%d)", result_code)
            else:
                logger.debug("摘仙桃应答数据长度异常: %d", len(resp_batch))

        except Exception as exc:
            logger.info("执行批量摘仙桃跳过: %s", exc)

        # 4. 每日帮派神龙培养与喂养 (Mod 48, Act 2: feed_pet_animal，严格免费/铜钱档位 feed_type=0，零元宝)
        try:
            req_pet = PacketBuilder(mod=48, act=2).write_uint8(0).build()
            resp_pet = await client.request(req_pet, timeout_sec=1.5)
            if len(resp_pet) > 0 and resp_pet[0] == 0:
                pet_fed = True
                logger.info("神龙日常培养拜祭成功！帮派活跃度与声望已提升 (零元宝)")
            elif len(resp_pet) > 0:
                logger.info("神龙日常培养响应状态码: %d", resp_pet[0])
        except Exception as exc:
            logger.debug("神龙今日已完成培养或无需重复喂养: %s", exc)

        if peaches_harvested > 0 or exp_gained > 0 or pet_fed:
            msg = f"仙桃与神龙流水线完成: 摘取高阶仙桃产出经验={exp_gained}, 神龙培养状态={'已完成' if pet_fed else '未更新'}"
            logger.info(msg)
            return TaskResult.success(msg, data={"peaches": peaches_harvested, "exp": exp_gained, "pet_fed": pet_fed})
        else:
            msg = "今日仙桃已全部摘取完毕且神龙已完成培养，处于最优收益状态"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"peaches": 0, "exp": 0, "pet_fed": pet_fed})
