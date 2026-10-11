# Clinical content review workflow

CHARTER §6.1 requires two of three Clinical Co-Leads to approve changes to clinical content. This workflow records content reviews; it does not approve an individual patient's treatment plan. Software validates declared provenance, not medical credentials or the clinical truth of a review.

## Human authorization comes first

A registered `ReviewerProfile` must have human-recorded governance metadata:

- `authorization.status: approved` (the safe default is pending).
- `authorization.verified_on`: a valid, nonfuture ISO date.
- `authorization.decision_reference`: the governance decision reference.
- `authorization.identity_key`: a stable, non-sensitive key for the actual person. Multiple accounts for one person must share this key.

Only a responsible human governance process can establish these fields. Do not infer credentials from names, qualifications text or an ID without `PLACEHOLDER`; do not populate approvals with software or an LLM. Existing placeholder and unverified profiles confer no review coverage. Tests use expressly synthetic profiles in temporary directories, never production approvals.

`sign_off_scope.entity_types` explicitly lists `Indication`, `Algorithm`, `Regimen`, `RedFlag` or `BiomarkerActionability`. Empty scope is unknown, not unrestricted. `diseases_explicit` is an exact disease allow-list; otherwise declared disease categories restrict coverage. An explicit `[all]` category grants all-category scope for the declared entity types. Every disease context must be covered. Use explicit disease IDs when a coarse category is ambiguous.

## Record a review

From the repository root, after reviewing the actual content and sources:

```bash
python scripts/clinical_signoff.py approve \
  --reviewer REV-YOUR-AUTHORIZED-ID \
  --entity-id IND-ENTITY-YOU-REVIEWED \
  --rationale "Your actual review rationale" \
  --dry-run
```

Replace illustrative IDs with existing records. Remove `--dry-run` only when recording your actual decision. `--pattern` can select reviewed files relative to `knowledge_base/hosted/content/`.

The CLI writes schema-owned `reviewer_signoffs` and appends an audit event to `knowledge_base/hosted/audit/signoffs.jsonl`. Each review is pinned to the existing content revision: `last_verified` for BMA, `last_reviewed` for other supported entities. Recording a review does not change that revision date. Review timestamps must not predate the content revision or reviewer authorization.

Scope mismatches and missing revisions are always refused; `--strict` is retained for compatibility. `--force` permits a repeated affirmation of the same revision but cannot bypass authorization, scope or revision checks. Reaffirmations and aliases for one person do not count as independent reviews. A new content revision requires new reviews.

## Withdraw and inspect

```bash
python scripts/clinical_signoff.py withdraw \
  --reviewer REV-YOUR-REGISTERED-ID \
  --entity-id IND-ENTITY-ID \
  --rationale "Reason for withdrawing the recorded review"
python scripts/clinical_signoff.py list --entity-id IND-ENTITY-ID
```

Withdrawal removes the entity's recorded reviews by that reviewer and appends a withdrawal event. Historical audit events are retained. Revoking profile authorization removes current eligibility without rewriting historical events.

## Current coverage and reports

```bash
python scripts/build_signoff_dashboard.py --out build/review-status.md
python -m scripts.audit_escat_readiness --json-output build/escat-readiness.json
```

The dashboard counts current, explicitly in-scope, current-revision reviews by distinct authorized human identities. It separately reports raw retained records and historical activity. The ESCAT auditor also requires the existing clinician-authored evidence dossier and scope/applicability fields; it never assigns an evidence tier or chooses therapy. For a separate KB, `--reviewers-dir` can select its registry; the default is the supplied BMA directory's sibling `reviewers` directory. `--as-of` controls source-snapshot age; review eligibility uses the current UTC date, not reconstructed historical authority.

Patient badges say **Clinical content review pending**, **pending (1 of 2 eligible reviews recorded)** or **Required clinical-content reviews recorded**. A note explains that this is knowledge-base content review, not approval of a plan for the patient. ES/PT/DE/FR captions are translation drafts pending clinical and language review.

Engineering tests and green CI establish technical contracts only. Neither counts as clinical review, verified credentials or patient suitability.
