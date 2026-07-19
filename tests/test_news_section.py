"""Tests for the bilingual news section and its comment layer.

These build only the news pages (and the service worker) rather than the whole
site, so the suite stays fast enough to run on every change.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import build_news  # noqa: E402
from scripts.build_news import (  # noqa: E402
    NewsContentError,
    build_news as build_news_pages,
    load_news_entries,
    render_comments,
)
from scripts.build_site import _render_top_bar, write_service_worker  # noqa: E402
from scripts.site_head import _description_for, _schema_type  # noqa: E402


MINIMAL_POST = {
    "slug": "test-post",
    "tags": ["testing"],
    "body": {
        "en": [{"type": "p", "text": "Body in English."}],
        "uk": [{"type": "p", "text": "Текст українською."}],
    },
    "title": {"en": "Test post", "uk": "Тестовий допис"},
    "summary": {"en": "A summary.", "uk": "Опис."},
}


def _write_post(directory: Path, name: str, **overrides) -> Path:
    # A real date object, so safe_dump emits an unquoted YAML timestamp rather
    # than a quoted string that would load back as str and trip date validation.
    payload = {**json.loads(json.dumps(MINIMAL_POST)), "date": date(2026, 1, 15)}
    payload.update(overrides)
    path = directory / name
    path.write_text(yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8")
    return path


@pytest.fixture(scope="module")
def news_dir(tmp_path_factory) -> Path:
    """Real content built into a temp dir."""
    out = tmp_path_factory.mktemp("news_site")
    build_news_pages(out, top_bar=_render_top_bar)
    return out


# ── content loading ─────────────────────────────────────────────────────────

def test_repo_news_content_is_valid():
    """The checked-in articles must parse — a typo should fail the build."""
    entries = load_news_entries()
    assert entries, "no news articles found in content/news/"
    for entry in entries:
        for lang in ("en", "uk"):
            assert entry["title"][lang].strip()
            assert entry["summary"][lang].strip()
            assert entry["body"][lang], f"{entry['slug']} has no {lang} body"


def test_entries_sorted_newest_first():
    dates = [e["date"] for e in load_news_entries()]
    assert dates == sorted(dates, reverse=True)


@pytest.mark.parametrize("overrides,fragment", [
    ({"slug": "Not Kebab"}, "kebab-case"),
    ({"date": "not-a-date"}, "ISO date"),
    ({"title": {"en": "only english"}}, "missing uk"),
    ({"body": {"en": [], "uk": [{"type": "p", "text": "x"}]}}, "non-empty list"),
    ({"body": {"en": [{"type": "marquee", "text": "x"}],
               "uk": [{"type": "p", "text": "x"}]}}, "unknown type"),
])
def test_malformed_content_raises(tmp_path, overrides, fragment):
    _write_post(tmp_path, "bad.yaml", **overrides)
    with pytest.raises(NewsContentError) as excinfo:
        load_news_entries(tmp_path)
    assert fragment in str(excinfo.value)


def test_duplicate_slug_rejected(tmp_path):
    _write_post(tmp_path, "a.yaml")
    _write_post(tmp_path, "b.yaml")
    with pytest.raises(NewsContentError, match="duplicate slug"):
        load_news_entries(tmp_path)


# ── escaping and link safety ────────────────────────────────────────────────

def test_raw_html_in_yaml_is_escaped(tmp_path):
    _write_post(tmp_path, "x.yaml", body={
        "en": [{"type": "p", "text": "<script>alert(1)</script>"}],
        "uk": [{"type": "p", "text": "текст"}],
    })
    entry = load_news_entries(tmp_path)[0]
    html = build_news.render_news_article(entry, target_lang="en", top_bar_html="")
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


@pytest.mark.parametrize("url", [
    "javascript:alert",      # rejected by _safe_href
    "data:text/html,x",      # rejected by _safe_href
    "//evil.test",           # protocol-relative, rejected by _safe_href
    "javascript:alert(1)",   # parens mean the link regex never fires at all
])
def test_dangerous_link_targets_never_become_anchors(tmp_path, url):
    _write_post(tmp_path, "x.yaml", body={
        "en": [{"type": "p", "text": f"see [here]({url}) now"}],
        "uk": [{"type": "p", "text": "текст"}],
    })
    entry = load_news_entries(tmp_path)[0]
    html = build_news.render_news_article(entry, target_lang="en", top_bar_html="")
    body = html.split('class="news-body', 1)[1].split("</div>", 1)[0]
    assert "<a " not in body, f"{url!r} must not produce an anchor"
    assert "href" not in body


def test_external_links_get_noopener(tmp_path):
    _write_post(tmp_path, "x.yaml", body={
        "en": [{"type": "p", "text": "see [CIViC](https://civicdb.org/)"}],
        "uk": [{"type": "p", "text": "текст"}],
    })
    entry = load_news_entries(tmp_path)[0]
    html = build_news.render_news_article(entry, target_lang="en", top_bar_html="")
    assert '<a href="https://civicdb.org/" target="_blank" rel="noopener noreferrer">' in html


# ── page output ─────────────────────────────────────────────────────────────

def test_both_locales_built(news_dir: Path):
    assert (news_dir / "news.html").exists()
    assert (news_dir / "ukr" / "news.html").exists()
    for entry in load_news_entries():
        assert (news_dir / "news" / f"{entry['slug']}.html").exists()
        assert (news_dir / "ukr" / "news" / f"{entry['slug']}.html").exists()


def test_index_lists_every_post(news_dir: Path):
    index = (news_dir / "news.html").read_text(encoding="utf-8")
    for entry in load_news_entries():
        assert f'href="/news/{entry["slug"]}.html"' in index
        assert entry["title"]["en"] in index


def test_article_lang_switch_points_at_mirror(news_dir: Path):
    slug = load_news_entries()[0]["slug"]
    en = (news_dir / "news" / f"{slug}.html").read_text(encoding="utf-8")
    ua = (news_dir / "ukr" / "news" / f"{slug}.html").read_text(encoding="utf-8")
    assert f'href="/ukr/news/{slug}.html"' in en
    assert f'href="/news/{slug}.html"' in ua


def test_pages_use_root_relative_stylesheet(news_dir: Path):
    for rel in ("news.html", "ukr/news.html"):
        html = (news_dir / rel).read_text(encoding="utf-8")
        assert 'href="/style.css"' in html
        assert '<link href="style.css"' not in html


def test_title_uses_site_convention(news_dir: Path):
    """site_head.inject_seo_metadata scrapes `OpenOnco · <title>`."""
    assert "<title>OpenOnco · News</title>" in (
        news_dir / "news.html").read_text(encoding="utf-8")
    assert "<title>OpenOnco · Новини</title>" in (
        news_dir / "ukr" / "news.html").read_text(encoding="utf-8")


def test_news_index_json_shape(news_dir: Path):
    payload = json.loads((news_dir / "news_index.json").read_text(encoding="utf-8"))
    assert payload["kind"] == "openonco_news_index"
    assert payload["count"] == len(load_news_entries())
    for post in payload["posts"]:
        assert post["url"]["en"].startswith("/news/")
        assert post["url"]["uk"].startswith("/ukr/news/")


# ── navigation ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("lang,label,href", [
    ("en", "News", "/news.html"),
    ("uk", "Новини", "/ukr/news.html"),
])
def test_news_in_top_nav_for_both_locales(lang, label, href):
    html = _render_top_bar(active="news", target_lang=lang)
    nav = html.split('<nav class="top-nav">', 1)[1].split("</nav>", 1)[0]
    assert f'href="{href}"' in nav
    assert label in nav


def test_active_news_marks_nav_link():
    assert 'href="/news.html" class="active"' in _render_top_bar(
        active="news", target_lang="en")


# ── comments ────────────────────────────────────────────────────────────────

def test_house_rules_present_in_both_languages(news_dir: Path):
    slug = load_news_entries()[0]["slug"]
    en = (news_dir / "news" / f"{slug}.html").read_text(encoding="utf-8")
    ua = (news_dir / "ukr" / "news" / f"{slug}.html").read_text(encoding="utf-8")
    assert "Do not post personal medical data" in en
    assert "not medical advice" in en
    assert "Не публікуйте персональні медичні дані" in ua
    assert "не є медичною порадою" in ua


def test_comments_degrade_to_link_when_unconfigured(monkeypatch):
    monkeypatch.setitem(build_news.GISCUS, "repo_id", "")
    monkeypatch.setitem(build_news.GISCUS, "category_id", "")
    entry = load_news_entries()[0]
    html = render_comments(entry, "en")
    assert "giscus.app/client.js" not in html
    assert "github.com/romeo111/OpenOnco/discussions" in html


def test_configured_comments_are_click_to_load(monkeypatch):
    """The widget must not auto-load: no third-party request on a passive read."""
    monkeypatch.setitem(build_news.GISCUS, "repo_id", "R_test")
    monkeypatch.setitem(build_news.GISCUS, "category_id", "DIC_test")
    entry = load_news_entries()[0]
    html = render_comments(entry, "en")
    assert 'id="load-comments"' in html
    assert "addEventListener('click'" in html
    # The giscus script tag must be created by JS, never present in the markup.
    assert "<script src=" not in html
    assert 'data-repo-id="R_test"' in html
    assert f'data-term="news/{entry["slug"]}"' in html


def test_giscus_language_follows_page_locale(monkeypatch):
    monkeypatch.setitem(build_news.GISCUS, "repo_id", "R_test")
    monkeypatch.setitem(build_news.GISCUS, "category_id", "DIC_test")
    entry = load_news_entries()[0]
    assert 'data-lang="uk"' in render_comments(entry, "uk")
    assert 'data-lang="en"' in render_comments(entry, "en")


# ── service worker ──────────────────────────────────────────────────────────

def test_service_worker_ignores_cross_origin(tmp_path):
    """Without this guard the SW intercepts the giscus iframe navigation."""
    write_service_worker(tmp_path, core_version="testver")
    sw = (tmp_path / "sw.js").read_text(encoding="utf-8")
    guard = sw.index("url.origin !== self.location.origin")
    navigate = sw.index("event.request.mode === 'navigate'")
    assert guard < navigate, "same-origin guard must precede the navigation branch"


def test_service_worker_serves_news_stale_while_revalidate(tmp_path):
    write_service_worker(tmp_path, core_version="testver")
    sw = (tmp_path / "sw.js").read_text(encoding="utf-8")
    assert "'/news.html'" in sw
    assert "'/ukr/news.html'" in sw
    assert "SWR_PREFIXES" in sw
    # HTML must never be cache-first, or readers get stuck on an old build.
    cache_first = sw.split("const cacheFirstMatch", 1)[1].split(";", 1)[0]
    assert "news" not in cache_first


def test_service_worker_cache_prefix_bumped(tmp_path):
    """A routing change needs a new cache bucket or old SWs keep serving."""
    payload = write_service_worker(tmp_path, core_version="testver")
    assert payload["cache_name"].startswith("openonco-bundle-l4-")


# ── SEO wiring ──────────────────────────────────────────────────────────────

def test_news_article_is_typed_as_article():
    assert _schema_type("news/news-and-comments.html") == "NewsArticle"
    assert _schema_type("ukr/news/news-and-comments.html") == "NewsArticle"
    assert _schema_type("news.html") == "WebPage"


def test_article_description_uses_its_own_summary():
    entry = load_news_entries()[0]
    slug = entry["slug"]
    assert _description_for(f"news/{slug}.html", "t", "en") == entry["summary"]["en"]
    assert _description_for(f"ukr/news/{slug}.html", "t", "uk") == entry["summary"]["uk"]


def test_news_index_has_its_own_description():
    description = _description_for("news.html", "OpenOnco · News", "en")
    assert "release notes" in description.lower()
