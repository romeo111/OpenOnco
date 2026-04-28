"""Monthly CIViC snapshot refresh orchestrator.

Steps:
1. Locate the current (most-recent) snapshot dir under ``--out-root``.
2. Download CIViC nightly TSV (skipped with ``--no-network``; in that case
   ``--tsv`` must be supplied).
3. Run ``knowledge_base.ingestion.civic_loader.load_civic`` to write
   ``<out_root>/<today>/evidence.yaml``.
4. Run ``scripts/diff_civic_snapshots.py`` between the previous snapshot
   and the new one. Write the markdown summary into the new snapshot
   directory as ``diff_summary.md``.
5. Print a one-line summary to stdout.

Designed for CI (GitHub Actions). Hard-fails (non-zero exit) only on:
- network exhaustion when network is required, or
- ingestion failure (e.g. schema mismatch / missing TSV columns).
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
import time
from datetime import date
from pathlib import Path

# Allow `import knowledge_base...` when run from repo root.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from knowledge_base.ingestion.civic_loader import load_civic  # noqa: E402

CIVIC_NIGHTLY_URL = (
    "https://civicdb.org/downloads/nightly/nightly-ClinicalEvidenceSummaries.tsv"
)

DATE_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def find_latest_snapshot(out_root: Path) -> Path | None:
    """Return the most recent <YYYY-MM-DD> dir under ``out_root``, or None."""
    if not out_root.is_dir():
        return None
    candidates = [
        p for p in out_root.iterdir() if p.is_dir() and DATE_DIR_RE.match(p.name)
    ]
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: p.name)[-1]


def download_civic_tsv(
    dest: Path,
    *,
    url: str = CIVIC_NIGHTLY_URL,
    timeout: float = 60.0,
    retries: int = 3,
    backoff: float = 5.0,
) -> Path:
    """Download CIViC nightly TSV with retry/backoff. Raises on exhaustion."""
    import httpx

    last_exc: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with httpx.stream("GET", url, timeout=timeout, follow_redirects=True) as r:
                r.raise_for_status()
                with dest.open("wb") as f:
                    for chunk in r.iter_bytes():
                        f.write(chunk)
            print(f"  downloaded TSV: {dest} ({dest.stat().st_size} bytes)")
            return dest
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            print(
                f"  attempt {attempt}/{retries} failed: {exc!r}",
                file=sys.stderr,
            )
            if attempt < retries:
                time.sleep(backoff * attempt)
    raise RuntimeError(
        f"failed to download {url} after {retries} attempts: {last_exc!r}"
    )


def run_diff(old_yaml: Path, new_yaml: Path, out_md: Path, biomarkers_dir: Path) -> int:
    """Invoke diff_civic_snapshots.main() in-process."""
    from scripts.diff_civic_snapshots import main as diff_main

    return diff_main(
        [
            str(old_yaml),
            str(new_yaml),
            "--out",
            str(out_md),
            "--biomarkers-dir",
            str(biomarkers_dir),
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-root",
        type=Path,
        default=Path("knowledge_base/hosted/civic"),
        help="Snapshot root (default: knowledge_base/hosted/civic).",
    )
    parser.add_argument(
        "--biomarkers-dir",
        type=Path,
        default=Path("knowledge_base/hosted/content/biomarkers"),
        help="Directory of BIO-* YAMLs for actionability_lookup intersection.",
    )
    parser.add_argument(
        "--no-network",
        action="store_true",
        help="Skip download — read TSV from --tsv instead.",
    )
    parser.add_argument(
        "--tsv",
        type=Path,
        default=None,
        help="Pre-fetched TSV path (required if --no-network).",
    )
    parser.add_argument(
        "--snapshot-date",
        default=None,
        help="Override snapshot date (YYYY-MM-DD). Defaults to today UTC.",
    )
    args = parser.parse_args(argv)

    out_root: Path = args.out_root
    out_root.mkdir(parents=True, exist_ok=True)

    snapshot_date = args.snapshot_date or date.today().isoformat()
    new_dir = out_root / snapshot_date

    previous = find_latest_snapshot(out_root)
    if previous is not None and previous.name == snapshot_date:
        # Today's snapshot already exists — diff against the previous one.
        # Find prior dir (i.e. exclude today).
        candidates = [
            p
            for p in out_root.iterdir()
            if p.is_dir() and DATE_DIR_RE.match(p.name) and p.name < snapshot_date
        ]
        previous = sorted(candidates, key=lambda p: p.name)[-1] if candidates else None

    print(f"refresh_civic: out_root={out_root} snapshot_date={snapshot_date}")
    if previous:
        print(f"  previous snapshot: {previous}")
    else:
        print("  previous snapshot: (none — first run)")

    # Step 2/3: get TSV.
    tmp_handle: tempfile.TemporaryDirectory | None = None
    try:
        if args.no_network:
            if args.tsv is None or not args.tsv.is_file():
                print(
                    "ERROR: --no-network requires --tsv pointing at an existing file",
                    file=sys.stderr,
                )
                return 2
            tsv_path = args.tsv
        else:
            tmp_handle = tempfile.TemporaryDirectory(prefix="civic_refresh_")
            tsv_path = Path(tmp_handle.name) / "civic.tsv"
            try:
                download_civic_tsv(tsv_path)
            except Exception as exc:  # noqa: BLE001
                print(f"FATAL: download failed: {exc!r}", file=sys.stderr)
                return 3

        # Step 3: ingest.
        try:
            new_yaml = load_civic(tsv_path, out_root, snapshot_date=snapshot_date)
        except Exception as exc:  # noqa: BLE001
            print(f"FATAL: ingestion failed: {exc!r}", file=sys.stderr)
            return 4
    finally:
        if tmp_handle is not None:
            tmp_handle.cleanup()

    print(f"  wrote: {new_yaml}")

    # Step 4: diff (only if we have a prior snapshot).
    diff_md = new_dir / "diff_summary.md"
    if previous is None:
        diff_md.write_text(
            "# CIViC snapshot diff\n\n"
            f"Initial snapshot at {snapshot_date}; no prior snapshot to diff against.\n",
            encoding="utf-8",
        )
        print("  no prior snapshot — wrote placeholder diff_summary.md")
    else:
        old_yaml = previous / "evidence.yaml"
        if not old_yaml.is_file():
            print(
                f"WARN: previous snapshot has no evidence.yaml: {old_yaml}",
                file=sys.stderr,
            )
            diff_md.write_text(
                "# CIViC snapshot diff\n\n"
                f"Prior snapshot dir {previous} had no evidence.yaml — diff skipped.\n",
                encoding="utf-8",
            )
        else:
            run_diff(old_yaml, new_yaml, diff_md, args.biomarkers_dir)

    print(f"  diff summary: {diff_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
