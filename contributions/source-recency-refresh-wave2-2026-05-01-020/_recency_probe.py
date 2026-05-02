"""One-off URL probe for chunk source-recency-refresh-wave2-2026-05-01-020.

Per chunk brief (issue #222):
- httpx HEAD (NOT GET — wave-1 HEAD passed publisher bot-walls).
- UA "Mozilla/5.0 (compatible; OpenOnco-recency-bot)", timeout=30s, retries=3,
  follow_redirects=True.
- 200 -> upsert (last_verified=2026-05-02, bump current_as_of if old).
- 3xx -> upsert + redirect.
- 404 / 410 -> unreachable.dead.
- 403 -> DOI HEAD fallback -> PubMed canonical HEAD fallback -> if all fail
  unreachable.blocked (no current_as_of bump).
- No URL -> unreachable.no_url + suggest.

Prints JSON to stdout — used to author the sidecar files.
"""

from __future__ import annotations

import json
import sys
import time

import httpx

UA = "Mozilla/5.0 (compatible; OpenOnco-recency-bot)"
TIMEOUT = 30.0
RETRIES = 3

TARGETS = [
    {
        "id": "SRC-ESMO-SARCOMA-2024",
        "url": None,
        "doi_fallback": None,
        "pubmed_fallback": None,
        "note": "stub: no url/pmid/doi on master; suggest ESMO STS Annals Oncol 2021 update or 2024 STS guideline if present",
        "suggest": "https://www.esmo.org/guidelines/guidelines-by-topic/sarcoma-and-gist",
    },
    {
        "id": "SRC-SCOUT",
        "url": None,
        "doi_fallback": None,
        "pubmed_fallback": None,
        "note": "stub: no url/pmid/doi on master; SCOUT pediatric NTRK-fusion most-likely refers to Laetsch et al, Lancet Oncol 2018, PMID 29606586",
        "suggest": "https://pubmed.ncbi.nlm.nih.gov/29606586/",
    },
    {
        "id": "SRC-COMBI-D-LONG-2014",
        "url": "https://pubmed.ncbi.nlm.nih.gov/25265492",
        "doi_fallback": "https://doi.org/10.1056/NEJMoa1406037",
        "pubmed_fallback": "https://pubmed.ncbi.nlm.nih.gov/25265492",
    },
    {
        "id": "SRC-OLYMPIAD-ROBSON-2017",
        "url": "https://www.nejm.org/doi/full/10.1056/NEJMoa1706450",
        "doi_fallback": "https://doi.org/10.1056/NEJMoa1706450",
        "pubmed_fallback": "https://pubmed.ncbi.nlm.nih.gov/28578601",
    },
    {
        "id": "SRC-KEYNOTE-407-PAZ-ARES-2018",
        "url": "https://pubmed.ncbi.nlm.nih.gov/30280635",
        "doi_fallback": "https://doi.org/10.1056/NEJMoa1810865",
        "pubmed_fallback": "https://pubmed.ncbi.nlm.nih.gov/30280635",
    },
]


def head_probe(url: str | None) -> dict:
    """HEAD with retries. Returns {status_code, final_url, error, redirect_history}."""
    if not url:
        return {"status_code": None, "final_url": None, "error": "no-url",
                "redirect_history": None}
    last_err = None
    for attempt in range(RETRIES):
        try:
            with httpx.Client(
                headers={"User-Agent": UA},
                timeout=TIMEOUT,
                follow_redirects=True,
            ) as client:
                r = client.head(url)
                return {
                    "status_code": r.status_code,
                    "final_url": str(r.url),
                    "error": None,
                    "redirect_history": [str(h.url) for h in r.history] or None,
                }
        except Exception as exc:  # noqa: BLE001
            last_err = repr(exc)
            time.sleep(1.0 * (attempt + 1))
    return {"status_code": None, "final_url": None, "error": last_err,
            "redirect_history": None}


def main() -> int:
    results = []
    for t in TARGETS:
        primary = head_probe(t["url"])
        record = {
            "id": t["id"],
            "url": t["url"],
            "primary": primary,
            "doi_fallback": None,
            "pubmed_fallback": None,
            "note": t.get("note"),
            "suggest": t.get("suggest"),
        }
        # Fallback chain on 403 (or other non-2xx/3xx fail not 404/410)
        sc = primary.get("status_code")
        needs_fallback = sc == 403 or (sc is not None and sc not in (200, 301, 302, 303, 307, 308, 404, 410)) or sc is None
        if needs_fallback and t.get("doi_fallback"):
            record["doi_fallback"] = head_probe(t["doi_fallback"])
            doi_sc = record["doi_fallback"].get("status_code")
            doi_ok = doi_sc and 200 <= doi_sc < 400
            if not doi_ok and t.get("pubmed_fallback"):
                record["pubmed_fallback"] = head_probe(t["pubmed_fallback"])
        results.append(record)
    json.dump(results, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
