"""One-off URL probe for chunk source-recency-refresh-wave2-2026-05-01-019.

Runs httpx HEAD against publisher URLs with the OpenOnco recency UA, 30s
timeout, 3 retries, follow_redirects=True. Per chunk-brief instruction:
HEAD is used (not GET) because wave-1 demonstrated HEAD passes publisher
bot-walls that GET triggers (PubMed/NEJM/Elsevier/JAMA/ASCO).

On HEAD 403, falls back to https://doi.org/<doi> HEAD, then
https://pubmed.ncbi.nlm.nih.gov/<pmid> HEAD before flagging blocked.

Prints JSON results — used to populate sidecar files. Mirrors the
probe-then-author worker pattern of
contributions/source-recency-refresh-2026-04-29-001/_batch_worker.py and
contributions/source-recency-refresh-wave2-2026-05-01-018/_recency_probe.py.
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
        "id": "SRC-ESMO-SARCOMA",
        "url": None,  # auto-stub, no top-level url field
        "doi": None,
        "pmid": None,
    },
    {
        "id": "SRC-SAVOIR",
        "url": None,  # auto-stub, no top-level url field
        "doi": None,
        "pmid": None,
    },
    {
        "id": "SRC-COBRIM-LARKIN-2014",
        "url": "https://pubmed.ncbi.nlm.nih.gov/25265494",
        "doi": "10.1056/NEJMoa1408868",
        "pmid": "25265494",
    },
    {
        "id": "SRC-RATIFY-STONE-2017",
        "url": "https://www.nejm.org/doi/full/10.1056/NEJMoa1614359",
        "doi": "10.1056/NEJMoa1614359",
        "pmid": "28644114",
    },
    {
        "id": "SRC-ELOQUENT-3-DIMOPOULOS-2018",
        "url": "https://pubmed.ncbi.nlm.nih.gov/30403938",
        "doi": "10.1056/NEJMoa1805762",
        "pmid": "30403938",
    },
]


def probe(url: str | None) -> dict:
    """HEAD with retries. Returns {status_code, final_url, error, redirect_history}."""
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
        primary = probe(t["url"])
        record = {
            "id": t["id"],
            "url": t["url"],
            "primary": primary,
            "doi_fallback": None,
            "pubmed_fallback": None,
        }
        if primary.get("status_code") == 403:
            if t.get("doi"):
                record["doi_fallback"] = probe(f"https://doi.org/{t['doi']}")
            if (
                record["doi_fallback"]
                and record["doi_fallback"].get("status_code") == 403
                and t.get("pmid")
            ):
                record["pubmed_fallback"] = probe(
                    f"https://pubmed.ncbi.nlm.nih.gov/{t['pmid']}"
                )
        results.append(record)
    json.dump(results, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
