# Website languages

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

```bash
python -m pytest tests/test_clinical_locales.py tests/test_site_languages.py tests/test_clinical_question_endpoint.py tests/test_site_discovery.py tests/test_site_head_faq.py
node --check scripts/clinical-localization.js
python -m scripts.build_site
```

Review each medical translation against its linked English original. Translating prose never creates or upgrades a clinical sign-off.
