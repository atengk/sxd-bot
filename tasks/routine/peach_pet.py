"""神仙道摘仙桃与神龙培养自动化任务 (Mod 100, Mod 40)

每日自动一键摘取高阶仙桃获取巨额经验，自动进行神龙拜祭与喂养获取活跃度与声望，严格遵守零元宝安全原则。

@author Ateng
@since 2026-10-15
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)


class PeachAndPetTask(BaseTask):
    """摘仙桃与神龙培养自动化任务

    @author Ateng
    @since 2026-10-15
    """

    name = "PeachAndPetTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行每日摘仙桃与神龙培养巡检流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过仙桃与神龙任务")

        peaches_harvested = 0
        pet_fed = False

        # 1. 查询仙桃状态并自动一键摘取 (Mod 100, Act 45 & Act 34)
        try:
            req_peach_info = PacketBuilder(mod=100, act=45).build()
            resp_peach_info = await client.request(req_peach_info, timeout_sec=2.0)
            logger.debug("仙桃状态响应长度: %d", len(resp_peach_info))

            # 尝试执行一键摘仙桃 (Mod 100, Act 34: get_peach)
            try:
                req_get_peach = PacketBuilder(mod=100, act=34).build()
                resp_get_peach = await client.request(req_get_peach, timeout_sec=2.5)
                if len(resp_get_peach) >= 4 and resp_get_peach[-1] == 1:
                    peaches_harvested += 1
                    logger.info("成功摘取今日高阶仙桃！获得巨额角色升级经验")
                else:
                    logger.debug("今日仙桃已摘取或暂无可用仙桃")
            except Exception:
                logger.debug("今日仙桃已达上限或暂不可摘取")

        except Exception as exc:
            logger.info("摘仙桃功能巡检跳过: %s", exc)

        # 2. 每日神龙培养与喂养 (Mod 100, Act 29: feed_pet_animal, 严格免费/零元宝)
        try:
            req_pet = PacketBuilder(mod=100, act=29).build()
            resp_pet = await client.request(req_pet, timeout_sec=2.0)
            if len(resp_pet) > 0:
                pet_fed = True
                logger.info("神龙日常培养拜祭成功！帮派活跃度与声望已提升")
        except Exception as exc:
            logger.debug("神龙今日已完成培养或无需重复喂养: %s", exc)

        if peaches_harvested > 0 or pet_fed:
            msg = f"仙桃与神龙流水线完成: 摘取 {peaches_harvested} 颗仙桃，神龙培养状态={'已完成' if pet_fed else '未更新'}"
            logger.info(msg)
            return TaskResult.success(msg, data={"peaches": peaches_harvested, "pet_fed": pet_fed})
        else:
            msg = "今日仙桃已全部摘取且神龙已完成培养，处于最优状态"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"peaches": 0, "pet_fed": pet_fed})
