"""Draft acceptance invariants. These do not replace clinical translation review."""
import re
from functools import lru_cache
from pathlib import Path

import yaml

from scripts.site_translation_catalog import numeric_tokens, polarity_tokens, quantity_tokens
from scripts.clinical_curated_copy import AVAILABILITY_LABELS, STAGING_LABELS, diagnostic_display

IDENTIFIERS = re.compile(
    r'\b(?:SRC|DIS|BIO|DRUG|REG|ALGO|RF|IND|HQ|HB|PLAN|TEST|SUP|WORKUP|OQ|CI|CC|BMA|COVERAGE|VERIFIED|KEYNOTE|FIGHT|LIBRETTO)-[A-Z0-9_-]+\b'
)
STRUCTURED_TOKENS = re.compile(r'\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+\b|\b(?:findings|clinician_confirmations)\.[A-Za-z0-9_.-]+\b')
SYMBOLS = re.compile(r'\b(?:ALK|BRAF|BRCA1|BRCA2|CD19|CD20|CD22|CD30|CD33|CD38|CD52|CD79B|EGFR|ERBB2|ESR1|FGFR1|FGFR2|FGFR3|FLT3|HER2|HRD|IDH1|IDH2|JAK2|KIT|KRAS|MET|MSI|NPM1|NRAS|NTRK1|NTRK2|NTRK3|PD-L1|PIK3CA|RET|ROS1|TP53|TMB)(?:-[A-Z0-9]+)?\b')
VARIANTS = re.compile(r'\b(?:p\.)?[A-Z]\d{1,5}[A-Z*]\b')
ABBREVIATIONS = re.compile(r'\b(?:OpenOnco|CIViC|[Hh]edgehog|MYC|BCL2|BCL6|ATM|CHEK2|PALB2|PTEN|ESMO|NCCN|FDA|EMA|WHO|ESCAT|TKI|PARPi|IHC|ISH|TNM|ECOG|BID|TID|QD|PO|IV|SC|NSCLC|SCLC|AML|ALL|APL|CLL|CML|DLBCL|HRR|PDAC|GIST|[BT](?=-[Cc]ell))\b')
STATES = re.compile(r'\b[A-Za-z][A-Za-z0-9]*(?:/[A-Za-z0-9]+)*[+-](?!\w)')
RISK_SYSTEMS = re.compile(r'\b(?:ELN|IPSS-R|IPSS-M|IPSS|IPI|AAIPI|R-ISS|ISS|IGCCCG|IMDC|INRG|INSS|AJCC|FIGO|BCLC)\b', re.I)
TRIAL_NAMES = re.compile(r'\b(?:SUNLIGHT|MOUNTAINEER)\b')
STAGING_SOURCE = re.compile(r'\bstaging\b', re.I)
STAGING_MISTRANSLATIONS = {
    'it': re.compile(r'\b(?:stagione|messa in scena)\b', re.I),
    'da': re.compile(r'\b(?:igangsættelse|iscenesættelse)\b', re.I),
    'sv': re.compile(r'\biscensättning\b', re.I),
    'nb': re.compile(r'\b(?:igangsetting|iscenesettelse)\b', re.I),
    'fi': re.compile(r'\b(?:lavastus|paikannus)\b', re.I),
}


def staging_fidelity(source, translated, locale):
    if source == translated:
        return True
    labels = STAGING_LABELS.get(locale, {})
    if source in labels:
        return translated == labels[source]
    bad = STAGING_MISTRANSLATIONS.get(locale)
    if bad and STAGING_SOURCE.search(source) and bad.search(translated):
        return False
    if locale == 'da' and re.search(r'\bstage\b', source, re.I) and re.search(r'\betage\b', translated, re.I):
        return False
    return True
DAILY_EN = re.compile(r'\b(?:once daily|every day|daily)\b', re.I)
WEEKLY_EN = re.compile(r'\b(?:once weekly|every week|weekly)\b', re.I)
WEEKLY_TRANSLATION = {
    'es': re.compile(r'\b(?:una|1)\s+vez\s+por\s+semana\b|\bsemanal(?:mente)?\b', re.I),
    'pt': re.compile(r'\b(?:uma|1)\s+vez\s+por\s+semana\b|\bsemanal(?:mente)?\b', re.I),
    'de': re.compile(r'\bwöchentlich\b|\beinmal\s+pro\s+woche\b', re.I),
    'fr': re.compile(r'\b(?:une|1)\s+(?:seule\s+)?fois\s+par\s+semaine\b|\bhebdomadaire\b', re.I),
    'it': re.compile(r'\b(?:settimana|settimanale|settimanalmente)\b', re.I),
    'da': re.compile(r'\b(?:ugentlig\w*|hver uge)\b', re.I),
    'sv': re.compile(r'\b(?:veckovis|varje vecka|en gång i veckan)\b', re.I),
    'nb': re.compile(r'\b(?:ukentlig\w*|hver uke)\b', re.I),
    'fi': re.compile(r'\b(?:viikoittain|kerran viikossa|joka viikko)\b', re.I),
}
ADDITIONAL_DAILY_TRANSLATION = {
    'it': re.compile(r'\b(?:ogni giorno|al giorno|quotidianamente|giornalier\w*)\b', re.I),
    'da': re.compile(r'\b(?:daglig\w*|hver dag)\b', re.I),
    'sv': re.compile(r'\b(?:daglig\w*|varje dag)\b', re.I),
    'nb': re.compile(r'\b(?:daglig\w*|hver dag)\b', re.I),
    'fi': re.compile(r'\b(?:päivittäin|kerran päivässä|joka päivä)\b', re.I),
}
ALTERNATE_INJECTION_SITE = re.compile(r'\bAlternate (?:flanks/buttocks|sides|injection sites)\b', re.I)
ALTERNATION_TRANSLATION = {
    'es': re.compile(r'\baltern\w*\b', re.I),
    'pt': re.compile(r'\baltern\w*\b', re.I),
    'de': re.compile(r'\bwechsel\w*\b', re.I),
    'fr': re.compile(r'\baltern\w*\b', re.I),
}
# A translated sentence must retain explicit safety and treatment-duration
# clauses. These narrow source triggers avoid inferring clinical meaning from
# general sentence length, which differs substantially by language.
CRITICAL_CLAUSES = (
    (re.compile(r'Active bleeding is an absolute hold on systemic therapy until controlled', re.I), {
        'es': re.compile(r'\b(?:suspend|deten|interrump|aplaz|contraindic)\w*\b', re.I),
        'pt': re.compile(r'\b(?:suspend|interromp|adi|contraindic)\w*\b', re.I),
        'de': re.compile(r'\b(?:halt|stopp|unterbrech|aussetz)\w*\b', re.I),
        'fr': re.compile(r'\b(?:arrêt|suspend|interromp|contre.indic)\w*\b', re.I),
    }),
    (re.compile(r'Triggers carbo-mono OR weekly-dose-dense-pacli', re.I), {
        locale: re.compile(r'(?=.*carbo.mono)(?=.*pacli)(?=.*' + weekly + r')', re.I | re.S)
        for locale, weekly in {
            'es': r'semanal|weekly', 'pt': r'semanal|weekly',
            'de': r'wöch|weekly', 'fr': r'hebdomadaire|weekly',
        }.items()
    }),
    (re.compile(r'Continuous until progression or unacceptable toxicity', re.I), {
        'es': re.compile(r'progresi[oó]n.{0,50}toxicidad|toxicidad.{0,50}progresi[oó]n', re.I),
        'pt': re.compile(r'progress[aã]o.{0,50}toxicidade|toxicidade.{0,50}progress[aã]o', re.I),
        'de': re.compile(r'(?:progression|fortschreit\w*).{0,50}toxizit[aä]t|toxizit[aä]t.{0,50}(?:progression|fortschreit\w*)', re.I),
        'fr': re.compile(r'progression.{0,50}toxicit[eé]|toxicit[eé].{0,50}progression', re.I),
    }),
    (re.compile(r'Cornerstone of every APL induction regimen', re.I), {
        'es': re.compile(r'induc\w*', re.I),
        'pt': re.compile(r'indu[cç][aã]o', re.I),
        'de': re.compile(r'induktion', re.I),
        'fr': re.compile(r'induction', re.I),
    }),
    (re.compile(r'Edema dominant AE', re.I), {
        locale: re.compile(r'\b(?:edema|[oö]dem|œd[eè]me)\b', re.I)
        for locale in ('es', 'pt', 'de', 'fr')
    }),
)


@lru_cache(maxsize=1)
def registered_gene_symbols():
    """Protect canonical symbols declared by the current source records."""
    symbols = set()
    root = Path(__file__).resolve().parents[1] / 'knowledge_base/hosted/content/biomarkers'
    for path in root.glob('*.yaml'):
        record = yaml.safe_load(path.read_text(encoding='utf-8'))
        for section, field in [('mutation_details', 'gene'), ('actionability_lookup', 'gene'), ('external_ids', 'hgnc_symbol')]:
            value = (record.get(section) or {}).get(field)
            if isinstance(value, str) and re.fullmatch(r'[A-Z][A-Z0-9-]{1,20}', value):
                symbols.add(value)
    return re.compile(r'\b(?:' + '|'.join(re.escape(value) for value in sorted(symbols, key=len, reverse=True)) + r')\b') if symbols else None


def acceptable_draft(source, translated, locale, drug_pattern=None):
    if source == translated:
        return True  # Explicit original retained, not a translated clinical claim.
    if not staging_fidelity(source, translated, locale):
        return False
    if source == '✗ Not registered in UA' and translated == AVAILABILITY_LABELS.get(locale):
        return True  # Exact curated country and negation; no arbitrary exemption.
    if diagnostic_display(source, locale) == translated:
        return True  # Exact technical list: the code suffix is identical.
    if not translated or numeric_tokens(source) != numeric_tokens(translated):
        return False
    if quantity_tokens(source) != quantity_tokens(translated):
        return False
    # Numbers alone cannot distinguish a daily dose from a weekly dose.
    # Likewise, an injection-site rotation instruction must not disappear.
    weekly_form = WEEKLY_TRANSLATION.get(locale)
    if DAILY_EN.search(source) and not WEEKLY_EN.search(source):
        if weekly_form is None or weekly_form.search(translated):
            return False
        daily_form = ADDITIONAL_DAILY_TRANSLATION.get(locale)
        if daily_form is not None and not daily_form.search(translated):
            return False
    if locale in ADDITIONAL_DAILY_TRANSLATION and WEEKLY_EN.search(source):
        if weekly_form is None or not weekly_form.search(translated):
            return False
    alternation_form = ALTERNATION_TRANSLATION.get(locale)
    if ALTERNATE_INJECTION_SITE.search(source) and (alternation_form is None or not alternation_form.search(translated)):
        return False
    # Unmapped critical clinical clauses retain their complete original text.
    if any(source_pattern.search(source) and (locale not in translations or not translations[locale].search(translated))
           for source_pattern, translations in CRITICAL_CLAUSES):
        return False
    # Alternatives and machine-readable identifiers cannot be silently
    # collapsed into a shorter, seemingly fluent clinical statement.
    if source.count('|') > translated.count('|'):
        return False
    if source.startswith(r'\b') or (re.fullmatch(r'[A-Za-z0-9_./-]+', source) and sum(source.count(mark) for mark in '-_.') >= 2):
        return False
    if any(identifier not in translated for identifier in IDENTIFIERS.findall(source)):
        return False
    if any(token not in translated for token in STRUCTURED_TOKENS.findall(source)):
        return False
    if any(symbol.casefold() not in translated.casefold() for symbol in SYMBOLS.findall(source)):
        return False
    # Each occurrence matters: a correct MSI-H later in a paragraph must not
    # hide an earlier MSI/MMR mistranslated as IMS/RMR.
    for symbol in set(SYMBOLS.findall(source)):
        pattern = r'(?<!\w)' + re.escape(symbol) + r'(?!\w)'
        if len(re.findall(pattern, source, re.I)) != len(re.findall(pattern, translated, re.I)):
            return False
    if any(variant.casefold() not in translated.casefold() for variant in VARIANTS.findall(source)):
        return False
    if any(not re.search(r'(?<!\w)' + re.escape(token) + r'(?!\w)', translated, re.I) for token in ABBREVIATIONS.findall(source)):
        return False
    if any(not re.search(r'\b' + re.escape(name) + r'\b', translated) for name in TRIAL_NAMES.findall(source)):
        return False
    genes = registered_gene_symbols()
    protected = RISK_SYSTEMS.findall(source) + (genes.findall(source) if genes else [])
    if any(not re.search(r'(?<!\w)' + re.escape(token) + r'(?!\w)', translated, re.I) for token in protected):
        return False
    if any(state.casefold() not in translated.casefold() for state in STATES.findall(source)):
        return False
    if sorted(re.findall(r'\d+[+−-]\d+', re.sub(r'\s+', '', source))) != sorted(re.findall(r'\d+[+−-]\d+', re.sub(r'\s+', '', translated))):
        return False
    if drug_pattern and any(not re.search(r'(?<!\w)' + re.escape(match.group()) + r'(?!\w)', translated, re.I) for match in drug_pattern.finditer(source)):
        return False
    if polarity_tokens(source) != polarity_tokens(translated, locale):
        return False
    if len(source) >= 60 and len(translated) < len(source) * 0.65:
        return False
    # Known out-of-domain decoder hallucination on unfamiliar unit fragments.
    if 'regulation' not in source.casefold() and re.search(r'(?:presente reglamento|diario oficial|journal officiel|uniao europeia)', translated, re.I):
        return False
    if locale == 'fr':
        # Observed out-of-domain translations in the first UI review.
        bad_terms = {
            'staging': r'mise en sc[eè]ne',
            'chondrosarcoma': r'coffrosarcome',
            'thyroid': r'hydro[iï]de',
            'germline': r'germination',
            'ESCAT': r'[eé]vacuations',
            'high-grade': r'haute qualit[eé]',
            'low-grade': r'(?:faible|basse) qualit[eé]',
            'driver': r'conducteur',
            'backbone': r'[eé]pine',
            'fitness': r'conditionnement physique',
        }
        if any(term.casefold() in source.casefold() and re.search(pattern, translated, re.I) for term, pattern in bad_terms.items()):
            return False
    if locale == 'de' and re.search(r'\brefractor\w*\b', source, re.I) and 'feuerfest' in translated.casefold():
        return False
    if locale == 'de' and re.search(r'\bdrug\w*\b', source, re.I) and 'drogen' in translated.casefold():
        return False
    return True
