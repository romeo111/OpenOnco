"""Generate 6 hypothetical-variant patient profiles per qualifying disease.

Layered on top of `scripts/generate_auto_examples.py`. The auto-stub
serves as variant V0 (baseline typical patient). This script emits six
additional variants per disease — each varying the auto-stub along ONE
clinical axis (frailty, organ dysfunction, infection screening, line of
therapy, biomarker actionability, high-risk biology) — and verifies
that each produces a non-empty Plan/DiagnosticBrief from the engine.

Variants that fail engine verification are dropped silently from the
gallery (logged on stdout for debugging). The CASES patch + JSON write
happen atomically per (disease × variant) pair after verification.

Idempotent: rewrites JSON files in place each run; the AUTO-GENERATED
block in `scripts/site_cases.py` is replaced wholesale.

Per CHARTER §9.3 — all profiles are synthetic; the `_auto_variant`
flag identifies them as such for downstream tooling.

Usage:
    C:/Python312/python.exe -m scripts.generate_variant_examples
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
SITE_CASES = REPO_ROOT / "scripts" / "site_cases.py"
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
COVERAGE_THRESHOLD_PCT = 50

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.disease_coverage_matrix import per_disease_metrics  # noqa: E402
from scripts.generate_auto_examples import (  # noqa: E402
    _category_for,
    _representative_biomarker,
)
from scripts.example_redflag_quality import (  # noqa: E402
    enrich_profile_for_gallery_quality,
)
from knowledge_base.engine import (  # noqa: E402
    generate_diagnostic_brief,
    generate_plan,
    is_diagnostic_profile,
)
from knowledge_base.validation.loader import load_content  # noqa: E402


# ── Variant builders ──────────────────────────────────────────────────────


def _baseline(disease_id: str, bio_id: str | None, bio_value: str | None) -> dict:
    short = disease_id.replace("DIS-", "")
    profile: dict = {
        "patient_id": f"VAR-{short}-V0",
        "_auto_variant": True,
        "disease": {"id": disease_id},
        "line_of_therapy": 1,
        "demographics": {"age": 60, "sex": "male", "ecog": 1},
        "biomarkers": {},
        "findings": {
            "creatinine_clearance_ml_min": 90,
            "bilirubin_uln_x": 1.0,
            "absolute_neutrophil_count_k_ul": 2.5,
            "platelets_k_ul": 200,
            "hbsag": "negative",
            "anti_hbc_total": "negative",
            "hcv_status": "negative",
            "hiv_status": "negative",
        },
    }
    if bio_id:
        profile["biomarkers"][bio_id] = bio_value or "positive"
    return profile


def _build_frail(disease_id, bio_id, bio_value):
    p = _baseline(disease_id, bio_id, bio_value)
    p["patient_id"] = p["patient_id"].replace("V0", "FRAIL")
    p["demographics"]["age"] = 78
    p["demographics"]["ecog"] = 3
    p["findings"]["creatinine_clearance_ml_min"] = 50
    p["findings"]["albumin_g_dL"] = 3.0
    p["findings"]["frailty_clinical_assessment"] = "frail"
    return p


def _build_organ_dysf(disease_id, bio_id, bio_value):
    p = _baseline(disease_id, bio_id, bio_value)
    p["patient_id"] = p["patient_id"].replace("V0", "ORGAN")
    p["findings"]["creatinine_clearance_ml_min"] = 25
    p["findings"]["bilirubin_uln_x"] = 3.5
    p["findings"]["alt_uln_x"] = 5.0
    p["findings"]["AST_uln_x"] = 5.0
    p["findings"]["lvef_percent"] = 40
    p["findings"]["platelets_k_ul"] = 70
    return p


def _build_infection_hbv(disease_id, bio_id, bio_value):
    p = _baseline(disease_id, bio_id, bio_value)
    p["patient_id"] = p["patient_id"].replace("V0", "HBV")
    p["findings"]["hbsag"] = "positive"
    p["findings"]["anti_hbc_total"] = "positive"
    p["findings"]["hbv_dna_iu_ml"] = 5000
    return p


def _build_relapsed(disease_id, bio_id, bio_value):
    p = _baseline(disease_id, bio_id, bio_value)
    p["patient_id"] = p["patient_id"].replace("V0", "RELAPSED")
    p["line_of_therapy"] = 2
    p["findings"]["progression_after_first_line"] = True
    p["findings"]["transformation_suspect"] = True
    return p


def _build_biomarker_act(disease_id, bio_id, bio_value):
    p = _baseline(disease_id, bio_id, bio_value)
    p["patient_id"] = p["patient_id"].replace("V0", "BIOMARK")
    if bio_id:
        p["biomarkers"][bio_id] = bio_value or "positive"
    p["findings"]["biomarker_actionable_present"] = True
    return p


def _build_high_risk(disease_id, bio_id, bio_value):
    p = _baseline(disease_id, bio_id, bio_value)
    p["patient_id"] = p["patient_id"].replace("V0", "HIGHRISK")
    p["findings"]["high_risk_biology"] = True
    p["findings"]["bulky_disease"] = True
    p["findings"]["dominant_nodal_mass_cm"] = 10.0
    p["findings"]["ldh_ratio_to_uln"] = 2.5
    p["findings"]["b_symptoms_present"] = True
    return p


VARIANTS: list[tuple[str, callable, str, str]] = [
    ("frail", _build_frail,
     "Літній / крихкий пацієнт (age 78, ECOG 3)",
     "Elderly / frail patient (age 78, ECOG 3)"),
    ("organ_dysf", _build_organ_dysf,
     "Дисфункція органів (CrCl 25, bili 3.5×ULN)",
     "Organ dysfunction (CrCl 25, bili 3.5×ULN)"),
    ("infection_hbv", _build_infection_hbv,
     "HBV-позитивний (HBsAg+, anti-HBc+)",
     "HBV-positive (HBsAg+, anti-HBc+)"),
    ("relapsed_2l", _build_relapsed,
     "Релапс / 2-а лінія",
     "Relapsed / 2nd line"),
    ("biomarker_act", _build_biomarker_act,
     "Actionable біомаркер present",
     "Actionable biomarker present"),
    ("high_risk", _build_high_risk,
     "High-risk biology / bulky disease",
     "High-risk biology / bulky disease"),
]


# ── Engine verification ───────────────────────────────────────────────────


def _verify(profile: dict) -> tuple[bool, str]:
    """Return (ok, message). ok=True iff engine produces non-empty
    Plan or DiagnosticBrief. message is a short status string."""
    try:
        if is_diagnostic_profile(profile):
            brief = generate_diagnostic_brief(profile, kb_root=KB_ROOT)
            if brief is None:
                return False, "no diagnostic brief"
            return True, "diagnostic-brief"
        result = generate_plan(profile, kb_root=KB_ROOT)
        if result.plan is None:
            return False, "plan=None"
        if not result.plan.tracks:
            return False, "0 tracks"
        return True, f"{len(result.plan.tracks)} tracks"
    except Exception as exc:
        return False, f"exc {type(exc).__name__}: {str(exc)[:80]}"


# ── site_cases.py patching ────────────────────────────────────────────────


_VARIANT_BLOCK_BEGIN = (
    "    # ── AUTO-GENERATED variant cases "
    "(do not hand-edit; regen via scripts/generate_variant_examples.py) ──"
)
_VARIANT_BLOCK_END = "    # ── /AUTO-GENERATED-VARIANTS ──"


def _patch_site_cases(entries: list[str]) -> None:
    text = SITE_CASES.read_text(encoding="utf-8")
    block = _VARIANT_BLOCK_BEGIN + "\n" + "\n".join(entries) + "\n" + _VARIANT_BLOCK_END

    if _VARIANT_BLOCK_BEGIN in text and _VARIANT_BLOCK_END in text:
        s = text.index(_VARIANT_BLOCK_BEGIN)
        e = text.index(_VARIANT_BLOCK_END) + len(_VARIANT_BLOCK_END)
        new = text[:s] + block + text[e:]
    else:
        # First-time install: insert before the closing `]` of CASES
        marker = "\n]\n"
        last = text.rfind(marker)
        if last < 0:
            print("ERROR: CASES closing bracket not found in site_cases.py", file=sys.stderr)
            return
        new = text[:last] + "\n" + block + "\n" + text[last:]
    SITE_CASES.write_text(new, encoding="utf-8")


def _render_case_entry(
    disease_id: str, var_name: str, var_desc_ua: str, var_desc_en: str,
    file: str, category: str, msg: str,
) -> str:
    short_lower = disease_id.replace("DIS-", "").lower().replace("-", "_")
    case_id = f"variant-{short_lower}-{var_name.replace('_', '-')}"
    label_ua = f"{disease_id} · {var_desc_ua}"
    label_en = f"{disease_id} · {var_desc_en}"
    summary_ua = (
        f"Автогенерований variant '{var_name}'. Engine: {msg}. "
        "Синтетичний профіль — не для клінічних рішень."
    ).replace('"', '\\"')
    summary_en = (
        f"Auto-generated variant '{var_name}'. Engine: {msg}. "
        "Synthetic profile — not for clinical decisions."
    ).replace('"', '\\"')
    return (
        f'    CaseEntry(\n'
        f'        case_id="{case_id}",\n'
        f'        file="{file}",\n'
        f'        label_ua="{label_ua}",\n'
        f'        summary_ua="{summary_ua}",\n'
        f'        badge="Variant", badge_class="bdg-stub", category="{category}",\n'
        f'        label_en="{label_en}",\n'
        f'        summary_en="{summary_en}",\n'
        f'    ),'
    )


# ── Main ──────────────────────────────────────────────────────────────────


def main() -> int:
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    rows = per_disease_metrics(KB_ROOT)
    qualifying = [r for r in rows if r["fill_pct"] >= COVERAGE_THRESHOLD_PCT]
    print(f"Qualifying diseases (fill >= {COVERAGE_THRESHOLD_PCT}%): {len(qualifying)}/{len(rows)}")

    load = load_content(KB_ROOT)

    written = 0
    failed: list[tuple[str, str, str]] = []
    case_entries: list[str] = []

    for r in sorted(qualifying, key=lambda x: x["id"]):
        disease_id = r["id"]
        short_lower = disease_id.replace("DIS-", "").lower().replace("-", "_")
        bio_id, bio_value = _representative_biomarker(disease_id, load.entities_by_id)
        category = _category_for(disease_id, r["family"])

        for var_name, builder, var_desc_ua, var_desc_en in VARIANTS:
            profile = builder(disease_id, bio_id, bio_value)
            profile, _added = enrich_profile_for_gallery_quality(
                profile,
                kb_root=KB_ROOT,
            )
            ok, msg = _verify(profile)
            if not ok:
                failed.append((disease_id, var_name, msg))
                continue

            file = f"variant_{short_lower}_{var_name}.json"
            path = EXAMPLES_DIR / file
            path.write_text(
                json.dumps(profile, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            case_entries.append(
                _render_case_entry(disease_id, var_name, var_desc_ua, var_desc_en, file, category, msg)
            )
            written += 1

    print(f"\nWrote {written} variant profiles. Failed: {len(failed)}.")
    if failed:
        print("Failures (first 30):")
        for d, v, m in failed[:30]:
            print(f"  FAIL {d:28s} {v:18s} {m}")
        if len(failed) > 30:
            print(f"  ... +{len(failed) - 30} more")

    _patch_site_cases(case_entries)
    print(f"\nPatched scripts/site_cases.py with {len(case_entries)} variant CaseEntry rows.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
