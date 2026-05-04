"""One-off URL probe for chunk source-recency-refresh-wave2-2026-05-01-026.

Runs httpx HEAD against publisher URLs with the OpenOnco recency UA, 30s
timeout, 3 retries. Falls back to DOI then PubMed canonical URLs on 403,
per chunk-brief rule. Prints JSON results — used to populate sidecar files.
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
        "id": "SRC-FORTITUDE-101",
        # Hosted YAML is auto-stub: no top-level url field; title still has TODO.
        "url": None,
        "doi_fallback": None,
        "pubmed_fallback": None,
    },
    {
        "id": "SRC-BR21-SHEPHERD-2005",
        "url": "https://pubmed.ncbi.nlm.nih.gov/16014883",
        "doi_fallback": "https://doi.org/10.1056/NEJMoa050753",
        "pubmed_fallback": "https://pubmed.ncbi.nlm.nih.gov/16014883",
    },
    {
        "id": "SRC-KEYNOTE-006-ROBERT-2015",
        "url": "https://pubmed.ncbi.nlm.nih.gov/25891173",
        "doi_fallback": "https://doi.org/10.1056/NEJMoa1503093",
        "pubmed_fallback": "https://pubmed.ncbi.nlm.nih.gov/25891173",
    },
    {
        "id": "SRC-COMBI-AD-LONG-2017",
        "url": "https://pubmed.ncbi.nlm.nih.gov/28891408",
        "doi_fallback": "https://doi.org/10.1056/NEJMoa1708539",
        "pubmed_fallback": "https://pubmed.ncbi.nlm.nih.gov/28891408",
    },
]


def probe_head(url: str) -> dict:
    """HEAD with retries. Returns {status_code, final_url, error}."""
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
    return {"status_code": None, "final_url": None, "error": last_err}


def main() -> int:
    results = []
    for t in TARGETS:
        primary = probe_head(t["url"]) if t["url"] else {
            "status_code": None,
            "final_url": None,
            "error": "no-url",
        }
        record = {
            "id": t["id"],
            "url": t["url"],
            "primary": primary,
            "doi_fallback": None,
            "pubmed_fallback": None,
        }
        # Fallback chain: DOI → PubMed canonical (per chunk brief).
        if t["url"] and primary.get("status_code") == 403:
            if t["doi_fallback"]:
                record["doi_fallback"] = probe_head(t["doi_fallback"])
            if (
                t["pubmed_fallback"]
                and (
                    record["doi_fallback"] is None
                    or record["doi_fallback"].get("status_code") == 403
                )
                and t["pubmed_fallback"] != t["url"]
            ):
                record["pubmed_fallback"] = probe_head(t["pubmed_fallback"])
        results.append(record)
    json.dump(results, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
