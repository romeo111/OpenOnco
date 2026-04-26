# Engine bundle layout — core + per-disease lazy load

The `/try.html` Pyodide demo runs the real OpenOnco engine in the
browser. To do that it has to download the engine's Python code +
schemas + validation + the entire knowledge base as a zip. As the KB
has grown past 1.7K entities the monolithic `openonco-engine.zip` has
crossed 1.8 MB compressed, and the on-load latency for a first-time
visitor is dominated by that single fetch.

CSD-5B introduces a **two-tier bundle split** so the page becomes
interactive against the core (~1.4 MB compressed) while the
disease-specific tail is fetched only after the patient's `disease_id`
is known.

## Artifacts produced by `scripts/build_site.py::bundle_engine()`

```
docs/
  openonco-engine.zip              # legacy monolithic — back-compat / fallback
  openonco-engine-core.zip         # code + schemas + shared content
  openonco-engine-index.json       # disease_id → URL map + per-bundle SHA-256 versions
  disease/
    openonco-dis-dlbcl-nos.zip     # per-disease module
    openonco-dis-crc.zip
    …                              # one zip per disease the KB covers
```

### What goes into core

- `knowledge_base/__init__.py`, `engine/`, `schemas/`, `validation/`
- All shared content under `hosted/content/`:
  - `drugs/`, `sources/`, `biomarkers/`, `tests/`, `supportive_care/`,
    `monitoring/`, `workups/`, `questionnaires/`, `contraindications/`,
    `mdt_skills/`
  - All disease metadata (`diseases/dis_*.yaml`) — needed before the
    disease picker can render
- Universal redflags (`redflags/universal/*.yaml`)
- Any `indications/`, `algorithms/`, `regimens/`, `redflags/`, or
  `biomarker_actionability/` YAMLs that don't pin to a single disease

### What goes into a per-disease module

Files in the disease-scoped directories that resolve to a single
disease via:

- `disease_id: DIS-…` (top-level)
- `applicable_to_disease: DIS-…`
- `applicable_to.disease_id: DIS-…` (nested)
- A single concrete entry in `relevant_diseases:` (for redflags;
  `*` and multi-disease lists keep the file in core)

The attribution rule lives in
`scripts/build_site.py::_disease_id_for_yaml` — and is mirrored in
`scripts/profile_engine_bundle.py::_disease_id_from_yaml` so the
profile and the actual split agree.

### Bundle index

`openonco-engine-index.json`:

```json
{
  "core": "openonco-engine-core.zip",
  "core_version": "abc123def456",
  "monolithic": "openonco-engine.zip",
  "monolithic_version": "789aaa111bbb",
  "diseases": {
    "DIS-DLBCL-NOS": "disease/openonco-dis-dlbcl-nos.zip",
    "DIS-CRC": "disease/openonco-dis-crc.zip"
  },
  "disease_versions": {
    "DIS-DLBCL-NOS": "12ab34cd56ef",
    "DIS-CRC": "78ef90ab12cd"
  }
}
```

The `core_version` / `disease_versions` are 12-char SHA-256 prefixes of
each zip's bytes — used as `?v=…` cache-busters so the browser always
gets fresh bundles when the KB changes.

## Python-side merge — `knowledge_base.engine.lazy_loader`

```python
from knowledge_base.engine import (
    lazy_load_disease,       # high-level: index lookup + extract + cache-clear
    merge_disease_module,    # mid-level: extract bytes/path + cache-clear
    load_disease_module,     # low-level: extract only
    apply_disease_module,    # invalidate loader cache + return summary
    load_bundle_index,
    url_for_disease,
)

# Typical test / non-Pyodide use:
result = lazy_load_disease(
    "DIS-DLBCL-NOS",
    bundle_dir=Path("docs"),
    kb_root=tmp_kb,
)
# result["summary"]["by_type"] now lists the loaded entity counts
```

In Pyodide the JS layer owns the `fetch()` and the
`pyodide.unpackArchive(buf, "zip")` step. From Python it then suffices
to call `apply_disease_module(content_root)` to drop the loader cache,
so the next `generate_plan(...)` re-validates with the just-arrived
YAMLs included.

## Status of the /try.html JS handler

The Pyodide page in this commit still fetches the **monolithic**
`openonco-engine.zip` — the bundle infrastructure is in place but the
JS lazy-load handler that consults the index is a follow-up. The
monolithic bundle is intentionally still produced as a back-compat /
fallback artifact so that:

- old clients keep working,
- if the index fetch ever fails the page can fall back to the single
  zip without code changes,
- batch tests / non-browser callers (e.g. CLI patient runs) keep using
  one bundle.

Once `/try.html` is wired to the index, we expect on-load weight to
drop from the current ~1.8 MB to ~1.4 MB (core only) plus a ~25 KB
disease module fetched after the disease picker resolves.

## Testing

`tests/test_engine_bundle_optimization.py` covers:

- Core, index, monolithic, and per-disease zips all produced
- Core bundle stays under the 2 MB ceiling
- Each per-disease bundle stays under 300 KB
- Index entries match files on disk (no orphans either way)
- Slug rule (`disease_bundle_basename`) matches every URL in the index
- Per-disease bundles only contain that disease's YAMLs
- `lazy_load_disease()` round-trips: core → DLBCL merge → DLBCL
  entities visible to the loader, no CRC content leaks
- The monolithic bundle alone still produces a valid KB

Run:

```
py -3.12 -m pytest tests/test_engine_bundle_optimization.py
```

## Profile script

`scripts/profile_engine_bundle.py` walks the monolithic zip and writes
a Markdown report under `docs/plans/csd_5_bundle_profile_<date>.md`
showing weight by subtree, entity type, and attributed disease, plus
the largest individual files. Run it whenever you want to size the
next iteration of the split.
