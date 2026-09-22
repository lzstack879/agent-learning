from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Memory:
    """Three-layer memory with a SQLite fallback for durable structured facts."""
    working: dict[str, Any] = field(default_factory=dict)
    sessions: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    db_path: str = ":memory:"

    def __post_init__(self) -> None:
        self._db = sqlite3.connect(self.db_path)
        self._db.execute("CREATE TABLE IF NOT EXISTS memories (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
        self._db.commit()

    def remember(self, key: str, value: str) -> None:
        self._db.execute("INSERT OR REPLACE INTO memories VALUES (?, ?)", (key, value))
        self._db.commit()

    def recall(self, key: str) -> str | None:
        row = self._db.execute("SELECT value FROM memories WHERE key = ?", (key,)).fetchone()
        return row[0] if row else None

    def add_message(self, session_id: str, role: str, content: str) -> None:
        self.sessions.setdefault(session_id, []).append({"role": role, "content": content})

    def context(self, session_id: str) -> dict[str, Any]:
        return {"working": self.working, "session": self.sessions.get(session_id, [])}

