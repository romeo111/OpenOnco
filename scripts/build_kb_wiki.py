"""Deterministic static KB browser for OpenOnco.

This is intentionally not an LLM-authored medical wiki. It renders a
human-facing browser over the existing source-grounded YAML knowledge base:
entity facts, source IDs, file provenance, and reverse references.
"""

from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ENTITY_DIRS = {
    "drugs": "Drug",
    "biomarkers": "Biomarker",
    "redflags": "Red flag",
    "biomarker_actionability": "Actionability",
}

SEARCH_KINDS = set(ENTITY_DIRS)
ID_RE = re.compile(r"\b(?:DRUG|BIO|BMA|RF|DIS|REG|IND|ALGO|SRC|CI|SUP|TEST|MON)-[A-Z0-9][A-Z0-9_-]*\b")


@dataclass(frozen=True)
class KbEntity:
    kind: str
    kind_label: str
    id: str
    title: str
    data: dict[str, Any]
    path: Path
    rel_path: str

    @property
    def url(self) -> str:
        return f"kb/{self.kind}/{slugify(self.id)}.html"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "entity"


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _text(value: Any, *, limit: int | None = None) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True)
    text = " ".join(str(value).split())
    if limit and len(text) > limit:
        return text[: limit - 1].rstrip() + "..."
    return text


def _load_yaml(path: Path) -> dict[str, Any] | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    if not data.get("id"):
        return None
    return data


def _name_from_data(data: dict[str, Any]) -> str:
    names = data.get("names")
    if isinstance(names, dict):
        for key in ("preferred", "english", "ukrainian"):
            if names.get(key):
                return str(names[key])
    for key in ("title", "definition", "evidence_summary", "name"):
        if data.get(key):
            return _text(data[key], limit=90)
    return str(data.get("id", ""))


def _aliases(data: dict[str, Any]) -> list[str]:
    names = data.get("names")
    aliases: list[str] = []
    if isinstance(names, dict):
        for key in ("english", "ukrainian"):
            if names.get(key):
                aliases.append(str(names[key]))
        for key in ("synonyms", "brand_names"):
            for item in _as_list(names.get(key)):
                aliases.append(str(item))
    return sorted({a for a in aliases if a and a != _name_from_data(data)})


def load_entities(kb_root: Path) -> dict[str, KbEntity]:
    entities: dict[str, KbEntity] = {}
    for kind_dir in sorted(p for p in kb_root.iterdir() if p.is_dir()):
        kind = kind_dir.name
        kind_label = ENTITY_DIRS.get(kind, kind.replace("_", " ").title())
        for path in sorted(kind_dir.rglob("*.yaml")):
            data = _load_yaml(path)
            if not data:
                continue
            entity_id = str(data["id"])
            entities[entity_id] = KbEntity(
                kind=kind,
                kind_label=kind_label,
                id=entity_id,
                title=_name_from_data(data),
                data=data,
                path=path,
                rel_path=path.relative_to(kb_root.parent.parent.parent).as_posix(),
            )
    return entities


def _collect_ids(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for item in value.values():
            found.update(_collect_ids(item))
    elif isinstance(value, list):
        for item in value:
            found.update(_collect_ids(item))
    elif isinstance(value, str):
        found.update(ID_RE.findall(value))
    return found


def build_reverse_refs(entities: dict[str, KbEntity]) -> dict[str, list[KbEntity]]:
    reverse: dict[str, list[KbEntity]] = {}
    for entity in entities.values():
        for ref_id in _collect_ids(entity.data) - {entity.id}:
            reverse.setdefault(ref_id, []).append(entity)
    for refs in reverse.values():
        refs.sort(key=lambda e: (e.kind, e.id))
    return reverse


def _source_ids(data: dict[str, Any]) -> list[str]:
    ids = set()
    for key in ("sources", "primary_sources"):
        for item in _as_list(data.get(key)):
            if isinstance(item, str) and item.startswith("SRC-"):
                ids.add(item)
    for item in _as_list(data.get("evidence_sources")):
        if isinstance(item, dict) and str(item.get("source", "")).startswith("SRC-"):
            ids.add(str(item["source"]))
    return sorted(ids)


def _disease_ids(data: dict[str, Any]) -> list[str]:
    ids = set()
    for key in ("disease_id", "applicable_to_disease"):
        value = data.get(key)
        if isinstance(value, str) and value.startswith("DIS-"):
            ids.add(value)
    for item in _as_list(data.get("relevant_diseases")):
        if isinstance(item, str) and item.startswith("DIS-"):
            ids.add(item)
    applicable = data.get("applicable_to")
    if isinstance(applicable, dict):
        value = applicable.get("disease_id")
        if isinstance(value, str) and value.startswith("DIS-"):
            ids.add(value)
    return sorted(ids)


def _status(entity: KbEntity) -> str:
    data = entity.data
    flags = []
    if data.get("last_reviewed") or data.get("last_verified"):
        flags.append(f"reviewed {data.get('last_reviewed') or data.get('last_verified')}")
    if data.get("ukrainian_review_status"):
        flags.append(str(data["ukrainian_review_status"]))
    if data.get("actionability_review_required"):
        flags.append("actionability review required")
    return " | ".join(flags) or "status not declared"


def _source_title(source_id: str, entities: dict[str, KbEntity]) -> str:
    source = entities.get(source_id)
    if not source:
        return source_id
    return source.title


def _entity_link(entity_id: str, entities: dict[str, KbEntity], *, root_prefix: str = "/") -> str:
    entity = entities.get(entity_id)
    if entity and entity.kind in SEARCH_KINDS:
        return f'<a href="{root_prefix}{html.escape(entity.url)}"><code>{html.escape(entity_id)}</code></a>'
    return f"<code>{html.escape(entity_id)}</code>"


def _chips(ids: list[str], entities: dict[str, KbEntity], *, root_prefix: str = "/") -> str:
    if not ids:
        return '<span class="kb-muted">None declared</span>'
    return " ".join(f'<span class="kb-chip">{_entity_link(i, entities, root_prefix=root_prefix)}</span>' for i in ids)


def _rows(rows: list[tuple[str, str]]) -> str:
    return "\n".join(
        f"<tr><th>{html.escape(label)}</th><td>{value}</td></tr>"
        for label, value in rows
        if value
    )


def _json_block(value: Any) -> str:
    if value in (None, "", [], {}):
        return ""
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    return f"<pre>{html.escape(text)}</pre>"


def _page_shell(title: str, body: str, *, active: str = "kb") -> str:
    active_attr = ' class="active"' if active == "kb" else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} - OpenOnco</title>
  <link rel="stylesheet" href="/style.css">
  <style>{KB_CSS}</style>
</head>
<body>
  <header class="top-bar">
    <div class="brand-line"><a class="brand-mini" href="/">OpenOnco</a></div>
    <nav class="top-nav">
      <a href="/">Home</a>
      <a href="/kb.html"{active_attr}>KB Search</a>
      <a href="/diseases.html">Diseases</a>
      <a href="/gallery.html">Examples</a>
      <a href="/capabilities.html">Capabilities</a>
      <a href="/specs.html">Specs</a>
    </nav>
    <div class="top-right"><a class="btn-cta-try" href="/try.html">Try it</a></div>
  </header>
  {body}
</body>
</html>
"""


def _frontmatter(entity: KbEntity, entities: dict[str, KbEntity]) -> str:
    data = entity.data
    sources = _source_ids(data)
    diseases = _disease_ids(data)
    rows = [
        ("ID", f"<code>{html.escape(entity.id)}</code>"),
        ("Type", html.escape(entity.kind_label)),
        ("Status", html.escape(_status(entity))),
        ("File", f"<code>{html.escape(entity.rel_path)}</code>"),
        ("Diseases", _chips(diseases, entities)),
        (
            "Sources",
            " ".join(
                f'<span class="kb-chip" title="{html.escape(_source_title(s, entities))}"><code>{html.escape(s)}</code></span>'
                for s in sources
            )
            if sources
            else '<span class="kb-muted">None declared</span>',
        ),
    ]
    aliases = _aliases(data)
    if aliases:
        rows.insert(2, ("Aliases", html.escape(", ".join(aliases[:12]))))
    return f'<table class="kb-facts">{_rows(rows)}</table>'


def _drug_sections(entity: KbEntity) -> str:
    d = entity.data
    reg = ((d.get("regulatory_status") or {}).get("ukraine_registration") or {})
    rows = [
        ("Class", html.escape(_text(d.get("drug_class")))),
        ("Mechanism", html.escape(_text(d.get("mechanism"), limit=900))),
        ("Typical dosing", html.escape(_text(d.get("typical_dosing"), limit=700))),
        ("Ukraine registered", html.escape(str(reg.get("registered"))) if reg else ""),
        ("NSZU reimbursed", html.escape(str(reg.get("reimbursed_nszu"))) if reg else ""),
        ("Ukraine last verified", html.escape(str(reg.get("last_verified"))) if reg.get("last_verified") else ""),
    ]
    warnings = "".join(f"<li>{html.escape(_text(w))}</li>" for w in _as_list(d.get("black_box_warnings"))[:8])
    return f"<h2>Drug Facts</h2><table class=\"kb-facts\">{_rows(rows)}</table>" + (
        f"<h2>Warnings</h2><ul>{warnings}</ul>" if warnings else ""
    )


def _biomarker_sections(entity: KbEntity, entities: dict[str, KbEntity]) -> str:
    d = entity.data
    rows = [
        ("Biomarker type", html.escape(_text(d.get("biomarker_type")))),
        ("Mutation details", html.escape(_text(d.get("mutation_details"), limit=500))),
        ("Measurement", html.escape(_text(d.get("measurement"), limit=500))),
        ("Actionability lookup", html.escape(_text(d.get("actionability_lookup"), limit=500))),
        ("Related biomarkers", _chips([str(x) for x in _as_list(d.get("related_biomarkers"))], entities)),
    ]
    return f'<h2>Biomarker Facts</h2><table class="kb-facts">{_rows(rows)}</table>'


def _redflag_sections(entity: KbEntity) -> str:
    d = entity.data
    rows = [
        ("Definition", html.escape(_text(d.get("definition"), limit=900))),
        ("Clinical direction", html.escape(_text(d.get("clinical_direction")))),
        ("Category", html.escape(_text(d.get("category")))),
        ("Shifts algorithm", html.escape(", ".join(str(x) for x in _as_list(d.get("shifts_algorithm"))))),
    ]
    trigger = _json_block(d.get("trigger"))
    return f'<h2>Red Flag Origin</h2><table class="kb-facts">{_rows(rows)}</table>' + (
        f"<h2>Trigger Logic</h2>{trigger}" if trigger else ""
    )


def _actionability_sections(entity: KbEntity, entities: dict[str, KbEntity]) -> str:
    d = entity.data
    rows = [
        ("Biomarker", _entity_link(str(d.get("biomarker_id")), entities) if d.get("biomarker_id") else ""),
        ("Variant", html.escape(_text(d.get("variant_qualifier")))),
        ("Disease", _entity_link(str(d.get("disease_id")), entities) if d.get("disease_id") else ""),
        ("ESCAT tier", html.escape(_text(d.get("escat_tier")))),
        ("Recommended combinations", html.escape(", ".join(str(x) for x in _as_list(d.get("recommended_combinations"))))),
        ("Contraindicated monotherapy", html.escape(", ".join(str(x) for x in _as_list(d.get("contraindicated_monotherapy"))))),
        ("Evidence summary", html.escape(_text(d.get("evidence_summary"), limit=1100))),
    ]
    return f'<h2>Actionability Facts</h2><table class="kb-facts">{_rows(rows)}</table>'


def _reverse_ref_section(entity: KbEntity, reverse_refs: dict[str, list[KbEntity]]) -> str:
    refs = [r for r in reverse_refs.get(entity.id, []) if r.id != entity.id]
    if not refs:
        return "<h2>Used By</h2><p class=\"kb-muted\">No reverse references found in the YAML corpus.</p>"
    by_kind: dict[str, list[KbEntity]] = {}
    for ref in refs:
        by_kind.setdefault(ref.kind_label, []).append(ref)
    parts = ["<h2>Used By</h2>"]
    for kind, items in sorted(by_kind.items()):
        rows = "".join(
            f'<li><code>{html.escape(item.id)}</code> - {html.escape(item.title)} '
            f'<span class="kb-muted">({html.escape(item.rel_path)})</span></li>'
            for item in items[:40]
        )
        more = f'<li class="kb-muted">... {len(items) - 40} more</li>' if len(items) > 40 else ""
        parts.append(f"<h3>{html.escape(kind)}</h3><ul>{rows}{more}</ul>")
    return "\n".join(parts)


def render_entity_page(
    entity: KbEntity,
    entities: dict[str, KbEntity],
    reverse_refs: dict[str, list[KbEntity]],
) -> str:
    if entity.kind == "drugs":
        specifics = _drug_sections(entity)
    elif entity.kind == "biomarkers":
        specifics = _biomarker_sections(entity, entities)
    elif entity.kind == "redflags":
        specifics = _redflag_sections(entity)
    elif entity.kind == "biomarker_actionability":
        specifics = _actionability_sections(entity, entities)
    else:
        specifics = ""

    notes = entity.data.get("notes") or entity.data.get("evidence_summary")
    notes_html = (
        f"<h2>Notes</h2><p>{html.escape(_text(notes, limit=1200))}</p>"
        if notes
        else ""
    )
    body = f"""<main class="kb-page kb-entity">
  <p class="kb-breadcrumb"><a href="/kb.html">KB Search</a> / {html.escape(entity.kind_label)}</p>
  <h1>{html.escape(entity.title)}</h1>
  <p class="kb-lead">Deterministic view of the source YAML entity. Clinical authority remains with the cited source IDs and reviewer sign-off state.</p>
  {_frontmatter(entity, entities)}
  {specifics}
  {notes_html}
  {_reverse_ref_section(entity, reverse_refs)}
</main>"""
    return _page_shell(f"{entity.title}", body)


def _search_entry(entity: KbEntity, reverse_refs: dict[str, list[KbEntity]]) -> dict[str, Any]:
    d = entity.data
    sources = _source_ids(d)
    diseases = _disease_ids(d)
    refs = reverse_refs.get(entity.id, [])
    subtitle_parts = []
    if diseases:
        subtitle_parts.append("disease: " + ", ".join(diseases[:4]))
    if sources:
        subtitle_parts.append("sources: " + ", ".join(sources[:4]))
    subtitle_parts.append(_status(entity))
    search_text = " ".join(
        [
            entity.id,
            entity.title,
            entity.kind_label,
            " ".join(_aliases(d)),
            " ".join(sources),
            " ".join(diseases),
            _text(d.get("definition")),
            _text(d.get("mechanism")),
            _text(d.get("evidence_summary")),
            _text(d.get("notes")),
        ]
    )
    return {
        "id": entity.id,
        "kind": entity.kind_label,
        "title": entity.title,
        "url": "/" + entity.url,
        "subtitle": " | ".join(subtitle_parts),
        "sources": sources,
        "diseases": diseases,
        "used_by_count": len(refs),
        "search_text": search_text.lower(),
    }


def render_kb_home(entries: list[dict[str, Any]], counts: dict[str, int]) -> str:
    faq = """
  <section class="kb-faq">
    <h2>Clinician FAQ</h2>
    <details><summary>Does OpenOnco prescribe treatment?</summary><p>No. The engine emits source-cited drafts for MDT discussion and always requires clinician verification.</p></details>
    <details><summary>What does a red flag do?</summary><p>A red flag is structured logic that can intensify, de-escalate, block, or redirect an algorithm branch. Its page shows trigger logic, disease scope, source IDs, and reverse references.</p></details>
    <details><summary>Why are source IDs shown instead of copied guideline text?</summary><p>OpenOnco references sources while respecting source licensing. The source ID points to the KB source record and should be checked against the original guideline or database.</p></details>
    <details><summary>What does reviewed or STUB mean?</summary><p>Clinical content remains provisional until it meets the project sign-off rules. The status line exposes declared review dates and review-required flags from YAML.</p></details>
    <details><summary>Can this be used with real patient data?</summary><p>The public site is designed for synthetic or de-identified examples. Do not paste PHI into public tooling.</p></details>
  </section>
"""
    count_cards = "".join(
        f'<div class="kb-count"><span>{count}</span>{html.escape(label)}</div>'
        for label, count in counts.items()
    )
    body = f"""<main class="kb-page">
  <section class="kb-hero">
    <h1>KB Search</h1>
    <p class="kb-lead">Search drugs, biomarkers, red flags, and biomarker actionability. Results are generated directly from the YAML knowledge base, with source IDs and reverse references exposed for audit.</p>
    <div class="kb-info-box" role="note">
      <strong>Source-grounded browser.</strong>
      This page is generated from checked-in YAML entities, not from free-text LLM answers.
      Open an entity to see source IDs, review status, file provenance, and where it is used.
    </div>
    <div class="kb-counts">{count_cards}</div>
    <label class="kb-search-label" for="kbSearch">Search the clinical KB</label>
    <div class="kb-search-row">
      <input id="kbSearch" class="kb-search" type="search" autocomplete="off" placeholder="Try rituximab, EGFR L858R, SRC-CIVIC, RF-NSCLC...">
      <button id="kbSearchBtn" class="kb-search-btn" type="button">Search</button>
    </div>
    <div class="kb-filter-row">
      <button type="button" data-kind="">All</button>
      <button type="button" data-kind="Drug">Drugs</button>
      <button type="button" data-kind="Biomarker">Biomarkers</button>
      <button type="button" data-kind="Red flag">Red flags</button>
      <button type="button" data-kind="Actionability">Actionability</button>
    </div>
  </section>
  <section>
    <div id="kbResults" class="kb-results"></div>
  </section>
  {faq}
</main>
<script>
const KB_ENTRIES = {json.dumps(entries, ensure_ascii=False)};
const searchInput = document.getElementById('kbSearch');
const searchButton = document.getElementById('kbSearchBtn');
const results = document.getElementById('kbResults');
const filterButtons = Array.from(document.querySelectorAll('[data-kind]'));
let activeKind = '';

function escapeHtml(value) {{
  return String(value || '').replace(/[&<>"']/g, ch => ({{
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }}[ch]));
}}

function scoreEntry(entry, terms) {{
  let score = 0;
  for (const term of terms) {{
    if (!entry.search_text.includes(term)) return -1;
    if (entry.id.toLowerCase().includes(term)) score += 8;
    if (entry.title.toLowerCase().includes(term)) score += 6;
    if (entry.kind.toLowerCase().includes(term)) score += 2;
    score += 1;
  }}
  return score;
}}

function renderResults() {{
  const q = (searchInput.value || '').trim().toLowerCase();
  const terms = q.split(/\\s+/).filter(Boolean);
  const ranked = KB_ENTRIES
    .filter(e => !activeKind || e.kind === activeKind)
    .map(e => [scoreEntry(e, terms), e])
    .filter(pair => terms.length === 0 ? true : pair[0] >= 0)
    .sort((a, b) => b[0] - a[0] || a[1].title.localeCompare(b[1].title))
    .slice(0, 80)
    .map(pair => pair[1]);
  if (!ranked.length) {{
    results.innerHTML = '<p class="kb-muted">No matching KB entities.</p>';
    return;
  }}
  results.innerHTML = ranked.map(e => `
    <a class="kb-result" href="${{e.url}}">
      <span class="kb-kind">${{escapeHtml(e.kind)}}</span>
      <strong>${{escapeHtml(e.title)}}</strong>
      <code>${{escapeHtml(e.id)}}</code>
      <small>${{escapeHtml(e.subtitle)}} | used by ${{e.used_by_count}}</small>
    </a>
  `).join('');
}}

filterButtons.forEach(btn => btn.addEventListener('click', () => {{
  activeKind = btn.dataset.kind || '';
  filterButtons.forEach(b => b.classList.toggle('active', b === btn));
  renderResults();
}}));
searchInput.addEventListener('input', renderResults);
searchInput.addEventListener('keydown', event => {{
  if (event.key === 'Enter') {{
    event.preventDefault();
    renderResults();
    results.scrollIntoView({{ block: 'start', behavior: 'smooth' }});
  }}
}});
searchButton.addEventListener('click', () => {{
  renderResults();
  results.scrollIntoView({{ block: 'start', behavior: 'smooth' }});
}});
filterButtons[0].classList.add('active');
renderResults();
</script>
"""
    return _page_shell("KB Search", body)


def build_kb_wiki(kb_root: Path, output_dir: Path) -> dict[str, Any]:
    entities = load_entities(kb_root)
    reverse_refs = build_reverse_refs(entities)
    searchable = [e for e in entities.values() if e.kind in SEARCH_KINDS]
    searchable.sort(key=lambda e: (e.kind, e.title.lower(), e.id))

    entries = [_search_entry(e, reverse_refs) for e in searchable]
    counts = {
        "Drugs": sum(1 for e in searchable if e.kind == "drugs"),
        "Biomarkers": sum(1 for e in searchable if e.kind == "biomarkers"),
        "Red flags": sum(1 for e in searchable if e.kind == "redflags"),
        "Actionability": sum(1 for e in searchable if e.kind == "biomarker_actionability"),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    for kind in SEARCH_KINDS:
        (output_dir / "kb" / kind).mkdir(parents=True, exist_ok=True)

    (output_dir / "kb.html").write_text(render_kb_home(entries, counts), encoding="utf-8")
    (output_dir / "kb_search_index.json").write_text(
        json.dumps({"entries": entries, "counts": counts}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for entity in searchable:
        out_path = output_dir / entity.url
        out_path.write_text(render_entity_page(entity, entities, reverse_refs), encoding="utf-8")

    return {
        "entities": len(searchable),
        "counts": counts,
        "index": "kb_search_index.json",
        "home": "kb.html",
    }


KB_CSS = """
.kb-page { padding-top: 34px; }
.kb-page h1 { font-family: var(--font-display); font-size: 38px; color: var(--green-900); margin-bottom: 10px; }
.kb-page h2 { font-family: var(--font-display); color: var(--green-900); font-size: 24px; margin: 30px 0 12px; }
.kb-page h3 { color: var(--green-900); font-size: 17px; margin: 18px 0 8px; }
.kb-lead { color: var(--gray-700); font-size: 16px; max-width: 880px; margin-bottom: 22px; }
.kb-breadcrumb { font-size: 13px; margin-bottom: 12px; color: var(--gray-500); }
.kb-info-box { background: white; border: 1px solid var(--green-100); border-left: 5px solid var(--green-700); border-radius: 7px; padding: 13px 15px; color: var(--gray-700); margin: 18px 0 20px; max-width: 920px; }
.kb-info-box strong { color: var(--green-900); }
.kb-counts { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; margin: 20px 0 24px; }
.kb-count { border: 1px solid var(--gray-200); background: white; border-radius: 7px; padding: 12px; color: var(--gray-700); }
.kb-count span { display: block; color: var(--green-700); font-size: 28px; font-weight: 700; line-height: 1; }
.kb-search-label { display: block; font-weight: 700; margin-bottom: 7px; }
.kb-search-row { display: grid; grid-template-columns: 1fr auto; gap: 10px; align-items: stretch; }
.kb-search { width: 100%; border: 1px solid var(--gray-200); border-radius: 7px; padding: 13px 14px; font-size: 16px; background: white; }
.kb-search-btn { min-width: 118px; border: 1px solid var(--green-700); background: var(--green-700); color: white; border-radius: 7px; padding: 0 18px; font-weight: 700; cursor: pointer; }
.kb-search-btn:hover { background: var(--green-600); border-color: var(--green-600); }
.kb-filter-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0 22px; }
.kb-filter-row button { border: 1px solid var(--gray-200); background: white; color: var(--gray-700); border-radius: 5px; padding: 7px 11px; cursor: pointer; }
.kb-filter-row button.active { background: var(--green-700); color: white; border-color: var(--green-700); }
.kb-results { display: grid; gap: 8px; }
.kb-result { display: grid; grid-template-columns: 105px 1fr auto; gap: 10px; align-items: baseline; background: white; border: 1px solid var(--gray-200); border-radius: 7px; padding: 12px; text-decoration: none; color: var(--gray-900); }
.kb-result:hover { border-color: var(--green-600); }
.kb-result small { grid-column: 2 / -1; color: var(--gray-500); }
.kb-kind { font-family: var(--font-mono); font-size: 11px; color: var(--green-700); text-transform: uppercase; }
.kb-facts { width: 100%; border-collapse: collapse; background: white; border: 1px solid var(--gray-200); border-radius: 7px; overflow: hidden; }
.kb-facts th, .kb-facts td { border-bottom: 1px solid var(--gray-200); padding: 10px 12px; vertical-align: top; text-align: left; }
.kb-facts th { width: 190px; color: var(--gray-700); background: var(--gray-50); }
.kb-chip { display: inline-block; margin: 2px 4px 2px 0; padding: 3px 7px; border-radius: 4px; background: var(--green-50); border: 1px solid var(--green-100); }
.kb-muted { color: var(--gray-500); }
.kb-entity ul { padding-left: 22px; }
.kb-entity pre { background: var(--gray-900); color: white; border-radius: 7px; padding: 14px; overflow: auto; font-size: 12px; }
.kb-faq { margin-top: 36px; }
.kb-faq details { background: white; border: 1px solid var(--gray-200); border-radius: 7px; padding: 11px 13px; margin-bottom: 8px; }
.kb-faq summary { cursor: pointer; font-weight: 700; color: var(--green-900); }
@media (max-width: 700px) {
  .kb-search-row { grid-template-columns: 1fr; }
  .kb-search-btn { min-height: 44px; }
  .kb-result { grid-template-columns: 1fr; }
  .kb-result small { grid-column: auto; }
  .kb-facts th { width: auto; display: block; border-bottom: 0; }
  .kb-facts td { display: block; }
}
"""
