"""Generate the small public showcase used by the examples gallery.

The full examples/ corpus remains available to try.html so every
questionnaire disease still has at least one JSON profile. The public
gallery, however, should be a curated precision-oncology walkthrough:
few cases, each demonstrating why the CIViC/ESCAT actionability layer is
useful.

Usage:
    python -m scripts.generate_showcase_examples
"""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
SITE_CASES = REPO_ROOT / "scripts" / "site_cases.py"

SHOWCASE_IDS = [
    "showcase-nsclc-alk-fusion-1l",
    "showcase-crc-braf-v600e-2l",
    "showcase-breast-pik3ca-h1047r-2l",
    "showcase-ovarian-brca1-maintenance",
    "showcase-nsclc-egfr-t790m-2l",
    "showcase-ifs-ntrk-fusion",
    "showcase-melanoma-braf-v600e-1l",
    "showcase-cholangio-idh1-r132-2l",
    "showcase-gastric-her2-amp-1l",
    "showcase-prostate-brca2-germline-mcrpc",
    "showcase-endometrial-dmmr-msh2-1l",
    "showcase-thyroid-ret-fusion-rai-refractory",
    "showcase-gist-kit-exon11-1l",
    "showcase-aml-flt3-itd-1l",
]

_SHOWCASE_BLOCK_BEGIN = "    # -- CURATED SHOWCASE CASES (regen via scripts/generate_showcase_examples.py) --"
_SHOWCASE_BLOCK_END = "    # -- /CURATED SHOWCASE CASES --"


def _case(
    *,
    case_id: str,
    file: str,
    label_ua: str,
    summary_ua: str,
    category: str,
    label_en: str,
    summary_en: str,
    patient: dict,
) -> dict:
    return {
        "case_id": case_id,
        "file": file,
        "label_ua": label_ua,
        "summary_ua": summary_ua,
        "badge": "Treatment Plan",
        "badge_class": "bdg-plan",
        "category": category,
        "label_en": label_en,
        "summary_en": summary_en,
        "patient": patient,
    }


SHOWCASE_CASES = [
    _case(
        case_id="showcase-nsclc-alk-fusion-1l",
        file="patient_showcase_nsclc_alk_fusion_1l.json",
        label_ua="NSCLC - ALK fusion - ESCAT IA / CIViC evidence",
        summary_ua=(
            "Метастатична аденокарцинома легень з ALK fusion і метастазами в мозок. "
            "Показує сильний ESCAT IA сигнал, CIViC evidence lanes і те, що actionability "
            "подається як контекст для MDT, а не як прихований ranking engine."
        ),
        category="solid",
        label_en="NSCLC - ALK fusion - ESCAT IA / CIViC evidence",
        summary_en=(
            "Metastatic lung adenocarcinoma with ALK fusion and brain metastases. "
            "Demonstrates a strong ESCAT IA signal, CIViC evidence lanes, and the "
            "separation between MDT context and treatment-track selection."
        ),
        patient={
            "patient_id": "SHOWCASE-NSCLC-ALK-001",
            "comment": "Synthetic showcase case. Demonstrates BMA-ALK-FUSION-NSCLC with ESCAT IA and CIViC evidence lanes.",
            "disease": {"id": "DIS-NSCLC"},
            "line_of_therapy": 1,
            "biomarkers": {
                "ALK": "fusion (gene-level, TKI-naive)",
                "BIO-ALK-FUSION": "positive",
                "EGFR": "wildtype",
                "ROS1": "negative",
                "PD-L1 TPS": 0,
            },
            "demographics": {
                "age": 48,
                "sex": "female",
                "ecog": 0,
                "smoking_status": "never",
            },
            "findings": {
                "stage": "IV",
                "stage_iv": True,
                "histology": "adenocarcinoma",
                "alk_fusion": True,
                "alk_status": "positive",
                "metastatic_sites": ["brain", "bone"],
                "brain_mets": True,
                "creatinine_clearance_ml_min": 92,
                "bilirubin_uln_x": 0.8,
                "absolute_neutrophil_count_k_ul": 3.2,
                "platelets_k_ul": 245,
                "hbsag": "negative",
                "anti_hbc_total": "negative",
                "hcv_status": "negative",
                "hiv_status": "negative",
            },
        },
    ),
    _case(
        case_id="showcase-crc-braf-v600e-2l",
        file="patient_showcase_crc_braf_v600e_2l.json",
        label_ua="mCRC - BRAF V600E - tumor-specific actionability",
        summary_ua=(
            "BRAF V600E після прогресії на FOLFOX. Кейс показує, чому один і той самий "
            "варіант не можна трактувати поза пухлинним контекстом: у CRC потрібна "
            "EGFR-комбінація, а не проста BRAF-монотерапія."
        ),
        category="solid",
        label_en="mCRC - BRAF V600E - tumor-specific actionability",
        summary_en=(
            "BRAF V600E after FOLFOX progression. Shows why a variant cannot be "
            "interpreted outside tumor context: CRC needs an EGFR-combination strategy, "
            "not simple BRAF monotherapy."
        ),
        patient={
            "patient_id": "SHOWCASE-CRC-BRAF-001",
            "comment": "Synthetic showcase case. Demonstrates BMA-BRAF-V600E-CRC, ESCAT IB, CIViC support and resistance evidence lanes.",
            "disease": {"id": "DIS-CRC"},
            "line_of_therapy": 2,
            "biomarkers": {
                "BRAF": "V600E",
                "BIO-BRAF-V600E": "positive",
                "MSI": "MSS",
                "BIO-MSI-STATUS": "stable",
                "RAS": "wildtype",
            },
            "demographics": {"age": 61, "sex": "female", "ecog": 1},
            "findings": {
                "stage": "IV",
                "stage_iv": True,
                "primary_site": "right colon",
                "braf_v600e_mutation": True,
                "metastatic_sites": ["liver", "peritoneum"],
                "prior_lines": [
                    {
                        "line": 1,
                        "regimen": "FOLFOX + bevacizumab",
                        "cycles": 8,
                        "best_response": "PR",
                        "outcome": "PD at 6 mo",
                    }
                ],
                "creatinine_clearance_ml_min": 88,
                "bilirubin_uln_x": 0.9,
                "absolute_neutrophil_count_k_ul": 2.8,
                "platelets_k_ul": 240,
                "hbsag": "negative",
                "anti_hbc_total": "negative",
                "hcv_status": "negative",
                "hiv_status": "negative",
            },
        },
    ),
    _case(
        case_id="showcase-breast-pik3ca-h1047r-2l",
        file="patient_showcase_breast_pik3ca_h1047r_2l.json",
        label_ua="Breast HR+/HER2- - PIK3CA H1047R - post-CDK4/6i",
        summary_ua=(
            "HR+/HER2- метастатичний рак молочної залози після CDK4/6i з PIK3CA H1047R. "
            "Показує, як ESCAT/CIViC шар додає молекулярний контекст до 2L endocrine-targeted "
            "опцій і одночасно залишає клінічні обмеження видимими."
        ),
        category="solid",
        label_en="Breast HR+/HER2- - PIK3CA H1047R - post-CDK4/6i",
        summary_en=(
            "HR+/HER2- metastatic breast cancer after CDK4/6i with PIK3CA H1047R. "
            "Shows how the ESCAT/CIViC layer adds molecular context to 2L endocrine-targeted "
            "options while keeping clinical constraints visible."
        ),
        patient={
            "patient_id": "SHOWCASE-BREAST-PIK3CA-001",
            "comment": "Synthetic showcase case. Demonstrates BMA-PIK3CA-H1047R-BREAST with ESCAT IA and CIViC evidence.",
            "disease": {"id": "DIS-BREAST"},
            "disease_state": "HR-positive_HER2-negative",
            "line_of_therapy": 2,
            "biomarkers": {
                "ER": "positive",
                "PR": "positive",
                "HER2": "negative",
                "BIO-ER": "positive",
                "BIO-PR": "positive",
                "BIO-HER2-SOLID": "negative",
                "PIK3CA": "H1047R",
                "BIO-PIK3CA-MUTATION": "H1047R positive",
                "ESR1": "wildtype",
            },
            "demographics": {"age": 56, "sex": "female", "ecog": 1},
            "findings": {
                "stage": "IV",
                "stage_iv": True,
                "receptor_subtype": "HR_POS_HER2_NEG",
                "histology": "invasive ductal carcinoma",
                "metastatic_sites": ["bone", "liver"],
                "her2_status": "negative",
                "her2_ihc": 0,
                "er_status": "positive",
                "pr_status": "positive",
                "pik3ca_mutation": True,
                "pik3ca_hotspot": "positive",
                "progression_on_prior_endocrine_cdk46i": True,
                "prior_lines": [
                    {
                        "line": 1,
                        "regimen": "letrozole + palbociclib",
                        "duration_months": 22,
                        "best_response": "PR",
                        "outcome": "PD at 22 mo",
                    }
                ],
                "creatinine_clearance_ml_min": 90,
                "bilirubin_uln_x": 0.8,
                "absolute_neutrophil_count_k_ul": 3.0,
                "platelets_k_ul": 245,
                "fasting_glucose_mg_dL": 96,
                "hba1c_percent": 5.6,
                "hbsag": "negative",
                "anti_hbc_total": "negative",
                "hcv_status": "negative",
                "hiv_status": "negative",
            },
        },
    ),
    _case(
        case_id="showcase-ovarian-brca1-maintenance",
        file="patient_showcase_ovarian_brca1_maintenance.json",
        label_ua="Ovarian - germline BRCA1 - PARPi maintenance",
        summary_ua=(
            "Платин-чутливий рецидив high-grade serous ovarian carcinoma з germline BRCA1. "
            "Показує ESCAT IA, CIViC sensitivity/resistance evidence і практичний контекст "
            "для підтримувальної PARPi та каскадного тестування родини."
        ),
        category="solid",
        label_en="Ovarian - germline BRCA1 - PARPi maintenance",
        summary_en=(
            "Platinum-sensitive recurrent high-grade serous ovarian carcinoma with germline BRCA1. "
            "Shows ESCAT IA, CIViC sensitivity/resistance evidence, and the practical context for "
            "PARPi maintenance plus family cascade testing."
        ),
        patient={
            "patient_id": "SHOWCASE-OVARIAN-BRCA1-001",
            "comment": "Synthetic showcase case. Demonstrates BMA-BRCA1-GERMLINE-OVARIAN with ESCAT IA and CIViC evidence lanes.",
            "disease": {"id": "DIS-OVARIAN"},
            "line_of_therapy": 2,
            "biomarkers": {
                "BRCA1": "BRCA1 germline pathogenic",
                "BIO-HRD-STATUS": "HRD-positive",
            },
            "demographics": {"age": 57, "sex": "female", "ecog": 1},
            "findings": {
                "stage": "FIGO IIIC",
                "histology": "high-grade serous",
                "hrd_status": "HRD-positive",
                "brca1_brca2_pathogenic": True,
                "platinum_free_interval_months": 8,
                "platinum_sensitive": True,
                "primary_debulking_residual_cm": 0,
                "prior_lines": [
                    {
                        "line": 1,
                        "regimen": "carboplatin + paclitaxel + bevacizumab",
                        "cycles": 6,
                        "best_response": "CR",
                        "outcome": "biochemical recurrence at PFI 8 mo",
                    }
                ],
                "post_reinduction_response": "PR",
                "creatinine_clearance_ml_min": 92,
                "bilirubin_uln_x": 0.8,
                "absolute_neutrophil_count_k_ul": 2.6,
                "platelets_k_ul": 235,
                "ca125_U_mL": 92,
                "hbsag": "negative",
                "anti_hbc_total": "negative",
                "hcv_status": "negative",
                "hiv_status": "negative",
            },
        },
    ),
    _case(
        case_id="showcase-nsclc-egfr-t790m-2l",
        file="patient_showcase_nsclc_egfr_t790m_2l.json",
        label_ua="NSCLC - acquired EGFR T790M - resistance-aware review",
        summary_ua=(
            "EGFR-mutated NSCLC з прогресією після першого покоління TKI і acquired T790M. "
            "Показує, як resistance/actionability evidence стає видимим для MDT замість "
            "того, щоб губитися в загальному списку мутацій."
        ),
        category="solid",
        label_en="NSCLC - acquired EGFR T790M - resistance-aware review",
        summary_en=(
            "EGFR-mutated NSCLC progressing after first-generation TKI with acquired T790M. "
            "Shows resistance/actionability evidence explicitly for MDT review instead of "
            "burying it in a generic mutation list."
        ),
        patient={
            "patient_id": "SHOWCASE-NSCLC-EGFR-T790M-001",
            "comment": "Synthetic showcase case. Demonstrates BMA-EGFR-T790M-NSCLC and resistance-aware actionability rendering.",
            "disease": {"id": "DIS-NSCLC"},
            "line_of_therapy": 2,
            "biomarkers": {
                "EGFR": "T790M",
                "BIO-EGFR-MUTATION": "T790M",
                "ALK": "negative",
                "ROS1": "negative",
                "PD-L1 TPS": 10,
            },
            "demographics": {"age": 63, "sex": "female", "ecog": 1},
            "findings": {
                "stage": "IV",
                "stage_iv": True,
                "histology": "adenocarcinoma",
                "primary_site": "right upper lobe",
                "egfr_t790m": True,
                "egfr_mutation": "T790M",
                "metastatic_sites": ["bone", "contralateral lung"],
                "brain_mets": False,
                "prior_lines": [
                    {
                        "line": 1,
                        "regimen": "erlotinib",
                        "duration_months": 18,
                        "best_response": "PR",
                        "outcome": "PD with acquired T790M",
                    }
                ],
                "creatinine_clearance_ml_min": 86,
                "bilirubin_uln_x": 0.9,
                "absolute_neutrophil_count_k_ul": 3.1,
                "platelets_k_ul": 260,
                "hbsag": "negative",
                "anti_hbc_total": "negative",
                "hcv_status": "negative",
                "hiv_status": "negative",
            },
        },
    ),
    _case(
        case_id="showcase-ifs-ntrk-fusion",
        file="patient_showcase_ifs_ntrk_fusion.json",
        label_ua="Infantile fibrosarcoma - NTRK fusion - rare tumor target",
        summary_ua=(
            "Рідкісна пухлина з ETV6-NTRK3 fusion. Кейс показує, як молекулярна "
            "actionability допомагає не загубити targetable alteration у діагнозі, де "
            "традиційні сценарії лікування часто неповні."
        ),
        category="solid",
        label_en="Infantile fibrosarcoma - NTRK fusion - rare tumor target",
        summary_en=(
            "Rare tumor with ETV6-NTRK3 fusion. Shows how molecular actionability prevents "
            "a targetable alteration from being lost in a diagnosis where conventional "
            "treatment pathways are often sparse."
        ),
        patient={
            "patient_id": "SHOWCASE-IFS-NTRK-001",
            "comment": "Synthetic showcase case. Demonstrates BMA-NTRK-FUSION-IFS and rare-tumor precision actionability.",
            "disease": {"id": "DIS-IFS"},
            "line_of_therapy": 1,
            "biomarkers": {
                "NTRK": "ETV6-NTRK3 fusion",
                "BIO-NTRK-FUSION": "positive",
            },
            "demographics": {"age": 2, "sex": "female", "ecog": 1},
            "findings": {
                "stage": "locally_advanced",
                "primary_site": "left thigh soft tissue",
                "tumor_size_cm": 6.2,
                "unresectable_without_morbidity": True,
                "creatinine_clearance_ml_min": 75,
                "bilirubin_uln_x": 0.7,
                "absolute_neutrophil_count_k_ul": 2.9,
                "platelets_k_ul": 310,
                "hbsag": "negative",
                "anti_hbc_total": "negative",
                "hcv_status": "negative",
                "hiv_status": "negative",
            },
        },
    ),
    _case(
        case_id="showcase-melanoma-braf-v600e-1l",
        file="patient_showcase_melanoma_braf_v600e_1l.json",
        label_ua="Melanoma - BRAF V600E - targeted vs immunotherapy context",
        summary_ua=(
            "Метастатична меланома з BRAF V600E. Показує класичний ESCAT IA / CIViC приклад, "
            "де biomarker actionability пояснює BRAF/MEK чутливість, але MDT усе одно бачить "
            "клінічний контекст для вибору послідовності з immunotherapy."
        ),
        category="solid",
        label_en="Melanoma - BRAF V600E - targeted vs immunotherapy context",
        summary_en=(
            "Metastatic melanoma with BRAF V600E. Shows a classic ESCAT IA / CIViC case "
            "where actionability explains BRAF/MEK sensitivity while MDT still sees the "
            "clinical sequencing context with immunotherapy."
        ),
        patient={
            "patient_id": "SHOWCASE-MELANOMA-BRAF-001",
            "comment": "Synthetic showcase case. Demonstrates BMA-BRAF-V600E-MELANOMA with CIViC sensitivity and resistance lanes.",
            "disease": {"id": "DIS-MELANOMA"},
            "line_of_therapy": 1,
            "biomarkers": {
                "BRAF": "V600E",
                "BIO-BRAF-V600E": "V600E",
                "NRAS": "wildtype",
                "KIT": "wildtype",
                "PD-L1": "not required for melanoma decision",
            },
            "demographics": {"age": 44, "sex": "male", "ecog": 1},
            "findings": {
                "stage": "IV",
                "stage_iv": True,
                "histology": "cutaneous melanoma",
                "metastatic_sites": ["lung", "liver", "subcutaneous"],
                "brain_mets": False,
                "ldh_uln_x": 1.4,
                "symptomatic_bulk": True,
                "creatinine_clearance_ml_min": 96,
                "bilirubin_uln_x": 0.9,
                "absolute_neutrophil_count_k_ul": 3.3,
                "platelets_k_ul": 255,
                "hbsag": "negative",
                "anti_hbc_total": "negative",
                "hcv_status": "negative",
                "hiv_status": "negative",
            },
        },
    ),
    _case(
        case_id="showcase-cholangio-idh1-r132-2l",
        file="patient_showcase_cholangio_idh1_r132_2l.json",
        label_ua="Cholangiocarcinoma - IDH1 R132 - 2L molecular option",
        summary_ua=(
            "Внутрішньопечінкова холангіокарцинома з IDH1 R132C після gem/cis/durvalumab. "
            "Кейс показує, як ESCAT/CIViC шар не дає втратити 2L molecular option у пухлині, "
            "де стандартні chemotherapy tracks швидко вичерпуються."
        ),
        category="solid",
        label_en="Cholangiocarcinoma - IDH1 R132 - 2L molecular option",
        summary_en=(
            "Intrahepatic cholangiocarcinoma with IDH1 R132C after gem/cis/durvalumab. "
            "Shows how ESCAT/CIViC context keeps a 2L molecular option visible when "
            "standard chemotherapy tracks are limited."
        ),
        patient={
            "patient_id": "SHOWCASE-CHOLANGIO-IDH1-001",
            "comment": "Synthetic showcase case. Demonstrates BMA-IDH1-R132-CHOLANGIO and 2L ivosidenib context.",
            "disease": {"id": "DIS-CHOLANGIOCARCINOMA"},
            "line_of_therapy": 2,
            "biomarkers": {
                "IDH1": "R132C",
                "BIO-IDH-MUTATION": "R132C",
                "FGFR2": "negative",
                "MSI": "MSS",
            },
            "demographics": {"age": 59, "sex": "female", "ecog": 1},
            "findings": {
                "stage": "IV",
                "stage_iv": True,
                "primary_site": "intrahepatic bile duct",
                "idh1_r132_mutation": True,
                "idh1_status": "R132",
                "metastatic_sites": ["liver", "peritoneum"],
                "prior_lines": [
                    {
                        "line": 1,
                        "regimen": "gemcitabine + cisplatin + durvalumab",
                        "cycles": 8,
                        "best_response": "SD",
                        "outcome": "PD after 7 mo",
                    }
                ],
                "creatinine_clearance_ml_min": 82,
                "bilirubin_uln_x": 1.1,
                "absolute_neutrophil_count_k_ul": 2.7,
                "platelets_k_ul": 220,
                "hbsag": "negative",
                "anti_hbc_total": "negative",
                "hcv_status": "negative",
                "hiv_status": "negative",
            },
        },
    ),
    _case(
        case_id="showcase-gastric-her2-amp-1l",
        file="patient_showcase_gastric_her2_amp_1l.json",
        label_ua="Gastric/GEJ - HER2 amplification - IHC/ISH actionability",
        summary_ua=(
            "Метастатична gastric/GEJ adenocarcinoma з HER2 IHC 3+. Показує, як actionability "
            "шар розділяє IHC/ISH evidence, 1L trastuzumab-based tracks і подальший T-DXd контекст."
        ),
        category="solid",
        label_en="Gastric/GEJ - HER2 amplification - IHC/ISH actionability",
        summary_en=(
            "Metastatic gastric/GEJ adenocarcinoma with HER2 IHC 3+. Shows how the "
            "actionability layer connects IHC/ISH evidence, 1L trastuzumab-based tracks, "
            "and later T-DXd context."
        ),
        patient={
            "patient_id": "SHOWCASE-GASTRIC-HER2-001",
            "comment": "Synthetic showcase case. Demonstrates BMA-HER2-AMP-GASTRIC and gastric-specific HER2 interpretation.",
            "disease": {"id": "DIS-GASTRIC"},
            "line_of_therapy": 1,
            "biomarkers": {
                "HER2": "amplification / overexpression",
                "BIO-HER2-SOLID": "amplification / overexpression",
                "PD-L1 CPS": 8,
                "MSI": "MSS",
                "CLDN18.2": "negative",
            },
            "demographics": {"age": 67, "sex": "male", "ecog": 1},
            "findings": {
                "stage": "IV",
                "stage_iv": True,
                "primary_site": "GEJ",
                "histology": "adenocarcinoma",
                "her2_status": "positive",
                "her2_ihc": "3+",
                "metastatic_sites": ["liver", "nodes"],
                "creatinine_clearance_ml_min": 78,
                "bilirubin_uln_x": 0.9,
                "absolute_neutrophil_count_k_ul": 3.0,
                "platelets_k_ul": 230,
                "hbsag": "negative",
                "anti_hbc_total": "negative",
                "hcv_status": "negative",
                "hiv_status": "negative",
            },
        },
    ),
    _case(
        case_id="showcase-prostate-brca2-germline-mcrpc",
        file="patient_showcase_prostate_brca2_germline_mcrpc.json",
        label_ua="mCRPC - germline BRCA2 - PARP/HRR context",
        summary_ua=(
            "Метастатичний castration-resistant prostate cancer з germline BRCA2 після NHA. "
            "Показує, як ESCAT IA actionability додає HRR/PARP контекст, включно з родинним "
            "каскадним тестуванням і відмінністю BRCA2 від ширшого HRD label."
        ),
        category="solid",
        label_en="mCRPC - germline BRCA2 - PARP/HRR context",
        summary_en=(
            "Metastatic castration-resistant prostate cancer with germline BRCA2 after NHA. "
            "Shows HRR/PARP actionability, family cascade testing context, and the distinction "
            "between BRCA2 and broader HRD labels."
        ),
        patient={
            "patient_id": "SHOWCASE-PROSTATE-BRCA2-001",
            "comment": "Synthetic showcase case. Demonstrates BMA-BRCA2-GERMLINE-PROSTATE with ESCAT IA PARP context.",
            "disease": {"id": "DIS-PROSTATE"},
            "disease_state": "mCRPC",
            "line_of_therapy": 2,
            "biomarkers": {
                "BRCA2": "BRCA2 germline pathogenic",
                "MSI": "MSS",
                "PSMA PET": "avid",
            },
            "demographics": {"age": 69, "sex": "male", "ecog": 1},
            "findings": {
                "stage": "IV",
                "stage_iv": True,
                "castration_resistant": True,
                "ECOG PS 0-2": True,
                "BRCA1 or BRCA2 somatic or germline pathogenic variant (or ATM, CDK12, PALB2, RAD51C/D, BRIP1, FANCA)": True,
                "No prior PARPi therapy (olaparib, rucaparib, niraparib)": True,
                "testosterone_ng_dL": 12,
                "metastatic_sites": ["bone", "lymph nodes"],
                "prior_lines": [
                    {
                        "line": 1,
                        "regimen": "ADT + abiraterone",
                        "duration_months": 16,
                        "best_response": "PSA90",
                        "outcome": "radiographic PD",
                    }
                ],
                "creatinine_clearance_ml_min": 74,
                "bilirubin_uln_x": 0.8,
                "absolute_neutrophil_count_k_ul": 2.9,
                "platelets_k_ul": 205,
                "hbsag": "negative",
                "anti_hbc_total": "negative",
                "hcv_status": "negative",
                "hiv_status": "negative",
            },
        },
    ),
    _case(
        case_id="showcase-endometrial-dmmr-msh2-1l",
        file="patient_showcase_endometrial_dmmr_msh2_1l.json",
        label_ua="Endometrial - dMMR/MSH2 - immunotherapy evidence",
        summary_ua=(
            "Поширений endometrial carcinoma з dMMR/MSI-H через втрату MSH2. Кейс показує "
            "tumor-specific і tissue-agnostic immunotherapy evidence в одному місці, не змішуючи "
            "його з неспецифічним MSI label."
        ),
        category="solid",
        label_en="Endometrial - dMMR/MSH2 - immunotherapy evidence",
        summary_en=(
            "Advanced endometrial carcinoma with dMMR/MSI-H from MSH2 loss. Shows tumor-specific "
            "and tissue-agnostic immunotherapy evidence together without flattening it into a "
            "generic MSI label."
        ),
        patient={
            "patient_id": "SHOWCASE-ENDOMETRIAL-DMMR-001",
            "comment": "Synthetic showcase case. Demonstrates BMA-MSH2-GERMLINE-ENDOMETRIAL and dMMR immunotherapy evidence.",
            "disease": {"id": "DIS-ENDOMETRIAL"},
            "line_of_therapy": 1,
            "biomarkers": {
                "MSH2": "germline loss-of-function",
                "BIO-DMMR-IHC": "MSH2 germline loss-of-function (dMMR / MSI-H)",
                "MSI": "MSI-H",
                "POLE": "wildtype",
                "TP53": "wildtype pattern",
            },
            "demographics": {"age": 62, "sex": "female", "ecog": 1},
            "findings": {
                "stage": "IVB",
                "stage_iv": True,
                "histology": "endometrioid adenocarcinoma",
                "grade": 3,
                "metastatic_sites": ["peritoneum", "nodes"],
                "creatinine_clearance_ml_min": 84,
                "bilirubin_uln_x": 0.7,
                "absolute_neutrophil_count_k_ul": 3.4,
                "platelets_k_ul": 250,
                "hbsag": "negative",
                "anti_hbc_total": "negative",
                "hcv_status": "negative",
                "hiv_status": "negative",
            },
        },
    ),
    _case(
        case_id="showcase-thyroid-ret-fusion-rai-refractory",
        file="patient_showcase_thyroid_ret_fusion_rai_refractory.json",
        label_ua="Papillary thyroid - RET fusion - RAI-refractory target",
        summary_ua=(
            "RAI-refractory papillary thyroid carcinoma з RET fusion. Показує, як actionability "
            "відрізняє RET fusion у PTC від RET mutations у MTC і підсвічує selective RET-TKI."
        ),
        category="solid",
        label_en="Papillary thyroid - RET fusion - RAI-refractory target",
        summary_en=(
            "RAI-refractory papillary thyroid carcinoma with RET fusion. Shows how actionability "
            "separates RET fusion in PTC from RET mutations in MTC and highlights selective RET-TKI context."
        ),
        patient={
            "patient_id": "SHOWCASE-THYROID-RET-001",
            "comment": "Synthetic showcase case. Demonstrates BMA-RET-FUSION-THYROID-PAPILLARY and disease-specific RET interpretation.",
            "disease": {"id": "DIS-THYROID-PAPILLARY"},
            "line_of_therapy": 1,
            "biomarkers": {
                "RET": "fusion",
                "BIO-RET": "fusion",
                "BRAF": "wildtype",
                "NTRK": "negative",
            },
            "demographics": {"age": 51, "sex": "female", "ecog": 1},
            "findings": {
                "stage": "IV",
                "stage_iv": True,
                "histology": "papillary thyroid carcinoma",
                "radioiodine_refractory": True,
                "metastatic_sites": ["lung", "bone"],
                "prior_lines": [
                    {
                        "line": 1,
                        "regimen": "radioiodine + TSH suppression",
                        "outcome": "RAI-refractory progression",
                    }
                ],
                "creatinine_clearance_ml_min": 90,
                "bilirubin_uln_x": 0.8,
                "absolute_neutrophil_count_k_ul": 3.1,
                "platelets_k_ul": 240,
                "hbsag": "negative",
                "anti_hbc_total": "negative",
                "hcv_status": "negative",
                "hiv_status": "negative",
            },
        },
    ),
    _case(
        case_id="showcase-gist-kit-exon11-1l",
        file="patient_showcase_gist_kit_exon11_1l.json",
        label_ua="GIST - KIT exon 11 - genotype sets TKI dose",
        summary_ua=(
            "Метастатичний GIST з KIT exon 11 deletion. Кейс показує практичну перевагу "
            "структурованого biomarker layer: exon 11 підтримує стандартну 1L imatinib дозу, "
            "а не змішується з exon 9 чи PDGFRA D842V сценаріями."
        ),
        category="solid",
        label_en="GIST - KIT exon 11 - genotype sets TKI dose",
        summary_en=(
            "Metastatic GIST with KIT exon 11 deletion. Shows why structured biomarker context "
            "matters: exon 11 supports standard 1L imatinib dosing and should not be mixed with "
            "exon 9 or PDGFRA D842V scenarios."
        ),
        patient={
            "patient_id": "SHOWCASE-GIST-KIT11-001",
            "comment": "Synthetic showcase case. Demonstrates BMA-KIT-EXON11-GIST and genotype-specific TKI context.",
            "disease": {"id": "DIS-GIST"},
            "line_of_therapy": 1,
            "biomarkers": {
                "KIT": "exon 11 deletion",
                "BIO-KIT": "exon 11 deletion",
                "PDGFRA": "wildtype",
                "SDH": "retained",
            },
            "demographics": {"age": 58, "sex": "male", "ecog": 0},
            "findings": {
                "stage": "IV",
                "stage_iv": True,
                "primary_site": "stomach",
                "metastatic_sites": ["liver", "peritoneum"],
                "tumor_size_cm": 9.4,
                "mitoses_per_50_hpf": 8,
                "creatinine_clearance_ml_min": 94,
                "bilirubin_uln_x": 0.9,
                "absolute_neutrophil_count_k_ul": 3.5,
                "platelets_k_ul": 260,
                "hbsag": "negative",
                "anti_hbc_total": "negative",
                "hcv_status": "negative",
                "hiv_status": "negative",
            },
        },
    ),
    _case(
        case_id="showcase-aml-flt3-itd-1l",
        file="patient_showcase_aml_flt3_itd_1l.json",
        label_ua="AML - FLT3-ITD - heme actionability and risk",
        summary_ua=(
            "Новодіагностований fit AML з FLT3-ITD. Додає hematology приклад: BMA evidence "
            "пояснює targeted induction context, а ризик і transplant discussion лишаються окремими "
            "клінічними рішеннями."
        ),
        category="hematology",
        label_en="AML - FLT3-ITD - heme actionability and risk",
        summary_en=(
            "Newly diagnosed fit AML with FLT3-ITD. Adds a hematology example: BMA evidence "
            "explains targeted induction context while risk and transplant discussion remain "
            "separate clinical decisions."
        ),
        patient={
            "patient_id": "SHOWCASE-AML-FLT3-001",
            "comment": "Synthetic showcase case. Demonstrates BMA-FLT3-ITD-AML with CIViC and ELN-context rendering.",
            "disease": {"id": "DIS-AML"},
            "line_of_therapy": 1,
            "biomarkers": {
                "FLT3": "internal tandem duplication",
                "BIO-FLT3-ITD": "internal tandem duplication",
                "NPM1": "wildtype",
                "IDH1": "wildtype",
                "TP53": "wildtype",
            },
            "demographics": {"age": 52, "sex": "female", "ecog": 1},
            "findings": {
                "newly_diagnosed": True,
                "fit_for_intensive_induction": True,
                "bone_marrow_blasts_percent": 68,
                "wbc_k_ul": 42,
                "hemoglobin_g_dl": 8.9,
                "platelets_k_ul": 42,
                "creatinine_clearance_ml_min": 88,
                "bilirubin_uln_x": 0.8,
                "absolute_neutrophil_count_k_ul": 0.7,
                "hbsag": "negative",
                "anti_hbc_total": "negative",
                "hcv_status": "negative",
                "hiv_status": "negative",
            },
        },
    ),
]


def _json_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _render_case_entry(case: dict) -> str:
    return f"""    CaseEntry(
        case_id={_json_string(case["case_id"])},
        file={_json_string(case["file"])},
        label_ua={_json_string(case["label_ua"])},
        summary_ua={_json_string(case["summary_ua"])},
        badge={_json_string(case["badge"])},
        badge_class={_json_string(case["badge_class"])},
        category={_json_string(case["category"])},
        label_en={_json_string(case["label_en"])},
        summary_en={_json_string(case["summary_en"])},
    ),"""


def _patch_site_cases(entries: list[str]) -> None:
    text = SITE_CASES.read_text(encoding="utf-8")
    block = _SHOWCASE_BLOCK_BEGIN + "\n" + "\n".join(entries) + "\n" + _SHOWCASE_BLOCK_END

    if _SHOWCASE_BLOCK_BEGIN in text and _SHOWCASE_BLOCK_END in text:
        start = text.index(_SHOWCASE_BLOCK_BEGIN)
        end = text.index(_SHOWCASE_BLOCK_END) + len(_SHOWCASE_BLOCK_END)
        new = text[:start] + block + text[end:]
    else:
        marker = "CASES: list[CaseEntry] = [\n"
        pos = text.find(marker)
        if pos < 0:
            raise RuntimeError("Could not find CASES list in scripts/site_cases.py")
        insert_at = pos + len(marker)
        new = text[:insert_at] + block + "\n" + text[insert_at:]

    SITE_CASES.write_text(new, encoding="utf-8")


def _patch_featured_ids() -> None:
    text = SITE_CASES.read_text(encoding="utf-8")
    marker = "GALLERY_FEATURED_CASE_IDS: set[str] = {\n"
    start = text.find(marker)
    if start < 0:
        raise RuntimeError("Could not find GALLERY_FEATURED_CASE_IDS in scripts/site_cases.py")

    body_start = start + len(marker)
    end = text.find("}\n", body_start)
    if end < 0:
        raise RuntimeError("Could not find end of GALLERY_FEATURED_CASE_IDS")

    featured = (
        marker
        + "    # Public gallery is intentionally small: these curated cases demonstrate\n"
        + "    # the CIViC/ESCAT actionability layer better than hundreds of auto\n"
        + "    # stubs. The full CASES list still feeds try.html examples.json.\n"
        + "".join(f"    {_json_string(case_id)},\n" for case_id in SHOWCASE_IDS)
        + "}"
    )
    SITE_CASES.write_text(text[:start] + featured + text[end + 1 :], encoding="utf-8")


def main() -> int:
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    for case in SHOWCASE_CASES:
        path = EXAMPLES_DIR / case["file"]
        path.write_text(
            json.dumps(case["patient"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {path.relative_to(REPO_ROOT)}")

    _patch_site_cases([_render_case_entry(case) for case in SHOWCASE_CASES])
    _patch_featured_ids()
    print(f"patched {SITE_CASES.relative_to(REPO_ROOT)} with {len(SHOWCASE_CASES)} showcase cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
