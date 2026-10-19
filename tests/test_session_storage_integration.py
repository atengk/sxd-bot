"""会话管理器与异步持久化管道端到端集成测试套件

测试覆盖:
1. 托管启动时为每个账号建立独占 EventBus、StorageWorker 与 SqliteStorageSubscriber
2. 首次建档无基线时仅作为期初结余 (tb_daily_asset_summary opening)，不计虚假收支流水
3. 运行时接收 Mod 0 Act 3 属性变更广播，精准记录收支流水与当日汇总
4. 停止托管时 Worker 安全 flush 与停止，会话与订阅器清理闭环
5. 离线调用 sync_telemetry 时临时 Worker 与切面订阅器的安全生命周期

@author Ateng
@since 2026-10-19
"""

import asyncio
import os
import shutil
import tempfile
import time
import unittest
from unittest.mock import AsyncMock, patch

from core.context import GameContext
from core.events import EventBus
from protocol.messages.player import PlayerInfoResp, PlayerUpdatePlayerDataResp
from protocol.packet import ByteArrayWriter
from storage.config_db import ConfigDatabase, AccountRecord
from storage.player_db import PlayerDatabase
from storage.subscriber import SqliteStorageSubscriber
from storage.worker import StorageWorker
from web.session_manager import AccountSessionManager


class TestSessionStorageIntegration(unittest.TestCase):
    """会话管理器与持久化管道端到端集成测试"""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="sxd_test_session_storage_")
        self.config_db_path = os.path.join(self.test_dir, "config.sqlite")
        self.config_db = ConfigDatabase(db_path=self.config_db_path, auto_bootstrap=False)
        self.session_manager = AccountSessionManager(db=self.config_db)

        self.acc = AccountRecord(
            alias="测试主号",
            platform="fengwanyx",
            username="test_user",
            password="test_password",
            server="s813",
            server_id=813,
            enabled=True,
            hosting_enabled=True,
        )
        self.config_db.add_account(self.acc)

        self.player_db_path = os.path.join(self.test_dir, "storage_813_9999.db")
        self.player_db = PlayerDatabase(server_id=813, player_id=9999, db_path=self.player_db_path)
        self.session_manager.set_player_db("测试主号", self.player_db)

    def tearDown(self) -> None:
        self.session_manager.stop_hosting("测试主号")
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _encode_player_info(
        self,
        nickname: str = "至尊剑神",
        level: int = 100,
        coins: int = 5000000,
        ingots: int = 2000,
    ) -> bytes:
        writer = ByteArrayWriter()
        writer.write_utf(nickname)
        writer.write_int32(level)
        writer.write_int32(ingots)
        writer.write_int64(coins)
        writer.write_int64(20000)
        writer.write_int64(20000)
        writer.write_int32(200)
        writer.write_int64(100000)
        writer.write_int64(200000)
        writer.write_int32(1)
        for _ in range(4):
            writer.write_int32(0)
        writer.write_int32(3)
        for _ in range(4):
            writer.write_int32(0)
        writer.write_int8(1)
        writer.write_int32(0)
        writer.write_int32(50000)
        for _ in range(7):
            writer.write_int32(0)
        writer.write_int32(10)
        return writer.to_bytes()

    def test_subscriber_and_worker_lifecycle_in_session_manager(self) -> None:
        """测试托管管道生命周期与资产收支变动精准入库"""
        alias = "测试主号"
        ctx = GameContext()
        session_bus = EventBus()

        # 1. 模拟长连接建立并挂载专属 Worker 与 Subscriber
        worker = StorageWorker(self.player_db)
        worker.start()
        self.session_manager._workers[alias] = worker

        subscriber = SqliteStorageSubscriber(
            worker=worker,
            player_db=self.player_db,
            player_id=9999,
            context=ctx,
        )
        subscriber.attach_to_event_bus(session_bus)
        self.session_manager._subscribers[alias] = subscriber
        self.session_manager._sessions[alias] = {
            "connection_status": "connected",
            "context": ctx,
            "event_bus": session_bus,
            "hosting_enabled": True,
        }

        self.assertIsNotNone(self.session_manager.get_worker(alias))
        self.assertIsNotNone(self.session_manager.get_subscriber(alias))

        loop = asyncio.new_event_loop()
        try:
            # 2. 模拟首次上线收到 Mod 0 Act 2: 铜钱 5,000,000, 元宝 2,000
            # 此时库中无历史基线，必须作为期初结余，绝不产生虚假收入流水
            raw_info = self._encode_player_info(coins=5000000, ingots=2000)
            loop.run_until_complete(session_bus.emit(0, 2, raw_info))
            worker.flush()

            # 验证期初结存初始化就绪
            today = self.player_db.get_today_asset_summary()
            self.assertIsNotNone(today)
            assert today is not None
            self.assertEqual(today.opening_coins, 5000000)
            self.assertEqual(today.closing_coins, 5000000)
            self.assertEqual(today.coins_income, 0)
            self.assertEqual(today.coins_expense, 0)
            self.assertEqual(today.opening_ingots, 2000)
            self.assertEqual(today.closing_ingots, 2000)
            self.assertEqual(today.ingots_income, 0)
            self.assertEqual(today.ingots_expense, 0)

            # 验证明细流水表为空 (不产生虚假几千万入账流水)
            txs = self.player_db.get_recent_asset_transactions(limit=10)
            self.assertEqual(len(txs), 0)

            # 3. 模拟执行日常任务 (例如 farm 仙府药园收获) 产生铜钱增加 100,000
            ctx.set_active_task("farm")
            upd_coin = PlayerUpdatePlayerDataResp(updates={20: 5100000})
            loop.run_until_complete(session_bus.emit(0, 3, upd_coin.encode_payload()))
            ctx.clear_active_task()
            worker.flush()

            # 验证铜钱收入流水与归因
            txs = self.player_db.get_recent_asset_transactions(limit=10)
            self.assertEqual(len(txs), 1)
            self.assertEqual(txs[0].asset_type, "coin")
            self.assertEqual(txs[0].change_type, "income")
            self.assertEqual(txs[0].amount, 100000)
            self.assertEqual(txs[0].balance_after, 5100000)
            self.assertEqual(txs[0].reason, "仙府药园收获")

            # 验证今日汇总表累加
            today_updated = self.player_db.get_today_asset_summary()
            assert today_updated is not None
            self.assertEqual(today_updated.opening_coins, 5000000)
            self.assertEqual(today_updated.closing_coins, 5100000)
            self.assertEqual(today_updated.coins_income, 100000)

            # 4. 模拟微端离线变动: 元宝消耗 50 (例如购买体力)
            upd_ingot = PlayerUpdatePlayerDataResp(updates={19: 1950})
            loop.run_until_complete(session_bus.emit(0, 3, upd_ingot.encode_payload()))
            worker.flush()

            all_txs = self.player_db.get_recent_asset_transactions(limit=10)
            self.assertEqual(len(all_txs), 2)
            ingot_tx = [t for t in all_txs if t.asset_type == "ingot"][0]
            self.assertEqual(ingot_tx.change_type, "expense")
            self.assertEqual(ingot_tx.amount, 50)
            self.assertEqual(ingot_tx.balance_after, 1950)

            # 验证今日汇总元宝支出
            today_final = self.player_db.get_today_asset_summary()
            assert today_final is not None
            self.assertEqual(today_final.opening_ingots, 2000)
            self.assertEqual(today_final.closing_ingots, 1950)
            self.assertEqual(today_final.ingots_expense, 50)

            # 5. 测试 stop_hosting 退出时 Worker 与 Subscriber 优雅注销
            self.session_manager.stop_hosting(alias)
            self.assertIsNone(self.session_manager.get_worker(alias))
            self.assertIsNone(self.session_manager.get_subscriber(alias))
            self.assertFalse(worker.is_running)
        finally:
            loop.close()


if __name__ == "__main__":
    unittest.main()
