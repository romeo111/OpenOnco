"""The treatment runtime must not load unrelated Handbook references."""

from pathlib import Path
import json
import hashlib
import tarfile
import zipfile

from scripts import build_site


def test_learning_content_does_not_enter_treatment_bundles(tmp_path, monkeypatch):
    content = tmp_path / "knowledge_base" / "hosted" / "content"
    for folder in ("handbook_chapters", "handbook_questions", "sources", "algorithms"):
        (content / folder).mkdir(parents=True)
    (content / "handbook_chapters" / "chapter.yaml").write_text(
        "id: HB-OTHER\nlinked_entity_ids: [ALGO-OTHER]\n", encoding="utf-8"
    )
    (content / "handbook_questions" / "question.yaml").write_text(
        "id: HQ-OTHER\nchapter_id: HB-OTHER\n", encoding="utf-8"
    )
    (content / "sources" / "source.yaml").write_text("id: SRC-ONE\n", encoding="utf-8")
    (content / "algorithms" / "algorithm.yaml").write_text(
        "id: ALGO-AML\ndisease_id: DIS-AML\n", encoding="utf-8"
    )
    monkeypatch.setattr(build_site, "REPO_ROOT", tmp_path)
    entries = build_site._gather_engine_entries()
    names = {name for _, name, _ in entries}
    assert not any("/handbook_" in name for name in names)
    assert "knowledge_base/hosted/content/sources/source.yaml" in names
    assert any(name.endswith("/algorithm.yaml") and disease == "DIS-AML" for _, name, disease in entries)
    # These remain available to the separate static Handbook builder.
    assert (content / "handbook_chapters" / "chapter.yaml").is_file()


def test_runtime_packages_include_transitive_cross_disease_dependencies(tmp_path, monkeypatch):
    content = tmp_path / "knowledge_base" / "hosted" / "content"
    fixtures = {
        "contraindications/shared.yaml": "id: CI-SHARED\naffects_indications: [IND-OTHER]\n",
        "indications/other.yaml": "id: IND-OTHER\ndisease_id: DIS-OTHER\nregimen_id: REG-OTHER\n",
        "regimens/other.yaml": "id: REG-OTHER\ndisease_id: DIS-OTHER\n",
        "algorithms/aml.yaml": "id: ALGO-AML\ndisease_id: DIS-AML\nnext: IND-CROSS\n",
        "indications/cross.yaml": "id: IND-CROSS\ndisease_id: DIS-CROSS\nregimen_id: REG-CROSS\n",
        "regimens/cross.yaml": "id: REG-CROSS\ndisease_id: DIS-CROSS\n",
    }
    for name, text in fixtures.items():
        path = content / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    monkeypatch.setattr(build_site, "REPO_ROOT", tmp_path)
    output = tmp_path / "docs"
    output.mkdir()
    build_site.bundle_engine(output)
    with zipfile.ZipFile(output / "openonco-engine-core.zip") as archive:
        core = set(archive.namelist())
    assert any(name.endswith("/other.yaml") and "/indications/" in name for name in core)
    assert any(name.endswith("/other.yaml") and "/regimens/" in name for name in core)
    assert not any(name.endswith("/aml.yaml") for name in core)
    with zipfile.ZipFile(output / "disease/openonco-dis-aml.zip") as archive:
        module = set(archive.namelist())
    assert any(name.endswith("/cross.yaml") and "/indications/" in name for name in module)
    assert any(name.endswith("/cross.yaml") and "/regimens/" in name for name in module)
    index = json.loads((output / "openonco-engine-index.json").read_text())
    stream = output / index["core_compressed"]
    assert hashlib.sha256(stream.read_bytes()).hexdigest()[:12] == index["core_compressed_version"]
    with zipfile.ZipFile(output / index["core"]) as legacy, tarfile.open(stream, "r:gz") as compressed:
        assert set(legacy.namelist()) == set(compressed.getnames())
        for name in legacy.namelist():
            assert legacy.read(name) == compressed.extractfile(name).read()
    original = stream.read_bytes()
    build_site.bundle_engine(output)
    assert stream.read_bytes() == original
