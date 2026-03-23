from typing import Any, Dict, List, Optional, Tuple
#!/usr/bin/env python3
"""
pubmed_client.py — NCBI E-utilities Integration for Cancer AutoResearch

Fetches live PubMed data to enrich research reports with verified citations.
Uses only Python stdlib — no external dependencies.

Rate limit: 3 req/s without API key (NCBI policy).
A shared module-level limiter ensures thread-safe parallel use.

Usage:
    python pubmed_client.py search "pembrolizumab head neck squamous" --max 10
    python pubmed_client.py summarize 38500123 38499001
    python pubmed_client.py abstract 38500123
    python pubmed_client.py enrich experiment_reports/HN-001_report.json
"""

import argparse
import json
import re
import sys
import threading
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime


# ── Constants ────────────────────────────────────────────────────────────────

NCBI_BASE    = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ESEARCH_URL  = f"{NCBI_BASE}/esearch.fcgi"
ESUMMARY_URL = f"{NCBI_BASE}/esummary.fcgi"
EFETCH_URL   = f"{NCBI_BASE}/efetch.fcgi"
TOOL_NAME    = "cancer_autoresearch_loop"
CONTACT      = "autoresearch@localhost"
USER_AGENT   = "cancer_autoresearch/1.0 (Python urllib)"


# ── Rate Limiter ─────────────────────────────────────────────────────────────

class RateLimiter:
    """Token bucket limiter — thread-safe, shared across parallel callers."""

    def __init__(self, rate: float = 3.0):
        self._rate     = rate              # tokens per second
        self._tokens   = rate
        self._last     = time.monotonic()
        self._lock     = threading.Lock()

    def acquire(self) -> None:
        with self._lock:
            now    = time.monotonic()
            delta  = now - self._last
            self._last = now
            self._tokens = min(self._rate, self._tokens + delta * self._rate)
            if self._tokens < 1.0:
                sleep_for = (1.0 - self._tokens) / self._rate
                time.sleep(sleep_for)
                self._tokens = 0.0
            else:
                self._tokens -= 1.0


# Shared module-level limiter — all PubMedClient instances use this by default
_GLOBAL_LIMITER = RateLimiter(rate=3.0)


# ── Exceptions ───────────────────────────────────────────────────────────────

class PubMedError(Exception):
    pass


# ── Client ───────────────────────────────────────────────────────────────────

class PubMedClient:
    """
    Thin wrapper around NCBI E-utilities.
    All HTTP calls go through _get() which enforces rate limiting.
    """

    def __init__(self, rate_limit: float = 3.0, limiter: Optional[RateLimiter] = None):
        self._limiter = limiter or _GLOBAL_LIMITER

    # ── Internal HTTP ──────────────────────────────────────────────────────

    def _get(self, url: str, params: dict) -> str:
        """Throttled GET, returns response body as string."""
        params["tool"]  = TOOL_NAME
        params["email"] = CONTACT
        full_url = url + "?" + urllib.parse.urlencode(params)

        self._limiter.acquire()
        try:
            req = urllib.request.Request(full_url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as exc:
            raise PubMedError(f"HTTP error for {url}: {exc}") from exc

    # ── Public API ─────────────────────────────────────────────────────────

    def search(
        self,
        query: str,
        max_results: int = 10,
        date_range: Optional[tuple] = None,
        pub_types: Optional[list] = None,
    ) -> dict:
        """
        ESearch — find PMIDs matching a query.

        Returns:
            {
              "query": str,
              "count": int,
              "pmids": List[str],
              "query_translation": str,
            }
        """
        params: dict = {
            "db":      "pubmed",
            "term":    query,
            "retmax":  max_results,
            "retmode": "json",
            "sort":    "relevance",
        }
        if date_range:
            params["mindate"] = date_range[0]
            params["maxdate"] = date_range[1]
            params["datetype"] = "pdat"
        if pub_types:
            type_filter = " OR ".join(f'"{pt}"[pt]' for pt in pub_types)
            params["term"] = f"({query}) AND ({type_filter})"

        raw = self._get(ESEARCH_URL, params)
        try:
            data = json.loads(raw)["esearchresult"]
        except (json.JSONDecodeError, KeyError) as exc:
            raise PubMedError(f"Bad ESearch response: {exc}") from exc

        return {
            "query":             query,
            "count":             int(data.get("count", 0)),
            "pmids":             data.get("idlist", []),
            "query_translation": data.get("querytranslation", ""),
        }

    def get_summaries(self, pmids: list) -> list:
        """
        ESummary — document-level metadata for up to 200 PMIDs.

        Returns list of dicts:
            {
              "pmid", "title", "authors", "journal",
              "year", "volume", "issue", "pages", "doi", "pub_types"
            }
        """
        if not pmids:
            return []
        # ESummary handles up to 200 at a time; split if larger
        results = []
        for chunk_start in range(0, len(pmids), 200):
            chunk = pmids[chunk_start:chunk_start + 200]
            params = {
                "db":      "pubmed",
                "id":      ",".join(str(p) for p in chunk),
                "retmode": "xml",
            }
            raw = self._get(ESUMMARY_URL, params)
            results.extend(self._parse_esummary_xml(raw))
        return results

    def get_abstract(self, pmid: str) -> dict:
        """
        EFetch — full abstract + MeSH terms for a single PMID.

        Returns:
            {"pmid", "title", "abstract", "mesh_terms", "pub_date"}
        Raises PubMedError if PMID not found or no abstract.
        """
        params = {
            "db":      "pubmed",
            "id":      str(pmid),
            "retmode": "xml",
            "rettype": "abstract",
        }
        raw = self._get(EFETCH_URL, params)
        results = self._parse_efetch_xml(raw)
        if not results:
            raise PubMedError(f"PMID {pmid} not found or has no abstract")
        return results[0]

    def search_and_summarize(
        self,
        query: str,
        max_results: int = 10,
        include_abstracts: bool = False,
    ) -> list:
        """
        Convenience: search then get_summaries, optionally get_abstract for top 5.
        """
        search_result = self.search(query, max_results=max_results)
        pmids = search_result["pmids"]
        if not pmids:
            return []
        summaries = self.get_summaries(pmids)
        if include_abstracts:
            for summary in summaries[:5]:
                try:
                    ab = self.get_abstract(summary["pmid"])
                    summary["abstract"]   = ab.get("abstract", "")
                    summary["mesh_terms"] = ab.get("mesh_terms", [])
                except PubMedError:
                    pass
        return summaries

    # ── XML Parsers ────────────────────────────────────────────────────────

    @staticmethod
    def _parse_esummary_xml(xml_str: str) -> list:
        """Parse ESummary XML into list of summary dicts."""
        results = []
        try:
            root = ET.fromstring(xml_str)
        except ET.ParseError:
            return results

        for docsum in root.findall(".//DocSum"):
            pmid_el = docsum.find("Id")
            pmid = pmid_el.text.strip() if pmid_el is not None else ""

            def item(name: str) -> str:
                el = docsum.find(f".//Item[@Name='{name}']")
                return el.text.strip() if el is not None and el.text else ""

            # Authors: NameList items
            authors = []
            for auth_el in docsum.findall(".//Item[@Name='AuthorList']/Item[@Name='Author']"):
                if auth_el.text:
                    authors.append(auth_el.text.strip())
            if len(authors) > 3:
                authors = authors[:3] + ["et al"]

            # DOI from ArticleIds
            doi = ""
            for aid in docsum.findall(".//Item[@Name='ArticleIds']/Item"):
                if aid.get("Name") == "doi" and aid.text:
                    doi = aid.text.strip()

            # Publication types
            pub_types = [
                el.text.strip()
                for el in docsum.findall(".//Item[@Name='PubTypeList']/Item")
                if el.text
            ]

            year_str = item("PubDate")
            year_match = re.search(r"(\d{4})", year_str)
            year = int(year_match.group(1)) if year_match else 0

            results.append({
                "pmid":       pmid,
                "title":      item("Title"),
                "authors":    authors,
                "journal":    item("FullJournalName") or item("Source"),
                "year":       year,
                "volume":     item("Volume"),
                "issue":      item("Issue"),
                "pages":      item("Pages"),
                "doi":        doi,
                "pub_types":  pub_types,
            })
        return results

    @staticmethod
    def _parse_efetch_xml(xml_str: str) -> list:
        """Parse EFetch XML into list of abstract dicts."""
        results = []
        try:
            root = ET.fromstring(xml_str)
        except ET.ParseError:
            return results

        for article in root.findall(".//PubmedArticle"):
            # PMID
            pmid_el = article.find(".//PMID")
            pmid = pmid_el.text.strip() if pmid_el is not None and pmid_el.text else ""

            # Title
            title_el = article.find(".//ArticleTitle")
            title = "".join(title_el.itertext()).strip() if title_el is not None else ""

            # Abstract — may have multiple AbstractText elements (structured)
            abstract_parts = []
            for ab_el in article.findall(".//AbstractText"):
                label = ab_el.get("Label", "")
                text  = "".join(ab_el.itertext()).strip()
                if label:
                    abstract_parts.append(f"{label}: {text}")
                elif text:
                    abstract_parts.append(text)
            abstract = " ".join(abstract_parts)

            # MeSH terms
            mesh_terms = []
            for mesh_el in article.findall(".//MeshHeading/DescriptorName"):
                if mesh_el.text:
                    mesh_terms.append(mesh_el.text.strip())

            # Publication date
            pub_date_parts = []
            for tag in ("Year", "Month", "Day"):
                el = article.find(f".//PubDate/{tag}")
                if el is not None and el.text:
                    pub_date_parts.append(el.text.strip())
            pub_date = " ".join(pub_date_parts)

            results.append({
                "pmid":       pmid,
                "title":      title,
                "abstract":   abstract,
                "mesh_terms": mesh_terms,
                "pub_date":   pub_date,
            })
        return results


# ── Report Enrichment ────────────────────────────────────────────────────────

def enrich_report_with_pubmed(
    report_path: str,
    client: Optional[PubMedClient] = None,
    max_enrichments: int = 10,
    verbose: bool = False,
) -> int:
    """
    For each treatment in the report, search PubMed for the study_name + cancer_type.
    Attaches verified pmid, doi, and publication year to key_evidence.

    Returns: count of treatments enriched.
    Overwrites report_path in-place (atomic write via .tmp rename).
    """
    if client is None:
        client = PubMedClient()

    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cancer_type = data.get("report_metadata", {}).get("cancer_type", "")
    treatments  = data.get("treatments", [])
    enriched    = 0

    for treatment in treatments[:max_enrichments]:
        ev = treatment.get("key_evidence", {})
        study_name = ev.get("study_name", "")
        if not study_name or ev.get("pubmed_verified"):
            continue

        query = f"{study_name} {cancer_type}"
        if verbose:
            print(f"  PubMed: {query[:60]}...")

        try:
            results = client.search_and_summarize(query, max_results=3)
            if results:
                best = results[0]
                ev["pubmed_pmid"]     = best["pmid"]
                ev["pubmed_doi"]      = best.get("doi", "")
                ev["pubmed_verified"] = True
                if not ev.get("journal") and best.get("journal"):
                    ev["journal"] = best["journal"]
                if not ev.get("year") and best.get("year"):
                    ev["year"] = best["year"]
                # Add verified PubMed URL to source_urls
                pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{best['pmid']}/"
                source_urls = treatment.get("source_urls", [])
                if pubmed_url not in source_urls:
                    source_urls.insert(0, pubmed_url)
                    treatment["source_urls"] = source_urls
                enriched += 1
        except PubMedError as exc:
            if verbose:
                print(f"    PubMed error: {exc}")

    if enriched > 0:
        # Atomic write: write to .tmp, then rename
        tmp_path = report_path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        import os
        os.replace(tmp_path, report_path)

    return enriched


# ── CLI ──────────────────────────────────────────────────────────────────────

def _fmt_summary(s: dict) -> str:
    authors = ", ".join(s.get("authors", [])[:3])
    doi_str = f"  DOI: {s['doi']}" if s.get("doi") else ""
    return (
        f"  PMID: {s['pmid']}\n"
        f"  Title: {s.get('title', 'N/A')}\n"
        f"  Journal: {s.get('journal', 'N/A')} ({s.get('year', '?')})\n"
        f"  Authors: {authors}\n"
        f"  Types: {', '.join(s.get('pub_types', []))[:60]}"
        + (f"\n{doi_str}" if doi_str else "")
    )


def main():
    parser = argparse.ArgumentParser(
        description="PubMed E-utilities client for cancer autoresearch"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # search
    p_search = sub.add_parser("search", help="Search PubMed")
    p_search.add_argument("query", nargs="+")
    p_search.add_argument("--max", type=int, default=10)
    p_search.add_argument("--since", default=None, help="Min year e.g. 2020")
    p_search.add_argument("--abstracts", action="store_true")
    p_search.add_argument("--json", action="store_true", dest="as_json")

    # summarize
    p_sum = sub.add_parser("summarize", help="Get summaries for PMIDs")
    p_sum.add_argument("pmids", nargs="+")
    p_sum.add_argument("--json", action="store_true", dest="as_json")

    # abstract
    p_ab = sub.add_parser("abstract", help="Get full abstract for a PMID")
    p_ab.add_argument("pmid")
    p_ab.add_argument("--json", action="store_true", dest="as_json")

    # enrich
    p_en = sub.add_parser("enrich", help="Enrich a report JSON with PubMed data")
    p_en.add_argument("report")
    p_en.add_argument("--verbose", "-v", action="store_true")
    p_en.add_argument("--max", type=int, default=10, dest="max_enrich")

    args = parser.parse_args()
    client = PubMedClient()

    if args.command == "search":
        query = " ".join(args.query)
        date_range = (args.since, str(datetime.now().year)) if args.since else None
        results = client.search_and_summarize(
            query, max_results=args.max,
            include_abstracts=args.abstracts,
        )
        # Also print total hit count
        sr = client.search(query, max_results=1, date_range=date_range)
        print(f"\nPubMed: '{query}' — {sr['count']} total hits, showing {len(results)}\n")
        if args.as_json:
            print(json.dumps(results, indent=2))
        else:
            for i, s in enumerate(results, 1):
                print(f"[{i}]\n{_fmt_summary(s)}\n")

    elif args.command == "summarize":
        summaries = client.get_summaries(args.pmids)
        if args.as_json:
            print(json.dumps(summaries, indent=2))
        else:
            for s in summaries:
                print(f"\n{_fmt_summary(s)}")

    elif args.command == "abstract":
        ab = client.get_abstract(args.pmid)
        if args.as_json:
            print(json.dumps(ab, indent=2))
        else:
            print(f"\nPMID: {ab['pmid']}")
            print(f"Title: {ab['title']}")
            print(f"Date: {ab.get('pub_date', 'N/A')}")
            print(f"\nAbstract:\n{ab.get('abstract', 'N/A')}")
            if ab.get("mesh_terms"):
                print(f"\nMeSH: {', '.join(ab['mesh_terms'][:10])}")

    elif args.command == "enrich":
        n = enrich_report_with_pubmed(
            args.report, client=client,
            max_enrichments=args.max_enrich,
            verbose=args.verbose,
        )
        print(f"Enriched {n} treatments in {args.report}")


if __name__ == "__main__":
    main()
