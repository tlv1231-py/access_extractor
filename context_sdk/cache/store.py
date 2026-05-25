from __future__ import annotations

import hashlib
import json
import logging
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_DEFAULT_TTL = 300
_DEFAULT_MEM_CAPACITY = 128


@dataclass
class CacheEntry:
    value: Any
    expires_at: float

    def is_expired(self) -> bool:
        if self.expires_at == 0:
            return False
        return time.time() > self.expires_at


class ContextCache:
    def __init__(self, ttl: int = _DEFAULT_TTL, capacity: int = _DEFAULT_MEM_CAPACITY, disk_dir: str | Path | None = None) -> None:
        self._ttl = ttl
        self._capacity = capacity
        self._disk_dir: Path | None = Path(disk_dir) if disk_dir else None
        self._mem: OrderedDict[str, CacheEntry] = OrderedDict()
        if self._disk_dir:
            self._disk_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str) -> Any | None:
        entry = self._mem.get(key)
        if entry is not None:
            if entry.is_expired():
                self._mem.pop(key, None)
                self._delete_disk(key)
                return None
            self._mem.move_to_end(key)
            return entry.value
        if self._disk_dir:
            entry = self._load_disk(key)
            if entry is not None:
                if entry.is_expired():
                    self._delete_disk(key)
                    return None
                self._set_mem(key, entry)
                return entry.value
        return None

    def set(self, key: str, value: Any, pinned: bool = False) -> None:
        expires_at = 0.0 if pinned else time.time() + self._ttl
        entry = CacheEntry(value=value, expires_at=expires_at)
        self._set_mem(key, entry)
        if self._disk_dir:
            self._save_disk(key, entry)

    def invalidate(self, key: str) -> None:
        self._mem.pop(key, None)
        self._delete_disk(key)

    def clear(self) -> None:
        self._mem.clear()

    def stats(self) -> dict[str, Any]:
        return {"mem_entries": len(self._mem), "capacity": self._capacity, "ttl": self._ttl, "disk_enabled": self._disk_dir is not None, "disk_dir": str(self._disk_dir) if self._disk_dir else None}

    def _set_mem(self, key: str, entry: CacheEntry) -> None:
        if key in self._mem:
            self._mem.move_to_end(key)
        self._mem[key] = entry
        while len(self._mem) > self._capacity:
            self._mem.popitem(last=False)

    def _disk_path(self, key: str) -> Path:
        safe = hashlib.sha256(key.encode()).hexdigest()
        return self._disk_dir / f"{safe}.json"

    def _save_disk(self, key: str, entry: CacheEntry) -> None:
        try:
            payload = {"key": key, "expires_at": entry.expires_at, "value": entry.value}
            self._disk_path(key).write_text(json.dumps(payload), encoding="utf-8")
        except Exception as exc:
            logger.warning("Disk cache write failed for %s: %s", key, exc)

    def _load_disk(self, key: str) -> CacheEntry | None:
        path = self._disk_path(key)
        if not path.exists():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            return CacheEntry(value=payload["value"], expires_at=payload["expires_at"])
        except Exception as exc:
            logger.warning("Disk cache read failed for %s: %s", key, exc)
            return None

    def _delete_disk(self, key: str) -> None:
        if not self._disk_dir:
            return
        try:
            self._disk_path(key).unlink(missing_ok=True)
        except Exception:
            pass


def make_cache_key(repo: str, path: str, sha: str) -> str:
    return f"{repo}::{path}::{sha}"
