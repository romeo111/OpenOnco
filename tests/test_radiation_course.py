"""RadiationCourse — KNOWLEDGE_SCHEMA_SPECIFICATION §17.1 (RATIFIED 2026-05-07).

Schema-level tests for the RadiationCourse entity. Loader-side ref-integrity
(concurrent_chemo_regimen → Regimen) is exercised by `tests/test_loader.py`.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from knowledge_base.schemas import RadiationCourse, RadiationIntent


FIXTURES = Path(__file__).parent / "fixtures"


def test_radiation_course_minimal_loads():
    rc = RadiationCourse.model_validate(
        {
            "id": "RT-MINIMAL",
            "names": {"preferred": "Minimal RT"},
            "total_dose_gy": 30.0,
            "fractions": 10,
            "intent": "palliative",
        }
    )
    assert rc.id == "RT-MINIMAL"
    assert rc.total_dose_gy == 30.0
    assert rc.fractions == 10
    assert rc.intent == RadiationIntent.PALLIATIVE
    assert rc.concurrent_chemo_regimen is None


def test_radiation_course_full_loads():
    rc = RadiationCourse.model_validate(
        {
            "id": "RT-CROSS-NEOADJ",
            "names": {
                "preferred": "CROSS neoadjuvant CRT",
                "ukrainian": "CROSS неоад'ювантна ХПТ",
            },
            "total_dose_gy": 41.4,
            "fractions": 23,
            "fraction_size_gy": 1.8,
            "target_volume": "primary + involved nodes (CTV)",
            "schedule": "5 fx/week × 4.6 weeks",
            "concurrent_chemo_regimen": "REG-CARBOPLATIN-PACLITAXEL-WEEKLY",
            "intent": "neoadjuvant",
            "sources": ["SRC-CROSS-VAN-HAGEN-2012", "SRC-NCCN-ESOPHAGEAL-2025"],
        }
    )
    assert rc.total_dose_gy == 41.4
    assert rc.fractions == 23
    assert rc.fraction_size_gy == 1.8
    assert rc.concurrent_chemo_regimen == "REG-CARBOPLATIN-PACLITAXEL-WEEKLY"
    assert rc.intent == RadiationIntent.NEOADJUVANT


def test_radiation_course_rejects_invalid_intent():
    with pytest.raises(ValidationError):
        RadiationCourse.model_validate(
            {
                "id": "RT-BAD",
                "names": {"preferred": "Bad RT"},
                "total_dose_gy": 50.0,
                "fractions": 25,
                "intent": "induction",  # not in §2.3 enum
            }
        )


def test_radiation_course_requires_total_dose_gy():
    with pytest.raises(ValidationError):
        RadiationCourse.model_validate(
            {
                "id": "RT-NO-DOSE",
                "names": {"preferred": "No dose"},
                "fractions": 25,
                "intent": "definitive",
            }
        )


def test_radiation_course_requires_fractions():
    with pytest.raises(ValidationError):
        RadiationCourse.model_validate(
            {
                "id": "RT-NO-FX",
                "names": {"preferred": "No fractions"},
                "total_dose_gy": 50.0,
                "intent": "definitive",
            }
        )


def test_radiation_course_requires_intent():
    with pytest.raises(ValidationError):
        RadiationCourse.model_validate(
            {
                "id": "RT-NO-INTENT",
                "names": {"preferred": "No intent"},
                "total_dose_gy": 50.0,
                "fractions": 25,
            }
        )


def test_radiation_intent_enum_values():
    """Pin the §17.1 sketch enum vocabulary verbatim."""
    assert {i.value for i in RadiationIntent} == {
        "neoadjuvant",
        "definitive",
        "adjuvant",
        "palliative",
    }


def test_radiation_cross_fixture_loads():
    raw = yaml.safe_load(
        (FIXTURES / "radiation_cross.yaml").read_text(encoding="utf-8")
    )
    rc = RadiationCourse.model_validate(raw)
    assert rc.intent == RadiationIntent.NEOADJUVANT
    assert rc.id.startswith("RT-")
    assert rc.total_dose_gy == 41.4
