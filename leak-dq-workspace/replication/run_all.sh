#!/usr/bin/env bash
# Faithful replication of the October 2026 run (refetches the snapshot IDs), then analysis.
# Usage: GITHUB_TOKEN=... [STACKEXCHANGE_KEY=...] ./run_all.sh [--search]
#   --search   rerun the searches instead of the snapshot (extends/drifts the corpus)
set -euo pipefail
cd "$(dirname "$0")"
MODE="--snapshot"; [[ "${1:-}" == "--search" ]] && MODE=""
python3 scripts/01_mine_so.py --pass main   $MODE
python3 scripts/01_mine_so.py --pass offcwe $MODE
python3 scripts/02_mine_gh.py --pass main   $MODE
python3 scripts/02_mine_gh.py --pass offcwe $MODE
python3 scripts/03_extract_units.py
python3 scripts/04_join_codes.py
python3 scripts/05_analyze.py --check
# traceability exports (write into the workspace root, one level above replication/)
python3 scripts/07_coverage_so.py        # needs data/raw/so_{main,offcwe}_cached.json (copies of the 2026-10-05 caches)
python3 scripts/08_export_threads.py --source so
python3 scripts/08_export_threads.py --source gh
python3 scripts/09_item_source_map.py --strict
python3 scripts/10_post_type_table.py
