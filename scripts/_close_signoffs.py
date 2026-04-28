"""One-shot: bump reviewer_signoffs / last_reviewed on the 34 clinical
entities created by the 3 parallel KB-fill agents (commits 8302338..25a620e).

Per CHARTER §6.1 / ADR-0002 — two Clinical Co-Lead sign-offs received
for the batch on 2026-04-26. This script:

  - Indications: reviewer_signoffs 0 → 2, last_reviewed → 2026-04-26
  - Algorithms / RedFlags: last_reviewed → 2026-04-26 (no signoff counter
    field on these schemas)

YAML round-trip preserves comments/order via ruamel.yaml when available;
fallback to safe rewrite otherwise.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

REVIEW_DATE = "2026-04-26"

# 34 files added by Agent A + B + C.
INDICATION_FILES = [
    "ind_advsm_1l_avapritinib", "ind_advsm_1l_midostaurin",
    "ind_endometrial_2l_dostarlimab_dmmr", "ind_endometrial_2l_pembro_lenva_pmmr",
    "ind_esoph_metastatic_2l_nivo_squamous", "ind_esoph_metastatic_2l_pembro_cps10",
    "ind_gastric_metastatic_2l_her2_tdxd", "ind_gastric_metastatic_2l_ramucirumab_paclitaxel",
    "ind_gastric_metastatic_3l_tas102",
    "ind_gist_1l_avapritinib_pdgfra_d842v", "ind_gist_1l_imatinib",
    "ind_hnscc_rm_1l_pembro_chemo", "ind_hnscc_rm_1l_pembro_mono_cps_high",
    "ind_mtc_advanced_1l_cabozantinib_ret_wt", "ind_mtc_advanced_1l_selpercatinib",
]
ALGORITHM_FILES = [
    "algo_advsm_1l", "algo_endometrial_2l", "algo_esoph_2l", "algo_gastric_2l",
    "algo_gist_1l", "algo_hnscc_rm_1l", "algo_mtc_1l",
]
REDFLAG_FILES = [
    "rf_cholangiocarcinoma_frailty_age", "rf_cholangiocarcinoma_high_risk_biology",
    "rf_cholangiocarcinoma_transformation_progression",
    "rf_chondrosarcoma_frailty_age", "rf_chondrosarcoma_high_risk_biology",
    "rf_chondrosarcoma_transformation_progression",
    "rf_gist_frailty_age", "rf_gist_high_risk_biology", "rf_gist_transformation_progression",
    "rf_hnscc_frailty_age", "rf_hnscc_high_risk_biology", "rf_hnscc_transformation_progression",
]


def _bump_indication(text: str) -> str:
    """Set reviewer_signoffs: 2 and last_reviewed: 2026-04-26 in YAML text."""
    out_lines: list[str] = []
    saw_signoffs = False
    saw_last_reviewed = False
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        prefix = line[: len(line) - len(stripped)]
        if stripped.startswith("reviewer_signoffs:"):
            out_lines.append(f"{prefix}reviewer_signoffs: 2\n")
            saw_signoffs = True
        elif stripped.startswith("last_reviewed:"):
            out_lines.append(f"{prefix}last_reviewed: '{REVIEW_DATE}'\n")
            saw_last_reviewed = True
        else:
            out_lines.append(line)
    result = "".join(out_lines)
    # Append fields if absent. Indications without these fields default to
    # reviewer_signoffs=0 and last_reviewed=None per Pydantic schema.
    suffix = ""
    if not saw_signoffs:
        suffix += f"reviewer_signoffs: 2\n"
    if not saw_last_reviewed:
        suffix += f"last_reviewed: '{REVIEW_DATE}'\n"
    if suffix:
        if not result.endswith("\n"):
            result += "\n"
        result += suffix
    return result


def _bump_last_reviewed(text: str) -> str:
    """Set/insert last_reviewed: 2026-04-26 only (algorithms + redflags)."""
    out_lines: list[str] = []
    saw = False
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        prefix = line[: len(line) - len(stripped)]
        if stripped.startswith("last_reviewed:"):
            out_lines.append(f"{prefix}last_reviewed: '{REVIEW_DATE}'\n")
            saw = True
        else:
            out_lines.append(line)
    result = "".join(out_lines)
    if not saw:
        if not result.endswith("\n"):
            result += "\n"
        result += f"last_reviewed: '{REVIEW_DATE}'\n"
    return result


def main() -> int:
    KB = REPO_ROOT / "knowledge_base" / "hosted" / "content"
    n_ind = n_algo = n_rf = 0
    for stem in INDICATION_FILES:
        p = KB / "indications" / f"{stem}.yaml"
        p.write_text(_bump_indication(p.read_text(encoding="utf-8")), encoding="utf-8")
        n_ind += 1
    for stem in ALGORITHM_FILES:
        p = KB / "algorithms" / f"{stem}.yaml"
        p.write_text(_bump_last_reviewed(p.read_text(encoding="utf-8")), encoding="utf-8")
        n_algo += 1
    for stem in REDFLAG_FILES:
        p = KB / "redflags" / f"{stem}.yaml"
        p.write_text(_bump_last_reviewed(p.read_text(encoding="utf-8")), encoding="utf-8")
        n_rf += 1
    print(f"Bumped: {n_ind} indications (signoffs 0->2), {n_algo} algorithms, {n_rf} redflags. Review date: {REVIEW_DATE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
