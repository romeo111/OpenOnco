from copy import deepcopy
from types import SimpleNamespace

from knowledge_base.engine._patient_rationale import (
    RATIONALE_TRANSLATION_STATUS, build_track_rationale, build_track_rationale_html,
    build_plan_findings_context, build_plan_findings_context_html,
)
from knowledge_base.engine.render import _render_emergency_section
from knowledge_base.engine.render import _medicine_form_ua, _regimen_schedule_ua
from knowledge_base.engine.render import _regimen_tolerability_ua, _render_regimen_tolerability
from knowledge_base.engine.render import _render_track_drugs
import pytest
from knowledge_base.engine._patient_note_translations import PATIENT_NOTE_EN_DRAFT, translate_patient_note
from knowledge_base.engine._patient_vocabulary import (
    ESCAT_PLAIN_UA, ESCAT_TIER_PATIENT_LABEL, ESCAT_TIER_PATIENT_LABEL_EN,
    PATIENT_VOCABULARY_EN_DRAFT, PATIENT_VOCABULARY_TRANSLATION_STATUS, explain,
    DRUG_CLASS_PATIENT_ALIASES, explain_drug_class,
)


@pytest.mark.parametrize('target_lang', ['uk', 'en'])
@pytest.mark.parametrize('track_index', [0, 1])
@pytest.mark.parametrize('is_default', [False, True])
def test_patient_label_role_is_independent_of_position_and_clinical_reason(target_lang, track_index, is_default):
    from knowledge_base.engine.render import _track_label_ua
    track = SimpleNamespace(is_default=is_default, indication_id='IND-TEST',
                            selection_reason='Provisional option; no branch selected')
    before = deepcopy(track.__dict__)
    label, modifier = _track_label_ua(track_index, 2, track, target_lang=target_lang)
    expected_role = ('Main option in this report' if is_default else 'Alternative option in this report') if target_lang == 'en' else ('Основний варіант у звіті' if is_default else 'Альтернативний варіант у звіті')
    assert label.endswith(expected_role)
    assert modifier == ('default' if is_default else 'alternative')
    assert track.__dict__ == before


@pytest.mark.parametrize('locale', ['es', 'pt', 'de', 'fr'])
@pytest.mark.parametrize('track_index,track_count,is_default', [(0, 1, True), (0, 2, True), (1, 2, True), (0, 2, False), (1, 2, False)])
def test_native_patient_labels_translate_report_role_without_changing_track(locale, track_index, track_count, is_default):
    from scripts.build_clinical_locales import localize_page
    from scripts.clinical_curated_copy import messages_for
    from knowledge_base.engine.render import _track_label_ua
    track = SimpleNamespace(is_default=is_default, indication_id='IND-TEST')
    before = deepcopy(track.__dict__)
    label, modifier = _track_label_ua(track_index, track_count, track, target_lang='en')
    catalog = messages_for(locale)
    source = (f'<html lang="en"><body><div class="track-card track-card--{modifier}" data-source-id="REG-TEST">'
              f'<p class="track-label">{label}</p><span lang="und" data-original-source>Original source value: &lt;0.5</span></div></body></html>')
    localized = localize_page(source, locale, 'cases/test.patient.html', set(), catalog)
    assert f'<p class="track-label">{catalog[label]}</p>' in localized
    assert label not in localized
    assert f'class="track-card track-card--{modifier}"' in localized
    assert 'data-source-id="REG-TEST"' in localized
    assert 'Original source value: &lt;0.5' in localized
    assert track.__dict__ == before


def test_retained_ukrainian_drug_note_is_protected_from_english_expansion():
    from html import escape
    from knowledge_base.engine._patient_vocabulary import expand_first_use
    note = 'Не перекладати: ECOG, 0.5 mg/kg, <38.5°C; FDA.'
    drug = {'id': 'DRUG-TEST', 'notes_patient': note}
    track = SimpleNamespace(regimen_data={'components': [{'drug_id': 'DRUG-TEST', 'route': 'IV'}]})
    result = SimpleNamespace(disease_id='DIS-TEST')
    before = deepcopy((drug, track.__dict__))
    rendered = _render_track_drugs(result, track, {'DRUG-TEST': drug}, None, target_lang='en')
    protected = f'<span lang="uk" data-original-source>{escape(note)}</span>'
    assert protected in rendered
    expanded = expand_first_use(rendered + '<p>ECOG</p>', target_lang='en')
    assert protected in expanded
    assert 'daily activities' in expanded
    assert (drug, track.__dict__) == before


@pytest.mark.parametrize('locale', ['es', 'pt', 'de', 'fr'])
def test_native_notice_translates_while_retained_drug_note_does_not(locale):
    from html import escape
    from scripts.build_clinical_locales import localize_page
    from scripts.clinical_curated_copy import messages_for
    note = 'Синтетичний текст: ECOG <0.5; FDA.'
    drug = {'id': 'DRUG-TEST', 'notes_patient': note}
    track = SimpleNamespace(regimen_data={'components': [{'drug_id': 'DRUG-TEST', 'route': 'IV'}]})
    result = SimpleNamespace(disease_id='DIS-TEST')
    rendered = _render_track_drugs(result, track, {'DRUG-TEST': drug}, None, target_lang='en')
    catalog = messages_for(locale)
    catalog[note] = 'INCORRECT REPLACEMENT'
    output = localize_page('<html lang="en"><body>' + rendered + '</body></html>', locale, 'cases/test.patient.html', set(), catalog)
    assert catalog['Original source explanation; translation unavailable:'] in output
    assert f'<span lang="uk" data-original-source>{escape(note)}</span>' in output
    assert 'INCORRECT REPLACEMENT' not in output
    assert 'data-source-id="DRUG-TEST"' in output


def test_english_rationale_preserves_findings_thresholds_and_input():
    result = SimpleNamespace(
        plan=SimpleNamespace(variant_actionability=[{'biomarker_id': 'BIO-BRAF', 'variant_qualifier': 'V600E', 'escat_tier': 'IA'}]),
        trace=[{'fired_red_flags': ['RF-TEST'], 'branch': {'result': 'IND-TEST'}}],
        kb_resolved={'red_flags': {'RF-TEST': {'definition': 'Value <0.5 mg/L. Second sentence.', 'definition_ua': 'Показник <0.5 mg/L.'}}},
    )
    before = deepcopy(result.__dict__)
    bullets = build_track_rationale(result, SimpleNamespace(is_default=True, indication_id='IND-TEST'), target_lang='en')
    assert 'BRAF V600E' in build_plan_findings_context(result, target_lang='en')[0]
    assert '<0.5 mg/L' in bullets[1]
    assert 'Second sentence' not in bullets[1]
    assert result.__dict__ == before
    rendered = build_track_rationale_html(result, SimpleNamespace(is_default=True, indication_id='IND-TEST'), target_lang='en')
    assert '&lt;0.5 mg/L' in rendered
    assert RATIONALE_TRANSLATION_STATUS['en'] == 'draft_pending_review'


def test_missing_english_definition_explicitly_retains_original():
    result = SimpleNamespace(plan=None, trace=[{'fired_red_flags': ['RF-TEST'], 'branch': {'result': 'IND-TEST'}}], kb_resolved={'red_flags': {'RF-TEST': {'definition_ua': 'Не чекати.'}}})
    bullets = build_track_rationale(result, SimpleNamespace(is_default=True, indication_id='IND-TEST'), target_lang='en')
    assert 'original Ukrainian text; translation unavailable' in bullets[1]
    assert 'Не чекати' in bullets[1]
    rendered = build_track_rationale_html(result, SimpleNamespace(is_default=True, indication_id='IND-TEST'), target_lang='en')
    assert '<span lang="uk" data-original-source>Не чекати.</span>' in rendered


def test_no_fired_flags_is_not_a_claim_of_absent_clinical_risk():
    result = SimpleNamespace(plan=None, trace=[{'result':'IND-TEST','fired_red_flags':[]}], kb_resolved={})
    track = SimpleNamespace(is_default=True, indication_id='IND-TEST')
    assert 'does not rule out risks' in build_track_rationale(result, track, target_lang='en')[1]
    assert 'не виключає ризиків' in build_track_rationale(result, track)[1]


def test_english_emergency_section_uses_only_fired_records_and_preserves_values():
    result = SimpleNamespace(trace=[{'fired_red_flags': ['RF-TEST'], 'branch': {'result': 'IND-TEST'}}], kb_resolved={'red_flags': {
        'RF-TEST': {'id': 'RF-TEST', 'severity': 'critical', 'definition': 'Value <0.5 mg/L. More detail.', 'definition_ua': 'Показник <0.5 mg/L.'},
        'RF-OTHER': {'id': 'RF-OTHER', 'severity': 'critical', 'definition': 'Unfired condition'},
    }})
    before = deepcopy(result.__dict__)
    output = _render_emergency_section(result, target_lang='en')
    assert 'Signals requiring immediate attention' in output
    assert 'not a confirmed diagnosis' in output
    assert 'Value &lt;0.5 mg/L' in output
    assert 'Unfired condition' not in output
    assert 'More detail' not in output
    assert 'data-rf-id="RF-TEST"' in output
    assert result.__dict__ == before
    result.trace = []
    assert 'does not rule out emergencies' in _render_emergency_section(result, target_lang='en')


def test_english_emergency_section_marks_missing_translation():
    result = SimpleNamespace(trace=[{'fired_red_flags': ['RF-TEST'], 'branch': {'result': 'IND-TEST'}}], kb_resolved={'red_flags': {
        'RF-TEST': {'id': 'RF-TEST', 'severity': 'critical', 'definition_ua': 'Не чекати.'},
    }})
    output = _render_emergency_section(result, target_lang='en')
    assert 'Original Ukrainian text; translation unavailable' in output
    assert 'Не чекати' in output
    assert '<span lang="uk" data-original-source>Не чекати</span>' in output


@pytest.mark.parametrize('route,expected', [
    ('PO', 'taken by mouth'), ('IV', 'intravenous infusion'),
    ('SC', 'under the skin'), ('IM', 'into a muscle'),
    ('IT', 'spinal canal'), ('topical', 'cream or gel'),
])
def test_english_route_labels_keep_component_route_authoritative(route, expected):
    component = {'route': route, 'dose': '0.5 mg/kg'}
    drug = {'route': 'IV', 'formulations': ['tablet']}
    before = deepcopy((component, drug))
    assert expected in _medicine_form_ua(component, drug, target_lang='en')
    assert (component, drug) == before


def test_english_schedule_preserves_counts_and_freeform_source():
    assert _regimen_schedule_ua({'cycle_length_days': 28, 'total_cycles': 6}, target_lang='en') == '6 cycle(s) of 28 days'
    assert _regimen_schedule_ua({}, target_lang='en') == ''
    result = _regimen_schedule_ua({'cycle_length_days': 28, 'total_cycles': 'Не припиняти <умова>'}, target_lang='en')
    assert 'original source text' in result
    assert 'Не припиняти &lt;умова&gt;' in result
    assert '28 days' in result
    assert '<span lang="und" data-original-source>Не припиняти &lt;умова&gt;</span>' in result


@pytest.mark.parametrize('profile', ['', 'none', 'low', 'low_moderate', 'moderate', 'moderate-high', 'moderate-severe', 'high', 'severe', 'very-high', 'high special', 'unknown'])
def test_english_tolerability_keeps_category_and_personal_prediction_caveat(profile):
    data = {'toxicity_profile': profile}
    original = deepcopy(data)
    ua = _regimen_tolerability_ua(data)
    en = _regimen_tolerability_ua(data, target_lang='en')
    assert en[2] == ua[2]
    assert en[0] != ua[0]
    rendered = _render_regimen_tolerability(data, target_lang='en')
    assert 'not a prediction for you personally' in rendered
    assert f'data-toxicity-profile="{profile}"' in rendered
    assert data == original


def test_patient_escat_labels_do_not_claim_personal_regulatory_approval():
    assert ESCAT_TIER_PATIENT_LABEL_EN.keys() == ESCAT_TIER_PATIENT_LABEL.keys()
    assert 'FDA' not in ESCAT_TIER_PATIENT_LABEL['IA']
    assert 'FDA' not in ESCAT_PLAIN_UA['IA']
    assert 'рандомізованими' in ESCAT_TIER_PATIENT_LABEL['IA']
    assert 'нерандомізованими' in ESCAT_TIER_PATIENT_LABEL['IB']
    assert 'non-randomised' in ESCAT_TIER_PATIENT_LABEL_EN['IB']


def test_english_vocabulary_lookup_never_silently_returns_ukrainian():
    assert PATIENT_VOCABULARY_TRANSLATION_STATUS['en'] == 'draft_pending_review'
    for term, text in PATIENT_VOCABULARY_EN_DRAFT.items():
        assert explain(term, target_lang='en') == text
        assert explain(' ' + term.upper() + ' ', target_lang='en') == text
        assert explain(term) is not None
    assert explain('V600E', target_lang='en') is None
    assert explain('missense', target_lang='fr') is None
    assert 'may be preserved or disrupted' in explain('missense', target_lang='en')
    assert 'both copies' in explain('biallelic loss', target_lang='en')


def test_vaf_explanation_distinguishes_read_fraction_from_cell_fraction():
    ua = explain('VAF')
    en = explain('VAF', target_lang='en')
    assert 'прочитаних фрагментів ДНК' in ua
    assert '50% не означає автоматично' in ua
    assert 'DNA reads' in en
    assert '50% does not automatically mean' in en
    assert 'gene copy number' in en


def test_variant_origin_explanations_do_not_assume_parental_or_tumour_only_origin():
    assert 'виникнути вперше' in explain('germline')
    assert "не обов'язково походить від батьків" in explain('germline')
    assert 'can be passed on to children' in explain('germline', target_lang='en')
    assert 'does not necessarily come from a parent' in explain('germline', target_lang='en')
    assert 'пухлинних або інших клітинах' in explain('somatic')
    assert 'tumour cells or other cells' in explain('somatic', target_lang='en')
    assert 'is not passed on to children' in explain('somatic', target_lang='en')


def test_mismatch_repair_glosses_keep_distinct_test_meanings_and_response_uncertainty():
    assert 'не гарантує відповіді' in explain('MSI-H')
    assert 'does not guarantee a treatment response' in explain('MSI-H', target_lang='en')
    assert 'це не MSI-H' in explain('MSI-L')
    assert 'this is not MSI-H' in explain('MSI-L', target_lang='en')
    assert 'сам цей результат не визначає всі можливості' in explain('MSS')
    assert 'does not determine all immunotherapy options' in explain('MSS', target_lang='en')
    assert 'результати тестів можуть не збігатися' in explain('dMMR')
    assert 'test results may disagree' in explain('dMMR', target_lang='en')
    assert 'не означає, що в пухлині немає інших змін ДНК' in explain('pMMR')
    assert 'does not mean there are no other DNA changes' in explain('pMMR', target_lang='en')


def test_drug_class_aliases_are_explicit_and_do_not_match_combination_products():
    for alias, canonical in DRUG_CLASS_PATIENT_ALIASES.items():
        for language in ('uk', 'en'):
            assert explain_drug_class(' ' + alias.upper() + ' ', target_lang=language) == explain(canonical, target_lang=language)
    assert explain_drug_class('Anthracycline plus unknown investigational medicine') is None
    assert explain_drug_class('Liposomal-encapsulated cytarabine + daunorubicin (5:1 molar ratio)') is None
    assert explain_drug_class('MSI-H') is None
    assert explain_drug_class(None) is None


@pytest.mark.parametrize('filename,canonical', [
    ('daunorubicin', 'anthracycline'),
    ('venetoclax', 'BCL-2i'),
    ('azacitidine', 'HMA'),
    ('midostaurin', 'multi-kinase inhibitor'),
    ('alemtuzumab', 'anti-CD52 mAb'),
    ('mogamulizumab', 'anti-CCR4 mAb'),
    ('axicabtagene_ciloleucel', 'CAR-T'),
    ('blinatumomab', 'bispecific antibody'),
    ('brentuximab_vedotin', 'ADC'),
    ('inotuzumab_ozogamicin', 'ADC'),
    ('loncastuximab_tesirine', 'ADC'),
    ('daratumumab', 'anti-CD38 mAb'),
    ('rituximab', 'anti-CD20 mAb'),
    ('ciltacabtagene_autoleucel', 'CAR-T'),
    ('idecabtagene_vicleucel', 'CAR-T'),
    ('drug_tarlatamab', 'bispecific antibody'),
    ('elranatamab', 'bispecific antibody'),
    ('talquetamab', 'bispecific antibody'),
    ('teclistamab', 'bispecific antibody'),
    ('amivantamab', 'bispecific antibody'),
    ('zenocutuzumab', 'bispecific antibody'),
])
def test_actual_drug_class_renders_explanation_without_changing_record(filename, canonical):
    from html import escape
    from pathlib import Path
    import yaml
    path = Path(__file__).resolve().parents[1] / 'knowledge_base/hosted/content/drugs' / (filename + '.yaml')
    drug = yaml.load(path.read_text(encoding='utf-8'), Loader=getattr(yaml, 'CSafeLoader', yaml.SafeLoader))
    before = deepcopy(drug)
    track = SimpleNamespace(regimen_data={'components': [{'drug_id': drug['id'], 'route': 'IV'}]})
    result = SimpleNamespace(disease_id='DIS-AML')
    for language in ('uk', 'en'):
        html = _render_track_drugs(result, track, {drug['id']: drug}, None, target_lang=language)
        note = (drug.get('notes_patient') or '').strip()
        if note:
            from html import escape
            assert escape(note) in html
        if language == 'en' or not note:
            assert escape(explain(canonical, target_lang=language)) in html
        assert 'medicine for your condition' not in html
        assert 'препарат для лікування вашого захворювання' not in html
    assert drug == before


@pytest.mark.parametrize('filename', ['cytarabine', 'capecitabine', 'doxorubicin'])
def test_authored_note_translation_requires_current_source_and_retains_changed_original(filename):
    from pathlib import Path
    from html import escape
    import yaml
    path = Path(__file__).resolve().parents[1] / 'knowledge_base/hosted/content/drugs' / (filename + '.yaml')
    drug = yaml.load(path.read_text(encoding='utf-8'), Loader=getattr(yaml, 'CSafeLoader', yaml.SafeLoader))
    before = deepcopy(drug)
    translated = translate_patient_note(drug['id'], drug['notes_patient'])
    assert translated == PATIENT_NOTE_EN_DRAFT[drug['id']][1]
    assert translate_patient_note(drug['id'], drug['notes_patient'], target_lang='fr') is None
    track = SimpleNamespace(regimen_data={'components': [{'drug_id': drug['id'], 'route': 'IV'}]})
    result = SimpleNamespace(disease_id='DIS-AML')
    html = _render_track_drugs(result, track, {drug['id']: drug}, None, target_lang='en')
    assert escape(translated) in html
    assert 'Original source explanation; translation unavailable' not in html
    assert drug == before
    drug['notes_patient'] += ' Не змінюйте дозу 0.5 mg.'
    assert translate_patient_note(drug['id'], drug['notes_patient']) is None
    html = _render_track_drugs(result, track, {drug['id']: drug}, None, target_lang='en')
    assert escape(drug['notes_patient'].strip()) in html
    assert 'Original source explanation; translation unavailable' in html


def test_english_drug_class_explanation_retains_authored_patient_note():
    result = SimpleNamespace(disease_id='DIS-AML')
    track = SimpleNamespace(regimen_data={'components': [{'drug_id': 'DRUG-TEST', 'route': 'PO'}]})
    drug = {'names': {'english': 'Test medicine'}, 'drug_class': 'FLT3i', 'notes_patient': 'Не змінюйте дозу 0.5 mg.'}
    before = deepcopy(drug)
    rendered = _render_track_drugs(result, track, {'DRUG-TEST': drug}, None, target_lang='en')
    assert 'blocks FLT3' in rendered
    assert 'Не змінюйте дозу 0.5 mg.' in rendered
    assert 'Original source explanation; translation unavailable' in rendered
    assert drug == before
    del drug['notes_patient']
    rendered = _render_track_drugs(result, track, {'DRUG-TEST': drug}, None, target_lang='en')
    assert 'blocks FLT3' in rendered
    assert 'translation unavailable' not in rendered


@pytest.mark.parametrize('drug_class,expected', [
    ('alkylating agent', 'damages tumour DNA'),
    ('anthracycline', 'toxic to the heart'),
    ('platinum agent', 'cisplatin, carboplatin, oxaliplatin'),
    ('antimetabolite', '5-FU, methotrexate, gemcitabine'),
    ('topoisomerase inhibitor', 'irinotecan, etoposide'),
    ('vinca alkaloid', 'vincristine, vinblastine'),
    ('taxane', 'paclitaxel, docetaxel'),
    ('fluoropyrimidine', '5-FU/capecitabine'),
    ('nitrosourea', 'lomustine, carmustine'),
    ('epothilone', 'some resistance mechanisms'),
    ('purine analog', 'hairy cell leukaemia'),
    ('proteasome inhibitor', 'bortezomib, carfilzomib'),
    ('G-CSF', 'granulocyte production'),
    ('ESA', 'red blood cell production'),
    ('antiemetic', 'ondansetron, aprepitant, palonosetron'),
    ('steroid', 'dexamethasone, prednisone'),
    ('anti-fungal prophylaxis', 'very low neutrophil counts'),
    ('antiviral prophylaxis', 'entecavir, acyclovir, valacyclovir'),
    ('PCP prophylaxis', 'trimethoprim/sulfamethoxazole'),
    ('growth factor', 'erythropoietin'),
    ('TPO-mimetic', 'eltrombopag, romiplostim'),
    ('iron chelator', 'deferasirox'),
])
def test_english_drug_card_gloss_preserves_examples_and_plan_input(drug_class, expected):
    result = SimpleNamespace(disease_id='DIS-AML')
    track = SimpleNamespace(regimen_data={'components': [{'drug_id': 'DRUG-TEST', 'route': 'IV'}]})
    drug = {'names': {'english': 'Test medicine'}, 'drug_class': drug_class}
    before = deepcopy(drug)
    html = _render_track_drugs(result, track, {'DRUG-TEST': drug}, None, target_lang='en')
    assert expected in html
    assert 'translation unavailable' not in html
    assert drug == before


@pytest.mark.parametrize("lang", ["en", "uk"])
@pytest.mark.parametrize("tier", ["IA", "IB", "IIA", "IIB"])
@pytest.mark.parametrize("representation", ["dict", "object"])
@pytest.mark.parametrize("ready", [True, False, None])
def test_report_context_uses_selected_hit_review_status(lang, tier, representation, ready):
    selected = {"biomarker_id": "BIO-BRAF", "variant_qualifier": "V600E", "escat_tier": tier}
    if ready is not None:
        selected["clinical_use_ready"] = ready
    other = {"biomarker_id": "BIO-KRAS", "escat_tier": tier, "clinical_use_ready": not ready}
    if representation == "object":
        selected, other = SimpleNamespace(**selected), SimpleNamespace(**other)
    result = SimpleNamespace(plan=SimpleNamespace(variant_actionability=[selected, other]), trace=[], kb_resolved={})
    before = deepcopy(result.__dict__)
    track = SimpleNamespace(is_default=False)
    bullets = build_plan_findings_context(result, target_lang=lang)
    output = build_plan_findings_context_html(result, target_lang=lang)
    assert "BRAF V600E" in bullets[0]
    assert "KRAS" not in bullets[0]
    assert ('data-biomarker-review="pending"' in output) == (ready is not True)
    if ready is not True:
        assert ("pending" if lang == "en" else "не завершена") in bullets[0]
        assert "for choosing this treatment" not in bullets[0]
        assert "користь цього варіанту" not in bullets[0]
    elif lang == "en":
        assert f"tier {tier}" in bullets[0]
        assert "choosing this treatment" not in bullets[0]
    assert result.__dict__ == before


@pytest.mark.parametrize("locale", ["es", "pt", "de", "fr"])
def test_native_context_preserves_hit_and_translates_review_notice(locale):
    from scripts.build_clinical_locales import localize_page
    from scripts.clinical_curated_copy import messages_for
    result = SimpleNamespace(plan=SimpleNamespace(variant_actionability=[
        {"biomarker_id": "BIO-BRAF", "variant_qualifier": "V600E", "escat_tier": "IA", "clinical_use_ready": False}
    ]), trace=[], kb_resolved={})
    output = build_plan_findings_context_html(result, target_lang="en")
    catalog = messages_for(locale)
    localized = localize_page('<html lang="en"><body>' + output + '</body></html>', locale, 'cases/test.patient.html', set(), catalog)
    assert catalog['Clinical review of this biomarker record is pending.'] in localized
    assert 'data-biomarker-review="pending"' in localized
    assert 'BRAF V600E' in localized
    assert 'tier IA' in localized


@pytest.mark.parametrize("lang", ["en", "uk"])
@pytest.mark.parametrize("default", [True, False])
@pytest.mark.parametrize("terminal", ["branch", "fallback"])
def test_recorded_path_is_bound_to_exact_indication(lang, default, terminal):
    trace = [{"fired_red_flags": ["RF-SYNTHETIC"], "branch": {"next_step": 2}}]
    trace.append({"branch": {"result": "IND-SELECTED"}} if terminal == "branch" else {"result": "IND-SELECTED"})
    result = SimpleNamespace(plan=SimpleNamespace(variant_actionability=[
        {"biomarker_id": "BIO-BRAF", "variant_qualifier": "V600E", "escat_tier": "IA", "clinical_use_ready": True}
    ]), trace=trace, kb_resolved={"red_flags": {"RF-SYNTHETIC": {"definition": "Recorded threshold <0.5 mg/L.", "definition_ua": "Записаний поріг <0.5 mg/L."}}})
    before = deepcopy(result.__dict__)
    selected = SimpleNamespace(indication_id="IND-SELECTED", is_default=default)
    other = SimpleNamespace(indication_id="IND-OTHER", is_default=not default)
    selected_html = build_track_rationale_html(result, selected, target_lang=lang)
    other_html = build_track_rationale_html(result, other, target_lang=lang)
    assert "&lt;0.5 mg/L" in selected_html
    assert "0.5" not in other_html
    assert "BRAF" not in selected_html + other_html
    assert ("does not record" if lang == "en" else "не записано шлях") in other_html
    assert result.__dict__ == before


@pytest.mark.parametrize("trace", [[], [{"fired_red_flags": ["RF-X"]}],
    [{"branch": {"result": "IND-SELECTED"}}, {"branch": {"result": None}}],
    [{"branch": "legacy"}], [{"result": "IND-OTHER"}]])
def test_unlinked_and_legacy_paths_do_not_invent_reasons(trace):
    result = SimpleNamespace(plan=None, trace=trace, kb_resolved={"red_flags": {"RF-X": {"definition": "Must not appear."}}})
    output = build_track_rationale_html(result, SimpleNamespace(indication_id="IND-SELECTED", is_default=True), target_lang="en")
    assert "does not record an algorithm path selecting this option" in output
    assert "Must not appear" not in output
    assert "based on clinical guidelines" not in output


def test_real_showcase_context_is_outside_all_track_explanations():
    import json,re
    from pathlib import Path
    from knowledge_base.engine import generate_plan
    from knowledge_base.engine.render import render_plan_html
    root=Path(__file__).resolve().parents[1]
    profile=json.loads((root/'examples/patient_showcase_crc_braf_v600e_2l.json').read_text(encoding='utf-8'))
    result=generate_plan(profile,kb_root=root/'knowledge_base/hosted/content')
    before=deepcopy(result.plan.model_dump())
    document=render_plan_html(result,mode='patient',target_lang='en')
    context=re.search(r'<div class="why-findings-context".*?</div>',document,re.S).group()
    assert "BRAF V600E" in context
    assert context.count('data-biomarker-review="pending"')==1
    blocks=re.findall(r'<div class="why-track".*?</div>',document,re.S)
    assert len(blocks)==len(result.plan.tracks)
    for track,block in zip(result.plan.tracks,blocks):
        assert 'data-biomarker-review=' not in block
        if not track.is_default:
            assert "BRAF" not in block
            assert "does not record an algorithm path" in block
    assert result.plan.model_dump()==before


@pytest.mark.parametrize("locale", ["es", "pt", "de", "fr"])
@pytest.mark.parametrize("linked", [True, False])
def test_native_track_path_notices_translate_without_changing_association(locale, linked):
    from scripts.build_clinical_locales import localize_page
    from scripts.clinical_curated_copy import messages_for
    result=SimpleNamespace(plan=None, trace=[{"result":"IND-SELECTED","fired_red_flags":[]}], kb_resolved={})
    track=SimpleNamespace(indication_id="IND-SELECTED" if linked else "IND-OTHER",is_default=True)
    output=build_track_rationale_html(result,track,target_lang="en")
    catalog=messages_for(locale)
    localized=localize_page('<html lang="en"><body>'+output+'</body></html>',locale,'cases/test.patient.html',set(),catalog)
    expected=("The recorded algorithm path selected this option. This does not establish its suitability for you."
              if linked else "This report does not record an algorithm path selecting this option. Ask your doctor to review the technical report and its suitability for you.")
    assert catalog[expected] in localized
    assert expected not in localized
    if linked:
        assert catalog['No red flags were recorded as triggered on that path. This does not rule out risks or replace assessment by your doctor.'] in localized


def test_unselected_path_keeps_all_recorded_signals_outside_tracks():
    from knowledge_base.engine.render import _render_why_section
    track=SimpleNamespace(indication_id="IND-UNSELECTED",is_default=True,regimen_data={"id":"REG-SYNTHETIC"},label="")
    result=SimpleNamespace(plan=SimpleNamespace(tracks=[track],variant_actionability=[]),
        trace=[{"branch":{"result":None},"fired_red_flags":["RF-ONE","RF-TWO","RF-THREE"]}],
        kb_resolved={"red_flags":{f"RF-{name}":{"definition_ua":f"Синтетичний сигнал {name}: <0.5 mg/L."} for name in ("ONE","TWO","THREE")}})
    before=deepcopy(result.__dict__)
    document=_render_why_section(result,target_lang="en")
    assert 'data-rationale-scope="plan-signals"' in document
    for name in ("ONE","TWO","THREE"):
        assert f'data-source-id="RF-{name}"' in document
        assert f'Синтетичний сигнал {name}: &lt;0.5 mg/L.' in document
    track_block=document[document.index('<div class="why-track"'):]
    assert "Синтетичний" not in track_block
    assert result.__dict__==before


@pytest.mark.parametrize("lang,field,expected_lang", [("en","definition","en"),("en","definition_ua","uk"),("uk","definition","en"),("uk","definition_ua","uk")])
def test_signal_context_retains_declared_original_language_and_escaping(lang,field,expected_lang):
    from knowledge_base.engine._patient_rationale import build_plan_signal_context_html
    from knowledge_base.engine._patient_vocabulary import expand_first_use
    source='Original <0.5 mg/L; ECOG & <script>.'
    result=SimpleNamespace(trace=[{"fired_red_flags":["RF-SYNTHETIC"]}],kb_resolved={"red_flags":{"RF-SYNTHETIC":{field:source}}})
    output=build_plan_signal_context_html(result,target_lang=lang)
    expected=f'<span lang="{expected_lang}" data-original-source>Original &lt;0.5 mg/L; ECOG &amp; &lt;script&gt;.</span>'
    assert expected in output
    assert expected in expand_first_use(output,target_lang=lang)
    assert '<script>' not in output


@pytest.mark.parametrize("locale", ["es","pt","de","fr"])
def test_native_signal_context_translates_ui_and_preserves_all_originals(locale):
    from scripts.build_clinical_locales import localize_page
    from scripts.clinical_curated_copy import messages_for
    from knowledge_base.engine._patient_rationale import build_plan_signal_context_html
    source='Source <0.5 mg/L; ECOG.'
    result=SimpleNamespace(trace=[{"fired_red_flags":["RF-SOURCE","RF-MISSING","RF-SOURCE"]}],
        kb_resolved={"red_flags":{"RF-SOURCE":{"definition":source}}})
    output=build_plan_signal_context_html(result,target_lang="en")
    catalog=messages_for(locale);catalog[source]='INCORRECT REPLACEMENT'
    localized=localize_page('<html lang="en"><body>'+output+'</body></html>',locale,'cases/test.patient.html',set(),catalog)
    for key in ('Signals recorded in this report — not reasons for selecting every option.',
                'Recorded signal (original source text):',
                'A signal was recorded, but its explanation is unavailable. See the technical report.'):
        assert catalog[key] in localized
    assert '<span lang="en" data-original-source>Source &lt;0.5 mg/L; ECOG.</span>' in localized
    assert 'INCORRECT REPLACEMENT' not in localized
    assert localized.count('data-source-id="RF-SOURCE"')==1
    assert 'data-source-id="RF-MISSING"' in localized
