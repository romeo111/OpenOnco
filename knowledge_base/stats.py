"""Project stats: entity counters + per-disease coverage matrix.

Counts what is in the KB right now and shows per-disease coverage so
landing-page visitors see both the dynamics and the limits — which
diseases have the full chain disease→indication→regimen→algorithm,
which are partial, which still STUB pending Clinical Co-Lead sign-off.

Three output formats:

- text         — CLI summary
- json         — machine-readable
- html-widget  — embeddable single-block <div> (no external assets) for
                 the OpenOnco landing page

CLI:

    python -m knowledge_base.stats [--format text|json|html-widget]
                                   [--output PATH] [--no-style]
"""

from __future__ import annotations

from .review_policy import MIN_ELIGIBLE_CONTENT_REVIEWS

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


from .review_metrics import REVIEW_TYPES, current_review_count, historical_review_counts


# ── Layout ────────────────────────────────────────────────────────────────

_PKG_ROOT = Path(__file__).resolve().parent
_REPO_ROOT = _PKG_ROOT.parent
_KB_CONTENT = _PKG_ROOT / "hosted" / "content"
_SPECS_DIR = _REPO_ROOT / "specs"
_CLIENTS_DIR = _PKG_ROOT / "clients"
_SKILLS_DIR = _PKG_ROOT / "skills"

# Entity directories under hosted/content/. Order anchors the rendering;
# diseases first so coverage table is readable.
_ENTITY_DIRS: list[tuple[str, str]] = [
    ("diseases", "Хвороби"),
    ("indications", "Показання"),
    ("regimens", "Режими"),
    ("algorithms", "Алгоритми"),
    ("biomarkers", "Біомаркери / гени"),
    ("biomarker_actionability", "Дії за біомаркерами"),
    ("drugs", "Препарати"),
    ("tests", "Тести / процедури"),
    ("workups", "Workups (триаж)"),
    ("redflags", "Red flags"),
    ("contraindications", "Протипоказання"),
    ("monitoring", "Моніторинг"),
    ("supportive_care", "Супровідна терапія"),
    ("sources", "Джерела"),
]


def _role_catalog() -> dict[str, str]:
    from .engine.mdt_orchestrator import _ROLE_CATALOG
    return _ROLE_CATALOG


# ── Data shapes ───────────────────────────────────────────────────────────


@dataclass
class EntityCount:
    type: str
    label: str
    count: int


@dataclass
class DiseaseCoverage:
    disease_id: str
    name: str
    indications: int
    regimens: int
    has_algorithm: bool
    red_flags: int
    workups: int
    reviewer_signoffs_max: int
    clinical_records_total: int = 0
    clinical_records_reviewed: int = 0

    @property
    def coverage_status(self) -> str:
        # Full chain = disease + ≥1 indication + ≥1 regimen + algorithm.
        # Review records remain optional; technical checks alone confer no clinical review.
        if self.indications >= 1 and self.regimens >= 1 and self.has_algorithm:
            if self.clinical_records_total > 0 and self.clinical_records_reviewed == self.clinical_records_total:
                return "reviewed"
            return "stub_full_chain"
        if self.indications >= 1:
            return "partial"
        return "skeleton"


@dataclass
class Stats:
    generated_at_utc: str
    entities: list[EntityCount]
    total_yaml_entities: int
    specs_count: int
    api_clients_count: int
    skills_count: int
    skills_planned_roles: int
    reviewer_signoffs_total: int
    reviewer_signoffs_reviewed: int
    diseases: list[DiseaseCoverage]
    # Corpus mass behind the cited sources — sum of pages_count + references_count
    # across all Source entities. Surfaces the "scale of literature" marketing
    # metric on landing: visitors see "13 sources" but also "3,000+ primary
    # publications behind them" (NCCN B-Cell guideline alone cites ~700 RCTs).
    corpus_pages_total: int = 0
    corpus_references_total: int = 0
    sources_with_corpus_data: int = 0
    historical_structured_reviews: int = 0
    legacy_review_counter_total: int = 0


# ── Loaders ───────────────────────────────────────────────────────────────


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        data = yaml.load(fh, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping in public statistics input: {path.name}")
    return data


def _list_yaml(dir_path: Path) -> list[Path]:
    if not dir_path.exists():
        return []
    return sorted(p for p in dir_path.glob("*.yaml") if p.is_file())


# ── Coverage ──────────────────────────────────────────────────────────────


def _disease_name(d: dict[str, Any]) -> str:
    names = d.get("names") or {}
    return (
        names.get("ukrainian")
        or names.get("preferred")
        or names.get("english")
        or d.get("id", "?")
    )


def _build_coverage(
    diseases: list[dict[str, Any]],
    indications: list[dict[str, Any]],
    algorithms: list[dict[str, Any]],
    workups: list[dict[str, Any]],
    review_counts: dict[str, int] | None = None,
    clinical_records: dict[str, dict[str, Any]] | None = None,
) -> list[DiseaseCoverage]:
    review_counts = review_counts or {}
    clinical_records = clinical_records or {}
    by_disease_inds: dict[str, list[dict[str, Any]]] = {}
    for ind in indications:
        did = ((ind.get("applicable_to") or {}).get("disease_id")) or ""
        by_disease_inds.setdefault(did, []).append(ind)

    algo_diseases: set[str] = set()
    for algo in algorithms:
        d = algo.get("applicable_to_disease")
        if d:
            algo_diseases.add(d)

    out: list[DiseaseCoverage] = []
    for d in diseases:
        did = d.get("id", "")
        d_inds = by_disease_inds.get(did, [])
        regs = {
            ind.get("recommended_regimen")
            for ind in d_inds
            if ind.get("recommended_regimen")
        }
        rfs: set[str] = set()
        for ind in d_inds:
            for rf in (ind.get("red_flags_triggering_alternative") or []):
                if isinstance(rf, str):
                    rfs.add(rf)

        # Workups attach by triage flow (lineage_hints), not disease_id.
        # Heuristic: match disease lineage OR id-substring against workup's
        # lineage_hints / id. Imperfect but sufficient for landing-page display.
        lineage = (d.get("lineage") or "").lower()
        did_token = did.lower().replace("dis-", "").replace("-", "_")
        workup_count = 0
        for w in workups:
            hints = " ".join(
                ((w.get("applicable_to") or {}).get("lineage_hints")) or []
            ).lower()
            wid = (w.get("id") or "").lower()
            if (lineage and lineage in hints) or (
                did_token and (did_token in hints or did_token in wid)
            ):
                workup_count += 1

        signoffs_max = max(
            (review_counts.get(ind.get("id"), 0) for ind in d_inds),
            default=0,
        )
        # A reviewed indication cannot certify the entire disease chain.
        required_ids = {ind.get("id") for ind in d_inds} | regs | rfs
        required_ids.update(a.get("id") for a in algorithms if a.get("applicable_to_disease") == did)
        required_ids.update(
            entity_id for entity_id, record in clinical_records.items()
            if record.get("disease_id") == did or did in (record.get("relevant_diseases") or [])
        )
        required_ids.discard(None)
        reviewed_records = sum(
            entity_id in clinical_records and review_counts.get(entity_id, 0) >= MIN_ELIGIBLE_CONTENT_REVIEWS
            for entity_id in required_ids
        )
        out.append(
            DiseaseCoverage(
                disease_id=did,
                name=_disease_name(d),
                indications=len(d_inds),
                regimens=len(regs),
                has_algorithm=did in algo_diseases,
                red_flags=len(rfs),
                workups=workup_count,
                reviewer_signoffs_max=signoffs_max,
                clinical_records_total=len(required_ids),
                clinical_records_reviewed=reviewed_records,
            )
        )
    return out


# ── Collect ───────────────────────────────────────────────────────────────


def collect_stats() -> Stats:
    entities: list[EntityCount] = []
    total = 0
    diseases_yaml: list[dict[str, Any]] = []
    indications_yaml: list[dict[str, Any]] = []
    algorithms_yaml: list[dict[str, Any]] = []
    workups_yaml: list[dict[str, Any]] = []

    reviewer_total = 0
    reviewer_reviewed = 0
    structured_history = 0
    legacy_counters = 0
    clinical_records = {}
    review_counts = {}
    reviewers = {d["id"]: d for p in _list_yaml(_KB_CONTENT / "reviewers") if (d := _load_yaml(p)).get("id")}
    disease_context = {d["id"]: d for p in _list_yaml(_KB_CONTENT / "diseases") if (d := _load_yaml(p)).get("id")}

    corpus_pages = 0
    corpus_refs = 0
    sources_with_corpus = 0

    for dir_name, label in _ENTITY_DIRS:
        files = _list_yaml(_KB_CONTENT / dir_name)
        loaded = [_load_yaml(p) for p in files]
        entities.append(EntityCount(type=dir_name, label=label, count=len(files)))
        total += len(files)
        for d in loaded:
            if dir_name in REVIEW_TYPES:
                reviewer_total += 1
                count = current_review_count(d, dir_name, reviewers, disease_context)
                reviewer_reviewed += count >= MIN_ELIGIBLE_CONTENT_REVIEWS
                if d.get("id"):
                    clinical_records[d["id"]] = d
                    review_counts[d["id"]] = count
                structured, legacy = historical_review_counts(d)
                structured_history += structured
                legacy_counters += legacy
        if dir_name == "diseases":
            diseases_yaml = loaded
        elif dir_name == "indications":
            indications_yaml = loaded
        elif dir_name == "algorithms":
            algorithms_yaml = loaded
        elif dir_name == "workups":
            workups_yaml = loaded
        elif dir_name == "sources":
            for d in loaded:
                pages = d.get("pages_count") or 0
                refs = d.get("references_count") or 0
                if pages or refs:
                    sources_with_corpus += 1
                corpus_pages += int(pages or 0)
                corpus_refs += int(refs or 0)

    specs_count = (
        len(list(_SPECS_DIR.glob("*.md"))) if _SPECS_DIR.exists() else 0
    )
    clients_count = (
        len([p for p in _CLIENTS_DIR.glob("*_client.py") if p.is_file()])
        if _CLIENTS_DIR.exists()
        else 0
    )
    skills_count = (
        len([p for p in _SKILLS_DIR.rglob("*.py") if p.name != "__init__.py"])
        if _SKILLS_DIR.exists()
        else 0
    )
    planned_roles = len(_role_catalog())

    coverage = _build_coverage(
        diseases_yaml, indications_yaml, algorithms_yaml, workups_yaml, review_counts, clinical_records
    )

    return Stats(
        generated_at_utc=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        entities=entities,
        total_yaml_entities=total,
        specs_count=specs_count,
        api_clients_count=clients_count,
        skills_count=skills_count,
        skills_planned_roles=planned_roles,
        reviewer_signoffs_total=reviewer_total,
        reviewer_signoffs_reviewed=reviewer_reviewed,
        diseases=coverage,
        corpus_pages_total=corpus_pages,
        corpus_references_total=corpus_refs,
        sources_with_corpus_data=sources_with_corpus,
        historical_structured_reviews=structured_history,
        legacy_review_counter_total=legacy_counters,
    )


# ── Text formatter ────────────────────────────────────────────────────────


def format_text(s: Stats) -> str:
    lines: list[str] = []
    lines.append(f"OpenOnco — стан проекту  ({s.generated_at_utc})")
    lines.append("=" * 72)
    lines.append("")
    lines.append("KB entities:")
    width = max(len(e.label) for e in s.entities)
    for e in s.entities:
        lines.append(f"  {e.label.ljust(width)}  {e.count:>4}")
    lines.append(f"  {'Всього YAML'.ljust(width)}  {s.total_yaml_entities:>4}")
    lines.append("")
    lines.append("Інфраструктура:")
    lines.append(f"  Специфікації (specs/*.md)        {s.specs_count}")
    lines.append(f"  API-клієнти (live sources)       {s.api_clients_count}")
    lines.append(
        f"  Skills (MDT-ролі)                {s.skills_count} реалізовано "
        f"/ {s.skills_planned_roles} заплановано"
    )
    lines.append("")
    lines.append("Корпус літератури (за процитованими джерелами):")
    sources_total = next((e.count for e in s.entities if e.type == "sources"), 0)
    lines.append(
        f"  Джерел (top-level guidelines/RCTs)   {sources_total}"
    )
    lines.append(
        f"  Сторінок керівництв сумарно          {s.corpus_pages_total:,}"
    )
    lines.append(
        f"  Primary publications референсовано   {s.corpus_references_total:,}+"
    )
    lines.append(
        f"  Джерел з заповненим corpus mass      "
        f"{s.sources_with_corpus_data} / {sources_total}"
    )
    lines.append("")
    lines.append("Optional content-review audit (not a solo-project release gate):")
    lines.append(
        f"  Reviewer sign-offs ≥ 2           "
        f"{s.reviewer_signoffs_reviewed} / {s.reviewer_signoffs_total} "
        f"(описовий показник; не умова релізу)"
    )
    lines.append("  Лише актуальні, незалежні й уповноважені перегляди змісту; не схвалення лікування.")
    lines.append(f"  Історичні структуровані записи: {s.historical_structured_reviews}; старі лічильники: {s.legacy_review_counter_total} (не підтвердження).")
    lines.append("")
    lines.append("Покриття по хворобах:")
    if not s.diseases:
        lines.append("  (поки немає)")
    else:
        header = (
            "  ID                    Назва                              "
            "Ind  Reg  Алг  RF  Wkup  Status"
        )
        lines.append(header)
        lines.append("  " + "-" * (len(header) - 2))
        for d in s.diseases:
            algo = "✓" if d.has_algorithm else "·"
            lines.append(
                f"  {d.disease_id:<22}{d.name[:32]:<34}"
                f"{d.indications:>3}  {d.regimens:>3}  "
                f"{algo:>3}  {d.red_flags:>3}  {d.workups:>4}   "
                f"{d.coverage_status}"
            )
    lines.append("")
    return "\n".join(lines)


# ── JSON formatter ────────────────────────────────────────────────────────


def format_json(s: Stats) -> str:
    payload = asdict(s)
    for d_struct, d_obj in zip(payload["diseases"], s.diseases):
        d_struct["coverage_status"] = d_obj.coverage_status
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ── HTML widget (embeddable for landing page) ─────────────────────────────


_WIDGET_CSS = """
.oo-widget {
    --green-50:#f0fdf4; --green-100:#dcfce7; --green-500:#16a34a;
    --green-700:#14532d; --green-900:#0a2e1a;
    --gray-50:#f9fafb; --gray-100:#f3f4f6; --gray-200:#e5e7eb;
    --gray-500:#6b7280; --gray-700:#374151; --gray-900:#111827;
    --amber:#d97706; --amber-bg:#fffbeb;
    font-family:'Source Sans 3','Segoe UI',sans-serif;
    color:var(--gray-900); background:#fff;
    border:1px solid var(--gray-200); border-radius:14px;
    padding:24px; max-width:960px; line-height:1.5;
}
.oo-widget h2 {
    font-family:'Playfair Display',Georgia,serif;
    font-size:22px; color:var(--green-900); margin:0 0 4px;
}
.oo-widget .oo-sub { font-size:13px; color:var(--gray-500); margin-bottom:18px; }
.oo-widget .oo-grid {
    display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
    gap:10px; margin-bottom:20px;
}
.oo-widget .oo-card {
    background:var(--green-50); border:1px solid var(--green-100);
    border-radius:10px; padding:12px 14px;
}
.oo-widget .oo-card .oo-num {
    font-family:'Playfair Display',Georgia,serif;
    font-size:26px; color:var(--green-700); line-height:1;
}
.oo-widget .oo-card .oo-lbl {
    font-size:11px; color:var(--gray-700); margin-top:4px;
    text-transform:uppercase; letter-spacing:.04em;
}
.oo-widget .oo-meta {
    display:flex; flex-wrap:wrap; gap:18px; font-size:13px;
    color:var(--gray-700); padding:10px 14px; background:var(--gray-50);
    border-radius:8px; margin-bottom:18px;
}
.oo-widget .oo-meta b { color:var(--green-700); }
.oo-widget .oo-warn {
    background:var(--amber-bg); border-left:3px solid var(--amber);
    padding:8px 12px; font-size:13px; color:var(--gray-900);
    border-radius:4px; margin-bottom:18px;
}
.oo-widget table { width:100%; border-collapse:collapse; font-size:13px; }
.oo-widget th, .oo-widget td {
    text-align:left; padding:8px 10px; border-bottom:1px solid var(--gray-100);
}
.oo-widget th {
    background:var(--gray-50); font-weight:600; color:var(--gray-700);
    font-size:11px; text-transform:uppercase; letter-spacing:.04em;
}
.oo-widget td.num { text-align:right; font-variant-numeric:tabular-nums; }
.oo-widget code { font-family:'JetBrains Mono',Menlo,monospace; font-size:12px; }
.oo-widget .oo-pill {
    display:inline-block; padding:2px 8px; border-radius:999px;
    font-size:11px; font-weight:600; text-transform:uppercase;
    letter-spacing:.03em;
}
.oo-widget .oo-pill.reviewed { background:var(--green-100); color:var(--green-900); }
.oo-widget .oo-pill.stub_full_chain { background:#fef3c7; color:#78350f; }
.oo-widget .oo-pill.partial { background:#fde68a; color:#7c2d12; }
.oo-widget .oo-pill.skeleton { background:var(--gray-100); color:var(--gray-700); }
.oo-widget .oo-foot { margin-top:14px; font-size:11px; color:var(--gray-500); }
"""


_STATUS_LABEL = {
    "reviewed": "Reviewed",
    "stub_full_chain": "STUB · повний ланцюг",
    "partial": "Частково",
    "skeleton": "Тільки скелет",
}


def _esc(x: object) -> str:
    import html as _h

    return _h.escape(str(x))


def format_html_widget(s: Stats, *, embed_style: bool = True) -> str:
    out: list[str] = []
    if embed_style:
        out.append(f"<style>{_WIDGET_CSS}</style>")
    out.append('<div class="oo-widget" data-component="openonco-stats">')
    out.append("<h2>OpenOnco — стан бази знань</h2>")
    out.append(
        f'<div class="oo-sub">Зріз станом на {_esc(s.generated_at_utc)} · '
        f"видно і обсяг, і обмеження — поки покриваємо лише декілька хвороб.</div>"
    )

    out.append('<div class="oo-grid">')
    for e in s.entities:
        out.append(
            f'<div class="oo-card"><div class="oo-num">{e.count}</div>'
            f'<div class="oo-lbl">{_esc(e.label)}</div></div>'
        )
    out.append("</div>")

    out.append(
        f'<div class="oo-meta">'
        f"<span>Специфікації: <b>{s.specs_count}</b></span>"
        f"<span>Live API-клієнти: <b>{s.api_clients_count}</b></span>"
        f"<span>Skills (MDT): <b>{s.skills_count}</b> / "
        f"{s.skills_planned_roles} планується</span>"
        f"<span>Reviewer sign-offs ≥ 2: "
        f"<b>{s.reviewer_signoffs_reviewed}</b> / {s.reviewer_signoffs_total}</span>"
        f"</div>"
    )

    if s.corpus_references_total > 0:
        out.append(
            f'<div class="oo-meta">'
            f"<span>📚 Корпус літератури під {s.sources_with_corpus_data} цитованими джерелами: "
            f"<b>{s.corpus_references_total:,}+</b> primary publications · "
            f"<b>{s.corpus_pages_total:,}</b> сторінок керівництв</span>"
            f"</div>"
        )

    out.append(
        '<div class="oo-meta">Солопроєкт: зовнішній клінічний перегляд є додатковим '
        'і не є умовою розробки чи публікації. Технічні перевірки та простежувані '
        'джерела не є схваленням лікування.</div>'
    )

    out.append(
        "<table><thead><tr>"
        "<th>Хвороба</th><th>ID</th>"
        '<th class="num">Ind</th><th class="num">Reg</th>'
        '<th class="num">Алг</th><th class="num">RF</th>'
        '<th class="num">Workups</th><th>Статус</th>'
        "</tr></thead><tbody>"
    )
    for d in s.diseases:
        algo = "✓" if d.has_algorithm else "—"
        out.append(
            "<tr>"
            f"<td>{_esc(d.name)}</td>"
            f"<td><code>{_esc(d.disease_id)}</code></td>"
            f'<td class="num">{d.indications}</td>'
            f'<td class="num">{d.regimens}</td>'
            f'<td class="num">{algo}</td>'
            f'<td class="num">{d.red_flags}</td>'
            f'<td class="num">{d.workups}</td>'
            f'<td><span class="oo-pill {d.coverage_status}">'
            f"{_STATUS_LABEL.get(d.coverage_status, d.coverage_status)}</span></td>"
            "</tr>"
        )
    out.append("</tbody></table>")

    out.append(
        '<div class="oo-foot">Auto-generated · '
        "<code>python -m knowledge_base.stats --format html-widget</code></div>"
    )
    out.append("</div>")
    return "\n".join(out)


# ── CLI ───────────────────────────────────────────────────────────────────


def _cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m knowledge_base.stats",
        description=(
            "OpenOnco KB stats: entity counts + per-disease coverage matrix. "
            "Outputs text / JSON / embeddable HTML widget."
        ),
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["text", "json", "html-widget"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Write to file instead of stdout",
    )
    parser.add_argument(
        "--no-style",
        action="store_true",
        help="(html-widget only) Omit <style> block — use when host page "
        "already provides .oo-widget CSS.",
    )
    args = parser.parse_args(argv)

    s = collect_stats()
    if args.format == "text":
        out = format_text(s)
    elif args.format == "json":
        out = format_json(s)
    else:
        out = format_html_widget(s, embed_style=not args.no_style)

    if args.output:
        args.output.write_text(out, encoding="utf-8")
        print(f"Wrote {len(out):,} chars -> {args.output}", file=sys.stderr)
    else:
        # Windows console may default to cp1252; force UTF-8 so UA + ✓ render.
        try:
            sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        except Exception:
            pass
        try:
            sys.stdout.write(out)
        except UnicodeEncodeError:
            sys.stdout.buffer.write(out.encode("utf-8"))
        if not out.endswith("\n"):
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
