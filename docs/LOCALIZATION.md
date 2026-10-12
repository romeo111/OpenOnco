# Website languages

## Additional interface editions (2026-10-12)

Italian `/it/`, Danish `/da/`, Swedish `/sv/`, Norwegian Bokmål `/nb/` and Finnish `/fi/` extend the menu to eleven languages, retaining English first and Ukrainian second. Each edition includes a locally authored full-corpus display catalog, with original fragments retained when translation checks reject a draft. These translations remain pending clinical review; do not describe them as fully translated or clinically validated.

Public and interactive pages use the shared templates. Deep clinical documents use small same-origin readers with the same source presentation and saved display catalogs. The previous six-language inventory was 786,113,461 bytes; five fully duplicated clinical trees would exceed the published GitHub Pages 1 GB limit. Original documents remain accessible without JavaScript. Canonical diagnosis names retain their source wording after an observed literal model error; numbers, medication names, source IDs and engine inputs are protected.

`scripts/prepare_additional_locales.py` authors interface drafts; `scripts/publish_additional_locale_drafts.py` validates all five before changing source catalogs. `scripts/shared_clinical_reader.py` and `scripts/shared-clinical-reader.js` provide the readers. This solo project has no clinical-team or reviewer quota for publication; actual expert feedback is separate from technical and language checks.

Nordic authoring uses `Helsinki-NLP/opus-mt-en-gmq` at `1011a691a63e61b4beb68d47332790e072f685f0`; Finnish uses `Helsinki-NLP/opus-mt-en-fi` at `2f68f12519005b50f9e1afe6fd57b13add55e156`. Italian uses the existing pinned Romance model. Weights remain in the optional local authoring environment; no model or translation API runs on page visits. The clinical-question API retains its separate existing provider costs.

## Intended-use copy (2026-10-12)

All eleven editions use shared intended-use limits requiring qualified clinician review. The project Charter does not establish a regulatory classification or clinical validation. `scripts/regulatory_copy.py` overlays exact source aliases and curated labels without changing clinical rules, source identifiers or input values. Revised scope metadata may retain English until reviewed; existing clinical translation notices remain in place.

## Earlier editions and maintenance

The five new catalogs each contain 36,858 display strings. Native draft counts are IT 21,154; DA 19,658; SV 19,847; NB 19,260; FI 15,404. Remaining entries retain originals, including protected diagnosis names. These counts describe display strings, not medically approved records.

Stage/staging labels use explicit terminology checked against [AIRC](https://www.airc.it/cancro/affronta-la-malattia/la-fase-della-diagnosi/stadiazione), [Kræftens Bekæmpelse](https://www.cancer.dk/fakta-kraeft/ordbog-kraeft/s/stadieinddeling/), [Swedish RCC](https://kunskapsbanken.cancercentrum.se/diagnoser/njurcancer/vardprogram/bilaga-3-stadieindelning-uicc-2017-8th-ed/), [Helsedirektoratet](https://www.helsedirektoratet.no/retningslinjer/kreft-i-tykktarm-og-endetarm-handlingsprogram/IS%202849%20Nasjonalt%20handlingsprogram%20kreft%20i%20tykktarm%20og%20endetarm.pdf) and [Finnish Cancer Organizations](https://kaikkisyovasta.fi/tietoa-syovasta/mika-on-syopa/syovan-levinneisyys/). Observed translations into floors, seasons, theatre or startup terms are rejected; the complete original fragment is retained instead. This glossary check is not clinical approval.

The navigation shell is shared across all eleven languages. Runtime and catalog assets have content-addressed filenames so previous offline caches cannot substitute stale translations. Large discovery inventories use deterministic gzip sitemap shards, each below both 50,000 URLs and 50 MB uncompressed, referenced by `/sitemap.xml`.

Deep English/Ukrainian documents share the byte-identical geographic-language script through a content-addressed JavaScript asset, also cached offline. It executes synchronously in the same head position and preserves manual choices, bot exclusions and the guard against redirecting after a visitor starts entering data. Clinical content, source links and metadata outside that block remain unchanged; sharing this script saves approximately 34 MB in the published tree.

English (`/`), Ukrainian (`/ukr/`), Spanish (`/es/`), Portuguese (`/pt/`), German (`/de/`) and French (`/fr/`) share the same clinical engine. English is first in the flag menu; Ukrainian is second.

## Published scope

| Surface | Spanish / Portuguese / German / French |
| --- | --- |
| Navigation, homepage, overview | Curated translations |
| Onco Wiki | Draft record translations, local titles/summaries, bilingual search |
| Handbook | Draft translations of 9 chapters, 27 questions, feedback and explanations |
| Plan Builder, Tumor Board, prevention | Full interfaces and questionnaires; localized result displays |
| Examples, disease coverage, static reports | Draft translations with original links |
| HTML / print-to-PDF export | The currently displayed translated report |
| Technical documentation, news, participation/review packets | Original-language content; localized introductions where available |

Every clinical translation displays **clinical review pending** and an English-original link. Machine-assisted drafts require clinician/language review of wording, negation, context and regional terminology. Numeric checks alone do not establish clinical equivalence.

IDs, source IDs, international drug names, questionnaire values, JSON profiles, source review status, quiz answer keys and executable rules remain source data. Code/profile blocks and technical fragments retain their original language. Fragments that fail quantity, identifier or polarity checks retain the complete original. These checks are conservative safeguards, not proof of clinical equivalence. A changed source key never reuses a stale translation; new prose remains original until its catalog is updated. Portuguese interface copy uses European Portuguese; medical drafts also need regional terminology review.

## Build and maintenance

- `scripts/site_locales.py`: language registry and curated public copy.
- `scripts/site_nav.py`, `scripts/site_header.css`: shared header and flags.
- `scripts/build_international.py`: public introductions; the clinical builder replaces medical entry pages with full content/tools.
- `scripts/site_translation_catalog.py`: normalized public prose collection and quantity checks.
- `scripts/locales/clinical.<locale>.json`: exact English-source display catalogs.
- `scripts/locales/clinical_manifest.json`: completed catalog inventory, checksums, model provenance and review state. Partial generation is not published without this manifest.
- `serverless/clinical_locale_messages.py`: curated review, safety, quiz and clarification messages.
- `scripts/clinical_curated_copy.py`: explicit classification terminology, including NSCLC names checked against [NCI](https://www.cancer.gov/espanol/tipos), [Portuguese DGS](https://www.dgs.pt/documentos-e-publicacoes/recomendacoes-nacionais-para-diagnostico-e-tratamento-do-cancro-do-pulmao-pdf.aspx), [German DKFZ](https://www.krebsinformationsdienst.de/lungenkrebs/behandlung-nicht-kleinzelliges-bronchialkarzinom) and [French INCa](https://www.cancer.fr/personnes-malades/les-cancers/poumon/comprendre-la-maladie/l-essentiel). This display glossary does not change disease codes or clinically approve the catalogs.
- `scripts/build_clinical_locales.py`: translated HTML, local search indexes, source links and source SHA-256 metadata. Repeated inline styles are shared as content-addressed CSS with the original content and cascade order preserved, keeping the published site below the hosting size limit.
- `scripts/clinical-localization.js`: saved display translations for dynamic DOM/report frames. Static record pages do not fetch a runtime catalog; small interactive pages use a compact UI catalog and the Plan Builder uses the complete clinical catalog. No input values or engine data are translated. Original English/Ukrainian report buttons remain available.
- `serverless/clinical_question.py`: selected response language, unchanged extraction/engine contracts. This API deploys separately from GitHub Pages.
- `scripts/locales/handbook.uk.json`, `scripts/handbook_localization.py`: the existing Ukrainian Handbook overlay.
- `scripts/site_head.py`: metadata, existing reciprocal language URLs and sitemap. Explicit language URLs bypass country redirection.

The standard `python -m scripts.build_site` build publishes these assets. GitHub Pages serves committed `/docs` on `master`. There is **no paid translation API or visitor-time translation service**; visitors load saved catalogs. The optional clinical-question API retains its existing server/provider costs.

## Translation provenance

Drafts use local CTranslate2 int8 inference with University of Helsinki OPUS-MT models:

| Languages | Model | Pinned revision | Model license |
| --- | --- | --- | --- |
| es / pt / fr | [Helsinki-NLP/opus-mt-en-ROMANCE](https://huggingface.co/Helsinki-NLP/opus-mt-en-ROMANCE) | `f8f3a28e8b6272d0ccc0290b832f699e154ae431` | Apache 2.0 |
| de | [Helsinki-NLP/opus-mt-en-de](https://huggingface.co/Helsinki-NLP/opus-mt-en-de) | `6183067f769a302e3861815543b9f312c71b0ca4` | CC BY 4.0 |

Catalogs include local terminology corrections and curated safety messages. Model weights and translation-only packages are not shipped to visitors, the engine or serverless runtime. See `scripts/translate_clinical_catalogs.py` and `scripts/requirements-translation.txt` for optional regeneration.

Regeneration runs in an optional translation environment, from the repository root:

```bash
python scripts/prepare_translation_models.py
python -c "import json; from pathlib import Path; from scripts.site_translation_catalog import collect_strings; Path('.tmp/clinical-source-strings.json').write_text(json.dumps(collect_strings(Path('docs')), ensure_ascii=False), encoding='utf-8')"
python scripts/translate_clinical_catalogs.py es .tmp/clinical-source-strings.json
# Repeat for pt, de and fr. Completed summaries are required for all four.
python -m scripts.publish_clinical_catalogs
python -m scripts.build_site
```

Generation writes separate staging catalogs. Publication checks completeness, previous-key preservation and translation invariants for all four languages before copying any catalog. Previous versions are preserved under `.tmp/clinical-catalog-backups`; the published manifest records checksums and counts of original fragments retained.

## Verification

Public pages use the English component templates through `build_public_locales.py`,
with display copy in `scripts/locales/public.{es,pt,de,fr}.json`. The layout,
inline styles, controls and executable scripts remain the same. The English
and Ukrainian project pages share the extended project-story sections; all
six editions expose the same navigation destinations and shared stylesheet
version. Longer translations may wrap naturally on narrow screens.

Public copy is a language draft, generated with the same optional offline
models documented above and marked `pending_language_review`. News articles
and linked source documents keep their original language. Clinical translation
notices and explicit English fallback labels remain visible where applicable.

```bash
python -m pytest tests/test_clinical_locales.py tests/test_site_languages.py tests/test_clinical_question_endpoint.py tests/test_site_discovery.py tests/test_site_head_faq.py
python -m pytest tests/test_public_layout_parity.py
node --check scripts/clinical-localization.js
python -m scripts.build_site
```

Review each medical translation against its linked English original. Translating prose never creates or upgrades a clinical sign-off.

Browser storage status labels in Italian, Danish, Swedish, Norwegian Bokmål
and Finnish use shared explicit display copy in `scripts/offline_ui_copy.py`.
The partial-download message remains distinct from full offline readiness.
JavaScript options, including `force-cache`, are not localized. Finnish uses
`Välimuisti`, consistent with the terminology in the
[University of Helsinki browser-cache instructions](https://helpdesk.it.helsinki.fi/ohjeet/tuki-ja-neuvonta/selaimen-valimuistin-tyhjennys).

Offline module preparation retries incomplete index, network, storage or integrity failures. Returning online schedules another pass only after an engine-generated plan; verified retained modules are reused and concurrent/completed passes remain deduplicated. A partial cache is not full offline readiness. `tests/browser_offline_bundle_retry.cjs` exercises the shipped client code in CI; this does not establish full browser offline engine or PDF behavior.

Pinned runtime retention (2026-10-12): all eleven Plan Builder clients prepare
the same ten Pyodide 0.26.4 runtime files after generation and worker upgrades.
The separate cache survives clinical-bundle updates and validates SHA-256 plus
size for both retained and network responses. It accepts only the exact public
inventory; runtime requests omit credentials/referrers and contain no profile
or DOM data. First visits can retain already downloaded HTTP-cache bytes;
corrupt HTTP entries get one forced reload. Storage failures preserve online
operation. The complete pydantic/pyyaml dependency closure totals 20,815,756
bytes and adds no hosted binary assets. CI verifies the worker's offline and
failure behavior and runs a synthetic Node WASM plan with fetch/TCP disabled.
Full offline browser reopening/generation and PDF printing remain unproven.
