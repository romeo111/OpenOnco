#!/usr/bin/env python3
"""Verify KB indication content against live ESMO guideline PDFs.

PROTOTYPE — feat/esmo-pdf-extract-2026-05-03.
Nothing is written to knowledge_base/hosted/content/ automatically.
All output goes to docs/reviews/esmo-verify-*.md for clinician sign-off.

Per CHARTER §8.3: LLM-assisted extraction is permitted for verification;
human clinical review is mandatory before any KB update.

Usage
-----
  # Verify one source:
  python scripts/verify_esmo_content.py --source SRC-ESMO-AML-2020

  # Verify all sources that have a real DOI:
  python scripts/verify_esmo_content.py --all

  # Dry-run: show which sources would be processed, don't fetch PDFs:
  python scripts/verify_esmo_content.py --all --dry-run

  # Output to a custom directory:
  python scripts/verify_esmo_content.py --all --output docs/reviews/
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from textwrap import indent, wrap

# Repo root detection — works when called from anywhere.
REPO_ROOT    = Path(__file__).parent.parent
SOURCES_DIR  = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "sources"
IND_DIR      = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "indications"
REVIEWS_DIR  = REPO_ROOT / "docs" / "reviews"

sys.path.insert(0, str(REPO_ROOT))

try:
    import yaml  # type: ignore
except ImportError:
    print("ERROR: PyYAML required — pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# ── YAML helpers ─────────────────────────────────────────────────────────────

def _load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _is_placeholder_doi(doi: str) -> bool:
    """Return True for stub DOIs like '10.1016/j.annonc.2024.XX.YYY'."""
    return bool(re.search(r"[Xx]{2}|YYY|TBD|placeholder", doi, re.I))


# ── Source loading ────────────────────────────────────────────────────────────

def load_esmo_sources() -> list[dict]:
    """Load all src_esmo_*.yaml files; skip stubs and placeholder DOIs."""
    sources = []
    for path in sorted(SOURCES_DIR.glob("src_esmo_*.yaml")):
        data = _load_yaml(path)
        data["_path"] = str(path)
        sources.append(data)
    return sources


def sources_with_doi(sources: list[dict]) -> list[dict]:
    return [
        s for s in sources
        if s.get("doi") and not _is_placeholder_doi(str(s["doi"]))
    ]


# ── Indication loading ────────────────────────────────────────────────────────

def load_indications_for_disease(disease_id: str) -> list[dict]:
    """Return all indications that apply to a given disease_id."""
    results = []
    for path in sorted(IND_DIR.glob("*.yaml")):
        try:
            data = _load_yaml(path)
        except Exception:
            continue
        applicable = data.get("applicable_to", {})
        if isinstance(applicable, dict):
            if applicable.get("disease_id") == disease_id:
                data["_path"] = path.name
                results.append(data)
    return results


def indications_for_source(source: dict) -> list[dict]:
    """Return all KB indications linked to any disease this source covers."""
    disease_ids = source.get("relates_to_diseases") or []
    indications = []
    seen = set()
    for did in disease_ids:
        for ind in load_indications_for_disease(did):
            key = ind.get("id") or ind.get("_path")
            if key not in seen:
                seen.add(key)
                indications.append(ind)
    return indications


# ── Report generation ─────────────────────────────────────────────────────────

MAX_TEXT_CHARS = 3000  # max extracted therapy text shown per source in report


def _wrap_block(text: str, width: int = 90) -> str:
    lines = text.splitlines()
    wrapped = []
    for line in lines:
        if len(line) <= width:
            wrapped.append(line)
        else:
            wrapped.extend(wrap(line, width=width))
    return "\n".join(wrapped)


def _indication_summary(ind: dict) -> str:
    iid        = ind.get("id", ind.get("_path", "?"))
    regimen    = ind.get("recommended_regimen", "?")
    line       = ind.get("applicable_to", {}).get("line_of_therapy", "?")
    track      = ind.get("plan_track", "?")
    ev_level   = ind.get("evidence_level", "?")
    rationale  = ind.get("rationale", "").strip()
    sources    = ind.get("sources", [])
    src_ids    = ", ".join(
        (s.get("source_id") if isinstance(s, dict) else str(s))
        for s in sources
    )
    signoffs   = ind.get("reviewer_signoffs", 0)
    status     = ind.get("review_status") or ind.get("ukrainian_review_status", "?")

    lines = [
        f"### {iid}",
        f"- **Regimen:** {regimen}  |  **Line:** {line}  |  **Track:** {track}",
        f"- **Evidence level:** {ev_level}  |  **Reviewer sign-offs:** {signoffs}",
        f"- **Review status:** {status}",
        f"- **KB sources cited:** {src_ids or '(none)'}",
        "",
        "**Current KB rationale:**",
        "",
    ]
    if rationale:
        lines.append(indent(_wrap_block(rationale[:800]), "  "))
    else:
        lines.append("  *(empty)*")
    return "\n".join(lines)


def generate_report(
    source: dict,
    extraction_result: dict | None,
    indications: list[dict],
    output_dir: Path,
) -> Path:
    src_id  = source.get("id", "UNKNOWN")
    title   = source.get("title", src_id)
    doi     = source.get("doi", "N/A")
    version = source.get("version", "?")
    today   = date.today().isoformat()

    safe_id = src_id.lower().replace("src-", "").replace("-", "_")
    out_path = output_dir / f"esmo-verify-{safe_id}-{today}.md"

    # ── extraction details ────────────────────────────────────────────────
    if extraction_result:
        pdf_url       = extraction_result.get("pdf_url") or "(not resolved)"
        page_count    = extraction_result.get("page_count", 0)
        t_indices     = extraction_result.get("therapy_page_indices") or []
        error         = extraction_result.get("error")

        # Reconstruct therapy text from pages list.
        pages = extraction_result.get("pages") or []
        therapy_texts = []
        for idx in t_indices:
            if idx < len(pages):
                block = pages[idx]
                txt = block.get("text", "") if isinstance(block, dict) else ""
                if txt.strip():
                    therapy_texts.append(f"_[Page {idx + 1}]_\n\n{txt.strip()}")

        therapy_combined = "\n\n---\n\n".join(therapy_texts)
        if len(therapy_combined) > MAX_TEXT_CHARS:
            therapy_combined = therapy_combined[:MAX_TEXT_CHARS] + "\n\n… *(truncated)*"
    else:
        pdf_url = "(not fetched — dry run)"
        page_count = 0
        t_indices = []
        therapy_combined = "(not fetched)"
        error = None

    # ── build report ─────────────────────────────────────────────────────
    sections: list[str] = []

    sections.append(f"# ESMO Verification Report — {src_id}")
    sections.append(
        f"**Generated:** {today}  \n"
        f"**Branch:** feat/esmo-pdf-extract-2026-05-03  \n"
        f"**Mode:** PROTOTYPE — output for clinical review only, NOT auto-applied to KB  \n"
        f"**Legal status:** SOURCE_INGESTION_SPEC §6 red flag #1 pending resolution"
    )

    sections.append("## 1. Source metadata")
    sections.append(
        f"| Field | Value |\n"
        f"|---|---|\n"
        f"| **Source ID** | `{src_id}` |\n"
        f"| **Title** | {title} |\n"
        f"| **DOI** | [{doi}](https://doi.org/{doi}) |\n"
        f"| **Version** | {version} |\n"
        f"| **Hosting mode** | {source.get('hosting_mode', '?')} |\n"
        f"| **License** | {source.get('license', {}).get('name', '?') if isinstance(source.get('license'), dict) else '?'} |\n"
        f"| **Legal review** | {source.get('legal_review', {}).get('status', '?') if isinstance(source.get('legal_review'), dict) else '?'} |\n"
        f"| **PDF URL** | {pdf_url} |\n"
        f"| **PDF pages** | {page_count} |\n"
        f"| **Therapy pages found** | {len(t_indices)} ({', '.join(str(i+1) for i in t_indices[:10])}{'…' if len(t_indices) > 10 else ''}) |"
    )

    if error:
        sections.append(f"## ⚠️ Extraction error\n\n```\n{error}\n```")

    sections.append("## 2. Extracted therapy text (ESMO PDF source)")
    sections.append(
        "> **Attribution required on any use:** "
        + (source.get("attribution", {}).get("text", title) if isinstance(source.get("attribution"), dict) else title)
        + f" (DOI: {doi})"
    )
    sections.append(
        "> **Do not copy-paste into KB** — clinician paraphrase required per SOURCE_INGESTION_SPEC §1.2."
    )
    if therapy_combined.strip():
        sections.append("```text\n" + therapy_combined + "\n```")
    else:
        sections.append("*(No therapy-relevant text extracted.)*")

    sections.append("## 3. Current KB indications for this source's diseases")
    if indications:
        sections.append(
            f"Found **{len(indications)}** indication(s) linked to "
            f"{source.get('relates_to_diseases', [])}.\n"
        )
        for ind in indications[:15]:
            sections.append(_indication_summary(ind))
            sections.append("")
        if len(indications) > 15:
            sections.append(f"*(… {len(indications) - 15} more indications not shown)*")
    else:
        sections.append(
            "*(No indications found in KB for the diseases listed in `relates_to_diseases`. "
            "Either the disease IDs are missing from the source YAML, or the indications "
            "have not been authored yet.)*"
        )

    sections.append("## 4. Clinician verification checklist")
    sections.append(
        "For each item below, the reviewing clinician should check the extracted text "
        "against the current KB indication rationale and mark ✅ / ❌ / ➕."
    )
    checklist_items = [
        "First-line regimen(s) in PDF match `recommended_regimen` in KB indication(s)",
        "Expected outcomes (ORR, CR, PFS, OS) in PDF match KB `expected_outcomes` block",
        "Hard contraindications in PDF match KB `hard_contraindications` list",
        "Any regimens in PDF **not yet** in KB (gap → new indication needed) — mark ➕",
        "Any regimens in KB that PDF **does not support** (possible hallucination) — mark ❌",
        "ESMO evidence level / recommendation grade captured correctly in KB",
        "`rationale` field accurately paraphrases PDF (not a verbatim copy)",
        "All `sources` in the indication cite this source ID where appropriate",
        "`reviewer_signoffs` incremented after this review",
        "If discrepancies found: open a draft PR updating the indication(s), citing this report",
    ]
    for item in checklist_items:
        sections.append(f"- [ ] {item}")

    sections.append("## 5. Notes / findings")
    sections.append(
        "*(Clinician fills in here — discrepancies, missing regimens, outdated claims, etc.)*\n\n"
        "---"
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n\n".join(sections), encoding="utf-8")
    return out_path


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify KB indication content against ESMO guideline PDFs"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--source", metavar="SRC_ID",
        help="Verify a single source, e.g. SRC-ESMO-AML-2020",
    )
    group.add_argument(
        "--all", action="store_true",
        help="Verify all ESMO sources that have a real DOI",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="List sources that would be processed; skip PDF fetch",
    )
    parser.add_argument(
        "--output", default=str(REVIEWS_DIR), metavar="DIR",
        help=f"Output directory for review markdowns (default: {REVIEWS_DIR})",
    )
    parser.add_argument(
        "--pdf-cache", default=None, metavar="DIR",
        help="Local PDF cache directory (default: knowledge_base/cache/esmo_pdfs/)",
    )
    args = parser.parse_args()

    output_dir  = Path(args.output)
    pdf_cache   = Path(args.pdf_cache) if args.pdf_cache else None

    all_sources = load_esmo_sources()
    doi_sources = sources_with_doi(all_sources)

    if args.source:
        targets = [s for s in all_sources if s.get("id") == args.source]
        if not targets:
            print(f"ERROR: source '{args.source}' not found in {SOURCES_DIR}", file=sys.stderr)
            print("Available ESMO sources:", file=sys.stderr)
            for s in all_sources:
                print(f"  {s.get('id')}", file=sys.stderr)
            return 1
        # Allow --source even without DOI (user may supply direct_pdf_url in future).
        usable = targets
    else:
        usable = doi_sources

    if not usable:
        print("No sources with real DOIs found. Add DOI fields to src_esmo_*.yaml first.")
        return 0

    print(f"Sources to process: {len(usable)}")
    for s in usable:
        print(f"  {s.get('id'):40s}  DOI: {s.get('doi', '(none)')}")

    if args.dry_run:
        print("\nDry run — no PDFs fetched.")
        return 0

    # Lazy import to keep CLI fast when pdfplumber not installed.
    try:
        from knowledge_base.clients.esmo_pdf_client import (
            EsmoPdfClient,
            EsmoPdfQuery,
        )
        from knowledge_base.clients.base import InMemoryCacheBackend
    except ImportError as exc:
        print(f"ERROR: Could not import EsmoPdfClient: {exc}", file=sys.stderr)
        return 1

    client = EsmoPdfClient(
        cache=InMemoryCacheBackend(),
        pdf_cache_dir=pdf_cache,
    )

    failed = 0
    for source in usable:
        src_id = source.get("id", "?")
        doi    = source.get("doi")
        print(f"\n> {src_id}", end="", flush=True)

        extraction_result: dict | None = None
        if not args.dry_run:
            try:
                query = EsmoPdfQuery(source_id=src_id, doi=doi)
                resp  = client.fetch(query)
                extraction_result = resp.data
                err   = extraction_result.get("error")
                if err:
                    print(f"  WARN  {err[:80]}", end="")
                    failed += 1
                else:
                    n_therapy = len(extraction_result.get("therapy_page_indices") or [])
                    print(f"  OK  {extraction_result.get('page_count', 0)} pages, {n_therapy} therapy pages", end="")
            except Exception as exc:
                print(f"  FAIL  {exc}", end="")
                failed += 1

        indications = indications_for_source(source)
        out = generate_report(source, extraction_result, indications, output_dir)
        print(f"  -> {out.relative_to(REPO_ROOT)}")

    print(f"\nDone. {len(usable) - failed}/{len(usable)} sources succeeded.")
    print(f"Review reports written to: {output_dir}")
    if failed:
        print(
            f"\n{failed} source(s) failed (no OA PDF found or download error). "
            "Add `direct_pdf_url` to the source YAML, or resolve DOI manually."
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
