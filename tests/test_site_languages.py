"""Localization must preserve source provenance, quiz grading and real URLs."""
import json
import re
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree as ET

import pytest
import yaml

from scripts.build_handbook import render_chapter, render_handbook_index, _chapter_index_record
from scripts.build_international import build_international, SEARCH_COPY
from scripts.handbook_localization import translate_content
from scripts.site_head import finalize_site_discovery
from scripts.site_locales import COPY, LOCALES, locale_path
from scripts.site_nav import render_top_bar

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def handbook_load():
    entities = {}
    for kind in ("handbook_chapters", "handbook_questions"):
        for file in (ROOT / "knowledge_base/hosted/content" / kind).glob("*.yaml"):
            data = yaml.safe_load(file.read_text(encoding="utf-8"))
            entities[data["id"]] = {"type": kind, "data": data}
    return SimpleNamespace(entities_by_id=entities)


def test_ukrainian_chapters_preserve_grading_sources_and_review(handbook_load):
    for record in handbook_load.entities_by_id.values():
        data = record["data"]
        translated = translate_content(data)
        for field in ("id", "source_ids", "review_status", "correct_answer", "linked_entity_ids", "question_ids"):
            assert translated.get(field) == data.get(field)
        if record["type"] != "handbook_chapters":
            assert translated["stem"] != data["stem"]
            assert [o["key"] for o in translated["options"]] == [o["key"] for o in data["options"]]
            continue
        en, uk = render_chapter(handbook_load, data), render_chapter(handbook_load, data, "uk")
        assert '<html lang="uk">' in uk and 'Клінічне рев’ю перекладу очікується' in uk
        assert 'Практичні запитання' in uk and "'✓ Правильно'" in uk
        assert "'Pick an option first.'" not in uk
        assert re.findall(r'data-correct-answer="([^"]*)"', uk) == re.findall(r'data-correct-answer="([^"]*)"', en)
        assert re.findall(r'data-question-id="([^"]*)"', uk) == re.findall(r'data-question-id="([^"]*)"', en)
        assert set(re.findall(r'SRC-[A-Z0-9_-]+', uk)) == set(re.findall(r'SRC-[A-Z0-9_-]+', en))
        assert 'href="/ukr/handbook.html"' in uk
    index = render_handbook_index(handbook_load, "uk")
    assert 'Навчальні розділи з онкології' in index
    assert "' розділів'" in index and 'data-status="draft"' in index


def test_missing_translation_cannot_silently_reuse_stale_prose():
    with pytest.raises(ValueError, match="Missing Ukrainian"):
        translate_content({"body": "New clinical prose not yet translated"})


def test_international_build_and_reciprocal_discovery(tmp_path, handbook_load):
    entries = [{"id": "DRUG-RITUXIMAB", "title": "Rituximab", "search_text": "rituximab mabthera", "kind_key": "drugs", "url": "/kb/drugs/rituximab.html"}]
    (tmp_path / "kb_search_index.json").write_text(json.dumps({"entries": entries, "counts": {"Disease": 103, "Drugs": 321, "Biomarkers": 257}}), encoding="utf-8")
    chapters = [_chapter_index_record(handbook_load, e["data"]) for e in handbook_load.entities_by_id.values() if e["type"] == "handbook_chapters"]
    (tmp_path / "handbook_index.json").write_text(json.dumps({"chapters": chapters}), encoding="utf-8")
    for name in ("index.html", "about.html", "kb.html", "participate.html", "handbook.html"):
        for code in ("en", "uk"):
            path = tmp_path / locale_path(name, code)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('<html><head><title>OpenOnco</title></head><body></body></html>', encoding="utf-8")
    payload = build_international(tmp_path)
    assert len(payload["pages"]) == 48
    for code, t in COPY.items():
        home = (tmp_path / code / "index.html").read_text(encoding="utf-8")
        assert f'<html lang="{code}">' in home and t["title"] in home
        assert '<strong>321</strong>' in home and '<strong>257</strong>' in home
        wiki = (tmp_path / code / "kb.html").read_text(encoding="utf-8")
        assert SEARCH_COPY[code][14] in wiki
        assert 'e.search_text' in wiki and "fetch('/kb_search_index.json')" in wiki
        assert 'card.lang = \'en\'' in wiki and 'p.set(\'q\'' in wiki
        assert '<option value="indications">' in wiki and '<option value="regimens">' in wiki
        assert (tmp_path / code / "participate.html").is_file()
        assert t["english_note"] in (tmp_path / code / "try.html").read_text(encoding="utf-8")
        handbook = (tmp_path / code / "handbook.html").read_text(encoding="utf-8")
        assert f'<code>{t["draft"]}</code>' in handbook
        assert '<code>draft</code>' not in handbook
    finalize_site_discovery(tmp_path, stats={})
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
    for node in ET.parse(tmp_path / "sitemap.xml").getroot().findall("s:url", ns):
        if node.find("s:loc", ns).text.endswith(("/", "about.html", "kb.html", "participate.html", "handbook.html")):
            assert {n.get("hreflang") for n in node.findall("x:link", ns)} == set(LOCALES) | {"x-default"}
    es = (tmp_path / "es/index.html").read_text(encoding="utf-8")
    assert '"inLanguage":"es"' in es
    assert 'rel="canonical" href="https://openonco.info/es/"' in es
    assert f'<meta name="description" content="{COPY["es"]["lead"]}">' in es
    introduction = (tmp_path / "es/try.html").read_text(encoding="utf-8")
    assert 'hreflang="en"' not in introduction.split('</head>', 1)[0]
    assert '"@type":"SoftwareApplication"' not in introduction
    assert finalize_site_discovery(tmp_path, stats={})["html_pages_enriched"] == 0


@pytest.mark.parametrize("locale", LOCALES)
def test_language_menu_maps_pages_and_deep_fallbacks(locale):
    header = render_top_bar("kb", locale, page_path="kb.html")
    for code in LOCALES:
        assert f'href="/{locale_path("kb.html", code)}" lang="{code}" hreflang="{code}"' in header
    entity = render_top_bar("kb", locale, page_path="kb/drugs/rituximab.html")
    for code in COPY:
        assert f'href="/{code}/" lang="{code}"' in entity
        assert f'/{code}/kb/drugs/' not in entity
