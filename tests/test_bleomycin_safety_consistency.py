from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
def read(kind,name):
    return yaml.safe_load((ROOT/'knowledge_base/hosted/content'/kind/name).read_text(encoding='utf-8'))
def test_drug_oxygen_warning_preserves_oxygenation_and_does_not_impose_lifetime_ban():
    drug=read('drugs','bleomycin.yaml')
    assert 'Avoid high-flow O2' not in drug['notes']
    assert 'adequate oxygenation' in drug['notes']
    assert 'індивідуальної оцінки та достатньої оксигенації' in drug['notes_ua']
    claim=next(c for c in drug['clinical_claims'] if c['claim_id']=='bleomycin-individualized-perioperative-oxygen')
    assert 'SRC-AAKRE-BLEOMYCIN-PERIOPERATIVE-2014' in claim['source_ids']
    assert 'do not prove absence' in claim['scope']
def test_growth_factor_statements_are_contextual_and_fever_escalation_is_retained():
    drug=read('drugs','bleomycin.yaml');abvd=read('regimens','abvd.yaml')
    assert 'G-CSF: increases pulmonary toxicity (avoid in ABVD)' not in drug['major_interactions']
    assert 'not demonstrated increased pulmonary complications' in drug['major_interactions'][1]
    assert 'may be considered' in drug['notes'] and 'monitoring' in abvd['notes']
    assert 'Г-КСФ протипоказаний' not in abvd['notes_ua']
    assert 'не потрібний рутинно' in abvd['notes_ua']
    warning=next(w for w in abvd['between_visit_watchpoints'] if w['trigger_ua']=='Лихоманка вище 38°C')
    assert warning['urgency']=='call_clinic_same_day'
    assert 'Подзвоніть у клініку того ж дня' in warning['action_ua']
    assert 'не призначається' not in warning['action_ua']
    assert 'SRC-EVIQ-ABVD-56' in warning['sources']
    for record in (drug,abvd):
        assert record['last_reviewed'] is None
        assert record['review_status']=='pending_clinical_signoff'
        claim=next(c for c in record['clinical_claims'] if c['claim_id']=='abvd-growth-factor-not-routine-not-prohibited')
        assert claim['source_ids']==['SRC-EVIQ-ABVD-56','SRC-BLEOMYCIN-US-LABEL']
