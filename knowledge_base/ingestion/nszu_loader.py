"""НСЗУ формуляр loader — skeleton.

Per SOURCE_INGESTION_SPEC §15.2. Source: nszu.gov.ua publishes
monthly Excel / PDF with the reimbursed drug list. No API.

Required libs (optional extra): openpyxl (for Excel) + pdfplumber (for PDF).

Flow:
    1. Download monthly formulary file
    2. Parse Excel/PDF → normalized YAML of MNN + ATC + indications +
       reimbursement conditions
    3. Diff vs previous month — which drugs gained/lost reimbursement
    4. Alert clinical reviewers when an active Regimen is affected

Output path:
    knowledge_base/hosted/ukraine/nszu_formulary/<yyyy-mm>/reimbursed.yaml

TODO:
    [ ] Implement Excel parser (openpyxl)
    [ ] Implement PDF parser (pdfplumber, if MOZ ships PDF)
    [ ] Diff logic between two snapshots
    [ ] Alert hook that cross-references Regimen.components[].drug_id
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="НСЗУ formulary loader — SKELETON.")
    parser.add_argument("input", type=Path, help="Excel or PDF file")
    parser.add_argument("--month", required=True, help="YYYY-MM")
    args = parser.parse_args()
    print("nszu_loader: skeleton only, not implemented.", file=sys.stderr)
    print(f"  Input: {args.input} (month: {args.month})", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
