"""Audit the five largest clinical-coverage gaps.

This script turns broad roadmap language into a repeatable snapshot:

1. Clinical sign-off throughput.
2. Solid-tumor 2L+ coverage.
3. Structured surgery/radiation modeling.
4. Supportive-care depth on regimens.
5. Explicit on-label/off-label drug-indication tracking.

It intentionally does not create clinical recommendations. The output is a
governance and coverage artifact that tells maintainers which work is blocked
on clinical reviewers and which work is blocked on schema/data modeling.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from knowledge_base.validation.loader import load_content


REPO_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"

SIGNOFF_TYPES = (
    "indications",
    "algorithms",
    "regimens",
    "redflags",
    "biomarker_actionability",
)

SOLID_LINEAGE_TOKENS = (
    "carcinoma",
    "sarcoma",
    "solid",
    "skin",
    "ovarian",
    "squamous",
    "neuroendocrine",
    "mesothelial",
    "cns",
    "glioma",
    "rare_lung",
)

HEME_LINEAGE_TOKENS = (
    "lymphoma",
    "leukemia",
    "myeloid",
    "plasma_cell",
    "hodgkin",
    "mastocytosis",
)

RADIATION_TOKENS = ("radiation", "radiotherapy", "rt", "chemoradiation", "crt")
SURGERY_TOKENS = ("surgery", "surgical", "resection", "operative", "adjuvant")


@dataclass(frozen=True)
class GapMetric:
    id: str
    title: str
    current: str
    target: str
    status: str
    blocker: str
    next_action: str
    details: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "current": self.current,
            "target": self.target,
            "status": self.status,
            "blocker": self.blocker,
            "next_action": self.next_action,
            "details": self.details,
        }


def _signoff_count(value: Any) -> int:
    if isinstance(value, list):
        return len(value)
    if isinstance(value, int):
        return value
    return 0


def _name(entity: dict[str, Any]) -> str:
    names = entity.get("names") or {}
    return (
        names.get("english")
        or names.get("preferred")
        or entity.get("name")
        or entity.get("id")
        or "unknown"
    )


def _is_solid_disease(entity: dict[str, Any]) -> bool:
    lineage = str(entity.get("lineage") or "").lower()
    if any(token in lineage for token in HEME_LINEAGE_TOKENS):
        return False
    if any(token in lineage for token in SOLID_LINEAGE_TOKENS):
        return True
    # Conservative fallback: if it is not clearly heme, treat it as a solid
    # coverage row so it gets reviewed rather than silently skipped.
    return True


def _entity_type(result, etype: str) -> list[dict[str, Any]]:
    return [
        info["data"]
        for info in result.entities_by_id.values()
        if info["type"] == etype
    ]


def _entity_map(result, etype: str) -> dict[str, dict[str, Any]]:
    return {
        str(info["data"].get("id") or eid): info["data"]
        for eid, info in result.entities_by_id.items()
        if info["type"] == etype
    }


def _walk_source_ids(node: Any) -> set[str]:
    out: set[str] = set()
    if isinstance(node, dict):
        for value in node.values():
            out |= _walk_source_ids(value)
    elif isinstance(node, list):
        for item in node:
            out |= _walk_source_ids(item)
    elif isinstance(node, str) and node.startswith("SRC-"):
        out.add(node)
    return out


def _walk_text(node: Any) -> str:
    parts: list[str] = []
    if isinstance(node, dict):
        for value in node.values():
            parts.append(_walk_text(value))
    elif isinstance(node, list):
        for item in node:
            parts.append(_walk_text(item))
    elif isinstance(node, str):
        parts.append(node.lower())
    return " ".join(parts)


def _regimen_drugs(regimen: dict[str, Any]) -> set[str]:
    drugs: set[str] = set()

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            drug_id = node.get("drug_id")
            if isinstance(drug_id, str) and drug_id.startswith("DRUG-"):
                drugs.add(drug_id)
            for value in node.values():
                visit(value)
        elif isinstance(node, list):
            for item in node:
                visit(item)

    visit(regimen)
    return drugs


def audit(root: Path = KB_ROOT) -> dict[str, Any]:
    result = load_content(root)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    entities = result.entities_by_id
    by_type_counts: dict[str, int] = {}
    for info in entities.values():
        by_type_counts[info["type"]] = by_type_counts.get(info["type"], 0) + 1

    diseases = _entity_type(result, "diseases")
    algorithms = _entity_type(result, "algorithms")
    indications = _entity_type(result, "indications")
    regimens = _entity_type(result, "regimens")
    regimen_by_id = _entity_map(result, "regimens")

    # 1. Clinical sign-off.
    signoff_total = 0
    signoff_reviewed = 0
    signoff_by_type: dict[str, dict[str, int]] = {}
    for etype in SIGNOFF_TYPES:
        rows = _entity_type(result, etype)
        total = len(rows)
        reviewed = sum(1 for row in rows if _signoff_count(row.get("reviewer_signoffs")) >= 2)
        signoff_total += total
        signoff_reviewed += reviewed
        signoff_by_type[etype] = {"total": total, "reviewed": reviewed, "gap": total - reviewed}
    signoff_pct = round(100 * signoff_reviewed / max(1, signoff_total), 1)

    # 2. Solid tumor 2L+ coverage.
    solid_diseases = {str(d.get("id")): d for d in diseases if _is_solid_disease(d)}
    solid_with_2l_algo = {
        str(a.get("applicable_to_disease"))
        for a in algorithms
        if int(a.get("applicable_to_line_of_therapy") or 0) >= 2
        and str(a.get("applicable_to_disease")) in solid_diseases
    }
    solid_with_2l_ind = {
        str((i.get("applicable_to") or {}).get("disease_id"))
        for i in indications
        if int((i.get("applicable_to") or {}).get("line_of_therapy") or 0) >= 2
        and str((i.get("applicable_to") or {}).get("disease_id")) in solid_diseases
    }
    solid_missing_2l = sorted(set(solid_diseases) - solid_with_2l_algo)

    # 3. Surgery/radiation structure.
    has_surgery_dir = (root / "surgery").is_dir()
    has_radiation_dir = (root / "radiation").is_dir() or (root / "radiotherapy").is_dir()
    indication_text_rows = [
        i
        for i in indications
        if any(token in _walk_text(i) for token in SURGERY_TOKENS + RADIATION_TOKENS)
    ]
    radiation_mentions = [
        i.get("id") for i in indications
        if any(token in _walk_text(i) for token in RADIATION_TOKENS)
    ]
    surgery_mentions = [
        i.get("id") for i in indications
        if any(token in _walk_text(i) for token in SURGERY_TOKENS)
    ]

    # 4. Supportive-care depth.
    regimens_with_supportive = [
        r for r in regimens if r.get("mandatory_supportive_care")
    ]
    regimens_with_premed = [r for r in regimens if r.get("premedication")]
    regimens_with_monitoring = [r for r in regimens if r.get("monitoring_schedule_id")]
    regimens_with_dose_adjustments = [r for r in regimens if r.get("dose_adjustments")]
    regimens_with_watchpoints = [r for r in regimens if r.get("between_visit_watchpoints")]
    support_depth_pct = round(
        100 * len(regimens_with_supportive) / max(1, len(regimens)),
        1,
    )

    # 5. On-label/off-label drug indication tracking.
    indication_drug_pairs: set[tuple[str, str, str]] = set()
    indication_pairs_with_evidence = 0
    for ind in indications:
        ind_id = str(ind.get("id"))
        disease_id = str((ind.get("applicable_to") or {}).get("disease_id") or "")
        reg_id = ind.get("recommended_regimen")
        reg = regimen_by_id.get(str(reg_id)) if reg_id else None
        if not reg:
            continue
        drugs = _regimen_drugs(reg)
        if _walk_source_ids(ind) or ind.get("nccn_category") or ind.get("evidence_level"):
            indication_pairs_with_evidence += len(drugs)
        for drug_id in drugs:
            indication_drug_pairs.add((drug_id, disease_id, ind_id))
    explicit_label_status_pairs = 0
    label_status_schema_present = (root / "drug_indications").is_dir()

    gaps = [
        GapMetric(
            id="clinical_signoff",
            title="Clinical sign-off",
            current=f"{signoff_reviewed}/{signoff_total} signoff-eligible entities reviewed ({signoff_pct}%)",
            target=">=85% reviewed before public guideline-grade claims",
            status="blocked_on_reviewers",
            blocker="Cannot be fixed by code; requires qualified Clinical Co-Lead review.",
            next_action="Batch the largest STUB queues by entity type and assign reviewer owners.",
            details={"by_type": signoff_by_type},
        ),
        GapMetric(
            id="solid_2l_plus",
            title="Solid tumor 2L+ coverage",
            current=(
                f"{len(solid_with_2l_algo)}/{len(solid_diseases)} solid diseases have a 2L+ algorithm; "
                f"{len(solid_with_2l_ind)}/{len(solid_diseases)} have a 2L+ indication"
            ),
            target="Every modeled solid disease has at least one advanced/relapsed-line algorithm and indication.",
            status="coverage_gap",
            blocker="Missing disease-by-disease 2L+ algorithm/indication authoring queue.",
            next_action="Prioritize missing high-volume solid diseases, then rare solid diseases.",
            details={
                "solid_total": len(solid_diseases),
                "with_2l_algorithm": sorted(solid_with_2l_algo),
                "with_2l_indication": sorted(solid_with_2l_ind),
                "missing_2l_algorithm": [
                    {"id": did, "name": _name(solid_diseases[did])}
                    for did in solid_missing_2l
                ],
            },
        ),
        GapMetric(
            id="surgery_radiation_structure",
            title="Surgery/radiation detail",
            current=(
                "structured surgery entities: "
                f"{'yes' if has_surgery_dir else 'no'}; structured radiation entities: "
                f"{'yes' if has_radiation_dir else 'no'}; "
                f"{len(indication_text_rows)} indications mention surgery/radiation in text"
            ),
            target="Dedicated modality entities for surgery and radiation with dose/fraction/intent/timing fields.",
            status="schema_gap",
            blocker="Current KB carries surgery/radiation mostly as prose inside indications.",
            next_action="Add modality schemas first; migrate prose mentions after clinical review.",
            details={
                "has_surgery_entity_dir": has_surgery_dir,
                "has_radiation_entity_dir": has_radiation_dir,
                "surgery_mentions": sorted(x for x in surgery_mentions if x)[:80],
                "radiation_mentions": sorted(x for x in radiation_mentions if x)[:80],
                "mention_count": len(indication_text_rows),
            },
        ),
        GapMetric(
            id="supportive_care_depth",
            title="Supportive-care depth",
            current=(
                f"{len(regimens_with_supportive)}/{len(regimens)} regimens have mandatory supportive care "
                f"({support_depth_pct}%); {len(regimens_with_monitoring)} have monitoring; "
                f"{len(regimens_with_dose_adjustments)} have dose adjustments"
            ),
            target="Every active regimen has supportive care, monitoring, dose-adjustment, and patient-watchpoint coverage.",
            status="coverage_gap",
            blocker="Supportive-care records exist, but regimen attachment is incomplete.",
            next_action="Audit high-toxicity regimens first, then fill missing regimen attachments.",
            details={
                "regimens_total": len(regimens),
                "with_mandatory_supportive_care": len(regimens_with_supportive),
                "with_premedication": len(regimens_with_premed),
                "with_monitoring": len(regimens_with_monitoring),
                "with_dose_adjustments": len(regimens_with_dose_adjustments),
                "with_between_visit_watchpoints": len(regimens_with_watchpoints),
                "missing_mandatory_supportive_care": sorted(
                    str(r.get("id")) for r in regimens if not r.get("mandatory_supportive_care")
                )[:120],
            },
        ),
        GapMetric(
            id="drug_indication_tracking",
            title="Drug indication and off-label tracking",
            current=(
                f"{len(indication_drug_pairs)} drug-disease-indication pairs inferred from regimens; "
                f"{explicit_label_status_pairs} carry explicit labeled/off-label status"
            ),
            target="Every drug-use pair has explicit regulatory-label status, NCCN/ESMO category, and source provenance.",
            status="schema_gap",
            blocker="No first-class drug_indications entity directory/schema is present.",
            next_action="Introduce a drug_indications entity, then backfill from existing indications/regimens.",
            details={
                "drug_indications_schema_present": label_status_schema_present,
                "inferred_drug_disease_indication_pairs": len(indication_drug_pairs),
                "pairs_with_indication_evidence_context": indication_pairs_with_evidence,
                "explicit_label_status_pairs": explicit_label_status_pairs,
                "sample_pairs": [
                    {"drug_id": drug, "disease_id": disease, "indication_id": ind}
                    for drug, disease, ind in sorted(indication_drug_pairs)[:80]
                ],
            },
        ),
    ]

    return {
        "generated_at_utc": generated_at,
        "kb_root": str(root),
        "entity_counts": by_type_counts,
        "loader_ok": result.ok,
        "loader_error_counts": {
            "schema_errors": len(result.schema_errors),
            "ref_errors": len(result.ref_errors),
            "contract_errors": len(result.contract_errors),
            "contract_warnings": len(result.contract_warnings),
        },
        "gaps": [gap.to_dict() for gap in gaps],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Clinical gap audit")
    lines.append("")
    lines.append(f"Generated: `{report['generated_at_utc']}`")
    lines.append("")
    lines.append("This is a coverage/governance audit, not a clinical recommendation set.")
    lines.append("It makes the five largest known gaps measurable and repeatable.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Gap | Current | Target | Status |")
    lines.append("|---|---:|---|---|")
    for gap in report["gaps"]:
        lines.append(
            f"| {gap['title']} | {gap['current']} | {gap['target']} | `{gap['status']}` |"
        )
    lines.append("")
    lines.append("## Next actions")
    lines.append("")
    for gap in report["gaps"]:
        lines.append(f"### {gap['title']}")
        lines.append("")
        lines.append(f"- Blocker: {gap['blocker']}")
        lines.append(f"- Next action: {gap['next_action']}")
        details = gap.get("details") or {}
        if gap["id"] == "solid_2l_plus":
            missing = details.get("missing_2l_algorithm") or []
            lines.append(f"- Missing 2L+ algorithm rows: {len(missing)}")
            for row in missing[:25]:
                lines.append(f"  - `{row['id']}`: {row['name']}")
        elif gap["id"] == "supportive_care_depth":
            missing = details.get("missing_mandatory_supportive_care") or []
            lines.append(f"- Regimens missing mandatory supportive care: {len(missing)} shown below")
            for rid in missing[:40]:
                lines.append(f"  - `{rid}`")
        elif gap["id"] == "drug_indication_tracking":
            lines.append(
                f"- Inferred pairs to backfill: {details.get('inferred_drug_disease_indication_pairs', 0)}"
            )
            lines.append(
                f"- Explicit labeled/off-label statuses: {details.get('explicit_label_status_pairs', 0)}"
            )
        lines.append("")
    lines.append("## Machine-readable outputs")
    lines.append("")
    lines.append("- `docs/audits/clinical_gap_audit.json`")
    lines.append("- `docs/audits/clinical_gap_audit.md`")
    lines.append("- `docs/clinical-gaps.html`")
    return "\n".join(lines) + "\n"


def render_html(report: dict[str, Any], *, target_lang: str = "en") -> str:
    title = "Clinical Gap Audit"
    nav_prefix = "/ukr" if target_lang == "uk" else ""
    rows = []
    cards = []
    for gap in report["gaps"]:
        rows.append(
            "<tr>"
            f"<td>{html.escape(gap['title'])}</td>"
            f"<td>{html.escape(gap['current'])}</td>"
            f"<td>{html.escape(gap['target'])}</td>"
            f"<td><code>{html.escape(gap['status'])}</code></td>"
            "</tr>"
        )
        cards.append(
            '<div class="gap-card">'
            f"<div class=\"gap-tag\">{html.escape(gap['status'])}</div>"
            f"<h3>{html.escape(gap['title'])}</h3>"
            f"<p><strong>Current:</strong> {html.escape(gap['current'])}</p>"
            f"<p><strong>Blocker:</strong> {html.escape(gap['blocker'])}</p>"
            f"<p><strong>Next:</strong> {html.escape(gap['next_action'])}</p>"
            "</div>"
        )
    return f"""<!DOCTYPE html>
<html lang="{html.escape(target_lang)}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenOnco · {title}</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link href="/style.css" rel="stylesheet">
</head>
<body>
<header class="top-bar">
  <div class="brand-line">
    <a href="{nav_prefix or '/'}" class="brand-mini"><img src="/logo.svg" alt="" class="brand-logo" width="30" height="30">OpenOnco</a>
  </div>
  <nav class="top-nav">
    <a href="{nav_prefix or '/'}">Home</a>
    <a href="{nav_prefix}/capabilities.html">Capabilities</a>
    <a href="{nav_prefix}/kb.html">Onco Wiki</a>
  </nav>
</header>
<main>
  <section class="info-page">
    <h1>{title}</h1>
    <p class="lead">
      Generated {html.escape(report['generated_at_utc'])}. This page tracks
      the largest remaining clinical-coverage gaps. It is a maintainer audit,
      not clinical guidance.
    </p>
    <table class="kv-table">
      <thead><tr><th>Gap</th><th>Current</th><th>Target</th><th>Status</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
    <div class="gap-grid">{''.join(cards)}</div>
    <div class="callout">
      Detailed JSON and Markdown are published under <code>/audits/clinical_gap_audit.json</code>
      and <code>/audits/clinical_gap_audit.md</code>.
    </div>
  </section>
</main>
</body>
</html>
"""


def write_outputs(output_dir: Path, *, root: Path = KB_ROOT) -> dict[str, str]:
    report = audit(root)
    audits_dir = output_dir / "audits"
    audits_dir.mkdir(parents=True, exist_ok=True)
    json_path = audits_dir / "clinical_gap_audit.json"
    md_path = audits_dir / "clinical_gap_audit.md"
    html_path = output_dir / "clinical-gaps.html"
    uk_html_path = output_dir / "ukr" / "clinical-gaps.html"
    uk_html_path.parent.mkdir(parents=True, exist_ok=True)

    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    html_path.write_text(render_html(report, target_lang="en"), encoding="utf-8")
    uk_html_path.write_text(render_html(report, target_lang="uk"), encoding="utf-8")
    return {
        "json": str(json_path),
        "markdown": str(md_path),
        "html": str(html_path),
        "html_uk": str(uk_html_path),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit major clinical coverage gaps.")
    parser.add_argument("--root", default=str(KB_ROOT), help="KB content root.")
    parser.add_argument("--output-json", help="Write JSON report.")
    parser.add_argument("--output-md", help="Write Markdown report.")
    parser.add_argument("--output-html", help="Write HTML report.")
    args = parser.parse_args(argv)

    report = audit(Path(args.root))
    if args.output_json:
        Path(args.output_json).write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    if args.output_md:
        Path(args.output_md).write_text(render_markdown(report), encoding="utf-8")
    if args.output_html:
        Path(args.output_html).write_text(render_html(report), encoding="utf-8")
    if not (args.output_json or args.output_md or args.output_html):
        print(render_markdown(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
