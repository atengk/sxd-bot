"""神仙道异步事件广播总线

实现解耦的发布-订阅模式，用于分发服务端下行广播通知（如全服跑马灯、场景刷新）以及解包事件。

@author Ateng
@since 2026-10-15
"""

import asyncio
import inspect
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
        self._app_listeners: Dict[str, List[Callable]] = {}
        self._global_app_listeners: List[Callable] = []

    def subscribe_event(self, event_type: str, handler: Callable) -> None:
        """订阅应用级通用事件

        Args:
            event_type: 事件主题/类型。
            handler: 回调函数，支持 def 或 async def。
        """
        if event_type not in self._app_listeners:
            self._app_listeners[event_type] = []
        self._app_listeners[event_type].append(handler)

    def subscribe_all_events(self, handler: Callable) -> None:
        """订阅全量应用级通用事件广播"""
        self._global_app_listeners.append(handler)

    def unsubscribe_event(self, event_type: str, handler: Callable) -> None:
        """注销指定应用事件的监听器

        Args:
            event_type: 事件主题/类型。
            handler: 回调函数引用。
        """
        if event_type in self._app_listeners:
            self._app_listeners[event_type] = [
                h for h in self._app_listeners[event_type] if h != handler
            ]

    def unsubscribe_all_events(self, handler: Callable) -> None:
        """注销全量应用事件的全局监听器

        Args:
            handler: 回调函数引用。
        """
        self._global_app_listeners = [
            h for h in self._global_app_listeners if h != handler
        ]

    def publish(self, event_type: str, data: Any = None) -> None:
        """向所有已订阅应用事件的监听器分发事件 (非阻塞，支持同步与异步回调)

        Args:
            event_type: 事件主题/类型。
            data: 事件携带的数据载荷。
        """
        handlers: List[Callable] = []
        if event_type in self._app_listeners:
            handlers.extend(self._app_listeners[event_type])
        handlers.extend(self._global_app_listeners)

        loop = None
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            pass

        for h in handlers:
            try:
                try:
                    sig = inspect.signature(h)
                    params_cnt = len(sig.parameters)
                except Exception:
                    params_cnt = 2

                if inspect.iscoroutinefunction(h):
                    coro = h(data) if params_cnt == 1 else h(event_type, data)
                    if loop and loop.is_running():
                        loop.create_task(coro)
                    else:
                        asyncio.run(coro)
                else:
                    if params_cnt == 1:
                        h(data)
                    else:
                        h(event_type, data)
            except Exception as exc:
                logger.error("应用事件分发异常 [%s]: %s", event_type, exc)

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
                if inspect.iscoroutinefunction(h):
                    asyncio.create_task(h(mod, act, payload))
                else:
                    h(mod, act, payload)
            except Exception as exc:
                logger.error("事件分发异常 [Mod=%d, Act=%d]: %s", mod, act, exc)
