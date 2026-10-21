# Development and deployment

## Runtime

Use Python 3.12 (CI runtime), install `requirements.lock`, then `python -m pip install --no-build-isolation --no-deps -e .`. See [README](../README.md) for virtual-environment setup. The optional MCP extra is installed with `python -m pip install -e ".[mcp]"`.

## Verify a change

```bash
python scripts/audit_validator.py --human
python -m pytest tests/test_kb_wiki.py tests/test_site_head_faq.py tests/test_site_discovery.py -q
python -m ruff check --select E9,F63,F7,F82 scripts/ knowledge_base/ serverless/ api/ tests/
```

Run additional tests appropriate to the changed component. The [Validate Knowledge Base workflow](../.github/workflows/validate-kb.yml) also checks examples, executable conditions, DLBCL review contracts and engine regressions. The nightly suite covers a broader selection. A green test run is engineering evidence, not clinical approval.

## openFDA adverse-event source adapter

Use `OpenFDAClient.fetch(OpenFDAEventQuery(...))` for direct, read-only retrieval of FDA adverse-event reports by active substance and/or brand. The adapter is available to Python callers; it does not change treatment rules, dose calculations, patient recommendations or the clinical API.

```python
from knowledge_base.clients.openfda_client import OpenFDAClient, OpenFDAEventQuery

client = OpenFDAClient()
query = OpenFDAEventQuery(
    active_substance="osimertinib",
    brand_names=("Tagrisso",),
    received_from="2020-01-01",
    received_to="2026-06-30",
    limit=10,
    skip=0,
)
response = client.fetch(query)
reports = response.data["results"]
metadata = response.data["meta"]
provenance = (response.source_id, response.fetched_at, query.request_url)
```

For a loaded drug YAML record, pass `drug["names"]["english"]` and `tuple(drug["names"].get("brand_names", []))`. Search combines harmonized generic/brand fields with reported medicinal-product and active-substance fields, because harmonized names can be absent. Brand display annotations such as `(biosimilar)` are removed for retrieval; the input labels are preserved. Names are quoted literals, with duplicate clauses removed. This is broad discovery: combinations, formulations and similarly named products still require identity review. See the [eight-drug pilot](reviews/dataplex-openfda-pilot-2026-10-21.md).

`limit` accepts 1–1000 and `skip` 0–25000. Optional dates must be supplied together as inclusive `YYYY-MM-DD` bounds on FDA **receipt date**, not reaction onset. Results are sorted by receipt date descending; offset pages are not a stable snapshot. [FDA query parameters](https://open.fda.gov/apis/query-parameters/) and [event endpoint](https://open.fda.gov/apis/drug/event/how-to-use-the-endpoint/).

The response preserves original report arrays and FDA metadata, including `meta.last_updated` when present. `fetched_at` is retrieval time, not source freshness. Only FDA's explicit `404 NOT_FOUND / No matches found!` becomes an empty result; it has no invented update date. With `skip=0`, its total is zero. With `skip>0`, FDA may mean an exhausted page, so the adapter omits the unknown total. Other HTTP failures, throttling, transport failures and malformed responses raise `OpenFDAError` and are not cached. Error messages and `query.request_url` omit API credentials.

The existing client provides a 24-hour memory cache and request throttling; keep a client instance across calls. `OPENFDA_API_KEY` is optional for this endpoint and stays in the environment. The anonymous daily quota is shared by IP; the client does not track that quota or retry 429 responses. An optional disk cache must use an ignored local directory; do not commit fetched report bodies. Run `python -m pytest tests/test_openfda_client.py tests/test_base_source_client.py -q` for the offline adapter contract.

FDA reports may contain several drugs and several reactions without linking individual pairs. Counts are neither incidence nor proof of causality, and an empty search does not establish safety. The adapter performs no risk ranking or automatic clinical-rule updates. [FDA adverse-event limitations](https://open.fda.gov/apis/drug/event/).

## Preview and build

```bash
python -m scripts.build_site --output build/site-preview
python -m http.server 8000 --directory build/site-preview
```

This builds into a separate directory. To prepare the published output, use `python -m scripts.build_site --output docs`. Avoid `--clean` against `docs/`: that directory also contains manually authored Markdown and audit artifacts. For metadata-only changes, call `scripts.site_head.finalize_site_discovery(Path("docs"))`; it updates head/discovery assets without rebuilding clinical page bodies. Run discovery tests and inspect the resulting diff.

The shared navigation is in `scripts/site_nav.py`, styles in `scripts/site_header.css`, Wiki in `scripts/build_kb_wiki.py`, Handbook in `scripts/build_handbook.py`, and discovery metadata in `scripts/site_head.py`. Daily rebuilds use the same sources.

### Partial clinical releases

After generating a selected group of clinical pages, finalize that exact group before committing. Create a JSON manifest of relative HTML paths, including every changed original and its translated editions, for example `["cases/example.html", "ukr/cases/example.html", "fi/cases/example.html"]`.

```bash
python -m scripts.finalize_partial_site --output docs --manifest .tmp/release-pages.json
python -m scripts.finalize_partial_site --output docs --manifest .tmp/release-pages.json --write
node tests/browser_translation_cache.cjs
node tests/browser_bundle_versions.cjs
```

The first command is a dry run. Output is normalized to LF line endings, so an initial run can report formatting changes in a Windows checkout. The second applies the verified batch: shared navigation, discovery metadata, the existing versioned geographic-language asset, and reader fingerprints bound to final originals. It validates the whole batch before replacing files, preserves clinical bodies, rejects preserved pages and paths outside the output, and restores already-replaced pages if a write fails. Keep the normal shared header and language assets in the output; this command does not regenerate them. It also does not rebuild engine archives, search indexes, sitemaps or API packages: verify those separately when their source data changes.

The default path inventory comes from committed `docs/` filenames plus the manifest. For a separate preview with additional destinations, pass `--inventory .tmp/preview-paths.json`, a JSON list of available relative HTML paths. Reader originals outside the manifest must be inventoried; they remain unchanged. A synchronized fingerprint proves source identity, not translation accuracy or clinical approval.

When a partial release adds public pages, extend the existing sitemap separately:

```bash
python -m scripts.update_partial_sitemap --output docs --manifest .tmp/new-pages.json
python -m scripts.update_partial_sitemap --output docs --manifest .tmp/new-pages.json --write
```

The dry run lists additions and metadata changes. The command preserves all previously indexed URLs, even when their HTML is absent from a partial checkout, and reads only selected page heads to exclude redirects, noindex pages and canonical aliases. It rejects preserved pages before opening selected HTML, uses the normal deterministic compressed sitemap writer and reciprocal language links, and changes no HTML. It cannot establish actual search-engine indexing, translation accuracy or clinical approval.

## Source-withheld planning records

Indications and regimens can declare `planning_status: withheld` with a `planning_status_reason`. This is a source-content safety hold, independent of patient eligibility or clinical approval. An explicit unknown status also blocks planning. A selected/default withheld record suppresses treatment and sequencing without promoting another medicine; withheld alternatives and later-line references are omitted. Direct track materialization rejects held records. Wiki pages show the hold explicitly. An absent status preserves existing draft behavior and never implies clinical approval.

Review the source conflict and record as a whole before reactivation. Do not replace it automatically with a new transplant recommendation. Run `python -m pytest tests/test_withheld_planning_records.py tests/test_ptcl_firstline_transplant_reference.py` and the ordinary routing checks before refreshing scoped archives and Wiki pages.

## Patient watchpoint translation drafts

English patient contact instructions use saved pairs in `knowledge_base/engine/_patient_watchpoint_en.json`. A fingerprint binds each pair to its regimen ID, full source trigger/action, urgency, cycle-day window and source IDs. Changes invalidate both fragments together; unknown conditions and unmapped instructions retain the marked Ukrainian original. The clinician report and clinical records are unchanged. These drafts require clinical and language review.

Translated spans remain protected from a second machine translation in other language editions. Update and review an entire symptom/action pair when its source changes, then run `python -m pytest tests/test_patient_watchpoint_translations.py`. Refresh affected patient pages, shared-reader source hashes and browser/API packages through the scoped release workflow. Keep the original Ukrainian report available and the partial-draft notice visible.

## Publish

After deployment, check the eight main public pages in all eleven languages and the additional internal destinations linked from their headers:

```bash
python -m scripts.check_live_navigation --report .tmp/live-navigation.json
```

Use `--base-url http://localhost:8000/` for a locally served preview. The check uses bounded, read-only GET requests, verifies shared headers, language order and flags, document language, canonical links and main landmarks, and fails on broken navigation destinations. Redirects cannot leave the selected website origin. It does not submit cases, call the clinical API, execute JavaScript or prove visual layout, accessibility with assistive technology, or clinical correctness. Create the report directory before running.

GitHub Pages serves branch **`master`**, directory **`/docs`**, at **https://openonco.info/**. Push reviewed generated output and its source changes to the deployment branch through the repository's authorized delivery flow. The standard **pages build and deployment** run must succeed; inspect the live pages afterward. The [Daily Site Refresh](../.github/workflows/daily-site-refresh.yml) rebuilds from current KB content and commits changed output.

The optional question API is a separate deployment; updating GitHub Pages does not configure its secrets or deploy that backend. Keep all credentials outside Git and use synthetic fixtures in demos, screenshots and review packets.

The existing Vercel project is `openonco-vercel-api`, serving `https://openonco-vercel-api.vercel.app/api/clinical-question`. After verification, `python -m scripts.prepare_clinical_api_deploy` creates an isolated package under `.tmp/clinical-api-deploy` containing the API, serverless adapter and public knowledge base; it excludes website pages and translation models. Link that directory to the existing project and deploy with the authenticated Vercel CLI. Do not create a replacement project or copy secrets into source files. Verify an empty synthetic request after deployment; it must return a localized clarification without calling the model provider.


### BV-CHP CD30 input confirmation

The two first-line BV-CHP indication records require `biomarkers.BIO-CD30-IHC: "positive"` through the existing `confirmed_profile_values` contract. Missing, unknown, numeric, Boolean or structured results are not converted into confirmation. A false or malformed `findings.cd30_positive` blocks the candidate. The guard applies to selected, alternative and sequencing candidates: a failed selected record withholds the plan without promoting another treatment. Do not infer a universal percentage cutoff or regulatory region from interface language. This confirmation check does not approve histology-specific preference, individual eligibility or local authorization. Existing noncanonical marker aliases remain unconfirmed; input normalization and conflicting alias reconciliation require separate work.

Run `python -m pytest tests/test_cd30_confirmation.py tests/test_tcell_engine.py tests/test_tcell_monitoring.py` and the pinned Node WASM test when modifying this contract. Patient and clinician notices must explain CD30 confirmation in EN/UA and retain the no-substitute behavior. Source outcome and regional preference defects are tracked in the BV histology audit.


### BV-CHP evidence scope

Use the separate five-year ECHELON-2 source (`SRC-ECHELON-2-FIVE-YEAR-2022`, Annals of Oncology, DOI `10.1016/j.annonc.2021.12.002`) for long-term outcome estimates. Preserve pooled ITT versus AITL subgroup identity, exploratory status, comparator CHOP and confidence intervals. Do not transform pooled benefit into subtype-specific superiority or infer benefit/harm for an individual from a limited subgroup. The shared indication is still used by more than one disease; its pooled estimates must never be presented as PTCL-NOS or AITL estimates. Clinical reports currently expose source provenance but do not display all structured outcome values; the Wiki and data records preserve the detailed estimates.

US label authorization and histology-specific recommendations are distinct. Current regional authorization, access, algorithm preference and individual eligibility remain separate review work. Interface language is not jurisdiction. Unsupported cross-histology recommendation grading has been cleared in these two records. Do not restore grade or reviewer dates without applicable evidence and actual signoff. Run `python -m pytest tests/test_bv_evidence_scope.py tests/test_cd30_confirmation.py` and pinned Node WASM checks when changing these records.


### BV-CHP neuropathy and patient contact references

First-line BV-CHP indications surface `CI-BRENTUXIMAB-BLEOMYCIN` from US ADCETRIS section 4; the myeloma bortezomib contraindication and its alternative regimens are not applicable. This free-form contraindication is a displayed reference, not an executable medication-interaction screen. Baseline neuropathy needs specialist assessment; treatment-emergent modification rows must not be converted into an automatic baseline eligibility decision.

Keep US adult 1.8 mg/kg every-three-week chemotherapy Table 2 separate from eviQ 4038 v3. Preserve sensory versus motor grade and the eviQ recovery delay; monotherapy, AVD, pediatric and other schedules have different rules. The entries are clinician reference text and never modify patient dose inputs. The reference remains incomplete for full dosing, organ function, cycle selection and clinical eligibility.

BV-CHP patient contact points use their own eviQ patient-information source. Fever/contact urgency must not be limited to a presumed nadir window; infusion reactions are not restricted to cycle 1 or being physically in the clinic. Report neuropathy without inventing a next-visit delay or a self-adjustment instruction. English pairs retain source fingerprints and draft status. Run `python -m pytest tests/test_bv_neuropathy_safety.py tests/test_patient_watchpoint_translations.py` and pinned Node WASM checks.


### BV-CHP adult dose and course context

The shared BV-CHP reference states `1.8 mg/kg (maximum 180 mg)` and retains a 21-day frequency, without calculating an individual dose. Its `total_cycles` is unset: label/eviQ 6–8 references and the ESMO-EHA systemic-ALCL contexts are not interchangeable patient defaults. Typed `course_context_note` / `course_context_note_ua` fields render escaped, original-source text in both clinician and patient views; absent fields preserve other regimen behavior. Source context is information, not an automatic cycle selector.

Both first-line BV indications require confirmed canonical adult age (at least 18) in addition to confirmed CD30. A failed selected applicability check withholds all treatment without promoting an alternative. This is not whole-patient eligibility, pediatric/off-label care, organ-function review or regulatory approval. Biomarker/age alias reconciliation and explicit protocol-region selection remain separate work. Run `python -m pytest tests/test_bv_course_context.py tests/test_cd30_confirmation.py` and the pinned Node WASM check after changing these contracts.
