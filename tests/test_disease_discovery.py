"""Disease landing pages must expose real names and safe, localized JSON-LD."""

import json
import re
from pathlib import Path

import pytest

from scripts.site_head import inject_seo_metadata
from scripts.build_kb_wiki import KbEntity, render_entity_page


@pytest.mark.parametrize("prefix,name", [("", "Lung cancer & subtypes"), ("ukr/", "Рак легені"), ("", 'Cancer "variant" \\ subtype')])
def test_disease_schema_matches_visible_heading(prefix, name):
    source = f'<html><head><title>Onco Wiki</title></head><body><h1>{name}</h1></body></html>'
    rendered = inject_seo_metadata(source, path=f"{prefix}kb/diseases/dis-nsclc.html")
    block = re.search(r'<script type="application/ld\+json">(.*?)</script>', rendered).group(1)
    schema = json.loads(block)
    assert schema["@type"] == "MedicalWebPage"
    assert schema["mainEntity"]["@type"] == "MedicalCondition"
    assert schema["mainEntity"]["name"] == name
    assert schema["mainEntity"]["url"] == f"https://openonco.info/{prefix}kb/diseases/dis-nsclc.html"
    assert inject_seo_metadata(rendered, path=f"{prefix}kb/diseases/dis-nsclc.html") == rendered


def test_drug_page_is_not_classified_as_disease():
    rendered = inject_seo_metadata('<head><title>Drug</title></head><h1>Drug</h1>', path="kb/drugs/drug-x.html")
    schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', rendered).group(1))
    assert "mainEntity" not in schema


def test_disease_page_links_to_public_yaml_provenance():
    entity = KbEntity("diseases", "Disease", "DIS-EXAMPLE", "Example", {"id": "DIS-EXAMPLE"}, Path("example.yaml"), "knowledge_base/hosted/content/diseases/example.yaml")
    page = render_entity_page(entity, {entity.id: entity}, {})
    assert 'href="https://github.com/romeo111/OpenOnco/blob/master/knowledge_base/hosted/content/diseases/example.yaml"' in page
    assert "two-reviewer sign-off" in page
