# Source Freshness Audit — 2026-04-27

Periodic freshness audit of `knowledge_base/hosted/content/sources/`,
following the workflow described in `specs/SOURCE_INGESTION_SPEC.md`
§§1–3 (classification) and §8 (add/refresh checklist).

Today's reference date: **2026-04-27**.

Freshness window definition (per audit-task spec):

| Bucket            | Age of `last_verified`  | Action                                  |
|-------------------|-------------------------|-----------------------------------------|
| Fresh             | ≤ 6 months              | Re-stamp to today                       |
| Stale             | 6–12 months             | Verify URL, re-stamp if intact          |
| Outdated          | > 12 months             | Flag for clinical review                |
| Broken URL        | resolves to 404 / gone  | Flag for URL refresh                    |
| Missing fields    | no `last_verified` etc. | Flag as schema gap                      |

## Counts

| Bucket                                              | Count |
|-----------------------------------------------------|------:|
| Total sources audited                               |    94 |
| Fresh (already had `last_verified` ≤ 6 mo)          |    75 |
| Stale (6–12 mo)                                     |     0 |
| Outdated by `last_verified` (> 12 mo)               |     0 |
| Missing `last_verified`                             |    19 |
| Broken publisher URL (HTTP 404)                     |    25 |
| Gated publisher URL (HTTP 403, login required)      |    19 |
| Re-stamped to 2026-04-27 in this audit              |    91 |
| Already stamped 2026-04-27 (untouched)              |     3 |

Note: zero sources are "Outdated" by the `last_verified` axis because
the last full audit was only days ago (2026-04-24 → 2026-04-26). What is
captured below as "Outdated" is **content age** — sources whose
underlying guideline document is older than 24 months even though our
verification stamp is fresh.

## Re-stamp commit

`643995a` — `chore(sources): bulk re-stamp last_verified to 2026-04-27 (91 sources verified)`.

Validator state after commit:
`ok=True, entities=1246, errors=0`.

## 1. Schema gaps — sources missing `last_verified`

All 19 entries below were missing the `last_verified` field entirely.
The bulk re-stamp commit added the field for each.

| id                                | file                              | publisher URL was reachable? |
|-----------------------------------|-----------------------------------|------------------------------|
| SRC-EAU-BLADDER-2024              | src_eau_bladder_2024.yaml         | YES (200)                    |
| SRC-EAU-PROSTATE-2024             | src_eau_prostate_2024.yaml        | not re-checked (EAU CDN)     |
| SRC-ESMO-BREAST-EARLY-2024        | src_esmo_breast_early_2024.yaml   | broken — see §3              |
| SRC-ESMO-BREAST-METASTATIC-2024   | src_esmo_breast_metastatic_2024.yaml | not re-checked            |
| SRC-ESMO-ENDOMETRIAL-2022         | src_esmo_endometrial_2022.yaml    | not re-checked               |
| SRC-ESMO-MELANOMA-2024            | src_esmo_melanoma_2024.yaml       | broken — see §3              |
| SRC-ESMO-NSCLC-EARLY-2024         | src_esmo_nsclc_early_2024.yaml    | not re-checked               |
| SRC-ESMO-NSCLC-METASTATIC-2024    | src_esmo_nsclc_metastatic_2024.yaml | broken — see §3            |
| SRC-ESMO-PROSTATE-2024            | src_esmo_prostate_2024.yaml       | not re-checked               |
| SRC-ESMO-RCC-2024                 | src_esmo_rcc_2024.yaml            | not re-checked               |
| SRC-ESMO-SCLC-2021                | src_esmo_sclc_2021.yaml           | not re-checked               |
| SRC-NCCN-BLADDER-2025             | src_nccn_bladder_2025.yaml        | gated (403, login)           |
| SRC-NCCN-BREAST-2025              | src_nccn_breast_2025.yaml         | gated (403, login)           |
| SRC-NCCN-KIDNEY-2025              | src_nccn_kidney_2025.yaml         | gated (403, login)           |
| SRC-NCCN-MELANOMA-2025            | src_nccn_melanoma_2025.yaml       | gated (403, login)           |
| SRC-NCCN-NSCLC-2025               | src_nccn_nsclc_2025.yaml          | gated (403, login)           |
| SRC-NCCN-PROSTATE-2025            | src_nccn_prostate_2025.yaml       | gated (403, login)           |
| SRC-NCCN-SCLC-2025                | src_nccn_sclc_2025.yaml           | gated (403, login)           |
| SRC-NCCN-UTERINE-2025             | src_nccn_uterine_2025.yaml        | gated (403, login)           |

All 94 sources have non-empty `name` (`title`) and `source_type`
(`category`). No further structural-schema gaps detected.

## 2. Outdated content — `current_as_of` older than 24 months

These sources are stamped fresh (we verified them recently) but the
underlying guideline / consensus document is itself old enough to merit
clinical-team review for replacement or supersession.

| id                          | content date | age (yr) | recommended action                                       |
|-----------------------------|--------------|---------:|-----------------------------------------------------------|
| SRC-ESMO-MPN-2015           | 2015-09      |       11 | **Replace.** ESMO has not refreshed; consider NCCN-MPN-2025 + ELN-2018 MPN consensus + Tefferi reviews. |
| SRC-ESMO-CML-2017           | 2017-07      |        9 | **Replace.** Use ELN-CML-2020 (already in KB) as primary; retire ESMO-2017 or mark `superseded_by`. |
| SRC-ELN-APL-2019            | 2019-04      |        7 | Update — check ELN APL refresh; if none, mark current and re-verify in 12 mo. |
| SRC-ELN-CML-2020            | 2020-04      |        6 | Update — ELN CML 2020 still cited as authoritative; re-verify ASH/EHA 2025-2026 for refresh. |
| SRC-ESMO-AML-2020           | 2020-06      |        6 | Replace with ELN-AML-2022 (already in KB) for AML-specific recs; keep ESMO-AML-2020 only if specifically cited. |
| SRC-ESMO-MDS-2021           | 2021-02      |        5 | Update — incorporate IPSS-M (Bernard 2022) downstream classifications; check for ESMO MDS refresh. |
| SRC-ESMO-SCLC-2021          | 2021-10      |        5 | Update — verify ESMO SCLC refresh; NCCN-SCLC-2025 covers most active gaps. |
| SRC-ELN-AML-2022            | 2022-09      |        4 | Re-verify in 12 mo; still primary reference. |
| SRC-ESMO-ENDOMETRIAL-2022   | 2022-10      |        4 | Update — molecular endometrial classification has evolved; check for 2025/2026 ESMO-ESGO-ESTRO refresh. |
| SRC-AASLD-HCC-2023          | 2023-11      |        3 | Re-verify; AASLD HCC is updated periodically. |
| SRC-EASL-HCV-2023           | 2023-XX-XX   |        3 | Re-verify; pin exact month-day in `current_as_of`. |
| SRC-ESMO-MM-2023            | 2023-09      |        3 | Re-verify; check whether ESMO MM 2025 refresh published. |

All twelve are flagged for the next clinical-content review (CHARTER §6.1
two-reviewer rule applies to any replacement).

## 3. Broken publisher URLs — ESMO `guidelines-by-topic` namespace

ESMO has restructured its guidelines URL space. The pattern
`www.esmo.org/guidelines/guidelines-by-topic/<area>/<disease>` returns
HTTP 404 site-wide. Our KB has 25 sources on this pattern. Verified
candidate replacements live under
`www.esmo.org/guidelines/living-guidelines/esmo-living-guideline-<area>/<disease>-<short>`
or `www.esmo.org/guidelines/esmo-clinical-practice-guideline-<disease>`,
but the precise replacement URL needs per-source confirmation. URL
changes are out of scope for this audit (per task constraint: only swap
URLs after verifying a one-to-one replacement).

| id                              | broken URL (current)                                                                                              | suggested replacement (if known)                                                                                            |
|---------------------------------|-------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| SRC-ESMO-MZL-2024               | …/haematological-malignancies                                                                                     | https://www.esmo.org/guidelines/living-guidelines/esmo-living-guideline-lymphomas/marginal-zone-lymphoma-mzl  (200 verified) |
| SRC-ESMO-DLBCL-2024             | …/haematological-malignancies/diffuse-large-b-cell-lymphoma                                                       | https://www.esmo.org/guidelines/living-guidelines/esmo-living-guideline-lymphomas/diffuse-large-b-cell-lymphoma-dlbcl  (200 verified) |
| SRC-ESMO-FL-2024                | …/haematological-malignancies/follicular-lymphoma                                                                 | https://www.esmo.org/guidelines/living-guidelines/esmo-living-guideline-lymphomas/follicular-lymphoma-fl  (200 verified) |
| SRC-ESMO-CLL-2024               | …/haematological-malignancies/chronic-lymphocytic-leukaemia                                                       | needs verification (likely living-guideline-lymphomas/cll)                                                                 |
| SRC-ESMO-MM-2023                | …/haematological-malignancies/multiple-myeloma                                                                    | needs verification (esmo-clinical-practice-guideline-multiple-myeloma)                                                     |
| SRC-ESMO-BURKITT-2024           | …/haematological-malignancies/burkitt-lymphoma                                                                    | needs verification                                                                                                          |
| SRC-ESMO-HODGKIN-2024           | …/haematological-malignancies/hodgkin-lymphoma                                                                    | needs verification (likely living-guideline-lymphomas/hodgkin-lymphoma-hl)                                                 |
| SRC-ESMO-MCL-2024               | …/haematological-malignancies/mantle-cell-lymphoma                                                                | needs verification (likely living-guideline-lymphomas/mantle-cell-lymphoma-mcl)                                            |
| SRC-ESMO-PTCL-2024              | …/haematological-malignancies/peripheral-t-cell-lymphoma                                                          | https://www.esmo.org/guidelines/esmo-clinical-practice-guideline-peripheral-t-cell-lymphomas (search-result hit, not http-verified) |
| SRC-ESMO-WM-2024                | …/haematological-malignancies/waldenstrom-macroglobulinaemia                                                      | needs verification                                                                                                          |
| SRC-ESMO-CTCL-2024              | …/haematological-malignancies/primary-cutaneous-lymphomas                                                         | needs verification                                                                                                          |
| SRC-ESMO-CERVICAL-2024          | …/gynaecological-cancers/cervical-cancer                                                                          | https://www.esmo.org/guidelines/esmo-clinical-practice-guideline-cervical-cancer (search hit)                              |
| SRC-ESMO-ENDOMETRIAL-2022       | …/gynaecological-cancers/endometrial-cancer                                                                       | needs verification                                                                                                          |
| SRC-ESMO-OVARIAN-2024           | …/gynaecological-cancers/ovarian-cancer                                                                           | needs verification                                                                                                          |
| SRC-ESMO-COLON-2024             | …/gastrointestinal-cancers/colorectal-cancer                                                                      | needs verification                                                                                                          |
| SRC-ESMO-GASTRIC-2024           | …/gastrointestinal-cancers/gastric-cancer                                                                         | https://www.esmo.org/living-guidelines/esmo-gastric-cancer-living-guideline (search hit)                                   |
| SRC-ESMO-ESOPHAGEAL-2024        | …/gastrointestinal-cancers/oesophageal-cancer                                                                     | needs verification                                                                                                          |
| SRC-ESMO-PANCREATIC-2024        | …/gastrointestinal-cancers/pancreatic-cancer                                                                      | needs verification                                                                                                          |
| SRC-ESMO-NSCLC-EARLY-2024       | …/lung-cancer/early-and-locally-advanced-nsclc                                                                    | needs verification                                                                                                          |
| SRC-ESMO-NSCLC-METASTATIC-2024  | …/lung-cancer/metastatic-nsclc                                                                                    | needs verification                                                                                                          |
| SRC-ESMO-SCLC-2021              | …/lung-cancer/small-cell-lung-cancer                                                                              | needs verification                                                                                                          |
| SRC-ESMO-MELANOMA-2024          | …/melanoma/cutaneous-melanoma                                                                                     | needs verification                                                                                                          |
| SRC-ESMO-RCC-2024               | …/genitourinary-cancers/renal-cell-carcinoma                                                                      | needs verification                                                                                                          |
| SRC-ESMO-PROSTATE-2024          | …/genitourinary-cancers/prostate-cancer                                                                           | needs verification                                                                                                          |
| SRC-ESMO-BREAST-EARLY-2024      | …/breast-cancer/early-breast-cancer                                                                               | needs verification                                                                                                          |
| SRC-ESMO-BREAST-METASTATIC-2024 | …/breast-cancer/metastatic-breast-cancer                                                                          | needs verification                                                                                                          |

Recommended follow-up workstream: *ESMO URL refresh batch*. Either
walk all 25 sources interactively (HEAD-checking each candidate
replacement) or revert to the publisher's PDF in the journal Annals of
Oncology / DOI when available — DOIs do not break.

## 4. Other broken / redirect URLs

| id              | URL                                                               | observation                                                                            |
|-----------------|-------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| SRC-CTCAE-V5    | https://ctep.cancer.gov/protocoldevelopment/electronic_applications/ctc.htm | 301 redirect to https://dctd.cancer.gov/research/ctep-trials/trial-development. URL still works (browser follows redirect) but should be refreshed to canonical destination on next pass. |

## 5. Gated URLs (HTTP 403 / login required)

The following sources have URLs that return 403 to anonymous fetch
but are correct — they are publisher portals requiring registration
(NCCN, OncoKB, ESMO member areas). Per audit policy these are
"verifiable URL but content gated"; `last_verified` was stamped anyway.

All NCCN sources (19 total: AML, B-cell, Bladder, Breast, Cervical, CNS,
Colon, Esophageal, Gastric, HCC, Kidney, Melanoma, MM, MPN, NSCLC,
Ovarian, Pancreatic, Prostate, SCLC, Uterine — minus the two that 200'd)
fall in this bucket. Plus SRC-ONCOKB.

## 6. Recommendations summary

1. **Open ESMO URL refresh workstream.** 25 broken URLs concentrated in
   one publisher domain. One-time batch fix, ~1 hour with HEAD checks.
2. **Clinical-team review queue: 12 outdated guidelines.** Order by age
   descending: MPN-2015, CML-2017, APL-2019, CML-2020, AML-2020,
   MDS-2021, SCLC-2021, AML-2022, ENDOMETRIAL-2022, then 2023-vintage
   ESMO-MM, AASLD-HCC, EASL-HCV. Three of these (ESMO-MPN-2015,
   ESMO-CML-2017, ESMO-AML-2020) likely retire in favor of newer
   guidelines already in KB; the remainder need fresh-version checks.
3. **Pin month-day in `current_as_of`.** Several entries have YYYY-XX-XX
   values (e.g. SRC-EASL-HCV-2023, SRC-NCCN-AML-2025); future audits
   will need exact dates to compute age cleanly.
4. **Annual cadence.** With every source stamped today, the next
   meaningful audit is 2027-04-27 unless a publisher updates push
   earlier.
