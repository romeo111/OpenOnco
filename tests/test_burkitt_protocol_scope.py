"""The no-proven-CNS reference must not leak into another risk/CNS population."""
import copy
import json
from pathlib import Path

import pytest
import yaml

from knowledge_base.engine import generate_plan, render_plan_html

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'


def high_risk():
    profile = json.loads((ROOT / 'examples/patient_burkitt_high_risk.json').read_text())
    profile['findings']['cns_involvement'] = False
    return profile


def test_confirmed_high_risk_without_proven_cns_retains_reference():
    result = generate_plan(high_risk(), kb_root=KB)
    assert result.default_indication_id == 'IND-BURKITT-1L-CODOXM-IVAC'
    assert result.plan.tracks[0].regimen_data['id'] == 'REG-CODOX-M-IVAC'


@pytest.mark.parametrize('field,value', [
    ('cns_involvement', True), ('cns_involvement', None),
    ('cns_involvement', 'false'), ('cns_involvement', 0),
    ('cns_involvement', ''), ('cns_involvement', 'unknown'),
    ('burkitt_high_risk', False), ('burkitt_high_risk', None),
    ('burkitt_high_risk', 'true'), ('burkitt_high_risk', 1),
])
def test_failed_selected_protocol_scope_withholds_without_substitution(field, value):
    profile = high_risk()
    profile['findings'][field] = value
    result = generate_plan(profile, kb_root=KB)
    assert not result.plan.tracks
    assert result.default_indication_id is None
    assert result.plan.knowledge_base_state['profile_selection_withheld']
    assert 'findings.' + field in result.plan.knowledge_base_state['unconfirmed_profile_fields']


@pytest.mark.parametrize('field', ['cns_involvement', 'burkitt_high_risk'])
def test_missing_confirmation_is_not_assumed_negative_or_positive(field):
    profile = high_risk()
    del profile['findings'][field]
    result = generate_plan(profile, kb_root=KB)
    assert not result.plan.tracks and result.default_indication_id is None


def test_conflicting_cross_section_confirmation_blocks_route():
    profile = high_risk()
    profile['disease']['cns_involvement'] = True
    result = generate_plan(profile, kb_root=KB)
    assert not result.plan.tracks
    assert 'disease.cns_involvement' in result.plan.knowledge_base_state['unconfirmed_profile_fields']


def test_original_synthetic_cns_case_is_not_silently_changed_to_fit_reference():
    original = json.loads((ROOT / 'examples/patient_burkitt_high_risk.json').read_text())
    before = copy.deepcopy(original)
    assert original['findings']['cns_involvement'] is True
    result = generate_plan(original, kb_root=KB)
    assert not result.plan.tracks and result.default_indication_id is None
    assert original == before


@pytest.mark.parametrize('locale', ['en', 'uk'])
def test_cns_positive_render_has_no_reference_drug_calendar(locale):
    profile = high_risk()
    profile['findings']['cns_involvement'] = True
    result = generate_plan(profile, kb_root=KB)
    html = render_plan_html(result, target_lang=locale)
    assert 'IVAC blocks only' not in html
    assert '36 hours after IV methotrexate START' not in html
    assert result.plan.knowledge_base_state['profile_selection_withheld']
    assert ('CNS status' if locale == 'en' else 'стан ЦНС') in html
    assert 'Check metastatic stage' not in html and 'перевірте метастатичну стадію' not in html


def test_low_risk_keeps_existing_default_but_has_no_wrong_alternative():
    profile = json.loads((ROOT / 'examples/patient_burkitt_low_risk.json').read_text())
    result = generate_plan(profile, kb_root=KB)
    assert result.default_indication_id == 'IND-BURKITT-1L-DAEPOCHR'
    assert all(t.indication_id != 'IND-BURKITT-1L-CODOXM-IVAC' for t in result.plan.tracks)


def test_questionnaire_does_not_preselect_risk_or_cns_answers():
    q = yaml.safe_load((KB / 'questionnaires/quest_burkitt_1l.yaml').read_text(encoding='utf-8'))
    fields = {item['field']: item for group in q['groups'] for item in group['questions']}
    for field in ['findings.burkitt_high_risk', 'findings.cns_involvement']:
        assert fields[field]['type'] == 'boolean'
        assert fields[field]['impact'] == 'critical'
        assert 'default_value' not in fields[field]


def test_static_case_preserves_withholding_in_both_views(tmp_path, monkeypatch):
    from scripts import build_site as site
    monkeypatch.setattr(site, 'search_trials', None)
    case = next(c for c in site._public_case_entries() if c.case_id == 'burkitt-high-risk')
    for locale in ['en', 'uk']:
        output = site.build_one_case(case, tmp_path, target_lang=locale)
        for path in [output, output.with_name('burkitt-high-risk.patient.html')]:
            html = path.read_text(encoding='utf-8')
            assert '36 hours after IV methotrexate START' not in html
            assert 'IVAC blocks only' not in html
            assert ('CNS status' if locale == 'en' else 'стан ЦНС') in html


def test_unexpected_empty_plan_remains_a_build_failure(tmp_path, monkeypatch):
    from types import SimpleNamespace
    from scripts import build_site as site
    case = next(c for c in site._public_case_entries() if c.case_id == 'burkitt-high-risk')
    monkeypatch.setattr(site, 'generate_plan', lambda *a, **k: SimpleNamespace(
        plan=SimpleNamespace(tracks=[], knowledge_base_state={})))
    with pytest.raises(RuntimeError, match='no treatment plan'):
        site.build_one_case(case, tmp_path)


def test_public_audit_distinguishes_intentional_withholding_from_valid_treatment():
    from scripts.audit_examples import _audit_case
    from scripts.site_cases import CASES
    case = next(c for c in CASES if c.case_id == 'burkitt-high-risk')
    report = _audit_case(case, examples_dir=ROOT / 'examples', kb_root=KB)
    assert report['status'] == 'withheld' and not report['issues']
    assert 'no automatic substitute' in report['withheld_reason']


def test_withheld_flag_cannot_hide_an_active_treatment_from_public_audit(monkeypatch):
    from scripts import audit_examples as audit
    from scripts.site_cases import CASES
    result = generate_plan(high_risk(), kb_root=KB)
    result.plan.knowledge_base_state['profile_selection_withheld'] = True
    monkeypatch.setattr(audit, 'generate_plan', lambda *a, **k: result)
    case = next(c for c in CASES if c.case_id == 'burkitt-high-risk')
    report = audit._audit_case(case, examples_dir=ROOT / 'examples', kb_root=KB)
    assert report['status'] == 'fail'
    assert 'profile-withheld output still contains a treatment selection' in report['issues']


def test_published_questionnaire_retains_blank_confirmations():
    payload = json.loads((ROOT / 'docs/questionnaires.json').read_text(encoding='utf-8'))
    q = next(item for item in payload if item['id'] == 'QUEST-BURKITT-1L-STUB')
    for field in ['findings.burkitt_high_risk', 'findings.cns_involvement']:
        matching = [item for group in q['groups'] for item in group['questions']
                    if item['field'] == field]
        assert len(matching) == 1 and 'default_value' not in matching[0]
