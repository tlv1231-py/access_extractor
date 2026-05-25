from __future__ import annotations

import logging
from typing import Any

from context_sdk.schema.models import ContextEnvelope

logger = logging.getLogger(__name__)


def get_context_slice(envelope: ContextEnvelope, *, keys: list[str] | None = None, max_items: int | None = None, include_metadata: bool = False, depth: int | None = None) -> dict[str, Any]:
    payload = envelope.payload

    if not isinstance(payload, dict):
        result: dict[str, Any] = {"data": _truncate(payload, max_items)}
        if include_metadata:
            result["_metadata"] = envelope.metadata.to_dict()
        return result

    if keys:
        missing = [k for k in keys if k not in payload]
        if missing:
            logger.warning("Slice keys not found in payload: %s", missing)
        selected = {k: payload[k] for k in keys if k in payload}
    else:
        selected = dict(payload)

    if depth is not None:
        selected = {k: _prune_depth(v, depth) for k, v in selected.items()}

    if max_items is not None:
        selected = {k: _truncate(v, max_items) for k, v in selected.items()}

    if include_metadata:
        selected["_metadata"] = envelope.metadata.to_dict()

    return selected


def slice_for_prompt(envelope: ContextEnvelope, *, keys: list[str] | None = None, max_items: int | None = None, depth: int | None = None, prefix: str = "") -> str:
    import json
    slice_ = get_context_slice(envelope, keys=keys, max_items=max_items, include_metadata=False, depth=depth)
    body = json.dumps(slice_, indent=2, ensure_ascii=False)
    return f"{prefix}\n{body}" if prefix else body


def _truncate(value: Any, max_items: int | None) -> Any:
    if max_items is None:
        return value
    if isinstance(value, list) and len(value) > max_items:
        return value[:max_items]
    return value


def _prune_depth(value: Any, depth: int) -> Any:
    if depth <= 0:
        return "..."
    if isinstance(value, dict):
        return {k: _prune_depth(v, depth - 1) for k, v in value.items()}
    if isinstance(value, list):
        return [_prune_depth(item, depth - 1) for item in value]
    return value
