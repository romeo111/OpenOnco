# ⚠️ SUPERSEDED — 2026-04-27

This OncoKB-era decision-record is preserved for historical reference.
OncoKB integration was rejected after Terms-of-Service audit found a fundamental
conflict with CHARTER §2 (free public clinical decision-support). See
`docs/reviews/oncokb-public-civic-coverage-2026-04-27.md` and
`docs/plans/civic_integration_v1.md`.

---

# OncoKB · Source classification (recorded 2026-04-25)

**Status:** decision recorded — Source entity created at
`knowledge_base/hosted/content/sources/src_oncokb.yaml` during Phase 10.

## Decision

`SRC-ONCOKB` is registered with:

- `hosting_mode: referenced`
- `commercial_use_allowed: false`
- `redistribution_allowed: false`
- `legal_review.status: pending`

## Why "referenced", not "hosted"

OncoKB Academic Terms forbid mirroring / redistribution. Even with
the proxy architecture (in-memory cache, no persistent snapshot),
we technically only *forward* requests on behalf of clinicians; we
do not maintain a copy. This is the cleanest mapping to the
SOURCE_INGESTION_SPEC §1.4 default ("referenced is default unless
H1–H5 hosting justification applies").

H1–H5 hosting justifications considered and rejected:
- **H1** (high availability needed) — OncoKB API is reliable enough.
- **H2** (offline use) — irrelevant; OpenOnco runs in-browser.
- **H3** (license requires copy) — false; license forbids copy.
- **H4** (high query volume cost) — proxy LRU mitigates.
- **H5** (provenance integrity) — direct API call gives newer data
  than any snapshot would.

None apply. `referenced` it is.

## Proxy architecture as license-compliant

The decision tree of "are we hosting?" comes down to:
- Do we store OncoKB content on disk in a way that survives instance
  restart? **No** (in-memory LRU only).
- Do we redistribute OncoKB content to third parties? **No** (only the
  user who sent the patient profile sees the response).
- Do we attribute OncoKB on every render? **Yes** (per `attribution.text`).
- Do we use it commercially? **No** (CHARTER §2 binds us non-commercial).

This is the same legal posture as a clinician using the OncoKB website
directly — we just remove the friction of the clinician having to
copy-paste each gene-variant.

## Pending legal review

Before Cloud Run deployment with `ONCOKB_LIVE=1`:

1. Counsel reviews `src_oncokb.yaml` + `services/oncokb_proxy/README.md`
   against current OncoKB Academic Terms text.
2. Confirms the proxy architecture (server-side token, in-memory cache,
   per-request attribution) is consistent with academic-license
   "research use" interpretation.
3. Sets `legal_review.status: reviewed` + signed reviewer name + date.

If counsel disagrees: fall back to **Option B from earlier discussion**
— show only an OncoKB **link** in render output, no API call. That's
unambiguously fair use and requires zero infrastructure.
