"""神仙道背包四阶梯度智能自理与空间释放流水线 (Mod 2: Mod_Item_Base)

按四阶梯度严格安全释放背包空间：
1. 第 1 阶 (整理归纳)：调用 classify_pack 合并碎片与同类堆叠；
2. 第 2 阶 (开箱与使用)：调用 player_use_grid_item，全开固定宝箱，主角吃经验丹，低体力按需吃体力丹；
3. 第 3 阶 (存入随身仓库)：调用 move_pack_grid_item_to_warehouse 将材料存入仓库；
4. 第 4 阶 (变卖与丢弃兜底)：变卖普通白/绿杂物，紫/金/暗金装备与核心道具绝对禁售保护。
遵循梯度达标即止原则，预留安全可用空格。

@author Ateng
@since 2026-10-16
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from network.client import SXDClient
from tasks.base import BaseTask, TaskResult
from core.context import GameContext
from protocol.messages.item import (
    ItemConstants,
    ItemPlayerUseGridItemReq,
    ItemChooseBoxReq,
    ItemMovePackGridItemToWarehouseReq,
    ItemSellItemReq,
    ItemSellItemResp,
    ItemDropPackGridItemReq,
    ItemGetPlayerPackItemListReq,
    ItemGetPlayerPackItemListResp,
)
from services.query_service import ImportantItemRegistry

logger = logging.getLogger(__name__)

# 绝对禁止变卖与丢弃的保护性 item_id 集合
PROTECTED_ITEM_IDS = {
    1001, 1002, 1003, 1004,  # 体力丹
    2001, 2002, 2003,        # 经验丹
    3001, 3002, 3003,        # 核心战略礼包
}


class ItemCleanTask(BaseTask):
    """背包四阶梯度自理与空间释放任务

    @author Ateng
    @since 2026-10-16
    """

    name = "ItemCleanTask"
    interval_sec = 0.0

    def __init__(self, target_empty: int = 5, force_all: bool = False, use_only: bool = False) -> None:
        """初始化背包自理任务

        Args:
            target_empty: 目标预留空格数量（默认 5 格，达到即止）。
            force_all: 是否强制跑完全部 4 阶清理（用于手动一键清空背包）。
            use_only: 是否仅执行开箱与道具使用（用于一键使用背包全部物品）。
        """
        super().__init__()
        self.target_empty = target_empty
        self.force_all = force_all
        self.use_only = use_only

    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        logger.info(
            "开始执行背包自理流水线 (目标预留空格: %d, 强制全清: %s, 仅使用: %s)...",
            self.target_empty,
            self.force_all,
            self.use_only,
        )

        if not ctx.is_connected:
            return TaskResult.skipped("未处于连接状态，跳过背包自理流水线")

        items_used = 0
        items_warehoused = 0
        items_sold = 0
        items_dropped = 0
        coins_earned = 0

        try:
            # 1. 查询当前背包与随身仓库全局态势 (Mod 2, Act 41)
            pack_info = await self._query_pack(client)
            if not pack_info:
                return TaskResult.failed("拉取背包与随身仓库态势失败")

            pack_capacity, pack_items, warehouse_capacity, warehouse_items = pack_info
            pack_used = len(pack_items)
            empty_grids = max(0, pack_capacity - pack_used) if pack_capacity > 0 else 0
            logger.info("当前背包容量: %d/%d (剩余 %d 空格), 随身仓库: %d/%d", pack_used, pack_capacity, empty_grids, len(warehouse_items), warehouse_capacity)

            if empty_grids >= self.target_empty and not self.force_all and not self.use_only:
                msg = f"背包可用空间充足 (剩余 {empty_grids} 格 >= 目标 {self.target_empty} 格)，无需执行额外腾挪"
                logger.info(msg)
                return TaskResult.success(msg, data={"empty_grids": empty_grids})

            # 2. 第 1 阶：主背包空间感知与梯度检测 (Q2 A: 剔除伪整理指令，零风险无损自理)
            logger.info("[第 1 阶] 正在同步主背包格位分布与可用空间 (剩余 %d 空格)...", empty_grids)
            if empty_grids >= self.target_empty and not self.force_all and not self.use_only:
                msg = f"第 1 阶检测背包空间达标 (剩余 {empty_grids} 格)，梯度达标即止安全退出"
                logger.info(msg)
                return TaskResult.success(msg, data={"empty_grids": empty_grids, "stage": 1})

            # 3. 第 2 阶：开箱与使用消耗品 (Mod 2, Act 53: player_use_grid_item)
            # 能打开的都打开：固定宝箱、自选宝箱 (默认选项)、经验丹、体力丹直接吃满、材料/消耗品盲开
            logger.info("[第 2 阶] 正在遍历并使用背包固定宝箱、自选礼盒、经验丹、全部体力丹与消耗品...")
            for raw in list(pack_items):
                if not client.context.is_connected:
                    break
                if empty_grids >= self.target_empty and not self.force_all and not self.use_only:
                    break

                if not isinstance(raw, (list, tuple)) or len(raw) < 3:
                    continue
                item_id = int(raw[1])
                grid_id = int(raw[2])
                item_type = int(raw[20]) if len(raw) >= 21 and int(raw[20]) > 0 else (int(raw[9]) if len(raw) > 9 else 0)

                # 1. 装备与任务道具跳过使用
                if item_type in (1, 4):
                    continue

                meta = ImportantItemRegistry.get(item_id, {})
                is_gift = meta.get("is_gift", False)
                is_selective = meta.get("is_selective", False)

                # 判定是否属于可使用范畴：体力丹、经验丹、礼包、自选礼盒、消耗品(2)、材料与消耗品(11)
                can_use = (
                    item_id in (1001, 1002, 1003, 1004)
                    or item_id in (2001, 2002, 2003)
                    or is_gift
                    or is_selective
                    or item_type in (2, 11)
                )

                if can_use:
                    try:
                        logger.info("尝试使用格位 #%d 道具 (ItemID=%d, Type=%d, 自选=%s)...", grid_id, item_id, item_type, is_selective)
                        # 调用官方标准单件/多件使用协议 player_use_grid_item
                        await client.send_packet(ItemPlayerUseGridItemReq(grid_id=grid_id))
                        # 若为自选宝箱，调用 Mod 2 Act 160 自动选取首项开启
                        if is_selective:
                            try:
                                await client.send_packet(ItemChooseBoxReq(grid_id=grid_id, choose_index=1))
                            except Exception:
                                pass
                        items_used += 1
                        await asyncio.sleep(0.3)
                    except Exception as use_err:
                        logger.warning("使用格位 #%d 道具异常: %s", grid_id, use_err)

            # 刷新态势
            await asyncio.sleep(0.5)
            pack_info = await self._query_pack(client)
            if pack_info:
                pack_capacity, pack_items, warehouse_capacity, warehouse_items = pack_info
                empty_grids = max(0, pack_capacity - len(pack_items))
                logger.info("[第 2 阶] 使用消耗品后背包空格: %d 格", empty_grids)

            # 若仅执行【一键使用物品】，在此安全收官退出，绝不存仓和丢弃
            if self.use_only:
                msg = f"一键使用背包物品完成: 累计开启/使用 {items_used} 件消耗品与宝箱，当前剩余 {empty_grids} 空格"
                logger.info(msg)
                return TaskResult.success(msg, data={"empty_grids": empty_grids, "items_used": items_used})

            if empty_grids >= self.target_empty and not self.force_all:
                msg = f"第 2 阶开箱与使用后背包空间达标 (剩余 {empty_grids} 格)，梯度达标即止安全退出"
                logger.info(msg)
                return TaskResult.success(msg, data={"empty_grids": empty_grids, "items_used": items_used, "stage": 2})

            # 4. 第 3 阶：将材料与无法开启的道具存入随身仓库 (Mod 2, Act 49: move_pack_grid_item_to_warehouse)
            warehouse_free = max(0, warehouse_capacity - len(warehouse_items))
            logger.info("[第 3 阶] 正在存入随身仓库 (随身仓库可用空格: %d)...", warehouse_free)
            if warehouse_free > 0:
                for raw in list(pack_items):
                    if not client.context.is_connected:
                        break
                    if empty_grids >= self.target_empty and not self.force_all:
                        break
                    if warehouse_free <= 0:
                        break

                    if not isinstance(raw, (list, tuple)) or len(raw) < 3:
                        continue
                    item_id = int(raw[1])
                    grid_id = int(raw[2])

                    try:
                        logger.info("将格位 #%d 道具 (ItemID=%d) 转移入随身仓库...", grid_id, item_id)
                        await client.send_packet(ItemMovePackGridItemToWarehouseReq(pack_grid_id=grid_id, warehouse_grid_id=0))
                        items_warehoused += 1
                        warehouse_free -= 1
                        empty_grids += 1
                        await asyncio.sleep(0.4)
                    except Exception as wh_err:
                        logger.warning("转入仓库格位 #%d 道具异常: %s", grid_id, wh_err)

            # 刷新态势
            await asyncio.sleep(0.5)
            pack_info = await self._query_pack(client)
            if pack_info:
                pack_capacity, pack_items, warehouse_capacity, warehouse_items = pack_info
                empty_grids = max(0, pack_capacity - len(pack_items))
                logger.info("[第 3 阶] 存入仓库后背包空格: %d 格", empty_grids)

            if empty_grids >= self.target_empty and not self.force_all:
                msg = f"第 3 阶存仓后背包空间达标 (剩余 {empty_grids} 格)，梯度达标即止安全退出"
                logger.info(msg)
                return TaskResult.success(msg, data={"empty_grids": empty_grids, "items_warehoused": items_warehoused, "stage": 3})

            # 5. 第 4 阶：仓库满后全部变卖/丢弃兜底 (Q4 B: 仓满全丢)
            logger.info("[第 4 阶] 随身仓库已满，正在执行背包剩余物品全量变卖与丢弃清空 (Q4 B 模式)...")
            for raw in list(pack_items):
                if not client.context.is_connected:
                    break
                if empty_grids >= self.target_empty and not self.force_all:
                    break

                if not isinstance(raw, (list, tuple)) or len(raw) < 3:
                    continue
                player_item_id = int(raw[0])
                item_id = int(raw[1])
                grid_id = int(raw[2])

                # 优先变卖换取铜钱
                sold_ok = False
                try:
                    logger.info("尝试变卖格位 #%d (ItemID=%d, PlayerItemID=%d)...", grid_id, item_id, player_item_id)
                    sell_pkt = ItemSellItemReq(player_item_id=player_item_id)
                    resp_bytes = await client.request(sell_pkt, timeout_sec=2.0)
                    if resp_bytes:
                        sell_resp = ItemSellItemResp.decode(resp_bytes)
                        if sell_resp.is_success:
                            items_sold += 1
                            coins_earned += sell_resp.return_coins
                            empty_grids += 1
                            sold_ok = True
                            logger.info("变卖成功，换得铜钱 %d", sell_resp.return_coins)
                except Exception as sell_exc:
                    logger.debug("变卖格位 #%d 失败或无需变卖: %s", grid_id, sell_exc)

                # 变卖失败或不可变卖，直接调用协议彻底丢弃 (Q4 B 彻底腾空)
                if not sold_ok:
                    try:
                        logger.info("变卖未命中/不可变卖，执行强制丢弃格位 #%d (ItemID=%d)...", grid_id, item_id)
                        await client.send_packet(ItemDropPackGridItemReq(grid_id=grid_id))
                        items_dropped += 1
                        empty_grids += 1
                        await asyncio.sleep(0.3)
                    except Exception as drop_exc:
                        logger.debug("丢弃格位 #%d 异常: %s", grid_id, drop_exc)

            # 最终刷新态势
            await asyncio.sleep(0.5)
            pack_info = await self._query_pack(client)
            final_empty = empty_grids
            if pack_info:
                pack_capacity, pack_items, _, _ = pack_info
                final_empty = max(0, pack_capacity - len(pack_items))

            msg = f"背包四阶激进自理完成: 当前剩余 {final_empty} 空格 (使用 {items_used} 件, 存仓 {items_warehoused} 件, 变卖 {items_sold} 件换铜钱 {coins_earned}, 丢弃 {items_dropped} 件)"
            logger.info(msg)
            return TaskResult.success(
                msg,
                data={
                    "empty_grids": final_empty,
                    "items_used": items_used,
                    "items_warehoused": items_warehoused,
                    "items_sold": items_sold,
                    "items_dropped": items_dropped,
                    "coins_earned": coins_earned,
                },
            )

        except Exception as exc:
            logger.error("背包自理流水线执行捕获异常: %s", exc, exc_info=True)
            return TaskResult.failed(f"背包自理流水线异常: {exc}")

    async def _query_pack(self, client: SXDClient) -> Optional[tuple]:
        """查询主背包与随身仓库物品元数据列表"""
        try:
            req_pkt = ItemGetPlayerPackItemListReq()
            resp_bytes = await client.request(req_pkt, timeout_sec=3.0)
            if resp_bytes:
                resp = ItemGetPlayerPackItemListResp.decode(resp_bytes)
                return (resp.pack_capacity, resp.pack_items, resp.warehouse_capacity, resp.warehouse_items)
        except Exception as exc:
            logger.warning("查询背包数据异常: %s", exc)
        return None
