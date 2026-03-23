#!/usr/bin/env python3
"""
local_task_generator.py — RTX 5050 powered gap analysis + Claude API task generator

Workflow:
  1. Scan existing reports with evaluate.py (fast, local)
  2. For each report below threshold or with specific dimension gaps,
     use llama3.2:3b to identify the 3 most fixable data gaps
  3. Generate a targeted re-evaluation prompt for Claude API to fix
     only the broken parts — not redo the whole report

Output: tasks/reeval_{CASE_ID}.md  — one prompt per report that needs work
        tasks/manifest.json        — sorted by impact (largest score gain first)

Usage:
    # Scan all reports, generate tasks for anything below 88/100
    python local_task_generator.py --reports experiment_reports --threshold 88

    # Scan specific dimension
    python local_task_generator.py --reports experiment_reports --focus rating_calibration

    # Run Claude API on generated tasks (requires anthropic)
    python local_task_generator.py --execute --model claude-opus-4-6 --api-key sk-ant-...

    # Dry run — show what would be generated without writing files
    python local_task_generator.py --reports experiment_reports --dry-run
"""

import argparse
import glob
import json
import os
import sys
import io
import urllib.request
import urllib.error
from datetime import datetime
from typing import Optional

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── Constants ─────────────────────────────────────────────────────────────────

OLLAMA_BASE   = "http://localhost:11434"
PRESCORE_MODEL = "llama3.2:3b"
TASKS_DIR     = "tasks"

DIMENSION_MAX = {
    "structural_integrity":     15,
    "evidence_depth":           25,
    "tier_coverage":            10,
    "rating_calibration":       15,
    "source_quality":           15,
    "clinical_relevance":       10,
    "combo_supportive_coverage": 10,
}

# Maps dimension -> what Claude should fix
DIMENSION_FIX_INSTRUCTIONS = {
    "rating_calibration": """\
Your task: Fix ONLY the `rating_breakdown` fields in the `treatments` array.

For each treatment, verify:
1. `evidence_level.score` matches the actual study phase:
   - Phase 3 RCT (N>=500, top journal) = 9-10
   - Phase 3 RCT (N<500) = 7-8
   - Phase 2 = 5-7
   - Phase 1 = 2-4
   - Case series / retrospective = 1-3
2. `survival_benefit.score` matches actual OS delta:
   - >12 months delta = 9-10
   - 6-12 months = 7-8
   - 3-6 months = 5-6
   - 1-3 months = 3-4
   - <1 month or no control = 1-2
3. `composite_rating` = weighted average (evidence 30%, survival 30%, access 15%, safety 15%, biomarker 10%)
4. Treatments must be re-sorted descending by composite_rating after changes

Do NOT change any other field. Return the complete corrected `treatments` array only.""",

    "evidence_depth": """\
Your task: Fill missing evidence fields in `treatments[].key_evidence`.

For each treatment where these are null or missing, search and fill:
- `key_evidence.study_name` — full trial name
- `key_evidence.year` — publication year
- `key_evidence.sample_size` — numeric patient count
- `key_evidence.os_months.treatment` — median OS in treatment arm (months)
- `key_evidence.os_months.control` — median OS in control arm (months)
- `key_evidence.os_months.hazard_ratio` — HR from primary analysis
- `key_evidence.os_months.p_value` — p-value from OS analysis
- `key_evidence.pfs_months.treatment` — median PFS treatment arm
- `key_evidence.pfs_months.control` — median PFS control arm

Rules:
- Only fill with data you can verify from published trials
- Set to null (not omit) if genuinely unavailable after searching
- Do NOT fabricate or estimate numbers

Return the corrected `treatments` array only.""",

    "clinical_relevance": """\
Your task: Add missing `intent` fields and improve biomarker documentation.

For each treatment missing `intent`, add the correct value:
- curative: definitive treatment for localized/resectable disease
- adjuvant: post-operative to prevent recurrence
- neoadjuvant: pre-operative to downstage
- palliative: Stage IV / unresectable / incurable
- salvage: second+ line after prior treatment failure
- maintenance: ongoing after response to prevent progression

Also: for any treatment missing `ps_requirement`, add it (e.g. "ECOG 0-2" or "No restriction").

Return the corrected `treatments` array only.""",

    "source_quality": """\
Your task: Normalize the `type` field in all `sources` entries.

Replace non-standard type values with only these allowed values:
guideline, phase3_rct, phase2_trial, phase1_trial, meta_analysis,
network_meta_analysis, regulatory, clinical_trial_registry,
conference_abstract, review, case_series

Mapping rules:
- "Phase 3 RCT", "Phase III Trial", "Randomized Controlled Trial" -> phase3_rct
- "Phase 2 Trial", "Phase II Clinical Trial" -> phase2_trial
- "Review Article", "Narrative review", "Comprehensive Review" -> review
- "Clinical Guideline", "Clinical Practice Guideline", "NCCN" -> guideline
- "FDA Approval", "Regulatory Approval", "Regulatory" -> regulatory
- "Conference Abstract", "ASCO Abstract", "conference" -> conference_abstract
- "Meta-analysis", "Systematic Review", "Systematic Review / Meta-Analysis" -> meta_analysis

Return the corrected `sources` array only.""",
}


# ── Ollama Helpers ─────────────────────────────────────────────────────────────

def ollama_running() -> bool:
    try:
        urllib.request.urlopen(f"{OLLAMA_BASE}/api/tags", timeout=3)
        return True
    except Exception:
        return False


def ollama_generate(prompt: str, model: str = PRESCORE_MODEL, timeout: int = 120) -> Optional[str]:
    payload = json.dumps({
        "model":  model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 512},
    }).encode()
    req = urllib.request.Request(
        f"{OLLAMA_BASE}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
            return data.get("response", "").strip()
    except Exception as e:
        return None


# ── Gap Detection ──────────────────────────────────────────────────────────────

def find_evidence_gaps(report: dict) -> "list[str]":
    """Return list of specific missing evidence fields across treatments."""
    gaps = []
    for t in report.get("treatments", []):
        name = t.get("name", "?")[:50]
        ke   = t.get("key_evidence", {})
        os_d = ke.get("os_months", {})

        if not t.get("intent"):
            gaps.append(f"[intent missing] {name}")
        if not ke.get("study_name"):
            gaps.append(f"[no study name] {name}")
        if not ke.get("sample_size"):
            gaps.append(f"[no sample_size] {name}")
        if os_d.get("treatment") is None:
            gaps.append(f"[no OS treatment arm] {name}")
        if os_d.get("control") is None:
            gaps.append(f"[no OS control arm] {name}")
        if os_d.get("hazard_ratio") is None:
            gaps.append(f"[no HR] {name}")
        if os_d.get("p_value") is None:
            gaps.append(f"[no p-value] {name}")
    return gaps


def find_rating_violations(report: dict) -> "list[str]":
    """Detect evidence_level/survival_benefit scores inconsistent with study type."""
    violations = []
    for t in report.get("treatments", []):
        name = t.get("name", "?")[:50]
        rb   = t.get("rating_breakdown", {})
        ke   = t.get("key_evidence", {})
        ev   = rb.get("evidence_level", {}).get("score", 0)
        sv   = rb.get("survival_benefit", {}).get("score", 0)
        rationale = rb.get("evidence_level", {}).get("rationale", "").lower()
        os_d = ke.get("os_months", {})

        # Check evidence_level vs study phase
        is_p3 = any(x in rationale for x in ["phase 3", "phase iii", "rct", "randomized"])
        is_p2 = any(x in rationale for x in ["phase 2", "phase ii"])
        is_p1 = any(x in rationale for x in ["phase 1", "phase i ", "dose-escal"])

        if ev >= 8 and is_p2 and not is_p3:
            violations.append(f"[ev_level={ev} but Phase2] {name}")
        if ev >= 8 and is_p1:
            violations.append(f"[ev_level={ev} but Phase1] {name}")

        # Check survival_benefit vs OS delta
        os_trt = os_d.get("treatment")
        os_ctl = os_d.get("control")
        if os_trt is not None and os_ctl is not None:
            try:
                delta = float(os_trt) - float(os_ctl)
                if sv >= 8 and delta < 3:
                    violations.append(f"[sv={sv} but delta={delta:.1f}mo] {name}")
                if sv >= 9 and delta < 6:
                    violations.append(f"[sv={sv} but delta={delta:.1f}mo] {name}")
            except (TypeError, ValueError):
                pass

    return violations


def find_source_type_violations(report: dict) -> "list[str]":
    """Find sources with non-standard type values."""
    VALID = {"guideline","phase3_rct","phase2_trial","phase1_trial","meta_analysis",
             "network_meta_analysis","regulatory","clinical_trial_registry",
             "conference_abstract","review","case_series"}
    bad = []
    for s in report.get("sources", []):
        t = s.get("type","")
        if t.lower() not in VALID:
            bad.append(f"[type='{t}'] {s.get('title','?')[:60]}")
    return bad


def llm_summarize_gaps(case_id: str, gaps: "list[str]", score: int) -> str:
    """Use llama3.2:3b to write a 2-sentence gap summary for the task prompt."""
    if not ollama_running() or not gaps:
        return f"{len(gaps)} gaps found."
    prompt = (
        f"Cancer research report {case_id} scored {score}/100. "
        f"Specific data gaps found:\n" + "\n".join(f"- {g}" for g in gaps[:10]) +
        "\n\nWrite exactly 2 sentences summarizing the most critical gaps "
        "and why fixing them will improve the score. Be specific. No preamble."
    )
    result = ollama_generate(prompt, timeout=60)
    return result or f"{len(gaps)} gaps found."


# ── Task Generation ────────────────────────────────────────────────────────────

def generate_task(report: dict, report_path: str, score: int, dims: dict,
                  focus_dim: Optional[str], llm_summary: str) -> str:
    """Build the Claude API re-evaluation prompt for this report."""
    meta = report.get("report_metadata", {})
    case_id  = meta.get("case_id", os.path.basename(report_path).replace("_report.json",""))
    cancer   = meta.get("cancer_type", "Unknown")
    stage    = meta.get("stage", "Unknown")
    mol      = ", ".join(meta.get("molecular_profile", []))

    # Determine what to fix
    worst_dim = focus_dim or min(dims, key=lambda d: dims[d].get("pct", 100))
    fix_instructions = DIMENSION_FIX_INSTRUCTIONS.get(worst_dim, "")

    dim_table = "\n".join(
        f"| {k:<35} | {v['score']:>3}/{v['max']:<3} | {v['pct']:>5.1f}% |"
        for k, v in sorted(dims.items(), key=lambda x: x[1]["pct"])
    )

    prompt = f"""# Re-evaluation Task: {case_id}

## Context
- **Case ID**: {case_id}
- **Cancer type**: {cancer}
- **Stage**: {stage}
- **Molecular profile**: {mol}
- **Report file**: {report_path}
- **Current score**: {score}/100
- **Gap analysis (local GPU)**: {llm_summary}

## Current dimension scores
| Dimension | Score | % of max |
|---|---|---|
{dim_table}

## Target dimension: `{worst_dim}` ({dims.get(worst_dim, {}).get('pct', 0):.1f}% of max)

## Your instructions

Read the full report JSON at `{report_path}`.

{fix_instructions}

## Output format

Return a valid JSON object containing ONLY the corrected section (e.g., `{{"treatments": [...]}}` or `{{"sources": [...]}}`).

Do NOT return the full report — only the corrected array. The runner will merge it back.

After returning the JSON, add one line:
`SCORE_IMPACT: <estimated new score>/100`

## Report JSON (for reference)

```json
{json.dumps({"report_metadata": meta, "treatments": report.get("treatments", [])[:3]}, indent=2, ensure_ascii=False)[:3000]}
... (truncated — read full file from {report_path})
```
"""
    return prompt


# ── Execution (Claude API) ─────────────────────────────────────────────────────

def execute_task(task_path: str, report_path: str, model: str, api_key: str) -> dict:
    """Send task to Claude API, parse response, patch report JSON."""
    try:
        import anthropic
    except ImportError:
        print("  ERROR: pip install anthropic")
        return {"status": "error", "reason": "anthropic not installed"}

    with open(task_path, encoding="utf-8") as f:
        task_text = f.read()
    with open(report_path, encoding="utf-8") as f:
        full_report = json.load(f)

    client = anthropic.Anthropic(api_key=api_key)
    print(f"  Calling {model}...")

    try:
        message = client.messages.create(
            model=model,
            max_tokens=8192,
            messages=[{"role": "user", "content": task_text}],
        )
        response_text = message.content[0].text
    except Exception as e:
        return {"status": "error", "reason": str(e)}

    # Extract JSON from response
    import re
    json_match = re.search(r'\{[\s\S]+\}', response_text)
    if not json_match:
        return {"status": "error", "reason": "no JSON in response"}

    try:
        patch = json.loads(json_match.group())
    except json.JSONDecodeError as e:
        return {"status": "error", "reason": f"JSON parse error: {e}"}

    # Merge patch into report
    for key, value in patch.items():
        if key in full_report:
            full_report[key] = value

    # Update metadata
    full_report.setdefault("report_metadata", {})["last_reevaluated"] = datetime.now().isoformat()[:10]

    # Save patched report
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(full_report, f, indent=2, ensure_ascii=False)

    # Extract score impact if mentioned
    score_line = re.search(r'SCORE_IMPACT:\s*([\d.]+)/100', response_text)
    estimated = float(score_line.group(1)) if score_line else None

    return {
        "status": "ok",
        "estimated_score": estimated,
        "patch_keys": list(patch.keys()),
        "tokens_used": message.usage.input_tokens + message.usage.output_tokens,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Local GPU gap analysis + Claude API re-evaluation task generator"
    )
    parser.add_argument("--reports",   default="experiment_reports",
                        help="Directory containing *_report.json files (default: experiment_reports)")
    parser.add_argument("--threshold", type=float, default=88.0,
                        help="Generate tasks for reports below this score (default: 88)")
    parser.add_argument("--focus",     choices=list(DIMENSION_MAX.keys()),
                        help="Only fix this dimension (default: auto-detect worst)")
    parser.add_argument("--limit",     type=int, default=0,
                        help="Max tasks to generate (default: 0 = all)")
    parser.add_argument("--dry-run",   action="store_true",
                        help="Print analysis without writing task files")
    parser.add_argument("--execute",   action="store_true",
                        help="Execute tasks via Claude API after generating")
    parser.add_argument("--model",     default="claude-opus-4-6",
                        help="Claude model for --execute (default: claude-opus-4-6)")
    parser.add_argument("--api-key",   default=os.environ.get("ANTHROPIC_API_KEY",""),
                        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)")
    parser.add_argument("--no-llm",    action="store_true",
                        help="Skip llama3.2:3b gap summaries (faster, less detail)")
    args = parser.parse_args()

    # Check ollama
    llm_available = ollama_running() and not args.no_llm
    if llm_available:
        print(f"[ok] ollama running — using {PRESCORE_MODEL} for gap summaries")
    else:
        print("[--] ollama not available — gap summaries will be basic")

    # Load evaluate.py
    sys.path.insert(0, os.path.dirname(__file__) or ".")
    import evaluate

    # Find reports
    patterns = [
        os.path.join(args.reports, "*_report.json"),
        os.path.join(args.reports, "**", "*_report.json"),
    ]
    report_files = []
    for pat in patterns:
        report_files.extend(glob.glob(pat, recursive=True))
    report_files = sorted(set(report_files))
    print(f"\nFound {len(report_files)} reports in '{args.reports}'")

    # Score all reports
    print("Scoring reports locally...")
    scored = []
    for path in report_files:
        try:
            with open(path, encoding="utf-8") as f:
                report = json.load(f)
            result  = evaluate.evaluate_report(report)
            score   = result["quality_score"]
            dims    = result["dimensions"]
            scored.append((score, path, report, dims))
        except Exception as e:
            print(f"  SKIP {path}: {e}")

    scored.sort(key=lambda x: x[0])  # worst first

    # Filter by threshold
    needs_work = [(s, p, r, d) for s, p, r, d in scored if s < args.threshold]
    if args.focus:
        needs_work = [(s, p, r, d) for s, p, r, d in needs_work
                      if d.get(args.focus, {}).get("pct", 100) < 80]

    print(f"Reports below {args.threshold}/100: {len(needs_work)}")
    if args.focus:
        print(f"  (filtered to {args.focus} < 80%)")

    if args.limit:
        needs_work = needs_work[:args.limit]
        print(f"  (limited to top {args.limit})")

    if not needs_work:
        print("Nothing to do — all reports meet threshold.")
        return

    # Create tasks dir
    if not args.dry_run:
        os.makedirs(TASKS_DIR, exist_ok=True)

    # Generate tasks
    print(f"\nGenerating tasks -> {TASKS_DIR}/")
    manifest = []
    for score, path, report, dims in needs_work:
        case_id = os.path.basename(path).replace("_report.json","")
        worst_dim = args.focus or min(dims, key=lambda d: dims[d].get("pct", 100))
        worst_pct = dims.get(worst_dim, {}).get("pct", 0)

        # Detect specific gaps
        ev_gaps   = find_evidence_gaps(report)
        rt_gaps   = find_rating_violations(report)
        src_gaps  = find_source_type_violations(report)
        all_gaps  = ev_gaps + rt_gaps + src_gaps

        # LLM summary
        if llm_available and all_gaps:
            llm_summary = llm_summarize_gaps(case_id, all_gaps, score)
        else:
            llm_summary = f"{len(all_gaps)} gaps: {'; '.join(all_gaps[:3])}" if all_gaps else "No specific gaps detected."

        # Score impact estimate
        gap_deduction = len(ev_gaps)*0.3 + len(rt_gaps)*0.5
        est_gain = min(gap_deduction, 15)

        print(f"\n  {case_id}  score={score}/100  {worst_dim}={worst_pct:.0f}%  gaps={len(all_gaps)}")
        print(f"    est_gain: +{est_gain:.1f}pts  ->  {score+est_gain:.0f}/100")
        print(f"    {llm_summary[:120]}")

        if not args.dry_run:
            task_text = generate_task(report, path, score, dims, args.focus, llm_summary)
            task_path = os.path.join(TASKS_DIR, f"reeval_{case_id}.md")
            with open(task_path, "w", encoding="utf-8") as f:
                f.write(task_text)

            manifest.append({
                "case_id":      case_id,
                "report_path":  path,
                "task_path":    task_path,
                "current_score": score,
                "est_new_score": round(score + est_gain, 1),
                "est_gain":     round(est_gain, 1),
                "target_dim":   worst_dim,
                "dim_pct":      worst_pct,
                "gap_count":    len(all_gaps),
                "llm_summary":  llm_summary,
            })

    if args.dry_run:
        print(f"\n[dry-run] would generate {len(needs_work)} task files in {TASKS_DIR}/")
        return

    # Write manifest
    manifest.sort(key=lambda x: -x["est_gain"])
    manifest_path = os.path.join(TASKS_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "threshold":    args.threshold,
            "focus_dim":    args.focus,
            "total_tasks":  len(manifest),
            "total_est_gain": round(sum(t["est_gain"] for t in manifest) / max(len(manifest),1), 1),
            "tasks": manifest,
        }, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Tasks written: {len(manifest)}")
    print(f"Manifest:      {manifest_path}")
    if manifest:
        total_gain = sum(t["est_gain"] for t in manifest) / len(manifest)
        print(f"Est. avg gain: +{total_gain:.1f} pts/report")
        print(f"Highest gain:  {manifest[0]['case_id']} (+{manifest[0]['est_gain']:.1f}pts)")
        print(f"\nTo execute with Claude API:")
        print(f"  python local_task_generator.py --execute --api-key sk-ant-...")
    print(f"{'='*60}")

    # Execute
    if args.execute:
        if not args.api_key:
            print("ERROR: --api-key required for --execute")
            sys.exit(1)
        print(f"\nExecuting {len(manifest)} tasks via {args.model}...")
        results = []
        for task in manifest:
            print(f"\n  [{task['case_id']}] {task['current_score']}/100 -> target {task['est_new_score']}/100")
            result = execute_task(task["task_path"], task["report_path"], args.model, args.api_key)
            result["case_id"] = task["case_id"]
            results.append(result)
            if result["status"] == "ok":
                print(f"    OK  est={result['estimated_score']}  tokens={result['tokens_used']}")
            else:
                print(f"    FAIL: {result['reason']}")

        ok = [r for r in results if r["status"] == "ok"]
        print(f"\nCompleted: {len(ok)}/{len(results)} successful")
        exec_path = os.path.join(TASKS_DIR, "execution_results.json")
        with open(exec_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"Results:   {exec_path}")


if __name__ == "__main__":
    main()
