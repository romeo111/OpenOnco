"""Private translation drafts retain English provenance and cannot publish themselves."""
import csv
import hashlib
import json

import pytest

from scripts.prepare_translation_drafts import prepare_drafts


class FakeTranslator:
    def __init__(self):
        self.calls = []

    def translate(self, text, target_lang, source_lang=None):
        self.calls.append((text, target_lang, source_lang))
        return f"{text} translated"


def test_private_drafts_are_english_sourced_and_resumable(tmp_path):
    kb_root = tmp_path / "kb"
    kind_dir = kb_root / "diseases"
    kind_dir.mkdir(parents=True)
    source = kind_dir / "nsclc.yaml"
    source.write_text("id: DIS-NSCLC\n", encoding="utf-8")
    index = tmp_path / "index.json"
    index.write_text(json.dumps({"entries": [
        {"id": "DIS-NSCLC", "kind_key": "diseases", "title": "Non-small cell lung cancer"},
    ]}), encoding="utf-8")
    output = tmp_path / "private" / "drafts.jsonl"
    client = FakeTranslator()

    assert prepare_drafts(index, kb_root, output, locale="fr", kind="diseases", client=client, limit=1) == 1
    draft = json.loads(output.read_text(encoding="utf-8").splitlines()[0])
    assert client.calls == [("Non-small cell lung cancer", "fr", "en")]
    assert draft["clinical_review"] == "required"
    assert draft["publication"] == "blocked"
    assert draft["machine_translated"] is True
    assert draft["source_yaml"] == source.as_posix()
    assert prepare_drafts(index, kb_root, output, locale="fr", kind="diseases", client=client, limit=1) == 0

    source.write_text("id: DIS-NSCLC\nnotes: updated\n", encoding="utf-8")
    assert prepare_drafts(index, kb_root, output, locale="fr", kind="diseases", client=client, limit=1) == 1
    assert len(output.read_text(encoding="utf-8").splitlines()) == 2


def test_offline_manual_csv_checks_english_source_before_writing(tmp_path):
    kb_root = tmp_path / "kb"
    kind_dir = kb_root / "regimens"
    kind_dir.mkdir(parents=True)
    source = kind_dir / "abvd.yaml"
    source.write_text("id: REG-ABVD\n", encoding="utf-8")
    title = "ABVD (Adriamycin + Bleomycin), 2-6 cycles"
    index = tmp_path / "index.json"
    index.write_text(json.dumps({"entries": [
        {"id": "REG-ABVD", "kind_key": "regimens", "title": title},
    ]}), encoding="utf-8")
    manual_csv = tmp_path / "manual.csv"
    output = tmp_path / "private" / "drafts.jsonl"
    row = {
        "id": "REG-ABVD",
        "en": title,
        "fr": "ABVD (Adriamycin + Bleomycin), 2 à 6 cycles",
        "source_yaml": source.as_posix(),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    }

    def write_csv():
        with manual_csv.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=row)
            writer.writeheader()
            writer.writerow(row)

    write_csv()
    assert prepare_drafts(index, kb_root, output, locale="fr", kind="regimens", client=None,
                          manual_csv=manual_csv, limit=5) == 1
    draft = json.loads(output.read_text(encoding="utf-8"))
    assert draft["fr"] == row["fr"]
    assert draft["machine_translated"] is True
    assert draft["translation_method"] == "offline_csv"
    assert draft["clinical_review"] == "required" and draft["publication"] == "blocked"
    draft["translation_method"] = "translation_client"
    output.write_text(json.dumps(draft) + "\n", encoding="utf-8")
    assert prepare_drafts(index, kb_root, output, locale="fr", kind="regimens", client=None,
                          manual_csv=manual_csv, limit=5) == 1
    assert json.loads(output.read_text(encoding="utf-8").splitlines()[-1])["translation_method"] == "offline_csv"
    assert prepare_drafts(index, kb_root, output, locale="fr", kind="regimens", client=None,
                          manual_csv=manual_csv, limit=5) == 0

    row["fr"] = "ABVD (Adriamycin + Bleomycin), deux à six cycles"
    write_csv()
    assert prepare_drafts(index, kb_root, output, locale="fr", kind="regimens", client=None,
                          manual_csv=manual_csv, limit=5) == 1
    assert len(output.read_text(encoding="utf-8").splitlines()) == 3

    row["fr"] = title  # Drug names and abbreviations can be language-neutral.
    write_csv()
    assert prepare_drafts(index, kb_root, output, locale="fr", kind="regimens", client=None,
                          manual_csv=manual_csv, limit=5) == 1
    assert "unchanged from English" in json.loads(output.read_text(encoding="utf-8").splitlines()[-1])["review_flags"][0]

    source.write_text("id: REG-ABVD\nnotes: changed\n", encoding="utf-8")
    with pytest.raises(ValueError, match="English YAML changed"):
        prepare_drafts(index, kb_root, output, locale="fr", kind="regimens", client=None,
                       manual_csv=manual_csv, limit=5)
    assert len(output.read_text(encoding="utf-8").splitlines()) == 4
