# Help OpenOnco — Distributed AI Contributions Welcome

OpenOnco is a free public oncology decision-support resource. It is
specifications-first: clinical knowledge lives as versioned YAML in
`knowledge_base/hosted/content/`, validated by Pydantic, reviewed by
clinicians before publication.

We accept distributed AI-assisted contributions through the
**TaskTorrent** chunk-shelf model. Each "chunk" is one concrete,
complete, LLM-essential task — typically ~1 million tokens of structured
work — that one contributor takes end-to-end with their own AI tool
(Codex, Claude Code, Cursor, ChatGPT, etc.).

> **Safety boundaries (non-negotiable).** OpenOnco contributors do
> **not** make medical decisions, recommend treatments, or generate
> patient-specific outputs. Contributor work is structured evidence
> drafting, citation verification, normalization, and audit. All
> AI-generated output is reviewed by maintainers and Clinical
> Co-Leads before merging into hosted clinical content.

## Where the work surface lives

- **Chunk shelf:** https://github.com/romeo111/task_torrent/tree/main/chunks/openonco
- **Operational rules:** https://github.com/romeo111/task_torrent/blob/main/docs/openonco-pilot-workflow.md
- **Active chunks (claim one!):** https://github.com/romeo111/cancer-autoresearch/issues?q=is%3Aissue+is%3Aopen+label%3Achunk-task+label%3Astatus-active

If no chunks are `status-active`, the pilot has the maintainer cap of 2
active chunks reached. Subscribe to the repo or check back; new active
chunks open as previous ones close.

## How to take a chunk

**Step-by-step instructions:** [`CONTRIBUTOR_QUICKSTART.md`](CONTRIBUTOR_QUICKSTART.md) — fork → branch → run agent → validate → PR. Read this before starting.

**Per-chunk agent prompts:** copy-paste templates that you give to your AI tool. See `AGENT_PROMPT_<chunk-id>.md` for each chunk:

- [`AGENT_PROMPT_civic-bma-reconstruct-all.md`](AGENT_PROMPT_civic-bma-reconstruct-all.md) — CIViC BMA evidence reconstruction.
- (more added as chunks promote to `status-active`).

Quick summary of the flow:

1. **Pick** an open `[Chunk]` issue with label `status-active` and no assignee. Comment to claim. Maintainer assigns you within 24 hours (auto-released after 24h if not assigned).
2. **Read** [`CONTRIBUTOR_QUICKSTART.md`](CONTRIBUTOR_QUICKSTART.md) end-to-end.
3. **Branch** as `tasktorrent/<chunk-id>` AND **immediately push the empty branch to origin** (WIP-branch-first rule, see below).
4. **Run** your AI tool with the chunk's `AGENT_PROMPT_*.md` content. Output goes into `contributions/<chunk-id>/`.
5. **Self-validate**: `python -m scripts.tasktorrent.validate_contributions <chunk-id>` — must say `PASS`.
6. **Open PR** against `master`. CI auto-runs; maintainer reviews when CI green.
7. **Iterate** force-pushing if maintainer requests changes.
8. **PR merges** when accepted. Maintainer-run upsert promotes sidecars into hosted content after Clinical Co-Lead signoff (CHARTER §6.1) where applicable.

## Two claim methods (per chunk-spec)

Each chunk-spec declares one of two `claim_method` values. Use the method declared in the chunk you're taking.

### `formal-issue` (for open contributors)

The standard flow described in steps 1–8 above. Comment on issue → maintainer assigns → assignee field locks the slot. Other contributors see the assigned issue and don't duplicate.

**24h SLA:** if maintainer doesn't assign within 24 hours of your claim comment, the chunk auto-releases (a bot drops the claim label). You can re-claim or another contributor can take it.

### `trusted-agent-wip-branch-first` (for pre-authorized contributor agents)

Maintainer pre-authorizes the contributor (e.g. their own Codex or a known partner agent). No formal issue-claim ceremony.

**Critical:** push a minimal/empty WIP commit to `tasktorrent/<chunk-id>` on origin **immediately** when you start, BEFORE doing significant local work. This branch on origin = the visible lock.

```bash
git checkout -b tasktorrent/<chunk-id>
git commit --allow-empty -m "wip: starting <chunk-id>"
git push -u origin tasktorrent/<chunk-id>
# now do the actual work; force-push or new commits later
```

The WIP-branch-first rule prevents the "invisible window" between local-work-start and first-push from causing two trusted agents to duplicate the chunk. Without it, a 2-hour local session of agent A blocks nothing from origin's perspective; agent B starts the same chunk in parallel.

**Stale-claim auto-release:** chunk-task issues with `assignee` set + no commits to `tasktorrent/<chunk-id>` for 14 days are auto-released by a bot (drops assignee, re-labels `status-active`). If you fall behind, comment on the issue with an ETA before the bot fires.

## Reference output: the PoC sidecar

A working reference for the `civic-bma-reconstruct-all` chunk lives at
[`contributions/civic-bma-reconstruct-all/bma_egfr_t790m_nsclc.yaml`](../../contributions/civic-bma-reconstruct-all/bma_egfr_t790m_nsclc.yaml).
It demonstrates: (a) the `_contribution` wrapper, (b) `evidence_sources`
reconstruction from the local CIViC snapshot, (c) `task_manifest.txt`,
(d) `_contribution_meta.yaml`. Match this shape.

## What you'll need

- A GitHub account.
- An AI tool with enough capacity for ~1M tokens per chunk (paid Codex /
  Claude Code Pro / Cursor Pro tier, or equivalent).
- For citation-verification chunks: web access to PubMed, CIViC,
  DailyMed, openFDA, ClinicalTrials.gov.
- For UA-translation chunks: native-or-near-native Ukrainian + working
  medical English.
- Comfort with YAML, GitHub PR workflow.

## What you should NOT do

- **Edit `knowledge_base/hosted/content/` directly.** All output goes
  into `contributions/<chunk-id>/`. Maintainers run the upsert script.
- **Bundle multiple chunks.** One PR = one chunk.
- **Use `git add -A` / `git add .`.** Stage explicit pathspecs.
- **Bypass hooks (`--no-verify`).** Pre-commit gates exist to protect
  the repo.
- **Cite banned sources** (OncoKB, SNOMED CT, MedDRA — see
  pilot-workflow doc for why).
- **Invent `SRC-*` IDs.** If a citation has no Source entity yet, file a
  `source_stub.yaml` in the chunk dir.
- **Use recommendation wording** in any field. CHARTER §8.3.

## How review works

1. CI runs `validate_contributions.py` on every PR. Mechanical gate
   failures auto-reject.
2. Maintainer reviews PRs that pass CI. SLA: response within 7 working
   days.
3. Maintainer may request changes (force-push to fix) or accept.
4. Accepted PRs merge to `master`. Sidecars sit in `contributions/`.
5. Maintainer runs `upsert_contributions.py --confirm <chunk-id>` after
   Clinical Co-Lead signoff for claim-bearing content. Sidecar payloads
   become hosted content.

If your PR is rejected, expect a comment using one of the templates in
[`docs/contributing/REJECTION_TEMPLATES.md`](REJECTION_TEMPLATES.md).
The templates name the fix; iterate and re-push.

## Contributor recognition

Contributor names appear in `_contribution.contributor` on every sidecar
they author. The hosted content's `last_reviewed` and `verifier` fields
record the maintainer who upserted, not the contributor — but the
sidecar trail (and PR history) preserves contributor authorship
indefinitely.

OpenOnco does not pay contributors. Drops are an effort-tracking unit,
not a reward token. Contribution is volunteer.

## Questions?

Open an issue with label `question` on this repo, or a discussion at
https://github.com/romeo111/cancer-autoresearch/discussions .
