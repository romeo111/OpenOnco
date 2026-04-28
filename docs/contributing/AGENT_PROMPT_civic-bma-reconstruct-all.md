# Agent Prompt: `civic-bma-reconstruct-all`

Copy everything inside the fenced block below into your AI tool (Codex / Claude Code / Cursor / ChatGPT). Replace the four placeholders at the top before pasting:

- `<YOUR_GITHUB_USERNAME>` — your GitHub handle
- `<TODAY_DATE>` — today's date in `YYYY-MM-DD` format
- `<TOOL>` — `codex` | `claude-code` | `cursor` | `chatgpt` | `other`
- `<MODEL>` — short model name, e.g. `gpt-5-mini`, `claude-opus-4-7`, `gemini-2.5-pro`

After pasting, let the agent work. Watch for token-budget limits. The full chunk is ~1M tokens of structured work; if your tool runs out, save what you have and resume.

---

````
You are an AI agent helping OpenOnco — a free, open-source oncology decision-support project — reconstruct biomarker-actionability evidence from CIViC. You are executing the TaskTorrent chunk `civic-bma-reconstruct-all`.

## Identity (use these in every sidecar's _contribution block)

- contributor: <YOUR_GITHUB_USERNAME>
- submission_date: <TODAY_DATE>
- ai_tool: <TOOL>
- ai_model: <MODEL>

## Reading material (read in this order)

1. `docs/contributing/HELP_WANTED.md` — safety boundaries.
2. `https://github.com/romeo111/task_torrent/blob/main/chunks/openonco/civic-bma-reconstruct-all.md` — chunk spec (this is your task contract).
3. `contributions/civic-bma-reconstruct-all/task_manifest.txt` — exact list of BMA-* IDs in scope.
4. `contributions/civic-bma-reconstruct-all/bma_egfr_t790m_nsclc.yaml` — working reference. Your output for every other BMA must match this shape.
5. `knowledge_base/schemas/biomarker_actionability.py` — Pydantic schema. Field names and types are authoritative.
6. `knowledge_base/engine/civic_variant_matcher.py` — matching function for CIViC entries.

## Mission

For every `BMA-*` listed in `task_manifest.txt`:

1. Read the existing BMA YAML at `knowledge_base/hosted/content/biomarker_actionability/<bma_id_lowercase>.yaml`.
2. Extract `(gene, variant, disease)`:
   - `gene` from `biomarker_id` (e.g. `BIO-EGFR-MUTATION` → `EGFR`).
   - `variant` from `variant_qualifier` (e.g. `"T790M"`, `"V600E"`, `"Exon 19 deletion"`).
   - `disease` from `disease_id` (e.g. `DIS-NSCLC`).
3. Query the local CIViC snapshot at `knowledge_base/hosted/civic/2026-04-25/evidence.yaml` (or whichever date subdir exists — pick the latest). Filter for matching evidence items where:
   - `gene == <extracted gene>` (use `civic_variant_matcher.matches_civic_entry` if you can run Python; otherwise apply its rules — see `civic_variant_matcher.py`).
   - `variant == <extracted variant>` (allow whole-word match per matcher rules).
   - `disease` matches the OpenOnco disease (e.g. `DIS-NSCLC` → CIViC disease string contains "Lung Non-small Cell Carcinoma" / "Non-small Cell Lung Carcinoma").
   - `evidence_status == "accepted"`.
4. Build new `evidence_sources` block. **Group matching EIDs by `(level, evidence_direction, significance)` tuple.** One `EvidenceSourceRef` entry per group:
   - `source: SRC-CIVIC`
   - `level:` source-native CIViC token verbatim (`A` / `B` / `C` / `D` / `E`)
   - `evidence_ids: ["EID<n>", ...]` — all EIDs in this group
   - `direction:` (`Supports` / `Does Not Support`)
   - `significance:` (CIViC label, e.g. `Sensitivity/Response`, `Resistance`, `Poor Outcome`)
   - `note:` short clinical paraphrase (do NOT recommend; describe what the bucket attests)
5. **Drop** any existing `evidence_sources` entry with `source: SRC-ONCOKB`. Do not preserve it.
6. **Decide `actionability_review_required`:**
   - Set to `false` ONLY IF: (a) the new CIViC `evidence_sources` is non-empty, AND (b) the dropped `SRC-ONCOKB` entry did not describe a unique claim not covered by CIViC (typically true for variants with strong CIViC coverage), AND (c) the `escat_tier` is unchanged and well-supported by CIViC.
   - Otherwise set to `true` and explain in `_contribution.notes_for_reviewer`.
7. Update `last_verified` to <TODAY_DATE>.
8. Write the sidecar at `contributions/civic-bma-reconstruct-all/<existing_bma_filename>.yaml`. Same filename as the source, just relocated to the contributions dir.

## CRITICAL: Fields you must NOT change

These fields stay verbatim from the existing BMA file. Do not edit, regenerate, paraphrase, or "improve":

- `escat_tier`
- `evidence_summary`
- `evidence_summary_ua`
- `ukrainian_review_status`
- `ukrainian_drafted_by`
- `regulatory_approval` (whole block)
- `recommended_combinations`
- `contraindicated_monotherapy`
- `primary_sources`
- `notes`

If you change any of these, the maintainer's computational re-verification script will reject the entire batch.

## Sidecar shape (match this exactly)

```yaml
_contribution:
  chunk_id: civic-bma-reconstruct-all
  contributor: <YOUR_GITHUB_USERNAME>
  submission_date: <TODAY_DATE>
  target_action: upsert
  target_entity_id: BMA-<biomarker>-<variant>-<disease>
  duplicate_of: null
  ai_tool: <TOOL>
  ai_model: <MODEL>
  ai_model_version: ""
  ai_session_notes: ""
  notes_for_reviewer: >
    Brief — one or two sentences on the actionability_review_required choice
    and any borderline judgment.

# everything below is the BMA payload — match knowledge_base/schemas/biomarker_actionability.py
id: <BMA-id>
biomarker_id: <BIO-id, unchanged>
variant_qualifier: "<unchanged>"
disease_id: <DIS-id, unchanged>
escat_tier: "<unchanged>"
evidence_summary: <unchanged>
evidence_summary_ua: <unchanged>
ukrainian_review_status: <unchanged>
ukrainian_drafted_by: <unchanged>
regulatory_approval:
  fda: <unchanged>
  ema: <unchanged>
  ukraine: <unchanged>
recommended_combinations: <unchanged>
contraindicated_monotherapy: <unchanged>
primary_sources: <unchanged>
last_verified: "<TODAY_DATE>"
evidence_sources:
  - source: SRC-CIVIC
    level: "A"
    evidence_ids: ["EID...", "EID..."]
    direction: "Supports"
    significance: "Sensitivity/Response"
    note: "Brief clinical paraphrase, e.g. 'Osimertinib sensitivity in T790M+ NSCLC'."
  # ... one entry per (level, direction, significance) bucket
actionability_review_required: false  # or true with rationale in notes_for_reviewer
notes: <unchanged>
```

## Banned

- Never reference `SRC-ONCOKB`, `SRC-SNOMED`, or `SRC-MEDDRA` in `evidence_sources` or anywhere else.
- Never invent CIViC EIDs not in the local snapshot. Cross-check every EID by reading `evidence.yaml`.
- Never write to `knowledge_base/hosted/content/` directly. Output is ONLY to `contributions/civic-bma-reconstruct-all/`.
- Never use recommendation wording in `note` fields. "source attests", "evidence supports", "CIViC reports" — yes. "Best treatment", "preferred", "patients should" — no.

## Self-check before claiming done

Run:

```
python -m scripts.tasktorrent.validate_contributions civic-bma-reconstruct-all
```

The output must end with `All contributions pass validation.` Fix any FAIL before claiming the task complete.

## Reporting

When you finish (or hit a token wall), summarize:

- N sidecars produced (out of M in manifest).
- For each BMA where you set `actionability_review_required: true`: the BMA-id and one-line reason.
- Any BMA where the CIViC matcher returned 0 results: the BMA-id and the `(gene, variant, disease)` triple that didn't match.
- Validator status: PASS or list of FAIL messages.

If anything is unclear, stop and report the ambiguity rather than guessing. The contributor will then ask the maintainer.
````

---

## Notes for the contributor running the prompt

- **Token budget.** This chunk is ~1M tokens. Codex GPT-5-mini and Claude Code Opus 4.7 typically complete it in one session at Pro tier. If you run out, save your in-progress sidecars and resume — the validator is happy with a partial chunk dir as long as every sidecar individually passes.

- **CIViC matcher edge cases.** Some BMAs have fusion variants (`ALK-EML4`, `BCR-ABL1`, `EGFR-T790M-Cis`) — `civic_variant_matcher.py` handles fusion-on-fusion patterns and pan-fusion sentinels. Read its docstring; don't override its rules.

- **When CIViC returns nothing.** Some flagged BMAs may have no CIViC evidence (rare variants, rare diseases). For those, set `actionability_review_required: true` and `notes_for_reviewer: "No CIViC evidence found for <gene> <variant> in <disease>; needs maintainer triage."` — leave `evidence_sources` empty rather than inventing.

- **When the existing OncoKB claim disagrees with CIViC.** If the dropped `SRC-ONCOKB` entry described a level higher than what CIViC carries (e.g. OncoKB Level 1 vs CIViC Level D), set `actionability_review_required: true` and flag the discrepancy in `notes_for_reviewer`. The maintainer + Clinical Co-Lead decide whether to escalate or accept the downgrade.

- **Time estimate.** Realistic: 2–4 hours for a fluent contributor with a Pro AI account. The agent does the work; you supervise, sanity-check, and intervene when it gets stuck.
