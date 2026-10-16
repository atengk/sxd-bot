"""神仙道标准日志转 EventBus 桥接模块

透明捕获受管 Python logging 框架日志，自动提取关联账号别名，
并打包为规范事件通过 EventBus 发布，供前端 Web 控制台实时 SSE 流式消费。

@author Ateng
@since 2026-10-16
"""

import logging
import re
import time
from typing import Optional, Dict, Any

from core.events import EventBus

ALIAS_PATTERN = re.compile(r"^\[([^\]]+)\]")


class EventBusLogHandler(logging.Handler):
    """日志流转 EventBus 的桥接处理器

    @author Ateng
    @since 2026-10-16
    """

    def __init__(self, event_bus: EventBus, level: int = logging.INFO) -> None:
        """初始化日志桥接器

        Args:
            event_bus: 全局事件总线实例。
            level: 捕获的最低日志级别。
        """
        super().__init__(level=level)
        self.event_bus = event_bus

    def emit(self, record: logging.LogRecord) -> None:
        """格式化单条日志记录并分发至 EventBus"""
        try:
            raw_msg = record.getMessage()
            msg = self.format(record) if self.formatter else raw_msg

            # 1. 尝试从 record 显式属性中提取 alias，其次从消息头 [alias] 中解析
            alias: Optional[str] = getattr(record, "alias", None)
            if not alias:
                match = ALIAS_PATTERN.match(raw_msg)
                if match:
                    alias = match.group(1)

            payload: Dict[str, Any] = {
                "type": "log",
                "alias": alias,
                "level": record.levelname,
                "logger": record.name,
                "message": msg,
                "timestamp": record.created or time.time(),
            }
            self.event_bus.publish("log", payload)
        except Exception:
            self.handleError(record)


def attach_log_bridge(
    event_bus: EventBus,
    logger_name: Optional[str] = None,
    level: int = logging.INFO,
) -> EventBusLogHandler:
    """为指定日志记录器挂载 EventBus 桥接处理器

    Args:
        event_bus: 全局事件总线实例。
        logger_name: 待挂载的 logger 名称（为 None 时挂载至 root logger）。
        level: 日志级别。

    Returns:
        已挂载的 EventBusLogHandler 实例。
    """
    target_logger = logging.getLogger(logger_name)
    handler = EventBusLogHandler(event_bus=event_bus, level=level)
    target_logger.addHandler(handler)
    return handler


def detach_log_bridge(
    handler: EventBusLogHandler,
    logger_name: Optional[str] = None,
) -> None:
    """卸载已挂载的 EventBus 桥接处理器

    Args:
        handler: 待卸载的处理器实例。
        logger_name: 对应的 logger 名称。
    """
    target_logger = logging.getLogger(logger_name)
    target_logger.removeHandler(handler)
