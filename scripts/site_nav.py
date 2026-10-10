"""Shared navigation for public pages and the educational handbook."""

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
    """Top navigation bar with:
    - brand on the left → links to home
    - reading-only nav (Home, Capabilities, Onco Wiki, Tumor Board, About)
      in the middle
    - language switcher (UA / EN toggle) on the right
    - prominent action buttons on the far right (Plan Builder, Onco Wiki, Tumor Board)

    Per user direction: 'Спробувати' is an action and gets a separate CTA
    button styled distinctly from the nav links.

    Site layout: EN is the default at root (/), UA lives at /ukr/."""
    def cls(name: str) -> str:
        return ' class="active"' if active == name else ""

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

    return f"""<header class="top-bar">
  <div class="brand-line">
    <a href="{home_path}" class="brand-mini">OpenOnco</a>
  </div>
  <nav class="top-nav">
    <a href="{home_path}"{cls("home")}>{labels['home']}</a>
    {extra_links}
    <a href="{about_path}"{cls("about")}>{labels['about']}</a>
  </nav>
  <div class="top-right">
    <div class="lang-switch" role="group" aria-label="Language">
      <{ua_tag} class="{ua_cls}"{ua_attr}><span class="lang-flag flag-ua" aria-hidden="true"></span>UA</{ua_tag}>
      <{en_tag} class="{en_cls}"{en_attr}><span class="lang-flag flag-en" aria-hidden="true"></span>EN</{en_tag}>
    </div>
    <div class="top-cta-group">
      <a href="{try_path}" class="btn-cta-top btn-cta-try"{try_current}>{labels['try_cta']}</a>
      <a href="{prevent_href}" class="btn-cta-top btn-cta-secondary"{prevent_current}>{labels['prevent']}</a>
      <a href="{kb_href}" class="btn-cta-top btn-cta-secondary"{kb_current}>{labels['kb']}</a>
      <a href="{ask_path}" class="btn-cta-top btn-cta-secondary"{ask_current}>{labels['ask']}</a>
    </div>
  </div>
</header>"""
