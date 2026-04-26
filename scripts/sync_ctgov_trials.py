"""Prewarm the on-disk ctgov cache for every patient profile in `examples/`.

Per docs/plans/ua_ingestion_and_alternatives_2026-04-26.md §3.3 + §5.4.

Why this exists:
  - `scripts/build_site.py` renders ~190 case HTMLs server-side and
    needs ctgov data for the third Plan track. Hitting api.clinicaltrials.gov
    once per case during every build is slow and rate-limit-fragile.
  - The Pyodide bundle in the browser cannot reach ctgov at all
    (`knowledge_base/engine/experimental_options.py:14-17`); it must
    rely on a baked cache.

What it does:
  - Walks `examples/*.json`, runs `generate_plan(...)` with a live
    `search_trials` callable, points the cache at
    `knowledge_base/hosted/content/cache/ctgov/`.
  - `enumerate_experimental_options()` writes one JSON per
    (disease, biomarker, line) signature there. Subsequent calls
    within the 7-day TTL skip the network.

Run:
    python scripts/sync_ctgov_trials.py            # all examples
    python scripts/sync_ctgov_trials.py --force    # ignore existing TTL

The output cache directory is committed (commit it after running) so
the build is reproducible offline and the Pyodide bundle ships with
trials.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from knowledge_base.engine import generate_plan, is_diagnostic_profile
from knowledge_base.engine import experimental_options as eo_module
from knowledge_base.clients.ctgov_client import search_trials


KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"
CACHE_ROOT = KB_ROOT / "cache" / "ctgov"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Bypass the 7-day TTL and re-fetch every signature.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process only the first N example files (for smoke testing).",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.5,
        help="Seconds to sleep between ctgov calls (rate-limit courtesy).",
    )
    args = parser.parse_args()

    CACHE_ROOT.mkdir(parents=True, exist_ok=True)

    if args.force:
        eo_module._DEFAULT_TTL_DAYS = 0  # type: ignore[attr-defined]

    files = sorted(EXAMPLES.glob("patient_*.json"))
    if args.limit:
        files = files[: args.limit]

    print(f"[sync-ctgov] {len(files)} patient files; cache -> {CACHE_ROOT}")

    treatment_count = 0
    diagnostic_count = 0
    failures: list[tuple[str, str]] = []
    cached_before = {p.name for p in CACHE_ROOT.glob("ctgov_*.json")}

    for i, path in enumerate(files, 1):
        try:
            patient = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append((path.name, f"json parse: {exc}"))
            continue

        if is_diagnostic_profile(patient):
            diagnostic_count += 1
            continue

        try:
            result = generate_plan(
                patient,
                kb_root=KB_ROOT,
                experimental_search_fn=search_trials,
                experimental_cache_root=CACHE_ROOT,
            )
        except Exception as exc:
            failures.append((path.name, f"generate_plan: {exc}"))
            continue

        opt = result.experimental_options
        n_trials = len(opt.trials) if opt else 0
        note = f" — {opt.notes}" if opt and opt.notes else ""
        print(
            f"[{i:>3}/{len(files)}] {path.stem:50s} "
            f"trials={n_trials:>2}{note}"
        )
        treatment_count += 1
        time.sleep(args.sleep)

    cached_after = {p.name for p in CACHE_ROOT.glob("ctgov_*.json")}
    new_files = cached_after - cached_before

    print()
    print(f"[sync-ctgov] treatment plans synced: {treatment_count}")
    print(f"[sync-ctgov] diagnostic profiles skipped: {diagnostic_count}")
    print(f"[sync-ctgov] cache files total: {len(cached_after)} (+{len(new_files)} new)")
    if failures:
        print(f"[sync-ctgov] failures: {len(failures)}")
        for name, msg in failures:
            print(f"  - {name}: {msg}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
