"""A partial release must validate all pages before changing published files."""
import hashlib
from pathlib import Path
import pytest
from scripts.finalize_partial_site import finalize_batch
from scripts.shared_clinical_reader import render_shared_reader
from scripts.site_head import geo_lang_payload, geo_lang_url
from scripts.site_nav import render_top_bar


@pytest.fixture
def public_tree(tmp_path):
    root = tmp_path / 'public'
    (root / 'cases').mkdir(parents=True)
    (root / 'fi/cases').mkdir(parents=True)
    source = '<html lang="en"><head><meta charset="utf-8"><title>Synthetic</title></head><body>' + render_top_bar('gallery', 'en', page_path='cases/example.html') + '<main>Source dose: 20 mg.</main></body></html>'
    (root / 'cases/example.html').write_text(source, encoding='utf-8')
    reader = render_shared_reader(source, 'fi', 'cases/example.html', 'Synthetic')
    (root / 'fi/cases/example.html').write_text(reader, encoding='utf-8')
    (root / geo_lang_url().lstrip('/')).write_bytes(geo_lang_payload())
    (root / 'shared-site-header.js').write_text('/* fixture */')
    (root / 'header.css').write_text('/* fixture */')
    return root


def test_dry_run_then_write_binds_reader_to_final_original_and_is_idempotent(public_tree):
    pages = ['fi/cases/example.html', 'cases/example.html']  # Reader precedes original.
    before = {p: (public_tree / p).read_bytes() for p in pages}
    dry = finalize_batch(public_tree, pages, available_paths=set(pages))
    assert not dry['written'] and dry['reader_bindings']['updated'] == 1
    assert before == {p: (public_tree / p).read_bytes() for p in pages}
    result = finalize_batch(public_tree, pages, available_paths=set(pages), write=True)
    assert result['written'] and not result['clinical_approval']
    source = (public_tree / pages[1]).read_text(encoding='utf-8')
    reader = (public_tree / pages[0]).read_text(encoding='utf-8')
    assert 'Source dose: 20 mg.' in source
    assert hashlib.sha256(source.encode()).hexdigest() in reader
    assert 'data-shared-site-header' in source and geo_lang_url() in source
    assert finalize_batch(public_tree, pages, available_paths=set(pages), write=True)['changed'] == []


@pytest.mark.parametrize('bad', ['../outside.html', '/outside.html', 'cases/../example.html', 'cases/verified-crc-l2-tucatinib-trastuzumab-crc.html', 'cases/verified-prostate-l2-cabazitaxel-mcrpc.patient.html', 'cases/VERIFIED-CRC-L2-TUCATINIB-TRASTUZUMAB-CRC.html'])
def test_invalid_or_preserved_manifest_is_rejected_before_any_page_read(public_tree, monkeypatch, bad):
    original = Path.read_bytes
    reads = []
    def record_read(path):
        reads.append(path)
        return original(path)
    monkeypatch.setattr(Path, 'read_bytes', record_read)
    with pytest.raises(ValueError):
        finalize_batch(public_tree, ['cases/example.html', bad], available_paths=set(), write=True)
    assert reads == []


def test_malformed_reader_prevents_mutating_an_earlier_valid_original(public_tree):
    source = public_tree / 'cases/example.html'
    before = source.read_bytes()
    reader = public_tree / 'fi/cases/example.html'
    reader.write_text(reader.read_text(encoding='utf-8').replace('translation-source-sha256', 'invalid-fingerprint'), encoding='utf-8')
    with pytest.raises(ValueError, match='Ambiguous reader binding'):
        finalize_batch(public_tree, ['cases/example.html', 'fi/cases/example.html'], available_paths={'cases/example.html'}, write=True)
    assert source.read_bytes() == before


def test_unselected_original_is_read_only_and_must_be_inventoried(public_tree):
    source = public_tree / 'cases/example.html'
    before = source.read_bytes()
    pages = ['fi/cases/example.html']
    with pytest.raises(ValueError, match='not inventoried'):
        finalize_batch(public_tree, pages, available_paths=set(), write=True)
    finalize_batch(public_tree, pages, available_paths={'cases/example.html'}, write=True)
    assert source.read_bytes() == before


def test_filesystem_failure_restores_previously_replaced_page(public_tree, monkeypatch):
    pages = ['cases/example.html', 'fi/cases/example.html']
    before = {p: (public_tree / p).read_bytes() for p in pages}
    original = Path.replace
    replacements = 0
    def fail_second(path, target):
        nonlocal replacements
        replacements += 1
        if replacements == 2:
            raise OSError('Synthetic replace failure')
        return original(path, target)
    monkeypatch.setattr(Path, 'replace', fail_second)
    with pytest.raises(OSError, match='Synthetic replace failure'):
        finalize_batch(public_tree, pages, available_paths=set(pages), write=True)
    assert before == {p: (public_tree / p).read_bytes() for p in pages}
    assert not list(public_tree.rglob('.partial-page-*'))


def test_concurrent_edit_is_preserved_and_batch_is_not_applied(public_tree, monkeypatch):
    from scripts import finalize_partial_site as module
    source = public_tree / 'cases/example.html'
    reader = public_tree / 'fi/cases/example.html'
    reader_before = reader.read_bytes()
    original = module.finalize_public_page
    edited = False
    def edit_during_preparation(text, **kwargs):
        nonlocal edited
        if not edited:
            source.write_text(source.read_text(encoding='utf-8').replace('20 mg', '25 mg'), encoding='utf-8')
            edited = True
        return original(text, **kwargs)
    monkeypatch.setattr(module, 'finalize_public_page', edit_during_preparation)
    with pytest.raises(ValueError, match='changed during preparation'):
        finalize_batch(public_tree, ['cases/example.html', 'fi/cases/example.html'], available_paths={'cases/example.html'}, write=True)
    assert '25 mg' in source.read_text(encoding='utf-8')
    assert reader.read_bytes() == reader_before
