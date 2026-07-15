"""Smoke coverage for basal cell carcinoma showcase cases."""

from __future__ import annotations

import json
from pathlib import Path

from knowledge_base.engine import generate_plan

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def test_bcc_locally_advanced_showcase_generates_plan():
    plan = generate_plan(_patient("patient_showcase_bcc_labcc_hhi_1l.json"), kb_root=KB_ROOT)

    assert plan.disease_id == "DIS-BCC"
    assert plan.algorithm_id == "ALGO-BCC-1L"
    assert plan.default_indication_id == "IND-BCC-1L-VISMODEGIB"


def test_bcc_locally_advanced_showcase_has_hhi_tracks():
    plan = generate_plan(_patient("patient_showcase_bcc_labcc_hhi_1l.json"), kb_root=KB_ROOT)

    track_indications = {track.indication_id for track in plan.plan.tracks}
    assert "IND-BCC-1L-VISMODEGIB" in track_indications
    assert "IND-BCC-1L-SONIDEGIB" in track_indications
