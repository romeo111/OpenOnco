"""Structural input boundaries; no clinical ranges or treatment rules."""
import math


def validate_json_object(value):
    if not isinstance(value, dict):
        raise ValueError('JSON input must be an object.')
    active = set()
    pending = [(value, False)]
    while pending:
        item, leaving = pending.pop()
        if isinstance(item, float) and not math.isfinite(item):
            raise ValueError('JSON input contains a non-finite number.')
        if not isinstance(item, (dict, list, tuple)):
            continue
        identity = id(item)
        if leaving:
            active.remove(identity)
            continue
        if identity in active:
            raise ValueError('JSON input contains a cyclic structure.')
        active.add(identity)
        pending.append((item, True))
        children = item.values() if isinstance(item, dict) else item
        pending.extend((child, False) for child in children)


def validate_patient_profile(patient):
    validate_json_object(patient)
    for section in ('disease', 'demographics', 'findings', 'biomarkers', 'clinician_confirmations'):
        if patient.get(section) is not None and not isinstance(patient[section], dict):
            raise ValueError(f"Patient profile section '{section}' must be an object or null.")
