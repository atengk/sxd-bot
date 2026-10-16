"""自动化任务生命周期与定时调度器

支持一次性主线任务链与高频定时周期任务并发调度，统一管理异常重试与退出回收。

@author Ateng
@since 2026-10-15
"""

import asyncio
import logging
from typing import List, Optional
from tasks.base import BaseTask, TaskStatus
from core.context import GameContext
from network.client import SXDClient

logger = logging.getLogger(__name__)


class TaskScheduler:
    """任务调度管理器

    @author Ateng
    @since 2026-10-15
    """

    def __init__(self, client: SXDClient, context: GameContext) -> None:
        self.client = client
        self.context = context
        self._tasks: List[BaseTask] = []
        self._running = False
        self._background_tasks: List[asyncio.Task] = []

    def register(self, task: BaseTask) -> None:
        """注册自动化任务"""
        self._tasks.append(task)
        logger.debug("已注册任务: %s (周期: %.1fs)", task.name, task.interval_sec)

    async def start(self) -> None:
        """启动任务调度循环

        编排原则：
        1. 优先寻找并执行必须的登录鉴权任务；
        2. 登录就绪后立即启动所有后台周期任务 (特别是心跳保活协程)，保障长连接持续活性；
        3. 在心跳持续守护的前提下，串行执行其余单次日常福利任务。
        """
        self._running = True
        logger.info("任务调度引擎已启动，待执行任务数: %d", len(self._tasks))

        # 1. 提取登录任务、其他单次任务与周期任务
        login_tasks: List[BaseTask] = []
        routine_tasks: List[BaseTask] = []
        periodic_tasks: List[BaseTask] = []

        for task in self._tasks:
            if task.interval_sec > 0:
                periodic_tasks.append(task)
            elif task.name == "LoginTask":
                login_tasks.append(task)
            else:
                routine_tasks.append(task)

        # 2. 先行执行登录初始化
        for task in login_tasks:
            await self._run_single_task(task)

        # 3. 登录完成后，立即启动所有后台周期任务 (包括 HeartbeatTask 心跳保活)
        for task in periodic_tasks:
            t = asyncio.create_task(self._periodic_loop(task))
            self._background_tasks.append(t)
            logger.info("后台周期任务已就绪并启动: %s (周期: %.1fs)", task.name, task.interval_sec)

        # 4. 在心跳后台持续发送的保护下，依次执行单次日常任务
        for task in routine_tasks:
            if not self._running or not self.client.context.is_connected:
                logger.warning("连接状态异常，中止后续单次任务调度: %s", task.name)
                break
            await self._run_single_task(task)
            # 任务间防频控节奏缓冲 (300ms)，拟真交互并防止突发流量触发服务端防刷断连
            await asyncio.sleep(0.3)

    async def stop(self) -> None:
        """停止所有任务调度协程"""
        self._running = False
        for t in self._background_tasks:
            t.cancel()
        if self._background_tasks:
            await asyncio.gather(*self._background_tasks, return_exceptions=True)
        self._background_tasks.clear()
        logger.info("所有后台周期任务已安全退出")

    async def _run_single_task(self, task: BaseTask) -> None:
        """执行单次任务"""
        try:
            logger.info("开始执行前置任务: %s", task.name)
            res = await task.execute(self.client, self.context)
            if res.status == TaskStatus.SUCCESS:
                logger.info("任务执行成功 [%s]: %s", task.name, res.message)
            else:
                logger.warning("任务未成功 [%s] 状态=%s: %s", task.name, res.status.value, res.message)
        except Exception as exc:
            logger.error("单次任务未捕获异常 [%s]: %s", task.name, exc)

    async def _periodic_loop(self, task: BaseTask) -> None:
        """周期任务循环调度"""
        while self._running:
            try:
                res = await task.execute(self.client, self.context)
                if res.status == TaskStatus.FAILED:
                    logger.warning("周期任务执行失败 [%s]: %s", task.name, res.message)
            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.error("周期任务未捕获异常 [%s]: %s", task.name, exc)

            try:
                await asyncio.sleep(task.interval_sec)
            except asyncio.CancelledError:
                break
