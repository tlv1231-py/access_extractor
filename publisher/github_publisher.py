from __future__ import annotations

import base64
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)

_GITHUB_API = "https://api.github.com"


class GitHubPublisher:
    def __init__(self, repo: str, token: str, branch: str = "main", target_dir: str = "ai_context") -> None:
        self.repo = repo
        self.token = token
        self.branch = branch
        self.target_dir = target_dir.rstrip("/")

    def publish(self, output_dir: str | Path) -> dict[str, str]:
        output_path = Path(output_dir)
        files = list(output_path.iterdir())
        results: dict[str, str] = {}
        self._push_timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")

        for file in files:
            if not file.is_file():
                continue
            try:
                remote_name = self._normalize_filename(file.name)
                remote_path = f"{self.target_dir}/{remote_name}"
                url = self._push_file(file, remote_path)
                results[remote_name] = url
                logger.info("Published: %s → %s", file.name, remote_path)
            except Exception as exc:
                logger.warning("Failed to publish %s: %s", file.name, exc)
                results[file.name] = f"ERROR: {exc}"

        try:
            marker = json.dumps({"pushed_at": self._push_timestamp}).encode("utf-8")
            marker_path = f"{self.target_dir}/.cache_bust"
            self._push_bytes(marker_path, marker, f"chore: cache bust [{self._push_timestamp}]")
        except Exception as exc:
            logger.warning("Failed to write cache bust marker: %s", exc)

        return results

    def _normalize_filename(self, filename: str) -> str:
        static_names = {
            "access_summary.md",
            "access_graph_compact.json",
            "access_index.json",
        }
        if filename in static_names:
            return filename
        # Any other .json file is the full compiled graph — normalize to static name
        if filename.endswith(".json"):
            return "full_graph.json"
        return filename

    def cleanup(self, output_dir: str | Path) -> None:
        output_path = Path(output_dir)
        for file in output_path.iterdir():
            if file.is_file():
                try:
                    file.unlink()
                    logger.info("Deleted local file: %s", file.name)
                except Exception as exc:
                    logger.warning("Failed to delete %s: %s", file.name, exc)

    def _push_file(self, local_path: Path, remote_path: str) -> str:
        content = base64.b64encode(local_path.read_bytes()).decode("utf-8")
        sha = self._get_existing_sha(remote_path)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        message = f"chore: update {local_path.name} [{timestamp}]"

        payload: dict = {
            "message": message,
            "content": content,
            "branch": self.branch,
        }
        if sha:
            payload["sha"] = sha

        url = f"{_GITHUB_API}/repos/{self.repo}/contents/{remote_path}"
        self._request(url, method="PUT", payload=payload)
        return f"https://github.com/{self.repo}/blob/{self.branch}/{remote_path}"

    def _push_bytes(self, remote_path: str, content: bytes, message: str) -> None:
        encoded = base64.b64encode(content).decode("utf-8")
        sha = self._get_existing_sha(remote_path)
        payload: dict = {"message": message, "content": encoded, "branch": self.branch}
        if sha:
            payload["sha"] = sha
        url = f"{_GITHUB_API}/repos/{self.repo}/contents/{remote_path}"
        self._request(url, method="PUT", payload=payload)

    def _get_existing_sha(self, remote_path: str) -> str | None:
        url = f"{_GITHUB_API}/repos/{self.repo}/contents/{remote_path}?ref={self.branch}"
        try:
            data = self._request(url)
            return data.get("sha")
        except FileNotFoundError:
            return None

    def _request(self, url: str, method: str = "GET", payload: dict | None = None):
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        body = json.dumps(payload).encode() if payload else None
        req = Request(url, headers=headers, method=method, data=body)
        try:
            with urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code == 404:
                raise FileNotFoundError(f"Not found: {url}") from exc
            raise Exception(f"GitHub HTTP {exc.code}: {url}") from exc
