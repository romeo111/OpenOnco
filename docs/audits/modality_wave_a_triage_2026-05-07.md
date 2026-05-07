# Modality Structure Wave A Triage

Generated manually from local YAML grep on 2026-05-07 because Python is
not available in this sandbox. This is a triage queue only; do not convert
keyword hits into surgery/radiation entities without specialist review and
source anchoring.

## Scope

Wave A from `docs/plans/audit_remediation_deep_plan_2026-05-07.md`:
CRC, breast, NSCLC, ovarian, cervical, and anal.

## High-Confidence Candidates

| Candidate | Modality | Evidence in current YAML | Next safe action |
|---|---|---|---|
| `IND-ANAL-SCC-LA-1L-NIGRO-CRT` | radiation + salvage surgery | Mentions definitive concurrent CRT, EBRT 50.4 Gy, IMRT preference, and salvage APR after confirmed CRT failure | Radiation oncology review for definitive CRT record; colorectal surgery review for salvage APR record |
| `IND-CERVICAL-LOCALLY-ADVANCED-CRT` | radiation | Mentions cisplatin + RT, brachytherapy boost, and completion of CRT in <8 weeks | Radiation oncology review for EBRT + brachytherapy record |
| `IND-NSCLC-STAGE-III-PACIFIC` | radiation context | Mentions unresectable stage III post-concurrent CRT and pneumonitis exclusion before durvalumab | Radiation oncology review for prerequisite CRT record |
| `IND-CRC-ADJUVANT-STAGE2-HIGHRISK-FOLFOX` | surgery context | Stage II colon cancer post-curative R0 resection; post-surgical complication and timing language | Colorectal surgery review for disease-level colectomy/resection prerequisite record |
| `IND-CRC-ADJUVANT-STAGE3-CAPOX` | surgery context | Stage III colon cancer post-curative R0 resection and post-resection baseline CEA | Colorectal surgery review for disease-level colectomy/resection prerequisite record |
| `IND-CRC-ADJUVANT-STAGE3-FOLFOX` | surgery context | Stage III post-curative resection and adjuvant timing after surgery | Colorectal surgery review for disease-level colectomy/resection prerequisite record |
| `IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-NEG` | surgery context | Mentions suboptimal debulking red flag and bevacizumab timing after major surgery | Gynecologic oncology review for cytoreduction/debulking prerequisite record |
| `IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-OLAP` | surgery context | Mentions suboptimal debulking red flag | Gynecologic oncology review for cytoreduction/debulking prerequisite record |

## Guardrails

- Author no dose/fractionation unless it is present in a cited source.
- Keep new modality records `draft: true`.
- Link records to `indication_ids` only when the modality is truly part of
  that clinical context.
- Do not change engine treatment-selection behavior.

## Next Command When Python Is Available

```powershell
python scripts/audit_modality_structure.py
```

Expected output:

`docs/audits/modality_structure_audit.json`
