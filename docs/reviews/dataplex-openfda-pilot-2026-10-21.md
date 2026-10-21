# Dataplex vs direct openFDA: free eight-drug pilot

**Observed:** 21 October 2026, 12:32:07–12:32:36 UTC (15:32 Europe/Kyiv).
**Decision:** prioritize a direct openFDA event adapter for a future research workflow.
The tested free Dataplex interface is useful for catalog discovery and inspecting
report-header transformations, but cannot answer the eight drug-specific queries.
Its paid drug/substance joins and analytics remain untested.

This is a technical source-access evaluation, not clinical evidence or a treatment
recommendation. No subscriptions, signup, warehouse trials or credentials were used.
No patient inputs, clinical rules or knowledge-base content were changed.

## Method and provenance

- Eight existing Drug records were selected to exercise checkpoint antibodies,
  other antibodies, kinase inhibitors and cytotoxic agents: pembrolizumab,
  nivolumab, rituximab, trastuzumab, osimertinib, imatinib, cisplatin and paclitaxel.
  This is a purposeful engineering sample, not a representative clinical cohort.
- KB snapshot: `b153efd327274c45a6fa2845a09d50f92dc87630`. Each Drug's ID, path,
  original names, RxNorm ID where present, and file SHA-256 are recorded in the
  [machine-readable observations](dataplex-openfda-pilot-2026-10-21.json).
- openFDA queries used the same inclusive **initial receipt date (`receivedate`)
  window, 2020-01-01 through 2026-06-30**. It starts at the supplier's documented
  default AEMS coverage and ends at a completed FDA source quarter. It is not an
  adverse-event onset window. The Dataplex free endpoint cannot apply this filter;
  no cross-provider count comparison is claimed.
- Each drug had a harmonized `openfda.generic_name` query and a broader OR query
  over that field, active substance, raw medicinal product and KB brand aliases.
  Parenthetical KB annotations such as `(biosimilar)` were removed from search
  aliases; the original labels were preserved in provenance.
- The broader query sampled 10 reports sorted by `receivedate:desc`. These are
  recent, non-random records; tie order is not guaranteed. Local matching examines
  each drug object separately before recording its role and identifier presence.
  It does not assign another co-reported medicine's role to the queried drug.
- Broad retrieval may include salts, biosimilars, combinations and related
  formulations, including antibody-drug conjugates. Ingredient identity has not
  been adjudicated. Counts are **query-matching reports**, not exposed patients,
  drug-attributable events, unique clinical cases, or comparative safety measures.
- The final run made 22 requests: 16 to openFDA, two static Dataplex requests and
  four Dataplex MCP requests. All returned usable responses; the generic-only
  osimertinib search returned FDA's explicit no-matches response. A transport or
  schema failure is recorded as unknown, never converted to zero.
- Responses were summarized in memory. The saved artifact contains request URLs,
  timestamps, response hashes, field names/types and aggregate completeness
  measures. It contains no raw reports, report IDs, narratives, individual
  demographics or adverse-reaction terms. Script SHA-256 binds the capture to
  the exact collector used.

## Drug retrieval results

All eight broader openFDA queries returned reports. Dataplex drug coverage is
**not assessable from the free header sample**, rather than zero or absent.

| KB drug | Generic-field query matches | Broader query matches | Broader sample inspected | Matched drug entries with RxCUI / all matched entries |
|---|---:|---:|---:|---:|
| Pembrolizumab | 85,052 | 85,301 | 10 | 13 / 13 |
| Nivolumab | 54,800 | 55,072 | 10 | 10 / 11 |
| Rituximab | 136,168 | 156,051 | 10 | 12 / 12 |
| Trastuzumab | 48,062 | 56,710 | 10 | 10 / 10 |
| Osimertinib | 0 | 26,995 | 10 | 0 / 10 |
| Imatinib | 14,159 | 21,228 | 10 | 13 / 16 |
| Cisplatin | 35,621 | 36,964 | 10 | 13 / 13 |
| Paclitaxel | 56,480 | 63,543 | 10 | 10 / 11 |

The table evaluates retrieval behavior, **not drug risk**. The same report can
match several queries and contain repeated drug entries; do not sum these counts.
More matched entries than sampled reports is possible and was observed.

The most actionable finding is osimertinib: relying solely on a harmonized
generic-name field would incorrectly suggest no coverage. The broader query
returned 26,995 reports; all 10 inspected records contained a local name match
and an active-substance field, while their matched drug objects lacked harmonized
generic names and RxCUIs. The KB record also has no RxNorm ID. This supports
fallback name retrieval and explicit identifier-missing states; it does not
establish an exact molecule-specific cohort.

All 80 broader-query samples had reaction fields. Of those sampled reports, 56
contained multiple drug entries. Drug–reaction co-occurrence therefore cannot be
interpreted as a validated causal link. [FDA explains these limitations](https://open.fda.gov/apis/drug/event/).
FDA's [harmonization documentation](https://open.fda.gov/apis/openfda-fields/)
also explains why harmonized fields may be missing.

## What the free Dataplex service actually returned

Both the [static sample](https://api.dataplex-consulting.com/v1/products/fda_aems/sample.json)
and MCP `get_sample_data(slug="fda_aems", max_rows=100)` returned **the same 100
`DRUG_REPORTS` rows**, verified by a canonical rows hash. The sample exposed 45
fields, including report/version IDs, receipt dates, seriousness, demographics,
drug/reaction counts and a narrative field. No raw field values were retained.

There were **no drug-name, substance, brand or RxNorm fields** in those rows.
The live `get_sample_data` input schema accepted only `slug` and `max_rows`;
there was no drug, date or table selector. `search_health_datasets` searches the
catalog, not individual adverse-event records. No arbitrary SQL execution tool
was exposed. Thus the free interface did not let us inspect the underlying
`DRUG_SUBSTANCES` or `DRUG_REACTIONS` rows for any of the eight drugs.

Some transformations were directly observable: `SERIOUS` was a native Boolean,
`DRUG_COUNT` and `REACTION_COUNT` were integers, and decoded report/sex fields
were present. Age and weight remained strings when non-null. This does not
validate drug normalization, complete joins, deduplication or signal analytics.

The `get_data_dictionary` MCP response contained schema/table names, example SQL
and a link to full documentation. It did not return a column-level dictionary
through this tool. The catalog listed child tables and aggregate products, but
listing their names is not evidence that their data was tested.

## Freshness and cost

| Observation | Returned value | Interpretation |
|---|---|---|
| openFDA `meta.last_updated` | 2026-07-30 | Dataset metadata, not each report's last update |
| Dataplex catalog `generated_at` | 2026-07-30T22:56:04Z | Catalog snapshot was 83 calendar days old |
| Dataplex static sample `generated_at` | 2026-07-30T22:55:59Z | Free sample was 83 calendar days old |
| Dataplex sampled initial receipt dates | 2020-02-13–2026-01-23 | Describes these 100 rows, not full-dataset coverage |
| Dataplex catalog refresh claim | `DAILY` | Supplier claim; not a verified free-sample refresh |
| Dataplex catalog monthly price | USD 995 | Published product metadata, not a quote or purchase |
| Pilot charges | USD 0 | Public endpoints only; no paid access activated |

The MCP sample omitted the static file's generation timestamp. Its rows hash
matched the dated static sample, which supplied the freshness evidence.
The [MCP documentation](https://docs.dataplex-consulting.com/snowflake-access/mcp-server)
describes weekly sample regeneration; the observed free sample does not establish
that cadence or a freshness advantage over direct openFDA. The paid warehouse's
current contents were not inspected. Both vendors' dates are kept separate from
retrieval time.

The active supplier product is AEMS (`fda_aems`). The supplier's legacy FAERS
product retirement is not evidence that openFDA's event API is retired; it worked
throughout this pilot. Product descriptions and source-release dates should not
be conflated. See the [active Dataplex documentation](https://docs.dataplex-consulting.com/data-catalog/fda-aems-dataset)
and [FDA's quarterly extracts](https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html).

## Recommendation and follow-up boundary

1. **Use direct openFDA for the next research prototype.** It supplied drug-specific
   records and query metadata for all eight drugs without a subscription. The
   existing OpenOnco client supports labels and recalls; an event adapter remains
   separate implementation work.
2. **Implement name and identifier handling before any pharmacovigilance analysis.**
   Preserve missing harmonization, separate retrieval from ingredient adjudication,
   and retain matched-object drug roles. A name match does not establish indication,
   oncology use, causality or comparative incidence.
3. **Defer paid Dataplex integration.** This pilot verified free endpoint operation
   and some header transformations, but could not measure the advertised drug-table
   quality or the engineering time saved by paid analytics. No paid benefit is
   inferred from the successful catalog/sample calls.
4. **Keep findings in a research/review workflow.** Nothing here automatically
   creates red flags, changes doses, chooses regimens or alters treatment plans.
   Source licensing/redistribution review and human clinical review remain separate
   requirements for any future ingestion. No MedDRA dictionary or hierarchy was
   downloaded or added to the project.

## Reproduce and verify

From the repository root, with Python 3.12 and existing project dependencies:

```bash
python scripts/pilot_dataplex_openfda.py --output .tmp/dataplex-openfda-new-observation.json --sample-size 10
python -m pytest tests/test_pilot_dataplex_openfda.py -q
python -m ruff check scripts/pilot_dataplex_openfda.py tests/test_pilot_dataplex_openfda.py
```

The collector refuses to overwrite an observation. A rerun can change counts,
timestamps and sample membership as upstream data changes. Use a new output path.
It makes no use of API keys found in the environment and never submits local
patient records. The script is an isolated audit tool, not a production connector.

Verification completed: 10 focused pilot tests, 16 repository Wiki/head/discovery
tests, targeted Ruff checks and the repository's critical-correctness Ruff gate
passed. The KB validator loaded 4,273 entities with zero schema, reference or
contract errors (396 existing warnings). An independent read-only review checked
the report against its JSON observations and found no remaining actionable issues.
The delivery branch was then fast-forwarded over two news-only commits; the eight
Drug files and pilot paths were unchanged from the captured KB snapshot.
