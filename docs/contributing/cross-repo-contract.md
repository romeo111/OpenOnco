---
synced_from: task_torrent@main#docs/cross-repo-contract.md
last_synced: 2026-04-29
note: |
  This is a mirror of the canonical cross-repo contract maintained
  in romeo111/task_torrent. Do not edit here directly — propose
  changes upstream via PR to task_torrent. The mirror is for
  contributor convenience (linkable from OpenOnco docs without a
  cross-repo redirect).

  Sync-check CI deferred to protocol v0.5 per cross-repo plan §5.5.
  Until then, mirror staleness is detected by hand or via the
  changelog in protocol-v0.4-design.md.
---

# Cross-Repo Contract — task_torrent ↔ OpenOnco

**Canonical:** [`task_torrent/docs/cross-repo-contract.md`](https://github.com/romeo111/task_torrent/blob/main/docs/cross-repo-contract.md)

This file is a mirror. Read the canonical doc for the authoritative version. The mirror exists so that OpenOnco contributors don't need to context-switch repos to read the contract.

If the two diverge, **the canonical wins.** Open an issue if you spot drift.

## Quick reference for OpenOnco contributors

The full contract covers:

- **Discovery** — how `next_chunk.py` finds open chunks
- **Issue body** — what `## ` headings the parser expects
- **Chunk spec** — what fields the linter requires
- **Claim** — `formal-issue` vs `trusted-agent-wip-branch-first` flows
- **Sidecar** — required files in `contributions/<chunk-id>/`
- **Rejection codes** — 9-item vocabulary for maintainer rejections
- **Banned sources** — `SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA` (CHARTER §2)
- **Versioning** — v0.4 observability-only (optional commit-hash; no semver tags)
- **Trust tiers** — T0/T1/T2, per-consumer (not portable across consumers by default)
- **Reference implementations** — where each piece lives in this repo

## OpenOnco-specific addenda

The contract is generic. OpenOnco-specific bits:

- Banned sources list: `SRC-ONCOKB`, `SRC-SNOMED`, `SRC-MEDDRA`. CHARTER §2 enforces non-commercial.
- Two-reviewer signoff required for clinical content (CHARTER §6.1) — currently in dev-mode exemption per project-memory.
- Patient-specific output banned (CHARTER §9.3) — even with consent, requires de-identification + ethics approval before public release.
- Ukrainian-first KB; English mirrored where applicable.

For the full contract, read the [canonical](https://github.com/romeo111/task_torrent/blob/main/docs/cross-repo-contract.md).
