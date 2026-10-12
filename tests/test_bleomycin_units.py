from pathlib import Path
import re
import yaml
ROOT=Path(__file__).resolve().parents[1]
def read(kind,name):
    return yaml.safe_load((ROOT/'knowledge_base/hosted/content'/kind/name).read_text(encoding='utf-8'))
def test_bleomycin_protocol_units_are_explicit_and_not_generic_international_units():
    bep=read('regimens','reg_bep_gct.yaml')
    abvd=read('regimens','abvd.yaml')
    ind=read('indications','ind_gct_metastatic_1l_bep.yaml')
    drug=read('drugs','bleomycin.yaml')
    assert bep['components'][0]['dose'].startswith('30 USP units')
    assert not re.search(r'\b30 IU\b',bep['components'][0]['dose'])
    assert '400 USP units' in bep['components'][0]['cumulative_dose_limit']
    assert abvd['components'][1]['dose']=='10 USP units/m²'
    assert '30 USP units' in ind['rationale'] and '30 одиниць USP' in ind['rationale_ua']
    assert 'USP' in drug['typical_dosing'] and 'USP' in drug['formulations'][0]
    assert bep['components'][0]['schedule']=='Days 2, 9, 16 of each 21-day cycle (once weekly per cycle)'
    assert bep['cycle_length_days']==21 and abvd['cycle_length_days']==28
    for record in (bep,abvd,ind,drug):
        assert record['last_reviewed'] is None
        assert record['review_status']=='pending_clinical_signoff'
        claim=next(c for c in record['clinical_claims'] if c['claim_id']=='bleomycin-usp-international-unit-convention')
        assert 'SRC-BLEOMYCIN-US-LABEL' in claim['source_ids']
        assert 'not individualized dosing' in claim['scope']
