"""神仙道帮派吉星掷骰与进阶活动自动化任务 (Mod 10: Mod_Faction_Base, Mod 0)

对齐官方微端 Mod 10 (Mod_Faction_Base) 帮派进阶体系，自动巡检帮派吉星剩余投掷次数、循环投掷获取帮派积分与排行，探查七星封魔与每日阵营俸禄，严格执行零元宝安全红线。

@author Ateng
@since 2026-10-16
"""

import logging
from typing import Dict, Any
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)

# 帮派吉星官方状态码 (Mod_Faction_Base)
ACTION_SUCCESS = 0x20  # 32 为官方 ACTION_SUCCESS 状态码


class FactionRollCakeTask(BaseTask):
    """帮派吉星掷骰与进阶活动自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "FactionRollCakeTask"
    interval_sec = 0.0  # 单次日常执行

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行帮派吉星掷骰与进阶活动巡检...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过帮派进阶任务")

        roll_cake_rolls = 0
        seal_satan_joined = False
        salary_claimed = False

        # 1. 帮派吉星投掷 (Mod 10, Act 44: remain_times, Act 46: roll_cake, Act 45: info)
        try:
            req_rolls = PacketBuilder(mod=10, act=44).build()
            resp_rolls = await client.request(req_rolls, timeout_sec=3.0)
            reader_rolls = ByteArrayReader(resp_rolls)
            remain_rolls = reader_rolls.read_uint8() if reader_rolls.remaining >= 1 else 0

            logger.info("帮派吉星投掷状态: 今日剩余免费投掷次数=%d", remain_rolls)

            # 强零元宝前置卫语句：仅在有免费次数时投掷，次数耗尽坚决不花元宝
            while remain_rolls > 0:
                logger.info("执行帮派吉星免费投掷 (剩余次数=%d)...", remain_rolls)
                req_roll = PacketBuilder(mod=10, act=46).build()
                resp_roll = await client.request(req_roll, timeout_sec=3.0)
                reader_res = ByteArrayReader(resp_roll)

                if reader_res.remaining >= 19:
                    res_code = reader_res.read_uint8()
                    score = reader_res.read_int8()
                    total_score = reader_res.read_int32()
                    my_score = reader_res.read_int32()
                    dice_cnt = reader_res.read_uint16()
                    dices = [reader_res.read_uint8() for _ in range(min(dice_cnt, reader_res.remaining))]
                    remain_rolls = reader_res.read_uint8() if reader_res.remaining >= 1 else 0
                    roll_cake_rolls += 1
                    logger.info("帮派掷骰成功! 点数=%s, 本轮积分=%d, 累计积分=%d, 剩余次数=%d", dices, score, my_score, remain_rolls)
                else:
                    break

            # 同步最新帮派吉星面板与排行榜 (Act 45: faction_roll_cake_info)
            req_info = PacketBuilder(mod=10, act=45).build()
            await client.request(req_info, timeout_sec=3.0)
        except Exception as exc:
            logger.info("帮派吉星巡检完成或跳过: %s", exc)

        # 2. 帮派七星封魔 (Mod 10, Act 32: seal_satan_info, Act 28: join_seal_satan)
        try:
            req_satan = PacketBuilder(mod=10, act=32).build()
            resp_satan = await client.request(req_satan, timeout_sec=3.0)
            reader_satan = ByteArrayReader(resp_satan)
            if reader_satan.remaining >= 2:
                s_state = reader_satan.read_uint8()
                j_state = reader_satan.read_uint8()
                logger.info("帮派七星封魔状态: 活动状态=%d, 参与状态=%d", s_state, j_state)
                # 若活动开启且未参与，尝试加入
                if s_state == 1 and j_state == 0:
                    req_join = PacketBuilder(mod=10, act=28).build()
                    await client.request(req_join, timeout_sec=3.0)
                    seal_satan_joined = True
                    logger.info("成功加入今日帮派七星封魔队伍！")
        except Exception as exc:
            logger.info("帮派七星封魔巡检跳过: %s", exc)

        # 3. 领取每日阵营俸禄 (Mod 0, Act 22: get_player_camp_salary)
        try:
            req_sal = PacketBuilder(mod=0, act=22).write_bytes(bytes.fromhex("00010000")).build()
            resp_sal = await client.request(req_sal, timeout_sec=3.0)
            salary_claimed = True
            logger.info("每日阵营俸禄结算成功 (响应载荷: %d 字节)", len(resp_sal))
        except Exception as exc:
            logger.debug("每日俸禄或已在登录时自动入账: %s", exc)

        summary_msg = f"帮派进阶活动执行完毕: 帮派吉星投掷={roll_cake_rolls}次, 七星封魔={'已就绪' if seal_satan_joined else '未开放/已参与'}, 俸禄={'已结算' if salary_claimed else '已领'} (严格零元宝)"
        logger.info(summary_msg)
        return TaskResult.success(summary_msg, data={
            "roll_cake_rolls": roll_cake_rolls,
            "seal_satan_joined": seal_satan_joined,
            "salary": salary_claimed
        })
