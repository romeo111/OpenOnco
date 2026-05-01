"""One-off URL probe for chunk source-recency-refresh-wave2-2026-05-01-018.

Runs httpx GET against publisher URLs with the OpenOnco recency UA, 30s
timeout, 3 retries. Prints JSON results — used to populate sidecar files.
Not committed long-term (worker pattern matches contributions/source-recency-refresh-2026-04-29-001/_batch_worker.py
philosophy: probe-then-author).
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
        "id": "SRC-ESMO-SALIVARY",
        "url": "https://www.annalsofoncology.org/",
        "doi_fallback": None,
    },
    {
        "id": "SRC-PATHFINDER",
        # PATHFINDER trial publication: Gotlib et al., Nat Med 2021;27:2183-2191
        # PMID 34873347 / DOI 10.1038/s41591-021-01539-8
        "url": "https://pubmed.ncbi.nlm.nih.gov/34873347/",
        "doi_fallback": "https://doi.org/10.1038/s41591-021-01539-8",
    },
    {
        "id": "SRC-REVEL-GARON-2014",
        "url": "https://pubmed.ncbi.nlm.nih.gov/24933332/",
        "doi_fallback": "https://doi.org/10.1016/S0140-6736(14)60845-X",
    },
    {
        "id": "SRC-APHINITY-VONMINCKWITZ-2017",
        "url": "https://pubmed.ncbi.nlm.nih.gov/28581356",
        "doi_fallback": "https://doi.org/10.1056/NEJMoa1703643",
    },
    {
        "id": "SRC-LANCET-CPX351-2018",
        "url": "https://ascopubs.org/doi/10.1200/JCO.2017.77.6112",
        "doi_fallback": "https://doi.org/10.1200/JCO.2017.77.6112",
    },
]


def probe(url: str) -> dict:
    """GET with retries. Returns {status_code, final_url, error}."""
    if not url:
        return {"status_code": None, "final_url": None, "error": "no-url"}
    last_err = None
    for attempt in range(RETRIES):
        try:
            with httpx.Client(
                headers={"User-Agent": UA},
                timeout=TIMEOUT,
                follow_redirects=True,
            ) as client:
                r = client.get(url)
                return {
                    "status_code": r.status_code,
                    "final_url": str(r.url),
                    "error": None,
                    "redirect_history": [str(h.url) for h in r.history] or None,
                }
        except Exception as exc:  # noqa: BLE001
            last_err = repr(exc)
            time.sleep(1.0 * (attempt + 1))
    return {"status_code": None, "final_url": None, "error": last_err}


def main() -> int:
    results = []
    for t in TARGETS:
        primary = probe(t["url"])
        record = {
            "id": t["id"],
            "url": t["url"],
            "primary": primary,
            "doi_fallback": None,
        }
        if (
            t["doi_fallback"]
            and primary.get("status_code") == 403
        ):
            record["doi_fallback"] = probe(t["doi_fallback"])
        results.append(record)
    json.dump(results, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
