"""Publish verified local draft artifacts into source catalogs; never deploy.

All five authoring jobs must finish. This command preserves existing catalogs,
records draft scope and hashes, and keeps clinical review status pending.
"""
import argparse
import hashlib
import json
import pprint
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.additional_locale_copy import ADDITIONAL_LANGUAGES, CURATED_SITE_FIELDS, ENGLISH_COPY
from scripts.prepare_additional_locales import drug_pattern_from_site, interface_sources
from scripts.clinical_translation_checks import acceptable_draft
from serverless.clinical_locale_messages import MESSAGES

ALIASES = {
    'Перегляд клінічного змісту очікується': 'Clinical content review pending',
    'Перегляд клінічного змісту очікується (записано 1 із 2 допустимих переглядів)': 'Clinical content review pending (1 of 2 eligible reviews recorded)',
    'Записано необхідні перегляди клінічного змісту': 'Required clinical-content reviews recorded',
    'Цей статус описує перегляди змісту бази знань, а не схвалення плану для вас.': 'This status describes reviews of the knowledge-base content, not approval of a plan for you.',
    'Солопроєкт. Один власник доставляє оновлення з автоматичними перевірками та простежуваними джерелами. Зовнішній клінічний перегляд є додатковим і записується окремо.': 'Solo project. One maintainer delivers updates with automated checks and source traceability. External clinical review is optional and is recorded separately.',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staging', type=Path, default=ROOT / '.tmp/additional-locale-drafts')
    args = parser.parse_args()
    required = set(interface_sources(ROOT / 'docs'))
    drug_pattern = drug_pattern_from_site(ROOT / 'docs')
    index = json.loads((ROOT / 'docs/kb_search_index.json').read_text(encoding='utf-8'))
    diagnosis_names = {entry['title'] for entry in index['entries'] if entry.get('kind_key') == 'diseases'}
    prepared = {}
    for code in ADDITIONAL_LANGUAGES:
        clinical = json.loads((args.staging / f'clinical.{code}.json').read_text(encoding='utf-8'))
        site = json.loads((args.staging / f'site.{code}.json').read_text(encoding='utf-8'))
        curated = json.loads((args.staging / f'curated.{code}.json').read_text(encoding='utf-8'))
        explicit_copy = {ENGLISH_COPY[key]: value for key, value in CURATED_SITE_FIELDS[code].items()}
        clinical.update(explicit_copy)
        site.update(CURATED_SITE_FIELDS[code])
        if not required <= clinical.keys() or set(site) != set(ENGLISH_COPY):
            raise ValueError(f'Incomplete interface authoring job: {code}')
        if any(not isinstance(value, str) or not value.strip() for value in site.values()):
            raise ValueError(f'Empty native site copy: {code}')
        # The exact hand-curated disclaimer is checked separately and is not
        # rewritten to satisfy lexical-count heuristics.
        from serverless.clinical_question import DISCLAIMER_EN, DISCLAIMER_TRANSLATIONS
        disclaimer = ' '.join(DISCLAIMER_EN.split())
        for source, value in clinical.items():
            if source == disclaimer:
                if value != ' '.join(DISCLAIMER_TRANSLATIONS[code].split()):
                    raise ValueError(f'Native disclaimer mismatch: {code}')
            elif source in explicit_copy:
                if value != explicit_copy[source]:
                    raise ValueError(f'Curated interface copy mismatch: {code}')
            elif not acceptable_draft(source, value, code, drug_pattern):
                # Preserve the original instead of publishing a degraded drug,
                # quantity, identifier or polarity. This remains draft content.
                clinical[source] = source
        curated.update({source: clinical[source] for source in curated if source in clinical})
        clinical.update({name: name for name in diagnosis_names})
        curated.update({name: name for name in diagnosis_names})
        curated.update({source: clinical[english] for source, english in ALIASES.items()})
        prepared[code] = (clinical, site, curated)
    # No source mutation occurs until every language passes the checks above.
    directory = ROOT / 'scripts/locales'
    manifest_path = directory / 'clinical_manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    api_messages = {}
    for code, (clinical, site, curated) in prepared.items():
        for prefix, content in [('clinical', clinical), ('site', site), ('curated', curated), ('public', clinical)]:
            path = directory / f'{prefix}.{code}.json'
            path.write_text(json.dumps(content, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8', newline='\n')
        clinical_path = directory / f'clinical.{code}.json'
        original = sum(source == value for source, value in clinical.items())
        manifest['languages'][code] = {
            'sha256': hashlib.sha256(clinical_path.read_bytes()).hexdigest(),
            'strings': len(clinical), 'translated_strings': len(clinical) - original,
            'original_strings': original, 'review': 'pending_clinical_review',
            'scope': 'interface-first draft; clinical passages may retain their original language',
        }
        api_messages[code] = {source: clinical[source] for source in MESSAGES}
    (ROOT / 'serverless/additional_locale_messages.py').write_text(
        '"""Locally authored display drafts; not clinical validation."""\n'
        + 'MESSAGES = ' + pprint.pformat(api_messages, sort_dicts=True, width=100) + '\n', encoding='utf-8')
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('Five additional interface catalogs published to source; clinical and language review remain pending.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
