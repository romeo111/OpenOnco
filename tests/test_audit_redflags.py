from pathlib import Path

import yaml

from scripts.audit_redflags import _collect_rule_references


def test_collect_rule_references_uses_explicit_fields_not_prose(tmp_path: Path):
    """Notes and source IDs may contain RF-* text but are not graph edges."""
    rule = {
        "id": "ALGO-TEST",
        "notes": "Discuss RF-NOT-A-REFERENCE and SRC-WCRF-AICR-CUP-2018.",
        "decision_tree": [{"conditions": [{"red_flag": "RF-EXECUTABLE"}]}],
        "red_flags_triggering_alternative": ["RF-ALTERNATIVE"],
    }
    (tmp_path / "rule.yaml").write_text(
        yaml.safe_dump(rule), encoding="utf-8"
    )

    refs = _collect_rule_references([tmp_path])

    assert refs == {"RF-EXECUTABLE": 1, "RF-ALTERNATIVE": 1}
