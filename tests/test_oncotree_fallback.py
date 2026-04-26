"""Tests for engine/oncotree_fallback.py — three-tier OncoTree resolution.

Per safe-rollout v3 §5 + locked decision Q4 (pan-tumor with warning).
"""

from __future__ import annotations

import pytest

from knowledge_base.engine.oncotree_fallback import (
    resolve_icd10_to_oncotree,
    resolve_oncotree_code,
)


# ── ICD-10 → OncoTree direct mapping ────────────────────────────────────


@pytest.mark.parametrize(
    "icd10,expected",
    [
        # Common solid tumors
        ("C18", "COADREAD"),
        ("C18.7", "COADREAD"),       # subcode also resolves to family
        ("C19", "COADREAD"),
        ("C20", "COADREAD"),
        ("C34", "NSCLC"),
        ("C34.1", "NSCLC"),
        ("C50", "BREAST"),
        ("C50.9", "BREAST"),
        ("C53", "CESC"),
        ("C54", "UCEC"),
        ("C56", "OV"),
        ("C61", "PRAD"),
        ("C64", "RCC"),
        ("C67", "BLCA"),
        ("C71", "GBM"),
        ("C73", "THPA"),
        ("C25", "PAAD"),
        ("C22", "HCC"),
        ("C16", "STAD"),
        ("C15", "ESCA"),
        ("C43", "MEL"),
        # Hematologic
        ("C90", "MM"),
        ("C90.0", "MM"),
        ("C81", "CHL"),
        ("C82", "FL"),
        ("C83", "DLBCLNOS"),
        ("C91", "BLL"),
        ("C92", "AML"),
        ("D45", "PV"),
        ("D46", "MDS"),
        ("D47", "MPN"),
    ],
)
def test_icd10_resolves_to_oncotree(icd10: str, expected: str):
    assert resolve_icd10_to_oncotree(icd10) == expected


def test_unknown_icd10_returns_none():
    assert resolve_icd10_to_oncotree("Z99") is None
    assert resolve_icd10_to_oncotree("X99") is None


def test_empty_or_none_icd10_returns_none():
    assert resolve_icd10_to_oncotree(None) is None
    assert resolve_icd10_to_oncotree("") is None
    assert resolve_icd10_to_oncotree("   ") is None


def test_icd10_case_insensitive():
    assert resolve_icd10_to_oncotree("c34") == "NSCLC"
    assert resolve_icd10_to_oncotree("c50.9") == "BREAST"


# ── Three-tier resolution (resolve_oncotree_code) ───────────────────────


def test_tier1_explicit_oncotree_code_wins():
    """Explicit Disease.oncotree_code beats ICD-10 fallback even when
    the fallback would also resolve."""
    disease = {
        "oncotree_code": "LUAD",  # specific subtype
        "codes": {"icd_10": "C34"},  # would fall back to NSCLC
    }
    code, fallback = resolve_oncotree_code(disease)
    assert code == "LUAD"
    assert fallback is False


def test_tier2_icd10_fallback():
    """No explicit code → ICD-10 fallback resolves."""
    disease = {"codes": {"icd_10": "C18"}}
    code, fallback = resolve_oncotree_code(disease)
    assert code == "COADREAD"
    assert fallback is True


def test_tier3_pan_tumor_when_unresolvable():
    """No explicit code AND no ICD-10 mapping → pan-tumor (None)."""
    disease = {"codes": {"icd_10": "Z99"}}
    code, fallback = resolve_oncotree_code(disease)
    assert code is None
    assert fallback is True


def test_tier3_pan_tumor_when_no_codes_block():
    disease = {"id": "DIS-X"}
    code, fallback = resolve_oncotree_code(disease)
    assert code is None
    assert fallback is True


def test_tier3_pan_tumor_when_disease_data_none():
    code, fallback = resolve_oncotree_code(None)
    assert code is None
    assert fallback is True


def test_explicit_empty_string_falls_through_to_tier2():
    """Empty oncotree_code (e.g. from a placeholder) should not block fallback."""
    disease = {
        "oncotree_code": "   ",
        "codes": {"icd_10": "C50"},
    }
    code, fallback = resolve_oncotree_code(disease)
    assert code == "BREAST"
    assert fallback is True


# ── Coverage spot-check: every Disease in the KB resolves to *something* ─
# (This is an integration test — uses real Disease YAMLs.)


def test_all_kb_diseases_resolve_via_three_tier():
    """No Disease in the KB should fall to pan-tumor (we populated all 65
    in PR-B). If this test starts failing after a new disease is added,
    populate Disease.oncotree_code or update the fallback table."""
    from pathlib import Path
    from knowledge_base.validation.loader import load_content

    repo_root = Path(__file__).resolve().parent.parent
    r = load_content(repo_root / "knowledge_base" / "hosted" / "content")

    pan_tumor_diseases: list[str] = []
    for eid, info in r.entities_by_id.items():
        if info["type"] != "diseases":
            continue
        code, _ = resolve_oncotree_code(info["data"])
        if code is None:
            pan_tumor_diseases.append(eid)

    assert not pan_tumor_diseases, (
        f"Diseases without resolvable OncoTree code: {pan_tumor_diseases}. "
        f"Add Disease.oncotree_code or extend oncotree_fallback._ICD10_FAMILY_TO_ONCOTREE."
    )
