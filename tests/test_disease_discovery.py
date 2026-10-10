"""Disease landing pages must expose real names and safe, localized JSON-LD."""

import json
import re

import pytest

from scripts.site_head import inject_seo_metadata


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
