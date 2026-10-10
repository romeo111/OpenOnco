"""Private translation drafts retain English provenance and cannot publish themselves."""
import json

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
