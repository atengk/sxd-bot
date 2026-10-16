"""神仙道点金石点石成金与好友协助自动化任务 (Mod 551: Mod_GoldenTouchStone_Base)

每日自动检测并执行免费点金石抽取铜钱与珍稀材料，遍历好友列表执行无损协助互惠。

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


class GoldenTouchStoneTask(BaseTask):
    """点金石与好友协助自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "GoldenTouchStoneTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行点金石与好友协助流水线"""
        logger.info("开始执行点金石 (GoldenTouchStone) 每日点金与助友巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于有效长连接状态，跳过点金石任务")

        try:
            # 1. 查询点金石活动状态 (Mod 551, Act 0: get_status)
            req_status = PacketBuilder(mod=551, act=0).build()
            resp_status = await client.request(req_status, timeout_sec=2.5)
            status_code = resp_status[0] if resp_status else 0
            logger.info("点金石系统状态同步完成 (状态码: %d)", status_code)

            # 2. 查询点金主面板详情 (Mod 551, Act 2: get_touch_panel_info)
            req_panel = PacketBuilder(mod=551, act=2).build()
            resp_panel = await client.request(req_panel, timeout_sec=2.5)
            touch_done = 0

            # 3. 执行点石成金 (Mod 551, Act 6: touch_stone)
            try:
                req_touch = PacketBuilder(mod=551, act=6).build()
                resp_touch = await client.request(req_touch, timeout_sec=3.0)
                if resp_touch and len(resp_touch) >= 1:
                    t_status = resp_touch[0]
                    if t_status == 0:
                        touch_done += 1
                        logger.info("点石成金成功！成功转化海量铜钱与材料收益")
                    else:
                        logger.info("今日点金石免费次数已完成或暂无可点次数 (状态码: %d)", t_status)
            except Exception as e:
                logger.debug("点金操作结束: %s", e)

            # 4. 查询好友求助面板并批量协助 (Mod 551, Act 1: get_share_panel_info)
            helped_count = 0
            try:
                req_share = PacketBuilder(mod=551, act=1).build()
                resp_share = await client.request(req_share, timeout_sec=2.5)
                if resp_share and len(resp_share) >= 6:
                    reader = ByteArrayReader(resp_share)
                    share_total = reader.read_int32()
                    list_len = reader.read_uint16() if reader.remaining >= 2 else 0
                    logger.info("检测到好友点金求助列表: %d 条记录", list_len)
                    for _ in range(list_len):
                        if reader.remaining < 4:
                            break
                        f_pid = reader.read_int32()
                        f_name = reader.read_utf()
                        f_msg = reader.read_utf()
                        # 跳过剩余 3 个 int 字段 (剩余 12 字节)
                        if reader.remaining >= 12:
                            reader.read_int32()
                            reader.read_int32()
                            reader.read_int32()

                        # 执行协助好友 (Mod 551, Act 5: help_friend)
                        try:
                            req_help = PacketBuilder(mod=551, act=5).write_int32(f_pid).write_utf(f_name).write_utf(f_msg).build()
                            await client.send_packet(req_help)
                            helped_count += 1
                        except Exception:
                            pass
                    if helped_count > 0:
                        logger.info("已完成 %d 位好友的点石求助协助", helped_count)
            except Exception as e:
                logger.debug("好友协助列表解析跳过: %s", e)

            msg = f"点金石巡检完成: 状态已同步，成功执行点金 ({touch_done}次)，协助好友 ({helped_count}人)"
            logger.info(msg)
            return TaskResult.success(msg, data={"touch_done": touch_done, "helped_count": helped_count})

        except Exception as exc:
            logger.warning("点金石巡检异常 (安全跳过): %s", exc)
            return TaskResult.skipped(f"点金石功能暂未开启或处于静默期: {exc}")
