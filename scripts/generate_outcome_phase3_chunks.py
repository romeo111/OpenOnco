"""Generate Phase-3 chunk-issue stubs for the pivotal-trial-outcomes plan.

Reads the loaded KB, finds every indication whose `expected_outcomes` carries
at least one `SRC-LEGACY-UNCITED` placeholder (post-Phase-2 schema), groups
by disease, splits diseases with >10 uncited indications into multiple
≤10-indication chunks, and writes one chunk-issue markdown per chunk plus a
tracker file.

Output: `docs/plans/trial_outcomes_phase3_dispatch_<DATE-HHMM>/issues/*.md`.

Run once at dispatch time. Re-runnable; deterministic ordering.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
INDICATIONS_DIR = KB_ROOT / "indications"
DISEASES_DIR = KB_ROOT / "diseases"
LEGACY_PLACEHOLDER = "SRC-LEGACY-UNCITED"

# Outcome metadata keys we don't treat as values; matches audit script.
NON_OUTCOME_KEYS = {"notes", "note", "comment", "comments", "rationale", "follow_up", "followup", "caveats"}

DISPATCH_DIR_NAME = "trial_outcomes_phase3_dispatch_2026-05-01-0245"
CHUNK_PREFIX = "outcome-citations-phase3"
CHUNK_CAP = 10


def _is_uncited_outcome(value) -> bool:
    """Outcome counts as uncited if it's a plain non-empty string (legacy YAML
    that Phase-2 validator coerces to SRC-LEGACY-UNCITED) or an explicit dict
    with source=='SRC-LEGACY-UNCITED'."""
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, dict):
        return value.get("source") == LEGACY_PLACEHOLDER
    return False


def _uncited_field_names(eo: dict | None) -> list[str]:
    """Return outcome-field names pointing to legacy / uncited values."""
    if not isinstance(eo, dict):
        return []
    out: list[str] = []
    for fname, val in eo.items():
        if fname in NON_OUTCOME_KEYS:
            continue
        if _is_uncited_outcome(val):
            out.append(fname)
    return sorted(out)


def _slug(disease_id: str) -> str:
    return disease_id.replace("DIS-", "").lower().replace("_", "-")


def _chunk_id(disease_slug: str, idx: int, total_chunks_for_disease: int) -> str:
    suffix = f"-part{idx + 1}of{total_chunks_for_disease}" if total_chunks_for_disease > 1 else ""
    return f"{CHUNK_PREFIX}-{disease_slug}{suffix}-2026-05-01"


def _format_chunk_md(
    chunk_id: str,
    disease_id: str,
    disease_name: str,
    indications: list[tuple[str, Path, list[str]]],
    chunk_number: int,
    total_chunks_for_disease: int,
) -> str:
    """Render one chunk-issue stub. `indications` is list of (id, path, [uncited_fields])."""
    manifest_lines = [
        f"- {ind_id} (uncited: {', '.join(fields)}) — `{str(path.relative_to(REPO_ROOT)).replace(chr(92), '/')}`"
        for ind_id, path, fields in indications
    ]
    allowlist_paths = [
        str(path.relative_to(REPO_ROOT)).replace("\\", "/") for _, path, _ in indications
    ]

    return f"""# [Chunk] {chunk_id}

## Mission

Replace `SRC-LEGACY-UNCITED` placeholders in `expected_outcomes` for **{disease_name}** ({disease_id}) indications with real pivotal-trial citations. This is one of the Phase-3 chunks of the [trial-outcomes ingestion plan](../../pivotal_trial_outcomes_ingestion_plan_2026-04-30.md). Phase 2 schema (`OutcomeValue`) is already merged via [PR #177](https://github.com/romeo111/OpenOnco/pull/177).

This chunk owns **{len(indications)}** indication{"s" if len(indications) != 1 else ""} (chunk {chunk_number} of {total_chunks_for_disease} for this disease).

## Per-item workflow (per the plan §"Per-item workflow")

For each indication in the manifest below, for each `uncited` outcome field:

1. Identify the pivotal trial referenced by the indication's `notes` / `algorithm` step / `applicable_to` block. If unclear, escalate via `actionability_review_required: true` in the YAML and skip — do NOT guess.
2. Fetch the trial's pivotal publication via PubMed (use `mcp__plugin_bio-research_pubmed__lookup_article_by_citation` or `mcp__plugin_bio-research_pubmed__search_articles`, or fall back to `knowledge_base/clients/pubmed_client.py`).
3. Read the abstract + Results section. If the abstract is sparse, also fetch the NCT primary-results posting.
4. **Transcribe** (don't synthesize) ORR / CR / mPFS / mOS / OS-5y / DFS-HR exactly as the publication states them, with units. If a value is reported with median follow-up X mo, capture both via `OutcomeValue.median_followup_months`. Capture the 95% CI in `OutcomeValue.confidence_interval` when stated.
5. Create or reuse a `SRC-*` entity for the publication at `knowledge_base/hosted/content/sources/src_<trial>_<firstauthor>_<year>.yaml`. Citation must include PMID, DOI, journal, year, first-author surname. Follow existing `src_*.yaml` conventions.
6. Set each remediated `OutcomeValue.source` to the new `SRC-*` ID (drop the `SRC-LEGACY-UNCITED` placeholder).
7. Add a 1-line `notes` on the OutcomeValue if the value differs from frequently-quoted numbers.

## Forbidden (per the plan)

- Synthesizing or interpolating values not stated in the primary source.
- Picking which arm's outcomes apply when the indication's `applicable_to` block doesn't unambiguously map to a single trial arm — flag instead.
- Filling missing CIs from "typical" ranges.
- Translating outcome strings — keep them in the trial's English. UA goes elsewhere.
- Editing any KB file outside the allowlist.

## Manifest IDs (this chunk's allowlist)

{chr(10).join(manifest_lines)}

## Allowlist (file pathspecs this chunk may touch)

```
{chr(10).join(allowlist_paths)}
knowledge_base/hosted/content/sources/src_<trial>_<firstauthor>_<year>.yaml   ← new sources you author for this chunk
```

## Quality gates

1. KB validator clean: `PYTHONIOENCODING=utf-8 C:/Python312/python.exe -m knowledge_base.validation.loader knowledge_base/hosted/content` → `OK — all entities valid`.
2. Audit re-run: `py -3.12 scripts/audit_expected_outcomes.py` → confirm this chunk's indications moved out of the `uncited` bucket and into `cited`.
3. Per-chunk allowlist strictly enforced: `git diff --name-only origin/master` may only list paths in the allowlist + new `src_*.yaml` files.
4. Sources cited (no invented IDs / fabricated PMIDs).
5. Self-push authorized per CLAUDE.md `3a60901b` when all gates pass.

## Branch + commit + push

```
git fetch origin
git checkout -b chunk/{chunk_id} origin/master
# author files in allowlist
git status --short
git add <explicit pathspecs from allowlist>
git commit -m "$(cat <<'EOF'
feat(kb): {chunk_id}

Replace SRC-LEGACY-UNCITED in expected_outcomes for {len(indications)} {disease_name} indication{"s" if len(indications) != 1 else ""}; add N new SRC-* trial citations.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin chunk/{chunk_id}
```

## Stop conditions

- KB validator regresses.
- Edits land outside the allowlist.
- Indication's pivotal trial is not identifiable from the YAML — flag with `actionability_review_required: true` + 1-line note, do NOT guess.
- Trial publication paywalled and not on PubMed — Tier-2 fallback per plan: cite NCT primary-results posting + FDA label.
- PMID mismatch from typo in audit/source — cross-check first PubMed hit; if unsure, escalate.
- Two chunks editing the same `src_*.yaml` — coordination bug, escalate to orchestrator.

## Never

`git add -A`, `--no-verify`, force-push, branch deletion, edits to existing YAML beyond the allowlist, fabricating outcome values not stated in primary source.
"""


def _format_tracker(
    chunks_by_disease: dict[str, list[str]],
    total_uncited_indications: int,
    total_chunks: int,
) -> str:
    lines = [
        "# [Tracker] Trial-outcomes Phase 3 dispatch 2026-05-01-0245",
        "",
        "## Mission",
        "",
        "Master tracker for Phase-3 of the pivotal-trial-outcomes ingestion plan",
        "(`docs/plans/pivotal_trial_outcomes_ingestion_plan_2026-04-30.md`). Replace",
        f"`SRC-LEGACY-UNCITED` placeholders introduced by Phase-2 schema migration",
        f"with real pivotal-trial citations across **{total_uncited_indications} indications**",
        f"split into **{total_chunks} chunks**, ≤10 indications/chunk per the plan.",
        "",
        "Phase 2 schema reference: [PR #177](https://github.com/romeo111/OpenOnco/pull/177).",
        "Phase 1 audit baseline: [`docs/audits/expected_outcomes_traceability_2026-05-01.md`](../../../audits/expected_outcomes_traceability_2026-05-01.md).",
        "",
        "## Sub-issues checklist",
        "",
        "Check off each as it lands on master. Diseases ordered by audit `uncited` rank (highest first).",
        "",
    ]

    for disease_id, chunk_ids in chunks_by_disease.items():
        for chunk_id in chunk_ids:
            lines.append(f"- [ ] [{disease_id}] {chunk_id}")

    lines.extend(
        [
            "",
            "## Sequencing",
            "",
            "- **Wave A (parallel):** Top-5 worst-offender diseases (CRC, NSCLC, AML, Ovarian, DLBCL-NOS) — ~20 chunks.",
            "- **Wave B (parallel, after Wave A merges):** ranks 6-15 (Melanoma, FL, PV, B-ALL, MM, Breast, etc.) — ~30 chunks.",
            "- **Wave C (parallel, after Wave B):** remaining diseases — fewer indications/disease, lower priority.",
            "- **Phase 4 render** dispatched separately once Phase-3 hits ~70% completion (tracked at the plan level, not as a chunk here).",
            "",
            "## Quality gates (uniform per chunk)",
            "",
            "1. KB validator clean.",
            "2. Audit re-run shows the chunk's indications moved from `uncited` → `cited`.",
            "3. Per-chunk allowlist strictly enforced.",
            "4. Sources cited (no invented IDs, no fabricated PMIDs).",
            "5. Self-push authorized per CLAUDE.md commit `3a60901b`.",
            "",
            "## Acceptance for the wave",
            "",
            "- All non-deferred sub-issues closed.",
            "- KB validator clean throughout.",
            "- Audit `cited+probably-cited` rises from 15.7% baseline toward ≥90% v1.0 target.",
            "- No `SRC-LEGACY-UNCITED` placeholders remain (or remaining set is documented + intentionally deferred).",
            "- Phase 4 render chunk dispatched once Phase 3 hits 70%.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    diseases_by_id: dict[str, str] = {}
    for path in sorted(DISEASES_DIR.glob("*.yaml")):
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        did = doc.get("id")
        if not did or not did.startswith("DIS-"):
            continue
        names = doc.get("names") or {}
        diseases_by_id[did] = names.get("english") or did

    by_disease: dict[str, list[tuple[str, Path, list[str]]]] = defaultdict(list)
    for path in sorted(INDICATIONS_DIR.glob("*.yaml")):
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        ind_id = doc.get("id")
        if not ind_id or not ind_id.startswith("IND-"):
            continue
        eo = doc.get("expected_outcomes")
        uncited_fields = _uncited_field_names(eo)
        if not uncited_fields:
            continue
        applicable_to = doc.get("applicable_to") or {}
        disease_id = applicable_to.get("disease_id") or "DIS-UNKNOWN"
        by_disease[disease_id].append((ind_id, path, uncited_fields))

    # Sort diseases by uncited indication count desc, then disease_id
    sorted_diseases = sorted(by_disease.items(), key=lambda kv: (-len(kv[1]), kv[0]))

    out_root = REPO_ROOT / "docs" / "plans" / DISPATCH_DIR_NAME
    issues_dir = out_root / "issues"
    issues_dir.mkdir(parents=True, exist_ok=True)

    chunks_by_disease: dict[str, list[str]] = {}
    total_uncited = 0
    total_chunks = 0

    for disease_id, ind_list in sorted_diseases:
        ind_list.sort(key=lambda t: t[0])  # deterministic order
        disease_name = diseases_by_id.get(disease_id, disease_id)
        # Slice into ≤CHUNK_CAP groups
        slices = [ind_list[i : i + CHUNK_CAP] for i in range(0, len(ind_list), CHUNK_CAP)]
        slug = _slug(disease_id)
        chunks_by_disease[disease_id] = []
        for idx, chunk_inds in enumerate(slices):
            chunk_id = _chunk_id(slug, idx, len(slices))
            chunks_by_disease[disease_id].append(chunk_id)
            md = _format_chunk_md(
                chunk_id=chunk_id,
                disease_id=disease_id,
                disease_name=disease_name,
                indications=chunk_inds,
                chunk_number=idx + 1,
                total_chunks_for_disease=len(slices),
            )
            (issues_dir / f"{chunk_id}.md").write_text(md, encoding="utf-8")
            total_chunks += 1
        total_uncited += len(ind_list)

    tracker = _format_tracker(chunks_by_disease, total_uncited, total_chunks)
    (issues_dir / "00-trial-outcomes-phase3-tracker-2026-05-01-0245.md").write_text(
        tracker, encoding="utf-8"
    )

    print(
        f"Wrote {total_chunks} chunks for {total_uncited} indications across "
        f"{len(chunks_by_disease)} diseases → {issues_dir}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
