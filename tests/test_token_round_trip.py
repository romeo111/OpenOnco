"""Round-trip tests for scripts/_token_helpers — patient profile encode/decode.

Covers the URL-hash transport used by the QR-code / case-token flow
(CSD-3). The browser-side decoder in /try.html mirrors this logic, so
these tests double as a contract for that JS implementation.
"""

from __future__ import annotations

import pytest

from scripts._token_helpers import decode, encode


def test_round_trip_simple():
    patient = {"id": "PT-test", "age": 64, "sex": "M"}
    assert decode(encode(patient)) == patient


def test_round_trip_complex():
    """Realistic patient with nested biomarkers + labs."""
    patient = {
        "patient_id": "PT-csd1-demo",
        "demographics": {"age": 64, "sex": "male", "ecog": 1},
        "disease_id": "DIS-CRC",
        "biomarkers": {
            "BRAF": "V600E",
            "KRAS": "wildtype",
            "TP53": "pathogenic R175H",
        },
        "labs": {"hgb": 11.2, "platelets": 145, "creatinine": 1.1, "cea": 412},
        "imaging": "Multiple liver metastases",
        "prior_therapy": ["FOLFOX × 8 cycles → progression at 5mo"],
    }
    assert decode(encode(patient)) == patient


def test_decode_invalid_returns_none():
    assert decode("not-a-valid-token") is None
    assert decode("") is None
    assert decode("XXX@#$") is None


def test_token_url_safe():
    """Encoded token contains only URL-safe characters."""
    patient = {"id": "PT-test", "complex": "value with spaces & symbols !@#"}
    token = encode(patient)
    # URL-safe base64: only A-Za-z0-9-_
    assert all(c.isalnum() or c in "-_" for c in token)


def test_token_size_under_1500():
    """Realistic patient profile fits the QR-25 capacity."""
    realistic_patient = {
        "patient_id": "PT-csd1-demo",
        "demographics": {
            "age": 64, "sex": "male", "ecog": 1,
            "weight_kg": 78, "height_cm": 175,
        },
        "disease_id": "DIS-CRC",
        "biomarkers": {
            "BRAF": "V600E", "KRAS": "wildtype",
            "TP53": "pathogenic R175H", "APC": "R1450*",
            "MSI": "MSS", "TMB": 8,
        },
        "labs": {
            "hgb": 11.2, "platelets": 145, "wbc": 6.7, "anc": 3.4,
            "creatinine": 1.1, "alt": 24, "ast": 28, "bilirubin": 0.7,
            "albumin": 3.8, "cea": 412, "ldh": 285,
        },
        "imaging_summary": (
            "CT: liver-dominant metastases, 3 lesions, largest 4.2 cm; "
            "mesenteric LN involvement"
        ),
        "comorbidities": [
            "HTN controlled", "T2DM A1c 7.2",
            "former smoker 20 PY quit 8yr",
        ],
        "prior_therapy": [
            "FOLFOX-6 × 8 cycles 2026-Q3 → progression at 5mo",
        ],
    }
    token = encode(realistic_patient)
    assert len(token) < 1500, f"Token {len(token)} chars exceeds QR-25 cap"


def test_round_trip_unicode():
    """Cyrillic + emoji + non-ASCII survive the round-trip cleanly."""
    patient = {
        "patient_id": "PT-ua-test",
        "primary_site_ua": "пряма кишка",
        "comment": "Стан: ECOG 1 ✓",
    }
    assert decode(encode(patient)) == patient


def test_encode_deterministic():
    """Same dict → same token, regardless of key insertion order."""
    a = {"a": 1, "b": 2, "c": 3}
    b = {"c": 3, "b": 2, "a": 1}
    assert encode(a) == encode(b)


def test_csd1_demo_patient_round_trip():
    """The canonical CSD-1 demo patient (BRAF V600E mCRC) round-trips
    cleanly and produces a token small enough for the QR.
    """
    import json
    from pathlib import Path

    fixture = Path(__file__).resolve().parent.parent / "examples" / "patient_csd_1_demo_braf_mcrc.json"
    if not fixture.exists():
        pytest.skip(f"Fixture missing: {fixture}")
    patient = json.loads(fixture.read_text(encoding="utf-8"))
    token = encode(patient)
    assert decode(token) == patient
    # /try.html#p=<token> must fit a QR-25 (≈2300 chars URL).
    full_url = f"https://openonco.info/try.html#p={token}"
    assert len(full_url) < 2300, f"URL {len(full_url)} chars exceeds QR-25 cap"
