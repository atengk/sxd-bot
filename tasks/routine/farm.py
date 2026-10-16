"""神仙道仙府药园种植、收获与仙令福利自动化流水线任务 (Mod 13, Mod_Farm_Base)

对接官方微端最新版仙府药园协议，自动巡检角色已开垦土地，对成熟作物进行单倍安全收获，
对空闲土地自动播种经验或铜钱仙草，自动领取每日仙令礼包，严格遵循零元宝安全红线。

@author Ateng
@since 2026-10-16
"""

import logging
from typing import List, Dict, Any
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from network.client import SXDClient
from protocol.builder import PacketBuilder
from protocol.packet import ByteArrayReader

logger = logging.getLogger(__name__)


class FarmTask(BaseTask):
    """仙府药园自动化任务

    @author Ateng
    @since 2026-10-16
    """

    name = "FarmTask"
    interval_sec = 0.0  # 单次日常巡检

    # 默认保底种植的仙草种子 ID (169: 经验草, 175: 铜钱草)
    DEFAULT_SEED_ID = 169

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info("开始执行仙府药园作物巡检、收获与自动种植流水线...")

        if not ctx.is_connected:
            return TaskResult.skipped("未处于网络连接状态，跳过药园任务")

        harvested_count = 0
        planted_count = 0
        xianling_claimed = False

        # 1. 查询新版土地列表 (Mod 13, Act 21: get_new_farmlandinfo_list)
        try:
            req_lands = PacketBuilder(mod=13, act=21).build()
            resp_lands = await client.request(req_lands, timeout_sec=3.0)
            logger.info("成功同步新版药园土地数据 (回包长度: %d 字节)", len(resp_lands))

            lands = self._decode_farmlands(resp_lands)
            logger.info("药园当前已开垦土地总数: %d 块", len(lands))

        except Exception as exc:
            logger.warning("查询新版药园土地信息失败: %s", exc)
            return TaskResult.skipped("仙府药园土地数据同步超时或尚未开放")

        # 2. 查询可用仙草种子列表 (Mod 13, Act 22: new_farmland_herbs_list)
        available_seeds = await self._fetch_available_seeds(client)
        chosen_seed_id = available_seeds[0] if available_seeds else self.DEFAULT_SEED_ID

        # 3. 遍历土地执行成熟收获与空地播种
        for land in lands:
            land_id = land.get("farmland_id", 0)
            herbs_id = land.get("herbs_id", 0)
            remain_sec = land.get("farmland_time", 0)

            # 3.1 成熟作物执行一键安全收获 (Mod 13, Act 25: harvest_new，绝不消耗元宝)
            if herbs_id != 0 and remain_sec <= 0:
                logger.info("检测到土地 #%d 仙草已成熟，执行单倍安全收获 (零元宝)...", land_id)
                try:
                    harvest_pkt = PacketBuilder(mod=13, act=25).write_int32(land_id).build()
                    h_resp = await client.request(harvest_pkt, timeout_sec=2.0)
                    if len(h_resp) > 0 and h_resp[0] == 8:  # 0x08 = SUCCESS
                        harvested_count += 1
                        logger.info("土地 #%d 仙草收获成功！", land_id)
                except Exception as exc:
                    logger.warning("土地 #%d 收获失败: %s", land_id, exc)

            # 3.2 空闲土地执行自动播种 (Mod 13, Act 24: plant_new_herbs，零元宝)
            elif herbs_id == 0:
                logger.info("检测到土地 #%d 为空闲土地，自动播种仙草种子 #%d...", land_id, chosen_seed_id)
                try:
                    plant_pkt = PacketBuilder(mod=13, act=24).write_int32(land_id).write_int32(chosen_seed_id).build()
                    p_resp = await client.request(plant_pkt, timeout_sec=2.0)
                    if len(p_resp) > 0 and p_resp[0] == 8:  # 0x08 = SUCCESS
                        planted_count += 1
                        logger.info("土地 #%d 成功播种仙草种子 #%d！", land_id, chosen_seed_id)
                except Exception as exc:
                    logger.warning("土地 #%d 播种失败: %s", land_id, exc)
            else:
                logger.debug("土地 #%d 仙草正在茁壮成长 (剩余倒计时: %d 秒)", land_id, remain_sec)

        # 4. 每日仙令礼包巡检与领取 (Mod 13, Act 19 -> Act 20)
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

        summary = f"药园流水线完成: 收获 {harvested_count} 块, 补种 {planted_count} 块, 仙令礼包={'已领取' if xianling_claimed else '今日已领/不可领'}"
        logger.info(summary)
        return TaskResult.success(summary, data={
            "harvested_count": harvested_count,
            "planted_count": planted_count,
            "xianling_claimed": xianling_claimed,
            "total_farmlands": len(lands),
        })

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
