from pathlib import Path
import yaml

from knowledge_base.engine._claim_extraction import extract_claims

ROOT = Path(__file__).resolve().parents[1]


def test_bep_does_not_impose_an_absolute_oxygen_ceiling():
    data = yaml.safe_load((ROOT / 'knowledge_base/hosted/content/regimens/reg_bep_gct.yaml').read_text(encoding='utf-8'))
    raw = (ROOT / 'knowledge_base/hosted/content/regimens/reg_bep_gct.yaml').read_text(encoding='utf-8')
    assert 'MUST limit FiO₂ <30%' not in raw
    assert 'НІКОЛИ не давати FiO₂ >30%' not in raw
    assert 'FiO2 строго <30%' not in raw
    assert 'adequate oxygenation' in raw
    assert 'достатньої оксигенації' in raw
    assert data['review_status'] == 'pending_clinical_signoff'
    assert data['last_reviewed'] is None
    assert len(data['clinical_claims']) == 1
    assert 'other BEP dosing' in data['clinical_claims'][0]['scope']
    indication = yaml.safe_load((ROOT / 'knowledge_base/hosted/content/indications/ind_gct_metastatic_1l_bep.yaml').read_text(encoding='utf-8'))
    assert 'adequate oxygenation' in indication['do_not_do_en'][0]
    assert all('НІКОЛИ не давати FiO₂' not in line for line in indication['do_not_do'])
    assert 'must limit FiO₂ <30%' not in indication['rationale']


def test_scoped_oxygen_citations_do_not_approve_unrelated_regimen_prose():
    source_id = 'SRC-OXYGEN'
    entities = {
        source_id: {'type': 'sources', 'data': {'id': source_id}},
        'REG-TEST': {'type': 'regimens', 'data': {
            'id': 'REG-TEST', 'notes_ua': 'Unrelated dose statement requiring its own support.',
            'clinical_claims': [{'claim_id': 'oxygen', 'text': 'Scoped oxygen claim.', 'source_ids': [source_id]}],
        }},
    }
    claims = {claim.field: claim for claim in extract_claims(entities)}
    assert claims['clinical_claims[oxygen]'].has_anchor
    assert not claims['notes_ua'].has_anchor
    assert claims['notes_ua'].cited_sources == []
