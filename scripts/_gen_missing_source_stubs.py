"""One-shot stub generator for missing Source entities.

Walks every yaml under knowledge_base/hosted/content/, finds every SRC-*
identifier that does NOT have a corresponding Source entity, and writes a
placeholder yaml under knowledge_base/hosted/content/sources/ for each.

Stubs are tagged with `review_status: pending_clinical_signoff` and
`drafted_by: claude_extraction` so reviewers can find them. Filename
convention: lowercase id with hyphens preserved + `.yaml`.

Run once per branch when wiring new biomarker / trial / guideline citations.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

CONTENT = Path(__file__).resolve().parents[1] / "knowledge_base" / "hosted" / "content"
SOURCES = CONTENT / "sources"

ID_PATTERN = re.compile(r"^SRC-[A-Z0-9][A-Z0-9-]*$")
PROSE_PATTERN = re.compile(r"SRC-[A-Z0-9][A-Z0-9-]*")

# Known trial-flavored IDs (named trials whose ID does NOT carry NCT)
TRIAL_IDS: set[str] = {
    "SRC-ARROW", "SRC-B2222-DEMETRI", "SRC-CALGB-10801", "SRC-EORTC-62005",
    "SRC-EXPLORER", "SRC-FIGHT", "SRC-FIGHT-202", "SRC-FIGHT-207",
    "SRC-FOENIX-CCA2", "SRC-FORTITUDE-101", "SRC-GEOMETRY-MONO-1",
    "SRC-INVICTUS", "SRC-LIBRETTO-001", "SRC-LIBRETTO-431", "SRC-LIBRETTO-531",
    "SRC-NAVIGATE", "SRC-NAVIGATOR", "SRC-PAPMET", "SRC-PATHFINDER",
    "SRC-SAVOIR", "SRC-SCOUT", "SRC-SSG-XVIII", "SRC-STARTRK-2",
    "SRC-VISION", "SRC-VOYAGER",
}
PUB_IDS: set[str] = {"SRC-CARVAJAL-2013", "SRC-HODI-2013"}
# Cooperative groups / consortia — neither a single trial nor a single
# guideline; flag for human classification.
CONSORTIA: set[str] = {"SRC-COG", "SRC-NF1-CONSORTIUM"}

# Lightweight title hints — no inventing PMIDs/NCTs/DOIs. Only encodes
# what the ID literally tells us (trial name, year, society).
TITLE_HINTS: dict[str, str] = {
    "SRC-ARROW": "ARROW — pralsetinib in RET-altered solid tumors (TODO: confirm citation)",
    "SRC-ASCO-BTC-2023": "ASCO biliary tract cancer guideline (2023) (TODO: confirm citation)",
    "SRC-ATA-ATC-2021": "ATA anaplastic thyroid cancer guideline (2021) (TODO: confirm citation)",
    "SRC-ATA-THYROID-2015": "ATA differentiated thyroid cancer guideline (2015) (TODO: confirm citation)",
    "SRC-B2222-DEMETRI": "B2222 — imatinib in advanced GIST (Demetri et al.) (TODO: confirm citation)",
    "SRC-CALGB-10801": "CALGB 10801 — KIT-mutant AML (TODO: confirm citation)",
    "SRC-CARVAJAL-2013": "Carvajal et al. 2013 (TODO: confirm citation)",
    "SRC-COG": "Children's Oncology Group (TODO: confirm specific protocol/guideline)",
    "SRC-EANO-LGG-2024": "EANO low-grade glioma guideline (2024) (TODO: confirm citation)",
    "SRC-EASL-HBV-2025": "EASL hepatitis B guideline (2025) (TODO: confirm citation)",
    "SRC-EORTC-62005": "EORTC 62005 — adjuvant imatinib in GIST (TODO: confirm citation)",
    "SRC-ESMO-BONE-SARCOMA": "ESMO bone sarcoma guideline (TODO: confirm year/citation)",
    "SRC-ESMO-BTC-2023": "ESMO biliary tract cancer guideline (2023) (TODO: confirm citation)",
    "SRC-ESMO-CRC-2024": "ESMO colorectal cancer guideline (2024) (TODO: confirm citation)",
    "SRC-ESMO-HNSCC-2020": "ESMO head-and-neck SCC guideline (2020) (TODO: confirm citation)",
    "SRC-ESMO-SALIVARY": "ESMO salivary gland cancer guideline (TODO: confirm year/citation)",
    "SRC-ESMO-SARCOMA": "ESMO soft-tissue sarcoma guideline (TODO: confirm year/citation)",
    "SRC-ESMO-SARCOMA-2024": "ESMO soft-tissue sarcoma guideline (2024) (TODO: confirm citation)",
    "SRC-EXPLORER": "EXPLORER — avapritinib in advanced systemic mastocytosis (TODO: confirm citation)",
    "SRC-FIGHT": "FIGHT — bemarituzumab in FGFR2b+ gastric cancer (TODO: confirm phase/citation)",
    "SRC-FIGHT-202": "FIGHT-202 — pemigatinib in FGFR2-fusion cholangiocarcinoma (TODO: confirm citation)",
    "SRC-FIGHT-207": "FIGHT-207 — pemigatinib in FGFR-altered solid tumors (TODO: confirm citation)",
    "SRC-FOENIX-CCA2": "FOENIX-CCA2 — futibatinib in FGFR2-fusion cholangiocarcinoma (TODO: confirm citation)",
    "SRC-FORTITUDE-101": "FORTITUDE-101 — bemarituzumab in FGFR2b+ gastric (TODO: confirm citation)",
    "SRC-GEOMETRY-MONO-1": "GEOMETRY mono-1 — capmatinib in MET-altered NSCLC (TODO: confirm citation)",
    "SRC-HODI-2013": "Hodi et al. 2013 (TODO: confirm citation)",
    "SRC-INVICTUS": "INVICTUS — ripretinib in 4L+ GIST (TODO: confirm citation)",
    "SRC-LIBRETTO-001": "LIBRETTO-001 — selpercatinib in RET-altered cancers (TODO: confirm citation)",
    "SRC-LIBRETTO-431": "LIBRETTO-431 — selpercatinib in RET-fusion NSCLC (TODO: confirm citation)",
    "SRC-LIBRETTO-531": "LIBRETTO-531 — selpercatinib in RET-mutant MTC (TODO: confirm citation)",
    "SRC-NAVIGATE": "NAVIGATE — larotrectinib in NTRK-fusion solid tumors (TODO: confirm citation)",
    "SRC-NAVIGATOR": "NAVIGATOR — avapritinib in PDGFRA-mutant GIST (TODO: confirm citation)",
    "SRC-NCCN-ALL-2025": "NCCN Acute Lymphoblastic Leukemia guideline (2025) (TODO: confirm citation)",
    "SRC-NCCN-BONE-SARCOMA": "NCCN Bone Cancer guideline (TODO: confirm year/citation)",
    "SRC-NCCN-CNS": "NCCN CNS Cancers guideline (TODO: confirm year — likely placeholder for SRC-NCCN-CNS-2025)",
    "SRC-NCCN-GIST": "NCCN GIST guideline (TODO: confirm year — likely placeholder for SRC-NCCN-GIST-2025)",
    "SRC-NCCN-HEAD-AND-NECK": "NCCN Head and Neck Cancers guideline (TODO: confirm year/citation)",
    "SRC-NCCN-HEPATOBILIARY": "NCCN Hepatobiliary Cancers guideline (TODO: confirm year/citation)",
    "SRC-NCCN-MELANOMA": "NCCN Melanoma guideline (TODO: confirm year — placeholder for SRC-NCCN-MELANOMA-2025)",
    "SRC-NCCN-PEDIATRIC-SARCOMA": "NCCN Pediatric Sarcoma guideline (TODO: confirm year/citation)",
    "SRC-NCCN-SARCOMA": "NCCN Soft Tissue Sarcoma guideline (TODO: confirm year/citation)",
    "SRC-NCCN-SM": "NCCN Systemic Mastocytosis guideline (TODO: confirm year — placeholder for SRC-NCCN-SM-2025)",
    "SRC-NCCN-SM-2024": "NCCN Systemic Mastocytosis guideline (2024) (TODO: confirm citation; SRC-NCCN-SM-2025 also present)",
    "SRC-NCCN-THYROID": "NCCN Thyroid Carcinoma guideline (TODO: confirm year — placeholder for SRC-NCCN-THYROID-2025)",
    "SRC-NF1-CONSORTIUM": "NF1 Consortium recommendations (TODO: confirm specific publication)",
    "SRC-PAPMET": "PAPMET — cabozantinib vs sunitinib in papillary RCC (TODO: confirm citation)",
    "SRC-PATHFINDER": "PATHFINDER — avapritinib in advanced systemic mastocytosis (TODO: confirm citation)",
    "SRC-SAVOIR": "SAVOIR — savolitinib in MET-driven papillary RCC (TODO: confirm citation)",
    "SRC-SCOUT": "SCOUT — larotrectinib pediatric NTRK-fusion (TODO: confirm citation)",
    "SRC-SSG-XVIII": "SSG XVIII — adjuvant imatinib 3y vs 1y in GIST (TODO: confirm citation)",
    "SRC-STARTRK-2": "STARTRK-2 — entrectinib in NTRK/ROS1-altered tumors (TODO: confirm citation)",
    "SRC-VISION": "VISION — tepotinib in METex14 NSCLC (TODO: confirm citation)",
    "SRC-VOYAGER": "VOYAGER — avapritinib vs regorafenib in 3L+ GIST (TODO: confirm citation)",
}


def existing_source_ids() -> set[str]:
    out: set[str] = set()
    for p in SOURCES.glob("*.yaml"):
        raw = yaml.safe_load(p.read_text(encoding="utf-8"))
        if isinstance(raw, dict) and isinstance(raw.get("id"), str):
            out.add(raw["id"])
    return out


def all_referenced_ids() -> set[str]:
    refs: set[str] = set()
    for p in CONTENT.rglob("*.yaml"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        for m in PROSE_PATTERN.findall(text):
            refs.add(m)
    return refs


def classify(sid: str) -> str:
    """Return source_type per schema (guideline / clinical_trial / etc.)."""
    if sid.startswith("SRC-NCCN-"):
        return "guideline"
    if sid.startswith("SRC-ESMO-"):
        return "guideline"
    if sid.startswith("SRC-ASCO-"):
        return "guideline"
    if sid.startswith("SRC-ASH-"):
        return "guideline"
    if sid.startswith("SRC-ATA-"):
        return "guideline"
    if sid.startswith("SRC-EANO-"):
        return "guideline"
    if sid.startswith("SRC-EASL-"):
        return "guideline"
    if sid.startswith("SRC-FDA-"):
        return "regulatory"
    if sid.startswith("SRC-EMA-"):
        return "regulatory"
    if sid.startswith("SRC-MOZ-"):
        return "regulatory"
    if sid.startswith("SRC-PMID-"):
        return "rct_publication"
    if sid == "SRC-ONCOKB":
        return "molecular_kb"
    if sid in TRIAL_IDS:
        return "clinical_trial"
    if sid in PUB_IDS:
        return "rct_publication"
    if sid in CONSORTIA:
        return "unknown_classification"
    return "unknown_classification"


def filename_for(sid: str) -> str:
    # Existing convention: src_<lowercase-with-underscores>.yaml
    body = sid[len("SRC-"):]
    body = body.replace("-", "_").lower()
    return f"src_{body}.yaml"


def build_stub(sid: str, source_type: str) -> dict:
    title = TITLE_HINTS.get(sid, f"{sid} (TODO: confirm citation)")
    stub: dict = {
        "id": sid,
        "source_type": source_type,
        "title": title,
        # url intentionally omitted — user constraint forbids inventing
        # NCT / DOI / PMID we haven't seen in the citation. A reviewer
        # fills this in.
        "currency_status": "current",
        "hosting_mode": "referenced",
        "ingestion": {"method": "none"},
        "legal_review": {
            "status": "pending",
            "notes": "Auto-stub; license + citation pending clinical signoff.",
        },
        "last_verified": "2026-04-27",
        # Extras (extra='allow' on Base) — used by reviewers to find stubs.
        "review_status": "pending_clinical_signoff",
        "drafted_by": "claude_extraction",
        "notes": (
            "Auto-stub from referenced citation (source-gap mention in prose). "
            "Verify metadata + ingest via the appropriate client when proxy lands. "
            "Replace TODO in title with confirmed citation."
        ),
    }
    return stub


def main() -> int:
    existing = existing_source_ids()
    referenced = all_referenced_ids()
    # Drop the SRC-E artifact (regex truncation of a non-conforming token
    # `SRC-EpSSG-NRSTS` in prose). It is not a real citation.
    referenced.discard("SRC-E")

    missing = sorted(referenced - existing)
    print(f"existing sources: {len(existing)}")
    print(f"referenced (incl. prose): {len(referenced)}")
    print(f"missing: {len(missing)}")

    by_type: dict[str, list[str]] = {}
    written: list[str] = []

    for sid in missing:
        st = classify(sid)
        by_type.setdefault(st, []).append(sid)
        out = SOURCES / filename_for(sid)
        if out.exists():
            print(f"  SKIP (file exists): {out.name}")
            continue
        stub = build_stub(sid, st)
        # Dump with sort_keys=False to keep human-readable order.
        out.write_text(
            yaml.safe_dump(stub, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        written.append(sid)
        print(f"  WROTE {out.name}  source_type={st}")

    print()
    print("Breakdown by source_type:")
    for k, v in sorted(by_type.items()):
        print(f"  {k}: {len(v)}")
    print(f"Stubs written: {len(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
