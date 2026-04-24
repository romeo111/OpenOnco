# knowledge_base/

Implementation of the OpenOnco rule-engine knowledge base, per
[`specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md`](../specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md)
and [`specs/SOURCE_INGESTION_SPEC.md`](../specs/SOURCE_INGESTION_SPEC.md) Part B.

## Layout

```
knowledge_base/
├── schemas/              # Pydantic models — one file per entity type
├── clients/              # Live-API clients for referenced sources (base protocol + per-source)
├── validation/           # YAML loader + schema + referential integrity
├── ingestion/            # One-time / scheduled loaders for hosted sources
├── hosted/               # Everything we host locally (per SOURCE_INGESTION_SPEC §1.4 criteria)
│   ├── code_systems/     # ICD-O-3, LOINC, RxNorm, ATC (not yet populated)
│   ├── civic/            # CIViC bulk dump, per-date (not yet populated)
│   ├── ctcae/            # CTCAE v5.0 grading (not yet populated)
│   ├── ukraine/          # МОЗ протоколи, НСЗУ формуляр, Держреєстр (not yet populated)
│   └── content/          # Our own clinical content (Indications, Regimens, etc.)
│       ├── diseases/
│       ├── drugs/
│       ├── regimens/
│       ├── indications/
│       ├── biomarkers/
│       ├── contraindications/
│       ├── redflags/
│       ├── algorithms/
│       ├── tests/
│       ├── supportive_care/
│       ├── monitoring/
│       └── sources/
├── referenced/           # Source entity registry for `referenced` sources
└── cache/                # Query-level cache for live API calls (gitignored)
```

## Status

Skeleton + HCV-MZL reference case seed. Not yet a working rule engine.

What's here:
- Pydantic schemas for all 12 core entities (Source, Disease, Drug,
  Regimen, Indication, Biomarker, Test, Contraindication, RedFlag,
  SupportiveCare, MonitoringSchedule, Algorithm)
- `clients/base.py` — `SourceClient` protocol + `TTLCache` stub
- `validation/loader.py` — YAML loader + Pydantic validation + basic
  referential integrity check
- HCV-MZL seed: Disease + several Drugs + two Regimens + two Indications
  + Algorithm + Source entities

What's still missing (not yet needed for MVP skeleton):
- Actual rule engine (patient → applicable Indications → decision tree)
- Live client implementations (only `base.py` + protocol so far)
- Ingestion loaders (`ingestion/*.py` — placeholders only)
- Populated code systems, CIViC, CTCAE, Ukraine-local data

See `TODO.md` for known open issues and follow-ups.

## Running the validator

```bash
pip install -e .
python -m knowledge_base.validation.loader knowledge_base/hosted/content
```

Lists all entities, validates each against its schema, checks that
every referenced ID exists.

## Schema conventions

- `model_config = ConfigDict(extra="allow")` on every entity so adding
  fields in YAML doesn't break schema. Forces schema evolution to be
  intentional (pin specific fields as required when stable).
- IDs: prefix + upper-case, e.g. `DIS-HCV-MZL`, `DRUG-RITUXIMAB`,
  `IND-HCV-MZL-1L-STANDARD`.
- Citations to Source: always via `source_id` string (matches a Source
  entity `id`), never inline URL.
- Ukrainian + English names: `name` is the working name (usually EN for
  international entities, UA for МОЗ-only entities); `name_ua` and
  `name_en` always present when both are meaningful.

## Adding a new entity

1. Check `specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md` for the canonical
   entity definition.
2. Write YAML under the appropriate `hosted/content/<type>/` directory.
3. Run the validator.
4. If you add a new source, update `hosted/content/sources/` with full
   license/hosting metadata per `specs/SOURCE_INGESTION_SPEC.md` §3.
