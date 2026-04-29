"""One-off worker for chunk-task #36 — bma-civic-eid-recheck.

Walks all 399 BMA records in knowledge_base/hosted/content/biomarker_actionability/
and re-validates every CIViC EID referenced in `evidence_sources` against
the latest CIViC snapshot under knowledge_base/hosted/civic/.

Output: audit-report.yaml — deterministic; re-running yields identical
content (no timestamps, no random ordering).

Per chunk-spec: report-only, no KB content modified.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
BMA_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarker_actionability"
CIVIC_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "civic"
OUT_DIR = REPO_ROOT / "contributions" / "bma-civic-eid-recheck-2026-04-29-0030"


def load_snapshot_eids() -> tuple[str, set[str]]:
    """Return (snapshot_date, set_of_eid_strings) from the latest CIViC snapshot."""
    snapshot_dirs = sorted([d for d in CIVIC_DIR.iterdir() if d.is_dir()], reverse=True)
    if not snapshot_dirs:
        raise SystemExit("ERROR: no CIViC snapshot found under knowledge_base/hosted/civic/")
    latest = snapshot_dirs[0]
    snapshot_file = latest / "evidence.yaml"
    if not snapshot_file.is_file():
        raise SystemExit(f"ERROR: {snapshot_file} not found")

    with snapshot_file.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    eids: set[str] = set()
    for item in data.get("evidence_items", []) or []:
        if isinstance(item, dict):
            raw = item.get("id")
            if raw is not None:
                # Snapshot stores '1', '12345' — BMAs reference 'EID1', 'EID12345'
                eids.add(f"EID{str(raw).strip()}")
    return data.get("snapshot_date", latest.name), eids


def collect_bma_eid_usage() -> list[tuple[str, list[tuple[str, list[str]]]]]:
    """For every BMA file: return (path, [(source_id, [eid, ...]), ...])."""
    out: list[tuple[str, list[tuple[str, list[str]]]]] = []
    for path in sorted(BMA_DIR.glob("*.yaml")):
        try:
            with path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        bma_id = data.get("id") or path.stem
        sources = data.get("evidence_sources") or []
        per_bma: list[tuple[str, list[str]]] = []
        for es in sources:
            if not isinstance(es, dict):
                continue
            eids = es.get("evidence_ids") or []
            if not isinstance(eids, list):
                continue
            normalized: list[str] = []
            for e in eids:
                if isinstance(e, str) and e.startswith("EID"):
                    normalized.append(e)
                elif isinstance(e, (int, str)):
                    # tolerate bare integers / strings — normalize to EID-prefixed
                    normalized.append(f"EID{str(e).strip()}" if str(e).strip().isdigit() else str(e))
            per_bma.append((es.get("source") or "(unknown)", normalized))
        out.append((bma_id, per_bma))
    return out


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    snapshot_date, snapshot_eids = load_snapshot_eids()
    print(f"  CIViC snapshot {snapshot_date}: {len(snapshot_eids)} EIDs")

    bma_data = collect_bma_eid_usage()
    print(f"  Walking {len(bma_data)} BMAs...")

    rows: list[dict] = []
    bma_with_civic_count = 0
    eids_total = 0
    eids_known = 0
    eids_unknown = 0

    for bma_id, sources_list in bma_data:
        per_bma_eids: set[str] = set()
        per_bma_unknown: list[str] = []
        for src, eids in sources_list:
            if src == "SRC-CIVIC" and eids:
                bma_with_civic_count += 1 if not per_bma_eids else 0
                for e in eids:
                    per_bma_eids.add(e)
                    eids_total += 1
                    if e in snapshot_eids:
                        eids_known += 1
                    else:
                        eids_unknown += 1
                        per_bma_unknown.append(e)

        if per_bma_eids:  # only record BMAs that actually cite CIViC EIDs
            rows.append({
                "bma_id": bma_id,
                "total_eids": len(per_bma_eids),
                "known_eids": sum(1 for e in per_bma_eids if e in snapshot_eids),
                "unknown_eids_count": len(per_bma_unknown),
                "unknown_eids": sorted(set(per_bma_unknown)) or None,
            })

    rows.sort(key=lambda r: (-r["unknown_eids_count"], r["bma_id"]))

    report = {
        "_contribution_kind": "audit-report",
        "chunk_id": "bma-civic-eid-recheck-2026-04-29-0030",
        "snapshot_date": snapshot_date,
        "snapshot_eid_count": len(snapshot_eids),
        "bma_total_count": len(bma_data),
        "bma_with_civic_eids_count": sum(1 for r in rows if r["total_eids"] > 0),
        "bma_with_unknown_eids_count": sum(1 for r in rows if r["unknown_eids_count"] > 0),
        "eids_referenced_total": eids_total,
        "eids_known_total": eids_known,
        "eids_unknown_total": eids_unknown,
        "rows": rows,
    }

    out_path = OUT_DIR / "audit-report.yaml"
    out_path.write_text(
        yaml.safe_dump(report, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )
    print(f"  wrote {out_path.relative_to(REPO_ROOT).as_posix()}")
    print(f"  Summary: {report['bma_with_civic_eids_count']} BMAs cite CIViC; "
          f"{report['eids_known_total']}/{report['eids_referenced_total']} EIDs current; "
          f"{report['bma_with_unknown_eids_count']} BMAs have unknown EIDs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
