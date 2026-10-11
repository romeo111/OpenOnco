"""Recheck published draft catalogs and restore unsafe entries to English.

This is a fidelity fallback, not clinical approval. Generated locale pages must
be rebuilt after applying it.
"""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

from scripts.clinical_translation_checks import acceptable_draft
from scripts.site_translation_catalog import LANGUAGES


def recheck(catalog_dir: Path, index_path: Path, *, apply: bool = False) -> dict[str, int]:
    index = json.loads(index_path.read_text(encoding='utf-8'))
    drugs = {entry['title'] for entry in index['entries'] if entry.get('kind_key') == 'drugs' and len(entry['title']) < 70}
    pattern = re.compile(r'(?<!\w)(?:' + '|'.join(re.escape(name) for name in sorted(drugs, key=len, reverse=True)) + r')(?!\w)', re.IGNORECASE)
    manifest_path = catalog_dir / 'clinical_manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    repaired = {}
    inventory = {}
    for locale in LANGUAGES:
        if locale not in manifest['languages']:
            continue
        path = catalog_dir / f'clinical.{locale}.json'
        if hashlib.sha256(path.read_bytes()).hexdigest() != manifest['languages'][locale]['sha256']:
            raise ValueError(f'Catalog checksum mismatch: {locale}')
        catalog = json.loads(path.read_text(encoding='utf-8'))
        rejected = [source for source, value in catalog.items() if not acceptable_draft(source, value, locale, pattern)]
        for source in rejected:
            catalog[source] = source
        assert all(acceptable_draft(source, value, locale, pattern) for source, value in catalog.items())
        payload = (json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')
        repaired[locale] = len(rejected)
        inventory[locale] = (path, payload, catalog)
    if apply:
        backup = catalog_dir.parent.parent / '.tmp' / 'clinical-catalog-backups'
        backup.mkdir(parents=True, exist_ok=True)
        for locale, (path, payload, catalog) in inventory.items():
            old_hash = hashlib.sha256(path.read_bytes()).hexdigest()
            shutil.copy2(path, backup / f'{path.stem}.{old_hash}.json')
            path.write_bytes(payload)
            entry = manifest['languages'][locale]
            entry['sha256'] = hashlib.sha256(payload).hexdigest()
            entry['translated_strings'] = sum(source != value for source, value in catalog.items())
            entry['original_strings'] = sum(source == value for source, value in catalog.items())
            entry['fidelity_fallbacks'] = entry.get('fidelity_fallbacks', 0) + repaired[locale]
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return repaired


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Replace rejected translations with English source')
    args = parser.parse_args()
    result = recheck(Path('scripts/locales'), Path('docs/kb_search_index.json'), apply=args.apply)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
