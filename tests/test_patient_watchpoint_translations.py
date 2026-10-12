"""Source edits must invalidate the whole English symptom/action pair."""
import copy
import json
import re
from pathlib import Path

import pytest
import yaml
from bs4 import BeautifulSoup

from knowledge_base.engine import generate_plan, render_plan_html
from knowledge_base.engine._patient_watchpoint_translations import translate_watchpoint

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'


@pytest.mark.parametrize('name,expected', [('codox_m_ivac.yaml', 7), ('da_epoch_r.yaml', 10),
                                         ('codox_ivac_proven_cns.yaml', 12)])
def test_saved_pairs_preserve_numbers_and_unreviewed_entries_remain_original(name, expected):
    regimen = yaml.safe_load((KB / 'regimens' / name).read_text(encoding='utf-8'))
    pairs = [translate_watchpoint(regimen['id'], point) for point in regimen['between_visit_watchpoints']]
    assert sum(pair is not None for pair in pairs) == expected
    for point, pair in zip(regimen['between_visit_watchpoints'], pairs, strict=True):
        if pair:
            assert re.findall(r'\d+(?:\.\d+)?', point['trigger_ua']) == re.findall(r'\d+(?:\.\d+)?', pair[0])
            assert pair[0] and pair[1]


@pytest.mark.parametrize('field,value', [('trigger_ua', 'Температура 39°C'),
    ('action_ua', 'Зачекайте'), ('urgency', 'log_at_next_visit'),
    ('cycle_day_window', 'Only day 7'), ('sources', ['SRC-OTHER']), ('future_condition', 'new condition')])
def test_any_source_condition_change_invalidates_both_fragments(field, value):
    reg = yaml.safe_load((KB / 'regimens/da_epoch_r.yaml').read_text(encoding='utf-8'))
    point = copy.deepcopy(reg['between_visit_watchpoints'][4])
    assert translate_watchpoint(reg['id'], point)
    point[field] = value
    assert translate_watchpoint(reg['id'], point) is None
    assert translate_watchpoint('REG-OTHER', reg['between_visit_watchpoints'][4]) is None
    assert translate_watchpoint(reg['id'], reg['between_visit_watchpoints'][4], target_lang='uk') is None


def test_actual_english_report_is_a_draft_and_stale_pair_falls_back_together():
    examples = json.loads((ROOT / 'docs/examples.json').read_text(encoding='utf-8'))
    profile = next(e['json'] for e in examples if e['case_id'] == 'pmbcl-typical')
    result = generate_plan(profile, kb_root=KB)
    before = result.plan.model_dump()
    soup = BeautifulSoup(render_plan_html(result, mode='patient', target_lang='en'), 'html.parser')
    track = soup.select_one('.bv-track[data-source-id="REG-DA-EPOCH-R"]')
    assert track and not track.select('.translation-fallback')
    assert len(track.select('.bv-trigger[lang="en"]')) == 10
    assert len(track.select('.bv-trigger[lang="en"][data-original-source]')) == 10
    assert len(track.select('.bv-action[data-translation-status="draft_pending_clinical_and_language_review"]')) == 10
    assert '38°C or higher' in track.get_text() and 'even without a temperature' in track.get_text()
    assert 'If you cannot reach your treatment team' in track.get_text()
    assert soup.select_one('[data-translation-status="draft-partial"]')
    assert result.plan.model_dump() == before
    from scripts.build_clinical_locales import localize_page
    source = str(track)
    unsafe_catalog = {node.get_text(): 'Wait until your next visit'
                      for node in track.select('.bv-trigger,.bv-action')}
    localized = BeautifulSoup(localize_page(source, 'fr', 'cases/synthetic.patient.html',
                                            {'cases/synthetic.patient.html'}, unsafe_catalog), 'html.parser')
    assert [node.get_text() for node in localized.select('.bv-trigger,.bv-action')] == [
        node.get_text() for node in track.select('.bv-trigger,.bv-action')]
    result = copy.deepcopy(result)
    regimen = next(t.regimen_data for t in result.plan.tracks if t.regimen_data['id'] == 'REG-DA-EPOCH-R')
    point = regimen['between_visit_watchpoints'][4]
    point['urgency'] = 'call_clinic_same_day'
    soup = BeautifulSoup(render_plan_html(result, mode='patient', target_lang='en'), 'html.parser')
    original = next(node for node in soup.select('.bv-trigger[data-original-source]')
                    if point['trigger_ua'] == node.get_text())
    row = original.find_parent('li')
    assert row.select_one('.bv-action[data-original-source]').get_text() == point['action_ua']
    assert row.select_one('.translation-fallback')


def test_clinician_mode_never_uses_patient_watchpoint_translation(monkeypatch):
    import importlib
    render_module = importlib.import_module('knowledge_base.engine.render')
    examples = json.loads((ROOT / 'docs/examples.json').read_text(encoding='utf-8'))
    profile = next(e['json'] for e in examples if e['case_id'] == 'pmbcl-typical')
    result = generate_plan(profile, kb_root=KB)
    before = result.plan.model_dump()

    def forbidden(*args, **kwargs):
        raise AssertionError('Clinician mode must retain its own rendering path')

    monkeypatch.setattr(render_module, 'translate_watchpoint', forbidden)
    output = render_plan_html(result, mode='clinician', target_lang='en')
    assert output and not BeautifulSoup(output, 'html.parser').select_one('.between-visits')
    assert result.plan.model_dump() == before
