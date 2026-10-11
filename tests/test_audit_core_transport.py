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
