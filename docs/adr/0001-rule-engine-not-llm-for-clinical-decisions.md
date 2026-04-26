# 0001 — Rule engine, not LLM, makes the clinical decision

LLMs may not be the clinical decision-maker (CHARTER §8.3). Treatment-plan selection, dosing, and biomarker-driven branching come from a declarative rule engine traversing a versioned, human-authored knowledge base. LLMs are restricted to: boilerplate code, doc drafts, extraction from clinical documents (with human verification), and translation with clinical review.

## Why

A rule engine is auditable, reproducible, and revisable through a two-reviewer governance process (ADR-0002). A clinician can point at the exact Indication, Algorithm step, and Source that produced a given Plan. LLM outputs do not have that property at acceptable cost.

Many of the project's source licences (ESMO CC-BY-NC-ND, OncoKB academic, ATC) also depend on the system being non-commercial and not redistributing source content via generative output.

## Consequences

- Architecture proposals that move clinical reasoning into an LLM (re-rank Indications, generate dosing, pick a Regimen from prose) are out of scope and should not be re-litigated by refactor candidates.
- Acceptable LLM uses (extraction, drafting, translation, code scaffolding) sit clearly outside the engine's decision path.
- The retired `legacy/` autoresearch pipeline used an LLM-ranks-treatments approach and is preserved only as historical reference; do not pattern new work on it.
