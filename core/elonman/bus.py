"""Event bus: in-process publish/subscribe plus an append-only log (events.jsonl).

Parts never call each other. They emit events, and whoever cares listens.
"""
import json
import threading
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path


class Bus:
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self._subs = defaultdict(list)
        self._lock = threading.Lock()

    def on(self, event_type: str, fn):
        """Subscribe. Use "*" for every event."""
        self._subs[event_type].append(fn)

    def emit(self, event_type: str, **data) -> dict:
        ev = {"t": datetime.now().isoformat(timespec="seconds"), "type": event_type, "data": data}
        with self._lock:
            with self.log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")
        for fn in self._subs[event_type] + self._subs["*"]:
            try:
                fn(ev)
            except Exception as e:  # one bad listener never stops the bus
                print(f"[bus] listener for {event_type} failed: {e}")
        return ev


def tail(log_path: Path, n: int = 20) -> list:
    if not log_path.exists():
        return []
    with log_path.open(encoding="utf-8") as f:
        lines = deque(f, maxlen=n)
    out = []
    for line in lines:
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out
