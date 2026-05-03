"""ESMO PDF fetcher + text extractor for KB verification.

PROTOTYPE — feat/esmo-pdf-extract-2026-05-03.
NOT for merge until SOURCE_INGESTION_SPEC §6 red flag #1 (derivative-work
question) is resolved by legal review. Output goes to docs/reviews/ only;
nothing is auto-written to knowledge_base/hosted/content/.

Pipeline:
    1. UnpaywallResolver  — DOI → best open-access PDF URL (free API, CC0 data)
    2. _download_pdf      — HTTP GET → local cache (gitignored)
    3. _extract_text      — pdfplumber → text blocks + tables per page
    4. EsmoPdfClient      — orchestrates the above behind BaseSourceClient

Per SOURCE_INGESTION_SPEC §1.2 (referenced mode) + §1.3 (mixed mode):
- We do not store extracted content in the KB directly.
- Extracted text is a transient verification artefact, not a hosted asset.
- Attribution required on every use of any excerpt.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from knowledge_base.clients.base import (
    BaseSourceClient,
    CacheBackend,
    RateLimit,
    SourceResponse,
)

# ── Constants ────────────────────────────────────────────────────────────────

UNPAYWALL_BASE = "https://api.unpaywall.org/v2"
CONTACT_EMAIL  = "8054345@gmail.com"
USER_AGENT     = "OpenOnco-verification/0.1 (non-commercial; https://openonco.info)"

# Therapy-section keywords used to slice relevant pages from long PDFs.
THERAPY_KEYWORDS = [
    "first-line", "second-line", "third-line",
    "recommended", "recommendation",
    "treatment algorithm",
    "systemic therapy",
    "front-line", "salvage",
    "preferred regimen",
    "ESMO consensus",
]

# Local PDF cache — must be in .gitignore.
DEFAULT_CACHE_DIR = (
    Path(__file__).parent.parent.parent / "knowledge_base" / "cache" / "esmo_pdfs"
)


# ── Data classes ─────────────────────────────────────────────────────────────

@dataclass
class EsmoPdfQuery:
    """Input to EsmoPdfClient.fetch()."""
    source_id: str          # e.g. "SRC-ESMO-AML-2020"
    doi: Optional[str] = None
    direct_pdf_url: Optional[str] = None  # override Unpaywall when known


@dataclass
class PageBlock:
    page_number: int
    text: str
    tables: list[list[list[str]]] = field(default_factory=list)


@dataclass
class EsmoExtraction:
    source_id: str
    doi: Optional[str]
    pdf_url: str
    extracted_at: str           # ISO-8601
    page_count: int
    pages: list[PageBlock]
    therapy_page_indices: list[int]  # pages that contain therapy keywords
    error: Optional[str] = None  # non-None when extraction partially failed

    def therapy_text(self) -> str:
        """Concatenate text from therapy-relevant pages only."""
        blocks = [self.pages[i] for i in self.therapy_page_indices if i < len(self.pages)]
        return "\n\n--- Page {} ---\n".join(
            [b.text for b in blocks]
        ) if blocks else ""

    def to_dict(self) -> dict:
        return asdict(self)


# ── Unpaywall resolver ────────────────────────────────────────────────────────

class UnpaywallError(Exception):
    pass


class UnpaywallResolver:
    """Resolve a DOI to a best open-access PDF URL via the Unpaywall API.

    Unpaywall is free for non-commercial use; data is CC0.
    Rate limit: 100 000 req/day; no key needed, email required.
    """

    def __init__(self, email: str = CONTACT_EMAIL) -> None:
        self._email = email
        self._last_call: float = 0.0
        self._min_interval = 0.2  # 5 req/s max

    def resolve(self, doi: str) -> Optional[str]:
        """Return the best OA PDF URL for a DOI, or None if not found."""
        doi = doi.strip().lstrip("https://doi.org/").lstrip("doi:")
        url = f"{UNPAYWALL_BASE}/{urllib.parse.quote(doi, safe='')}?email={self._email}"

        # polite rate-limit
        gap = time.monotonic() - self._last_call
        if gap < self._min_interval:
            time.sleep(self._min_interval - gap)
        self._last_call = time.monotonic()

        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            raise UnpaywallError(f"Unpaywall HTTP {exc.code} for DOI {doi}") from exc
        except Exception as exc:
            raise UnpaywallError(f"Unpaywall error for DOI {doi}: {exc}") from exc

        # Prefer gold/hybrid OA with a direct PDF link.
        best = data.get("best_oa_location") or {}
        pdf_url = best.get("url_for_pdf")
        if pdf_url:
            return pdf_url

        # Fall back to any OA location with a PDF.
        for loc in (data.get("oa_locations") or []):
            if loc.get("url_for_pdf"):
                return loc["url_for_pdf"]

        return None


# ── PDF download + extraction ─────────────────────────────────────────────────

def _cache_path(pdf_url: str, cache_dir: Path) -> Path:
    digest = hashlib.sha256(pdf_url.encode()).hexdigest()[:16]
    return cache_dir / f"{digest}.pdf"


def _download_pdf(pdf_url: str, cache_dir: Path) -> Path:
    """Download a PDF to the local cache; return path. Cached across runs."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    dest = _cache_path(pdf_url, cache_dir)
    if dest.is_file() and dest.stat().st_size > 1024:
        return dest  # cache hit

    req = urllib.request.Request(pdf_url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            dest.write_bytes(resp.read())
    except Exception as exc:
        raise RuntimeError(f"PDF download failed ({pdf_url}): {exc}") from exc

    if dest.stat().st_size < 1024:
        dest.unlink(missing_ok=True)
        raise RuntimeError(f"Downloaded PDF too small — likely a gate page: {pdf_url}")

    return dest


def _extract_with_pdfplumber(pdf_path: Path) -> list[PageBlock]:
    try:
        import pdfplumber  # type: ignore
    except ImportError:
        raise ImportError(
            "pdfplumber is required for ESMO PDF extraction. "
            "Install with: pip install pdfplumber"
        )

    blocks: list[PageBlock] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            raw_tables = page.extract_tables() or []
            # Normalise table cells to strings.
            tables = [
                [[cell or "" for cell in row] for row in tbl]
                for tbl in raw_tables
            ]
            blocks.append(PageBlock(page_number=i + 1, text=text, tables=tables))
    return blocks


def _therapy_pages(blocks: list[PageBlock]) -> list[int]:
    """Return 0-based indices of pages that contain therapy-relevant keywords."""
    kw_lower = [k.lower() for k in THERAPY_KEYWORDS]
    indices = []
    for i, block in enumerate(blocks):
        text_lower = block.text.lower()
        if any(kw in text_lower for kw in kw_lower):
            indices.append(i)
    return indices


# ── BaseSourceClient implementation ──────────────────────────────────────────

class EsmoPdfClient(BaseSourceClient[EsmoPdfQuery, dict]):
    """Fetch + extract an ESMO guideline PDF for verification.

    Wraps UnpaywallResolver + pdfplumber behind the shared BaseSourceClient
    interface (caching, rate-limiting). The raw payload stored in the cache
    is a dict serialisation of EsmoExtraction so it survives JSON round-trips.

    NOTE: This client is VERIFICATION-ONLY. Nothing it produces is written
    to knowledge_base/hosted/content/ automatically. See module docstring.
    """

    source_id        = "SRC-ESMO-PDF-CLIENT"
    rate_limit       = RateLimit(tokens_per_second=0.5, burst=2)  # polite
    cache_ttl_seconds = 30 * 24 * 3600  # 30 days — guidelines change slowly
    api_version      = "unpaywall-v2+pdfplumber"

    def __init__(
        self,
        cache: Optional[CacheBackend] = None,
        pdf_cache_dir: Optional[Path] = None,
        unpaywall_email: str = CONTACT_EMAIL,
    ) -> None:
        super().__init__(cache=cache)
        self._pdf_cache_dir = pdf_cache_dir or DEFAULT_CACHE_DIR
        self._unpaywall = UnpaywallResolver(email=unpaywall_email)

    def _fetch_raw(self, query: EsmoPdfQuery) -> tuple[dict, Optional[str]]:
        pdf_url = query.direct_pdf_url

        if not pdf_url and query.doi:
            pdf_url = self._unpaywall.resolve(query.doi)

        if not pdf_url:
            extraction = EsmoExtraction(
                source_id=query.source_id,
                doi=query.doi,
                pdf_url="",
                extracted_at=datetime.now(timezone.utc).isoformat(),
                page_count=0,
                pages=[],
                therapy_page_indices=[],
                error="No open-access PDF found via Unpaywall and no direct_pdf_url provided.",
            )
            return extraction.to_dict(), self.api_version

        try:
            pdf_path  = _download_pdf(pdf_url, self._pdf_cache_dir)
            blocks    = _extract_with_pdfplumber(pdf_path)
            t_indices = _therapy_pages(blocks)

            extraction = EsmoExtraction(
                source_id=query.source_id,
                doi=query.doi,
                pdf_url=pdf_url,
                extracted_at=datetime.now(timezone.utc).isoformat(),
                page_count=len(blocks),
                pages=blocks,
                therapy_page_indices=t_indices,
            )
        except Exception as exc:
            extraction = EsmoExtraction(
                source_id=query.source_id,
                doi=query.doi,
                pdf_url=pdf_url or "",
                extracted_at=datetime.now(timezone.utc).isoformat(),
                page_count=0,
                pages=[],
                therapy_page_indices=[],
                error=str(exc),
            )

        return extraction.to_dict(), self.api_version


__all__ = [
    "EsmoPdfClient",
    "EsmoPdfQuery",
    "EsmoExtraction",
    "PageBlock",
    "UnpaywallResolver",
    "UnpaywallError",
]
