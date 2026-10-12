"""Additional language routes, native navigation and conservative draft guards."""
from bs4 import BeautifulSoup
import pytest

from scripts.additional_locale_copy import ADDITIONAL_LANGUAGES, ENGLISH_COPY, NAVIGATION, NAVIGATION_KEYS
from scripts.site_locales import COPY, LOCALES, locale_href, split_locale
from scripts.site_nav import render_top_bar
from scripts.site_translation_catalog import polarity_tokens
from scripts.clinical_translation_checks import acceptable_draft
from scripts.shared_clinical_reader import render_shared_reader


@pytest.mark.parametrize('locale', ADDITIONAL_LANGUAGES)
def test_additional_navigation_has_native_names_flags_and_stable_routes(locale):
    header = BeautifulSoup(render_top_bar('capabilities', locale, page_path='capabilities.html'), 'html.parser')
    menu = header.select('.language-menu nav a')
    assert [link['lang'] for link in menu][:2] == ['en', 'uk']
    assert [link['lang'] for link in menu] == list(LOCALES)
    assert len(menu) == 11
    assert all(link.select_one('svg.language-flag') for link in menu)
    current = header.select_one('.language-menu a[aria-current="true"]')
    assert current['lang'] == locale
    assert current['href'] == f'/{locale}/capabilities.html'
    assert header.select_one('.brand-mini')['href'] == f'/{locale}/'
    assert NAVIGATION[locale][9] in header.get_text()
    assert locale_href('index.html', locale) == f'/{locale}/'
    assert split_locale(f'{locale}/try.html') == (locale, 'try.html')
    assert set(COPY[locale]) == set(ENGLISH_COPY)
    assert len(NAVIGATION_KEYS) == len(NAVIGATION[locale]) == 15


@pytest.mark.parametrize('locale,negative', [('it', 'non'), ('da', 'ikke'), ('sv', 'inte'), ('nb', 'ikke'), ('fi', 'ei')])
def test_added_language_guards_do_not_accept_lost_negation_or_changed_dose(locale, negative):
    assert polarity_tokens(negative, locale)[0] == 1
    assert not acceptable_draft('not EGFR 20 mg', 'EGFR 20 mg', locale)
    assert not acceptable_draft('EGFR 20 mg', 'EGFR 200 mg', locale)
    assert acceptable_draft('EGFR 20 mg', 'EGFR 20 mg', locale)


@pytest.mark.parametrize('locale,weekly', [
    ('it', '100 mg una volta alla settimana'), ('da', '100 mg ugentligt'),
    ('sv', '100 mg varje vecka'), ('nb', '100 mg ukentlig'), ('fi', '100 mg viikoittain'),
])
def test_added_language_cannot_turn_daily_dose_into_weekly(locale, weekly):
    source = '100 mg once daily'
    assert not acceptable_draft(source, weekly, locale)
    assert not acceptable_draft(source, '100 mg', locale)
    assert acceptable_draft(source, source, locale)


@pytest.mark.parametrize('locale,daily', [
    ('it', '100 mg al giorno'), ('da', '100 mg dagligt'),
    ('sv', '100 mg dagligen'), ('nb', '100 mg daglig'), ('fi', '100 mg päivittäin'),
])
def test_added_language_dosing_schedule_is_retained_when_translated(locale, daily):
    assert acceptable_draft('100 mg daily', daily, locale)
    assert not acceptable_draft('100 mg once weekly', daily, locale)


@pytest.mark.parametrize('locale', ADDITIONAL_LANGUAGES)
def test_unmapped_critical_clause_falls_back_to_the_complete_original(locale):
    source = 'Continuous until progression or unacceptable toxicity.'
    assert not acceptable_draft(source, 'Continue until progression.', locale)
    assert acceptable_draft(source, source, locale)


@pytest.mark.parametrize('locale', ADDITIONAL_LANGUAGES)
def test_shared_readers_preserve_source_and_fit_the_free_hosting_budget(locale):
    source = '<html lang="en"><head><title>Synthetic report</title></head><body><main>' + ('<p>SRC-EXAMPLE: 20 mg</p>' * 5000) + '</main></body></html>'
    reader = render_shared_reader(source, locale, 'cases/synthetic.html', 'Synthetic report')
    soup = BeautifulSoup(reader, 'html.parser')
    assert soup.html['lang'] == locale
    assert soup.select_one('[data-shared-clinical-source]')['src'] == '/cases/synthetic.html'
    assert soup.select_one('script[data-catalog]')['data-catalog'] == f'/{locale}/clinical-translations.json'
    assert len(reader.encode('utf-8')) < 4000
    assert ('<p>SRC-EXAMPLE: 20 mg</p>' * 5000) not in reader
    assert 'data-original-source' in reader
    assert 'pending_clinical_review' in reader
    assert source.count('20 mg') == 5000


@pytest.mark.parametrize('path', ['../private.html', '/outside.html', 'https://example.com/case.html', 'case.json'])
def test_reader_does_not_accept_uninventoried_or_external_paths(path):
    with pytest.raises(ValueError):
        render_shared_reader('Original', 'it', path, 'Test')


@pytest.mark.parametrize('language', ['en', 'uk', 'und'])
def test_shared_reader_original_link_uses_actual_source_language(language):
    reader = render_shared_reader(f'<html lang="{language}"><body>Source</body></html>', 'fi', 'plans/archive/demo.html', 'Demo')
    link = BeautifulSoup(reader, 'html.parser').select_one('[data-original-source]')
    assert link['lang'] == link['hreflang'] == language


@pytest.mark.parametrize('word', ['cancro', 'kræft', 'cancer', 'kreft', 'syöpä'])
def test_new_language_oncology_terms_are_recognized_without_provider_calls(word):
    from serverless.clinical_question import _looks_like_oncology
    assert _looks_like_oncology(word)


@pytest.mark.parametrize('locale', ADDITIONAL_LANGUAGES)
def test_new_language_empty_request_has_native_disclaimer_without_model_use(locale):
    from serverless.clinical_question import DISCLAIMER_TRANSLATIONS, answer_clinical_question
    answer = answer_clinical_question('', locale=locale)
    assert answer['status'] == 'needs_clarification'
    assert answer['safety_note'] == DISCLAIMER_TRANSLATIONS[locale]
    assert answer.get('extraction') is None


@pytest.mark.parametrize('locale', ADDITIONAL_LANGUAGES)
def test_canonical_diagnosis_names_do_not_publish_literal_model_corruption(locale):
    from scripts.clinical_curated_copy import messages_for
    assert messages_for(locale)['Colorectal carcinoma'] == 'Colorectal carcinoma'


@pytest.mark.parametrize('locale', ['es', 'pt', 'de', 'fr', 'it', 'da', 'sv', 'nb', 'fi'])
def test_treatment_line_copy_overrides_literal_row_translations(locale):
    import json
    import re
    from pathlib import Path
    from scripts.clinical_curated_copy import messages_for, TREATMENT_LINE_LABELS
    runtime = (Path(__file__).resolve().parents[1] / 'scripts/clinical-localization.js').read_text(encoding='utf-8')
    embedded = json.loads(re.search(r'const treatmentLineCopy = (.*);', runtime)[1])
    assert embedded == TREATMENT_LINE_LABELS
    assert messages_for(locale)['first line'] == embedded[locale]
    assert embedded[locale] not in ['prima riga', 'första raden', 'ensimmäinen rivi']
    assert runtime.index("catalog['first line'] = treatmentLineCopy[locale]") < runtime.index('const nativeValues =')
