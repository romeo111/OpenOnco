# ⚠️ SUPERSEDED — 2026-04-27

This document described the planned OncoKB integration (proxy-based, with
academic API token). The plan was abandoned 2026-04-27 after audit
revealed OncoKB Terms of Service explicitly forbid the OpenOnco use case
(redistribution, patient-care report generation, AI model training).
Replaced by CIViC (CC0).

**See instead:**
- `docs/reviews/oncokb-public-civic-coverage-2026-04-27.md` — the audit
- `docs/plans/civic_integration_v1.md` — the replacement plan
- Engine modules use `actionability_*` naming to keep source-pluggability open.

The original document below is preserved for historical reference and
to document the architectural decisions (engine firewall, fail-open
contract, level taxonomy) that carried over to the CIViC implementation.

---

# OncoKB integration · Safe rollout plan v3

**Status:** ratified 2026-04-26. Supersedes v1/v2 (in-conversation drafts).
Consolidates `oncokb_data_scope.md`, `oncokb_cache_strategy.md`,
`oncokb_render_integration.md`, `oncokb_source_classification.md`.

**Authoritative for OncoKB integration work.** Other oncokb_*.md plans
remain as decision-records but are subordinate to this document.

---

## 0. Founding principles

1. **§8.3 invariant:** OncoKB never influences routing — surface only.
2. **Default-OFF feature flag** at every layer (extractor → engine call → render).
3. **Fail-open for plan generation:** OncoKB outage never blocks `generate_plan()`.
4. **Token never leaves server-side proxy.**
5. **No on-disk snapshot** (OncoKB Academic Terms).
6. **Patient-mode = OncoKB section fully hidden** (HCP evidence layer only).
7. **Each phase mergeable independently.** No big-bang PR.
8. **Hard-pause gates** at deploy, real-user exposure, and default-on transitions.

---

## 1. Threat model (12 items)

| # | Threat | Severity | Mitigation |
|---|--------|----------|-----------|
| T1 | Token leaks to browser | 🔴 critical | Server-side proxy only; CSP forbids direct oncokb.org from browser |
| T2 | Engine routing depends on OncoKB | 🔴 critical | Architectural firewall: `_build_tracks` is pure, no oncokb args; lint rule + import-graph test |
| T3 | R1/R2 contradicts engine recommendation, clinician misses it | 🔴 critical | `engine/oncokb_conflict.py`: detect drug overlap → inline banner in track-card + ProvenanceEvent + MDT trigger |
| T4 | OncoKB unavailable → Plan fails | 🟠 high | Fail-open contract: any error → `oncokb_layer=None` + warning |
| T5 | Variant string mismatch → false negative | 🟠 high | Normalization layer (3-format fallback) + 30+ test corpus |
| T6 | OncoKB content stale | 🟡 medium | Record `oncokb_data_version` in provenance; alert >90d unchanged |
| T7 | Cache stampede on cold-start | 🟡 medium | Singleflight (asyncio.Lock per key) |
| T8 | Patient-mode HTML accidentally contains OncoKB | 🟠 high | Snapshot test + secondary regex grep CI step |
| T9 | Quota exhaustion (Academic ~1000/day) | 🟡 medium | Rate-limit middleware + daily counter + 80% alert |
| T10 | Token in logs via error echo | 🟡 medium | Scrub middleware (regex Bearer/api-key/token) |
| T11 | Privacy: gene+variant+oncotree+timing → re-id | 🟢 low | Batched + jitter; OncoTree top-level only; no session id |
| T12 | Auto-bias: clinician anchors on OncoKB Level 1 | 🟠 high | Levels 1/2 filtered out (locked decision Q1); section visually separated, after both tracks |

---

## 2. Locked clinical decisions (Q1–Q8)

| # | Decision | Rationale |
|---|----------|-----------|
| **Q1** | Show **only Levels 3A/3B/4 + R1/R2**. Filter out 1/2. | Engine already covers Levels 1/2 in its tracks; surfacing them = noise + automation-bias risk. |
| **Q2** | R1 + R2 **both inline** in track-card. R1 = red `🛑`, R2 = amber `⚠` ("preclinical resistance signal"). Both also in OncoKB section "Resistance" block. | Overshow > hide for safety (§15.2 C6). Differential styling preserves signal hierarchy. |
| **Q3** | Top 3 (by level rank) visible; rest in `<details>` "Show N more". | Density vs completeness balance. |
| **Q4** | Pan-tumor fallback **shown with warning badge** "ℹ Без фільтра tumor-type" + tooltip. | Better than silently hiding evidence; warning prevents over-trust. |
| **Q5** | Multiple biomarkers → **single combined table + cross-biomarker analysis block**. Sort: level desc, gene asc. Cross-analysis surfaces (a) drug-overlap (1 drug ∈ ≥2 rows = efficiency signal) and (b) co-occurrence sanity check ("rare co-occurrence; consider re-test"). | One table = one mental model. Cross-analysis adds value uniquely possible at integration layer. |
| **Q6** | PMID inline as clickable PubMed links: `<a href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank" rel="noopener">PMID:{pmid}</a>` next to drug. | Inline = lower friction for verify. |
| **Q7** | revise_plan re-queries OncoKB (forces `oncokb_enabled=True` if previous version had it). Provenance records `oncokb_data_version` drift if changed. | Data may have updated; staleness defeats the integration's value. |
| **Q8** | Confidence display: `Level 3A · 5 PMIDs · FDA-approved (sotorasib, 2021)`. Pulls level + PMID count + FDA-approval status from OncoKB response. | Quality signal beyond level alone. |

---

## 3. Constraints to verify in Phase 0 (assumption registry)

| # | Assumption | How to verify | Risk if false |
|---|------------|---------------|---------------|
| A1 | Endpoint = `GET /api/v1/annotate/mutations/byProteinChange?hugoSymbol=&alteration=&tumorType=` | curl with real token | Rewrite proxy `_call_oncokb` |
| A2 | Auth = `Bearer {token}` | docs.oncokb.org + curl | Rewrite auth |
| A3 | Response `treatments[].level` = `LEVEL_1` etc. | Live response inspection | Parser breaks |
| A3-bis | Response `treatments[].fdaApproved` exists (boolean or string) | Inspection | Q8 FDA badge needs alt source |
| A4 | Response contains `dataVersion` | Inspection | Provenance gap |
| A5 | Academic quota = X req/day (exact) | OncoKB account dashboard | Cost model breaks |
| A6 | Variants accepted as `V600E` short OR `p.V600E` OR `p.Val600Glu` | curl with all three | Normalization layer needs more cases |
| A7 | tumorType param key = `tumorType` (vs `oncoTreeCode`) | docs + curl | URL params |
| A8 | Structural variants need separate endpoint | docs | Out-of-scope confirmed |
| A9 | `X-RateLimit-Remaining` header present | inspection | Use counter-based quota tracking |
| A10 | Token rotation cadence (manual? annual?) | account UI | Operational SLA gap |
| A11 | `treatments[].pmids` is structured array | inspection | Parsing layer adapts |

**Phase 0 deliverable:** `docs/plans/oncokb_api_evidence.md` — table with results + sanitized sample responses as reference fixtures.

---

## 4. Variant normalization spec

Patient profiles carry variants in many formats. Normalize to OncoKB-canonical short form.

### `engine/oncokb_extract.normalize_variant(raw, gene) -> Optional[NormalizedVariant]`

Rules:
1. **HGVS-p 3-letter → short:** `p.Val600Glu` → `V600E` via amino-acid table
2. **HGVS-c → ⛔ skip** (no transcript-mapping; could resolve to wrong AA)
3. **Exon-deletion unstructured → skip;** structured `del E746_A750` → pass through
4. **Fusion → skip in MVP** (out-of-scope per data_scope.md)
5. **Boolean flag (`tp53_mutation: true`) → skip** (no specific variant)
6. Cache normalization map; pure function; deterministic

### Test corpus (`tests/test_oncokb_variant_normalize.py`)

≥30 scenarios from real examples: BRAF V600E, EGFR L858R, EGFR T790M, EGFR Exon19Del, KRAS G12C, KRAS G12D, BRCA1 c.5266dupC (skip), TP53 R175H, MYD88 L265P, NPM1 W288fs, FLT3-ITD (skip in MVP), ALK rearrangement (skip).

---

## 5. OncoTree mapping (3-tier)

### Tier 1 — explicit field

`Disease.oncotree_code: Optional[str]` added to schema. Populate all 50 existing diseases (one PR). New Diseases: schema validator warns if missing.

### Tier 2 — fallback table

`engine/oncotree_fallback.py` hard-codes ICD-10 → OncoTree top-level mapping (e.g. `C34.*` → `LUNG`).

### Tier 3 — pan-tumor query

OncoKB accepts queries without `tumorType`. Falls back to pan-tumor evidence; render shows warning badge per Q4.

### Coverage report

`scripts/oncokb_coverage_report.py` runs in CI as warning. Reports: explicit code? fallback resolves? hint coverage on biomarkers?

---

## 6. Resistance-conflict policy (T3 mitigation)

### `engine/oncokb_conflict.py`

```python
def detect_resistance_conflicts(
    tracks: list[PlanTrack],
    oncokb_layer: OncoKBLayer,
) -> list[ResistanceConflict]:
    """Pure. Returns (track_id, drug, oncokb_evidence) where
    a recommended drug appears in OncoKB R1 OR R2 evidence
    for one of the patient's biomarkers."""
```

### Surface behavior

- **Inline in track-card:** banner above regimen
  - R1: red `🛑 OncoKB R1: резистентність {drug} для {gene} {variant}. Перегляньте перед призначенням.`
  - R2: amber `⚠ OncoKB R2: preclinical resistance signal — {drug}/{gene} {variant}.`
- **OncoKB section:** dedicated "Resistance conflicts detected" block at top
- **Provenance:** `ResistanceConflictDetected` event in `Plan.provenance_graph`
- **MDT trigger:** `molecular_geneticist` added to `MDTOrchestrationResult.required_roles` with reason. Priority: R1 high, R2 medium.

---

## 7. Provenance & audit

### `external_kb_consulted` ProvenanceEvent

```python
ProvenanceEvent(
    event_type="external_kb_consulted",
    target_type="oncokb_query",
    target_id=f"oncokb:{gene}:{variant}:{oncotree_code}",
    actor="oncokb_proxy",
    timestamp=...,
    metadata={
        "oncokb_data_version": "v4.21",
        "queried_at_iso": "2026-04-26T14:23:11Z",
        "cache_status": "miss",
        "result_count": 3,
        "highest_level": "3A",
        "oncokb_url": "https://www.oncokb.org/gene/BRAF/V600E",
        "levels_filtered_out": ["1", "2"],
        "pmid_count_total": 12,
        "fda_approved_count": 1,
    }
)
```

### Schema migration

`provenance.py` Literal enums extend `event_type` += `"external_kb_consulted"` and `target_type` += `"oncokb_query"`. Backward compatible.

### revise_plan version drift (Q7)

When previous and current `oncokb_data_version` differ → emit `Modified` event with `reason="external_kb_version_drift"` referencing both versions.

---

## 8. Dual-client architecture

| Runtime | HTTP stack | OncoKB call path |
|---------|-----------|------------------|
| Pyodide (try.html) | `pyodide.http.pyfetch` (JS bridge) | → proxy |
| CLI / pytest / Cloud | `httpx.AsyncClient` | → proxy |
| `scripts/build_site.py` (build-time) | `httpx` sync | → proxy (for pre-render of `docs/cases/`) |

### Protocol

```python
class OncoKBClient(Protocol):
    async def lookup(self, query) -> Result | Error: ...
    async def batch_lookup(self, queries) -> list[Result | Error]: ...

class HttpxOncoKBClient(OncoKBClient): ...    # CLI/Cloud
class PyodideOncoKBClient(OncoKBClient): ...  # browser
class NullOncoKBClient(OncoKBClient): ...     # default — all errors
class StubOncoKBClient(OncoKBClient): ...     # tests — fixture-driven
```

### Pyodide quirks

- `pyfetch` no native `timeout` → wrap with `asyncio.wait_for`
- Background fetch may not complete if tab sleeps → guard "if render started, skip"

---

## 9. Caching (multi-tier, hardened)

| Layer | Storage | TTL | Scope |
|-------|---------|-----|-------|
| L1 | Proxy in-memory LRU | 7d | per-instance |
| L0 | Engine in-memory dict per `generate_plan` call | request lifetime | single Plan |

### Negative caching

OncoKB returns 0 therapeutic options → cache the empty result (7d TTL, `is_negative: true` for observability).

### Singleflight

Concurrent identical keys → 1 upstream call, others wait. `asyncio.Lock` keyed by tuple.

### Cache poisoning prevention

Only HTTP 200 → cache. 4xx (incl. 401/403/429) → never. 5xx → never + circuit breaker increment.

### Circuit breaker

- 5 consecutive 5xx in 60s → open 5min
- Open → all `batch_lookup` calls return errors without upstream contact
- Half-open after 5min → 1 probe → close on OK

---

## 10. Observability + SLOs

### Metrics

- `oncokb_proxy.requests_total{status,cache}` (counter)
- `oncokb_proxy.upstream_latency_ms` (histogram)
- `oncokb_proxy.cache_size` (gauge)
- `oncokb_proxy.upstream_errors_total{code}` (counter)
- `oncokb_proxy.daily_quota_remaining` (gauge)

### SLOs

- p95 lookup latency (cache hit) ≤ 50ms
- p95 lookup latency (cache miss) ≤ 1500ms
- Proxy availability ≥ 99% / 30d (excl. upstream)
- Cache hit ratio ≥ 80% after 24h warmup

### Alerts

- Quota >80%/day → email
- 5xx rate >5% / 5min → email
- Cache size = 0 on warm instance >1h → investigate
- `oncokb_data_version` unchanged >120d → manual check

---

## 11. Schema migrations + governance

### PROPOSAL §18 (new in KNOWLEDGE_SCHEMA_SPECIFICATION.md)

Adds:
- `Biomarker.oncokb_lookup: Optional[OncoKBLookupHint]`
- `Disease.oncotree_code: Optional[str]` (Optional in MVP, required next minor)
- `PlanResult.oncokb_layer: Optional[OncoKBLayer]`
- `OncoKBLayer` dataclass spec
- ProvenanceEvent enum extensions

### Migration PRs (independently mergeable)

- **PR-A:** schema fields (Pydantic + spec)
- **PR-B:** 50 disease YAMLs with `oncotree_code`
- **PR-C:** ~20 actionable biomarkers with `oncokb_lookup` hints
- **PR-D:** provenance enum extension

### CHARTER cross-reference

§8.3 footnote: "OncoKB is the first external KB integrated via surface-only pattern. Reference: `services/oncokb_proxy/` + `engine/oncokb_*.py`. Re-review trigger if another external KB proposes routing-impact."

### Re-review triggers (in `services/oncokb_proxy/README.md`)

- Data scope expansion (Dx/Px, structural variants, gene-level)
- Caching strategy change
- Token handling change
- License terms change
- CHARTER §2 posture shift

---

## 12. Test taxonomy

### Unit (mocked)
- Variant normalization: ≥30 cases
- OncoTree resolution: tier 1/2/3
- Conflict detector: pure-function tests
- LRU cache: TTL, eviction, singleflight
- Circuit breaker: state transitions

### Integration (mocked httpx)
- Proxy `/lookup`: happy / 401 / 502 / 429 / timeout
- Engine `generate_plan(oncokb_enabled=True)` with `StubOncoKBClient`
- Engine with `NullOncoKBClient` → fail-open

### Contract (recorded fixtures)
- `tests/fixtures/oncokb_responses/` — sanitized JSON snapshots for 12 canonical variants
- `pytest --update-fixtures` flag for manual refresh (never CI)
- CI uses fixtures only

### Snapshot
- HCP HTML render with/without OncoKB → golden files
- Patient HTML → assert "oncokb" not in output (case-insensitive)

### Property-based (hypothesis)
- `normalize_variant` idempotent: `normalize(normalize(x)) == normalize(x)`

### Architectural invariants
- Import-graph: `engine/track_builder.py` does not import `engine/oncokb_*`
- Secret-leak grep: no `Bearer\s+\w+` in test artifacts

---

## 13. Phased rollout — explicit gates

| Phase | Scope | Entry gate | Exit gate | Rollback |
|-------|-------|-----------|-----------|----------|
| **0** API verification | Phase 0 doc | — | All A1–A11 verified or STOP | n/a |
| **1a** Proxy harden | Code only | 0 done | Tests green, scrub middleware reviewed | Revert PR |
| **1b** Proxy deploy (no consumer) | Cloud Run live | 1a merged | `/healthz` green, smoke OK, p95 <1500ms | `gcloud run services delete` |
| **2** Schema PRs A–D | KB only | 1b green | KB validator clean, coverage report attached | Revert PR |
| **3a** Variant normalizer | Pure code | 2 done | 30+ tests green | Revert PR |
| **3b** Engine wiring (default OFF) | Code | 3a done | Architectural invariants green, AC-1..AC-7 pass | Revert PR |
| **4** Render (HCP only) | Code | 3b done | Patient-mode regex grep green, snapshots green, bundle ≤1.5MB | Revert PR |
| **5a** Internal — local CLI | Manual | 4 done | 5 ref patients render OK, manual review | Empty `--oncokb-proxy=` |
| **5b** Pre-render 1 case | `docs/cases/cll_high_risk.html` | 5a + clinical HTML review | Static HTML reviewed and merged | Revert build_site.py change |
| **5c** Pre-render all HCP cases | `docs/cases/*` | 5b stable 7d | Build cache hit ≥80%, 0 build failures | Revert build_site.py |
| **5d** Live `try.html` opt-in | Pyodide reads `window.OPENONCO_ONCOKB_PROXY` | 5c stable 7d | 7d soak with real users, logs clean | Remove env var |
| **5e** Default-on in Pyodide | Default URL set | 5d soak clean | Quota stable, hit-rate stable, 0 incidents | Set env var to `""` |
| **6** Docs + handoff | Docs | 5e merged | All docs updated, roadmap `[x]` | n/a |

### Hard pause points (explicit user OK required)

- Before **1b** (live deploy)
- Before **5d** (real users see new section)
- Before **5e** (default-on)

---

## 14. Acceptance criteria (gate per phase)

| # | Criterion | Test |
|---|-----------|------|
| AC-1 | `_build_tracks` does not accept oncokb params | Unit + import-graph |
| AC-2 | Engine fail-open on OncoKB unreachable | Integration with NullClient |
| AC-3 | Patient-mode HTML never contains "oncokb" (case-insensitive) | Snapshot + regex grep |
| AC-4 | Token absent from logs / responses / Pyodide bundle | grep CI step |
| AC-5 | CORS closed to non-production origins | Unit on parsing |
| AC-6 | Bundle size ≤1.5MB | CI size-check |
| AC-7 | Default-OFF: `generate_plan(patient)` no-kwargs → 0 network calls | Mock httpx, call_count=0 |
| AC-8 | Attribution in section header, not footnote | Snapshot |
| AC-9 | Resistance conflict surfaced inline + provenance event recorded | Integration |
| AC-10 | Negative cache populated | Unit |
| AC-11 | Circuit breaker opens after 5 consecutive 5xx | Unit |
| AC-12 | Variant normalization 30+ canonical inputs | Unit corpus |
| AC-13 | OncoTree fallback covers 50 existing diseases | Coverage report |
| AC-14 | ProvenanceEvent `external_kb_consulted` for every query | Integration |
| AC-15 | MDT triggers `molecular_geneticist` on resistance conflict | Integration |
| AC-16 | Levels 1/2 never appear in OncoKB section | Snapshot (BRAF V600E plan → 0 rows) |
| AC-17 | Cross-biomarker drug-overlap badge when 1 drug ∈ ≥2 rows | Integration |
| AC-18 | revise_plan emits `Modified` event on `oncokb_data_version` drift | Integration |
| AC-19 | PMID links: valid PubMed URL, target=_blank, rel=noopener | Snapshot |
| AC-20 | FDA badge format: `FDA-approved ({drug}, {year})` | Snapshot |

---

## 15. Explicit no-go

- ❌ OncoKB content stored in KB YAML
- ❌ Engine routing depends on OncoKB
- ❌ OncoKB visible in patient mode
- ❌ Live OncoKB calls in CI
- ❌ Token in repo / Pyodide bundle
- ❌ Redis / Memorystore cache in MVP
- ❌ Auto-promote 3A/3B → engine track
- ❌ Diagnostic / Prognostic levels (Dx/Px)
- ❌ Structural variants / fusions in MVP
- ❌ Direct browser → oncokb.org (CSP forbids)
- ❌ Polling fresh data — on-demand only
- ❌ Caching 4xx responses
- ❌ Retry on 401/403 (signals token issue, not transient)
- ❌ Logging request body (key fields in structured log only)
- ❌ Showing Levels 1/2 (Q1 — engine already covers)

---

## 16. Estimate

| Phase | Effort | Calendar | Risk |
|-------|--------|----------|------|
| 0 API verification | 1d | 1d | 0 |
| 1a Proxy harden | 1d | 1d | low |
| 1b Proxy deploy | ½d | 1d | low (gated) |
| 2 Schema migrations | 1d | 1d | 0 |
| 3a Variant normalizer | 1.5d | 2d | 0 (pure) |
| 3b Engine wiring | 2d | 3d | medium |
| 4 Render | 2d (incl. cross-biomarker) | 3d | medium |
| 5a–c Internal + pre-render | 1d code | 1–2 weeks soak | low |
| 5d–e Live rollout | ½d | 2 weeks soak | medium (gated) |
| 6 Docs | 1d | 1d | 0 |
| **Total** | **~11 working days code** | **~5–6 weeks calendar** | |

---

## 17. Dependencies + blockers

- **Hard:** OncoKB Academic token still valid (verify Phase 0)
- **Hard:** Cloud Run access for current GCP project (already used per `oncokb_source_classification.md`)
- **Soft:** None — Q1–Q8 all answered, conservative defaults locked in

---

## 18. Disaster recovery (incident runbook)

| Scenario | Detection | Response |
|----------|-----------|----------|
| Proxy 5xx rate spike | Cloud Logging alert | Check upstream OncoKB status; if upstream healthy → roll back last proxy revision |
| Token revoked / expired | 401 from upstream | Rotate token in Secret Manager; restart Cloud Run revision (cache flushes) |
| Quota exhausted | `daily_quota_remaining` alert | Set `ONCOKB_INTEGRATION_ENABLED=0` env var on Cloud Run; render falls back to no-OncoKB-section |
| Cache poisoning suspected | Anomalous results reported by clinician | Restart Cloud Run revision (RAM cache flushes); investigate via structured logs |
| OncoKB API breaking change | Contract test fails on `--update-fixtures` | Pin to Phase 0 verified shape; update parsing layer; release patch |
| Pyodide can't reach proxy | Browser console errors | Check CORS headers; add origin to `ONCOKB_PROXY_CORS_ORIGINS` |

### Master kill-switch

Single env-var: `ONCOKB_INTEGRATION_ENABLED=0` on Cloud Run → proxy returns 503 → engine fail-opens → all Plans render without OncoKB section. Documented in proxy README.
