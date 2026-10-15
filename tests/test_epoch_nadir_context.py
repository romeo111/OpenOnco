"""DA-EPOCH monitoring must retain the scheduled-nadir clinical context."""
import json
from pathlib import Path
import pytest
import yaml
from knowledge_base.engine import generate_plan, render_plan_html

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'


@pytest.mark.parametrize('case_id', ['hgbl-double-hit', 'pmbcl-typical', 'burkitt-high-risk'])
def test_actual_epoch_tracks_resolve_their_own_nadir_monitoring(case_id):
    examples = json.loads((ROOT / 'docs/examples.json').read_text(encoding='utf-8'))
    profile = json.loads(json.dumps(next(e['json'] for e in examples if e['case_id'] == case_id)))
    if case_id == 'burkitt-high-risk':
        # The original CNS-positive fixture is withheld by the protocol-scope
        # guard. Monitor verification uses a separate CNS-negative fixture.
        profile['findings']['cns_involvement'] = False
    result = generate_plan(profile, kb_root=KB)
    tracks = [t for t in result.plan.tracks if (t.regimen_data or {}).get('id') == 'REG-DA-EPOCH-R']
    assert tracks
    for track in tracks:
        mon = track.monitoring_data
        assert mon['id'] == 'MON-DA-EPOCH-R-REGIMEN'
        assert mon['linked_to_regimen'] == track.regimen_data['id']
        assert any('twice weekly, three days apart' in p['window'] for p in mon['phases'])
        assert 'SUP-GCSF-NEUTROPENIA' in track.regimen_data['mandatory_supportive_care']
        assert mon['last_reviewed'] is None
        for p in mon['phases']:
            assert len(p['checkpoints']) == len(p['checkpoints_ua'])
    for lang, phrase in [('en', 'During every cycle: CBC twice weekly'), ('uk', 'Під час кожного циклу: загальний аналіз крові двічі на тиждень')]:
        html = render_plan_html(result, target_lang=lang)
        assert phrase in html and 'MON-DA-EPOCH-R-REGIMEN' in html


def test_nadir_context_does_not_reduce_every_drug_after_one_low_anc_or_escalate_missing_data():
    reg = yaml.safe_load((KB / 'regimens/da_epoch_r.yaml').read_text(encoding='utf-8'))
    up, same, down, missing, growth, cns = reg['dose_adjustments']
    assert 'all measurements' in up['condition'] and 'platelet nadir ≥25' in up['condition']
    assert 'one or two' in same['condition'] and 'retain the previous dose level' in same['modification']
    assert 'three or more' in down['condition'] and 'platelet nadir <25' in down['condition']
    assert 'below starting level 1, only cyclophosphamide' in down['modification']
    assert 'before choosing the next level' in missing['modification']
    assert 'not restricted to HIV-positive' in growth['modification']
    assert 'not prescribe a universal' in cns['modification']
    assert 'CALGB 10002' not in reg['notes'] and 'CALGB 10002' not in reg['notes_ua']
    assert reg['last_reviewed'] is None and reg['review_status'] == 'pending_clinical_signoff'


def test_pmbcl_published_efs_is_not_relabelled_as_pfs_or_individual_cure():
    indication = yaml.safe_load((KB / 'indications/ind_pmbcl_1l_da_epoch_r.yaml').read_text(encoding='utf-8'))
    assert 'event-free survival (EFS)' in indication['expected_outcomes']['progression_free_survival']
    assert 'not a verified PFS' in indication['expected_outcomes']['progression_free_survival']
    claim = next(c for c in indication['clinical_claims'] if c['claim_id'] == 'pmbcl-nci-efs-not-pfs')
    assert claim['source_ids'] == ['SRC-DUNLEAVY-PMBCL-DAEPOCH-2013']
    assert '51' in claim['text'] and 'individual probability of cure' in claim['text']
    assert 'not verification of other' in claim['scope']
    assert indication['last_reviewed'] is None
