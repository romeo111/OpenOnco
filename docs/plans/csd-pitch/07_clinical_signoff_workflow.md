# Clinical Sign-off Workflow

Audience: Clinical Co-Leads onboarding to OpenOnco.

CHARTER §6.1 requires that every change to clinical content
(`knowledge_base/hosted/content/{indications,algorithms,regimens,redflags,biomarker_actionability}/`)
is approved by **two of three Clinical Co-Leads** before publication. This
document explains how to record those approvals.

## What sign-off is

A *sign-off* is a structured, dated, free-text-justified approval by a
named Clinical Co-Lead, recorded:

1. inside the entity YAML itself (field: `reviewer_signoffs_v2`), and
2. as an append-only row in the audit log
   `knowledge_base/hosted/audit/signoffs.jsonl`.

A withdraw deletes the YAML row but **keeps** the audit history — the
chain of approvals + revocations is replayable.

The render layer surfaces three sign-off states next to each
recommendation in the generated treatment Plan:

| State | Badge (clinician) | Badge (patient) |
|---|---|---|
| 0 sign-offs   | red — `Очікує підпису Clinical Co-Lead` | red — `Очікує перевірки лікарями` |
| 1 sign-off    | yellow — `Підписано (1/2): {reviewer}` | yellow — `Очікує перевірки лікарями (1 з 2)` |
| ≥2 sign-offs  | green — `Клінічно затверджено: {r1}, {r2}` | green — `Затверджено лікарями` |

## Setup

```
git clone https://github.com/openonco/openonco.git
cd openonco
pip install pyyaml pydantic
```

No additional dependencies are needed for sign-off — the CLI is stdlib + yaml + pydantic.

## CLI: `scripts/clinical_signoff.py`

Three sub-commands:

### `approve`

Add a sign-off to one or many entities.

```bash
# Single entity by ID
py scripts/clinical_signoff.py approve \
    --reviewer REV-HEME-LEAD-PLACEHOLDER \
    --entity-id IND-DLBCL-1L-RCHOP \
    --rationale "NCCN-aligned, R-CHOP-21 standard 1L"

# Bulk by glob (relative to knowledge_base/hosted/content/)
py scripts/clinical_signoff.py approve \
    --reviewer REV-HEME-LEAD-PLACEHOLDER \
    --pattern "indications/ind_dlbcl_*.yaml" \
    --rationale "DLBCL 1L NCCN/ESMO-aligned, evidence reviewed"

# Dry-run: preview without writing
py scripts/clinical_signoff.py approve \
    --reviewer REV-SOLID-LEAD-PLACEHOLDER \
    --pattern "indications/ind_crc_*.yaml" \
    --rationale "..." \
    --dry-run

# --strict refuses to proceed when reviewer scope doesn't cover the entity.
# Without --strict, scope mismatch produces a warning + proceeds.
py scripts/clinical_signoff.py approve \
    --reviewer REV-HEME-LEAD-PLACEHOLDER \
    --entity-id IND-CRC-METASTATIC-1L-FOLFOX-BEV \
    --rationale "..." \
    --strict   # → REFUSE because heme lead doesn't cover gastrointestinal

# --force allows re-affirming an existing sign-off.
py scripts/clinical_signoff.py approve \
    --reviewer REV-HEME-LEAD-PLACEHOLDER \
    --entity-id IND-DLBCL-1L-RCHOP \
    --rationale "Re-affirm after POLARIX update review" \
    --force
```

### `withdraw`

Remove a sign-off (and append a withdraw row to the audit log).

```bash
py scripts/clinical_signoff.py withdraw \
    --reviewer REV-HEME-LEAD-PLACEHOLDER \
    --entity-id IND-AML-1L-7-3 \
    --rationale "Reconsider after IDH1+ subgroup data"
```

### `list`

Inspect sign-offs for one entity OR all sign-offs by one reviewer.

```bash
py scripts/clinical_signoff.py list --entity-id IND-DLBCL-1L-RCHOP
py scripts/clinical_signoff.py list --reviewer REV-HEME-LEAD-PLACEHOLDER
```

## Reviewer profiles

Located at `knowledge_base/hosted/content/reviewers/rev_*.yaml`. Each
profile carries:

- `display_name`, `affiliation`, `role_title`, `credentials`
- `sign_off_scope`:
  - `entity_types` — `indications`, `algorithms`, `regimens`, `redflags`, `biomarker_actionability` (empty list = no restriction)
  - `disease_categories` — `hematologic`, `lymphoid`, `myeloid`, `plasma-cell`, `solid`, `gastrointestinal`, `breast`, `gu`, `gyn`, `thoracic`, `cns`, `hnscc`, `sarcoma`, `melanoma` (empty list = no restriction)
  - `disease_ids` — explicit `DIS-*` allow-list (overrides categories)
- `status`: `active` | `inactive` | `placeholder`

Three placeholder profiles ship with the v0.1 KB
(`rev_*_placeholder.yaml`) so the CLI can be exercised end-to-end before
real Clinical Co-Leads onboard. Sign-offs by placeholder reviewers are
illustrative — real clinician verification is still required.

## Dashboard

Generate a coverage snapshot:

```bash
py scripts/build_signoff_dashboard.py
# Writes docs/plans/signoff_status_<YYYY-MM-DD>.md
```

The dashboard reports:

- total entities requiring sign-off, with ≥1 / ≥2 / 0 sign-off coverage
- per-entity-type breakdown
- per-disease (top 20) breakdown with average sign-off count
- per-reviewer activity counts + most-recent timestamp + withdrawals
- last 7 days of audit activity (max 50 entries)

Re-run after every batch of sign-offs to track CHARTER §6.1 progress.

## GitHub Action template

`.github/workflows/clinical-content-pr.yml.disabled` — disabled
template. Drop the `.disabled` suffix to enable. Requires the
`clinical-co-lead` GitHub team to exist before un-commenting the
auto-request-review job.

When enabled, the action:

- adds a `clinical-review-required` label to any PR touching clinical content
- posts a comment pointing the author at `scripts/clinical_signoff.py`
- (optional) requests review from the `clinical-co-lead` team
- (optional) validates the KB after the PR's changes apply

## Troubleshooting

**`ERR: reviewer 'REV-…' not found`**
The CLI walks `knowledge_base/hosted/content/reviewers/`. Confirm the
profile YAML exists and its top-level `id:` matches what you passed. IDs
are case-sensitive.

**`ERR: entity 'IND-…' not found`**
The CLI infers the directory from the ID prefix (`IND-` → `indications/`,
`ALGO-` → `algorithms/`, etc.) and falls back to a full search if the
prefix is unknown. Confirm the entity YAML exists and its top-level `id:`
matches.

**`SKIP (duplicate sign-off, use --force to override)`**
You already signed off this entity. Pass `--force` to re-affirm (a fresh
audit row is appended). Otherwise the second approval is a no-op.

**`REFUSE (scope, --strict)`**
Your `sign_off_scope` doesn't cover the entity (wrong entity type or
wrong disease category). Drop `--strict` to override (a warning is
emitted but the sign-off proceeds, with `scope_match=false` recorded for
audit).

**`No entities matched`**
Your `--pattern` resolved to zero files. Patterns are globs *relative to*
`knowledge_base/hosted/content/`. Examples:

- `indications/ind_dlbcl_*.yaml` — all DLBCL indications
- `algorithms/algo_aml_*.yaml` — all AML algorithms
- `redflags/rf_*_organ_dysfunction.yaml` — all organ-dysfunction RedFlags

**Render shows the wrong reviewer name**
The renderer caches reviewer labels per process. Restart any long-running
process (devserver, jupyter) after editing reviewer profiles.
