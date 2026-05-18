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


def test_handbook_index_carries_search_fields(tmp_path: Path):
    payload = build_handbook(KB_ROOT, tmp_path)

    chapters_by_id = {chapter["id"]: chapter for chapter in payload["chapters"]}
    dlbcl = chapters_by_id["HB-DLBCL-1L"]

    # Backward-compatible fields still present.
    assert dlbcl["url"] == "/handbook/hb-dlbcl-1l.html"
    assert dlbcl["question_count"] == 3
    assert "SRC-POLARIX-TILLY-2022" in dlbcl["source_ids"]
    assert dlbcl["disease_ids"] == ["DIS-DLBCL-NOS"]

    # New filter/search-friendly fields land deterministically.
    assert "first-line" in dlbcl["topic_tags"]
    assert "lymphoma" in dlbcl["topic_tags"]
    assert dlbcl["learning_objectives"], "learning_objectives must surface in index for search"
    assert dlbcl["at_a_glance"], "at_a_glance must surface in index for search"
    # Disease labels resolve, not just IDs.
    assert dlbcl["disease_labels"], "disease_labels must resolve so the filter UI shows readable names"

    # Per-chapter records must always carry these keys (search UI relies on them).
    for chapter in payload["chapters"]:
        for key in (
            "topic_tags",
            "learning_objectives",
            "at_a_glance",
            "disease_labels",
        ):
            assert key in chapter, f"{chapter['id']} missing {key}"


def test_handbook_index_page_renders_filter_controls(tmp_path: Path):
    build_handbook(KB_ROOT, tmp_path)
    index = (tmp_path / "handbook.html").read_text(encoding="utf-8")

    # Filter + search controls present and dependency-free (inline JS, no
    # bundler or framework reference).
    assert 'id="hb-search"' in index
    assert 'id="hb-filter-disease"' in index
    assert 'id="hb-filter-tag"' in index
    assert 'id="hb-filter-status"' in index
    assert 'id="hb-result-count"' in index

    # Cards carry the data-* attributes the JS needs to filter without
    # rebuilding the page.
    assert 'data-diseases="DIS-DLBCL-NOS"' in index
    assert 'data-status="draft"' in index
    assert 'data-tags="' in index
    assert 'data-search="' in index

    # Disease dropdown is populated server-side with the actual chapter
    # diseases so the filter is meaningful at page load.
    assert 'value="DIS-CRC"' in index
    assert 'value="DIS-NSCLC"' in index
    assert 'value="DIS-MM"' in index
    assert 'value="DIS-DLBCL-NOS"' in index

    # Topic tag options come from the chapter YAMLs.
    assert 'value="first-line"' in index
    assert 'value="biomarkers"' in index


def test_chapter_page_renders_quiz_forms_with_grading_attrs(tmp_path: Path):
    build_handbook(KB_ROOT, tmp_path)
    dlbcl_chapter = (tmp_path / "handbook" / "hb-dlbcl-1l.html").read_text(encoding="utf-8")

    # Practice section now hosts a quiz with a per-chapter score widget
    # and reset, not a "Show answer" toggle.
    assert 'id="hb-score"' in dlbcl_chapter
    assert 'id="hb-quiz-reset"' in dlbcl_chapter
    assert "0 of 3 answered" in dlbcl_chapter, "score widget seeds with graded_total"
    assert "hb-answer-toggle" not in dlbcl_chapter, "old reveal-toggle must be gone"

    # Single-best-answer (type_a) renders as radios with the correct key
    # as the data-correct-answer.
    assert 'data-question-id="HQ-DLBCL-1L-001"' in dlbcl_chapter
    assert 'data-question-type="type_a"' in dlbcl_chapter
    assert 'data-correct-answer="A"' in dlbcl_chapter

    # Multi-select (type_k) renders as checkboxes; correct keys are
    # normalized to sorted, pipe-separated form so JS can do exact
    # set-equality without parsing commas at runtime.
    assert 'data-question-id="HQ-DLBCL-1L-003"' in dlbcl_chapter
    assert 'data-question-type="type_k"' in dlbcl_chapter
    assert 'data-correct-answer="A|B|D"' in dlbcl_chapter

    # Submit + reset controls are wired per-question.
    assert 'data-action="submit"' in dlbcl_chapter
    assert 'data-action="reset"' in dlbcl_chapter

    # Source IDs remain visible in the result block (Phase 3 acceptance).
    assert 'class="hb-result-source">SRC-NCCN-BCELL-2025' in dlbcl_chapter
    assert 'class="hb-result-source">SRC-POLARIX-TILLY-2022' in dlbcl_chapter

    # Quiz JS is inlined (no external script tag added) and keys
    # storage per chapter so different chapters don't share score state.
    assert 'CHAPTER_ID = "HB-DLBCL-1L"' in dlbcl_chapter
    assert "sessionStorage" in dlbcl_chapter


def test_chapter_page_uses_radios_for_type_a_and_checkboxes_for_type_k(tmp_path: Path):
    build_handbook(KB_ROOT, tmp_path)
    dlbcl_chapter = (tmp_path / "handbook" / "hb-dlbcl-1l.html").read_text(encoding="utf-8")

    # DLBCL chapter has 2 type_a + 1 type_k question, all with 4 options.
    radio_count = dlbcl_chapter.count('type="radio"')
    checkbox_count = dlbcl_chapter.count('type="checkbox"')
    assert radio_count == 8, f"expected 8 radio inputs (2 type_a × 4 options), got {radio_count}"
    assert checkbox_count == 4, f"expected 4 checkbox inputs (1 type_k × 4 options), got {checkbox_count}"


def test_correct_keys_handles_both_single_and_multi(tmp_path: Path):
    """Direct unit test on the normalization helper."""
    from scripts.build_handbook import _correct_keys

    assert _correct_keys({"correct_answer": "A"}) == ["A"]
    assert _correct_keys({"correct_answer": "A,B,D"}) == ["A", "B", "D"]
    # Robust to whitespace, alternative separators, case variants.
    assert _correct_keys({"correct_answer": " a | c "}) == ["A", "C"]
    # short_answer has no correct_answer in option-key form.
    assert _correct_keys({"correct_answer": None}) == []
