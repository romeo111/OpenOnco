"""Smoke tests for the clinical sign-off infrastructure (CSD-5).

Covers:
  - ReviewerProfile entity loads cleanly
  - The 3 placeholder profiles ship and are picked up by the loader
  - reviewer_signoffs migration: legacy int (0), new empty list, new
    structured list all parse on Indication
  - Loader's referential check rejects sign-offs whose reviewer_id does
    not resolve to a ReviewerProfile

Full publish-gate machinery (≥2 distinct reviewers, scope-match, etc.)
is the subject of the CSD-5A signoff-tooling task; this module covers
the schema + loader prerequisites only.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from knowledge_base.schemas import (
    Indication,
    ReviewerProfile,
    ReviewerSignoff,
)
from knowledge_base.validation.loader import clear_load_cache, load_content


PLACEHOLDER_IDS = {
    "REV-HEME-LEAD-PLACEHOLDER",
    "REV-SOLID-LEAD-PLACEHOLDER",
    "REV-MOLPATH-LEAD-PLACEHOLDER",
}


# ── ReviewerProfile schema ────────────────────────────────────────────────


def test_reviewer_profile_loads_minimal():
    rp = ReviewerProfile.model_validate({
        "id": "REV-TEST-MINIMAL",
        "name": {"preferred": "Test Reviewer"},
        "specialty": "Hematology",
        "last_active": "2026-04-27",
    })
    assert rp.id == "REV-TEST-MINIMAL"
    assert rp.sign_off_scope.disease_categories == []
    assert rp.sign_off_scope.entity_types == []


def test_reviewer_profile_loads_with_full_scope():
    rp = ReviewerProfile.model_validate({
        "id": "REV-TEST-FULL",
        "name": {"preferred": "Full Reviewer", "ukrainian": "Повний"},
        "specialty": "Medical Oncology — Solid Tumors",
        "qualifications": ["board-certified", "≥5 yr experience"],
        "sign_off_scope": {
            "disease_categories": ["breast", "nsclc"],
            "entity_types": ["Indication", "Regimen"],
            "diseases_explicit": ["DIS-BREAST-HR-POS"],
        },
        "last_active": "2026-04-27",
        "notes": "test",
    })
    assert "breast" in rp.sign_off_scope.disease_categories
    assert "DIS-BREAST-HR-POS" in rp.sign_off_scope.diseases_explicit


# ── 3 placeholder profiles in the live KB ─────────────────────────────────


def test_three_placeholder_profiles_present():
    clear_load_cache()
    r = load_content(Path("knowledge_base/hosted/content"))
    assert r.ok, (
        f"KB load failed: schema={len(r.schema_errors)} "
        f"ref={len(r.ref_errors)} contract={len(r.contract_errors)}"
    )
    reviewer_ids = {
        eid for eid, info in r.entities_by_id.items()
        if info["type"] == "reviewers"
    }
    missing = PLACEHOLDER_IDS - reviewer_ids
    assert not missing, f"missing placeholder profiles: {missing}"


# ── Migration: int → list[ReviewerSignoff] ────────────────────────────────


def _minimal_indication_dict(**overrides):
    base = {
        "id": "IND-TEST",
        "applicable_to": {"disease_id": "DIS-TEST", "line_of_therapy": 1},
    }
    base.update(overrides)
    return base


def test_legacy_int_zero_coerces_to_empty_list():
    ind = Indication.model_validate(
        _minimal_indication_dict(reviewer_signoffs=0)
    )
    assert ind.reviewer_signoffs == []


def test_legacy_int_nonzero_also_coerces_to_empty_list():
    # The int never carried identity, so we discard it (rather than fabricate
    # placeholder rows). Authors who held a real signed-off entity must
    # re-author the sign-off rows via the CSD-5A tooling.
    ind = Indication.model_validate(
        _minimal_indication_dict(reviewer_signoffs=2)
    )
    assert ind.reviewer_signoffs == []


def test_new_empty_list_loads_cleanly():
    ind = Indication.model_validate(
        _minimal_indication_dict(reviewer_signoffs=[])
    )
    assert ind.reviewer_signoffs == []


def test_structured_signoff_list_loads_cleanly():
    ind = Indication.model_validate(_minimal_indication_dict(
        reviewer_signoffs=[
            {
                "reviewer_id": "REV-HEME-LEAD-PLACEHOLDER",
                "timestamp": "2026-04-27T10:00:00Z",
                "rationale": "Tier-1 evidence cited; aligns with NCCN v2.2026.",
            },
            {
                "reviewer_id": "REV-SOLID-LEAD-PLACEHOLDER",
                "timestamp": "2026-04-27T11:30:00Z",
                "entity_version": "2026-04-27",
            },
        ]
    ))
    assert len(ind.reviewer_signoffs) == 2
    assert isinstance(ind.reviewer_signoffs[0], ReviewerSignoff)
    assert ind.reviewer_signoffs[0].reviewer_id == "REV-HEME-LEAD-PLACEHOLDER"
    assert ind.reviewer_signoffs[1].entity_version == "2026-04-27"


# ── Loader referential integrity ──────────────────────────────────────────


def test_loader_flags_unknown_reviewer_id(tmp_path: Path):
    """A reviewer_signoff pointing at REV-NONEXISTENT must surface as ref_error."""
    root = tmp_path / "content"

    # Minimum viable KB: one Disease, one Source, one Regimen, one Drug,
    # one ReviewerProfile, plus the bad Indication.
    (root / "diseases").mkdir(parents=True)
    (root / "diseases" / "dis_test.yaml").write_text(yaml.safe_dump({
        "id": "DIS-TEST",
        "names": {"preferred": "Test Disease"},
        "codes": {},
    }), encoding="utf-8")

    (root / "drugs").mkdir(parents=True)
    (root / "drugs" / "drug_test.yaml").write_text(yaml.safe_dump({
        "id": "DRUG-TEST",
        "names": {"preferred": "Testdrug"},
    }), encoding="utf-8")

    (root / "regimens").mkdir(parents=True)
    (root / "regimens" / "reg_test.yaml").write_text(yaml.safe_dump({
        "id": "REG-TEST",
        "name": "Test Regimen",
        "components": [{"drug_id": "DRUG-TEST"}],
    }), encoding="utf-8")

    (root / "reviewers").mkdir(parents=True)
    (root / "reviewers" / "rev_real.yaml").write_text(yaml.safe_dump({
        "id": "REV-REAL",
        "name": {"preferred": "Real Reviewer"},
        "specialty": "Hematology",
        "last_active": "2026-04-27",
    }), encoding="utf-8")

    (root / "indications").mkdir(parents=True)
    (root / "indications" / "ind_bad.yaml").write_text(yaml.safe_dump({
        "id": "IND-BAD",
        "applicable_to": {"disease_id": "DIS-TEST", "line_of_therapy": 1},
        "recommended_regimen": "REG-TEST",
        "reviewer_signoffs": [
            {
                "reviewer_id": "REV-NONEXISTENT",
                "timestamp": "2026-04-27T10:00:00Z",
            }
        ],
    }), encoding="utf-8")

    clear_load_cache()
    r = load_content(root)
    clear_load_cache()  # don't pollute global cache for other tests

    # Schema must pass (the structure is valid); the ref check must fail.
    assert not r.schema_errors, f"unexpected schema errors: {r.schema_errors}"
    bad_refs = [msg for _, msg in r.ref_errors if "REV-NONEXISTENT" in msg]
    assert bad_refs, (
        f"expected a ref_error for REV-NONEXISTENT, got: {r.ref_errors}"
    )


def test_loader_accepts_valid_reviewer_id(tmp_path: Path):
    """Sanity check the positive path: when the reviewer_id resolves, no error."""
    root = tmp_path / "content"

    (root / "diseases").mkdir(parents=True)
    (root / "diseases" / "dis_test.yaml").write_text(yaml.safe_dump({
        "id": "DIS-TEST",
        "names": {"preferred": "Test Disease"},
        "codes": {},
    }), encoding="utf-8")

    (root / "drugs").mkdir(parents=True)
    (root / "drugs" / "drug_test.yaml").write_text(yaml.safe_dump({
        "id": "DRUG-TEST",
        "names": {"preferred": "Testdrug"},
    }), encoding="utf-8")

    (root / "regimens").mkdir(parents=True)
    (root / "regimens" / "reg_test.yaml").write_text(yaml.safe_dump({
        "id": "REG-TEST",
        "name": "Test Regimen",
        "components": [{"drug_id": "DRUG-TEST"}],
    }), encoding="utf-8")

    (root / "reviewers").mkdir(parents=True)
    (root / "reviewers" / "rev_real.yaml").write_text(yaml.safe_dump({
        "id": "REV-REAL",
        "name": {"preferred": "Real Reviewer"},
        "specialty": "Hematology",
        "last_active": "2026-04-27",
    }), encoding="utf-8")

    (root / "indications").mkdir(parents=True)
    (root / "indications" / "ind_good.yaml").write_text(yaml.safe_dump({
        "id": "IND-GOOD",
        "applicable_to": {"disease_id": "DIS-TEST", "line_of_therapy": 1},
        "recommended_regimen": "REG-TEST",
        "reviewer_signoffs": [
            {
                "reviewer_id": "REV-REAL",
                "timestamp": "2026-04-27T10:00:00Z",
            }
        ],
    }), encoding="utf-8")

    clear_load_cache()
    r = load_content(root)
    clear_load_cache()

    bad_refs = [msg for _, msg in r.ref_errors if "REV-REAL" in msg]
    assert not bad_refs, f"REV-REAL should resolve, but got: {bad_refs}"
