"""Держреєстр ЛЗ (drlz.com.ua) per-drug lookup — skeleton.

Per SOURCE_INGESTION_SPEC §15.3. Purpose: verify a drug is registered
in Ukraine (and still active, not withdrawn).

No bulk download — only per-drug web search UI. Our approach:
    1. At Drug entity creation, lookup by MNN (or trade name)
    2. Populate Drug.regulatory_status.ukraine_registration block
    3. Quarterly re-verification cron iterates all Drugs and re-queries

Implementation requires HTML scraping of drlz.com.ua search results.
May be brittle — website redesigns break it. Alert path needed.

TODO:
    [ ] Implement search-by-MNN via POST to drlz.com.ua form endpoint
    [ ] Parse result table (HTML parser)
    [ ] Extract registration number, date, holder, status
    [ ] Update corresponding Drug YAML in place (or emit a diff PR)
"""

from __future__ import annotations

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Держреєстр ЛЗ lookup — SKELETON.")
    parser.add_argument("mnn", help="International non-proprietary name (e.g. 'Rituximab')")
    args = parser.parse_args()
    print("drlz_lookup: skeleton only, not implemented.", file=sys.stderr)
    print(f"  Query MNN: {args.mnn}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
