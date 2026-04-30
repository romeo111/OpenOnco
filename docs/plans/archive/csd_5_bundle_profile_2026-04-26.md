# CSD-5B engine-bundle composition profile — 2026-04-26

Bundle: `docs/openonco-engine.zip`  
Compressed size: **1775.7 KB** (1,818,317 bytes)

## Breakdown by top-level subtree (compressed)

| Subtree | Size | % |
|---|--:|--:|
| `hosted` | 1406.6 KB | 92.8% |
| `engine` | 83.5 KB | 5.5% |
| `schemas` | 20.1 KB | 1.3% |
| `validation` | 5.2 KB | 0.3% |
| `__init__.py` | 0.1 KB | 0.0% |

## Code vs content

- Python code: **108.9 KB** across 39 files
- KB content (YAML): **1406.6 KB** across 1275 files

## KB content by entity type (compressed)

| Entity dir | Files | Compressed | % of content |
|---|--:|--:|--:|
| `indications` | 200 | 340.1 KB | 24.2% |
| `redflags` | 270 | 238.1 KB | 16.9% |
| `drugs` | 167 | 220.5 KB | 15.7% |
| `regimens` | 171 | 203.4 KB | 14.5% |
| `algorithms` | 88 | 87.7 KB | 6.2% |
| `sources` | 105 | 87.5 KB | 6.2% |
| `diseases` | 52 | 58.9 KB | 4.2% |
| `tests` | 95 | 52.7 KB | 3.7% |
| `biomarkers` | 67 | 48.4 KB | 3.4% |
| `workups` | 24 | 30.6 KB | 2.2% |
| `contraindications` | 12 | 10.9 KB | 0.8% |
| `questionnaires` | 3 | 9.7 KB | 0.7% |
| `supportive_care` | 13 | 9.4 KB | 0.7% |
| `monitoring` | 8 | 8.7 KB | 0.6% |

## Top diseases by attributed bundle weight

Best-effort tagging: a YAML is attributed to a disease when it cites `disease_id`, `applicable_to_disease`, `applicable_to.disease_id`, or (for redflags) the first concrete entry in `relevant_diseases`.

| Disease | Files | Compressed |
|---|--:|--:|
| `DIS-AML` | 16 | 24.8 KB |
| `DIS-MM` | 14 | 24.5 KB |
| `DIS-DLBCL-NOS` | 15 | 24.2 KB |
| `DIS-FL` | 15 | 23.0 KB |
| `DIS-CML` | 15 | 22.4 KB |
| `DIS-CLL` | 13 | 20.7 KB |
| `DIS-PMF` | 14 | 19.8 KB |
| `DIS-CRC` | 16 | 19.6 KB |
| `DIS-MCL` | 13 | 19.3 KB |
| `DIS-BURKITT` | 12 | 19.2 KB |
| `DIS-AITL` | 11 | 18.0 KB |
| `DIS-APL` | 13 | 17.9 KB |
| `DIS-CHL` | 12 | 17.5 KB |
| `DIS-MDS-LR` | 13 | 17.3 KB |
| `DIS-HCV-MZL` | 12 | 17.1 KB |
| `DIS-PV` | 13 | 17.0 KB |
| `DIS-ALCL` | 12 | 16.5 KB |
| `DIS-WM` | 12 | 16.3 KB |
| `DIS-B-ALL` | 9 | 16.1 KB |
| `DIS-MF-SEZARY` | 11 | 15.4 KB |

**Total disease-attributed YAML weight:** 650.4 KB across 492 files

**Shared / un-attributable YAML weight (drugs, sources, biomarkers, …):** 756.1 KB

## Top-15 largest individual files in the bundle

| Compressed | Path |
|--:|---|
| 21.6 KB | `knowledge_base/engine/render.py` |
| 15.0 KB | `knowledge_base/engine/mdt_orchestrator.py` |
| 6.2 KB | `knowledge_base/engine/plan.py` |
| 5.5 KB | `knowledge_base/engine/cli.py` |
| 5.4 KB | `knowledge_base/engine/mdt_protocol.py` |
| 5.2 KB | `knowledge_base/validation/loader.py` |
| 4.0 KB | `knowledge_base/engine/experimental_options.py` |
| 3.6 KB | `knowledge_base/hosted/content/questionnaires/quest_hcv_mzl_1l.yaml` |
| 3.5 KB | `knowledge_base/hosted/content/drugs/methotrexate.yaml` |
| 3.4 KB | `knowledge_base/engine/access_matrix.py` |
| 3.4 KB | `knowledge_base/hosted/content/drugs/isatuximab.yaml` |
| 3.3 KB | `knowledge_base/hosted/content/questionnaires/quest_mm_1l.yaml` |
| 3.3 KB | `knowledge_base/engine/diagnostic.py` |
| 3.2 KB | `knowledge_base/hosted/content/drugs/gemcitabine.yaml` |
| 3.2 KB | `knowledge_base/hosted/content/drugs/trastuzumab.yaml` |

## Implications for the core/per-disease split

- Biggest single disease attributed: `DIS-AML` at 24.8 KB compressed. Per-disease bundles should comfortably fit under 300 KB compressed.

- Estimated core bundle (code + shared content + disease metadata): **~1402.3 KB** compressed.

- Estimated per-disease tail (indications + algorithms + regimens + disease-specific RFs + BMA cells): **~650.4 KB** total, distributed.

