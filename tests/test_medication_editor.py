"""Compare browser medication input with the canonical engine contract."""

import json
import subprocess
from pathlib import Path

import pytest

from knowledge_base.engine.medication_input import parse_medication_input
from scripts.medication_editor import COPY, render_medication_editor

ROOT = Path(__file__).resolve().parents[1]


def test_editor_catalog_and_contract():
    rendered = render_medication_editor("en")
    config = json.loads(
        rendered.splitlines()[0].removeprefix("const medicationEditorConfig = ").removesuffix(";")
    )
    known = {drug["id"] for drug in config["drugs"]}
    assert len(known) == len(config["drugs"])
    assert "DRUG-BLEOMYCIN" in known
    cases = [
        None,
        {"status": "unknown", "drug_ids": []},
        {"status": "partial", "drug_ids": ["DRUG-BLEOMYCIN"]},
        {"status": "complete", "drug_ids": []},
        {"status": "complete", "drug_ids": ["DRUG-BLEOMYCIN"]},
        {"status": "unknown", "drug_ids": ["DRUG-BLEOMYCIN"]},
        {"status": "partial", "drug_ids": ["Bleomycin"]},
        {"status": "partial", "drug_ids": ["DRUG-BLEOMYCIN"] * 2},
        {"status": "complete", "drug_ids": [], "extra": True},
        {"status": "complete"},
        {"status": True, "drug_ids": []},
        [],
    ]
    expected = []
    for value in cases:
        try:
            parsed = parse_medication_input({"concomitant_medications": value}, known)
            expected.append({"status": parsed.status, "drug_ids": list(parsed.drug_ids)})
        except ValueError:
            expected.append(None)
    source = (
        (ROOT / "scripts/medication_editor.js")
        .read_text(encoding="utf-8")
        .split("(function installMedicationEditor()", 1)[0]
    )
    runner = (
        source
        + "\nconst cases="
        + json.dumps(cases)
        + ";const catalog="
        + json.dumps(config["drugs"])
        + ";\nconsole.log(JSON.stringify(cases.map(value=>{try{return medicationEditorState({concomitant_medications:value},catalog)}catch{return null}})));"
    )
    result = subprocess.run(["node", "-e", runner], capture_output=True, text=True, check=True)
    assert json.loads(result.stdout) == expected


@pytest.mark.parametrize("locale", list(COPY))
def test_medication_copy_is_complete(locale):
    assert set(COPY[locale]) == set(COPY["en"])
    assert all(isinstance(value, str) and value for value in COPY[locale].values())
    if locale != "en":
        assert COPY[locale]["notice"] != COPY["en"]["notice"]
        assert COPY[locale]["complete"] != COPY["en"]["complete"]
