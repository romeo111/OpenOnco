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

Comments are open: no account, no login, no mandatory name or email. The EN and
UA versions of a post share one thread, so a discussion is not split by which
translation the reader opened. The backend is configurable (see COMMENTS) —
this layer churns, and pinning one vendor is how the section rots. Setup is in
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

# ── comment backend ─────────────────────────────────────────────────────────
# Readers comment with no account and no login. The provider is swappable on
# purpose: this layer churns, and Cusdis — a leading privacy-first option — was
# archived on 2026-07-17, so hard-wiring one vendor is how the section breaks.
#
# provider: "waline" | "remark42" | "disqus" | "none"
# Fill in `server_url` (plus `site_id` for remark42, `shortname` for disqus) and
# rebuild. While it is blank the section still ships; each post just says
# comments are not switched on yet. See docs/news-comments-setup.md.
COMMENTS = {
    "provider": "waline",
    "server_url": "",
    "site_id": "openonco",
    "shortname": "",
    # Client assets. Point at a self-hosted copy to avoid a third-party CDN.
    "client_base": "https://unpkg.com/@waline/client@v3/dist",
}

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

        event_date = raw.get("date")
        if not isinstance(event_date, date):
            raise NewsContentError(f"{source}: 'date' must be an ISO date (YYYY-MM-DD)")

        # Optional. Set it when a post is written up after the fact: `date` is
        # what the post is about, `published` is when it actually appeared. The
        # page then says so, rather than implying the news section existed all
        # along.
        published = raw.get("published")
        if published is not None and not isinstance(published, date):
            raise NewsContentError(f"{source}: 'published' must be an ISO date (YYYY-MM-DD)")
        if published is not None and published < event_date:
            raise NewsContentError(
                f"{source}: 'published' ({published}) precedes 'date' ({event_date})"
            )

        body_raw = raw.get("body")
        if not isinstance(body_raw, dict):
            raise NewsContentError(f"{source}: 'body' must be a mapping with 'en' and 'uk'")

        tags = raw.get("tags") or []
        if not isinstance(tags, list):
            raise NewsContentError(f"{source}: 'tags' must be a list")

        entries.append({
            "slug": slug,
            "date": event_date,
            "published": published,
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


def thread_id(slug: str) -> str:
    """Comment-thread key for an article.

    Deliberately carries no language prefix: the EN and UA versions of a post
    share one thread, so a discussion is not split by which translation the
    reader happened to open.
    """
    return f"/news/{slug}"


def comments_enabled() -> bool:
    provider = COMMENTS.get("provider", "none")
    if provider == "none":
        return False
    if provider == "disqus":
        return bool(COMMENTS.get("shortname"))
    return bool(COMMENTS.get("server_url"))


# Waline ships no Ukrainian UI (zh/en/jp/ko/pt-BR/ru/fr/vi/es only). Falling
# back to its Russian locale on a Ukrainian site is not acceptable, so the UA
# pages pass their own strings via the `locale` override and keep `en` as the
# base for anything not listed here.
_WALINE_LOCALE_UK = {
    "nick": "Імʼя",
    "nickError": "Імʼя має містити щонайменше 3 символи.",
    "mail": "Email",
    "mailError": "Перевірте адресу email.",
    "link": "Сайт",
    "optional": "Необовʼязково",
    "placeholder": "Напишіть коментар…",
    "sofa": "Коментарів ще немає.",
    "submit": "Надіслати",
    "comment": "Коментарі",
    "refresh": "Оновити",
    "more": "Показати ще",
    "preview": "Перегляд",
    "emoji": "Емодзі",
    "uploadImage": "Завантажити зображення",
    "uploading": "Завантаження…",
    "reply": "Відповісти",
    "cancelReply": "Скасувати",
    "like": "Подобається",
    "cancelLike": "Скасувати",
    "admin": "Адміністрація",
    "sticky": "Закріплено",
    "word": "символів",
    "anonymous": "Анонім",
    "oldest": "Найстаріші",
    "latest": "Найновіші",
    "hottest": "Найпопулярніші",
    "approved": "Схвалено",
    "waiting": "Очікує перевірки",
    "spam": "Спам",
    "seconds": "с тому",
    "minutes": "хв тому",
    "hours": "год тому",
    "days": "дн тому",
    "now": "щойно",
}


def _js_object(value: Any) -> str:
    """JSON for embedding inside a <script> block.

    `</` is neutralised because it would close the enclosing script element
    early wherever it appeared, turning a config typo into broken markup.
    """
    return json.dumps(value, ensure_ascii=False, indent=8).replace("</", "<\\/")


def _waline_embed(entry: dict[str, Any], target_lang: str) -> str:
    base = COMMENTS["client_base"].rstrip("/")
    server = COMMENTS["server_url"].rstrip("/")
    options = {
        "el": "#waline-thread",
        "serverURL": server,
        # Constant, with no /ukr prefix — this is what makes both language
        # versions of a post share one thread.
        "path": thread_id(entry["slug"]),
        "lang": "en",
        # No account, and nothing mandatory: name and email are both optional
        # (requiredMeta stays empty), and a blank name posts as "Anonymous".
        "login": "disable",
        "meta": ["nick", "mail"],
        "requiredMeta": [],
        # Waline's default emoji set is Weibo packs fetched from unpkg — an
        # odd and needless third-party request for this site.
        "emoji": False,
        "search": False,
        "reaction": False,
        "dark": "auto",
    }
    if target_lang == "uk":
        options["locale"] = _WALINE_LOCALE_UK
    return f"""    <link rel="stylesheet" href="{_esc(base)}/waline.css">
    <div id="waline-thread"></div>
    <script type="module">
      import {{ init }} from '{base}/waline.js';
      init({_js_object(options)});
    </script>"""


def _remark42_embed(entry: dict[str, Any], target_lang: str) -> str:
    # Remark42 has no Ukrainian locale either; 'en' rather than its 'ru'.
    config = {
        "host": COMMENTS["server_url"].rstrip("/"),
        "site_id": COMMENTS["site_id"],
        "url": f"https://openonco.info{thread_id(entry['slug'])}",
        "components": ["embed"],
        "locale": "en",
        "theme": "light",
    }
    return f"""    <div id="remark42"></div>
    <script>
      window.remark_config = {_js_object(config)};
      (function (c) {{
        for (var i = 0; i < c.length; i++) {{
          var d = document, s = d.createElement('script');
          s.src = window.remark_config.host + '/web/' + c[i] + '.js';
          s.defer = true;
          d.head.appendChild(s);
        }}
      }})(window.remark_config.components);
    </script>"""


def _disqus_embed(entry: dict[str, Any], target_lang: str) -> str:
    # Last resort only: Disqus' free tier is ad-supported and it runs
    # cross-context behavioural advertising, which sits badly on pages where
    # someone is reading about a cancer diagnosis.
    config = {
        "identifier": thread_id(entry["slug"]),
        "url": f"https://openonco.info{thread_id(entry['slug'])}",
        "src": f"https://{COMMENTS['shortname']}.disqus.com/embed.js",
    }
    return f"""    <div id="disqus_thread"></div>
    <script>
      var openoncoDisqus = {_js_object(config)};
      window.disqus_config = function () {{
        this.page.identifier = openoncoDisqus.identifier;
        this.page.url = openoncoDisqus.url;
      }};
      (function () {{
        var d = document, s = d.createElement('script');
        s.src = openoncoDisqus.src;
        s.setAttribute('data-timestamp', +new Date());
        d.head.appendChild(s);
      }})();
    </script>"""


def render_comments(entry: dict[str, Any], target_lang: str) -> str:
    """Open comment section: anyone can post, no account, no login.

    The EN and UA pages of a post share one thread (see thread_id), so the
    discussion is not split by translation.
    """
    is_en = target_lang == "en"
    heading = "Comments" if is_en else "Коментарі"
    if is_en:
        note = (
            "Threads are public and indexed — please keep personal medical data out "
            "of them. Found a clinical error? "
            f"[Open an issue](https://github.com/{GH_REPO}/issues/new) instead."
        )
        offline = (
            "Comments are not switched on yet — the backend still needs to be "
            "configured."
        )
    else:
        note = (
            "Гілки публічні й індексуються — будь ласка, не пишіть у них персональні "
            "медичні дані. Знайшли клінічну помилку? "
            f"[Відкрийте issue](https://github.com/{GH_REPO}/issues/new)."
        )
        offline = (
            "Коментарі ще не увімкнено — бекенд потрібно налаштувати."
        )

    if not comments_enabled():
        body = f'    <p class="news-comments-offline">{_esc(offline)}</p>'
    else:
        embed = {
            "waline": _waline_embed,
            "remark42": _remark42_embed,
            "disqus": _disqus_embed,
        }[COMMENTS["provider"]]
        body = embed(entry, target_lang)

    return f"""  <section class="news-comments" id="comments">
    <h2>{_esc(heading)}</h2>
    <p class="news-comments-note">{_inline(note)}</p>
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

    # Say so when a post documents something from before the news section
    # existed, instead of quietly implying it was published at the time.
    retro_html = ""
    if entry.get("published"):
        when = _format_date(entry["published"], target_lang)
        retro = (
            f"Written retrospectively and published on {when}."
            if is_en else
            f"Написано ретроспективно, опубліковано {when}."
        )
        retro_html = f'\n    <p class="news-retro">{_esc(retro)}</p>'

    main_html = f"""  <article class="info-page news-article">
    <a class="case-back-btn news-back" href="{index_path(target_lang)}">{_esc(back)}</a>
    <div class="case-badge-row">
      <span class="case-badge bdg-plan">{_esc(dateline)}</span>
{tags_html}
    </div>
    <h1>{_esc(title)}</h1>
    <p class="lead">{_esc(entry['summary'][target_lang])}</p>
    <p class="news-byline">{_esc(by_line)} {_esc(entry['author'])}</p>{retro_html}

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
                "published": e["published"].isoformat() if e["published"] else None,
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
