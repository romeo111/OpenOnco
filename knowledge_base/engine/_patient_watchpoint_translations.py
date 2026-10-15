"""Saved English drafts bound to the complete source watchpoint and regimen.

Source changes invalidate both trigger and action. No network, clinical-record
mutation, urgency inference or clinical approval is performed here.
"""
import json
from functools import lru_cache
from hashlib import sha256
from pathlib import Path

TRANSLATION_STATUS = 'draft_pending_clinical_and_language_review'
SOURCE_FIELDS = ('trigger_ua', 'action_ua', 'urgency', 'cycle_day_window', 'sources')


def source_fingerprint(regimen_id, point):
    if not isinstance(point, dict) or set(point) - set(SOURCE_FIELDS):
        return None
    source = {'regimen_id': regimen_id, **{key: point.get(key) for key in SOURCE_FIELDS}}
    try:
        payload = json.dumps(source, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    except (TypeError, ValueError):
        return None
    return sha256(payload.encode('utf-8')).hexdigest()


@lru_cache(maxsize=1)
def _drafts():
    try:
        data = json.loads(Path(__file__).with_name('_patient_watchpoint_en.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict) or data.get('review_status') != TRANSLATION_STATUS:
        return {}
    return data.get('entries', {}) if isinstance(data.get('entries'), dict) else {}


def translate_watchpoint(regimen_id, point, *, target_lang='en'):
    if target_lang != 'en':
        return None
    entry = _drafts().get(source_fingerprint(regimen_id, point))
    if not isinstance(entry, dict):
        return None
    trigger, action = entry.get('trigger_en'), entry.get('action_en')
    if not all(isinstance(text, str) and text.strip() for text in (trigger, action)):
        return None
    return trigger, action
