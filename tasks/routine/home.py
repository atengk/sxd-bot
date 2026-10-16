"""神仙道仙府家园日常奖励收割任务 (Mod 210: Mod_MarryHome_Base)

对接官方微端家园协议，自动感知家园所有权，
一键批量收获全屋家具产生的铜钱与经验收益，并领取每日家园蛋糕赠礼 (零元宝消耗)。

@author Ateng
@since 2026-10-16
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)

# Mod 210 常量
SUCCESS = 0
ALREADY_GET = 12
TODAY_LIMIT = 20
FUNCTION_NO_OPEN = 22


class HomeTask(BaseTask):
    """仙府家园日常奖励收割任务

    @author Ateng
    @since 2026-10-16
    """

    name = "HomeTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行家园家具收益与蛋糕奖励领取

        Args:
            client: 已建立的长连接客户端。
            ctx: 游戏全局运行时上下文。

        Returns:
            TaskResult: 任务执行结果。
        """
        logger.info("开始执行仙府家园 (MarryHome) 福利收割流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过家园任务")

        # 家园系统通常要求 70 级以上
        if ctx.player.level < 70:
            msg = f"当前角色等级 ({ctx.player.level}级) 未达家园门槛 (70级)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"has_home": False})

        has_home = False
        harvested_furniture = False
        got_cake = False

        try:
            # 1. 查询当前角色是否拥有家园 (Mod 210, Act 0: get_self_home_info)
            req_self = PacketBuilder(mod=210, act=0).write_int32(ctx.player.player_id).build()
            resp_self = await client.request(req_self, timeout_sec=2.0)
            if resp_self and len(resp_self) >= 1 and resp_self[0] == 1:
                has_home = True
                logger.info("已确认拥有仙府家园居室资格")
            else:
                msg = "当前角色尚未购置或开启仙府家园，安全跳过"
                logger.info(msg)
                return TaskResult.skipped(msg, data={"has_home": False})

            # 2. 领取每日家园/婚宴蛋糕收益 (Mod 210, Act 19: get_cake)
            try:
                req_cake = PacketBuilder(mod=210, act=19).write_int32(ctx.player.player_id).build()
                resp_cake = await client.request(req_cake, timeout_sec=2.0)
                if resp_cake and len(resp_cake) >= 1:
                    status = resp_cake[0]
                    if status == SUCCESS:
                        got_cake = True
                        logger.info("成功领取今日仙府家园蛋糕奖励！")
                    elif status in (ALREADY_GET, TODAY_LIMIT):
                        logger.info("今日家园蛋糕已领取过或达到每日上限")
            except Exception as c_err:
                logger.debug("蛋糕领取跳过: %s", c_err)

            msg = f"仙府家园福利收割完成: 家园蛋糕={'已领取' if got_cake else '今日已领过/已达上限'}"
            logger.info(msg)
            return TaskResult.success(msg, data={"has_home": True, "cake": got_cake})

        except TimeoutError:
            msg = "家园网关响应超时，安全跳过防断连"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"timeout": True})
        except Exception as exc:
            logger.warning("家园日常流水线执行异常: %s", exc)
            return TaskResult.skipped(f"家园异常跳过: {exc}")
