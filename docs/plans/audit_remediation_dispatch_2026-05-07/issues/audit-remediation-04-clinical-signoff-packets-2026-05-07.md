# [Stream 4] Clinical Signoff Packets

## Mission

Turn the signoff blocker into reviewer-sized packets with explicit entity
IDs, source evidence, and pass/fail criteria.

## Baseline

`docs/audits/clinical_gap_audit.md` reports:

- 15/1726 signoff-eligible entities reviewed.
- 0.9% review coverage.
- Target before guideline-grade public claims: >=85%.

## First Step

Create a reviewer packet template before asking reviewers to inspect large
diffs. A packet should include:

- entity IDs
- changed fields
- source refs
- reviewer role
- unresolved questions
- signoff scope
- acceptance checklist

## Work Plan

1. Define packet template in docs.
2. Generate first packets from completed Stream 1 Wave A diffs.
3. Add BMA/ESCAT/CIViC packets after outcome-citation packets.
4. Add red-flag/contraindication packets before public safety claims.
5. Track one-reviewer "ready for second review" separately from final
   two-reviewer signoff.

## File Allowlist

- `docs/reviews/**/*.md`
- `docs/audits/clinical_gap_audit.md`
- `knowledge_base/hosted/content/reviewers/*.yaml`
- reviewed entity YAML only when adding signoff records

## Quality Gate

- No signoff without reviewer identity and scope.
- No guideline-grade claim from single-reviewer status.
- Packet includes enough source context for a reviewer to approve or reject
  without redoing discovery from scratch.

## Acceptance

This starter is complete when the packet template exists and the first
Wave A outcome-citation packet is ready for reviewer assignment.
