# Generated Normalized Fill Chunk Specs

These are compact task skeletons for low-token delegation. They intentionally avoid clinical claims.
Each chunk should be filled only from existing or newly ingested source-grounded `SRC-*` evidence.

## Chunk 1: DIS-ENDOMETRIAL

- Tier: `major_solid`
- Score: `51`
- Review readiness: `44.0%`
- Workflow lane: `fill_first`
- Current: `SOC/IND/REG/Drug/RF = 1/5/4/5/7`
- Gaps: `SOC 5, IND 5, REG 4, Drug 3, RF 0`
- Recommended work: Add 5 guideline-backed SOC/actionable biomarker family or document no biomarker axis.
- Quality flags: `signoff_cold, low_tier_dominant`

Scope:
- Inventory existing disease-specific YAML before authoring.
- Prefer indication/regimen/drug/redflag fill when the disease is not biomarker-driven.
- Add BMA only for a real guideline-backed actionable biomarker family, or document why no biomarker axis is appropriate.
- Do not copy NSCLC-style variant splitting unless resistance/variant handling is clinically required and source-grounded.

Low-token inventory commands:
```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-ENDOMETRIAL --compact-json
```

Validation:
```powershell
py -3.12 -m knowledge_base.validation.loader knowledge_base/hosted/content
py -3.12 -m pytest tests/test_normalized_actionability_coverage.py
py -3.12 -m scripts.normalized_actionability_coverage --rank-fill-next --disease DIS-ENDOMETRIAL --compact-json
```

Suggested cheaper-model prompt:
```text
Switch to GPT-5.4-Mini medium. For DIS-ENDOMETRIAL, do inventory/skeleton only: existing YAML paths, source IDs, normalized gaps, and validation commands. Do not author clinical claims or edit YAML.
```
