from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ContextMetadata:
    version: str
    source: str
    timestamp: str = ""
    sha: str = ""
    ref: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"version": self.version, "source": self.source}
        if self.timestamp:
            d["timestamp"] = self.timestamp
        if self.sha:
            d["sha"] = self.sha
        if self.ref:
            d["ref"] = self.ref
        if self.extra:
            d.update(self.extra)
        return d


@dataclass
class ContextEnvelope:
    metadata: ContextMetadata
    payload: Any
    path: str

    @classmethod
    def from_raw(cls, raw: Any, path: str, sha: str = "", ref: str = "", *, strict: bool = False) -> "ContextEnvelope":
        if isinstance(raw, dict) and "_metadata" in raw:
            meta_raw = raw["_metadata"]
            payload = {k: v for k, v in raw.items() if k != "_metadata"}
        elif isinstance(raw, dict):
            meta_raw = {}
            payload = raw
        else:
            meta_raw = {}
            payload = raw

        metadata = _parse_metadata(meta_raw, path=path, sha=sha, ref=ref, strict=strict)
        return cls(metadata=metadata, payload=payload, path=path)

    def to_dict(self) -> dict[str, Any]:
        return {"_metadata": self.metadata.to_dict(), "payload": self.payload}

    def to_prompt_dict(self) -> dict[str, Any]:
        return self.payload if isinstance(self.payload, dict) else {"data": self.payload}

    def summary(self) -> str:
        return (f"ContextEnvelope(path={self.path!r}, version={self.metadata.version!r}, sha={self.metadata.sha[:8] if self.metadata.sha else 'n/a'})")


def _parse_metadata(meta_raw: dict[str, Any], *, path: str, sha: str, ref: str, strict: bool) -> ContextMetadata:
    version = meta_raw.get("version", "")
    source = meta_raw.get("source", path)
    timestamp = meta_raw.get("timestamp", "")
    extra = {k: v for k, v in meta_raw.items() if k not in ("version", "source", "timestamp")}

    missing = []
    if not version:
        missing.append("version")
        version = "unknown"
    if not source:
        missing.append("source")
        source = path

    if missing:
        msg = f"Context file {path!r} missing metadata fields: {missing}. Normalizing."
        if strict:
            raise SchemaError(msg)
        logger.warning(msg)

    if not timestamp:
        timestamp = datetime.now(timezone.utc).isoformat()

    return ContextMetadata(version=version, source=source, timestamp=timestamp, sha=sha, ref=ref, extra=extra)


class SchemaError(Exception):
    pass
