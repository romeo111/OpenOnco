"""Do not turn pooled lymphoma outcomes into unsupported subtype superiority."""
import json
from pathlib import Path

import pytest
import yaml

from knowledge_base.engine import generate_plan, render_plan_html

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'knowledge_base/hosted/content'
FOLLOWUP = 'SRC-ECHELON-2-FIVE-YEAR-2022'


@pytest.mark.parametrize('filename', ['ind_tcell_1l_chp_bv.yaml', 'ind_aitl_1l_chp_bv.yaml'])
def test_outcome_estimates_have_separate_followup_provenance_without_invented_grading(filename):
    data = yaml.safe_load((KB / 'indications' / filename).read_text(encoding='utf-8'))
    assert data['strength_of_recommendation'] is None and data['nccn_category'] is None
    assert data['last_reviewed'] is None and not data['reviewer_signoffs']
    assert {value['source'] for value in data['expected_outcomes'].values()} == {FOLLOWUP}
    assert all('95% CI' in value['confidence_interval'] for value in data['expected_outcomes'].values())
    assert 'SRC-NCCN-BCELL-2025' not in {source['source_id'] for source in data['sources']}
    assert 'CHOEP' in data['rationale'] and 'CHOEP' in data['rationale_ua']
    assert 'signal favorable' not in json.dumps(data)
    assert 'substantial improvement over CHOP-only era' not in json.dumps(data)


def test_followup_is_not_misattributed_to_original_trial_or_jco():
    source = yaml.safe_load((KB / 'sources/src_echelon2_five_year_2022.yaml').read_text())
    original = yaml.safe_load((KB / 'sources/src_echelon2_horwitz_2019.yaml').read_text())
    assert source['doi'] == '10.1016/j.annonc.2021.12.002'
    assert source['journal'] == 'Annals of Oncology'
    assert original['doi'] != source['doi']
    assert 'Horwitz JCO 2022' not in original['notes']


@pytest.mark.parametrize('case,scope', [('aitl-cd30-positive', 'AITL subgroup'), ('ptcl-cd30-positive', 'pooled ITT cohort')])
@pytest.mark.parametrize('mode', ['clinician', 'patient'])
def test_generated_outputs_preserve_cohort_scope_and_existing_confirmed_route(case, scope, mode):
    rows = json.loads((ROOT / 'docs/examples.json').read_text(encoding='utf-8'))
    profile = next(row['json'] for row in rows if row['case_id'] == case)
    result = generate_plan(profile, kb_root=KB)
    assert result.plan.tracks[0].regimen_data['id'] == 'REG-CHP-BV'
    outcomes = result.plan.tracks[0].indication_data['expected_outcomes']
    assert scope in outcomes['progression_free_survival']['value']
    output = render_plan_html(result, target_lang='en', mode=mode)
    assert 'signal favorable' not in output and 'substantial improvement over CHOP-only era' not in output
    assert FOLLOWUP in output
    assert 'showed superior outcomes vs standard CHOP' not in output


def test_cd30_flag_cannot_claim_eligibility_or_unverified_reimbursement():
    data = yaml.safe_load((KB / 'redflags/rf_tcell_cd30_positive.yaml').read_text(encoding='utf-8'))
    assert 'qualifies' not in data['definition'] and '≥10%' not in data['definition']
    assert 'not НСЗУ-reimbursed' not in data['notes']
    assert 'CHOEP' in data['notes'] and 'CHOEP' in data['notes_ua']
