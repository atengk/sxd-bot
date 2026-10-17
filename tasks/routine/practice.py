"""神仙道角色城镇打坐与挂机练功自动化任务 (Mod 0: Player.start_practice)

在日常主线任务结束后或守护空闲时，指令角色进入打坐挂机练功状态，保障离线与空闲收益。

@author Ateng
@since 2026-10-16
"""

import logging
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder

logger = logging.getLogger(__name__)


class PracticeTask(BaseTask):
    """城镇挂机打坐练功任务

    @author Ateng
    @since 2026-10-16
    """

    name = "PracticeTask"
    interval_sec = 0.0  # 单次流水线收官任务

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行角色挂机打坐修行经验签收与持续打坐指令"""
        logger.info("开始执行角色城镇挂机打坐修行经验结算与续练流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于有效长连接状态，跳过练功任务")

        claimed_exp = 0
        claimed_auras = 0
        try:
            # 1. 查询现代练功修行系统累积经验与灵气 (Mod 584, Act 1: get_practice_info)
            from protocol.packet import ByteArrayReader
            try:
                req_info = PacketBuilder(mod=584, act=1).build()
                resp_info = await client.request(req_info, timeout_sec=2.5)
                if resp_info and len(resp_info) >= 20:
                    reader = ByteArrayReader(resp_info)
                    status = reader.read_uint8()
                    aura_cnt = reader.read_uint16() if reader.remaining >= 2 else 0
                    auras = []
                    for _ in range(aura_cnt):
                        if reader.remaining >= 8:
                            aid = reader.read_int32()
                            acount = reader.read_int32()
                            auras.append((aid, acount))
                    if reader.remaining >= 16:
                        reader.read_int32()
                        reader.read_int32()
                        accumulated_exp = reader.read_int64()
                        if accumulated_exp > 0:
                            claimed_exp = accumulated_exp
                    claimed_auras = sum(a[1] for a in auras)
                    logger.info("练功修行状态同步: 累积经验=%d, 待采灵气=%d", claimed_exp, claimed_auras)
            except Exception as e:
                logger.debug("查询现代练功修行状态跳过: %s", e)

            # 2. 一键聚气汇集灵气 (Mod 584, Act 2: collect_air)
            try:
                req_air = PacketBuilder(mod=584, act=2).build()
                await client.send_packet(req_air)
                logger.debug("已提交一键聚气指令 (Mod 584, Act 2)")
            except Exception as e:
                logger.debug("一键聚气跳过: %s", e)

            # 3. 一键全收累积挂机经验与灵气 (Mod 584, Act 3: collect_all)
            try:
                req_all = PacketBuilder(mod=584, act=3).build()
                resp_all = await client.request(req_all, timeout_sec=2.5)
                if resp_all and len(resp_all) >= 10:
                    reader_all = ByteArrayReader(resp_all)
                    reader_all.read_uint8()  # status
                    acnt = reader_all.read_uint16() if reader_all.remaining >= 2 else 0
                    for _ in range(acnt):
                        if reader_all.remaining >= 8:
                            reader_all.read_int32()
                            reader_all.read_int32()
                    if reader_all.remaining >= 8:
                        got_exp = reader_all.read_int64()
                        if got_exp > 0:
                            claimed_exp = got_exp
                    logger.info("已成功一键签收练功修行挂机经验与灵气: +%d 经验入账！", claimed_exp)
            except Exception as e:
                logger.debug("一键领取练功经验跳过: %s", e)

            # 4. 兼容性旧版打坐经验查询签收 (Mod 0, Act 37/38)
            try:
                req_data = PacketBuilder(mod=0, act=37).build()
                resp_data = await client.request(req_data, timeout_sec=1.5)
                if resp_data and len(resp_data) >= 20:
                    r0 = ByteArrayReader(resp_data)
                    r0.read_int16()
                    r0.read_int16()
                    r0.read_int32()
                    r0.read_int32()
                    old_exp = r0.read_int64() if r0.remaining >= 8 else 0
                    if old_exp > 0:
                        req_finish = PacketBuilder(mod=0, act=38).build()
                        await client.send_packet(req_finish)
                        claimed_exp += old_exp
                        logger.info("已签收城镇打坐修行经验: +%d 经验", old_exp)
            except Exception:
                pass

            # 5. 发送角色打坐练功指令无缝续练 (Mod 0, Act 36: start_practice)
            req_practice = PacketBuilder(mod=0, act=36).build()
            await client.send_packet(req_practice)
            logger.info("已成功向服务端提交角色打坐练功挂机指令 (Mod 0, Act 36)")

            msg = f"角色打坐练功已完成结算与续练 (本次结算经验: {claimed_exp} 点, 灵气: {claimed_auras} 个)"
            return TaskResult.success(msg, data={"practice_active": True, "claimed_exp": claimed_exp, "claimed_auras": claimed_auras})

        except Exception as exc:
            logger.warning("激活打坐练功异常 (安全跳过): %s", exc)
            return TaskResult.skipped(f"激活打坐练功跳过: {exc}")
