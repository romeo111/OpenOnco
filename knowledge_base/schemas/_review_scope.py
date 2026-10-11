"""Shared reviewer-scope checks; unknown scope cannot confer approval."""
from typing import Any, Mapping

_TYPE_ALIASES = {
    'indication': 'Indication', 'indications': 'Indication',
    'algorithm': 'Algorithm', 'algorithms': 'Algorithm',
    'regimen': 'Regimen', 'regimens': 'Regimen',
    'redflag': 'RedFlag', 'redflags': 'RedFlag',
    'biomarkeractionability': 'BiomarkerActionability',
}
_HEME_TOKENS = (
    'DLBCL', 'FL', 'CLL', 'AML', 'APL', 'MM', 'MCL', 'CHL', 'NLPBL',
    'ALCL', 'AITL', 'PTCL', 'ATLL', 'B-ALL', 'T-ALL', 'PMBCL', 'PCNSL',
    'BURKITT', 'HCL', 'MZL', 'SMZL', 'NMZL', 'WM', 'MF', 'SEZARY',
    'ET', 'MDS', 'CML', 'MPN', 'ADVSM', 'HGBL', 'TFL', 'PTLD',
    'RICHTER', 'PV', 'PMF',
)
_SOLID_TOKENS = (
    'BRCA', 'CRC', 'NSCLC', 'SCLC', 'LUNG', 'PROSTATE', 'BLADDER',
    'OVARIAN', 'ENDOMETRIAL', 'CERVICAL', 'GASTRIC', 'ESOPH', 'PANC',
    'HCC', 'CHOLANGIO', 'MELANOMA', 'HNSCC', 'MTC', 'GIST', 'SARCOMA',
    'RENAL', 'GLIOMA', 'MENINGIOMA', 'TESTICULAR', 'BREAST',
    'CHONDROSARCOMA', 'OSTEOSARCOMA',
)


def canonical_entity_type(value: Any) -> str | None:
    return _TYPE_ALIASES.get(str(value).lower().replace('_', ''))


def entity_disease_ids(data: Mapping[str, Any], entity_type: str) -> list[str | None]:
    """Resolve all declared disease contexts instead of approving the first only."""
    kind = canonical_entity_type(entity_type)
    if kind == 'Indication':
        applicable = data.get('applicable_to')
        return [applicable.get('disease_id') if isinstance(applicable, Mapping) else None]
    if kind == 'Algorithm':
        return [data.get('applicable_to_disease')]
    if kind == 'BiomarkerActionability':
        return [data.get('disease_id')]
    if kind == 'RedFlag':
        diseases = data.get('relevant_diseases')
        if isinstance(diseases, list) and diseases and '*' not in diseases:
            return diseases
    return [None]


def infer_review_categories(disease_id: str | None, disease_lineage: str | None) -> set[str]:
    """Retain legacy broad scope tags and add the exact disease identifier tag.

    These tags only restrict declared reviewer authority, never select therapy.
    Explicit disease allow-lists remain available when a category is ambiguous.
    """
    tags: set[str] = set()
    lin = (disease_lineage or '').lower().replace('-', '_').replace(' ', '_')
    did = (disease_id or '').upper().removeprefix('DIS-')
    if did:
        tags.add(did.lower().replace('-', '_'))
    if lin.startswith(('b_cell', 't_cell', 'myeloid', 'plasma_cell', 'lymphoid', 'nk_cell', 'histiocytic')):
        tags.add('hematologic')
        if 'lymph' in lin or 'b_cell' in lin or 't_cell' in lin:
            tags.add('lymphoid')
        if 'myeloid' in lin:
            tags.add('myeloid')
        if 'plasma' in lin:
            tags.add('plasma-cell')
    for token in _HEME_TOKENS:
        if token in did.split('-'):
            tags.add('hematologic')
            tags.add('myeloid' if token in ('AML', 'APL', 'MDS', 'CML', 'MPN', 'PV', 'PMF', 'ET')
                     else 'plasma-cell' if token in ('MM', 'WM') else 'lymphoid')
            break
    for token in _SOLID_TOKENS:
        if token not in did:
            continue
        tags.add('solid')
        if token in ('CRC', 'GASTRIC', 'ESOPH', 'PANC', 'HCC', 'CHOLANGIO', 'GIST'):
            tags.add('gastrointestinal')
        elif token in ('BREAST', 'BRCA'):
            tags.add('breast')
        elif token in ('PROSTATE', 'BLADDER', 'TESTICULAR', 'RENAL'):
            tags.add('gu')
        elif token in ('OVARIAN', 'ENDOMETRIAL', 'CERVICAL'):
            tags.add('gyn')
        elif token in ('NSCLC', 'SCLC', 'LUNG'):
            tags.add('thoracic')
        elif token in ('GLIOMA', 'MENINGIOMA'):
            tags.add('cns')
        elif token in ('HNSCC', 'MTC'):
            tags.add('hnscc')
        elif 'SARCOMA' in token:
            tags.add('sarcoma')
        elif token == 'MELANOMA':
            tags.add('melanoma')
        break
    return tags


def reviewer_scope_matches(scope: Any, entity_type: str, disease_id: str | None,
                           disease_lineage: str | None = None) -> tuple[bool, str]:
    if not isinstance(scope, Mapping):
        return False, 'reviewer scope is absent'
    canonical = canonical_entity_type(entity_type)
    declared_types = scope.get('entity_types')
    if canonical is None or not isinstance(declared_types, list) or canonical not in {
        canonical_entity_type(value) for value in declared_types
    }:
        return False, f'reviewer scope excludes entity_type {entity_type!r}'
    explicit = scope.get('diseases_explicit') or []
    if explicit:
        match = isinstance(explicit, list) and bool(disease_id) and disease_id in explicit
        return bool(match), 'explicit disease allow-list match' if match else 'disease not on explicit allow-list'
    categories = scope.get('disease_categories')
    if not isinstance(categories, list) or not categories:
        return False, 'reviewer disease scope is absent'
    if canonical in {'Indication', 'Algorithm', 'BiomarkerActionability'} and not disease_id:
        return False, 'entity disease context is absent'
    if 'all' in categories:
        return True, 'explicit all-category scope'
    inferred = infer_review_categories(disease_id, disease_lineage)
    match = bool(inferred.intersection(categories))
    return match, 'disease category match' if match else 'entity disease category is outside reviewer scope'
