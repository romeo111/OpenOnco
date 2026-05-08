# Generated Normalized Fill Chunk Specs

These are compact task skeletons for low-token delegation. They intentionally avoid clinical claims.
Each chunk should be filled only from existing or newly ingested source-grounded `SRC-*` evidence.

## Chunk 1: DIS-GBM

- Tier: `major_solid`
- Score: `46`
- Review readiness: `35.2%`
- Workflow lane: `fill_first`
- Current: `SOC/IND/REG/Drug/RF = 1/4/1/1/5`
- Gaps: `SOC 1, IND 6, REG 7, Drug 7, RF 2`
- Recommended work: Create or backfill 3 linked regimen records referenced by existing indications.
- Quality flags: `signoff_cold, indication_signoff_cold, low_tier_dominant, missing_regimen_records`

Scope:
- Inventory existing disease-specific YAML before authoring.
- Prefer indication/regimen/drug/redflag fill when the disease is not biomarker-driven.
- Add BMA only for a real guideline-backed actionable biomarker family, or document why no biomarker axis is appropriate.
- Do not copy NSCLC-style variant splitting unless resistance/variant handling is clinically required and source-grounded.

Low-token inventory commands:
```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-GBM --compact-json
```

Validation:
```powershell
py -3.12 -m knowledge_base.validation.loader knowledge_base/hosted/content
py -3.12 -m pytest tests/test_normalized_actionability_coverage.py
py -3.12 -m scripts.normalized_actionability_coverage --rank-fill-next --disease DIS-GBM --compact-json
```

Suggested cheaper-model prompt:
```text
Switch to GPT-5.4-Mini medium. For DIS-GBM, do inventory/skeleton only: existing YAML paths, source IDs, normalized gaps, and validation commands. Do not author clinical claims or edit YAML.
```
