"""Published forms must have one control per profile path, preserving authored values."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re
import yaml

from scripts.build_site import _COMMON_SCREENING_GROUP, _inject_common_screening, bundle_questionnaires


def test_common_screening_preserves_authored_hiv_options_and_bilirubin_defaults():
    hiv = {'field': 'findings.hiv_status', 'type': 'enum', 'options': [
        {'value': 'positive_controlled', 'label': 'Positive, on ART'},
        {'value': 'positive_uncontrolled', 'label': 'Positive, uncontrolled'},
    ], 'default_value': 'negative', 'impact': 'critical'}
    bilirubin = {'field': 'findings.bilirubin_uln_x', 'type': 'float', 'default_value': 1, 'range_max': 30}
    quest = {'groups': [{'title': 'Authored screening', 'questions': [hiv, bilirubin]}]}
    original = deepcopy(quest)
    enriched = _inject_common_screening(quest)
    questions = [q for group in enriched['groups'] for q in group['questions']]
    assert [q for q in questions if q['field'] == hiv['field']] == [hiv]
    assert [q for q in questions if q['field'] == bilirubin['field']] == [bilirubin]
    assert len(questions) > 2
    assert quest == original


def test_screening_injection_is_idempotent_and_does_not_mutate_shared_template():
    template = deepcopy(_COMMON_SCREENING_GROUP)
    first = _inject_common_screening({'groups': [{'title': 'Custom', 'questions': [template['questions'][0]]}]})
    assert _inject_common_screening(first) == first
    second = _inject_common_screening({'groups': []})
    assert second['groups'][0] == template
    assert _COMMON_SCREENING_GROUP == template


def test_all_bundled_questionnaires_have_unique_profile_paths_and_control_ids(tmp_path):
    result = bundle_questionnaires(tmp_path)
    questionnaires = json.loads((tmp_path / result['path']).read_text(encoding='utf-8'))
    assert result['count'] == len(questionnaires)
    repository = Path(__file__).resolve().parents[1]
    authored = [yaml.safe_load(path.read_text(encoding='utf-8')) for path in
                (repository / 'knowledge_base/hosted/content/questionnaires').glob('*.yaml')]
    by_id = {questionnaire['id']: questionnaire for questionnaire in questionnaires}
    assert set(by_id) == {questionnaire['id'] for questionnaire in authored}
    for questionnaire in authored:
        published_questions = {q['field']: q for group in by_id[questionnaire['id']]['groups'] for q in group['questions']}
        for group in questionnaire.get('groups') or []:
            for question in group.get('questions') or []:
                assert published_questions[question['field']] == question, (questionnaire['id'], question['field'])
    for questionnaire in questionnaires:
        fields = [q['field'] for group in questionnaire['groups'] for q in group['questions']]
        assert all(count == 1 for count in Counter(fields).values()), questionnaire['id']
        control_ids = ['fld-' + re.sub('[^A-Za-z0-9]', '_', field) for field in fields]
        assert len(control_ids) == len(set(control_ids)), questionnaire['id']
    source = Path(__file__).resolve().parents[1] / 'docs/questionnaires.json'
    if source.exists():
        published = json.loads(source.read_text(encoding='utf-8'))
        assert {q['id'] for q in published} == {q['id'] for q in questionnaires}
