"""Indication.phases — KNOWLEDGE_SCHEMA_SPECIFICATION §17 (RATIFIED 2026-05-07).

Schema-level tests for the phased-indication contract. Loader-level
ref-integrity (FK resolution to Surgery / RadiationCourse / Regimen)
is exercised by `tests/test_loader.py`; here we only pin the Pydantic
accept/reject surface.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from knowledge_base.schemas import (
    Indication,
    IndicationPhase,
    IndicationPhaseStage,
    IndicationPhaseType,
)


FIXTURES = Path(__file__).parent / "fixtures"


# ── IndicationPhase XOR validator ────────────────────────────────────────────


def test_phase_accepts_regimen_id_only():
    p = IndicationPhase.model_validate(
        {
            "phase": "neoadjuvant",
            "type": "chemotherapy",
            "regimen_id": "REG-FLOT",
            "cycles": 4,
        }
    )
    assert p.phase == IndicationPhaseStage.NEOADJUVANT
    assert p.type == IndicationPhaseType.CHEMOTHERAPY
    assert p.regimen_id == "REG-FLOT"
    assert p.surgery_id is None
    assert p.radiation_id is None
    assert p.cycles == 4


def test_phase_accepts_surgery_id_only():
    p = IndicationPhase.model_validate(
        {
            "phase": "surgery",
            "type": "surgery",
            "surgery_id": "SUR-WHIPPLE",
        }
    )
    assert p.surgery_id == "SUR-WHIPPLE"
    assert p.regimen_id is None
    assert p.radiation_id is None


def test_phase_accepts_radiation_id_only():
    p = IndicationPhase.model_validate(
        {
            "phase": "definitive",
            "type": "chemoradiation",
            "radiation_id": "RT-CROSS-NEOADJ",
            "duration_weeks": 5,
        }
    )
    assert p.radiation_id == "RT-CROSS-NEOADJ"
    assert p.duration_weeks == 5


def test_phase_rejects_zero_foreign_keys():
    """Pydantic model_validator must trip when no FK is populated."""
    with pytest.raises(ValidationError, match=r"exactly one"):
        IndicationPhase.model_validate(
            {"phase": "surgery", "type": "surgery"}
        )


def test_phase_rejects_two_foreign_keys():
    """Multi-FK is the §17.1 anti-pattern — exactly one allowed."""
    with pytest.raises(ValidationError, match=r"exactly one"):
        IndicationPhase.model_validate(
            {
                "phase": "neoadjuvant",
                "type": "chemoradiation",
                "regimen_id": "REG-CARBO-PACLI",
                "radiation_id": "RT-CROSS-NEOADJ",
            }
        )


def test_phase_rejects_three_foreign_keys():
    with pytest.raises(ValidationError, match=r"exactly one"):
        IndicationPhase.model_validate(
            {
                "phase": "surgery",
                "type": "surgery",
                "regimen_id": "REG-X",
                "surgery_id": "SUR-Y",
                "radiation_id": "RT-Z",
            }
        )


def test_phase_rejects_invalid_phase_enum():
    with pytest.raises(ValidationError):
        IndicationPhase.model_validate(
            {
                "phase": "consolidation",  # not in enum (RegimenPhase has it; IndicationPhase doesn't)
                "type": "chemotherapy",
                "regimen_id": "REG-X",
            }
        )


def test_phase_rejects_invalid_type_enum():
    with pytest.raises(ValidationError):
        IndicationPhase.model_validate(
            {
                "phase": "neoadjuvant",
                "type": "hormonal",  # not in §2.2 enum extension
                "regimen_id": "REG-X",
            }
        )


# ── Indication.phases integration ────────────────────────────────────────────


def test_indication_without_phases_loads_unchanged():
    """Backward-compat invariant: existing indications (no `phases:`) must
    continue loading. Planning doc §2.5: phases is opt-in."""
    ind = Indication.model_validate(
        {
            "id": "IND-TEST-NO-PHASES",
            "applicable_to": {
                "disease_id": "DIS-GASTRIC",
                "line_of_therapy": 1,
            },
            "recommended_regimen": "REG-FLOT",
        }
    )
    assert ind.phases is None
    assert ind.recommended_regimen == "REG-FLOT"


def test_indication_with_phases_loads():
    ind = Indication.model_validate(
        {
            "id": "IND-TEST-PERIOP-FLOT",
            "applicable_to": {
                "disease_id": "DIS-GASTRIC",
                "line_of_therapy": 1,
            },
            "phases": [
                {
                    "phase": "neoadjuvant",
                    "type": "chemotherapy",
                    "regimen_id": "REG-FLOT",
                    "cycles": 4,
                },
                {
                    "phase": "surgery",
                    "type": "surgery",
                    "surgery_id": "SUR-TOTAL-GASTRECTOMY",
                },
                {
                    "phase": "adjuvant",
                    "type": "chemotherapy",
                    "regimen_id": "REG-FLOT",
                    "cycles": 4,
                },
            ],
        }
    )
    assert ind.phases is not None
    assert len(ind.phases) == 3
    assert ind.phases[0].phase == IndicationPhaseStage.NEOADJUVANT
    assert ind.phases[1].surgery_id == "SUR-TOTAL-GASTRECTOMY"
    assert ind.phases[2].cycles == 4


def test_phased_indication_fixture_loads():
    """Golden-fixture round-trip — pure Pydantic, no loader ref-integrity."""
    raw = yaml.safe_load(
        (FIXTURES / "phased_indication.yaml").read_text(encoding="utf-8")
    )
    ind = Indication.model_validate(raw)
    assert ind.phases is not None
    assert len(ind.phases) >= 2
    # First phase must be valid (XOR validator already gated it on load)
    assert ind.phases[0].phase in IndicationPhaseStage
    assert ind.phases[0].type in IndicationPhaseType


def test_indication_phases_propagates_invalid_phase_through_indication():
    """The XOR validator on IndicationPhase fires even when nested in
    Indication.phases — Pydantic v2 runs nested validators bottom-up."""
    with pytest.raises(ValidationError, match=r"exactly one"):
        Indication.model_validate(
            {
                "id": "IND-BAD",
                "applicable_to": {
                    "disease_id": "DIS-GASTRIC",
                    "line_of_therapy": 1,
                },
                "phases": [
                    {
                        "phase": "neoadjuvant",
                        "type": "chemoradiation",
                        # NO foreign key set — invalid
                    }
                ],
            }
        )
