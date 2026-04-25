"""End-to-end engine test for Follicular Lymphoma — second-largest NHL.

Validates 3-track GELF-driven decision: low burden → W&W (surveillance);
high burden (GELF+) → BR; transformation suspect → R-CHOP.
"""

from __future__ import annotations

import json
from pathlib import Path

from knowledge_base.engine import generate_plan, orchestrate_mdt, render_plan_html

REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


def _patient(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def test_fl_disease_resolves():
    p = _patient("patient_fl_low_burden.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    assert plan.disease_id == "DIS-FL"
    assert plan.algorithm_id == "ALGO-FL-1L"


def test_fl_three_tracks_present():
    """FL has 3 tracks (W&W + BR + R-CHOP) — different from 2-track diseases."""
    for name in ("patient_fl_low_burden.json", "patient_fl_high_burden.json",
                 "patient_fl_transformation.json"):
        p = _patient(name)
        plan = generate_plan(p, kb_root=KB_ROOT)
        assert plan.plan is not None
        assert len(plan.plan.tracks) == 3
        track_ids = {t.track_id for t in plan.plan.tracks}
        assert track_ids == {"surveillance", "standard", "aggressive"}, (
            f"{name}: unexpected tracks {track_ids}"
        )


def test_fl_low_burden_defaults_to_watch():
    p = _patient("patient_fl_low_burden.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    assert plan.default_indication_id == "IND-FL-1L-WATCH"


def test_fl_high_burden_defaults_to_br():
    p = _patient("patient_fl_high_burden.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    assert plan.default_indication_id == "IND-FL-1L-BR"


def test_fl_transformation_defaults_to_rchop():
    p = _patient("patient_fl_transformation.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    assert plan.default_indication_id == "IND-FL-1L-RCHOP-AGGRESSIVE"


def test_fl_watch_track_has_no_regimen():
    """Surveillance track has no recommended_regimen — render shows track
    without drug list."""
    p = _patient("patient_fl_low_burden.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    surv = next(t for t in plan.plan.tracks if t.track_id == "surveillance")
    assert surv.regimen_data is None


def test_fl_br_track_uses_shared_br_regimen():
    """FL BR track reuses REG-BR-STANDARD originally created for HCV-MZL."""
    p = _patient("patient_fl_high_burden.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    standard = next(t for t in plan.plan.tracks if t.track_id == "standard")
    assert standard.regimen_data["id"] == "REG-BR-STANDARD"


def test_fl_aggressive_track_uses_shared_rchop_regimen():
    """FL aggressive track reuses REG-R-CHOP originally created for DLBCL."""
    p = _patient("patient_fl_transformation.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    aggressive = next(t for t in plan.plan.tracks if t.track_id == "aggressive")
    assert aggressive.regimen_data["id"] == "REG-R-CHOP"


def test_fl_render_handles_three_track_plan():
    p = _patient("patient_fl_high_burden.json")
    plan = generate_plan(p, kb_root=KB_ROOT)
    mdt = orchestrate_mdt(p, plan, kb_root=KB_ROOT)
    html = render_plan_html(plan, mdt=mdt)
    assert "IND-FL-1L-WATCH" in html
    assert "IND-FL-1L-BR" in html
    assert "IND-FL-1L-RCHOP-AGGRESSIVE" in html
