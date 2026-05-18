from __future__ import annotations

import json
from pathlib import Path

from knowledge_base.validation.loader import clear_load_cache, load_content
from scripts.build_handbook import build_handbook


KB_ROOT = Path("knowledge_base/hosted/content")


def test_handbook_seed_loads_with_questions():
    result = load_content(KB_ROOT)

    chapter_ids = {
        eid
        for eid, info in result.entities_by_id.items()
        if info["type"] == "handbook_chapters"
    }
    assert chapter_ids == {
        "HB-CRC-METASTATIC-1L",
        "HB-DLBCL-1L",
        "HB-MM-1L",
        "HB-NSCLC-METASTATIC-1L",
    }

    chapter = result.entities_by_id["HB-DLBCL-1L"]
    assert chapter["type"] == "handbook_chapters"
    assert chapter["data"]["review_status"] == "draft"
    assert "SRC-POLARIX-TILLY-2022" in chapter["data"]["source_ids"]

    question_ids = {
        eid
        for eid, info in result.entities_by_id.items()
        if info["type"] == "handbook_questions"
    }
    assert len(question_ids) == 12
    assert {
        "HQ-DLBCL-1L-001",
        "HQ-DLBCL-1L-002",
        "HQ-DLBCL-1L-003",
        "HQ-CRC-MET-1L-001",
        "HQ-NSCLC-MET-1L-001",
        "HQ-MM-1L-001",
    }.issubset(question_ids)


def test_handbook_rejects_unresolved_linked_entities(tmp_path: Path):
    clear_load_cache()
    chapter_dir = tmp_path / "handbook_chapters"
    chapter_dir.mkdir()
    (chapter_dir / "bad.yaml").write_text(
        """
id: HB-BAD
title: Bad chapter
learning_objectives:
  - Learn why unresolved IDs fail.
at_a_glance:
  - Broken on purpose.
source_ids:
  - SRC-MISSING
linked_entities:
  diseases:
    - DIS-MISSING
sections:
  - heading: Broken
    body: This intentionally references a missing entity.
    linked_entity_ids:
      - IND-MISSING
review_status: draft
""",
        encoding="utf-8",
    )

    result = load_content(tmp_path)

    messages = "\n".join(
        message for _, message in result.ref_errors + result.contract_warnings
    )
    assert "source_ids[0]" in messages
    assert "disease_ids" not in messages
    assert "linked_entities.diseases[0]" in messages
    assert "sections[0].linked_entity_ids[0]" in messages


def test_build_handbook_writes_index_and_chapter(tmp_path: Path):
    payload = build_handbook(KB_ROOT, tmp_path)

    chapters_by_id = {chapter["id"]: chapter for chapter in payload["chapters"]}

    assert payload["count"] == 4
    assert set(chapters_by_id) == {
        "HB-CRC-METASTATIC-1L",
        "HB-DLBCL-1L",
        "HB-MM-1L",
        "HB-NSCLC-METASTATIC-1L",
    }
    assert all(chapter["question_count"] == 3 for chapter in chapters_by_id.values())

    index = (tmp_path / "handbook.html").read_text(encoding="utf-8")
    dlbcl_chapter = (tmp_path / "handbook" / "hb-dlbcl-1l.html").read_text(
        encoding="utf-8"
    )
    crc_chapter = (tmp_path / "handbook" / "hb-crc-metastatic-1l.html").read_text(
        encoding="utf-8"
    )
    nsclc_chapter = (tmp_path / "handbook" / "hb-nsclc-metastatic-1l.html").read_text(
        encoding="utf-8"
    )
    mm_chapter = (tmp_path / "handbook" / "hb-mm-1l.html").read_text(encoding="utf-8")
    search = json.loads((tmp_path / "handbook_index.json").read_text(encoding="utf-8"))

    assert "OpenOnco Handbook" in index
    assert "not official ESMO content" in index
    assert "Metastatic colorectal cancer" in index
    assert "Metastatic NSCLC" in index
    assert "Multiple myeloma" in index
    assert "Practice questions" in dlbcl_chapter
    assert "Question 1" in dlbcl_chapter
    assert "SRC-POLARIX-TILLY-2022" in dlbcl_chapter
    assert "MSI-H/dMMR is treatment-defining" in crc_chapter
    assert "driver-first routing" in nsclc_chapter
    assert "transplant-eligible" in mm_chapter

    urls_by_id = {chapter["id"]: chapter["url"] for chapter in search["chapters"]}
    assert urls_by_id == {
        "HB-CRC-METASTATIC-1L": "/handbook/hb-crc-metastatic-1l.html",
        "HB-DLBCL-1L": "/handbook/hb-dlbcl-1l.html",
        "HB-MM-1L": "/handbook/hb-mm-1l.html",
        "HB-NSCLC-METASTATIC-1L": "/handbook/hb-nsclc-metastatic-1l.html",
    }
