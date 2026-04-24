"""МОЗ протоколи extractor — skeleton.

Per SOURCE_INGESTION_SPEC §15.1. Flow:
    1. Manual discovery of new Наказ on moz.gov.ua / dec.gov.ua
    2. Download PDF → knowledge_base/hosted/ukraine/moz_protocols/<slug>/<date>/source.pdf
    3. OCR if scanned (tesseract + ukr language pack)
    4. LLM-assisted extraction of structured sections → extracted.yaml
       (allowed per CHARTER §8.1; human verification mandatory)
    5. Clinical reviewer signoff in review.yaml before Indications can
       cite this protocol

Current status: **skeleton only**. No external calls implemented.
Extraction step requires Anthropic or local LLM — choice + prompt
structure to be designed with clinical co-leads.

Required libraries (optional extra in pyproject.toml):
    pypdf / pdfplumber — PDF text extraction for text-layer PDFs
    pytesseract — OCR for scanned PDFs (requires tesseract + ukr data)

TODO list:
    [ ] Implement `extract_text_from_pdf(path) -> str`
    [ ] Implement `ocr_pdf(path) -> str` using pytesseract
    [ ] Design LLM extraction prompt per CHARTER §8.1 constraints
    [ ] Implement `write_extracted_yaml(text, metadata) -> Path`
    [ ] Implement `require_clinical_review(extracted_path) -> ReviewStub`
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def extract_text_from_pdf(pdf_path: Path) -> str:
    """TODO: pypdf/pdfplumber extraction; fallback to OCR when no text layer."""
    raise NotImplementedError("moz_extractor.extract_text_from_pdf — see module docstring")


def ocr_pdf(pdf_path: Path) -> str:
    """TODO: pytesseract with Ukrainian language pack."""
    raise NotImplementedError("moz_extractor.ocr_pdf — see module docstring")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract МОЗ protocol from PDF — SKELETON.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--slug", required=True, help="e.g. lymphoma-2024")
    args = parser.parse_args()
    print("moz_extractor: skeleton only, not implemented.", file=sys.stderr)
    print(f"  Input: {args.pdf} (slug: {args.slug})", file=sys.stderr)
    print("  See module docstring for implementation TODO list.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
