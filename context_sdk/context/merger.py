from __future__ import annotations

import logging
from typing import Any

from context_sdk.schema.models import ContextEnvelope, ContextMetadata

logger = logging.getLogger(__name__)


def merge_contexts(envelopes: list[ContextEnvelope], *, key_map: dict[str, str] | None = None, on_conflict: str = "last_wins") -> ContextEnvelope:
    if not envelopes:
        raise ValueError("Cannot merge empty list of envelopes")

    merged_payload: dict[str, Any] = {}
    sources: list[str] = []
    versions: list[str] = []

    for envelope in envelopes:
        ns_key = _namespace_key(envelope.path, key_map)
        sources.append(envelope.metadata.source or envelope.path)
        versions.append(envelope.metadata.version)

        if ns_key in merged_payload:
            if on_conflict == "raise":
                raise MergeConflictError(f"Key conflict during merge: {ns_key!r} from {envelope.path!r}")
            elif on_conflict == "first_wins":
                continue
            # else last_wins — fall through

        merged_payload[ns_key] = envelope.payload if isinstance(envelope.payload, dict) else {"data": envelope.payload}

    merged_meta = ContextMetadata(
        version=_reconcile_versions(versions),
        source=", ".join(sources),
        timestamp=envelopes[-1].metadata.timestamp,
        sha=envelopes[-1].metadata.sha,
        ref=envelopes[-1].metadata.ref,
        extra={"merged_from": sources, "envelope_count": len(envelopes)},
    )

    return ContextEnvelope(metadata=merged_meta, payload=merged_payload, path="<merged>")


def _namespace_key(path: str, key_map: dict[str, str] | None) -> str:
    if key_map and path in key_map:
        return key_map[path]
    stem = path.rstrip("/").rsplit("/", 1)[-1]
    if "." in stem:
        stem = stem.rsplit(".", 1)[0]
    return stem


def _reconcile_versions(versions: list[str]) -> str:
    unique = list(dict.fromkeys(v for v in versions if v and v != "unknown"))
    if not unique:
        return "unknown"
    if len(unique) == 1:
        return unique[0]
    return f"mixed({', '.join(unique)})"


class MergeConflictError(Exception):
    pass
