"""Shared navigation for public pages and the educational handbook."""

from pathlib import Path
from scripts.site_locales import COPY, LOCALES, PUBLIC_PAGES, locale_href, split_locale

_NAV_LABELS = {
    "uk": {"home": "Головна", "about": "Про проєкт", "try_cta": "План лікування",
           "diseases": "Хвороби", "ask": "Туморборд", "kb": "Онко-вікі",
           "prevent": "Профілактика", "news": "Новини"},
    "en": {"home": "Home", "about": "About", "try_cta": "Plan Builder",
           "diseases": "Diseases", "ask": "Tumor Board", "kb": "Onco Wiki",
           "prevent": "Prevention", "news": "News"},
}
_NAV_LABELS.update(COPY)


def _language_flag(locale: str) -> str:
    """Inline vectors render consistently, including on Windows without flag emoji."""
    artwork = {
        "en": '<path fill="#21468b" d="M0 0h24v16H0z"/><path stroke="#fff" stroke-width="4" d="m0 0 24 16M24 0 0 16"/><path stroke="#cf142b" stroke-width="1.5" d="m0 0 24 16M24 0 0 16"/><path stroke="#fff" stroke-width="6" d="M12 0v16M0 8h24"/><path stroke="#cf142b" stroke-width="3" d="M12 0v16M0 8h24"/>',
        "uk": '<path fill="#0057b7" d="M0 0h24v8H0z"/><path fill="#ffd700" d="M0 8h24v8H0z"/>',
        "es": '<path fill="#aa151b" d="M0 0h24v16H0z"/><path fill="#f1bf00" d="M0 4h24v8H0z"/><path fill="#aa151b" d="M6 6h3v4H6z"/>',
        "pt": '<path fill="#ff0000" d="M0 0h24v16H0z"/><path fill="#006600" d="M0 0h9.6v16H0z"/><circle cx="9.6" cy="8" r="3" fill="#ffcc00"/><path fill="#fff" d="M8 6h3.2v3L9.6 10 8 9z"/><path fill="#d71920" d="M8.6 6.6h2v2L9.6 9.3l-1-.7z"/>',
        "de": '<path fill="#000" d="M0 0h24v5.34H0z"/><path fill="#dd0000" d="M0 5.33h24v5.34H0z"/><path fill="#ffce00" d="M0 10.66h24V16H0z"/>',
        "fr": '<path fill="#0055a4" d="M0 0h8v16H0z"/><path fill="#fff" d="M8 0h8v16H8z"/><path fill="#ef4135" d="M16 0h8v16h-8z"/>',
    }
    return f'<svg class="language-flag" viewBox="0 0 24 16" aria-hidden="true" focusable="false">{artwork[locale]}</svg>'


def render_top_bar(active: str = "", target_lang: str = "en",
                    lang_switch_href: str = "/ukr/", page_path: str | None = None) -> str:
    """Render an accessible six-language header; unavailable twins lead home."""
    def cls(name: str) -> str:
        return ' class="active" aria-current="page"' if active == name else ""

    labels = _NAV_LABELS.get(target_lang, _NAV_LABELS["en"])
    home_path = locale_href("index.html", target_lang)
    try_path = locale_href("try.html", target_lang)
    ask_path = locale_href("ask.html", target_lang)
    about_path = locale_href("about.html", target_lang)

    # The Ukrainian project page now folds in the former Capabilities and
    # Limitations material. GitHub, examples and specs stay grouped under
    # About to keep the main nav focused.
    # News is bilingual from day one, so it appears on both navs (unlike
    # Handbook, which is EN-only MVP).
    handbook_label = "Посібник" if target_lang == "uk" else labels.get("handbook", "Handbook")
    extra_links = (
        (f'<a href="/capabilities.html"{cls("capabilities")}>Capabilities</a>' if target_lang == "en" else "")
        + f'<a href="{locale_href("handbook.html", target_lang)}"{cls("handbook")}>{handbook_label}</a>'
        + f'<a href="{locale_href("news.html", target_lang)}"{cls("news")}>{labels["news"]}</a>'
    )

    is_uk = target_lang == "uk"

    kb_href = locale_href("kb.html", target_lang)
    kb_current = ' aria-current="page"' if active in {"kb", "diseases"} else ""
    ask_current = ' aria-current="page"' if active == "ask" else ""
    try_current = ' aria-current="page"' if active == "try" else ""
    prevent_href = locale_href("prevent.html", target_lang)
    prevent_current = ' aria-current="page"' if active == "prevent" else ""

    reading_links = f"""
    <a href="{home_path}"{cls("home")}>{labels['home']}</a>
    {extra_links}
    <a href="{about_path}"{cls("about")}>{labels['about']}</a>
    """
    icons = {
        "kb": '<path d="M4 5.5A3 3 0 0 1 7 4h5v15H7a3 3 0 0 0-3 1.5zM20 5.5A3 3 0 0 0 17 4h-5v15h5a3 3 0 0 1 3 1.5z"/>',
        "ask": '<path d="M20 11a7 7 0 0 1-7 7H6l-3 3V11a7 7 0 0 1 7-7h3a7 7 0 0 1 7 7Z"/><path d="M8 11h8M8 8h5"/>',
        "prevent": '<path d="M12 3 4 6v6c0 5 8 9 8 9s8-4 8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    }

    def icon(name: str) -> str:
        return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{icons[name]}</svg>'

    tools = f"""
      <a href="{kb_href}" class="btn-cta-top btn-cta-secondary"{kb_current}>{icon('kb')}<span>{labels['kb']}</span></a>
      <a href="{ask_path}" class="btn-cta-top btn-cta-secondary"{ask_current}>{icon('ask')}<span>{labels['ask']}</span></a>
      <a href="{prevent_href}" class="btn-cta-top btn-cta-secondary"{prevent_current}>{icon('prevent')}<span>{labels['prevent']}</span></a>
    """
    menu_label = "Меню" if is_uk else "Menu"
    tools_label = "Інструменти" if is_uk else "Workspace"
    brand_caption = "ВІДКРИТА ОНКОЛОГІЯ" if is_uk else "OPEN ONCOLOGY"
    open_label = "Відкритий код" if is_uk else "Open source"
    language_label = "Мова" if is_uk else "Language"
    if target_lang in COPY:
        menu_label, tools_label, brand_caption, open_label, language_label = (
            labels[k] for k in ("menu", "tools", "brand", "open", "language")
        )
    # Existing renderers supply a twin URL. It also identifies the current
    # page without fragile inference from its active navigation category.
    _, page = split_locale(page_path or lang_switch_href)
    if page == "capabilities.html":
        page = "about.html"
    language_items = []
    for code, (_, native_name, abbreviation) in LOCALES.items():
        available = page in PUBLIC_PAGES or code in {"en", "uk"} and (
            page.startswith("kb/") or page.startswith("cases/") or page.startswith("handbook/") or page.startswith("news/")
        )
        href = locale_href(page if available else "index.html", code)
        current = ' aria-current="true"' if code == target_lang else ""
        language_items.append(f'<a href="{href}" lang="{code}" hreflang="{code}"{current}>{_language_flag(code)}<span>{native_name}</span><small>{abbreviation}</small></a>')
    language_menu = f'''<details class="language-menu lang-switch">
      <summary aria-label="{language_label}">{_language_flag(target_lang)}{LOCALES[target_lang][2]} <span aria-hidden="true">⌄</span></summary>
      <nav aria-label="{language_label}">{"".join(language_items)}</nav>
    </details>'''

    return f"""<header class="top-bar site-header">
  <link rel="stylesheet" href="/header.css?v=flags-20261010">
  <div class="header-shell">
  <div class="header-main">
    <div class="brand-line">
      <a href="{home_path}" class="brand-mini" aria-label="OpenOnco">
        <img class="header-mark" src="/logo.svg" width="44" height="44" alt="">
        <span class="brand-copy"><span class="brand-wordmark">Open<span>Onco</span></span><span class="brand-caption">{brand_caption}</span></span>
      </a>
    </div>
    <nav class="top-nav">{reading_links}</nav>
    <div class="top-right">
    {language_menu}
    <a href="{try_path}" class="btn-cta-top btn-cta-try"{try_current}><span>{labels['try_cta']}</span><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5 12h14m-5-5 5 5-5 5"/></svg></a>
    <details class="mobile-menu">
      <summary aria-label="{menu_label}"><span class="menu-lines" aria-hidden="true"></span></summary>
      <div class="mobile-menu-panel">
        <nav aria-label="{menu_label}">{reading_links}</nav>
        <div class="mobile-tools">{tools}</div>
      </div>
    </details>
    </div>
  </div>
  <div class="header-tools">
    <span class="header-tools-label">{tools_label}</span>
    <div class="top-cta-group">{tools}</div>
    <span class="header-open-label"><span aria-hidden="true"></span>{open_label}</span>
  </div>
  </div>
</header>"""


def write_header_assets(output_dir: Path) -> None:
    """Keep standalone and full-site builds on the same header stylesheet."""
    (output_dir / "header.css").write_text(
        Path(__file__).with_name("site_header.css").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
