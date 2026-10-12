"""Regression tests for refusing clinical output from an invalid KB."""

from __future__ import annotations

from pathlib import Path
import json

from knowledge_base.engine import generate_diagnostic_brief, generate_plan
from serverless import clinical_question as cq


def test_packaged_core_cannot_defer_a_missing_source(tmp_path, monkeypatch):
    from knowledge_base.validation import bundle
    from knowledge_base.validation.loader import LoadResult

    path = tmp_path / 'indication.yaml'
    message = 'Missing citation SRC-MISSING'
    raw = LoadResult(ref_errors=[(path, message)], missing_refs=[(path, message, 'SRC-MISSING', 'sources')])
    monkeypatch.setattr(bundle, 'load_content', lambda root: raw)
    (tmp_path / '_bundle_manifest.json').write_text(json.dumps({
        'deferred_entities': {'SRC-MISSING': {'type': 'sources', 'disease_id': 'DIS-TEST'}}
    }), encoding='utf-8')
    checked = bundle.load_packaged_content(tmp_path, core_only=True)
    assert not checked.ok
    assert checked.ref_errors == raw.ref_errors


def _invalid_kb(root: Path) -> Path:
    biomarker_dir = root / "biomarkers"
    biomarker_dir.mkdir()
    (biomarker_dir / "bio_invalid.yaml").write_text(
        """\
id: BIO-INVALID
names:
  preferred: Invalid marker
clinical_context: [not-a-valid-context]
""",
        encoding="utf-8",
    )
    return root


def test_treatment_engine_stops_when_kb_has_schema_error(tmp_path: Path) -> None:
    result = generate_plan(
        {"patient_id": "TEST-INVALID-KB", "disease": {"id": "DIS-TEST"}},
        kb_root=_invalid_kb(tmp_path),
    )

    assert result.plan is None
    assert result.default_indication_id is None
    assert any("validation failed" in warning.lower() for warning in result.warnings)


def test_diagnostic_engine_stops_when_kb_has_schema_error(tmp_path: Path) -> None:
    result = generate_diagnostic_brief(
        {
            "patient_id": "TEST-INVALID-KB",
            "disease": {"suspicion": {"lineage_hint": "lymphoma"}},
        },
        kb_root=_invalid_kb(tmp_path),
    )

    assert result.diagnostic_plan is None
    assert any("validation failed" in warning.lower() for warning in result.warnings)


def test_public_engine_reports_unavailable_when_kb_has_schema_error(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(cq, "KB_ROOT", _invalid_kb(tmp_path))

    result = cq.run_engine({"patient_id": "TEST-INVALID-KB", "disease": {"id": "DIS-TEST"}})

    assert result.ok is False
    assert result.mode == "unavailable"
    assert result.error == "knowledge_base_validation_failed"
