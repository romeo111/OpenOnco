from types import SimpleNamespace
from scripts import privacy_copy
from scripts.build_site import render_landing,render_about,render_ask
from scripts.build_public_locales import localize_public_page
from scripts.public_curated_copy import messages_for
from scripts.site_locales import LOCALES


def test_all_language_entry_pages_describe_server_transfer():
    stats=SimpleNamespace(entities=[],coverage=[])
    source_home=render_landing(stats,target_lang='en')
    source_about=render_about(stats,target_lang='en')
    for locale in LOCALES:
        if locale in ('en','uk'):
            home=render_landing(stats,target_lang=locale)
            about=render_about(stats,target_lang=locale)
        else:
            catalog=messages_for(locale)
            home=localize_public_page(source_home,locale,'index.html',set(),catalog)
            about=localize_public_page(source_about,locale,'about.html',set(),catalog)
        assert privacy_copy.HOME[locale] in home
        assert privacy_copy.LOCAL_BODY[locale] in about
        assert privacy_copy.TRANSFER_BODY[locale] in about
        assert 'Patient data stays in your browser' not in home


def test_server_notice_precedes_case_submission_controls():
    for locale in ('en','uk'):
        page=render_ask(target_lang=locale)
        assert privacy_copy.TRANSFER_BODY[locale] in page
        assert page.index('data-data-flow="server"') < page.index('id="caseText"')
