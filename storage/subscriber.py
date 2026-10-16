"""神仙道非侵入式 SQLite 持久化切面订阅器

挂载至 EventBus 异步事件总线，静默监听下行关键协议广播与应答，
自动提取实体有效载荷打包并分发至 StorageWorker 后台专职写入队列，
实现游戏角色属性、背包资产、关卡战报、子系统快照及高危操作审计的自动化无锁持久化。

@author Ateng
@since 2026-10-16
"""

import json
import logging
from typing import Any, Dict, List, Optional

from core.events import EventBus
from protocol.contracts.mod_13_farm import FarmGetFarmlandinfoListResp
from protocol.contracts.mod_2_item import ItemGetAllPlayerItemInfosResp
from protocol.messages.battle import (
    MissionFightMonsterResp,
    SuperSportGetChallengeTimesResp,
)
from protocol.messages.player import (
    PlayerInfoResp,
    PlayerUpdatePlayerDataResp,
)
from protocol.messages.routine import FarmHarvestResp
from storage.player_db import (
    AuditLogRecord,
    BattleRecord,
    InventoryItemRecord,
    ModuleStateRecord,
    PlayerDatabase,
    PlayerProfileRecord,
)
from storage.worker import StorageWorker

logger = logging.getLogger(__name__)


class SqliteStorageSubscriber:
    """SQLite 自动持久化切面订阅器

    @author Ateng
    @since 2026-10-16
    """

    def __init__(
        self,
        worker: StorageWorker,
        player_db: PlayerDatabase,
        player_id: int = 0,
    ) -> None:
        self.worker = worker
        self.player_db = player_db
        self.player_id = player_id or player_db.player_id

    def attach_to_event_bus(self, event_bus: EventBus) -> None:
        """挂载订阅器至目标事件总线

        Args:
            event_bus: 异步事件总线实例。
        """
        # 1. 订阅角色模块 (Mod 0)
        event_bus.subscribe(0, 2, self._on_player_info)
        event_bus.subscribe(0, 3, self._on_update_player_data)

        # 2. 订阅背包物品模块 (Mod 2)
        event_bus.subscribe(2, 3, self._on_get_all_player_item_infos)

        # 3. 订阅副本与战斗模块 (Mod 4)
        event_bus.subscribe(4, 2, self._on_fight_monster_settlement)

        # 4. 订阅药园模块 (Mod 13)
        event_bus.subscribe(13, 0, self._on_farm_farmland_list)
        event_bus.subscribe(13, 6, self._on_farm_harvest)

        # 5. 订阅命格模块 (Mod 22)
        event_bus.subscribe(22, 4, self._on_fate_bag_list)

        # 6. 订阅竞技场模块 (Mod 28)
        event_bus.subscribe(28, 13, self._on_supersport_challenge_times)

        # 7. 订阅帮派祭神模块 (Mod 41)
        event_bus.subscribe(41, 1, self._on_worship_mars)

        logger.info(
            "SqliteStorageSubscriber 已成功挂载至 EventBus (Mod 0, 2, 4, 13, 22, 28, 41 协议监听已就绪)"
        )

    async def _on_player_info(self, mod: int, act: int, payload: bytes) -> None:
        """监听角色基础与高阶属性同步 (Mod 0, Act 2)"""
        try:
            resp = PlayerInfoResp.decode(payload)
            target_pid = resp.player_id if resp.player_id > 0 else self.player_id

            record = PlayerProfileRecord(
                player_id=target_pid,
                nickname=resp.nickname,
                level=resp.level,
                coins=resp.coins,
                ingots=resp.ingots,
                power=resp.power,
                fame=resp.fame,
                vip_level=resp.vip_level,
                town_id=resp.town_map_id,
            )
            self.worker.submit_profile(record)
            logger.debug("切面已捕获并提交角色全量档案更新: %s", resp.nickname)
        except Exception as exc:
            logger.warning("切面解析角色基础信息异常 [Mod=%d, Act=%d]: %s", mod, act, exc)

    async def _on_update_player_data(self, mod: int, act: int, payload: bytes) -> None:
        """监听角色属性动态权威变更广播 (Mod 0, Act 3)"""
        try:
            resp = PlayerUpdatePlayerDataResp.decode(payload)
            if not resp.updates:
                return

            # 读取当前库中最新角色档案做基准增量合并
            current = self.player_db.get_player_profile()
            if current is None:
                current = PlayerProfileRecord(player_id=self.player_id)

            changed = False
            for prop_id, val in resp.updates.items():
                if prop_id == 18:
                    current.level = int(val)
                    changed = True
                elif prop_id == 19:
                    current.ingots = int(val)
                    changed = True
                elif prop_id == 20:
                    current.coins = int(val)
                    changed = True
                elif prop_id in (23, 77):
                    current.power = int(val)
                    changed = True
                elif prop_id == 37:
                    current.fame = int(val)
                    changed = True
                elif prop_id == 39:
                    current.vip_level = int(val)
                    changed = True

            if changed:
                self.worker.submit_profile(current)
                logger.debug("切面已提交角色属性增量更新: %s", resp.updates)
        except Exception as exc:
            logger.warning("切面解析角色属性变更广播异常 [Mod=%d, Act=%d]: %s", mod, act, exc)

    async def _on_get_all_player_item_infos(self, mod: int, act: int, payload: bytes) -> None:
        """监听主背包与装备全量信息应答 (Mod 2, Act 3)"""
        try:
            resp = ItemGetAllPlayerItemInfosResp.decode(payload)
            items: List[InventoryItemRecord] = []

            # 遍历 Flash 契约返回的动态列表
            if hasattr(resp, "field_0") and resp.field_0:
                for idx, raw_item in enumerate(resp.field_0):
                    if isinstance(raw_item, (list, tuple)) and len(raw_item) >= 3:
                        grid_id = int(raw_item[2])
                        item_id = int(raw_item[1])
                        item_type = int(raw_item[9]) if len(raw_item) > 9 else 0
                        count = int(raw_item[10]) if len(raw_item) > 10 else 1
                        props = {"raw": list(raw_item)}
                        items.append(
                            InventoryItemRecord(
                                grid_id=grid_id,
                                item_id=item_id,
                                count=max(1, count),
                                item_type=item_type,
                                props=props,
                            )
                        )
                    elif isinstance(raw_item, dict):
                        items.append(
                            InventoryItemRecord(
                                grid_id=int(raw_item.get("grid_id", idx + 1)),
                                item_id=int(raw_item.get("item_id", 0)),
                                count=int(raw_item.get("count", 1)),
                                item_type=int(raw_item.get("item_type", 0)),
                                props=raw_item.get("props", {}),
                            )
                        )

            if items:
                self.worker.submit_inventory(items)
                logger.debug("切面已捕获并提交背包物品批量更新: %d 件物品", len(items))

            # 同时记录子系统快照
            self.worker.submit_module_state(
                ModuleStateRecord(
                    module_id=2,
                    state_key="inventory_snapshot",
                    payload={"item_count": len(items)},
                )
            )
        except Exception as exc:
            logger.warning("切面解析背包全量物品异常 [Mod=%d, Act=%d]: %s", mod, act, exc)

    async def _on_fight_monster_settlement(self, mod: int, act: int, payload: bytes) -> None:
        """监听普通副本怪物挑战结算 (Mod 4, Act 2)"""
        try:
            resp = MissionFightMonsterResp.decode(payload)
            record = BattleRecord(
                mission_id=0,
                is_win=resp.is_win,
                exp_gain=resp.exp_gain,
                coins_gain=resp.coins_gain,
                payload={"result_code": resp.result_code},
            )
            self.worker.submit_battle_record(record)
            logger.debug(
                "切面已捕获并提交战报: 胜利=%s, 经验=+%d, 铜钱=+%d",
                resp.is_win,
                resp.exp_gain,
                resp.coins_gain,
            )
        except Exception as exc:
            logger.warning("切面解析战斗结算异常 [Mod=%d, Act=%d]: %s", mod, act, exc)

    async def _on_farm_farmland_list(self, mod: int, act: int, payload: bytes) -> None:
        """监听药园地块列表快照广播 (Mod 13, Act 0)"""
        try:
            resp = FarmGetFarmlandinfoListResp.decode(payload)
            farmlands = resp.field_0 if hasattr(resp, "field_0") else []
            self.worker.submit_module_state(
                ModuleStateRecord(
                    module_id=13,
                    state_key="farmland_list",
                    payload={
                        "farmlands": farmlands,
                        "extra_1": getattr(resp, "field_1", 0),
                        "extra_2": getattr(resp, "field_2", 0),
                    },
                )
            )
            logger.debug("切面已捕获药园地块快照: %d 块土地", len(farmlands))
        except Exception as exc:
            logger.warning("切面解析药园地块列表异常 [Mod=%d, Act=%d]: %s", mod, act, exc)

    async def _on_farm_harvest(self, mod: int, act: int, payload: bytes) -> None:
        """监听药园草药收获结算回执 (Mod 13, Act 6)"""
        try:
            resp = FarmHarvestResp.decode(payload)
            self.worker.submit_module_state(
                ModuleStateRecord(
                    module_id=13,
                    state_key="last_harvest",
                    payload={
                        "result_code": resp.result_code,
                        "gain_exp": resp.gain_exp,
                        "gain_coins": resp.gain_coins,
                    },
                )
            )
            logger.debug(
                "切面已记录药园收获回执: 经验=+%d, 铜钱=+%d", resp.gain_exp, resp.gain_coins
            )
        except Exception as exc:
            logger.warning("切面解析药园收获回执异常 [Mod=%d, Act=%d]: %s", mod, act, exc)

    async def _on_fate_bag_list(self, mod: int, act: int, payload: bytes) -> None:
        """监听命格背包数据应答 (Mod 22, Act 4)"""
        try:
            self.worker.submit_module_state(
                ModuleStateRecord(
                    module_id=22,
                    state_key="fate_bag",
                    payload={"raw_size": len(payload)},
                )
            )
            logger.debug("切面已记录命格背包数据快照")
        except Exception as exc:
            logger.warning("切面解析命格背包数据异常 [Mod=%d, Act=%d]: %s", mod, act, exc)

    async def _on_supersport_challenge_times(self, mod: int, act: int, payload: bytes) -> None:
        """监听竞技场剩余免费挑战次数 (Mod 28, Act 13)"""
        try:
            resp = SuperSportGetChallengeTimesResp.decode(payload)
            self.worker.submit_module_state(
                ModuleStateRecord(
                    module_id=28,
                    state_key="challenge_times",
                    payload={"free_times": resp.free_times},
                )
            )
            logger.debug("切面已记录竞技场剩余次数: %d", resp.free_times)
        except Exception as exc:
            logger.warning("切面解析竞技场挑战次数异常 [Mod=%d, Act=%d]: %s", mod, act, exc)

    async def _on_worship_mars(self, mod: int, act: int, payload: bytes) -> None:
        """监听帮派祭神关公上香广播 (Mod 41, Act 1)"""
        try:
            self.worker.submit_module_state(
                ModuleStateRecord(
                    module_id=41,
                    state_key="last_worship",
                    payload={"raw_size": len(payload)},
                )
            )
            logger.debug("切面已记录帮派祭神关公上香状态")
        except Exception as exc:
            logger.warning("切面解析帮派祭神异常 [Mod=%d, Act=%d]: %s", mod, act, exc)

    def record_hazardous_audit(
        self,
        module_id: int,
        action_id: int,
        action_name: str,
        allow_ingot: bool = False,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """记录高危元宝操作审计流水

        Args:
            module_id: 业务模块 ID。
            action_id: 协议动作 ID。
            action_name: 动作语义名称。
            allow_ingot: 是否获得显式安全授权。
            details: 附属上下文审计字典。
        """
        audit = AuditLogRecord(
            module_id=module_id,
            action_id=action_id,
            action_name=action_name,
            allow_ingot=allow_ingot,
            details=details or {},
        )
        self.worker.submit_audit_log(audit)
        logger.info(
            "高危元宝审计已入库: Mod=%d, Act=%d, Name='%s', allow_ingot=%s",
            module_id,
            action_id,
            action_name,
            allow_ingot,
        )
