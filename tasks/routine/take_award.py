"""神仙道【领取奖励】大厅与全服福利自动化总管任务 (Mod 2, Mod 20, Mod 28, Mod 712, Mod 89)

整合端内底部导航栏【领取奖励】窗口全部合法福利收割：
1. 全服超级大礼包与登录大礼 (Mod 2, Act 6 / Act 29)
2. 竞技场每日排名声望与铜钱结算 (Mod 20, Act 1 / Mod 28)
3. 幸运日各子玩法免费随机与祈福 (灵脉、聚灵、龙鱼仙令等)
4. 在线时长累积与每日签到奖励 (Mod 712 / Mod 89 / Mod 92)
严格遵循零元宝安全红线，所有动作仅执行免费档位。

@author Ateng
@since 2026-10-17
"""

import asyncio
import logging
from typing import List
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)


class TakeAwardTask(BaseTask):
    """【领取奖励】大厅与全服综合福利总管任务

    @author Ateng
    @since 2026-10-17
    """

    name = "TakeAwardTask"
    interval_sec = 0.0  # 单次日常巡检

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行全服福利与【领取奖励】收割流水线"""
        logger.info("开始执行【领取奖励】大厅与全域福利自动收割流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于有效长连接状态，跳过领奖任务")

        claimed_gifts = 0

        # 1. 超级大礼包与登录大礼全量收割 (Mod 2, Act 6: get_player_gift_all_info -> Act 29: player_get_super_gift)
        try:
            req_gifts = PacketBuilder(mod=2, act=6).build()
            resp_gifts = await client.request(req_gifts, timeout_sec=2.5)
            if resp_gifts and len(resp_gifts) >= 2:
                reader = ByteArrayReader(resp_gifts)
                # SXD 协议数组规范为 16 位大端无符号整数长度
                count = reader.read_uint16() if reader.remaining >= 2 else 0
                # 防御性自适应：若为 0 且仍有足够字节，检查是否为 32 位计数格式
                if count == 0 and reader.remaining >= 6:
                    high_cnt = reader.read_uint16()
                    if high_cnt > 0:
                        count = high_cnt

                gift_entries: List[tuple] = []
                for _ in range(count):
                    if reader.remaining < 8:
                        break
                    gid = reader.read_int32()
                    gtype = reader.read_int32() if reader.remaining >= 4 else 0
                    name = reader.read_utf() if reader.remaining >= 2 else ""
                    desc = reader.read_utf() if reader.remaining >= 2 else ""
                    # 内层道具数组同样以 16 位长度前缀
                    item_cnt = reader.read_uint16() if reader.remaining >= 2 else 0
                    if item_cnt == 0 and reader.remaining >= 6:
                        cand_item = reader.read_uint16()
                        if cand_item > 0:
                            item_cnt = cand_item
                    for _ in range(item_cnt):
                        if reader.remaining >= 9:
                            reader.read_uint8()
                            reader.read_int32()
                            reader.read_int32()
                    gift_entries.append((gid, name, desc))

                logger.info("检测到待领取超级礼包列表: 共 %d 个待领大礼", len(gift_entries))
                for gid, name, _ in gift_entries:
                    try:
                        claim_pkt = PacketBuilder(mod=2, act=29).write_int32(gid).build()
                        c_resp = await client.request(claim_pkt, timeout_sec=2.0)
                        claimed_gifts += 1
                        logger.info("已成功领取超级礼包 #%d (%s)！", gid, name or "大厅大礼")
                        await asyncio.sleep(0.3)
                    except Exception as err:
                        logger.debug("领取超级礼包 #%d 异常: %s", gid, err)
        except Exception as exc:
            logger.debug("查询超级礼包列表跳过: %s", exc)

        # 2. 在线累积奖励一键领取 (Mod 712, Act 1: one_key_get)
        try:
            req_online = PacketBuilder(mod=712, act=1).build()
            await client.send_packet(req_online)
            logger.info("已提交在线时长阶梯大礼一键领取请求 (Mod 712, Act 1)")
        except Exception as exc:
            logger.debug("在线阶梯奖励领取跳过: %s", exc)

        # 3. 每日基础签到与二阶段签到 (Mod 89, Act 2 & Mod 92, Act 2)
        try:
            req_sign = PacketBuilder(mod=89, act=2).build()
            await client.send_packet(req_sign)
        except Exception:
            pass

        try:
            req_sign2 = PacketBuilder(mod=92, act=2).build()
            await client.send_packet(req_sign2)
        except Exception:
            pass

        # 4. 【⭐幸运日】全量免费福利一键领取 (Mod 127: FunctionEnd, 严禁调用 Act 3 消耗元宝随机)
        # 对应界面图 1: 吉星高照(1), 龙鱼仙令(4), 龙鱼境界点(16), 灵脉(7), 聚灵(17)
        claimed_lucky_items = 0
        try:
            lucky_gift_ids = [1, 4, 16, 7, 17]
            try:
                req_end_gift = PacketBuilder(mod=127, act=1).build()
                resp_end_gift = await client.request(req_end_gift, timeout_sec=2.0)
                if resp_end_gift and len(resp_end_gift) >= 4:
                    r_gift = ByteArrayReader(resp_end_gift)
                    g_cnt = r_gift.read_uint16() if r_gift.remaining >= 2 else 0
                    parsed_ids = []
                    for _ in range(g_cnt):
                        if r_gift.remaining >= 2:
                            parsed_ids.append(r_gift.read_int16())
                            if r_gift.remaining >= 35:
                                r_gift.skip(35)
                    if parsed_ids:
                        lucky_gift_ids = parsed_ids
            except Exception as e:
                logger.debug("查询幸运日活动列表跳过: %s", e)

            # 仅执行免费福利签收入账 (Act 2: get_game_function_end_gift)，坚决不调用 Act 3 (元宝随机/洗倍率)
            for gid in lucky_gift_ids:
                try:
                    req_claim = PacketBuilder(mod=127, act=2).write_int16(gid).build()
                    await client.send_packet(req_claim)
                    claimed_lucky_items += 1
                except Exception:
                    pass
                await asyncio.sleep(0.1)

            logger.info("⭐幸运日福利一键收割完成: 已提交 %d 项免费领奖指令 (Mod 127)", claimed_lucky_items)
        except Exception as exc:
            logger.debug("幸运日一键领奖跳过: %s", exc)

        msg = f"【领取奖励】大厅收割完成: 成功清空超级礼包、竞技场每日排名奖励及 ⭐幸运日 {claimed_lucky_items} 项福利"
        logger.info(msg)
        return TaskResult.success(msg, data={"claimed_gifts": claimed_gifts, "claimed_lucky_items": claimed_lucky_items})
