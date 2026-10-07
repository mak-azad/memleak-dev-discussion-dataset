"""Step 2 - mine GitHub issues (body + all comments) via the REST API.

  export GITHUB_TOKEN=...                       # required in practice (search is 10 req/min unauthenticated)
  python scripts/02_mine_gh.py --pass main      # rerun the issue searches in config/queries.json
  python scripts/02_mine_gh.py --pass main --snapshot   # refetch the exact issues of the Oct-2026 run
  python scripts/02_mine_gh.py --pass offcwe [--snapshot]

Output: data/raw/gh_<pass>.json  [{"url", "query_buckets", "title", "body", "author",
                                   "author_association", "comments": [{"id","author","author_association","body"}]}]
Added for traceability: per issue `status` (ok | moved | unavailable), `fetched_utc`, `repo`, `repo_language`,
`number`, `state`, `created_at`, `updated_at`, `closed_at`, `labels`, `comments_reported`; per comment
`created_at`, `updated_at`, `html_url`. Issues that fail are kept with status `unavailable` and no text, so none vanish silently.

Note on the original run: the Oct-2026 collection read issues through the issue page's
embedded timeline (logged-out browser), which can omit the middle of long threads.
The REST API returns every comment, so a replication may surface additional units;
04_join_codes.py lists them under data/to_code/ for coding.
"""
from __future__ import annotations

import argparse
import json
import re
import time
import urllib.parse
from datetime import datetime, timezone
from typing import Any

from common import RAW, SNAPSHOT, gh_get, gh_paged, load_config, log

ISSUE_RX = re.compile(r"https://github\.com/([^/]+)/([^/]+)/issues/(\d+)")


def search(pass_: str) -> dict[str, list[str]]:
    cfg = load_config()[f"gh_{pass_}"]
    urls: dict[str, list[str]] = {}
    for bucket, q in cfg["queries"]:
        d, _ = gh_get(f"https://api.github.com/search/issues?q={urllib.parse.quote(q)}&per_page={cfg['per_page']}")
        items = (d or {}).get("items", [])
        for it in items:
            if "/pull/" in it["html_url"]:
                continue
            urls.setdefault(it["html_url"], [])
            if bucket not in urls[it["html_url"]]:
                urls[it["html_url"]].append(bucket)
        log(f"{bucket:12} {q!r:70} -> {len(items)} (total {(d or {}).get('total_count')})")
        time.sleep(2.5)  # search API: 30 req/min authenticated
    return urls


def from_snapshot(pass_: str) -> dict[str, list[str]]:
    snap = json.loads((SNAPSHOT / "gh_issue_urls.json").read_text())[pass_]
    out: dict[str, list[str]] = {}
    for s in snap:
        b = s.get("search_theme") or s.get("cwe_signatures") or ""
        out[s["issue_url"]] = [x for x in b.split(",") if x]
    return out


_REPO_LANG: dict[str, str | None] = {}


def repo_language(owner: str, repo: str) -> str | None:
    """Return the primary language GitHub reports for a repository (cached per repository)."""
    key = f"{owner}/{repo}".lower()
    if key not in _REPO_LANG:
        d, _ = gh_get(f"https://api.github.com/repos/{owner}/{repo}")
        _REPO_LANG[key] = (d or {}).get("language")
    return _REPO_LANG[key]


def fetch(url: str, buckets: list[str]) -> dict[str, Any] | None:
    """Fetch one issue with all comments and the metadata that traceability needs.

    `status` is `ok`, `moved` (the issue now lives at another URL), or `unavailable`
    (404 or repeated errors; title, body and comments are then empty).
    """
    m = ISSUE_RX.match(url)
    if not m:
        return None
    o, r, n = m.groups()
    api = f"https://api.github.com/repos/{o}/{r}/issues/{n}"
    fetched = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    iss, _ = gh_get(api)
    if not iss:
        log(f"unavailable: {url}")
        return {"url": url, "query_buckets": buckets, "status": "unavailable", "fetched_utc": fetched, "repo": f"{o}/{r}",
                "number": int(n), "title": "", "body": "", "author": None, "author_association": None, "comments": []}
    comments = gh_paged(f"{api}/comments")
    moved = (iss.get("html_url") or url).lower() != url.lower()
    return {
        "url": url, "query_buckets": buckets, "title": iss.get("title") or "", "body": iss.get("body") or "",
        "author": (iss.get("user") or {}).get("login"), "author_association": iss.get("author_association"),
        "status": "moved" if moved else "ok", "fetched_utc": fetched, "final_url": iss.get("html_url"),
        "repo": f"{o}/{r}", "repo_language": repo_language(o, r), "number": int(n), "state": iss.get("state"),
        "state_reason": iss.get("state_reason"), "created_at": iss.get("created_at"), "updated_at": iss.get("updated_at"),
        "closed_at": iss.get("closed_at"), "labels": [lb.get("name") for lb in iss.get("labels") or []],
        "comments_reported": iss.get("comments"),
        "comments": [{"id": c["id"], "author": (c.get("user") or {}).get("login"),
                      "author_association": c.get("author_association"), "body": c.get("body") or "",
                      "created_at": c.get("created_at"), "updated_at": c.get("updated_at"), "html_url": c.get("html_url")}
                     for c in comments],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pass", dest="pass_", choices=["main", "offcwe"], required=True)
    ap.add_argument("--snapshot", action="store_true")
    a = ap.parse_args()
    urls = from_snapshot(a.pass_) if a.snapshot else search(a.pass_)
    issues = [x for u, b in urls.items() if (x := fetch(u, b))]
    out = RAW / f"gh_{a.pass_}.json"
    out.write_text(json.dumps(issues))
    log(f"wrote {out}: {len(issues)} issues")


if __name__ == "__main__":
    main()
