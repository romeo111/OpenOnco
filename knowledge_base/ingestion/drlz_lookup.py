"""Держреєстр ЛЗ (drlz.com.ua) — official CSV ingestion.

UPDATED 2026-04-25: scraping path replaced with official CSV download.

The Ministry of Health publishes the full Державний реєстр лікарських
засобів as a CSV file (cp1251-encoded, semicolon-separated, ~16K rows
× 35 columns) at two equivalent endpoints:

  - http://www.drlz.com.ua/ibp/zvity.nsf/all/zvit/$file/reestr.csv
    (canonical, updated daily by ДЕЦ МОЗ — ~12 MB)
  - https://data.gov.ua/dataset/fded13b8-4e2c-4c48-bf14-65d0e3106463/
    resource/.../download/reestr-lz.csv
    (official mirror on Ukrainian Open Data portal, Creative Commons
    Attribution license)

Both are public, no API key, no rate limit. We use the data.gov.ua
mirror by default for license clarity (CC-BY) and fall back to the
canonical drlz endpoint if the mirror is stale or unreachable.

Schema (35 columns; we keep the clinically-relevant subset):
    ID                                — registration number
    Торгівельне найменування          — trade name (UA)
    Міжнародне непатентоване найменування — INN / MNN (UA)
    Форма випуску                     — dosage form
    Виробник                          — manufacturer
    АТС код 1 / АТС код 2 / АТС код 3 — ATC classification (1-3 levels)
    Реєстраційне посвідчення №        — registration certificate №
    Дата закінчення дії               — expiry date
    Дата видання                      — issue date
    Код МКХ                           — ICD code (linked condition)

Public entry point — `match_drug(query, csv_path)` finds matching
rows by INN, trade name, or ATC. Used at Drug entity creation/refresh
time to populate Drug.regulatory_status.ukraine_registration.

CLI:
    python -m knowledge_base.ingestion.drlz_lookup --refresh
    python -m knowledge_base.ingestion.drlz_lookup --inn "Бортезоміб"
    python -m knowledge_base.ingestion.drlz_lookup --atc "L01XC"
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Optional


DEFAULT_CACHE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "knowledge_base"
    / "cache"
    / "drlz"
    / "reestr.csv"
)

DRLZ_CANONICAL_URL = (
    "http://www.drlz.com.ua/ibp/zvity.nsf/all/zvit/$file/reestr.csv"
)
DRLZ_OPENDATA_URL = (
    "https://data.gov.ua/dataset/fded13b8-4e2c-4c48-bf14-65d0e3106463/"
    "resource/17f245cd-86f7-404e-8ee1-dfd0e186ee6a/download/reestr-lz.csv"
)


@dataclass
class DrlzRecord:
    id: str
    trade_name: str
    inn: str
    form: Optional[str] = None
    manufacturer: Optional[str] = None
    atc_codes: list[str] = field(default_factory=list)
    registration_cert_number: Optional[str] = None
    registration_cert_expiry: Optional[str] = None
    registration_issue_date: Optional[str] = None
    icd_code: Optional[str] = None

    def is_active(self, today: Optional[str] = None) -> bool:
        """A registration is active if its expiry date has not passed.
        Records without an explicit expiry are treated as active."""
        if not self.registration_cert_expiry:
            return True
        try:
            today_dt = (
                datetime.strptime(today, "%Y-%m-%d")
                if today
                else datetime.now(timezone.utc).replace(tzinfo=None)
            )
            exp = datetime.strptime(self.registration_cert_expiry, "%d.%m.%Y")
            return exp >= today_dt
        except (ValueError, TypeError):
            return True


def download_csv(
    out_path: Path = DEFAULT_CACHE_PATH,
    *,
    prefer_opendata: bool = True,
) -> Path:
    """Fetch the latest Держреєстр CSV. Tries data.gov.ua first
    (CC-BY mirror) by default, falls back to canonical drlz.com.ua.
    Saves to `out_path` (parents created)."""
    import httpx

    out_path.parent.mkdir(parents=True, exist_ok=True)
    urls = (
        [DRLZ_OPENDATA_URL, DRLZ_CANONICAL_URL]
        if prefer_opendata
        else [DRLZ_CANONICAL_URL, DRLZ_OPENDATA_URL]
    )
    last_err: Optional[Exception] = None
    for url in urls:
        try:
            with httpx.stream(
                "GET", url, timeout=180.0, follow_redirects=True
            ) as resp:
                resp.raise_for_status()
                with out_path.open("wb") as fh:
                    for chunk in resp.iter_bytes():
                        fh.write(chunk)
            return out_path
        except Exception as exc:
            last_err = exc
            continue
    raise RuntimeError(
        f"Failed to download DRLZ CSV from any URL: {last_err}"
    )


def iter_records(csv_path: Path = DEFAULT_CACHE_PATH) -> Iterator[DrlzRecord]:
    """Stream-parse the CSV. Encoding is cp1251 (Windows-1251)."""
    if not csv_path.exists():
        raise FileNotFoundError(
            f"DRLZ CSV not found at {csv_path}. Run --refresh first."
        )
    with csv_path.open(
        "r", encoding="cp1251", newline="", errors="replace"
    ) as fh:
        reader = csv.reader(fh, delimiter=";", quotechar='"')
        try:
            next(reader)  # header
        except StopIteration:
            return
        for row in reader:
            if not row or not row[0]:
                continue

            def get(i: int) -> Optional[str]:
                return row[i].strip() if i < len(row) and row[i] else None

            atc = [c for c in (get(7), get(8), get(9)) if c]
            yield DrlzRecord(
                id=get(0) or "",
                trade_name=get(1) or "",
                inn=get(2) or "",
                form=get(3),
                manufacturer=get(5),
                atc_codes=atc,
                registration_cert_number=get(10),
                registration_cert_expiry=get(31) or get(30),
                registration_issue_date=get(11),
                icd_code=get(34),
            )


def match_drug(
    query: str,
    csv_path: Path = DEFAULT_CACHE_PATH,
    *,
    by: str = "inn",
    case_insensitive: bool = True,
    only_active: bool = True,
) -> list[DrlzRecord]:
    """Find matching DRLZ records by INN (default), trade_name, or atc.

    `query` is matched as substring. Returns all matches; caller decides
    which to use.
    """
    target = query.lower() if case_insensitive else query
    out: list[DrlzRecord] = []
    for rec in iter_records(csv_path):
        if by == "inn":
            field_val = rec.inn
        elif by == "trade_name":
            field_val = rec.trade_name
        elif by == "atc":
            field_val = " ".join(rec.atc_codes)
        else:
            raise ValueError(f"Unknown match field: {by}")
        haystack = field_val.lower() if case_insensitive else field_val
        if target and target in haystack:
            if only_active and not rec.is_active():
                continue
            out.append(rec)
    return out


def _cli(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m knowledge_base.ingestion.drlz_lookup",
        description=(
            "Держреєстр ЛЗ (drlz.com.ua) lookup — verifies a drug is "
            "currently registered in Ukraine. Uses the official CSV "
            "download (no scraping)."
        ),
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Download the latest CSV from data.gov.ua (CC-BY mirror).",
    )
    parser.add_argument(
        "--inn",
        type=str,
        help="Search by international non-proprietary name (substring).",
    )
    parser.add_argument(
        "--trade-name",
        type=str,
        help="Search by trade name (substring).",
    )
    parser.add_argument(
        "--atc",
        type=str,
        help="Search by ATC code (substring, e.g. 'L01XC18' for daratumumab).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Max records to print (default 20).",
    )
    parser.add_argument(
        "--include-expired",
        action="store_true",
        help="Include records whose registration certificate expired.",
    )
    args = parser.parse_args(argv)

    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

    if args.refresh:
        path = download_csv()
        size_mb = path.stat().st_size / 1_000_000
        print(f"Downloaded {size_mb:.1f} MB -> {path}")
        return 0

    if not (args.inn or args.trade_name or args.atc):
        parser.error("Provide --refresh or one of --inn/--trade-name/--atc")

    if args.inn:
        results = match_drug(
            args.inn, by="inn", only_active=not args.include_expired
        )
    elif args.trade_name:
        results = match_drug(
            args.trade_name,
            by="trade_name",
            only_active=not args.include_expired,
        )
    else:
        results = match_drug(
            args.atc, by="atc", only_active=not args.include_expired
        )

    print(
        f"Знайдено: {len(results)} записів "
        f"(показано {min(args.limit, len(results))})"
    )
    for r in results[: args.limit]:
        atc = ", ".join(r.atc_codes) or "—"
        exp = r.registration_cert_expiry or "—"
        print(
            f"  ID={r.id[:8]:<10} INN={(r.inn[:40]):<40} "
            f"Trade={(r.trade_name[:30]):<30} ATC={atc:<25} exp={exp}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(_cli())


__all__ = [
    "DEFAULT_CACHE_PATH",
    "DRLZ_CANONICAL_URL",
    "DRLZ_OPENDATA_URL",
    "DrlzRecord",
    "download_csv",
    "iter_records",
    "match_drug",
]
