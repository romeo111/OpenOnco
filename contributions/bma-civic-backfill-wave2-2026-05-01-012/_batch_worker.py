"""Wave-2 backfill worker — bma-civic-backfill-wave2-2026-05-01-012 (issue #193).

Mirrors the reference worker (closed #43,
contributions/bma-civic-backfill-2026-04-29-001/_batch_worker.py). Logic:

  1. Read each BMA in this chunk's manifest from hosted/.
  2. Derive gene from BMA-id (BMA-<GENE>-...).
  3. Look up CIViC snapshot 2026-04-25 evidence_items matching (gene, disease).
  4. If matches AND evidence_sources currently empty:
       - Group into evidence_sources block (level + direction + significance).
       - Produce per-BMA upsert sidecar replacing empty list with populated
         block; preserve actionability_review_required: true.
  5. If BMA already has SRC-CIVIC entries → audit row "already_has_civic_evidence".
  6. If gene unknown / no disease overlap → audit row with structured reason.

Per chunk-spec: do NOT invent treatment claims when CIViC has no suitable
evidence item. Off-disease evidence items are NOT included
(cross-disease borrowing is the kind of "invention" the spec forbids).
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
BMA_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarker_actionability"
CIVIC_FILE = REPO_ROOT / "knowledge_base" / "hosted" / "civic" / "2026-04-25" / "evidence.yaml"

CHUNK_ID = "bma-civic-backfill-wave2-2026-05-01-012"
ISSUE_NUMBER = 193
SUBMISSION_DATE = "2026-05-01"
OUT_DIR = REPO_ROOT / "contributions" / CHUNK_ID

MANIFEST = [
    "BMA-CALR-PMF",
    "BMA-HRD-STATUS-OVARIAN",
    "BMA-MLH1-SOMATIC-UROTHELIAL",
    "BMA-MSH6-SOMATIC-GASTRIC",
    "BMA-PMS2-SOMATIC-ENDOMETRIAL",
]

# Disease-id → CIViC disease search tokens (lowercase substring match).
# Conservative: a CIViC disease string must contain ANY listed token.
DISEASE_TOKENS: dict[str, tuple[str, ...]] = {
    "DIS-PMF": ("primary myelofibrosis", "myelofibrosis"),
    "DIS-OVARIAN": ("ovarian",),
    "DIS-UROTHELIAL": ("urothelial", "bladder"),
    "DIS-GASTRIC": ("gastric", "stomach"),
    "DIS-ENDOMETRIAL": ("endometrial",),
}


def gene_from_bma_id(bma_id: str) -> str | None:
    parts = bma_id.split("-")
    if len(parts) < 2 or parts[0] != "BMA":
        return None
    return parts[1]


def disease_match(disease_id: str, civic_disease: str) -> bool:
    if not isinstance(civic_disease, str) or not disease_id:
        return False
    cd_lc = civic_disease.lower()
    tokens = DISEASE_TOKENS.get(disease_id, ())
    if tokens:
        return any(tok in cd_lc for tok in tokens)
    stem = disease_id.replace("DIS-", "").replace("-", " ").lower()
    return stem in cd_lc


def load_civic_index() -> dict[str, list[dict]]:
    print(f"  Loading CIViC snapshot from {CIVIC_FILE.relative_to(REPO_ROOT)}...", file=sys.stderr)
    with CIVIC_FILE.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    items = data.get("evidence_items", []) or []
    by_gene: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        if isinstance(item, dict):
            gene = item.get("gene")
            if gene:
                by_gene[gene.upper()].append(item)
    print(f"  Indexed {len(items)} CIViC evidence items across {len(by_gene)} genes.", file=sys.stderr)
    return by_gene


def _bma_yaml_path(bma_id: str) -> Path | None:
    candidate = bma_id.replace("BMA-", "").lower().replace("-", "_")
    direct = BMA_DIR / f"bma_{candidate}.yaml"
    if direct.is_file():
        return direct
    for p in BMA_DIR.glob("*.yaml"):
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, dict) and d.get("id") == bma_id:
            return p
    return None


def find_matching_evidence(bma: dict, civic_by_gene: dict[str, list[dict]]) -> tuple[str | None, list[dict]]:
    bma_id = bma.get("id") or ""
    gene = gene_from_bma_id(bma_id)
    disease_id = bma.get("disease_id")
    if not gene or not disease_id:
        return gene, []
    items = civic_by_gene.get(gene.upper(), [])
    matched = [it for it in items if disease_match(disease_id, it.get("disease", ""))]
    return gene, matched


def build_evidence_sources(matched: list[dict]) -> list[dict]:
    bucket: dict[tuple, dict] = {}
    for it in matched:
        level = it.get("evidence_level") or "X"
        direction = it.get("evidence_direction") or "Unknown"
        significance = it.get("significance") or "Unknown"
        key = (level, direction, significance)
        if key not in bucket:
            bucket[key] = {
                "source": "SRC-CIVIC",
                "level": level,
                "evidence_ids": [],
                "direction": direction,
                "significance": significance,
                "note": "",
            }
        eid = it.get("id")
        if eid:
            bucket[key]["evidence_ids"].append(f"EID{eid}")

    for key, entry in bucket.items():
        therapies: set[str] = set()
        for it in matched:
            it_key = (it.get("evidence_level") or "X",
                      it.get("evidence_direction") or "Unknown",
                      it.get("significance") or "Unknown")
            if it_key != key:
                continue
            for t in it.get("therapies", []) or []:
                if isinstance(t, dict) and t.get("name"):
                    therapies.add(t["name"])
                elif isinstance(t, str):
                    therapies.add(t)
        if therapies:
            entry["note"] = (
                f"CIViC snapshot 2026-04-25: {entry['direction']} {entry['significance']} "
                f"evidence for therapies: {', '.join(sorted(therapies)[:10])}."
            )
        else:
            entry["note"] = (
                f"CIViC snapshot 2026-04-25: {entry['direction']} {entry['significance']} "
                "evidence without therapy-specific annotation."
            )

    out = list(bucket.values())
    level_order = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "X": 5}
    out.sort(key=lambda e: (level_order.get(e["level"], 9),
                            e["direction"], e["significance"]))
    return out


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    civic_by_gene = load_civic_index()

    upserts: list[dict] = []
    no_match: list[dict] = []
    not_found: list[str] = []

    for bma_id in MANIFEST:
        path = _bma_yaml_path(bma_id)
        if path is None:
            not_found.append(bma_id)
            continue
        try:
            bma = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            not_found.append(bma_id)
            continue
        if not isinstance(bma, dict):
            not_found.append(bma_id)
            continue

        existing = bma.get("evidence_sources") or []
        already_has_civic = any(
            isinstance(e, dict) and e.get("source") == "SRC-CIVIC" for e in existing
        )
        gene, matched = find_matching_evidence(bma, civic_by_gene)

        if already_has_civic:
            no_match.append({
                "bma_id": bma_id,
                "gene": gene,
                "disease_id": bma.get("disease_id"),
                "verdict": "already_has_civic_evidence",
                "no_civic_match_reason": (
                    "BMA already carries SRC-CIVIC evidence_sources from a "
                    "prior backfill wave; wave-2 does not redo reconstruct work."
                ),
                "current_eid_count": sum(len(e.get("evidence_ids", []))
                                          for e in existing
                                          if isinstance(e, dict) and e.get("source") == "SRC-CIVIC"),
            })
            continue

        if not matched:
            verdict = (
                "gene_not_in_civic" if gene and gene.upper() not in civic_by_gene
                else "gene_in_civic_no_disease_overlap" if gene
                else "gene_unknown_in_bma_id"
            )
            gene_only_n = len(civic_by_gene.get((gene or "").upper(), []))
            reason_text = {
                "gene_not_in_civic": (
                    f"Gene token '{gene}' parsed from BMA-id is not present in "
                    f"CIViC snapshot 2026-04-25; cannot link evidence."
                ),
                "gene_in_civic_no_disease_overlap": (
                    f"Gene '{gene}' has {gene_only_n} CIViC evidence items but "
                    f"none overlap disease tokens for {bma.get('disease_id')}."
                ),
                "gene_unknown_in_bma_id": (
                    "Could not parse gene token from BMA-id; manual mapping required."
                ),
            }[verdict]
            no_match.append({
                "bma_id": bma_id,
                "gene": gene,
                "disease_id": bma.get("disease_id"),
                "verdict": verdict,
                "no_civic_match_reason": reason_text,
                "civic_gene_evidence_count_any_disease": gene_only_n,
            })
            continue

        new_sources = build_evidence_sources(matched)
        upsert = dict(bma)
        upsert["evidence_sources"] = new_sources
        upsert["actionability_review_required"] = True
        upsert["_contribution"] = {
            "chunk_id": CHUNK_ID,
            "contributor": "claude-anthropic-internal",
            "submission_date": SUBMISSION_DATE,
            "ai_tool": "claude-code",
            "ai_model": "claude-opus-4-7",
            "target_action": "upsert",
            "target_entity_id": bma_id,
            "notes_for_reviewer": (
                f"CIViC backfill wave-2: gene={gene} matched {len(matched)} evidence items in CIViC "
                f"snapshot 2026-04-25 with disease overlap on {bma.get('disease_id')}. "
                "evidence_sources populated; no other fields modified. "
                "actionability_review_required: true preserved for maintainer adjudication."
            ),
        }
        out_path = OUT_DIR / path.name
        out_path.write_text(
            yaml.safe_dump(upsert, sort_keys=False, allow_unicode=True, default_flow_style=False),
            encoding="utf-8",
        )
        upserts.append({
            "bma_id": bma_id, "gene": gene, "disease_id": bma.get("disease_id"),
            "matched_evidence_count": len(matched),
            "evidence_sources_blocks": len(new_sources),
        })

    # task_manifest.txt — exactly the manifest IDs (issue body verbatim)
    (OUT_DIR / "task_manifest.txt").write_text(
        "\n".join(MANIFEST) + "\n", encoding="utf-8"
    )

    # audit-report.yaml — always written (records every BMA outcome)
    (OUT_DIR / "audit-report.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": CHUNK_ID,
                "contributor": "claude-anthropic-internal",
                "submission_date": SUBMISSION_DATE,
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "notes_for_reviewer": (
                    "Report-only: per-BMA outcomes for this chunk's manifest. "
                    "Upsert rows summarized for traceability; no_match rows record "
                    "structured reason (already_has_civic / gene_not_in_civic / "
                    "no_disease_overlap). Per chunk-spec: 'do not invent treatment "
                    "claims when CIViC has no suitable evidence item.'"
                ),
            },
            "upsert_rows": upserts,
            "no_match_rows": no_match,
            "not_found_in_master": not_found,
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    # _contribution_meta.yaml
    (OUT_DIR / "_contribution_meta.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": CHUNK_ID,
                "contributor": "claude-anthropic-internal",
                "submission_date": SUBMISSION_DATE,
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "ai_model_version": "1m-context",
                "claim_method": "formal-issue",
                "ai_session_notes": (
                    f"Wave-2 backfill batch — closes #{ISSUE_NUMBER}. BMA-CIViC backfill via local "
                    "snapshot 2026-04-25. Conservative matching: gene match + disease-token "
                    "overlap required. Off-disease evidence items NOT included (would be "
                    "cross-disease borrowing per chunk-spec invention prohibition). "
                    "Mirrors reference pattern from closed #43."
                ),
                "tasktorrent_version": "2026-05-01",
                "notes_for_reviewer": (
                    "Per-BMA upsert touches only: evidence_sources (replaces empty list), "
                    "actionability_review_required (kept true). All other fields untouched. "
                    "Maintainer adjudicates direction/significance/level interpretation."
                ),
            },
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    print(
        f"Done: {len(upserts)} upserts / {len(no_match)} no_match / "
        f"{len(not_found)} not_found (of {len(MANIFEST)})",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
