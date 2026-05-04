"""One-off URL probe for chunk source-recency-refresh-wave2-2026-05-01-022.

Runs httpx HEAD against publisher URLs with the OpenOnco recency UA, 30s
timeout, 3 retries. Per chunk brief:

  - 200 -> upsert
  - 3xx -> upsert + redirect
  - 404 -> dead
  - 403 -> DOI HEAD fallback -> PubMed canonical HEAD fallback
           -> if all fail unreachable.blocked
  - No URL -> unreachable.no_url

Mirrors wave-1 _batch_worker.py / wave-2-018 _recency_probe.py philosophy
(probe-then-author). Prints JSON results to stdout for sidecar authoring.
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
        "id": "SRC-FIGHT",
        # Auto-stub: hosted YAML has no top-level url field.
        "url": None,
        "doi_fallback": None,
        "pubmed_fallback": None,
    },
    {
        "id": "SRC-VOYAGER",
        # Auto-stub: hosted YAML has no top-level url field.
        "url": None,
        "doi_fallback": None,
        "pubmed_fallback": None,
    },
    {
        "id": "SRC-RESPONSE-VANNUCCHI-2015",
        "url": "https://www.nejm.org/doi/full/10.1056/NEJMoa1409002",
        "doi_fallback": "https://doi.org/10.1056/NEJMoa1409002",
        "pubmed_fallback": "https://pubmed.ncbi.nlm.nih.gov/25629741/",
    },
    {
        "id": "SRC-MONARCH-2-SLEDGE-2017",
        "url": "https://pubmed.ncbi.nlm.nih.gov/28580882",
        "doi_fallback": "https://doi.org/10.1200/JCO.2017.73.7585",
        "pubmed_fallback": "https://pubmed.ncbi.nlm.nih.gov/28580882/",
    },
    {
        "id": "SRC-IMC-HTLV-2017",
        "url": "https://ascopubs.org/doi/10.1200/JCO.18.00501",
        "doi_fallback": "https://doi.org/10.1200/JCO.18.00501",
        "pubmed_fallback": "https://pubmed.ncbi.nlm.nih.gov/30657736/",
    },
]


def probe(url: str | None) -> dict:
    """HEAD with retries. Returns {status_code, final_url, error, redirect_history}."""
    if not url:
        return {
            "status_code": None,
            "final_url": None,
            "error": "no-url",
            "redirect_history": None,
        }
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
    return {
        "status_code": None,
        "final_url": None,
        "error": last_err,
        "redirect_history": None,
    }


def main() -> int:
    results = []
    for t in TARGETS:
        primary = probe(t["url"])
        record = {
            "id": t["id"],
            "url": t["url"],
            "primary": primary,
            "doi_fallback": None,
            "pubmed_fallback": None,
        }
        # Brief: 403 -> DOI HEAD fallback -> PubMed canonical HEAD fallback.
        if primary.get("status_code") == 403 and t.get("doi_fallback"):
            record["doi_fallback"] = probe(t["doi_fallback"])
            doi_status = (record["doi_fallback"] or {}).get("status_code")
            if doi_status == 403 and t.get("pubmed_fallback"):
                record["pubmed_fallback"] = probe(t["pubmed_fallback"])
        results.append(record)
    json.dump(results, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
