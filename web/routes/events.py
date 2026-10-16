"""神仙道 SSE (Server-Sent Events) 实时事件与日志推送路由

支持账号别名过滤、心跳保活与客户端断连安全注销。

@author Ateng
@since 2026-10-16
"""

import asyncio
import json
import logging
import time
from typing import Optional, Any, AsyncGenerator

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from core.events import EventBus
from web.app import require_auth_token

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/events",
    tags=["Events"],
    dependencies=[Depends(require_auth_token)],
)


@router.get("", response_class=StreamingResponse)
async def sse_event_stream(
    request: Request,
    alias: Optional[str] = None,
    limit: Optional[int] = None,
    timeout_sec: float = 5.0,
    max_idle_sec: Optional[float] = None,
) -> StreamingResponse:
    """建立 SSE 长连接流式推送通道
    
    Args:
        request: FastAPI 请求上下文。
        alias: 可选的账号别名过滤器。若指定，则仅推送该账号相关事件及全局系统事件。
        limit: 可选的接收事件条数上限（达到后安全退出，适用于自动化测试与快照捕获）。
        timeout_sec: 空闲心跳保活周期 (秒)。
        max_idle_sec: 最大空闲等待超时 (秒)，若指定且超过该时间无新事件则安全退出。

    Returns:
        StreamingResponse (text/event-stream)。
    """
    session_manager = getattr(request.app.state, "session_manager", None)
    event_bus: EventBus = (
        session_manager.event_bus
        if session_manager and hasattr(session_manager, "event_bus")
        else getattr(request.app.state, "event_bus", EventBus())
    )

    async def event_generator() -> AsyncGenerator[str, None]:
        queue: asyncio.Queue = asyncio.Queue()
        loop = asyncio.get_running_loop()
        count = 0

        def on_event(event_type: str, data: Any) -> None:
            # 1. 过滤逻辑：若客户端指定了 alias 过滤器，且该事件携带具体 alias 且不匹配，则过滤
            if isinstance(data, dict):
                ev_alias = data.get("alias")
                if alias and ev_alias and ev_alias != alias:
                    return
                loop.call_soon_threadsafe(queue.put_nowait, (event_type, data))
            else:
                loop.call_soon_threadsafe(queue.put_nowait, (event_type, {"data": data}))

        event_bus.subscribe_all_events(on_event)

        try:
            # 2. 发送初始建立连接通知
            init_data = json.dumps(
                {
                    "type": "connected",
                    "alias_filter": alias,
                    "timestamp": time.time(),
                },
                ensure_ascii=False,
            )
            yield f"event: connected\ndata: {init_data}\n\n"
            count += 1
            if limit and count >= limit:
                return

            idle_wait = max_idle_sec if max_idle_sec is not None else timeout_sec

            # 3. 循环等待并推送事件流
            while True:
                try:
                    event_type, data = await asyncio.wait_for(queue.get(), timeout=idle_wait)
                    ev_name = data.get("type", event_type) if isinstance(data, dict) else event_type
                    ev_body = json.dumps(data, ensure_ascii=False)
                    yield f"event: {ev_name}\ndata: {ev_body}\n\n"
                    count += 1
                    if limit and count >= limit:
                        break
                except asyncio.TimeoutError:
                    if max_idle_sec is not None:
                        break
                    yield ": keepalive\n\n"

                # 4. 客户端断开检测防御
                if await request.is_disconnected():
                    break
        except (asyncio.CancelledError, GeneratorExit):
            pass
        finally:
            event_bus.unsubscribe_all_events(on_event)

    headers = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
    }

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers=headers,
    )
