"""Shared paths and HTTP helpers (stdlib only)."""
from __future__ import annotations

import gzip
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

CONFIG = ROOT / "config" / "queries.json"
SNAPSHOT = ROOT / "snapshot"
CODES = ROOT / "codes"
DATA = ROOT / "data"
RAW = DATA / "raw"
UNITS = DATA / "units"
CODED = DATA / "coded"
TO_CODE = DATA / "to_code"
RESULTS = ROOT / "results"
PASSES = ("main", "offcwe")

for d in (RAW, UNITS, CODED, TO_CODE, RESULTS):
    d.mkdir(parents=True, exist_ok=True)


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG.read_text())


def log(*a: object) -> None:
    print(*a, file=sys.stderr, flush=True)


# ------------------------------------------------------------- StackExchange
SE_BASE = "https://api.stackexchange.com/2.3"
SE_KEY = os.environ.get("STACKEXCHANGE_KEY")  # optional: raises quota from 300 to 10,000/day


def se_get(path: str, **params: str) -> dict[str, Any]:
    params.setdefault("site", "stackoverflow")
    if SE_KEY:
        params["key"] = SE_KEY
    url = f"{SE_BASE}{path}?{urllib.parse.urlencode(params)}"
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip"})
            raw = urllib.request.urlopen(req, timeout=60).read()
            try:
                raw = gzip.decompress(raw)
            except OSError:
                pass
            d = json.loads(raw)
            if d.get("backoff"):
                time.sleep(int(d["backoff"]) + 1)
            if d.get("quota_remaining", 1) < 5:
                log("WARNING: StackExchange quota nearly exhausted; set STACKEXCHANGE_KEY")
            time.sleep(0.35)
            return d
        except urllib.error.HTTPError as e:
            log(f"SE HTTP {e.code} on {path}; retry {attempt}")
            time.sleep(5 * (attempt + 1))
    return {}


def se_paged(path: str, **params: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    page = 1
    while True:
        d = se_get(path, page=str(page), pagesize="100", **params)
        items += d.get("items", [])
        if not d.get("has_more") or page >= 10:
            return items
        page += 1


def chunks(xs: list[Any], n: int) -> Iterable[list[Any]]:
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


# ------------------------------------------------------------- GitHub
def _read_gh_token() -> str | None:
    """Token lookup order: GITHUB_TOKEN / GH_TOKEN env, a .env file at the repo root, then `gh auth token`."""
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        return tok
    for env in (ROOT / ".env", ROOT.parent / ".env"):
        if env.exists():
            for line in env.read_text().splitlines():
                if line.strip().startswith(("GITHUB_TOKEN=", "GH_TOKEN=")):
                    return line.split("=", 1)[1].strip().strip('"\'')
    try:
        import subprocess
        out = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=10)
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


GH_TOKEN = _read_gh_token()


def gh_get(url: str) -> tuple[Any, dict[str, str]]:
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if GH_TOKEN:
        headers["Authorization"] = f"Bearer {GH_TOKEN}"
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
                return json.loads(r.read()), dict(r.headers)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                reset = int(e.headers.get("X-RateLimit-Reset", time.time() + 60))
                wait = max(5, reset - int(time.time()) + 2)
                log(f"GitHub rate limit; sleeping {wait}s")
                time.sleep(min(wait, 900))
                continue
            if e.code == 404:
                return None, {}
            log(f"GitHub HTTP {e.code} on {url}; retry {attempt}")
            time.sleep(5)
    return None, {}


def gh_paged(url: str) -> list[Any]:
    out: list[Any] = []
    sep = "&" if "?" in url else "?"
    page = 1
    while True:
        d, _ = gh_get(f"{url}{sep}per_page=100&page={page}")
        if not d:
            return out
        out += d
        if len(d) < 100:
            return out
        page += 1


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    n = 0
    with path.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    return n


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
