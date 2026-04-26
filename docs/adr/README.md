# Architecture Decision Records

Decisions that should not be re-litigated by future refactor proposals. Format follows `.claude/skills/domain-model/ADR-FORMAT.md`.

| # | Title | Source |
|---|---|---|
| [0001](0001-rule-engine-not-llm-for-clinical-decisions.md) | Rule engine, not LLM, makes the clinical decision | CHARTER §8.3 |
| [0002](0002-two-reviewer-merge-for-clinical-content.md) | Two-reviewer merge for clinical content | CHARTER §6.1 |
| [0003](0003-no-patient-data-in-public-artifacts.md) | No real patient data in public artifacts | CHARTER §9.3 |
| [0004](0004-source-hosting-default-referenced.md) | Source hosting default is `referenced`, not `hosted` | SOURCE_INGESTION_SPEC §1.4 |

These four are restatements of pre-existing CHARTER and SPEC clauses, formatted as ADRs so that the `improve-codebase-architecture` skill (`.claude/skills/improve-codebase-architecture/`) treats them as gates rather than open questions. Future ADRs added during refactor work continue the sequential numbering.
