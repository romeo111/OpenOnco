# Citation verification sweep — 2026-04-27

Read-only audit (no YAMLs modified). Triage input for clinical co-leads.


## Summary

- Source yamls indexed: **162**
- Total entities checked: **785**
  - BiomarkerActionability (BMA): 376
  - Indications: 223
  - Regimens: 186

### Counters by severity

- YAML parse errors (entity could not be evaluated): **0**
- Broken citations (primary_sources entry not found in `sources/`): **0**
- Missing trial sources (trial named in evidence_summary/notes but no matching SRC-*): **352**
- Missing regulatory sources (FDA/EMA approval cited without an FDA/EMA Source entity): **153**
- ESCAT vs OncoKB level mismatches: **124**
- recommended_combinations vs regulatory_approval drug inconsistencies: **285**

### Counters by entity kind

- Findings on BMA: 696
- Findings on Indication: 129
- Findings on Regimen: 89
- Total findings: **914**
- Entities with at least one finding: **464**

## Top 20 most-impactful gaps

Ordered by (worst severity first, then highest finding count). Use this list for Source-stub triage.

| # | Entity | Kind | Worst severity | Findings | First-line note |
|---|--------|------|----------------|----------|-----------------|
| 1 | `BMA-TP53-MUT-CLL` | BMA | missing-trial-source | 6 | trial 'CLL14' mentioned but no matching source citation (looked for substrings: ['CLL14', 'VENETOCLAX']) |
| 2 | `BMA-BCR-ABL1-P210-BALL` | BMA | missing-trial-source | 5 | trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM']) |
| 3 | `BMA-BRCA1-GERMLINE-OVARIAN` | BMA | missing-trial-source | 5 | trial 'SOLO1' mentioned but no matching source citation (looked for substrings: ['SOLO', 'OLAPARIB']) |
| 4 | `BMA-BRCA1-GERMLINE-PROSTATE` | BMA | missing-trial-source | 5 | trial 'PROpel' mentioned but no matching source citation (looked for substrings: ['PROPEL', 'OLAPARIB-PROST']) |
| 5 | `BMA-BRCA2-GERMLINE-BREAST` | BMA | missing-trial-source | 5 | trial 'OLYMPIA' mentioned but no matching source citation (looked for substrings: ['OLYMPIA', 'OLAPARIB']) |
| 6 | `BMA-BRCA2-GERMLINE-PROSTATE` | BMA | missing-trial-source | 5 | trial 'PROpel' mentioned but no matching source citation (looked for substrings: ['PROPEL', 'OLAPARIB-PROST']) |
| 7 | `BMA-EGFR-C797S-NSCLC` | BMA | missing-trial-source | 5 | trial 'MARIPOSA' mentioned but no matching source citation (looked for substrings: ['MARIPOSA']) |
| 8 | `BMA-EGFR-EX19DEL-NSCLC` | BMA | missing-trial-source | 5 | trial 'FLAURA' mentioned but no matching source citation (looked for substrings: ['FLAURA', 'OSIMERTINIB', 'AURA']) |
| 9 | `BMA-EGFR-L858R-NSCLC` | BMA | missing-trial-source | 5 | trial 'FLAURA' mentioned but no matching source citation (looked for substrings: ['FLAURA', 'OSIMERTINIB', 'AURA']) |
| 10 | `BMA-MLH1-GERMLINE-ENDOMETRIAL` | BMA | missing-trial-source | 5 | trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB']) |
| 11 | `BMA-MLH1-SOMATIC-ENDOMETRIAL` | BMA | missing-trial-source | 5 | trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB']) |
| 12 | `BMA-MSH2-GERMLINE-ENDOMETRIAL` | BMA | missing-trial-source | 5 | trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB']) |
| 13 | `BMA-MSH2-SOMATIC-ENDOMETRIAL` | BMA | missing-trial-source | 5 | trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB']) |
| 14 | `BMA-MSH6-GERMLINE-ENDOMETRIAL` | BMA | missing-trial-source | 5 | trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB']) |
| 15 | `BMA-MSH6-SOMATIC-ENDOMETRIAL` | BMA | missing-trial-source | 5 | trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB']) |
| 16 | `BMA-NOTCH1-ACTIVATING-CLL` | BMA | missing-trial-source | 5 | trial 'CLL14' mentioned but no matching source citation (looked for substrings: ['CLL14', 'VENETOCLAX']) |
| 17 | `BMA-PMS2-GERMLINE-ENDOMETRIAL` | BMA | missing-trial-source | 5 | trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB']) |
| 18 | `BMA-PMS2-SOMATIC-ENDOMETRIAL` | BMA | missing-trial-source | 5 | trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB']) |
| 19 | `BMA-RAD51B-GERMLINE-OVARIAN` | BMA | missing-trial-source | 5 | trial 'PAOLA-1' mentioned but no matching source citation (looked for substrings: ['PAOLA', 'OLAPARIB']) |
| 20 | `BMA-RAD51C-GERMLINE-OVARIAN` | BMA | missing-trial-source | 5 | trial 'PAOLA-1' mentioned but no matching source citation (looked for substrings: ['PAOLA', 'OLAPARIB']) |

## Per-entity findings

Severity precedence: yaml-parse-error > broken-citation > missing-trial-source / missing-regulatory-source > level-mismatch > drug-inconsistency > suggestion.

### `BMA-TP53-MUT-CLL` (BMA — `bma_tp53_mut_cll.yaml`)
- **[missing-trial-source]** trial 'CLL14' mentioned but no matching source citation (looked for substrings: ['CLL14', 'VENETOCLAX'])
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3A'
- **[drug-inconsistency]** recommended_combination 'acalabrutinib monotherapy' contains drug name(s) ['acalabrutinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'zanubrutinib monotherapy' contains drug name(s) ['zanubrutinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'venetoclax + obinutuzumab (CLL14)' contains drug name(s) ['venetoclax', 'obinutuzumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'BTKi + venetoclax (CAPTIVATE / GLOW)' contains drug name(s) ['btki', 'venetoclax'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BCR-ABL1-P210-BALL` (BMA — `bma_bcr_abl1_p210_ball.yaml`)
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '2'
- **[drug-inconsistency]** recommended_combination 'ponatinib + hyper-CVAD' contains drug name(s) ['hyper-cvad'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'dasatinib + blinatumomab' contains drug name(s) ['blinatumomab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRCA1-GERMLINE-OVARIAN` (BMA — `bma_brca1_germline_ovarian.yaml`)
- **[missing-trial-source]** trial 'SOLO1' mentioned but no matching source citation (looked for substrings: ['SOLO', 'OLAPARIB'])
- **[missing-trial-source]** trial 'PAOLA-1' mentioned but no matching source citation (looked for substrings: ['PAOLA', 'OLAPARIB'])
- **[missing-trial-source]** trial 'ARIEL3' mentioned but no matching source citation (looked for substrings: ['ARIEL3'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab (PAOLA-1, HRD+)' contains drug name(s) ['bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRCA1-GERMLINE-PROSTATE` (BMA — `bma_brca1_germline_prostate.yaml`)
- **[missing-trial-source]** trial 'PROpel' mentioned but no matching source citation (looked for substrings: ['PROPEL', 'OLAPARIB-PROST'])
- **[missing-trial-source]** trial 'MAGNITUDE' mentioned but no matching source citation (looked for substrings: ['MAGNITUDE', 'NIRAPARIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (5) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'olaparib + abiraterone + prednisone (1L)' contains drug name(s) ['prednisone'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'niraparib + abiraterone + prednisone (1L)' contains drug name(s) ['prednisone'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRCA2-GERMLINE-BREAST` (BMA — `bma_brca2_germline_breast.yaml`)
- **[missing-trial-source]** trial 'OLYMPIA' mentioned but no matching source citation (looked for substrings: ['OLYMPIA', 'OLAPARIB'])
- **[missing-trial-source]** trial 'OLYMPIAD' mentioned but no matching source citation (looked for substrings: ['OLYMPIAD', 'OLAPARIB'])
- **[missing-trial-source]** trial 'EMBRACA' mentioned but no matching source citation (looked for substrings: ['EMBRACA', 'TALAZOPARIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (3) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'platinum-based chemo (TNBC)' contains drug name(s) ['platinum-based'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRCA2-GERMLINE-PROSTATE` (BMA — `bma_brca2_germline_prostate.yaml`)
- **[missing-trial-source]** trial 'PROpel' mentioned but no matching source citation (looked for substrings: ['PROPEL', 'OLAPARIB-PROST'])
- **[missing-trial-source]** trial 'MAGNITUDE' mentioned but no matching source citation (looked for substrings: ['MAGNITUDE', 'NIRAPARIB'])
- **[missing-trial-source]** trial 'TALAPRO-2' mentioned but no matching source citation (looked for substrings: ['TALAPRO', 'TALAZOPARIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'rucaparib monotherapy' contains drug name(s) ['rucaparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-EGFR-C797S-NSCLC` (BMA — `bma_egfr_c797s_nsclc.yaml`)
- **[missing-trial-source]** trial 'MARIPOSA' mentioned but no matching source citation (looked for substrings: ['MARIPOSA'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IIB typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level 'R2'
- **[drug-inconsistency]** recommended_combination 'amivantamab + carboplatin + pemetrexed (MARIPOSA-2)' contains drug name(s) ['carboplatin', 'pemetrexed'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'platinum-doublet chemotherapy' contains drug name(s) ['platinum-doublet'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-EGFR-EX19DEL-NSCLC` (BMA — `bma_egfr_ex19del_nsclc.yaml`)
- **[missing-trial-source]** trial 'FLAURA' mentioned but no matching source citation (looked for substrings: ['FLAURA', 'OSIMERTINIB', 'AURA'])
- **[missing-trial-source]** trial 'ADAURA' mentioned but no matching source citation (looked for substrings: ['ADAURA', 'OSIMERTINIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'osimertinib + pemetrexed/platinum (FLAURA2 regimen)' contains drug name(s) ['pemetrexed'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'amivantamab + lazertinib (MARIPOSA, 1L alternative)' contains drug name(s) ['amivantamab', 'lazertinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-EGFR-L858R-NSCLC` (BMA — `bma_egfr_l858r_nsclc.yaml`)
- **[missing-trial-source]** trial 'FLAURA' mentioned but no matching source citation (looked for substrings: ['FLAURA', 'OSIMERTINIB', 'AURA'])
- **[missing-trial-source]** trial 'ADAURA' mentioned but no matching source citation (looked for substrings: ['ADAURA', 'OSIMERTINIB'])
- **[missing-trial-source]** trial 'MARIPOSA' mentioned but no matching source citation (looked for substrings: ['MARIPOSA'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'osimertinib + pemetrexed/platinum (FLAURA2)' contains drug name(s) ['pemetrexed'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MLH1-GERMLINE-ENDOMETRIAL` (BMA — `bma_mlh1_germline_endometrial.yaml`)
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])
- **[missing-trial-source]** trial 'NRG-GY018' mentioned but no matching source citation (looked for substrings: ['GY018', 'PEMBRO-ENDOM'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'dostarlimab + carbo/paclitaxel (1L advanced dMMR, RUBY)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'pembrolizumab + carbo/paclitaxel (1L advanced, NRG-GY018)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MLH1-SOMATIC-ENDOMETRIAL` (BMA — `bma_mlh1_somatic_endometrial.yaml`)
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])
- **[missing-trial-source]** trial 'NRG-GY018' mentioned but no matching source citation (looked for substrings: ['GY018', 'PEMBRO-ENDOM'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'dostarlimab + carbo/paclitaxel (1L advanced dMMR, RUBY)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'pembrolizumab + carbo/paclitaxel (1L advanced, NRG-GY018)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH2-GERMLINE-ENDOMETRIAL` (BMA — `bma_msh2_germline_endometrial.yaml`)
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])
- **[missing-trial-source]** trial 'NRG-GY018' mentioned but no matching source citation (looked for substrings: ['GY018', 'PEMBRO-ENDOM'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'dostarlimab + carbo/paclitaxel (1L advanced dMMR, RUBY)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'pembrolizumab + carbo/paclitaxel (1L advanced, NRG-GY018)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH2-SOMATIC-ENDOMETRIAL` (BMA — `bma_msh2_somatic_endometrial.yaml`)
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])
- **[missing-trial-source]** trial 'NRG-GY018' mentioned but no matching source citation (looked for substrings: ['GY018', 'PEMBRO-ENDOM'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'dostarlimab + carbo/paclitaxel (1L advanced dMMR, RUBY)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'pembrolizumab + carbo/paclitaxel (1L advanced, NRG-GY018)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH6-GERMLINE-ENDOMETRIAL` (BMA — `bma_msh6_germline_endometrial.yaml`)
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])
- **[missing-trial-source]** trial 'NRG-GY018' mentioned but no matching source citation (looked for substrings: ['GY018', 'PEMBRO-ENDOM'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'dostarlimab + carbo/paclitaxel (1L advanced dMMR, RUBY)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'pembrolizumab + carbo/paclitaxel (1L advanced, NRG-GY018)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH6-SOMATIC-ENDOMETRIAL` (BMA — `bma_msh6_somatic_endometrial.yaml`)
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])
- **[missing-trial-source]** trial 'NRG-GY018' mentioned but no matching source citation (looked for substrings: ['GY018', 'PEMBRO-ENDOM'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'dostarlimab + carbo/paclitaxel (1L advanced dMMR, RUBY)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'pembrolizumab + carbo/paclitaxel (1L advanced, NRG-GY018)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-NOTCH1-ACTIVATING-CLL` (BMA — `bma_notch1_activating_cll.yaml`)
- **[missing-trial-source]** trial 'CLL14' mentioned but no matching source citation (looked for substrings: ['CLL14', 'VENETOCLAX'])
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'
- **[drug-inconsistency]** recommended_combination 'venetoclax + obinutuzumab (CLL14)' contains drug name(s) ['venetoclax', 'obinutuzumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'acalabrutinib monotherapy' contains drug name(s) ['acalabrutinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'zanubrutinib monotherapy' contains drug name(s) ['zanubrutinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PMS2-GERMLINE-ENDOMETRIAL` (BMA — `bma_pms2_germline_endometrial.yaml`)
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])
- **[missing-trial-source]** trial 'NRG-GY018' mentioned but no matching source citation (looked for substrings: ['GY018', 'PEMBRO-ENDOM'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'dostarlimab + carbo/paclitaxel (1L advanced dMMR, RUBY)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'pembrolizumab + carbo/paclitaxel (1L advanced, NRG-GY018)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PMS2-SOMATIC-ENDOMETRIAL` (BMA — `bma_pms2_somatic_endometrial.yaml`)
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])
- **[missing-trial-source]** trial 'NRG-GY018' mentioned but no matching source citation (looked for substrings: ['GY018', 'PEMBRO-ENDOM'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'dostarlimab + carbo/paclitaxel (1L advanced dMMR, RUBY)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'pembrolizumab + carbo/paclitaxel (1L advanced, NRG-GY018)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-RAD51B-GERMLINE-OVARIAN` (BMA — `bma_rad51b_germline_ovarian.yaml`)
- **[missing-trial-source]** trial 'PAOLA-1' mentioned but no matching source citation (looked for substrings: ['PAOLA', 'OLAPARIB'])
- **[missing-trial-source]** trial 'ARIEL3' mentioned but no matching source citation (looked for substrings: ['ARIEL3'])
- **[drug-inconsistency]** recommended_combination 'niraparib maintenance' contains drug name(s) ['niraparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab (HRD-positive)' contains drug name(s) ['olaparib', 'bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'rucaparib maintenance' contains drug name(s) ['rucaparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-RAD51C-GERMLINE-OVARIAN` (BMA — `bma_rad51c_germline_ovarian.yaml`)
- **[missing-trial-source]** trial 'PAOLA-1' mentioned but no matching source citation (looked for substrings: ['PAOLA', 'OLAPARIB'])
- **[missing-trial-source]** trial 'ARIEL3' mentioned but no matching source citation (looked for substrings: ['ARIEL3'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab (HRD-positive)' contains drug name(s) ['bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'rucaparib maintenance' contains drug name(s) ['rucaparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-RAD51D-GERMLINE-OVARIAN` (BMA — `bma_rad51d_germline_ovarian.yaml`)
- **[missing-trial-source]** trial 'PAOLA-1' mentioned but no matching source citation (looked for substrings: ['PAOLA', 'OLAPARIB'])
- **[missing-trial-source]** trial 'ARIEL3' mentioned but no matching source citation (looked for substrings: ['ARIEL3'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab (HRD-positive)' contains drug name(s) ['bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'rucaparib maintenance' contains drug name(s) ['rucaparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `IND-OVARIAN-MAINT-BEV` (Indication — `ind_ovarian_maint_bev.yaml`)
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])
- **[missing-trial-source]** trial 'SOLO-1' mentioned but no matching source citation (looked for substrings: ['SOLO', 'OLAPARIB'])
- **[missing-trial-source]** trial 'PAOLA-1' mentioned but no matching source citation (looked for substrings: ['PAOLA', 'OLAPARIB'])
- **[missing-trial-source]** trial 'GOG-218' mentioned but no matching source citation (looked for substrings: ['GOG-218'])
- **[missing-trial-source]** trial 'ICON7' mentioned but no matching source citation (looked for substrings: ['ICON7'])

### `BMA-ALK-FUSION-ALCL` (BMA — `bma_alk_fusion_alcl.yaml`)
- **[missing-trial-source]** trial 'ECHELON-2' mentioned but no matching source citation (looked for substrings: ['ECHELON-2', 'ECHELON2', 'BRENTUXIMAB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '2'
- **[drug-inconsistency]** recommended_combination 'brentuximab vedotin + cyclophosphamide/doxorubicin/prednisone (BV-CHP, 1L)' contains drug name(s) ['cyclophosphamide', 'doxorubicin', 'prednisone'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-ALK-FUSION-NSCLC` (BMA — `bma_alk_fusion_nsclc.yaml`)
- **[missing-trial-source]** trial 'ALEX' mentioned but no matching source citation (looked for substrings: ['ALEX', 'ALECTINIB'])
- **[missing-trial-source]** trial 'ALINA' mentioned but no matching source citation (looked for substrings: ['ALINA', 'ALECTINIB'])
- **[missing-trial-source]** trial 'CROWN' mentioned but no matching source citation (looked for substrings: ['CROWN', 'LORLATINIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-BCL2-EXPRESSION-CLL` (BMA — `bma_bcl2_expression_cll.yaml`)
- **[missing-trial-source]** trial 'MURANO' mentioned but no matching source citation (looked for substrings: ['MURANO', 'VENETOCLAX'])
- **[missing-trial-source]** trial 'CLL14' mentioned but no matching source citation (looked for substrings: ['CLL14', 'VENETOCLAX'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'venetoclax + ibrutinib (CAPTIVATE / GLOW)' contains drug name(s) ['ibrutinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRCA1-GERMLINE-BREAST` (BMA — `bma_brca1_germline_breast.yaml`)
- **[missing-trial-source]** trial 'OLYMPIA' mentioned but no matching source citation (looked for substrings: ['OLYMPIA', 'OLAPARIB'])
- **[missing-trial-source]** trial 'OLYMPIAD' mentioned but no matching source citation (looked for substrings: ['OLYMPIAD', 'OLAPARIB'])
- **[missing-trial-source]** trial 'EMBRACA' mentioned but no matching source citation (looked for substrings: ['EMBRACA', 'TALAZOPARIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (3) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-BRCA2-GERMLINE-OVARIAN` (BMA — `bma_brca2_germline_ovarian.yaml`)
- **[missing-trial-source]** trial 'SOLO1' mentioned but no matching source citation (looked for substrings: ['SOLO', 'OLAPARIB'])
- **[missing-trial-source]** trial 'ARIEL3' mentioned but no matching source citation (looked for substrings: ['ARIEL3'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab (PAOLA-1)' contains drug name(s) ['bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-CCND1-T1114-MCL` (BMA — `bma_ccnd1_t1114_mcl.yaml`)
- **[missing-trial-source]** trial 'TRIANGLE' mentioned but no matching source citation (looked for substrings: ['TRIANGLE'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (5) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'BR or R-CHOP/R-DHAP + autoSCT (1L fit, TP53-WT)' contains drug name(s) ['r-chop', 'r-dhap', 'autosct'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'venetoclax + ibrutinib (R/R)' contains drug name(s) ['venetoclax'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-FGFR2-MUTATION-ENDOMETRIAL` (BMA — `bma_fgfr2_mutation_endometrial.yaml`)
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])
- **[missing-trial-source]** trial 'NRG-GY018' mentioned but no matching source citation (looked for substrings: ['GY018', 'PEMBRO-ENDOM'])
- **[drug-inconsistency]** recommended_combination 'pemigatinib (basket trial / NCI-MATCH for FGFR2-mutant endometrial)' contains drug name(s) ['pemigatinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'erdafitinib (basket trial)' contains drug name(s) ['erdafitinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-FLT3-ITD-AML` (BMA — `bma_flt3_itd_aml.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'midostaurin + 7+3 induction + HiDAC consolidation + midostaurin maintenance' contains drug name(s) ['hidac'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'quizartinib + 7+3 induction + HiDAC consolidation + quizartinib maintenance (FLT3-ITD specifically)' contains drug name(s) ['hidac'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'allo-SCT in CR1 (high-allelic-ratio FLT3-ITD or other adverse-risk features)' contains drug name(s) ['allo-sct'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-KRAS-G12C-PDAC` (BMA — `bma_kras_g12c_pdac.yaml`)
- **[missing-trial-source]** trial 'CodeBreaK' mentioned but no matching source citation (looked for substrings: ['CODEBREAK', 'SOTORASIB'])
- **[missing-trial-source]** trial 'KRYSTAL-1' mentioned but no matching source citation (looked for substrings: ['KRYSTAL', 'ADAGRASIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'adagrasib monotherapy' contains drug name(s) ['adagrasib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PALB2-GERMLINE-OVARIAN` (BMA — `bma_palb2_germline_ovarian.yaml`)
- **[missing-trial-source]** trial 'PAOLA-1' mentioned but no matching source citation (looked for substrings: ['PAOLA', 'OLAPARIB'])
- **[missing-trial-source]** trial 'ARIEL3' mentioned but no matching source citation (looked for substrings: ['ARIEL3'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'rucaparib maintenance' contains drug name(s) ['rucaparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-RET-FUSION-NSCLC` (BMA — `bma_ret_fusion_nsclc.yaml`)
- **[missing-trial-source]** trial 'LIBRETTO-001' mentioned but no matching source citation (looked for substrings: ['LIBRETTO', 'SELPERCATINIB'])
- **[missing-trial-source]** trial 'LIBRETTO-431' mentioned but no matching source citation (looked for substrings: ['LIBRETTO', 'SELPERCATINIB'])
- **[missing-trial-source]** trial 'ARROW' mentioned but no matching source citation (looked for substrings: ['ARROW', 'PRALSETINIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-RET-KIF5B-NSCLC` (BMA — `bma_ret_kif5b_nsclc.yaml`)
- **[missing-trial-source]** trial 'LIBRETTO-001' mentioned but no matching source citation (looked for substrings: ['LIBRETTO', 'SELPERCATINIB'])
- **[missing-trial-source]** trial 'LIBRETTO-431' mentioned but no matching source citation (looked for substrings: ['LIBRETTO', 'SELPERCATINIB'])
- **[missing-trial-source]** trial 'ARROW' mentioned but no matching source citation (looked for substrings: ['ARROW', 'PRALSETINIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-TP53-MUT-MCL` (BMA — `bma_tp53_mut_mcl.yaml`)
- **[missing-trial-source]** trial 'TRIANGLE' mentioned but no matching source citation (looked for substrings: ['TRIANGLE'])
- **[drug-inconsistency]** recommended_combination 'acalabrutinib + rituximab (1L)' contains drug name(s) ['acalabrutinib', 'rituximab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'ibrutinib + rituximab + venetoclax (R/R)' contains drug name(s) ['ibrutinib', 'rituximab', 'venetoclax'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'CAR-T brexu-cel (R/R)' contains drug name(s) ['car-t'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `IND-BREAST-HR-POS-MAINT-CDK46I` (Indication — `ind_breast_hr_pos_maint_cdk46i.yaml`)
- **[missing-trial-source]** trial 'MONALEESA-2' mentioned but no matching source citation (looked for substrings: ['MONALEESA', 'RIBOCICLIB'])
- **[missing-trial-source]** trial 'MONARCH-3' mentioned but no matching source citation (looked for substrings: ['MONARCH', 'ABEMACICLIB'])
- **[missing-trial-source]** trial 'PALOMA-2' mentioned but no matching source citation (looked for substrings: ['PALOMA', 'PALBOCICLIB'])
- **[missing-trial-source]** trial 'TROPiCS-02' mentioned but no matching source citation (looked for substrings: ['TROPICS', 'SACITUZUMAB'])

### `IND-PROSTATE-MHSPC-1L-ARPI-DOUBLET` (Indication — `ind_prostate_mhspc_1l_arpi_doublet.yaml`)
- **[missing-trial-source]** trial 'LATITUDE' mentioned but no matching source citation (looked for substrings: ['LATITUDE', 'ABIRATERONE'])
- **[missing-trial-source]** trial 'ENZAMET' mentioned but no matching source citation (looked for substrings: ['ENZAMET', 'ENZALUTAMIDE'])
- **[missing-trial-source]** trial 'TITAN' mentioned but no matching source citation (looked for substrings: ['TITAN', 'APALUTAMIDE'])
- **[missing-trial-source]** trial 'ARASENS' mentioned but no matching source citation (looked for substrings: ['ARASENS', 'DAROLUTAMIDE'])

### `BMA-BARD1-GERMLINE-OVARIAN` (BMA — `bma_bard1_germline_ovarian.yaml`)
- **[missing-trial-source]** trial 'PAOLA-1' mentioned but no matching source citation (looked for substrings: ['PAOLA', 'OLAPARIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab (HRD-positive)' contains drug name(s) ['bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BCR-ABL1-E255K-CML` (BMA — `bma_bcr_abl1_e255k_cml.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IB typically maps to OncoKB {1,2} but entity declares OncoKB level 'R2'
- **[drug-inconsistency]** recommended_combination 'asciminib monotherapy (in multi-TKI failure)' contains drug name(s) ['asciminib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BCR-ABL1-F317L-BALL` (BMA — `bma_bcr_abl1_f317l_ball.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level 'R2'
- **[drug-inconsistency]** recommended_combination 'ponatinib + blinatumomab' contains drug name(s) ['blinatumomab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BCR-ABL1-T315I-BALL` (BMA — `bma_bcr_abl1_t315i_ball.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IA typically maps to OncoKB {1} but entity declares OncoKB level 'R1'
- **[drug-inconsistency]** recommended_combination 'ponatinib + blinatumomab (chemo-free)' contains drug name(s) ['blinatumomab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BCR-ABL1-T315I-CML` (BMA — `bma_bcr_abl1_t315i_cml.yaml`)
- **[missing-trial-source]** trial 'ASCEMBL' mentioned but no matching source citation (looked for substrings: ['ASCEMBL', 'ASCIMINIB', 'REA'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IA typically maps to OncoKB {1} but entity declares OncoKB level 'R1'

### `BMA-BRAF-V600E-CRC` (BMA — `bma_braf_v600e_crc.yaml`)
- **[missing-trial-source]** trial 'BEACON' mentioned but no matching source citation (looked for substrings: ['BEACON', 'ENCORAFENIB', 'KOPETZ'])
- **[missing-trial-source]** trial 'BEACON-CRC' mentioned but no matching source citation (looked for substrings: ['BEACON', 'ENCORAFENIB', 'KOPETZ'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-BRAF-V600E-HCL` (BMA — `bma_braf_v600e_hcl.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'vemurafenib + rituximab (consolidation / R/R)' contains drug name(s) ['rituximab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'dabrafenib + trametinib (alternative)' contains drug name(s) ['dabrafenib', 'trametinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRAF-V600E-MELANOMA` (BMA — `bma_braf_v600e_melanoma.yaml`)
- **[missing-trial-source]** trial 'COMBI-d' mentioned but no matching source citation (looked for substrings: ['COMBI', 'DABRAFENIB-TRAMETINIB'])
- **[missing-trial-source]** trial 'COMBI-AD' mentioned but no matching source citation (looked for substrings: ['COMBI-AD'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (3) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-BRAF-V600K-MELANOMA` (BMA — `bma_braf_v600k_melanoma.yaml`)
- **[missing-trial-source]** trial 'COMBI-d' mentioned but no matching source citation (looked for substrings: ['COMBI', 'DABRAFENIB-TRAMETINIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'vemurafenib + cobimetinib' contains drug name(s) ['vemurafenib', 'cobimetinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRCA1-SOMATIC-OVARIAN` (BMA — `bma_brca1_somatic_ovarian.yaml`)
- **[missing-trial-source]** trial 'SOLO1' mentioned but no matching source citation (looked for substrings: ['SOLO', 'OLAPARIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab (PAOLA-1)' contains drug name(s) ['bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRCA1-SOMATIC-PROSTATE` (BMA — `bma_brca1_somatic_prostate.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'niraparib + abiraterone (1L)' contains drug name(s) ['niraparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'talazoparib + enzalutamide (1L)' contains drug name(s) ['talazoparib', 'enzalutamide'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRCA2-SOMATIC-OVARIAN` (BMA — `bma_brca2_somatic_ovarian.yaml`)
- **[missing-trial-source]** trial 'SOLO1' mentioned but no matching source citation (looked for substrings: ['SOLO', 'OLAPARIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab (PAOLA-1)' contains drug name(s) ['bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRCA2-SOMATIC-PROSTATE` (BMA — `bma_brca2_somatic_prostate.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'niraparib + abiraterone (1L)' contains drug name(s) ['niraparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'talazoparib + enzalutamide (1L)' contains drug name(s) ['talazoparib', 'enzalutamide'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRIP1-GERMLINE-OVARIAN` (BMA — `bma_brip1_germline_ovarian.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab (HRD-positive)' contains drug name(s) ['bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'rucaparib (LOH-high)' contains drug name(s) ['rucaparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-EGFR-EX20INS-NSCLC` (BMA — `bma_egfr_ex20ins_nsclc.yaml`)
- **[missing-trial-source]** trial 'PAPILLON' mentioned but no matching source citation (looked for substrings: ['PAPILLON', 'AMIVANTAMAB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'platinum-doublet chemotherapy (alternative)' contains drug name(s) ['platinum-doublet'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-EPCAM-GERMLINE-CRC` (BMA — `bma_epcam_germline_crc.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-177' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-177', 'KEYNOTE177'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'nivolumab + ipilimumab (2L+, CheckMate-142)' contains drug name(s) ['nivolumab', 'ipilimumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-EPCAM-GERMLINE-ENDOMETRIAL` (BMA — `bma_epcam_germline_endometrial.yaml`)
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'dostarlimab + carbo/paclitaxel (1L, RUBY)' contains drug name(s) ['carbo', 'paclitaxel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-FGFR2-MUTATION-UROTHELIAL` (BMA — `bma_fgfr2_mutation_urothelial.yaml`)
- **[missing-trial-source]** trial 'BLC2001' mentioned but no matching source citation (looked for substrings: ['BLC2001', 'ERDAFITINIB'])
- **[missing-trial-source]** trial 'THOR' mentioned but no matching source citation (looked for substrings: ['THOR', 'ERDAFITINIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-FGFR3-TACC3-UROTHELIAL` (BMA — `bma_fgfr3_tacc3_urothelial.yaml`)
- **[missing-trial-source]** trial 'BLC2001' mentioned but no matching source citation (looked for substrings: ['BLC2001', 'ERDAFITINIB'])
- **[missing-trial-source]** trial 'THOR' mentioned but no matching source citation (looked for substrings: ['THOR', 'ERDAFITINIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-FLT3-D835-AML` (BMA — `bma_flt3_d835_aml.yaml`)
- **[missing-trial-source]** trial 'MAGNITUDE' mentioned but no matching source citation (looked for substrings: ['MAGNITUDE', 'NIRAPARIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'midostaurin + 7+3 + HiDAC consolidation + midostaurin maintenance' contains drug name(s) ['hidac'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-FLT3-F691L-AML` (BMA — `bma_flt3_f691l_aml.yaml`)
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level 'R1'
- **[drug-inconsistency]** recommended_combination 'salvage chemo + allo-SCT (preferred when fit)' contains drug name(s) ['salvage', 'allo-sct'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-IDH1-R132C-AML` (BMA — `bma_idh1_r132c_aml.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'olutasidenib' contains drug name(s) ['olutasidenib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'ivosidenib + azacitidine' contains drug name(s) ['azacitidine'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-KRAS-G12C-CRC` (BMA — `bma_kras_g12c_crc.yaml`)
- **[missing-trial-source]** trial 'CodeBreaK' mentioned but no matching source citation (looked for substrings: ['CODEBREAK', 'SOTORASIB'])
- **[missing-trial-source]** trial 'KRYSTAL-1' mentioned but no matching source citation (looked for substrings: ['KRYSTAL', 'ADAGRASIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-KRAS-G12C-NSCLC` (BMA — `bma_kras_g12c_nsclc.yaml`)
- **[missing-trial-source]** trial 'CodeBreaK' mentioned but no matching source citation (looked for substrings: ['CODEBREAK', 'SOTORASIB'])
- **[missing-trial-source]** trial 'KRYSTAL-1' mentioned but no matching source citation (looked for substrings: ['KRYSTAL', 'ADAGRASIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-MLH1-GERMLINE-GASTRIC` (BMA — `bma_mlh1_germline_gastric.yaml`)
- **[missing-trial-source]** trial 'CheckMate-649' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-649', 'CHECKMATE649'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'nivolumab + FOLFOX/CapeOX (1L MSI-H gastric, CheckMate-649)' contains drug name(s) ['folfox', 'capeox'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MLH1-SOMATIC-GASTRIC` (BMA — `bma_mlh1_somatic_gastric.yaml`)
- **[missing-trial-source]** trial 'CheckMate-649' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-649', 'CHECKMATE649'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'nivolumab + FOLFOX/CapeOX (1L MSI-H gastric, CheckMate-649)' contains drug name(s) ['folfox', 'capeox'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH2-GERMLINE-GASTRIC` (BMA — `bma_msh2_germline_gastric.yaml`)
- **[missing-trial-source]** trial 'CheckMate-649' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-649', 'CHECKMATE649'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'nivolumab + FOLFOX/CapeOX (1L MSI-H gastric, CheckMate-649)' contains drug name(s) ['folfox', 'capeox'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH2-SOMATIC-GASTRIC` (BMA — `bma_msh2_somatic_gastric.yaml`)
- **[missing-trial-source]** trial 'CheckMate-649' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-649', 'CHECKMATE649'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'nivolumab + FOLFOX/CapeOX (1L MSI-H gastric, CheckMate-649)' contains drug name(s) ['folfox', 'capeox'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH6-GERMLINE-GASTRIC` (BMA — `bma_msh6_germline_gastric.yaml`)
- **[missing-trial-source]** trial 'CheckMate-649' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-649', 'CHECKMATE649'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'nivolumab + FOLFOX/CapeOX (1L MSI-H gastric, CheckMate-649)' contains drug name(s) ['folfox', 'capeox'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH6-SOMATIC-GASTRIC` (BMA — `bma_msh6_somatic_gastric.yaml`)
- **[missing-trial-source]** trial 'CheckMate-649' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-649', 'CHECKMATE649'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'nivolumab + FOLFOX/CapeOX (1L MSI-H gastric, CheckMate-649)' contains drug name(s) ['folfox', 'capeox'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MYD88-L265P-HCV-MZL` (BMA — `bma_myd88_l265p_hcv_mzl.yaml`)
- **[missing-trial-source]** trial 'MAGNOLIA' mentioned but no matching source citation (looked for substrings: ['MAGNOLIA'])
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'
- **[drug-inconsistency]** recommended_combination 'zanubrutinib (FDA-approved R/R MZL — not MYD88-selected)' contains drug name(s) ['zanubrutinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MYD88-L265P-NODAL-MZL` (BMA — `bma_myd88_l265p_nodal_mzl.yaml`)
- **[missing-trial-source]** trial 'MAGNOLIA' mentioned but no matching source citation (looked for substrings: ['MAGNOLIA'])
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'
- **[drug-inconsistency]** recommended_combination 'zanubrutinib (FDA-approved R/R MZL — not MYD88-selected)' contains drug name(s) ['zanubrutinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MYD88-L265P-SPLENIC-MZL` (BMA — `bma_myd88_l265p_splenic_mzl.yaml`)
- **[missing-trial-source]** trial 'MAGNOLIA' mentioned but no matching source citation (looked for substrings: ['MAGNOLIA'])
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'
- **[drug-inconsistency]** recommended_combination 'zanubrutinib (FDA-approved R/R MZL — not MYD88-selected)' contains drug name(s) ['zanubrutinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PMS2-GERMLINE-GASTRIC` (BMA — `bma_pms2_germline_gastric.yaml`)
- **[missing-trial-source]** trial 'CheckMate-649' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-649', 'CHECKMATE649'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'nivolumab + FOLFOX/CapeOX (1L MSI-H gastric, CheckMate-649)' contains drug name(s) ['folfox', 'capeox'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PMS2-SOMATIC-GASTRIC` (BMA — `bma_pms2_somatic_gastric.yaml`)
- **[missing-trial-source]** trial 'CheckMate-649' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-649', 'CHECKMATE649'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'nivolumab + FOLFOX/CapeOX (1L MSI-H gastric, CheckMate-649)' contains drug name(s) ['folfox', 'capeox'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-RET-CCDC6-NSCLC` (BMA — `bma_ret_ccdc6_nsclc.yaml`)
- **[missing-trial-source]** trial 'LIBRETTO-001' mentioned but no matching source citation (looked for substrings: ['LIBRETTO', 'SELPERCATINIB'])
- **[missing-trial-source]** trial 'ARROW' mentioned but no matching source citation (looked for substrings: ['ARROW', 'PRALSETINIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-RET-FUSION-THYROID-PAPILLARY` (BMA — `bma_ret_fusion_thyroid_papillary.yaml`)
- **[missing-trial-source]** trial 'LIBRETTO-001' mentioned but no matching source citation (looked for substrings: ['LIBRETTO', 'SELPERCATINIB'])
- **[missing-trial-source]** trial 'ARROW' mentioned but no matching source citation (looked for substrings: ['ARROW', 'PRALSETINIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-ROS1-G2032R-NSCLC` (BMA — `bma_ros1_g2032r_nsclc.yaml`)
- **[missing-trial-source]** trial 'TRIDENT-1' mentioned but no matching source citation (looked for substrings: ['TRIDENT-1'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IB typically maps to OncoKB {1,2} but entity declares OncoKB level 'R1'

### `BMA-TP53-MUT-BREAST` (BMA — `bma_tp53_mut_breast.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-522' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-522', 'KEYNOTE522'])
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'per usual TNBC algorithm (KEYNOTE-522)' contains drug name(s) ['per'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `IND-CML-1L-2GEN-TKI` (Indication — `ind_cml_1l_2gen_tki.yaml`)
- **[missing-trial-source]** trial 'ENESTnd' mentioned but no matching source citation (looked for substrings: ['ENESTND', 'NILOTINIB'])
- **[missing-trial-source]** trial 'DASISION' mentioned but no matching source citation (looked for substrings: ['DASISION', 'DASATINIB'])
- **[missing-trial-source]** trial 'BFORE' mentioned but no matching source citation (looked for substrings: ['BFORE', 'BOSUTINIB'])

### `IND-ENDOMETRIAL-ADVANCED-1L-PEMBRO-CHEMO` (Indication — `ind_endometrial_advanced_1l_pembro_chemo.yaml`)
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])
- **[missing-trial-source]** trial 'NRG-GY018' mentioned but no matching source citation (looked for substrings: ['GY018', 'PEMBRO-ENDOM'])

### `IND-MTC-ADVANCED-1L-SELPERCATINIB` (Indication — `ind_mtc_advanced_1l_selpercatinib.yaml`)
- **[missing-trial-source]** trial 'LIBRETTO-001' mentioned but no matching source citation (looked for substrings: ['LIBRETTO', 'SELPERCATINIB'])
- **[missing-trial-source]** trial 'ARROW' mentioned but no matching source citation (looked for substrings: ['ARROW', 'PRALSETINIB'])
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])

### `IND-NSCLC-ALK-MAINT-ALECTINIB` (Indication — `ind_nsclc_alk_maint_alectinib.yaml`)
- **[missing-trial-source]** trial 'ALEX' mentioned but no matching source citation (looked for substrings: ['ALEX', 'ALECTINIB'])
- **[missing-trial-source]** trial 'CROWN' mentioned but no matching source citation (looked for substrings: ['CROWN', 'LORLATINIB'])
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])

### `REG-2GEN-TKI-CML` (Regimen — `dasatinib_or_nilotinib_cml.yaml`)
- **[missing-trial-source]** trial 'ENESTnd' mentioned but no matching source citation (looked for substrings: ['ENESTND', 'NILOTINIB'])
- **[missing-trial-source]** trial 'DASISION' mentioned but no matching source citation (looked for substrings: ['DASISION', 'DASATINIB'])
- **[missing-trial-source]** trial 'BFORE' mentioned but no matching source citation (looked for substrings: ['BFORE', 'BOSUTINIB'])

### `BMA-ALK-EML4-V1-NSCLC` (BMA — `bma_alk_eml4_v1_nsclc.yaml`)
- **[missing-trial-source]** trial 'ALEX' mentioned but no matching source citation (looked for substrings: ['ALEX', 'ALECTINIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-ALK-EML4-V3-NSCLC` (BMA — `bma_alk_eml4_v3_nsclc.yaml`)
- **[missing-trial-source]** trial 'CROWN' mentioned but no matching source citation (looked for substrings: ['CROWN', 'LORLATINIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-ALK-G1202R-NSCLC` (BMA — `bma_alk_g1202r_nsclc.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IB typically maps to OncoKB {1,2} but entity declares OncoKB level 'R1'

### `BMA-ALK-L1196M-NSCLC` (BMA — `bma_alk_l1196m_nsclc.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IB typically maps to OncoKB {1,2} but entity declares OncoKB level 'R1'

### `BMA-ATM-SOMATIC-PROSTATE` (BMA — `bma_atm_somatic_prostate.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'talazoparib + enzalutamide (1L, HRR-mut)' contains drug name(s) ['talazoparib', 'enzalutamide'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BCR-ABL1-F317L-CML` (BMA — `bma_bcr_abl1_f317l_cml.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IB typically maps to OncoKB {1,2} but entity declares OncoKB level 'R2'

### `BMA-BCR-ABL1-P190-BALL` (BMA — `bma_bcr_abl1_p190_ball.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'ponatinib + hyper-CVAD (1L)' contains drug name(s) ['hyper-cvad'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BCR-ABL1-P210-CML` (BMA — `bma_bcr_abl1_p210_cml.yaml`)
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-BCR-ABL1-V299L-CML` (BMA — `bma_bcr_abl1_v299l_cml.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IB typically maps to OncoKB {1,2} but entity declares OncoKB level 'R2'

### `BMA-BRAF-V600E-GBM` (BMA — `bma_braf_v600e_gbm.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '2'

### `BMA-BRAF-V600E-OVARIAN` (BMA — `bma_braf_v600e_ovarian.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '2'

### `BMA-BRAF-V600E-PDAC` (BMA — `bma_braf_v600e_pdac.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3A'

### `BMA-CHEK1-SOMATIC-PROSTATE` (BMA — `bma_chek1_somatic_prostate.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'

### `BMA-CHEK2-GERMLINE-PROSTATE` (BMA — `bma_chek2_germline_prostate.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'talazoparib + enzalutamide (HRR-mutated 1L)' contains drug name(s) ['talazoparib', 'enzalutamide'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-CHEK2-SOMATIC-PROSTATE` (BMA — `bma_chek2_somatic_prostate.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'talazoparib + enzalutamide (HRR-mutated 1L)' contains drug name(s) ['talazoparib', 'enzalutamide'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-EGFR-T790M-NSCLC` (BMA — `bma_egfr_t790m_nsclc.yaml`)
- **[missing-trial-source]** trial 'AURA3' mentioned but no matching source citation (looked for substrings: ['AURA3'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-FGFR3-R248C-UROTHELIAL` (BMA — `bma_fgfr3_r248c_urothelial.yaml`)
- **[missing-trial-source]** trial 'THOR' mentioned but no matching source citation (looked for substrings: ['THOR', 'ERDAFITINIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-FGFR3-S249C-UROTHELIAL` (BMA — `bma_fgfr3_s249c_urothelial.yaml`)
- **[missing-trial-source]** trial 'THOR' mentioned but no matching source citation (looked for substrings: ['THOR', 'ERDAFITINIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-IDH1-R132C-GBM` (BMA — `bma_idh1_r132c_gbm.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '2'

### `BMA-IDH1-R132G-AML` (BMA — `bma_idh1_r132g_aml.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'olutasidenib' contains drug name(s) ['olutasidenib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-IDH1-R132H-AML` (BMA — `bma_idh1_r132h_aml.yaml`)
- **[missing-trial-source]** trial 'AGILE' mentioned but no matching source citation (looked for substrings: ['AGILE', 'IVOSIDENIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-IDH1-R132H-GBM` (BMA — `bma_idh1_r132h_gbm.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '2'

### `BMA-IDH1-R132L-AML` (BMA — `bma_idh1_r132l_aml.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'olutasidenib' contains drug name(s) ['olutasidenib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-IDH1-R132S-AML` (BMA — `bma_idh1_r132s_aml.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'olutasidenib' contains drug name(s) ['olutasidenib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-IDH2-R172K-AITL` (BMA — `bma_idh2_r172k_aitl.yaml`)
- **[missing-trial-source]** trial 'ECHELON-2' mentioned but no matching source citation (looked for substrings: ['ECHELON-2', 'ECHELON2', 'BRENTUXIMAB'])
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'

### `BMA-KIT-D816V-GIST` (BMA — `bma_kit_d816v_gist.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level 'R1'

### `BMA-KIT-EXON11-GIST` (BMA — `bma_kit_exon11_gist.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'imatinib 400 mg/day adjuvant 3 yr (high-risk resected: ≥3 cm + mitoses ≥5/50 HPF, or rupture, or non-gastric primary)' contains drug name(s) ['day'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-KIT-EXON13-17-GIST` (BMA — `bma_kit_exon13_17_gist.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '1'

### `BMA-KIT-EXON9-GIST` (BMA — `bma_kit_exon9_gist.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'imatinib 800 mg/day split BID (1L advanced/metastatic exon 9)' contains drug name(s) ['day'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-KRAS-G12C-OVARIAN` (BMA — `bma_kras_g12c_ovarian.yaml`)
- **[missing-trial-source]** trial 'CodeBreaK' mentioned but no matching source citation (looked for substrings: ['CODEBREAK', 'SOTORASIB'])
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3A'

### `BMA-MET-AMP-NSCLC` (BMA — `bma_met_amp_nsclc.yaml`)
- **[missing-trial-source]** trial 'MARIPOSA' mentioned but no matching source citation (looked for substrings: ['MARIPOSA'])
- **[drug-inconsistency]** recommended_combination 'amivantamab + lazertinib (post-EGFR-TKI MET-amp resistance, MARIPOSA-2 / SAVANNAH context)' contains drug name(s) ['amivantamab', 'lazertinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MET-AMP-RCC-PAPILLARY` (BMA — `bma_met_amp_rcc_papillary.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '2'

### `BMA-MET-EX14-NSCLC` (BMA — `bma_met_ex14_nsclc.yaml`)
- **[missing-trial-source]** trial 'VISION' mentioned but no matching source citation (looked for substrings: ['VISION', 'LUTETIUM', 'PSMA'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-MLH1-GERMLINE-CRC` (BMA — `bma_mlh1_germline_crc.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-177' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-177', 'KEYNOTE177'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-MLH1-GERMLINE-OVARIAN` (BMA — `bma_mlh1_germline_ovarian.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'standard EOC therapy by HRD/BRCA status' contains drug name(s) ['brca'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MLH1-GERMLINE-PROSTATE` (BMA — `bma_mlh1_germline_prostate.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'pembrolizumab monotherapy (pan-tumor MSI-H/dMMR, FDA 2017) in mCRPC after NHA/taxane' contains drug name(s) ['taxane'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MLH1-SOMATIC-CRC` (BMA — `bma_mlh1_somatic_crc.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-177' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-177', 'KEYNOTE177'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-MLH1-SOMATIC-OVARIAN` (BMA — `bma_mlh1_somatic_ovarian.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'standard EOC therapy by HRD/BRCA status' contains drug name(s) ['brca'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MLH1-SOMATIC-PROSTATE` (BMA — `bma_mlh1_somatic_prostate.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'pembrolizumab monotherapy (pan-tumor MSI-H/dMMR, FDA 2017) in mCRPC after NHA/taxane' contains drug name(s) ['taxane'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH2-GERMLINE-CRC` (BMA — `bma_msh2_germline_crc.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-177' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-177', 'KEYNOTE177'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-MSH2-GERMLINE-OVARIAN` (BMA — `bma_msh2_germline_ovarian.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'standard EOC therapy by HRD/BRCA status' contains drug name(s) ['brca'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH2-GERMLINE-PROSTATE` (BMA — `bma_msh2_germline_prostate.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'pembrolizumab monotherapy (pan-tumor MSI-H/dMMR, FDA 2017) in mCRPC after NHA/taxane' contains drug name(s) ['taxane'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH2-SOMATIC-CRC` (BMA — `bma_msh2_somatic_crc.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-177' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-177', 'KEYNOTE177'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-MSH2-SOMATIC-OVARIAN` (BMA — `bma_msh2_somatic_ovarian.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'standard EOC therapy by HRD/BRCA status' contains drug name(s) ['brca'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH2-SOMATIC-PROSTATE` (BMA — `bma_msh2_somatic_prostate.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'pembrolizumab monotherapy (pan-tumor MSI-H/dMMR, FDA 2017) in mCRPC after NHA/taxane' contains drug name(s) ['taxane'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH6-GERMLINE-CRC` (BMA — `bma_msh6_germline_crc.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-177' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-177', 'KEYNOTE177'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-MSH6-GERMLINE-OVARIAN` (BMA — `bma_msh6_germline_ovarian.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'standard EOC therapy by HRD/BRCA status' contains drug name(s) ['brca'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH6-GERMLINE-PROSTATE` (BMA — `bma_msh6_germline_prostate.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'pembrolizumab monotherapy (pan-tumor MSI-H/dMMR, FDA 2017) in mCRPC after NHA/taxane' contains drug name(s) ['taxane'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH6-SOMATIC-CRC` (BMA — `bma_msh6_somatic_crc.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-177' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-177', 'KEYNOTE177'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-MSH6-SOMATIC-OVARIAN` (BMA — `bma_msh6_somatic_ovarian.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'standard EOC therapy by HRD/BRCA status' contains drug name(s) ['brca'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MSH6-SOMATIC-PROSTATE` (BMA — `bma_msh6_somatic_prostate.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'pembrolizumab monotherapy (pan-tumor MSI-H/dMMR, FDA 2017) in mCRPC after NHA/taxane' contains drug name(s) ['taxane'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PMS2-GERMLINE-CRC` (BMA — `bma_pms2_germline_crc.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-177' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-177', 'KEYNOTE177'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-PMS2-GERMLINE-OVARIAN` (BMA — `bma_pms2_germline_ovarian.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'standard EOC therapy by HRD/BRCA status' contains drug name(s) ['brca'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PMS2-GERMLINE-PROSTATE` (BMA — `bma_pms2_germline_prostate.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'pembrolizumab monotherapy (pan-tumor MSI-H/dMMR, FDA 2017) in mCRPC after NHA/taxane' contains drug name(s) ['taxane'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PMS2-SOMATIC-CRC` (BMA — `bma_pms2_somatic_crc.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-177' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-177', 'KEYNOTE177'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (4) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-PMS2-SOMATIC-OVARIAN` (BMA — `bma_pms2_somatic_ovarian.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'standard EOC therapy by HRD/BRCA status' contains drug name(s) ['brca'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PMS2-SOMATIC-PROSTATE` (BMA — `bma_pms2_somatic_prostate.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources
- **[drug-inconsistency]** recommended_combination 'pembrolizumab monotherapy (pan-tumor MSI-H/dMMR, FDA 2017) in mCRPC after NHA/taxane' contains drug name(s) ['taxane'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-RET-C634R-MTC` (BMA — `bma_ret_c634r_mtc.yaml`)
- **[missing-trial-source]** trial 'LIBRETTO-001' mentioned but no matching source citation (looked for substrings: ['LIBRETTO', 'SELPERCATINIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-RET-M918T-MTC` (BMA — `bma_ret_m918t_mtc.yaml`)
- **[missing-trial-source]** trial 'ARROW' mentioned but no matching source citation (looked for substrings: ['ARROW', 'PRALSETINIB'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-ROS1-FUSION-NSCLC` (BMA — `bma_ros1_fusion_nsclc.yaml`)
- **[missing-trial-source]** trial 'TRIDENT-1' mentioned but no matching source citation (looked for substrings: ['TRIDENT-1'])
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `IND-ALCL-MAINTENANCE-BV-POST-ASCT` (Indication — `ind_alcl_maintenance_bv_post_asct.yaml`)
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])
- **[missing-trial-source]** trial 'ECHELON-2' mentioned but no matching source citation (looked for substrings: ['ECHELON-2', 'ECHELON2', 'BRENTUXIMAB'])

### `IND-APL-1L-ATRA-ATO-IDA` (Indication — `ind_apl_1l_atra_ato_ida.yaml`)
- **[missing-trial-source]** trial 'APL0406' mentioned but no matching source citation (looked for substrings: ['APL0406', 'PETHEMA', 'LOCOCO'])
- **[missing-trial-source]** trial 'AIDA' mentioned but no matching source citation (looked for substrings: ['AIDA'])

### `IND-BREAST-BRCA-POS-MET-PARPI` (Indication — `ind_breast_brca_pos_met_parpi.yaml`)
- **[missing-trial-source]** trial 'OLYMPIAD' mentioned but no matching source citation (looked for substrings: ['OLYMPIAD', 'OLAPARIB'])
- **[missing-trial-source]** trial 'EMBRACA' mentioned but no matching source citation (looked for substrings: ['EMBRACA', 'TALAZOPARIB'])

### `IND-BREAST-HER2-POS-EARLY-NEOADJUVANT` (Indication — `ind_breast_her2_pos_early_neoadjuvant.yaml`)
- **[missing-trial-source]** trial 'APHINITY' mentioned but no matching source citation (looked for substrings: ['APHINITY'])
- **[missing-trial-source]** trial 'KATHERINE' mentioned but no matching source citation (looked for substrings: ['KATHERINE', 'TDM1'])

### `IND-BREAST-HR-POS-MET-1L-CDKI` (Indication — `ind_breast_hr_pos_met_1l_cdki.yaml`)
- **[missing-trial-source]** trial 'MONALEESA-2' mentioned but no matching source citation (looked for substrings: ['MONALEESA', 'RIBOCICLIB'])
- **[missing-trial-source]** trial 'MONALEESA-7' mentioned but no matching source citation (looked for substrings: ['MONALEESA', 'RIBOCICLIB'])

### `IND-BREAST-TNBC-EARLY-NEOADJUVANT` (Indication — `ind_breast_tnbc_early_neoadjuvant.yaml`)
- **[missing-trial-source]** trial 'OLYMPIA' mentioned but no matching source citation (looked for substrings: ['OLYMPIA', 'OLAPARIB'])
- **[missing-trial-source]** trial 'KEYNOTE-522' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-522', 'KEYNOTE522'])

### `IND-CLL-2L-VENR-MURANO` (Indication — `ind_cll_2l_venr_murano.yaml`)
- **[missing-trial-source]** trial 'MURANO' mentioned but no matching source citation (looked for substrings: ['MURANO', 'VENETOCLAX'])
- **[missing-trial-source]** trial 'CLL14' mentioned but no matching source citation (looked for substrings: ['CLL14', 'VENETOCLAX'])

### `IND-DLBCL-3L-AXICEL-CART` (Indication — `ind_dlbcl_3l_axicel_cart.yaml`)
- **[missing-trial-source]** trial 'ZUMA-1' mentioned but no matching source citation (looked for substrings: ['ZUMA-1', 'ZUMA1', 'AXICEL'])
- **[missing-trial-source]** trial 'ZUMA-7' mentioned but no matching source citation (looked for substrings: ['ZUMA-7', 'ZUMA7', 'AXICEL'])

### `IND-ENDOMETRIAL-2L-DOSTARLIMAB-DMMR` (Indication — `ind_endometrial_2l_dostarlimab_dmmr.yaml`)
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])
- **[missing-trial-source]** trial 'NRG-GY018' mentioned but no matching source citation (looked for substrings: ['GY018', 'PEMBRO-ENDOM'])

### `IND-ENDOMETRIAL-2L-PEMBRO-LENVA-PMMR` (Indication — `ind_endometrial_2l_pembro_lenva_pmmr.yaml`)
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])
- **[missing-trial-source]** trial 'NRG-GY018' mentioned but no matching source citation (looked for substrings: ['GY018', 'PEMBRO-ENDOM'])

### `IND-ESOPH-ADJUVANT-NIVOLUMAB-POST-CROSS` (Indication — `ind_esoph_adjuvant_nivolumab_post_cross.yaml`)
- **[missing-trial-source]** trial 'CheckMate-577' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-577', 'CHECKMATE577'])
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])

### `IND-FL-1L-BR` (Indication — `ind_fl_1l_br.yaml`)
- **[missing-trial-source]** trial 'STIL' mentioned but no matching source citation (looked for substrings: ['STIL'])
- **[missing-trial-source]** trial 'PRIMA' mentioned but no matching source citation (looked for substrings: ['PRIMA', 'NIRAPARIB'])

### `IND-HGBL-DH-2L-CART-AXICEL` (Indication — `ind_hgbl_dh_2l_cart_axicel.yaml`)
- **[missing-trial-source]** trial 'ZUMA-1' mentioned but no matching source citation (looked for substrings: ['ZUMA-1', 'ZUMA1', 'AXICEL'])
- **[missing-trial-source]** trial 'ZUMA-7' mentioned but no matching source citation (looked for substrings: ['ZUMA-7', 'ZUMA7', 'AXICEL'])

### `IND-MELANOMA-BRAF-METASTATIC-1L-DABRA-TRAME` (Indication — `ind_melanoma_braf_metastatic_1l_dabra_trame.yaml`)
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])
- **[missing-trial-source]** trial 'COMBI-d' mentioned but no matching source citation (looked for substrings: ['COMBI', 'DABRAFENIB-TRAMETINIB'])

### `IND-NSCLC-ALK-2L-LORLATINIB` (Indication — `ind_nsclc_alk_2l_lorlatinib.yaml`)
- **[missing-trial-source]** trial 'CROWN' mentioned but no matching source citation (looked for substrings: ['CROWN', 'LORLATINIB'])
- **[missing-trial-source]** trial 'TRIDENT-1' mentioned but no matching source citation (looked for substrings: ['TRIDENT-1'])

### `IND-NSCLC-ALK-MET-1L` (Indication — `ind_nsclc_alk_met_1l.yaml`)
- **[missing-trial-source]** trial 'ALEX' mentioned but no matching source citation (looked for substrings: ['ALEX', 'ALECTINIB'])
- **[missing-trial-source]** trial 'CROWN' mentioned but no matching source citation (looked for substrings: ['CROWN', 'LORLATINIB'])

### `IND-NSCLC-EGFR-MAINT-OSIMERTINIB` (Indication — `ind_nsclc_egfr_maint_osimertinib.yaml`)
- **[missing-trial-source]** trial 'FLAURA' mentioned but no matching source citation (looked for substrings: ['FLAURA', 'OSIMERTINIB', 'AURA'])
- **[missing-trial-source]** trial 'MARIPOSA' mentioned but no matching source citation (looked for substrings: ['MARIPOSA'])

### `IND-NSCLC-PDL1-LOW-NONSQ-MET-1L` (Indication — `ind_nsclc_pdl1_low_nonsq_met_1l.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-189' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-189', 'KEYNOTE189'])
- **[missing-trial-source]** trial 'KEYNOTE-407' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-407', 'KEYNOTE407'])

### `IND-NSCLC-PEMBRO-MAINTENANCE-POST-CHEMO` (Indication — `ind_nsclc_pembro_maintenance_post_chemo.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-189' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-189', 'KEYNOTE189'])
- **[missing-trial-source]** trial 'KEYNOTE-407' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-407', 'KEYNOTE407'])

### `IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-NEG` (Indication — `ind_ovarian_advanced_1l_carbo_pacli_hrd_neg.yaml`)
- **[missing-trial-source]** trial 'PRIMA' mentioned but no matching source citation (looked for substrings: ['PRIMA', 'NIRAPARIB'])
- **[missing-trial-source]** trial 'GOG-218' mentioned but no matching source citation (looked for substrings: ['GOG-218'])

### `IND-OVARIAN-ADVANCED-1L-CARBO-PACLI-HRD-OLAP` (Indication — `ind_ovarian_advanced_1l_carbo_pacli_hrd_olap.yaml`)
- **[missing-trial-source]** trial 'SOLO-1' mentioned but no matching source citation (looked for substrings: ['SOLO', 'OLAPARIB'])
- **[missing-trial-source]** trial 'PAOLA-1' mentioned but no matching source citation (looked for substrings: ['PAOLA', 'OLAPARIB'])

### `IND-OVARIAN-MAINTENANCE-OLAPARIB` (Indication — `ind_ovarian_maintenance_olaparib.yaml`)
- **[missing-trial-source]** trial 'SOLO-1' mentioned but no matching source citation (looked for substrings: ['SOLO', 'OLAPARIB'])
- **[missing-trial-source]** trial 'PAOLA-1' mentioned but no matching source citation (looked for substrings: ['PAOLA', 'OLAPARIB'])

### `IND-PROSTATE-MCRPC-1L-PARPI` (Indication — `ind_prostate_mcrpc_1l_parpi.yaml`)
- **[missing-trial-source]** trial 'MAGNITUDE' mentioned but no matching source citation (looked for substrings: ['MAGNITUDE', 'NIRAPARIB'])
- **[missing-trial-source]** trial 'TALAPRO-2' mentioned but no matching source citation (looked for substrings: ['TALAPRO', 'TALAZOPARIB'])

### `IND-SCLC-EXTENSIVE-1L` (Indication — `ind_sclc_extensive_1l.yaml`)
- **[missing-trial-source]** trial 'CASPIAN' mentioned but no matching source citation (looked for substrings: ['CASPIAN', 'DURVALUMAB-SCLC'])
- **[missing-trial-source]** trial 'IMpower133' mentioned but no matching source citation (looked for substrings: ['IMPOWER133', 'ATEZOLIZUMAB-SCLC'])

### `IND-UROTHELIAL-METASTATIC-1L-EV-PEMBRO` (Indication — `ind_urothelial_metastatic_1l_ev_pembro.yaml`)
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])
- **[missing-trial-source]** trial 'EV-302' mentioned but no matching source citation (looked for substrings: ['EV-302', 'EV302', 'ENFORTUMAB', 'PADCEV'])

### `REG-ADT-ABIRATERONE` (Regimen — `reg_adt_abiraterone.yaml`)
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])
- **[missing-trial-source]** trial 'LATITUDE' mentioned but no matching source citation (looked for substrings: ['LATITUDE', 'ABIRATERONE'])

### `REG-ALECTINIB-NSCLC` (Regimen — `reg_alectinib_nsclc.yaml`)
- **[missing-trial-source]** trial 'ALEX' mentioned but no matching source citation (looked for substrings: ['ALEX', 'ALECTINIB'])
- **[missing-trial-source]** trial 'ALINA' mentioned but no matching source citation (looked for substrings: ['ALINA', 'ALECTINIB'])

### `REG-CAR-T-AXICEL` (Regimen — `reg_car_t_axicel.yaml`)
- **[missing-trial-source]** trial 'ZUMA-1' mentioned but no matching source citation (looked for substrings: ['ZUMA-1', 'ZUMA1', 'AXICEL'])
- **[missing-trial-source]** trial 'ZUMA-7' mentioned but no matching source citation (looked for substrings: ['ZUMA-7', 'ZUMA7', 'AXICEL'])

### `REG-CAR-T-AXICEL-FL` (Regimen — `reg_car_t_axicel_fl.yaml`)
- **[missing-trial-source]** trial 'ZUMA-1' mentioned but no matching source citation (looked for substrings: ['ZUMA-1', 'ZUMA1', 'AXICEL'])
- **[missing-trial-source]** trial 'TRANSCEND' mentioned but no matching source citation (looked for substrings: ['TRANSCEND', 'LISOCABTAGENE'])

### `REG-CAR-T-AXICEL-HGBL` (Regimen — `reg_car_t_axicel_hgbl.yaml`)
- **[missing-trial-source]** trial 'ZUMA-1' mentioned but no matching source citation (looked for substrings: ['ZUMA-1', 'ZUMA1', 'AXICEL'])
- **[missing-trial-source]** trial 'ZUMA-7' mentioned but no matching source citation (looked for substrings: ['ZUMA-7', 'ZUMA7', 'AXICEL'])

### `REG-DOSTARLIMAB-MONO-ENDOM` (Regimen — `reg_dostarlimab_mono_endom.yaml`)
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])
- **[missing-trial-source]** trial 'NRG-GY018' mentioned but no matching source citation (looked for substrings: ['GY018', 'PEMBRO-ENDOM'])

### `REG-EV-PEMBRO-UROTHELIAL` (Regimen — `reg_ev_pembro_urothelial.yaml`)
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])
- **[missing-trial-source]** trial 'EV-302' mentioned but no matching source citation (looked for substrings: ['EV-302', 'EV302', 'ENFORTUMAB', 'PADCEV'])

### `REG-FOLFOX-CETUX` (Regimen — `folfox_cetuximab.yaml`)
- **[missing-trial-source]** trial 'FIRE-3' mentioned but no matching source citation (looked for substrings: ['FIRE-3'])
- **[missing-trial-source]** trial 'CRYSTAL' mentioned but no matching source citation (looked for substrings: ['CRYSTAL'])

### `REG-NIVO-ADJUVANT-ESOPH` (Regimen — `nivolumab_adjuvant_esophageal.yaml`)
- **[missing-trial-source]** trial 'CheckMate-577' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-577', 'CHECKMATE577'])
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])

### `REG-OLAPARIB-BREAST` (Regimen — `reg_olaparib_breast.yaml`)
- **[missing-trial-source]** trial 'OLYMPIA' mentioned but no matching source citation (looked for substrings: ['OLYMPIA', 'OLAPARIB'])
- **[missing-trial-source]** trial 'OLYMPIAD' mentioned but no matching source citation (looked for substrings: ['OLYMPIAD', 'OLAPARIB'])

### `REG-OLAPARIB-MAINT-OVARIAN` (Regimen — `olaparib_maintenance_ovarian.yaml`)
- **[missing-trial-source]** trial 'SOLO-1' mentioned but no matching source citation (looked for substrings: ['SOLO', 'OLAPARIB'])
- **[missing-trial-source]** trial 'PAOLA-1' mentioned but no matching source citation (looked for substrings: ['PAOLA', 'OLAPARIB'])

### `REG-OSIMERTINIB-NSCLC` (Regimen — `reg_osimertinib_nsclc.yaml`)
- **[missing-trial-source]** trial 'FLAURA' mentioned but no matching source citation (looked for substrings: ['FLAURA', 'OSIMERTINIB', 'AURA'])
- **[missing-trial-source]** trial 'ADAURA' mentioned but no matching source citation (looked for substrings: ['ADAURA', 'OSIMERTINIB'])

### `REG-PEMBRO-CHEMO-NSCLC-NONSQ` (Regimen — `reg_pembro_chemo_nsclc_nonsq.yaml`)
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])
- **[missing-trial-source]** trial 'KEYNOTE-189' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-189', 'KEYNOTE189'])

### `REG-PEMBROLIZUMAB-MAINTENANCE` (Regimen — `reg_pembrolizumab_maintenance.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-189' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-189', 'KEYNOTE189'])
- **[missing-trial-source]** trial 'KEYNOTE-407' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-407', 'KEYNOTE407'])

### `REG-RICE-BURKITT` (Regimen — `reg_rice_burkitt.yaml`)
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])
- **[missing-trial-source]** trial 'ZUMA-7' mentioned but no matching source citation (looked for substrings: ['ZUMA-7', 'ZUMA7', 'AXICEL'])

### `REG-SACITUZUMAB` (Regimen — `reg_sacituzumab.yaml`)
- **[missing-trial-source]** trial 'ASCENT' mentioned but no matching source citation (looked for substrings: ['ASCENT', 'SACITUZUMAB'])
- **[missing-trial-source]** trial 'TROPiCS-02' mentioned but no matching source citation (looked for substrings: ['TROPICS', 'SACITUZUMAB'])

### `REG-SELPERCATINIB-MTC-1L` (Regimen — `reg_selpercatinib_mtc_1l.yaml`)
- **[missing-trial-source]** trial 'LIBRETTO-001' mentioned but no matching source citation (looked for substrings: ['LIBRETTO', 'SELPERCATINIB'])
- **[missing-trial-source]** trial 'ARROW' mentioned but no matching source citation (looked for substrings: ['ARROW', 'PRALSETINIB'])

### `REG-TDXD-METASTATIC` (Regimen — `reg_tdxd_metastatic.yaml`)
- **[missing-trial-source]** trial 'DESTINY-Breast03' mentioned but no matching source citation (looked for substrings: ['DESTINY-BREAST03', 'TDXD', 'TRASTUZUMAB-DERUXTECAN'])
- **[missing-trial-source]** trial 'DESTINY-Breast04' mentioned but no matching source citation (looked for substrings: ['DESTINY-BREAST04', 'TDXD', 'TRASTUZUMAB-DERUXTECAN'])

### `REG-TECLISTAMAB` (Regimen — `reg_teclistamab.yaml`)
- **[missing-trial-source]** trial 'MajesTEC-1' mentioned but no matching source citation (looked for substrings: ['MAJESTEC', 'TECLISTAMAB'])
- **[missing-trial-source]** trial 'MonumenTAL-1' mentioned but no matching source citation (looked for substrings: ['MONUMENTAL', 'TALQUETAMAB'])

### `REG-VENETOCLAX-RITUXIMAB` (Regimen — `reg_venetoclax_rituximab.yaml`)
- **[missing-trial-source]** trial 'MURANO' mentioned but no matching source citation (looked for substrings: ['MURANO', 'VENETOCLAX'])
- **[missing-trial-source]** trial 'CLL14' mentioned but no matching source citation (looked for substrings: ['CLL14', 'VENETOCLAX'])

### `BMA-ATM-GERMLINE-PROSTATE` (BMA — `bma_atm_germline_prostate.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-ATM-LOSS-CLL` (BMA — `bma_atm_loss_cll.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-BRAF-V600E-NSCLC` (BMA — `bma_braf_v600e_nsclc.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-BRCA1-GERMLINE-PDAC` (BMA — `bma_brca1_germline_pdac.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-BRCA2-GERMLINE-PDAC` (BMA — `bma_brca2_germline_pdac.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-EGFR-G719X-NSCLC` (BMA — `bma_egfr_g719x_nsclc.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-FGFR2-BICC1-CHOLANGIO` (BMA — `bma_fgfr2_bicc1_cholangio.yaml`)
- **[missing-trial-source]** trial 'FIGHT-202' mentioned but no matching source citation (looked for substrings: ['FIGHT-202', 'PEMIGATINIB'])

### `BMA-FGFR2-FUSION-CHOLANGIO` (BMA — `bma_fgfr2_fusion_cholangio.yaml`)
- **[missing-trial-source]** trial 'FIGHT-202' mentioned but no matching source citation (looked for substrings: ['FIGHT-202', 'PEMIGATINIB'])

### `BMA-FGFR3-Y373C-UROTHELIAL` (BMA — `bma_fgfr3_y373c_urothelial.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-FLT3-D835-AML-RR` (BMA — `bma_flt3_d835_aml_rr.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-FLT3-ITD-AML-RR` (BMA — `bma_flt3_itd_aml_rr.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-IDH2-R140Q-AML` (BMA — `bma_idh2_r140q_aml.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-IDH2-R172K-AML` (BMA — `bma_idh2_r172k_aml.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-KIT-D816V-MASTOCYTOSIS` (BMA — `bma_kit_d816v_mastocytosis.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-MLH1-GERMLINE-UROTHELIAL` (BMA — `bma_mlh1_germline_urothelial.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-MLH1-SOMATIC-UROTHELIAL` (BMA — `bma_mlh1_somatic_urothelial.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-MSH2-GERMLINE-UROTHELIAL` (BMA — `bma_msh2_germline_urothelial.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-MSH2-SOMATIC-UROTHELIAL` (BMA — `bma_msh2_somatic_urothelial.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-MSH6-GERMLINE-UROTHELIAL` (BMA — `bma_msh6_germline_urothelial.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-MSH6-SOMATIC-UROTHELIAL` (BMA — `bma_msh6_somatic_urothelial.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-MYD88-L265P-WM` (BMA — `bma_myd88_l265p_wm.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-NTRK-ETV6-SALIVARY` (BMA — `bma_ntrk_etv6_salivary.yaml`)
- **[missing-trial-source]** trial 'STARTRK' mentioned but no matching source citation (looked for substrings: ['STARTRK'])

### `BMA-NTRK-FUSION-CRC` (BMA — `bma_ntrk_fusion_crc.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-NTRK-FUSION-IFS` (BMA — `bma_ntrk_fusion_ifs.yaml`)
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])

### `BMA-NTRK-FUSION-NSCLC` (BMA — `bma_ntrk_fusion_nsclc.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (2) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-NTRK-FUSION-SALIVARY` (BMA — `bma_ntrk_fusion_salivary.yaml`)
- **[missing-trial-source]** trial 'STARTRK' mentioned but no matching source citation (looked for substrings: ['STARTRK'])

### `BMA-NTRK-FUSION-THYROID-PAPILLARY` (BMA — `bma_ntrk_fusion_thyroid_papillary.yaml`)
- **[missing-trial-source]** trial 'STARTRK' mentioned but no matching source citation (looked for substrings: ['STARTRK'])

### `BMA-PDGFRA-EXON12-GIST` (BMA — `bma_pdgfra_exon12_gist.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-PDGFRA-EXON14-GIST` (BMA — `bma_pdgfra_exon14_gist.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-PDGFRA-EXON18-NON-D842-GIST` (BMA — `bma_pdgfra_exon18_non_d842_gist.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-PIK3CA-E542K-BREAST` (BMA — `bma_pik3ca_e542k_breast.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-PIK3CA-E545K-BREAST` (BMA — `bma_pik3ca_e545k_breast.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-PIK3CA-H1047L-BREAST` (BMA — `bma_pik3ca_h1047l_breast.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-PIK3CA-H1047R-BREAST` (BMA — `bma_pik3ca_h1047r_breast.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (3) + EMA approvals listed (2) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-PMS2-GERMLINE-UROTHELIAL` (BMA — `bma_pms2_germline_urothelial.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-PMS2-SOMATIC-UROTHELIAL` (BMA — `bma_pms2_somatic_urothelial.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-ROS1-CD74-NSCLC` (BMA — `bma_ros1_cd74_nsclc.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-ROS1-EZR-NSCLC` (BMA — `bma_ros1_ezr_nsclc.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `BMA-ROS1-SLC34A2-NSCLC` (BMA — `bma_ros1_slc34a2_nsclc.yaml`)
- **[missing-regulatory-source]** regulatory_approval cites FDA approvals listed (1) + EMA approvals listed (1) but no FDA/EMA-tagged Source entity is among primary_sources

### `IND-AITL-1L-CHP-BV` (Indication — `ind_aitl_1l_chp_bv.yaml`)
- **[missing-trial-source]** trial 'ECHELON-2' mentioned but no matching source citation (looked for substrings: ['ECHELON-2', 'ECHELON2', 'BRENTUXIMAB'])

### `IND-APL-1L-ATRA-ATO` (Indication — `ind_apl_1l_atra_ato.yaml`)
- **[missing-trial-source]** trial 'AIDA' mentioned but no matching source citation (looked for substrings: ['AIDA'])

### `IND-APL-SALVAGE-ATRA-ATO` (Indication — `ind_apl_salvage_atra_ato.yaml`)
- **[missing-trial-source]** trial 'AIDA' mentioned but no matching source citation (looked for substrings: ['AIDA'])

### `IND-ATLL-2L-MOGAMULIZUMAB` (Indication — `ind_atll_2l_mogamulizumab.yaml`)
- **[missing-trial-source]** trial 'BRIGHT' mentioned but no matching source citation (looked for substrings: ['BRIGHT'])

### `IND-B-ALL-POST-CONSOLIDATION-POMP-MAINTENANCE` (Indication — `ind_b_all_post_consolidation_pomp_maintenance.yaml`)
- **[missing-trial-source]** trial 'QUAZAR' mentioned but no matching source citation (looked for substrings: ['QUAZAR', 'ORAL-AZA', 'CC-486'])

### `IND-BREAST-HER2-POS-MAINT-TRAST` (Indication — `ind_breast_her2_pos_maint_trast.yaml`)
- **[missing-trial-source]** trial 'CLEOPATRA' mentioned but no matching source citation (looked for substrings: ['CLEOPATRA', 'PERTUZUMAB'])

### `IND-BREAST-HER2-POS-MET-1L-THP` (Indication — `ind_breast_her2_pos_met_1l_thp.yaml`)
- **[missing-trial-source]** trial 'CLEOPATRA' mentioned but no matching source citation (looked for substrings: ['CLEOPATRA', 'PERTUZUMAB'])

### `IND-BREAST-HER2-POS-MET-2L-TDXD` (Indication — `ind_breast_her2_pos_met_2l_tdxd.yaml`)
- **[missing-trial-source]** trial 'DESTINY-Breast03' mentioned but no matching source citation (looked for substrings: ['DESTINY-BREAST03', 'TDXD', 'TRASTUZUMAB-DERUXTECAN'])

### `IND-BURKITT-2L-RDHAP-ASCT` (Indication — `ind_burkitt_2l_rdhap_asct.yaml`)
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])

### `IND-BURKITT-2L-RICE-ASCT` (Indication — `ind_burkitt_2l_rice_asct.yaml`)
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])

### `IND-CHL-1L-A-AVD` (Indication — `ind_chl_1l_a_avd.yaml`)
- **[missing-trial-source]** trial 'ECHELON-1' mentioned but no matching source citation (looked for substrings: ['ECHELON-1', 'ECHELON1', 'BRENTUXIMAB'])

### `IND-CHL-1L-ABVD` (Indication — `ind_chl_1l_abvd.yaml`)
- **[missing-trial-source]** trial 'ECHELON-1' mentioned but no matching source citation (looked for substrings: ['ECHELON-1', 'ECHELON1', 'BRENTUXIMAB'])

### `IND-CLL-1L-BTKI` (Indication — `ind_cll_1l_btki.yaml`)
- **[missing-trial-source]** trial 'CLL14' mentioned but no matching source citation (looked for substrings: ['CLL14', 'VENETOCLAX'])

### `IND-CLL-1L-VENO` (Indication — `ind_cll_1l_veno.yaml`)
- **[missing-trial-source]** trial 'CLL14' mentioned but no matching source citation (looked for substrings: ['CLL14', 'VENETOCLAX'])

### `IND-CLL-3L-PIRTOBRUTINIB` (Indication — `ind_cll_3l_pirtobrutinib.yaml`)
- **[missing-trial-source]** trial 'TRANSCEND' mentioned but no matching source citation (looked for substrings: ['TRANSCEND', 'LISOCABTAGENE'])

### `IND-CML-3L-ASCIMINIB` (Indication — `ind_cml_3l_asciminib.yaml`)
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])

### `IND-CRC-METASTATIC-1L-MSI-H-PEMBRO` (Indication — `ind_crc_metastatic_1l_msi_h_pembro.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-177' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-177', 'KEYNOTE177'])

### `IND-CRC-METASTATIC-1L-RAS-WT-LEFT` (Indication — `ind_crc_metastatic_1l_ras_wt_left.yaml`)
- **[missing-trial-source]** trial 'FIRE-3' mentioned but no matching source citation (looked for substrings: ['FIRE-3'])

### `IND-CRC-METASTATIC-2L-BRAF-BEACON` (Indication — `ind_crc_metastatic_2l_braf_beacon.yaml`)
- **[missing-trial-source]** trial 'BEACON' mentioned but no matching source citation (looked for substrings: ['BEACON', 'ENCORAFENIB', 'KOPETZ'])

### `IND-CRC-METASTATIC-2L-FOLFIRI-BEV` (Indication — `ind_crc_metastatic_2l_folfiri_bev.yaml`)
- **[missing-trial-source]** trial 'BEACON' mentioned but no matching source citation (looked for substrings: ['BEACON', 'ENCORAFENIB', 'KOPETZ'])

### `IND-CRC-METASTATIC-3L-TAS102-BEV` (Indication — `ind_crc_metastatic_3l_tas102_bev.yaml`)
- **[missing-trial-source]** trial 'BEACON' mentioned but no matching source citation (looked for substrings: ['BEACON', 'ENCORAFENIB', 'KOPETZ'])

### `IND-CRC-METASTATIC-MAINT-FOLFIRI-BEV` (Indication — `ind_crc_metastatic_maint_folfiri_bev.yaml`)
- **[missing-trial-source]** trial 'PRODIGE' mentioned but no matching source citation (looked for substrings: ['PRODIGE'])

### `IND-EATL-2L-ICE` (Indication — `ind_eatl_2l_ice.yaml`)
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])

### `IND-ENDOMETRIAL-ADVANCED-1L-DOSTARLIMAB-CHEMO` (Indication — `ind_endometrial_advanced_1l_dostarlimab_chemo.yaml`)
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])

### `IND-ESOPH-METASTATIC-2L-NIVO-SQUAMOUS` (Indication — `ind_esoph_metastatic_2l_nivo_squamous.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-590' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-590', 'KEYNOTE590'])

### `IND-ESOPH-RESECTABLE-CROSS-NEOADJUVANT` (Indication — `ind_esoph_resectable_cross_neoadjuvant.yaml`)
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])

### `IND-FL-3L-AXICEL-CART` (Indication — `ind_fl_3l_axicel_cart.yaml`)
- **[missing-trial-source]** trial 'TRANSCEND' mentioned but no matching source citation (looked for substrings: ['TRANSCEND', 'LISOCABTAGENE'])

### `IND-FL-3L-MOSUNETUZUMAB` (Indication — `ind_fl_3l_mosunetuzumab.yaml`)
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])

### `IND-FL-POST-INDUCTION-RITUXIMAB-MAINTENANCE` (Indication — `ind_fl_post_induction_rituximab_maintenance.yaml`)
- **[missing-trial-source]** trial 'PRIMA' mentioned but no matching source citation (looked for substrings: ['PRIMA', 'NIRAPARIB'])

### `IND-GASTRIC-METASTATIC-1L-PDL1-CHEMO-ICI` (Indication — `ind_gastric_metastatic_1l_pdl1_chemo_ici.yaml`)
- **[missing-trial-source]** trial 'CheckMate-649' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-649', 'CHECKMATE649'])

### `IND-GBM-NEWLY-DIAGNOSED-STUPP` (Indication — `ind_gbm_newly_diagnosed_stupp.yaml`)
- **[missing-trial-source]** trial 'Stupp' mentioned but no matching source citation (looked for substrings: ['STUPP', 'TEMOZOLOMIDE'])

### `IND-GIST-1L-IMATINIB` (Indication — `ind_gist_1l_imatinib.yaml`)
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])

### `IND-MDS-LR-1L-ESA` (Indication — `ind_mds_lr_1l_esa.yaml`)
- **[missing-trial-source]** trial 'COMMANDS' mentioned but no matching source citation (looked for substrings: ['COMMANDS'])

### `IND-MELANOMA-METASTATIC-1L-NIVO-IPI` (Indication — `ind_melanoma_metastatic_1l_nivo_ipi.yaml`)
- **[missing-trial-source]** trial 'CheckMate-067' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-067', 'CHECKMATE067'])

### `IND-MELANOMA-NIVO-MAINT` (Indication — `ind_melanoma_nivo_maint.yaml`)
- **[missing-trial-source]** trial 'CheckMate-067' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-067', 'CHECKMATE067'])

### `IND-MM-1L-DVRD` (Indication — `ind_mm_1l_dvrd.yaml`)
- **[missing-trial-source]** trial 'GRIFFIN' mentioned but no matching source citation (looked for substrings: ['GRIFFIN'])

### `IND-MM-4L-TECLISTAMAB` (Indication — `ind_mm_4l_teclistamab.yaml`)
- **[missing-trial-source]** trial 'MajesTEC-1' mentioned but no matching source citation (looked for substrings: ['MAJESTEC', 'TECLISTAMAB'])

### `IND-MTC-ADVANCED-1L-CABOZANTINIB-RET-WT` (Indication — `ind_mtc_advanced_1l_cabozantinib_ret_wt.yaml`)
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])

### `IND-NLPBL-2L-RCHOP-TRANSFORMATION` (Indication — `ind_nlpbl_2l_rchop_transformation.yaml`)
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])

### `IND-NMZL-1L-WATCH` (Indication — `ind_nmzl_1l_watch.yaml`)
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])

### `IND-NSCLC-2L-DOCETAXEL-RAMUCIRUMAB` (Indication — `ind_nsclc_2l_docetaxel_ramucirumab.yaml`)
- **[missing-trial-source]** trial 'IMpower150' mentioned but no matching source citation (looked for substrings: ['IMPOWER150'])

### `IND-NSCLC-EGFR-MUT-MET-1L` (Indication — `ind_nsclc_egfr_mut_met_1l.yaml`)
- **[missing-trial-source]** trial 'FLAURA' mentioned but no matching source citation (looked for substrings: ['FLAURA', 'OSIMERTINIB', 'AURA'])

### `IND-NSCLC-KRAS-G12C-MET-2L` (Indication — `ind_nsclc_kras_g12c_met_2l.yaml`)
- **[missing-trial-source]** trial 'CodeBreaK' mentioned but no matching source citation (looked for substrings: ['CODEBREAK', 'SOTORASIB'])

### `IND-NSCLC-PDL1-HIGH-MET-1L` (Indication — `ind_nsclc_pdl1_high_met_1l.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-024' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-024', 'KEYNOTE024'])

### `IND-NSCLC-STAGE-III-PACIFIC` (Indication — `ind_nsclc_stage_iii_pacific.yaml`)
- **[missing-trial-source]** trial 'PACIFIC' mentioned but no matching source citation (looked for substrings: ['PACIFIC', 'DURVALUMAB'])

### `IND-PDAC-METASTATIC-1L-FOLFIRINOX` (Indication — `ind_pdac_metastatic_1l_folfirinox.yaml`)
- **[missing-trial-source]** trial 'PRODIGE' mentioned but no matching source citation (looked for substrings: ['PRODIGE'])

### `IND-PROSTATE-MCRPC-2L-LU-PSMA` (Indication — `ind_prostate_mcrpc_2l_lu_psma.yaml`)
- **[missing-trial-source]** trial 'VISION' mentioned but no matching source citation (looked for substrings: ['VISION', 'LUTETIUM', 'PSMA'])

### `IND-PROSTATE-MHSPC-1L-TRIPLET` (Indication — `ind_prostate_mhspc_1l_triplet.yaml`)
- **[missing-trial-source]** trial 'ARASENS' mentioned but no matching source citation (looked for substrings: ['ARASENS', 'DAROLUTAMIDE'])

### `IND-PTCL-1L-CHOEP-ALLOSCT` (Indication — `ind_ptcl_1l_choep_allosct.yaml`)
- **[missing-trial-source]** trial 'ECHELON-2' mentioned but no matching source citation (looked for substrings: ['ECHELON-2', 'ECHELON2', 'BRENTUXIMAB'])

### `IND-PTCL-2L-PRALATREXATE` (Indication — `ind_ptcl_2l_pralatrexate.yaml`)
- **[missing-trial-source]** trial 'PROpel' mentioned but no matching source citation (looked for substrings: ['PROPEL', 'OLAPARIB-PROST'])

### `IND-RCC-METASTATIC-1L-NIVO-IPI` (Indication — `ind_rcc_metastatic_1l_nivo_ipi.yaml`)
- **[missing-trial-source]** trial 'CheckMate-214' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-214', 'CHECKMATE214'])

### `IND-RCC-METASTATIC-1L-PEMBRO-AXI` (Indication — `ind_rcc_metastatic_1l_pembro_axi.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-426' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-426', 'KEYNOTE426'])

### `IND-TCELL-1L-CHP-BV` (Indication — `ind_tcell_1l_chp_bv.yaml`)
- **[missing-trial-source]** trial 'ECHELON-2' mentioned but no matching source citation (looked for substrings: ['ECHELON-2', 'ECHELON2', 'BRENTUXIMAB'])

### `IND-WM-2L-VRD` (Indication — `ind_wm_2l_vrd.yaml`)
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])

### `REG-A-AVD` (Regimen — `a_avd.yaml`)
- **[missing-trial-source]** trial 'ECHELON-1' mentioned but no matching source citation (looked for substrings: ['ECHELON-1', 'ECHELON1', 'BRENTUXIMAB'])

### `REG-ABVD` (Regimen — `abvd.yaml`)
- **[missing-trial-source]** trial 'ECHELON-1' mentioned but no matching source citation (looked for substrings: ['ECHELON-1', 'ECHELON1', 'BRENTUXIMAB'])

### `REG-ACALABRUTINIB-RITUXIMAB` (Regimen — `acalabrutinib_rituximab.yaml`)
- **[missing-trial-source]** trial 'SHINE' mentioned but no matching source citation (looked for substrings: ['SHINE', 'IBRUTINIB-MCL'])

### `REG-ADT-APALUTAMIDE` (Regimen — `reg_adt_apalutamide.yaml`)
- **[missing-trial-source]** trial 'TITAN' mentioned but no matching source citation (looked for substrings: ['TITAN', 'APALUTAMIDE'])

### `REG-ADT-DAROLUTAMIDE-DOCETAXEL` (Regimen — `reg_adt_darolutamide_docetaxel.yaml`)
- **[missing-trial-source]** trial 'ARASENS' mentioned but no matching source citation (looked for substrings: ['ARASENS', 'DAROLUTAMIDE'])

### `REG-ADT-ENZALUTAMIDE` (Regimen — `reg_adt_enzalutamide.yaml`)
- **[missing-trial-source]** trial 'ENZAMET' mentioned but no matching source citation (looked for substrings: ['ENZAMET', 'ENZALUTAMIDE'])

### `REG-AI-PALBOCICLIB` (Regimen — `reg_ai_palbociclib.yaml`)
- **[missing-trial-source]** trial 'PALOMA-2' mentioned but no matching source citation (looked for substrings: ['PALOMA', 'PALBOCICLIB'])

### `REG-AI-RIBOCICLIB` (Regimen — `reg_ai_ribociclib.yaml`)
- **[missing-trial-source]** trial 'MONALEESA-2' mentioned but no matching source citation (looked for substrings: ['MONALEESA', 'RIBOCICLIB'])

### `REG-ASCIMINIB-CML` (Regimen — `reg_asciminib_cml.yaml`)
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])

### `REG-ATRA-ATO-APL` (Regimen — `atra_ato_apl.yaml`)
- **[missing-trial-source]** trial 'AIDA' mentioned but no matching source citation (looked for substrings: ['AIDA'])

### `REG-ATRA-ATO-APL-SALVAGE` (Regimen — `reg_atra_ato_apl_salvage.yaml`)
- **[missing-trial-source]** trial 'AIDA' mentioned but no matching source citation (looked for substrings: ['AIDA'])

### `REG-ATRA-ATO-IDA-APL` (Regimen — `atra_ato_ida_apl.yaml`)
- **[missing-trial-source]** trial 'AIDA' mentioned but no matching source citation (looked for substrings: ['AIDA'])

### `REG-AZA-MDS-HR` (Regimen — `azacitidine_mds_hr.yaml`)
- **[missing-trial-source]** trial 'VIALE-A' mentioned but no matching source citation (looked for substrings: ['VIALE-A', 'VIALEA', 'VEN-AZA'])

### `REG-BRENTUXIMAB-MAINTENANCE-ALCL` (Regimen — `reg_brentuximab_maintenance_alcl.yaml`)
- **[missing-trial-source]** trial 'ECHELON-2' mentioned but no matching source citation (looked for substrings: ['ECHELON-2', 'ECHELON2', 'BRENTUXIMAB'])

### `REG-CARBO-PACLI-OVARIAN` (Regimen — `carboplatin_paclitaxel_ovarian.yaml`)
- **[missing-trial-source]** trial 'GOG-218' mentioned but no matching source citation (looked for substrings: ['GOG-218'])

### `REG-CARBOPLATIN-PACLITAXEL-WEEKLY` (Regimen — `carboplatin_paclitaxel_weekly.yaml`)
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])

### `REG-CHP-BV` (Regimen — `chp_bv.yaml`)
- **[missing-trial-source]** trial 'ECHELON-2' mentioned but no matching source citation (looked for substrings: ['ECHELON-2', 'ECHELON2', 'BRENTUXIMAB'])

### `REG-DARA-VRD` (Regimen — `dara_vrd.yaml`)
- **[missing-trial-source]** trial 'GRIFFIN' mentioned but no matching source citation (looked for substrings: ['GRIFFIN'])

### `REG-DOSTARLIMAB-CARBO-PACLI-ENDOM` (Regimen — `reg_dostarlimab_carbo_pacli_endom.yaml`)
- **[missing-trial-source]** trial 'RUBY' mentioned but no matching source citation (looked for substrings: ['RUBY', 'DOSTARLIMAB'])

### `REG-DURVA-CONSOLIDATION-PACIFIC` (Regimen — `reg_durva_consolidation_pacific.yaml`)
- **[missing-trial-source]** trial 'PACIFIC' mentioned but no matching source citation (looked for substrings: ['PACIFIC', 'DURVALUMAB'])

### `REG-ENCORAFENIB-CETUXIMAB` (Regimen — `encorafenib_cetuximab_beacon.yaml`)
- **[missing-trial-source]** trial 'BEACON' mentioned but no matching source citation (looked for substrings: ['BEACON', 'ENCORAFENIB', 'KOPETZ'])

### `REG-EP-ATEZO-SCLC` (Regimen — `reg_ep_atezo_sclc.yaml`)
- **[missing-trial-source]** trial 'IMpower133' mentioned but no matching source citation (looked for substrings: ['IMPOWER133', 'ATEZOLIZUMAB-SCLC'])

### `REG-EP-DURVA-SCLC` (Regimen — `reg_ep_durva_sclc.yaml`)
- **[missing-trial-source]** trial 'CASPIAN' mentioned but no matching source citation (looked for substrings: ['CASPIAN', 'DURVALUMAB-SCLC'])

### `REG-ESA-MDS-LR` (Regimen — `esa_mds_lr.yaml`)
- **[missing-trial-source]** trial 'COMMANDS' mentioned but no matching source citation (looked for substrings: ['COMMANDS'])

### `REG-FOLFIRINOX` (Regimen — `folfirinox.yaml`)
- **[missing-trial-source]** trial 'PRODIGE' mentioned but no matching source citation (looked for substrings: ['PRODIGE'])

### `REG-FOLFOX-NIVO` (Regimen — `folfox_nivolumab.yaml`)
- **[missing-trial-source]** trial 'CheckMate-649' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-649', 'CHECKMATE649'])

### `REG-LORLATINIB-NSCLC` (Regimen — `reg_lorlatinib_nsclc.yaml`)
- **[missing-trial-source]** trial 'CROWN' mentioned but no matching source citation (looked for substrings: ['CROWN', 'LORLATINIB'])

### `REG-LUTETIUM-PSMA` (Regimen — `reg_lutetium_psma.yaml`)
- **[missing-trial-source]** trial 'VISION' mentioned but no matching source citation (looked for substrings: ['VISION', 'LUTETIUM', 'PSMA'])

### `REG-NIVO-IPI-MELANOMA` (Regimen — `reg_nivo_ipi_melanoma.yaml`)
- **[missing-trial-source]** trial 'CheckMate-067' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-067', 'CHECKMATE067'])

### `REG-NIVO-IPI-RCC` (Regimen — `reg_nivo_ipi_rcc.yaml`)
- **[missing-trial-source]** trial 'CheckMate-214' mentioned but no matching source citation (looked for substrings: ['CHECKMATE-214', 'CHECKMATE214'])

### `REG-PEMBRO-AXI-RCC` (Regimen — `reg_pembro_axi_rcc.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-426' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-426', 'KEYNOTE426'])

### `REG-PEMBRO-CARBO-PACLI-ENDOM` (Regimen — `reg_pembro_carbo_pacli_endom.yaml`)
- **[missing-trial-source]** trial 'NRG-GY018' mentioned but no matching source citation (looked for substrings: ['GY018', 'PEMBRO-ENDOM'])

### `REG-PEMBRO-CHEMO-TNBC-NEOADJUVANT` (Regimen — `reg_pembro_chemo_tnbc_neoadjuvant.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-522' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-522', 'KEYNOTE522'])

### `REG-PEMBRO-MONO-ESOPH-2L` (Regimen — `reg_pembro_mono_esoph_2l.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-590' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-590', 'KEYNOTE590'])

### `REG-PEMBRO-MONO-NSCLC` (Regimen — `reg_pembro_mono_nsclc.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-024' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-024', 'KEYNOTE024'])

### `REG-PEMBROLIZUMAB-MSI-MONO` (Regimen — `pembrolizumab_msi_mono.yaml`)
- **[missing-trial-source]** trial 'KEYNOTE-177' mentioned but no matching source citation (looked for substrings: ['KEYNOTE-177', 'KEYNOTE177'])

### `REG-PRALATREXATE-PTCL` (Regimen — `reg_pralatrexate_ptcl.yaml`)
- **[missing-trial-source]** trial 'PROpel' mentioned but no matching source citation (looked for substrings: ['PROPEL', 'OLAPARIB-PROST'])

### `REG-RDHAP-BURKITT` (Regimen — `reg_rdhap_burkitt.yaml`)
- **[missing-trial-source]** trial 'CROSS' mentioned but no matching source citation (looked for substrings: ['CROSS'])

### `REG-RITUXIMAB-MAINTENANCE-FL` (Regimen — `reg_rituximab_maintenance_fl.yaml`)
- **[missing-trial-source]** trial 'PRIMA' mentioned but no matching source citation (looked for substrings: ['PRIMA', 'NIRAPARIB'])

### `REG-SOTORASIB-KRAS` (Regimen — `reg_sotorasib_kras.yaml`)
- **[missing-trial-source]** trial 'CodeBreaK' mentioned but no matching source citation (looked for substrings: ['CODEBREAK', 'SOTORASIB'])

### `REG-STUPP-TMZ` (Regimen — `stupp_temozolomide.yaml`)
- **[missing-trial-source]** trial 'Stupp' mentioned but no matching source citation (looked for substrings: ['STUPP', 'TEMOZOLOMIDE'])

### `REG-TCHP-NEOADJUVANT` (Regimen — `reg_tchp_neoadjuvant.yaml`)
- **[missing-trial-source]** trial 'KATHERINE' mentioned but no matching source citation (looked for substrings: ['KATHERINE', 'TDM1'])

### `REG-TDM1-ADJUVANT` (Regimen — `reg_tdm1_adjuvant.yaml`)
- **[missing-trial-source]** trial 'KATHERINE' mentioned but no matching source citation (looked for substrings: ['KATHERINE', 'TDM1'])

### `REG-THP-METASTATIC` (Regimen — `reg_thp_metastatic.yaml`)
- **[missing-trial-source]** trial 'CLEOPATRA' mentioned but no matching source citation (looked for substrings: ['CLEOPATRA', 'PERTUZUMAB'])

### `REG-VENETOCLAX-OBINUTUZUMAB` (Regimen — `venetoclax_obinutuzumab.yaml`)
- **[missing-trial-source]** trial 'CLL14' mentioned but no matching source citation (looked for substrings: ['CLL14', 'VENETOCLAX'])

### `REG-VRD-WM` (Regimen — `reg_vrd_wm.yaml`)
- **[missing-trial-source]** trial 'PARADIGM' mentioned but no matching source citation (looked for substrings: ['PARADIGM'])

### `BMA-BCL2-REARRANGEMENT-FL` (BMA — `bma_bcl2_rearrangement_fl.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'
- **[drug-inconsistency]** recommended_combination 'BR or R-CHOP or O-CHOP/O-Benda (1L per FLIPI/burden)' contains drug name(s) ['r-chop', 'o-chop', 'o-benda'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'tazemetostat (EZH2-mut R/R)' contains drug name(s) ['tazemetostat'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'mosunetuzumab / axi-cel (R/R 3L+)' contains drug name(s) ['mosunetuzumab', 'axi-cel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-MUT-AML` (BMA — `bma_tp53_mut_aml.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'azacitidine + venetoclax (palliative, R/R)' contains drug name(s) ['azacitidine', 'venetoclax'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'decitabine 10-day' contains drug name(s) ['decitabine'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'alloSCT consideration' contains drug name(s) ['allosct'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BCL2-EXPRESSION-DLBCL-NOS` (BMA — `bma_bcl2_expression_dlbcl_nos.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'R-CHOP / pola-R-CHP per usual algorithm' contains drug name(s) ['r-chop', 'pola-r-chp'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'venetoclax + R-CHOP (trial; CAVALLI)' contains drug name(s) ['venetoclax', 'r-chop'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-FANCA-GERMLINE-OVARIAN` (BMA — `bma_fanca_germline_ovarian.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'
- **[drug-inconsistency]** recommended_combination 'niraparib (HRD-positive)' contains drug name(s) ['niraparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab' contains drug name(s) ['olaparib', 'bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-FANCL-GERMLINE-OVARIAN` (BMA — `bma_fancl_germline_ovarian.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'
- **[drug-inconsistency]** recommended_combination 'niraparib (HRD-positive)' contains drug name(s) ['niraparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab' contains drug name(s) ['olaparib', 'bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MYC-REARRANGEMENT-NLPBL` (BMA — `bma_myc_rearrangement_nlpbl.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'R-CHOP' contains drug name(s) ['r-chop'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'DA-EPOCH-R (if HGBL-DH)' contains drug name(s) ['da-epoch-r'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-MUT-DLBCL-NOS` (BMA — `bma_tp53_mut_dlbcl_nos.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'pola-R-CHP (1L; not TP53-selected)' contains drug name(s) ['pola-r-chp'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'CAR-T axi-cel / liso-cel (2L+)' contains drug name(s) ['car-t', 'liso-cel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-MUT-MDS-HR` (BMA — `bma_tp53_mut_mds_hr.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'alloSCT consideration (preferred curative path despite poor outcomes)' contains drug name(s) ['allosct'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'azacitidine + venetoclax (palliative; modest CR but non-durable)' contains drug name(s) ['azacitidine', 'venetoclax'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R175H-AML` (BMA — `bma_tp53_r175h_aml.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'azacitidine + venetoclax' contains drug name(s) ['azacitidine', 'venetoclax'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'alloSCT consideration' contains drug name(s) ['allosct'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R175H-CLL` (BMA — `bma_tp53_r175h_cll.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3A'
- **[drug-inconsistency]** recommended_combination 'acalabrutinib' contains drug name(s) ['acalabrutinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'venetoclax + obinutuzumab' contains drug name(s) ['venetoclax', 'obinutuzumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R175H-DLBCL-NOS` (BMA — `bma_tp53_r175h_dlbcl_nos.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'pola-R-CHP' contains drug name(s) ['pola-r-chp'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'CAR-T 2L+' contains drug name(s) ['car-t'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R175H-MDS-HR` (BMA — `bma_tp53_r175h_mds_hr.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'azacitidine + venetoclax' contains drug name(s) ['azacitidine', 'venetoclax'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'alloSCT consideration' contains drug name(s) ['allosct'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R248Q-AML` (BMA — `bma_tp53_r248q_aml.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'azacitidine + venetoclax' contains drug name(s) ['azacitidine', 'venetoclax'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'alloSCT consideration' contains drug name(s) ['allosct'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R248Q-CLL` (BMA — `bma_tp53_r248q_cll.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3A'
- **[drug-inconsistency]** recommended_combination 'acalabrutinib' contains drug name(s) ['acalabrutinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'venetoclax + obinutuzumab' contains drug name(s) ['venetoclax', 'obinutuzumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R248Q-DLBCL-NOS` (BMA — `bma_tp53_r248q_dlbcl_nos.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'pola-R-CHP' contains drug name(s) ['pola-r-chp'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'CAR-T 2L+' contains drug name(s) ['car-t'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R248Q-MDS-HR` (BMA — `bma_tp53_r248q_mds_hr.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'azacitidine + venetoclax' contains drug name(s) ['azacitidine', 'venetoclax'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'alloSCT consideration' contains drug name(s) ['allosct'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R273H-AML` (BMA — `bma_tp53_r273h_aml.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'azacitidine + venetoclax' contains drug name(s) ['azacitidine', 'venetoclax'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'alloSCT consideration' contains drug name(s) ['allosct'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R273H-CLL` (BMA — `bma_tp53_r273h_cll.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3A'
- **[drug-inconsistency]** recommended_combination 'acalabrutinib' contains drug name(s) ['acalabrutinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'venetoclax + obinutuzumab' contains drug name(s) ['venetoclax', 'obinutuzumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R273H-DLBCL-NOS` (BMA — `bma_tp53_r273h_dlbcl_nos.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'pola-R-CHP' contains drug name(s) ['pola-r-chp'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'CAR-T 2L+' contains drug name(s) ['car-t'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R273H-MDS-HR` (BMA — `bma_tp53_r273h_mds_hr.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'azacitidine + venetoclax' contains drug name(s) ['azacitidine', 'venetoclax'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'alloSCT consideration' contains drug name(s) ['allosct'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R282W-AML` (BMA — `bma_tp53_r282w_aml.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'azacitidine + venetoclax' contains drug name(s) ['azacitidine', 'venetoclax'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'alloSCT consideration' contains drug name(s) ['allosct'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R282W-CLL` (BMA — `bma_tp53_r282w_cll.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3A'
- **[drug-inconsistency]** recommended_combination 'acalabrutinib' contains drug name(s) ['acalabrutinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'venetoclax + obinutuzumab' contains drug name(s) ['venetoclax', 'obinutuzumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R282W-DLBCL-NOS` (BMA — `bma_tp53_r282w_dlbcl_nos.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'pola-R-CHP' contains drug name(s) ['pola-r-chp'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'CAR-T 2L+' contains drug name(s) ['car-t'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R282W-MDS-HR` (BMA — `bma_tp53_r282w_mds_hr.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'azacitidine + venetoclax' contains drug name(s) ['azacitidine', 'venetoclax'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'alloSCT consideration' contains drug name(s) ['allosct'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BCL2-EXPRESSION-FL` (BMA — `bma_bcl2_expression_fl.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'
- **[drug-inconsistency]** recommended_combination 'BR / R-CHOP / O-Benda per FLIPI / burden' contains drug name(s) ['r-chop', 'o-benda', 'burden'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BCL2-EXPRESSION-MCL` (BMA — `bma_bcl2_expression_mcl.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'
- **[drug-inconsistency]** recommended_combination 'venetoclax + acalabrutinib (trials)' contains drug name(s) ['venetoclax', 'acalabrutinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BCL2-REARRANGEMENT-DLBCL-NOS` (BMA — `bma_bcl2_rearrangement_dlbcl_nos.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'R-CHOP / pola-R-CHP per usual DLBCL algorithm' contains drug name(s) ['r-chop', 'pola-r-chp'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRAF-V600E-MM` (BMA — `bma_braf_v600e_mm.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'
- **[drug-inconsistency]** recommended_combination 'vemurafenib (case-report level)' contains drug name(s) ['vemurafenib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRCA2-GERMLINE-MELANOMA` (BMA — `bma_brca2_germline_melanoma.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'
- **[drug-inconsistency]** recommended_combination 'standard melanoma therapy by stage/biomarker (ICI, BRAFi+MEKi if BRAF V600)' contains drug name(s) ['biomarker'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-CHEK1-SOMATIC-OVARIAN` (BMA — `bma_chek1_somatic_ovarian.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'
- **[drug-inconsistency]** recommended_combination 'platinum-based chemo' contains drug name(s) ['platinum-based'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-IDH1-R132G-GBM` (BMA — `bma_idh1_r132g_gbm.yaml`)
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '2'
- **[drug-inconsistency]** recommended_combination 'vorasidenib' contains drug name(s) ['vorasidenib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-IDH1-R132H-MDS-HR` (BMA — `bma_idh1_r132h_mds_hr.yaml`)
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '2'
- **[drug-inconsistency]** recommended_combination 'ivosidenib + azacitidine (trial)' contains drug name(s) ['ivosidenib', 'azacitidine'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-IDH1-R132H-MDS-LR` (BMA — `bma_idh1_r132h_mds_lr.yaml`)
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '2'
- **[drug-inconsistency]** recommended_combination 'ivosidenib + azacitidine (trial)' contains drug name(s) ['ivosidenib', 'azacitidine'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-IDH1-R132L-GBM` (BMA — `bma_idh1_r132l_gbm.yaml`)
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '2'
- **[drug-inconsistency]** recommended_combination 'vorasidenib' contains drug name(s) ['vorasidenib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-IDH1-R132S-GBM` (BMA — `bma_idh1_r132s_gbm.yaml`)
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '2'
- **[drug-inconsistency]** recommended_combination 'vorasidenib' contains drug name(s) ['vorasidenib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-NRAS-G12-MELANOMA` (BMA — `bma_nras_g12_melanoma.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'
- **[drug-inconsistency]** recommended_combination 'anti-PD1-based ICI' contains drug name(s) ['anti-pd1-based'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-NRAS-G13-MELANOMA` (BMA — `bma_nras_g13_melanoma.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'
- **[drug-inconsistency]** recommended_combination 'anti-PD1-based ICI' contains drug name(s) ['anti-pd1-based'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PIK3CA-HOTSPOT-ENDOMETRIAL` (BMA — `bma_pik3ca_hotspot_endometrial.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'
- **[drug-inconsistency]** recommended_combination 'everolimus + letrozole' contains drug name(s) ['everolimus', 'letrozole'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-MUT-NSCLC` (BMA — `bma_tp53_mut_nsclc.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'per usual NSCLC algorithm based on driver' contains drug name(s) ['per'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R175H-BREAST` (BMA — `bma_tp53_r175h_breast.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'per usual breast algorithm' contains drug name(s) ['per'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R175H-NSCLC` (BMA — `bma_tp53_r175h_nsclc.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'per usual NSCLC algorithm' contains drug name(s) ['per'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R248Q-BREAST` (BMA — `bma_tp53_r248q_breast.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'per usual breast algorithm' contains drug name(s) ['per'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R248Q-NSCLC` (BMA — `bma_tp53_r248q_nsclc.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'per usual NSCLC algorithm' contains drug name(s) ['per'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R273H-BREAST` (BMA — `bma_tp53_r273h_breast.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'per usual breast algorithm' contains drug name(s) ['per'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R273H-NSCLC` (BMA — `bma_tp53_r273h_nsclc.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'per usual NSCLC algorithm' contains drug name(s) ['per'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R282W-BREAST` (BMA — `bma_tp53_r282w_breast.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'per usual breast algorithm' contains drug name(s) ['per'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R282W-NSCLC` (BMA — `bma_tp53_r282w_nsclc.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')
- **[drug-inconsistency]** recommended_combination 'per usual NSCLC algorithm' contains drug name(s) ['per'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BARD1-SOMATIC-BREAST` (BMA — `bma_bard1_somatic_breast.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'

### `BMA-BRAF-CLASS3-NSCLC` (BMA — `bma_braf_class3_nsclc.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-BRAF-V600E-AML` (BMA — `bma_braf_v600e_aml.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-BRAF-V600E-CLL` (BMA — `bma_braf_v600e_cll.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-BRAF-V600E-HCC` (BMA — `bma_braf_v600e_hcc.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-BRIP1-GERMLINE-BREAST` (BMA — `bma_brip1_germline_breast.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'

### `BMA-EGFR-MUTATION-GBM` (BMA — `bma_egfr_mutation_gbm.yaml`)
- **[level-mismatch]** ESCAT X typically maps to OncoKB {} but entity declares OncoKB level '4'

### `BMA-FGFR1-AMP-NSCLC-SQUAMOUS` (BMA — `bma_fgfr1_amp_nsclc_squamous.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'

### `BMA-FGFR3-MUTATION-MM` (BMA — `bma_fgfr3_mutation_mm.yaml`)
- **[level-mismatch]** ESCAT X typically maps to OncoKB {} but entity declares OncoKB level '4'

### `BMA-FLT3-ITD-B-ALL` (BMA — `bma_flt3_itd_b_all.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'

### `BMA-IDH2-R140Q-AITL` (BMA — `bma_idh2_r140q_aitl.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-IDH2-R140Q-MDS-HR` (BMA — `bma_idh2_r140q_mds_hr.yaml`)
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '2'

### `BMA-IDH2-R140Q-MDS-LR` (BMA — `bma_idh2_r140q_mds_lr.yaml`)
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '2'

### `BMA-IDH2-R172K-MDS-HR` (BMA — `bma_idh2_r172k_mds_hr.yaml`)
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '2'

### `BMA-IDH2-R172K-MDS-LR` (BMA — `bma_idh2_r172k_mds_lr.yaml`)
- **[level-mismatch]** ESCAT IIA typically maps to OncoKB {3,3A,3B} but entity declares OncoKB level '2'

### `BMA-KRAS-G12C-ENDOMETRIAL` (BMA — `bma_kras_g12c_endometrial.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'

### `BMA-KRAS-G12C-GASTRIC` (BMA — `bma_kras_g12c_gastric.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-KRAS-G12D-OVARIAN` (BMA — `bma_kras_g12d_ovarian.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-MET-AMP-GASTRIC` (BMA — `bma_met_amp_gastric.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'

### `BMA-NOTCH1-ACTIVATING-MCL` (BMA — `bma_notch1_activating_mcl.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-NRAS-G12-MDS-HR` (BMA — `bma_nras_g12_mds_hr.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-NRAS-G12-MDS-LR` (BMA — `bma_nras_g12_mds_lr.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-NRAS-G13-MDS-HR` (BMA — `bma_nras_g13_mds_hr.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-NRAS-G13-MDS-LR` (BMA — `bma_nras_g13_mds_lr.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-NRAS-Q61R-MDS-HR` (BMA — `bma_nras_q61r_mds_hr.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-NRAS-Q61R-MDS-LR` (BMA — `bma_nras_q61r_mds_lr.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-PIK3CA-HOTSPOT-CERVICAL` (BMA — `bma_pik3ca_hotspot_cervical.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'

### `BMA-PIK3CA-HOTSPOT-ESOPHAGEAL` (BMA — `bma_pik3ca_hotspot_esophageal.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-PIK3CA-HOTSPOT-GASTRIC` (BMA — `bma_pik3ca_hotspot_gastric.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-PIK3CA-HOTSPOT-NSCLC` (BMA — `bma_pik3ca_hotspot_nsclc.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-PIK3CA-HOTSPOT-PROSTATE` (BMA — `bma_pik3ca_hotspot_prostate.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-PIK3CA-HOTSPOT-RCC` (BMA — `bma_pik3ca_hotspot_rcc.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-PIK3CA-HOTSPOT-UROTHELIAL` (BMA — `bma_pik3ca_hotspot_urothelial.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-RAD51B-GERMLINE-BREAST` (BMA — `bma_rad51b_germline_breast.yaml`)
- **[level-mismatch]** ESCAT IIIA typically maps to OncoKB {4} but entity declares OncoKB level '3B'

### `BMA-TP53-MUT-CERVICAL` (BMA — `bma_tp53_mut_cervical.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-TP53-MUT-CRC` (BMA — `bma_tp53_mut_crc.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-TP53-MUT-ENDOMETRIAL` (BMA — `bma_tp53_mut_endometrial.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-TP53-MUT-ESOPHAGEAL` (BMA — `bma_tp53_mut_esophageal.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-TP53-MUT-GASTRIC` (BMA — `bma_tp53_mut_gastric.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-TP53-MUT-GBM` (BMA — `bma_tp53_mut_gbm.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-TP53-MUT-HCC` (BMA — `bma_tp53_mut_hcc.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-TP53-MUT-MELANOMA` (BMA — `bma_tp53_mut_melanoma.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-TP53-MUT-PDAC` (BMA — `bma_tp53_mut_pdac.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-TP53-MUT-PROSTATE` (BMA — `bma_tp53_mut_prostate.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-TP53-MUT-RCC` (BMA — `bma_tp53_mut_rcc.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-TP53-MUT-SCLC` (BMA — `bma_tp53_mut_sclc.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-TP53-MUT-UROTHELIAL` (BMA — `bma_tp53_mut_urothelial.yaml`)
- **[level-mismatch]** unknown ESCAT tier 'IIIB' (cannot validate against OncoKB level '4')

### `BMA-TP53-MUT-MM` (BMA — `bma_tp53_mut_mm.yaml`)
- **[drug-inconsistency]** recommended_combination 'D-VRd (1L transplant-eligible)' contains drug name(s) ['d-vrd'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'Dara-Rd (1L transplant-ineligible)' contains drug name(s) ['dara-rd'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'ide-cel / cilta-cel (R/R)' contains drug name(s) ['ide-cel', 'cilta-cel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'alloSCT consideration in young high-risk' contains drug name(s) ['allosct'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BCL2-REARRANGEMENT-HGBL-DH` (BMA — `bma_bcl2_rearrangement_hgbl_dh.yaml`)
- **[drug-inconsistency]** recommended_combination 'DA-EPOCH-R' contains drug name(s) ['da-epoch-r'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'pola-R-CHP' contains drug name(s) ['pola-r-chp'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'CAR-T (R/R)' contains drug name(s) ['car-t'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MYC-REARRANGEMENT-BURKITT` (BMA — `bma_myc_rearrangement_burkitt.yaml`)
- **[drug-inconsistency]** recommended_combination 'DA-EPOCH-R (low/intermediate-risk Burkitt)' contains drug name(s) ['da-epoch-r'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'CODOX-M/IVAC + rituximab (high-risk/CNS+)' contains drug name(s) ['codox-m', 'ivac', 'rituximab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'R-hyperCVAD (alternative)' contains drug name(s) ['r-hypercvad'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MYC-REARRANGEMENT-DLBCL-NOS` (BMA — `bma_myc_rearrangement_dlbcl_nos.yaml`)
- **[drug-inconsistency]** recommended_combination 'R-CHOP (1L standard)' contains drug name(s) ['r-chop'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'pola-R-CHP (POLARIX)' contains drug name(s) ['pola-r-chp'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'DA-EPOCH-R (intensification consideration)' contains drug name(s) ['da-epoch-r'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MYC-REARRANGEMENT-FL` (BMA — `bma_myc_rearrangement_fl.yaml`)
- **[drug-inconsistency]** recommended_combination 'DA-EPOCH-R' contains drug name(s) ['da-epoch-r'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'pola-R-CHP' contains drug name(s) ['pola-r-chp'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'CAR-T 2L+' contains drug name(s) ['car-t'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MYC-REARRANGEMENT-HGBL-DH` (BMA — `bma_myc_rearrangement_hgbl_dh.yaml`)
- **[drug-inconsistency]** recommended_combination 'DA-EPOCH-R (1L preferred)' contains drug name(s) ['da-epoch-r'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'pola-R-CHP (1L alternative)' contains drug name(s) ['pola-r-chp'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'axi-cel / liso-cel (2L+)' contains drug name(s) ['axi-cel', 'liso-cel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-NOTCH1-ACTIVATING-T-ALL` (BMA — `bma_notch1_activating_t_all.yaml`)
- **[drug-inconsistency]** recommended_combination 'per CALGB-10403 / GMALL / BFM-inspired regimen (1L)' contains drug name(s) ['per', 'gmall', 'bfm-inspired'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'nelarabine (R/R T-ALL)' contains drug name(s) ['nelarabine'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'venetoclax + navitoclax (early-phase trials)' contains drug name(s) ['venetoclax', 'navitoclax'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PALB2-SOMATIC-OVARIAN` (BMA — `bma_palb2_somatic_ovarian.yaml`)
- **[drug-inconsistency]** recommended_combination 'niraparib maintenance' contains drug name(s) ['niraparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'rucaparib maintenance (LOH-high)' contains drug name(s) ['rucaparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab (HRD-positive)' contains drug name(s) ['olaparib', 'bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PIK3CA-EXON20-BREAST` (BMA — `bma_pik3ca_exon20_breast.yaml`)
- **[drug-inconsistency]** recommended_combination 'alpelisib + fulvestrant' contains drug name(s) ['alpelisib', 'fulvestrant'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'inavolisib + palbociclib + fulvestrant' contains drug name(s) ['inavolisib', 'palbociclib', 'fulvestrant'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'capivasertib + fulvestrant' contains drug name(s) ['capivasertib', 'fulvestrant'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PIK3CA-EXON9-BREAST` (BMA — `bma_pik3ca_exon9_breast.yaml`)
- **[drug-inconsistency]** recommended_combination 'alpelisib + fulvestrant' contains drug name(s) ['alpelisib', 'fulvestrant'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'inavolisib + palbociclib + fulvestrant' contains drug name(s) ['inavolisib', 'palbociclib', 'fulvestrant'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'capivasertib + fulvestrant' contains drug name(s) ['capivasertib', 'fulvestrant'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-RAD51B-SOMATIC-OVARIAN` (BMA — `bma_rad51b_somatic_ovarian.yaml`)
- **[drug-inconsistency]** recommended_combination 'niraparib (HRD-positive)' contains drug name(s) ['niraparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab' contains drug name(s) ['olaparib', 'bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'rucaparib (LOH-high)' contains drug name(s) ['rucaparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-RAD51C-SOMATIC-OVARIAN` (BMA — `bma_rad51c_somatic_ovarian.yaml`)
- **[drug-inconsistency]** recommended_combination 'niraparib (HRD-positive)' contains drug name(s) ['niraparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab' contains drug name(s) ['olaparib', 'bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'rucaparib (LOH-high)' contains drug name(s) ['rucaparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-RAD51D-SOMATIC-OVARIAN` (BMA — `bma_rad51d_somatic_ovarian.yaml`)
- **[drug-inconsistency]** recommended_combination 'niraparib (HRD-positive)' contains drug name(s) ['niraparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab' contains drug name(s) ['olaparib', 'bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'rucaparib (LOH-high)' contains drug name(s) ['rucaparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R175H-MM` (BMA — `bma_tp53_r175h_mm.yaml`)
- **[drug-inconsistency]** recommended_combination 'D-VRd' contains drug name(s) ['d-vrd'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'Dara-Rd' contains drug name(s) ['dara-rd'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'ide-cel / cilta-cel' contains drug name(s) ['ide-cel', 'cilta-cel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R248Q-MM` (BMA — `bma_tp53_r248q_mm.yaml`)
- **[drug-inconsistency]** recommended_combination 'D-VRd' contains drug name(s) ['d-vrd'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'Dara-Rd' contains drug name(s) ['dara-rd'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'ide-cel / cilta-cel' contains drug name(s) ['ide-cel', 'cilta-cel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R273H-MM` (BMA — `bma_tp53_r273h_mm.yaml`)
- **[drug-inconsistency]** recommended_combination 'D-VRd' contains drug name(s) ['d-vrd'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'Dara-Rd' contains drug name(s) ['dara-rd'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'ide-cel / cilta-cel' contains drug name(s) ['ide-cel', 'cilta-cel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R282W-MM` (BMA — `bma_tp53_r282w_mm.yaml`)
- **[drug-inconsistency]** recommended_combination 'D-VRd' contains drug name(s) ['d-vrd'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'Dara-Rd' contains drug name(s) ['dara-rd'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'ide-cel / cilta-cel' contains drug name(s) ['ide-cel', 'cilta-cel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-ATM-GERMLINE-BREAST` (BMA — `bma_atm_germline_breast.yaml`)
- **[drug-inconsistency]** recommended_combination 'standard breast therapy by HR/HER2' contains drug name(s) ['her2'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'enhanced screening (annual MRI)' contains drug name(s) ['enhanced'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BARD1-SOMATIC-OVARIAN` (BMA — `bma_bard1_somatic_ovarian.yaml`)
- **[drug-inconsistency]** recommended_combination 'niraparib (HRD-positive)' contains drug name(s) ['niraparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab' contains drug name(s) ['olaparib', 'bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRIP1-SOMATIC-OVARIAN` (BMA — `bma_brip1_somatic_ovarian.yaml`)
- **[drug-inconsistency]** recommended_combination 'niraparib (HRD-positive)' contains drug name(s) ['niraparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'olaparib + bevacizumab' contains drug name(s) ['olaparib', 'bevacizumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-KIT-MUTATION-AML` (BMA — `bma_kit_mutation_aml.yaml`)
- **[drug-inconsistency]** recommended_combination 'standard 7+3 + HiDAC consolidation (CBF-AML backbone)' contains drug name(s) ['hidac'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'avapritinib (D816V-AML, basket trial)' contains drug name(s) ['avapritinib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MYD88-L265P-DLBCL-NOS` (BMA — `bma_myd88_l265p_dlbcl_nos.yaml`)
- **[drug-inconsistency]** recommended_combination 'pola-R-CHP (1L; POLARIX — not MYD88-selected but consider)' contains drug name(s) ['pola-r-chp'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'CAR-T axi-cel / liso-cel (R/R)' contains drug name(s) ['car-t', 'liso-cel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-MYD88-L265P-PCNSL` (BMA — `bma_myd88_l265p_pcnsl.yaml`)
- **[drug-inconsistency]** recommended_combination 'ibrutinib + HD-MTX-based regimens (trial)' contains drug name(s) ['ibrutinib', 'hd-mtx-based'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'MTX-based induction → consolidation per usual PCNSL algorithm' contains drug name(s) ['mtx-based'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-MUT-OVARIAN` (BMA — `bma_tp53_mut_ovarian.yaml`)
- **[drug-inconsistency]** recommended_combination 'bevacizumab + carbo/pacli (1L HGSOC)' contains drug name(s) ['bevacizumab', 'carbo', 'pacli'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'niraparib maintenance (BRCA-WT/HRD-test)' contains drug name(s) ['niraparib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R175H-MCL` (BMA — `bma_tp53_r175h_mcl.yaml`)
- **[drug-inconsistency]** recommended_combination 'acalabrutinib + rituximab' contains drug name(s) ['acalabrutinib', 'rituximab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'brexu-cel' contains drug name(s) ['brexu-cel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R175H-OVARIAN` (BMA — `bma_tp53_r175h_ovarian.yaml`)
- **[drug-inconsistency]** recommended_combination 'bevacizumab + carbo/pacli' contains drug name(s) ['bevacizumab', 'carbo', 'pacli'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'PARPi maintenance per HRD/BRCA' contains drug name(s) ['parpi', 'brca'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R248Q-MCL` (BMA — `bma_tp53_r248q_mcl.yaml`)
- **[drug-inconsistency]** recommended_combination 'acalabrutinib + rituximab' contains drug name(s) ['acalabrutinib', 'rituximab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'brexu-cel' contains drug name(s) ['brexu-cel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R248Q-OVARIAN` (BMA — `bma_tp53_r248q_ovarian.yaml`)
- **[drug-inconsistency]** recommended_combination 'bevacizumab + carbo/pacli' contains drug name(s) ['bevacizumab', 'carbo', 'pacli'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'PARPi maintenance per HRD/BRCA' contains drug name(s) ['parpi', 'brca'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R273H-MCL` (BMA — `bma_tp53_r273h_mcl.yaml`)
- **[drug-inconsistency]** recommended_combination 'acalabrutinib + rituximab' contains drug name(s) ['acalabrutinib', 'rituximab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'brexu-cel' contains drug name(s) ['brexu-cel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R273H-OVARIAN` (BMA — `bma_tp53_r273h_ovarian.yaml`)
- **[drug-inconsistency]** recommended_combination 'bevacizumab + carbo/pacli' contains drug name(s) ['bevacizumab', 'carbo', 'pacli'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'PARPi maintenance per HRD/BRCA' contains drug name(s) ['parpi', 'brca'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R282W-MCL` (BMA — `bma_tp53_r282w_mcl.yaml`)
- **[drug-inconsistency]** recommended_combination 'acalabrutinib + rituximab' contains drug name(s) ['acalabrutinib', 'rituximab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'brexu-cel' contains drug name(s) ['brexu-cel'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-TP53-R282W-OVARIAN` (BMA — `bma_tp53_r282w_ovarian.yaml`)
- **[drug-inconsistency]** recommended_combination 'bevacizumab + carbo/pacli' contains drug name(s) ['bevacizumab', 'carbo', 'pacli'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)
- **[drug-inconsistency]** recommended_combination 'PARPi maintenance per HRD/BRCA' contains drug name(s) ['parpi', 'brca'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-ATM-GERMLINE-PDAC` (BMA — `bma_atm_germline_pdac.yaml`)
- **[drug-inconsistency]** recommended_combination 'FOLFIRINOX or gem-cis (platinum induction)' contains drug name(s) ['folfirinox', 'gem-cis'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-ATM-SOMATIC-PDAC` (BMA — `bma_atm_somatic_pdac.yaml`)
- **[drug-inconsistency]** recommended_combination 'FOLFIRINOX (platinum-based)' contains drug name(s) ['folfirinox'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRCA1-SOMATIC-PDAC` (BMA — `bma_brca1_somatic_pdac.yaml`)
- **[drug-inconsistency]** recommended_combination 'platinum-based chemo (FOLFIRINOX preferred)' contains drug name(s) ['platinum-based'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-BRCA2-SOMATIC-PDAC` (BMA — `bma_brca2_somatic_pdac.yaml`)
- **[drug-inconsistency]** recommended_combination 'platinum-based chemo (FOLFIRINOX)' contains drug name(s) ['platinum-based'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-CCND1-IHC-MCL` (BMA — `bma_ccnd1_ihc_mcl.yaml`)
- **[drug-inconsistency]** recommended_combination 'per DIS-MCL algorithm (BTKi-centric)' contains drug name(s) ['per'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-CCND1-T1114-MM` (BMA — `bma_ccnd1_t1114_mm.yaml`)
- **[drug-inconsistency]** recommended_combination 'venetoclax + carfilzomib + dex (NCT trials)' contains drug name(s) ['venetoclax', 'carfilzomib'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-CHEK2-GERMLINE-BREAST` (BMA — `bma_chek2_germline_breast.yaml`)
- **[drug-inconsistency]** recommended_combination 'enhanced screening (annual MRI from age 40)' contains drug name(s) ['enhanced'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-KIT-MUTATION-MELANOMA` (BMA — `bma_kit_mutation_melanoma.yaml`)
- **[drug-inconsistency]** recommended_combination 'anti-PD-1 ± anti-CTLA-4 (1L irrespective of KIT status)' contains drug name(s) ['anti-pd-1'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-NRAS-Q61K-MELANOMA` (BMA — `bma_nras_q61k_melanoma.yaml`)
- **[drug-inconsistency]** recommended_combination 'anti-PD1-based ICI' contains drug name(s) ['anti-pd1-based'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-NRAS-Q61R-MELANOMA` (BMA — `bma_nras_q61r_melanoma.yaml`)
- **[drug-inconsistency]** recommended_combination 'nivolumab + ipilimumab (1L preferred)' contains drug name(s) ['nivolumab', 'ipilimumab'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PALB2-GERMLINE-BREAST` (BMA — `bma_palb2_germline_breast.yaml`)
- **[drug-inconsistency]** recommended_combination 'platinum-based chemo (TNBC)' contains drug name(s) ['platinum-based'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PALB2-GERMLINE-PDAC` (BMA — `bma_palb2_germline_pdac.yaml`)
- **[drug-inconsistency]** recommended_combination 'FOLFIRINOX (platinum induction)' contains drug name(s) ['folfirinox'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

### `BMA-PALB2-SOMATIC-PDAC` (BMA — `bma_palb2_somatic_pdac.yaml`)
- **[drug-inconsistency]** recommended_combination 'FOLFIRINOX' contains drug name(s) ['folfirinox'] not appearing in regulatory_approval text (may be legitimate combination-component naming OR off-label not flagged)

## Methodology notes

- Trial-name pattern list is a curated set of well-known oncology trials; entities citing trials outside that list are not flagged. Treat findings as a triage seed, not an exhaustive audit.
- Trial-to-source matching is loose: an entity passes if ANY of its cited source IDs contains one of the substring hints registered for that trial. False negatives are possible when source IDs are named idiosyncratically.
- ESCAT->OncoKB mapping uses the loose ranges in the brief (IA->1, IB->1/2, II->3A/3B, III->4). Real-world borderline cases (e.g. IB->3A for combo-only approvals) are flagged for human review, not auto-corrected.
- FDA/EMA regulatory check passes if any cited source's ID contains `FDA`, `EMA`, `DAILYMED`, or `OPENFDA`, OR if its `source_type` is regulatory/label.
- Drug-consistency check is best-effort token matching against the `regulatory_approval` block; combinations explicitly tagged 'off-label' / 'investigational' are skipped.
- This script is `scripts/verify_citations_2026_04_27.py`.
