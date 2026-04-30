# knowledge_base/

The OpenOnco rule-engine and knowledge base. Live at
[**openonco.info**](https://openonco.info) (EN default, UA mirror at
[`/ukr/`](https://openonco.info/ukr/)). Specifications under
[`../specs/`](../specs/) — start with
[`CHARTER.md`](../specs/CHARTER.md) for governance + scope and
[`KNOWLEDGE_SCHEMA_SPECIFICATION.md`](../specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md)
for the entity model.

**Version:** v0.1.2 (released 2026-04-30, see
[`__init__.py`](__init__.py)).

## What it does

Patient profile (FHIR R4 / mCODE compatible) → declarative rule engine
→ two alternative treatment plans (standard + aggressive) with full
source citations, MDT role activation, red flags, dose adjustments,
and monitoring schedule. Plans refresh as new data arrives (new labs,
doctor decisions, updated guidelines). LLMs do **not** make clinical
decisions (CHARTER §8.3) — clinical logic runs in the rule engine
reading versioned YAML.

## Layout

```
knowledge_base/
├── schemas/                   # 23 Pydantic models (entities + KB facets)
├── clients/                   # Live-API clients for referenced sources
│   ├── base.py                # SourceClient protocol + TokenBucket + cache
│   ├── ctgov_client.py        # ClinicalTrials.gov v2
│   ├── pubmed_client.py
│   ├── dailymed_client.py
│   ├── openfda_client.py
│   └── translate_client.py    # DeepL / LibreTranslate (UI + KB free-text)
├── engine/                    # 34 modules — rule engine, MDT, render
│   ├── plan.py                # generate_plan() / PlanResult
│   ├── diagnostic.py          # generate_diagnostic_brief() — pre-biopsy mode
│   ├── algorithm_eval.py      # algorithm step evaluator
│   ├── redflag_eval.py        # red-flag firing
│   ├── questionnaire_eval.py  # questionnaire impact + what-if
│   ├── mdt_orchestrator.py    # role activation + Open Questions (Q1-Q6 / DQ1-DQ4)
│   ├── mdt_protocol.py        # multidisciplinary team protocol
│   ├── access_matrix.py       # per-Plan access (NHSU / MoH / commercial)
│   ├── experimental_options.py # CT.gov match into Plan
│   ├── lazy_loader.py         # per-disease bundle loading (Pyodide-friendly)
│   ├── render.py              # Plan/Brief HTML renderer (UA + EN)
│   ├── render_styles.py       # render-time CSS
│   ├── _citation_guard.py     # render-time citation-presence guard (Layer 3)
│   ├── _ask_doctor.py         # patient-mode "ask your doctor" prompt
│   ├── _emergency_rf.py       # RF emergency triage
│   ├── _patient_vocabulary.py # plain-language drug / ICD glossing
│   ├── _track_filter.py       # per-track filter logic
│   ├── _nszu.py               # NHSU coverage lookup
│   ├── actionability_*.py     # CIViC actionability extractor + conflict
│   ├── civic_variant_matcher.py # fusion-aware variant match
│   ├── persistence.py         # event store on top of YAML
│   └── …
├── ingestion/                 # Loaders for hosted sources
│   ├── civic_loader.py        # CIViC monthly snapshot import
│   ├── ctcae_loader.py        # CTCAE v5.0
│   ├── icd_loader.py          # ICD-O-3 morphology
│   ├── loinc_loader.py
│   ├── rxnorm_loader.py
│   ├── atc_loader.py
│   ├── moz_extractor.py       # МОЗ (Ukraine MoH) PDF extractor
│   ├── nszu_loader.py         # НСЗУ formulary
│   └── drlz_lookup.py         # Держреєстр лікарських засобів
├── validation/                # YAML loader + schema + referential integrity
├── hosted/                    # Everything we host locally
│   ├── content/               # Our clinical content (see counts below)
│   ├── code_systems/          # ICD-O-3, HGNC populated; LOINC/RxNorm pending
│   ├── civic/<date>/          # CIViC nightly snapshot (CC0)
│   ├── ctcae/v5.0/            # CTCAE v5.0 grading
│   └── audit/                 # signoffs.jsonl — clinical sign-off log
├── cache/                     # Live API query cache (gitignored)
├── stats.py                   # Compute KB stats for /capabilities.html
├── README.md                  # this file
└── TODO.md
```

## Status

**Working rule engine + 65-disease KB + bilingual rendering.** First
real-patient plans validated by practising oncologists (see
`CLAUDE.md`).

### Content scale (as of v0.1.2)

| Entity type             | Count |
|-------------------------|-------|
| Diseases                | 65    |
| Indications             | 312   |
| Regimens                | 253   |
| Algorithms              | 113   |
| Biomarkers              | 125   |
| Biomarker actionability | 399   |
| Drugs                   | 220   |
| Tests                   | 95    |
| Workups                 | 24    |
| RedFlags                | 442   |
| Contraindications       | 12    |
| Supportive care         | 13    |
| Monitoring schedules    | 8     |
| Questionnaires          | 65    |
| MDT skills              | 16    |
| Sources                 | 272   |
| Reviewers               | 4     |

### What's implemented

- **Rule engine** — `generate_plan()` and `generate_diagnostic_brief()`
  produce a versioned `PlanResult` from a patient profile.
- **MDT orchestrator** — role activation (required / recommended /
  optional), Open Questions Q1-Q6 (treatment) + DQ1-DQ4 (diagnostic),
  decision-provenance graph for audit-grade explanation
  (`MDT_ORCHESTRATOR_SPEC.md`, `DIAGNOSTIC_MDT_SPEC.md`).
- **Two-track plans** — standard + aggressive side-by-side
  (CHARTER §15.2 C6 anti-automation-bias).
- **CIViC actionability** (CC0) — fusion-aware variant matcher,
  ESCAT-tier rendering, monthly snapshot CI refresh
  (replaced OncoKB on 2026-04-27 — see
  `docs/reviews/oncokb-public-civic-coverage-2026-04-27.md`).
- **Three-layer citation guard** — loader-level SRC-* referential
  integrity, background citation-verifier, render-time
  `_citation_guard` strip-or-fail.
- **Bilingual render** — Plan/Brief HTML in UA and EN. UI labels via
  `_UI_STRINGS`; KB names via `_pick_name()` (english → preferred →
  ukrainian or reverse depending on `target_lang`); free-text prose
  via `_translate_kb_text()` (DeepL/LibreTranslate, env-configured —
  graceful UA fallback when no client).
- **Pre-biopsy mode** (CHARTER §15.2 C7 hard rule) — engine refuses
  to emit a treatment Plan without `disease.id` / `icd_o_3_morphology`,
  emits a `DiagnosticPlan` with workup brief instead.
- **Live clients** — ClinicalTrials.gov (v2), PubMed, DailyMed,
  openFDA. All inherit `BaseSourceClient` (per-source rate-limit +
  TTL-cache).
- **Patient mode** — separate render path with plain-language drug /
  ICD glossing, "ask your doctor" prompts, technical-ID stripping.
- **Per-disease lazy loading** — engine bundle is a core zip + per-
  disease zips (`lazy_loader.py`); `/try.html` Pyodide engine fetches
  on demand.

### What's pending

- Full EN translation of long-form prose fields (`do_not_do`, redflag
  definitions, indication notes) — handled by `_translate_kb_text` at
  render time when DeepL/LibreTranslate is configured; otherwise
  falls back to UA inline. Adding `*_en` mirror fields to KB schemas
  is one option; pre-translating via cached client is another.
- Code-system populations: LOINC + RxNorm + ATC ingestion loaders
  exist but data not yet fully populated.
- PostgreSQL migration: the spec mentions transitioning from YAML
  files + git history once entity count passes ~10K
  (`SOURCE_INGESTION_SPEC.md` §12.1). Not urgent at current scale.

## Running the validator

```bash
pip install -e .
python -m knowledge_base.validation.loader knowledge_base/hosted/content
```

Lists all entities, validates each against its schema, checks that
every referenced ID exists, runs contract validators (e.g. every
clinical claim cites a Source, every Indication wires to an Algorithm
when one exists for the disease).

## Generating a Plan from a profile

```python
from pathlib import Path
from knowledge_base.engine import (
    generate_plan, generate_diagnostic_brief, is_diagnostic_profile,
    orchestrate_mdt, render_plan_html, render_diagnostic_brief_html,
)

KB = Path("knowledge_base/hosted/content")
patient = {...}  # FHIR R4 / mCODE-shaped dict

if is_diagnostic_profile(patient):
    result = generate_diagnostic_brief(patient, kb_root=KB)
    mdt = orchestrate_mdt(patient, result, kb_root=KB)
    html = render_diagnostic_brief_html(result, mdt=mdt, target_lang="en")
else:
    result = generate_plan(patient, kb_root=KB)
    mdt = orchestrate_mdt(patient, result, kb_root=KB)
    html = render_plan_html(result, mdt=mdt, target_lang="en")
```

The same engine ships in-browser via Pyodide — see `/try.html` on
[openonco.info](https://openonco.info/try.html) for the interactive
demo.

## Schema conventions

- `model_config = ConfigDict(extra="allow")` on every entity so adding
  fields in YAML doesn't break schema. Forces schema evolution to be
  intentional (pin specific fields as required when stable).
- IDs: prefix + upper-case, e.g. `DIS-HCV-MZL`, `DRUG-RITUXIMAB`,
  `IND-HCV-MZL-1L-STANDARD`, `BMA-EGFR-L858R-OSIMERTINIB`.
- Citations: every clinical claim references a Source via
  `source_id`, never inline URL.
- Names: `names: {ukrainian, english, preferred, synonyms: [...]}`.
  Render picks based on `target_lang` (EN: english → preferred →
  ukrainian; UA: ukrainian → preferred → english).
- **Two-reviewer signoff** for clinical content (CHARTER §6.1) — any
  Indication / Regimen / RedFlag merged on master needs 2 of 3
  Clinical Co-Lead approvals; otherwise stays STUB.

## Adding a new entity

1. Check `specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md` for the canonical
   entity definition.
2. Write YAML under the appropriate `hosted/content/<type>/` directory.
3. Run the validator.
4. If you add a new source, add a Source YAML under
   `hosted/content/sources/` with full license/hosting metadata per
   `specs/SOURCE_INGESTION_SPEC.md` §3 + §8 (referenced vs hosted vs
   mixed; H1-H5 hosting justification).
5. For clinical content (Indication / Regimen / RedFlag /
   Contraindication / SupportiveCare): mark `reviewer_signoffs: 0`
   STUB until two Clinical Co-Leads approve via the signoff log
   (`hosted/audit/signoffs.jsonl`).

## Contributing via TaskTorrent

Idle capacity in Claude Code, Codex, Cursor, or ChatGPT? Take a
structured chunk of work from the queue and open a PR — full guide at
[`docs/contributing/CONTRIBUTOR_QUICKSTART.md`](../docs/contributing/CONTRIBUTOR_QUICKSTART.md)
or the public landing page
[openonco.info/contribute.html](https://openonco.info/contribute.html).
