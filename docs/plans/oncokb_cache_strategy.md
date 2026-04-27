# ⚠️ SUPERSEDED — 2026-04-27

This OncoKB-era decision-record is preserved for historical reference.
OncoKB integration was rejected after Terms-of-Service audit found a fundamental
conflict with CHARTER §2 (free public clinical decision-support). See
`docs/reviews/oncokb-public-civic-coverage-2026-04-27.md` and
`docs/plans/civic_integration_v1.md`.

---

# OncoKB · Cache strategy (deferred decision, parked 2026-04-25)

**Status:** parked default — implemented in Phase 10 scaffold.

## Decision

The OncoKB proxy uses an **in-memory LRU cache** with **7-day TTL**:

- `ONCOKB_CACHE_MAX_ENTRIES`: 4096 (≈ 200KB at typical entry size)
- `ONCOKB_CACHE_TTL_SECONDS`: 604800 (= 7 days)
- Cache key: `(gene_uppercase, variant, oncotree_code, tumor_type)`
- Eviction: LRU when over `MAX_ENTRIES`; TTL-driven on read

Per Cloud Run instance — i.e. each warm instance maintains its own LRU.
Cold-starts hit the cache empty; a single warm instance services most
traffic since openonco.org has low concurrent load.

## Why 7 days

OncoKB's underlying knowledge updates **roughly quarterly** (per their
release notes). Within a 7-day window, the probability of a meaningful
content change for a given (gene, variant, tumor) triplet is near-zero,
so cache freshness is not the limiting factor — bandwidth + token
quota is.

A 7-day TTL gives:
- ≥99% cache hit rate after warm-up (most patients have 1-3 biomarkers
  drawn from a small set of genes — KRAS, EGFR, BRAF, TP53, BRCA1/2,
  MYD88, etc.).
- ≤1 OncoKB call per gene/variant/tumor per week per Cloud Run instance.
- Bounded staleness — clinically meaningful changes propagate within 7d
  of next user query.

## Why in-memory (not Redis / Memcached / file)

- **Simplicity.** No additional GCP service, no auth, no monitoring
  surface. Single Python dict + `OrderedDict` is ~30 lines.
- **No persistence cost.** OncoKB Academic terms forbid creating a
  redistributable snapshot; in-memory cache reaches GC eventually,
  matches "no on-disk snapshot" claim in `src_oncokb.yaml`.
- **Cloud Run model fits.** Cloud Run scales to zero on idle —
  in-memory cache is naturally bounded to instance lifetime, no
  cleanup needed.

## Revisit triggers

Move to **Redis (or Memorystore)** if:
- We scale to >5 simultaneous Cloud Run instances and cache miss rate
  becomes load-bearing on OncoKB quota.
- We want cache to survive instance recycling (cold-start latency
  becomes user-visible).

Move to **persistent file cache** never — that crosses the line from
"referenced" to "hosted snapshot" per OncoKB Academic terms (see
`src_oncokb.yaml` `legal_review`).

## Operational notes

- `/healthz` reports `cache_size` so we can monitor warmup. If a
  Cloud Run instance has been alive for hours but cache is small,
  user traffic likely cold — investigate.
- Cache cannot be flushed via API (intentional — clinicians shouldn't
  trigger OncoKB requery on whim). Restart the Cloud Run revision to
  flush.
