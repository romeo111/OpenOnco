"""Positive, type-preserving confirmation of authored profile requirements."""
import math


def _matches(value, allowed):
    return any(
        (type(value) is type(expected) and value == expected)
        or (type(value) in (int, float) and type(expected) is int and value == expected)
        for expected in allowed
    )


def unconfirmed_profile_fields(indication, patient):
    applicability = indication.get('applicable_to') or {}
    requirements = applicability.get('confirmed_profile_values') or {}
    missing = []
    for path, allowed in requirements.items():
        value = patient
        for part in path.split('.'):
            value = value.get(part) if isinstance(value, dict) else None
        if not _matches(value, allowed):
            missing.append(path)
        parts = path.split('.')
        if len(parts) == 2 and parts[0] in ('findings', 'disease', 'demographics'):
            for section in ('findings', 'disease', 'demographics'):
                if section == parts[0]:
                    continue
                other = patient.get(section) or {}
                if parts[1] in other and other[parts[1]] is not None and not _matches(other[parts[1]], allowed):
                    missing.append(section + '.' + parts[1])
    if requirements:
        limits = (indication.get('applicable_to') or {}).get('demographic_constraints') or {}
        age = (patient.get('demographics') or {}).get('age')
        if 'age_min' in limits and (type(age) not in (int, float) or (type(age) is float and not math.isfinite(age)) or age < limits['age_min']):
            missing.append('demographics.age')
    for path, excluded in (applicability.get('excluded_profile_values') or {}).items():
        parts = path.split('.')
        paths = [path]
        if len(parts) == 2 and parts[0] in ('findings', 'disease', 'demographics'):
            paths = [section + '.' + parts[1] for section in ('findings', 'disease', 'demographics')]
        for candidate in paths:
            value = patient
            for part in candidate.split('.'):
                value = value.get(part) if isinstance(value, dict) else None
            malformed_boolean = value is not None and all(type(item) is bool for item in excluded) and type(value) is not bool
            if _matches(value, excluded) or malformed_boolean:
                missing.append(candidate)
    return missing
