# Contributing to OpenOnco

Start with the [README](README.md), [Charter](specs/CHARTER.md) and [development guide](docs/DEVELOPMENT.md). Use [issues](https://github.com/romeo111/OpenOnco/issues/new/choose) for bugs, clinical feedback and proposals. Use synthetic profiles only.

## Code and website

1. Create a focused branch from current `master`.
2. Change the source builder as well as generated HTML so a daily rebuild preserves the fix.
3. Run relevant tests and correctness lint; run the KB validator when applicable. Inspect desktop and mobile rendering for visual changes.
4. Submit a PR describing the problem, resulting behavior and exact verification. Stage only relevant files.

For browser bundle changes, run `python -m scripts.audit_core_transport` against the shipped `docs/` artifacts (or pass `--site-dir <built-site>`). This read-only CI gate requires valid index hashes, identical ZIP/tar.gz member contents, safe regular-file paths, and the preferred compressed core below 4,250,000 bytes. The ZIP remains a compatibility artifact; `scripts.profile_engine_bundle` reports its composition, while the transport audit checks the preferred download. Run the Node bundle/loading/export suites as well. Archive consistency and byte budgets do not prove clinical validity, cold-device speed or offline generation.

See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for commands and deployment. Do not commit credentials, patient artifacts, caches or unrelated generated files. `legacy/` is historical, not the current architecture.

## Clinical content and translations

Follow [content standards](specs/CLINICAL_CONTENT_STANDARDS.md), [source ingestion](specs/SOURCE_INGESTION_SPEC.md) and the [RedFlag guide](specs/REDFLAG_AUTHORING_GUIDE.md). Cite sources, preserve licensing, expose uncertainty and keep content provisional until the Charter's review conditions are met. Do not independently set reviewed/sign-off status. AI assistance for code, docs, extraction or translation requires verification; an LLM must not choose regimens or doses.

Check interface translations, accessible labels, links and missing language counterparts. Clinical translations require clinical review. English specs and README are canonical; Ukrainian originals/translations are retained separately.

Patient reports currently offer the Ukrainian original and an incomplete English draft. Keep the draft notice and marked fallback for untranslated text. Source-bound drug-note drafts live in `knowledge_base/engine/_patient_note_translations.py`: compare each full translation with the current `notes_patient`, including negations, numbers, routes and warnings. Update its source fingerprint only after reviewing the changed text; never refresh a fingerprint merely to make CI pass. Run `python -m scripts.audit_patient_localization --check-note-drafts` and the patient rendering/translation tests. For the remaining work list, run `python -m scripts.audit_patient_localization --include-dynamic --include-drug-classes --output <review-file.json>`. These checks confirm source consistency, not clinical approval; class lookup counts do not prove complete report translation.

## Review and conduct

The [DLBCL packet](https://openonco.info/review/dlbcl-1l/) contains synthetic scenarios and exports feedback locally. Passing engineering contracts is not clinical approval. Follow the [Code of Conduct](CODE_OF_CONDUCT.md). Vulnerabilities use the [private channel](SECURITY.md).
