# ⚠️ SUPERSEDED — 2026-04-27

This OncoKB-era decision-record is preserved for historical reference.
OncoKB integration was rejected after Terms-of-Service audit found a fundamental
conflict with CHARTER §2 (free public clinical decision-support). See
`docs/reviews/oncokb-public-civic-coverage-2026-04-27.md` and
`docs/plans/civic_integration_v1.md`.

---

# OncoKB API · Evidence registry (Phase 0 deliverable)

**Status:** 🟡 **MOCK-MODE PROVISIONAL** (2026-04-27) — derived from public
docs (api.oncokb.org/oncokb-website/api, faq.oncokb.org/technical,
github.com/oncokb/oncokb-annotator). Clearly marked unverified rows
need real-token curl confirmation before Phase 1b production deploy.

This doc unblocks downstream coding (Phases 3b/4 + follow-ups) by
locking the response shape we'll parse against. If real-token
verification reveals divergence, we update the parsing layer + these
notes together — no schema migration risk because the proxy already
isolates parsing from the engine.

Public-doc sources used:
- [OncoKB API Reference](https://api.oncokb.org/oncokb-website/api)
- [OncoKB Technical FAQ](https://faq.oncokb.org/technical)
- [oncokb-annotator AnnotatorCore.py master](https://github.com/oncokb/oncokb-annotator/blob/master/AnnotatorCore.py)
- [waldronlab/oncoKBData docs](https://waldronlab.io/oncoKBData/articles/oncoKBData.html)

---

## Procedure (when real token is available)

```bash
# Set once
export ONCOKB_TOKEN='<academic-tier-token>'
export H="Authorization: Bearer ${ONCOKB_TOKEN}"
export H_ACCEPT="Accept: application/json"
export BASE="https://www.oncokb.org/api/v1"

mkdir -p tests/fixtures/oncokb_responses
```

Re-run each verification below; replace `Result (provisional)` rows
with `Result (verified YYYY-MM-DD)`. Promote the doc status banner
from 🟡 PROVISIONAL → ✅ VERIFIED when all A1–A11 have verified rows.

---

## A1. Endpoint shape

**Hypothesis:** `GET /api/v1/annotate/mutations/byProteinChange?hugoSymbol=&alteration=&tumorType=`

**Result (provisional):** ✅ confirmed by public docs. Endpoint exists
at `/annotate/mutations/byProteinChange` with documented query params:
`referenceGenome` (GRCh37|GRCh38), `hugoSymbol`, `entrezGeneId`,
`alteration`, `consequence`, `proteinStart`, `proteinEnd`, `tumorType`.

**Action if false:** rewrite `services/oncokb_proxy/app.py:_call_oncokb`
URL composition.

---

## A2. Auth scheme

**Hypothesis:** `Authorization: Bearer {token}`

**Result (provisional):** ✅ confirmed. Public API reference lists
header format `Authorization: Bearer [your personal token]`.

**Action if false:** rewrite auth header in `_call_oncokb`. Low risk.

---

## A3. Response `treatments[].level` format

**Hypothesis:** values like `LEVEL_1`, `LEVEL_2`, `LEVEL_3A`, `LEVEL_3B`,
`LEVEL_4`, `LEVEL_R1`, `LEVEL_R2`.

**Result (provisional):** ✅ confirmed. Web-search hits multiple sources
quoting the level hierarchy as `LEVEL_R1 > LEVEL_1 > LEVEL_2 > LEVEL_3A
> LEVEL_3B > LEVEL_4 > LEVEL_R2`. Our existing parser strips `LEVEL_`
prefix → 200 OK against the spec.

**Action if false:** rewrite parsing in `_call_oncokb`
(`.replace("LEVEL_", "")`). Already in code; trivial swap.

---

## A3-bis. FDA-approval field (relevant to locked Q8)

**Hypothesis:** `treatments[].fdaApproved` exists as boolean.

**Result (provisional):** 🔴 **DOES NOT EXIST in OncoKB response.**
The oncokb-annotator code (line 1534-1544) accesses only:
`treatment['level']`, `treatment['drugs']` (with `.drugName`),
`treatment['pmids']`, `treatment['abstracts']`. No `fdaApproved`.

**Decision:** Q8 FDA badge needs **alternative data source**. Options:
1. Look up Drug entity in our own KB — we already have
   `Drug.regulatory_status.fda` (approved boolean + indications)
2. Use openFDA client (already in `knowledge_base/clients/openfda_client.py`)
3. Drop the badge and replace with "FDA-recognized via OncoKB Level 1/2"
   (since Level 1/2 by definition imply FDA-recognized — but we filter
   those out per Q1!)

**Recommended:** option 1 (cross-reference Drug entity). Render-side
work; engine wiring already accepts the field as Optional.

**Action item:** update `render_oncokb._format_fda_badge` to lookup
Drug ID by name in `plan_result.kb_resolved["drugs"]`. Tracked as
**§ NEW Phase 4.1 follow-up** below.

---

## A4. `dataVersion` field

**Hypothesis:** top-level response field e.g. `"dataVersion": "v4.21"`.

**Result (provisional):** ✅ confirmed. Documented response shape includes
`dataVersion` at top level — example value `"v2.1"` shown in old docs;
current data version is in v4.x range (release notes June 2024+).

**Action if false:** provenance metadata gap; fall back to query-time
timestamp only.

---

## A5. Academic-tier quota

**Hypothesis:** ~1000 requests/day per token.

**Result (provisional):** 🔴 **NOT documented publicly.** OncoKB FAQ
does not specify rate limits or per-day caps. Discovery at runtime
only — first 429 response will reveal the actual cap. Mitigation
already in place: proxy rate-limit middleware (60/min default;
bounded), in-memory LRU 7-day TTL minimizes upstream calls.

**Action if false:** adjust proxy `MAX_INSTANCES`, rate-limit budget,
alert thresholds.

---

## A6. Variant string formats accepted

**Hypothesis:** OncoKB accepts `V600E` short, `p.V600E`, AND `p.Val600Glu`.

**Result (provisional):** ✅ short HGVS-p (`V600E`) confirmed by public
docs (parameter described as "protein change", example `V600E`).
Whether `p.V600E` and 3-letter `p.Val600Glu` are also accepted is
**not explicitly documented** — our normalizer canonicalizes everything
to short form, so we'll always send short. Safe.

**Action if false:** beef up `engine/oncokb_extract.normalize_variant`
to whichever format OncoKB accepts. Already short-form-only — no risk.

---

## A7. tumorType param key

**Hypothesis:** URL param key is `tumorType` (camelCase), not `oncoTreeCode`.

**Result (provisional):** ✅ confirmed. Public docs list parameter
literally as `tumorType` accepting OncoTree name OR code. Our proxy
already uses this name.

---

## A8. Structural-variant endpoint

**Hypothesis:** Fusions / structural variants need a separate endpoint.

**Result (provisional):** ✅ confirmed. Separate endpoints exist:
- `/annotate/copyNumberAlterations` — params: `copyNameAlterationType`
  (AMPLIFICATION|DELETION|GAIN|LOSS), `hugoSymbol`, `entrezGeneId`,
  `tumorType`
- `/annotate/structuralVariants` — params: `structuralVariantType`
  (DELETION|FUSION|...), `hugoSymbolA`/`hugoSymbolB`,
  `isFunctionalFusion` (boolean), `tumorType`

Confirms our MVP scope decision (skip fusions / CNAs in normalize_variant
per `oncokb_data_scope.md`).

---

## A9. Rate-limit response headers

**Hypothesis:** `X-RateLimit-Remaining` / `X-RateLimit-Reset` headers.

**Result (provisional):** 🔴 **NOT documented publicly.** Our proxy
metrics will use a counter-based approximation: count each upstream
call, daily reset at UTC midnight. If verified-via-curl reveals
rate-limit headers, proxy can read them directly (cleaner).

---

## A10. Token rotation cadence

**Hypothesis:** Academic-tier tokens are issued manually with no expiry.

**Result (verified — public docs):** 🔵 **6-month auto-renewal cycle.**
"Your OncoKB API token will expire after 6 months. Before it expires,
we will send an email to your registered email address to verify that
it is still valid. Following verification, the token will be renewed
automatically." (faq.oncokb.org/technical)

**Action item:** add operational runbook entry — calendar reminder
30 days before token expiry; check email for renewal request.
Tracked in **§ NEW Phase 1b operational gate** below.

---

## A11. PMID array shape

**Hypothesis:** `treatments[].pmids` is a flat array of strings.

**Result (provisional):** ✅ confirmed by oncokb-annotator code (line
1540 accesses `treatment['pmids']` directly as a list). Also separate
`treatment['abstracts']` array for non-PubMed citations.

**Note:** there's also a `mutationEffect.citations.{pmids, abstracts}`
nested structure at the top level — different signal, our render layer
doesn't surface it.

---

## NEW: § Phase 4.1 follow-up — FDA badge alternative source

Locked Q8 ("Confidence display = level + PMID count + FDA-approved")
relies on `treatments[].fdaApproved` which **does not exist** in the
OncoKB response (A3-bis discovery).

**Plan:**
1. `render_oncokb._format_fda_badge` accepts an optional drug-lookup
   dict (passed through from `plan_result.kb_resolved["drugs"]`).
2. For each drug name in OncoKB's `treatments[].drugs[].drugName`,
   case-insensitive match against `Drug.names.preferred` in our KB.
3. If matched and `Drug.regulatory_status.fda.approved == True`:
   render badge with year from `Drug.regulatory_status.fda.year`.
4. If unmatched OR not approved: no badge.

Engine-side wiring: `render.py` already passes `kb_resolved.drugs` to
the OncoKB section indirectly — needs a small param-passing edit.

**Acceptance:** re-run `tests/test_oncokb_render.py::test_fda_approval_badge_renders_with_year`
with new drug-lookup signature. Adjust 1 test fixture.

**Effort:** ~30 min. Optional — doesn't block Phase 1b deploy.

---

## NEW: § Phase 1b operational gate — token rotation runbook

Per A10 (6-month cycle), add to `services/oncokb_proxy/README.md`:

```markdown
## Token rotation

OncoKB Academic-tier tokens auto-renew every 6 months upon email
verification. Operational runbook:

1. T-30 days: calendar reminder fires. Check inbox for OncoKB renewal email.
2. Verify token is still valid via OncoKB account UI.
3. Click confirmation link in renewal email → token renews automatically.
4. No code change or redeploy needed (same token string remains valid).

If renewal email is missed, token expires and proxy returns
`502: ONCOKB_LIVE=1 but ONCOKB_API_TOKEN is unset`-equivalent (401
from upstream). Recovery: log in to oncokb.org/account → request new
token → update Secret Manager (`gcloud secrets versions add oncokb-token`)
→ Cloud Run picks up new version on next request.
```

---

## Sample responses to capture (provisional fixtures)

12 synthesized fixture JSONs created at
`tests/fixtures/oncokb_responses/` (Phase 0 deliverable). Marked
**PROVISIONAL** in their headers — replace with real-curl captures
when token is available.

| # | Gene | Variant | TumorType | Filename | Status |
|---|------|---------|-----------|----------|--------|
| 1 | BRAF | V600E | MEL | `braf_v600e_mel.json` | 🟡 prov |
| 2 | BRAF | V600E | COADREAD | `braf_v600e_crc.json` | 🟡 prov |
| 3 | EGFR | L858R | NSCLC | `egfr_l858r_nsclc.json` | 🟡 prov |
| 4 | EGFR | T790M | NSCLC | `egfr_t790m_nsclc.json` | 🟡 prov |
| 5 | EGFR | Exon 19 deletion | NSCLC | `egfr_ex19del_nsclc.json` | 🟡 prov |
| 6 | KRAS | G12C | NSCLC | `kras_g12c_nsclc.json` | 🟡 prov |
| 7 | KRAS | G12C | COADREAD | `kras_g12c_crc.json` | 🟡 prov |
| 8 | KRAS | G12D | PAAD | `kras_g12d_pdac.json` | 🟡 prov |
| 9 | TP53 | R175H | _(no tumor)_ | `tp53_r175h_pan.json` | 🟡 prov |
| 10 | MYD88 | L265P | LYMPH | `myd88_l265p_lymph.json` | 🟡 prov |
| 11 | NPM1 | W288fs | AML | `npm1_w288fs_aml.json` | 🟡 prov |
| 12 | BRCA1 | _(any pathogenic)_ | OV | `brca1_path_ov.json` | 🟡 prov |

**Sanitization note:** real-curl captures must strip `responseId` /
`requestId` / token echoes before commit.

---

## Exit criteria

Phase 0 complete (status banner promotion 🟡 → ✅) when:
- All A1–A11 rows have **verified** results from real-curl runs (not provisional).
- All 12 fixtures replaced with real-token captures.
- Parsing layer adjustments (if any) merged + tests green.
- This document committed with verification dates.

Until then: 🟡 PROVISIONAL — **safe for engine development, NOT safe
for Phase 1b production deploy** without follow-up curl pass.
