import json
from pathlib import Path

from knowledge_base.engine.plan import generate_plan


def _reason_texts(patient_path: Path) -> list[str]:
    patient = json.loads(patient_path.read_text(encoding="utf-8"))
    result = generate_plan(patient)
    if result.plan is None:
        return []
    return [track.selection_reason or "" for track in result.plan.tracks]


def test_selection_reasons_do_not_render_raw_trace_dicts():
    for patient_path in sorted(Path("examples").glob("*.json")):
        for reason in _reason_texts(patient_path):
            assert "{'step'" not in reason, patient_path
            assert '"step"' not in reason, patient_path
            assert "'branch'" not in reason, patient_path
            assert "winner_red_flag" not in reason, patient_path


def test_null_algorithm_branch_uses_provisional_reason():
    reasons = _reason_texts(Path("examples/auto_anal_scc.json"))
    assert reasons
    assert reasons[0].startswith(
        "Provisional current-line default from ALGO-ANAL-SCC-1L"
    )
    assert "did not select a treatment branch" in reasons[0]
    assert "Histological confirmation" in reasons[0]
