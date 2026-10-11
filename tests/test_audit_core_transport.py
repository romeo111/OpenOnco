import hashlib
import io
import json
import tarfile
import zipfile

import pytest

from scripts import audit_core_transport as audit


def make_site(path, *, changed=False, unsafe=False):
    name = "knowledge_base/engine/example.py" if not unsafe else "knowledge_base/../escape.py"
    with zipfile.ZipFile(path / "openonco-engine-core.zip", "w") as archive:
        archive.writestr(name, b"original")
    with tarfile.open(path / "openonco-engine-core.tar.gz", "w:gz") as archive:
        data = b"changed" if changed else b"original"
        member = tarfile.TarInfo(name)
        member.size = len(data)
        archive.addfile(member, io.BytesIO(data))
    refresh_hashes(path)


def refresh_hashes(path):
    index = {}
    for key, filename in (("core", "openonco-engine-core.zip"), ("core_compressed", "openonco-engine-core.tar.gz")):
        index[key] = filename
        index[key + "_version"] = hashlib.sha256((path / filename).read_bytes()).hexdigest()[:12]
    (path / "openonco-engine-index.json").write_text(json.dumps(index))


def test_actual_bytes_and_members_pass_without_extraction(tmp_path):
    make_site(tmp_path)
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    assert audit.audit_core_transport(tmp_path)["files"] == 1
    assert before == {p.name: p.read_bytes() for p in tmp_path.iterdir()}


@pytest.mark.parametrize("changed,unsafe,message", [(True, False, "content differs"), (False, True, "Unsafe archive")])
def test_valid_hashes_do_not_hide_changed_or_unsafe_members(tmp_path, changed, unsafe, message):
    make_site(tmp_path, changed=changed, unsafe=unsafe)
    with pytest.raises(ValueError, match=message):
        audit.audit_core_transport(tmp_path)


def test_budget_and_hash_failures_block_cli(tmp_path, monkeypatch):
    make_site(tmp_path)
    monkeypatch.setattr(audit, "CORE_BUDGET_BYTES", 1)
    assert audit.main(["--site-dir", str(tmp_path)]) == 1
    monkeypatch.setattr(audit, "CORE_BUDGET_BYTES", 4_250_000)
    with (tmp_path / "openonco-engine-core.tar.gz").open("ab") as stream:
        stream.write(b"corrupt")
    assert audit.main(["--site-dir", str(tmp_path)]) == 1


@pytest.mark.parametrize("kind", ["duplicate", "symlink", "empty", "dot", "double-slash"])
def test_matching_archive_hashes_cannot_bypass_member_safety(tmp_path, kind):
    name = {"dot": "knowledge_base/./engine/example.py",
            "double-slash": "knowledge_base//engine/example.py"}.get(kind, "knowledge_base/engine/example.py")
    with zipfile.ZipFile(tmp_path / "openonco-engine-core.zip", "w") as legacy:
        if kind != "empty":
            legacy.writestr(name, b"original")
    with tarfile.open(tmp_path / "openonco-engine-core.tar.gz", "w:gz") as stream:
        if kind != "empty":
            member = tarfile.TarInfo(name)
            if kind == "symlink":
                member.type = tarfile.SYMTYPE
                member.linkname = "../../escape.py"
                stream.addfile(member)
            else:
                member.size = len(b"original")
                stream.addfile(member, io.BytesIO(b"original"))
                if kind == "duplicate":
                    stream.addfile(member, io.BytesIO(b"original"))
    refresh_hashes(tmp_path)
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    with pytest.raises(ValueError, match="Duplicate|Unsafe|Empty"):
        audit.audit_core_transport(tmp_path)
    assert before == {p.name: p.read_bytes() for p in tmp_path.iterdir()}


@pytest.mark.parametrize("index", [[], {}, {"core": "../outside.zip"}])
def test_invalid_index_fails_before_opening_archive_paths(tmp_path, index):
    (tmp_path / "openonco-engine-index.json").write_text(json.dumps(index))
    assert audit.main(["--site-dir", str(tmp_path)]) == 1
