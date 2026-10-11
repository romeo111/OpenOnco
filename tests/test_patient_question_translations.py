import copy
import re

from knowledge_base.engine._ask_doctor import (
    QUESTION_TEMPLATES, QUESTION_TRANSLATION_STATUS, select_questions,
)


def test_all_question_templates_have_english_drafts_and_originals():
    assert QUESTION_TRANSLATION_STATUS['en'] == 'draft_pending_review'
    assert len(QUESTION_TEMPLATES) == 11
    for question in QUESTION_TEMPLATES:
        assert question['question_ua'].strip()
        assert question['question_en'].strip().endswith('?')
        assert not re.search(r'[\u0400-\u04ff]', question['question_en'])
    family = next(q for q in QUESTION_TEMPLATES if q['id'] == 'family_screening')
    assert '(germline)' in family['question_en']
    assert family['question_en'].startswith('If ')
    dose = next(q for q in QUESTION_TEMPLATES if q['id'] == 'dose_reduction')
    assert dose['question_en'].startswith('Could I ')


def test_translated_questions_keep_selection_and_do_not_mutate_plan():
    plan = {'patient_age': 30, 'plan_tracks': [{}, {}]}
    before = copy.deepcopy(plan)
    selected = select_questions(plan, target_count=11)
    assert [q['id'] for q in selected] == [
        'second_opinion', 'duration', 'side_effects', 'support',
        'fertility', 'second_track',
    ]
    assert all(q['question_en'] and q['question_ua'] for q in selected)
    assert plan == before
