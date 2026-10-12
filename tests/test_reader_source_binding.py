import hashlib
from pathlib import Path

import pytest
from scripts.shared_clinical_reader import render_shared_reader, synchronize_reader_source_hashes
from scripts.site_head import finalize_site_discovery
from scripts.build_site import _normalize_generated_text_whitespace


def fixture(root):
    source = root / 'cases/synthetic.html'
    source.parent.mkdir(parents=True)
    source.write_text('<html lang="en"><head><title>Synthetic</title></head><body><main>20 mg</main></body></html>', encoding='utf-8')
    reader = root / 'it/cases/synthetic.html'
    reader.parent.mkdir(parents=True)
    reader.write_text(render_shared_reader(source.read_text(encoding='utf-8'), 'it', 'cases/synthetic.html', 'Synthetic'), encoding='utf-8')
    return source, reader


def test_final_discovery_binds_after_seo_and_header_changes(tmp_path):
    source, reader = fixture(tmp_path)
    original = source.read_text(encoding='utf-8')
    result = finalize_site_discovery(tmp_path, stats={})
    assert source.read_text(encoding='utf-8') != original
    digest = hashlib.sha256(source.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    assert f'name="translation-source-sha256" content="{digest}"' in reader.read_text(encoding='utf-8')
    assert result['reader_source_bindings_updated'] == 1
    assert synchronize_reader_source_hashes(tmp_path)['updated'] == 0
    assert finalize_site_discovery(tmp_path, stats={})['reader_source_bindings_updated'] == 0


def test_only_actual_hash_attribute_changes_not_nested_strings(tmp_path):
    source, reader = fixture(tmp_path)
    text = reader.read_text(encoding='utf-8')
    fake = 'data-example="content=\'example\'" '
    text = text.replace('name="translation-source-sha256"', fake + 'name="translation-source-sha256"')
    text = text.replace('<title>', '\u2028<title>')
    text += '<script>const example = \'<iframe data-shared-clinical-source src="https://example.com">\';</script>'
    reader.write_text(text, encoding='utf-8')
    source.write_text(source.read_text(encoding='utf-8') + '\n', encoding='utf-8')
    expected = hashlib.sha256(source.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    assert synchronize_reader_source_hashes(tmp_path)['updated'] == 1
    updated = reader.read_text(encoding='utf-8')
    assert fake in updated
    assert 'content="' + expected + '"' in updated
    assert '<script>const example' in updated


def test_final_whitespace_pass_requires_another_binding_pass(tmp_path):
    source, reader = fixture(tmp_path)
    source.write_text(source.read_text(encoding='utf-8') + '  \n', encoding='utf-8')
    assert synchronize_reader_source_hashes(tmp_path)['updated'] == 1
    assert _normalize_generated_text_whitespace(tmp_path) > 0
    assert synchronize_reader_source_hashes(tmp_path)['updated'] == 1
    expected = hashlib.sha256(source.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    assert 'content="' + expected + '"' in reader.read_text(encoding='utf-8')


@pytest.mark.parametrize('href', ['https://example.com/x.html', '/cases/../../private.html', '/cases/x.html?token=1', '/cases/%2e%2e/private.html'])
def test_unsafe_original_is_rejected_without_any_batch_write(tmp_path, href):
    source, reader = fixture(tmp_path)
    text = reader.read_text(encoding='utf-8').replace('src="/cases/synthetic.html"', f'src="{href}"')
    reader.write_text(text, encoding='utf-8')
    source.write_text('Changed original', encoding='utf-8')
    with pytest.raises(ValueError, match='Invalid original path'):
        synchronize_reader_source_hashes(tmp_path)
    assert reader.read_text(encoding='utf-8') == text


def test_duplicate_binding_is_rejected(tmp_path):
    _, reader = fixture(tmp_path)
    text = reader.read_text(encoding='utf-8') + '<iframe data-shared-clinical-source src="/cases/synthetic.html"></iframe>'
    reader.write_text(text, encoding='utf-8')
    with pytest.raises(ValueError, match='Ambiguous reader binding'):
        synchronize_reader_source_hashes(tmp_path)
    assert reader.read_text(encoding='utf-8') == text


def test_later_invalid_reader_leaves_earlier_valid_reader_unchanged(tmp_path):
    source, first = fixture(tmp_path)
    before = first.read_text(encoding='utf-8')
    second = first.with_name('invalid.html')
    second.write_text(before.replace('src="/cases/synthetic.html"', 'src="https://example.com/private.html"'), encoding='utf-8')
    source.write_text('Updated fictional source', encoding='utf-8')
    with pytest.raises(ValueError, match='Invalid original path'):
        synchronize_reader_source_hashes(tmp_path, pages=[first, second])
    assert first.read_text(encoding='utf-8') == before


def test_preserved_name_is_skipped_before_reading(tmp_path, monkeypatch):
    preserved = tmp_path / 'verified-crc-l2-tucatinib-trastuzumab-crc.html'
    def forbidden(*args, **kwargs):
        raise AssertionError('Preserved file must not be opened')
    monkeypatch.setattr(Path, 'read_text', forbidden)
    assert synchronize_reader_source_hashes(tmp_path, pages=[preserved]) == {'checked': 0, 'updated': 0, 'preserved': 1}
