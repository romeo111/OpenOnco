"""Translated display must preserve treatment inputs and quiz grading."""
import errno
import hashlib
import json
import re
from pathlib import Path

import pytest

from scripts.build_clinical_locales import build_clinical_locales, localize_page
from scripts.site_translation_catalog import numeric_tokens, quantity_tokens
from scripts.clinical_translation_checks import acceptable_draft
from serverless import clinical_question as cq


@pytest.mark.parametrize('locale', ['es', 'pt', 'de', 'fr'])
def test_original_source_blocks_preserve_text_attributes_and_links(locale):
    original = '<span lang="uk" data-original-source title="Original label"><b>Не перекладати ECOG &lt;0.5</b><a href="/cases/source.html" title="Original label">Original label</a></span>'
    source = '<html lang="en"><body><main>' + original + '<p>Translate this</p></main></body></html>'
    catalog = {'Не перекладати ECOG <0.5': 'INCORRECT', 'Original label': 'INCORRECT', 'Translate this': 'NATIVE COPY'}
    output = localize_page(source, locale, 'cases/test.html', {'cases/source.html'}, catalog)
    assert original in output
    assert 'INCORRECT' not in output
    assert '<p>NATIVE COPY</p>' in output
    assert f'<html lang="{locale}">' in output


def test_original_scope_ends_at_self_closing_and_nested_elements():
    source = '<html lang="en"><body><input data-original-source title="Original label"/><p>Translate this</p><div data-original-source><span><b>Original label</b></span></div><p>Translate this</p></body></html>'
    output = localize_page(source, 'fr', 'try.html', set(), {'Original label': 'INCORRECT', 'Translate this': 'NATIVE COPY'})
    assert 'title="Original label"' in output
    assert '<b>Original label</b>' in output
    assert 'INCORRECT' not in output
    assert output.count('<p>NATIVE COPY</p>') == 2


@pytest.mark.parametrize('locale', ['es', 'pt', 'de', 'fr'])
@pytest.mark.parametrize('language', ['uk', 'en'])
def test_patient_findings_review_label_is_translated_and_preserves_variant(locale, language):
    from scripts.clinical_curated_copy import messages_for
    catalog = messages_for(locale)
    label = ('Interpretation requires clinical review' if language == 'en'
             else 'Інтерпретація потребує клінічного перегляду')
    source = f'<html lang="{language}"><head><title>Test</title></head><body><main><ul class="findings-list"><li><strong data-variant-original="V600E">BRAF V600E</strong><span class="patient-badge patient-warn" data-clinical-review="pending">{label}</span></li></ul></main></body></html>'
    rendered = localize_page(source, locale, 'cases/test.patient.html', set(), catalog)
    assert catalog[label] in rendered
    assert 'data-clinical-review="pending"' in rendered
    assert 'data-variant-original="V600E">BRAF V600E' in rendered
    assert 'content="pending_clinical_review"' in rendered


@pytest.mark.parametrize('locale', ['es', 'pt', 'de', 'fr'])
def test_original_fragments_honor_nested_language_and_restore_parent_language(locale):
    original = 'Оригінальні дані збережено для перевірки без зміни клінічних значень. ' * 4
    source = '<html lang="en"><body><main><section lang="uk"><div><p>' + original + '</p></div></section><p>' + original + '</p></main></body></html>'
    output = localize_page(source, locale, 'cases/test.html', set(), {})
    assert output.count('class="translation-original-fragment" lang="uk"') == 1
    assert output.count('class="translation-original-fragment" lang="en"') == 1
    assert output.count(original) == 2
    assert 'lang="en" hreflang="en" data-original-source' in output


@pytest.mark.parametrize('locale', ['es', 'pt', 'de', 'fr'])
@pytest.mark.parametrize('declared,expected', [('en', 'en'), ('uk', 'uk'), ('uk-UA', 'uk-ua'), (None, 'und')])
def test_original_attribution_uses_declared_source_language_without_guessing(locale, declared, expected):
    from scripts.build_clinical_locales import ORIGINAL_LABELS, NOTICES, UKRAINIAN_ORIGINAL_LINKS, UNSPECIFIED_ORIGINAL_LINKS
    paragraph = 'Оригінальний текст із результатами дослідження збережено для перевірки. ' * 4
    language = f' lang="{declared}"' if declared else ''
    source = f'<html{language}><head><title>Test</title></head><body><main><p>{paragraph}</p><input value="positive"><script>const original = "uk";</script></main></body></html>'
    output = localize_page(source, locale, 'try.html', set(), {})
    assert f'class="translation-original-fragment" lang="{expected}"' in output
    assert f'data-label="{ORIGINAL_LABELS[locale]}"' in output
    assert paragraph in output
    assert f'lang="{expected}" hreflang="{expected}" data-original-source' in output
    expected_link = UKRAINIAN_ORIGINAL_LINKS[locale] if expected.startswith('uk') else NOTICES[locale][1] if expected == 'en' else UNSPECIFIED_ORIGINAL_LINKS[locale]
    assert expected_link in output
    assert 'value="positive"' in output
    assert '<script>const original = "uk";</script>' in output
    assert 'clinical-localization.js?v=20261011-source-language' in output
    assert hashlib.sha256(source.encode('utf-8')).hexdigest() in output


@pytest.mark.parametrize('locale', ['es', 'pt', 'de', 'fr'])
@pytest.mark.parametrize('source_lang', ['uk', 'en'])
def test_missing_molecular_interpretation_notice_is_localized_without_changing_data(locale, source_lang):
    from types import SimpleNamespace
    from knowledge_base.engine.render import _render_findings_plain
    from scripts.site_translation_catalog import load_catalog
    result = SimpleNamespace(disease_id='DIS-SYNTHETIC', plan=SimpleNamespace(variant_actionability=[]))
    paragraph = _render_findings_plain(result, target_lang=source_lang)
    source_text = paragraph.removeprefix('<p>').removesuffix('</p>')
    catalog = load_catalog(locale)
    source = '<html lang="en"><head><title>Test</title></head><body><main>' + paragraph + '<input value="positive" data-biomarker-id="BIO-SYNTHETIC"></main></body></html>'
    output = localize_page(source, locale, 'cases/synthetic.patient.html', set(), catalog)
    assert catalog[source_text] != source_text
    assert catalog[source_text] in output
    assert source_text not in output
    assert 'value="positive"' in output
    assert 'data-biomarker-id="BIO-SYNTHETIC"' in output
    assert 'pending_clinical_review' in output


@pytest.mark.parametrize('locale', ['es', 'pt', 'de', 'fr'])
def test_overlay_preserves_executable_values_and_source_ids(locale):
    source = '''<!doctype html><html lang="en"><head><title>Clinical draft</title></head>
<body><main><h1>Clinical draft</h1><p>Use 10 mg/m²; SRC-EXAMPLE-2026.</p>
<a href="../drugs/test.html">Drug</a><input value="negative" placeholder="Enter age">
<article data-search="Clinical draft" data-correct-answer="B" data-question-id="HQ-TEST">
<label><input type="radio" name="HQ-TEST" value="B">Correct option</label></article>
<pre>&lt;profile age="10"&gt;</pre><script>const correct = 'B';</script></main></body></html>'''
    source = source.replace('</main>', '<textarea>Clinical draft</textarea><svg><path d="M0 0 L10 10"/><text>Clinical draft</text></svg></main>')
    catalog = {'Clinical draft': 'Draft local', 'Enter age': 'Age local', 'Correct option': 'Option local'}
    output = localize_page(source, locale, 'kb/diseases/test.html', {'kb/drugs/test.html'}, catalog)
    assert f'<html lang="{locale}">' in output
    assert 'value="negative"' in output and 'value="B"' in output
    assert 'data-correct-answer="B"' in output and 'data-question-id="HQ-TEST"' in output
    assert "<script>const correct = 'B';</script>" in output
    assert '<pre>&lt;profile age="10"&gt;</pre>' in output
    assert '<textarea>Clinical draft</textarea>' in output
    assert '<path d="M0 0 L10 10"/>' in output
    assert f'href="/{locale}/kb/drugs/test.html"' in output
    assert 'href="/kb/diseases/test.html" lang="en"' in output
    assert 'translation-review" content="pending_clinical_review"' in output
    assert 'Use 10 mg/m²; SRC-EXAMPLE-2026.' in output
    assert 'data-search="Clinical draft Draft local"' in output
    assert 'clinical-localization.js' not in output


def test_local_wiki_fetches_local_index_without_rewriting_other_scripts():
    source = '<html><head></head><body><main></main><script>const KB_INDEX_URL = "/kb_search_index.json"; const id = "DRUG-X";</script></body></html>'
    output = localize_page(source, 'fr', 'kb.html', set(), {})
    assert 'const KB_INDEX_URL = "/fr/kb_search_index.json"' in output
    assert 'const id = "DRUG-X"' in output
    assert 'data-catalog="/fr/clinical-ui-translations.json"' in output


def test_plan_builder_uses_full_clinical_display_catalog():
    output = localize_page('<html><head></head><body><main></main></body></html>', 'de', 'try.html', set(), {})
    assert 'data-catalog="/de/clinical-translations.json"' in output
    assert '<html lang="de">' in output


def test_shared_css_preserves_styles_and_cannot_rewrite_script_literals():
    css = '\nmain { color: #123; }\n'
    source = '<html><head><style>' + css + '</style></head><body><script>const template = "<style>p { color: red; }</style>";</script><main>Clinical draft</main></body></html>'
    styles = {}
    output = localize_page(source, 'fr', 'try.html', set(), {}, style_assets=styles)
    digest = hashlib.sha256(css.encode('utf-8')).hexdigest()
    assert styles == {digest: css}
    assert f'href="/clinical-styles/{digest}.css"' in output
    assert 'const template = "<style>p { color: red; }</style>";' in output


def test_language_flags_do_not_guess_missing_archive_counterparts():
    from scripts.site_nav import render_top_bar
    available = {'plans/archive/example.html', 'fr/plans/archive/example.html', 'ukr/index.html'}
    header = render_top_bar('try', 'fr', page_path='plans/archive/example.html', available_paths=available)
    assert re.search(r'<a[^>]*href="/plans/archive/example.html"[^>]*hreflang="en"', header)
    assert re.search(r'<a[^>]*href="/ukr/"[^>]*hreflang="uk"', header)
    assert 'href="/ukr/plans/archive/example.html"' not in header


def test_record_slug_ending_in_index_is_not_a_directory_homepage():
    from scripts.site_locales import locale_href
    assert locale_href('kb/biomarkers/bio-ki67-ihc-proliferation-index.html', 'fr') == '/fr/kb/biomarkers/bio-ki67-ihc-proliferation-index.html'
    assert locale_href('index.html', 'fr') == '/fr/'
    assert locale_href('plans/archive/index.html', 'fr') == '/fr/plans/archive/'


def test_catalog_tampering_blocks_publication_before_writing_pages(tmp_path):
    catalogs = tmp_path / 'catalogs'
    catalogs.mkdir()
    inventory = {}
    for locale in ('es', 'pt', 'de', 'fr'):
        path = catalogs / f'clinical.{locale}.json'
        path.write_text('{"Clinical draft":"Draft"}', encoding='utf-8')
        inventory[locale] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    (catalogs / 'clinical_manifest.json').write_text(json.dumps({'languages': inventory}), encoding='utf-8')
    (catalogs / 'clinical.es.json').write_text('{"Clinical draft":"Changed after verification"}', encoding='utf-8')
    output = tmp_path / 'site'
    output.mkdir()
    with pytest.raises(ValueError, match='checksum mismatch: es'):
        build_clinical_locales(output, catalogs)
    assert list(output.iterdir()) == []


def test_generated_page_write_retries_transient_windows_error(monkeypatch):
    from scripts.build_clinical_locales import write_generated_text

    class FlakyPath:
        calls = 0

        def write_text(self, value, encoding):
            self.calls += 1
            if self.calls == 1:
                raise OSError(errno.EINVAL, 'transient write failure')
            assert value == 'localized' and encoding == 'utf-8'

    monkeypatch.setattr('scripts.build_clinical_locales.time.sleep', lambda _: None)
    path = FlakyPath()
    write_generated_text(path, 'localized')
    assert path.calls == 2


def test_digit_check_keeps_exponents_and_inequalities():
    assert numeric_tokens('ANC <1.0 × 10⁹/L; 20 mg/m²') == numeric_tokens('ANC <1,0 × 10⁹/L ; 20 mg/m²')
    assert numeric_tokens('10 mg') != numeric_tokens('100 mg')
    assert numeric_tokens('ANC <1') != numeric_tokens('ANC >1')
    assert quantity_tokens('20 mg/m²') == quantity_tokens('20 mg/m2')
    assert not acceptable_draft('20 mg', '20 mL', 'fr')
    assert not acceptable_draft('CA-19-9 normal.', 'CA-19-9 No es normal.', 'es')
    assert not acceptable_draft('HER2 positive', 'HER2 negativo', 'es')
    assert not acceptable_draft('EGFR positive', 'EGF positivo', 'es')
    assert not acceptable_draft('MSI/MMR; MSI-H/dMMR', 'IMS/RMR ; MSI-H/dMRR', 'fr')
    assert not acceptable_draft('Actionable driver testing', 'Tests de conducteurs réalisables', 'fr')
    assert not acceptable_draft('EGFR T790M', 'EGFR T790L', 'fr')
    assert not acceptable_draft('VHL disease', 'Maladie de la LVH', 'fr')
    assert not acceptable_draft('CDH1 mutation', 'Mutation HDC1', 'fr')
    assert not acceptable_draft('IPSS-M risk assessment', 'IPSS M Risikobewertung', 'de')
    assert not acceptable_draft('HER2-', 'HER2+', 'fr')
    assert not acceptable_draft('7+3 induction', 'Induction 7-3', 'fr')
    assert not acceptable_draft('OpenOnco', 'OuvreOnco', 'fr')
    assert not acceptable_draft('Clinical staging', 'Mise en scène clinique', 'fr')
    assert not acceptable_draft('midostaurin', 'midostaurina', 'pt', re.compile(r'\bmidostaurin\b', re.I))
    assert not acceptable_draft('TEST-CBC, TEST-LFT, TEST-ECHO', 'ESC, ESC', 'pt')
    assert not acceptable_draft('PLAN-AML-SECONDARY-CPX351-1L-001-V1', 'PLAN-AML-SECUNDARIO-CPX351-1L-001-V1', 'es')
    assert not acceptable_draft('clinician_confirmations.CC-ALGO-TEST-1L', 'C-ALGO-TEST-1L', 'fr')
    assert not acceptable_draft('findings.peripheral_neuropathy_grade', 'a.détermination.', 'fr')
    assert not acceptable_draft('showcase-endometrial-dmmr-msh2-1l', 'dmmr-msh2-1l', 'fr')
    assert not acceptable_draft('Refractory lymphoma', 'Feuerfestes Lymphom', 'de')
    assert not acceptable_draft('Primary Refractory lymphoma', 'Primärfeuerfestes Lymphom', 'de')
    assert not acceptable_draft('Drugs + NSZU', 'Drogen + NSZU', 'de')
    assert not acceptable_draft('Drug Facts', 'Drogenakten', 'de')
    assert not acceptable_draft('categorical (mutated | wild-type)', 'categórico (mutado en el tipo salvaje)', 'es')
    assert not acceptable_draft(
        'POLE POLE germline exonuclease-domain pathogenic (PPAP — polymerase proofreading–associated polyposis)',
        'Polipropileno (pole)', 'es',
    )


def test_technical_code_list_translates_only_its_label():
    from scripts.clinical_curated_copy import diagnostic_display
    source = 'Unevaluated RedFlags: RF-NO-PRIOR-TREATMENT, RF-EGFR-T790M'
    translated = diagnostic_display(source, 'fr')
    assert translated == 'Alertes non évaluées : RF-NO-PRIOR-TREATMENT, RF-EGFR-T790M'
    assert acceptable_draft(source, translated, 'fr')
    assert diagnostic_display(source + '; avoid treatment.', 'fr') is None
    assert not acceptable_draft(source, translated.replace('RF-EGFR-T790M', 'RF-EGFR-T790L'), 'fr')


def _publication_fixture(root):
    baseline = root / 'scripts/locales'
    staging = root / '.tmp/clinical-next'
    docs = root / 'docs'
    for directory in (baseline, staging, docs):
        directory.mkdir(parents=True)
    source = 'Use 10 mg osimertinib; EGFR T790M.'
    (root / '.tmp/clinical-source-strings.json').write_text(json.dumps([source]), encoding='utf-8')
    (docs / 'kb_search_index.json').write_text(json.dumps({'entries': [{'kind_key': 'drugs', 'title': 'osimertinib'}]}), encoding='utf-8')
    for locale in ('es', 'pt', 'de', 'fr'):
        (baseline / f'clinical.{locale}.json').write_text(json.dumps({'Previous key': 'Previous key'}), encoding='utf-8')
        (staging / f'clinical.{locale}.json').write_text(json.dumps({'Previous key': 'Previous key', source: 'Use 100 mg osimertinib; EGFR T790L.'}), encoding='utf-8')
        (staging / f'clinical.{locale}.summary.json').write_text(json.dumps({'source_strings': 1, 'strings': 2}), encoding='utf-8')
    return baseline, staging, source


def test_publication_preserves_prior_keys_and_uses_complete_original_for_failed_dose(monkeypatch, tmp_path):
    from scripts.publish_clinical_catalogs import publish
    baseline, staging, source = _publication_fixture(tmp_path)
    monkeypatch.chdir(tmp_path)
    publish()
    for locale in ('es', 'pt', 'de', 'fr'):
        result = json.loads((baseline / f'clinical.{locale}.json').read_text(encoding='utf-8'))
        assert result == {'Previous key': 'Previous key', source: source}
        assert json.loads((staging / f'clinical.{locale}.json').read_text(encoding='utf-8'))[source].startswith('Use 100 mg')
    assert len(list((tmp_path / '.tmp/clinical-catalog-backups').glob('*.json'))) == 4
    manifest = json.loads((baseline / 'clinical_manifest.json').read_text(encoding='utf-8'))
    assert all(item['final_check_originals'] == 1 for item in manifest['languages'].values())


def test_incomplete_language_blocks_all_catalog_replacement(monkeypatch, tmp_path):
    from scripts.publish_clinical_catalogs import publish
    baseline, staging, _ = _publication_fixture(tmp_path)
    (staging / 'clinical.fr.summary.json').write_text('{"source_strings":1,"strings":99}', encoding='utf-8')
    before = {path.name: path.read_bytes() for path in baseline.iterdir()}
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError, match='completion summary mismatch'):
        publish()
    assert before == {path.name: path.read_bytes() for path in baseline.iterdir()}


def test_recheck_restores_corrupted_identifiers_without_clinical_approval(tmp_path):
    from scripts.recheck_clinical_catalogs import recheck
    catalogs = tmp_path / 'scripts' / 'locales'
    catalogs.mkdir(parents=True)
    index = tmp_path / 'index.json'
    index.write_text('{"entries": []}', encoding='utf-8')
    source = 'TEST-CBC, TEST-LFT, TEST-ECHO'
    languages = {}
    for locale in ('es', 'pt', 'de', 'fr'):
        path = catalogs / f'clinical.{locale}.json'
        path.write_text(json.dumps({source: 'ESC, ESC'}), encoding='utf-8')
        languages[locale] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    manifest = catalogs / 'clinical_manifest.json'
    manifest.write_text(json.dumps({'languages': languages}), encoding='utf-8')
    before = {path.name: path.read_bytes() for path in catalogs.iterdir()}
    assert recheck(catalogs, index) == dict.fromkeys(languages, 1)
    assert before == {path.name: path.read_bytes() for path in catalogs.iterdir()}
    assert recheck(catalogs, index, apply=True) == dict.fromkeys(languages, 1)
    updated = json.loads(manifest.read_text(encoding='utf-8'))
    for locale in languages:
        path = catalogs / f'clinical.{locale}.json'
        assert json.loads(path.read_text(encoding='utf-8'))[source] == source
        assert updated['languages'][locale]['sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert updated['languages'][locale]['fidelity_fallbacks'] == 1


def test_curated_safety_notices_preserve_english_negations_and_identifiers():
    from scripts.clinical_curated_copy import safety_notices_for
    for locale in ('es', 'pt', 'de', 'fr'):
        notices = safety_notices_for(locale)
        assert len(notices) == 7
        assert all(acceptable_draft(source, translated, locale) for source, translated in notices.items())
        assert all('CHARTER' in translated for source, translated in notices.items() if 'CHARTER' in source)


def test_curated_safety_notice_application_checksums_and_is_idempotent(tmp_path):
    from scripts.apply_curated_safety_notices import apply_notices
    from scripts.clinical_curated_copy import safety_notices_for
    catalogs = tmp_path / 'scripts' / 'locales'
    catalogs.mkdir(parents=True)
    languages = {}
    for locale in ('es', 'pt', 'de', 'fr'):
        source = next(iter(safety_notices_for(locale)))
        path = catalogs / f'clinical.{locale}.json'
        path.write_text(json.dumps({source: source}), encoding='utf-8')
        languages[locale] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    manifest = catalogs / 'clinical_manifest.json'
    manifest.write_text(json.dumps({'languages': languages}), encoding='utf-8')
    assert apply_notices(catalogs) == dict.fromkeys(languages, 1)
    assert apply_notices(catalogs, apply=True) == dict.fromkeys(languages, 1)
    assert apply_notices(catalogs) == dict.fromkeys(languages, 0)
    updated = json.loads(manifest.read_text(encoding='utf-8'))
    for locale in languages:
        source, translated = next(iter(safety_notices_for(locale).items()))
        path = catalogs / f'clinical.{locale}.json'
        assert json.loads(path.read_text(encoding='utf-8'))[source] == translated
        assert updated['languages'][locale]['sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.parametrize('locale,language', [('es','Spanish'),('pt','European Portuguese'),('de','German'),('fr','French')])
def test_presenter_requests_native_language_without_changing_engine_payload(monkeypatch, locale, language):
    captured = {}
    monkeypatch.setattr(cq, 'call_openai_json', lambda **kwargs: captured.update(kwargs) or {})
    engine = cq.EngineSummary(mode='treatment', ok=False, payload=None, warnings=[], error=None)
    cq.compose_answer(case_text='Synthetic example', extraction={}, patient={}, engine=engine, locale=locale)
    assert f'Write all user-facing prose in {language}.' in captured['system']
    assert 'doses, numeric values and source identifiers exactly' in captured['system']
    assert json.loads(captured['user'])['required_safety_note'] == cq.DISCLAIMER_TRANSLATIONS[locale]


def test_html_export_uses_visible_translated_document():
    import subprocess

    root = Path(__file__).resolve().parents[1]
    # Execute export behavior, including native translation and actual Ukrainian fallback.
    subprocess.run(['node', 'tests/browser_report_export.cjs'], cwd=root, check=True, timeout=30)


def test_completed_clinical_inventory_advertises_real_tool_counterparts():
    from scripts.site_head import render_seo_metadata
    inventory = {'try.html', 'ukr/try.html', 'fr/try.html', 'fr/handbook/hb-dlbcl-1l.html'}
    metadata = render_seo_metadata(path='fr/try.html', title='OpenOnco', description='Tool', locale='fr', available_paths=inventory)
    assert '"@type":"SoftwareApplication"' in metadata
    assert 'hreflang="en"' in metadata and 'hreflang="fr"' in metadata
    assert 'hreflang="de"' not in metadata


@pytest.mark.parametrize('locale', ['es', 'pt', 'de', 'fr'])
def test_classification_name_is_localized_without_changing_disease_code(locale):
    from scripts.clinical_curated_copy import NSCLC
    from scripts.site_translation_catalog import load_catalog
    source = '<html><head></head><body><main><select><option value="DIS-NSCLC">Non-small cell lung cancer</option></select></main></body></html>'
    output = localize_page(source, locale, 'try.html', set(), load_catalog(locale))
    assert f'value="DIS-NSCLC">{NSCLC[locale]}</option>' in output


@pytest.mark.parametrize('locale', ['es', 'pt', 'de', 'fr'])
def test_empty_question_is_native_without_using_an_api(monkeypatch, locale):
    monkeypatch.setattr(cq, 'call_openai_json', lambda **kwargs: pytest.fail('No API call expected'))
    answer = cq.answer_clinical_question('', locale=locale)
    assert answer['clarifying_questions'][0] != 'Надішліть клінічну ситуацію текстом.'
    assert answer['safety_note'] == cq.DISCLAIMER_TRANSLATIONS[locale]


@pytest.mark.parametrize('case', ['Lungenkrebs, Stadium IV', 'Cancro da mama', 'Cáncer de pulmón', 'Leucémie aiguë'])
def test_native_oncology_cases_pass_preflight_without_translation(case):
    assert cq._preflight_case_text(case, locale='fr') is None


def test_committed_catalogs_preserve_numeric_claims():
    repository = Path(__file__).resolve().parents[1]
    root = repository / 'scripts/locales'
    index = json.loads((repository / 'docs/kb_search_index.json').read_text(encoding='utf-8'))
    drugs = {entry['title'] for entry in index['entries'] if entry.get('kind_key') == 'drugs' and len(entry['title']) < 70}
    pattern = re.compile(r'(?<!\w)(?:' + '|'.join(re.escape(name) for name in sorted(drugs, key=len, reverse=True)) + r')(?!\w)', re.I)
    for locale in ('es', 'pt', 'de', 'fr'):
        path = root / f'clinical.{locale}.json'
        if not path.exists():
            continue
        for source, translated in json.loads(path.read_text(encoding='utf-8')).items():
            if (root / 'clinical_manifest.json').exists():
                assert acceptable_draft(source, translated, locale, pattern), (locale, source, translated)
            assert numeric_tokens(source) == numeric_tokens(translated), (locale, source, translated)
            for identifier in re.findall(r'\b(?:SRC|DIS|BIO|DRUG|REG|ALGO|RF|IND|HQ|HB)-[A-Z0-9_-]+\b', source):
                assert identifier in translated, (locale, source, identifier)


def test_generated_locale_html_uses_fidelity_fallback_for_structured_status():
    repository = Path(__file__).resolve().parents[1]
    page = (repository / 'docs/es/kb/diseases/dis-aml.html').read_text(encoding='utf-8')
    assert 'reviewed 2026-04-25 | pending_clinical_signoff' in page
    assert 'pendance_clinical_signoff' not in page
