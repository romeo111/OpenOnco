"""Shared navigation for public pages and the educational handbook."""

from pathlib import Path

_NAV_LABELS = {
    "uk": {"home": "Головна", "about": "Про проєкт", "try_cta": "План лікування",
           "diseases": "Хвороби", "ask": "Туморборд", "kb": "Онко-вікі",
           "prevent": "Профілактика", "news": "Новини"},
    "en": {"home": "Home", "about": "About", "try_cta": "Plan Builder",
           "diseases": "Diseases", "ask": "Tumor Board", "kb": "Onco Wiki",
           "prevent": "Prevention", "news": "News"},
}


def render_top_bar(active: str = "", target_lang: str = "en",
                    lang_switch_href: str = "/ukr/") -> str:
    """Render the bilingual header with a primary action and native mobile menu."""
    def cls(name: str) -> str:
        return ' class="active" aria-current="page"' if active == name else ""

    labels = _NAV_LABELS.get(target_lang, _NAV_LABELS["en"])
    home_path = "/ukr/" if target_lang == "uk" else "/"
    try_path = "/ukr/try.html" if target_lang == "uk" else "/try.html"
    ask_path = "/ukr/ask.html" if target_lang == "uk" else "/ask.html"
    about_path = "/ukr/about.html" if target_lang == "uk" else "/about.html"

    # The Ukrainian project page now folds in the former Capabilities and
    # Limitations material. GitHub, examples and specs stay grouped under
    # About to keep the main nav focused.
    # News is bilingual from day one, so it appears on both navs (unlike
    # Handbook, which is EN-only MVP).
    extra_links = ""
    if target_lang == "uk":
        extra_links = (
            f'<a href="/ukr/news.html"{cls("news")}>{labels["news"]}</a>'
        )
    else:  # target_lang == "en"
        # Handbook is EN-only MVP — only surfaced on EN nav. When UA chapters
        # land, mirror this into the UA branch and add the page kind to
        # _lang_switch_href.
        extra_links = (
            f'<a href="/capabilities.html"{cls("capabilities")}>Capabilities</a>'
            f'<a href="/handbook.html"{cls("handbook")}>Handbook</a>'
            f'<a href="/news.html"{cls("news")}>{labels["news"]}</a>'
        )

    # Stable visual order is always [UA · EN] regardless of which language
    # is current — clicking the toggle must NOT swap pill positions, only
    # which one is highlighted (CSS .lang-current vs .lang-other).
    is_uk = target_lang == "uk"
    ua_cls = "lang-current" if is_uk else "lang-other"
    en_cls = "lang-other" if is_uk else "lang-current"
    # Tags: <span> for the current pill (no link), <a> for the other.
    ua_tag, ua_attr = ("span", "") if is_uk else ("a", f' href="{lang_switch_href}"')
    en_tag, en_attr = ("a", f' href="{lang_switch_href}"') if is_uk else ("span", "")

    kb_href = "/ukr/kb.html" if target_lang == "uk" else "/kb.html"
    kb_current = ' aria-current="page"' if active in {"kb", "diseases"} else ""
    ask_current = ' aria-current="page"' if active == "ask" else ""
    try_current = ' aria-current="page"' if active == "try" else ""
    prevent_href = "/ukr/prevent.html" if target_lang == "uk" else "/prevent.html"
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

    return f"""<header class="top-bar site-header">
  <link rel="stylesheet" href="/header.css?v=design-20261010">
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
    <div class="lang-switch" role="group" aria-label="Language">
      <{ua_tag} class="{ua_cls}"{ua_attr}><span class="lang-flag flag-ua" aria-hidden="true"></span>UA</{ua_tag}>
      <{en_tag} class="{en_cls}"{en_attr}><span class="lang-flag flag-en" aria-hidden="true"></span>EN</{en_tag}>
    </div>
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
