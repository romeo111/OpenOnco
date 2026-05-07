from pathlib import Path

import yaml

from knowledge_base.schemas.regimen import Regimen
from knowledge_base.validation.loader import clear_load_cache, load_content


def test_regimen_schema_accepts_legacy_agents_shape() -> None:
    regimen = Regimen.model_validate({
        "id": "REG-BEP-GCT",
        "agents": [
            {
                "drug_id": "DRG-BLEOMYCIN",
                "dose": "10 units/m2",
                "schedule": "Days 1, 8, 15",
                "route": "IV",
            },
            {
                "drug_id": "DRG-FLUOROURACIL",
                "dose": "1000 mg/m2/day",
                "schedule": "Continuous infusion",
                "route": "IV_CI",
            },
        ],
        "total_planned_cycles": "3-4 cycles",
    })

    assert regimen.name == "BEP GCT"
    assert regimen.total_cycles == "3-4 cycles"
    assert [c.drug_id for c in regimen.components] == [
        "DRUG-BLEOMYCIN",
        "DRUG-5-FLUOROURACIL",
    ]
    assert regimen.phases[0].name == "main"
    assert [c.drug_id for c in regimen.phases[0].components] == [
        "DRUG-BLEOMYCIN",
        "DRUG-5-FLUOROURACIL",
    ]


def test_loader_stores_normalized_legacy_regimen_components(tmp_path: Path) -> None:
    clear_load_cache()

    drugs_dir = tmp_path / "drugs"
    regimens_dir = tmp_path / "regimens"
    drugs_dir.mkdir()
    regimens_dir.mkdir()

    (drugs_dir / "bleomycin.yaml").write_text(
        yaml.safe_dump({
            "id": "DRUG-BLEOMYCIN",
            "names": {"preferred": "Bleomycin"},
        }),
        encoding="utf-8",
    )
    (regimens_dir / "reg_bep.yaml").write_text(
        yaml.safe_dump({
            "id": "REG-BEP-GCT",
            "agents": [{
                "drug_id": "DRG-BLEOMYCIN",
                "dose": "10 units/m2",
                "schedule": "Days 1, 8, 15",
                "route": "IV",
            }],
        }),
        encoding="utf-8",
    )

    result = load_content(tmp_path)

    assert not result.schema_errors
    assert not result.ref_errors
    regimen = result.entities_by_id["REG-BEP-GCT"]["data"]
    assert regimen["name"] == "BEP GCT"
    assert regimen["components"] == [{
        "drug_id": "DRUG-BLEOMYCIN",
        "dose": "10 units/m2",
        "schedule": "Days 1, 8, 15",
        "route": "IV",
    }]


def test_loader_warns_on_legacy_supportive_care_text(tmp_path: Path) -> None:
    clear_load_cache()

    drugs_dir = tmp_path / "drugs"
    regimens_dir = tmp_path / "regimens"
    drugs_dir.mkdir()
    regimens_dir.mkdir()

    (drugs_dir / "bleomycin.yaml").write_text(
        yaml.safe_dump({
            "id": "DRUG-BLEOMYCIN",
            "names": {"preferred": "Bleomycin"},
        }),
        encoding="utf-8",
    )
    (regimens_dir / "reg_bep.yaml").write_text(
        yaml.safe_dump({
            "id": "REG-BEP-GCT",
            "name": "BEP",
            "components": [{"drug_id": "DRUG-BLEOMYCIN"}],
            "mandatory_supportive_care": [
                "CBC before each cycle",
                "SUP-MISSING",
            ],
        }),
        encoding="utf-8",
    )

    result = load_content(tmp_path)

    assert not result.schema_errors
    assert any("legacy free text" in msg for _path, msg in result.contract_warnings)
    assert any("SUP-MISSING" in msg for _path, msg in result.ref_errors)
    assert not any("CBC before each cycle" in msg for _path, msg in result.ref_errors)


def test_hosted_regimen_component_drug_refs_resolve() -> None:
    clear_load_cache()

    result = load_content(Path("knowledge_base/hosted/content"))

    assert result.ok
    regimen_drug_ref_errors = [
        (path, msg)
        for path, msg in result.ref_errors
        if path.parts[-2] == "regimens" and "components[" in msg
    ]
    assert regimen_drug_ref_errors == []


def test_loader_normalizes_legacy_indication_shapes(tmp_path: Path) -> None:
    clear_load_cache()

    for dirname in ("diseases", "regimens", "drugs", "indications"):
        (tmp_path / dirname).mkdir()

    (tmp_path / "diseases" / "dis_test.yaml").write_text(
        yaml.safe_dump({
            "id": "DIS-TEST",
            "names": {"preferred": "Test disease"},
            "codes": {},
        }),
        encoding="utf-8",
    )
    (tmp_path / "drugs" / "drug_test.yaml").write_text(
        yaml.safe_dump({
            "id": "DRUG-TEST",
            "names": {"preferred": "Test drug"},
        }),
        encoding="utf-8",
    )
    (tmp_path / "regimens" / "reg_test.yaml").write_text(
        yaml.safe_dump({
            "id": "REG-TEST",
            "name": "Test regimen",
            "components": [{"drug_id": "DRUG-TEST"}],
        }),
        encoding="utf-8",
    )
    (tmp_path / "indications" / "ind_test.yaml").write_text(
        yaml.safe_dump({
            "id": "IND-TEST",
            "applicable_to": {
                "disease_id": "DIS-TEST",
                "line_of_therapy": 1,
                "biomarker_requirements_excluded": ["free-text exclusion"],
            },
            "recommended_regimen": "REG-TEST",
            "strength_of_recommendation": "moderate",
            "red_flags_triggering_alternative": [{
                "condition": "legacy prose trigger",
            }],
            "hard_contraindications": ["ECOG PS >= 3"],
            "required_tests": ["CBC baseline", "TEST-MISSING"],
        }),
        encoding="utf-8",
    )

    result = load_content(tmp_path)

    assert not result.schema_errors
    assert any("legacy free text" in msg for _path, msg in result.contract_warnings)
    assert any("TEST-MISSING" in msg for _path, msg in result.ref_errors)
    assert not any("CBC baseline" in msg for _path, msg in result.ref_errors)
    ind = result.entities_by_id["IND-TEST"]["data"]
    assert ind["strength_of_recommendation"] == "conditional"
    assert ind["red_flags_triggering_alternative"] == []
