# Clinical Review Packet

This packet is a signoff-oriented review surface built from existing YAML and source links.
It does not author new clinical claims or modify signoff state.

## DIS-ENDOMETRIAL

- Disease file: `knowledge_base/hosted/content/diseases/endometrial.yaml`
- Name: Endometrial carcinoma
- Queue: `intermediate_family_audit` [medium] for 3 records; Single-record actionable families with IIA/IIB evidence that need clean review packets.
- Shared primary sources: SRC-ESGO-ENDOMETRIAL-2025, SRC-NCCN-UTERINE-2025
- Metadata consistency: ready=3, missing_primary=0, missing_evidence=0, missing_contra=0, guideline_order_mismatch=0

### Record Matrix

| ID | Biomarker | ESCAT | Review | Verified | Primary Sources | Evidence Sources | Path |
|---|---|---|---|---|---|---|---|
| BMA-CTNNB1-ENDOMETRIAL | BIO-CTNNB1 | IIB | pending_clinical_signoff | 2026-05-04 | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | knowledge_base/hosted/content/biomarker_actionability/bma_ctnnb1_endometrial.yaml |
| BMA-FGFR2-MUTATION-ENDOMETRIAL | BIO-FGFR2 | IIA | pending_clinical_signoff | 2026-04-27 | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | SRC-CIVIC | knowledge_base/hosted/content/biomarker_actionability/bma_fgfr2_mutation_endometrial.yaml |
| BMA-PIK3R1-ENDOMETRIAL | BIO-PIK3R1 | IIB | pending_clinical_signoff | 2026-05-04 | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | SRC-NCCN-UTERINE-2025, SRC-ESGO-ENDOMETRIAL-2025 | knowledge_base/hosted/content/biomarker_actionability/bma_pik3r1_endometrial.yaml |

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
py -3.12 -m scripts.normalized_actionability_coverage --review-packet --inventory-disease DIS-ENDOMETRIAL --inventory-queue intermediate_family_audit --compact-json
```

Suggested cheaper-model prompt:
```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --review-packet --inventory-disease DIS-ENDOMETRIAL --inventory-queue intermediate_family_audit --compact-json` as the only input. Produce a source-grounded clinical review packet plan and YAML edit plan. Do not author new clinical claims. Do not edit files.
```
