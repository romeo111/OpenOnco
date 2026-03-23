#!/usr/bin/env python3
"""
local_llm.py — Local GPU inference via Ollama for Cancer AutoResearch

Two models with complementary strengths:
  llama3.2:3b  (~2 GB, fast, structured JSON output)
               → pre-scoring reports, format validation
  phi3:mini    (~2.2 GB, Microsoft reasoning-tuned)
               → semantic strategy.md mutation proposals

Both fit simultaneously in RTX 5050 8 GB VRAM (~6 GB combined).

Requires ollama running locally: https://ollama.ai
    ollama pull llama3.2:3b
    ollama pull phi3:mini

Usage:
    python local_llm.py check
    python local_llm.py prescore experiment_reports/HN-001_report.json
    python local_llm.py suggest-edit --last-run experiment_reports/last_run_scores.json
    python local_llm.py suggest-edit --output strategy_semantic.md
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from typing import Optional

OLLAMA_BASE  = "http://localhost:11434"
FILTER_MODEL = "llama3.2:3b"   # fast, JSON-structured output
MUTATE_MODEL = "phi3:mini"     # better multi-step reasoning

# Maps evaluate.py dimension names → strategy.md section headers
_DIM_TO_SECTION = {
    "evidence_depth":             "## Search Budget Allocation",
    "source_quality":             "## Source Fetch Prioritization",
    "rating_calibration":         "## Rating Calibration Rubric",
    "tier_coverage":              "## Search Budget Allocation",
    "combo_supportive_coverage":  "## Combination Strategy Guidance",
    "clinical_relevance":         "## Treatment Inclusion Criteria",
    "structural_integrity":       "## Data Density Targets",
}


# ── Ollama Connectivity ────────────────────────────────────────────────────────

def check_ollama() -> bool:
    """Return True if ollama API is reachable at localhost:11434."""
    try:
        req = urllib.request.urlopen(f"{OLLAMA_BASE}/api/tags", timeout=3)
        return req.status == 200
    except Exception:
        return False


def list_models() -> list:
    """Return list of model names currently pulled in ollama."""
    try:
        req = urllib.request.urlopen(f"{OLLAMA_BASE}/api/tags", timeout=5)
        data = json.loads(req.read().decode())
        return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []


def is_model_available(model: str) -> bool:
    """Check if model is already pulled (handles 'phi3:mini' == 'phi3' normalization)."""
    available = list_models()
    model_base = model.split(":")[0]
    for m in available:
        if m == model or m.startswith(model_base + ":") or m == model_base:
            return True
    return False


def ensure_models(verbose: bool = True) -> dict:
    """Check required models. Returns {model: bool}. Does NOT auto-pull."""
    status = {}
    for model in [FILTER_MODEL, MUTATE_MODEL]:
        ok = is_model_available(model)
        status[model] = ok
        if verbose:
            tag = "[ok]     " if ok else "[MISSING]"
            hint = "" if ok else f"  →  ollama pull {model}"
            print(f"  {tag} {model}{hint}")
    return status


# ── Core Generation ────────────────────────────────────────────────────────────

def generate(
    model: str,
    prompt: str,
    temperature: float = 0.3,
    json_format: bool = False,
    timeout: int = 90,
) -> Optional[str]:
    """
    Call ollama /api/generate (non-streaming).
    Returns response text, or None on any failure.
    """
    payload: dict = {
        "model":   model,
        "prompt":  prompt,
        "stream":  False,
        "options": {"temperature": temperature},
    }
    if json_format:
        payload["format"] = "json"

    try:
        data = json.dumps(payload).encode()
        req  = urllib.request.Request(
            f"{OLLAMA_BASE}/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        resp   = urllib.request.urlopen(req, timeout=timeout)
        result = json.loads(resp.read().decode())
        return result.get("response", "").strip()
    except urllib.error.URLError as e:
        print(f"  [local_llm] ollama request failed: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  [local_llm] generate error: {e}", file=sys.stderr)
        return None


# ── Pre-Scoring (llama3.2:3b) ─────────────────────────────────────────────────

def prescore_report(report_path: str) -> Optional[float]:
    """
    Fast quality pre-score (0-100) using llama3.2:3b.
    Much cheaper than running full evaluate.py on a 130-case benchmark.
    Returns estimated score or None if model unavailable.
    """
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            report = json.load(f)
    except Exception:
        return None

    treatments = report.get("treatments", [])
    trials     = report.get("clinical_trials", [])
    combos     = report.get("combination_strategies", [])
    supportive = report.get("supportive_care", [])
    sources    = report.get("sources", [])

    with_os = sum(
        1 for t in treatments
        if t.get("key_evidence", {}).get("os_months", {}).get("treatment") is not None
    )
    with_urls = sum(1 for t in treatments if t.get("source_urls"))

    prompt = f"""Rate this cancer research report quality. Output JSON only.

Report statistics:
- Treatments: {len(treatments)} (good: 8-15)
- Treatments with OS survival data: {with_os}/{len(treatments)} (good: >50%)
- Treatments with source URLs: {with_urls}/{len(treatments)} (good: all)
- Clinical trials listed: {len(trials)} (good: 3+)
- Combination strategies: {len(combos)} (good: 4+)
- Supportive care items: {len(supportive)} (good: 4+)
- Total sources cited: {len(sources)} (good: 12-15)
- Has tier 1 (standard of care): {"yes" if any(t.get("tier") == 1 for t in treatments) else "no"}
- Has tier 4 (experimental): {"yes" if any(t.get("tier") in [4, 5] for t in treatments) else "no"}

Output JSON: {{"score": <integer 0-100>, "main_weakness": "<one phrase>"}}"""

    response = generate(FILTER_MODEL, prompt, temperature=0.1, json_format=True, timeout=30)
    if not response:
        return None

    try:
        data  = json.loads(response)
        score = float(data.get("score", 0))
        return max(0.0, min(100.0, score))
    except (json.JSONDecodeError, ValueError, TypeError):
        nums = re.findall(r"\b(\d{1,3})\b", response or "")
        for n in nums:
            val = float(n)
            if 0 <= val <= 100:
                return val
        return None


def prescore_batch(report_paths: list, verbose: bool = True) -> dict:
    """
    Pre-score multiple reports. Returns {path: score}.
    Useful for fast screening before committing to a full 130-case benchmark.
    """
    results = {}
    for path in report_paths:
        score = prescore_report(path)
        results[path] = score
        if verbose:
            label = f"{score:.1f}/100" if score is not None else "FAILED"
            name  = os.path.basename(path)
            print(f"  pre-score [{name}]: {label}")
    return results


# ── Semantic Strategy Mutation (phi3:mini) ────────────────────────────────────

def _extract_section(strategy_content: str, section_header: str) -> Optional[str]:
    """Extract text from ## Section Header to the next ## header (or EOF)."""
    pattern = re.escape(section_header)
    m = re.search(rf"({pattern}.*?)(?=\n##\s|\Z)", strategy_content, re.DOTALL)
    return m.group(1).strip() if m else None


def _replace_section(strategy_content: str, section_header: str, new_section: str) -> Optional[str]:
    """Replace the named section in strategy_content with new_section text."""
    pattern = re.escape(section_header)
    new_content, count = re.subn(
        rf"({pattern}.*?)(?=\n##\s|\Z)",
        lambda _: new_section.rstrip(),
        strategy_content,
        count=1,
        flags=re.DOTALL,
    )
    return new_content if count > 0 else None


def suggest_strategy_edit(
    strategy_content: str,
    weak_dims: dict,   # {dim_name: pct_of_max (0.0–1.0)}
) -> Optional[str]:
    """
    Use phi3:mini to propose a semantic edit to strategy.md for the weakest
    scoring dimension.

    Returns the full modified strategy.md text, or None on failure.
    """
    if not weak_dims:
        return None

    worst_dim  = min(weak_dims, key=lambda d: weak_dims[d])
    worst_pct  = weak_dims[worst_dim] * 100
    section_hdr = _DIM_TO_SECTION.get(worst_dim)
    if not section_hdr:
        return None

    section_text = _extract_section(strategy_content, section_hdr)
    if not section_text:
        return None

    prompt = f"""You are editing a Markdown configuration file that controls how a cancer research AI searches for treatments.

The weakest scoring dimension in recent experiments is:
  Dimension: {worst_dim.replace("_", " ")}
  Current score: {worst_pct:.0f}% of maximum

Here is the section responsible for this dimension:

---
{section_text}
---

Your task: Propose ONE specific, minimal change to improve {worst_dim.replace("_", " ")}.

Rules:
- Output ONLY the modified section text, starting with {section_hdr}
- Keep all Markdown table formatting intact (pipes, dashes, column alignment)
- Change exactly ONE thing (a number, a threshold, an added requirement, a reworded criterion)
- Do NOT add explanations or comments after the section
- Do NOT change any other section

Begin output now with {section_hdr}:"""

    modified_section = generate(MUTATE_MODEL, prompt, temperature=0.35, timeout=90)
    if not modified_section:
        return None

    # Clean: ensure it starts with the section header
    if section_hdr not in modified_section:
        idx = modified_section.find("##")
        if idx >= 0:
            modified_section = modified_section[idx:]
        else:
            return None

    # Strip anything the LLM added after the section (next ## or explanatory text)
    next_section = re.search(r"\n##\s", modified_section)
    if next_section:
        modified_section = modified_section[:next_section.start()]

    return _replace_section(strategy_content, section_hdr, modified_section)


# ── High-Level Variant Generator ───────────────────────────────────────────────

def generate_semantic_variant(
    strategy_content: str,
    last_run_path: str = "experiment_reports/last_run_scores.json",
) -> Optional[tuple]:
    """
    Read last run's dimension scores, identify weakest dimension, call
    suggest_strategy_edit(), and return (modified_strategy_str, mutation_dict).

    Returns None if ollama is unreachable, models missing, or generation fails.
    Called by auto_loop.py when --local-llm is set.
    """
    if not check_ollama():
        print("  [local_llm] ollama not reachable — skipping semantic variant", file=sys.stderr)
        return None

    if not is_model_available(MUTATE_MODEL):
        print(f"  [local_llm] {MUTATE_MODEL} not available — run: ollama pull {MUTATE_MODEL}",
              file=sys.stderr)
        return None

    if not os.path.exists(last_run_path):
        print(f"  [local_llm] no last-run data at {last_run_path}", file=sys.stderr)
        return None

    try:
        with open(last_run_path, "r", encoding="utf-8") as f:
            run_data = json.load(f)
    except Exception as e:
        print(f"  [local_llm] failed to read last-run: {e}", file=sys.stderr)
        return None

    cases = [c for c in run_data.get("cases", [])
             if c.get("status") == "evaluated" and c.get("dimensions")]
    if not cases:
        return None

    # Compute pct-of-max for each dimension across all evaluated cases
    dim_pcts: dict = {}
    for dim in cases[0]["dimensions"]:
        scores = []
        for case in cases:
            d  = case["dimensions"].get(dim, {})
            mx = d.get("max", 1)
            sc = d.get("score", 0)
            if mx > 0:
                scores.append(sc / mx)
        if scores:
            dim_pcts[dim] = sum(scores) / len(scores)

    worst_dim = min(dim_pcts, key=lambda d: dim_pcts[d])
    print(f"  [local_llm] targeting weakest dimension: {worst_dim} "
          f"({dim_pcts[worst_dim]*100:.0f}%)")

    new_strategy = suggest_strategy_edit(strategy_content, dim_pcts)
    if not new_strategy:
        print("  [local_llm] phi3:mini returned no valid edit", file=sys.stderr)
        return None

    mutation = {
        "knob":  f"semantic_{worst_dim}",
        "from":  f"{dim_pcts[worst_dim]*100:.0f}% avg",
        "to":    "llm_edit",
        "type":  "semantic",
        "model": MUTATE_MODEL,
    }
    return new_strategy, mutation


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Local Ollama LLM helper for cancer autoresearch loop"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # check
    sub.add_parser("check", help="Check ollama status and model availability")

    # prescore
    p_pre = sub.add_parser("prescore", help="Fast pre-score a report JSON")
    p_pre.add_argument("report", help="Path to report JSON file")

    # prescore-batch
    p_batch = sub.add_parser("prescore-batch", help="Pre-score all JSON files in a directory")
    p_batch.add_argument("directory", help="Directory containing report JSON files")

    # suggest-edit
    p_sug = sub.add_parser("suggest-edit",
                            help="Propose semantic strategy.md edit from last run data")
    p_sug.add_argument("--strategy",  default="strategy.md")
    p_sug.add_argument("--last-run",  default="experiment_reports/last_run_scores.json")
    p_sug.add_argument("--output",    default=None,
                       help="Write modified strategy to this file (default: stdout)")

    args = parser.parse_args()

    if args.command == "check":
        if check_ollama():
            print("ollama is running at localhost:11434")
            ensure_models(verbose=True)
        else:
            print("ollama is NOT running.")
            print("Start with:  ollama serve")
            print("Then pull:   ollama pull llama3.2:3b && ollama pull phi3:mini")
            sys.exit(1)

    elif args.command == "prescore":
        if not check_ollama():
            print("ollama not running", file=sys.stderr); sys.exit(1)
        score = prescore_report(args.report)
        if score is None:
            print("Pre-score failed", file=sys.stderr); sys.exit(1)
        print(f"Pre-score: {score:.1f}/100")

    elif args.command == "prescore-batch":
        if not check_ollama():
            print("ollama not running", file=sys.stderr); sys.exit(1)
        paths = [
            os.path.join(args.directory, f)
            for f in os.listdir(args.directory)
            if f.endswith("_report.json")
        ]
        if not paths:
            print("No *_report.json files found"); sys.exit(1)
        results = prescore_batch(sorted(paths))
        scores  = [s for s in results.values() if s is not None]
        if scores:
            print(f"\nMean pre-score: {sum(scores)/len(scores):.1f}/100 ({len(scores)} reports)")

    elif args.command == "suggest-edit":
        if not check_ollama():
            print("ollama not running", file=sys.stderr); sys.exit(1)
        with open(args.strategy, "r", encoding="utf-8") as f:
            strategy = f.read()
        result = generate_semantic_variant(strategy, args.last_run)
        if result is None:
            print("Suggestion failed (model unavailable or insufficient data)", file=sys.stderr)
            sys.exit(1)
        new_strategy, mutation = result
        print(f"Mutation: {mutation['knob']} ({mutation['from']} → {mutation['to']})")
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(new_strategy)
            print(f"Written to: {args.output}")
        else:
            print("\n" + "=" * 60)
            print(new_strategy)


if __name__ == "__main__":
    main()
