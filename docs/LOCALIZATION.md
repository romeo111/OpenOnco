# Website languages

The website provides English (`/`), Ukrainian (`/ukr/`), Spanish (`/es/`), Portuguese (`/pt/`), German (`/de/`) and French (`/fr/`). Portuguese currently uses European Portuguese wording and the neutral `pt` language tag; it is not a separate Brazilian Portuguese edition.

## Published scope

| Surface | English / Ukrainian | Spanish / Portuguese / German / French |
| --- | --- | --- |
| Shared navigation and language menu | Localized | Localized |
| Homepage, project overview | Localized | Localized |
| Onco Wiki search controls, loading/error messages, filters and pagination | Localized | Localized; records and results retain English |
| Handbook | English original and Ukrainian draft translation of 9 chapters / 27 questions | Localized catalog; explicit links to English and Ukrainian chapters |
| Plan Builder, Tumor Board, prevention, examples, diseases, specifications, news | Existing English and Ukrainian tools/pages | Localized introduction and explicit English launch link |
| Generated engine results | Existing English/Ukrainian rendering | English launch; no claim of translated clinical output |

The new languages are public entry points, **not complete translations of the clinical knowledge base or interactive tools**. Every introduction labels the destination language before opening it. International search supports the existing international drug names, gene symbols, identifiers and English synonyms. It does not invent translations of disease names or clinical records.

## Build and maintenance

- `scripts/site_locales.py`: locale registry, URLs and public copy.
- `scripts/site_nav.py`: shared accessible native `<details>` language menu. Unsupported deep-page translations link to the selected language's homepage.
- `scripts/build_international.py`, `scripts/site_international.css`: four international editions; built by `scripts.build_site` after the search and Handbook indexes exist.
- `scripts/locales/handbook.uk.json`: exact English source prose mapped to Ukrainian. Changes to source prose require a corresponding catalog update; missing prose raises an error rather than silently serving a stale translation.
- `scripts/handbook_localization.py`: Ukrainian content overlay and visible quiz UI translation. It preserves source IDs, entity IDs, answer keys, question types, source lists, timestamps and clinical-review metadata. Original source titles, technical tags and entity labels are retained.
- `scripts/build_handbook.py`: builds both Handbook editions and their JSON indexes. Ukrainian pages explicitly say clinical review of the translation is pending.
- `scripts/site_head.py`: metadata and sitemap advertise existing counterparts only. Localized tool introductions are not advertised as full translations of English interactive tools. Explicit international URLs are never redirected by IP-country detection.

No paid translation API or visitor-time translation service is used. Copy is checked into Git. The normal static-site build and GitHub Pages deployment publish it.

Verification:

```bash
python -m pytest tests/test_site_languages.py tests/test_site_discovery.py tests/test_site_head_faq.py
python -m scripts.build_handbook
python -m scripts.build_site
```

Before extending clinical content to more languages, arrange terminology and clinician review. A prose translation never creates or upgrades a clinical sign-off.
