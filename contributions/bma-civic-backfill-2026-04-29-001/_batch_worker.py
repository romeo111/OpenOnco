"""Wave 7 batch worker — bma-civic-backfill chunks #43-#63 (21 chunks × ~5 BMAs each).

For each BMA in each chunk's manifest:
  1. Read BMA yaml to get biomarker_id, variant_qualifier, disease_id, evidence_sources state.
  2. Derive gene from BMA-id (BMA-<GENE>-<VARIANT>-<DISEASE>).
  3. Look up CIViC snapshot for evidence_items matching (gene, disease).
  4. If matches:
     - Group into evidence_sources block (by level + direction + significance).
     - Produce upsert sidecar replacing empty evidence_sources with the populated block.
  5. If no matches OR gene unknown:
     - Produce no-match report row in audit-report.yaml.

Per chunk-spec: do NOT invent treatment claims when CIViC has no suitable evidence.

Conservative matching: requires gene + disease-token-overlap. Off-disease
CIViC items for matching gene are NOT included (they'd be cross-disease
borrowing, which is the kind of "invention" the spec forbids).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
BMA_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "biomarker_actionability"
CIVIC_FILE = REPO_ROOT / "knowledge_base" / "hosted" / "civic" / "2026-04-25" / "evidence.yaml"
CONTRIB_ROOT = REPO_ROOT / "contributions"
MANIFESTS_FILE = "/tmp/bma_civic_manifests.json"


# Disease-id → CIViC disease search tokens (lowercase substring match).
# Conservative: a CIViC disease string must contain ANY listed token.
DISEASE_TOKENS: dict[str, tuple[str, ...]] = {
    "DIS-CLL": ("chronic lymphocytic leukemia", "lymphocytic leukemia", "cll"),
    "DIS-DLBCL-NOS": ("diffuse large b-cell", "dlbcl"),
    "DIS-FL": ("follicular lymphoma",),
    "DIS-MCL": ("mantle cell lymphoma",),
    "DIS-MZL": ("marginal zone lymphoma",),
    "DIS-NODAL-MZL": ("marginal zone lymphoma",),
    "DIS-SPLENIC-MZL": ("marginal zone lymphoma",),
    "DIS-BURKITT": ("burkitt lymphoma",),
    "DIS-CHL": ("hodgkin lymphoma", "classical hodgkin"),
    "DIS-NLPBL": ("hodgkin", "nodular lymphocyte"),
    "DIS-WM": ("waldenstrom", "lymphoplasmacytic"),
    "DIS-AITL": ("angioimmunoblastic", "ptcl"),
    "DIS-ALCL": ("anaplastic large cell"),
    "DIS-PTCL-NOS": ("peripheral t-cell", "ptcl"),
    "DIS-T-ALL": ("t-cell acute lymphoblastic", "t-all", "t lymphoblastic"),
    "DIS-B-ALL": ("b-cell acute lymphoblastic", "b-all", "b lymphoblastic"),
    "DIS-AML": ("acute myeloid leukemia", "aml"),
    "DIS-APL": ("acute promyelocytic", "apl"),
    "DIS-MM": ("multiple myeloma",),
    "DIS-CML": ("chronic myeloid leukemia", "cml"),
    "DIS-MDS-HR": ("myelodysplastic syndromes", "mds"),
    "DIS-MDS-LR": ("myelodysplastic syndromes", "mds"),
    "DIS-PMF": ("primary myelofibrosis", "myelofibrosis"),
    "DIS-PV": ("polycythemia vera",),
    "DIS-ET": ("essential thrombocythemia",),
    "DIS-NSCLC": ("non-small cell lung", "nsclc", "lung adenocarcinoma", "lung squamous"),
    "DIS-SCLC": ("small cell lung",),
    "DIS-BREAST": ("breast cancer", "breast carcinoma"),
    "DIS-COLORECTAL": ("colorectal", "colon cancer", "rectal cancer"),
    "DIS-CRC": ("colorectal", "colon cancer", "rectal cancer"),
    "DIS-GASTRIC": ("gastric", "stomach"),
    "DIS-ESOPHAGEAL": ("esophageal",),
    "DIS-PANCREATIC": ("pancreatic",),
    "DIS-PDAC": ("pancreatic ductal", "pancreatic adenocarcinoma"),
    "DIS-HCC": ("hepatocellular",),
    "DIS-CHOLANGIOCARCINOMA": ("cholangiocarcinoma", "biliary tract"),
    "DIS-OVARIAN": ("ovarian",),
    "DIS-CERVICAL": ("cervical",),
    "DIS-ENDOMETRIAL": ("endometrial",),
    "DIS-PROSTATE": ("prostate",),
    "DIS-UROTHELIAL": ("urothelial", "bladder"),
    "DIS-RCC": ("renal cell", "kidney"),
    "DIS-MELANOMA": ("melanoma",),
    "DIS-GBM": ("glioblastoma",),
    "DIS-GLIOMA-LOW-GRADE": ("glioma", "astrocytoma", "oligodendroglioma"),
    "DIS-HNSCC": ("head and neck", "squamous cell carcinoma"),
    "DIS-THYROID-PAPILLARY": ("papillary thyroid",),
    "DIS-THYROID-ANAPLASTIC": ("anaplastic thyroid",),
    "DIS-MTC": ("medullary thyroid",),
    "DIS-GIST": ("gastrointestinal stromal", "gist"),
    "DIS-SARCOMA-STS": ("soft tissue sarcoma", "sarcoma"),
    "DIS-CHONDROSARCOMA": ("chondrosarcoma",),
    "DIS-IMT": ("inflammatory myofibroblastic",),
    "DIS-MPNST": ("malignant peripheral nerve",),
    "DIS-IFS": ("infantile fibrosarcoma",),
    "DIS-SALIVARY": ("salivary gland",),
    "DIS-MASTOCYTOSIS": ("mastocytosis",),
    "DIS-MF-SEZARY": ("mycosis fungoides", "sezary"),
    "DIS-NK-T-NASAL": ("nk/t-cell", "natural killer t-cell"),
    "DIS-EATL": ("enteropathy",),
    "DIS-HSTCL": ("hepatosplenic",),
    "DIS-PMBCL": ("primary mediastinal", "mediastinal large b-cell"),
    "DIS-PCNSL": ("primary cns", "central nervous system lymphoma"),
    "DIS-PTLD": ("post-transplant lymphoproliferative", "ptld"),
    "DIS-HCV-MZL": ("marginal zone",),
    "DIS-T-PLL": ("t-cell prolymphocytic", "t-pll"),
    "DIS-HCL": ("hairy cell",),
    "DIS-ATLL": ("adult t-cell", "atll"),
    "DIS-HGBL-DH": ("high-grade b-cell", "high grade b-cell"),
}


def gene_from_bma_id(bma_id: str) -> str | None:
    """BMA-<GENE>-... → GENE. Cope with multi-word gene tokens (BCRABL etc.)"""
    parts = bma_id.split("-")
    if len(parts) < 2 or parts[0] != "BMA":
        return None
    return parts[1]


def disease_from_bma_yaml(data: dict) -> str | None:
    return data.get("disease_id")


def disease_match(disease_id: str, civic_disease: str) -> bool:
    if not isinstance(civic_disease, str) or not disease_id:
        return False
    cd_lc = civic_disease.lower()
    tokens = DISEASE_TOKENS.get(disease_id, ())
    if tokens:
        return any(tok in cd_lc for tok in tokens)
    # Fallback: try exact-substring of stripped DIS-id
    stem = disease_id.replace("DIS-", "").replace("-", " ").lower()
    return stem in cd_lc


def load_civic_index() -> dict[str, list[dict]]:
    """gene → list of evidence_items."""
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
    """Returns (gene, matching_items). gene is uppercase if found else None."""
    bma_id = bma.get("id") or ""
    gene = gene_from_bma_id(bma_id)
    disease_id = bma.get("disease_id")
    if not gene or not disease_id:
        return gene, []
    items = civic_by_gene.get(gene.upper(), [])
    matched = [it for it in items if disease_match(disease_id, it.get("disease", ""))]
    return gene, matched


def build_evidence_sources(matched: list[dict]) -> list[dict]:
    """Group matched CIViC items into evidence_sources block by (level, direction, significance)."""
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

    # Build note for each bucket: list distinct therapies + brief
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
    # Stable sort: A→B→C→D→E→X
    level_order = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "X": 5}
    out.sort(key=lambda e: (level_order.get(e["level"], 9),
                            e["direction"], e["significance"]))
    return out


def process_chunk(chunk_id: str, bma_ids: list[str], issue_number: int,
                  civic_by_gene: dict[str, list[dict]]) -> dict:
    out_dir = CONTRIB_ROOT / chunk_id
    out_dir.mkdir(parents=True, exist_ok=True)

    upserts: list[dict] = []
    no_match: list[dict] = []
    not_found: list[str] = []

    for bma_id in bma_ids:
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

        # If BMA already has CIViC evidence_sources, skip (don't redo civic-bma-reconstruct work).
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
            # Count gene-only candidates for transparency
            gene_only_n = len(civic_by_gene.get((gene or "").upper(), []))
            no_match.append({
                "bma_id": bma_id,
                "gene": gene,
                "disease_id": bma.get("disease_id"),
                "verdict": verdict,
                "civic_gene_evidence_count_any_disease": gene_only_n,
            })
            continue

        # Build upsert: replace empty evidence_sources with populated block
        new_sources = build_evidence_sources(matched)
        upsert = dict(bma)
        upsert["evidence_sources"] = new_sources
        # Keep actionability_review_required: true so maintainer reviews
        upsert["actionability_review_required"] = True
        upsert["_contribution"] = {
            "chunk_id": chunk_id,
            "contributor": "claude-anthropic-internal",
            "submission_date": "2026-04-29",
            "ai_tool": "claude-code",
            "ai_model": "claude-opus-4-7",
            "target_action": "upsert",
            "target_entity_id": bma_id,
            "notes_for_reviewer": (
                f"CIViC backfill: gene={gene} matched {len(matched)} evidence items in CIViC "
                f"snapshot 2026-04-25 with disease overlap on {bma.get('disease_id')}. "
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
            "bma_id": bma_id, "gene": gene, "disease_id": bma.get("disease_id"),
            "matched_evidence_count": len(matched),
            "evidence_sources_blocks": len(new_sources),
        })

    # task_manifest.txt — per chunk-spec, must list all manifest entries
    manifest_lines = list(bma_ids)
    if not_found:
        manifest_lines.append("")
        manifest_lines.append("# Not found in master:")
        manifest_lines.extend(f"# {b}" for b in not_found)
    (out_dir / "task_manifest.txt").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    # audit-report.yaml — for chunks where some BMAs are no-match (always include)
    if no_match or not_found:
        (out_dir / "audit-report.yaml").write_text(
            yaml.safe_dump({
                "_contribution": {
                    "chunk_id": chunk_id,
                    "contributor": "claude-anthropic-internal",
                    "submission_date": "2026-04-29",
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
    (out_dir / "_contribution_meta.yaml").write_text(
        yaml.safe_dump({
            "_contribution": {
                "chunk_id": chunk_id,
                "contributor": "claude-anthropic-internal",
                "submission_date": "2026-04-29",
                "ai_tool": "claude-code",
                "ai_model": "claude-opus-4-7",
                "ai_model_version": "1m-context",
                "ai_session_notes": (
                    f"Wave 7 batch — closes #{issue_number}. BMA-CIViC backfill via local "
                    "snapshot 2026-04-25. Conservative matching: gene match + disease-token "
                    "overlap required. Off-disease evidence items NOT included (would be "
                    "cross-disease borrowing per chunk-spec invention prohibition)."
                ),
                "tasktorrent_version": "2026-04-29-pending-first-commit",
                "notes_for_reviewer": (
                    "Per-BMA upsert touches only: evidence_sources (replaces empty list), "
                    "actionability_review_required (kept true). All other fields untouched. "
                    "Maintainer adjudicates direction/significance/level interpretation."
                ),
            },
        }, sort_keys=False, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )

    return {
        "chunk_id": chunk_id, "issue_number": issue_number,
        "bma_count": len(bma_ids),
        "upserts": len(upserts),
        "no_match": len(no_match),
        "not_found": len(not_found),
    }


def main() -> int:
    civic_by_gene = load_civic_index()
    with open(MANIFESTS_FILE, encoding="utf-8") as f:
        manifests = json.load(f)
    summaries = []
    for issue_num_str in sorted(manifests.keys(), key=int):
        n = int(issue_num_str)
        chunk_id, bmas = manifests[issue_num_str]
        s = process_chunk(chunk_id, bmas, n, civic_by_gene)
        summaries.append(s)
        print(f"  #{n} {chunk_id}: {s['upserts']}u / {s['no_match']}nm / "
              f"{s['not_found']}nf (of {s['bma_count']})", file=sys.stderr)
    total = {
        "total_chunks": len(summaries),
        "total_upserts": sum(s["upserts"] for s in summaries),
        "total_no_match": sum(s["no_match"] for s in summaries),
        "total_not_found": sum(s["not_found"] for s in summaries),
    }
    print(f"\nBatch done: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
