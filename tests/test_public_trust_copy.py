"""Regression checks for promises on published entry points and their templates."""
import html
import re
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import privacy_copy, public_trust_copy
from scripts.build_site import render_landing, render_about, render_ask, _DISEASES_PAGE_LABELS


def text_of(page):
    page = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', page, flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>', '', page))


@pytest.mark.parametrize('locale', public_trust_copy.LANGUAGES)
def test_published_entrypoints_explain_review_and_data_flow(locale):
    root = Path(__file__).resolve().parents[1] / 'docs'
    root /= '' if locale == 'en' else 'ukr' if locale == 'uk' else locale
    disease_text = text_of((root / 'diseases.html').read_text(encoding='utf-8'))
    assert public_trust_copy.REVIEW_METRIC[locale] in disease_text
    for name in ('index', 'about', 'capabilities', 'try', 'ask'):
        page = (root / f'{name}.html').read_text(encoding='utf-8')
        visible = text_of(page)
        assert public_trust_copy.REVIEW_BODY[locale] in visible, (locale, name)
        assert 'No server.' not in visible
        assert 'Patient JSON never leaves' not in visible
        assert 'Two-reviewer merge' not in visible
        assert 'Clinical review gate' not in visible
        if name in ('about', 'capabilities', 'try'):
            assert privacy_copy.LOCAL_BODY[locale] in visible
        if name in ('about', 'capabilities', 'ask'):
            assert privacy_copy.TRANSFER_BODY[locale] in visible
        if name == 'capabilities':
            assert visible.count(privacy_copy.HOME[locale]) == 2
        if name == 'index':
            assert public_trust_copy.HEADLINE[locale] in visible
            assert public_trust_copy.LEAD[locale] in visible
        if name == 'ask':
            assert page.index('data-data-flow="server"') < page.index('id="caseText"')


@pytest.mark.parametrize('locale', ('en', 'uk'))
def test_source_templates_keep_review_limits(locale):
    stats = SimpleNamespace(entities=[], coverage=[])
    for render in (render_landing, render_about):
        assert public_trust_copy.REVIEW_BODY[locale] in text_of(render(stats, target_lang=locale))
    assert public_trust_copy.REVIEW_BODY[locale] in text_of(render_ask(target_lang=locale))


def test_review_percentage_is_content_review_not_accuracy_or_quorum():
    for locale in ('en', 'uk'):
        assert public_trust_copy.REVIEW_METRIC[locale] in _DISEASES_PAGE_LABELS[locale]['metrics']
        assert not any('≥ 2' in value for value in _DISEASES_PAGE_LABELS[locale]['metrics'])
