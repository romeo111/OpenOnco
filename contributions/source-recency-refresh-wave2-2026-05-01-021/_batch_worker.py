"""Wave-2 source recency HEAD checker.

Per chunk source-recency-refresh-wave2-2026-05-01-021:
- httpx HEAD with UA Mozilla/5.0 (compatible; OpenOnco-recency-bot)
- 30s timeout, 3 retries, follow_redirects=True
- 200 -> upsert; 3xx -> upsert+redirect; 404 -> dead;
  403 -> DOI HEAD fallback -> PubMed canonical HEAD fallback ->
        if all fail, unreachable.blocked (no current_as_of bump)
- No URL -> unreachable.no_url
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, field
from typing import Optional

import httpx

UA = "Mozilla/5.0 (compatible; OpenOnco-recency-bot)"
TIMEOUT = 30.0
RETRIES = 3


@dataclass
class CheckOutcome:
    sid: str
    primary_url: Optional[str]
    pmid: Optional[str]
    doi: Optional[str]
    status: str = ""           # "ok" | "redirect" | "dead" | "blocked" | "no_url"
    final_url: Optional[str] = None
    status_code: Optional[int] = None
    fallback_chain: list[dict] = field(default_factory=list)
    error: Optional[str] = None


def head_once(client: httpx.Client, url: str) -> tuple[Optional[int], Optional[str], Optional[str]]:
    """Return (status_code, final_url, error). Final URL is reported via response.url."""
    try:
        r = client.head(url, follow_redirects=True, timeout=TIMEOUT)
        return r.status_code, str(r.url), None
    except httpx.HTTPError as exc:
        return None, None, f"{type(exc).__name__}: {exc}"


def head_with_retry(client: httpx.Client, url: str) -> tuple[Optional[int], Optional[str], Optional[str]]:
    last_err = None
    for attempt in range(RETRIES):
        code, final_url, err = head_once(client, url)
        if code is not None:
            return code, final_url, None
        last_err = err
        time.sleep(0.5 * (2 ** attempt))
    return None, None, last_err


def check(item: CheckOutcome) -> None:
    headers = {"User-Agent": UA}
    with httpx.Client(headers=headers) as client:
        if not item.primary_url:
            item.status = "no_url"
            item.error = "Source has no URL field"
            return

        code, final_url, err = head_with_retry(client, item.primary_url)
        item.fallback_chain.append({
            "step": "primary_url",
            "url": item.primary_url,
            "status_code": code,
            "final_url": final_url,
            "error": err,
        })

        if code is not None and 200 <= code < 300:
            item.status = "ok"
            item.status_code = code
            item.final_url = final_url
            return
        if code is not None and 300 <= code < 400:
            item.status = "redirect"
            item.status_code = code
            item.final_url = final_url
            return
        if code == 404:
            item.status = "dead"
            item.status_code = code
            item.final_url = final_url
            return

        # 403 or other failure: fallback to DOI
        if code == 403 or code is None:
            if item.doi:
                doi_url = f"https://doi.org/{item.doi}"
                code2, final2, err2 = head_with_retry(client, doi_url)
                item.fallback_chain.append({
                    "step": "doi_fallback",
                    "url": doi_url,
                    "status_code": code2,
                    "final_url": final2,
                    "error": err2,
                })
                if code2 is not None and 200 <= code2 < 400:
                    item.status = "ok" if code2 < 300 else "redirect"
                    item.status_code = code2
                    item.final_url = final2
                    return
            if item.pmid:
                pm_url = f"https://pubmed.ncbi.nlm.nih.gov/{item.pmid}/"
                code3, final3, err3 = head_with_retry(client, pm_url)
                item.fallback_chain.append({
                    "step": "pubmed_fallback",
                    "url": pm_url,
                    "status_code": code3,
                    "final_url": final3,
                    "error": err3,
                })
                if code3 is not None and 200 <= code3 < 400:
                    item.status = "ok" if code3 < 300 else "redirect"
                    item.status_code = code3
                    item.final_url = final3
                    return
            item.status = "blocked"
            item.status_code = code
            item.error = f"primary {code}; DOI/PubMed fallbacks did not resolve"
            return

        # other non-403 failures with code
        item.status = "blocked"
        item.status_code = code
        item.error = f"unexpected status {code}"


SOURCES = [
    CheckOutcome(
        sid="SRC-EXPLORER",
        primary_url=None,
        pmid=None,
        doi=None,
    ),
    CheckOutcome(
        sid="SRC-SSG-XVIII",
        primary_url=None,
        pmid=None,
        doi=None,
    ),
    CheckOutcome(
        sid="SRC-COMBI-V-ROBERT-2015",
        primary_url="https://pubmed.ncbi.nlm.nih.gov/25399551",
        pmid="25399551",
        doi="10.1056/NEJMoa1412690",
    ),
    CheckOutcome(
        sid="SRC-ALEX-PETERS-2017",
        primary_url="https://pubmed.ncbi.nlm.nih.gov/28586279",
        pmid="28586279",
        doi="10.1056/NEJMoa1704795",
    ),
    CheckOutcome(
        sid="SRC-SOLO1-MOORE-2018",
        primary_url="https://www.nejm.org/doi/full/10.1056/NEJMoa1810858",
        pmid="30345884",
        doi="10.1056/NEJMoa1810858",
    ),
]


def main() -> None:
    results = []
    for src in SOURCES:
        print(f"=== {src.sid} ===", flush=True)
        check(src)
        print(f"  status={src.status} code={src.status_code} final_url={src.final_url}", flush=True)
        for step in src.fallback_chain:
            print(f"    {step}", flush=True)
        results.append({
            "id": src.sid,
            "primary_url": src.primary_url,
            "status": src.status,
            "status_code": src.status_code,
            "final_url": src.final_url,
            "error": src.error,
            "chain": src.fallback_chain,
        })
    with open("_recency_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("\nWritten _recency_results.json", flush=True)


if __name__ == "__main__":
    main()
