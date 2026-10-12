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
    oxygen_claim = next(claim for claim in data['clinical_claims'] if claim['claim_id'] == 'bleomycin-perioperative-oxygen')
    assert 'other BEP dosing' in oxygen_claim['scope']
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


def test_bep_supportive_care_is_individualized_and_does_not_guarantee_pulmonary_safety():
    reg = yaml.safe_load((ROOT / 'knowledge_base/hosted/content/regimens/reg_bep_gct.yaml').read_text(encoding='utf-8'))
    ind = yaml.safe_load((ROOT / 'knowledge_base/hosted/content/indications/ind_gct_metastatic_1l_bep.yaml').read_text(encoding='utf-8'))
    assert 'not universally required' in reg['premedication'][2]
    assert "обов'язкова" not in reg['notes_ua'].split('G-КСФ', 1)[1].split('Кумулятивна', 1)[0]
    assert 'does not guarantee prevention' in ind['rationale']
    assert 'HRCT' in reg['monitoring'][0]
    assert 'not an automatic permanent-discontinuation' in reg['components'][0]['dose_modifications'][0]['action']
    assert 'допоміжними' in reg['notes_ua']
    for record in (reg, ind):
        claims = {claim['claim_id']: claim for claim in record['clinical_claims']}
        assert claims['bep-individualized-gcsf']['source_ids'] == ['SRC-EVIQ-TESTICULAR-BEP-320']
        assert claims['bleomycin-pulmonary-assessment']['source_ids'] == ['SRC-BLEOMYCIN-UK-BEST-PRACTICE-2018']
        assert record['review_status'] == 'pending_clinical_signoff'
        assert record['last_reviewed'] is None
    assert [(component['drug_id'], component['schedule']) for component in reg['components']] == [
        ('DRUG-BLEOMYCIN', 'Days 2, 9, 16 of each 21-day cycle (once weekly per cycle)'),
        ('DRUG-ETOPOSIDE', 'Days 1-5 of each 21-day cycle'),
        ('DRUG-CISPLATIN', 'Days 1-5 of each 21-day cycle (total 100 mg/m² per cycle)'),
    ]
    assert reg['cycle_length_days'] == 21


def test_scoped_wiki_evidence_is_visible_escaped_and_does_not_change_record_wide_sources():
    from types import SimpleNamespace
    from scripts.build_kb_wiki import _scoped_claim_sections, _source_ids
    source = SimpleNamespace(title='Official evidence', data={'url': 'https://example.org/evidence'})
    entity = SimpleNamespace(data={'clinical_claims': [{'text': 'Suspected toxicity: HRCT <assessment>', 'scope': 'Pulmonary assessment only', 'source_locator': 'Symptom monitoring', 'source_ids': ['SRC-TEST']} ]})
    before = yaml.safe_dump(entity.data)
    output = _scoped_claim_sections(entity, {'SRC-TEST': source})
    assert 'HRCT &lt;assessment&gt;' in output
    assert 'href="https://example.org/evidence"' in output
    assert 'Pulmonary assessment only' in output
    assert 'do not establish clinical approval' in output
    assert _source_ids(entity.data) == []
    assert yaml.safe_dump(entity.data) == before
    assert 'Докази для окремих тверджень' in _scoped_claim_sections(entity, {'SRC-TEST': source}, locale='uk')
    assert _scoped_claim_sections(SimpleNamespace(data={}), {}) == ''


def test_scoped_claim_terms_are_searchable_without_becoming_record_wide_sources():
    from types import SimpleNamespace
    from scripts.build_kb_wiki import _search_entry
    entity = SimpleNamespace(id='REG-TEST', url='kb/regimens/reg-test.html', title='Synthetic regimen', kind='regimens', kind_label='Regimen', data={'review_status': 'pending_clinical_signoff', 'clinical_claims': [{'text': 'HRCT assessment', 'scope': 'Symptoms only', 'source_ids': ['SRC-TEST']} ]})
    row = _search_entry(entity, {})
    assert 'hrct assessment' in row['search_text']
    assert 'symptoms only' in row['search_text']
    assert 'src-test' in row['search_text']
    assert row['sources'] == []


def test_bep_kidney_actions_do_not_prescribe_unverified_reduction_or_substitution():
    reg_path = 'knowledge_base/hosted/content/regimens/reg_bep_gct.yaml'
    current = yaml.safe_load((ROOT / reg_path).read_text(encoding='utf-8'))
    renal_bleomycin = current['components'][0]['dose_modifications'][2]['action']
    cisplatin_rules = current['components'][2]['dose_modifications']
    assert 'EP still contains cisplatin' in renal_bleomycin
    assert 'universal 15 mg/m²/day rule' in cisplatin_rules[0]['action']
    assert 'Do not automatically substitute' in cisplatin_rules[1]['action']
    assert 'slightly less effective' not in cisplatin_rules[1]['action']
    assert current['last_reviewed'] is None
    assert current['review_status'] == 'pending_clinical_signoff'
    claims = {claim['claim_id']: claim for claim in current['clinical_claims']}
    assert claims['bep-kidney-specialist-assessment']['source_ids'] == ['SRC-EVIQ-TESTICULAR-BEP-320']
    assert 'severe kidney impairment' in claims['metastatic-nonseminoma-carboplatin-not-equivalent']['scope']
