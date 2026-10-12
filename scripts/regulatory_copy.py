"""Intended-use display copy, without claiming a regulatory determination."""
import json
from functools import lru_cache
from pathlib import Path

INFO = {
    'en': 'Informational support requiring qualified clinician review (CHARTER §11 + §15).',
    'uk': 'Інформаційна підтримка, що потребує перегляду кваліфікованим лікарем (CHARTER §11 + §15).',
    'es': 'Apoyo informativo que requiere revisión por un profesional sanitario cualificado (CHARTER §11 + §15).',
    'pt': 'Apoio informativo que requer revisão por um profissional de saúde qualificado (CHARTER §11 + §15).',
    'de': 'Informationshilfe, die eine Prüfung durch qualifiziertes medizinisches Fachpersonal erfordert (CHARTER §11 + §15).',
    'fr': 'Appui informatif nécessitant une vérification par un professionnel de santé qualifié (CHARTER §11 + §15).',
    'it': 'Supporto informativo che richiede la verifica di un professionista sanitario qualificato (CHARTER §11 + §15).',
    'da': 'Informationsstøtte, der kræver gennemgang af en kvalificeret sundhedsperson (CHARTER §11 + §15).',
    'sv': 'Informationsstöd som kräver granskning av kvalificerad vårdpersonal (CHARTER §11 + §15).',
    'nb': 'Informasjonsstøtte som krever gjennomgang av kvalifisert helsepersonell (CHARTER §11 + §15).',
    'fi': 'Tietotukea, joka edellyttää pätevän terveydenhuollon ammattilaisen arviointia (CHARTER §11 + §15).',
}
LABEL = {
    'en': 'Project intended-use limits (CHARTER §11 + §15):',
    'uk': 'Межі призначення проєкту (CHARTER §11 + §15):',
    'es': 'Límites del uso previsto del proyecto (CHARTER §11 + §15):',
    'pt': 'Limites do uso previsto do projeto (CHARTER §11 + §15):',
    'de': 'Grenzen des vorgesehenen Projektzwecks (CHARTER §11 + §15):',
    'fr': 'Limites de l’usage prévu du projet (CHARTER §11 + §15):',
    'it': 'Limiti dell’uso previsto del progetto (CHARTER §11 + §15):',
    'da': 'Grænser for projektets tilsigtede anvendelse (CHARTER §11 + §15):',
    'sv': 'Gränser för projektets avsedda användning (CHARTER §11 + §15):',
    'nb': 'Grenser for prosjektets tiltenkte bruk (CHARTER §11 + §15):',
    'fi': 'Hankkeen tarkoitetun käytön rajat (CHARTER §11 + §15):',
}
NOTE = {
    'en': 'The Charter records design goals; it does not establish regulatory classification or clinical validation.',
    'uk': 'Хартія описує цілі дизайну, а не встановлює регуляторну класифікацію чи клінічну валідацію.',
    'es': 'La Carta describe objetivos de diseño; no establece una clasificación regulatoria ni una validación clínica.',
    'pt': 'A Carta descreve objetivos de conceção; não estabelece uma classificação regulamentar nem uma validação clínica.',
    'de': 'Die Charta beschreibt Gestaltungsziele; sie begründet weder eine regulatorische Einstufung noch eine klinische Validierung.',
    'fr': 'La Charte décrit des objectifs de conception ; elle ne détermine ni une classification réglementaire ni une validation clinique.',
    'it': 'La Carta descrive obiettivi di progettazione; non stabilisce una classificazione normativa né una validazione clinica.',
    'da': 'Charteret beskriver designmål; det fastslår hverken en regulatorisk klassifikation eller klinisk validering.',
    'sv': 'Stadgan beskriver designmål; den fastställer varken regulatorisk klassificering eller klinisk validering.',
    'nb': 'Charteret beskriver designmål; det fastslår verken regulatorisk klassifisering eller klinisk validering.',
    'fi': 'Peruskirja kuvaa suunnittelutavoitteita; se ei vahvista sääntelyluokitusta eikä kliinistä validointia.',
}


@lru_cache(maxsize=1)
def source_aliases():
    return json.loads((Path(__file__).with_name('locales') / 'intended-use-source-aliases.json').read_text(encoding='utf-8'))


def messages_for(locale):
    footer_keys = (
        'Informational tool for clinicians, not a medical device (CHARTER §15 + §11).',
        'Informational tool, not a medical device (CHARTER §15 + §11).',
        'Information tool for clinicians, not a medical device (CHARTER §15 + §11).',
        'Informational tool for clinicians, requiring qualified clinician review (CHARTER §11 + §15).',
        'Informational tool, requiring qualified clinician review (CHARTER §11 + §15).',
        'Information tool for clinicians, requiring qualified clinician review (CHARTER §11 + §15).',
    )
    result = dict(source_aliases())
    result.update({value: value for value in source_aliases().values()})
    result.update({key: INFO[locale] for key in footer_keys})
    result.update({key: LABEL[locale] for key in (
        'Per FDA non-device CDS positioning (CHARTER §15):',
        'FDA non-device CDS positioning (CHARTER §15):',
        'Відповідно до позиціонування FDA як non-device CDS (CHARTER §15):',
        LABEL['en'], LABEL['uk'],
    )})
    result.update({key: NOTE[locale] for key in (
        'OpenOnco is designed for the §520(o)(1)(E) carve-out — not a medical device. Constraints C1-C7 are hard-enforced.',
        'CHARTER §15 records project design constraints; it does not establish regulatory classification or clinical validation.',
    )})
    return result
