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
        """检查当前时间是否处于周末狂欢活动期 (周六=5, 周日=6, 周一=0)"""
        return datetime.datetime.now().weekday() in (5, 6, 0)

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行周末狂欢福利流水线"""
        logger.info("开始执行周末狂欢 (WeekendRevelry) 福利与委托巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于有效长连接状态，跳过周末狂欢任务")

        # 1. 严格时段守卫：仅周六、周日与周一激活
        weekday = datetime.datetime.now().weekday()
        if not self.is_weekend():
            today_name = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][weekday]
            msg = f"当前为 {today_name}，非周末狂欢活动时段 (周六/周日/周一开放)，安全跳过防断连"
            logger.info(msg)
            return TaskResult.skipped(msg, data={"is_weekend": False})

        # 映射当日推荐礼包档位 (周六=1, 周日=2, 周一=3)
        today_pack_map = {5: 1, 6: 2, 0: 3}
        target_pack = today_pack_map.get(weekday, 1)

        claimed_packs = 0
        entrusts_set = 0

        try:
            # 2. 周末礼包面板查询与免费档位抽取 (Mod 637, Act 0: panel_info -> Act 1: get_award)
            try:
                req_pack_panel = PacketBuilder(mod=637, act=0).build()
                resp_pack_panel = await client.request(req_pack_panel, timeout_sec=2.5)
                logger.info("周末礼包面板数据已同步 (响应: %d 字节)", len(resp_pack_panel) if resp_pack_panel else 0)
                if resp_pack_panel and len(resp_pack_panel) >= 6:
                    reader = ByteArrayReader(resp_pack_panel)
                    _ = reader.read_int32()  # cur_day / panel_status
                    p_cnt = reader.read_uint16() if reader.remaining >= 2 else 0
                    for _ in range(p_cnt):
                        if reader.remaining < 16:
                            break
                        pid = reader.read_int32()
                        p_status = reader.read_int32()
                        need_ingot = reader.read_int32()
                        _ = reader.read_int32()  # pool_id
                        logger.debug("周末礼包档位 #%d: 状态=%d, 消耗元宝=%d", pid, p_status, need_ingot)
            except Exception as e:
                logger.debug("查询周末狂欢面板跳过: %s", e)

            # 遍历尝试领取当日及可用免费礼包档位 (Mod 637, Act 1: get_award，严格零元宝，绝不执行 Act 2 元宝找回)
            pack_order = [target_pack] + [p for p in (1, 2, 3) if p != target_pack]
            for pack_id in pack_order:
                try:
                    req_get = PacketBuilder(mod=637, act=1).write_int32(pack_id).build()
                    resp_get = await client.request(req_get, timeout_sec=2.0)
                    if resp_get and len(resp_get) >= 1:
                        res_code = resp_get[0]
                        # SUCCESS: 0, FAILED: 1, HAS_GET: 2, CAN_NOT_GET: 3, DAY_ERROR: 4
                        if res_code == 0:
                            claimed_packs += 1
                            logger.info("周末狂欢第 %d 档狂欢礼【抽取奖励】成功入账！", pack_id)
                        elif res_code == 2:
                            logger.info("周末狂欢第 %d 档礼包今日已完成抽取", pack_id)
                        elif res_code == 4:
                            logger.debug("周末狂欢第 %d 档礼包非今日抽取日 (DAY_ERROR)", pack_id)
                        else:
                            logger.debug("周末狂欢第 %d 档礼包响应状态: %d", pack_id, res_code)
                except Exception as ex:
                    logger.debug("抽取周末礼包 #%d 异常: %s", pack_id, ex)

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

            # 4. 周末狂欢仙果转盘免费抽取 (Mod 242: SundayFruit, Act 2: draw)
            claimed_draws = 0
            try:
                # 先拉取仙果活动状态 (Mod 242, Act 1: sunday_fruit_info)
                req_fruit = PacketBuilder(mod=242, act=1).build()
                resp_fruit = await client.request(req_fruit, timeout_sec=2.0)
                logger.debug("仙果转盘状态响应长度: %d 字节", len(resp_fruit) if resp_fruit else 0)

                # 循环执行免费仙果抽取，直至免费次数用尽 (TIME_USE=3 或 非 SUCCESS=2)
                for _ in range(5):
                    req_draw = PacketBuilder(mod=242, act=2).build()
                    resp_draw = await client.request(req_draw, timeout_sec=2.5)
                    if resp_draw and len(resp_draw) >= 1:
                        draw_res = resp_draw[0]
                        if draw_res == 2:  # SUCCESS
                            claimed_draws += 1
                            logger.info("周末仙果转盘抽取成功！(第 %d 次)", claimed_draws)
                        elif draw_res == 3:  # TIME_USE
                            logger.debug("今日仙果转盘免费抽取次数已用尽")
                            break
                        else:
                            break
                    else:
                        break
            except Exception as e:
                logger.debug("仙果转盘抽取跳过: %s", e)

            # 5. 周末活跃回馈转盘抽取 (Mod 644: ActiveRepay, Act 1: apply_draw)
            try:
                req_repay_info = PacketBuilder(mod=644, act=0).build()
                resp_repay_info = await client.request(req_repay_info, timeout_sec=2.0)
                if resp_repay_info and len(resp_repay_info) >= 1:
                    req_repay_draw = PacketBuilder(mod=644, act=1).build()
                    resp_repay_draw = await client.request(req_repay_draw, timeout_sec=2.5)
                    if resp_repay_draw and len(resp_repay_draw) >= 1 and resp_repay_draw[0] == 0:
                        claimed_draws += 1
                        logger.info("周末活跃回馈转盘抽取成功！")
            except Exception as e:
                logger.debug("周末活跃回馈抽奖跳过: %s", e)

            msg = f"周末狂欢巡检完成: 成功领取 {claimed_packs} 个周末大礼包，开启 {entrusts_set} 项减负委托，完成 {claimed_draws} 次免费转盘抽取"
            logger.info(msg)
            return TaskResult.success(msg, data={"claimed_packs": claimed_packs, "entrusts_set": entrusts_set, "claimed_draws": claimed_draws})

        except Exception as exc:
            logger.warning("周末狂欢处理异常 (安全跳过): %s", exc)
            return TaskResult.skipped(f"周末狂欢功能暂未开启: {exc}")
