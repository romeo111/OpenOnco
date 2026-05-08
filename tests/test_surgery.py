"""Surgery — KNOWLEDGE_SCHEMA_SPECIFICATION §17.1 (RATIFIED 2026-05-07).

Schema-level tests for the Surgery entity. Loader-side ref-integrity
(applicable_diseases → Disease) is exercised by `tests/test_loader.py`.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from knowledge_base.schemas import Surgery, SurgeryComplication, SurgeryIntent


FIXTURES = Path(__file__).parent / "fixtures"


def test_surgery_minimal_loads():
    s = Surgery.model_validate(
        {
            "id": "SUR-MINIMAL",
            "names": {"preferred": "Minimal example"},
            "intent": "curative",
        }
    )
    assert s.id == "SUR-MINIMAL"
    assert s.intent == SurgeryIntent.CURATIVE
    assert s.applicable_diseases == []
    assert s.common_complications == []


def test_surgery_full_loads():
    s = Surgery.model_validate(
        {
            "id": "SUR-WHIPPLE",
            "names": {
                "preferred": "Pancreaticoduodenectomy (Whipple)",
                "ukrainian": "Панкреатодуоденектомія (Уіппла)",
            },
            "type": "pancreaticoduodenectomy",
            "intent": "curative",
            "target_organ": "pancreas_head",
            "applicable_diseases": ["DIS-PDAC"],
            "operative_mortality_pct": "1-3% in high-volume centers",
            "common_complications": [
                {"name": "POPF (pancreatic fistula)", "frequency": "10-20%"},
                {"name": "Delayed gastric emptying", "frequency": "15-25%"},
            ],
            "sources": ["SRC-NCCN-PANCREATIC-2025", "SRC-ESMO-PANCREATIC-2024"],
        }
    )
    assert s.type == "pancreaticoduodenectomy"
    assert s.target_organ == "pancreas_head"
    assert "DIS-PDAC" in s.applicable_diseases
    assert len(s.common_complications) == 2
    assert isinstance(s.common_complications[0], SurgeryComplication)
    assert s.common_complications[0].frequency == "10-20%"


def test_surgery_rejects_invalid_intent():
    with pytest.raises(ValidationError):
        Surgery.model_validate(
            {
                "id": "SUR-BAD",
                "names": {"preferred": "Bad intent"},
                "intent": "experimental",  # not in enum
            }
        )


def test_surgery_requires_id():
    with pytest.raises(ValidationError):
        Surgery.model_validate(
            {
                "names": {"preferred": "No id"},
                "intent": "curative",
            }
        )


def test_surgery_requires_names():
    with pytest.raises(ValidationError):
        Surgery.model_validate(
            {
                "id": "SUR-NO-NAMES",
                "intent": "curative",
            }
        )


def test_surgery_requires_intent():
    with pytest.raises(ValidationError):
        Surgery.model_validate(
            {
                "id": "SUR-NO-INTENT",
                "names": {"preferred": "No intent"},
            }
        )


def test_surgery_intent_enum_values():
    """Pin the §17.1 sketch enum vocabulary verbatim."""
    assert {i.value for i in SurgeryIntent} == {
        "curative",
        "palliative",
        "diagnostic",
        "salvage",
    }


def test_surgery_whipple_fixture_loads():
    raw = yaml.safe_load(
        (FIXTURES / "surgery_whipple.yaml").read_text(encoding="utf-8")
    )
    s = Surgery.model_validate(raw)
    assert s.intent == SurgeryIntent.CURATIVE
    assert s.id.startswith("SUR-")
