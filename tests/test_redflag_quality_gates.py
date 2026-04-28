"""Phase-7 quality gates for RedFlag content.

Two contracts beyond the wiring check:

1. **Source-count gate (CHARTER §6.1, REDFLAG_AUTHORING_GUIDE §6).**
   Every non-draft RedFlag must cite ≥2 real Tier-1/2 sources.
   "SRC-TODO" is intentionally not a real source — the scaffold tool
   leaves it as a placeholder so CI is loud, not silent.

2. **5-type matrix gate (REDFLAG_AUTHORING_GUIDE §2).**
   For each Disease in the KB, the union of its non-universal RFs
   should cover all 5 spec categories: organ_dysfunction,
   infection_screening, high_risk_biology, transformation_progression,
   frailty_age.

Both run in baseline-snapshot mode: the current shortfall is recorded
as a constant so CI fails on REGRESSION (more shortfalls than baseline)
but tolerates the existing gap until Phase 3+4 close it. Tightening
the gate = lowering the baseline number.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"

# ── Phase 7 baselines (frozen 2026-04-25). Lower as Phase 3+4 land. ─────────

# Non-draft RFs that currently cite <2 real sources.
# When this number drops to 0, delete the test's tolerance branch.
SOURCES_BASELINE_SHORTFALL = 0

# Diseases missing one or more of the 5 spec categories.
# Frozen list lets us see exactly which gaps Phase 3 closes; new gaps fail.
SPEC_CATEGORIES = (
    "organ_dysfunction",
    "infection_screening",
    "high_risk_biology",
    "transformation_progression",
    "frailty_age",
)

# 2026-04-27 5-type matrix fully closed across all 28 diseases:
# - DIS-DLBCL-NOS closed by Phase 3 first batch (4 new RFs added 2026-04-25)
# - DIS-MM closed by Phase 3 second batch (3 new RFs added 2026-04-25)
# - 2026-04-26 GI solid-tumor batch — CRC, HCC, gastric, PDAC, esophageal.
# - 2026-04-27 Plan C: AITL, ENDOMETRIAL, HCV-MZL, MELANOMA, OVARIAN, RCC,
#   SCLC, UROTHELIAL.
# - 2026-04-27 Plan A: ALCL, BURKITT, CERVICAL, CHL, CLL, FL, GBM, MCL,
#   MF-SEZARY, PTCL-NOS, WM.
# 2026-04-28 — rare-tumour RF families now cover the 5-type matrix too.
DISEASES_WITH_GAPS_BASELINE: set[str] = set()

# Per spec §2: "Якщо для хвороби якась з категорій клінічно нерелевантна
# ... постав <rf>.notes: з обґрунтуванням замість заглушки." We model that
# exception here: each entry maps disease → set of categories that the
# clinical leads explicitly waive. CI tolerates these gaps; new waivers
# require this constant to grow with a comment.
WAIVED_CATEGORIES_PER_DISEASE: dict[str, set[str]] = {
    # DLBCL NOS first-line: "transformation_progression" is a relapse /
    # interim-PET concept, not an indication-switching trigger at 1L.
    # DLBCL is itself the aggressive endpoint of B-cell transformation.
    "DIS-DLBCL-NOS": {"transformation_progression"},
}


# ── helpers ─────────────────────────────────────────────────────────────────


def _yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _all_redflags() -> list[dict]:
    return [_yaml(p) for p in (KB_ROOT / "redflags").rglob("*.yaml")]


def _all_diseases() -> list[str]:
    out: list[str] = []
    for p in (KB_ROOT / "diseases").rglob("*.yaml"):
        d = _yaml(p)
        if d.get("id"):
            out.append(d["id"])
    return out


def _categorize(rf: dict) -> str:
    """Map an RF to one of the 5 spec categories.

    Priority order:
    1. Explicit `category:` field on the RF (RedFlagCategory enum, see
       schemas/base.py). Hyphenated values translated to underscored
       SPEC_CATEGORIES form. Canonical extension categories added
       2026-04-26 are mapped onto the closest 5-type slot they substitute
       for (see CANONICAL_EXTENSION_TO_SPEC).
    2. Id-suffix (matches scaffold-tool naming convention).
    3. Fallback: keyword scan over id + definition for legacy-named RFs."""

    explicit = rf.get("category")
    if explicit:
        # Hyphen → underscore: "organ-dysfunction" → "organ_dysfunction"
        normalized = explicit.replace("-", "_")
        if normalized in SPEC_CATEGORIES:
            return normalized
        # Canonical extension categories substitute for spec slots:
        #   risk-score              → high_risk_biology (clinical risk
        #                             stratification scores fill the
        #                             high-risk-biology slot per §2)
        #   fitness-eligibility     → frailty_age (performance status +
        #                             eligibility composites)
        #   oncologic-emergency     → organ_dysfunction (acute end-organ
        #                             threat — TLS, SVC, cord compression)
        #   prior-therapy-class     → high_risk_biology (resistance signature
        #                             after class-defining failure)
        #   reproductive-status     → no spec-slot mapping; treated as
        #                             non-matrix metadata (universal RFs are
        #                             skipped by the matrix test anyway).
        extension_map = {
            "risk_score": "high_risk_biology",
            "fitness_eligibility": "frailty_age",
            "oncologic_emergency": "organ_dysfunction",
            "prior_therapy_class": "high_risk_biology",
        }
        if normalized in extension_map:
            return extension_map[normalized]

    rf_id = rf.get("id", "")
    suffix_map = {
        "-FRAILTY-AGE": "frailty_age",
        "-ORGAN-DYSFUNCTION": "organ_dysfunction",
        "-INFECTION-SCREENING": "infection_screening",
        "-HIGH-RISK-BIOLOGY": "high_risk_biology",
        "-TRANSFORMATION-PROGRESSION": "transformation_progression",
    }
    for suffix, cat in suffix_map.items():
        if rf_id.endswith(suffix):
            return cat

    blob = (rf_id + " " + (rf.get("definition") or "")).lower()
    if "frailty" in blob:
        return "frailty_age"
    if any(
        k in blob
        for k in ("organ", "crcl", "lvef", "cirrhosis", "dysfunction", "cardiac")
    ):
        return "organ_dysfunction"
    if any(
        k in blob
        for k in ("infection", "hbv", "hcv", "hiv", "cmv", "serology", "screening")
    ):
        return "infection_screening"
    if any(
        k in blob
        for k in (
            "biology",
            "tp53",
            "del-17",
            "del_17",
            "high-risk",
            "high_risk",
            "high-ipi",
            "cytogen",
            "mutation",
        )
    ):
        return "high_risk_biology"
    if any(
        k in blob
        for k in ("transformation", "progression", "rapid", "lct", "blastoid")
    ):
        return "transformation_progression"
    return "other"


# ── tests ──────────────────────────────────────────────────────────────────


def test_non_draft_rf_has_two_sources():
    shortfall: list[str] = []
    for rf in _all_redflags():
        if rf.get("draft"):
            continue
        real_sources = [s for s in (rf.get("sources") or []) if s and s != "SRC-TODO"]
        if len(real_sources) < 2:
            shortfall.append(rf["id"])

    if len(shortfall) > SOURCES_BASELINE_SHORTFALL:
        pytest.fail(
            f"Source-count regression: {len(shortfall)} non-draft RFs cite "
            f"<2 real sources, baseline allows {SOURCES_BASELINE_SHORTFALL}. "
            f"Either add a second tier-1/2 source per spec §6.1, or revert "
            f"the change.\nFailing RFs:\n  "
            + "\n  ".join(sorted(shortfall))
        )

    if len(shortfall) < SOURCES_BASELINE_SHORTFALL:
        pytest.fail(
            f"Source-count baseline is stale: only {len(shortfall)} RFs "
            f"now have <2 sources, but baseline says "
            f"{SOURCES_BASELINE_SHORTFALL}. Lower SOURCES_BASELINE_SHORTFALL "
            f"to {len(shortfall)} to lock in the improvement."
        )


def test_5type_matrix_coverage():
    diseases = set(_all_diseases())
    by_disease_cats: dict[str, set[str]] = defaultdict(set)
    for rf in _all_redflags():
        rel = rf.get("relevant_diseases") or []
        if rel == ["*"]:
            continue
        cat = _categorize(rf)
        for d in rel:
            by_disease_cats[d].add(cat)

    gaps: set[str] = set()
    for d in diseases:
        cats = by_disease_cats.get(d, set())
        waived = WAIVED_CATEGORIES_PER_DISEASE.get(d, set())
        required = set(SPEC_CATEGORIES) - waived
        if not all(c in cats for c in required):
            gaps.add(d)

    new_gaps = gaps - DISEASES_WITH_GAPS_BASELINE
    if new_gaps:
        pytest.fail(
            f"Disease(s) regressed below 5-type matrix baseline:\n  "
            + "\n  ".join(sorted(new_gaps))
            + "\nEither add the missing category RFs or "
            f"add the disease to DISEASES_WITH_GAPS_BASELINE with a reason."
        )

    closed = DISEASES_WITH_GAPS_BASELINE - gaps
    if closed:
        pytest.fail(
            f"5-type matrix baseline is stale: these diseases now cover all "
            f"5 categories but are still listed in "
            f"DISEASES_WITH_GAPS_BASELINE — remove them to lock the win:\n  "
            + "\n  ".join(sorted(closed))
        )
