"""自动化业务任务基础抽象体系与执行结果契约

定义 BaseTask 插件化生命周期与 TaskResult 语义状态。

@author Ateng
@since 2026-10-15
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Any
from core.context import GameContext
from network.client import SXDClient


class TaskStatus(Enum):
    """任务执行结果状态码"""

    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRY_LATER = "retry_later"


class TaskResult:
    """任务执行结果对象

    @author Ateng
    @since 2026-10-15
    """

    def __init__(self, status: TaskStatus, message: str = "", data: Optional[Any] = None) -> None:
        self.status = status
        self.message = message
        self.data = data

    @classmethod
    def success(cls, message: str = "", data: Optional[Any] = None) -> "TaskResult":
        return cls(TaskStatus.SUCCESS, message, data)

    @classmethod
    def failed(cls, message: str = "", data: Optional[Any] = None) -> "TaskResult":
        return cls(TaskStatus.FAILED, message, data)

    @classmethod
    def retry_later(cls, message: str = "", data: Optional[Any] = None) -> "TaskResult":
        return cls(TaskStatus.RETRY_LATER, message, data)

    @classmethod
    def skipped(cls, message: str = "", data: Optional[Any] = None) -> "TaskResult":
        return cls(TaskStatus.SKIPPED, message, data)


class BaseTask(ABC):
    """自动化业务任务抽象基类

    @author Ateng
    @since 2026-10-15
    """

    name: str = "BaseTask"
    interval_sec: float = 0.0  # 循环执行间隔 (秒)，0 表示单次执行任务

    @abstractmethod
    async def execute(self, client: SXDClient, ctx: GameContext) -> TaskResult:
        """执行具体的业务自动化逻辑

        Args:
            client: 具备请求发送与长连接能力的客户端。
            ctx: 当前全局上下文只读状态池。

        Returns:
            TaskResult 任务执行状态与结果。
        """
        raise NotImplementedError
