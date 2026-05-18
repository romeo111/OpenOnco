"""Build the OpenOnco Handbook static pages.

The handbook is a deterministic educational layer over checked-in YAML.
It deliberately does not ingest or rewrite third-party handbook text.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from knowledge_base.validation.loader import load_content  # noqa: E402

DEFAULT_KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "docs"


def _esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _slug(entity_id: str) -> str:
    return entity_id.lower().replace("_", "-")


def _entity_label(entity: dict[str, Any] | None, fallback: str) -> str:
    if not entity:
        return fallback
    data = entity.get("data") or {}
    names = data.get("names")
    if isinstance(names, dict):
        return str(names.get("english") or names.get("preferred") or fallback)
    for key in ("title", "name", "display_name", "definition"):
        if data.get(key):
            return str(data[key])
    return fallback


def _source_ids_from_question(question: dict[str, Any]) -> list[str]:
    return [sid for sid in question.get("source_ids") or [] if isinstance(sid, str)]


def _chapter_questions(load, chapter_id: str) -> list[dict[str, Any]]:
    questions = []
    for info in load.entities_by_id.values():
        if info["type"] != "handbook_questions":
            continue
        data = info["data"]
        if data.get("chapter_id") == chapter_id:
            questions.append(data)
    return sorted(questions, key=lambda q: q["id"])


def _chapter_cards(load) -> list[dict[str, Any]]:
    chapters = [
        info["data"]
        for info in load.entities_by_id.values()
        if info["type"] == "handbook_chapters"
    ]
    return sorted(chapters, key=lambda chapter: chapter["title"].lower())


def _render_badge(text: str, class_name: str = "") -> str:
    cls = "hb-badge" + (f" {class_name}" if class_name else "")
    return f'<span class="{cls}">{_esc(text)}</span>'


def _chapter_index_record(load, chapter: dict[str, Any]) -> dict[str, Any]:
    """Per-chapter record carried in handbook_index.json and inlined into
    the index page for client-side filter/search. Adds a few resolved
    labels to keep the search UI working without a second fetch."""
    questions = _chapter_questions(load, chapter["id"])
    disease_labels = [
        _entity_label(load.entities_by_id.get(did), did)
        for did in chapter.get("disease_ids") or []
    ]
    return {
        "id": chapter["id"],
        "title": chapter["title"],
        "review_status": chapter.get("review_status", "draft"),
        "url": f"/handbook/{_slug(chapter['id'])}.html",
        "question_count": len(questions),
        "source_ids": list(chapter.get("source_ids") or []),
        "disease_ids": list(chapter.get("disease_ids") or []),
        "disease_labels": disease_labels,
        "topic_tags": list(chapter.get("topic_tags") or []),
        "learning_objectives": list(chapter.get("learning_objectives") or []),
        "at_a_glance": list(chapter.get("at_a_glance") or []),
    }


def _search_blob(record: dict[str, Any]) -> str:
    """Lowercased haystack for substring search. Includes the fields the
    handoff names: title, learning objectives, at-a-glance bullets,
    source IDs, disease labels."""
    parts: list[str] = [record.get("title") or "", record.get("id") or ""]
    parts.extend(record.get("learning_objectives") or [])
    parts.extend(record.get("at_a_glance") or [])
    parts.extend(record.get("source_ids") or [])
    parts.extend(record.get("disease_ids") or [])
    parts.extend(record.get("disease_labels") or [])
    parts.extend(record.get("topic_tags") or [])
    return " \n ".join(p for p in parts if p).lower()


def _render_source_list(load, source_ids: list[str]) -> str:
    items = []
    for sid in source_ids:
        source = load.entities_by_id.get(sid)
        label = _entity_label(source, sid)
        items.append(f"<li><code>{_esc(sid)}</code> {_esc(label)}</li>")
    return "<ul>" + "".join(items) + "</ul>"


def _render_entity_chips(load, entity_ids: list[str]) -> str:
    chips = []
    for entity_id in entity_ids:
        entity = load.entities_by_id.get(entity_id)
        label = _entity_label(entity, entity_id)
        etype = entity["type"] if entity else "entity"
        chips.append(
            '<span class="hb-chip">'
            f"<code>{_esc(entity_id)}</code>"
            f"<span>{_esc(label)}</span>"
            f'<small>{_esc(etype)}</small>'
            "</span>"
        )
    return '<div class="hb-chip-grid">' + "".join(chips) + "</div>"


def _correct_keys(question: dict[str, Any]) -> list[str]:
    """Normalize `correct_answer` (e.g. "A" or "A,B,D") into a sorted list
    of option keys. Empty for short_answer (free-text) questions."""
    raw = question.get("correct_answer")
    if raw is None:
        return []
    keys = [k.strip().upper() for k in str(raw).replace("|", ",").split(",") if k.strip()]
    return sorted(set(keys))


def _question_input_type(question_type: str) -> str:
    """type_k is multi-select; type_a/mcq are single best answer."""
    return "checkbox" if question_type == "type_k" else "radio"


def _render_question(question: dict[str, Any], ordinal: int) -> str:
    """Render one practice question as an interactive quiz form.

    Per Phase 3 of the handbook handoff: replaces the old reveal-toggle
    with a real self-check workflow — pick an answer, submit, see
    correct/incorrect + explanation + source IDs. Multi-select (type_k)
    correctness is set-equality: every correct key chosen, no extras.
    short_answer falls back to a reveal-only "model answer" panel
    because we can't grade free text in JS.
    """
    qtype = question.get("type") or "type_a"
    qid = question.get("id") or ""
    correct_keys = _correct_keys(question)
    correct_attr = "|".join(correct_keys)
    input_type = _question_input_type(qtype)

    is_short_answer = qtype == "short_answer"

    if is_short_answer:
        controls_html = f"""
          <label class="hb-option hb-option--short">
            <span>Your answer (free text — not graded)</span>
            <input type="text" name="hb-answer-{_esc(qid)}" autocomplete="off">
          </label>
        """
        buttons_html = """
          <button type="button" class="hb-btn hb-btn--reveal" data-action="reveal">Reveal model answer</button>
        """
    else:
        option_rows = []
        for option in question.get("options") or []:
            key = (option.get("key") or "").upper()
            option_rows.append(
                f"""
                <label class="hb-option">
                  <input type="{input_type}" name="hb-answer-{_esc(qid)}" value="{_esc(key)}">
                  <span class="hb-option-key">{_esc(key)}.</span>
                  <span class="hb-option-text">{_esc(option.get('text'))}</span>
                </label>
                """
            )
        controls_html = f'<div class="hb-options">{"".join(option_rows)}</div>'
        buttons_html = """
          <button type="submit" class="hb-btn hb-btn--submit" data-action="submit">Submit answer</button>
          <button type="button" class="hb-btn hb-btn--reset" data-action="reset">Reset</button>
        """

    source_chips = "".join(
        f'<code class="hb-result-source">{_esc(sid)}</code>'
        for sid in question.get("source_ids") or []
    )
    reasoning_chips = "".join(
        f'<span class="hb-result-tag">{_esc(tag)}</span>'
        for tag in question.get("tests_reasoning") or []
    )
    reasoning_html = (
        f'<div class="hb-result-tags">Reasoning tags: {reasoning_chips}</div>'
        if reasoning_chips
        else ""
    )
    correct_text = (
        "" if is_short_answer else f"<strong>Correct answer:</strong> {_esc(', '.join(correct_keys))}"
    )

    return f"""
      <form class="hb-question"
            data-question-id="{_esc(qid)}"
            data-question-type="{_esc(qtype)}"
            data-correct-answer="{_esc(correct_attr)}"
            data-graded="{('false' if is_short_answer else 'true')}"
            novalidate>
        <div class="hb-question-top">
          <span class="hb-question-ord">Question {ordinal}</span>
          {_render_badge(qtype)}
          {_render_badge(question.get('difficulty', 'intermediate'))}
          <span class="hb-question-id"><code>{_esc(qid)}</code></span>
        </div>
        <p class="hb-question-stem">{_esc(question.get('stem'))}</p>
        {controls_html}
        <div class="hb-question-buttons">
          {buttons_html}
          <span class="hb-question-status" data-role="status" aria-live="polite"></span>
        </div>
        <div class="hb-result" hidden>
          <p class="hb-result-headline" data-role="headline">{correct_text}</p>
          <p class="hb-result-explanation">{_esc(question.get('explanation'))}</p>
          <div class="hb-result-sources"><span>Sources:</span> {source_chips or '<em>none</em>'}</div>
          {reasoning_html}
        </div>
      </form>
    """


def _page_shell(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{_esc(title)} - OpenOnco Handbook</title>
  <link rel="stylesheet" href="/style.css">
  <style>
    .hb-wrap {{ max-width: 1120px; margin: 0 auto; padding: 28px 20px 56px; }}
    .hb-kicker {{ color: #4b5563; font-size: 13px; font-weight: 700; text-transform: uppercase; }}
    .hb-hero {{ display: grid; gap: 14px; border-bottom: 1px solid #d6dee8; padding-bottom: 22px; }}
    .hb-hero h1 {{ margin: 0; font-size: 34px; line-height: 1.08; }}
    .hb-lead {{ max-width: 820px; color: #334155; font-size: 17px; line-height: 1.55; }}
    .hb-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 24px; }}
    .hb-card, .hb-panel, .hb-question {{ border: 1px solid #d6dee8; border-radius: 8px; background: #fff; padding: 16px; }}
    .hb-card h2, .hb-panel h2 {{ margin-top: 0; font-size: 20px; }}
    .hb-card a {{ color: #0f766e; font-weight: 700; text-decoration: none; }}
    .hb-meta {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }}
    .hb-badge {{ display: inline-flex; align-items: center; border: 1px solid #cbd5e1; border-radius: 999px; padding: 3px 8px; font-size: 12px; background: #f8fafc; color: #334155; }}
    .hb-badge--draft {{ border-color: #f59e0b; background: #fffbeb; color: #92400e; }}
    .hb-layout {{ display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 22px; margin-top: 24px; }}
    .hb-main {{ display: grid; gap: 18px; }}
    .hb-side {{ display: grid; gap: 16px; align-content: start; }}
    .hb-chip-grid {{ display: grid; gap: 8px; }}
    .hb-chip {{ display: grid; gap: 3px; border: 1px solid #d6dee8; border-radius: 6px; padding: 8px; }}
    .hb-chip small {{ color: #64748b; }}
    .hb-question {{ display: grid; gap: 10px; }}
    .hb-question-top {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
    .hb-question-id {{ margin-left: auto; font-size: 12px; color: #64748b; }}
    .hb-question-stem {{ margin: 0; font-size: 15px; line-height: 1.5; color: #0f172a; }}
    .hb-options {{ display: grid; gap: 6px; }}
    .hb-option {{ display: grid; grid-template-columns: auto auto 1fr; gap: 8px; align-items: start; padding: 8px 10px; border: 1px solid #e2e8f0; border-radius: 6px; cursor: pointer; transition: border-color .12s, background .12s; }}
    .hb-option:hover {{ border-color: #99f6e4; background: #f0fdfa; }}
    .hb-option input {{ margin-top: 3px; }}
    .hb-option-key {{ font-weight: 700; color: #115e59; }}
    .hb-option--short {{ grid-template-columns: 1fr; }}
    .hb-option--short input {{ font: inherit; padding: 7px 9px; border: 1px solid #cbd5e1; border-radius: 6px; }}
    .hb-question-buttons {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
    .hb-question-status {{ font-size: 13px; color: #475569; }}
    .hb-btn {{ font: inherit; cursor: pointer; padding: 7px 12px; border-radius: 6px; border: 1px solid #0f766e; background: #0f766e; color: #fff; }}
    .hb-btn--reset, .hb-btn--ghost {{ background: transparent; color: #0f766e; }}
    .hb-btn--reveal {{ background: #475569; border-color: #475569; }}
    .hb-result {{ margin-top: 4px; padding: 12px; border-left: 4px solid #0f766e; border-radius: 6px; background: #f8fafc; color: #1f2937; }}
    .hb-result--correct {{ border-left-color: #16a34a; background: #f0fdf4; }}
    .hb-result--incorrect {{ border-left-color: #dc2626; background: #fef2f2; }}
    .hb-result--reveal {{ border-left-color: #475569; background: #f1f5f9; }}
    .hb-result-headline {{ margin: 0 0 6px; font-weight: 600; }}
    .hb-result-explanation {{ margin: 0 0 8px; }}
    .hb-result-sources {{ display: flex; flex-wrap: wrap; gap: 6px; align-items: center; font-size: 13px; color: #475569; }}
    .hb-result-source {{ background: #fff; border: 1px solid #cbd5e1; border-radius: 4px; padding: 2px 6px; }}
    .hb-result-tags {{ margin-top: 6px; font-size: 12px; color: #475569; }}
    .hb-result-tag {{ display: inline-block; background: #e0f2fe; border-radius: 999px; padding: 2px 8px; margin-right: 4px; color: #075985; }}
    .hb-quiz-header {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 8px; }}
    .hb-quiz-header h2 {{ margin: 0; }}
    .hb-quiz-tools {{ display: flex; align-items: center; gap: 10px; }}
    .hb-score {{ font-size: 13px; color: #0f172a; background: #f1f5f9; padding: 4px 10px; border-radius: 999px; }}
    .hb-quiz-note {{ margin: 6px 0 12px; font-size: 13px; color: #475569; }}
    .hb-disclaimer {{ border-left: 4px solid #f59e0b; background: #fffbeb; padding: 12px; color: #78350f; }}
    .hb-controls {{ display: grid; grid-template-columns: minmax(220px, 2fr) repeat(3, minmax(150px, 1fr)); gap: 10px 14px; align-items: end; margin-top: 22px; padding: 14px; border: 1px solid #d6dee8; border-radius: 8px; background: #f8fafc; }}
    .hb-control {{ display: grid; gap: 4px; font-size: 12px; color: #475569; }}
    .hb-control span {{ font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }}
    .hb-control input, .hb-control select {{ font: inherit; padding: 7px 9px; border: 1px solid #cbd5e1; border-radius: 6px; background: #fff; color: #0f172a; }}
    .hb-control input:focus, .hb-control select:focus {{ outline: 2px solid #0f766e; outline-offset: 1px; }}
    .hb-result-count {{ grid-column: 1 / -1; margin: 4px 0 0; font-size: 13px; color: #475569; }}
    .hb-empty {{ grid-column: 1 / -1; margin: 0; padding: 12px; border: 1px dashed #cbd5e1; border-radius: 6px; background: #fff; color: #475569; text-align: center; }}
    .hb-tag-row {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }}
    .hb-tag {{ display: inline-flex; padding: 2px 8px; font-size: 11px; border-radius: 999px; background: #e0f2f1; color: #115e59; border: 1px solid #99f6e4; }}
    @media (max-width: 860px) {{ .hb-layout {{ grid-template-columns: 1fr; }} .hb-hero h1 {{ font-size: 28px; }} .hb-controls {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <main class="hb-wrap">
    {body}
  </main>
</body>
</html>
"""


def render_handbook_index(load) -> str:
    chapters = _chapter_cards(load)
    records = [_chapter_index_record(load, chapter) for chapter in chapters]

    cards = []
    for chapter, record in zip(chapters, records):
        chapter_href = f"handbook/{_slug(chapter['id'])}.html"
        diseases_attr = "|".join(record["disease_ids"])
        tags_attr = "|".join(record["topic_tags"])
        search_attr = _search_blob(record)
        cards.append(
            f"""
            <article class="hb-card"
                     data-id="{_esc(record['id'])}"
                     data-diseases="{_esc(diseases_attr)}"
                     data-tags="{_esc(tags_attr)}"
                     data-status="{_esc(record['review_status'])}"
                     data-search="{_esc(search_attr)}">
              <h2><a href="{_esc(chapter_href)}">{_esc(record['title'])}</a></h2>
              <p>{_esc('; '.join(record['learning_objectives'])[:260])}</p>
              <div class="hb-meta">
                {_render_badge(record['review_status'], 'hb-badge--draft')}
                {_render_badge(f"{record['question_count']} questions")}
                {_render_badge(", ".join(record['disease_labels']) or "no disease")}
              </div>
              <div class="hb-tag-row">
                {''.join(f'<span class="hb-tag">{_esc(t)}</span>' for t in record['topic_tags'])}
              </div>
            </article>
            """
        )

    # Sorted union of values for each filter, so the UI is deterministic
    # across builds.
    all_diseases = sorted(
        {(did, label) for r in records for did, label in zip(r["disease_ids"], r["disease_labels"])}
    )
    all_tags = sorted({t for r in records for t in r["topic_tags"]})
    all_statuses = sorted({r["review_status"] for r in records})

    disease_options = "".join(
        f'<option value="{_esc(did)}">{_esc(label or did)}</option>'
        for did, label in all_diseases
    )
    tag_options = "".join(f'<option value="{_esc(t)}">{_esc(t)}</option>' for t in all_tags)
    status_options = "".join(f'<option value="{_esc(s)}">{_esc(s)}</option>' for s in all_statuses)

    body = f"""
    <section class="hb-hero">
      <div class="hb-kicker">OpenOnco Handbook</div>
      <h1>Source-grounded oncology learning chapters</h1>
      <p class="hb-lead">Educational chapters generated from checked-in OpenOnco
      YAML entities, source IDs, synthetic cases, and review metadata. This is
      not official ESMO content and does not grant CME credit.</p>
    </section>
    <section class="hb-controls" aria-label="Filter and search chapters">
      <label class="hb-control hb-control--search">
        <span>Search</span>
        <input type="search" id="hb-search" placeholder="Title, objective, source ID…" autocomplete="off">
      </label>
      <label class="hb-control">
        <span>Disease</span>
        <select id="hb-filter-disease">
          <option value="">All diseases</option>
          {disease_options}
        </select>
      </label>
      <label class="hb-control">
        <span>Topic tag</span>
        <select id="hb-filter-tag">
          <option value="">All tags</option>
          {tag_options}
        </select>
      </label>
      <label class="hb-control">
        <span>Review status</span>
        <select id="hb-filter-status">
          <option value="">All statuses</option>
          {status_options}
        </select>
      </label>
      <p class="hb-result-count" id="hb-result-count" aria-live="polite"></p>
      <p class="hb-empty" id="hb-empty" hidden>No chapters match the current filters.</p>
    </section>
    <section class="hb-grid" id="hb-grid">
      {''.join(cards) or '<p>No handbook chapters are authored yet.</p>'}
    </section>
    <script>
      (function() {{
        var cards = Array.prototype.slice.call(document.querySelectorAll('#hb-grid .hb-card'));
        var total = cards.length;
        var search = document.getElementById('hb-search');
        var disease = document.getElementById('hb-filter-disease');
        var tag = document.getElementById('hb-filter-tag');
        var status = document.getElementById('hb-filter-status');
        var count = document.getElementById('hb-result-count');
        var empty = document.getElementById('hb-empty');
        if (!search || !disease || !tag || !status) {{ return; }}
        function listFor(card, name) {{
          var v = card.getAttribute('data-' + name) || '';
          return v ? v.split('|') : [];
        }}
        function apply() {{
          var q = (search.value || '').trim().toLowerCase();
          var d = disease.value;
          var t = tag.value;
          var s = status.value;
          var visible = 0;
          cards.forEach(function(card) {{
            var diseases = listFor(card, 'diseases');
            var tags = listFor(card, 'tags');
            var blob = card.getAttribute('data-search') || '';
            var show = true;
            if (q && blob.indexOf(q) === -1) {{ show = false; }}
            if (show && d && diseases.indexOf(d) === -1) {{ show = false; }}
            if (show && t && tags.indexOf(t) === -1) {{ show = false; }}
            if (show && s && card.getAttribute('data-status') !== s) {{ show = false; }}
            card.hidden = !show;
            if (show) {{ visible += 1; }}
          }});
          count.textContent = visible + ' of ' + total + ' chapter' + (total === 1 ? '' : 's');
          empty.hidden = visible !== 0;
        }}
        [search, disease, tag, status].forEach(function(el) {{
          el.addEventListener('input', apply);
          el.addEventListener('change', apply);
        }});
        apply();
      }})();
    </script>
    """
    return _page_shell("OpenOnco Handbook", body)


def render_chapter(load, chapter: dict[str, Any]) -> str:
    questions = _chapter_questions(load, chapter["id"])
    at_a_glance = "".join(f"<li>{_esc(item)}</li>" for item in chapter.get("at_a_glance") or [])
    objectives = "".join(
        f"<li>{_esc(item)}</li>" for item in chapter.get("learning_objectives") or []
    )
    sections = []
    for section in chapter.get("sections") or []:
        sections.append(
            f"""
            <section class="hb-panel">
              <h2>{_esc(section.get('heading'))}</h2>
              <p>{_esc(section.get('body'))}</p>
              <h3>Linked entities</h3>
              {_render_entity_chips(load, section.get('linked_entity_ids') or [])}
              <h3>Section sources</h3>
              {_render_source_list(load, section.get('source_ids') or [])}
            </section>
            """
        )
    cases = []
    for case in chapter.get("case_links") or []:
        focuses = ", ".join(case.get("learning_focus") or [])
        cases.append(
            f"<li><code>{_esc(case.get('id'))}</code> "
            f"{_esc(case.get('title'))} - <span>{_esc(focuses)}</span> "
            f"<small>{_esc(case.get('path'))}</small></li>"
        )
    question_html = "".join(
        _render_question(question, index + 1) for index, question in enumerate(questions)
    )
    graded_questions = [q for q in questions if (q.get("type") or "type_a") != "short_answer"]
    graded_total = len(graded_questions)
    linked_all = []
    for values in (chapter.get("linked_entities") or {}).values():
        if isinstance(values, list):
            linked_all.extend(values)
    body = f"""
    <section class="hb-hero">
      <div class="hb-kicker"><a href="/handbook.html">OpenOnco Handbook</a></div>
      <h1>{_esc(chapter['title'])}</h1>
      <div class="hb-meta">
        {_render_badge(chapter.get('review_status', 'draft'), 'hb-badge--draft')}
        {_render_badge(chapter.get('audience', 'hcp_learner'))}
        {_render_badge(chapter.get('language', 'en'))}
      </div>
      <p class="hb-lead">Deterministic learning chapter over OpenOnco KB entities,
      synthetic cases, and source records.</p>
    </section>
    <div class="hb-layout">
      <div class="hb-main">
        <section class="hb-panel">
          <h2>Learning objectives</h2>
          <ol>{objectives}</ol>
        </section>
        <section class="hb-panel">
          <h2>At a glance</h2>
          <ul>{at_a_glance}</ul>
        </section>
        {''.join(sections)}
        <section class="hb-panel">
          <h2>Worked synthetic cases</h2>
          <ul>{''.join(cases) or '<li>No cases linked yet.</li>'}</ul>
        </section>
        <section class="hb-panel hb-quiz">
          <div class="hb-quiz-header">
            <h2>Practice questions</h2>
            <div class="hb-quiz-tools">
              <span class="hb-score" id="hb-score" aria-live="polite">0 of {graded_total} answered · 0 correct</span>
              <button type="button" class="hb-btn hb-btn--ghost" id="hb-quiz-reset">Reset quiz</button>
            </div>
          </div>
          <p class="hb-quiz-note">Answers, score, and reasoning tags are kept in your
          browser session only and clear when you close this tab. Multi-select
          questions require every correct option (and no extras) for a credit.</p>
          {question_html or '<p>No questions linked yet.</p>'}
        </section>
      </div>
      <aside class="hb-side">
        <section class="hb-panel hb-disclaimer">
          <strong>Educational use only.</strong>
          <p>This OpenOnco-authored chapter is not official ESMO material,
          not a CME-credit activity, and not patient-specific medical advice.</p>
        </section>
        <section class="hb-panel">
          <h2>Chapter sources</h2>
          {_render_source_list(load, chapter.get('source_ids') or [])}
        </section>
        <section class="hb-panel">
          <h2>Entity map</h2>
          {_render_entity_chips(load, linked_all)}
        </section>
      </aside>
    </div>
    <script>
      (function() {{
        var CHAPTER_ID = {json.dumps(chapter['id'])};
        var GRADED_TOTAL = {graded_total};
        var STORAGE_KEY = 'openonco-handbook-' + CHAPTER_ID + '-quiz';
        var forms = Array.prototype.slice.call(document.querySelectorAll('.hb-quiz .hb-question'));
        var scoreEl = document.getElementById('hb-score');
        var resetAllBtn = document.getElementById('hb-quiz-reset');
        var storage;
        try {{ storage = window.sessionStorage; }} catch (e) {{ storage = null; }}
        var state = {{}};
        if (storage) {{
          try {{ state = JSON.parse(storage.getItem(STORAGE_KEY) || '{{}}') || {{}}; }} catch (e) {{ state = {{}}; }}
        }}
        function persist() {{
          if (!storage) {{ return; }}
          try {{ storage.setItem(STORAGE_KEY, JSON.stringify(state)); }} catch (e) {{}}
        }}
        function normalize(list) {{
          return (list || []).map(function(k) {{ return String(k).toUpperCase(); }}).slice().sort().join('|');
        }}
        function updateScore() {{
          var answered = 0;
          var correct = 0;
          Object.keys(state).forEach(function(qid) {{
            var entry = state[qid];
            if (entry && entry.submitted && entry.graded) {{
              answered += 1;
              if (entry.correct) {{ correct += 1; }}
            }}
          }});
          if (scoreEl) {{
            scoreEl.textContent = answered + ' of ' + GRADED_TOTAL + ' answered · ' + correct + ' correct';
          }}
        }}
        forms.forEach(function(form) {{
          var qid = form.getAttribute('data-question-id');
          var qtype = form.getAttribute('data-question-type');
          var graded = form.getAttribute('data-graded') === 'true';
          var correctAttr = form.getAttribute('data-correct-answer') || '';
          var correctKey = correctAttr.split('|').filter(Boolean).slice().sort().join('|');
          var resultEl = form.querySelector('.hb-result');
          var headlineEl = form.querySelector('[data-role="headline"]');
          var statusEl = form.querySelector('[data-role="status"]');
          var submitBtn = form.querySelector('[data-action="submit"]');
          var resetBtn = form.querySelector('[data-action="reset"]');
          var revealBtn = form.querySelector('[data-action="reveal"]');
          function selectedKeys() {{
            return Array.prototype.slice.call(
              form.querySelectorAll('input[type=radio]:checked, input[type=checkbox]:checked')
            ).map(function(input) {{ return input.value; }});
          }}
          function setResultClass(isCorrect) {{
            resultEl.classList.remove('hb-result--correct', 'hb-result--incorrect', 'hb-result--reveal');
            if (isCorrect === true) {{ resultEl.classList.add('hb-result--correct'); }}
            else if (isCorrect === false) {{ resultEl.classList.add('hb-result--incorrect'); }}
            else {{ resultEl.classList.add('hb-result--reveal'); }}
          }}
          function showResult(entry) {{
            resultEl.hidden = false;
            if (graded) {{
              setResultClass(entry.correct);
              if (statusEl) {{
                statusEl.textContent = entry.correct ? '✓ Correct' : '✗ Not yet — see explanation';
              }}
            }} else {{
              setResultClass(null);
              if (statusEl) {{ statusEl.textContent = 'Model answer revealed'; }}
            }}
          }}
          function clearResult() {{
            resultEl.hidden = true;
            resultEl.classList.remove('hb-result--correct', 'hb-result--incorrect', 'hb-result--reveal');
            if (statusEl) {{ statusEl.textContent = ''; }}
          }}
          function rehydrate() {{
            var entry = state[qid];
            if (!entry) {{ return; }}
            (entry.selected || []).forEach(function(key) {{
              var input = form.querySelector('input[value="' + key + '"]');
              if (input) {{ input.checked = true; }}
            }});
            if (entry.submitted) {{ showResult(entry); }}
          }}
          function submitGraded(event) {{
            if (event && event.preventDefault) {{ event.preventDefault(); }}
            var selected = selectedKeys();
            if (selected.length === 0) {{
              if (statusEl) {{ statusEl.textContent = 'Pick an option first.'; }}
              return;
            }}
            var selectedKey = normalize(selected);
            var isCorrect = selectedKey === correctKey;
            state[qid] = {{ submitted: true, graded: true, selected: selected, correct: isCorrect }};
            persist();
            showResult(state[qid]);
            updateScore();
          }}
          function revealOnly(event) {{
            if (event && event.preventDefault) {{ event.preventDefault(); }}
            state[qid] = {{ submitted: true, graded: false, selected: [], correct: null }};
            persist();
            showResult(state[qid]);
            updateScore();
          }}
          function resetQuestion(event) {{
            if (event && event.preventDefault) {{ event.preventDefault(); }}
            Array.prototype.slice.call(form.querySelectorAll('input')).forEach(function(input) {{
              if (input.type === 'radio' || input.type === 'checkbox') {{ input.checked = false; }}
              else {{ input.value = ''; }}
            }});
            delete state[qid];
            persist();
            clearResult();
            updateScore();
          }}
          if (submitBtn) {{ submitBtn.addEventListener('click', submitGraded); }}
          if (resetBtn) {{ resetBtn.addEventListener('click', resetQuestion); }}
          if (revealBtn) {{ revealBtn.addEventListener('click', revealOnly); }}
          form.addEventListener('submit', function(event) {{ event.preventDefault(); if (graded) {{ submitGraded(event); }} }});
          rehydrate();
        }});
        if (resetAllBtn) {{
          resetAllBtn.addEventListener('click', function() {{
            state = {{}};
            persist();
            forms.forEach(function(form) {{
              Array.prototype.slice.call(form.querySelectorAll('input')).forEach(function(input) {{
                if (input.type === 'radio' || input.type === 'checkbox') {{ input.checked = false; }}
                else {{ input.value = ''; }}
              }});
              var resultEl = form.querySelector('.hb-result');
              var statusEl = form.querySelector('[data-role="status"]');
              if (resultEl) {{
                resultEl.hidden = true;
                resultEl.classList.remove('hb-result--correct', 'hb-result--incorrect', 'hb-result--reveal');
              }}
              if (statusEl) {{ statusEl.textContent = ''; }}
            }});
            updateScore();
          }});
        }}
        updateScore();
      }})();
    </script>
    """
    return _page_shell(chapter["title"], body)


def build_handbook(kb_root: Path = DEFAULT_KB_ROOT, output_dir: Path = DEFAULT_OUTPUT_DIR) -> dict:
    load = load_content(kb_root)
    if not load.ok:
        raise RuntimeError(
            "KB did not validate: "
            f"{len(load.schema_errors)} schema, {len(load.ref_errors)} refs, "
            f"{len(load.contract_errors)} contracts"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    chapter_dir = output_dir / "handbook"
    chapter_dir.mkdir(parents=True, exist_ok=True)

    chapters = _chapter_cards(load)
    for chapter in chapters:
        (chapter_dir / f"{_slug(chapter['id'])}.html").write_text(
            render_chapter(load, chapter),
            encoding="utf-8",
        )
    (output_dir / "handbook.html").write_text(render_handbook_index(load), encoding="utf-8")

    payload = {
        "kind": "openonco_handbook_index",
        "count": len(chapters),
        "chapters": [_chapter_index_record(load, chapter) for chapter in chapters],
    }
    (output_dir / "handbook_index.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build OpenOnco Handbook static pages.")
    parser.add_argument("--kb-root", type=Path, default=DEFAULT_KB_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)
    payload = build_handbook(args.kb_root, args.output_dir)
    print(f"Built {payload['count']} handbook chapter(s) into {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
