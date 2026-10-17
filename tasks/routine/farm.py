"""神仙道仙府药园种植、收获与果园仙树全自动化流水线任务 (Mod 13, Mod 135)

整合“我的药园”与“果园”全域生态：
1. 经典药园土地巡检 (Mod 13, Act 0: get_farmlandinfo_list)
2. 经典伙伴仙草经验/铜钱播种与收获 (Mod 13, Act 1 / Act 5 / Act 6)
3. 新版药园土地作物巡检、单倍收获与补种 (Mod 13, Act 21 / Act 22 / Act 24 / Act 25)
4. 果园仙树铜钱与修行经验免费采摘 (Mod 135: FairyTree, Act 0 / Act 2 / Act 3 / Act 4)
5. 仙令树免费礼包与摇钱树免费次数巡检 (Mod 13, Act 19 / Act 20 / Act 12 / Act 13)
严格遵循零元宝安全红线，所有动作仅执行免费单倍档位，坚决不消耗元宝加速或翻倍。

@author Ateng
@since 2026-10-17
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)


class FarmTask(BaseTask):
    """仙府药园与果园全自动化综合总管任务

    @author Ateng
    @since 2026-10-17
    """

    name = "FarmTask"
    interval_sec = 0.0  # 单次日常巡检

    # 默认保底种植的仙草种子 ID (169: 经验草, 175: 铜钱草)
    DEFAULT_SEED_ID = 169

    def __init__(self, plant_type: Optional[str] = None) -> None:
        super().__init__()
        self.plant_type = plant_type

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行我的药园与果园全域自动化流水线"""
        logger.info("开始执行仙府药园与果园全域作物巡检、收获、播种与采摘流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过药园任务")

        effective_plant_type = self.plant_type or ctx.extra_props.get("farm_plant_type", "auto")
        harvested_count = 0
        planted_count = 0
        upgraded_lands_count = 0
        plant_type_desc = "经验树"
        xianling_claimed = False
        fairy_tree_count = 0

        # // 1. 经典药园土地巡检、仙露升级与智能补种 (Mod 13, Act 0 / Act 1 / Act 5 / Act 6 / Act 15 / Act 16)
        try:
            req_c_lands = PacketBuilder(mod=13, act=0).build()
            resp_c_lands = await client.request(req_c_lands, timeout_sec=2.5)
            if resp_c_lands and len(resp_c_lands) >= 2:
                reader_c = ByteArrayReader(resp_c_lands)
                c_cnt = reader_c.read_uint16() if reader_c.remaining >= 2 else 0
                c_lands: List[Dict[str, Any]] = []
                for _ in range(c_cnt):
                    if reader_c.remaining < 8:
                        break
                    lid = reader_c.read_int32()
                    rid = reader_c.read_int32()
                    rname = reader_c.read_utf() if reader_c.remaining >= 2 else ""
                    hname = reader_c.read_utf() if reader_c.remaining >= 2 else ""
                    htype = reader_c.read_int32() if reader_c.remaining >= 4 else 0
                    hexp = reader_c.read_int64() if reader_c.remaining >= 8 else 0
                    hcoin = reader_c.read_int64() if reader_c.remaining >= 8 else 0
                    grow_time = reader_c.read_int32() if reader_c.remaining >= 4 else 0
                    plant_time = reader_c.read_int32() if reader_c.remaining >= 4 else 0
                    star = reader_c.read_int32() if reader_c.remaining >= 4 else 0
                    is_plant = reader_c.read_uint8() if reader_c.remaining >= 1 else 0
                    level = reader_c.read_uint8() if reader_c.remaining >= 1 else 0
                    is_double = reader_c.read_int8() if reader_c.remaining >= 1 else 0

                    c_lands.append({
                        "farmland_id": lid,
                        "player_role_id": rid,
                        "is_plant": is_plant,
                        "grow_time": grow_time,
                        "level": level,
                    })

                # 解析可用仙露存量 (dew_count)
                dew_count = reader_c.read_int32() if reader_c.remaining >= 4 else 0
                _ = reader_c.read_int32() if reader_c.remaining >= 4 else 0

                if c_lands:
                    logger.info("已同步经典药园土地: 共 %d 块, 可用仙露: %d 滴", len(c_lands), dew_count)

                    # 1.1 成熟作物一键单倍安全收获 (Mod 13, Act 6: harvest(farmland_id, is_double=0))
                    for cl in c_lands:
                        lid = cl["farmland_id"]
                        if cl["is_plant"] != 0 and cl["grow_time"] <= 0:
                            try:
                                h_pkt = PacketBuilder(mod=13, act=6).write_int32(lid).write_uint8(0).build()
                                h_resp = await client.request(h_pkt, timeout_sec=2.0)
                                if h_resp and len(h_resp) >= 1 and h_resp[0] in (0, 8):
                                    harvested_count += 1
                                    cl["is_plant"] = 0  # 收获后地块重置为空闲
                                    logger.info("经典药园土地 #%d 仙草成功收获！", lid)
                            except Exception as e:
                                logger.debug("经典药园土地 #%d 收获异常: %s", lid, e)

                    # 1.2 仙露土地品阶安全巡检升级 (Mod 13, Act 15 预检 + Act 16 升级)
                    if dew_count > 0:
                        upgraded_lands_count = await self._upgrade_lands_with_dew(client, c_lands, dew_count)

                    # 1.3 经验树与发财树智能决策与补种 (Mod 13, Act 5: plant_herbs)
                    candidate_role_id, needs_exp = await self._fetch_best_cultivation_role(client, ctx)

                    if effective_plant_type == "exp_only":
                        herbs_type = 2  # EXP_HERBS (经验树)
                        target_role_id = candidate_role_id
                        plant_type_desc = f"经验树(指定: 伙伴 #{candidate_role_id})"
                    elif effective_plant_type == "coin_only":
                        herbs_type = 3  # COIN_HERBS (发财树)
                        target_role_id = ctx.player_id or 4
                        plant_type_desc = "发财树(指定: 铜钱入库)"
                    else:  # "auto"
                        if needs_exp:
                            herbs_type = 2
                            target_role_id = candidate_role_id
                            plant_type_desc = f"经验树(自适应: 伙伴 #{candidate_role_id})"
                        else:
                            herbs_type = 3
                            target_role_id = ctx.player_id or 4
                            plant_type_desc = "发财树(自适应: 全员满级转产铜钱)"

                    for cl in c_lands:
                        lid = cl["farmland_id"]
                        if cl["is_plant"] == 0:
                            try:
                                # herbs_type: 2=经验树, 3=发财树; is_double: 0 (普通单倍，零元宝)
                                p_pkt = (
                                    PacketBuilder(mod=13, act=5)
                                    .write_int32(lid)
                                    .write_int32(target_role_id)
                                    .write_uint8(herbs_type)
                                    .write_int8(0)
                                    .build()
                                )
                                p_resp = await client.request(p_pkt, timeout_sec=2.0)
                                if p_resp and len(p_resp) >= 1 and p_resp[0] in (0, 8):
                                    planted_count += 1
                                    cl["is_plant"] = 1
                                    logger.info("经典药园土地 #%d 成功播种【%s】！", lid, plant_type_desc)
                            except Exception as e:
                                logger.debug("经典药园土地 #%d 播种异常: %s", lid, e)
        except Exception as exc:
            logger.debug("经典药园巡检跳过: %s", exc)

        # // 2. 新版药园土地巡检、单倍收获与补种 (Mod 13, Act 21 / Act 22 / Act 24 / Act 25)
        try:
            req_lands = PacketBuilder(mod=13, act=21).build()
            resp_lands = await client.request(req_lands, timeout_sec=3.0)
            if resp_lands and len(resp_lands) >= 2:
                logger.info("成功同步新版药园土地数据 (回包长度: %d 字节)", len(resp_lands))
                lands = self._decode_farmlands(resp_lands)
                logger.info("新版药园当前已开垦土地总数: %d 块", len(lands))

                available_seeds = await self._fetch_available_seeds(client)
                chosen_seed_id = available_seeds[0] if available_seeds else self.DEFAULT_SEED_ID

                for land in lands:
                    land_id = land.get("farmland_id", 0)
                    herbs_id = land.get("herbs_id", 0)
                    remain_sec = land.get("farmland_time", 0)

                    # 成熟作物执行单倍安全收获 (Mod 13, Act 25: harvest_new，绝不消耗元宝)
                    if herbs_id != 0 and remain_sec <= 0:
                        logger.info("检测到新版土地 #%d 仙草已成熟，执行单倍安全收获 (零元宝)...", land_id)
                        try:
                            harvest_pkt = PacketBuilder(mod=13, act=25).write_int32(land_id).build()
                            h_resp = await client.request(harvest_pkt, timeout_sec=2.0)
                            if len(h_resp) > 0 and h_resp[0] in (0, 8):
                                harvested_count += 1
                                logger.info("土地 #%d 仙草收获成功！", land_id)
                        except Exception as exc:
                            logger.warning("土地 #%d 收获失败: %s", land_id, exc)

                    # 空闲土地执行自动播种 (Mod 13, Act 24: plant_new_herbs，零元宝)
                    elif herbs_id == 0:
                        logger.info("检测到新版土地 #%d 为空闲土地，自动播种仙草种子 #%d...", land_id, chosen_seed_id)
                        try:
                            plant_pkt = PacketBuilder(mod=13, act=24).write_int32(land_id).write_int32(chosen_seed_id).build()
                            p_resp = await client.request(plant_pkt, timeout_sec=2.0)
                            if len(p_resp) > 0 and p_resp[0] in (0, 8):
                                planted_count += 1
                                logger.info("土地 #%d 成功播种仙草种子 #%d！", land_id, chosen_seed_id)
                        except Exception as exc:
                            logger.warning("土地 #%d 播种失败: %s", land_id, exc)
                    else:
                        logger.debug("土地 #%d 仙草正在茁壮成长 (剩余倒计时: %d 秒)", land_id, remain_sec)
        except Exception as exc:
            logger.debug("新版药园土地数据同步跳过: %s", exc)

        # // 3. 果园仙树巡检与免费采摘 (Mod 135: FairyTree)
        try:
            req_ft_open = PacketBuilder(mod=135, act=0).build()
            resp_ft_open = await client.request(req_ft_open, timeout_sec=2.0)
            if resp_ft_open and len(resp_ft_open) >= 1 and resp_ft_open[0] == 0:  # 0=OPEN
                logger.info("检测到果园仙树系统已开放 (Mod 135)，执行仙树铜钱与经验免费采摘...")
                # 采摘仙树铜钱 (Mod 135, Act 3: use_fairy_tree_coin)
                try:
                    req_coin = PacketBuilder(mod=135, act=3).build()
                    resp_coin = await client.request(req_coin, timeout_sec=2.0)
                    if resp_coin and len(resp_coin) >= 1 and resp_coin[0] in (0, 2):
                        fairy_tree_count += 1
                        logger.info("果园仙树免费铜钱采摘成功！")
                except Exception as ex:
                    logger.debug("果园仙树采摘铜钱跳过: %s", ex)

                # 采摘仙树修行经验 (Mod 135, Act 4: use_fairy_tree_expr)
                try:
                    target_pid = ctx.player_id or 4
                    req_expr = PacketBuilder(mod=135, act=4).write_int32(target_pid).write_int16(1).write_int16(1).build()
                    resp_expr = await client.request(req_expr, timeout_sec=2.0)
                    if resp_expr and len(resp_expr) >= 1 and resp_expr[0] in (0, 2):
                        fairy_tree_count += 1
                        logger.info("果园仙树免费修行经验采摘成功！")
                except Exception as ex:
                    logger.debug("果园仙树采摘经验跳过: %s", ex)
        except Exception as exc:
            logger.debug("果园仙树系统巡检跳过: %s", exc)

        # // 4. 每日仙令树礼包与摇钱树免费次数巡检 (Mod 13, Act 19 / Act 20 / Act 12 / Act 13)
        try:
            xlg_req = PacketBuilder(mod=13, act=19).build()
            xlg_resp = await client.request(xlg_req, timeout_sec=2.0)
            if len(xlg_resp) > 0 and xlg_resp[0] != 0:
                logger.info("检测到有可领取的仙府仙令礼包，执行安全领取 (Mod 13, Act 20)...")
                claim_req = PacketBuilder(mod=13, act=20).build()
                claim_resp = await client.request(claim_req, timeout_sec=2.0)
                if len(claim_resp) > 0:
                    xianling_claimed = True
                    logger.info("仙府仙令礼包领取成功！")
        except Exception as exc:
            logger.debug("仙令礼包巡检跳过: %s", exc)

        try:
            req_tree_info = PacketBuilder(mod=13, act=12).build()
            resp_tree_info = await client.request(req_tree_info, timeout_sec=2.0)
            if resp_tree_info and len(resp_tree_info) >= 16:
                t_reader = ByteArrayReader(resp_tree_info)
                used_t = t_reader.read_int32()
                free_t = t_reader.read_int32()
                if free_t > used_t:
                    req_tb = PacketBuilder(mod=13, act=13).build()
                    resp_tb = await client.request(req_tb, timeout_sec=2.0)
                    if resp_tb and len(resp_tb) >= 1 and resp_tb[0] in (0, 8):
                        logger.info("果园摇钱树免费次数摇奖成功！")
        except Exception as exc:
            logger.debug("果园摇钱树免费次数巡检跳过: %s", exc)

        summary = (
            f"药园与果园全域巡检完成: 仙草收获 {harvested_count} 块, 补种 {planted_count} 块 ({plant_type_desc}), "
            f"土地升级 {upgraded_lands_count} 次, 果园仙树采摘 {fairy_tree_count} 次, "
            f"仙令礼包={'已领取' if xianling_claimed else '今日已领/不可领'}"
        )
        logger.info(summary)
        return TaskResult.success(summary, data={
            "harvested_count": harvested_count,
            "planted_count": planted_count,
            "upgraded_lands_count": upgraded_lands_count,
            "plant_type_desc": plant_type_desc,
            "fairy_tree_count": fairy_tree_count,
            "xianling_claimed": xianling_claimed,
        })

    async def _fetch_best_cultivation_role(self, client: SXDClient, ctx: GameContext) -> Tuple[int, bool]:
        """获取最适宜药园传功经验培养的伙伴角色 ID 及是否需要经验 (Mod 13, Act 1)

        优先挑选当前等级低于主角等级 (role_lvl < ctx.level) 的待培养伙伴；
        若全部伙伴均已达到或超过主角等级（如大号全员 Lv.300），则 needs_exp = False。

        Args:
            client: 异步长连接客户端。
            ctx: 全局游戏上下文。

        Returns:
            (目标角色 ID, 是否存在待培养伙伴 needs_exp)
        """
        candidate_role_id = ctx.player_id or 4
        needs_exp = False
        try:
            req_roles = PacketBuilder(mod=13, act=1).build()
            resp_roles = await client.request(req_roles, timeout_sec=2.0)
            if resp_roles and len(resp_roles) >= 2:
                reader = ByteArrayReader(resp_roles)
                cnt = reader.read_uint16()
                underleveled: List[Tuple[int, int]] = []
                for _ in range(cnt):
                    if reader.remaining < 4:
                        break
                    role_id = reader.read_int32()
                    _ = reader.read_utf() if reader.remaining >= 2 else ""
                    _ = reader.read_utf() if reader.remaining >= 2 else ""
                    role_lvl = reader.read_int32() if reader.remaining >= 4 else 0
                    if reader.remaining >= 29:
                        reader.skip(29)
                    if role_lvl < ctx.level:
                        underleveled.append((role_id, role_lvl))

                if underleveled:
                    # 优先挑选当前等级最低的伙伴
                    underleveled.sort(key=lambda x: x[1])
                    candidate_role_id = underleveled[0][0]
                    needs_exp = True
        except Exception as exc:
            logger.debug("获取药园伙伴列表跳过: %s", exc)
        return candidate_role_id, needs_exp

    async def _upgrade_lands_with_dew(
        self,
        client: SXDClient,
        c_lands: List[Dict[str, Any]],
        available_dew: int,
    ) -> int:
        """使用存量仙露安全升级土地品阶 (Mod 13, Act 15 预检 + Act 16 升级)

        严格按照最低等级优先原则，采用三重零元宝熔断防御：
        1. 存量守卫：available_dew <= 0 直接返回；
        2. 元宝预检：调用 ingot_for_farmland(lid)，若需元宝 > 0 且仙露不足直接跳过；
        3. 状态熔断：调用 up_farmland_level(lid)，若返回非 SUCCESS(8) 立即熔断终止后续升级。

        Args:
            client: 异步长连接客户端。
            c_lands: 土地字典列表。
            available_dew: 仙露可用存量。

        Returns:
            成功升级的土地次数。
        """
        upgraded_count = 0
        cur_dew = available_dew
        logger.info("检测到持有仙露 x%d，开始执行土地品阶巡检升级 (最低等级优先)...", cur_dew)

        while cur_dew > 0:
            # 按等级升序排序，挑选最低等级的土地
            c_lands.sort(key=lambda x: (x.get("level", 0), x.get("farmland_id", 0)))
            target_land = c_lands[0]
            lid = target_land["farmland_id"]
            cur_lvl = target_land.get("level", 0)

            # 1. 预检升级所需元宝 (Mod 13, Act 15: ingot_for_farmland)
            try:
                p_probe = PacketBuilder(mod=13, act=15).write_int32(lid).build()
                resp_probe = await client.request(p_probe, timeout_sec=2.0)
                if resp_probe and len(resp_probe) >= 4:
                    r_probe = ByteArrayReader(resp_probe)
                    needed_ingot = r_probe.read_int32()
                    if needed_ingot > 0:
                        logger.info("土地 #%d 升级需消耗 %d 元宝，触发零元宝守卫中断升级", lid, needed_ingot)
                        break
            except Exception as e:
                logger.debug("土地 #%d 升级元宝预检异常: %s", lid, e)

            # 2. 尝试执行仙露升级 (Mod 13, Act 16: up_farmland_level)
            try:
                up_pkt = PacketBuilder(mod=13, act=16).write_int32(lid).build()
                resp_up = await client.request(up_pkt, timeout_sec=2.0)
                if resp_up and len(resp_up) >= 1:
                    code = resp_up[0]
                    if code in (0, 8):  # SUCCESS=8
                        upgraded_count += 1
                        cur_dew -= 1
                        target_land["level"] = cur_lvl + 1
                        logger.info("土地 #%d 成功升级至 Lv.%d (剩余仙露: %d)", lid, cur_lvl + 1, cur_dew)
                    else:
                        logger.info("土地 #%d 升级返回状态码 %d，立即熔断后续土地升级", lid, code)
                        break
                else:
                    break
            except Exception as ex:
                logger.warning("土地 #%d 升级异常，熔断退出: %s", lid, ex)
                break

        return upgraded_count

    def _decode_farmlands(self, payload: bytes) -> List[Dict[str, Any]]:
        """解包新版药园土地列表 (Mod 13, Act 21)

        Args:
            payload: 服务端回包字节载荷。

        Returns:
            土地属性字典列表。
        """
        if len(payload) < 2:
            return []

        reader = ByteArrayReader(payload)
        count = reader.read_uint16()
        lands: List[Dict[str, Any]] = []

        # 每块土地固定占用 19 字节
        for _ in range(count):
            if reader.remaining < 19:
                break
            land_id = reader.read_int32()
            herbs_id = reader.read_int32()
            farmland_time = reader.read_int32()
            level = reader.read_uint8()
            is_plant = reader.read_uint8()
            # 剩余 5 字节扩展字段
            _ = reader.read_bytes(5)

            lands.append({
                "farmland_id": land_id,
                "herbs_id": herbs_id,
                "farmland_time": farmland_time,
                "farmland_level": level,
                "is_plant": is_plant,
                "is_empty": herbs_id == 0,
                "is_mature": herbs_id > 0 and farmland_time <= 0,
            })

        return lands

    async def _fetch_available_seeds(self, client: SXDClient) -> List[int]:
        """获取当前角色可用仙草种子列表 (Mod 13, Act 22)

        Args:
            client: 异步长连接客户端。

        Returns:
            可用种子 ID 列表。
        """
        try:
            req_seed = PacketBuilder(mod=13, act=22).build()
            resp_seed = await client.request(req_seed, timeout_sec=2.0)
            if len(resp_seed) < 2:
                return []

            reader = ByteArrayReader(resp_seed)
            seed_count = reader.read_uint16()
            seeds: List[int] = []

            for _ in range(seed_count):
                if reader.remaining < 20:
                    break
                sid = reader.read_int32()
                _ = reader.read_bytes(16)
                seeds.append(sid)

            return seeds
        except Exception:
            return []
