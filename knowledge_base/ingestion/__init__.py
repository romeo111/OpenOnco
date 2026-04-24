"""One-shot / scheduled loaders for hosted sources.

Each loader reads an external file (CSV / TSV / JSON / PDF) and emits
normalized YAML under `knowledge_base/hosted/<kind>/<version>/`. Loaders
are invoked manually for hosted sources that have no live API, or on
a schedule for sources that update regularly (CIViC weekly, НСЗУ
monthly, etc. — see SOURCE_INGESTION_SPEC §18).

All loaders must be idempotent: running twice on the same input
produces the same output. Diff vs previous version is the
responsibility of the workflow calling the loader.
"""
