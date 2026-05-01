"""Wave-2 batch worker — bma-civic-backfill-wave2-2026-05-01-013 (closes #194).

Pattern mirrors closed `bma-civic-backfill-2026-04-29-001` (#43): for each
BMA in the chunk manifest, emit either an upsert sidecar with CIViC-derived
evidence_sources, or an audit-row with a structured `verdict`.

Conservative matching: gene-from-BMA-id + disease-token-overlap. Off-disease
or off-gene CIViC items are NOT included (would be cross-disease borrowing
per chunk-spec invention prohibition). HRD-status / panel biomarkers whose
BMA-id token is not a CIViC gene fall through to `gene_not_in_civic` —
intentional; promoting BRCA1/2 evidence into an HRD-status BMA would be
fabrication out of scope for this chunk.

Variant-aware filter: variant_qualifier strings are recorded in audit rows
but are NOT used to subset evidence items here — the maintainer adjudicates
which CIViC variants apply. Synonym expansion is limited to disease tokens
(see DISEASE_TOKENS); gene synonyms are out of scope for wave-2.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
BMA_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarker_actionability"
CIVIC_FILE = REPO_ROOT / "knowledge_base" / "hosted" / "civic" / "2026-04-25" / "evidence.yaml"
CONTRIB_ROOT = REPO_ROOT / "contributions"
CHUNK_ID = "bma-civic-backfill-wave2-2026-05-01-013"
ISSUE_NUMBER = 194
SUBMISSION_DATE = "2026-05-01"

MANIFEST = [
    "BMA-CCND1-IHC-MCL",
    "BMA-HRD-STATUS-PDAC",
    "BMA-MSH2-GERMLINE-CRC",
    "BMA-MSH6-SOMATIC-OVARIAN",
    "BMA-PMS2-SOMATIC-GASTRIC",
]

# Disease-id → CIViC disease search tokens (lowercase substring match).
DISEASE_TOKENS: dict[str, tuple[str, ...]] = {
    "DIS-MCL": ("mantle cell lymphoma",),
    "DIS-PDAC": ("pancreatic ductal", "pancreatic adenocarcinoma", "pancreatic cancer"),
    "DIS-CRC": ("colorectal", "colon cancer", "rectal cancer"),
    "DIS-OVARIAN": ("ovarian",),
    "DIS-GASTRIC": ("gastric", "stomach"),
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
    print(f"  Indexed {len(items)} CIViC items across {len(by_gene)} genes.", file=sys.stderr)
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
            it_key = (
                it.get("evidence_level") or "X",
                it.get("evidence_direction") or "Unknown",
                it.get("significance") or "Unknown",
            )
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
    out.sort(key=lambda e: (level_order.get(e["level"], 9), e["direction"], e["significance"]))
    return out


def main() -> int:
    civic_by_gene = load_civic_index()
    out_dir = CONTRIB_ROOT / CHUNK_ID
    out_dir.mkdir(parents=True, exist_ok=True)

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
                "variant_qualifier": bma.get("variant_qualifier"),
                "verdict": "already_has_civic_evidence",
                "current_eid_count": sum(
                    len(e.get("evidence_ids", []))
                    for e in existing
                    if isinstance(e, dict) and e.get("source") == "SRC-CIVIC"
                ),
                "no_civic_match_reason": (
                    "Hosted BMA already carries SRC-CIVIC evidence_sources from a "
                    "prior backfill wave. Wave-2 does not redo prior linkage; "
                    "maintainer adjudicates if EID set needs refresh."
                ),
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
                    f"CIViC snapshot 2026-04-25 has zero evidence_items with "
                    f"gene='{gene}'. Token derived from BMA-id; for panel/composite "
                    "biomarkers (HRD-status, dMMR-IHC, etc.) the BMA-id token is not "
                    "a single CIViC gene. Promoting BRCA1/BRCA2/component-gene "
                    "evidence into a panel BMA is out of scope for this chunk per "
                    "issue 194 'no invented treatment claims' rule."
                ),
                "gene_in_civic_no_disease_overlap": (
                    f"CIViC snapshot 2026-04-25 has {gene_only_n} evidence_items "
                    f"with gene='{gene}' but none with disease overlap on "
                    f"{bma.get('disease_id')} (token set: "
                    f"{list(DISEASE_TOKENS.get(bma.get('disease_id'), ()))}). "
                    "Cross-disease evidence not borrowed."
                ),
                "gene_unknown_in_bma_id": (
                    "Could not derive a gene token from BMA-id. Manual review "
                    "needed to identify CIViC gene mapping."
                ),
            }[verdict]
            no_match.append({
                "bma_id": bma_id,
                "gene": gene,
                "disease_id": bma.get("disease_id"),
                "variant_qualifier": bma.get("variant_qualifier"),
                "verdict": verdict,
                "civic_gene_evidence_count_any_disease": gene_only_n,
                "no_civic_match_reason": reason_text,
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
                f"CIViC backfill (wave-2): gene={gene} matched {len(matched)} "
                f"evidence items in CIViC snapshot 2026-04-25 with disease overlap "
                f"on {bma.get('disease_id')}. evidence_sources populated; no other "
                "fields modified. actionability_review_required: true preserved."
            ),
        }
        out_path = out_dir / path.name
        out_path.write_text(
            yaml.safe_dump(upsert, sort_keys=False, allow_unicode=True, default_flow_style=False),
            encoding="utf-8",
        )
        upserts.append({
            "bma_id": bma_id, "gene": gene, "disease_id": bma.get("disease_id"),
            "matched_evidence_count": len(matched),
            "evidence_sources_blocks": len(new_sources),
        })

    # task_manifest.txt
    manifest_lines = list(MANIFEST)
    if not_found:
        manifest_lines.append("")
        manifest_lines.append("# Not found in master:")
        manifest_lines.extend(f"# {b}" for b in not_found)
    (out_dir / "task_manifest.txt").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    # audit-report.yaml
    (out_dir / "audit-report.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": CHUNK_ID,
                "contributor": "claude-anthropic-internal",
                "submission_date": SUBMISSION_DATE,
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "notes_for_reviewer": (
                    "Report-only: BMAs in this chunk's manifest where CIViC "
                    "backfill produced no upsert (gene not in CIViC, no disease "
                    "overlap, or BMA already has CIViC evidence). Per chunk-spec: "
                    "'do not invent treatment claims when CIViC has no suitable "
                    "evidence item.'"
                ),
            },
            "no_match_rows": no_match,
            "not_found_in_master": not_found,
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    # _contribution_meta.yaml
    (out_dir / "_contribution_meta.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": CHUNK_ID,
                "contributor": "claude-anthropic-internal",
                "submission_date": SUBMISSION_DATE,
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "ai_model_version": "1m-context",
                "ai_session_notes": (
                    f"Wave-2 batch — closes #{ISSUE_NUMBER}. BMA-CIViC backfill "
                    "via local snapshot 2026-04-25. Conservative matching: gene "
                    "match + disease-token overlap required. Off-disease evidence "
                    "items NOT included (cross-disease borrowing prohibited). "
                    "Panel/composite-biomarker IDs (HRD-status, dMMR-IHC) whose "
                    "BMA-id token is not a CIViC gene fall through to "
                    "gene_not_in_civic — promoting component-gene evidence into a "
                    "panel BMA is fabrication out of scope for this chunk."
                ),
                "tasktorrent_version": "2026-04-29-pending-first-commit",
                "notes_for_reviewer": (
                    "Per-BMA upsert touches only: evidence_sources (replaces "
                    "empty list) and actionability_review_required (kept true). "
                    "All other fields untouched. Maintainer adjudicates "
                    "direction/significance/level interpretation."
                ),
            },
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    summary = {
        "chunk_id": CHUNK_ID,
        "issue_number": ISSUE_NUMBER,
        "bma_count": len(MANIFEST),
        "upserts": len(upserts),
        "no_match": len(no_match),
        "not_found": len(not_found),
    }
    print(f"\nSummary: {summary}")
    for u in upserts:
        print(f"  UPSERT {u['bma_id']}: gene={u['gene']} matched={u['matched_evidence_count']}")
    for nm in no_match:
        print(f"  NO_MATCH {nm['bma_id']}: verdict={nm['verdict']}")
    for nf in not_found:
        print(f"  NOT_FOUND {nf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
