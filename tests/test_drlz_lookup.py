"""Tests for the Держреєстр ЛЗ (drlz.com.ua) CSV ingestion.

Light tests — they do NOT hit the network. Instead they construct a tiny
synthetic cp1251-encoded CSV in a temp dir and exercise iter_records()
+ match_drug() against it.

Network smoke test (`download_csv()` → real CSV) is out of scope for
unit tests — run manually with:
    python -m knowledge_base.ingestion.drlz_lookup --refresh
"""

from __future__ import annotations

from pathlib import Path

import pytest

from knowledge_base.ingestion.drlz_lookup import (
    DrlzRecord,
    iter_records,
    match_drug,
)


# Synthetic 3-row CSV mirroring the real drlz columns (35+ cols, semicolon
# delimited, cp1251). We populate only the indices the parser actually reads.
def _make_fixture_csv(tmp: Path) -> Path:
    headers = ["ID"] + [f"col{i}" for i in range(1, 36)]
    rows = [
        [
            "ID-001",  # 0 = id
            "БОРТЕБІН",  # 1 = trade_name
            "Bortezomib",  # 2 = inn
            "порошок 3.5 мг",  # 3 = form
            "",  # 4
            "ТОВ Тест",  # 5 = manufacturer
            "",  # 6
            "L01XX32",  # 7 = atc1
            "",  # 8
            "",  # 9
            "UA/0001/01/01",  # 10 = registration_cert_number
            "01.01.2020",  # 11 = registration_issue_date
        ] + ["" for _ in range(12, 31)] + ["02.07.2030"]  # 31 = expiry
        + ["", "", "C90.0"],  # 32, 33, 34 = icd_code
        [
            "ID-002",
            "ДАРЗАЛЕКС",
            "Daratumumab",
            "конц. для розчину 100 мг",
            "", "Janssen", "", "L01FC01", "", "",
            "UA/0002/01/01", "10.10.2022",
        ] + ["" for _ in range(12, 31)] + ["09.04.2027", "", "", "C90.0"],
        [
            "ID-003",
            "СТАРИЙ ПРЕПАРАТ",
            "Obsoletum",
            "таблетки",
            "", "ТОВ", "", "X99XX99", "", "",
            "UA/0003/01/01", "01.01.2010",
        ] + ["" for _ in range(12, 31)] + ["01.01.2015", "", "", ""],  # expired
    ]
    out = tmp / "reestr.csv"
    with out.open("w", encoding="cp1251", errors="replace", newline="") as fh:
        fh.write(";".join(f'"{h}"' for h in headers) + "\n")
        for r in rows:
            fh.write(";".join(f'"{v}"' for v in r) + "\n")
    return out


def test_iter_records_parses_three_rows(tmp_path: Path):
    csv = _make_fixture_csv(tmp_path)
    recs = list(iter_records(csv))
    assert len(recs) == 3
    assert recs[0].id == "ID-001"
    assert recs[0].inn == "Bortezomib"
    assert recs[0].atc_codes == ["L01XX32"]
    assert recs[0].registration_cert_expiry == "02.07.2030"


def test_match_by_inn_substring(tmp_path: Path):
    csv = _make_fixture_csv(tmp_path)
    out = match_drug("Bortezomib", csv_path=csv, by="inn")
    assert len(out) == 1
    assert out[0].trade_name == "БОРТЕБІН"


def test_match_by_atc(tmp_path: Path):
    csv = _make_fixture_csv(tmp_path)
    out = match_drug("L01FC01", csv_path=csv, by="atc")
    assert len(out) == 1
    assert out[0].inn == "Daratumumab"


def test_match_by_trade_name(tmp_path: Path):
    csv = _make_fixture_csv(tmp_path)
    out = match_drug("ДАРЗАЛЕКС", csv_path=csv, by="trade_name")
    assert len(out) == 1
    assert out[0].inn == "Daratumumab"


def test_only_active_default_excludes_expired(tmp_path: Path):
    csv = _make_fixture_csv(tmp_path)
    out = match_drug("Obsoletum", csv_path=csv, by="inn")
    assert len(out) == 0  # expired registration filtered out
    out = match_drug(
        "Obsoletum", csv_path=csv, by="inn", only_active=False
    )
    assert len(out) == 1


def test_iter_records_missing_csv_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        list(iter_records(tmp_path / "does-not-exist.csv"))


def test_drlz_record_is_active_with_no_expiry():
    r = DrlzRecord(id="X", trade_name="T", inn="I")
    assert r.is_active()  # missing expiry → active


def test_match_unknown_field_raises(tmp_path: Path):
    csv = _make_fixture_csv(tmp_path)
    with pytest.raises(ValueError):
        match_drug("X", csv_path=csv, by="bogus_field")
