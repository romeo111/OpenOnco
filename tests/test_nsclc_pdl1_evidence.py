"""Keep combination eligibility distinct from monotherapy PD-L1 thresholds."""
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_pdl1_combination_record_matches_primary_evidence_without_claiming_signoff():
    record = yaml.safe_load((ROOT / 'knowledge_base/hosted/content/biomarker_actionability/bma_pdl1_tps_nsclc.yaml').read_text(encoding='utf-8'))
    combinations = record['recommended_combinations']
    assert 'TPS≥50%' in combinations[0]  # Monotherapy remains a separate route.
    for combination in combinations[1:]:
        assert 'regardless of TPS' in combination
        assert 'TPS≥1%' not in combination
    assert 'non-sq' in combinations[1] and 'EGFR/ALK' in combinations[1]
    assert 'sq 1L' in combinations[2]
    assert 'either paclitaxel or nab-paclitaxel' in combinations[2]
    for key in ('evidence_summary', 'evidence_summary_ua'):
        assert 'TPS <1%' in record[key]
        assert 'KEYNOTE-189' in record[key] and 'KEYNOTE-407' in record[key]
    assert all('regardless of TPS' in x for x in record['regulatory_approval']['ema'][1:])
    assert record['last_verified'] == '2026-05-07'
    assert record['review_status'] == 'pending_clinical_signoff'
    assert record['actionability_review_required'] is True
    audit = json.loads((ROOT / 'docs/audits/nsclc_pdl1_combination_2026-10-12.json').read_text(encoding='utf-8'))
    assert audit['clinical_signoff'] is False
    assert len(audit['observations']) == 4
