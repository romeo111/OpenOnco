# Citation Verification 914 Audit Contribution

Chunk: citation-verify-914-audit
Source audit: docs/reviews/citation-verification-2026-04-27.md
Source commit: d580b0b
Generated: 2026-04-27

## Scope

This contribution converts the existing read-only citation verification sweep into a machine-readable report. It does not modify hosted content and does not mark any row as supported without source-level verification.

## Counts

- total findings: 914
- BMA: 696
- Indication: 129
- Regimen: 89
- drug-inconsistency: 285
- level-mismatch: 124
- missing-regulatory-source: 153
- missing-trial-source: 352

## Review Note

Rows with missing source findings use `support_status: unclear` and `suggested_action: source_stub_needed`. Level and drug-text findings use maintainer review actions. This keeps the report conservative and avoids implying source verification that was not performed.
