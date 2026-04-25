"""Smoke tests for the YAML loader + referential integrity checks."""

from __future__ import annotations

from pathlib import Path

from knowledge_base.validation.loader import load_content

KB_ROOT = Path(__file__).parent.parent / "knowledge_base" / "hosted" / "content"


def test_seed_loads_without_errors():
    result = load_content(KB_ROOT)
    assert result.schema_errors == [], f"Schema errors: {result.schema_errors}"
    assert result.ref_errors == [], f"Ref errors: {result.ref_errors}"
    assert result.ok


def test_seed_has_hcv_mzl_core():
    result = load_content(KB_ROOT)
    ids = set(result.entities_by_id.keys())
    # Core HCV-MZL entities we expect present
    for required in [
        "DIS-HCV-MZL",
        "DRUG-RITUXIMAB",
        "DRUG-BENDAMUSTINE",
        "DRUG-SOFOSBUVIR-VELPATASVIR",
        "REG-DAA-SOF-VEL",
        "REG-BR-STANDARD",
        "IND-HCV-MZL-1L-ANTIVIRAL",
        "IND-HCV-MZL-1L-BR-AGGRESSIVE",
        "ALGO-HCV-MZL-1L",
        "RF-BULKY-DISEASE",
        "RF-AGGRESSIVE-HISTOLOGY-TRANSFORMATION",
        "BIO-HCV-RNA",
        "SRC-ESMO-MZL-2024",
        "SRC-NCCN-BCELL-2025",
        "SRC-MOZ-UA-LYMPH-2013",
        "SRC-EASL-HCV-2023",
    ]:
        assert required in ids, f"Missing seed entity: {required}"
