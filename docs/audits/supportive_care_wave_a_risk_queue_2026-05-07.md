# Supportive-Care Wave A Risk Queue

Generated from `docs/audits/clinical_gap_audit.md` on 2026-05-07.
This is an authoring queue only. It does not add or change safety
instructions.

## Baseline

- 138/302 regimens have mandatory supportive care.
- 120 regimens are missing mandatory supportive care.
- 40 regimens have monitoring.
- 292 regimens have dose adjustments.

## Risk Tiers

| Tier | Meaning |
|---|---|
| 1 | Highest acute safety risk: platinum/taxane, cisplatin, intensive cytotoxic, CAR-T/immune effector |
| 2 | High monitoring burden: targeted oral agents with cardiac, hepatic, QT, ocular, pneumonitis, metabolic, or infection risks |
| 3 | Moderate risk: maintenance biologics, lower-intensity oral therapy, palliative monotherapy |
| 4 | Needs audit clarification before authoring supportive care |

## Wave A Candidates

| Regimen | Provisional tier | Why first |
|---|---:|---|
| `REG-CAR-T-AXICEL-HGBL` | 1 | Immune effector toxicity requires explicit CRS/ICANS/infection monitoring path |
| `REG-CISPLATIN-GEMCITABINE-UROTHELIAL` | 1 | Cisplatin regimen; antiemesis, hydration, renal/electrolyte monitoring likely safety-critical |
| `REG-CISPLATIN-RADIOSENS` | 1 | Concurrent radiation context; renal, antiemesis, hydration, marrow monitoring likely safety-critical |
| `REG-CARBO-PACLI-OVARIAN` | 1 | Platinum/taxane backbone; antiemesis, hypersensitivity, neuropathy, marrow monitoring |
| `REG-CARBOPLATIN-PACLITAXEL-WEEKLY` | 1 | Platinum/taxane weekly schedule; marrow/neuropathy/hypersensitivity coverage |
| `REG-CARBO-GEM-BEV-OVARIAN` | 1 | Platinum/gemcitabine/bevacizumab; marrow, bleeding/thrombosis, BP/proteinuria considerations |
| `REG-CARBO-PLD-BEV-OVARIAN` | 1 | Platinum/anthracycline-like PLD/bevacizumab; hand-foot, cardiac, BP/proteinuria considerations |
| `REG-CAPOX` | 1 | Oxaliplatin/capecitabine; neuropathy, diarrhea, hand-foot, antiemesis |
| `REG-5FU-LV-BEV-CKD-MODIFIED` | 1 | Frail/renal modified regimen plus bevacizumab; access and toxicity edge case |
| `REG-AMIVANTAMAB-LAZERTINIB-NSCLC-2L` | 2 | EGFR/MET antibody + TKI; infusion reaction, rash, VTE, ocular/pulmonary monitoring |
| `REG-AMIVANTAMAB-MONO-NSCLC-EX20INS` | 2 | Infusion reaction/rash/pulmonary monitoring burden |
| `REG-ALPELISIB-FULVESTRANT-BREAST` | 2 | Hyperglycemia/rash/diarrhea monitoring burden |
| `REG-CAPIVASERTIB-FULVESTRANT-BREAST` | 2 | Hyperglycemia/rash/diarrhea monitoring burden |
| `REG-ADAGRASIB-NSCLC` | 2 | GI, hepatic, QT, drug-interaction monitoring burden |
| `REG-ALECTINIB-NSCLC` | 2 | Hepatic, CPK, bradycardia, pneumonitis monitoring burden |
| `REG-CAPMATINIB-NSCLC` | 2 | Edema, hepatic, pulmonary toxicity monitoring burden |
| `REG-CABOZANTINIB-MTC-1L` | 2 | Hypertension, bleeding, wound healing, diarrhea, hepatic/thyroid monitoring |
| `REG-AVAPRITINIB-GIST-1L` | 2 | Cognitive/bleeding/cytopenia monitoring burden |
| `REG-AVAPRITINIB-ADVSM-1L` | 2 | Cytopenia/bleeding/cognitive monitoring burden |
| `REG-CRIZOTINIB-IMT` | 2 | Visual, hepatic, QT/bradycardia, pulmonary monitoring burden |

## Authoring Rule

For each regimen, author or reuse:

- `mandatory_supportive_care`
- `monitoring_schedule_id`
- patient-facing `between_visit_watchpoints`
- source refs for safety claims

## Guardrails

- Do not delete existing dose-adjustment content.
- Do not invent supportive-care instructions from memory.
- Prefer linking existing `supportive_care` and `monitoring` entities.
- If a needed supportive-care entity is absent, create it as `draft: true`
  with source refs and review notes.

## Next Command When Python Is Available

```powershell
python scripts/audit_clinical_gaps.py
```

Then regenerate this queue from the full 120-regimen list, not just the
visible top section in the current markdown.
