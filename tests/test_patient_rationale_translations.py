from copy import deepcopy
from types import SimpleNamespace

from knowledge_base.engine._patient_rationale import (
    RATIONALE_TRANSLATION_STATUS, build_track_rationale, build_track_rationale_html,
)
from knowledge_base.engine.render import _render_emergency_section
from knowledge_base.engine.render import _medicine_form_ua, _regimen_schedule_ua
from knowledge_base.engine.render import _regimen_tolerability_ua, _render_regimen_tolerability
from knowledge_base.engine.render import _render_track_drugs
import pytest
from knowledge_base.engine._patient_vocabulary import (
    ESCAT_PLAIN_UA, ESCAT_TIER_PATIENT_LABEL, ESCAT_TIER_PATIENT_LABEL_EN,
    PATIENT_VOCABULARY_EN_DRAFT, PATIENT_VOCABULARY_TRANSLATION_STATUS, explain,
    DRUG_CLASS_PATIENT_ALIASES, explain_drug_class,
)


def test_english_rationale_preserves_findings_thresholds_and_input():
    result = SimpleNamespace(
        plan=SimpleNamespace(variant_actionability=[{'biomarker_id': 'BIO-BRAF', 'variant_qualifier': 'V600E', 'escat_tier': 'IA'}]),
        trace=[{'fired_red_flags': ['RF-TEST']}],
        kb_resolved={'red_flags': {'RF-TEST': {'definition': 'Value <0.5 mg/L. Second sentence.', 'definition_ua': 'Показник <0.5 mg/L.'}}},
    )
    before = deepcopy(result.__dict__)
    bullets = build_track_rationale(result, SimpleNamespace(is_default=True), target_lang='en')
    assert 'BRAF V600E' in bullets[0]
    assert '<0.5 mg/L' in bullets[1]
    assert 'Second sentence' not in bullets[1]
    assert result.__dict__ == before
    rendered = build_track_rationale_html(result, SimpleNamespace(is_default=True), target_lang='en')
    assert '&lt;0.5 mg/L' in rendered
    assert RATIONALE_TRANSLATION_STATUS['en'] == 'draft_pending_review'


def test_missing_english_definition_explicitly_retains_original():
    result = SimpleNamespace(plan=None, trace=[{'fired_red_flags': ['RF-TEST']}], kb_resolved={'red_flags': {'RF-TEST': {'definition_ua': 'Не чекати.'}}})
    bullets = build_track_rationale(result, SimpleNamespace(is_default=True), target_lang='en')
    assert 'original Ukrainian text; translation unavailable' in bullets[0]
    assert 'Не чекати' in bullets[0]


def test_no_fired_flags_is_not_a_claim_of_absent_clinical_risk():
    result = SimpleNamespace(plan=None, trace=[], kb_resolved={})
    track = SimpleNamespace(is_default=True)
    assert 'does not rule out risks' in build_track_rationale(result, track, target_lang='en')[0]
    assert 'не виключає ризиків' in build_track_rationale(result, track)[0]


def test_english_emergency_section_uses_only_fired_records_and_preserves_values():
    result = SimpleNamespace(trace=[{'fired_red_flags': ['RF-TEST']}], kb_resolved={'red_flags': {
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
    result = SimpleNamespace(trace=[{'fired_red_flags': ['RF-TEST']}], kb_resolved={'red_flags': {
        'RF-TEST': {'id': 'RF-TEST', 'severity': 'critical', 'definition_ua': 'Не чекати.'},
    }})
    output = _render_emergency_section(result, target_lang='en')
    assert 'Original Ukrainian text; translation unavailable' in output
    assert 'Не чекати' in output


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
])
def test_actual_drug_class_renders_explanation_without_changing_record(filename, canonical):
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
            assert explain(canonical, target_lang=language) in html
        assert 'medicine for your condition' not in html
        assert 'препарат для лікування вашого захворювання' not in html
    assert drug == before


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
