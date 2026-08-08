# Clinical gap audit

Generated: `2026-08-08T08:06:35Z`

This is a coverage/governance audit, not a clinical recommendation set.
It makes the five largest known gaps measurable and repeatable.

## Summary

| Gap | Current | Target | Status |
|---|---:|---|---|
| Clinical sign-off | 15/2614 signoff-eligible entities reviewed (0.6%) | >=85% reviewed before public guideline-grade claims | `blocked_on_reviewers` |
| Solid tumor 2L+ coverage | 23/67 solid diseases have a 2L+ algorithm; 26/67 have a 2L+ indication | Every modeled solid disease has at least one advanced/relapsed-line algorithm and indication. | `coverage_gap` |
| Surgery/radiation detail | 21 structured procedure entities; 9 structured radiation-course entities; 816 indications mention surgery/radiation in text | Dedicated modality entities for surgery and radiation with dose/fraction/intent/timing fields. | `coverage_gap` |
| Supportive-care depth | 136/404 regimens have mandatory supportive care (33.7%); 43 have monitoring; 358 have dose adjustments | Every active regimen has supportive care, monitoring, dose-adjustment, and patient-watchpoint coverage. | `coverage_gap` |
| Drug indication and off-label tracking | 1/862 inferred drug-disease-indication pairs have a first-class record; 1 carry a source-backed assessed status | Every drug-use pair has explicit regulatory-label status, NCCN/ESMO category, and source provenance. | `coverage_gap` |

## Next actions

### Clinical sign-off

- Blocker: Cannot be fixed by code; requires qualified Clinical Co-Lead review.
- Next action: Batch the largest STUB queues by entity type and assign reviewer owners.

### Solid tumor 2L+ coverage

- Blocker: Missing disease-by-disease 2L+ algorithm/indication authoring queue.
- Next action: Prioritize missing high-volume solid diseases, then rare solid diseases.
- Missing 2L+ algorithm rows: 44
  - `DIS-ADRENOCORTICAL-CARCINOMA`: Adrenocortical carcinoma
  - `DIS-ANAL-SCC`: Anal squamous cell carcinoma (Anal SCC)
  - `DIS-ATRT`: Atypical teratoid/rhabdoid tumor
  - `DIS-BCC`: Basal cell carcinoma
  - `DIS-CERVICAL`: Cervical carcinoma
  - `DIS-CHONDROSARCOMA`: Chondrosarcoma
  - `DIS-CHOROID-PLEXUS-CARCINOMA`: Choroid plexus carcinoma
  - `DIS-CYSTIC-NEPHROMA`: Cystic nephroma
  - `DIS-EPITHELIOID-SARCOMA`: Epithelioid sarcoma
  - `DIS-GI-NET`: GI neuroendocrine tumor (carcinoid)
  - `DIS-GLIOMA-LOW-GRADE`: Low-grade glioma
  - `DIS-GRANULOSA-CELL`: Adult granulosa cell tumor
  - `DIS-HEPATOBLASTOMA`: Hepatoblastoma
  - `DIS-IFS`: Infantile fibrosarcoma
  - `DIS-IMT`: Inflammatory myofibroblastic tumor
  - `DIS-KAPOSI`: Kaposi sarcoma
  - `DIS-LAM`: Lymphangioleiomyomatosis
  - `DIS-LARYNGEAL`: Laryngeal squamous cell carcinoma
  - `DIS-LEIOMYOSARCOMA`: Leiomyosarcoma
  - `DIS-MEDULLOBLASTOMA`: Medulloblastoma
  - `DIS-MENINGIOMA`: Meningioma
  - `DIS-MPNST`: Malignant peripheral nerve sheath tumor
  - `DIS-MTC`: Medullary thyroid carcinoma
  - `DIS-NEUROBLASTOMA`: Neuroblastoma
  - `DIS-NPC`: Nasopharyngeal carcinoma

### Surgery/radiation detail

- Blocker: The modality schemas and initial entities exist, but many indication-level references remain prose-only.
- Next action: Prioritize high-volume prose mentions; attach an existing or newly verified procedure/radiation-course entity to each reviewed indication phase.

### Supportive-care depth

- Blocker: Supportive-care records exist, but regimen attachment is incomplete.
- Next action: Audit high-toxicity regimens first, then fill missing regimen attachments.
- Regimens missing mandatory supportive care: 120 shown below
  - `REG-2GEN-TKI-CML`
  - `REG-5FU-LV-BEV-CKD-MODIFIED`
  - `REG-ABEMACICLIB-ADJUVANT`
  - `REG-ACALABRUTINIB-CONTINUOUS`
  - `REG-ACALABRUTINIB-MCL`
  - `REG-ACALABRUTINIB-RITUXIMAB`
  - `REG-ADAGRASIB-NSCLC`
  - `REG-ALECTINIB-NSCLC`
  - `REG-ALLOHCT-JMML`
  - `REG-ALPELISIB-FULVESTRANT-BREAST`
  - `REG-ALPHA-BLOCKADE-PREOP-PHEO`
  - `REG-AMI-LAZ-NSCLC`
  - `REG-AMIVANTAMAB-LAZERTINIB-NSCLC-2L`
  - `REG-AMIVANTAMAB-MONO-NSCLC-EX20INS`
  - `REG-ANAGRELIDE-ET`
  - `REG-ASCIMINIB-CML`
  - `REG-ATEZO-ADJUVANT-NSCLC`
  - `REG-ATEZO-BEV`
  - `REG-AVAPRITINIB-ADVSM-1L`
  - `REG-AVAPRITINIB-GIST-1L`
  - `REG-AVELUMAB-MAINTENANCE`
  - `REG-AVELUMAB-MONO-NK-T`
  - `REG-BELZUTIFAN-MONO`
  - `REG-BEMARITUZUMAB-MFOLFOX6`
  - `REG-BEP-GCT`
  - `REG-BEV-MAINTENANCE-OVARIAN`
  - `REG-BEVACIZUMAB-GBM`
  - `REG-BEXAROTENE-MAINTENANCE-CTCL`
  - `REG-BEXAROTENE-MONO-CTCL`
  - `REG-BV-MONO-MF`
  - `REG-CABAZITAXEL-MCRPC`
  - `REG-CABERGOLINE-PROLACTINOMA`
  - `REG-CABOZANTINIB-HCC`
  - `REG-CABOZANTINIB-MTC-1L`
  - `REG-CABOZANTINIB-PHEO`
  - `REG-CABOZANTINIB-RCC`
  - `REG-CAPE-BEV-MAINTENANCE`
  - `REG-CAPECITABINE-CRT-CONCURRENT`
  - `REG-CAPECITABINE-PALLIATIVE`
  - `REG-CAPIVASERTIB-FULVESTRANT-BREAST`

### Drug indication and off-label tracking

- Blocker: The first-class model is present, but most regimen-derived drug-use pairs still need source-backed assessment.
- Next action: Backfill high-volume and high-risk pairs from current regulatory labels first; keep uncertain pairs explicitly not_assessed until verified.
- Inferred pairs to backfill: 862
- First-class records: 1; source-backed assessed statuses: 1; explicitly not assessed: 0

## Machine-readable outputs

- `docs/audits/clinical_gap_audit.json`
- `docs/audits/clinical_gap_audit.md`
- `docs/clinical-gaps.html`
