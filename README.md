# OpenOnco

[![Validate Knowledge Base](https://github.com/romeo111/OpenOnco/actions/workflows/validate-kb.yml/badge.svg)](https://github.com/romeo111/OpenOnco/actions/workflows/validate-kb.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Release](https://img.shields.io/github/v/release/romeo111/OpenOnco)](https://github.com/romeo111/OpenOnco/releases)
[![Website](https://img.shields.io/badge/website-openonco.info-14532d.svg)](https://openonco.info/)

**Free, open-source oncology knowledge base and tools for source-cited clinical discussion.** A deterministic Python rule engine drafts alternative plans from versioned YAML. An LLM does not select regimens or doses.

[Live website](https://openonco.info/) · [Українською](README.uk.md) · [Documentation](docs/README.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md)

OpenOnco is an early-stage informational project. Clinical content can be draft, incomplete or awaiting review. Technical tests and source citations do not constitute clinical approval. A qualified clinician must verify outputs against original sources and the full clinical context. Patient-facing material supports education and preparation of questions for an oncologist.

## Explore the project

| Tool | English | Українська | What to expect |
| --- | --- | --- | --- |
| Onco Wiki | [Search](https://openonco.info/kb.html) | [Пошук](https://openonco.info/ukr/kb.html) | Diseases, drugs, biomarkers, risk signals and source links |
| Plan builder | [Try](https://openonco.info/try.html) | [Спробувати](https://openonco.info/ukr/try.html) | Python engine runs in the browser through Pyodide |
| Synthetic examples | [Gallery](https://openonco.info/gallery.html) | [Приклади](https://openonco.info/ukr/gallery.html) | Public, synthetic examples of rendered outputs |
| Coverage | [Capabilities](https://openonco.info/capabilities.html) | [Про проєкт](https://openonco.info/ukr/about.html) | Counts and limitations; coverage is not clinical readiness |
| Tumor-board questions | [Ask](https://openonco.info/ask.html) | [Запитати](https://openonco.info/ukr/ask.html) | Server-backed prototype; submitted inputs leave the browser |
| Handbook | [Read](https://openonco.info/handbook.html) | [Читати](https://openonco.info/ukr/handbook.html) | 9 chapters / 27 questions; Ukrainian translation awaits clinical review; no ESMO endorsement or CME credit |
| Clinician review | [DLBCL 1L packet](https://openonco.info/review/dlbcl-1l/) | English packet | 26 synthetic scenarios, actual plans, traces and local feedback export |

Use synthetic profiles for public demos and feedback. Do not submit identifiable patient data to the question prototype or GitHub. The browser plan builder processes profiles locally; that privacy property does not apply to server-backed tools.

Onco Wiki records, Handbook chapters and quizzes, interactive tools and result displays also have draft [Español](https://openonco.info/es/), [Português](https://openonco.info/pt/), [Deutsch](https://openonco.info/de/) and [Français](https://openonco.info/fr/) translations. Clinical translation review is pending. Original English pages remain accessible; identifiers, questionnaire values, answer keys and engine decisions stay unchanged. See the [localization scope and maintenance guide](docs/LOCALIZATION.md).

## Current repository snapshot

Measured on **2026-10-10** with `python -m knowledge_base.stats --format json`:

| Entity | Count | Entity | Count |
| --- | ---: | --- | ---: |
| Diseases | 103 | Indications | 831 |
| Regimens | 404 | Algorithms | 189 |
| Drugs | 321 | Biomarkers | 257 |
| Red flags | 671 | Sources | 542 |

These are entity counts, not independently validated treatment pathways. The published wiki index can differ because it is a separately generated snapshot. Check [live coverage](https://openonco.info/diseases.html) and each entity's provenance and review status. The latest tagged software release is [v0.1.3](https://github.com/romeo111/OpenOnco/releases/tag/v0.1.3); the website also includes subsequent changes from `master`.

## Run locally

Python **3.12** is recommended and used in CI; the package declares Python 3.11+.

```bash
git clone https://github.com/romeo111/OpenOnco.git
cd OpenOnco
python -m venv .venv
```

Activate with `source .venv/bin/activate` on Linux/macOS or `.venv/Scripts/Activate.ps1` in PowerShell, then:

```bash
python -m pip install -r requirements.lock
python -m pip install --no-build-isolation --no-deps -e .
python scripts/audit_validator.py --human
python -m pytest tests/test_kb_wiki.py tests/test_site_head_faq.py tests/test_site_discovery.py -q
python -m http.server 8000 --directory docs
```

Open [localhost:8000](http://localhost:8000/). To regenerate into a separate preview, run `python -m scripts.build_site --output build/site-preview`, then serve `build/site-preview`. Run the broader suite with `python -m pytest tests/`; some integrations use optional dependencies or fixtures. See [development and deployment](docs/DEVELOPMENT.md) for CI gates.

## Use the engine through MCP

```bash
python -m pip install -e ".[mcp]"
python -m mcp_server.server
```

Tools include `engine_info`, `list_diseases`, `generate_treatment_plan` and `generate_diagnostic_brief`. See the [MCP guide](mcp_server/README.md) for client setup. The assistant relays the engine's output, provenance and limitations; it does not independently choose treatment.

## Architecture

```text
knowledge_base/hosted/content/   Versioned YAML entities and source records
knowledge_base/engine/           Deterministic rules, plans and renderers
knowledge_base/clients/          External source clients
scripts/                        Builders, audits and discovery metadata
docs/                           Published site and project documentation
specs/                          Governance, schemas and clinical standards
tests/                          Contracts, regressions and synthetic fixtures
mcp_server/                     Local MCP interface
api/, serverless/               Optional server-backed question interface
legacy/                         Historical implementation; not authoritative
```

Read the [Charter](specs/CHARTER.md) first. English specifications are canonical; Ukrainian originals are retained under [specs/uk/](specs/uk/). Sources are referenced under their upstream licensing terms.

## Help improve OpenOnco

- Review the [DLBCL packet](https://openonco.info/review/dlbcl-1l/): inspect plans, traces and sources; export feedback locally. Engineering checks are not clinical sign-off.
- Report reproducible bugs or source discrepancies through [Issues](https://github.com/romeo111/OpenOnco/issues/new/choose), using synthetic data.
- Follow [CONTRIBUTING.md](CONTRIBUTING.md) for code, translations and clinical changes. Do not independently mark content reviewed.
- For vulnerabilities, use [private reporting](https://github.com/romeo111/OpenOnco/security/advisories/new), not a public issue containing exploit details or secrets.

## License and citation

Code: [MIT](LICENSE). Specifications and generated project content: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cited sources retain their own licenses and are not relicensed or redistributed. See [CITATION.cff](CITATION.cff) for software citation. OpenOnco is not an emergency service or a substitute for a qualified oncologist.

Developer setup, synthetic clinical review, interoperability gaps and launch materials are collected in the [participation hub](https://openonco.info/participate.html).
