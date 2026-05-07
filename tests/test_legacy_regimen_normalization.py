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
