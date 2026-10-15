"""神仙道异步事件广播总线

实现解耦的发布-订阅模式，用于分发服务端下行广播通知（如全服跑马灯、场景刷新）以及解包事件。

@author Ateng
@since 2026-10-15
"""

import asyncio
import logging
from typing import Callable, Coroutine, Dict, List, Tuple, Any

logger = logging.getLogger(__name__)

EventHandler = Callable[[int, int, bytes], Coroutine[Any, Any, None]]


class EventBus:
    """异步事件总线

    @author Ateng
    @since 2026-10-15
    """

    def __init__(self) -> None:
        self._listeners: Dict[Tuple[int, int], List[EventHandler]] = {}
        self._global_listeners: List[EventHandler] = []

    def subscribe(self, mod: int, act: int, handler: EventHandler) -> None:
        """订阅指定模块和动作的事件广播

        Args:
            mod: 模块 ID。
            act: 动作 ID。
            handler: 异步回调函数 async def handler(mod, act, payload)。
        """
        key = (mod, act)
        if key not in self._listeners:
            self._listeners[key] = []
        self._listeners[key].append(handler)

    def subscribe_all(self, handler: EventHandler) -> None:
        """订阅全量下行数据包广播 (用于全局日志或统计)"""
        self._global_listeners.append(handler)

    async def emit(self, mod: int, act: int, payload: bytes) -> None:
        """向所有已订阅监听器分发事件

        Args:
            mod: 模块 ID。
            act: 动作 ID。
            payload: 解压后的有效载荷。
        """
        handlers: List[EventHandler] = []

        # 1. 收集特定目标监听器与全局监听器
        key = (mod, act)
        if key in self._listeners:
            handlers.extend(self._listeners[key])
        handlers.extend(self._global_listeners)

        # 2. 并发非阻塞调用所有回调
        for h in handlers:
            try:
                if asyncio.iscoroutinefunction(h):
                    asyncio.create_task(h(mod, act, payload))
                else:
                    h(mod, act, payload)
            except Exception as exc:
                logger.error("事件分发异常 [Mod=%d, Act=%d]: %s", mod, act, exc)
