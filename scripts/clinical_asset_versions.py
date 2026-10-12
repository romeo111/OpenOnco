"""Immutable translation asset URLs; retain the original catalog contents."""
import hashlib
import re
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def clinical_runtime_bytes():
    return Path(__file__).with_name('clinical-localization.js').read_text(encoding='utf-8').encode('utf-8')


def asset_name(name, payload):
    path = Path(name)
    return f'{path.stem}.{hashlib.sha256(payload).hexdigest()[:12]}{path.suffix}'


def clinical_runtime_url():
    return '/' + asset_name('clinical-localization.js', clinical_runtime_bytes())


def write_asset(directory, name, payload, *, retain_previous=False):
    directory = Path(directory)
    target_name = asset_name(name, payload)
    (directory / name).write_bytes(payload)
    (directory / target_name).write_bytes(payload)
    # Old generated versions have no references in the newly rendered edition.
    # Keep the canonical compatibility path and only prune our exact hash form.
    pattern = re.compile(re.escape(Path(name).stem) + r'\.[0-9a-f]{12}' + re.escape(Path(name).suffix))
    for old in directory.glob(Path(name).stem + '.*' + Path(name).suffix):
        if not retain_previous and old.name != target_name and pattern.fullmatch(old.name):
            if not old.resolve().is_relative_to(directory.resolve()):
                raise ValueError('Generated asset must remain in its publication directory')
            old.unlink()
    return target_name


def write_clinical_assets(output_dir, locale):
    output_dir = Path(output_dir)
    write_asset(output_dir, 'clinical-localization.js', clinical_runtime_bytes(), retain_previous=True)
    result = {'runtime': clinical_runtime_url()}
    for name in ('clinical-translations.json', 'clinical-ui-translations.json'):
        directory = output_dir / locale
        payload = (directory / name).read_text(encoding='utf-8').encode('utf-8')
        result[name] = f'/{locale}/' + write_asset(directory, name, payload, retain_previous=name == 'clinical-ui-translations.json')
    return result
