# Knowledge Schema Specification

**Проєкт:** OpenOnco
**Документ:** Knowledge Schema Specification
**Версія:** v0.1 (draft)
**Статус:** Draft для обговорення з командою розробки + Clinical Co-Leads
**Попередні документи:** CHARTER.md, CLINICAL_CONTENT_STANDARDS.md

---

## Мета документа

Цей документ визначає **технічну структуру даних knowledge base** —
які сутності зберігаються, які поля обов'язкові, як сутності
пов'язані між собою, і як правила (rules) представлені у форматі,
що може виконуватися rule engine.

Без цього документа:
- Розробники не знають, які таблиці/колекції будувати
- Clinical Co-Leads не мають формату для подання рекомендацій
- Неможливо написати ні engine, ні валідатор, ні migration скрипт
- Кожна нозологія моделюється ad-hoc, що руйнує консистентність

Цей документ — **контракт між клінічним і технічним шарами**.

---

## 1. Принципи моделювання

### 1.1. Separation of knowledge and code

Правила, показання, протипоказання — в декларативному форматі (YAML),
не hardcoded у коді. Rule engine інтерпретує декларацію.

**Мотивація:** клініцист повинен мати змогу редагувати knowledge base
без участі розробника. Зміна в NCCN guideline → редагування YAML →
pull request → review → merge. Без code changes.

### 1.2. Immutability through versioning

Кожна сутність має версію. Старі версії зберігаються вічно (retention
policy у Charter §10). Update = нова версія, не overwrite.

### 1.3. Traceability

Кожна рекомендація посилається на sources (Tier 1-5 per CCS §2).
Dangling reference = invalid entity.

### 1.4. Explicit unknowns

"Невідомо" — це `unknown` enum value, не `null`. Різниця важлива: null
може означати "не заповнено", unknown означає "явно невідомо для цього
пацієнта". Rule engine трактує їх по-різному.

### 1.5. Standards-based, not bespoke

Використовуємо стандартні vocabularies (SNOMED CT, LOINC, RxNorm,
ICD-O-3) для кодування, не винаходимо свої коди.

### 1.6. No composite scoring

Schema не містить `composite_rating` чи `overall_score`. Evidence
level і strength of recommendation зберігаються окремо (per CCS §4).

---

## 2. Top-level entities (огляд)

Всього 12 основних сутностей:

```
┌──────────────────────────────────────────────────────────────────┐
│                     KNOWLEDGE BASE                                │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Disease ─────┐                                                   │
│               ├──── Indication ─────── Regimen ─────── Drug       │
│  Biomarker ──┤         │                   │                      │
│               │         │                   └── Contraindication  │
│  Stage  ─────┘         │                                          │
│                         │                                          │
│                         └── Source (evidence refs)                 │
│                                                                    │
│  RedFlag ─────────── (modifies Indication selection)              │
│                                                                    │
│  Test ────────────── (pre-treatment / monitoring)                  │
│                                                                    │
│  SupportiveCare ──── (linked to Regimen or RiskProfile)           │
│                                                                    │
│  MonitoringSchedule ─ (linked to Regimen + Phase)                 │
│                                                                    │
│  Algorithm ────────── (decision tree referencing Indications)     │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
```

Patient entity — окремий шар (див. документ 3: Data Standards /
mCODE). Тут ми моделюємо лише knowledge, не пацієнтські дані.

---

## 3. Entity: Disease

Нозологія з класифікацією за WHO.

### 3.1. Schema

```yaml
# File: knowledge_base/diseases/hcv_mzl.yaml

entity_type: Disease
id: DIS-HCV-MZL
version: "1.0.0"
created: "2026-04-01"
last_reviewed: "2026-04-15"
reviewers: [reviewer-id-1, reviewer-id-2]

# Classification
names:
  preferred: "HCV-associated marginal zone lymphoma"
  ukrainian: "HCV-асоційована лімфома маргінальної зони"
  synonyms:
    - "HCV-related MZL"
    - "Hepatitis C-associated marginal zone lymphoma"
  abbreviations: ["HCV-MZL"]

codes:
  icd_o_3: "9699/3"
  icd_10: "C85.1"
  snomed_ct: "118605005"
  who_classification:
    edition: "5th"
    year: 2024
    entity: "Extranodal marginal zone lymphoma of mucosa-associated lymphoid tissue"
    category: "Mature B-cell neoplasms"

# Clinical characteristics
lineage: "B-cell"
cell_of_origin: "Marginal zone B-cell"
typical_sites:
  - "Spleen"
  - "Extranodal (MALT variants)"
  - "Lymph nodes (NMZL)"

# Etiological drivers (for archetype classification)
etiological_factors:
  - factor: "HCV chronic infection"
    strength: "causal"  # causal | associated | background
    source_refs: [SRC-FERRI-2008, SRC-ARCAINI-2016]

# Epidemiology (optional, for context)
epidemiology:
  incidence_global: "1-2 per 100,000/year (MZL overall)"
  hcv_mzl_proportion: "20-30% of NMZL in HCV-endemic regions"

# Archetype — determines document structure for this disease
archetype: "etiologically_driven"
# Valid values: etiologically_driven | biomarker_driven | stage_driven |
#               risk_stratified | line_of_therapy_sequential

# Linked entities
related_diseases:
  - {id: DIS-MZL-SPLENIC, relation: "variant"}
  - {id: DIS-DLBCL-TRANSFORMATION, relation: "can_transform_to"}

metadata:
  maintainer_domain: "hematologic_malignancies"
  priority_for_mvp: true
  notes: >
    First reference disease for the project. Chosen because it has
    well-defined etiological driver (HCV), clear guidelines (NCCN,
    ESMO, EASL), and reference document exists (HCV-MZL case V.0.0).
```

### 3.2. Required fields

- `entity_type`, `id`, `version`
- `names.preferred`
- `codes.icd_o_3` (обов'язково для всіх онкологічних)
- `codes.who_classification.entity`
- `lineage`
- `archetype`
- `last_reviewed`, `reviewers`

### 3.3. Archetype values

Based on CDSS architecture analysis (see project docs):

| Archetype | Meaning | Example diseases |
|---|---|---|
| `etiologically_driven` | Causal agent removal is part of treatment | HCV-MZL, MALT/H.pylori, HPV-OPC |
| `biomarker_driven` | Molecular profile primarily determines Rx | EGFR+ NSCLC, HER2+ BC, BRAF+ melanoma |
| `stage_driven` | Stage is primary therapy split | Early-stage breast, CRC |
| `risk_stratified` | Prognostic classification dominant | AML, CLL, multiple myeloma |
| `line_of_therapy_sequential` | Treatment = sequential lines | Metastatic NSCLC, mCRC 2L+ |

Archetype determines document template structure.

---

## 4. Entity: Biomarker

Молекулярний, гістологічний, лабораторний маркер.

### 4.1. Schema

```yaml
# File: knowledge_base/biomarkers/ki67.yaml

entity_type: Biomarker
id: BIO-KI67
version: "1.0.0"

names:
  preferred: "Ki-67"
  full_name: "Ki-67 proliferation index"
  alternative: "MIB-1"

codes:
  loinc: "85319-2"
  snomed_ct: "386030001"

# Type
biomarker_type: "protein_expression_ihc"
# Valid: mutation | fusion | amplification | deletion |
#         protein_expression_ihc | protein_expression_flow |
#         msi_status | tmb | methylation | chromosomal |
#         serum_marker | other

# Measurement
measurement:
  method: "immunohistochemistry"
  units: "percent"
  typical_range: [0, 100]
  rounding: "nearest 5%"

# Clinical interpretation cutoffs
# NOTE: cutoffs are disease-specific; stored in Indication entities,
# not here. This field shows general interpretation guidance.
interpretation_notes: >
  Proliferation index. Higher values indicate more rapidly dividing
  tumor. Cutoffs for clinical decisions vary by disease entity
  (e.g., ≥30% in some lymphomas triggers consideration of aggressive
  regimens; ≥20% in breast cancer correlates with luminal B subtype).

# Technical requirements
specimen_requirements:
  specimen_type: ["FFPE tissue", "Fresh frozen tissue"]
  minimum_cellularity: "sufficient tumor cells (>200 cells preferred)"

# Related biomarkers
related_biomarkers: []

last_reviewed: "2026-04-15"
reviewers: [reviewer-id]
```

### 4.2. Example: mutation biomarker

```yaml
entity_type: Biomarker
id: BIO-EGFR-L858R
names:
  preferred: "EGFR L858R"
  full_name: "Epidermal Growth Factor Receptor, exon 21, L858R mutation"
codes:
  hgvs_protein: "NP_005219.2:p.Leu858Arg"
  hgvs_coding: "NM_005228.5:c.2573T>G"
  oncokb_id: "EGFR_L858R"

biomarker_type: "mutation"
mutation_details:
  gene: "EGFR"
  gene_hugo_id: "3236"
  exon: 21
  type: "missense"
  functional_impact: "activating"

measurement:
  method: ["NGS panel", "PCR-based specific assay"]
  sensitivity_requirement: "allele frequency ≥5% typically detectable"

# OncoKB reference
knowledge_base_ref:
  oncokb: "https://oncokb.org/gene/EGFR/L858R"
  civic: "https://civicdb.org/links/variants/33"
  last_synced: "2026-04-15"
```

---

## 5. Entity: Drug

Окремий препарат.

### 5.1. Schema

```yaml
# File: knowledge_base/drugs/rituximab.yaml

entity_type: Drug
id: DRUG-RITUXIMAB
version: "1.0.0"

names:
  generic: "rituximab"
  ukrainian: "ритуксимаб"
  brand_names: ["Rituxan", "MabThera", "Truxima (biosimilar)", "Ruxience (biosimilar)"]
  atc_code: "L01FA01"
  inn: "rituximab"

codes:
  rxnorm: "121191"
  snomed_ct: "386919002"
  ndc: []  # multiple; per-formulation basis

# Drug class
drug_class:
  primary: "monoclonal_antibody"
  mechanism: "anti-CD20 monoclonal antibody"
  target: "CD20 (B-cell surface marker)"

# Regulatory status
regulatory_status:
  fda:
    approved: true
    first_approval_year: 1997
    indications_link: ["NCCN-B-Cell-Lymphomas", "multiple"]
  ema:
    approved: true
  ukraine_registration:
    registered: true
    registration_number: "[filled by UA regulatory lookup]"
    reimbursed_nszu: true
    reimbursement_indications: ["specific - see НСЗУ list"]

# Dosing (generic; disease-specific doses in Regimen entity)
typical_dosing:
  standard_dose: "375 mg/m²"
  standard_route: "intravenous infusion"
  notes: >
    Dose varies by disease and line of therapy. See Regimen entities
    for disease-specific dosing. Infusion rate protocols apply.

# Formulations available
formulations:
  - {form: "solution_for_infusion", strength: "10 mg/mL", volumes: ["10 mL", "50 mL"]}
  - {form: "subcutaneous_injection", strength: "120 mg/mL", note: "1400 mg fixed dose"}

# Contraindications (general; disease-specific in Contraindication entity)
absolute_contraindications:
  - "Known severe hypersensitivity to rituximab or murine proteins"
  - "Active severe infection"

# Safety warnings
black_box_warnings:
  - warning: "Fatal infusion reactions"
    source: "FDA label, updated 2024"
  - warning: "Severe mucocutaneous reactions"
    source: "FDA label"
  - warning: "Hepatitis B reactivation"
    source: "FDA label"
  - warning: "Progressive multifocal leukoencephalopathy (PML)"
    source: "FDA label"

# Important drug interactions
interactions:
  - with: "live vaccines"
    severity: "contraindicated"
    mechanism: "immune suppression reduces immune response"

# Key toxicities
common_adverse_events:
  - {event: "infusion_reaction", frequency: "10-20%", grade: "typically 1-2"}
  - {event: "neutropenia", frequency: "15-30%", grade: "3-4: 5-10%"}
  - {event: "infection", frequency: "variable"}
  - {event: "tumor_lysis_syndrome", frequency: "rare; depends on disease burden"}

# Pharmacology
pharmacology:
  half_life_days: [11, 30]  # range
  elimination: "Reticuloendothelial system; not renal"
  crosses_bbb: false

source_refs: [SRC-RITUXIMAB-FDA-LABEL, SRC-NCCN-BCELL-V2-2026]

last_reviewed: "2026-04-15"
reviewers: [reviewer-id-1, reviewer-id-2]
```

### 5.2. Required fields

- `id`, `names.generic`, `names.ukrainian`
- `drug_class.mechanism`
- `regulatory_status.ukraine_registration.registered`
- `absolute_contraindications`
- At least one `source_refs`

---

## 6. Entity: Regimen

Лікувальна схема — комбінація препаратів з графіком.

### 6.1. Schema

```yaml
# File: knowledge_base/regimens/br.yaml

entity_type: Regimen
id: REG-BR-LYMPHOMA
version: "1.0.0"

names:
  preferred: "Bendamustine-Rituximab (BR)"
  acronym: "BR"
  ukrainian: "Бендамустин + Ритуксимаб (BR)"

# Components
components:
  - drug_id: DRUG-BENDAMUSTINE
    dose: "90 mg/m²"
    route: "intravenous"
    schedule: "days 1-2 of each cycle"
    order: 1
  - drug_id: DRUG-RITUXIMAB
    dose: "375 mg/m²"
    route: "intravenous"
    schedule: "day 1 of each cycle"
    order: 2
    notes: "May be given as day 0 per institutional protocol"

# Cycle structure
cycle_length_days: 28
total_cycles: 6
total_duration_weeks: 24

# Intent
typical_intent: ["curative", "palliative"]
# Specific intent determined per Indication

# Dose modifications
dose_adjustments:
  - condition: "FIB-4 > 3.25 OR cirrhosis"
    modification: "Reduce bendamustine to 70 mg/m²"
    rationale: "Hepatic dysfunction increases bendamustine toxicity"
    source_refs: [SRC-EMA-BENDAMUSTINE-SmPC]
  - condition: "ECOG >= 2 OR age >= 75"
    modification: "Consider bendamustine 70-80 mg/m²"
    rationale: "Reduced tolerance in frail patients"
  - condition: "CrCl < 30 mL/min"
    modification: "Not recommended; use alternative regimen"

# Toxicity profile (summary)
toxicity_profile:
  myelosuppression: "moderate-severe"
  cardiotoxicity: "low"
  neurotoxicity: "low"
  hepatotoxicity: "moderate"
  nephrotoxicity: "low"
  alopecia: "moderate"
  emetogenic_risk: "moderate"
  treatment_related_mortality_percent: [1, 2]

# Required premedication
premedication:
  rituximab:
    - "paracetamol 1000 mg PO"
    - "diphenhydramine 25-50 mg PO or IV"
    - "methylprednisolone 100 mg IV (or equivalent)"
  bendamustine:
    - "ondansetron 8 mg IV or equivalent 5-HT3 antagonist"
    - "dexamethasone 8-12 mg IV"

# Required supportive care
mandatory_supportive_care:
  - id: SUPP-PJP-PROPHYLAXIS
    notes: "Cotrimoxazole 480 mg daily during treatment + 6 months"
  - id: SUPP-ANTIVIRAL-PROPHYLAXIS
    notes: "Acyclovir 400 mg BID during treatment + 6 months"
  - id: SUPP-HBV-SCREENING-PROPHYLAXIS
    notes: "Required per CCS §3 — see Contraindication CONTRA-HBV"

# Monitoring during regimen
monitoring_schedule_id: MON-BR-STANDARD

# Ukraine availability
ukraine_availability:
  bendamustine:
    registered: true
    reimbursed_nszu: true  # verify current
    typical_cost_per_cycle_uah: "[to fill from pricing analysis]"
  rituximab:
    registered: true
    reimbursed_nszu: true
    biosimilar_available: true

source_refs:
  - SRC-NCCN-BCELL-V2-2026
  - SRC-ESMO-MZL-2020
  - SRC-BRIGHT-TRIAL-FLINN-2019
  - SRC-STIL-NHL1-RUMMEL-2013

last_reviewed: "2026-04-15"
reviewers: [reviewer-id-hem-1, reviewer-id-hem-2]
```

### 6.2. Required fields

- `id`, `names.preferred`, `names.ukrainian`
- `components` (список з мінімум одного Drug)
- `cycle_length_days`
- `total_cycles` OR `total_duration_weeks`
- `toxicity_profile`
- `monitoring_schedule_id`
- At least one `source_refs`

### 6.3. Toxicity profile values

For each toxicity category, use enum:
- `none`
- `low`
- `moderate`
- `severe`
- `variable` (з описом в `notes`)

Numeric rates (where available) в окремих полях з джерелом.

---

## 7. Entity: Indication

**Найважливіша сутність.** Пов'язує Disease + clinical profile → Regimen
з рівнем доказовості.

### 7.1. Schema

```yaml
# File: knowledge_base/indications/hcv_mzl_1l_standard.yaml

entity_type: Indication
id: IND-HCV-MZL-1L-STANDARD
version: "1.0.0"

# What clinical scenario this covers
applicable_to:
  disease_id: DIS-HCV-MZL
  line_of_therapy: 1  # 1 = first-line; 2 = second-line; etc.
  stage_requirements:
    stages: ["all"]  # or specific: ["I-II", "III-IV"]
  biomarker_requirements:
    required:
      - biomarker_id: BIO-HCV-RNA-POSITIVE
        value_constraint: "positive"
    excluded:
      - biomarker_id: BIO-TRANSFORMATION-MARKERS
        value_constraint: "negative"
  demographic_constraints:
    age_range: [18, null]  # null = no upper limit
    performance_status_max: 2  # ECOG
  additional_constraints:
    - "No red flags for histological transformation"

# The recommendation
recommended_regimen_id: REG-BR-LYMPHOMA
concurrent_therapy:
  - regimen_id: REG-DAA-SOFOSBUVIR-VELPATASVIR
    timing: "concurrent_with_br"
    rationale: "HCV eradication removes antigenic driver; safe co-administration confirmed"

# Sequential/maintenance phase
followed_by:
  - regimen_id: REG-RITUXIMAB-MAINTENANCE
    timing: "after_completion_of_induction"
    duration: "2 years (q8w × 12 doses)"
    rationale: "BRIGHT trial: EFS 81% → 94% with maintenance"

# Evidence assessment (per CCS §4)
evidence_level: "moderate"
# high | moderate | low | very_low
evidence_level_rationale: >
  Phase 2 BArT trial (Arcaini 2014, N=44); supported by retrospective
  analyses and aligned with NCCN/ESMO recommendations. No Phase 3 RCT
  specifically for HCV-MZL 1L (HCV-MZL too rare for dedicated Phase 3).

strength_of_recommendation: "preferred"
# preferred | alternative | not_recommended | insufficient_evidence
strength_rationale: >
  Consensus across NCCN, ESMO, and EASL recommendations. Benefit-harm
  balance clearly favorable in appropriate population. Lower toxicity
  than historical R-CHOP with equivalent efficacy in non-transformed MZL.

nccn_category: "2A"  # 1 | 2A | 2B | 3 | N/A

# Expected outcomes (key evidence numbers)
expected_outcomes:
  overall_response_rate:
    value: "85-90%"
    source_ref: SRC-BRIGHT-TRIAL
    notes: "For BR in indolent lymphomas broadly"
  complete_response:
    value: "~60%"
    source_ref: SRC-BRIGHT-TRIAL
  progression_free_survival:
    median_months: 42
    source_ref: SRC-BRIGHT-TRIAL
    note: "For indolent NHL; HCV-MZL-specific data limited"
  hcv_cure_rate_svr12:
    value: "95-98%"
    source_ref: SRC-EASL-HCV-2023
  overall_survival_5y:
    value: "80-85%"
    source_ref: SRC-ARCAINI-2016

# Contraindications (hard)
hard_contraindications: [CONTRA-AMIODARONE-SOFOSBUVIR, CONTRA-HBV-NO-PROPHYLAXIS]

# Red flags that should trigger alternative indication
red_flags_triggering_alternative:
  - red_flag_id: RF-B-SYMPTOMS
    alternative_indication: IND-HCV-MZL-1L-AGGRESSIVE
  - red_flag_id: RF-LDH-HIGH
    alternative_indication: IND-HCV-MZL-1L-AGGRESSIVE
  - red_flag_id: RF-BULKY-DISEASE
    alternative_indication: IND-HCV-MZL-1L-AGGRESSIVE
  - red_flag_id: RF-RAPID-PROGRESSION
    alternative_indication: IND-HCV-MZL-1L-AGGRESSIVE

# Pre-treatment workup
required_tests: [TEST-CBC, TEST-LFT-COMPREHENSIVE, TEST-HCV-RNA-QUANT, TEST-HBV-SEROLOGY, TEST-FIB-4]
desired_tests: [TEST-ECHO-LVEF, TEST-LDH, TEST-B2-MICROGLOBULIN]

# Sources
sources:
  - id: SRC-NCCN-BCELL-V2-2026
    section: "MZL-3, MZL-4"
    weight: "primary"
  - id: SRC-ESMO-MZL-2020
    weight: "primary"
  - id: SRC-EASL-HCV-2023
    weight: "primary_for_daa_component"
  - id: SRC-BART-ARCAINI-2014
    weight: "supporting_phase2"
  - id: SRC-BRIGHT-FLINN-2019
    weight: "supporting_phase3_indolent_broad"

# Controversies (per CCS §1.2 — show, don't hide)
known_controversies:
  - topic: "Bendamustine dosing in elderly/cirrhotic"
    positions:
      - "NCCN: 90 mg/m² standard"
      - "ESMO: consider 70 mg/m² for elderly/cirrhotic"
    resolution: "Implemented as dose_adjustment in Regimen"

last_reviewed: "2026-04-15"
reviewers: [reviewer-id-hem-1, reviewer-id-hem-2]
```

### 7.2. Required fields

- `id`, `version`
- `applicable_to.disease_id`, `applicable_to.line_of_therapy`
- `recommended_regimen_id`
- `evidence_level`, `strength_of_recommendation`
- `hard_contraindications` (may be empty array)
- Minimum 2 `sources` of Tier 1 or Tier 2 (per CCS §6.1)

### 7.3. The two-plan architecture

For the project's core use case (generating two alternative plans),
pairs of Indications are created:

```
IND-HCV-MZL-1L-STANDARD   (less intensive)
IND-HCV-MZL-1L-AGGRESSIVE (more intensive)
```

Linked by shared `applicable_to` but different `recommended_regimen_id`
and `red_flags_triggering_alternative` bidirectionally.

Algorithm entity (§12) determines which is "default" vs "alternative"
for a given patient.

---

## 8. Entity: Contraindication

Hard rules that prevent regimen use.

### 8.1. Schema

```yaml
# File: knowledge_base/contraindications/amiodarone_sofosbuvir.yaml

entity_type: Contraindication
id: CONTRA-AMIODARONE-SOFOSBUVIR
version: "1.0.0"

# Severity
severity: "absolute"
# absolute | relative | caution

# Trigger condition (machine-readable)
trigger:
  type: "drug_drug_interaction"
  conditions:
    - patient_current_medication_includes: DRUG-AMIODARONE
    - proposed_regimen_contains: DRUG-SOFOSBUVIR
  logic: "AND"  # all conditions must be true

# Human-readable description
description:
  english: >
    Concurrent use of sofosbuvir and amiodarone can cause severe,
    potentially fatal bradyarrhythmia. This combination is absolutely
    contraindicated.
  ukrainian: >
    Одночасне використання софосбувіру та аміодарону може спричинити
    важку, потенційно фатальну брадиаритмію. Ця комбінація абсолютно
    протипоказана.

# What to do instead
alternative_actions:
  - "Use DAA combination that does not include sofosbuvir (e.g., glecaprevir/pibrentasvir)"
  - "If sofosbuvir essential, discontinue amiodarone ≥6 months before (long half-life)"
  - "Consult cardiology for amiodarone alternatives"

# Sources
sources:
  - id: SRC-FDA-SOFOSBUVIR-LABEL
    section: "Boxed Warning"
  - id: SRC-BACK-2015-DRUG-INTERACTION

# Related entities
affects_indications:
  - IND-HCV-MZL-1L-STANDARD
  - IND-HCV-MZL-1L-AGGRESSIVE
  - IND-HCV-ANY-WITH-SOFOSBUVIR  # generic

last_reviewed: "2026-04-15"
reviewers: [reviewer-id-pharm, reviewer-id-hem]
```

### 8.2. Severity levels

| Severity | Meaning | Engine behavior |
|---|---|---|
| `absolute` | Never proceed with this combination | Regimen excluded; show hard block |
| `relative` | Proceed only with specific precautions | Show warning; require acknowledgment |
| `caution` | Proceed with monitoring | Show informational note |

### 8.3. Trigger types

- `patient_condition` — patient has specific diagnosis/status
- `lab_value` — lab value outside range
- `medication` — patient on specific drug
- `drug_drug_interaction` — proposed + existing drug conflict
- `allergy` — documented allergy
- `prior_treatment` — specific prior treatment history
- `biomarker_status` — specific biomarker value/absence
- `demographic` — age/sex-specific

---

## 9. Entity: RedFlag

Clinical findings that shift treatment intensity choice.

### 9.1. Schema

```yaml
# File: knowledge_base/red_flags/b_symptoms.yaml

entity_type: RedFlag
id: RF-B-SYMPTOMS
version: "1.0.0"

names:
  preferred: "B symptoms"
  ukrainian: "B-симптоми"

# What defines it
definition:
  english: >
    Constitutional symptoms of lymphoma including: unexplained fever >38°C,
    drenching night sweats, or unexplained weight loss >10% body weight
    over 6 months.
  ukrainian: >
    Загальні симптоми лімфоми: незрозуміла лихоманка >38°C, нічна
    пітливість, втрата ваги >10% за 6 місяців.

# Trigger (machine-readable)
trigger:
  type: "symptom_composite"
  any_of:
    - {symptom: "fever_unexplained", threshold_celsius: 38.0, duration: ">2 weeks"}
    - {symptom: "night_sweats_drenching"}
    - {symptom: "weight_loss_unexplained", threshold_percent: 10, duration_months: 6}

# Clinical implication
clinical_direction: "intensify"
# intensify | de_escalate | hold | investigate

# Which diseases this is relevant to
relevant_diseases: [DIS-HCV-MZL, DIS-DLBCL, DIS-FOLLICULAR-LYMPHOMA, DIS-HODGKIN]

# In MVP: linked to alternative indication logic
shifts_algorithm:
  from_indication: IND-HCV-MZL-1L-STANDARD
  to_indication: IND-HCV-MZL-1L-AGGRESSIVE
  strength: "strong_indication_to_shift"
  # strong_indication_to_shift | consider_shift | weak_signal

source_refs: [SRC-LUGANO-CLASSIFICATION, SRC-NCCN-BCELL-V2-2026]
last_reviewed: "2026-04-15"
reviewers: [reviewer-id]
```

---

## 10. Entity: Test

Clinical tests — pre-treatment workup and monitoring.

### 10.1. Schema

```yaml
# File: knowledge_base/tests/hcv_rna_quant.yaml

entity_type: Test
id: TEST-HCV-RNA-QUANT
version: "1.0.0"

names:
  preferred: "HCV RNA quantitative PCR"
  ukrainian: "HCV-RNA ПЛР кількісний"

codes:
  loinc: "11011-4"

category: "virology"
# hematology | biochemistry | virology | immunology | imaging |
# pathology | molecular | cardiac | other

purpose:
  - "Baseline HCV viral load before DAA treatment"
  - "Monitoring response to DAA"
  - "Detection of SVR12 (sustained virologic response)"

specimen:
  type: "blood"
  volume_ml: 5
  tube: "EDTA or SST"

turnaround_time_business_days: [2, 5]

priority_class: "critical"
# critical | standard | desired | calculation_based

availability_ukraine:
  state_funded: true
  typical_cost_uah: "[estimate; varies]"
  typical_availability: "widely available in oncology centers"

linked_to_regimens: [REG-DAA-SOFOSBUVIR-VELPATASVIR]
linked_to_diseases: [DIS-HCV-MZL, DIS-HCV-DLBCL, DIS-HCV-ANY]

source_refs: [SRC-EASL-HCV-2023]
last_reviewed: "2026-04-15"
reviewers: [reviewer-id]
```

### 10.2. Priority classes

Follows HCV-MZL reference document convention:
- `critical` — must have before treatment decision
- `standard` — routine part of workup
- `desired` — helpful but not blocking
- `calculation_based` — derived from other tests (e.g., FIB-4, BSA)

---

## 11. Entity: SupportiveCare

Profylactic and supportive interventions.

### 11.1. Schema

```yaml
# File: knowledge_base/supportive_care/pjp_prophylaxis.yaml

entity_type: SupportiveCare
id: SUPP-PJP-PROPHYLAXIS
version: "1.0.0"

names:
  preferred: "PJP (Pneumocystis jirovecii) prophylaxis"
  ukrainian: "Профілактика пневмоцистної пневмонії"

intervention_type: "pharmacological"
# pharmacological | procedural | nutritional | psychosocial | monitoring

# What
standard_intervention:
  drug_id: DRUG-COTRIMOXAZOLE
  dose: "480 mg once daily OR 960 mg three times weekly"
  route: "oral"
  duration: "during_immunosuppressive_therapy + 6 months post"

alternatives:
  - {drug_id: DRUG-DAPSONE, condition: "sulfa allergy", dose: "100 mg daily"}
  - {drug_id: DRUG-ATOVAQUONE, condition: "sulfa allergy, dapsone intolerance"}
  - {drug_id: DRUG-PENTAMIDINE-INHALED, condition: "drug intolerance"}

# When indicated
triggers:
  - {regimen_contains_drug_class: "purine_analog"}
  - {regimen_id: REG-BR-LYMPHOMA}
  - {regimen_id: REG-R-CHOP}
  - {prolonged_corticosteroid_use_days: ">21"}
  - {patient_immunodeficiency: true}

# Rationale
rationale: >
  Regimens causing CD4 lymphopenia (including bendamustine-containing
  and R-CHOP) increase risk of PJP. Prophylaxis reduces incidence from
  ~5% to <1%.

source_refs: [SRC-IDSA-PJP-GUIDELINES, SRC-NCCN-SUPPORTIVE]
last_reviewed: "2026-04-15"
reviewers: [reviewer-id-id, reviewer-id-hem]
```

---

## 12. Entity: MonitoringSchedule

Schedule of tests/visits during regimen.

### 12.1. Schema

```yaml
# File: knowledge_base/monitoring/br_standard.yaml

entity_type: MonitoringSchedule
id: MON-BR-STANDARD
version: "1.0.0"

linked_to_regimen: REG-BR-LYMPHOMA

phases:
  - phase_name: "Pre-treatment"
    window: "week -2 to week 0"
    required_tests: [TEST-CBC, TEST-LFT, TEST-HCV-RNA, TEST-HBV-SEROLOGY, TEST-FIB-4, TEST-ECG]
    desired_tests: [TEST-ECHO-LVEF]
    visits: 1

  - phase_name: "Cycle 1 intensive monitoring"
    window: "weeks 0-4"
    recurring_tests:
      - {test: TEST-CBC, frequency: "weekly"}
      - {test: TEST-CMP, frequency: "weekly"}
    checkpoints:
      - {week: 4, test: TEST-HCV-RNA-QUANT}
    visits: "weekly"

  - phase_name: "Cycles 2-6"
    window: "weeks 4-24"
    recurring_tests:
      - {test: TEST-CBC, frequency: "before each cycle + day 14"}
      - {test: TEST-CMP, frequency: "before each cycle"}
    checkpoints:
      - {week: 12, test: TEST-HCV-RNA-QUANT, note: "Post-DAA completion"}
      - {after_cycle: 3, test: IMAGING-CT-OR-PET, note: "Interim response assessment"}
      - {after_cycle: 6, test: IMAGING-CT-OR-PET, note: "End-of-induction response"}

  - phase_name: "Maintenance (rituximab q8w)"
    window: "weeks 24-128"
    recurring_tests:
      - {test: TEST-CBC, frequency: "before each dose"}
      - {test: TEST-CMP, frequency: "before each dose"}
    checkpoints:
      - {week: 48, test: TEST-HCV-RNA-QUANT, note: "SVR24 confirmation"}
      - {frequency_months: 6, tests: [TEST-LIVER-US, TEST-AFP], note: "HCC screening post-HCV"}

  - phase_name: "Lifelong surveillance"
    window: "after week 128"
    recurring_tests:
      - {frequency_months: [3, 6], test: "clinical_exam"}
      - {frequency_months: [6, 12], test: IMAGING-CT, duration_years: 5}
      - {frequency_months: 6, tests: [TEST-LIVER-US, TEST-AFP], duration: "lifelong"}

source_refs: [SRC-NCCN-BCELL-V2-2026, SRC-EASL-HCV-2023]
last_reviewed: "2026-04-15"
reviewers: [reviewer-id]
```

---

## 13. Entity: Algorithm

Decision tree for two-plan generation.

### 13.1. Schema

```yaml
# File: knowledge_base/algorithms/hcv_mzl_1l_choice.yaml

entity_type: Algorithm
id: ALGO-HCV-MZL-1L-CHOICE
version: "1.0.0"

applicable_to:
  disease_id: DIS-HCV-MZL
  line_of_therapy: 1

# Output
purpose: "Select between standard and aggressive 1L regimen"
output_indications: [IND-HCV-MZL-1L-STANDARD, IND-HCV-MZL-1L-AGGRESSIVE]
default_indication: IND-HCV-MZL-1L-STANDARD

# Decision tree
decision_tree:
  - step: 1
    description: "Are there red flags AGAINST aggressive regimen?"
    evaluate:
      any_of:
        - red_flag: RF-LVEF-LOW
        - red_flag: RF-CIRRHOSIS-OR-FIB4-HIGH
        - red_flag: RF-ECOG-HIGH
        - red_flag: RF-SEVERE-NEUROPATHY
        - red_flag: RF-AMIODARONE
        - red_flag: RF-NO-ECHO-AVAILABLE
        - red_flag: RF-AGE-OVER-75
    if_true:
      result: IND-HCV-MZL-1L-STANDARD
      reason: "Contraindications to aggressive regimen"
      stop: true
    if_false:
      continue_to: 2

  - step: 2
    description: "Are there red flags FOR aggressive regimen?"
    evaluate:
      any_of:
        - red_flag: RF-B-SYMPTOMS
        - red_flag: RF-LDH-HIGH
        - red_flag: RF-RAPID-PROGRESSION
        - red_flag: RF-BULKY-DISEASE
        - red_flag: RF-HYPERCALCEMIA
        - red_flag: RF-HISTOLOGICAL-TRANSFORMATION
    if_true:
      result: IND-HCV-MZL-1L-AGGRESSIVE
      reason: "Indicators for aggressive regimen present"
    if_false:
      result: IND-HCV-MZL-1L-STANDARD
      reason: "Default recommendation (consensus)"

# Output format
always_show_both:
  description: >
    Both standard and aggressive indications are always presented to
    the clinician. Algorithm determines which is marked "default" vs
    "alternative", but both documents are generated for comparison.
  enforcement: "mandatory_two_plan_output"

source_refs: [SRC-NCCN-BCELL-V2-2026, SRC-ESMO-MZL-2020, SRC-ALDERUCCIO-2024]
last_reviewed: "2026-04-15"
reviewers: [reviewer-id-hem-1, reviewer-id-hem-2]
```

---

## 14. Entity: Source

Metadata для будь-якого джерела.

### 14.1. Schema

```yaml
# File: knowledge_base/sources/nccn_bcell_v2_2026.yaml

entity_type: Source
id: SRC-NCCN-BCELL-V2-2026
version: "1.0.0"

source_type: "guideline"
# guideline | phase3_rct | phase2_trial | phase1_trial |
# meta_analysis | systematic_review | regulatory |
# clinical_trial_registry | molecular_kb | monograph | review

title: "NCCN Clinical Practice Guidelines in Oncology: B-Cell Lymphomas"
version_or_edition: "Version 2.2026"
publisher: "National Comprehensive Cancer Network"
publication_year: 2026
publication_date: "2026-02-15"

# For articles
authors: []
journal: null
doi: null
pmid: null

# Access
url: "https://www.nccn.org/guidelines/guidelines-detail?category=1&id=1480"
access_level: "subscription_required"
# open_access | subscription_required | registered_free | limited

currency_status: "current"
# current | superseded | historical
superseded_by: null
current_as_of: "2026-04-15"

# Tier assignment per CCS §2
evidence_tier: 1

# Related
relates_to_diseases: [DIS-HCV-MZL, DIS-DLBCL, DIS-FOLLICULAR-LYMPHOMA, "..."]

notes: >
  Primary reference for all B-cell lymphoma indications. Updated
  quarterly. Check for new versions every 3 months as part of
  knowledge base hygiene (CCS §9.1).

last_verified: "2026-04-15"
verifier: [reviewer-id]
```

---

## 15. Overall data model (relational view)

For developers, relational mapping:

```
DISEASE (1) ──────< (N) INDICATION >──────── (1) REGIMEN
                       │                         │
                       │                         ├──< (N) DRUG (via components)
                       │                         │
                       │                         ├── (1) MONITORING_SCHEDULE
                       │                         │
                       │                         └──< (N) SUPPORTIVE_CARE (mandatory)
                       │
                       ├──< (N) CONTRAINDICATION (hard)
                       │
                       ├──< (N) RED_FLAG (triggers alternative)
                       │
                       ├──< (N) TEST (required / desired)
                       │
                       └──< (N) SOURCE (evidence)

ALGORITHM (1) ──────< (N) INDICATION (outputs)
          └──────< (N) RED_FLAG (uses as inputs)

BIOMARKER ──── linked_via ──── INDICATION, DISEASE, DRUG
```

---

## 16. Storage options

Schema is **format-agnostic**. Three reasonable implementations:

### 16.1. YAML files in git (MVP recommended)

```
knowledge_base/
├── diseases/
│   └── hcv_mzl.yaml
├── drugs/
│   ├── rituximab.yaml
│   └── bendamustine.yaml
├── regimens/
│   ├── br.yaml
│   └── r_chop.yaml
├── indications/
│   ├── hcv_mzl_1l_standard.yaml
│   └── hcv_mzl_1l_aggressive.yaml
├── contraindications/
├── red_flags/
├── tests/
├── supportive_care/
├── monitoring/
├── algorithms/
└── sources/
```

**Переваги:**
- Git history = complete audit trail
- Standard OSS workflow (PRs, reviews)
- Клініцисти можуть редагувати у текстовому редакторі
- Human-readable, human-reviewable
- No database infrastructure needed for MVP

**Мінуси:**
- Referential integrity не enforced автоматично — потрібен валідатор
- Performance обмежена для великих KBs (тисячі entities)

### 16.2. PostgreSQL з JSON columns

Для версії, коли knowledge base виростає:
- Core fields — typed columns
- Flexible content (trees, conditions) — JSONB
- Referential integrity через foreign keys
- Повнотекстовий пошук built-in

### 16.3. Graph database (Neo4j, ArangoDB)

Оптимально для складних декілька-hop queries (biomarker → drugs → regimens → ...).
Overkill для MVP.

**Рекомендація:** почати з 16.1, перейти на 16.2 коли тестова нозологія
доведе life (шкалiрування + production reliability).

---

## 17. Validation tooling

Що розробник має побудувати з першого дня:

**Entity validator:**
- Перевіряє, що всі required fields заповнені
- Перевіряє, що всі `_id` references валідні (не dangling)
- Перевіряє, що `version` semantic і увеличивается
- Перевіряє, що `last_reviewed` не старіше threshold

**Source checker:**
- Перевіряє, що всі sources існують у `sources/`
- Перевіряє, що URLs доступні (periodic check)
- Перевіряє `currency_status` не `superseded` без `superseded_by`

**Clinical review enforcer:**
- Перевіряє, що кожна Indication має >= 2 reviewers
- Перевіряє, що reviewers — з approved list
- Блокує merge без approval від required number

**CI/CD pipeline:**
```yaml
# .github/workflows/knowledge_validation.yml
on: pull_request
jobs:
  validate:
    steps:
      - validate_entity_schemas
      - check_referential_integrity
      - verify_source_availability
      - check_review_requirements
      - run_clinical_tests  # sample patient cohort
```

---

## 18. Governance цього документа

- Зміни в Schema потребують consensus всіх Clinical Co-Leads + Tech Lead
- 14 днів public comment перед major version
- Breaking changes (renaming fields, changing types) — major version bump
- Changelog в CHANGELOG-SCHEMA.md

---

## 19. Поточний статус і обмеження

**v0.1 означає:**
- Skeleton для першого enrolment — HCV-MZL
- Потребує refactoring після first real implementation
- Не валідований на інших нозологіях

**Відомі обмеження:**
- Не моделюються: clinical trial matching (потрібен окремий entity), genetic syndromes (як in germline BRCA), multidisciplinary coordination
- Fine-grained dose modifications — спрощено
- Temporal reasoning (що через скільки) — обмежений
- Interaction з patient preferences — ще не моделюється

**Що треба зробити після v0.1:**
- Реалізувати HCV-MZL в повному обсязі за цією schema
- Порівняти згенерований output з reference document
- Iterate на основі gaps

---

**Pull requests на Schema — welcomed, але через governance CHARTER §6.**
