import copy
from html.parser import HTMLParser
from pathlib import Path

import pytest

from knowledge_base.clients.openfda_client import OpenFDAEventQuery
from scripts.build_kb_wiki import KbEntity, render_entity_page
from scripts.openfda_drug_card import assets, render_openfda_card, write_assets
from scripts.build_clinical_locales import localize_page


class Tags(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.tags = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


@pytest.mark.parametrize("locale", ["en", "uk"])
def test_card_uses_adapter_query_and_never_fetches_at_build_time(monkeypatch, locale):
    monkeypatch.setattr("urllib.request.urlopen", lambda *a, **k: pytest.fail("Build must stay offline"))
    drug = {"names": {"english": "osimertinib", "brand_names": ["Tagrisso"]}}
    before = copy.deepcopy(drug)
    page = render_openfda_card(drug, locale=locale)
    section = next(attrs for tag, attrs in Tags(page).tags if tag == "section")
    assert section["data-query-url"] == OpenFDAEventQuery(active_substance="osimertinib", brand_names=("Tagrisso",), limit=5).request_url
    assert section["lang"] == locale
    assert "data-original-source" in section
    assert drug == before
    assert 'role="status"' in page and "<noscript>" in page
    assert "2026-" not in page  # No build date masquerading as FDA freshness.


def test_untrusted_aliases_cannot_create_markup_or_event_handlers():
    alias = '\"><img src=x onerror="alert(1)">'
    page = render_openfda_card({"names": {"english": alias, "brand_names": [alias]}})
    tags = Tags(page).tags
    assert not any(tag == "img" or any(key.startswith("on") for key in attrs) for tag, attrs in tags)
    assert "data-openfda-card" in next(attrs for tag, attrs in tags if tag == "section")


def test_asset_publication_matches_hashed_references(tmp_path):
    write_assets(tmp_path)
    page = render_openfda_card({"names": {"english": "imatinib"}})
    for name, payload in assets().items():
        assert (tmp_path / name).read_bytes() == payload
        assert "/" + name in page


def test_block_is_drug_only_and_does_not_replace_existing_facts():
    data = {"id": "DRUG-EXAMPLE", "names": {"english": "Example"}, "mechanism": "Existing mechanism"}
    drug = KbEntity("drugs", "Drug", "DRUG-EXAMPLE", "Example", data, Path("example.yaml"), "example.yaml")
    page = render_entity_page(drug, {drug.id: drug}, {})
    assert page.count("data-openfda-card") == 1
    assert "Existing mechanism" in page
    biomarker = KbEntity("biomarkers", "Biomarker", "BIO-EXAMPLE", "Example", {}, Path("example.yaml"), "example.yaml")
    assert "openfda" not in render_entity_page(biomarker, {biomarker.id: biomarker}, {})


def test_missing_name_has_honest_fallback_without_empty_search():
    page = render_openfda_card({"names": {}}, locale="en")
    assert "searchable medicine name is not available" in page
    assert "data-query-url" not in page
    assert "https://open.fda.gov/apis/drug/event/" in page


def test_localized_editions_preserve_original_fda_block():
    block = render_openfda_card({"names": {"english": "osimertinib"}})
    source = '<html lang="en"><head><title>Example</title></head><body><main>' + block + '</main></body></html>'
    page = localize_page(source, "de", "kb/drugs/example.html", set(), {"FDA dataset updated": "SHOULD NOT REPLACE"})
    assert "SHOULD NOT REPLACE" not in page
    assert 'lang="en" data-original-source' in page
    assert "FDA dataset updated" in page
