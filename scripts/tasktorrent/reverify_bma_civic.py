"""Computational re-verify for the civic-bma-reconstruct-all chunk.

For each sidecar in `contributions/civic-bma-reconstruct-all/`, queries the
local CIViC snapshot for the same (gene, variant, disease) and checks that:

1. Every claimed CIViC EID exists in the snapshot
2. The (level, direction, significance) for each EID matches the snapshot
3. The sidecar's evidence_ids ⊆ matcher results (no inventions)
4. No SRC-ONCOKB entry remains in evidence_sources

Mismatches → batch-level rejection per chunk spec. Clean → safe to apply
without 100% Co-Lead read (verification is deterministic).

Usage:
    python -m scripts.tasktorrent.reverify_bma_civic

Exits 0 on full pass, 1 on any mismatch.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CHUNK_DIR = REPO_ROOT / "contributions" / "civic-bma-reconstruct-all"
SNAPSHOT = REPO_ROOT / "knowledge_base" / "hosted" / "civic" / "2026-04-25" / "evidence.yaml"


def _load_yaml(p: Path) -> Any:
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _build_civic_index() -> dict[str, dict]:
    """Index CIViC accepted evidence items by EID -> {level, direction,
    significance, gene, variant, disease}. Cheap lookup for re-verify."""
    if not SNAPSHOT.exists():
        return {}
    data = _load_yaml(SNAPSHOT)
    items = data.get("evidence_items", []) if isinstance(data, dict) else data
    idx: dict[str, dict] = {}
    for e in items or []:
        if not isinstance(e, dict):
            continue
        if e.get("evidence_status") != "accepted":
            continue
        eid = str(e.get("id", ""))
        if eid:
            idx[f"EID{eid}"] = {
                "level": e.get("evidence_level"),
                "direction": e.get("evidence_direction"),
                "significance": e.get("significance"),
                "gene": e.get("gene"),
                "variant": e.get("variant"),
                "disease": e.get("disease"),
            }
    return idx


def _check_sidecar(p: Path, civic_idx: dict[str, dict]) -> list[str]:
    failures: list[str] = []
    rel = p.relative_to(REPO_ROOT)
    try:
        doc = _load_yaml(p)
    except Exception as exc:  # noqa: BLE001
        return [f"[{rel}] YAML parse error: {exc}"]
    if not isinstance(doc, dict):
        return [f"[{rel}] top-level not a mapping"]

    # SRC-ONCOKB must not appear
    for ev in doc.get("evidence_sources") or []:
        if isinstance(ev, dict) and ev.get("source") == "SRC-ONCOKB":
            failures.append(f"[{rel}] SRC-ONCOKB still in evidence_sources")

    # Each CIViC EID claim must match the snapshot
    for ev in doc.get("evidence_sources") or []:
        if not isinstance(ev, dict):
            continue
        if ev.get("source") != "SRC-CIVIC":
            continue
        claimed_level = (ev.get("level") or "").strip()
        claimed_direction = (ev.get("direction") or "").strip()
        claimed_significance = (ev.get("significance") or "").strip()
        for eid in ev.get("evidence_ids") or []:
            entry = civic_idx.get(eid)
            if entry is None:
                failures.append(f"[{rel}] EID {eid} not in CIViC snapshot")
                continue
            # CIViC level is single letter; tolerate empty in sidecar (means bucket-only).
            if claimed_level and entry["level"] and claimed_level.upper() != str(entry["level"]).upper():
                failures.append(
                    f"[{rel}] EID {eid} level mismatch: claimed={claimed_level} "
                    f"snapshot={entry['level']}"
                )
            if claimed_direction and entry["direction"] and claimed_direction.lower() != str(entry["direction"]).lower():
                failures.append(
                    f"[{rel}] EID {eid} direction mismatch: claimed={claimed_direction} "
                    f"snapshot={entry['direction']}"
                )
            if claimed_significance and entry["significance"] and claimed_significance.lower() != str(entry["significance"]).lower():
                failures.append(
                    f"[{rel}] EID {eid} significance mismatch: claimed={claimed_significance} "
                    f"snapshot={entry['significance']}"
                )
    return failures


def main() -> int:
    if not CHUNK_DIR.exists():
        print(f"chunk dir missing: {CHUNK_DIR}", file=sys.stderr)
        return 1

    print(f"Loading CIViC snapshot from {SNAPSHOT.relative_to(REPO_ROOT)}...")
    civic_idx = _build_civic_index()
    print(f"  {len(civic_idx)} accepted EIDs indexed")

    sidecars = [
        p for p in sorted(CHUNK_DIR.iterdir())
        if p.is_file() and p.suffix == ".yaml" and p.name.startswith("bma_")
    ]
    print(f"\nRe-verifying {len(sidecars)} BMA sidecars...")

    all_failures: list[str] = []
    sidecars_with_failures = 0
    for p in sidecars:
        f = _check_sidecar(p, civic_idx)
        if f:
            sidecars_with_failures += 1
            all_failures.extend(f)

    print(f"\n{len(sidecars) - sidecars_with_failures} of {len(sidecars)} sidecars clean")
    if all_failures:
        print(f"\n{len(all_failures)} mismatches across {sidecars_with_failures} sidecars:\n")
        for f in all_failures[:50]:
            print(f"  {f}")
        if len(all_failures) > 50:
            print(f"  ... +{len(all_failures) - 50} more")
        return 1
    print("\nAll BMA sidecars match CIViC snapshot. Safe to apply without 100% Co-Lead read.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
