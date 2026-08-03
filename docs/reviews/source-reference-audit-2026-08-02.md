# Source-reference audit — 2026-08-02

Scope: provenance and bibliographic integrity only. This document does not add,
validate, or approve clinical recommendations.

## Result

| Check | Baseline in this run | After first pass | After continuation | After priority safety/source pass | Final pass |
|---|---:|---:|---:|---:|---:|
| Narrative `SRC-*` occurrences without a Source record | 133 | 108 | 75 | 67 | 0 |
| Unique unresolved narrative `SRC-*` IDs | 89 | 67 | 58 | 54 | 0 |
| YAML/schema/reference/contract errors | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |

`py -3.12 -m scripts.audit_unresolved_sources --json` now exits `0` with zero
unresolved IDs. Truncated placeholder tokens were removed as prose placeholders,
not turned into invented Source records. Where several legacy labels denoted one
verified publication, they were normalized to a documented canonical record.

## Bibliographic records added

Each record is `referenced` only: no publisher article text, tables, or figures
are hosted. Its license review is `pending`, and its notes explicitly require
dual clinical sign-off before a clinical claim is mapped to the source.

| Source ID | Primary bibliographic record |
|---|---|
| `SRC-AGILE-MONTESINOS-2022` | [PubMed 35443108](https://pubmed.ncbi.nlm.nih.gov/35443108/), DOI `10.1056/NEJMoa2117344` |
| `SRC-BLC2001-LORIOT-2019` | [PubMed 31340094](https://pubmed.ncbi.nlm.nih.gov/31340094/), DOI `10.1056/NEJMoa1817323` |
| `SRC-OLYMPIA-TUTT-2021` | [PubMed 34081848](https://pubmed.ncbi.nlm.nih.gov/34081848/), DOI `10.1056/NEJMoa2105215` |
| `SRC-PAOLA1-RAY-COQUARD-2019` | [PubMed 31851799](https://pubmed.ncbi.nlm.nih.gov/31851799/), DOI `10.1056/NEJMoa1911361` |
| `SRC-TALAPRO2-AGARWAL-2023` | [PubMed 37285865](https://pubmed.ncbi.nlm.nih.gov/37285865/), DOI `10.1016/S0140-6736(23)01055-3` |
| `SRC-THOR-LORIOT-2023` | [NEJM article record](https://www.nejm.org/doi/full/10.1056/NEJMoa2308849), DOI `10.1056/NEJMoa2308849` |
| `SRC-EPCORE-NHL-1-THIEBLEMONT-2023` | [PubMed 36548927](https://pubmed.ncbi.nlm.nih.gov/36548927/), DOI `10.1200/JCO.22.01725` |
| `SRC-NP30179-DICKINSON-2022` | [PubMed 36507690](https://pubmed.ncbi.nlm.nih.gov/36507690/), DOI `10.1056/NEJMoa2206913` |
| `SRC-MAGNETISMM-3-LESOKHIN-2023` | [PubMed 37582952](https://pubmed.ncbi.nlm.nih.gov/37582952/), DOI `10.1038/s41591-023-02528-9` |
| `SRC-MONUMENTAL-1-CHARI-2022` | [PubMed 36507686](https://pubmed.ncbi.nlm.nih.gov/36507686/), DOI `10.1056/NEJMoa2204591` |
| `SRC-GLOW` | [PubMed 37524953](https://pubmed.ncbi.nlm.nih.gov/37524953/), DOI `10.1038/s41591-023-02465-7` |
| `SRC-AUGMENT-101` | [PubMed 39121437](https://pubmed.ncbi.nlm.nih.gov/39121437/), DOI `10.1200/JCO.24.00826` |
| `SRC-TROPION-BREAST01-BARDIA-2024` | [PubMed 39265124](https://pubmed.ncbi.nlm.nih.gov/39265124/), DOI `10.1200/JCO.24.00920` |
| `SRC-INNOVATV-204` | [PubMed 33845034](https://pubmed.ncbi.nlm.nih.gov/33845034/), DOI `10.1016/S1470-2045(21)00056-5` |
| `SRC-IDHENTIFY` | [PubMed 35714312](https://pubmed.ncbi.nlm.nih.gov/35714312/), DOI `10.1182/blood.2021014901` |
| `SRC-AG221-AML-001` | [PubMed 28588020](https://pubmed.ncbi.nlm.nih.gov/28588020/), DOI `10.1182/blood-2017-04-779405` |
| `SRC-CARTITUDE-4-SAN-MIGUEL-2023` | [PubMed 37272512](https://pubmed.ncbi.nlm.nih.gov/37272512/), DOI `10.1056/NEJMoa2303379` |
| `SRC-CBGJ398X2204` | [PubMed 34358484](https://pubmed.ncbi.nlm.nih.gov/34358484/), DOI `10.1016/S2468-1253(21)00196-5` |
| `SRC-INAVO120-TURNER-2024` | [PubMed 39476340](https://pubmed.ncbi.nlm.nih.gov/39476340/), DOI `10.1056/NEJMoa2404625` |

## Legacy aliases resolved to existing canonical records

The following replacements were one-to-one name matches; no source was inferred
from a treatment claim:

```text
SRC-AETHERA → SRC-AETHERA-MOSKOWITZ-2015
SRC-BOLERO2 → SRC-BOLERO2-BASELGA-2012
SRC-CAPITELLO291-TURNER- → SRC-CAPITELLO291-TURNER-2023
SRC-DESTINY-CRC01 → SRC-DESTINY-CRC01-SIENA-2021
SRC-DESTINY-GASTRIC01 → SRC-DESTINY-GASTRIC01-SHITARA-2020
SRC-ECHELON-1 → SRC-ECHELON-1-CONNORS-2018
SRC-ECHELON-2 → SRC-ECHELON-2-HORWITZ-2019
SRC-ELEVATE-TN → SRC-ELEVATE-TN-SHARMAN-2020
SRC-EMBRACA → SRC-EMBRACA-LITTON-2018
SRC-MORSCHHAUSER- → SRC-MORSCHHAUSER-2020-TAZEMETOSTAT-FL
SRC-OLYMPIAD → SRC-OLYMPIAD-ROBSON-2017
SRC-PRIMA → SRC-PRIMA-GONZALEZ-MARTIN-2019
SRC-PROFOUND → SRC-PROFOUND-DEBONO-2020
SRC-SOLO1 → SRC-SOLO1-MOORE-2018
SRC-SPOTLIGHT → SRC-SPOTLIGHT-SHITARA-2023
```

## Required clinical review

Before any of these sources supports a public recommendation, two qualified
clinical reviewers must confirm the specific source-to-claim linkage, population,
endpoint, line of therapy, and regulatory context. This audit deliberately did
not change recommendation logic, structured `primary_sources`, eligibility, or
regimen content.

## Continuation: final source closure

The final pass added or normalized reference-only records for pivotal trial,
registry, and regulator/sponsor materials. Examples include [AHOD1331](https://pubmed.ncbi.nlm.nih.gov/36322844/),
[CheckMate 744](https://pubmed.ncbi.nlm.nih.gov/36564047/),
[POD1UM-202](https://pubmed.ncbi.nlm.nih.gov/35816951/),
[POD1UM-303](https://pubmed.ncbi.nlm.nih.gov/40517007/),
[TRANSCEND CLL 004](https://pubmed.ncbi.nlm.nih.gov/37295445/),
[TROPION-Breast02](https://pubmed.ncbi.nlm.nih.gov/41937088/), and the
[FDA infigratinib withdrawal notice](https://www.fda.gov/drugs/resources-information-approved-drugs/withdrawn-fda-grants-accelerated-approval-infigratinib-metastatic-cholangiocarcinoma).

The `Loehrer 1995` prose citation was handled differently: its stated PMID was
invalid and it did not establish the outcome attributed to it. The formal
placeholder was removed rather than silently supplied with guessed metadata;
the remaining guideline context is explicitly marked for qualified primary-source
verification.

Zero unresolved reference tokens is a provenance-integrity result only. It does
not mean that a source endorses every nearby sentence, that a regimen is current,
or that clinical signoff has been completed. In particular, these reference-only
records never gate availability of a visible draft recommendation.

## Reproduction

```powershell
py -3.12 scripts/audit_validator.py --human
py -3.12 -m scripts.audit_unresolved_sources --json
```
