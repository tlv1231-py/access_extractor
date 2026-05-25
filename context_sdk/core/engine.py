from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from context_sdk.cache.store import ContextCache, make_cache_key
from context_sdk.context.merger import merge_contexts
from context_sdk.context.slicer import get_context_slice, slice_for_prompt
from context_sdk.core.github import GitHubClient
from context_sdk.schema.models import ContextEnvelope

logger = logging.getLogger(__name__)


class ContextEngine:
    def __init__(self, repo: str, token: str | None = None, ref: str = "HEAD", ttl: int = 300, disk_cache: str | Path | None = None, strict: bool = False) -> None:
        self._repo = repo
        self._default_ref = ref
        self._strict = strict
        self._gh = GitHubClient(repo=repo, token=token)
        self._cache = ContextCache(ttl=ttl, disk_dir=disk_cache)

    def load_context(self, path: str, ref: str | None = None) -> ContextEnvelope:
        resolved_ref = ref or self._default_ref
        sha = self._resolve_sha(resolved_ref)
        cache_key = make_cache_key(self._repo, path, sha)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached
        raw = self._gh.get_file_json(path, ref=sha or resolved_ref)
        envelope = ContextEnvelope.from_raw(raw, path=f"{self._repo}/{path}", sha=sha, ref=resolved_ref, strict=self._strict)
        self._cache.set(cache_key, envelope, pinned=_is_sha(sha))
        return envelope

    def load_contexts(self, paths: list[str], ref: str | None = None) -> list[ContextEnvelope]:
        results = []
        for path in paths:
            try:
                results.append(self.load_context(path, ref=ref))
            except FileNotFoundError:
                logger.warning("Context file not found, skipping: %s", path)
            except Exception as exc:
                logger.warning("Failed to load context %s: %s", path, exc)
        return results

    def merge_contexts(self, paths: list[str], ref: str | None = None, *, key_map: dict[str, str] | None = None, on_conflict: str = "last_wins") -> ContextEnvelope:
        envelopes = self.load_contexts(paths, ref=ref)
        if not envelopes:
            raise ValueError(f"No context files could be loaded from: {paths}")
        return merge_contexts(envelopes, key_map=key_map, on_conflict=on_conflict)

    def get_context_slice(self, envelope: ContextEnvelope, *, keys: list[str] | None = None, max_items: int | None = None, include_metadata: bool = False, depth: int | None = None) -> dict[str, Any]:
        return get_context_slice(envelope, keys=keys, max_items=max_items, include_metadata=include_metadata, depth=depth)

    def slice_for_prompt(self, envelope: ContextEnvelope, *, keys: list[str] | None = None, max_items: int | None = None, depth: int | None = None, prefix: str = "") -> str:
        return slice_for_prompt(envelope, keys=keys, max_items=max_items, depth=depth, prefix=prefix)

    def list_context_files(self, directory: str = "", ref: str | None = None) -> list[str]:
        return self._gh.list_files(directory, ref=ref or self._default_ref)

    def pin_to_latest(self, ref: str | None = None) -> str:
        sha = self._gh.resolve_ref(ref or self._default_ref)
        logger.info("Pinned %r → %s", ref or self._default_ref, sha)
        return sha

    def cache_stats(self) -> dict[str, Any]:
        return self._cache.stats()

    def invalidate_cache(self, path: str | None = None) -> None:
        if path is None:
            self._cache.clear()
        else:
            sha = self._resolve_sha(self._default_ref)
            self._cache.invalidate(make_cache_key(self._repo, path, sha))

    def _resolve_sha(self, ref: str) -> str:
        if _is_sha(ref):
            return ref
        cache_key = make_cache_key(self._repo, "__ref__", ref)
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached
        try:
            sha = self._gh.resolve_ref(ref)
            self._cache.set(cache_key, sha, pinned=False)
            return sha
        except Exception as exc:
            logger.warning("Could not resolve ref %r: %s. Using ref directly.", ref, exc)
            return ref


def _is_sha(ref: str) -> bool:
    return len(ref) == 40 and all(c in "0123456789abcdefABCDEF" for c in ref)
