# Treatment-line display terminology correction

Scope: presentation of `first line` in disease labels. Diagnosis codes, questionnaire values, engine input and treatment eligibility are unchanged. This correction is not clinical sign-off or approval of a treatment plan.

Observed defects: Italian `prima riga`, Swedish `första raden`, and Finnish `ensimmäinen rivi` described a row rather than a treatment line. Explicit display terminology overrides retained draft catalogs in the runtime before native identity detection.

Terminology references (consulted 2026-10-12):

- Finnish: `ensilinjan hoito`, used by the [Finnish Käypä hoito ovarian-cancer recommendation](https://www.kaypahoito.fi/xmedia/extra/hoi/hoi25050.pdf) and defined in the [Roche Finnish lung-cancer glossary](https://keuhkosyopa.fi/tietoa-keuhkosyovasta/keuhkosyopasanasto/). These are terminology references, not evidence for every regimen.
- Swedish: `första behandlingslinjen`, used by [Regionala cancercentrum in the myeloma care programme](https://kunskapsbanken.cancercentrum.se/diagnoser/myelom/vardprogram/behandling-av-aterfall/).
- Italian: `prima linea di trattamento`, used by [AIOM in its oncology education material](https://www.aiom.it/speciale-2021-news-in-oncology-melanoma-e-tumori-cutanei-non-melanoma/).

Other locale labels are explicit editorial drafts. A native-language review of the whole interface remains pending.

Verification: nine-locale stale-catalog regression runs the actual runtime translation functions and preserves diagnosis/ICD metadata; language-source/runtime consistency, numeric dose-frequency protections, cache-version contracts and NSCLC canonical-value contracts are checked separately. Passing these technical checks does not establish clinical accuracy of the entire corpus.
