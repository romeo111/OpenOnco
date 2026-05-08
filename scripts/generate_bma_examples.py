"""Generate one patient profile per uncovered BMA entry (ESCAT IA/IB/IIA/IIB).

For each (disease_id, biomarker_id) pair not already represented in curated
examples, emits a synthetic patient JSON and registers a CaseEntry in
scripts/site_cases.py.

Target: ESCAT IA, IB, IIA, IIB (all clinically actionable tiers).
IIIA/IIIB (pre-clinical/limited evidence), IV (investigational), X
(not actionable) are skipped — auto-stubs already cover disease-level
representation.

Idempotent: skips (disease, biomarker) pairs already covered.

Usage:
    python -m scripts.generate_bma_examples
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
SITE_CASES = REPO_ROOT / "scripts" / "site_cases.py"
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
BMA_DIR = KB_ROOT / "biomarker_actionability"

ESCAT_INCLUDE = {"IA", "IB", "IIA", "IIB"}

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.generate_auto_examples import _category_for  # noqa: E402
from scripts.disease_coverage_matrix import per_disease_metrics  # noqa: E402
from knowledge_base.engine import (  # noqa: E402
    generate_diagnostic_brief,
    generate_plan,
    is_diagnostic_profile,
)
from knowledge_base.validation.loader import load_content  # noqa: E402


# ── Biomarker value overrides ─────────────────────────────────────────────
# Keys: BIO-* IDs (or prefix fragments). Matched longest-prefix-first.
# If not found → default "positive".

BIO_VALUE_OVERRIDES: dict[str, str] = {
    "BIO-MSI-STATUS": "MSI-H",
    "BIO-DMMR-IHC": "deficient",
    "BIO-HRD-STATUS": "HRD-positive",
    "BIO-BRCA1-BRCA2-GERMLINE": "pathogenic",
    "BIO-BRCA-GERMLINE": "pathogenic",
    "BIO-BRCA1-GERMLINE": "pathogenic",
    "BIO-BRCA2-GERMLINE": "pathogenic",
    "BIO-HRR-PANEL": "pathogenic",
    "BIO-HER2-LOW": "HER2-low",
    "BIO-JAK2": "JAK2 V617F positive",
    "BIO-KRAS-G12C": "G12C-positive",
    "BIO-CALR": "CALR-mutated",
    "BIO-MPL": "MPL-mutated",
    "BIO-CLL-HIGH-RISK-GENETICS": "high_risk",
    "BIO-MM-CYTOGENETICS-HR": "high_risk",
    "BIO-SEZARY-COUNT": "B2",
    "BIO-HCV-RNA": "detectable",
    "BIO-HCV-STATUS": "detectable",
    "BIO-IDH1-R132": "IDH1 R132 positive",
    "BIO-IDH2-R140": "IDH2 R140 positive",
    "BIO-IDH2-R172": "IDH2 R172 positive",
    "BIO-FLT3-TKD": "D835 mutation positive",
    "BIO-TP53-MUTATION": "pathogenic",
    "BIO-SF3B1-MUTATION": "SF3B1 mutation positive",
    "BIO-NPM1-MUTATION": "positive (type A)",
    "BIO-BCR-ABL1": "positive_p210_e14a2",
    "BIO-VHL-STATUS": "germline_pathogenic",
    "BIO-AKT1": "E17K mutation",
    "BIO-PIK3CA-MUTATION": "positive",
    "BIO-PTEN": "loss-of-function",
}


def _bio_value(bio_id: str) -> str:
    """Return actionable value for this biomarker ID."""
    if bio_id in BIO_VALUE_OVERRIDES:
        return BIO_VALUE_OVERRIDES[bio_id]
    # Prefix scan
    for prefix, val in BIO_VALUE_OVERRIDES.items():
        if bio_id.startswith(prefix):
            return val
    return "positive"


# ── Line of therapy inference ─────────────────────────────────────────────

_RESISTANCE_KEYWORDS = re.compile(
    r"resistance|acquired|refractory|relaps|post.line|post.tki|post.io|"
    r"g1202r|t790m|c797s|l718|g12d.2l|2nd.line|second.line|salvage",
    re.I,
)


def _line_of_therapy(bma: dict) -> int:
    vq = bma.get("variant_qualifier") or ""
    return 2 if _RESISTANCE_KEYWORDS.search(vq) else 1


# ── Patient profile builder ───────────────────────────────────────────────


def _build_profile(bma: dict) -> dict:
    dis = bma["disease_id"]
    bio_id = bma.get("biomarker_id") or ""
    bio_val = _bio_value(bio_id)
    bma_id_lower = bma["id"].lower().replace("-", "_")
    line = _line_of_therapy(bma)

    profile: dict = {
        "patient_id": f"BMA-{bma_id_lower.replace('bma_', '').upper()[:28]}",
        "_auto_bma": True,
        "_bma_id": bma["id"],
        "_bma_escat": bma.get("escat_tier", "?"),
        "_bma_variant": bma.get("variant_qualifier", ""),
        "disease": {"id": dis},
        "line_of_therapy": line,
        "demographics": {"age": 58, "sex": "female", "ecog": 1},
        "biomarkers": {},
        "findings": {
            "creatinine_clearance_ml_min": 85,
            "bilirubin_uln_x": 1.0,
            "alt_uln_x": 1.2,
            "absolute_neutrophil_count_k_ul": 2.8,
            "platelets_k_ul": 210,
            "hemoglobin_g_dl": 11.5,
            "hbsag": "negative",
            "anti_hbc_total": "negative",
            "hcv_status": "negative",
            "hiv_status": "negative",
        },
    }
    if bio_id:
        profile["biomarkers"][bio_id] = bio_val
        profile["findings"]["biomarker_actionable_present"] = True
    if line >= 2:
        profile["findings"]["progression_after_first_line"] = True

    return profile


# ── Engine verification ───────────────────────────────────────────────────


def _verify(profile: dict) -> tuple[bool, str]:
    try:
        if is_diagnostic_profile(profile):
            brief = generate_diagnostic_brief(profile, kb_root=KB_ROOT)
            return (brief is not None), "diagnostic-brief"
        result = generate_plan(profile, kb_root=KB_ROOT)
        if result.plan is None:
            return False, "plan=None"
        if not result.plan.tracks:
            return False, "0 tracks"
        return True, f"{len(result.plan.tracks)} tracks"
    except Exception as exc:
        return False, f"exc {type(exc).__name__}: {str(exc)[:80]}"


# ── site_cases.py patching ────────────────────────────────────────────────

_BMA_BLOCK_BEGIN = (
    "    # ── AUTO-BMA-EXAMPLES "
    "(do not hand-edit; regen via scripts/generate_bma_examples.py) ──"
)
_BMA_BLOCK_END = "    # ── /AUTO-BMA-EXAMPLES ──"


def _render_case_entry(bma: dict, file: str, category: str, msg: str) -> str:
    bma_id = bma["id"]
    dis = bma["disease_id"]
    bio = bma.get("biomarker_id", "")
    escat = bma.get("escat_tier", "?")
    vq = (bma.get("variant_qualifier") or "")[:60].replace('"', '\\"')
    case_id = f"bma-{bma_id.lower().replace('_', '-')}"
    label_ua = f"{dis} · {bio} (ESCAT {escat})"
    label_en = f"{dis} · {bio} (ESCAT {escat})"
    summary_ua = (
        f"Синтетичний профіль: {bio} ({vq}). ESCAT {escat}. Engine: {msg}. "
        "Не для клінічних рішень."
    ).replace('"', '\\"')
    summary_en = (
        f"Synthetic profile: {bio} ({vq}). ESCAT {escat}. Engine: {msg}. "
        "Not for clinical decisions."
    ).replace('"', '\\"')
    return (
        f'    CaseEntry(\n'
        f'        case_id="{case_id}",\n'
        f'        file="{file}",\n'
        f'        label_ua="{label_ua}",\n'
        f'        summary_ua="{summary_ua}",\n'
        f'        badge="BMA", badge_class="bdg-stub", category="{category}",\n'
        f'        label_en="{label_en}",\n'
        f'        summary_en="{summary_en}",\n'
        f'    ),'
    )


def _patch_site_cases(entries: list[str]) -> None:
    text = SITE_CASES.read_text(encoding="utf-8")
    block = _BMA_BLOCK_BEGIN + "\n" + "\n".join(entries) + "\n" + _BMA_BLOCK_END

    if _BMA_BLOCK_BEGIN in text and _BMA_BLOCK_END in text:
        s = text.index(_BMA_BLOCK_BEGIN)
        e = text.index(_BMA_BLOCK_END) + len(_BMA_BLOCK_END)
        new_text = text[:s] + block + text[e:]
    else:
        marker = "\n]\n"
        last = text.rfind(marker)
        if last < 0:
            print("ERROR: CASES closing bracket not found", file=sys.stderr)
            return
        new_text = text[:last] + "\n" + block + "\n" + text[last:]
    SITE_CASES.write_text(new_text, encoding="utf-8")


# ── Main ──────────────────────────────────────────────────────────────────


def main() -> int:
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    # ── Load all BMAs ──
    bmas: list[dict] = []
    for f in sorted(BMA_DIR.iterdir()):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        if isinstance(d, dict) and d.get("escat_tier") in ESCAT_INCLUDE:
            bmas.append(d)
    print(f"BMA entries (ESCAT I-II): {len(bmas)}")

    # ── Already-covered (disease, biomarker) pairs ──
    docs_examples = REPO_ROOT / "docs" / "examples.json"
    covered_pairs: set[tuple[str, str]] = set()
    if docs_examples.exists():
        for e in json.loads(docs_examples.read_text(encoding="utf-8")):
            j = e.get("json") or {}
            dis = (j.get("disease") or {}).get("id") or ""
            for bio_id in (j.get("biomarkers") or {}):
                covered_pairs.add((dis, bio_id))
    print(f"Already-covered (disease, biomarker) pairs: {len(covered_pairs)}")

    # ── Build target list (deduplicate by (disease, biomarker)) ──
    seen: set[tuple[str, str]] = set()
    targets: list[dict] = []
    for b in bmas:
        key = (b.get("disease_id", ""), b.get("biomarker_id", ""))
        if key in covered_pairs or key in seen:
            continue
        seen.add(key)
        targets.append(b)
    print(f"Target (disease, biomarker) pairs to generate: {len(targets)}")

    # ── Disease family lookup for category ──
    rows = per_disease_metrics(KB_ROOT)
    family_map = {r["id"]: r.get("family", "") for r in rows}

    load = load_content(KB_ROOT)

    written = 0
    failed: list[tuple[str, str]] = []
    case_entries: list[str] = []

    for b in targets:
        dis = b["disease_id"]
        bio = b.get("biomarker_id", "")
        bma_id_lower = b["id"].lower()
        file = f"bma_{bma_id_lower.replace('-', '_')}.json"
        path = EXAMPLES_DIR / file

        profile = _build_profile(b)
        ok, msg = _verify(profile)

        if not ok:
            failed.append((b["id"], msg))
            print(f"  FAIL {b['id']}: {msg}")
            continue

        path.write_text(
            json.dumps(profile, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        category = _category_for(dis, family_map.get(dis, ""))
        case_entries.append(_render_case_entry(b, file, category, msg))
        written += 1
        print(f"  OK   {b['id']} ({b.get('escat_tier')}) => {msg}")

    print(f"\nWrote {written} BMA example profiles. Failed: {len(failed)}.")
    if failed:
        print("Failures:")
        for bma_id, m in failed:
            print(f"  FAIL {bma_id}: {m}")

    if case_entries:
        _patch_site_cases(case_entries)
        print(f"Patched scripts/site_cases.py with {len(case_entries)} BMA CaseEntry rows.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
