"""
GitHubClient — the single gateway for all GitHub API access.

No other module in this SDK may make HTTP requests directly.
All access is authenticated, rate-limit-aware, and failure-tolerant.
"""

from __future__ import annotations

import base64
import logging
import time
from dataclasses import dataclass, field
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json

logger = logging.getLogger(__name__)

_GITHUB_API = "https://api.github.com"
_RATE_LIMIT_RESET_HEADER = "x-ratelimit-reset"
_RATE_LIMIT_REMAINING_HEADER = "x-ratelimit-remaining"


@dataclass
class GitHubClient:
    repo: str
    token: str | None = None
    timeout: int = 15
    _remaining: int = field(default=60, init=False, repr=False)
    _reset_at: float = field(default=0.0, init=False, repr=False)

    def get_file(self, path: str, ref: str = "HEAD") -> bytes:
        url = f"{_GITHUB_API}/repos/{self.repo}/contents/{path}?ref={ref}"
        data = self._request(url)
        if data.get("encoding") != "base64":
            raise GitHubError(f"Unexpected encoding for {path}: {data.get('encoding')}")
        return base64.b64decode(data["content"])

    def get_file_text(self, path: str, ref: str = "HEAD") -> str:
        return self.get_file(path, ref).decode("utf-8")

    def get_file_json(self, path: str, ref: str = "HEAD") -> Any:
        return json.loads(self.get_file_text(path, ref))

    def resolve_ref(self, ref: str) -> str:
        if _is_sha(ref):
            return ref
        try:
            data = self._request(f"{_GITHUB_API}/repos/{self.repo}/branches/{ref}")
            return data["commit"]["sha"]
        except GitHubError:
            pass
        try:
            tags = self._request(f"{_GITHUB_API}/repos/{self.repo}/tags")
            for tag in tags:
                if tag["name"] == ref:
                    return tag["commit"]["sha"]
        except GitHubError:
            pass
        raise GitHubError(f"Cannot resolve ref: {ref!r}")

    def list_files(self, path: str = "", ref: str = "HEAD") -> list[str]:
        url = f"{_GITHUB_API}/repos/{self.repo}/contents/{path}?ref={ref}"
        items = self._request(url)
        if not isinstance(items, list):
            raise GitHubError(f"{path!r} is not a directory")
        return [item["path"] for item in items if item["type"] == "file"]

    def rate_limit_status(self) -> dict[str, Any]:
        return self._request(f"{_GITHUB_API}/rate_limit").get("rate", {})

    def _request(self, url: str) -> Any:
        self._wait_for_rate_limit()
        headers = {"Accept": "application/vnd.github+json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        req = Request(url, headers=headers)
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                self._update_rate_limit(resp.headers)
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as exc:
            self._update_rate_limit(exc.headers)
            if exc.code == 404:
                raise FileNotFoundError(f"Not found on GitHub: {url}") from exc
            if exc.code == 403:
                body = exc.read().decode("utf-8", errors="replace")
                if "rate limit" in body.lower():
                    raise RateLimitError(f"GitHub rate limit exceeded. Resets at {self._reset_at}") from exc
                raise GitHubError(f"GitHub 403 Forbidden: {url}") from exc
            if exc.code == 401:
                raise GitHubError("GitHub 401 Unauthorized — check your token") from exc
            raise GitHubError(f"GitHub HTTP {exc.code}: {url}") from exc
        except URLError as exc:
            raise GitHubError(f"Network error fetching {url}: {exc.reason}") from exc

    def _update_rate_limit(self, headers: Any) -> None:
        try:
            remaining = headers.get(_RATE_LIMIT_REMAINING_HEADER)
            reset = headers.get(_RATE_LIMIT_RESET_HEADER)
            if remaining is not None:
                self._remaining = int(remaining)
            if reset is not None:
                self._reset_at = float(reset)
        except (TypeError, ValueError):
            pass

    def _wait_for_rate_limit(self) -> None:
        if self._remaining <= 1 and self._reset_at > time.time():
            wait = self._reset_at - time.time() + 1
            logger.warning("Rate limit nearly exhausted. Waiting %.1fs", wait)
            time.sleep(wait)


class GitHubError(Exception):
    pass

class RateLimitError(GitHubError):
    pass

def _is_sha(ref: str) -> bool:
    return len(ref) == 40 and all(c in "0123456789abcdefABCDEF" for c in ref)
