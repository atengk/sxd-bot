"""神仙道周末狂欢福利礼包与委托减负任务 (Mod 637: WeekendRevelryGiftPack, Mod 638: WeekendRevelryEntrust)

仅在每周六与周日全服活动窗口激活，自动领取周末专属免费礼包，开启周末日常委托自动完成。

@author Ateng
@since 2026-10-16
"""

import datetime
import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)


class WeekendRevelryTask(BaseTask):
    """周末狂欢福利与委托任务

    @author Ateng
    @since 2026-10-16
    """

    name = "WeekendRevelryTask"
    interval_sec = 0.0  # 单次日常巡检

    @staticmethod
    def is_weekend() -> bool:
        """检查当前时间是否为周六或周日 (0=Mon, 5=Sat, 6=Sun)"""
        return datetime.datetime.now().weekday() in (5, 6)

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行周末狂欢福利流水线"""
        logger.info("开始执行周末狂欢 (WeekendRevelry) 福利与委托巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于有效长连接状态，跳过周末狂欢任务")

        # 1. 严格时段守卫：仅周末激活
        if not self.is_weekend():
            today_name = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.datetime.now().weekday()]
            msg = f"当前为 {today_name}，非周末狂欢活动时段 (周六/周日开放)，安全跳过防断连"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"is_weekend": False})

        claimed_packs = 0
        entrusts_set = 0

        try:
            # 2. 周末礼包面板查询与免费档位领取 (Mod 637, Act 0: panel_info)
            req_pack_panel = PacketBuilder(mod=637, act=0).build()
            resp_pack_panel = await client.request(req_pack_panel, timeout_sec=2.5)
            logger.info("周末礼包面板数据已同步 (响应: %d 字节)", len(resp_pack_panel))

            # 遍历尝试领取免费礼包档位 (Mod 637, Act 1: get_award)
            for pack_id in range(1, 4):
                try:
                    req_get = PacketBuilder(mod=637, act=1).write_int32(pack_id).build()
                    resp_get = await client.request(req_get, timeout_sec=2.0)
                    if resp_get and resp_get[0] == 0:
                        claimed_packs += 1
                        logger.info("周末狂欢第 %d 档礼包成功领取！", pack_id)
                except Exception:
                    pass

            # 3. 周末日常委托自动完成 (Mod 638, Act 0: panel_info, Act 1: set_auto_finish)
            try:
                req_entrust_panel = PacketBuilder(mod=638, act=0).build()
                resp_entrust_panel = await client.request(req_entrust_panel, timeout_sec=2.5)
                if resp_entrust_panel and len(resp_entrust_panel) >= 6:
                    reader = ByteArrayReader(resp_entrust_panel)
                    reader.read_int32()  # state
                    cnt = reader.read_uint16() if reader.remaining >= 2 else 0
                    for _ in range(cnt):
                        if reader.remaining < 4:
                            break
                        eid = reader.read_int32()
                        try:
                            req_auto = PacketBuilder(mod=638, act=1).write_int32(eid).build()
                            await client.send_packet(req_auto)
                            entrusts_set += 1
                        except Exception:
                            pass
                    logger.info("已提交 %d 项周末日常自动委托完成指令", entrusts_set)
            except Exception as e:
                logger.debug("周末委托面板跳过: %s", e)

            msg = f"周末狂欢巡检完成: 成功领取 {claimed_packs} 个周末大礼包，开启 {entrusts_set} 项减负委托"
            logger.info(msg)
            return TaskResult.success(msg, data={"claimed_packs": claimed_packs, "entrusts_set": entrusts_set})

        except Exception as exc:
            logger.warning("周末狂欢处理异常 (安全跳过): %s", exc)
            return TaskResult.skipped(f"周末狂欢功能暂未开启: {exc}")
