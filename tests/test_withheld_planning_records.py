"""Historical/source-withheld content cannot become treatment or a substitute."""
import copy
import importlib
import json
from pathlib import Path

import pytest
import yaml

from knowledge_base.engine import generate_plan, render_plan_html
from knowledge_base.engine._planning_status import planning_block_reason

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'
IND = 'IND-PTCL-1L-CHOEP-ALLOSCT'
REG = 'REG-CHOEP-ALLOSCT-CONSOLIDATION'


def profile():
    return json.loads((ROOT / 'examples/patient_ptcl_cd30_negative.json').read_text())


def injected(monkeypatch, route, *, regimen_only=False):
    bundle = importlib.import_module('knowledge_base.validation.bundle')
    original = bundle.load_packaged_content

    def load(*args, **kwargs):
        data = copy.deepcopy(original(*args, **kwargs))
        algo = data.entities_by_id['ALGO-PTCL-1L']['data']
        if regimen_only:
            data.entities_by_id[IND]['data']['planning_status'] = 'active'
        algo['output_indications'] = ['IND-TCELL-1L-CHOEP', IND]
        if route == 'selected':
            algo['default_indication'] = IND
            algo['alternative_indication'] = 'IND-TCELL-1L-CHOEP'
            algo['decision_tree'] = [{'step': 1, 'evaluate': {'any_of': []},
                                     'if_true': {'result': IND}, 'if_false': {'result': IND}}]
        elif route == 'sequencing':
            data.entities_by_id[IND]['data']['applicable_to']['line_of_therapy'] = 2
        return data

    monkeypatch.setattr(bundle, 'load_packaged_content', load)


@pytest.mark.parametrize('regimen_only', [False, True])
def test_forced_historical_selection_withholds_whole_route_without_promoting_alternative(monkeypatch, regimen_only):
    injected(monkeypatch, 'selected', regimen_only=regimen_only)
    patient = profile()
    patient['findings']['planning_status'] = 'active'
    patient['findings']['specialist_confirmation'] = True
    result = generate_plan(patient, kb_root=KB)
    assert result.plan.knowledge_base_state['planning_selection_withheld']
    assert not result.plan.tracks and not result.plan.sequencing_tracks
    assert result.default_indication_id is None
    for lang in ['en', 'uk']:
        for mode in ['clinician', 'patient']:
            html = render_plan_html(result, target_lang=lang, mode=mode)
            assert ('withheld from planning' if lang == 'en' else 'виключено з планування') in html
            assert ('automatic substitute' if lang == 'en' else 'автоматичну заміну') in html
            assert 'Flu/Mel' not in html and '5y PFS ~50%' not in html


@pytest.mark.parametrize('route', ['alternative', 'sequencing'])
def test_withheld_candidates_cannot_enter_alternatives_or_later_lines(monkeypatch, route):
    injected(monkeypatch, route)
    result = generate_plan(profile(), kb_root=KB)
    assert result.default_indication_id == 'IND-TCELL-1L-CHOEP'
    assert all(t.indication_id != IND for t in result.plan.tracks + result.plan.sequencing_tracks)


@pytest.mark.parametrize('status', ['withheld', None, False, 'approved', ''])
def test_explicit_unknown_statuses_do_not_unlock_planning(status):
    assert planning_block_reason({'planning_status': status})
    assert planning_block_reason({}, {'planning_status': status})
    assert planning_block_reason({}) is None


def test_historical_materialization_and_public_claims_are_blocked():
    plan = importlib.import_module('knowledge_base.engine.plan')
    ind = yaml.safe_load((KB / 'indications/ind_ptcl_1l_choep_allosct.yaml').read_text(encoding='utf-8'))
    reg = yaml.safe_load((KB / 'regimens/reg_choep_allosct_consolidation.yaml').read_text(encoding='utf-8'))
    with pytest.raises(ValueError, match='withheld planning record'):
        plan._materialize_track('aggressive', IND, True, 'Synthetic test',
                                {IND: {'data': ind}, REG: {'data': reg}})
    assert 'expected_outcomes' not in ind and 'nccn_category' not in ind
    assert 'known_controversies' not in ind and 'do_not_do' not in ind
    assert not reg.get('monitoring_schedule_id') and not reg.get('between_visit_watchpoints')
    assert all(phase['optional'] for phase in reg['phases'])
    from scripts.build_kb_wiki import load_entities, build_reverse_refs, render_entity_page
    entities = load_entities(KB)
    refs = build_reverse_refs(entities)
    for eid in [IND, REG]:
        for lang in ['en', 'uk']:
            page = render_entity_page(entities[eid], entities, refs, locale=lang)
            assert 'data-planning-status="withheld"' in page
            assert '5y PFS ~50%' not in page and 'dramatically improves' not in page
