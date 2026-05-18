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


# ---------------------------------------------------------------------------
# Phase 4: reviewer workflow — schema and loader checks.
# ---------------------------------------------------------------------------

import pytest
from pydantic import ValidationError


_MINIMAL_CHAPTER = {
    "id": "HB-TEST",
    "title": "Test",
    "learning_objectives": ["x"],
    "at_a_glance": ["x"],
    "source_ids": ["SRC-FAKE"],
}


def _chapter(**overrides):
    from knowledge_base.schemas.handbook import HandbookChapter
    payload = dict(_MINIMAL_CHAPTER, **overrides)
    return HandbookChapter(**payload)


def test_chapter_draft_status_needs_no_review_metadata():
    chapter = _chapter()  # default review_status='draft'
    assert chapter.review_status == "draft"
    assert chapter.last_reviewed is None
    assert chapter.reviewer_signoffs == []


def test_chapter_reviewed_requires_last_reviewed_and_two_distinct_signoffs():
    # Missing last_reviewed → reject.
    with pytest.raises(ValidationError, match="last_reviewed"):
        _chapter(
            review_status="reviewed",
            reviewer_signoffs=[
                {"reviewer_id": "REV-A", "timestamp": "2026-01-01"},
                {"reviewer_id": "REV-B", "timestamp": "2026-01-01"},
            ],
        )

    # Only one signoff → reject (need ≥2 per CHARTER §6.1).
    with pytest.raises(ValidationError, match="≥2 reviewer_signoffs"):
        _chapter(
            review_status="reviewed",
            last_reviewed="2026-05-01",
            reviewer_signoffs=[
                {"reviewer_id": "REV-A", "timestamp": "2026-01-01"},
            ],
        )

    # Two signoffs from the *same* reviewer → reject. Distinct reviewer
    # identities are the whole point of the two-reviewer gate.
    with pytest.raises(ValidationError, match="distinct reviewers"):
        _chapter(
            review_status="reviewed",
            last_reviewed="2026-05-01",
            reviewer_signoffs=[
                {"reviewer_id": "REV-A", "timestamp": "2026-01-01"},
                {"reviewer_id": "REV-A", "timestamp": "2026-02-01"},
            ],
        )

    # Two distinct reviewers + last_reviewed → accepted.
    chapter = _chapter(
        review_status="reviewed",
        last_reviewed="2026-05-01",
        reviewer_signoffs=[
            {"reviewer_id": "REV-A", "timestamp": "2026-01-01"},
            {"reviewer_id": "REV-B", "timestamp": "2026-02-01"},
        ],
    )
    assert chapter.review_status == "reviewed"
    assert len(chapter.reviewer_signoffs) == 2


def test_chapter_proposed_requires_at_least_one_signoff():
    with pytest.raises(ValidationError, match="≥1 reviewer_signoff"):
        _chapter(review_status="proposed", last_reviewed="2026-05-01")

    chapter = _chapter(
        review_status="proposed",
        last_reviewed="2026-05-01",
        reviewer_signoffs=[{"reviewer_id": "REV-A", "timestamp": "2026-01-01"}],
    )
    assert chapter.review_status == "proposed"


def test_chapter_needs_refresh_requires_last_reviewed():
    with pytest.raises(ValidationError, match="last_reviewed"):
        _chapter(review_status="needs_refresh")
    chapter = _chapter(review_status="needs_refresh", last_reviewed="2024-01-01")
    assert chapter.review_status == "needs_refresh"


def test_chapter_retired_is_permissive_terminal_state():
    chapter = _chapter(review_status="retired")
    assert chapter.review_status == "retired"


def test_handbook_question_status_rules_match_chapter():
    from knowledge_base.schemas.handbook import HandbookQuestion

    base = {
        "id": "HQ-TEST",
        "chapter_id": "HB-TEST",
        "type": "type_a",
        "stem": "?",
        "options": [{"key": "A", "text": "x"}, {"key": "B", "text": "y"}],
        "correct_answer": "A",
        "explanation": "x",
        "source_ids": ["SRC-FAKE"],
    }
    # reviewed without enough signoffs → reject.
    with pytest.raises(ValidationError, match="≥2 reviewer_signoffs"):
        HandbookQuestion(
            **base,
            review_status="reviewed",
            last_reviewed="2026-05-01",
            reviewer_signoffs=[{"reviewer_id": "REV-A", "timestamp": "2026-01-01"}],
        )


def test_loader_flags_unresolved_reviewer_signoff(tmp_path: Path):
    clear_load_cache()
    chapter_dir = tmp_path / "handbook_chapters"
    chapter_dir.mkdir()
    (chapter_dir / "ghost.yaml").write_text(
        """
id: HB-GHOST
title: Ghost
learning_objectives:
  - "x"
at_a_glance:
  - "x"
source_ids:
  - SRC-FAKE
review_status: proposed
last_reviewed: "2026-05-01"
reviewer_signoffs:
  - reviewer_id: REV-DOES-NOT-EXIST
    timestamp: "2026-05-01"
""",
        encoding="utf-8",
    )

    result = load_content(tmp_path)
    messages = "\n".join(message for _, message in result.ref_errors)
    assert "reviewer_signoffs[0].reviewer_id" in messages
    assert "REV-DOES-NOT-EXIST" in messages


def test_loader_warns_on_stale_reviewed_handbook(tmp_path: Path):
    from knowledge_base.validation.loader import HANDBOOK_REVIEW_STALE_DAYS
    clear_load_cache()
    chapter_dir = tmp_path / "handbook_chapters"
    chapter_dir.mkdir()
    # Two distinct REV-* peers so the schema accepts review_status=reviewed.
    reviewers_dir = tmp_path / "reviewers"
    reviewers_dir.mkdir()
    for rid, name in [("REV-X", "X"), ("REV-Y", "Y")]:
        (reviewers_dir / f"{rid.lower()}.yaml").write_text(
            f"""
id: {rid}
name:
  preferred: "{name} Reviewer"
  ukrainian: "{name}"
  english: "{name} Reviewer"
  suffix: "MD"
specialty: "Test"
qualifications: []
sign_off_scope: {{}}
last_active: "2026-01-01"
""",
            encoding="utf-8",
        )
    (chapter_dir / "stale.yaml").write_text(
        """
id: HB-STALE
title: Old chapter
learning_objectives:
  - "x"
at_a_glance:
  - "x"
source_ids:
  - SRC-FAKE
review_status: reviewed
last_reviewed: "2020-01-01"
reviewer_signoffs:
  - reviewer_id: REV-X
    timestamp: "2020-01-01"
  - reviewer_id: REV-Y
    timestamp: "2020-01-01"
""",
        encoding="utf-8",
    )

    result = load_content(tmp_path)
    messages = "\n".join(message for _, message in result.contract_warnings)
    assert "HB-STALE" in messages
    assert f">{HANDBOOK_REVIEW_STALE_DAYS}-day threshold" in messages
    assert "needs_refresh" in messages


def test_loader_emits_draft_review_warning_on_seed():
    """The four seed chapters are still drafts; the loader surfaces them
    as needs-clinical-review so contributors see them without scanning
    each YAML."""
    result = load_content(KB_ROOT)
    messages = [m for _, m in result.contract_warnings if "handbook draft" in m]
    chapter_ids_in_warnings = {m.split(":", 1)[0].strip() for m in messages}
    assert {"HB-DLBCL-1L", "HB-CRC-METASTATIC-1L", "HB-MM-1L", "HB-NSCLC-METASTATIC-1L"}.issubset(
        chapter_ids_in_warnings
    )


def test_chapter_page_renders_review_panel(tmp_path: Path):
    build_handbook(KB_ROOT, tmp_path)
    chapter_html = (tmp_path / "handbook" / "hb-dlbcl-1l.html").read_text(encoding="utf-8")

    # Status-aware badge class for the seed draft chapter.
    assert 'hb-badge hb-badge--draft' in chapter_html
    # Sidebar review panel present.
    assert "hb-review-panel" in chapter_html
    assert "Clinical sign-offs" in chapter_html
    assert "No clinical sign-offs recorded yet" in chapter_html
    assert "not yet reviewed" in chapter_html
    # Spec link present so reviewers can find the rules.
    assert "HANDBOOK_MODE_SPEC §4" in chapter_html


def test_is_stale_review_helper():
    from scripts.build_handbook import _is_stale_review
    # Draft never stale even if last_reviewed is ancient.
    assert _is_stale_review("draft", "2020-01-01") is False
    # reviewed + recent date → not stale.
    from datetime import date, timedelta
    recent = (date.today() - timedelta(days=10)).isoformat()
    old = (date.today() - timedelta(days=500)).isoformat()
    assert _is_stale_review("reviewed", recent) is False
    assert _is_stale_review("reviewed", old) is True
    # Missing or malformed → not stale (loader handles the validation).
    assert _is_stale_review("reviewed", None) is False
    assert _is_stale_review("reviewed", "not-a-date") is False
