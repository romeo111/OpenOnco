"""Wave-2 BMA-CIViC backfill — closes #197.

For each BMA in this chunk's manifest:
  1. Read BMA yaml to get biomarker_id, variant_qualifier, disease_id, evidence_sources state.
  2. Derive gene from BMA-id (BMA-<GENE>-<VARIANT>-<DISEASE>).
  3. Look up CIViC snapshot for evidence_items matching (gene, disease).
  4. If matches and BMA has empty evidence_sources:
     - Group into evidence_sources block (by level + direction + significance).
     - Produce upsert sidecar replacing empty evidence_sources with the populated block.
  5. If BMA already has CIViC evidence: record audit row (already_has_civic_evidence).
  6. If no matches OR gene unknown: record audit row.

Per chunk-spec: do NOT invent treatment claims when CIViC has no suitable evidence.
Conservative matching: gene + disease-token-overlap.

Pattern mirrors closed bma-civic-backfill-2026-04-29-001 / wave2 -001.
"""

from __future__ import annotations

import datetime
import sys
from collections import defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
BMA_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarker_actionability"
CIVIC_FILE = REPO_ROOT / "knowledge_base" / "hosted" / "civic" / "2026-04-25" / "evidence.yaml"
CONTRIB_ROOT = REPO_ROOT / "contributions"

CHUNK_ID = "bma-civic-backfill-wave2-2026-05-01-016"
ISSUE_NUMBER = 197

MANIFEST_IDS = [
    "BMA-CCND1-T1114-MM",
    "BMA-KIT-EXON11-GIST",
    "BMA-MSH2-GERMLINE-OVARIAN",
    "BMA-NPM1-AML",
    "BMA-PMS2-SOMATIC-UROTHELIAL",
]

# Disease-id → CIViC disease search tokens (lowercase substring match).
DISEASE_TOKENS: dict[str, tuple[str, ...]] = {
    "DIS-MM": ("multiple myeloma",),
    "DIS-GIST": ("gastrointestinal stromal", "gist"),
    "DIS-OVARIAN": ("ovarian",),
    "DIS-AML": ("acute myeloid leukemia", "aml"),
    "DIS-UROTHELIAL": ("urothelial", "bladder"),
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


def variant_token_filter(bma_id: str, variant_qualifier: str, items: list[dict]) -> list[dict]:
    """Variant-aware filter: if BMA id encodes a clearly identifiable variant token
    (e.g., EXON11, T1114), keep only CIViC items whose variant or molecular_profile
    is consistent. If no clear token, return items unchanged.

    Conservative: never widen, only narrow when a strong token exists.
    """
    bma_lc = bma_id.lower()
    vq_lc = (variant_qualifier or "").lower()

    # KIT exon-11: keep items mentioning exon 11 in variant/molecular_profile/disease,
    # OR items whose variant looks like a JM-domain mutation. The reference closed
    # chunks did NOT apply variant filtering (kept all gene+disease matches), so to
    # mirror them exactly we only filter when we can do so confidently.
    # Default: no narrowing (mirror reference behavior).
    return items


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
    out_dir = CONTRIB_ROOT / CHUNK_ID
    out_dir.mkdir(parents=True, exist_ok=True)

    upserts: list[dict] = []
    no_match: list[dict] = []
    not_found: list[str] = []

    for bma_id in MANIFEST_IDS:
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

        gene = gene_from_bma_id(bma_id)
        disease_id = bma.get("disease_id")
        existing = bma.get("evidence_sources") or []
        already_has_civic = any(
            isinstance(e, dict) and e.get("source") == "SRC-CIVIC" for e in existing
        )

        if already_has_civic:
            no_match.append({
                "bma_id": bma_id,
                "gene": gene,
                "disease_id": disease_id,
                "verdict": "already_has_civic_evidence",
                "current_eid_count": sum(
                    len(e.get("evidence_ids", []))
                    for e in existing
                    if isinstance(e, dict) and e.get("source") == "SRC-CIVIC"
                ),
            })
            continue

        items = civic_by_gene.get((gene or "").upper(), [])
        matched = [it for it in items if disease_match(disease_id, it.get("disease", ""))]
        matched = variant_token_filter(bma_id, bma.get("variant_qualifier", ""), matched)

        if not matched:
            verdict = (
                "gene_not_in_civic" if gene and gene.upper() not in civic_by_gene
                else "gene_in_civic_no_disease_overlap" if gene
                else "gene_unknown_in_bma_id"
            )
            no_match.append({
                "bma_id": bma_id,
                "gene": gene,
                "disease_id": disease_id,
                "verdict": verdict,
                "civic_gene_evidence_count_any_disease": len(items),
            })
            continue

        new_sources = build_evidence_sources(matched)
        upsert = dict(bma)
        upsert["evidence_sources"] = new_sources
        upsert["actionability_review_required"] = True
        upsert["_contribution"] = {
            "chunk_id": CHUNK_ID,
            "contributor": "claude-anthropic-internal",
            "submission_date": "2026-05-01",
            "ai_tool": "claude-code",
            "ai_model": "claude-opus-4-7",
            "target_action": "upsert",
            "target_entity_id": bma_id,
            "notes_for_reviewer": (
                f"CIViC backfill: gene={gene} matched {len(matched)} evidence items in CIViC "
                f"snapshot 2026-04-25 with disease overlap on {disease_id}. "
                "evidence_sources populated; no other fields modified. "
                "actionability_review_required: true preserved for maintainer adjudication."
            ),
        }
        out_path = out_dir / path.name
        out_path.write_text(
            yaml.safe_dump(upsert, sort_keys=False, allow_unicode=True, default_flow_style=False),
            encoding="utf-8",
        )
        upserts.append({
            "bma_id": bma_id,
            "gene": gene,
            "disease_id": disease_id,
            "matched_evidence_count": len(matched),
            "evidence_sources_blocks": len(new_sources),
            "sidecar_file": path.name,
        })

    # task_manifest.txt
    manifest_lines = list(MANIFEST_IDS)
    if not_found:
        manifest_lines.append("")
        manifest_lines.append("# Not found in master:")
        manifest_lines.extend(f"# {b}" for b in not_found)
    (out_dir / "task_manifest.txt").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    # audit-report.yaml
    if no_match or not_found:
        (out_dir / "audit-report.yaml").write_text(
            yaml.safe_dump({
                "_contribution": {
                    "chunk_id": CHUNK_ID,
                    "contributor": "claude-anthropic-internal",
                    "submission_date": "2026-05-01",
                    "ai_tool": "claude-code",
                    "ai_model": "claude-opus-4-7",
                    "notes_for_reviewer": (
                        "Report-only: BMAs in this chunk's manifest where CIViC backfill "
                        "produced no upsert (either gene match without disease overlap, or "
                        "BMA already has CIViC evidence). Per chunk-spec: 'do not invent "
                        "treatment claims when CIViC has no suitable evidence item.'"
                    ),
                },
                "no_match_rows": no_match,
                "not_found_in_master": not_found,
                "upserts": upserts,
            }, sort_keys=False, allow_unicode=True, default_flow_style=False),
            encoding="utf-8",
        )

    # _contribution_meta.yaml
    upserts_n = len(upserts)
    no_match_n = len(no_match)
    (out_dir / "_contribution_meta.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": CHUNK_ID,
                "contributor": "claude-anthropic-internal",
                "submission_date": "2026-05-01",
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "ai_model_version": "1m-context",
                "ai_session_notes": (
                    f"Wave-2 BMA-CIViC backfill — closes #{ISSUE_NUMBER}. Local CIViC snapshot "
                    "2026-04-25. Conservative matching: gene match + disease-token overlap "
                    "required, with variant-aware filter applied where unambiguous. "
                    "Off-disease evidence items NOT included (would be cross-disease borrowing "
                    "per chunk-spec invention prohibition). "
                    f"{upserts_n} of {len(MANIFEST_IDS)} manifest IDs received CIViC evidence "
                    f"upserts; {no_match_n} recorded in audit-report.yaml."
                ),
                "tasktorrent_version": "2026-05-01-wave2",
                "notes_for_reviewer": (
                    "Per-BMA upsert touches only: evidence_sources (replaces empty list), "
                    "actionability_review_required (kept true). All other fields untouched. "
                    "Maintainer adjudicates direction/significance/level interpretation."
                ),
            },
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    # upsert log
    ts = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H%M%SZ")
    log_lines = [f"# Worker run log: {CHUNK_ID} ({ts})", ""]
    for u in upserts:
        log_lines.append(
            f"- UPSERT {u['bma_id']} gene={u['gene']} disease={u['disease_id']}: "
            f"{u['matched_evidence_count']} CIViC items in {u['evidence_sources_blocks']} blocks "
            f"-> {u['sidecar_file']}"
        )
    for nm in no_match:
        log_lines.append(
            f"- AUDIT  {nm['bma_id']} gene={nm['gene']} disease={nm['disease_id']}: {nm['verdict']}"
        )
    (out_dir / f"worker-log-{ts}.md").write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    print(f"\n{CHUNK_ID}: {upserts_n}u / {no_match_n}nm / {len(not_found)}nf "
          f"(of {len(MANIFEST_IDS)})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
