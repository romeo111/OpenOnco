# Solid Tumor 2L+ Coverage Queue

Generated from `docs/audits/clinical_gap_audit.md` on 2026-05-07.
This is a provisional authoring queue, not clinical content. Each lane must
be verified against disease-specific sources before adding indications or
algorithms.

## Baseline

- 21/42 solid diseases have a 2L+ algorithm.
- 18/42 solid diseases have a 2L+ indication.

## Lane Definitions

| Lane | Meaning |
|---|---|
| A | Systemic 2L+ standard likely needed |
| B | Biomarker/targeted 2L+ pathway likely needed |
| C | Local-therapy or surgery/radiation-dominant recurrence pathway likely needed |
| D | Sparse evidence; explicit trial/referral/supportive-care state may be safer than a regimen recommendation |

## Provisional Disease Queue

| Disease | Provisional lane | First authoring question |
|---|---|---|
| `DIS-CERVICAL` | A | Does the current 2L tisotumab row need an algorithm link and alternatives after platinum/pembrolizumab? |
| `DIS-GIST` | B | Which post-imatinib / post-sunitinib targeted sequence is source-backed in this KB version? |
| `DIS-MTC` | B | Which RET-targeted or multikinase path should be default after progression? |
| `DIS-PNET` | A | Which somatostatin/targeted/chemotherapy sequence should define advanced-line state? |
| `DIS-SALIVARY` | B | Which HER2, AR, NTRK, or other biomarker-selected options deserve explicit paths? |
| `DIS-BCC` | A | Which hedgehog-inhibitor and PD-1 sequencing paths are source-backed? |
| `DIS-TGCT` | A | Is CSF1R-targeted systemic therapy modeled, or should recurrence remain local/surgical? |
| `DIS-IMT` | B | Which ALK/NTRK/ROS1-targeted path is source-backed after recurrence/progression? |
| `DIS-IFS` | B | Which NTRK-fusion targeted path is appropriate and age-scoped? |
| `DIS-ANAL-SCC` | A/C | Separate metastatic systemic line from definitive CRT/salvage APR local path. |
| `DIS-GLIOMA-LOW-GRADE` | A/C | Separate systemic options from surgery/radiation sequencing and surveillance. |
| `DIS-MENINGIOMA` | C/D | Decide if recurrent disease should model surgery/radiation first with trial referral for systemic therapy. |
| `DIS-MESOTHELIOMA` | A | Add relapsed systemic pathway if source-backed. |
| `DIS-THYROID-ANAPLASTIC` | B/D | Separate BRAF-targeted path from non-actionable urgent trial/supportive-care state. |
| `DIS-THYROID-PAPILLARY` | B | Add radioiodine-refractory targeted sequencing if source-backed. |
| `DIS-CHONDROSARCOMA` | C/D | Determine whether explicit systemic 2L is appropriate or trial/referral is safer. |
| `DIS-EPITHELIOID-SARCOMA` | B/D | Verify EZH2-targeted or systemic recurrence path. |
| `DIS-GI-NET` | A/B | Clarify SSA/PRRT/everolimus/sunitinib sequencing by site/grade. |
| `DIS-GRANULOSA-CELL` | D | Likely needs specialist review before algorithm authoring. |
| `DIS-LAM` | D | Confirm whether this belongs in oncology treatment-line coverage or should be deferred. |
| `DIS-MPNST` | D | Sparse evidence; likely trial/referral-centered advanced-line state. |

## Wave A Starter Set

Start with one disease per chunk:

1. `DIS-CERVICAL`
2. `DIS-GIST`
3. `DIS-MTC`
4. `DIS-PNET`
5. `DIS-SALIVARY`

## Quality Gate

- New advanced-line indication has source refs and expected outcomes.
- New algorithm references valid indication IDs.
- If no systemic standard exists, add an explicit sourced deferral state
  instead of leaving a silent blank.
- Rerun `scripts/audit_clinical_gaps.py` and `scripts/kb_coverage_matrix.py`
  when Python is available.
