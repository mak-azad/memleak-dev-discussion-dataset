"""Sanity tests for the unit-selection rules (run: python -m pytest tests  or  python tests/test_extract.py)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("extract", ROOT / "scripts" / "03_extract_units.py")
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)  # type: ignore[union-attr]

ISSUE = {
    "url": "https://github.com/o/r/issues/1", "query_buckets": ["CWE-401"], "author": "alice",
    "author_association": "NONE", "title": "Does this leak memory?",
    "body": "We never free the buffer on the error path. Is the pointer overwritten?\n\n```c\nfree(p);\n```",
    "comments": [{"id": 11, "author": "bob", "author_association": "MEMBER",
                  "body": "Who is responsible for freeing it? The caller must free the result."}],
}


def test_main_gh_keys() -> None:
    units = ex.gh_main_units([ISSUE])
    keys = [u["unit_key"] for u in units]
    assert keys[0] == "https://github.com/o/r/issues/1|-|Q|0"          # title question comes first
    assert "https://github.com/o/r/issues/1|-|Q|1" in keys              # body question
    assert any(k.endswith("|11|Q|0") for k in keys)                      # maintainer question
    assert any(u["role"] == "M" for u in units)
    assert all("free(p)" not in u["text"] for u in units)                # code blocks stripped
    assert any(u["form"] == "statement" for u in units)                  # DQ-prefiltered statements


def test_offcwe_cap() -> None:
    body = ". ".join(f"Sentence {i} leaks a descriptor here" for i in range(10)) + "."
    iss = {**ISSUE, "body": body, "comments": []}
    units = ex.gh_offcwe_units([iss])
    assert sum(u["form"] == "statement" for u in units) == 4             # at most 4 statements per post


if __name__ == "__main__":
    test_main_gh_keys()
    test_offcwe_cap()
    print("ok")
