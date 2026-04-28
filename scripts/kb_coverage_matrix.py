"""KB coverage matrix generator.

Walks knowledge_base/hosted/content/ and emits docs/kb-coverage-matrix.md:

  - Per-disease rows (65) × axes (BMA / IND / RF / regimen / source-coverage)
  - Quality columns (clinical signoff %, ESCAT-tier %, citation density,
    recency, NSZU reimbursement %)
  - Top-level KPIs (entity counts, quality scores, gap counts)
  - Specific gap lists (diseases with 0 BMA, diseases without 5-type RF
    matrix, BMAs without ESCAT tier, etc.)

Run:
    py -V:3.12 -m scripts.kb_coverage_matrix
or:
    C:/Python312/python.exe -m scripts.kb_coverage_matrix

Read-only against the KB. Writes only docs/kb-coverage-matrix.md.
"""

from __future__ import annotations

import datetime as dt
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
OUT = REPO_ROOT / "docs" / "kb-coverage-matrix.md"

ESCAT_TIERS = ("IA", "IB", "IIA", "IIB", "IIIA", "IIIB", "IV", "V", "X")


def load_yaml(path: Path) -> dict | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def load_all(subdir: str) -> list[dict]:
    out: list[dict] = []
    d = KB_ROOT / subdir
    if not d.is_dir():
        return out
    for p in sorted(d.glob("*.yaml")):
        data = load_yaml(p)
        if data:
            data["__path"] = str(p.relative_to(REPO_ROOT)).replace("\\", "/")
            out.append(data)
    return out


@dataclass
class DiseaseRow:
    id: str
    name: str
    name_ua: str
    archetype: str
    bma_count: int = 0
    bma_with_escat: int = 0
    bma_with_civic: int = 0
    bma_signed_off_ua: int = 0
    ind_count: int = 0
    ind_with_outcomes: int = 0
    ind_with_nccn_cat: int = 0
    rf_count: int = 0
    rf_with_sources: int = 0
    rf_categories: set[str] = field(default_factory=set)
    regimens_referenced: set[str] = field(default_factory=set)
    sources_cited: set[str] = field(default_factory=set)
    has_questionnaire: bool = False
    molecular_subtypes_count: int = 0


def safe_pct(num: int, den: int) -> str:
    if den == 0:
        return "—"
    return f"{int(round(100 * num / den))}%"


def main() -> int:
    diseases = load_all("diseases")
    bmas = load_all("biomarker_actionability")
    inds = load_all("indications")
    rfs = load_all("redflags")
    drugs = load_all("drugs")
    sources = load_all("sources")
    regimens = load_all("regimens")
    questionnaires = load_all("questionnaires")
    biomarkers = load_all("biomarkers")
    algorithms = load_all("algorithms")

    rows: dict[str, DiseaseRow] = {}
    for d in diseases:
        did = d.get("id", "")
        names = d.get("names", {}) or {}
        rows[did] = DiseaseRow(
            id=did,
            name=names.get("preferred") or names.get("english") or did,
            name_ua=names.get("ukrainian") or "",
            archetype=d.get("archetype") or "",
            molecular_subtypes_count=len(d.get("molecular_subtypes") or []),
        )

    # BMA pass
    for b in bmas:
        did = b.get("disease_id")
        if did not in rows:
            continue
        row = rows[did]
        row.bma_count += 1
        if b.get("escat_tier") in ESCAT_TIERS:
            row.bma_with_escat += 1
        es = b.get("evidence_sources") or []
        if any(isinstance(e, dict) and e.get("source") == "SRC-CIVIC" for e in es):
            row.bma_with_civic += 1
        if b.get("ukrainian_review_status") == "signed_off":
            row.bma_signed_off_ua += 1

    # IND pass
    for i in inds:
        applicable = i.get("applicable_to", {}) or {}
        did = applicable.get("disease_id")
        if did not in rows:
            continue
        row = rows[did]
        row.ind_count += 1
        if i.get("expected_outcomes"):
            row.ind_with_outcomes += 1
        if i.get("nccn_category"):
            row.ind_with_nccn_cat += 1
        reg = i.get("recommended_regimen")
        if reg:
            row.regimens_referenced.add(reg)
        for s in i.get("primary_sources", []) or []:
            row.sources_cited.add(s)

    # RF pass
    for rf in rfs:
        rel = rf.get("relevant_diseases") or []
        cat = rf.get("category") or ""
        for did in rel:
            if did not in rows:
                continue
            row = rows[did]
            row.rf_count += 1
            if rf.get("sources"):
                row.rf_with_sources += 1
            if cat:
                row.rf_categories.add(cat)
            for s in rf.get("sources", []) or []:
                row.sources_cited.add(s)

    # Questionnaires (simple file-name heuristic)
    q_diseases = set()
    for q in questionnaires:
        # questionnaire id format heuristic: QUES-<DISEASE>
        qid = q.get("id") or ""
        m = re.match(r"^QUES[-_](.+?)(?:[-_]|$)", qid)
        if m:
            q_diseases.add(f"DIS-{m.group(1).upper().replace('_', '-')}")
    for did, row in rows.items():
        row.has_questionnaire = did in q_diseases or any(
            (q.get("disease_id") == did) for q in questionnaires
        )

    # ----- Top-level metrics -----

    total_entities = (
        len(diseases) + len(bmas) + len(inds) + len(rfs) + len(drugs)
        + len(sources) + len(regimens) + len(biomarkers) + len(algorithms)
    )

    bmas_with_escat = sum(1 for b in bmas if b.get("escat_tier") in ESCAT_TIERS)
    bmas_with_civic = sum(
        1 for b in bmas
        if any(isinstance(e, dict) and e.get("source") == "SRC-CIVIC"
               for e in (b.get("evidence_sources") or []))
    )
    bmas_signed_off_ua = sum(1 for b in bmas if b.get("ukrainian_review_status") == "signed_off")
    bmas_pending_ua = sum(1 for b in bmas if b.get("ukrainian_review_status") == "pending_clinical_signoff")

    inds_with_outcomes = sum(1 for i in inds if i.get("expected_outcomes"))
    inds_with_nccn = sum(1 for i in inds if i.get("nccn_category"))

    rfs_with_sources = sum(1 for r in rfs if r.get("sources"))
    rfs_with_review_date = sum(1 for r in rfs if r.get("last_reviewed"))

    # Source recency
    today = dt.date.today()
    src_recent = 0
    src_with_license = 0
    for s in sources:
        lic = s.get("license") or {}
        if lic.get("name") or lic.get("spdx_id"):
            src_with_license += 1
        cao = s.get("current_as_of")
        if isinstance(cao, str):
            try:
                d = dt.date.fromisoformat(cao[:10])
                if (today - d).days < 365:
                    src_recent += 1
            except ValueError:
                pass

    # Drug NSZU coverage
    drugs_nszu = sum(
        1 for d in drugs
        if (d.get("regulatory_status", {}) or {})
            .get("ukraine_registration", {}).get("reimbursed_nszu") is True
    )
    drugs_ua_registered = sum(
        1 for d in drugs
        if (d.get("regulatory_status", {}) or {})
            .get("ukraine_registration", {}).get("registered") is True
    )

    # ESCAT tier distribution
    escat_dist: Counter[str] = Counter()
    for b in bmas:
        t = b.get("escat_tier")
        escat_dist[t if t in ESCAT_TIERS else "(unset)"] += 1

    # ----- Gap lists -----

    diseases_no_bma = [r for r in rows.values() if r.bma_count == 0]
    diseases_thin_bma = [r for r in rows.values() if 0 < r.bma_count < 3]
    diseases_no_rf = [r for r in rows.values() if r.rf_count == 0]
    diseases_no_questionnaire = [r for r in rows.values() if not r.has_questionnaire]
    diseases_no_indication = [r for r in rows.values() if r.ind_count == 0]

    bmas_without_escat = [b for b in bmas if b.get("escat_tier") not in ESCAT_TIERS]
    bmas_without_civic = [
        b for b in bmas
        if not any(isinstance(e, dict) and e.get("source") == "SRC-CIVIC"
                   for e in (b.get("evidence_sources") or []))
    ]
    inds_without_outcomes = [i for i in inds if not i.get("expected_outcomes")]
    rfs_without_sources = [r for r in rfs if not r.get("sources")]

    # ----- Render -----

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# KB Coverage Matrix")
    lines.append("")
    lines.append(f"_Generated_: {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")
    lines.append(
        "Auto-generated from `knowledge_base/hosted/content/` by "
        "`scripts/kb_coverage_matrix.py`. **Do not edit by hand** — re-run the "
        "script. The strategy doc that explains how to read this is "
        "[`kb-coverage-strategy.md`](kb-coverage-strategy.md)."
    )
    lines.append("")

    # ===== Top-level KPIs =====

    lines.append("## Top-level KPIs")
    lines.append("")
    lines.append("| Entity | Count |")
    lines.append("|---|---:|")
    lines.append(f"| Diseases | {len(diseases)} |")
    lines.append(f"| Biomarker_actionability (BMA) | {len(bmas)} |")
    lines.append(f"| Indications | {len(inds)} |")
    lines.append(f"| Red flags | {len(rfs)} |")
    lines.append(f"| Drugs | {len(drugs)} |")
    lines.append(f"| Regimens | {len(regimens)} |")
    lines.append(f"| Sources | {len(sources)} |")
    lines.append(f"| Biomarkers | {len(biomarkers)} |")
    lines.append(f"| Algorithms | {len(algorithms)} |")
    lines.append(f"| Questionnaires | {len(questionnaires)} |")
    lines.append(f"| **Total entities** | **{total_entities}** |")
    lines.append("")

    # ===== Quality scores =====

    lines.append("## Quality scores")
    lines.append("")
    lines.append("| Axis | Numerator | Denominator | Score |")
    lines.append("|---|---:|---:|---:|")
    lines.append(f"| BMA with ESCAT tier | {bmas_with_escat} | {len(bmas)} | {safe_pct(bmas_with_escat, len(bmas))} |")
    lines.append(f"| BMA with CIViC evidence_sources | {bmas_with_civic} | {len(bmas)} | {safe_pct(bmas_with_civic, len(bmas))} |")
    lines.append(f"| BMA UA-signed-off | {bmas_signed_off_ua} | {len(bmas)} | {safe_pct(bmas_signed_off_ua, len(bmas))} |")
    lines.append(f"| BMA UA pending review | {bmas_pending_ua} | {len(bmas)} | {safe_pct(bmas_pending_ua, len(bmas))} |")
    lines.append(f"| Indications with expected_outcomes | {inds_with_outcomes} | {len(inds)} | {safe_pct(inds_with_outcomes, len(inds))} |")
    lines.append(f"| Indications with NCCN category | {inds_with_nccn} | {len(inds)} | {safe_pct(inds_with_nccn, len(inds))} |")
    lines.append(f"| RF with sources | {rfs_with_sources} | {len(rfs)} | {safe_pct(rfs_with_sources, len(rfs))} |")
    lines.append(f"| RF with last_reviewed | {rfs_with_review_date} | {len(rfs)} | {safe_pct(rfs_with_review_date, len(rfs))} |")
    lines.append(f"| Sources with license declared | {src_with_license} | {len(sources)} | {safe_pct(src_with_license, len(sources))} |")
    lines.append(f"| Sources current_as_of <365d | {src_recent} | {len(sources)} | {safe_pct(src_recent, len(sources))} |")
    lines.append(f"| Drugs UA-registered | {drugs_ua_registered} | {len(drugs)} | {safe_pct(drugs_ua_registered, len(drugs))} |")
    lines.append(f"| Drugs NSZU-reimbursed | {drugs_nszu} | {len(drugs)} | {safe_pct(drugs_nszu, len(drugs))} |")
    lines.append("")

    # ===== ESCAT distribution =====

    lines.append("## ESCAT tier distribution (across 399 BMAs)")
    lines.append("")
    lines.append("| Tier | Count | % |")
    lines.append("|---|---:|---:|")
    for t in ESCAT_TIERS + ("(unset)",):
        c = escat_dist.get(t, 0)
        lines.append(f"| {t} | {c} | {safe_pct(c, len(bmas))} |")
    lines.append("")

    # ===== Per-disease matrix =====

    lines.append("## Per-disease coverage matrix")
    lines.append("")
    lines.append(
        "Sorted by (BMA + IND + RF) descending. Diseases with 0 across "
        "all axes are listed under \"Coverage gaps\" below."
    )
    lines.append("")
    lines.append(
        "| Disease | Archetype | Subtypes | BMA | ESCAT% | CIViC% | UA✓ | IND | "
        "Outcomes% | NCCN% | RF | RF cats | Regimens | Sources | Quest |"
    )
    lines.append(
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|"
    )

    sorted_rows = sorted(
        rows.values(),
        key=lambda r: (r.bma_count + r.ind_count + r.rf_count),
        reverse=True,
    )
    for r in sorted_rows:
        if r.bma_count + r.ind_count + r.rf_count == 0:
            continue  # in gap section
        lines.append(
            "| {name} | {arch} | {sub} | {bma} | {escat} | {civic} | {ua} | "
            "{ind} | {out} | {nccn} | {rf} | {rfcat} | {reg} | {src} | {q} |".format(
                name=f"{r.name} ({r.id.replace('DIS-', '')})",
                arch=r.archetype or "—",
                sub=r.molecular_subtypes_count or "—",
                bma=r.bma_count,
                escat=safe_pct(r.bma_with_escat, r.bma_count),
                civic=safe_pct(r.bma_with_civic, r.bma_count),
                ua=safe_pct(r.bma_signed_off_ua, r.bma_count),
                ind=r.ind_count,
                out=safe_pct(r.ind_with_outcomes, r.ind_count),
                nccn=safe_pct(r.ind_with_nccn_cat, r.ind_count),
                rf=r.rf_count,
                rfcat=len(r.rf_categories),
                reg=len(r.regimens_referenced),
                src=len(r.sources_cited),
                q="✓" if r.has_questionnaire else "—",
            )
        )
    lines.append("")

    # ===== Coverage gaps =====

    lines.append("## Coverage gaps")
    lines.append("")

    lines.append(f"### Diseases with **zero BMA** ({len(diseases_no_bma)})")
    lines.append("")
    if diseases_no_bma:
        lines.append("| Disease | Archetype | IND | RF |")
        lines.append("|---|---|---:|---:|")
        for r in sorted(diseases_no_bma, key=lambda x: x.id):
            lines.append(f"| {r.name} ({r.id}) | {r.archetype or '—'} | {r.ind_count} | {r.rf_count} |")
    lines.append("")

    lines.append(f"### Diseases with **thin BMA coverage (1-2 entries)** ({len(diseases_thin_bma)})")
    lines.append("")
    if diseases_thin_bma:
        lines.append("| Disease | BMA |")
        lines.append("|---|---:|")
        for r in sorted(diseases_thin_bma, key=lambda x: x.bma_count):
            lines.append(f"| {r.name} ({r.id}) | {r.bma_count} |")
    lines.append("")

    lines.append(f"### Diseases with **zero red-flags** ({len(diseases_no_rf)})")
    lines.append("")
    if diseases_no_rf:
        for r in sorted(diseases_no_rf, key=lambda x: x.id):
            lines.append(f"- {r.name} ({r.id})")
    lines.append("")

    lines.append(f"### Diseases with **zero indications** ({len(diseases_no_indication)})")
    lines.append("")
    if diseases_no_indication:
        for r in sorted(diseases_no_indication, key=lambda x: x.id):
            lines.append(f"- {r.name} ({r.id})")
    lines.append("")

    lines.append(f"### Diseases with **no questionnaire** ({len(diseases_no_questionnaire)})")
    lines.append("")
    if diseases_no_questionnaire:
        for r in sorted(diseases_no_questionnaire, key=lambda x: x.id)[:30]:
            lines.append(f"- {r.name} ({r.id})")
        if len(diseases_no_questionnaire) > 30:
            lines.append(f"- … and {len(diseases_no_questionnaire) - 30} more")
    lines.append("")

    # ===== Quality gaps =====

    lines.append("## Quality gaps")
    lines.append("")
    lines.append(f"- **{len(bmas_without_escat)}** BMAs without ESCAT tier")
    lines.append(f"- **{len(bmas_without_civic)}** BMAs without CIViC evidence_sources")
    lines.append(f"- **{len(inds_without_outcomes)}** indications without `expected_outcomes` block")
    lines.append(f"- **{len(rfs_without_sources)}** redflags without `sources` block")
    lines.append("")

    # ===== Footer =====

    lines.append("---")
    lines.append("")
    lines.append("## How to act on this matrix")
    lines.append("")
    lines.append(
        "Each new TaskTorrent chunk should reference a specific cell or gap "
        "and state how it advances coverage. Example chunk-spec preamble: "
        "_\"This chunk advances `Per-disease matrix > breast_cancer > IND-Outcomes%` "
        "from 60% to 95% by adding expected_outcomes to 12 missing indications.\"_"
    )
    lines.append("")
    lines.append(
        "Re-run this script after each KB-mutating PR is applied. Schedule "
        "weekly via cron once the strategy doc lands."
    )

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(REPO_ROOT)}")
    print(f"  diseases={len(diseases)}  BMA={len(bmas)}  IND={len(inds)}  RF={len(rfs)}  drugs={len(drugs)}  sources={len(sources)}")
    print(f"  diseases-with-zero-BMA={len(diseases_no_bma)}  no-RF={len(diseases_no_rf)}  no-IND={len(diseases_no_indication)}")
    print(f"  BMAs-without-ESCAT={len(bmas_without_escat)}  BMAs-without-CIViC={len(bmas_without_civic)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
