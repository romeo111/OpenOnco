"""Verify completed staged catalogs, preserve originals, then publish them."""
import hashlib
import json
import re
import shutil
from pathlib import Path

from scripts.clinical_translation_checks import acceptable_draft
from scripts.site_translation_catalog import LANGUAGES


def publish(staging=Path('.tmp/clinical-next'), corpus=Path('.tmp/clinical-source-strings.json')):
    sources = json.loads(corpus.read_text(encoding='utf-8'))
    destination = Path('scripts/locales')
    index = json.loads(Path('docs/kb_search_index.json').read_text(encoding='utf-8'))
    drugs = {entry['title'] for entry in index['entries'] if entry.get('kind_key') == 'drugs' and len(entry['title']) < 70}
    pattern = re.compile(r'(?<!\w)(?:' + '|'.join(re.escape(name) for name in sorted(drugs, key=len, reverse=True)) + r')(?!\w)', re.I)
    verified = {}
    inventory = {}
    for locale in LANGUAGES:
        path = staging / f'clinical.{locale}.json'
        summary = json.loads(path.with_suffix('.summary.json').read_text(encoding='utf-8'))
        catalog = json.loads(path.read_text(encoding='utf-8'))
        previous = destination / path.name
        baseline = json.loads(previous.read_text(encoding='utf-8')) if previous.exists() else {}
        if not set(baseline) <= set(catalog) or not set(sources) <= set(catalog):
            raise ValueError(f'{locale}: incomplete catalog or missing previous keys')
        if summary['source_strings'] != len(sources) or summary['strings'] != len(catalog):
            raise ValueError(f'{locale}: completion summary mismatch')
        failures = [source for source, value in catalog.items() if not acceptable_draft(source, value, locale, pattern)]
        # A stricter final check may reject an earlier generation checkpoint.
        # Preserve the complete source for that key; never reconstruct a dose
        # or biomarker fragment. The staged version itself remains untouched.
        for source in failures:
            catalog[source] = source
        assert all(acceptable_draft(source, value, locale, pattern) for source, value in catalog.items())
        payload = (json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')
        verified[locale] = (path, payload)
        inventory[locale] = {
            'sha256': hashlib.sha256(payload).hexdigest(),
            'strings': len(catalog),
            'translated_strings': sum(catalog[source] != source for source in sources),
            'original_strings': sum(catalog[source] == source for source in sources),
            'review': 'pending_clinical_review',
            'final_check_originals': len(failures),
        }
    # Validation of all languages precedes any replacement. Preserve every
    # previous version by its content hash; repeated publication is reversible.
    backup = Path('.tmp/clinical-catalog-backups')
    backup.mkdir(parents=True, exist_ok=True)
    for locale, (path, payload) in verified.items():
        previous = destination / path.name
        if previous.exists():
            digest = hashlib.sha256(previous.read_bytes()).hexdigest()
            shutil.copy2(previous, backup / f'{previous.stem}.{digest}.json')
        previous.write_bytes(payload)
    manifest = {
        'source_sha256': hashlib.sha256(corpus.read_bytes()).hexdigest(),
        'languages': inventory,
        'models': {
            'es/pt/fr': {'name': 'Helsinki-NLP/opus-mt-en-ROMANCE', 'revision': 'f8f3a28e8b6272d0ccc0290b832f699e154ae431', 'license': 'Apache-2.0'},
            'de': {'name': 'Helsinki-NLP/opus-mt-en-de', 'revision': '6183067f769a302e3861815543b9f312c71b0ca4', 'license': 'CC-BY-4.0'},
        },
    }
    (destination / 'clinical_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(inventory, indent=2))


if __name__ == '__main__':
    publish()
