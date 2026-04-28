"""Check that an incoming chunk manifest does not overlap with any
currently-active chunk's manifest.

Run by maintainer before opening a new `[Chunk]` GitHub issue. Reads
all `task_manifest.txt` files in `contributions/<chunk-id>/` (proxy for
active chunks — every active chunk has a contributions/ subdir created
when the chunk-task issue opens) and verifies the new manifest is disjoint.

Usage:
    python -m scripts.tasktorrent.check_manifest_overlap <new-chunk-id> <new_manifest.txt>

Exit 0 on disjoint, 1 on overlap detected.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRIB_ROOT = REPO_ROOT / "contributions"


def _read_manifest(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("new_chunk_id", help="chunk-id of the chunk being opened")
    parser.add_argument("new_manifest", help="path to the proposed task_manifest.txt")
    args = parser.parse_args()

    new_manifest = _read_manifest(Path(args.new_manifest))
    if not new_manifest:
        print(f"new manifest empty or missing: {args.new_manifest}", file=sys.stderr)
        return 1

    print(f"Checking {args.new_chunk_id} ({len(new_manifest)} entities) against active chunks...")
    overlaps_found = False
    if CONTRIB_ROOT.exists():
        for chunk_dir in sorted(CONTRIB_ROOT.iterdir()):
            if not chunk_dir.is_dir() or chunk_dir.name == args.new_chunk_id:
                continue
            existing = _read_manifest(chunk_dir / "task_manifest.txt")
            if not existing:
                continue
            overlap = new_manifest & existing
            if overlap:
                overlaps_found = True
                print(
                    f"  OVERLAP with contributions/{chunk_dir.name}/ "
                    f"({len(overlap)} entities):"
                )
                for eid in sorted(overlap)[:20]:
                    print(f"    - {eid}")
                if len(overlap) > 20:
                    print(f"    ... +{len(overlap) - 20} more")

    if overlaps_found:
        print("\nOverlap detected. Resolve before opening the new chunk-task issue.")
        return 1
    print("No overlap. Safe to open the new chunk-task issue.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
