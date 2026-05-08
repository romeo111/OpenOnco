# Fill Lane Runbook Top 5

This runbook covers the current top five `fill_first` diseases from the normalized backlog.
It is source-grounded planning only. Do not use it to author new clinical claims.

## Queue Order

1. `DIS-ENDOMETRIAL`
2. `DIS-GBM`
3. `DIS-HNSCC`
4. `DIS-RCC`
5. `DIS-HCC`

## 1. DIS-ENDOMETRIAL

- Readiness: `44.0%`
- Score: `51`
- Main gap: `SOC 5 / IND 5 / REG 4 / Drug 3 / RF 0`
- Inventory doc: `docs/plans/endometrial-normalized-fill-inventory-2026-05-08.md`
- Execution doc: `docs/plans/endometrial-fill-execution-plan-2026-05-08.md`

Command:

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-ENDOMETRIAL --compact-json
```

Suggested cheaper-model prompt:

```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-ENDOMETRIAL --compact-json` as the only input. Produce a source-grounded fill execution plan focused on SOC/IND/REG/Drug gaps. Do not author clinical claims. Do not edit files.
```

## 2. DIS-GBM

- Readiness: `35.2%`
- Score: `46`
- Main gap: `SOC 1 / IND 6 / REG 7 / Drug 7 / RF 2`
- Inventory doc: `docs/plans/gbm-normalized-fill-inventory-2026-05-08.md`

Command:

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-GBM --compact-json
```

Suggested cheaper-model prompt:

```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-GBM --compact-json` as the only input. Produce a source-grounded fill execution plan focused first on backfilling the 3 missing linked regimen records, then on truthful SOC/IND/REG/Drug additions. Do not author clinical claims. Do not edit files.
```

## 3. DIS-HNSCC

- Readiness: `49.3%`
- Score: `40`
- Main gap: `SOC 2 / IND 5 / REG 3 / Drug 3 / RF 2`
- Inventory doc: `docs/plans/hnscc-normalized-fill-inventory-2026-05-08.md`

Command:

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-HNSCC --compact-json
```

Suggested cheaper-model prompt:

```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-HNSCC --compact-json` as the only input. Produce a source-grounded fill execution plan focused on whether HNSCC needs actionable biomarker families or explicit no-biomarker documentation first. Do not author clinical claims. Do not edit files.
```

## 4. DIS-RCC

- Readiness: `61.5%`
- Score: `35`
- Main gap: `SOC 5 / IND 2 / REG 1 / Drug 1 / RF 1`
- Inventory doc: `docs/plans/rcc-normalized-fill-inventory-2026-05-08.md`

Command:

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-RCC --compact-json
```

Suggested cheaper-model prompt:

```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-RCC --compact-json` as the only input. Produce a source-grounded fill execution plan focused on missing SOC/actionable biomarker families and the minimum IND/REG/Drug closure needed next. Do not author clinical claims. Do not edit files.
```

## 5. DIS-HCC

- Readiness: `57.7%`
- Score: `30`
- Main gap: `SOC 2 / IND 4 / REG 2 / Drug 3 / RF 1`
- Inventory doc: `docs/plans/hcc-normalized-fill-inventory-2026-05-08.md`

Command:

```powershell
py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-HCC --compact-json
```

Suggested cheaper-model prompt:

```text
Switch to GPT-5.4-Mini medium. Use `py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-HCC --compact-json` as the only input. Produce a source-grounded fill execution plan focused on the next credible SOC/IND/REG/Drug additions. Do not author clinical claims. Do not edit files.
```

## Validation

```powershell
py -3.12 -m pytest tests/test_normalized_actionability_coverage.py
py -3.12 -m scripts.normalized_actionability_coverage --rank-fill-next --workflow-lane fill_first --compact-json
py -3.12 -m scripts.normalized_actionability_coverage --rank-fill-next --workflow-lane review_ready --compact-json
```
