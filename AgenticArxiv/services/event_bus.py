# AgenticArxiv/services/event_bus.py
from __future__ import annotations

import json
import queue
import threading
import uuid
from typing import Dict, Tuple, Any


class EventBus:
    """
    进程内事件总线（MVP）
    - session_id 维度订阅
    - 每个订阅一个 thread-safe Queue，用于 SSE StreamingResponse 读取
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._subs: Dict[str, Dict[str, "queue.Queue[str]"]] = {}

    def subscribe(self, session_id: str) -> Tuple[str, "queue.Queue[str]"]:
        sid = session_id or "default"
        sub_id = uuid.uuid4().hex
        q: "queue.Queue[str]" = queue.Queue()
        with self._lock:
            self._subs.setdefault(sid, {})[sub_id] = q
        return sub_id, q

    def unsubscribe(self, session_id: str, sub_id: str) -> None:
        sid = session_id or "default"
        with self._lock:
            m = self._subs.get(sid)
            if not m:
                return
            m.pop(sub_id, None)
            if not m:
                self._subs.pop(sid, None)

    def publish(self, session_id: str, event: Dict[str, Any]) -> None:
        """
        event 会被 json dumps 后广播给该 session 的所有订阅者
        """
        sid = session_id or "default"
        try:
            data = json.dumps(event, ensure_ascii=False)
        except Exception:
            # 兜底：保证不因序列化失败影响主流程
            data = json.dumps({"type": "error", "message": "event serialization failed"}, ensure_ascii=False)

        with self._lock:
            subs = list(self._subs.get(sid, {}).values())

        for q in subs:
            try:
                q.put_nowait(data)
            except Exception:
                # 单个订阅异常不影响广播
                pass
