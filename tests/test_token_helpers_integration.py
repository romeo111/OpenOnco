"""Integration tests for `scripts/_token_helpers` against realistic fixtures.

`tests/test_token_round_trip.py` covers the synthesizable round-trip
contract (small + complex + unicode inputs, deterministic ordering, URL
safety on a hand-built dict). This module focuses on the on-disk
fixtures shipped in `examples/` so that we catch regressions caused by
real-world payload shape (NGS variants, prior-line lists, etc.) blowing
past the QR-25 capacity.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts._token_helpers import decode, encode


REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = REPO_ROOT / "examples"

# QR-25 holds ~2300 chars of URL — the token itself must clear 1500 to
# leave room for the host + path + base64 padding.
QR25_TOKEN_BUDGET = 1500


def _load(name: str) -> dict:
    p = EXAMPLES / name
    if not p.exists():
        pytest.skip(f"Fixture missing: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def test_encode_csd_1_demo_patient_under_qr_25():
    """Canonical CSD-1 demo (mCRC + BRAF V600E + NGS report) fits in
    the QR-25 budget."""
    patient = _load("patient_csd_1_demo_braf_mcrc.json")
    token = encode(patient)
    assert len(token) <= QR25_TOKEN_BUDGET, (
        f"CSD-1 demo token is {len(token)} chars; budget is {QR25_TOKEN_BUDGET}"
    )


def test_encode_dlbcl_low_ipi_under_qr_25():
    """A larger lymphoma fixture also fits — protects against a
    regression that bloats serialization (e.g. accidentally re-adding
    whitespace to json.dumps separators)."""
    patient = _load("patient_dlbcl_low_ipi.json")
    token = encode(patient)
    assert len(token) <= QR25_TOKEN_BUDGET, (
        f"DLBCL low-IPI token is {len(token)} chars; budget is {QR25_TOKEN_BUDGET}"
    )


def test_encode_decode_preserves_all_keys():
    """Every top-level key in the original fixture survives encode →
    decode round-trip — this is the contract the /try.html browser-side
    decoder relies on."""
    patient = _load("patient_csd_1_demo_braf_mcrc.json")
    decoded = decode(encode(patient))
    assert decoded is not None
    assert set(decoded.keys()) == set(patient.keys()), (
        f"Keys diverged: missing={set(patient.keys()) - set(decoded.keys())}, "
        f"added={set(decoded.keys()) - set(patient.keys())}"
    )
    # Deep equality for good measure (round_trip tests already cover
    # this on synthetic dicts; we duplicate the assertion against the
    # on-disk fixture because real-world payloads have bitten us before).
    assert decoded == patient


def test_encoded_token_is_url_safe_strict():
    """Encoded token uses only the URL-safe base64 alphabet
    (`A-Za-z0-9-_`). No `+`, `/`, or `=` should appear — `=` padding is
    stripped by `encode()` and re-added by `decode()`."""
    patient = _load("patient_csd_1_demo_braf_mcrc.json")
    token = encode(patient)
    forbidden = set(token) & set("+/=")
    assert not forbidden, f"Token contains non-URL-safe chars: {forbidden}"
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")
    leftover = set(token) - allowed
    assert not leftover, f"Token contains chars outside URL-safe alphabet: {leftover}"


def test_decode_truncated_token_returns_none():
    """A token truncated mid-stream must decode to `None` rather than
    crash. The browser-side decoder uses the same contract."""
    patient = _load("patient_csd_1_demo_braf_mcrc.json")
    token = encode(patient)
    truncated = token[:50]
    assert decode(truncated) is None


def test_decode_corrupted_payload_returns_none():
    """Same fixture, but flip one character mid-stream. Decode should
    return None — gzip will raise CRC mismatch internally."""
    patient = _load("patient_csd_1_demo_braf_mcrc.json")
    token = encode(patient)
    # Replace a middle char with one that's still URL-safe (so base64
    # decode succeeds) but breaks the gzip stream.
    midpoint = len(token) // 2
    swap = "A" if token[midpoint] != "A" else "B"
    corrupted = token[:midpoint] + swap + token[midpoint + 1:]
    assert decode(corrupted) is None
