"""Per-disease coverage matrix — biomarkers, drugs, fill %, verified %.

For each Disease in the KB:
  - biomarker_count: # of distinct biomarkers referenced by indications
  - drug_count: # of distinct drugs referenced by regimens used in indications
  - indications_count, regimens_count, redflags_count
  - has_algorithm_1L, has_algorithm_2L (boolean)
  - has_questionnaire (boolean) + is_stub
  - has_workup (boolean)
  - fill_pct: composite % across 8 expected entity types
  - verified_pct: weighted % of indications with reviewer_signoffs ≥ 2
  - outcomes_cited_pct: loose %-cited from
    ``scripts/audit_expected_outcomes.disease_outcomes_cited_pct``
    (Phase 2 — Pivotal Trial Outcomes Ingestion Plan). Reuses the
    audit's bucketing instead of duplicating it; if the audit module
    fails to import (e.g. PyYAML missing in a stripped harness),
    the column falls back to ``n/a``.

Outputs Markdown table grouped by disease family (lymphoid heme,
myeloid heme, solid tumor) for readability.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _signoff_count(value) -> int:
    """Count reviewer sign-offs across legacy int + structured list shapes."""
    if isinstance(value, list):
        return len(value)
    if isinstance(value, int):
        return value
    return 0

from knowledge_base.validation.loader import load_content  # noqa: E402


# ── Disease family tagging ────────────────────────────────────────────────


_LYMPHOID_HEME = {
    "DIS-MM", "DIS-DLBCL-NOS", "DIS-FL", "DIS-CLL", "DIS-MCL",
    "DIS-SPLENIC-MZL", "DIS-NODAL-MZL", "DIS-HCV-MZL", "DIS-BURKITT",
    "DIS-HCL", "DIS-WM", "DIS-HGBL-DH", "DIS-PTCL-NOS", "DIS-ALCL",
    "DIS-AITL", "DIS-MF-SEZARY", "DIS-CHL", "DIS-NLPBL", "DIS-PMBCL",
    "DIS-PCNSL", "DIS-B-ALL", "DIS-T-ALL", "DIS-PTLD", "DIS-EATL",
    "DIS-HSTCL", "DIS-NK-T-NASAL", "DIS-ATLL", "DIS-T-PLL",
}
_MYELOID_HEME = {
    "DIS-AML", "DIS-APL", "DIS-CML", "DIS-MDS-LR", "DIS-MDS-HR",
    "DIS-PV", "DIS-ET", "DIS-PMF", "DIS-MASTOCYTOSIS",
}


def _family(disease_id: str) -> str:
    if disease_id in _LYMPHOID_HEME:
        return "Лімфоїдна гематологія"
    if disease_id in _MYELOID_HEME:
        return "Мієлоїдна гематологія"
    return "Солідні пухлини"


# Disease-id ↔ examples/patient_*.json filename-prefix mapping.
# Each value is a list of stem prefixes (after `examples/patient_`) that
# attribute a curated chunk case to this disease. Both treatment cases
# (e.g. `nsclc_alk_1l_*`) and pre-biopsy diagnostic cases
# (e.g. `diagnostic_lung_mass_*` for NSCLC, `diagnostic_breast_lump_*`
# for BREAST) count toward the same disease.
#
# Only diseases that actually have curated chunk cases (under the
# 60-file PR #150 set or future curated chunks) need entries — diseases
# without a key get #Curated = 0.
_DISEASE_PREFIXES: dict[str, list[str]] = {
    # Lymphoid heme
    "DIS-CLL": ["cll_"],
    "DIS-DLBCL-NOS": ["dlbcl_"],
    "DIS-MCL": ["mcl_"],
    # Myeloid heme
    "DIS-AML": ["aml_"],
    # Solid tumors
    "DIS-BREAST": ["breast_", "diagnostic_breast_"],
    "DIS-CRC": ["crc_"],
    "DIS-ENDOMETRIAL": ["endometrial_"],
    "DIS-ESOPHAGEAL": ["esophageal_"],
    "DIS-GASTRIC": ["gastric_"],
    "DIS-HCC": ["hcc_"],
    "DIS-HNSCC": ["hnscc_"],
    "DIS-MELANOMA": ["melanoma_"],
    "DIS-NSCLC": ["nsclc_", "diagnostic_lung_"],
    "DIS-OVARIAN": ["ovarian_"],
    "DIS-PDAC": ["pdac_"],
    "DIS-PROSTATE": ["prostate_", "diagnostic_prostate_"],
    "DIS-RCC": ["rcc_"],
    "DIS-SCLC": ["sclc_"],
    "DIS-UROTHELIAL": ["urothelial_"],
}


def _count_curated_cases(examples_root: Path) -> dict[str, int]:
    """Count `examples/patient_<prefix>*.json` curated chunk cases per
    disease id. Excludes `auto_*` and `variant_*` (different test
    contracts) — those don't live under `patient_` anyway, so the glob
    already excludes them, but we re-state the invariant for safety."""
    if not examples_root.is_dir():
        return {}
    counts: dict[str, int] = defaultdict(int)
    for f in examples_root.glob("patient_*.json"):
        # Defensive: skip if somehow auto/variant snuck under patient_
        name = f.name
        if "auto_" in name or "variant_" in name:
            continue
        stem = name[len("patient_"):-len(".json")]  # drop prefix + ext
        for did, prefixes in _DISEASE_PREFIXES.items():
            if any(stem.startswith(p) for p in prefixes):
                counts[did] += 1
                break
    return dict(counts)


# ── Walkers ───────────────────────────────────────────────────────────────


def _collect_biomarkers_and_drugs(entities_by_id: dict) -> dict[str, dict]:
    """{disease_id: {biomarkers: set, drugs: set, indications: list, ...}}."""
    out: dict[str, dict] = defaultdict(lambda: {
        "biomarkers": set(),
        "drugs": set(),
        "indications": [],
        "regimens": set(),
        "redflags": set(),
    })

    # Helper: walk a structure and collect BIO-* / DRUG-*
    def _walk_collect(node, bios: set, drugs: set):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "biomarker_id" and isinstance(v, str):
                    bios.add(v)
                elif k == "drug_id" and isinstance(v, str):
                    drugs.add(v)
                else:
                    _walk_collect(v, bios, drugs)
        elif isinstance(node, list):
            for item in node:
                _walk_collect(item, bios, drugs)
        elif isinstance(node, str):
            if node.startswith("BIO-"):
                bios.add(node)
            elif node.startswith("DRUG-"):
                drugs.add(node)

    # 1) Indications applicable to each disease
    for eid, info in entities_by_id.items():
        if info["type"] != "indications":
            continue
        d = info["data"]
        applicable = d.get("applicable_to") or {}
        if not isinstance(applicable, dict):
            continue
        disease_id = applicable.get("disease_id") or applicable.get("disease")
        if not disease_id:
            continue
        out[disease_id]["indications"].append(d)
        # Walk indication for biomarkers + drugs
        bios, drugs = set(), set()
        _walk_collect(d, bios, drugs)
        out[disease_id]["biomarkers"] |= bios
        out[disease_id]["drugs"] |= drugs
        # Track recommended_regimen
        reg = d.get("recommended_regimen")
        if reg:
            out[disease_id]["regimens"].add(reg)

    # 2) Resolve regimen → its components → drugs
    for eid, info in entities_by_id.items():
        if info["type"] != "regimens":
            continue
        reg_id = info["data"].get("id") or eid
        # Find which diseases reference this regimen
        referencing = [did for did, data in out.items() if reg_id in data["regimens"]]
        if not referencing:
            continue
        bios, drugs = set(), set()
        _walk_collect(info["data"], bios, drugs)
        for did in referencing:
            out[did]["biomarkers"] |= bios
            out[did]["drugs"] |= drugs

    # 3) RedFlags applicable per disease (relevant_diseases field, when present)
    for eid, info in entities_by_id.items():
        if info["type"] != "redflags":
            continue
        d = info["data"]
        rel = d.get("relevant_diseases") or []
        if not isinstance(rel, list):
            continue
        for did in rel:
            if did == "*":
                continue  # universal — skip for per-disease count
            if did in out or did.startswith("DIS-"):
                out[did]["redflags"].add(d.get("id") or eid)

    return out


def _has_entity(entities_by_id: dict, etype: str, predicate) -> bool:
    for _, info in entities_by_id.items():
        if info["type"] != etype:
            continue
        if predicate(info["data"]):
            return True
    return False


# ── Per-disease metric ────────────────────────────────────────────────────


def _outcomes_cited_pct_map() -> dict[str, float] | None:
    """Lazy import of the audit's helper. Returns ``None`` if the module
    cannot be imported (rare — keeps the matrix script usable on a
    stripped Python harness without PyYAML, even though that's not a
    supported configuration). Phase 2 — Pivotal Trial Outcomes
    Ingestion Plan."""
    try:
        from scripts.audit_expected_outcomes import (
            disease_outcomes_cited_pct,
        )
    except Exception:
        return None
    try:
        return disease_outcomes_cited_pct()
    except Exception:
        return None


def per_disease_metrics(load_root: Path) -> list[dict]:
    load = load_content(load_root)
    coll = _collect_biomarkers_and_drugs(load.entities_by_id)
    curated_counts = _count_curated_cases(REPO_ROOT / "examples")
    outcomes_pct = _outcomes_cited_pct_map() or {}

    rows: list[dict] = []
    for eid, info in sorted(load.entities_by_id.items()):
        if info["type"] != "diseases":
            continue
        d = info["data"]
        names = d.get("names") or {}
        name = names.get("english") or names.get("preferred") or eid

        agg = coll.get(eid, {})
        bios = agg.get("biomarkers", set())
        drugs = agg.get("drugs", set())
        inds = agg.get("indications", [])
        regs = agg.get("regimens", set())
        rfs = agg.get("redflags", set())

        # Algorithm presence (1L / 2L)
        algo_1l = _has_entity(
            load.entities_by_id, "algorithms",
            lambda dd: dd.get("applicable_to_disease") == eid and (dd.get("applicable_to_line_of_therapy") or 1) == 1,
        )
        algo_2l = _has_entity(
            load.entities_by_id, "algorithms",
            lambda dd: dd.get("applicable_to_disease") == eid and (dd.get("applicable_to_line_of_therapy") or 1) >= 2,
        )

        # Questionnaire — check stub flag
        quest = None
        for _, qinfo in load.entities_by_id.items():
            if qinfo["type"] == "questionnaires" and qinfo["data"].get("disease_id") == eid:
                quest = qinfo["data"]
                break
        has_quest = quest is not None
        is_stub_quest = bool(quest and quest.get("_stub_auto_generated"))

        has_workup = _has_entity(
            load.entities_by_id, "diagnostic_workups",
            lambda dd: eid in (dd.get("applicable_to_diseases") or []),
        )

        # Fill % composite (8 expected entity types)
        fill_components = [
            len(inds) >= 1,
            len(regs) >= 1,
            len(bios) >= 1,
            len(drugs) >= 1,
            len(rfs) >= 1,
            algo_1l,
            has_quest,
            has_workup,
        ]
        fill_pct = round(100 * sum(fill_components) / len(fill_components))

        # Verified % — weighted by indications with reviewer_signoffs >= 2
        if inds:
            verified = sum(
                1 for ind in inds
                if _signoff_count(ind.get("reviewer_signoffs")) >= 2
            )
            verified_pct = round(100 * verified / len(inds))
        else:
            verified_pct = 0

        # Outcomes-Cited % from Phase 2 audit. Diseases the audit didn't
        # rollup (e.g. zero indications, or a stripped harness where the
        # audit module failed to import) get None → render as "n/a".
        outcomes_cited_pct = outcomes_pct.get(eid)

        rows.append({
            "id": eid,
            "name": name,
            "family": _family(eid),
            "icd10": (d.get("codes") or {}).get("icd_10") or "",
            "n_bios": len(bios),
            "n_drugs": len(drugs),
            "n_inds": len(inds),
            "n_regs": len(regs),
            "n_rfs": len(rfs),
            "algo_1l": algo_1l,
            "algo_2l": algo_2l,
            "has_quest": has_quest,
            "is_stub_quest": is_stub_quest,
            "has_workup": has_workup,
            "fill_pct": fill_pct,
            "verified_pct": verified_pct,
            "n_curated": curated_counts.get(eid, 0),
            "outcomes_cited_pct": outcomes_cited_pct,
        })

    return rows


# ── Markdown rendering ────────────────────────────────────────────────────


def render_markdown_table(rows: list[dict]) -> str:
    families = {}
    for r in rows:
        families.setdefault(r["family"], []).append(r)

    out: list[str] = []
    out.append("# Per-disease coverage matrix (auto)")
    out.append("")
    out.append(f"**Total diseases:** {len(rows)}")
    out.append("")

    # Summary stats
    fill_avg = round(sum(r["fill_pct"] for r in rows) / max(1, len(rows)), 1)
    verified_avg = round(sum(r["verified_pct"] for r in rows) / max(1, len(rows)), 1)
    n_signed_at_least_one = sum(1 for r in rows if r["verified_pct"] > 0)
    n_with_quest_real = sum(1 for r in rows if r["has_quest"] and not r["is_stub_quest"])
    n_with_quest_stub = sum(1 for r in rows if r["has_quest"] and r["is_stub_quest"])
    n_with_algo_1l = sum(1 for r in rows if r["algo_1l"])
    n_with_algo_2l = sum(1 for r in rows if r["algo_2l"])
    total_curated = sum(r["n_curated"] for r in rows)
    n_with_curated = sum(1 for r in rows if r["n_curated"] > 0)

    out.append("## Summary")
    out.append("")
    out.append(f"- Avg fill: **{fill_avg}%** | Avg verified: **{verified_avg}%**")
    out.append(f"- Diseases with ≥1 verified indication: **{n_signed_at_least_one}/{len(rows)}**")
    out.append(f"- Hand-authored questionnaires: **{n_with_quest_real}** | STUB questionnaires: **{n_with_quest_stub}**")
    out.append(f"- Has 1L algorithm: **{n_with_algo_1l}/{len(rows)}** | Has 2L+ algorithm: **{n_with_algo_2l}/{len(rows)}**")
    out.append(f"- Curated chunk cases: **{total_curated}** total across **{n_with_curated}/{len(rows)}** diseases")
    out.append("")

    def _outcomes_cell(pct: float | None) -> str:
        if pct is None:
            return "n/a"
        return f"{pct:.1f}%"

    for family in ("Лімфоїдна гематологія", "Мієлоїдна гематологія", "Солідні пухлини"):
        flist = families.get(family, [])
        if not flist:
            continue
        out.append(f"## {family} ({len(flist)} хвороб)")
        out.append("")
        out.append("| Disease | ICD-10 | #Bio | #Drug | #Ind | #Reg | #RF | 1L | 2L | Quest | #Curated | Fill% | Ver% | Outcomes-Cited% |")
        out.append("|---------|--------|------|-------|------|------|-----|----|----|-------|---------:|-------|------|-----------------|")
        # Sort by fill desc then name
        for r in sorted(flist, key=lambda x: (-x["fill_pct"], x["name"])):
            algo_1l_mark = "✓" if r["algo_1l"] else "—"
            algo_2l_mark = "✓" if r["algo_2l"] else "—"
            if r["has_quest"]:
                quest_mark = "STUB" if r["is_stub_quest"] else "✓"
            else:
                quest_mark = "—"
            curated_cell = str(r["n_curated"]) if r["n_curated"] > 0 else "—"
            short_id = r["id"].replace("DIS-", "")
            short_name = r["name"][:36] + ("…" if len(r["name"]) > 36 else "")
            out.append(
                f"| **{short_id}** {short_name} | {r['icd10']} | "
                f"{r['n_bios']} | {r['n_drugs']} | {r['n_inds']} | {r['n_regs']} | {r['n_rfs']} | "
                f"{algo_1l_mark} | {algo_2l_mark} | {quest_mark} | {curated_cell} | "
                f"**{r['fill_pct']}%** | {r['verified_pct']}% | "
                f"{_outcomes_cell(r['outcomes_cited_pct'])} |"
            )
        # Family avg + total curated. Outcomes-Cited avg ignores diseases
        # the audit didn't rollup (None entries) so the average reflects
        # only diseases with measurable expected_outcomes coverage.
        f_fill = round(sum(r["fill_pct"] for r in flist) / max(1, len(flist)), 1)
        f_ver = round(sum(r["verified_pct"] for r in flist) / max(1, len(flist)), 1)
        f_curated = sum(r["n_curated"] for r in flist)
        f_outcomes_vals = [r["outcomes_cited_pct"] for r in flist if r["outcomes_cited_pct"] is not None]
        if f_outcomes_vals:
            f_outcomes = f"{sum(f_outcomes_vals) / len(f_outcomes_vals):.1f}%"
        else:
            f_outcomes = "n/a"
        out.append(
            f"| _Avg_ |  |  |  |  |  |  |  |  |  | _{f_curated}_ | _{f_fill}%_ | _{f_ver}%_ | _{f_outcomes}_ |"
        )
        out.append("")

    out.append("## Метрики")
    out.append("")
    out.append("- **#Bio** — distinct biomarkers, на які посилаються Indications + Regimens цієї хвороби")
    out.append("- **#Drug** — distinct drugs у regimens цієї хвороби")
    out.append("- **#Ind / #Reg / #RF** — Indications / Regimens / RedFlags для цієї хвороби")
    out.append("- **1L / 2L** — наявність Algorithm для першої / другої+ лінії")
    out.append("- **Quest** — `✓` hand-authored questionnaire / `STUB` auto-generated / `—` відсутній")
    out.append("- **#Curated** — кількість curated chunk patient-кейсів `examples/patient_<prefix>_*.json` (включно з pre-biopsy `diagnostic_*` файлами для відповідної хвороби); auto/variant виключені — у них інший test contract")
    out.append("- **Fill%** = composite з 8 ентити-типів: ≥1 indication, ≥1 regimen, ≥1 biomarker, ≥1 drug, ≥1 redflag, 1L algo, questionnaire, workup")
    out.append("- **Ver%** = % indications цієї хвороби з `reviewer_signoffs ≥ 2` (CHARTER §6.1)")
    out.append(
        "- **Outcomes-Cited%** = loose %-cited over populated `expected_outcomes` "
        "fields per `scripts/audit_expected_outcomes.disease_outcomes_cited_pct` "
        "(Phase 2, Pivotal Trial Outcomes Ingestion Plan). "
        "v1.0 target ≥90%."
    )
    out.append("")
    out.append("> **Verified взагалі = 0** для всіх — діє dev-mode signoff exemption (`project_charter_dev_mode_exemptions`)")
    out.append("> до призначення Clinical Co-Leads. Це навмисно, не bug.")

    return "\n".join(out)


def _force_utf8_stdout() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:  # pylint: disable=broad-except
                pass


def main() -> int:
    _force_utf8_stdout()
    rows = per_disease_metrics(REPO_ROOT / "knowledge_base" / "hosted" / "content")
    print(render_markdown_table(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
