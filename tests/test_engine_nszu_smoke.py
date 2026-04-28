"""Smoke tests for the NSZU availability lookup helper
(`knowledge_base/engine/_nszu.py`). Validates that the four well-known
drugs land on the expected status against representative patient
diseases:

  - Rituximab + DLBCL → covered (UA-registered, NSZU-reimbursed,
    DLBCL listed in `reimbursement_indications`).
  - Axicabtagene ciloleucel + DLBCL → not-registered (no РП in UA
    register).
  - Olaparib + ovarian → covered (BRCA1/2 ovarian maintenance is
    listed verbatim in indications).
  - Olaparib + pancreatic cancer → partial (registered+reimbursed
    drug, no pancreatic line in indications).
  - Teclistamab + multiple myeloma → not-registered (no РП).

Helper is render-time-only metadata; engine selection MUST NOT depend
on it (CHARTER §8.3 invariant). These tests run on the live KB so they
double as a contract-check on the drug YAMLs after the CSD-2 NSZU
verification batches.
"""

from __future__ import annotations

from pathlib import Path

from knowledge_base.engine._nszu import (
    NszuBadge,
    _disease_tokens,
    _indication_match,
    lookup_nszu_status,
    nszu_label,
)
from knowledge_base.validation.loader import load_content


REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"


def _kb():
    """Load the KB once per test (small; no caching needed for smoke)."""
    res = load_content(KB_ROOT)
    assert res.ok, f"KB did not load cleanly: {len(res.schema_errors)} schema errors"
    return res.entities_by_id


def _drug(entities, drug_id: str) -> dict:
    info = entities.get(drug_id)
    assert info is not None, f"Drug {drug_id} missing from KB"
    return info["data"]


def _disease_names(entities, disease_id: str) -> dict:
    info = entities.get(disease_id)
    assert info is not None, f"Disease {disease_id} missing from KB"
    return (info["data"].get("names") or {})


# ── Status assertions on real drug YAMLs ─────────────────────────────────


def test_rituximab_dlbcl_nszu_covered():
    """Rituximab + DLBCL: registered+reimbursed, indication string carries
    'Дифузна великоклітинна B-клітинна лімфома (R-CHOP)' which contains
    the disease's Ukrainian name → status='covered'."""
    entities = _kb()
    badge = lookup_nszu_status(
        _drug(entities, "DRUG-RITUXIMAB"),
        "DIS-DLBCL-NOS",
        disease_names=_disease_names(entities, "DIS-DLBCL-NOS"),
    )
    assert badge.status == "covered", badge
    assert badge.indication_match is not None
    assert badge.label.startswith("✓")
    assert badge.drug_id == "DRUG-RITUXIMAB"
    assert badge.notes_excerpt  # non-empty tooltip text


def test_axi_cel_dlbcl_nszu_not_registered():
    """Axicabtagene ciloleucel: no РП in UA → status='not-registered'."""
    entities = _kb()
    badge = lookup_nszu_status(
        _drug(entities, "DRUG-AXICABTAGENE-CILOLEUCEL"),
        "DIS-DLBCL-NOS",
        disease_names=_disease_names(entities, "DIS-DLBCL-NOS"),
    )
    assert badge.status == "not-registered", badge
    assert badge.indication_match is None
    assert badge.label.startswith("✗")


def test_olaparib_ovarian_nszu_covered():
    """Olaparib + ovarian carcinoma: registered+reimbursed, ovarian
    BRCA1/2 maintenance is enumerated in indications → 'covered'."""
    entities = _kb()
    badge = lookup_nszu_status(
        _drug(entities, "DRUG-OLAPARIB"),
        "DIS-OVARIAN",
        disease_names=_disease_names(entities, "DIS-OVARIAN"),
    )
    assert badge.status == "covered", badge
    assert badge.indication_match is not None
    # Sanity — the matched indication should mention oвaria/яєчник
    matched_lower = badge.indication_match.lower()
    assert "яєчник" in matched_lower or "ovarian" in matched_lower


def test_olaparib_pancreatic_nszu_partial():
    """Olaparib + pancreatic cancer: drug is registered+reimbursed but
    the pancreatic indication is explicitly NOT in the НСЗУ package
    (per drug.notes), so substring search misses → 'partial'.
    Surfaces the funding gap to the clinician."""
    entities = _kb()
    badge = lookup_nszu_status(
        _drug(entities, "DRUG-OLAPARIB"),
        "DIS-PANCREATIC",  # may or may not be in KB; tokens still derive cleanly
        disease_names={"preferred": "Pancreatic adenocarcinoma",
                       "ukrainian": "Аденокарцинома підшлункової залози"},
    )
    assert badge.status == "partial", badge
    assert badge.indication_match is None
    assert "не для цього показання" in badge.label


def test_teclistamab_mm_nszu_not_registered():
    """Teclistamab — no РП in UA register → 'not-registered'."""
    entities = _kb()
    badge = lookup_nszu_status(
        _drug(entities, "DRUG-TECLISTAMAB"),
        "DIS-MM",
        disease_names={"preferred": "Multiple myeloma",
                       "ukrainian": "Множинна мієлома"},
    )
    assert badge.status == "not-registered", badge


# ── Helper-level unit tests ──────────────────────────────────────────────


def test_disease_tokens_strip_dis_prefix():
    toks = _disease_tokens("DIS-DLBCL-NOS", {"ukrainian": "ДВКЛ", "preferred": "DLBCL NOS"})
    # Lowercase form of full id
    assert "dis-dlbcl-nos" in toks
    # Disease stem
    assert "dlbcl" in toks
    # Ukrainian + preferred names lowercased
    assert "двкл" in toks
    assert "dlbcl nos" in toks


def test_disease_tokens_handles_empty_names():
    toks = _disease_tokens("DIS-OVARIAN")
    assert "dis-ovarian" in toks
    assert "ovarian" in toks


def test_indication_match_substring_case_insensitive():
    indications = [
        "Дифузна великоклітинна B-клітинна лімфома (R-CHOP)",
        "Фолікулярна лімфома (R-CHOP / R-Bendamustine; підтримка R)",
    ]
    # Disease stem 'DLBCL' won't match Ukrainian text — but
    # 'дифузна великоклітинна' should match the full Ukrainian disease name.
    assert _indication_match(indications, ["дифузна великоклітинна"]) is not None
    assert _indication_match(indications, ["mantle cell"]) is None


def test_indication_match_skips_too_short_tokens():
    """Tokens shorter than 3 chars are ignored to avoid pathological
    over-matching (e.g. 'fl' matching 'follicular лімфома')."""
    indications = ["Фолікулярна лімфома"]
    assert _indication_match(indications, ["fl"]) is None
    assert _indication_match(indications, ["follicular"]) is None  # not in UA text
    assert _indication_match(indications, ["фолік"]) is not None


def test_status_oop_when_registered_but_not_reimbursed():
    """Synthetic drug — registered=True, reimbursed_nszu=False → 'oop'."""
    drug = {
        "id": "DRUG-FAKE",
        "regulatory_status": {
            "ukraine_registration": {
                "registered": True,
                "reimbursed_nszu": False,
                "reimbursement_indications": [],
            }
        },
        "notes": "Test fixture — not a real drug.",
    }
    badge = lookup_nszu_status(drug, "DIS-FOO")
    assert isinstance(badge, NszuBadge)
    assert badge.status == "oop"
    assert "Поза НСЗУ" in badge.label


def test_status_partial_when_reimbursed_but_no_match():
    drug = {
        "id": "DRUG-FAKE",
        "regulatory_status": {
            "ukraine_registration": {
                "registered": True,
                "reimbursed_nszu": True,
                "reimbursement_indications": ["Some other indication entirely"],
            }
        },
    }
    badge = lookup_nszu_status(drug, "DIS-FOO", disease_names={"preferred": "Foo carcinoma"})
    assert badge.status == "partial"
    assert badge.indication_match is None


def test_status_not_registered_when_no_regulatory_block():
    """A drug with no `regulatory_status` block at all defaults to
    'not-registered' — defensive, so the render layer never silently
    drops a badge."""
    badge = lookup_nszu_status({"id": "DRUG-X"}, "DIS-FOO")
    assert badge.status == "not-registered"


def test_label_localization():
    assert nszu_label("covered", "uk") == "✓ НСЗУ покриває"
    assert nszu_label("covered", "en") == "✓ NSZU covered"
    assert nszu_label("oop", "uk").startswith("⚠")
    assert nszu_label("oop", "en") == "⚠ Out-of-pocket"
    # Unknown lang falls back to UA
    assert nszu_label("partial", "fr").startswith("⚠")
