"""Recency check worker for source-recency-refresh-wave2-2026-05-01-008.

Per chunk brief: httpx GET with desktop UA, 30s timeout, 3 retries. Maps
status codes to outcomes:
  200       -> upsert, bump current_as_of if old
  301/302   -> upsert + url_redirected_from
  404/410   -> unreachable.yaml (dead, replacement_needed)
  403       -> try DOI fallback; if 200 -> upsert; else unreachable
                (blocked_by_bot_protection, do NOT bump current_as_of)
  no URL    -> unreachable.yaml with PMID/DOI suggestion
"""
from __future__ import annotations

import json
import sys
import time

import httpx

UA = "Mozilla/5.0 (compatible; OpenOnco-recency-bot)"
HEADERS = {"User-Agent": UA}

TARGETS = [
    {
        "id": "SRC-COG",
        "url": None,
        "doi": None,
        "pmid": None,
    },
    {
        "id": "SRC-NCCN-BCELL-2025",
        "url": "https://www.nccn.org/guidelines/guidelines-detail?category=1&id=1480",
        "doi": None,
        "pmid": None,
    },
    {
        "id": "SRC-COIFFIER-2012-ROMIDEPSIN-PTCL",
        "url": "https://pubmed.ncbi.nlm.nih.gov/22271479",
        "doi": "10.1200/JCO.2011.37.4223",
        "pmid": "22271479",
    },
    {
        "id": "SRC-MONALEESA-2-HORTOBAGYI-2016",
        "url": "https://pubmed.ncbi.nlm.nih.gov/27717303",
        "doi": "10.1056/NEJMoa1609709",
        "pmid": "27717303",
    },
    {
        "id": "SRC-MURANO-SEYMOUR-2018",
        "url": "https://pubmed.ncbi.nlm.nih.gov/29562156",
        "doi": "10.1056/NEJMoa1713976",
        "pmid": "29562156",
    },
]


def fetch(url: str, timeout: float = 30.0, retries: int = 3) -> dict:
    last_exc = None
    for attempt in range(retries):
        try:
            with httpx.Client(
                headers=HEADERS,
                timeout=timeout,
                follow_redirects=False,
            ) as client:
                r = client.get(url)
                return {
                    "status_code": r.status_code,
                    "final_url": str(r.url),
                    "location": r.headers.get("location"),
                    "ok": r.status_code < 400,
                }
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            time.sleep(2 ** attempt)
    return {
        "status_code": None,
        "final_url": url,
        "location": None,
        "ok": False,
        "error": str(last_exc),
    }


def fetch_redirects(url: str) -> dict:
    """Follow redirects to capture final 200/4xx and the chain."""
    last_exc = None
    for attempt in range(3):
        try:
            with httpx.Client(
                headers=HEADERS,
                timeout=30.0,
                follow_redirects=True,
            ) as client:
                r = client.get(url)
                return {
                    "status_code": r.status_code,
                    "final_url": str(r.url),
                    "history": [str(h.url) for h in r.history],
                    "ok": r.status_code < 400,
                }
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            time.sleep(2 ** attempt)
    return {
        "status_code": None,
        "final_url": url,
        "history": [],
        "ok": False,
        "error": str(last_exc),
    }


def main() -> int:
    results = []
    for tgt in TARGETS:
        out = {"id": tgt["id"], "url": tgt["url"], "doi": tgt["doi"], "pmid": tgt["pmid"]}
        if tgt["url"] is None:
            out["outcome"] = "no_url_on_stub"
            results.append(out)
            print(f"[{tgt['id']}] no URL on stub -> unreachable")
            continue
        # Initial GET without follow.
        first = fetch(tgt["url"])
        out["initial"] = first
        sc = first["status_code"]
        print(f"[{tgt['id']}] initial GET status={sc}")
        if sc and 300 <= sc < 400:
            # Follow.
            followed = fetch_redirects(tgt["url"])
            out["followed"] = followed
            print(f"  redirected -> status={followed['status_code']} final={followed['final_url']}")
        elif sc == 403 and tgt.get("doi"):
            doi_url = f"https://doi.org/{tgt['doi']}"
            print(f"  403 -> DOI fallback {doi_url}")
            doi_res = fetch_redirects(doi_url)
            out["doi_fallback"] = {"url": doi_url, **doi_res}
            print(f"  DOI status={doi_res['status_code']} final={doi_res['final_url']}")
        results.append(out)
        time.sleep(1)
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
