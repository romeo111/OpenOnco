"""Wave-2 worker — bma-civic-backfill-wave2-2026-05-01-010 (issue #191).

Pattern mirrors the closed Wave-7 batch (issue #43, chunk
bma-civic-backfill-2026-04-29-001). For each BMA in the manifest:
  1. Load BMA yaml; derive gene from BMA-id (BMA-<GENE>-<VARIANT>-<DISEASE>).
  2. Look up CIViC snapshot 2026-04-25 evidence_items for (gene, disease)
     using disease-token substring overlap.
  3. If match → upsert sidecar with grouped evidence_sources block,
     preserving actionability_review_required: true.
  4. If no match → audit-report.yaml row with structured verdict.

Conservative matching: gene + disease-token-overlap required. Off-disease
items NOT included (cross-disease borrowing forbidden by chunk-spec).
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
BMA_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarker_actionability"
CIVIC_FILE = REPO_ROOT / "knowledge_base" / "hosted" / "civic" / "2026-04-25" / "evidence.yaml"
CHUNK_ID = "bma-civic-backfill-wave2-2026-05-01-010"
ISSUE_NUMBER = 191
OUT_DIR = REPO_ROOT / "contributions" / CHUNK_ID

MANIFEST = [
    "BMA-BCL2-REARRANGEMENT-MCL",
    "BMA-HER2-AMP-GASTRIC",
    "BMA-MLH1-SOMATIC-OVARIAN",
    "BMA-MSH6-SOMATIC-CRC",
    "BMA-PMS2-GERMLINE-UROTHELIAL",
]

# Disease-id → CIViC disease search tokens (lowercase substring).
# Limited to the 4 diseases this chunk's manifest references.
DISEASE_TOKENS: dict[str, tuple[str, ...]] = {
    "DIS-MCL": ("mantle cell lymphoma",),
    "DIS-GASTRIC": ("gastric", "stomach"),
    "DIS-OVARIAN": ("ovarian",),
    "DIS-CRC": ("colorectal", "colon cancer", "rectal cancer"),
    "DIS-UROTHELIAL": ("urothelial", "bladder"),
}


# Gene synonyms — BMA-id token → CIViC canonical gene symbol(s).
# CIViC uses HUGO symbols (ERBB2, not HER2). When a BMA encodes a familiar
# alias in its ID, the matcher must expand to the HUGO symbol the snapshot
# actually carries. Conservative: only well-established 1:1 aliases are
# included (HER2↔ERBB2, HER3↔ERBB3, HER4↔ERBB4 — same-locus protein
# nomenclature). Cross-paralog aliasing is NOT done.
GENE_SYNONYMS: dict[str, tuple[str, ...]] = {
    "HER2": ("ERBB2",),
    "HER3": ("ERBB3",),
    "HER4": ("ERBB4",),
}


def gene_from_bma_id(bma_id: str) -> str | None:
    """BMA-<GENE>-... → GENE."""
    parts = bma_id.split("-")
    if len(parts) < 2 or parts[0] != "BMA":
        return None
    return parts[1]


def gene_candidates(gene: str) -> tuple[str, ...]:
    """Return HUGO-canonical gene candidates for matching, including synonyms."""
    if not gene:
        return ()
    g = gene.upper()
    return (g,) + GENE_SYNONYMS.get(g, ())


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
    items: list[dict] = []
    seen_eids: set[str] = set()
    for cand in gene_candidates(gene):
        for it in civic_by_gene.get(cand, []):
            eid = it.get("id")
            if eid in seen_eids:
                continue
            seen_eids.add(eid)
            items.append(it)
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
    civic_by_gene = load_civic_index()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

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
                "current_eid_count": sum(
                    len(e.get("evidence_ids", []))
                    for e in existing
                    if isinstance(e, dict) and e.get("source") == "SRC-CIVIC"
                ),
            })
            continue

        if not matched:
            cands = gene_candidates(gene or "")
            any_in_civic = any(c in civic_by_gene for c in cands)
            verdict = (
                "gene_not_in_civic" if gene and not any_in_civic
                else "gene_in_civic_no_disease_overlap" if gene
                else "gene_unknown_in_bma_id"
            )
            gene_only_n = sum(len(civic_by_gene.get(c, [])) for c in cands)
            no_match.append({
                "bma_id": bma_id,
                "gene": gene,
                "gene_candidates": list(cands),
                "disease_id": bma.get("disease_id"),
                "verdict": verdict,
                "civic_gene_evidence_count_any_disease": gene_only_n,
            })
            continue

        new_sources = build_evidence_sources(matched)
        upsert = dict(bma)
        upsert["evidence_sources"] = new_sources
        upsert["actionability_review_required"] = True
        cands = gene_candidates(gene or "")
        synonym_note = (
            f" Gene synonyms expanded: {gene}→{','.join(cands)}."
            if len(cands) > 1 else ""
        )
        upsert["_contribution"] = {
            "chunk_id": CHUNK_ID,
            "contributor": "claude-anthropic-internal",
            "submission_date": "2026-05-01",
            "ai_tool": "claude-code",
            "ai_model": "claude-opus-4-7",
            "target_action": "upsert",
            "target_entity_id": bma_id,
            "notes_for_reviewer": (
                f"CIViC backfill (wave-2): gene={gene} matched {len(matched)} evidence "
                f"items in CIViC snapshot 2026-04-25 with disease overlap on "
                f"{bma.get('disease_id')}.{synonym_note} evidence_sources populated; "
                "no other fields modified. actionability_review_required: true "
                "preserved for maintainer adjudication."
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

    # task_manifest.txt
    manifest_lines = list(MANIFEST)
    if not_found:
        manifest_lines.append("")
        manifest_lines.append("# Not found in master:")
        manifest_lines.extend(f"# {b}" for b in not_found)
    (OUT_DIR / "task_manifest.txt").write_text(
        "\n".join(manifest_lines) + "\n", encoding="utf-8"
    )

    # audit-report.yaml — always include when there are no-match or already-has rows
    if no_match or not_found:
        (OUT_DIR / "audit-report.yaml").write_text(
            yaml.safe_dump({
                "_contribution": {
                    "chunk_id": CHUNK_ID,
                    "contributor": "claude-anthropic-internal",
                    "submission_date": "2026-05-01",
                    "ai_tool": "claude-code",
                    "ai_model": "claude-opus-4-7",
                    "notes_for_reviewer": (
                        "Report-only: BMAs in this chunk's manifest where CIViC backfill "
                        "produced no upsert (either no gene match, no disease overlap, or "
                        "BMA already has CIViC evidence). Per chunk-spec: 'do not invent "
                        "treatment claims when CIViC has no suitable evidence item.'"
                    ),
                },
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
                "submission_date": "2026-05-01",
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "ai_model_version": "1m-context",
                "ai_session_notes": (
                    f"Wave-2 batch — closes #{ISSUE_NUMBER}. BMA-CIViC backfill via local "
                    "snapshot 2026-04-25. Conservative matching: gene match + disease-token "
                    "overlap required. Off-disease evidence items NOT included (cross-disease "
                    "borrowing forbidden by chunk-spec). Mirrors closed wave-7 chunk pattern "
                    "(issue #43, contributions/bma-civic-backfill-2026-04-29-001/)."
                ),
                "tasktorrent_version": "2026-05-01",
                "claim_method": "formal-issue",
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
        f"\n{CHUNK_ID}: {len(upserts)} upsert / {len(no_match)} no-match / "
        f"{len(not_found)} not-found (of {len(MANIFEST)})",
        file=sys.stderr,
    )
    for u in upserts:
        print(f"  upsert: {u['bma_id']} gene={u['gene']} matches={u['matched_evidence_count']} blocks={u['evidence_sources_blocks']}", file=sys.stderr)
    for nm in no_match:
        print(f"  no-match: {nm['bma_id']} verdict={nm['verdict']} civic_gene_n={nm.get('civic_gene_evidence_count_any_disease', nm.get('current_eid_count', '?'))}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
