"""Submit deployed canonical sitemap URLs to IndexNow after verifying ownership.

The hosted key is an IndexNow ownership proof, not an account credential.
This command does not run during builds and does not imply indexing.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

HOST = "openonco.info"
BASE = f"https://{HOST}/"
ENDPOINT = "https://api.indexnow.org/indexnow"
MAX_URLS_PER_POST = 10_000


def payload_for(site: Path) -> dict:
    candidates = [p for p in site.glob("*.txt") if re.fullmatch(r"[a-f0-9]{32}", p.stem)]
    if len(candidates) != 1:
        raise ValueError("Expected exactly one hosted IndexNow key file")
    key_file = candidates[0]
    key = key_file.read_text(encoding="utf-8").strip()
    if key != key_file.stem:
        raise ValueError("IndexNow key filename and content must match")
    urls = sorted({e.text for e in ET.parse(site / "sitemap.xml").findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")})
    if not urls or any(not u.startswith(BASE) for u in urls):
        raise ValueError("Expected canonical URLs on openonco.info")
    return {"host": HOST, "key": key, "keyLocation": BASE + key_file.name, "urlList": urls}


def batches(payload: dict):
    """IndexNow permits at most 10,000 URLs in each POST."""
    urls = payload["urlList"]
    for start in range(0, len(urls), MAX_URLS_PER_POST):
        yield {**payload, "urlList": urls[start:start + MAX_URLS_PER_POST]}


def submit(payload: dict) -> int:
    # Check the live proof before sending, to avoid submitting before deployment.
    with urlopen(payload["keyLocation"], timeout=30) as response:
        if response.read().decode("utf-8").strip() != payload["key"]:
            raise ValueError("Live IndexNow ownership proof does not match")
    request = Request(ENDPOINT, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "OpenOnco-discovery/1.0"}, method="POST")
    with urlopen(request, timeout=60) as response:
        return response.status


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=Path("docs"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    payload = payload_for(args.site)
    if args.dry_run:
        print(json.dumps({"urls": len(payload["urlList"]), "batches": len(list(batches(payload))), "submitted": False}))
        return
    statuses = []
    for number, batch in enumerate(batches(payload), start=1):
        status = submit(batch)
        statuses.append(status)
        print(json.dumps({"batch": number, "urls": len(batch["urlList"]), "http_status": status}))
    print(json.dumps({"urls": len(payload["urlList"]), "batches": len(statuses), "received": all(status in (200, 202) for status in statuses), "indexing_confirmed": False}))


if __name__ == "__main__":
    main()
