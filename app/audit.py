"""Append-only local audit events; production needs durable, access-controlled storage."""
import json
from datetime import datetime, timezone
from pathlib import Path


class AuditLog:
    def __init__(self, path: str = "data/audit.jsonl"):
        self.path = Path(path)

    def append(self, event_type: str, payload: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "payload": payload,
        }
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
