# Contributing to OpenOnco

Start with the [README](README.md), [Charter](specs/CHARTER.md) and [development guide](docs/DEVELOPMENT.md). Use [issues](https://github.com/romeo111/OpenOnco/issues/new/choose) for bugs, clinical feedback and proposals. Use synthetic profiles only.

## Code and website

1. Create a focused branch from current `master`.
2. Change the source builder as well as generated HTML so a daily rebuild preserves the fix.
3. Run relevant tests and correctness lint; run the KB validator when applicable. Inspect desktop and mobile rendering for visual changes.
4. Submit a PR describing the problem, resulting behavior and exact verification. Stage only relevant files.

See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for commands and deployment. Do not commit credentials, patient artifacts, caches or unrelated generated files. `legacy/` is historical, not the current architecture.

## Clinical content and translations

Follow [content standards](specs/CLINICAL_CONTENT_STANDARDS.md), [source ingestion](specs/SOURCE_INGESTION_SPEC.md) and the [RedFlag guide](specs/REDFLAG_AUTHORING_GUIDE.md). Cite sources, preserve licensing, expose uncertainty and keep content provisional until the Charter's review conditions are met. Do not independently set reviewed/sign-off status. AI assistance for code, docs, extraction or translation requires verification; an LLM must not choose regimens or doses.

Check interface translations, accessible labels, links and missing language counterparts. Clinical translations require clinical review. English specs and README are canonical; Ukrainian originals/translations are retained separately.

## Review and conduct

The [DLBCL packet](https://openonco.info/review/dlbcl-1l/) contains synthetic scenarios and exports feedback locally. Passing engineering contracts is not clinical approval. Follow the [Code of Conduct](CODE_OF_CONDUCT.md). Vulnerabilities use the [private channel](SECURITY.md).
