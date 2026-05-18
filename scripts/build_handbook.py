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


def _render_question(question: dict[str, Any], ordinal: int) -> str:
    options = []
    for option in question.get("options") or []:
        options.append(
            "<li>"
            f'<strong>{_esc(option.get("key"))}.</strong> {_esc(option.get("text"))}'
            "</li>"
        )
    options_html = "<ol>" + "".join(options) + "</ol>" if options else ""
    return f"""
      <article class="hb-question" data-answer="{_esc(question.get('correct_answer'))}">
        <div class="hb-question-top">
          <span>Question {ordinal}</span>
          {_render_badge(question.get("type", "question"))}
          {_render_badge(question.get("difficulty", "intermediate"))}
        </div>
        <p>{_esc(question.get("stem"))}</p>
        {options_html}
        <button type="button" class="hb-answer-toggle">Show answer</button>
        <div class="hb-answer" hidden>
          <strong>Answer: {_esc(question.get("correct_answer"))}</strong>
          <p>{_esc(question.get("explanation"))}</p>
        </div>
      </article>
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
    .hb-question-top {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 8px; }}
    .hb-answer-toggle {{ border: 1px solid #0f766e; background: #0f766e; color: #fff; border-radius: 6px; padding: 7px 10px; cursor: pointer; }}
    .hb-answer {{ margin-top: 12px; border-left: 3px solid #0f766e; padding-left: 12px; color: #1f2937; }}
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
  <script>
    document.querySelectorAll('.hb-answer-toggle').forEach((button) => {{
      button.addEventListener('click', () => {{
        const answer = button.parentElement.querySelector('.hb-answer');
        answer.hidden = !answer.hidden;
        button.textContent = answer.hidden ? 'Show answer' : 'Hide answer';
      }});
    }});
  </script>
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
        <section class="hb-panel">
          <h2>Practice questions</h2>
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
