"""Real byte accounting, attribution and fail-closed read-only audit."""
import json
import zipfile
import pytest
from scripts import profile_engine_bundle as profile


def test_profile_accounts_for_every_byte_with_builder_attribution(tmp_path):
    bundle = tmp_path / "core.zip"
    entries = {
        "knowledge_base/engine/runtime.py": "print('runtime')",
        "knowledge_base/hosted/content/diseases/aml.yaml": "id: DIS-AML\n",
        "knowledge_base/hosted/content/indications/aml.yaml": "id: IND-AML\ndisease_id: DIS-AML\n",
        "knowledge_base/hosted/content/redflags/shared.yaml": "id: RF-SHARED\nrelevant_diseases: [DIS-AML, DIS-CLL]\n",
    }
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, text in entries.items():
            archive.writestr(name, text)
    original = bundle.read_bytes()
    report = profile.profile_bundle(bundle)
    assert bundle.read_bytes() == original
    assert report["files"] == 4
    assert report["archive_bytes"] == len(original)
    assert sum(group["compressed_bytes"] for group in report["groups"].values()) == report["compressed_payload_bytes"]
    assert report["compressed_payload_bytes"] + report["zip_overhead_bytes"] == len(original)
    assert set(report["single_disease_scoped_groups"]) == {"DIS-AML"}
    assert report["single_disease_scoped_groups"]["DIS-AML"]["files"] == 1
    assert report["single_disease_scoped_payload_bytes"] + report["other_payload_bytes"] == report["compressed_payload_bytes"]


def test_missing_archive_never_starts_a_build(tmp_path):
    with pytest.raises(SystemExit) as error:
        profile.main(["--bundle", str(tmp_path / "missing.zip")])
    assert error.value.code == 2
    assert list(tmp_path.iterdir()) == []


def test_budget_gate_and_overwrite_guard_preserve_archive(tmp_path, monkeypatch):
    bundle = tmp_path / "core.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        archive.writestr("runtime.py", "runtime")
    original = bundle.read_bytes()
    monkeypatch.setattr(profile, "CORE_BUDGET_BYTES", 1)
    output = tmp_path / "audit.json"
    assert profile.main(["--bundle", str(bundle), "--output", str(output), "--check-budget"]) == 1
    assert json.loads(output.read_text())["over_budget_bytes"] == len(original) - 1
    assert bundle.read_bytes() == original
    with pytest.raises(SystemExit):
        profile.main(["--bundle", str(bundle), "--output", str(bundle)])
    assert bundle.read_bytes() == original
