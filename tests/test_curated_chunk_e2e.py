"""End-to-end regression fixture for the 60 curated chunk patient cases.

Per docs/plans/kb_data_quality_plan_2026-04-29.md > Q5 Regression Prevention,
the 60 curated patient_*.json cases shipped via PR #150 each prokachuyut
a unique algorithm path through knowledge_base.engine. They are the
natural regression-prevention layer: changes anywhere upstream
(rule edits, schema changes, render tweaks) that perturb a case's
default-track indication or break engine/render pipeline land here as
a test failure.

Per case the fixture asserts:

  1. generate_plan() (or generate_diagnostic_brief() for the 3
     diagnostic profiles) returns successfully.
  2. The default-track indication ID matches a recorded golden
     (or the matched_workup_id, for diagnostic mode).
  3. The rendered HTML is > 8000 bytes.
  4. The rendered HTML contains "FDA" (CHARTER §15 disclosure).

Goldens (CASE_TREATMENT_GOLDENS / CASE_DIAGNOSTIC_GOLDENS) record what
the engine actually emits today — including any documented drift in the
case's JSON `comment` field. The fixture's job is locking current
behavior, not validating clinical correctness; clinical-correctness
review happens in the curated chunk plans + per-case comments.

Scope: ONLY the 60 NEW cases shipped via PR #150 (master commits
234ddfc5..56014acc). `examples/auto_*.json` and `examples/variant_*.json`
have a different test contract and are out of scope here. Existing
patient_*.json files predating PR #150 are also out of scope.

Updating goldens: when an intentional engine/data change perturbs a
case's default indication, regenerate the goldens with
`_scratch/gen_curated_goldens.py` and replace the affected entries
in this file. Do NOT silently widen assertions to "any indication" —
that defeats the regression-prevention purpose.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from knowledge_base.engine import (
    generate_diagnostic_brief,
    generate_plan,
    is_diagnostic_profile,
    render_diagnostic_brief_html,
    render_plan_html,
)
from knowledge_base.validation.loader import load_content

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
EXAMPLES = REPO_ROOT / "examples"


# ── Golden values ─────────────────────────────────────────────────────────
#
# Generated 2026-04-29 by `_scratch/gen_curated_goldens.py`. Each entry is
# the engine's CURRENT default-track indication (treatment) or matched
# workup id (diagnostic). Re-run the generator after intentional engine
# or KB changes; never hand-edit clinical anchors here.

CASE_TREATMENT_GOLDENS: dict[str, str] = {
    "patient_aml_cbf_inv16_7_3_go.json": "IND-AML-1L-7-3",
    "patient_aml_flt3_itd_midostaurin_7_3.json": "IND-AML-1L-7-3",
    "patient_aml_rr_gilteritinib.json": "IND-AML-2L-GILTERITINIB-FLT3",
    "patient_aml_secondary_cpx351.json": "IND-AML-1L-CPX351-SECONDARY",
    "patient_breast_brca_germline_met_olaparib.json": "IND-BREAST-HR-POS-MET-1L-CDKI",
    "patient_breast_her2_pos_early_neoadj_kn522_path.json": "IND-BREAST-HER2-POS-MET-1L-THP",
    "patient_breast_her2_pos_met_1l_thp.json": "IND-BREAST-HER2-POS-MET-1L-THP",
    "patient_breast_her2_pos_met_2l_tdxd.json": "IND-BREAST-HER2-POS-MET-2L-TDXD",
    "patient_breast_hr_pos_her2_neg_met_1l_cdk46i.json": "IND-BREAST-HR-POS-MET-1L-CDKI",
    "patient_breast_hr_pos_post_cdk46i_pik3ca_alpelisib.json": "IND-BREAST-HR-POS-2L-AKT-CAPIVASERTIB",
    "patient_breast_tnbc_met_sacituzumab_2l.json": "IND-BREAST-TNBC-2L-SACITUZUMAB",
    "patient_breast_tnbc_neoadj_kn522_pembro_chemo.json": "IND-BREAST-HR-POS-MET-1L-CDKI",
    "patient_cll_venr_2l_murano.json": "IND-CLL-2L-VENR-MURANO",
    "patient_crc_metastatic_2l_folfiri_bev.json": "IND-CRC-METASTATIC-2L-FOLFIRI-BEV",
    "patient_crc_metastatic_3l_regorafenib.json": "IND-CRC-METASTATIC-3L-TAS102-BEV",
    "patient_crc_metastatic_msi_h_pembro_mono.json": "IND-CRC-METASTATIC-1L-MSI-H-PEMBRO",
    "patient_crc_metastatic_ras_mut_folfox_bev.json": "IND-CRC-METASTATIC-1L-FOLFOX-BEV",
    "patient_crc_metastatic_ras_wt_left_folfox_cetux.json": "IND-CRC-METASTATIC-1L-RAS-WT-LEFT",
    "patient_crc_stage_iii_adjuvant_folfox.json": "IND-CRC-METASTATIC-1L-FOLFOX-BEV",
    "patient_dlbcl_2l_pola_r_b.json": "IND-DLBCL-2L-POLA-R-BENDAMUSTINE",
    "patient_dlbcl_3l_axi_cel.json": "IND-DLBCL-2L-POLA-R-BENDAMUSTINE",
    "patient_dlbcl_primary_refractory_loncast_post_pola.json": "IND-DLBCL-3L-LONCASTUXIMAB",
    "patient_endometrial_dmmr_pembro_kn775.json": "IND-ENDOMETRIAL-ADVANCED-1L-DOSTARLIMAB-CHEMO",
    "patient_endometrial_p53_abn_dosta_kn775.json": "IND-ENDOMETRIAL-ADVANCED-1L-PEMBRO-CHEMO",
    "patient_esophageal_adeno_neoadj_cross_then_nivo.json": "IND-ESOPH-ADJUVANT-NIVOLUMAB-POST-CROSS",
    "patient_gastric_her2_pos_toga.json": "IND-GASTRIC-METASTATIC-1L-HER2-TOGA",
    "patient_gastric_pdl1_cps_high_chemo_nivo.json": "IND-GASTRIC-METASTATIC-1L-PDL1-CHEMO-ICI",
    "patient_hcc_atezo_bev_imbrave150.json": "IND-HCC-SYSTEMIC-1L-ATEZO-BEV",
    "patient_hcc_durva_treme_stride.json": "IND-HCC-SYSTEMIC-1L-DURVA-TREME",
    "patient_hnscc_cps_high_pembro_mono.json": "IND-HNSCC-RM-1L-PEMBRO-MONO-CPS-HIGH",
    "patient_hnscc_extreme_cetux_platin_5fu.json": "IND-HNSCC-RM-1L-EXTREME",
    "patient_mcl_pirtobrutinib_3l_post_btki.json": "IND-MCL-3L-PIRTOBRUTINIB",
    "patient_melanoma_adjuvant_pembro_stage_iii.json": "IND-MELANOMA-ADJUVANT-PEMBRO-STAGE-III",
    "patient_melanoma_braf_v600_dab_tram.json": "IND-MELANOMA-BRAF-METASTATIC-1L-DABRA-TRAME",
    "patient_melanoma_braf_v600_nivo_ipi.json": "IND-MELANOMA-METASTATIC-1L-NIVO-IPI",
    "patient_melanoma_braf_wt_pembro_mono.json": "IND-MELANOMA-METASTATIC-1L-PEMBRO-MONO",
    "patient_melanoma_nivo_relatlimab.json": "IND-MELANOMA-2L-RELATLIMAB-NIVOLUMAB",
    "patient_nsclc_alk_1l_alectinib.json": "IND-NSCLC-ALK-MET-1L",
    "patient_nsclc_alk_2l_lorlatinib.json": "IND-NSCLC-ALK-2L-LORLATINIB",
    "patient_nsclc_braf_v600e_2l_dab_tram.json": "IND-NSCLC-2L-BRAF-V600E-DAB-TRAM",
    "patient_nsclc_egfr_ex19del_1l_osimertinib.json": "IND-NSCLC-EGFR-MUT-MET-1L",
    "patient_nsclc_egfr_t790m_2l_post_1g_tki.json": "IND-NSCLC-2L-EGFR-POST-OSI-AMI-LAZ",
    "patient_nsclc_kras_g12c_2l_sotorasib.json": "IND-NSCLC-2L-KRAS-G12C-SOTORASIB",
    "patient_nsclc_metex14_2l_capmatinib.json": "IND-NSCLC-2L-MET-EX14-CAPMATINIB",
    "patient_nsclc_pdl1_high_pembro_mono.json": "IND-NSCLC-PDL1-HIGH-MET-1L",
    "patient_nsclc_pdl1_low_chemo_io.json": "IND-NSCLC-PDL1-LOW-NONSQ-MET-1L",
    "patient_nsclc_ret_fusion_2l_selpercatinib.json": "IND-NSCLC-2L-RET-FUSION-SELPERCATINIB",
    "patient_nsclc_ros1_2l_entrectinib.json": "IND-NSCLC-2L-ROS1-POST-CRIZ-ENTRECTINIB",
    "patient_nsclc_tmb_high_pembro_mono.json": "IND-NSCLC-PDL1-LOW-NONSQ-MET-1L",
    "patient_ovarian_hrd_neg_carbo_pacli_no_parpi.json": "IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-NEG",
    "patient_pdac_metastatic_folfirinox_fit.json": "IND-PDAC-METASTATIC-1L-FOLFIRINOX",
    "patient_prostate_mcrpc_brca_olaparib_profound.json": "IND-PROSTATE-MCRPC-1L-PARPI",
    "patient_rcc_imdc_fav_axi_pembro.json": "IND-RCC-METASTATIC-1L-PEMBRO-AXI",
    "patient_rcc_imdc_int_nivo_ipi.json": "IND-RCC-METASTATIC-1L-NIVO-IPI",
    "patient_sclc_es_atezo_chemo_impower133.json": "IND-SCLC-EXTENSIVE-1L",
    "patient_sclc_ls_chemo_rt.json": "IND-SCLC-EXTENSIVE-1L",
    "patient_urothelial_muc_ev_pembro.json": "IND-UROTHELIAL-METASTATIC-1L-EV-PEMBRO",
}

CASE_DIAGNOSTIC_GOLDENS: dict[str, str] = {
    "patient_diagnostic_breast_lump_prebiopsy.json": "WORKUP-SUSPECTED-BREAST",
    "patient_diagnostic_lung_mass_smoker_prebiopsy.json": "WORKUP-SUSPECTED-NSCLC",
    "patient_diagnostic_prostate_psa_elevated_prebiopsy.json": "WORKUP-SUSPECTED-PROSTATE",
    # Diagnostic-mode expansion 2026-05-01 (13 new cases — covers
    # workups that had no curated example before): acute leukemia,
    # CRC, endometrial, GBM, HCC, melanoma, MDS-pancytopenia
    # (cytopenia-eval), MPN polycythemia, MM, ovarian, RCC, SCLC,
    # urothelial. Each emits Diagnostic Brief, NOT Treatment Plan
    # (CHARTER §15.2 C7).
    "patient_diagnostic_acute_leukemia_circulating_blasts.json": "WORKUP-SUSPECTED-ACUTE-LEUKEMIA",
    "patient_diagnostic_crc_lgib_iron_deficiency.json": "WORKUP-SUSPECTED-CRC",
    "patient_diagnostic_endometrial_pmb.json": "WORKUP-SUSPECTED-ENDOMETRIAL",
    "patient_diagnostic_gbm_focal_neuro_deficit.json": "WORKUP-SUSPECTED-GBM",
    "patient_diagnostic_hcc_cirrhosis_li_rads.json": "WORKUP-SUSPECTED-HCC",
    "patient_diagnostic_melanoma_atypical_lesion.json": "WORKUP-SUSPECTED-MELANOMA",
    "patient_diagnostic_mm_bone_pain_m_protein.json": "WORKUP-SUSPECTED-MULTIPLE-MYELOMA",
    "patient_diagnostic_mpn_mds_pancytopenia.json": "WORKUP-CYTOPENIA-EVALUATION",
    "patient_diagnostic_mpn_polycythemia_pruritus.json": "WORKUP-SUSPECTED-MPN-MDS",
    "patient_diagnostic_ovarian_pelvic_mass_ca125.json": "WORKUP-SUSPECTED-OVARIAN",
    "patient_diagnostic_rcc_incidental_mass.json": "WORKUP-SUSPECTED-RCC",
    "patient_diagnostic_sclc_central_lung_siadh.json": "WORKUP-SUSPECTED-SCLC",
    "patient_diagnostic_urothelial_gross_hematuria.json": "WORKUP-SUSPECTED-UROTHELIAL",
}

# Combined param list: 73 cases (57 treatment + 16 diagnostic).
ALL_CASES: list[str] = sorted(
    list(CASE_TREATMENT_GOLDENS.keys()) + list(CASE_DIAGNOSTIC_GOLDENS.keys())
)

MIN_RENDER_BYTES = 8000


# ── Module-level fixtures ─────────────────────────────────────────────────


@pytest.fixture(scope="module")
def kb_validator() -> dict[str, Any]:
    """Load + validate the KB once for the whole module.

    A KB with schema_errors or ref_errors is itself a regression — fail
    the entire module before any per-case test runs."""
    load = load_content(KB_ROOT)
    schema_errors = list(load.schema_errors)
    ref_errors = list(load.ref_errors)
    assert not schema_errors, (
        f"KB schema_errors before curated chunk run: {schema_errors[:3]}"
    )
    assert not ref_errors, (
        f"KB ref_errors before curated chunk run: {ref_errors[:3]}"
    )
    return {
        "entities": load.entities_by_id,
        "n_entities": len(load.entities_by_id),
    }


# ── Sanity ────────────────────────────────────────────────────────────────


def test_curated_case_count_matches_expected_scope():
    """Guard against silent drift in the curated case set.

    PR #150 shipped 60 curated patient_*.json files (57 treatment +
    3 diagnostic). The 2026-05-01 diagnostic-mode expansion added 13
    new diagnostic cases, bringing total to 73 (57 treatment + 16
    diagnostic). If this count changes, update the golden dicts
    deliberately rather than letting parametrize drift."""
    assert len(ALL_CASES) == 73, (
        f"expected 73 curated cases (PR #150 + 2026-05-01 diagnostic "
        f"expansion); got {len(ALL_CASES)}"
    )
    assert len(CASE_TREATMENT_GOLDENS) == 57
    assert len(CASE_DIAGNOSTIC_GOLDENS) == 16


def test_golden_files_exist_on_disk():
    """Every golden key must reference an actual file under examples/."""
    missing = [fn for fn in ALL_CASES if not (EXAMPLES / fn).is_file()]
    assert not missing, f"golden refs to missing files: {missing}"


# ── Per-case parametrized smoke ──────────────────────────────────────────


@pytest.mark.parametrize("case_filename", ALL_CASES)
def test_curated_case_e2e(case_filename: str, kb_validator):
    """For each curated case: engine + render must succeed and match
    recorded goldens for the default track."""
    patient = json.loads(
        (EXAMPLES / case_filename).read_text(encoding="utf-8")
    )

    if is_diagnostic_profile(patient):
        # Diagnostic mode: workup-only, no Plan/tracks.
        expected_workup = CASE_DIAGNOSTIC_GOLDENS.get(case_filename)
        assert expected_workup, (
            f"diagnostic golden missing for {case_filename}"
        )
        result = generate_diagnostic_brief(patient, kb_root=KB_ROOT)
        assert result.matched_workup_id == expected_workup, (
            f"{case_filename}: expected matched_workup_id="
            f"{expected_workup!r}, got {result.matched_workup_id!r}"
        )
        # Diagnostic plan must materialise (non-None means workup
        # was found and steps populated).
        assert result.diagnostic_plan is not None, (
            f"{case_filename}: diagnostic_plan is None despite "
            f"matched_workup_id={result.matched_workup_id!r}"
        )
        html = render_diagnostic_brief_html(result)
    else:
        expected_ind = CASE_TREATMENT_GOLDENS.get(case_filename)
        assert expected_ind, (
            f"treatment golden missing for {case_filename}"
        )
        result = generate_plan(patient, kb_root=KB_ROOT)
        assert result.default_indication_id == expected_ind, (
            f"{case_filename}: expected default_indication_id="
            f"{expected_ind!r}, got {result.default_indication_id!r}"
        )
        # Plan must materialise. Track count is intentionally NOT
        # asserted here: a few cases (e.g.,
        # patient_crc_metastatic_msi_h_pembro_mono.json,
        # patient_esophageal_adeno_neoadj_cross_then_nivo.json)
        # currently emit a single track because the algorithm only
        # exposes one output_indication for the matched branch — the
        # case JSON `comment` field documents this engine drift. The
        # CHARTER §2 ≥2-tracks invariant is enforced at the engine /
        # reference-case level (test_reference_case_e2e.py); this
        # fixture's job is locking current per-case behavior.
        assert result.plan is not None, f"{case_filename}: result.plan is None"
        html = render_plan_html(result)

    assert len(html) > MIN_RENDER_BYTES, (
        f"{case_filename}: rendered HTML only {len(html)} bytes "
        f"(< {MIN_RENDER_BYTES})"
    )
    assert "FDA" in html, (
        f"{case_filename}: rendered HTML missing 'FDA' "
        f"(CHARTER §15 non-device CDS disclosure)"
    )
