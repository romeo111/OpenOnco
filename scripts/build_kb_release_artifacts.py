#!/usr/bin/env python3
"""Build deterministic release metadata and a dependency graph for the KB.

The output contains only curated knowledge-base metadata. It must never be
used for patient inputs, generated patient answers, or clinical decisions.

Examples:
  py -3.12 scripts/build_kb_release_artifacts.py
  py -3.12 scripts/build_kb_release_artifacts.py --manifest-output build/kb-manifest.json --graph-output build/kb-graph.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from knowledge_base.release_manifest import build_release_artifacts  # noqa: E402


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument(
        "--kb-root",
        type=Path,
        default=REPO_ROOT / "knowledge_base" / "hosted" / "content",
        help="KB content root (default: %(default)s)",
    )
    parser.add_argument(
        "--manifest-output",
        type=Path,
        help="Optional JSON path for the release manifest.",
    )
    parser.add_argument(
        "--graph-output",
        type=Path,
        help="Optional JSON path for the dependency graph.",
    )
    parser.add_argument(
        "--strict-source-refs",
        action="store_true",
        help="Promote unresolved narrative SRC-* tokens to reference errors.",
    )
    args = parser.parse_args()
    if not args.kb_root.is_dir():
        print(f"ERROR: not a directory: {args.kb_root}", file=sys.stderr)
        return 2

    manifest, graph = build_release_artifacts(
        args.kb_root,
        strict_source_refs=args.strict_source_refs,
    )
    if args.manifest_output:
        _write_json(args.manifest_output, manifest)
    if args.graph_output:
        _write_json(args.graph_output, graph)
    if not args.manifest_output:
        print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))

    validation = manifest["validation"]
    return int(any(
        validation[key]
        for key in ("schema_errors", "reference_errors", "contract_errors")
    ))


if __name__ == "__main__":
    raise SystemExit(main())
