"""神仙道版本更新福利与维护补偿自动化收割任务 (Mod 240: Mod_ReleaseWelfare_Base)

自动同步官方版本发布公告状态，一键全量领取版本更新礼包、额外元宝补偿及专属版本福利，严格恪守零成本白嫖原则。

@author Ateng
@since 2026-10-17
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)


class ReleaseWelfareTask(BaseTask):
    """版本更新福利自动化任务

    @author Ateng
    @since 2026-10-17
    """

    name = "ReleaseWelfareTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行版本更新福利领取流水线"""
        logger.info("开始执行版本更新福利与维护补偿巡检 (Mod 240: ReleaseWelfare)...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于有效长连接状态，跳过更新福利任务")

        claimed_items = 0
        try:
            # 1. 查询版本更新福利系统状态并动态解析待领礼包 (Mod 240, Act 0: get_info)
            from protocol.packet import ByteArrayReader
            welfare_ids = []
            try:
                req_info = PacketBuilder(mod=240, act=0).build()
                resp_info = await client.request(req_info, timeout_sec=2.5)
                logger.debug("更新福利状态响应长度: %d 字节", len(resp_info))
                if resp_info and len(resp_info) >= 14:
                    reader = ByteArrayReader(resp_info)
                    reader.read_int32()
                    reader.read_int32()
                    reader.read_int32()
                    w_cnt = reader.read_uint16() if reader.remaining >= 2 else 0
                    for _ in range(w_cnt):
                        if reader.remaining >= 1:
                            wid = reader.read_int8()
                            welfare_ids.append(wid)
                            if reader.remaining >= 27:
                                reader.skip(27)
            except Exception as e:
                logger.debug("查询更新福利状态跳过: %s", e)

            if not welfare_ids:
                welfare_ids = [0, 1, 2, 3]  # 防御性回退档位

            # 2. 遍历领取各档版本更新礼包 (Mod 240, Act 1: get_welfare) 与额外元宝补偿 (Act 3: get_extra_ingot)
            for wid in welfare_ids:
                try:
                    req_wel = PacketBuilder(mod=240, act=1).write_int8(wid).build()
                    await client.send_packet(req_wel)
                    claimed_items += 1
                except Exception:
                    pass
                try:
                    req_ingot = PacketBuilder(mod=240, act=3).write_int8(wid).build()
                    await client.send_packet(req_ingot)
                    claimed_items += 1
                except Exception:
                    pass

            # 3. 激活免费版本特权 (Mod 240, Act 2) 与领取专属大奖 (Act 4)
            try:
                req_priv = PacketBuilder(mod=240, act=2).build()
                await client.send_packet(req_priv)
            except Exception:
                pass

            try:
                req_extra = PacketBuilder(mod=240, act=4).build()
                await client.send_packet(req_extra)
            except Exception:
                pass

            # 4. 联动城镇版本更新反馈福利收割 (Mod 342, Act 0: get_feedback_info)
            try:
                req_town_fb = PacketBuilder(mod=342, act=0).build()
                await client.send_packet(req_town_fb)
                logger.info("已提交城镇更新反馈福利请求 (Mod 342, Act 0)")
            except Exception as e:
                logger.debug("城镇更新反馈福利跳过: %s", e)

            msg = f"版本更新福利与维护补偿巡检完成，已提交 {claimed_items} 项福利请求"
            logger.info(msg)
            return TaskResult.success(msg, data={"claimed_items": claimed_items})

        except Exception as exc:
            logger.warning("版本更新福利巡检异常 (安全跳过): %s", exc)
            return TaskResult.skipped(f"版本更新福利暂不可用: {exc}")
