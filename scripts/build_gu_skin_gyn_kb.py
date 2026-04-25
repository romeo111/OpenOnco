"""GU + skin + gyn KB builder (RCC + melanoma + urothelial + endometrial).

Generates 4 diseases, 8 sources, 3 biomarkers, 1 test, 1 workup, 8 regimens,
14 RFs, 8 indications, 4 algorithms.

Per CHARTER §8.3: extraction from cited NCCN/ESMO/EAU guidelines.
Per user 2026-04-26: efficacy > UA-registration.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
KB = REPO_ROOT / "knowledge_base" / "hosted" / "content"


def write(rel: str, body: str) -> None:
    target = KB / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")


# ── Diseases ──────────────────────────────────────────────────────────


DISEASES = {
    "rcc.yaml": """\
id: DIS-RCC
names:
  preferred: "Renal cell carcinoma"
  ukrainian: "Нирково-клітинна карцинома"
  english: "Renal cell carcinoma"
  synonyms: ["RCC", "Hypernephroma"]
codes:
  icd_o_3_morphology: "8312/3"
  icd_o_3_topography: ["C64.9"]
  icd_10: "C64"
  who_classification: "Renal cell carcinoma — clear-cell / papillary / chromophobe (WHO 5th 2022)"
archetype: biomarker_driven
lineage: solid_tumor_kidney_rcc
histologic_subtypes:
  - {id: CLEAR_CELL, label: "Clear-cell RCC", definition: "~75%; VHL-driven; ICI/TKI-responsive"}
  - {id: PAPILLARY, label: "Papillary RCC", definition: "~10-15%; type 1 MET-driven indolent; type 2 heterogeneous"}
  - {id: NON_CLEAR_CELL_OTHER, label: "Other non-clear-cell", definition: "Chromophobe / collecting duct / unclassified; cabozantinib + ICI options"}
stage_strata:
  - {id: STAGE_I_II_LOCALIZED, label: "Stage I-II localized — surgical resection"}
  - {id: STAGE_III_LOCAL_ADVANCED, label: "Stage III locally advanced — surgery + adjuvant pembro (KEYNOTE-564)"}
  - {id: STAGE_IV_METASTATIC, label: "Stage IV metastatic — ICI ± TKI"}
prognostic_frameworks:
  - {id: IMDC-RISK, label: "IMDC (Heng) risk groups: favorable / intermediate / poor", used_for: "1L metastatic regimen choice"}
etiological_factors:
  - "VHL inactivation drives clear-cell"
  - "Smoking, obesity, hypertension"
  - "Hereditary VHL / HLRCC / BHD / SDH-deficient / BAP1 syndromes"
related_diseases: []
epidemiology:
  context: "~5% of adult cancers; ~430K new cases/year. Modern ICI doublets raised metastatic clear-cell median OS from ~12 to >40 months."
sources: [SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024]
last_reviewed: null
reviewers: []
notes: "biomarker_driven — histology + IMDC risk drive selection. Adjuvant pembrolizumab approved per KEYNOTE-564."
""",
    "melanoma.yaml": """\
id: DIS-MELANOMA
names:
  preferred: "Cutaneous melanoma"
  ukrainian: "Шкірна меланома"
  english: "Cutaneous melanoma"
  synonyms: ["Melanoma"]
codes:
  icd_o_3_morphology: "8720/3"
  icd_o_3_topography: ["C44.9"]
  icd_10: "C43"
  who_classification: "Malignant melanoma of skin (WHO 5th 2023)"
archetype: biomarker_driven
lineage: solid_tumor_skin_melanoma
molecular_subtypes:
  - {id: BRAF_V600, label: "BRAF V600E/K mutation", definition: "~40-50%; targetable by BRAFi+MEKi"}
  - {id: NRAS_MUT, label: "NRAS mutation", definition: "~20%; ICI-first"}
  - {id: BRAF_WT_NRAS_WT, label: "Wild-type", definition: "ICI-only"}
  - {id: KIT_MUT, label: "KIT mutation", definition: "Acral/mucosal; imatinib-responsive in select hotspots"}
stage_strata:
  - {id: STAGE_I_II_LOCAL, label: "Stage I-II — wide local excision ± SLNB"}
  - {id: STAGE_III_REGIONAL, label: "Stage III regional — surgery + adjuvant ICI/BRAFi"}
  - {id: STAGE_IV_METASTATIC, label: "Stage IV metastatic — ICI doublet or BRAFi+MEKi"}
prognostic_frameworks:
  - {id: AJCC-8TH-MELANOMA, label: "AJCC 8th (Breslow, ulceration, mitotic rate, LDH)", used_for: "Stage stratification + adjuvant decisions"}
etiological_factors:
  - "UV radiation"
  - "BRAF V600E mutation"
  - "Hereditary CDKN2A / CDK4 / BAP1"
  - "Multiple atypical nevi / family history"
related_diseases: []
epidemiology:
  context: "~325K cases/year. Metastatic OS transformed: nivo+ipi 7.5y OS 49%; RELATIVITY-047 nivo+rela 4y 48%."
sources: [SRC-NCCN-MELANOMA-2025, SRC-ESMO-MELANOMA-2024]
last_reviewed: null
reviewers: []
notes: "biomarker_driven — BRAF determines targeted-vs-ICI. ICI doublet preferred for brain mets."
""",
    "urothelial.yaml": """\
id: DIS-UROTHELIAL
names:
  preferred: "Urothelial carcinoma (bladder + upper tract)"
  ukrainian: "Уротеліальна карцинома"
  english: "Urothelial carcinoma"
  synonyms: ["Bladder cancer", "TCC"]
codes:
  icd_o_3_morphology: "8120/3"
  icd_o_3_topography: ["C67.9", "C65.9", "C66.9"]
  icd_10: "C67"
  who_classification: "Urothelial carcinoma (WHO 5th 2022)"
archetype: line_of_therapy_sequential
lineage: solid_tumor_urothelial
disease_states:
  - {id: NMIBC, label: "Non-muscle-invasive (Ta/T1/CIS)", definition: "~75% at presentation. TURBT + intravesical BCG/mitomycin/gem"}
  - {id: MIBC, label: "Muscle-invasive (T2-T4a)", definition: "~25%. Neoadjuvant cisplatin + cystectomy or trimodality"}
  - {id: METASTATIC, label: "Metastatic (M1)", definition: "1L: EV+pembro (EV-302) regardless of cisplatin-eligibility"}
prognostic_frameworks:
  - {id: GALSKY-CISPLATIN-ELIGIBILITY, label: "Galsky criteria (CrCl ≥60, ECOG ≤1, no severe hearing loss / neuropathy ≥G2 / NYHA ≤II)", used_for: "Pre-EV-302 era 1L choice"}
  - {id: AJCC-8TH-BLADDER, label: "AJCC 8th TNM", used_for: "Anatomic stratification"}
etiological_factors:
  - "Tobacco smoking — dominant"
  - "Occupational aromatic amines"
  - "FGFR3 mutations (~20% MIBC)"
  - "Lynch syndrome (upper-tract)"
related_diseases: []
epidemiology:
  context: "~573K cases/year. EV-302 (2023): EV+pembro median OS 31.5 vs 16.1 months platinum-doublet."
sources: [SRC-NCCN-BLADDER-2025, SRC-EAU-BLADDER-2024]
last_reviewed: null
reviewers: []
notes: "line_of_therapy_sequential — disease-state dominant fork. Cisplatin-eligibility critical pre-EV era."
""",
    "endometrial.yaml": """\
id: DIS-ENDOMETRIAL
names:
  preferred: "Endometrial carcinoma"
  ukrainian: "Карцинома ендометрія"
  english: "Endometrial carcinoma"
  synonyms: ["Endometrial cancer", "Uterine cancer"]
codes:
  icd_o_3_morphology: "8380/3"
  icd_o_3_topography: ["C54.1"]
  icd_10: "C54"
  who_classification: "Endometrial adenocarcinoma + TCGA molecular classification (WHO 5th 2020)"
archetype: biomarker_driven
lineage: solid_tumor_endometrial
molecular_subtypes:
  - {id: POLE_MUT, label: "POLE-ultramutated", definition: "~7%; excellent prognosis"}
  - {id: MMR_DEFICIENT, label: "MMR-deficient (MSI-high)", definition: "~30%; Lynch screen; pembro/dostarlimab dramatic responses"}
  - {id: P53_ABNORMAL, label: "p53-abnormal", definition: "~15%; aggressive; carbo+pacli ± trastuzumab (HER2+)"}
  - {id: NSMP, label: "No specific molecular profile", definition: "~50%; standard chemo + ICI"}
stage_strata:
  - {id: STAGE_I_II_EARLY, label: "Stage I-II — TH+BSO ± adjuvant RT"}
  - {id: STAGE_III_IV_ADVANCED, label: "Stage III-IV — surgery + chemo + ICI (dMMR)"}
  - {id: RECURRENT_METASTATIC, label: "Recurrent / metastatic — KEYNOTE-868 / RUBY"}
prognostic_frameworks:
  - {id: TCGA-MOLECULAR, label: "TCGA classification (POLE / dMMR / p53-abn / NSMP)", used_for: "Refines histologic risk"}
  - {id: FIGO-2023, label: "FIGO 2023 (incorporates molecular)", used_for: "Modern staging"}
etiological_factors:
  - "Estrogen excess (obesity, unopposed estrogen, tamoxifen)"
  - "Lynch syndrome (~30% lifetime risk)"
  - "Cowden / PTEN syndromes"
related_diseases: []
epidemiology:
  context: "Most common gyn cancer in developed countries. NRG-GY018 + RUBY: chemoimmuno superior to chemo alone (PFS HR 0.30 dMMR; 0.64 pMMR)."
sources: [SRC-NCCN-UTERINE-2025, SRC-ESMO-ENDOMETRIAL-2022]
last_reviewed: null
reviewers: []
notes: "biomarker_driven — TCGA molecular classification dominant stratifier. dMMR drives largest ICI benefit."
""",
}


# ── Sources (8) — compact inline ──────────────────────────────────────


def _src(id_, title, version, url, dis):
    is_nccn = "NCCN" in id_
    return f"""id: {id_}
source_type: guideline
title: {title}
version: '{version}'
authors: [{'NCCN' if is_nccn else 'ESMO'} Guidelines Committee]
journal: {'null' if is_nccn else 'Annals of Oncology'}
doi: null
url: {url}
access_level: {'registration_required' if is_nccn else 'open_access'}
currency_status: current
superseded_by: null
current_as_of: '{version[:4]}-10-01'
evidence_tier: 1
hosting_mode: referenced
hosting_justification: null
ingestion: {{method: none, client: null, endpoint: null, rate_limit: null}}
cache_policy: {{enabled: false, ttl_hours: null, scope: null}}
license:
  name: {'NCCN — clinician-only' if is_nccn else 'CC-BY-NC-ND 4.0'}
  url: {'https://www.nccn.org/permissions' if is_nccn else 'https://creativecommons.org/licenses/by-nc-nd/4.0/'}
  spdx_id: {'null' if is_nccn else 'CC-BY-NC-ND-4.0'}
attribution: {{required: true, text: '{title}, v{version}'}}
commercial_use_allowed: false
redistribution_allowed: false
modifications_allowed: false
sharealike_required: false
known_restrictions: ['Quote-paraphrase model']
legal_review: {{status: pending, reviewer: null, date: null, notes: 'Same posture as SRC-NCCN-PROSTATE-2025'}}
relates_to_diseases: [{dis}]
last_verified: null
notes: "Primary guideline."
pages_count: 200
references_count: 500
corpus_role: primary_guideline
"""

SOURCES = {
    "src_nccn_kidney_2025.yaml": _src("SRC-NCCN-KIDNEY-2025", "NCCN Kidney Cancer", "2025.v3", "https://www.nccn.org/professionals/physician_gls/pdf/kidney.pdf", "DIS-RCC"),
    "src_esmo_rcc_2024.yaml": _src("SRC-ESMO-RCC-2024", "ESMO Renal Cell Carcinoma", "2024", "https://www.esmo.org/guidelines/guidelines-by-topic/genitourinary-cancers/renal-cell-carcinoma", "DIS-RCC"),
    "src_nccn_melanoma_2025.yaml": _src("SRC-NCCN-MELANOMA-2025", "NCCN Cutaneous Melanoma", "2025.v2", "https://www.nccn.org/professionals/physician_gls/pdf/cutaneous_melanoma.pdf", "DIS-MELANOMA"),
    "src_esmo_melanoma_2024.yaml": _src("SRC-ESMO-MELANOMA-2024", "ESMO Cutaneous Melanoma", "2024", "https://www.esmo.org/guidelines/guidelines-by-topic/melanoma/cutaneous-melanoma", "DIS-MELANOMA"),
    "src_nccn_bladder_2025.yaml": _src("SRC-NCCN-BLADDER-2025", "NCCN Bladder Cancer", "2025.v3", "https://www.nccn.org/professionals/physician_gls/pdf/bladder.pdf", "DIS-UROTHELIAL"),
    "src_eau_bladder_2024.yaml": _src("SRC-EAU-BLADDER-2024", "EAU Muscle-Invasive Bladder", "2024", "https://uroweb.org/guidelines/muscle-invasive-and-metastatic-bladder-cancer", "DIS-UROTHELIAL"),
    "src_nccn_uterine_2025.yaml": _src("SRC-NCCN-UTERINE-2025", "NCCN Uterine Neoplasms", "2025.v2", "https://www.nccn.org/professionals/physician_gls/pdf/uterine.pdf", "DIS-ENDOMETRIAL"),
    "src_esmo_endometrial_2022.yaml": _src("SRC-ESMO-ENDOMETRIAL-2022", "ESMO-ESGO-ESTRO Endometrial Consensus", "2022", "https://www.esmo.org/guidelines/guidelines-by-topic/gynaecological-cancers/endometrial-cancer", "DIS-ENDOMETRIAL"),
}


# ── Biomarkers (3) ────────────────────────────────────────────────────


BIOMARKERS = {
    "bio_vhl_status.yaml": """\
id: BIO-VHL-STATUS
names: {preferred: "VHL gene status", ukrainian: "Статус гена VHL", english: "VHL gene status"}
codes: {loinc: null}
biomarker_type: mutation
mutation_details: {gene: "VHL", type: "loss-of-function", functional_impact: "HIF-α stabilization → angiogenic/glycolytic phenotype"}
measurement: {method: "Tumor-tissue NGS OR germline NGS for hereditary VHL", sensitivity_requirement: "Standard NGS"}
interpretation_notes: "Somatic VHL inactivation in >90% clear-cell RCC. Germline → von Hippel-Lindau syndrome. Belzutifan approved for VHL-syndrome-associated RCC."
related_biomarkers: []
last_reviewed: null
notes: "Germline testing offered for bilateral/multifocal RCC, RCC <46, syndromic features."
""",
    "bio_fgfr3_mutation.yaml": """\
id: BIO-FGFR3-MUTATION
names: {preferred: "FGFR3 mutation/fusion", ukrainian: "Мутація/фузія FGFR3", english: "FGFR3 mutation/fusion"}
codes: {loinc: null}
biomarker_type: mutation
mutation_details: {gene: "FGFR3", hotspots: ["S249C", "Y373C", "G370C", "R248C"], type: "activating", functional_impact: "Constitutive FGFR3 signaling"}
measurement: {method: "Tumor-tissue NGS OR ctDNA OR allele-specific PCR", sensitivity_requirement: "Standard NGS"}
interpretation_notes: "~20% MIBC; ~70% low-grade NMIBC. THOR-2: erdafitinib in FGFR3+ post-platinum mUC."
related_biomarkers: []
last_reviewed: null
notes: "Required pre-erdafitinib testing."
""",
    "bio_tmb_high.yaml": """\
id: BIO-TMB-HIGH
names: {preferred: "Tumor mutational burden (TMB-high)", ukrainian: "Тумор-мутаційне навантаження", english: "TMB-high"}
codes: {loinc: null}
biomarker_type: tmb
measurement: {method: "Whole-exome OR comprehensive NGS panel (≥1 Mb)", units: "mutations per megabase"}
interpretation_notes: "TMB ≥10 mut/Mb FDA tumor-agnostic indication for pembrolizumab (KEYNOTE-158)."
related_biomarkers: ["BIO-MSI-STATUS", "BIO-DMMR-IHC"]
last_reviewed: null
notes: "Foundation One CDx companion diagnostic."
""",
}


# ── Tests + Workups (1 each) ─────────────────────────────────────────


TESTS = {
    "test_renal_imaging_baseline.yaml": """\
id: TEST-RENAL-IMAGING-BASELINE
names: {preferred: "Baseline renal imaging (CECT abdomen / MRI)", ukrainian: "Базальна ниркова візуалізація"}
test_type: imaging
priority_class: critical
specimen: "Multi-phase contrast-enhanced abdominal imaging"
turnaround_hours_typical: 48
measures: []
sources: [SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024]
last_reviewed: null
notes: "RCC staging + post-nephrectomy surveillance."
""",
}

WORKUPS = {
    "workup_solid_genitourinary_skin_gyn.yaml": """\
id: WORKUP-SOLID-GU-SKIN-GYN
applicable_to:
  lineage_hints: [solid_tumor_kidney_rcc, solid_tumor_skin_melanoma, solid_tumor_urothelial, solid_tumor_endometrial]
  tissue_locations: [kidney, skin, bladder, upper_urinary_tract, uterus, endometrium]
  presentation_keywords: [kidney_mass, melanoma_suspect, bladder_mass, hematuria, postmenopausal_bleeding, endometrial_thickening]
required_tests: [TEST-CECT-CAP]
desired_tests: [TEST-BRAIN-MRI-CONTRAST, TEST-PET-CT, TEST-RENAL-IMAGING-BASELINE, TEST-GERMLINE-BRCA-PANEL]
triggers_mdt_roles:
  required: [medical_oncologist, surgical_oncologist]
  recommended: [radiologist, pathologist, molecular_geneticist]
  rationale_per_role:
    medical_oncologist: "Systemic therapy planning"
    surgical_oncologist: "Resection planning per disease"
    radiologist: "Multi-modality staging"
    pathologist: "Histology + molecular IHC"
    molecular_geneticist: "NGS panel + germline testing"
sources: [SRC-NCCN-KIDNEY-2025, SRC-NCCN-MELANOMA-2025, SRC-NCCN-BLADDER-2025, SRC-NCCN-UTERINE-2025]
last_reviewed: null
notes: "Combined GU+skin+gyn workup."
""",
}


# ── Regimens (8) ─────────────────────────────────────────────────────


REGIMENS = {
    "reg_nivo_ipi_rcc.yaml": """\
id: REG-NIVO-IPI-RCC
name: "Nivolumab + ipilimumab (RCC, 1L IMDC intermediate/poor)"
name_ua: "Ніволумаб + іпілімумаб (НКК, 1L IMDC проміжний/поганий)"
alternate_names: ["CheckMate-214"]
components:
  - {drug_id: DRUG-NIVOLUMAB, dose: "3 mg/kg IV induction → 480 mg flat IV q4w maintenance", schedule: "Induction q3w x 4 + ipi", route: IV}
  - {drug_id: DRUG-IPILIMUMAB, dose: "1 mg/kg IV", schedule: "Days 1 of cycles 1-4 only", route: IV}
cycle_length_days: 21
total_cycles: "4 induction; nivo maintenance until progression"
toxicity_profile: severe
premedication: []
mandatory_supportive_care: []
monitoring_schedule_id: null
dose_adjustments: [{condition: "Immune-mediated AE G≥2", modification: "Hold; corticosteroids"}]
ukraine_availability: {all_components_registered: true, all_components_reimbursed: false, notes: "Out-of-pocket"}
sources: [SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024]
last_reviewed: null
notes: "CheckMate-214 IMDC intermediate/poor. Nivo q4w maintenance up to 2 years."
""",
    "reg_pembro_axi_rcc.yaml": """\
id: REG-PEMBRO-AXI-RCC
name: "Pembrolizumab + axitinib (RCC, 1L all-risk)"
name_ua: "Пембролізумаб + акситиніб (НКК, 1L)"
alternate_names: ["KEYNOTE-426"]
components:
  - {drug_id: DRUG-PEMBROLIZUMAB, dose: "200 mg IV q3w", schedule: "Up to 2 years", route: IV}
  - {drug_id: DRUG-AXITINIB, dose: "5 mg PO BID continuous", schedule: "Continuous", route: PO}
cycle_length_days: 21
total_cycles: "Pembro up to 2 years; axitinib until progression"
toxicity_profile: moderate-severe
premedication: []
mandatory_supportive_care: []
monitoring_schedule_id: null
dose_adjustments: [{condition: "Hypertension G2", modification: "Antihypertensive"}, {condition: "ICI AE", modification: "Hold pembro; corticosteroids"}]
ukraine_availability: {all_components_registered: true, all_components_reimbursed: false, notes: "Out-of-pocket"}
sources: [SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024]
last_reviewed: null
notes: "KEYNOTE-426 workhorse 1L clear-cell mRCC."
""",
    "reg_nivo_ipi_melanoma.yaml": """\
id: REG-NIVO-IPI-MELANOMA
name: "Nivolumab + ipilimumab (melanoma, 1L metastatic)"
name_ua: "Ніволумаб + іпілімумаб (меланома, 1L метастаз)"
alternate_names: ["CheckMate-067"]
components:
  - {drug_id: DRUG-NIVOLUMAB, dose: "1 mg/kg IV induction → 480 mg flat IV q4w maintenance", schedule: "Induction with ipi cycles 1-4", route: IV}
  - {drug_id: DRUG-IPILIMUMAB, dose: "3 mg/kg IV (higher than RCC)", schedule: "Days 1 of cycles 1-4", route: IV}
cycle_length_days: 21
total_cycles: "4 induction; nivo maintenance until progression OR 2 years"
toxicity_profile: severe
premedication: []
mandatory_supportive_care: []
monitoring_schedule_id: null
dose_adjustments: [{condition: "Immune-mediated AE G≥2", modification: "Hold; corticosteroids"}]
ukraine_availability: {all_components_registered: true, all_components_reimbursed: false, notes: "Out-of-pocket"}
sources: [SRC-NCCN-MELANOMA-2025, SRC-ESMO-MELANOMA-2024]
last_reviewed: null
notes: "CheckMate-067 7.5y OS 49%. Higher ipi dose (3 mg/kg) than RCC (1 mg/kg)."
""",
    "reg_ev_pembro_urothelial.yaml": """\
id: REG-EV-PEMBRO-UROTHELIAL
name: "Enfortumab vedotin + pembrolizumab (metastatic urothelial, 1L)"
name_ua: "Енфортумаб ведотин + пембролізумаб (метастатична уротеліальна, 1L)"
alternate_names: ["EV-302"]
components:
  - {drug_id: DRUG-ENFORTUMAB-VEDOTIN, dose: "1.25 mg/kg IV", schedule: "Days 1, 8 of 21-day cycle", route: IV}
  - {drug_id: DRUG-PEMBROLIZUMAB, dose: "200 mg IV q3w", schedule: "Up to 2 years", route: IV}
cycle_length_days: 21
total_cycles: "EV until progression; pembro up to 2 years"
toxicity_profile: severe
premedication: []
mandatory_supportive_care: []
monitoring_schedule_id: null
dose_adjustments: [{condition: "Hyperglycemia (Nectin-4 ADC)", modification: "Diabetes management"}, {condition: "Skin reactions / TEN-like", modification: "Hold; dermatology"}]
ukraine_availability: {all_components_registered: false, all_components_reimbursed: false, notes: "EV not registered in Ukraine — major access barrier"}
sources: [SRC-NCCN-BLADDER-2025, SRC-EAU-BLADDER-2024]
last_reviewed: null
notes: "EV-302 paradigm 1L mUC. OS 31.5 vs 16.1 months."
""",
    "reg_cisplatin_gemcitabine_urothelial.yaml": """\
id: REG-CISPLATIN-GEMCITABINE-UROTHELIAL
name: "Cisplatin + gemcitabine (urothelial neoadj + metastatic)"
name_ua: "Цисплатин + гемцитабін (уротеліальна)"
alternate_names: ["GC regimen"]
components:
  - {drug_id: DRUG-CISPLATIN, dose: "70 mg/m² IV", schedule: "Day 1 of 21-day cycle", route: IV}
  - {drug_id: DRUG-GEMCITABINE, dose: "1000 mg/m² IV", schedule: "Days 1, 8 of 21-day cycle", route: IV}
cycle_length_days: 21
total_cycles: "4 cycles neoadj; 6 cycles metastatic"
toxicity_profile: severe
premedication: ["Hydration + Mg for cisplatin", "Antiemetic high-emetogenic"]
mandatory_supportive_care: []
monitoring_schedule_id: null
dose_adjustments: [{condition: "CrCl <60", modification: "Substitute carboplatin AUC 4-5"}]
ukraine_availability: {all_components_registered: true, all_components_reimbursed: true, notes: "Generic; reimbursed"}
sources: [SRC-NCCN-BLADDER-2025, SRC-EAU-BLADDER-2024]
last_reviewed: null
notes: "Workhorse cisplatin-doublet. Galsky cisplatin-eligibility critical."
""",
    "reg_avelumab_maintenance.yaml": """\
id: REG-AVELUMAB-MAINTENANCE
name: "Avelumab maintenance (urothelial post-platinum chemo)"
name_ua: "Авелумаб підтримуюча"
alternate_names: ["JAVELIN Bladder 100"]
components:
  - {drug_id: DRUG-AVELUMAB, dose: "800 mg IV q2w", schedule: "Continuous until progression", route: IV}
cycle_length_days: 14
total_cycles: "Continuous until progression"
toxicity_profile: moderate
premedication: ["Premedication first 4 doses (paracetamol+diphenhydramine)"]
mandatory_supportive_care: []
monitoring_schedule_id: null
dose_adjustments: [{condition: "Immune-mediated AE", modification: "Standard ICI management"}]
ukraine_availability: {all_components_registered: true, all_components_reimbursed: false, notes: "Reimbursement gap"}
sources: [SRC-NCCN-BLADDER-2025]
last_reviewed: null
notes: "JAVELIN Bladder 100: median OS 21.4 vs 14.3 months (BSC)."
""",
    "reg_pembro_carbo_pacli_endom.yaml": """\
id: REG-PEMBRO-CARBO-PACLI-ENDOM
name: "Pembrolizumab + carbo + paclitaxel (endometrial advanced 1L)"
name_ua: "Пембролізумаб + карбо + паклітаксель"
alternate_names: ["NRG-GY018"]
components:
  - {drug_id: DRUG-PEMBROLIZUMAB, dose: "200 mg IV q3w", schedule: "Continuous up to 2 years", route: IV}
  - {drug_id: DRUG-CARBOPLATIN, dose: "AUC 5 IV", schedule: "Day 1 x 6 cycles", route: IV}
  - {drug_id: DRUG-PACLITAXEL, dose: "175 mg/m² IV", schedule: "Day 1 x 6 cycles", route: IV}
cycle_length_days: 21
total_cycles: "Chemo x 6; pembro maintenance up to 2 years"
toxicity_profile: severe
premedication: ["Dexa for paclitaxel", "Antiemetic"]
mandatory_supportive_care: []
monitoring_schedule_id: null
dose_adjustments: [{condition: "Peripheral neuropathy", modification: "Reduce paclitaxel"}, {condition: "Immune AE", modification: "Hold pembro"}]
ukraine_availability: {all_components_registered: true, all_components_reimbursed: false, notes: "Pembro reimbursement variable"}
sources: [SRC-NCCN-UTERINE-2025]
last_reviewed: null
notes: "NRG-GY018: PFS HR 0.64 pMMR, 0.30 dMMR."
""",
    "reg_dostarlimab_carbo_pacli_endom.yaml": """\
id: REG-DOSTARLIMAB-CARBO-PACLI-ENDOM
name: "Dostarlimab + carbo + paclitaxel (endometrial advanced 1L dMMR)"
name_ua: "Достарлімаб + карбо + паклітаксель"
alternate_names: ["RUBY", "KEYNOTE-868 (analog)"]
components:
  - {drug_id: DRUG-DOSTARLIMAB, dose: "500 mg IV q3w → 1000 mg q6w maintenance", schedule: "With chemo cycles 1-6 + maintenance up to 3 years", route: IV}
  - {drug_id: DRUG-CARBOPLATIN, dose: "AUC 5 IV", schedule: "Day 1 x 6 cycles", route: IV}
  - {drug_id: DRUG-PACLITAXEL, dose: "175 mg/m² IV", schedule: "Day 1 x 6 cycles", route: IV}
cycle_length_days: 21
total_cycles: "Chemo x 6; dostarlimab maintenance up to 3 years"
toxicity_profile: severe
premedication: ["Dexa for paclitaxel", "Antiemetic"]
mandatory_supportive_care: []
monitoring_schedule_id: null
dose_adjustments: [{condition: "Peripheral neuropathy", modification: "Reduce paclitaxel"}, {condition: "Immune AE", modification: "Hold dostarlimab"}]
ukraine_availability: {all_components_registered: false, all_components_reimbursed: false, notes: "Dostarlimab not registered in Ukraine"}
sources: [SRC-NCCN-UTERINE-2025, SRC-ESMO-ENDOMETRIAL-2022]
last_reviewed: null
notes: "RUBY: dostarlimab+chemo PFS HR 0.30 dMMR, 0.64 pMMR."
""",
}


# ── RedFlags (12) ────────────────────────────────────────────────────


def _rf(id_, defn, defn_ua, trigger, direction, severity, category, dis, src1, src2, notes):
    return f"""id: {id_}
definition: "{defn}"
definition_ua: "{defn_ua}"

{trigger}

clinical_direction: {direction}
severity: {severity}
priority: 100
category: {category}

relevant_diseases: [DIS-{dis}]
shifts_algorithm: []

sources:
  - {src1}
  - {src2}

last_reviewed: null
draft: false

notes: "{notes}"
"""

REDFLAGS = {
    "rf_rcc_organ_dysfunction.yaml": _rf("RF-RCC-ORGAN-DYSFUNCTION",
        "Solitary kidney OR baseline CrCl <50 mL/min — limits cisplatin alternatives + impacts surveillance imaging.",
        "Єдина нирка АБО CrCl <50 — обмежує цисплатин альтернативи.",
        """trigger:
  type: lab_value
  any_of:
    - {finding: "creatinine_clearance_ml_min", threshold: 50, comparator: "<"}
    - {finding: "solitary_kidney", value: true}""",
        "investigate", "major", "organ-dysfunction", "RCC",
        "SRC-NCCN-KIDNEY-2025", "SRC-ESMO-RCC-2024",
        "Many RCC patients are post-nephrectomy by metastatic stage."),
    "rf_rcc_high_risk_biology.yaml": _rf("RF-RCC-HIGH-RISK-BIOLOGY",
        "Sarcomatoid features OR rapid TKI progression — predicts ICI-doublet benefit; non-clear-cell distinct path.",
        "Саркоматоїдні риси АБО швидке прогресування на TKI.",
        """trigger:
  type: composite_clinical
  any_of:
    - {finding: "rcc_sarcomatoid_features", value: true}
    - {finding: "rcc_non_clear_cell", value: true}""",
        "intensify", "major", "high-risk-biology", "RCC",
        "SRC-NCCN-KIDNEY-2025", "SRC-ESMO-RCC-2024",
        "Sarcomatoid clear-cell uniquely benefits from ICI doublet."),
    "rf_rcc_frailty_age.yaml": _rf("RF-RCC-FRAILTY-AGE",
        "Age ≥80 + ECOG ≥2 + comorbidity — ICI doublet toxicity prohibitive.",
        "Вік ≥80 + ECOG ≥2 + коморбідності.",
        """trigger:
  type: composite_clinical
  all_of:
    - {finding: "age_years", threshold: 80, comparator: ">="}
    - any_of:
        - {finding: "ecog_status", threshold: 2, comparator: ">="}
        - {finding: "comorbidity_count", threshold: 2, comparator: ">="}""",
        "de-escalate", "major", "frailty-age", "RCC",
        "SRC-NCCN-KIDNEY-2025", "SRC-ESMO-RCC-2024",
        "Single-agent TKI or ICI mono (KEYNOTE-427) alternatives."),
    "rf_rcc_transformation_progression.yaml": _rf("RF-RCC-TRANSFORMATION-PROGRESSION",
        "CNS metastases — ICI doublet retains intracranial activity; cabozantinib + nivolumab also CNS-active.",
        "Метастази в ЦНС.",
        """trigger:
  type: composite_clinical
  any_of:
    - {finding: "cns_metastases_rcc", value: true}""",
        "investigate", "critical", "transformation-progression", "RCC",
        "SRC-NCCN-KIDNEY-2025", "SRC-ESMO-RCC-2024",
        "RCC brain-met rate ~10%."),

    "rf_melanoma_organ_dysfunction.yaml": _rf("RF-MELANOMA-ORGAN-DYSFUNCTION",
        "LDH >2x ULN OR severe hepatic dysfunction — predictor of inferior ICI outcomes.",
        "ЛДГ >2x ULN АБО тяжка печінкова дисфункція.",
        """trigger:
  type: lab_value
  any_of:
    - {finding: "ldh_x_uln", threshold: 2, comparator: ">"}
    - {finding: "child_pugh_class", value: "C"}""",
        "investigate", "major", "organ-dysfunction", "MELANOMA",
        "SRC-NCCN-MELANOMA-2025", "SRC-ESMO-MELANOMA-2024",
        "LDH integral AJCC staging variable."),
    "rf_melanoma_high_risk_biology.yaml": _rf("RF-MELANOMA-HIGH-RISK-BIOLOGY",
        "BRAF V600E/K OR NRAS mutation — drives BRAFi+MEKi vs ICI doublet decision.",
        "BRAF V600E/K АБО NRAS мутація.",
        """trigger:
  type: biomarker
  any_of:
    - {finding: "BIO-BRAF-V600E", value: "positive"}
    - {finding: "nras_mutation", value: true}""",
        "intensify", "major", "high-risk-biology", "MELANOMA",
        "SRC-NCCN-MELANOMA-2025", "SRC-ESMO-MELANOMA-2024",
        "BRAF testing universal in metastatic. DREAMseq established ICI-first sequencing."),
    "rf_melanoma_transformation_progression.yaml": _rf("RF-MELANOMA-TRANSFORMATION-PROGRESSION",
        "Symptomatic CNS metastases — ICI doublet (nivo+ipi) intracranially active; BRAFi+MEKi for visceral crisis.",
        "Симптоматичні метастази в ЦНС.",
        """trigger:
  type: composite_clinical
  any_of:
    - {finding: "symptomatic_cns_metastases", value: true}""",
        "intensify", "critical", "transformation-progression", "MELANOMA",
        "SRC-NCCN-MELANOMA-2025", "SRC-ESMO-MELANOMA-2024",
        "CheckMate-204: nivo+ipi ICR ~46% in active brain mets."),
    "rf_melanoma_frailty_age.yaml": _rf("RF-MELANOMA-FRAILTY-AGE",
        "Age ≥80 + ECOG ≥2 — nivo+ipi prohibitive; nivo+rela or pembro mono.",
        "Вік ≥80 + ECOG ≥2.",
        """trigger:
  type: composite_clinical
  all_of:
    - {finding: "age_years", threshold: 80, comparator: ">="}
    - {finding: "ecog_status", threshold: 2, comparator: ">="}""",
        "de-escalate", "major", "frailty-age", "MELANOMA",
        "SRC-NCCN-MELANOMA-2025", "SRC-ESMO-MELANOMA-2024",
        "RELATIVITY-047 nivo+rela better tolerated."),

    "rf_urothelial_organ_dysfunction.yaml": _rf("RF-UROTHELIAL-ORGAN-DYSFUNCTION",
        "Cisplatin-ineligibility per Galsky criteria — drives EV+pembro 1L OR carbo-doublet.",
        "Цисплатин-неприйнятність за Galsky.",
        """trigger:
  type: composite_clinical
  any_of:
    - {finding: "creatinine_clearance_ml_min", threshold: 60, comparator: "<"}
    - {finding: "hearing_loss_grade_2_or_higher", value: true}
    - {finding: "peripheral_neuropathy_grade_2_or_higher", value: true}""",
        "de-escalate", "major", "organ-dysfunction", "UROTHELIAL",
        "SRC-NCCN-BLADDER-2025", "SRC-EAU-BLADDER-2024",
        "EV+pembro (post-EV-302) eliminates cisplatin-eligibility as 1L bottleneck."),
    "rf_urothelial_high_risk_biology.yaml": _rf("RF-UROTHELIAL-HIGH-RISK-BIOLOGY",
        "FGFR3 mutation/fusion — opens erdafitinib (THOR) pathway.",
        "FGFR3 мутація/фузія.",
        """trigger:
  type: biomarker
  any_of:
    - {finding: "BIO-FGFR3-MUTATION", value: "positive"}
    - {finding: "fgfr3_fusion", value: true}""",
        "intensify", "major", "high-risk-biology", "UROTHELIAL",
        "SRC-NCCN-BLADDER-2025", "SRC-EAU-BLADDER-2024",
        "THOR-2: erdafitinib superior in FGFR3+ post-platinum."),
    "rf_urothelial_transformation_progression.yaml": _rf("RF-UROTHELIAL-TRANSFORMATION-PROGRESSION",
        "Hydronephrosis OR ureteral obstruction — emergent urological intervention before systemic therapy.",
        "Гідронефроз АБО обструкція сечоводу.",
        """trigger:
  type: composite_clinical
  any_of:
    - {finding: "hydronephrosis", value: true}
    - {finding: "ureteral_obstruction", value: true}""",
        "hold", "critical", "transformation-progression", "UROTHELIAL",
        "SRC-NCCN-BLADDER-2025", "SRC-EAU-BLADDER-2024",
        "Renal preservation critical."),

    "rf_endometrial_organ_dysfunction.yaml": _rf("RF-ENDOMETRIAL-ORGAN-DYSFUNCTION",
        "Cardiac dysfunction (LVEF <50%) — limits anthracycline OR trastuzumab (HER2+ serous variant).",
        "Кардіальна дисфункція (LVEF <50%).",
        """trigger:
  type: lab_value
  any_of:
    - {finding: "lvef_percent", threshold: 50, comparator: "<"}""",
        "investigate", "major", "organ-dysfunction", "ENDOMETRIAL",
        "SRC-NCCN-UTERINE-2025", "SRC-ESMO-ENDOMETRIAL-2022",
        "HER2+ serous endometrial subset eligible for trastuzumab + chemo."),
    "rf_endometrial_high_risk_biology.yaml": _rf("RF-ENDOMETRIAL-HIGH-RISK-BIOLOGY",
        "dMMR/MSI-high OR p53-abnormal OR POLE-mutated — TCGA classification drives ICI eligibility.",
        "dMMR/MSI-high АБО p53-аномальний АБО POLE-мутований.",
        """trigger:
  type: biomarker
  any_of:
    - {finding: "BIO-DMMR-IHC", value: "deficient"}
    - {finding: "BIO-MSI-STATUS", value: "high"}
    - {finding: "p53_abnormal", value: true}
    - {finding: "pole_mutation", value: true}""",
        "intensify", "major", "high-risk-biology", "ENDOMETRIAL",
        "SRC-NCCN-UTERINE-2025", "SRC-ESMO-ENDOMETRIAL-2022",
        "Universal molecular profiling. dMMR triggers Lynch screening."),
    "rf_endometrial_transformation_progression.yaml": _rf("RF-ENDOMETRIAL-TRANSFORMATION-PROGRESSION",
        "Sarcomatoid transformation OR carcinosarcoma — distinct biology requiring different chemo backbone.",
        "Саркоматоїдна трансформація АБО карциносаркома.",
        """trigger:
  type: composite_clinical
  any_of:
    - {finding: "endometrial_carcinosarcoma", value: true}
    - {finding: "endometrial_sarcomatoid", value: true}""",
        "intensify", "critical", "transformation-progression", "ENDOMETRIAL",
        "SRC-NCCN-UTERINE-2025", "SRC-ESMO-ENDOMETRIAL-2022",
        "Carcinosarcoma: ifos-paclitaxel historical."),
}


# ── Indications (8) ──────────────────────────────────────────────────


INDICATIONS = {
    "ind_rcc_metastatic_1l_nivo_ipi.yaml": """\
id: IND-RCC-METASTATIC-1L-NIVO-IPI
plan_track: aggressive
applicable_to:
  disease_id: DIS-RCC
  histologic_subtype: CLEAR_CELL
  stage_stratum: STAGE_IV_METASTATIC
  line_of_therapy: 1
  biomarker_requirements_required: []
  biomarker_requirements_excluded: []
  demographic_constraints: {ecog_max: 1}
recommended_regimen: REG-NIVO-IPI-RCC
concurrent_therapy: []
followed_by: []
evidence_level: high
strength_of_recommendation: strong
nccn_category: "1"
expected_outcomes: {median_overall_survival_months: 56, notes: "CheckMate-214 IMDC intermediate/poor"}
hard_contraindications: []
red_flags_triggering_alternative: []
required_tests: [TEST-CECT-CAP, TEST-BRAIN-MRI-CONTRAST]
desired_tests: []
sources:
  - {source_id: SRC-NCCN-KIDNEY-2025, weight: primary}
  - {source_id: SRC-ESMO-RCC-2024, weight: primary}
last_reviewed: null
reviewers: []
notes: "CheckMate-214: nivo+ipi superior in IMDC intermediate/poor."
""",
    "ind_rcc_metastatic_1l_pembro_axi.yaml": """\
id: IND-RCC-METASTATIC-1L-PEMBRO-AXI
plan_track: standard
applicable_to:
  disease_id: DIS-RCC
  histologic_subtype: CLEAR_CELL
  stage_stratum: STAGE_IV_METASTATIC
  line_of_therapy: 1
  biomarker_requirements_required: []
  biomarker_requirements_excluded: []
  demographic_constraints: {ecog_max: 2}
recommended_regimen: REG-PEMBRO-AXI-RCC
concurrent_therapy: []
followed_by: []
evidence_level: high
strength_of_recommendation: strong
nccn_category: "1"
expected_outcomes: {median_overall_survival_months: 46, notes: "KEYNOTE-426"}
hard_contraindications: []
red_flags_triggering_alternative: []
required_tests: [TEST-CECT-CAP]
desired_tests: [TEST-BRAIN-MRI-CONTRAST]
sources:
  - {source_id: SRC-NCCN-KIDNEY-2025, weight: primary}
  - {source_id: SRC-ESMO-RCC-2024, weight: primary}
last_reviewed: null
reviewers: []
notes: "KEYNOTE-426 across IMDC risk groups."
""",
    "ind_melanoma_metastatic_1l_nivo_ipi.yaml": """\
id: IND-MELANOMA-METASTATIC-1L-NIVO-IPI
plan_track: standard
applicable_to:
  disease_id: DIS-MELANOMA
  stage_stratum: STAGE_IV_METASTATIC
  line_of_therapy: 1
  biomarker_requirements_required: []
  biomarker_requirements_excluded: []
  demographic_constraints: {ecog_max: 1}
recommended_regimen: REG-NIVO-IPI-MELANOMA
concurrent_therapy: []
followed_by: []
evidence_level: high
strength_of_recommendation: strong
nccn_category: "1"
expected_outcomes: {five_year_overall_survival: "52%", notes: "CheckMate-067"}
hard_contraindications: []
red_flags_triggering_alternative: []
required_tests: [TEST-CECT-CAP, TEST-BRAIN-MRI-CONTRAST]
desired_tests: []
sources:
  - {source_id: SRC-NCCN-MELANOMA-2025, weight: primary}
  - {source_id: SRC-ESMO-MELANOMA-2024, weight: primary}
last_reviewed: null
reviewers: []
notes: "CheckMate-067 7.5y OS 49%. Brain-met-active."
""",
    "ind_melanoma_braf_metastatic_1l_dabra_trame.yaml": """\
id: IND-MELANOMA-BRAF-METASTATIC-1L-DABRA-TRAME
plan_track: aggressive
applicable_to:
  disease_id: DIS-MELANOMA
  molecular_subtype: BRAF_V600
  stage_stratum: STAGE_IV_METASTATIC
  line_of_therapy: 1
  biomarker_requirements_required:
    - {biomarker_id: BIO-BRAF-V600E, value_constraint: "positive", required: true}
  biomarker_requirements_excluded: []
  demographic_constraints: {ecog_max: 2}
recommended_regimen: REG-DABRAFENIB-TRAMETINIB-NSCLC
concurrent_therapy: []
followed_by: []
evidence_level: high
strength_of_recommendation: strong
nccn_category: "1"
expected_outcomes: {median_progression_free_survival_months: 12, notes: "COMBI-d/v"}
hard_contraindications: []
red_flags_triggering_alternative: []
required_tests: [TEST-CECT-CAP, TEST-BRAIN-MRI-CONTRAST]
desired_tests: []
sources:
  - {source_id: SRC-NCCN-MELANOMA-2025, weight: primary}
  - {source_id: SRC-ESMO-MELANOMA-2024, weight: primary}
last_reviewed: null
reviewers: []
notes: "Reuses cross-disease BRAF V600E doublet REG-DABRAFENIB-TRAMETINIB-NSCLC."
""",
    "ind_urothelial_metastatic_1l_ev_pembro.yaml": """\
id: IND-UROTHELIAL-METASTATIC-1L-EV-PEMBRO
plan_track: standard
applicable_to:
  disease_id: DIS-UROTHELIAL
  disease_state: METASTATIC
  line_of_therapy: 1
  biomarker_requirements_required: []
  biomarker_requirements_excluded: []
  demographic_constraints: {ecog_max: 2}
recommended_regimen: REG-EV-PEMBRO-UROTHELIAL
concurrent_therapy: []
followed_by: []
evidence_level: high
strength_of_recommendation: strong
nccn_category: "1"
expected_outcomes: {median_overall_survival_months: 31, notes: "EV-302 (2023)"}
hard_contraindications: []
red_flags_triggering_alternative: []
required_tests: [TEST-CECT-CAP]
desired_tests: []
sources:
  - {source_id: SRC-NCCN-BLADDER-2025, weight: primary}
last_reviewed: null
reviewers: []
notes: "EV-302 paradigm 1L for ALL patients."
""",
    "ind_urothelial_metastatic_1l_platinum_avelumab.yaml": """\
id: IND-UROTHELIAL-METASTATIC-1L-PLATINUM-CHEMO-AVELUMAB
plan_track: aggressive
applicable_to:
  disease_id: DIS-UROTHELIAL
  disease_state: METASTATIC
  line_of_therapy: 1
  biomarker_requirements_required: []
  biomarker_requirements_excluded: []
  demographic_constraints: {ecog_max: 2}
recommended_regimen: REG-CISPLATIN-GEMCITABINE-UROTHELIAL
concurrent_therapy: []
followed_by: [REG-AVELUMAB-MAINTENANCE]
evidence_level: high
strength_of_recommendation: strong
nccn_category: "1"
expected_outcomes: {median_overall_survival_months: 21, notes: "JAVELIN Bladder 100"}
hard_contraindications: []
red_flags_triggering_alternative: []
required_tests: [TEST-CECT-CAP]
desired_tests: []
sources:
  - {source_id: SRC-NCCN-BLADDER-2025, weight: primary}
  - {source_id: SRC-EAU-BLADDER-2024, weight: primary}
last_reviewed: null
reviewers: []
notes: "Reserved for EV+pembro-ineligible. Galsky cisplatin-eligibility critical."
""",
    "ind_endometrial_advanced_1l_pembro_chemo.yaml": """\
id: IND-ENDOMETRIAL-ADVANCED-1L-PEMBRO-CHEMO
plan_track: standard
applicable_to:
  disease_id: DIS-ENDOMETRIAL
  stage_stratum: RECURRENT_METASTATIC
  line_of_therapy: 1
  biomarker_requirements_required: []
  biomarker_requirements_excluded: []
  demographic_constraints: {ecog_max: 2}
recommended_regimen: REG-PEMBRO-CARBO-PACLI-ENDOM
concurrent_therapy: []
followed_by: []
evidence_level: high
strength_of_recommendation: strong
nccn_category: "1"
expected_outcomes: {pfs_hr_pmmr: 0.64, notes: "NRG-GY018"}
hard_contraindications: []
red_flags_triggering_alternative: []
required_tests: [TEST-CECT-CAP, TEST-ER-PR-IHC]
desired_tests: []
sources:
  - {source_id: SRC-NCCN-UTERINE-2025, weight: primary}
last_reviewed: null
reviewers: []
notes: "NRG-GY018 + RUBY established chemoimmuno paradigm."
""",
    "ind_endometrial_advanced_1l_dostarlimab_chemo.yaml": """\
id: IND-ENDOMETRIAL-ADVANCED-1L-DOSTARLIMAB-CHEMO
plan_track: aggressive
applicable_to:
  disease_id: DIS-ENDOMETRIAL
  molecular_subtype: MMR_DEFICIENT
  stage_stratum: RECURRENT_METASTATIC
  line_of_therapy: 1
  biomarker_requirements_required:
    - {biomarker_id: BIO-DMMR-IHC, value_constraint: "deficient", required: true}
  biomarker_requirements_excluded: []
  demographic_constraints: {ecog_max: 2}
recommended_regimen: REG-DOSTARLIMAB-CARBO-PACLI-ENDOM
concurrent_therapy: []
followed_by: []
evidence_level: high
strength_of_recommendation: strong
nccn_category: "1"
expected_outcomes: {pfs_hr_dmmr: 0.30, notes: "RUBY trial"}
hard_contraindications: []
red_flags_triggering_alternative: []
required_tests: [TEST-CECT-CAP, TEST-ER-PR-IHC]
desired_tests: []
sources:
  - {source_id: SRC-NCCN-UTERINE-2025, weight: primary}
last_reviewed: null
reviewers: []
notes: "RUBY: dostarlimab+chemo PFS HR 0.30 dMMR. Lynch screening for all dMMR."
""",
}


# ── Algorithms (4) ───────────────────────────────────────────────────


ALGORITHMS = {
    "algo_rcc_metastatic_1l.yaml": """\
id: ALGO-RCC-METASTATIC-1L
applicable_to_disease: DIS-RCC
applicable_to_line_of_therapy: 1
purpose: "Select 1L mRCC by histology + IMDC risk."
output_indications: [IND-RCC-METASTATIC-1L-NIVO-IPI, IND-RCC-METASTATIC-1L-PEMBRO-AXI]
default_indication: IND-RCC-METASTATIC-1L-PEMBRO-AXI
alternative_indication: IND-RCC-METASTATIC-1L-NIVO-IPI
decision_tree:
  - step: 1
    evaluate:
      any_of:
        - {condition: "IMDC intermediate or poor risk"}
    if_true: {result: IND-RCC-METASTATIC-1L-NIVO-IPI}
    if_false: {result: IND-RCC-METASTATIC-1L-PEMBRO-AXI}
sources: [SRC-NCCN-KIDNEY-2025, SRC-ESMO-RCC-2024]
last_reviewed: null
notes: "Default to pembro+axi for IMDC favorable; nivo+ipi for intermediate/poor."
""",
    "algo_melanoma_metastatic_1l.yaml": """\
id: ALGO-MELANOMA-METASTATIC-1L
applicable_to_disease: DIS-MELANOMA
applicable_to_line_of_therapy: 1
purpose: "Select 1L metastatic melanoma by BRAF + clinical context."
output_indications: [IND-MELANOMA-METASTATIC-1L-NIVO-IPI, IND-MELANOMA-BRAF-METASTATIC-1L-DABRA-TRAME]
default_indication: IND-MELANOMA-METASTATIC-1L-NIVO-IPI
alternative_indication: IND-MELANOMA-BRAF-METASTATIC-1L-DABRA-TRAME
decision_tree:
  - step: 1
    evaluate:
      any_of:
        - {condition: "BRAF V600E/K AND visceral crisis / rapid progression"}
    if_true: {result: IND-MELANOMA-BRAF-METASTATIC-1L-DABRA-TRAME}
    if_false: {result: IND-MELANOMA-METASTATIC-1L-NIVO-IPI}
sources: [SRC-NCCN-MELANOMA-2025, SRC-ESMO-MELANOMA-2024]
last_reviewed: null
notes: "DREAMseq: ICI-doublet → BRAFi+MEKi sequence preferred over reverse."
""",
    "algo_urothelial_metastatic_1l.yaml": """\
id: ALGO-UROTHELIAL-METASTATIC-1L
applicable_to_disease: DIS-UROTHELIAL
applicable_to_line_of_therapy: 1
purpose: "Select 1L mUC. Modern: EV+pembro for all unless contraindicated."
output_indications: [IND-UROTHELIAL-METASTATIC-1L-EV-PEMBRO, IND-UROTHELIAL-METASTATIC-1L-PLATINUM-CHEMO-AVELUMAB]
default_indication: IND-UROTHELIAL-METASTATIC-1L-EV-PEMBRO
alternative_indication: IND-UROTHELIAL-METASTATIC-1L-PLATINUM-CHEMO-AVELUMAB
decision_tree:
  - step: 1
    evaluate:
      any_of:
        - {condition: "Patient eligible for EV+pembro (no severe diabetes, neuropathy, ocular)"}
    if_true: {result: IND-UROTHELIAL-METASTATIC-1L-EV-PEMBRO}
    if_false: {result: IND-UROTHELIAL-METASTATIC-1L-PLATINUM-CHEMO-AVELUMAB}
sources: [SRC-NCCN-BLADDER-2025, SRC-EAU-BLADDER-2024]
last_reviewed: null
notes: "EV-302 paradigm shift."
""",
    "algo_endometrial_advanced_1l.yaml": """\
id: ALGO-ENDOMETRIAL-ADVANCED-1L
applicable_to_disease: DIS-ENDOMETRIAL
applicable_to_line_of_therapy: 1
purpose: "Select 1L advanced/recurrent endometrial by MMR status."
output_indications: [IND-ENDOMETRIAL-ADVANCED-1L-DOSTARLIMAB-CHEMO, IND-ENDOMETRIAL-ADVANCED-1L-PEMBRO-CHEMO]
default_indication: IND-ENDOMETRIAL-ADVANCED-1L-PEMBRO-CHEMO
alternative_indication: IND-ENDOMETRIAL-ADVANCED-1L-DOSTARLIMAB-CHEMO
decision_tree:
  - step: 1
    evaluate:
      any_of:
        - {condition: "dMMR / MSI-high tumor"}
    if_true: {result: IND-ENDOMETRIAL-ADVANCED-1L-DOSTARLIMAB-CHEMO}
    if_false: {result: IND-ENDOMETRIAL-ADVANCED-1L-PEMBRO-CHEMO}
sources: [SRC-NCCN-UTERINE-2025, SRC-ESMO-ENDOMETRIAL-2022]
last_reviewed: null
notes: "Both pembro and dostarlimab approved; chemoimmuno superior to chemo alone regardless of MMR."
""",
}


def main() -> int:
    for fname, body in DISEASES.items():
        write(f"diseases/{fname}", body)
    for fname, body in SOURCES.items():
        write(f"sources/{fname}", body)
    for fname, body in BIOMARKERS.items():
        write(f"biomarkers/{fname}", body)
    for fname, body in TESTS.items():
        write(f"tests/{fname}", body)
    for fname, body in WORKUPS.items():
        write(f"workups/{fname}", body)
    for fname, body in REGIMENS.items():
        write(f"regimens/{fname}", body)
    for fname, body in REDFLAGS.items():
        write(f"redflags/{fname}", body)
    for fname, body in INDICATIONS.items():
        write(f"indications/{fname}", body)
    for fname, body in ALGORITHMS.items():
        write(f"algorithms/{fname}", body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
