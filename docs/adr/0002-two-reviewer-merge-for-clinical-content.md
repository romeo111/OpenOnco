# 0002 — Two-reviewer merge for clinical content

Any change under `knowledge_base/hosted/content/` that affects clinical recommendations needs sign-off from two of the three Clinical Co-Leads before merge (CHARTER §6.1). This applies to Indications, Regimens, RedFlags, Algorithms, Workups, Contraindications, MonitoringSchedules, and any Source whose addition changes a clinical claim.

## Why

The KB is the system's clinical decision authority (ADR-0001). A single reviewer is one bus-factor away from a silently wrong recommendation; two-reviewer merge raises the bar to the point where a real-world clinician would expect.

Pure code changes (engine, schemas, validators, ingestion clients, build scripts) do not require two-reviewer sign-off — they go through the standard one-reviewer path.

## Consequences

- Refactors that move clinical content out of `knowledge_base/hosted/content/` (e.g. into hard-coded Python) bypass the gate and are not acceptable. The YAML+git format is what makes two-reviewer governance auditable.
- Refactors that change the *shape* of clinical entities (Pydantic schema changes, new required fields) are code changes — they don't need two reviewers themselves, but the migration of existing YAML to the new shape is clinical content and does.
- Refactors that propose a new clinical-content entity must show how the two-reviewer process applies to it.
