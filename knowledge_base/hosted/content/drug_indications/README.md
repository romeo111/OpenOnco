# drug_indications

First-class drug-use rows for label, off-label, and reimbursement status.

Each YAML in this directory should describe one `Drug` in one disease /
Indication / Regimen context. Generated backfill rows must stay
`draft: true` and `unknown_pending_review` until a qualified reviewer confirms
the regulatory and reimbursement status from cited Sources.
