"""OncoKB integration coverage report.

For each Disease in the KB, reports:
  - Whether Disease.oncotree_code is explicit (tier-1)
  - Whether tier-2 ICD-10 fallback resolves (if no explicit code)
  - Whether the disease would land in pan-tumor mode (tier-3 — warning badge)
  - Count of biomarkers with `oncokb_lookup` hint that are referenced
    by indications under this disease

Run:
    python scripts/oncokb_coverage_report.py            # text report (stdout)
    python scripts/oncokb_coverage_report.py --json     # JSON output
    python scripts/oncokb_coverage_report.py --warn     # exit non-zero on pan-tumor coverage

Wired into CI as a non-blocking warning step (--warn).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from knowledge_base.engine.oncotree_fallback import resolve_oncotree_code  # noqa: E402
from knowledge_base.validation.loader import load_content  # noqa: E402


@dataclass
class DiseaseCoverage:
    disease_id: str
    name_en: Optional[str]
    icd_10: Optional[str]
    oncotree_explicit: Optional[str]      # tier-1
    oncotree_fallback_resolved: Optional[str]  # tier-2 result if tier-1 absent
    final_oncotree_code: Optional[str]    # what would actually be used
    pan_tumor_warning: bool               # render shows badge?
    referenced_biomarker_ids: list[str] = field(default_factory=list)
    referenced_biomarkers_with_hint: list[str] = field(default_factory=list)
    indications_count: int = 0

    @property
    def hint_coverage_pct(self) -> Optional[float]:
        n = len(self.referenced_biomarker_ids)
        if n == 0:
            return None
        return round(100.0 * len(self.referenced_biomarkers_with_hint) / n, 1)


def _collect_biomarker_hints(entities_by_id: dict) -> dict[str, dict]:
    """Return {biomarker_id: hint_dict} for all biomarkers with a hint."""
    out: dict[str, dict] = {}
    for eid, info in entities_by_id.items():
        if info["type"] != "biomarkers":
            continue
        hint = info["data"].get("oncokb_lookup")
        if isinstance(hint, dict) and hint.get("gene") and hint.get("variant"):
            out[eid] = hint
    return out


def _collect_disease_to_indications(entities_by_id: dict) -> dict[str, list[dict]]:
    """{disease_id: [indication_dict, ...]} for indications applicable to each disease.

    KB indications use either `applicable_to.disease_id` or `applicable_to.disease`
    (older shape) — accept both."""
    out: dict[str, list[dict]] = defaultdict(list)
    for eid, info in entities_by_id.items():
        if info["type"] != "indications":
            continue
        d = info["data"]
        applicable = d.get("applicable_to") or {}
        if isinstance(applicable, dict):
            for key in ("disease_id", "disease"):
                disease_id = applicable.get(key)
                if disease_id:
                    out[disease_id].append(d)
                    break
        # Some indications use `disease_id` top-level
        if "disease_id" in d:
            out[d["disease_id"]].append(d)
    return out


def _biomarkers_referenced_by_indication(indication: dict) -> list[str]:
    """Extract biomarker IDs from any nested structure in an indication.

    KB shapes observed (be permissive):
      applicable_to:
        biomarker_requirements_required:
          - biomarker_id: BIO-BRAF-V600E
            value_constraint: positive
        biomarker_requirements_excluded: [...]
      applicable_to.biomarkers: [BIO-X, {id: BIO-Y}]
      requires: {biomarkers: [BIO-Z]} / loose BIO-* strings anywhere

    Approach: walk the whole indication tree and collect any string
    starting with "BIO-" or any dict with `biomarker_id`."""
    out: set[str] = set()

    def _walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "biomarker_id" and isinstance(v, str):
                    out.add(v)
                else:
                    _walk(v)
        elif isinstance(node, list):
            for item in node:
                _walk(item)
        elif isinstance(node, str):
            if node.startswith("BIO-"):
                out.add(node)

    _walk(indication)
    return sorted(out)


def build_report(kb_root: Path) -> list[DiseaseCoverage]:
    load = load_content(kb_root)
    biomarker_hints = _collect_biomarker_hints(load.entities_by_id)
    disease_to_inds = _collect_disease_to_indications(load.entities_by_id)

    reports: list[DiseaseCoverage] = []
    for eid, info in sorted(load.entities_by_id.items()):
        if info["type"] != "diseases":
            continue
        data = info["data"]

        explicit = data.get("oncotree_code")
        final_code, used_fallback = resolve_oncotree_code(data)
        tier2_result = None
        if not explicit:
            tier2_result = final_code  # whatever tier-2 produced (may be None)

        # Biomarkers referenced by this disease's indications
        ind_list = disease_to_inds.get(eid, [])
        ref_bms: set[str] = set()
        for ind in ind_list:
            for bm_id in _biomarkers_referenced_by_indication(ind):
                ref_bms.add(bm_id)

        with_hint = sorted(b for b in ref_bms if b in biomarker_hints)

        reports.append(
            DiseaseCoverage(
                disease_id=eid,
                name_en=(data.get("names") or {}).get("english") or (data.get("names") or {}).get("preferred"),
                icd_10=(data.get("codes") or {}).get("icd_10"),
                oncotree_explicit=explicit if isinstance(explicit, str) and explicit.strip() else None,
                oncotree_fallback_resolved=tier2_result,
                final_oncotree_code=final_code,
                pan_tumor_warning=used_fallback,
                referenced_biomarker_ids=sorted(ref_bms),
                referenced_biomarkers_with_hint=with_hint,
                indications_count=len(ind_list),
            )
        )
    return reports


def _print_text_report(reports: list[DiseaseCoverage]) -> None:
    print("=" * 80)
    print("OncoKB Integration · Coverage Report")
    print("=" * 80)

    total = len(reports)
    explicit = sum(1 for r in reports if r.oncotree_explicit)
    fallback_only = sum(
        1 for r in reports
        if not r.oncotree_explicit and r.oncotree_fallback_resolved
    )
    pan_tumor = sum(1 for r in reports if r.pan_tumor_warning and r.final_oncotree_code is None)

    print(f"\nTotal diseases:        {total}")
    print(f"  tier-1 explicit:     {explicit:3d}  ({100*explicit/max(1,total):.1f}%)")
    print(f"  tier-2 fallback:     {fallback_only:3d}  ({100*fallback_only/max(1,total):.1f}%)")
    print(f"  tier-3 pan-tumor:    {pan_tumor:3d}  ({100*pan_tumor/max(1,total):.1f}%)  <- render shows warning")

    biomarkers_referenced = sum(len(r.referenced_biomarker_ids) for r in reports)
    biomarkers_with_hint = sum(len(r.referenced_biomarkers_with_hint) for r in reports)
    print(
        f"\nBiomarker references:  {biomarkers_referenced} total / "
        f"{biomarkers_with_hint} with oncokb_lookup hint "
        f"({100*biomarkers_with_hint/max(1,biomarkers_referenced):.1f}%)"
    )

    # Pan-tumor warnings
    pan_tumor_diseases = [r for r in reports if r.final_oncotree_code is None]
    if pan_tumor_diseases:
        print("\n[WARN] Diseases that would render with pan-tumor warning badge:")
        for r in pan_tumor_diseases:
            print(f"  - {r.disease_id} ({r.name_en or '?'}, ICD-10: {r.icd_10 or '?'})")

    # Diseases with low hint coverage
    print("\nLow-coverage diseases (< 50% of referenced biomarkers have hints, indications > 0):")
    low = [r for r in reports if r.indications_count > 0 and (r.hint_coverage_pct or 0) < 50]
    if not low:
        print("  (none)")
    for r in sorted(low, key=lambda x: x.hint_coverage_pct or 0):
        n = len(r.referenced_biomarker_ids)
        m = len(r.referenced_biomarkers_with_hint)
        if n > 0:
            print(f"  - {r.disease_id:25s} {m}/{n} ({r.hint_coverage_pct}%)")


def _print_json_report(reports: list[DiseaseCoverage]) -> None:
    print(json.dumps(
        {"diseases": [asdict(r) for r in reports]},
        indent=2,
        ensure_ascii=False,
        default=str,
    ))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--kb-root",
        type=Path,
        default=Path("knowledge_base/hosted/content"),
    )
    parser.add_argument("--json", action="store_true", help="JSON output instead of text")
    parser.add_argument(
        "--warn",
        action="store_true",
        help="Exit non-zero if any disease falls to pan-tumor (tier-3)",
    )
    args = parser.parse_args()

    if not args.kb_root.exists():
        print(f"ERROR: {args.kb_root} not found", file=sys.stderr)
        return 1

    reports = build_report(args.kb_root)

    if args.json:
        _print_json_report(reports)
    else:
        _print_text_report(reports)

    if args.warn:
        n_pan_tumor = sum(1 for r in reports if r.final_oncotree_code is None)
        if n_pan_tumor:
            print(
                f"\n[FAIL --warn] {n_pan_tumor} disease(s) without OncoTree code.",
                file=sys.stderr,
            )
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
