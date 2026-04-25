"""One-off populate corpus_role / pages_count / references_count on Source YAMLs.

These are honest estimates of document mass behind each cited source —
NCCN guidelines really are 300-500 pages with 400-700 references each.
Marketing metric: total references_count = sum of primary RCTs / cohort
studies / meta-analyses behind the curated corpus, surfaced on landing
to communicate "no human can process this much per case".

Round all numbers to nearest 50 references / 10 pages so we don't claim
more precision than we have. Estimates verified against:
- NCCN guideline lengths from public PDFs
- ESMO/BSH typical guideline format (30-50 pages, 100-200 refs)
- EASL HCV 2023 published metadata
- CTCAE v5 spec page count
- FDA CDS Guidance page count from regulations.gov

Run once:  py -3.12 -m scripts._populate_source_corpus
"""

from __future__ import annotations

from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "sources"


CORPUS: dict[str, dict] = {
    "SRC-NCCN-BCELL-2025":  {"pages": 500, "refs": 700, "role": "primary_guideline"},
    "SRC-NCCN-MM-2025":     {"pages": 400, "refs": 600, "role": "primary_guideline"},
    "SRC-NCCN-AML-2025":    {"pages": 350, "refs": 500, "role": "primary_guideline"},
    "SRC-NCCN-MPN-2025":    {"pages": 300, "refs": 400, "role": "primary_guideline"},
    "SRC-ESMO-MZL-2024":    {"pages":  30, "refs": 150, "role": "primary_guideline"},
    "SRC-BSH-MZL-2024":     {"pages":  50, "refs": 120, "role": "regional_guideline"},
    "SRC-EHA-WORKUP-2024":  {"pages":  40, "refs": 100, "role": "diagnostic_methodology"},
    "SRC-EASL-HCV-2023":    {"pages":  80, "refs": 250, "role": "primary_guideline"},
    "SRC-WHO-LNSC-2023":    {"pages": 150, "refs": 200, "role": "diagnostic_methodology"},
    "SRC-MOZ-UA-LYMPH-2024":{"pages":  60, "refs":  50, "role": "regional_guideline"},
    "SRC-CTCAE-V5":         {"pages": 150, "refs":  30, "role": "terminology"},
    "SRC-FDA-CDS-2026":     {"pages":  30, "refs":  20, "role": "regulatory"},
    "SRC-ARCAINI-2014":     {"pages":  10, "refs":  50, "role": "rct_publication"},
}


def main() -> int:
    updated = 0
    for path in sorted(SRC_DIR.glob("*.yaml")):
        with path.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        sid = data.get("id")
        if sid not in CORPUS:
            print(f"  skip {path.name}: id {sid!r} not in CORPUS map")
            continue
        info = CORPUS[sid]
        # Don't clobber pre-existing values if someone already filled them in
        data["pages_count"] = data.get("pages_count") or info["pages"]
        data["references_count"] = data.get("references_count") or info["refs"]
        data["corpus_role"] = data.get("corpus_role") or info["role"]
        with path.open("w", encoding="utf-8") as fh:
            yaml.safe_dump(
                data,
                fh,
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False,
                width=100,
            )
        updated += 1
        print(f"  ok   {path.name}  pages={info['pages']}  refs={info['refs']}  role={info['role']}")
    total_pages = sum(c["pages"] for c in CORPUS.values())
    total_refs = sum(c["refs"] for c in CORPUS.values())
    print(f"\nUpdated {updated} files. Total pages={total_pages}, refs={total_refs}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
