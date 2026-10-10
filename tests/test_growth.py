"""Verify discovery covers the KB and exposes audit data without new dosing."""
import json
import re
from pathlib import Path

from scripts.build_kb_wiki import KbEntity, _source_ids, render_entity_page
from scripts.build_participation import build_participation
from scripts.site_head import inject_seo_metadata


def test_nested_source_ids_are_indexed():
    assert _source_ids({"sources": [{"source_id": "SRC-A"}, "SRC-B", {"source_id": "SRC-ONCOKB"}, {"source": "SRC-A"}], "evidence_sources": [{"source": "SRC-C"}]}) == ["SRC-A", "SRC-B", "SRC-C"]


def test_regimen_and_indication_link_to_sources_and_each_other():
    regimen = KbEntity("regimens", "Regimen", "REG-X", "Regimen X", {"id": "REG-X", "name": "Regimen X", "components": [{"drug_id": "DRUG-X", "dose": "SHOULD_NOT_PUBLISH_DOSE"}]}, Path("x.yaml"), "knowledge_base/hosted/content/regimens/x.yaml")
    indication = KbEntity("indications", "Indication", "IND-X", "IND-X", {"id": "IND-X", "applicable_to": {"disease_id": "DIS-X", "line_of_therapy": 1}, "recommended_regimen": "REG-X", "sources": [{"source_id": "SRC-X"}]}, Path("i.yaml"), "knowledge_base/hosted/content/indications/i.yaml")
    entities = {e.id: e for e in (regimen, indication)}
    page = render_entity_page(indication, entities, {})
    assert 'href="/kb/regimens/reg-x.html"' in page
    assert "SRC-X" in page
    assert "not a prescription" in page
    assert "Source YAML: complete record" in page
    assert "line 1" in page
    assert "SHOULD_NOT_PUBLISH_DOSE" not in render_entity_page(regimen, entities, {})
    for path in ("kb/regimens/reg-x.html", "ukr/kb/indications/ind-x.html"):
        enriched = inject_seo_metadata(page, path=path)
        schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', enriched).group(1))
        assert schema["@type"] == "MedicalWebPage"
        assert "mainEntity" not in schema


def test_participation_resources_are_honest_and_local(tmp_path):
    build_participation(tmp_path)
    assert (tmp_path / "participate.html").is_file()
    assert (tmp_path / "ukr/participate.html").is_file()
    assert "not a completed study" in (tmp_path / "resources/evaluation-outline.md").read_text()
    assert "not submitted" in (tmp_path / "resources/launch.txt").read_text(encoding="utf-8")
    assert "not a FHIR adapter" in (tmp_path / "resources/interop-gap-analysis.md").read_text(encoding="utf-8")
