import hashlib
import json
from scripts.clinical_asset_versions import write_asset, write_clinical_assets, clinical_runtime_bytes


def test_asset_revisions_change_paths_and_prune_only_generated_versions(tmp_path):
    first = write_asset(tmp_path, 'clinical-translations.json', b'{"a":"a"}\n')
    unrelated = tmp_path / 'clinical-translations.notes.json'
    unrelated.write_text('preserve')
    second = write_asset(tmp_path, 'clinical-translations.json', b'{"a":"updated"}\n')
    assert first != second and not (tmp_path / first).exists()
    assert unrelated.read_text() == 'preserve'
    assert (tmp_path / second).read_bytes() == (tmp_path / 'clinical-translations.json').read_bytes()


def test_catalog_assets_retain_every_value_and_match_published_fingerprints(tmp_path):
    directory = tmp_path / 'fi'
    directory.mkdir()
    original = {'Dose': '100 mg', 'Original clause': 'Original clause', 'Label': 'Suomi'}
    for name in ('clinical-translations.json', 'clinical-ui-translations.json'):
        (directory / name).write_text(json.dumps(original), encoding='utf-8')
    assets = write_clinical_assets(tmp_path, 'fi')
    for key, url in assets.items():
        data = (tmp_path / url.lstrip('/')).read_bytes()
        assert hashlib.sha256(data).hexdigest()[:12] in url
        if key == 'runtime':
            assert data == clinical_runtime_bytes()
        else:
            assert json.loads(data) == original
