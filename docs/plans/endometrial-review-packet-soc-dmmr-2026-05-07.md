# Clinical Review Packet

This packet is a signoff-oriented review surface built from existing YAML and source links.
It does not author new clinical claims or modify signoff state.

## DIS-ENDOMETRIAL

- Disease file: `knowledge_base/hosted/content/diseases/endometrial.yaml`
- Name: Endometrial carcinoma
- Queue: `soc_dmmr_family` [high] for 9 records; Largest family block; IA evidence; highest review leverage.
- Shared primary sources: SRC-ESGO-ENDOMETRIAL-2025, SRC-NCCN-UTERINE-2025
- Metadata consistency: ready=9, missing_primary=0, missing_evidence=0, missing_contra=0, guideline_order_mismatch=0

### Record Matrix

| ID | Biomarker | ESCAT | Review | Verified | Primary Sources | Evidence Sources | Path |
|---|---|---|---|---|---|---|---|
| BMA-EPCAM-GERMLINE-ENDOMETRIAL | BIO-DMMR-IHC | IA | pending_clinical_signoff | 2026-04-27 | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | SRC-CIVIC | knowledge_base/hosted/content/biomarker_actionability/bma_epcam_germline_endometrial.yaml |
| BMA-MLH1-GERMLINE-ENDOMETRIAL | BIO-DMMR-IHC | IA | pending_clinical_signoff | 2026-04-27 | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | SRC-CIVIC | knowledge_base/hosted/content/biomarker_actionability/bma_mlh1_germline_endometrial.yaml |
| BMA-MLH1-SOMATIC-ENDOMETRIAL | BIO-DMMR-IHC | IA | pending_clinical_signoff | 2026-04-27 | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | SRC-CIVIC | knowledge_base/hosted/content/biomarker_actionability/bma_mlh1_somatic_endometrial.yaml |
| BMA-MSH2-GERMLINE-ENDOMETRIAL | BIO-DMMR-IHC | IA | pending_clinical_signoff | 2026-04-27 | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | SRC-CIVIC | knowledge_base/hosted/content/biomarker_actionability/bma_msh2_germline_endometrial.yaml |
| BMA-MSH2-SOMATIC-ENDOMETRIAL | BIO-DMMR-IHC | IA | pending_clinical_signoff | 2026-04-27 | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | SRC-CIVIC | knowledge_base/hosted/content/biomarker_actionability/bma_msh2_somatic_endometrial.yaml |
| BMA-MSH6-GERMLINE-ENDOMETRIAL | BIO-DMMR-IHC | IA | pending_clinical_signoff | 2026-04-27 | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | SRC-CIVIC | knowledge_base/hosted/content/biomarker_actionability/bma_msh6_germline_endometrial.yaml |
| BMA-MSH6-SOMATIC-ENDOMETRIAL | BIO-DMMR-IHC | IA | pending_clinical_signoff | 2026-04-27 | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | SRC-CIVIC | knowledge_base/hosted/content/biomarker_actionability/bma_msh6_somatic_endometrial.yaml |
| BMA-PMS2-GERMLINE-ENDOMETRIAL | BIO-DMMR-IHC | IA | pending_clinical_signoff | 2026-04-27 | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | SRC-CIVIC | knowledge_base/hosted/content/biomarker_actionability/bma_pms2_germline_endometrial.yaml |
| BMA-PMS2-SOMATIC-ENDOMETRIAL | BIO-DMMR-IHC | IA | pending_clinical_signoff | 2026-04-27 | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | SRC-CIVIC | knowledge_base/hosted/content/biomarker_actionability/bma_pms2_somatic_endometrial.yaml |

### Linked Context

- Indications: IND-ENDOMETRIAL-2L-DOSTARLIMAB-DMMR, IND-ENDOMETRIAL-2L-PEMBRO-LENVA-PMMR, IND-ENDOMETRIAL-ADVANCED-1L-DOSTARLIMAB-CHEMO, IND-ENDOMETRIAL-ADVANCED-1L-PEMBRO-CHEMO, IND-ENDOMETRIAL-STAGE-I-POLE-OBSERVATION
- Regimens: REG-DOSTARLIMAB-CARBO-PACLI-ENDOM, REG-DOSTARLIMAB-MONO-ENDOM, REG-PEMBRO-CARBO-PACLI-ENDOM, REG-PEMBRO-LENVATINIB-ENDOM
- Source IDs: SRC-CIVIC, SRC-CTCAE-V5, SRC-ESGO-ENDOMETRIAL-2025, SRC-GY018-MAKKER-2022, SRC-NCCN-UTERINE-2025, SRC-RUBY-MIRZA-2023

### Review Tasks

- Confirm claim language against the already-cited guideline and study sources.
- Preserve `pending_clinical_signoff` and `actionability_review_required` until clinician review is complete.
- Use metadata-ready status to avoid reopening structural cleanup unless the reviewer requests it.

### Low-Token Command

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --review-packet --inventory-disease DIS-ENDOMETRIAL --inventory-queue soc_dmmr_family --compact-json
```

Suggested cheaper-model prompt:
```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --review-packet --inventory-disease DIS-ENDOMETRIAL --inventory-queue soc_dmmr_family --compact-json` as the only input. Produce a source-grounded clinical review packet plan and YAML edit plan. Do not author new clinical claims. Do not edit files.
```
