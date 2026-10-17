"""Build the OpenOnco news section with open comments.

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

from scripts.news_archive_copy import LANGUAGES as NEWS_LOCALES, article_translation
from scripts.site_locales import LOCALES, locale_path, split_locale

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

# "project" = what changed in OpenOnco. "explainer" = background on cancer
# biology or how the clinical literature works. The distinction is not
# cosmetic: an explainer asserts things about the world rather than about our
# own commits, so it must carry citations and says on the page that it is not
# clinical advice.
POST_KINDS = {"project", "explainer"}
AUTOMATED_SERIES = "openonco-three-day"
SERIES_FORMATS = {"research", "platform"}
STARTUP_SERIES = "openonco-startups-daily"

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

# Complete article-page chrome for languages with a full translation.
# Source titles in the bibliography remain in their original publication language.
ARTICLE_UI = {
    "es": ("← Todas las noticias", "por", "Fuentes", "Escrito retrospectivamente; publicado el {date}.", "Material informativo, no consejo médico. Consulte las fuentes y hable con su equipo clínico.", "Comentarios", "Los comentarios son públicos. No incluya datos personales de pacientes. ¿Detectó un error clínico? [Abra una incidencia](https://github.com/romeo111/OpenOnco/issues/new).", "Los comentarios aún no están activados."),
    "pt": ("← Todas as notícias", "por", "Fontes", "Escrito retrospetivamente; publicado em {date}.", "Material informativo, não aconselhamento médico. Consulte as fontes e fale com a sua equipa clínica.", "Comentários", "Os comentários são públicos. Não inclua dados pessoais de pacientes. Encontrou um erro clínico? [Abra uma ocorrência](https://github.com/romeo111/OpenOnco/issues/new).", "Os comentários ainda não estão ativos."),
    "de": ("← Alle Neuigkeiten", "von", "Quellen", "Rückblickend verfasst; veröffentlicht am {date}.", "Hintergrundinformation, keine medizinische Beratung. Prüfen Sie die Quellen und sprechen Sie mit Ihrem Behandlungsteam.", "Kommentare", "Kommentare sind öffentlich. Bitte keine persönlichen Patientendaten eingeben. Klinischen Fehler entdeckt? [Issue eröffnen](https://github.com/romeo111/OpenOnco/issues/new).", "Kommentare sind noch nicht aktiviert."),
    "fr": ("← Toutes les actualités", "par", "Sources", "Rédigé rétrospectivement ; publié le {date}.", "Information générale, pas un avis médical. Vérifiez les sources et parlez-en à votre équipe soignante.", "Commentaires", "Les commentaires sont publics. N’y publiez aucune donnée personnelle de patient. Une erreur clinique ? [Ouvrez un ticket](https://github.com/romeo111/OpenOnco/issues/new).", "Les commentaires ne sont pas encore activés."),
    "it": ("← Tutte le notizie", "di", "Fonti", "Scritto retrospettivamente; pubblicato il {date}.", "Informazioni generali, non consulenza medica. Verifica le fonti e parlane con il team curante.", "Commenti", "I commenti sono pubblici. Non inserire dati personali dei pazienti. Hai trovato un errore clinico? [Apri una segnalazione](https://github.com/romeo111/OpenOnco/issues/new).", "I commenti non sono ancora attivi."),
    "da": ("← Alle nyheder", "af", "Kilder", "Skrevet efterfølgende; udgivet {date}.", "Baggrundsinformation, ikke lægelig rådgivning. Kontrollér kilderne, og tal med dit behandlingsteam.", "Kommentarer", "Kommentarer er offentlige. Del ikke personlige patientoplysninger. Fundet en klinisk fejl? [Opret en sag](https://github.com/romeo111/OpenOnco/issues/new).", "Kommentarer er endnu ikke slået til."),
    "sv": ("← Alla nyheter", "av", "Källor", "Skriven i efterhand; publicerad {date}.", "Bakgrundsinformation, inte medicinsk rådgivning. Kontrollera källorna och tala med ditt vårdteam.", "Kommentarer", "Kommentarer är offentliga. Ange inga personliga patientuppgifter. Hittat ett kliniskt fel? [Skapa ett ärende](https://github.com/romeo111/OpenOnco/issues/new).", "Kommentarer är ännu inte aktiverade."),
    "nb": ("← Alle nyheter", "av", "Kilder", "Skrevet i ettertid; publisert {date}.", "Bakgrunnsinformasjon, ikke medisinske råd. Sjekk kildene og snakk med behandlingsteamet ditt.", "Kommentarer", "Kommentarer er offentlige. Ikke legg inn personlige pasientopplysninger. Funnet en klinisk feil? [Opprett en sak](https://github.com/romeo111/OpenOnco/issues/new).", "Kommentarer er ennå ikke aktivert."),
    "fi": ("← Kaikki uutiset", "kirjoittaja", "Lähteet", "Kirjoitettu jälkikäteen; julkaistu {date}.", "Taustatietoa, ei lääketieteellisiä neuvoja. Tarkista lähteet ja keskustele hoitotiimisi kanssa.", "Kommentit", "Kommentit ovat julkisia. Älä kirjoita potilaiden henkilötietoja. Löysitkö kliinisen virheen? [Avaa ilmoitus](https://github.com/romeo111/OpenOnco/issues/new).", "Kommentointi ei ole vielä käytössä."),
}

INDEX_LANGUAGE_NOTE = {
    "es": "Las tarjetas traducidas abren el artículo completo en español; las demás abren el original en inglés.",
    "pt": "Os cartões traduzidos abrem o artigo completo em português; os restantes abrem o original em inglês.",
    "de": "Übersetzte Karten öffnen den vollständigen deutschen Artikel; die übrigen führen zum englischen Original.",
    "fr": "Les cartes traduites ouvrent l’article complet en français ; les autres mènent à l’original anglais.",
    "it": "Le schede tradotte aprono l’articolo completo in italiano; le altre aprono l’originale inglese.",
    "da": "Oversatte kort åbner hele artiklen på dansk; de øvrige åbner den engelske original.",
    "sv": "Översatta kort öppnar hela artikeln på svenska; övriga öppnar det engelska originalet.",
    "nb": "Oversatte kort åpner hele artikkelen på norsk; de øvrige åpner den engelske originalen.",
    "fi": "Käännetyt kortit avaavat koko artikkelin suomeksi; muut avaavat englanninkielisen alkuperäisen.",
}

DOCTOR_NOTE = {
    "en": "This article does not replace a doctor.",
    "uk": "Цей матеріал не замінює консультації лікаря.",
    "es": "Este artículo no sustituye la consulta con un médico.",
    "pt": "Este artigo não substitui a consulta com um médico.",
    "de": "Dieser Artikel ersetzt keine ärztliche Beratung.",
    "fr": "Cet article ne remplace pas une consultation médicale.",
    "it": "Questo articolo non sostituisce il parere di un medico.",
    "da": "Denne artikel erstatter ikke lægelig rådgivning.",
    "sv": "Den här artikeln ersätter inte en läkares bedömning.",
    "nb": "Denne artikkelen erstatter ikke en leges vurdering.",
    "fi": "Tämä artikkeli ei korvaa lääkärin arviota.",
}

STARTUP_NOTE = {
    "en": "A company announcement is not independent evidence of clinical benefit. This comparison is informational, not medical advice.",
    "uk": "Повідомлення компанії не є незалежним доказом клінічної користі. Це інформаційне порівняння, а не медична порада.",
    "es": "Un comunicado empresarial no demuestra de forma independiente un beneficio clínico. Esta comparación es informativa, no un consejo médico.",
    "pt": "Um comunicado da empresa não demonstra de forma independente benefício clínico. Esta comparação é informativa, não aconselhamento médico.",
    "de": "Eine Unternehmensmitteilung ist kein unabhängiger Beleg für klinischen Nutzen. Dieser Vergleich informiert und ist keine medizinische Beratung.",
    "fr": "Un communiqué d’entreprise ne prouve pas indépendamment un bénéfice clinique. Cette comparaison informe et ne constitue pas un avis médical.",
    "it": "Un comunicato aziendale non dimostra in modo indipendente un beneficio clinico. Questo confronto è informativo, non è un consiglio medico.",
    "da": "En virksomhedsmeddelelse er ikke uafhængig dokumentation for klinisk nytte. Denne sammenligning er information, ikke lægelig rådgivning.",
    "sv": "Ett företagsmeddelande är inte oberoende belägg för klinisk nytta. Jämförelsen är information, inte medicinsk rådgivning.",
    "nb": "En selskapsmelding er ikke uavhengig dokumentasjon på klinisk nytte. Denne sammenligningen er informasjon, ikke medisinske råd.",
    "fi": "Yhtiön tiedote ei ole riippumaton näyttö kliinisestä hyödystä. Tämä vertailu on tietoa, ei lääketieteellinen neuvo.",
}


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
    if lang in NEWS_LOCALES:
        return value.isoformat()
    return f"{_EN_MONTHS[value.month - 1]} {value.day}, {value.year}"


def _require_bilingual(raw: dict[str, Any], field: str, source: str) -> dict[str, str]:
    value = raw.get(field)
    if not isinstance(value, dict):
        raise NewsContentError(f"{source}: '{field}' must be a mapping with 'en' and 'uk'")
    missing = [lang for lang in ("en", "uk") if not str(value.get(lang, "")).strip()]
    if missing:
        raise NewsContentError(f"{source}: '{field}' missing {'/'.join(missing)} text")
    return {"en": str(value["en"]).strip(), "uk": str(value["uk"]).strip()}


def _validate_sources(raw: object, source: str, kind: str) -> list[dict[str, str]]:
    """Reference list for a post.

    Optional for project news, which reports on our own commits. **Required**
    for `explainer` posts: those make factual claims about cancer biology and
    the clinical literature, and CLINICAL_CONTENT_STANDARDS requires a citation
    behind every such claim. Enforcing it here means the build fails rather
    than an uncited claim reaching a public medical page.
    """
    if raw is None:
        raw = []
    if not isinstance(raw, list):
        raise NewsContentError(f"{source}: 'sources' must be a list")

    checked: list[dict[str, str]] = []
    for index, item in enumerate(raw):
        where = f"{source}: sources[{index}]"
        if not isinstance(item, dict):
            raise NewsContentError(f"{where} must be a mapping with 'citation' and 'id'")
        citation = str(item.get("citation", "")).strip()
        identifier = str(item.get("id", "")).strip()
        if not citation:
            raise NewsContentError(f"{where} needs a 'citation'")
        if not identifier:
            raise NewsContentError(f"{where} needs an 'id' (PMID, DOI or URL)")
        checked.append({"citation": citation, "id": identifier})

    if kind == "explainer" and not checked:
        raise NewsContentError(
            f"{source}: an 'explainer' post makes clinical claims and must cite "
            f"at least one source (CLINICAL_CONTENT_STANDARDS)"
        )
    return checked


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

        kind = str(raw.get("kind", "project")).strip()
        if kind not in POST_KINDS:
            raise NewsContentError(
                f"{source}: 'kind' must be one of {sorted(POST_KINDS)}, got {kind!r}"
            )
        series = raw.get("series")
        series_format = raw.get("series_format")
        if series is not None or series_format is not None:
            valid_series = (
                series == AUTOMATED_SERIES and series_format in SERIES_FORMATS
            ) or (
                series == STARTUP_SERIES and series_format == "startup"
                and published is not None and kind == "explainer"
            )
            if not valid_series:
                raise NewsContentError(f"{source}: invalid automated series or series_format")

        sources = _validate_sources(raw.get("sources"), source, kind)

        translations = raw.get("translations") or {}
        if not isinstance(translations, dict) or set(translations) - set(NEWS_LOCALES):
            raise NewsContentError(f"{source}: translations must map supported non-EN/UK locales")

        entry = {
            "slug": slug,
            "date": event_date,
            "published": published,
            "kind": kind,
            "series": series,
            "series_format": series_format,
            "sources": sources,
            "tags": [str(t).strip() for t in tags if str(t).strip()],
            "author": str(raw.get("author", "OpenOnco")).strip() or "OpenOnco",
            "title": _require_bilingual(raw, "title", source),
            "summary": _require_bilingual(raw, "summary", source),
            "body": {
                lang: _validate_blocks(body_raw.get(lang), source, lang)
                for lang in ("en", "uk")
            },
            "source_file": source,
        }
        for locale, translated in translations.items():
            if not isinstance(translated, dict):
                raise NewsContentError(f"{source}: translations.{locale} must be a mapping")
            for field in ("title", "summary"):
                value = translated.get(field)
                if not isinstance(value, str) or not value.strip():
                    raise NewsContentError(f"{source}: translations.{locale}.{field} is required")
                entry[field][locale] = value.strip()
            entry["body"][locale] = _validate_blocks(translated.get("body"), source, locale)
        if "archive" in entry["tags"]:
            for locale in NEWS_LOCALES:
                if locale in entry["body"]:
                    raise NewsContentError(f"{source}: archive translation is already curated")
                try:
                    translated = article_translation(entry, locale)
                except (KeyError, ValueError) as exc:
                    raise NewsContentError(f"{source}: incomplete {locale} archive translation: {exc}") from exc
                for field in ("title", "summary", "body"):
                    entry[field][locale] = translated[field]
        entries.append(entry)

    entries.sort(key=lambda e: (e["date"], e["slug"]), reverse=True)
    sequence = sorted(
        (e for e in entries if e["series"] == AUTOMATED_SERIES),
        key=lambda e: (e["published"] or e["date"], e["slug"]),
    )
    for earlier, later in zip(sequence, sequence[1:]):
        if earlier["series_format"] == later["series_format"]:
            raise NewsContentError(
                f"{later['source_file']}: automated series must alternate after {earlier['source_file']}"
            )
    startup_dates: set[date] = set()
    for entry in entries:
        if entry["series"] != STARTUP_SERIES:
            continue
        if entry["published"] in startup_dates:
            raise NewsContentError(
                f"{entry['source_file']}: only one startup issue may be published per day"
            )
        startup_dates.add(entry["published"])
    return entries


def _source_href(identifier: str) -> str | None:
    """Turn a PMID / DOI / URL into a link target."""
    value = identifier.strip()
    low = value.lower()
    if low.startswith(("http://", "https://")):
        return value
    if low.startswith("pmid:"):
        return f"https://pubmed.ncbi.nlm.nih.gov/{value.split(':', 1)[1].strip()}/"
    if low.startswith("doi:"):
        return f"https://doi.org/{value.split(':', 1)[1].strip()}"
    if low.startswith("10."):
        return f"https://doi.org/{value}"
    if value.isdigit():
        return f"https://pubmed.ncbi.nlm.nih.gov/{value}/"
    return None


def _render_sources(entry: dict[str, Any], target_lang: str) -> str:
    if not entry.get("sources"):
        return ""
    is_en = target_lang == "en"
    heading = "Sources" if is_en else "Джерела" if target_lang == "uk" else ARTICLE_UI[target_lang][2]
    items = []
    for src in entry["sources"]:
        href = _source_href(src["id"])
        label = _esc(src["id"])
        link = (
            f'<a href="{_esc(href)}" target="_blank" rel="noopener noreferrer">{label}</a>'
            if href else label
        )
        items.append(f"      <li>{_esc(src['citation'])} · {link}</li>")
    return f"""  <section class="news-sources">
    <h2>{_esc(heading)}</h2>
    <ol>
{chr(10).join(items)}
    </ol>
  </section>"""


def _render_explainer_note(target_lang: str, series: str | None = None) -> str:
    """Shown on explainer posts only.

    A reader who arrives from search at a page about tumour biology should not
    have to infer that it is background reading rather than guidance for their
    own case.
    """
    if series == STARTUP_SERIES:
        text = STARTUP_NOTE[target_lang]
    elif target_lang == "en":
        text = (
            "Background reading, not clinical guidance. This describes published "
            "research; it is not a recommendation for any individual case, and the "
            "cited studies may have been superseded."
        )
    elif target_lang == "uk":
        text = (
            "Матеріал для загального розуміння, а не клінічна настанова. Тут описані "
            "опубліковані дослідження; це не рекомендація для конкретного випадку, а "
            "згадані праці могли бути переглянуті пізнішими даними."
        )
    else:
        text = ARTICLE_UI[target_lang][4]
    return f'    <p class="news-kind-note">{_esc(text + " " + DOCTOR_NOTE[target_lang])}</p>'


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
    return "/" + locale_path(f"news/{slug}.html", target_lang)


def index_path(target_lang: str) -> str:
    return "/" + locale_path("news.html", target_lang)


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
    heading = "Comments" if is_en else "Коментарі" if target_lang == "uk" else ARTICLE_UI[target_lang][5]
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
    elif target_lang == "uk":
        note = (
            "Гілки публічні й індексуються — будь ласка, не пишіть у них персональні "
            "медичні дані. Знайшли клінічну помилку? "
            f"[Відкрийте issue](https://github.com/{GH_REPO}/issues/new)."
        )
        offline = (
            "Коментарі ще не увімкнено — бекенд потрібно налаштувати."
        )
    else:
        note, offline = ARTICLE_UI[target_lang][6:8]

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
    lang_attr = target_lang
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
    h1 = "What changed. What it means." if is_en else "Що змінилося. Що це означає."
    kicker = "OpenOnco / News" if is_en else "OpenOnco / Новини"
    if is_en:
        lead = (
            "Fresh project updates and source-cited explainers, written for "
            "people who want to see the evidence and the limits."
        )
        empty = "No posts yet."
        read_more = "Read the story"
        footer = "Informational tool for clinicians, requiring qualified clinician review (CHARTER §11 + §15)."
        count_word = "posts"
        latest_label = "Just shipped"
        explain_label = "Worth understanding"
        explain_note = "Source-cited background, not treatment advice."
        archive_label = "Browse the archive"
        archive_note = "Earlier releases and explainers, newest first"
        project_label = "Project update"
        kind_label = "Explainer"
        language_note = "Every post has English and Ukrainian text; selected posts have nine more full translations."
        retro_label = "Retrospective"
    else:
        lead = (
            "Свіжі зміни проєкту й пояснення з джерелами — для тих, "
            "хто хоче бачити докази та межі їх застосування."
        )
        empty = "Дописів поки немає."
        read_more = "Читати матеріал"
        footer = "Це інформаційний інструмент для лікаря, що потребує перегляду кваліфікованим лікарем (CHARTER §11 + §15)."
        count_word = "дописів"
        latest_label = "Щойно на сайті"
        explain_label = "Варто розібратися"
        explain_note = "Пояснення з джерелами, а не порада щодо лікування."
        archive_label = "Архів матеріалів"
        archive_note = "Попередні зміни й пояснення, від нових до давніх"
        project_label = "Оновлення проєкту"
        kind_label = "Пояснення"
        language_note = "Кожен допис має повний текст англійською й українською; для частини є ще дев’ять перекладів."
        retro_label = "Ретроспектива"

    def card(entry: dict[str, Any], *, featured: bool = False) -> str:
        kind = (
            "Startup watch" if is_en else "Огляд стартапів"
        ) if entry["series"] == STARTUP_SERIES else (
            kind_label if entry["kind"] == "explainer" else project_label
        )
        classes = "case-card news-card news-feature" if featured else "case-card news-card"
        retro_badge = (
            f'\n          <span>{_esc(retro_label)}</span>'
            if entry.get("published") and entry["published"] > entry["date"] else ""
        )
        return f"""      <a class="{classes}" href="{article_path(entry['slug'], target_lang)}">
        <div class="news-card-meta">
          <span>{_esc(kind)}</span>
          <time datetime="{entry['date'].isoformat()}">{_esc(_format_date(entry['date'], target_lang))}</time>{retro_badge}
        </div>
        <h3>{_esc(entry['title'][target_lang])}</h3>
        <p>{_esc(entry['summary'][target_lang])}</p>
        <span class="news-card-link">{_esc(read_more)} <span aria-hidden="true">↗</span></span>
      </a>"""

    if entries:
        # Backfilled release notes belong in the archive, even when their
        # event date matches a current story. Do not let a batch of historical
        # notes displace the editorial front page.
        fresh = [e for e in entries if "archive" not in e["tags"]] or entries
        fresh = sorted(
            fresh,
            key=lambda e: (e["published"] or e["date"], e["date"], e["slug"]),
            reverse=True,
        )
        feature = card(fresh[0], featured=True)
        recent = fresh[1:3]
        explainers = [e for e in fresh[1:] if e["kind"] == "explainer"][:3]
        visible_slugs = {e["slug"] for e in [fresh[0], *recent, *explainers]}
        archive = [e for e in entries if e["slug"] not in visible_slugs]
        recent_html = f"""    <section class="news-group" aria-labelledby="news-latest">
      <div class="news-group-head"><h2 id="news-latest">{_esc(latest_label)}</h2></div>
      <div class="news-grid">{''.join(card(e) for e in recent)}</div>
    </section>""" if recent else ""
        explain_html = f"""    <section class="news-group" aria-labelledby="news-explainers">
      <div class="news-group-head"><h2 id="news-explainers">{_esc(explain_label)}</h2>
        <p>{_esc(explain_note)}</p></div>
      <div class="news-grid">{''.join(card(e) for e in explainers)}</div>
    </section>""" if explainers else ""
        archive_html = f"""    <details class="news-archive">
      <summary>{_esc(archive_label)} <span>{len(archive)}</span></summary>
      <p>{_esc(archive_note)}</p>
      <div class="news-archive-list">{''.join(card(e) for e in archive)}</div>
    </details>""" if archive else ""
        listing = f"""{feature}
{recent_html}
{explain_html}
{archive_html}"""
    else:
        listing = f'    <div class="case-empty">{_esc(empty)}</div>'

    main_html = f"""  <section class="info-page news-index">
    <p class="home-kicker">{_esc(kicker)}</p>
    <h1>{_esc(h1)}</h1>
    <p class="lead">{_esc(lead)}</p>
    <p class="news-count"><span>{len(entries)}</span> <span>{_esc(count_word)}</span> · <span>{_esc(language_note)}</span></p>
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
        footer = "Informational tool for clinicians, requiring qualified clinician review (CHARTER §11 + §15)."
    elif target_lang == "uk":
        back = "← Усі новини"
        by_line = "—"
        footer = "Це інформаційний інструмент для лікаря, що потребує перегляду кваліфікованим лікарем (CHARTER §11 + §15)."
    else:
        back, by_line = ARTICLE_UI[target_lang][:2]
        footer = ARTICLE_UI[target_lang][4]

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
            if target_lang == "uk" else
            ARTICLE_UI[target_lang][3].format(date=when)
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
{_render_explainer_note(target_lang, entry['series']) if entry['kind'] == 'explainer' else ''}
    <div class="news-body info-text">
      {body_html}
    </div>
  </article>

{_render_sources(entry, target_lang)}
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
    """Write the EN/UK indexes and every available full article translation.

    `top_bar` is injected rather than imported so this module stays free of a
    circular import with build_site.py.
    """
    entries = load_news_entries(news_dir)
    article_paths = {
        locale_path(f"news/{entry['slug']}.html", locale)
        for entry in entries for locale in LOCALES if locale in entry["body"]
    }

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
                page_path=f"news/{entry['slug']}.html",
                available_paths=article_paths,
            )
            article_rel = f"{prefix}news/{entry['slug']}.html"
            (output_dir / article_rel).write_text(
                render_news_article(entry, target_lang=target_lang, top_bar_html=article_bar),
                encoding="utf-8",
            )
            written.append(article_rel)

    for locale in NEWS_LOCALES:
        for entry in entries:
            if locale not in entry["body"]:
                continue
            rel = locale_path(f"news/{entry['slug']}.html", locale)
            target = output_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            article_bar = top_bar(
                active="news",
                target_lang=locale,
                lang_switch_href=article_path(entry["slug"], "en"),
                page_path=f"news/{entry['slug']}.html",
                available_paths=article_paths,
            )
            target.write_text(
                render_news_article(entry, target_lang=locale, top_bar_html=article_bar),
                encoding="utf-8",
            )
            written.append(rel)

    payload = {
        "kind": "openonco_news_index",
        "count": len(entries),
        "comments_enabled": comments_enabled(),
        "posts": [
            {
                "slug": e["slug"],
                "date": e["date"].isoformat(),
                "published": e["published"].isoformat() if e["published"] else None,
                "kind": e["kind"],
                "series": e["series"],
                "series_format": e["series_format"],
                "sources": e["sources"],
                "tags": e["tags"],
                "author": e["author"],
                "title": e["title"],
                "summary": e["summary"],
                "url": {
                    locale: article_path(e["slug"], locale)
                    for locale in LOCALES if locale in e["body"]
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


def connect_localized_news_indexes(output_dir: Path, *, news_dir: Path = DEFAULT_NEWS_DIR) -> int:
    """Point translated index cards at complete local articles when they exist.

    Public-page localization creates the nine indexes after build_news. An
    untranslated article keeps its English destination and an explicit language
    marker; no article is invented from a translated teaser.
    """
    entries = load_news_entries(news_dir)
    translated = {
        locale: {entry["slug"] for entry in entries if locale in entry["body"]}
        for locale in NEWS_LOCALES
    }
    changed = 0
    for locale in NEWS_LOCALES:
        path = output_dir / locale / "news.html"
        if not path.exists():
            continue
        source = path.read_text(encoding="utf-8")

        def replace_link(match: re.Match[str]) -> str:
            slug = match.group(1)
            if slug in translated[locale]:
                return f'href="{article_path(slug, locale)}"'
            return match.group(0) + ' lang="en" hreflang="en"'

        result = re.sub(r'href="/news/([a-z0-9-]+)\.html"', replace_link, source)
        result, note_count = re.subn(
            r'(<p class="news-count">.*? · <span>).*?(</span></p>)',
            lambda match: match.group(1) + _esc(INDEX_LANGUAGE_NOTE[locale]) + match.group(2),
            result,
            count=1,
            flags=re.S,
        )
        if note_count != 1:
            raise NewsContentError(f"{path}: expected one language-availability note")
        path.write_text(result, encoding="utf-8")
        changed += 1
    return changed


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
