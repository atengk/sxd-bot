"""神仙道多人副本自动化组队与挑战任务 (Mod 14, Mod_MultipleMission_Base)

支持官方多人副本活动时段自动感知 (每日 12:30-13:30 与 18:30-19:30)，自动检索队伍快速加入或自建房间召集挑战，获取高额声望与白玉牌。

@author Ateng
@since 2026-10-15
"""

import datetime
import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)


class MultiMissionTask(BaseTask):
    """多人副本自动组队与挑战任务

    @author Ateng
    @since 2026-10-15
    """

    name = "MultiMissionTask"
    interval_sec = 0.0  # 单次日常巡检

    @staticmethod
    def is_multi_mission_open() -> bool:
        """检查当前时间是否处于神仙道官方多人副本活动开放时间窗"""
        now = datetime.datetime.now().time()
        # 中午场: 12:30 ~ 13:30
        noon_start = datetime.time(12, 30)
        noon_end = datetime.time(13, 30)
        # 晚间场: 18:30 ~ 19:30
        eve_start = datetime.time(18, 30)
        eve_end = datetime.time(19, 30)

        return (noon_start <= now <= noon_end) or (eve_start <= now <= eve_end)

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行多人副本自动组队与挑战巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过多人副本任务")

        # 1. 活动时间窗口守卫
        if not self.is_multi_mission_open():
            now_str = datetime.datetime.now().strftime("%H:%M")
            msg = f"当前时间 ({now_str}) 非多人副本活动时段 (每日 12:30-13:30 / 18:30-19:30)，安全跳过"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"in_schedule": False})

        joined_or_created = False

        # 2. 活动进行中: 打开多人副本并同步队伍列表 (Mod 14)
        try:
            req_open = PacketBuilder(mod=14, act=0).build()
            try:
                resp_open = await client.request(req_open, timeout_sec=2.0)
                logger.debug("多人副本面板状态同步成功，长度=%d", len(resp_open))
            except Exception:
                logger.debug("多人副本状态暂无即时应答，直接尝试检索队伍")

            # 3. 检索当前招募队伍并尝试加入 (Mod 14, Act 20: random_join)
            try:
                req_join = PacketBuilder(mod=14, act=20).build()
                await client.send_packet(req_join)
                joined_or_created = True
                logger.info("已提交多人副本快速随机加入队伍指令 (Mod 14, Act 20)")
            except Exception:
                # 4. 若无现成队伍，自动创建房间 (Mod 14, Act 3: create_multiple_mission_team, 参数: mission_id=1, type=0)
                req_create = PacketBuilder(mod=14, act=3).write_int32(1).write_uint8(0).build()
                await client.send_packet(req_create)
                joined_or_created = True
                logger.info("已自动创建多人副本房间并召集队伍挑战 (Mod 14, Act 3)")

            if joined_or_created:
                msg = "多人副本巡检完成，已完成组队/进入副本流水线"
                logger.info(msg)
                return TaskResult.success(msg, data={"in_schedule": True, "active": True})
            else:
                return TaskResult.skipped("今日多人副本已达上限或暂无就绪队伍")

        except Exception as exc:
            logger.info("多人副本巡检跳过: %s", exc)
            return TaskResult.skipped("多人副本系统暂不可挑战或活动已结束")
