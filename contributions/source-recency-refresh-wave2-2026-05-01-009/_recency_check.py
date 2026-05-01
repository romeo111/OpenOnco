"""One-shot recency check for chunk source-recency-refresh-wave2-2026-05-01-009.

Reads the five source URLs from this chunk's manifest, performs an HTTP GET
with the OpenOnco-recency-bot User-Agent, and prints structured outcomes.
This script is throwaway — it lives next to the audit YAML so the
maintainer can re-run it and reproduce the recency-check status codes.
"""

from __future__ import annotations

import json
import sys
import time
from typing import Any

import httpx

UA = "Mozilla/5.0 (compatible; OpenOnco-recency-bot)"
TIMEOUT = 30.0
RETRIES = 3

TARGETS = [
    {
        "id": "SRC-EANO-LGG-2024",
        "url": "https://pubmed.ncbi.nlm.nih.gov/33293629/",
        "doi": "10.1038/s41571-020-00447-z",
    },
    {
        "id": "SRC-NCCN-BONE-SARCOMA",
        "url": None,  # Stub source — no URL on file.
        "doi": None,
    },
    {
        "id": "SRC-COMFORT-I-VERSTOVSEK-2012",
        "url": "https://www.nejm.org/doi/full/10.1056/NEJMoa1110557",
        "doi": "10.1056/NEJMoa1110557",
    },
    {
        "id": "SRC-KEYNOTE-024-RECK-2016",
        "url": "https://pubmed.ncbi.nlm.nih.gov/27718847",
        "doi": "10.1056/NEJMoa1606774",
    },
    {
        "id": "SRC-BLAST-GOKBUGET-2018",
        "url": "https://ashpublications.org/blood/article/131/14/1522/36798",
        "doi": "10.1182/blood-2017-08-798322",
    },
]


def fetch(url: str) -> dict[str, Any]:
    """GET url with retry; follow redirects; return outcome dict."""
    headers = {"User-Agent": UA}
    last_err: str | None = None
    for attempt in range(1, RETRIES + 1):
        try:
            with httpx.Client(
                follow_redirects=True, timeout=TIMEOUT, headers=headers
            ) as client:
                r = client.get(url)
                final_url = str(r.url)
                redirected = final_url != url
                return {
                    "status_code": r.status_code,
                    "final_url": final_url,
                    "redirected": redirected,
                    "error": None,
                }
        except Exception as exc:  # noqa: BLE001
            last_err = f"{type(exc).__name__}: {exc}"
            time.sleep(2 * attempt)
    return {
        "status_code": None,
        "final_url": None,
        "redirected": False,
        "error": last_err or "unknown",
    }


def main() -> int:
    out: list[dict[str, Any]] = []
    for t in TARGETS:
        if not t["url"]:
            out.append(
                {
                    "id": t["id"],
                    "outcome": "no_url_on_file",
                    "url": None,
                    "doi": t["doi"],
                }
            )
            continue
        primary = fetch(t["url"])
        result: dict[str, Any] = {
            "id": t["id"],
            "url": t["url"],
            "doi": t["doi"],
            "primary": primary,
        }
        if primary["status_code"] == 403 and t["doi"]:
            doi_url = f"https://doi.org/{t['doi']}"
            result["doi_fallback"] = {"url": doi_url, **fetch(doi_url)}
        out.append(result)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
