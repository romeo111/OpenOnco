"""Pulmonary warnings must preserve indication and measurement context."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def record(kind, name):
    return yaml.safe_load((ROOT / 'knowledge_base/hosted/content' / kind / name).read_text(encoding='utf-8'))


def test_pulmonary_risk_is_not_an_universal_numeric_contraindication():
    drug = record('drugs', 'bleomycin.yaml')
    assert all('DLCO' not in item for item in drug['absolute_contraindications'])
    assert 'Hypersensitivity' in drug['absolute_contraindications']
    assert any('brentuximab' in item for item in drug['absolute_contraindications'])
    assert 'extreme caution' in drug['notes']
    assert 'особливої обережності' in drug['notes_ua']
    for entry in [drug, record('regimens', 'abvd.yaml')]:
        claim = next(c for c in entry['clinical_claims'] if c['claim_id'] == 'chl-bleomycin-pulmonary-assessment-context')
        assert 'pretreatment value' in claim['text'] and 'not percent predicted' in claim['text']
        assert 'not germ-cell' in claim['scope']
        assert claim['source_ids'] == ['SRC-BSH-CHL-BLEOMYCIN-2025', 'SRC-EVIQ-ABVD-56']
        assert entry['last_reviewed'] is None


def test_abvd_does_not_permanently_stop_on_an_isolated_decline_or_risk_marker():
    abvd = record('regimens', 'abvd.yaml')
    lung, exposure = abvd['dose_adjustments'][:2]
    assert 'DLCO drop ≥25%' not in lung['condition']
    assert 'withhold bleomycin' in lung['modification']
    assert 'Stop bleomycin if pulmonary toxicity is established' in lung['modification']
    assert 'infection and pulmonary embolism' in lung['modification']
    assert '400 USP units (400000 International Units)' in exposure['modification']
    assert 'not an automatic universal stopping dose' in exposure['modification']
    assert abvd['dose_adjustments'][2] == {'condition': 'Cumulative anthracycline >300 mg/m²', 'modification': 'Echo + LVEF check'}
    assert 'no routine repeated PFTs' in abvd['notes']
    assert 'без рутинного повторення PFT' in abvd['notes_ua']
    symptom = next(w for w in abvd['between_visit_watchpoints'] if 'Новий сухий кашель' in w['trigger_ua'])
    assert symptom['urgency'] == 'call_clinic_same_day'
