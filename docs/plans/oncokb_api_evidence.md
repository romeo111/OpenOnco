# OncoKB API · Evidence registry (Phase 0 deliverable)

**Status:** 🔴 **BLOCKED — needs real OncoKB Academic-tier token**

Per `oncokb_integration_safe_rollout_v3.md` §3, Phase 0 entry gate for
all subsequent phases requires verification of A1–A11 with curl against
the real OncoKB API. Without a token we cannot proceed past assumption
to fact for the production-shape integration.

This document is the skeleton — fill the Result columns once the token
is in Secret Manager (or available locally for one-time verification).

---

## Procedure

```bash
# Set once
export ONCOKB_TOKEN='<academic-tier-token>'
export H="Authorization: Bearer ${ONCOKB_TOKEN}"
export H_ACCEPT="Accept: application/json"
export BASE="https://www.oncokb.org/api/v1"

# Save sanitized response samples for fixtures
mkdir -p tests/fixtures/oncokb_responses
```

---

## A1. Endpoint shape

**Hypothesis:** `GET /api/v1/annotate/mutations/byProteinChange?hugoSymbol=&alteration=&tumorType=`

**Verify:**
```bash
curl -s -H "$H" -H "$H_ACCEPT" \
  "$BASE/annotate/mutations/byProteinChange?hugoSymbol=BRAF&alteration=V600E&tumorType=MEL" \
  | tee tests/fixtures/oncokb_responses/braf_v600e_mel.json | head -50
```

**Result:** _(pending)_

**Action if false:** rewrite `services/oncokb_proxy/app.py:_call_oncokb` URL composition.

---

## A2. Auth scheme

**Hypothesis:** `Authorization: Bearer {token}`

**Verify:**
```bash
# Should return 200
curl -s -o /dev/null -w "%{http_code}\n" -H "$H" "$BASE/info"
# Should return 401
curl -s -o /dev/null -w "%{http_code}\n" "$BASE/info"
```

**Result:** _(pending)_

**Action if false:** rewrite auth header in `_call_oncokb`.

---

## A3. Response `treatments[].level` format

**Hypothesis:** values like `LEVEL_1`, `LEVEL_2`, `LEVEL_3A`, `LEVEL_3B`, `LEVEL_4`, `LEVEL_R1`, `LEVEL_R2`

**Verify:** inspect `braf_v600e_mel.json` from A1 — pull all unique `treatments[].level` values across 3 representative queries (BRAF V600E in MEL, EGFR T790M in NSCLC, BRCA1 mutation in OV).

**Result:** _(pending)_

**Action if false:** rewrite parsing in `_call_oncokb` (`.replace("LEVEL_", "")`).

---

## A3-bis. FDA-approval field

**Hypothesis:** `treatments[].fdaApproved` exists as boolean OR there is `treatments[].approvedIndications` with year/agency.

**Verify:** grep response for `fdaApproved` or `approved`.

**Result:** _(pending)_

**Action if false:** Q8 FDA badge (per v3 plan §2) needs alternative source — likely manual `fda_approval` field on Drug schema, populated from openFDA client.

---

## A4. `dataVersion` field

**Hypothesis:** top-level response field e.g. `"dataVersion": "v4.21"`.

**Verify:**
```bash
curl -s -H "$H" "$BASE/info" | jq '.dataVersion // .ncitVersion'
```

**Result:** _(pending)_

**Action if false:** provenance `oncokb_data_version` metadata gap — fall back to query-time-only timestamp.

---

## A5. Academic-tier quota

**Hypothesis:** ~1000 requests/day per token (educated guess).

**Verify:** OncoKB account dashboard at https://www.oncokb.org/account — exact daily/monthly cap.

**Result:** _(pending — manual UI check)_

**Action if false:** adjust `MAX_INSTANCES`, rate-limit middleware budget, alert thresholds (currently 80% triggers).

---

## A6. Variant string formats accepted

**Hypothesis:** OncoKB accepts `V600E` short, `p.V600E` HGVS-p with prefix, AND `p.Val600Glu` 3-letter.

**Verify:**
```bash
for v in "V600E" "p.V600E" "p.Val600Glu"; do
  echo "=== $v ==="
  curl -s -H "$H" "$BASE/annotate/mutations/byProteinChange?hugoSymbol=BRAF&alteration=$v&tumorType=MEL" \
    | jq '.treatments | length'
done
```

**Result:** _(pending)_

**Action if false:** beef up `engine/oncokb_extract.normalize_variant` to canonicalize to whichever format OncoKB accepts. Tests in `tests/test_oncokb_variant_normalize.py` pin to verified format.

---

## A7. tumorType param key

**Hypothesis:** URL param key is `tumorType` (camelCase), not `oncoTreeCode`.

**Verify:** A1 sample already uses `tumorType=MEL` — check 200 OK + non-empty `treatments`.

**Result:** _(pending)_

**Action if false:** swap key in `_call_oncokb` params dict.

---

## A8. Structural-variant endpoint

**Hypothesis:** Fusions / structural variants need a separate endpoint (e.g. `/annotate/structuralVariants/...`) — confirms MVP out-of-scope decision per `oncokb_data_scope.md`.

**Verify:** read https://docs.oncokb.org/web-api or curl `/annotate/copyNumberAlterations` to confirm separate path exists.

**Result:** _(pending)_

**Action if false:** if fusions are returned by the same `/byProteinChange` endpoint, scope decision still holds (we skip them in normalize_variant) but worth documenting.

---

## A9. Rate-limit response headers

**Hypothesis:** OncoKB returns `X-RateLimit-Remaining` / `X-RateLimit-Reset` headers we can surface in our own `daily_quota_remaining` metric.

**Verify:**
```bash
curl -sI -H "$H" "$BASE/info" | grep -i ratelimit
```

**Result:** _(pending)_

**Action if false:** use counter-based quota tracking in our middleware (we count each upstream call ourselves; daily reset at UTC midnight).

---

## A10. Token rotation cadence

**Hypothesis:** Academic-tier tokens are issued manually with no expiry, rotated by user request.

**Verify:** OncoKB account UI — look for token-expiry or rotation policy.

**Result:** _(pending — manual UI check)_

**Action if false:** if tokens auto-expire, add Cloud Scheduler job to alert N days before expiry; document rotation runbook in `services/oncokb_proxy/README.md`.

---

## A11. PMID array shape

**Hypothesis:** `treatments[].pmids` is a flat array of strings.

**Verify:** inspect any treatment with citations from A1 sample.

**Result:** _(pending)_

**Action if false:** parsing layer adapts (currently `[str(p) for p in tx.get("pmids", []) or []]`).

---

## Sample responses to capture

For variant-normalization test corpus and contract-test fixtures, save sanitized JSON for all 12 canonical cases (one curl per row, BRAF V600E + 11 others — see `oncokb_integration_safe_rollout_v3.md` §4 test corpus).

| # | Gene | Variant | TumorType | Filename | Captured? |
|---|------|---------|-----------|----------|-----------|
| 1 | BRAF | V600E | MEL | `braf_v600e_mel.json` | ☐ |
| 2 | BRAF | V600E | COADREAD | `braf_v600e_crc.json` | ☐ |
| 3 | EGFR | L858R | NSCLC | `egfr_l858r_nsclc.json` | ☐ |
| 4 | EGFR | T790M | NSCLC | `egfr_t790m_nsclc.json` | ☐ |
| 5 | EGFR | Exon 19 deletion | NSCLC | `egfr_ex19del_nsclc.json` | ☐ |
| 6 | KRAS | G12C | NSCLC | `kras_g12c_nsclc.json` | ☐ |
| 7 | KRAS | G12C | COADREAD | `kras_g12c_crc.json` | ☐ |
| 8 | KRAS | G12D | PAAD | `kras_g12d_pdac.json` | ☐ |
| 9 | TP53 | R175H | _(no tumor)_ | `tp53_r175h_pan.json` | ☐ |
| 10 | MYD88 | L265P | LYMPH | `myd88_l265p_lymph.json` | ☐ |
| 11 | NPM1 | W288fs | AML | `npm1_w288fs_aml.json` | ☐ |
| 12 | BRCA1 | _(any pathogenic)_ | OV | `brca1_path_ov.json` | ☐ |

**Sanitization rule:** before commit, strip any `responseId` / `requestId` / token echoes and any patient-correlatable identifiers (there shouldn't be any but verify).

---

## Exit criteria

Phase 0 complete when:
- All A1–A11 rows have a Result.
- All 12 sample responses captured in `tests/fixtures/oncokb_responses/`.
- Any "Action if false" triggered → corresponding code/doc updated and re-verified.
- This document committed on `feat/oncokb-wiring`.

Then Phase 1a-onwards is unblocked.
