"""Tests for the bilingual news section and its comment layer.

These build only the news pages (and the service worker) rather than the whole
site, so the suite stays fast enough to run on every change.
"""

from __future__ import annotations

import html
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
from scripts import site_head  # noqa: E402
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
        # Escaped, not raw: a title containing an apostrophe or angle bracket
        # must reach the page encoded.
        assert html.escape(entry["title"]["en"], quote=True) in index


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


# ── backfilled posts ────────────────────────────────────────────────────────

def test_backfilled_post_says_it_was_written_later(tmp_path):
    """A post about an old event must not imply it was published back then."""
    _write_post(tmp_path, "x.yaml", date=date(2026, 4, 27), published=date(2026, 7, 19))
    entry = load_news_entries(tmp_path)[0]
    en = build_news.render_news_article(entry, target_lang="en", top_bar_html="")
    ua = build_news.render_news_article(entry, target_lang="uk", top_bar_html="")
    assert "Written retrospectively and published on July 19, 2026." in en
    assert "Написано ретроспективно, опубліковано 19 липня 2026." in ua
    # The dateline still shows the date of the event being described.
    assert "April 27, 2026" in en


def test_ordinary_post_has_no_retro_note(tmp_path):
    _write_post(tmp_path, "x.yaml")
    entry = load_news_entries(tmp_path)[0]
    html = build_news.render_news_article(entry, target_lang="en", top_bar_html="")
    assert "retrospectively" not in html
    assert entry["published"] is None


def test_published_before_date_is_rejected(tmp_path):
    _write_post(tmp_path, "x.yaml", date=date(2026, 7, 19), published=date(2026, 4, 27))
    with pytest.raises(NewsContentError, match="precedes"):
        load_news_entries(tmp_path)


def test_structured_data_reports_real_publication_date():
    """datePublished must be when the post appeared, not what it is about."""
    entry = load_news_entries()[0]
    published, modified = site_head._news_dates(f"news/{entry['slug']}.html")
    expected = (entry["published"] or entry["date"]).isoformat()
    assert published == expected
    assert modified == entry["date"].isoformat()
    assert site_head._news_dates("about.html") is None


# ── explainer posts ─────────────────────────────────────────────────────────

SRC = [{"citation": "Martincorena et al., Science 2015", "id": "25999502"}]


def test_explainer_without_sources_is_rejected(tmp_path):
    """An uncited clinical claim must not reach a public medical page."""
    _write_post(tmp_path, "x.yaml", kind="explainer")
    with pytest.raises(NewsContentError, match="must cite at least one source"):
        load_news_entries(tmp_path)


def test_project_post_needs_no_sources(tmp_path):
    _write_post(tmp_path, "x.yaml")
    entry = load_news_entries(tmp_path)[0]
    assert entry["kind"] == "project"
    assert entry["sources"] == []


def test_unknown_kind_is_rejected(tmp_path):
    _write_post(tmp_path, "x.yaml", kind="opinion")
    with pytest.raises(NewsContentError, match="'kind' must be one of"):
        load_news_entries(tmp_path)


@pytest.mark.parametrize("bad,fragment", [
    ([{"citation": "No id here"}], "needs an 'id'"),
    ([{"id": "25999502"}], "needs a 'citation'"),
])
def test_incomplete_source_is_rejected(tmp_path, bad, fragment):
    _write_post(tmp_path, "x.yaml", kind="explainer", sources=bad)
    with pytest.raises(NewsContentError, match=fragment):
        load_news_entries(tmp_path)


def test_explainer_renders_note_and_reference_list(tmp_path):
    _write_post(tmp_path, "x.yaml", kind="explainer", sources=SRC)
    entry = load_news_entries(tmp_path)[0]
    en = build_news.render_news_article(entry, target_lang="en", top_bar_html="")
    ua = build_news.render_news_article(entry, target_lang="uk", top_bar_html="")
    assert "Background reading, not clinical guidance" in en
    assert "не клінічна настанова" in ua
    assert "news-sources" in en
    assert "Martincorena" in en
    # A bare PMID becomes a PubMed link.
    assert "https://pubmed.ncbi.nlm.nih.gov/25999502/" in en


def test_project_post_has_no_explainer_furniture(tmp_path):
    _write_post(tmp_path, "x.yaml")
    entry = load_news_entries(tmp_path)[0]
    html = build_news.render_news_article(entry, target_lang="en", top_bar_html="")
    assert "news-kind-note" not in html
    assert "news-sources" not in html


@pytest.mark.parametrize("identifier,expected", [
    ("25999502", "https://pubmed.ncbi.nlm.nih.gov/25999502/"),
    ("PMID:25999502", "https://pubmed.ncbi.nlm.nih.gov/25999502/"),
    ("10.1126/science.aaa6806", "https://doi.org/10.1126/science.aaa6806"),
    ("doi:10.1126/science.aaa6806", "https://doi.org/10.1126/science.aaa6806"),
    ("https://www.nccn.org/x", "https://www.nccn.org/x"),
])
def test_source_identifiers_become_links(identifier, expected):
    assert build_news._source_href(identifier) == expected


def test_unlinkable_source_identifier_stays_plain_text():
    assert build_news._source_href("NCCN Guidelines v3.2026") is None


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

@pytest.fixture
def waline(monkeypatch):
    monkeypatch.setitem(build_news.COMMENTS, "provider", "waline")
    monkeypatch.setitem(build_news.COMMENTS, "server_url", "https://comments.example.test")
    return load_news_entries()[0]


def test_both_language_versions_share_one_thread(waline):
    """The whole point: one discussion per article, not one per translation."""
    en = render_comments(waline, "en")
    ua = render_comments(waline, "uk")
    key = f'"path": "/news/{waline["slug"]}"'
    assert key in en
    assert key in ua
    # No language prefix may leak into the thread key.
    assert "/ukr/" not in en.split('"path"')[1].split(",")[0]
    assert "/ukr/" not in ua.split('"path"')[1].split(",")[0]


def test_commenting_needs_no_account(waline):
    html = render_comments(waline, "en")
    assert '"login": "disable"' in html
    assert '"requiredMeta": []' in html


def test_no_third_party_emoji_fetch(waline):
    """Waline's default emoji packs are fetched from unpkg at runtime."""
    assert '"emoji": false' in render_comments(waline, "en")


def test_ukrainian_ui_strings_supplied_not_russian(waline):
    """Waline has no Ukrainian locale and must never fall back to Russian."""
    ua = render_comments(waline, "uk")
    assert '"locale"' in ua
    assert "Надіслати" in ua
    assert '"lang": "ru"' not in ua
    assert '"locale"' not in render_comments(waline, "en")


def test_short_note_replaces_the_old_rules_panel(news_dir: Path):
    slug = load_news_entries()[0]["slug"]
    en = (news_dir / "news" / f"{slug}.html").read_text(encoding="utf-8")
    ua = (news_dir / "ukr" / "news" / f"{slug}.html").read_text(encoding="utf-8")
    assert "personal medical data" in en
    assert "персональні медичні дані" in ua
    assert "news-comments-note" in en
    assert "news-comment-rules" not in en, "the heavy rules panel should be gone"


def test_config_cannot_break_out_of_the_script_tag(monkeypatch):
    monkeypatch.setitem(build_news.COMMENTS, "provider", "waline")
    monkeypatch.setitem(
        build_news.COMMENTS, "server_url", "https://x.test/</script><img src=x>",
    )
    html = render_comments(load_news_entries()[0], "uk")
    assert "</script><img" not in html
    assert "<\\/script>" in html


def test_comments_say_so_when_unconfigured(monkeypatch):
    monkeypatch.setitem(build_news.COMMENTS, "server_url", "")
    entry = load_news_entries()[0]
    html = render_comments(entry, "en")
    assert "not switched on yet" in html
    assert "waline.js" not in html


@pytest.mark.parametrize("provider,needle", [
    ("remark42", "remark_config"),
    ("disqus", "disqus_thread"),
])
def test_provider_is_swappable(monkeypatch, provider, needle):
    """Cusdis was archived 2026-07-17; no single vendor may be load-bearing."""
    monkeypatch.setitem(build_news.COMMENTS, "provider", provider)
    monkeypatch.setitem(build_news.COMMENTS, "server_url", "https://c.example.test")
    monkeypatch.setitem(build_news.COMMENTS, "shortname", "openonco")
    assert needle in render_comments(load_news_entries()[0], "en")


# ── service worker ──────────────────────────────────────────────────────────

def test_service_worker_ignores_cross_origin(tmp_path):
    """Without this guard the SW intercepts the comment widget's iframe."""
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
