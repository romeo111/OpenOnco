"""Apply source-checked safety notices to existing draft translation catalogs."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

from scripts.clinical_curated_copy import safety_notices_for
from scripts.clinical_translation_checks import acceptable_draft
from scripts.site_translation_catalog import LANGUAGES


def apply_notices(catalog_dir: Path, *, apply: bool = False) -> dict[str, int]:
    manifest_path = catalog_dir / 'clinical_manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    updates = {}
    changed = {}
    for locale in LANGUAGES:
        if locale not in manifest['languages']:
            continue
        path = catalog_dir / f'clinical.{locale}.json'
        if hashlib.sha256(path.read_bytes()).hexdigest() != manifest['languages'][locale]['sha256']:
            raise ValueError(f'Catalog checksum mismatch: {locale}')
        catalog = json.loads(path.read_text(encoding='utf-8'))
        count = 0
        for source, translated in safety_notices_for(locale).items():
            if source not in catalog:
                continue
            if not acceptable_draft(source, translated, locale):
                raise ValueError(f'Invalid curated safety notice: {locale}: {source}')
            if catalog[source] != translated:
                catalog[source] = translated
                count += 1
        payload = (json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')
        changed[locale] = count
        updates[locale] = (path, payload, catalog)
    if apply:
        backup = catalog_dir.parent.parent / '.tmp' / 'clinical-catalog-backups'
        backup.mkdir(parents=True, exist_ok=True)
        for locale, (path, payload, catalog) in updates.items():
            if not changed[locale]:
                continue
            previous_hash = hashlib.sha256(path.read_bytes()).hexdigest()
            shutil.copy2(path, backup / f'{path.stem}.{previous_hash}.json')
            path.write_bytes(payload)
            entry = manifest['languages'][locale]
            entry['sha256'] = hashlib.sha256(payload).hexdigest()
            entry['translated_strings'] = sum(source != value for source, value in catalog.items())
            entry['original_strings'] = sum(source == value for source, value in catalog.items())
            entry['curated_safety_notices'] = len(safety_notices_for(locale))
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    print(json.dumps(apply_notices(Path('scripts/locales'), apply=args.apply), indent=2))


if __name__ == '__main__':
    main()
