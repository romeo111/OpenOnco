"""Generate a deterministic inventory report for a CIViC snapshot.

Usage:
    python scripts/inventory_civic_snapshot.py knowledge_base/hosted/civic/2026-04-25/evidence.yaml
    python scripts/inventory_civic_snapshot.py ... --out docs/reviews/civic-inventory.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from knowledge_base.ingestion.civic_inventory import (  # noqa: E402
    build_civic_inventory_from_path,
    render_inventory_markdown,
)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("snapshot", type=Path, help="Path to CIViC evidence.yaml")
    ap.add_argument("--out", type=Path, help="Optional markdown output path")
    ap.add_argument("--top-n", type=int, default=20)
    args = ap.parse_args(argv)

    inventory = build_civic_inventory_from_path(args.snapshot, top_n=args.top_n)
    markdown = render_inventory_markdown(
        inventory,
        snapshot_label=str(args.snapshot).replace("\\", "/"),
    )

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(markdown + "\n", encoding="utf-8")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
