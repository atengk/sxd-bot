"""神仙道异步持久化工作线程与无锁队列流水线

提供无阻塞的持久化写入管道，将网络长连接主循环与数据库 I/O 物理隔离。
通过专职后台 Worker 线程无锁消费内存队列，批量执行 SQLite 事务提交与 FIFO 滚动清理。

@author Ateng
@since 2026-10-16
"""

import logging
import queue
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Tuple
from storage.player_db import (
    PlayerDatabase,
    PlayerProfileRecord,
    InventoryItemRecord,
    ModuleStateRecord,
    BattleRecord,
    AuditLogRecord,
)

logger = logging.getLogger(__name__)


@dataclass
class StorageTask:
    """持久化异步任务载荷

    @author Ateng
    @since 2026-10-16
    """

    task_type: str
    data: Any


class StorageWorker:
    """专职异步持久化写入线程

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self, db: PlayerDatabase, batch_size: int = 50, flush_interval: float = 0.05) -> None:
        self.db = db
        self.batch_size = batch_size
        self.flush_interval = flush_interval

        self._queue: queue.Queue[Optional[StorageTask]] = queue.Queue()
        self._thread: Optional[threading.Thread] = None
        self._running: bool = False
        self._stopped_event = threading.Event()

    @property
    def is_running(self) -> bool:
        """工作线程是否处于活跃运行状态"""
        return self._running and self._thread is not None and self._thread.is_alive()

    def start(self) -> None:
        """启动后台持久化工作线程"""
        if self.is_running:
            return
        self._running = True
        self._stopped_event.clear()
        self._thread = threading.Thread(target=self._worker_loop, name=f"StorageWorker-{self.db.player_id}", daemon=True)
        self._thread.start()
        logger.debug("StorageWorker 后台写入线程已启动: PlayerID=%d", self.db.player_id)

    def submit(self, task: StorageTask) -> None:
        """向持久化队列提交写任务 (绝对零阻塞)"""
        if not self._running:
            self.start()
        self._queue.put_nowait(task)

    def submit_profile(self, profile: PlayerProfileRecord) -> None:
        """提交角色核心数值保存任务"""
        self.submit(StorageTask(task_type="profile", data=profile))

    def submit_inventory(self, items: List[InventoryItemRecord]) -> None:
        """提交背包装备批量保存任务"""
        self.submit(StorageTask(task_type="inventory", data=items))

    def submit_inventory_remove(self, grid_id: int) -> None:
        """提交背包格子清除任务"""
        self.submit(StorageTask(task_type="inventory_remove", data=grid_id))

    def submit_module_state(self, state: ModuleStateRecord) -> None:
        """提交子系统状态快照保存任务"""
        self.submit(StorageTask(task_type="module_state", data=state))

    def submit_battle_record(self, record: BattleRecord) -> None:
        """提交战斗战报与战利品结算任务"""
        self.submit(StorageTask(task_type="battle", data=record))

    def submit_audit_log(self, log: AuditLogRecord) -> None:
        """提交高危元宝操作审计流水任务"""
        self.submit(StorageTask(task_type="audit", data=log))

    def submit_custom_action(self, action: Callable[[PlayerDatabase], None]) -> None:
        """提交自定义写数据库事务闭包"""
        self.submit(StorageTask(task_type="custom", data=action))

    def flush(self, timeout: float = 5.0) -> None:
        """阻塞等待当前队列中的全部任务执行完毕并落盘"""
        deadline = time.time() + timeout
        while self._queue.unfinished_tasks > 0:
            if time.time() > deadline:
                logger.warning("StorageWorker 等待队列排空超时")
                break
            time.sleep(0.005)

    def stop(self, timeout: float = 5.0) -> None:
        """优雅关闭工作线程并确保剩余任务全部入库"""
        if not self._running:
            return
        self._running = False
        self._queue.put(None)  # 终止信号哨兵
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=timeout)
        self._stopped_event.set()
        logger.debug("StorageWorker 后台写入线程已优雅停止: PlayerID=%d", self.db.player_id)

    def _worker_loop(self) -> None:
        """后台专职线程主循环，执行批量抽取与合并事务提交"""
        while self._running:
            try:
                task = self._queue.get(timeout=self.flush_interval)
            except queue.Empty:
                continue

            if task is None:
                self._queue.task_done()
                break

            # 收集批次
            batch: List[StorageTask] = [task]
            while len(batch) < self.batch_size:
                try:
                    next_task = self._queue.get_nowait()
                    if next_task is None:
                        # 延迟处理哨兵
                        self._queue.put(None)
                        break
                    batch.append(next_task)
                except queue.Empty:
                    break

            # 批量执行入库
            try:
                self._execute_batch(batch)
            except Exception as exc:
                logger.error("StorageWorker 批量事务写入异常: %s", exc)
            finally:
                for _ in batch:
                    self._queue.task_done()

        # 线程退出前排空残留队列
        self._drain_remaining()

    def _execute_batch(self, batch: List[StorageTask]) -> None:
        """按业务类型批量派发写入操作"""
        for t in batch:
            try:
                if t.task_type == "profile":
                    self.db.upsert_player_profile(t.data)
                elif t.task_type == "inventory":
                    self.db.upsert_inventory_items(t.data)
                elif t.task_type == "inventory_remove":
                    self.db.remove_inventory_item(t.data)
                elif t.task_type == "module_state":
                    self.db.set_module_state(t.data)
                elif t.task_type == "battle":
                    self.db.add_battle_record(t.data)
                elif t.task_type == "audit":
                    self.db.add_audit_log(t.data)
                elif t.task_type == "custom":
                    t.data(self.db)
            except Exception as exc:
                logger.error("执行持久化子任务异常 [%s]: %s", t.task_type, exc)

    def _drain_remaining(self) -> None:
        """排空队列中遗留的有效任务"""
        while not self._queue.empty():
            try:
                task = self._queue.get_nowait()
                if task is not None:
                    self._execute_batch([task])
                self._queue.task_done()
            except queue.Empty:
                break
            except Exception as exc:
                logger.error("排空队列遗留任务异常: %s", exc)
