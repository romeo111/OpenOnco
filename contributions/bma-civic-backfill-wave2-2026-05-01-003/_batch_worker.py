"""Wave-2 batch worker — bma-civic-backfill-wave2-2026-05-01-003 (issue #184).

Mirrors the wave-1 worker (chunks #43+, ref `bma-civic-backfill-2026-04-29-001/_batch_worker.py`)
with one strengthening: per-BMA variant-aware filtering when the BMA's
variant_qualifier names a specific alteration that is mechanistically
distinct from CIViC items also matching gene+disease (issue #184 wording:
"Each proposed CIViC link is checked against disease context, biomarker
alteration, therapy, and evidence direction.").

For this manifest the only BMA that requires variant filtering is
BMA-PDGFRA-EXON12-GIST: CIViC's PDGFRA-GIST evidence is overwhelmingly for
exon 18 D842 codon variants (D842V/I/Y, I843DEL, D842_I843delinsVM), which
are imatinib-RESISTANT — attaching them to an imatinib-SENSITIVE
exon-12 BMA would invert the clinical message. We exclude those variants;
remaining gene+disease items, if any, attach.

For the other four BMAs (BCL2-CLL, EPCAM-CRC, MLH1-Gastric,
MSH2-Urothelial) the variant_qualifier matches CIViC's gene-level
phenotype (universal expression, dMMR/MSI-H pathway), and per-variant
filtering would over-prune. We follow wave-1's gene+disease overlap rule.

Per chunk-spec (issue #184 Quality Gate): do NOT invent treatment claims
when CIViC has no suitable evidence item.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
BMA_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarker_actionability"
CIVIC_FILE = REPO_ROOT / "knowledge_base" / "hosted" / "civic" / "2026-04-25" / "evidence.yaml"
CHUNK_ID = "bma-civic-backfill-wave2-2026-05-01-003"
ISSUE_NUMBER = 184
SUBMISSION_DATE = "2026-05-01"
OUT_DIR = REPO_ROOT / "contributions" / CHUNK_ID

MANIFEST = [
    "BMA-BCL2-EXPRESSION-CLL",
    "BMA-EPCAM-GERMLINE-CRC",
    "BMA-MLH1-GERMLINE-GASTRIC",
    "BMA-MSH2-SOMATIC-UROTHELIAL",
    "BMA-PDGFRA-EXON12-GIST",
]

# Disease-id → CIViC disease search tokens (lowercase substring match).
# Only the diseases present in this manifest are required.
DISEASE_TOKENS: dict[str, tuple[str, ...]] = {
    "DIS-CLL": ("chronic lymphocytic leukemia", "lymphocytic leukemia", "cll"),
    "DIS-CRC": ("colorectal", "colon cancer", "rectal cancer"),
    "DIS-GASTRIC": ("gastric", "stomach"),
    "DIS-UROTHELIAL": ("urothelial", "bladder", "transitional cell"),
    "DIS-GIST": ("gastrointestinal stromal", "gist"),
}

# Per-BMA variant exclusion. Items in CIViC whose variant string matches
# any listed substring (lowercase) are excluded from the upsert. Used when
# the BMA's variant_qualifier names a mechanistically distinct alteration
# from the dominant CIViC variants for the gene+disease.
PER_BMA_EXCLUDE_VARIANTS: dict[str, tuple[str, ...]] = {
    # PDGFRA exon-12 in GIST: exclude exon-18 D842/I843 variants which are
    # imatinib-resistant. Exon 12 itself is V561D + neighbours; keep CIViC
    # items only if they don't match the exon-18 codon set.
    "BMA-PDGFRA-EXON12-GIST": (
        "d842",        # D842V, D842I, D842Y, D842_I843delinsVM
        "i843",        # I843DEL, I843_S847del
        "exon 18",     # any explicit exon-18 mutation tags
    ),
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


def find_matching_evidence(bma: dict, civic_by_gene: dict[str, list[dict]]) -> tuple[str | None, list[dict], list[dict]]:
    """Returns (gene, kept_items, excluded_items_due_to_variant)."""
    bma_id = bma.get("id") or ""
    gene = gene_from_bma_id(bma_id)
    disease_id = bma.get("disease_id")
    if not gene or not disease_id:
        return gene, [], []
    items = civic_by_gene.get(gene.upper(), [])
    matched = [it for it in items if disease_match(disease_id, it.get("disease", ""))]
    excludes = PER_BMA_EXCLUDE_VARIANTS.get(bma_id, ())
    if not excludes:
        return gene, matched, []
    kept: list[dict] = []
    skipped: list[dict] = []
    for it in matched:
        v = (it.get("variant") or "").lower()
        if any(tok in v for tok in excludes):
            skipped.append(it)
        else:
            kept.append(it)
    return gene, kept, skipped


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
        gene, matched, variant_skipped = find_matching_evidence(bma, civic_by_gene)

        if already_has_civic:
            no_match.append({
                "bma_id": bma_id,
                "gene": gene,
                "disease_id": bma.get("disease_id"),
                "verdict": "already_has_civic_evidence",
                "current_eid_count": sum(len(e.get("evidence_ids", []))
                                          for e in existing
                                          if isinstance(e, dict) and e.get("source") == "SRC-CIVIC"),
            })
            continue

        if not matched:
            gene_only_n = len(civic_by_gene.get((gene or "").upper(), []))
            if variant_skipped:
                verdict = "gene_disease_match_but_variant_mismatch"
            elif gene and gene.upper() not in civic_by_gene:
                verdict = "gene_not_in_civic"
            elif gene:
                verdict = "gene_in_civic_no_disease_overlap"
            else:
                verdict = "gene_unknown_in_bma_id"
            # Surface the gene-only CIViC items so reviewers can audit why
            # they were rejected (predisposition vs. tumor evidence,
            # off-disease, etc.).
            gene_items = civic_by_gene.get((gene or "").upper(), [])
            row = {
                "bma_id": bma_id,
                "gene": gene,
                "disease_id": bma.get("disease_id"),
                "variant_qualifier": bma.get("variant_qualifier"),
                "verdict": verdict,
                "civic_gene_evidence_count_any_disease": gene_only_n,
                "civic_gene_items_summary": [
                    {
                        "eid": f"EID{it.get('id')}",
                        "variant": it.get("variant"),
                        "disease": it.get("disease"),
                        "evidence_type": it.get("evidence_type"),
                        "direction": it.get("evidence_direction"),
                        "significance": it.get("significance"),
                    }
                    for it in gene_items[:10]
                ],
            }
            if variant_skipped:
                row["variant_filtered_count"] = len(variant_skipped)
                row["filter_rationale"] = (
                    "BMA variant_qualifier names a specific alteration "
                    "(exon 12); CIViC gene+disease items match a "
                    "mechanistically distinct alteration (exon 18 D842 codon, "
                    "imatinib-resistant). Cross-attaching would invert "
                    "the clinical message. See _batch_worker.py "
                    "PER_BMA_EXCLUDE_VARIANTS."
                )
                row["civic_skipped_variants"] = sorted({
                    f"{it.get('variant')} (EID{it.get('id')})" for it in variant_skipped
                })
            no_match.append(row)
            continue

        new_sources = build_evidence_sources(matched)
        upsert = dict(bma)
        upsert["evidence_sources"] = new_sources
        upsert["actionability_review_required"] = True
        notes = (
            f"CIViC backfill: gene={gene} matched {len(matched)} evidence items in CIViC "
            f"snapshot 2026-04-25 with disease overlap on {bma.get('disease_id')}. "
            "evidence_sources populated; no other fields modified. "
            "actionability_review_required: true preserved for maintainer adjudication."
        )
        if variant_skipped:
            notes += (
                f" Variant-aware filter excluded {len(variant_skipped)} CIViC items whose "
                "variant string conflicted with this BMA's variant_qualifier "
                "(see audit-report.yaml in chunk dir for filter rationale)."
            )
        upsert["_contribution"] = {
            "chunk_id": CHUNK_ID,
            "contributor": "claude-anthropic-internal",
            "submission_date": SUBMISSION_DATE,
            "ai_tool": "claude-code",
            "ai_model": "claude-opus-4-7",
            "target_action": "upsert",
            "target_entity_id": bma_id,
            "notes_for_reviewer": notes,
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
            "variant_filtered_excluded": len(variant_skipped),
        })

    # task_manifest.txt — exactly the manifest IDs (per Output Requirements)
    (OUT_DIR / "task_manifest.txt").write_text(
        "\n".join(MANIFEST) + "\n", encoding="utf-8"
    )

    # audit-report.yaml — always include (issue requires "one outcome per manifest ID")
    audit_payload = {
        "_contribution": {
            "chunk_id": CHUNK_ID,
            "contributor": "claude-anthropic-internal",
            "submission_date": SUBMISSION_DATE,
            "ai_tool": "claude-code",
            "ai_model": "claude-opus-4-7",
            "notes_for_reviewer": (
                f"Per-manifest outcome record for chunk #{ISSUE_NUMBER}. "
                "BMAs producing an upsert sidecar appear in 'upserts'. "
                "BMAs without a sidecar (no gene/disease/variant match, or "
                "already-has-civic-evidence) appear in 'no_match_rows' with a "
                "structured verdict. Per chunk-spec: 'do not invent treatment "
                "claims when CIViC has no suitable evidence item.'"
            ),
        },
        "upserts": upserts,
        "no_match_rows": no_match,
        "not_found_in_master": not_found,
    }
    (OUT_DIR / "audit-report.yaml").write_text(
        yaml.safe_dump(audit_payload, sort_keys=False, allow_unicode=True, default_flow_style=False),
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
                "ai_session_notes": (
                    f"Wave-2 batch — closes #{ISSUE_NUMBER}. BMA-CIViC backfill via local "
                    "snapshot 2026-04-25. Conservative matching: gene match + disease-token "
                    "overlap required. Off-disease evidence items NOT included. "
                    "Variant-aware filter applied when BMA variant_qualifier is "
                    "mechanistically distinct from CIViC's dominant gene+disease "
                    "variants (BMA-PDGFRA-EXON12-GIST: exon-18 D842/I843 items "
                    "excluded as imatinib-resistant)."
                ),
                "tasktorrent_version": "2026-04-29-pending-first-commit",
                "notes_for_reviewer": (
                    "Per-BMA upsert touches only: evidence_sources (replaces empty list), "
                    "actionability_review_required (kept true). All other fields untouched. "
                    "Maintainer adjudicates direction/significance/level interpretation. "
                    "audit-report.yaml records one outcome per manifest ID."
                ),
            },
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    print(f"\n#{ISSUE_NUMBER} {CHUNK_ID}: {len(upserts)}u / {len(no_match)}nm / "
          f"{len(not_found)}nf (of {len(MANIFEST)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
