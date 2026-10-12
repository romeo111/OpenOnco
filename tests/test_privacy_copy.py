from types import SimpleNamespace
import re
from pathlib import Path
from scripts import privacy_copy
from scripts.build_site import render_landing,render_about,render_ask
from scripts.build_public_locales import localize_public_page
from scripts.public_curated_copy import messages_for
from scripts.site_locales import LOCALES
from scripts.ask_page_copy import messages_for as ask_messages
from scripts.build_clinical_locales import localize_page


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


def test_question_redesign_keeps_privacy_and_works_in_each_language():
    source = render_ask(target_lang='en')
    assert 'OpenOnco AI draft' not in source
    assert '<h1 id="askTitle">Ask an oncology question</h1>' in source
    assert '<details class="ask-advanced">' in source
    assert '<details class="ask-examples-wrap">' in source
    assert source.index('data-data-flow="server"') < source.index('id="caseText"')
    for locale in LOCALES:
        if locale in ('en', 'uk'):
            page = render_ask(target_lang=locale)
        else:
            page = localize_page(source, locale, 'ask.html', {'ask.html'}, {})
            copy = ask_messages(locale)
            assert copy['Ask an oncology question'] in page
            assert f'<title>{copy["OpenOnco · Ask an oncology question"]}</title>' in page
            assert copy['Discussion draft'] in page
            assert f'data-empty-label="{copy["Your draft will appear here after you submit a question."]}"' in page
            assert copy['Before you submit'] in page
        assert 'id="caseText"' in page
        assert 'id="endpointInput"' in page
        assert 'id="askResult"' in page
        assert page.index('data-data-flow="server"') < page.index('id="caseText"')


def test_published_question_pages_have_localized_copy_and_existing_assets():
    root = Path(__file__).resolve().parents[1] / 'docs'
    for locale in LOCALES:
        prefix = '' if locale == 'en' else 'ukr' if locale == 'uk' else locale
        page = (root / prefix / 'ask.html').read_text(encoding='utf-8')
        assert 'class="ask-guidance"' in page
        assert 'class="ask-examples-wrap"' in page
        assert page.index('data-data-flow="server"') < page.index('id="caseText"')
        if locale not in ('en', 'uk'):
            copy = ask_messages(locale)
            assert copy['Ask an oncology question'] in page
            assert copy['Your draft will appear here after you submit a question.'] in page
            for asset in re.findall(r'(?:href|src)="(/clinical-(?:styles|localization)[^"]+)"', page):
                assert (root / asset.lstrip('/').split('?')[0]).is_file(), (locale, asset)
