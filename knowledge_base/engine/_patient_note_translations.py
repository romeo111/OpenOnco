"""Patient-note translation drafts bound to the exact authored source text.

Source edits invalidate the translation instead of silently displaying stale copy.
These translations do not change clinical records or prescribing decisions.
"""
from hashlib import sha256
from typing import Optional

TRANSLATION_STATUS = 'draft_pending_clinical_and_language_review'
PATIENT_NOTE_EN_DRAFT = {
    'DRUG-CYTARABINE': (
        '5805465ef03fc073e8b409d91099a8a96581a329c552fb672f168e5b98994765',
        'Chemotherapy that blocks DNA synthesis in tumour cells. A treatment foundation for acute leukaemias; given intravenously or under the skin in courses.',
    ),
    'DRUG-CAPECITABINE': (
        '7e9214a5d51298b0cd301f77cbb53aacea93bfd2e2f022e5321b8f89e6f09451',
        'A prodrug tablet that is converted into 5-FU in the body and blocks tumour DNA synthesis. A convenient form for taking at home. Redness and pain in the palms and soles may occur (hand-foot syndrome).',
    ),
    'DRUG-DOXORUBICIN': (
        'c02ea3ca9726963589532202cf6800a56ff5a36963ce47ba32623bcaeff2eda1',
        'Conventional red-coloured chemotherapy (an anthracycline). Damages tumour-cell DNA and blocks cell division. Given intravenously in combination regimens; it may affect the heart, so echocardiograms are used for monitoring.',
    ),
}


def translate_patient_note(drug_id: str, source: str, *, target_lang: str = 'en') -> Optional[str]:
    if target_lang != 'en' or not isinstance(source, str):
        return None
    entry = PATIENT_NOTE_EN_DRAFT.get(drug_id)
    if not entry or sha256(source.strip().encode('utf-8')).hexdigest() != entry[0]:
        return None
    return entry[1]
