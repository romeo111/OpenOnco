"""Generate one minimal auto-stub example per disease with fill >= 50%.

For each qualifying disease:
  - examples/auto_<disease_short>.json — minimal valid patient profile
    (disease.id + line_of_therapy + age + ECOG + 1 representative biomarker
    if biomarker_driven)
  - Label encodes the fill% so the user sees readiness right in the
    /try.html "Завантажити приклад" dropdown
    ("DIS-NSCLC — Auto-stub (88% fill)")

Idempotent: skips files that already exist; generator file (CaseEntry list
patch) is rewritten in place each run.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
SITE_CASES = REPO_ROOT / "scripts" / "site_cases.py"
COVERAGE_THRESHOLD_PCT = 0

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.disease_coverage_matrix import per_disease_metrics  # noqa: E402
from knowledge_base.validation.loader import load_content  # noqa: E402


# ── Family → category mapping (matches scripts/site_cases.py CASE_CATEGORIES) ──


def _category_for(disease_id: str, family: str) -> str:
    if family == "Солідні пухлини":
        return "solid"
    if family == "Мієлоїдна гематологія":
        return "myeloid"
    # Lymphoid heme — split further
    lymphoblastic = {"DIS-B-ALL", "DIS-T-ALL"}
    hodgkin = {"DIS-CHL", "DIS-NLPBL"}
    myeloma = {"DIS-MM"}
    t_cell = {
        "DIS-PTCL-NOS", "DIS-ALCL", "DIS-AITL", "DIS-MF-SEZARY",
        "DIS-EATL", "DIS-HSTCL", "DIS-NK-T-NASAL", "DIS-ATLL", "DIS-T-PLL",
    }
    indolent = {
        "DIS-FL", "DIS-CLL", "DIS-SPLENIC-MZL", "DIS-NODAL-MZL",
        "DIS-HCV-MZL", "DIS-HCL", "DIS-WM",
    }
    if disease_id in lymphoblastic:
        return "lymphoblastic"
    if disease_id in hodgkin:
        return "hodgkin"
    if disease_id in myeloma:
        return "myeloma"
    if disease_id in t_cell:
        return "t_cell"
    if disease_id in indolent:
        return "b_indolent"
    return "b_aggressive"


# ── Pick one representative biomarker per disease ─────────────────────────


def _representative_biomarker(disease_id: str, entities_by_id: dict) -> tuple[str | None, str | None]:
    """Walk indications applicable to this disease; return the first
    biomarker_id seen with `value_constraint: positive`. Falls back to
    any BIO-* string. Returns (bio_id, value) where value defaults to "positive"."""
    for eid, info in entities_by_id.items():
        if info["type"] != "indications":
            continue
        d = info["data"]
        applicable = d.get("applicable_to") or {}
        if not isinstance(applicable, dict):
            continue
        did = applicable.get("disease_id") or applicable.get("disease")
        if did != disease_id:
            continue
        # Look for biomarker_requirements_required
        reqs = applicable.get("biomarker_requirements_required")
        if isinstance(reqs, list):
            for r in reqs:
                if isinstance(r, dict) and r.get("biomarker_id"):
                    val = r.get("value_constraint") or "positive"
                    return r["biomarker_id"], val
    return None, None


# ── Minimal patient profile builder ───────────────────────────────────────


def _build_minimal_profile(disease_id: str, entities_by_id: dict, fill_pct: int) -> dict:
    bio_id, bio_value = _representative_biomarker(disease_id, entities_by_id)
    short = disease_id.replace("DIS-", "")
    profile: dict = {
        "patient_id": f"AUTO-{short}-001",
        "_auto_stub": True,
        "_fill_pct": fill_pct,
        "disease": {"id": disease_id},
        "line_of_therapy": 1,
        "demographics": {
            "age": 60,
            "sex": "male",
            "ecog": 1,
        },
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
        profile["biomarkers"][bio_id] = bio_value
    return profile


# ── site_cases.py CaseEntry block writer ──────────────────────────────────


_AUTO_BLOCK_BEGIN = "    # ── AUTO-GENERATED disease-coverage stubs (do not hand-edit; regen via scripts/generate_auto_examples.py) ──"
_AUTO_BLOCK_END = "    # ── /AUTO-GENERATED ──"


def _render_case_entry(disease_id: str, fill_pct: int, family: str, name: str) -> str:
    short = disease_id.replace("DIS-", "")
    short_lower = short.lower().replace("-", "_")
    case_id = f"auto-{short_lower}"
    file = f"auto_{short_lower}.json"
    cat = _category_for(disease_id, family)
    label_ua = f"{disease_id} — Auto-stub ({fill_pct}% наповненість)"
    label_en = f"{disease_id} — Auto-stub ({fill_pct}% KB fill)"
    summary_ua = (
        f"Автогенерований мінімальний профіль для {name[:80]}. "
        f"Фактична наповненість бази для цієї хвороби — {fill_pct}%. "
        "Використовується для перевірки end-to-end engine + render — "
        "не для клінічних рішень."
    )
    summary_en = (
        f"Auto-generated minimal profile for {name[:80]}. "
        f"Actual KB fill for this disease is {fill_pct}%. "
        "Used to verify end-to-end engine + render — "
        "not for clinical decisions."
    )
    bs = chr(92) + chr(34)  # \"
    return f"""    CaseEntry(
        case_id="{case_id}",
        file="{file}",
        label_ua="{label_ua}",
        summary_ua="{summary_ua.replace('"', bs)}",
        badge="Auto-stub", badge_class="bdg-stub", category="{cat}",
        label_en="{label_en}",
        summary_en="{summary_en.replace('"', bs)}",
    ),"""


def _patch_site_cases(entries: list[str]) -> None:
    """Replace the auto-generated block in scripts/site_cases.py.

    If the markers don't exist yet, append the block right before the
    closing `]` of the CASES list (assumed to be the last `]` in the file)."""
    text = SITE_CASES.read_text(encoding="utf-8")
    auto_block = _AUTO_BLOCK_BEGIN + "\n" + "\n".join(entries) + "\n" + _AUTO_BLOCK_END

    if _AUTO_BLOCK_BEGIN in text and _AUTO_BLOCK_END in text:
        start = text.index(_AUTO_BLOCK_BEGIN)
        end = text.index(_AUTO_BLOCK_END) + len(_AUTO_BLOCK_END)
        new = text[:start] + auto_block + text[end:]
    else:
        # First-time install: insert before final `]\n` of the CASES list
        marker = "\n]\n"
        last_close = text.rfind(marker)
        if last_close < 0:
            print("ERROR: could not find CASES list closing bracket", file=sys.stderr)
            return
        new = text[:last_close] + "\n" + auto_block + "\n" + text[last_close:]

    SITE_CASES.write_text(new, encoding="utf-8")


# ── Main ──────────────────────────────────────────────────────────────────


def main() -> int:
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    rows = per_disease_metrics(REPO_ROOT / "knowledge_base" / "hosted" / "content")
    qualifying = [r for r in rows if r["fill_pct"] >= COVERAGE_THRESHOLD_PCT]
    print(f"Qualifying diseases (fill >= {COVERAGE_THRESHOLD_PCT}%): {len(qualifying)}/{len(rows)}")

    load = load_content(REPO_ROOT / "knowledge_base" / "hosted" / "content")

    written = 0
    skipped = 0
    case_entries: list[str] = []

    for r in sorted(qualifying, key=lambda x: x["id"]):
        short = r["id"].replace("DIS-", "")
        short_lower = short.lower().replace("-", "_")
        path = EXAMPLES_DIR / f"auto_{short_lower}.json"
        case_entries.append(_render_case_entry(r["id"], r["fill_pct"], r["family"], r["name"]))

        if path.exists():
            skipped += 1
            continue

        profile = _build_minimal_profile(r["id"], load.entities_by_id, r["fill_pct"])
        path.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
        written += 1
        print(f"  + {path.name:40s} ({r['fill_pct']}% fill)")

    print(f"\nWrote {written} new auto-stub examples; {skipped} already existed.")

    _patch_site_cases(case_entries)
    print(f"Patched scripts/site_cases.py with {len(case_entries)} CaseEntry rows.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
