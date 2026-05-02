# HEAD-check audit — source-recency-refresh-wave2-2026-05-01-024

Run: 2026-05-02T06:17:42Z
Method: `httpx.Client.head(url, follow_redirects=True, timeout=30)` with
`User-Agent: Mozilla/5.0 (compatible; OpenOnco-recency-bot)`, 3 retries
on transport error. On 403, fall back to DOI HEAD then PubMed-canonical
HEAD before declaring `unreachable.blocked`.

| ID | Primary URL | Primary | DOI | PubMed | Outcome |
|---|---|---|---|---|---|
| SRC-FIGHT-207 | (none) | - | - | - | unreachable.no_url |
| SRC-IRIS-OBRIEN-2003 | nejm.org/.../NEJMoa022457 | 403 | 403 | 403 | unreachable.blocked |
| SRC-AETHERA-MOSKOWITZ-2015 | pubmed.../25796459 | 403 | 403 | 403 | unreachable.blocked |
| SRC-ARIEL3-COLEMAN-2017 | thelancet.com/.../PIIS0140-6736(17)32440-6 | 403 | 403 | 403 | unreachable.blocked |

## Interpretation

- **403 = bot-blocking, not dead URL.** Wave-1 (#92-#121) established
  that NEJM, Elsevier, and Lancet routinely return 403 to non-browser
  HEAD requests; the canonical convention is to flag and let the
  maintainer browser-verify or bump in a follow-up.
- **PubMed normally returns 200**; this run got 403 for all three PubMed
  fallbacks, suggesting transient rate-limiting / bot detection rather
  than permanent block (see SRC-AETHERA-MOSKOWITZ-2015 — same URL
  returned 200 in wave-1 batch on 2026-04-29).
- **SRC-FIGHT-207** is an auto-stub with no URL/DOI/PMID; not a recency
  problem, a content-completion problem. Suggested follow-up chunk:
  resolve the stub.

## Files written

- `_contribution_meta.yaml`
- `task_manifest.txt` (4 IDs)
- `source_recency_audit.yaml` (issue-mandated per-source audit)
- `unreachable.yaml` (flag list, 4 rows)
- `refresh_summary.yaml` (aggregate stats)
- this file

No upsert sidecars produced — all 4 sources fell into unreachable.* per
spec. Hosted KB files are untouched.
