"""Positive confirmation of explicitly authored histology applicability."""
import re


def _key(value):
    return re.sub(r'[-_\s]+', ' ', value.strip().casefold())


def histology_confirmed(indication, patient):
    allowed = (indication.get('applicable_to') or {}).get('histology_allowed_values') or []
    if not allowed:
        return True
    expected = {_key(value) for value in allowed}
    values = [(patient.get(section) or {}).get('histology') for section in ('disease', 'findings')]
    supplied = [value for value in values if value is not None]
    return bool(supplied) and all(isinstance(value, str) and _key(value) in expected for value in supplied)
