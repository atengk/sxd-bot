"""神仙道自动化业务任务与调度框架

@author Ateng
@since 2026-10-15
"""

from tasks.base import BaseTask, TaskResult, TaskStatus
from tasks.scheduler import TaskScheduler
from tasks.routine.login import LoginTask
from tasks.routine.heartbeat import HeartbeatTask
from tasks.routine.signin import DailySignInTask
from tasks.routine.money_tree import FreeMoneyTreeTask
from tasks.routine.online_gift import OnlineGiftTask

__all__ = [
    "BaseTask",
    "TaskResult",
    "TaskStatus",
    "TaskScheduler",
    "LoginTask",
    "HeartbeatTask",
    "DailySignInTask",
    "FreeMoneyTreeTask",
    "OnlineGiftTask",
]
