"""Build the OpenOnco news section (bilingual) with open comments.

News is editorial content, not clinical knowledge base content. It lives in
`content/news/*.yaml` rather than under `knowledge_base/hosted/content/` so it
does not enter the CHARTER §6.1 two-reviewer clinical-signoff path, and so a
project announcement can never be mistaken for a source-cited clinical claim.

Article bodies are structured blocks (paragraph / heading / list / quote /
callout / code), not Markdown: the repo declares only pydantic, httpx and
pyyaml, and no Markdown parser is importable under the required Python 3.12
interpreter or in CI. Leaf text is HTML-escaped first, then a small inline
formatter re-introduces links, bold and code. Raw HTML in YAML stays escaped.

Comments use giscus (GitHub Discussions) and are loaded only after an explicit
click, so no third-party request leaves the browser until a reader opts in.
Until the repo owner enables Discussions and installs the giscus app, the
widget degrades to a plain link to the GitHub discussion space — see
`docs/news-comments-setup.md`.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Callable

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DEFAULT_NEWS_DIR = REPO_ROOT / "content" / "news"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "docs"

GH_REPO = "romeo111/OpenOnco"

# ── giscus configuration ────────────────────────────────────────────────────
# `repo_id` and `category_id` come from https://giscus.app after the repo owner
# (a) turns on GitHub Discussions and (b) installs the giscus app. Both are
# public identifiers, not secrets. While either is blank, comments render as a
# link-out instead of an embedded widget — the section still ships and works.
GISCUS = {
    "repo": GH_REPO,
    "repo_id": "",
    "category": "Announcements",
    "category_id": "",
    "host": "https://giscus.app",
}

DISCUSSIONS_URL = f"https://github.com/{GH_REPO}/discussions"

BLOCK_TYPES = {"p", "h2", "h3", "ul", "ol", "quote", "callout", "code"}
CALLOUT_TONES = {"info": "", "good": " callout-good", "warn": " callout-hard"}

_UK_MONTHS_GENITIVE = (
    "січня", "лютого", "березня", "квітня", "травня", "червня",
    "липня", "серпня", "вересня", "жовтня", "листопада", "грудня",
)
_EN_MONTHS = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_LINK_RE = re.compile(r"\[([^\]\[]+)\]\(([^()\s]+)\)")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_CODE_RE = re.compile(r"`([^`]+)`")


class NewsContentError(ValueError):
    """Raised when a news YAML file is malformed. Fails the build loudly."""


def _esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _safe_href(url: str) -> str | None:
    """Allow only http(s), site-relative, anchor and mailto targets.

    Everything else — `javascript:`, `data:`, protocol-relative `//evil` — is
    dropped, so a link in YAML can never become script execution.
    """
    candidate = url.strip()
    if not candidate or candidate.startswith("//"):
        return None
    if candidate.startswith(("https://", "http://", "/", "#", "mailto:")):
        return candidate
    return None


def _inline(text: object) -> str:
    """Escape leaf text, then re-introduce a tiny, closed set of inline markup.

    Escaping happens first and is never undone, so the only tags that can reach
    the page are the ones this function emits itself.
    """
    out = _esc(text)

    def _link(match: re.Match[str]) -> str:
        label, raw_url = match.group(1), match.group(2)
        href = _safe_href(html.unescape(raw_url))
        if href is None:
            return label
        external = href.startswith(("https://", "http://"))
        rel = ' target="_blank" rel="noopener noreferrer"' if external else ""
        return f'<a href="{_esc(href)}"{rel}>{label}</a>'

    out = _LINK_RE.sub(_link, out)
    out = _BOLD_RE.sub(r"<strong>\1</strong>", out)
    out = _CODE_RE.sub(r"<code>\1</code>", out)
    return out


def _format_date(value: date, lang: str) -> str:
    if lang == "uk":
        return f"{value.day} {_UK_MONTHS_GENITIVE[value.month - 1]} {value.year}"
    return f"{_EN_MONTHS[value.month - 1]} {value.day}, {value.year}"


def _require_bilingual(raw: dict[str, Any], field: str, source: str) -> dict[str, str]:
    value = raw.get(field)
    if not isinstance(value, dict):
        raise NewsContentError(f"{source}: '{field}' must be a mapping with 'en' and 'uk'")
    missing = [lang for lang in ("en", "uk") if not str(value.get(lang, "")).strip()]
    if missing:
        raise NewsContentError(f"{source}: '{field}' missing {'/'.join(missing)} text")
    return {"en": str(value["en"]).strip(), "uk": str(value["uk"]).strip()}


def _validate_blocks(blocks: object, source: str, lang: str) -> list[dict[str, Any]]:
    if not isinstance(blocks, list) or not blocks:
        raise NewsContentError(f"{source}: body.{lang} must be a non-empty list of blocks")
    checked: list[dict[str, Any]] = []
    for index, block in enumerate(blocks):
        where = f"{source}: body.{lang}[{index}]"
        if not isinstance(block, dict):
            raise NewsContentError(f"{where} must be a mapping")
        kind = str(block.get("type", "")).strip()
        if kind not in BLOCK_TYPES:
            raise NewsContentError(
                f"{where} has unknown type {kind!r}; allowed: {sorted(BLOCK_TYPES)}"
            )
        if kind in {"ul", "ol"}:
            items = block.get("items")
            if not isinstance(items, list) or not items:
                raise NewsContentError(f"{where} ({kind}) needs a non-empty 'items' list")
        elif not str(block.get("text", "")).strip():
            raise NewsContentError(f"{where} ({kind}) needs non-empty 'text'")
        checked.append(block)
    return checked


def load_news_entries(news_dir: Path = DEFAULT_NEWS_DIR) -> list[dict[str, Any]]:
    """Parse and validate every article, newest first.

    Raises NewsContentError on malformed content so a typo fails the build
    rather than silently publishing a half-rendered article.
    """
    if not news_dir.is_dir():
        return []

    entries: list[dict[str, Any]] = []
    seen_slugs: dict[str, str] = {}

    for path in sorted(news_dir.glob("*.yaml")):
        source = path.name
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise NewsContentError(f"{source}: invalid YAML — {exc}") from exc
        if not isinstance(raw, dict):
            raise NewsContentError(f"{source}: top level must be a mapping")

        slug = str(raw.get("slug", "")).strip()
        if not _SLUG_RE.match(slug):
            raise NewsContentError(
                f"{source}: 'slug' must be lowercase kebab-case, got {slug!r}"
            )
        if slug in seen_slugs:
            raise NewsContentError(
                f"{source}: duplicate slug {slug!r} (also in {seen_slugs[slug]})"
            )
        seen_slugs[slug] = source

        published = raw.get("date")
        if not isinstance(published, date):
            raise NewsContentError(f"{source}: 'date' must be an ISO date (YYYY-MM-DD)")

        body_raw = raw.get("body")
        if not isinstance(body_raw, dict):
            raise NewsContentError(f"{source}: 'body' must be a mapping with 'en' and 'uk'")

        tags = raw.get("tags") or []
        if not isinstance(tags, list):
            raise NewsContentError(f"{source}: 'tags' must be a list")

        entries.append({
            "slug": slug,
            "date": published,
            "tags": [str(t).strip() for t in tags if str(t).strip()],
            "author": str(raw.get("author", "OpenOnco")).strip() or "OpenOnco",
            "title": _require_bilingual(raw, "title", source),
            "summary": _require_bilingual(raw, "summary", source),
            "body": {
                lang: _validate_blocks(body_raw.get(lang), source, lang)
                for lang in ("en", "uk")
            },
            "source_file": source,
        })

    entries.sort(key=lambda e: (e["date"], e["slug"]), reverse=True)
    return entries


def _render_blocks(blocks: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for block in blocks:
        kind = block["type"]
        if kind == "p":
            parts.append(f"<p>{_inline(block['text'])}</p>")
        elif kind in {"h2", "h3"}:
            parts.append(f"<{kind}>{_esc(block['text'])}</{kind}>")
        elif kind in {"ul", "ol"}:
            items = "".join(f"<li>{_inline(item)}</li>" for item in block["items"])
            parts.append(f"<{kind}>{items}</{kind}>")
        elif kind == "quote":
            parts.append(f"<blockquote>{_inline(block['text'])}</blockquote>")
        elif kind == "callout":
            tone = CALLOUT_TONES.get(str(block.get("tone", "info")), "")
            parts.append(f'<div class="callout{tone}">{_inline(block["text"])}</div>')
        elif kind == "code":
            parts.append(f"<pre class=\"news-code\"><code>{_esc(block['text'])}</code></pre>")
    return "\n      ".join(parts)


def article_path(slug: str, target_lang: str) -> str:
    prefix = "/ukr" if target_lang == "uk" else ""
    return f"{prefix}/news/{slug}.html"


def index_path(target_lang: str) -> str:
    return "/ukr/news.html" if target_lang == "uk" else "/news.html"


def comments_enabled() -> bool:
    return bool(GISCUS["repo_id"] and GISCUS["category_id"])


def render_comments(entry: dict[str, Any], target_lang: str) -> str:
    """Comment area: house rules, then click-to-load giscus.

    The widget is not embedded on page load. Nothing is requested from
    giscus.app until the reader presses the button, so a passive visit to a
    cancer-information page makes no third-party request at all.
    """
    is_en = target_lang == "en"
    heading = "Comments" if is_en else "Коментарі"
    rules_title = "Before you post" if is_en else "Перед тим, як писати"
    if is_en:
        rules = [
            "**Do not post personal medical data** — diagnosis, test results, dates, "
            "or anything that identifies you or a patient. This page is public and "
            "permanently indexed by search engines.",
            "Comments are readers' opinions. They are **not medical advice** and are "
            "not reviewed by the OpenOnco clinical leads.",
            "Nothing here is monitored for urgent problems. For a clinical emergency, "
            "contact your treating team or emergency services.",
            "For a clinical error in the knowledge base, open a "
            f"[`clinical-error` issue](https://github.com/{GH_REPO}/issues/new) instead — "
            "that path has a triage SLA.",
        ]
        load_label = "Load comments"
        privacy_note = (
            "Comments are hosted on GitHub Discussions via giscus. Pressing the button "
            "loads content from giscus.app and github.com; nothing is sent before that."
        )
        offline_title = "Comments are not switched on yet"
        offline_body = (
            "The embedded comment widget needs GitHub Discussions enabled on the "
            "repository. Until then you can discuss this post directly on GitHub."
        )
        offline_cta = "Open the discussion on GitHub"
    else:
        rules = [
            "**Не публікуйте персональні медичні дані** — діагноз, результати аналізів, "
            "дати чи будь-що, що ідентифікує вас або пацієнта. Ця сторінка публічна й "
            "постійно індексується пошуковими системами.",
            "Коментарі — це думки читачів. Вони **не є медичною порадою** і не проходять "
            "перевірку клінічними лідами OpenOnco.",
            "Тут ніхто не відстежує термінові проблеми. У невідкладній ситуації "
            "звертайтеся до лікуючої команди або екстреної допомоги.",
            "Якщо ви знайшли клінічну помилку в базі знань, натомість відкрийте "
            f"[issue з міткою `clinical-error`](https://github.com/{GH_REPO}/issues/new) — "
            "там діє SLA на розбір.",
        ]
        load_label = "Завантажити коментарі"
        privacy_note = (
            "Коментарі розміщені в GitHub Discussions через giscus. Натискання кнопки "
            "завантажує вміст із giscus.app і github.com; до цього нічого не надсилається."
        )
        offline_title = "Коментарі ще не увімкнено"
        offline_body = (
            "Вбудований віджет коментарів потребує увімкнених GitHub Discussions у "
            "репозиторії. Поки що обговорити цей пост можна напряму на GitHub."
        )
        offline_cta = "Відкрити обговорення на GitHub"

    rules_html = "\n        ".join(f"<li>{_inline(rule)}</li>" for rule in rules)
    rules_block = f"""    <div class="news-comment-rules">
      <h3>{_esc(rules_title)}</h3>
      <ul>
        {rules_html}
      </ul>
    </div>"""

    if not comments_enabled():
        body = f"""    <div class="news-comments-offline">
      <strong>{_esc(offline_title)}</strong>
      <p>{_esc(offline_body)}</p>
      <a class="btn btn-secondary" href="{_esc(DISCUSSIONS_URL)}"
         target="_blank" rel="noopener noreferrer">{_esc(offline_cta)} →</a>
    </div>"""
    else:
        giscus_lang = "uk" if target_lang == "uk" else "en"
        term = f"news/{entry['slug']}"
        body = f"""    <div class="news-comments-mount" id="giscus-mount"
         data-repo="{_esc(GISCUS['repo'])}"
         data-repo-id="{_esc(GISCUS['repo_id'])}"
         data-category="{_esc(GISCUS['category'])}"
         data-category-id="{_esc(GISCUS['category_id'])}"
         data-term="{_esc(term)}"
         data-lang="{giscus_lang}"
         data-host="{_esc(GISCUS['host'])}">
      <button type="button" class="btn btn-secondary news-comments-load"
              id="load-comments">{_esc(load_label)}</button>
      <p class="news-comments-privacy">{_esc(privacy_note)}</p>
    </div>
    <script>
    (function () {{
      var mount = document.getElementById('giscus-mount');
      var button = document.getElementById('load-comments');
      if (!mount || !button) return;
      button.addEventListener('click', function () {{
        button.disabled = true;
        var script = document.createElement('script');
        script.src = mount.dataset.host + '/client.js';
        script.async = true;
        script.crossOrigin = 'anonymous';
        script.setAttribute('data-repo', mount.dataset.repo);
        script.setAttribute('data-repo-id', mount.dataset.repoId);
        script.setAttribute('data-category', mount.dataset.category);
        script.setAttribute('data-category-id', mount.dataset.categoryId);
        script.setAttribute('data-mapping', 'specific');
        script.setAttribute('data-term', mount.dataset.term);
        script.setAttribute('data-reactions-enabled', '1');
        script.setAttribute('data-emit-metadata', '0');
        script.setAttribute('data-input-position', 'top');
        script.setAttribute('data-theme', 'light');
        script.setAttribute('data-lang', mount.dataset.lang);
        script.setAttribute('data-loading', 'lazy');
        mount.appendChild(script);
      }});
    }})();
    </script>"""

    return f"""  <section class="news-comments" id="comments">
    <h2>{_esc(heading)}</h2>
{rules_block}
{body}
  </section>"""


def _page_shell(*, target_lang: str, page_title: str, top_bar_html: str,
                main_html: str, footer: str) -> str:
    """Document skeleton matching render_about in build_site.py.

    The <head> is intentionally minimal: description, canonical, hreflang, OG
    and JSON-LD are injected afterwards by site_head.finalize_site_discovery,
    which scrapes the `OpenOnco · <title>` form emitted here.
    """
    lang_attr = "en" if target_lang == "en" else "uk"
    return f"""<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenOnco · {_esc(page_title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<noscript><link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"></noscript>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link href="/style.css" rel="stylesheet">
</head>
<body>
{top_bar_html}

<main>
{main_html}

  <footer class="page-foot">
    Open-source · MIT-style usage · <a href="https://github.com/{GH_REPO}">{GH_REPO}</a>
    <br>
    {footer}
  </footer>
</main>
</body>
</html>
"""


def render_news_index(entries: list[dict[str, Any]], *, target_lang: str,
                      top_bar_html: str) -> str:
    is_en = target_lang == "en"
    page_title = "News" if is_en else "Новини"
    h1 = "Project news" if is_en else "Новини проєкту"
    if is_en:
        lead = (
            "Release notes, knowledge-base milestones and governance decisions. "
            "Every post is open for comment."
        )
        empty = "No posts yet."
        read_more = "Read"
        footer = "Informational tool for clinicians, not a medical device (CHARTER §15 + §11)."
        count_word = "posts"
    else:
        lead = (
            "Нотатки до релізів, віхи бази знань і рішення governance. "
            "Кожен допис відкритий для коментарів."
        )
        empty = "Дописів поки немає."
        read_more = "Читати"
        footer = "Це інформаційний інструмент для лікаря, не медичний пристрій (CHARTER §15 + §11)."
        count_word = "дописів"

    if entries:
        cards = "\n".join(
            f"""      <a class="case-card news-card" href="{article_path(e['slug'], target_lang)}">
        <div class="case-badge-row">
          <span class="case-badge bdg-plan">{_esc(_format_date(e['date'], target_lang))}</span>
{_render_tags(e['tags'])}
        </div>
        <h3>{_esc(e['title'][target_lang])}</h3>
        <p>{_esc(e['summary'][target_lang])}</p>
        <div class="case-foot">{_esc(read_more)} →</div>
      </a>"""
            for e in entries
        )
        listing = f"""    <div class="case-grid">
{cards}
    </div>"""
    else:
        listing = f'    <div class="case-empty">{_esc(empty)}</div>'

    main_html = f"""  <section class="info-page">
    <p class="home-kicker">OpenOnco</p>
    <h1>{_esc(h1)}</h1>
    <p class="lead">{_esc(lead)}</p>

    <div class="case-list-header">
      <h2>{_esc(page_title)}</h2>
      <span class="case-list-count">{len(entries)} {_esc(count_word)}</span>
    </div>
{listing}
  </section>"""

    return _page_shell(
        target_lang=target_lang,
        page_title=page_title,
        top_bar_html=top_bar_html,
        main_html=main_html,
        footer=footer,
    )


def _render_tags(tags: list[str]) -> str:
    return "\n".join(
        f'          <span class="case-quality quality-starter">{_esc(tag)}</span>'
        for tag in tags
    )


def render_news_article(entry: dict[str, Any], *, target_lang: str,
                        top_bar_html: str) -> str:
    is_en = target_lang == "en"
    title = entry["title"][target_lang]
    if is_en:
        back = "← All news"
        by_line = "by"
        footer = "Informational tool for clinicians, not a medical device (CHARTER §15 + §11)."
    else:
        back = "← Усі новини"
        by_line = "—"
        footer = "Це інформаційний інструмент для лікаря, не медичний пристрій (CHARTER §15 + §11)."

    dateline = _format_date(entry["date"], target_lang)
    tags_html = _render_tags(entry["tags"])
    body_html = _render_blocks(entry["body"][target_lang])

    main_html = f"""  <article class="info-page news-article">
    <a class="case-back-btn news-back" href="{index_path(target_lang)}">{_esc(back)}</a>
    <div class="case-badge-row">
      <span class="case-badge bdg-plan">{_esc(dateline)}</span>
{tags_html}
    </div>
    <h1>{_esc(title)}</h1>
    <p class="lead">{_esc(entry['summary'][target_lang])}</p>
    <p class="news-byline">{_esc(by_line)} {_esc(entry['author'])}</p>

    <div class="news-body info-text">
      {body_html}
    </div>
  </article>

{render_comments(entry, target_lang)}"""

    return _page_shell(
        target_lang=target_lang,
        page_title=title,
        top_bar_html=top_bar_html,
        main_html=main_html,
        footer=footer,
    )


def build_news(
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    *,
    top_bar: Callable[..., str],
    news_dir: Path = DEFAULT_NEWS_DIR,
) -> dict:
    """Write the bilingual news index and article pages.

    `top_bar` is injected rather than imported so this module stays free of a
    circular import with build_site.py.
    """
    entries = load_news_entries(news_dir)

    for rel in ("news", "ukr/news"):
        (output_dir / rel).mkdir(parents=True, exist_ok=True)

    written: list[str] = []
    for target_lang, prefix in (("en", ""), ("uk", "ukr/")):
        index_bar = top_bar(
            active="news",
            target_lang=target_lang,
            lang_switch_href=index_path("uk" if target_lang == "en" else "en"),
        )
        index_rel = f"{prefix}news.html"
        (output_dir / index_rel).write_text(
            render_news_index(entries, target_lang=target_lang, top_bar_html=index_bar),
            encoding="utf-8",
        )
        written.append(index_rel)

        mirror_lang = "uk" if target_lang == "en" else "en"
        for entry in entries:
            article_bar = top_bar(
                active="news",
                target_lang=target_lang,
                lang_switch_href=article_path(entry["slug"], mirror_lang),
            )
            article_rel = f"{prefix}news/{entry['slug']}.html"
            (output_dir / article_rel).write_text(
                render_news_article(entry, target_lang=target_lang, top_bar_html=article_bar),
                encoding="utf-8",
            )
            written.append(article_rel)

    payload = {
        "kind": "openonco_news_index",
        "count": len(entries),
        "comments_enabled": comments_enabled(),
        "posts": [
            {
                "slug": e["slug"],
                "date": e["date"].isoformat(),
                "tags": e["tags"],
                "author": e["author"],
                "title": e["title"],
                "summary": e["summary"],
                "url": {
                    "en": article_path(e["slug"], "en"),
                    "uk": article_path(e["slug"], "uk"),
                },
            }
            for e in entries
        ],
    }
    (output_dir / "news_index.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8",
    )

    return {
        "posts": len(entries),
        "pages_written": len(written),
        "comments_enabled": comments_enabled(),
        "index_json": "news_index.json",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the OpenOnco news section.")
    parser.add_argument("--output", default="docs", help="Output directory (default: docs/)")
    parser.add_argument("--check", action="store_true",
                        help="Validate content only; write nothing.")
    args = parser.parse_args(argv)

    if args.check:
        entries = load_news_entries()
        print(json.dumps({"posts": len(entries),
                          "slugs": [e["slug"] for e in entries]}, indent=2))
        return 0

    from scripts.build_site import _render_top_bar  # noqa: PLC0415

    output_dir = Path(args.output)
    if not output_dir.is_absolute():
        output_dir = REPO_ROOT / output_dir
    print(json.dumps(build_news(output_dir, top_bar=_render_top_bar), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
