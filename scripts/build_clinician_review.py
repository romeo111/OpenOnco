"""Build a reproducible, synthetic DLBCL packet for independent clinician review.

Technical contracts describe current authored rule behavior only. Passing them
never grants clinical sign-off. This builder cannot load user patient files or
change clinical entities, review status, algorithm selection or doses.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import html
import json
import re
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from knowledge_base.engine import generate_plan, orchestrate_mdt, render_plan_html
from knowledge_base.validation.loader import load_content
from scripts.review_dlbcl_scenarios import make_profile, scenarios
from scripts.site_nav import render_top_bar

KB_ROOT = REPO_ROOT / "knowledge_base/hosted/content"
ASSETS = Path(__file__).with_name("review_assets")
DISCLAIMER = "Synthetic review only. Engineering checks are not clinical approval. No treatment decision should be based on this packet."


def _json(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n"


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _text_sha(path: Path) -> str:
    """Git text content fingerprint, independent of checkout CRLF/LF."""
    return _sha(path.read_text(encoding="utf-8").encode("utf-8"))


def _canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode()


def _snapshot(root: Path, suffix: str) -> dict:
    files = {p.relative_to(root).as_posix(): _text_sha(p)
             for p in sorted(root.rglob(f"*{suffix}")) if p.is_file() and "cache" not in p.parts}
    return {"sha256": _sha(_canonical(files)), "file_count": len(files), "encoding": "UTF-8, LF normalized"}


def _decision(result) -> dict:
    """Stable routing/materialization fingerprint; excludes runtime timestamps."""
    return {"algorithm": result.algorithm_id, "default": result.default_indication_id,
            "tracks": [{"id": t.track_id, "indication": t.indication_id,
                        "regimen": (t.regimen_data or {}).get("id"),
                        "monitoring": (t.monitoring_data or {}).get("id"),
                        "supportive_care": [s["id"] for s in t.supportive_care_data],
                        "contraindications": [c["id"] for c in t.contraindications_data]}
                       for t in result.plan.tracks] if result.plan else [],
            "trace": result.trace, "warnings": result.warnings}


def input_findings(profile: dict, result) -> list[dict]:
    """Describe observable gaps and contradictions; do not change engine output."""
    findings, demo, biomarkers = (profile.get(k, {}) for k in ("findings", "demographics", "biomarkers"))
    issues = []
    for path, value in (("findings.ipi_score", findings.get("ipi_score")),
                        ("demographics.ecog", demo.get("ecog")),
                        ("findings.lvef_percent", findings.get("lvef_percent")),
                        ("findings.hbsag", findings.get("hbsag"))):
        if value is None or value == "unknown":
            issues.append({"code": "missing_input", "field": path,
                           "detail": "Not supplied in this probe; inspect missing-data handling before relying on its output."})
    if biomarkers.get("BIO-CD20-IHC") in (None, "unknown"):
        issues.append({"code": "unknown_biomarker", "field": "biomarkers.BIO-CD20-IHC",
                       "detail": "The CD20 value is missing or unknown; review how eligibility is communicated."})
    score = findings.get("ipi_score")
    # The threshold is the checked-in RF-DLBCL-HIGH-IPI rule contract, not
    # independently validated medical evidence.
    if isinstance(score, (int, float)) and "high_ipi" in findings and findings["high_ipi"] != (score >= 2):
        issues.append({"code": "conflicting_input", "field": "findings.high_ipi",
                       "detail": "The boolean conflicts with the numeric IPI trigger in the authored rule."})
    if result.plan:
        for track in result.plan.tracks:
            applicable = (track.indication_data or {}).get("applicable_to", {})
            for requirement in applicable.get("biomarker_requirements_required", []):
                bio = requirement.get("biomarker_id")
                constraint = str(requirement.get("value_constraint", ""))
                if constraint.lower().startswith("positive") and biomarkers.get(bio) == "negative":
                    issues.append({"code": "positive_requirement_conflict", "field": bio,
                                   "detail": f"{track.indication_id} remains present with a negative value beside its authored positive requirement."})
    return issues


def _linked_entities(load, result) -> list[str]:
    roots = {result.disease_id, result.algorithm_id}
    if result.plan:
        for track in result.plan.tracks:
            roots.add(track.indication_id)
            for data in (track.regimen_data, track.monitoring_data,
                         *track.supportive_care_data, *track.contraindications_data):
                if data:
                    roots.add(data.get("id"))
    # Follow actual referenced IDs, including RFs, sources, drugs and tests.
    def refs(value):
        if isinstance(value, str) and value in load.entities_by_id:
            yield value
        elif isinstance(value, dict):
            for item in value.values():
                yield from refs(item)
        elif isinstance(value, list):
            for item in value:
                yield from refs(item)
    visited = set()
    pending = [eid for eid in roots if eid in load.entities_by_id]
    while pending:
        eid = pending.pop()
        if eid in visited:
            continue
        visited.add(eid)
        pending.extend(set(refs(load.entities_by_id[eid]["data"])) - visited)
    return sorted(visited)


def _entity_record(info, kb_root: Path) -> dict:
    data = info["data"]
    path = info["path"]
    signoffs = data.get("reviewer_signoffs", [])
    return {"id": data["id"], "type": info["type"],
            "path": path.relative_to(kb_root).as_posix(), "sha256": _text_sha(path),
            "last_reviewed": data.get("last_reviewed"), "last_verified": data.get("last_verified"),
            "review_status": data.get("review_status"), "draft": data.get("draft"),
            "reviewer_signoffs_recorded": signoffs,
            "reviewer_ids_recorded": [s.get("reviewer_id") for s in signoffs if isinstance(s, dict)] if isinstance(signoffs, list) else [],
            "title": data.get("title"), "url": data.get("url"),
            "currency_status_recorded": data.get("currency_status"),
            "independently_verified_for_packet": False}


def _questionnaire_gaps(load) -> list[dict]:
    questionnaire = next(info["data"] for info in load.entities_by_id.values()
                         if info["type"] == "questionnaires" and info["data"].get("disease_id") == "DIS-DLBCL-NOS")
    fields = {q["field"] for group in questionnaire.get("groups", []) for q in group.get("questions", [])}
    gaps = []
    for field in ("findings.ipi_score", "findings.lvef_percent", "findings.hbsag", "findings.anti_hbc_total"):
        if field not in fields:
            gaps.append({"code": "questionnaire_field_absent", "field": field,
                         "detail": "Exact engine field is not asked by the current DLBCL questionnaire; verify alias/default coverage."})
    if questionnaire.get("_stub_auto_generated"):
        gaps.append({"code": "questionnaire_stub", "field": questionnaire["id"],
                     "detail": "The questionnaire is explicitly an auto-generated STUB awaiting clinical review."})
    return gaps


def _e(value) -> str:
    return html.escape(str(value), quote=True)


def _index(report: dict) -> str:
    summary = report["summary"]
    cards = []
    for case in report["cases"]:
        issues = "".join(f'<li>{_e(i["detail"])}</li>' for i in case["input_findings"])
        tests = "".join(f'<li class="{"ok" if check["passed"] else "failed"}">{_e(check["name"])}: {"PASS" if check["passed"] else "FAIL"}</li>' for check in case["checks"])
        inputs = "".join(f'<div><dt>{_e(label)}</dt><dd>{_e(value if value is not None else "Not supplied")}</dd></div>' for label, value in case["input_summary"].items())
        questions = "".join(f'<li>{_e(q["question"])}</li>' for q in case["open_questions"])
        cards.append(f'''<article class="review-card" id="{_e(case['id'])}" data-category="{_e(case['category'])}" data-case="{_e(case['id'])}">
<div class="card-heading"><span class="tag">{_e(case['category'])}</span><span class="case-id">{_e(case['id'])}</span></div>
<h2>{_e(case['title'])}</h2><p>Observed default: <code>{_e(case['observed_default'] or 'None')}</code></p>
<dl class="input-summary">{inputs}</dl>
<p class="muted">Expected engineering route: <code>{_e(case['expected_default'] or 'None')}</code>. This is not a clinical verdict.</p>
<details><summary>Technical checks and observed input issues</summary><ul>{tests}{issues}</ul></details>
<details><summary>Engine's open MDT questions ({len(case['open_questions'])})</summary><ul>{questions or '<li>No questions emitted.</li>'}</ul></details>
<div class="case-links"><a href="cases/{_e(case['id'])}.html">Open actual plan</a><a href="cases/{_e(case['id'])}.profile.json" download>Input JSON</a><a href="cases/{_e(case['id'])}.result.json" download>Output + trace</a></div>
<label>Review assessment<select class="assessment"><option value="unreviewed">Not assessed</option><option value="acceptable">Acceptable for this synthetic scenario</option><option value="needs_changes">Needs changes</option><option value="cannot_assess">Cannot assess</option></select></label>
<label>Comments for this scenario<textarea class="comment" rows="3" maxlength="10000" placeholder="Rule, source, missing information or suggested correction. No patient data."></textarea></label>
</article>''')
    sources = [e for e in report["entities"] if e["type"] == "sources"]
    def source_link(source):
        url = source.get("url")
        return f'<a href="{_e(url)}">Source</a>' if url and url.startswith("https://") else "No public URL"

    source_rows = "".join(f'<tr><td><code>{_e(s["id"])}</code></td><td>{_e(s["title"] or "")}</td><td>{_e(s["last_verified"] or "Not recorded")}</td><td>{source_link(s)}</td></tr>' for s in sources)
    gaps = "".join(f'<li><code>{_e(g["field"])}</code>: {_e(g["detail"])}</li>' for g in report["questionnaire_findings"])
    payload = json.dumps({"packet_id": report["packet_id"], "kb_sha256": report["kb_snapshot"]["sha256"], "engine_sha256": report["engine_snapshot"]["sha256"], "scenario_sha256": report["scenario_definition_sha256"], "case_ids": [c["id"] for c in report["cases"]]}, ensure_ascii=False).replace("<", "\\u003c")
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,follow"><title>DLBCL 1L · Clinician review packet</title><link rel="stylesheet" href="/style.css?v=header-20261010"><link rel="stylesheet" href="review.css"></head>
<body>{render_top_bar(lang_switch_href='/ukr/')}<main class="review-wrap">
<p class="eyebrow">OpenOnco · Prepared for clinician assessment</p><h1>DLBCL first-line review packet</h1>
<div class="notice"><strong>Clinical status: awaiting independent clinician review.</strong><p>{_e(DISCLAIMER)}</p></div>
<p>Inspect actual engine outputs, source provenance and edge cases before assessing the clinical rules. These isolated rule probes use supplied scores, not scores recalculated from a complete clinical vignette. They do not change the knowledge base.</p>
<div class="metrics"><div><strong>{summary['cases']}</strong><span>Synthetic scenarios</span></div><div><strong>{summary['contracts_passed']}/{summary['contracts_total']}</strong><span>Engineering checks</span></div><div><strong>{summary['cases_with_input_findings']}</strong><span>Targeted input findings</span></div><div><strong>Pending</strong><span>Clinical review</span></div></div>
<section class="review-intro"><h2>What to assess</h2><ol><li>Confirm each route and threshold against the applicable source, disease population and current evidence.</li><li>Check contraindications, monitoring, supportive care and local availability in both tracks.</li><li>Check how unknown, missing, negative and contradictory inputs are represented.</li><li>Check whether the original questionnaire captures the information used by the engine.</li></ol>
<p>Expected results below are existing rule contracts, not independently validated treatment choices. A PASS does not establish source grounding or clinical suitability. A recorded source date is not a fresh literature search.</p>
<details><summary>Questionnaire gaps to assess ({len(report['questionnaire_findings'])})</summary><ul>{gaps}</ul></details></section>
<section class="review-tools" aria-label="Review controls"><label>Scenario group<select id="category"><option value="all">All scenarios</option>{''.join(f'<option>{_e(c)}</option>' for c in sorted({x['category'] for x in report['cases']}))}</select></label><button id="export-review" type="button">Export my review (JSON)</button><button id="clear-review" type="button">Clear local review</button><a href="report.json" download>Technical report</a><a href="review-template.json" download>Blank review template</a><a href="provenance.json" download>Provenance</a><p id="save-status" role="status">Review comments stay in this browser. Export to retain a copy. No upload occurs.</p></section>
<div class="review-grid">{''.join(cards)}</div>
<section><h2>Sources referenced by the generated plans</h2><p>Listed as recorded in the KB. Applicability and currency remain review questions.</p><div class="table-scroll"><table><thead><tr><th>ID</th><th>Title</th><th>Last verified (recorded)</th><th>Link</th></tr></thead><tbody>{source_rows}</tbody></table></div></section>
<footer><p>Generated {_e(report['generated_at'])} · KB SHA-256 <code>{_e(report['kb_snapshot']['sha256'])}</code></p><p>Assessment notes are feedback only. They do not grant the repository's two-reviewer sign-off or change clinical content.</p></footer>
</main><script id="review-config" type="application/json">{payload}</script><script src="review.js" defer></script></body></html>'''


def build_clinician_review(kb_root: Path = KB_ROOT, output_dir: Path | None = None) -> dict:
    kb_root = Path(kb_root)
    output_dir = Path(output_dir or REPO_ROOT / "docs/review/dlbcl-1l")
    load = load_content(kb_root)
    if not load.ok:
        raise RuntimeError("Refusing to build clinician packet from an invalid knowledge base")
    output_dir.mkdir(parents=True, exist_ok=True)
    case_dir = output_dir / "cases"
    case_dir.mkdir(exist_ok=True)
    records, entity_ids = [], set()
    for case in scenarios():
        profile = make_profile(case, REPO_ROOT / "examples")
        result = generate_plan(profile, kb_root=kb_root)
        mdt = orchestrate_mdt(profile, result, kb_root=kb_root) if result.plan else None
        decision = _decision(result)
        flag = case["expected_flag"]
        checks = [{"name": "Authored routing contract", "passed": result.default_indication_id == case["expected_default"]},
                  {"name": "Resolved regimen references", "passed": all(t.regimen_data is not None for t in result.plan.tracks) if result.plan else True},
                  {"name": "Repeat run produces identical decision and trace", "passed": decision == _decision(generate_plan(profile, kb_root=kb_root))}]
        if flag:
            checks.append({"name": f"Trace exposes {flag}", "passed": flag in json.dumps(result.trace)})
        if case["expected_default"] is not None:
            checks.append({"name": "Alternatives visible", "passed": result.plan is not None and len(result.plan.tracks) >= 2})
        if case["category"] == "scope":
            checks.append({"name": "Unresolvable scope emits no current treatment tracks", "passed": not decision["tracks"]})
        record = {**case, "observed_default": result.default_indication_id,
                  "input_summary": {"Age": profile.get("demographics", {}).get("age"),
                      "ECOG": profile.get("demographics", {}).get("ecog"),
                      "IPI": profile.get("findings", {}).get("ipi_score"),
                      "CD20": profile.get("biomarkers", {}).get("BIO-CD20-IHC"),
                      "LVEF (%)": profile.get("findings", {}).get("lvef_percent"),
                      "CrCl (mL/min)": profile.get("findings", {}).get("creatinine_clearance_ml_min"),
                      "Bilirubin / ULN": profile.get("findings", {}).get("bilirubin_ratio_to_uln"),
                      "DLCO (%)": profile.get("findings", {}).get("dlco_percent"),
                      "HBsAg": profile.get("findings", {}).get("hbsag"),
                      "Anti-HBc total": profile.get("findings", {}).get("anti_hbc_total")},
                  "checks": checks, "input_findings": input_findings(profile, result),
                  "profile_sha256": _sha(_canonical(profile)), "decision_sha256": _sha(_canonical(decision)),
                  "clinical_review_status": "pending", "warnings": result.warnings,
                  "open_questions": [q.to_dict() for q in mdt.open_questions] if mdt else [],
                  "tracks": decision["tracks"]}
        records.append(record)
        entity_ids.update(_linked_entities(load, result))
        (case_dir / f"{case['id']}.profile.json").write_text(_json(profile), encoding="utf-8")
        (case_dir / f"{case['id']}.result.json").write_text(_json({"synthetic_only": True,
            "clinical_review_status": "pending", "result": result.to_dict(),
            "mdt": mdt.to_dict() if mdt else None}), encoding="utf-8")
        rendered = render_plan_html(result, mdt=mdt, target_lang="en")
        banner = f'<aside style="padding:16px;background:#fffbeb;border:2px solid #d97706;color:#78350f;font:16px/1.5 system-ui"><strong>{_e(DISCLAIMER)}</strong><p>{_e(case["title"])}</p><a href="../index.html#{_e(case["id"])}">Back to review packet</a></aside>'
        rendered = re.sub(r"(<body\b[^>]*>)", lambda match: match.group(1) + banner, rendered, count=1)
        rendered = re.sub(r"(<head\b[^>]*>)", lambda match: match.group(1) + '<meta name="robots" content="noindex,follow">', rendered, count=1)
        (case_dir / f"{case['id']}.html").write_text(rendered, encoding="utf-8")
    checks = [check for record in records for check in record["checks"]]
    report = {"schema_version": 1, "packet_id": "dlbcl-1l", "synthetic_only": True,
              "clinical_review_status": "pending", "generated_at": datetime.now(timezone.utc).isoformat(),
              "kb_snapshot": _snapshot(kb_root, ".yaml"),
              "engine_snapshot": _snapshot(REPO_ROOT / "knowledge_base", ".py"),
              "scenario_definition_sha256": _text_sha(Path(__file__).with_name("review_dlbcl_scenarios.py")),
              "summary": {"cases": len(records), "contracts_total": len(checks),
                          "contracts_passed": sum(c["passed"] for c in checks),
                          "cases_with_input_findings": sum(bool(c["input_findings"]) for c in records),
                          "groups": dict(Counter(c["category"] for c in records))},
              "questionnaire_findings": _questionnaire_gaps(load), "cases": records,
              "entities": [_entity_record(load.entities_by_id[eid], kb_root) for eid in sorted(entity_ids)]}
    (output_dir / "report.json").write_text(_json(report), encoding="utf-8")
    (output_dir / "provenance.json").write_text(_json({k: report[k] for k in
        ("schema_version", "packet_id", "kb_snapshot", "engine_snapshot", "scenario_definition_sha256", "entities")}), encoding="utf-8")
    (output_dir / "review-template.json").write_text(_json({"packet_id": report["packet_id"],
        "kb_sha256": report["kb_snapshot"]["sha256"], "engine_sha256": report["engine_snapshot"]["sha256"],
        "scenario_sha256": report["scenario_definition_sha256"], "clinical_signoff_granted": False,
        "cases": [{"case_id": c["id"], "assessment": "unreviewed", "comment": ""} for c in records]}), encoding="utf-8")
    (output_dir / "index.html").write_text(_index(report), encoding="utf-8")
    for asset in ("review.css", "review.js"):
        (output_dir / asset).write_text((ASSETS / asset).read_text(encoding="utf-8"), encoding="utf-8")
    (output_dir / "README.md").write_text(
        "# DLBCL first-line clinician review packet\n\n" + DISCLAIMER +
        "\n\nOpen index.html through the published site. Inspect each input, actual plan, trace and source. "
        "Assess each scenario and export feedback as JSON. Browser feedback is not a clinical sign-off. "
        "No real patient data is included or accepted by the builder.\n\n"
        "Rebuild: `python -m scripts.build_clinician_review`. Technical contracts: `--check`. "
        "The builder reads existing public synthetic seeds and does not change clinical YAML.\n", encoding="utf-8")
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--check", action="store_true", help="Exit nonzero if an engineering contract fails")
    args = parser.parse_args(argv)
    report = build_clinician_review(output_dir=args.output_dir)
    summary = report["summary"]
    print(f"{summary['cases']} synthetic scenarios; {summary['contracts_passed']}/{summary['contracts_total']} engineering checks; clinical review pending")
    return int(args.check and summary["contracts_passed"] != summary["contracts_total"])


if __name__ == "__main__":
    raise SystemExit(main())
