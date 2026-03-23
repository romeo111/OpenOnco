#!/usr/bin/env python3
"""
worker.py — Distributed Worker Client for Cancer AutoResearch Platform

Connects to the orchestrator server and processes research jobs in a loop.
Supports two modes:
  --mode local   Use ollama to run a local LLM (llama3.1:70b or best available)
  --mode claude  Use Anthropic API with claude-opus-4-6

For --mode claude, the ANTHROPIC_API_KEY environment variable must be set.

Usage:
    python worker.py --server http://localhost:8765 --mode local
    python worker.py --server http://localhost:8765 --mode claude --worker-id my-node-01
    python worker.py --server http://localhost:8765 --mode local --model llama3.2:3b
    python worker.py --server http://localhost:8765 --mode claude --max-jobs 10
    python worker.py --server http://localhost:8765 --mode local --dry-run
"""

import argparse
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


# ── Constants ─────────────────────────────────────────────────────────────────

VERSION = "1.0.0"
DEFAULT_SERVER = "http://localhost:8765"
OLLAMA_BASE = "http://localhost:11434"
MUTATION_PROPOSE_EVERY = 5       # propose a mutation every N jobs
RETRY_DELAY_SECONDS = 30         # wait between retries on no-job or error
MAX_RETRY_BACKOFF = 300          # cap backoff at 5 minutes
RESEARCH_TIMEOUT_LOCAL = 180     # seconds for local LLM generation
RESEARCH_TIMEOUT_CLAUDE = 120    # seconds for Claude API call


# ── HTTP Client Helpers ───────────────────────────────────────────────────────

def _http_get(url: str, timeout: int = 30) -> Optional[dict]:
    try:
        req = urllib.request.urlopen(url, timeout=timeout)
        return json.loads(req.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  [http] GET {url} -> {e.code}: {body[:200]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  [http] GET {url} failed: {e}", file=sys.stderr)
        return None


def _http_post(url: str, payload: dict, timeout: int = 60) -> Optional[dict]:
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=timeout)
        return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  [http] POST {url} -> {e.code}: {body[:200]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  [http] POST {url} failed: {e}", file=sys.stderr)
        return None


# ── Local Evaluator ───────────────────────────────────────────────────────────

def evaluate_report_local(report_data: dict) -> Tuple[float, dict]:
    """
    Score a report JSON using evaluate.py.
    Returns (quality_score, quality_dimensions).
    Falls back to 0.0 if evaluate.py is unavailable.
    """
    try:
        # evaluate.py must be importable from the same directory
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from evaluate import evaluate_report
        result = evaluate_report(report_data)
        score = float(result.get("quality_score", 0.0))
        dims = {}
        for dim_name, dim_data in result.get("dimensions", {}).items():
            dims[dim_name] = {
                "score": dim_data.get("score", 0),
                "max": dim_data.get("max", 0),
                "pct": dim_data.get("pct", 0.0),
            }
        return score, dims
    except ImportError:
        print("  [worker] evaluate.py not found — scoring skipped", file=sys.stderr)
        return 0.0, {}
    except Exception as e:
        print(f"  [worker] evaluation error: {e}", file=sys.stderr)
        return 0.0, {}


# ── Research Prompt Builder ───────────────────────────────────────────────────

def _build_research_prompt(case_data: dict, strategy_content: str) -> str:
    """Build the research prompt from case data and strategy content."""
    ctx = case_data.get("patient_context", {})
    markers = ", ".join(case_data.get("molecular_markers", []))
    risk_factors = ", ".join(ctx.get("risk_factors", []))
    comorbidities = ", ".join(ctx.get("comorbidities", [])) or "none"

    cancer_type = case_data.get("cancer_type", "unknown")
    stage = case_data.get("stage", "unknown")
    age = ctx.get("age", "unknown")
    sex = ctx.get("sex", "unknown")
    ps = ctx.get("performance_status", "unknown")

    return f"""You are a cancer treatment research specialist. Research the following case and
produce a comprehensive, evidence-ranked treatment report in JSON format.

## Patient Case
- Cancer type: {cancer_type}
- Stage: {stage}
- Molecular markers: {markers or 'none specified'}
- Patient: {age} year old {sex}
- Performance status: {ps}
- Risk factors: {risk_factors or 'none'}
- Comorbidities: {comorbidities}

## Research Strategy
Follow this strategy for search queries, source prioritization, rating calibration,
and output structure:

{strategy_content}

## Output Requirements
Produce a JSON report with these top-level keys:
- report_metadata: {{cancer_type, stage, generated_date, molecular_profile, disclaimer}}
- treatments: list of 8-15 treatments, each with:
  - rank, name, category, intent, availability, composite_rating
  - rating_breakdown: {{evidence_level, survival_benefit, accessibility, safety_profile, biomarker_match}}
    each factor: {{score (1-10), rationale}}
  - key_evidence: {{study_name, journal, year, sample_size,
    os_months: {{treatment, control, hazard_ratio, p_value}},
    pfs_months: {{treatment, control}},
    orr_percent: {{treatment}}}}
  - biomarker_requirements: list
  - notable_side_effects: list
  - source_urls: list of at least 1 URL
  - ps_requirement (if applicable)
  - qol_impact (for H&N, lung, GI cancers)
- clinical_trials: list of 3+ active trials with trial_id (NCT number), title, phase,
  status, eligibility_key_points, url
- combination_strategies: list of 4+ combos with base_therapy, combination_partner,
  evidence_level, rationale (≥20 words), source_url
- supportive_care: list of 4+ approaches with approach, evidence, benefit,
  recommendation_level
- sources: list of 10-15 sources, each with url, title, type, year
- methodology: {{searches_performed, tiers_covered, date_range}}

IMPORTANT: Output ONLY valid JSON, starting with {{ and ending with }}.
Do not include markdown code blocks, explanatory text, or any content outside the JSON.
"""


def _extract_json_from_response(text: str) -> Optional[dict]:
    """Extract JSON from LLM response, handling markdown code blocks and leading text."""
    if not text:
        return None

    # Try direct parse first
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strip markdown code block
    import re
    code_block = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if code_block:
        try:
            return json.loads(code_block.group(1))
        except json.JSONDecodeError:
            pass

    # Find first { and last }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    return None


# ── Worker Class ──────────────────────────────────────────────────────────────

class Worker:
    """Distributed research worker that connects to the orchestrator."""

    def __init__(
        self,
        server_url: str,
        mode: str,
        worker_id: str,
        model: str,
        max_jobs: int,
        dry_run: bool = False,
        verbose: bool = True,
    ):
        self.server_url = server_url.rstrip("/")
        self.mode = mode
        self.worker_id = worker_id
        self.model = model
        self.max_jobs = max_jobs
        self.dry_run = dry_run
        self.verbose = verbose

        self.jobs_completed = 0
        self.jobs_failed = 0
        self.total_score = 0.0
        self.current_strategy_hash: Optional[str] = None
        self.current_strategy_content: str = ""

        # Claude client (lazy init)
        self._claude_client: Optional[Any] = None

    # ── Registration ──────────────────────────────────────────────────────────

    def register(self) -> bool:
        """Register this worker with the orchestrator."""
        gpu_model = self._detect_gpu()
        payload = {
            "worker_id": self.worker_id,
            "mode": self.mode,
            "gpu_model": gpu_model,
        }
        resp = _http_post(f"{self.server_url}/register", payload)
        if not resp:
            print(f"[worker] Registration failed — server unreachable at {self.server_url}",
                  file=sys.stderr)
            return False
        self.current_strategy_hash = resp.get("canonical_strategy_hash")
        self._log(f"Registered: worker_id={self.worker_id} mode={self.mode} "
                  f"strategy_hash={self.current_strategy_hash}")
        return True

    def _detect_gpu(self) -> Optional[str]:
        """Try to detect GPU model for registration metadata."""
        try:
            import subprocess
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip().split("\n")[0]
        except Exception:
            pass
        return None

    # ── Strategy ──────────────────────────────────────────────────────────────

    def fetch_strategy(self) -> bool:
        """Fetch the current canonical strategy from the orchestrator."""
        resp = _http_get(f"{self.server_url}/strategy")
        if not resp or "content" not in resp:
            self._log("Failed to fetch strategy", error=True)
            return False
        self.current_strategy_hash = resp["strategy_hash"]
        self.current_strategy_content = resp["content"]
        self._log(f"Strategy fetched: hash={self.current_strategy_hash} "
                  f"({len(self.current_strategy_content)} chars)")
        return True

    # ── Job Pulling ───────────────────────────────────────────────────────────

    def pull_job(self) -> Optional[dict]:
        """Pull next job from the orchestrator queue."""
        url = (f"{self.server_url}/jobs/next"
               f"?worker_id={self.worker_id}&mode={self.mode}")
        resp = _http_get(url)
        if not resp:
            return None
        if resp.get("status") == "no_jobs":
            return None  # Queue empty
        if "job_id" not in resp:
            return None
        # Update strategy from job response if newer
        if resp.get("strategy_hash") and resp["strategy_hash"] != self.current_strategy_hash:
            self.current_strategy_hash = resp["strategy_hash"]
            self.current_strategy_content = resp.get("strategy_content", self.current_strategy_content)
            self._log(f"Strategy updated by job: hash={self.current_strategy_hash}")
        return resp

    # ── Research Execution ────────────────────────────────────────────────────

    def run_research_local(self, case_data: dict) -> Optional[dict]:
        """Generate research report using local ollama LLM."""
        prompt = _build_research_prompt(case_data, self.current_strategy_content)
        model = self.model or self._best_available_ollama_model()
        if not model:
            self._log("No ollama model available", error=True)
            return None

        self._log(f"Running local inference: model={model} "
                  f"case={case_data.get('cancer_type', '?')}")

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.3, "num_predict": 8192},
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{OLLAMA_BASE}/api/generate",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            resp = urllib.request.urlopen(req, timeout=RESEARCH_TIMEOUT_LOCAL)
            result = json.loads(resp.read().decode("utf-8"))
            raw_text = result.get("response", "")
        except Exception as e:
            self._log(f"Ollama generate failed: {e}", error=True)
            return None

        return _extract_json_from_response(raw_text)

    def run_research_claude(self, case_data: dict) -> Optional[dict]:
        """Generate research report using Anthropic Claude API."""
        try:
            import anthropic
        except ImportError:
            self._log("anthropic package not installed. Run: pip install anthropic", error=True)
            return None

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            self._log("ANTHROPIC_API_KEY environment variable not set", error=True)
            return None

        if self._claude_client is None:
            self._claude_client = anthropic.Anthropic(api_key=api_key)

        prompt = _build_research_prompt(case_data, self.current_strategy_content)
        cancer_type = case_data.get("cancer_type", "unknown")
        self._log(f"Calling Claude API: model=claude-opus-4-6 case={cancer_type}")

        try:
            response = self._claude_client.messages.create(
                model="claude-opus-4-6",
                max_tokens=16000,
                messages=[{"role": "user", "content": prompt}]
            )
            raw_text = response.content[0].text if response.content else ""
        except Exception as e:
            self._log(f"Claude API call failed: {e}", error=True)
            return None

        return _extract_json_from_response(raw_text)

    # ── Result Submission ─────────────────────────────────────────────────────

    def submit_result(self, job_id: str, score: float, quality_dims: dict,
                      report_json: Optional[dict]) -> bool:
        """Submit scored result to the orchestrator."""
        payload: Dict[str, Any] = {
            "worker_id": self.worker_id,
            "score": score,
            "quality_dimensions": quality_dims,
        }
        if report_json is not None:
            payload["report_json"] = report_json

        resp = _http_post(f"{self.server_url}/jobs/{job_id}/result", payload, timeout=60)
        if not resp:
            return False
        return resp.get("status") == "accepted"

    # ── Mutation Proposal ─────────────────────────────────────────────────────

    def propose_mutation(self) -> bool:
        """
        Propose a strategy mutation using local_llm.suggest_strategy_edit.
        Only runs when local_llm.py is available and ollama is running.
        Called every MUTATION_PROPOSE_EVERY completed jobs.
        """
        if not self.current_strategy_content or not self.current_strategy_hash:
            return False

        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from local_llm import check_ollama, suggest_strategy_edit, is_model_available

            if not check_ollama():
                self._log("Ollama not running — skipping mutation proposal")
                return False

            # Build weak_dims from recent jobs (use uniform 0.5 if no data)
            weak_dims = {
                "evidence_depth": 0.5,
                "source_quality": 0.5,
                "rating_calibration": 0.5,
                "tier_coverage": 0.5,
                "combo_supportive_coverage": 0.5,
                "clinical_relevance": 0.5,
                "structural_integrity": 0.5,
            }
            new_strategy = suggest_strategy_edit(self.current_strategy_content, weak_dims)
            if not new_strategy:
                self._log("Mutation proposal returned nothing")
                return False

            payload = {
                "worker_id": self.worker_id,
                "base_hash": self.current_strategy_hash,
                "variant_content": new_strategy,
                "mutation_desc": f"semantic_edit_by_{self.worker_id}",
            }
            resp = _http_post(f"{self.server_url}/mutations/propose", payload)
            if resp and "mutation_id" in resp:
                self._log(f"Mutation proposed: id={resp['mutation_id']}")
                return True
            return False
        except ImportError:
            return False  # local_llm.py not available
        except Exception as e:
            self._log(f"Mutation proposal error: {e}", error=True)
            return False

    # ── Mutation Validation ───────────────────────────────────────────────────

    def validate_mutations(self) -> int:
        """
        Check for pending mutations to validate. Run the variant strategy on a
        fresh benchmark case and submit the score. Returns number validated.
        """
        url = f"{self.server_url}/mutations/next?worker_id={self.worker_id}"
        resp = _http_get(url)
        if not resp or resp.get("status") == "none":
            return 0

        mutation_id = resp.get("mutation_id")
        variant_content = resp.get("variant_content", "")
        if not mutation_id or not variant_content:
            return 0

        self._log(f"Validating mutation {mutation_id}: {resp.get('mutation_desc', '')}")

        # Temporarily use the variant strategy
        saved_strategy = self.current_strategy_content
        self.current_strategy_content = variant_content

        # Create a minimal synthetic test case
        test_case = {
            "id": f"validation_{mutation_id}",
            "cancer_type": "non-small cell lung cancer",
            "stage": "IIIB",
            "molecular_markers": ["PD-L1 TPS 50%", "KRAS G12C"],
            "patient_context": {
                "age": 65,
                "sex": "male",
                "performance_status": "ECOG 1",
                "risk_factors": ["smoking history"],
                "comorbidities": ["hypertension"],
            },
        }

        if self.mode == "claude":
            report_json = self.run_research_claude(test_case)
        else:
            report_json = self.run_research_local(test_case)

        # Restore original strategy
        self.current_strategy_content = saved_strategy

        if not report_json:
            self._log(f"Mutation {mutation_id} validation: research failed")
            return 0

        score, quality_dims = evaluate_report_local(report_json)
        self._log(f"Mutation {mutation_id} validation score: {score:.1f}")

        payload = {
            "worker_id": self.worker_id,
            "case_id": test_case["id"],
            "score": score,
            "quality_dimensions": quality_dims,
        }
        resp2 = _http_post(
            f"{self.server_url}/mutations/{mutation_id}/validate", payload
        )
        if resp2:
            if resp2.get("promoted"):
                self._log(f"Mutation {mutation_id} PROMOTED to canonical! "
                           f"New hash: {resp2.get('new_canonical_hash')}")
                # Fetch the new canonical strategy
                self.fetch_strategy()
            else:
                self._log(f"Mutation {mutation_id} validated "
                           f"({resp2.get('validations_so_far', '?')} validations, "
                           f"mean={resp2.get('mean_score', '?')})")
            return 1
        return 0

    # ── Best Model Detection ──────────────────────────────────────────────────

    def _best_available_ollama_model(self) -> Optional[str]:
        """Query ollama for available models and pick the best one for research."""
        preferred_order = [
            "llama3.1:70b", "llama3.1:70b-instruct-q4_K_M",
            "llama3.1:8b", "llama3.1:8b-instruct-q4_K_M",
            "llama3.2:3b", "llama3.2:3b-instruct-q4_K_M",
            "phi3:medium", "phi3:mini",
            "mistral:7b", "gemma:7b",
        ]
        try:
            req = urllib.request.urlopen(f"{OLLAMA_BASE}/api/tags", timeout=5)
            data = json.loads(req.read().decode())
            available = [m["name"] for m in data.get("models", [])]
            for preferred in preferred_order:
                base = preferred.split(":")[0]
                for avail in available:
                    if avail == preferred or avail.startswith(base + ":") or avail == base:
                        return avail
            # Fall back to first available
            return available[0] if available else None
        except Exception:
            return None

    def _check_ollama_available(self) -> bool:
        """Check if ollama is running."""
        try:
            req = urllib.request.urlopen(f"{OLLAMA_BASE}/api/tags", timeout=3)
            return req.status == 200
        except Exception:
            return False

    # ── Logging ───────────────────────────────────────────────────────────────

    def _log(self, message: str, error: bool = False) -> None:
        if not self.verbose and not error:
            return
        ts = datetime.utcnow().strftime("%H:%M:%S")
        prefix = "[ERROR]" if error else "[worker]"
        dest = sys.stderr if error else sys.stdout
        print(f"{ts} {prefix} {message}", file=dest)

    # ── Main Loop ─────────────────────────────────────────────────────────────

    def run(self) -> None:
        """Main worker loop: register → fetch strategy → pull jobs → run → submit."""
        print(f"\n{'='*60}")
        print(f"  Cancer AutoResearch Worker v{VERSION}")
        print(f"  Worker ID: {self.worker_id}")
        print(f"  Mode:      {self.mode}")
        print(f"  Server:    {self.server_url}")
        print(f"  Model:     {self.model or 'auto-detect'}")
        print(f"  Max jobs:  {self.max_jobs if self.max_jobs > 0 else 'unlimited'}")
        print(f"  Dry run:   {self.dry_run}")
        print(f"{'='*60}\n")

        # Pre-flight checks
        if self.mode == "local":
            if not self._check_ollama_available():
                print("[ERROR] Ollama is not running. Start with: ollama serve",
                      file=sys.stderr)
                sys.exit(1)
            model = self.model or self._best_available_ollama_model()
            if not model:
                print("[ERROR] No ollama models available. Run: ollama pull llama3.2:3b",
                      file=sys.stderr)
                sys.exit(1)
            if not self.model:
                self.model = model
            print(f"[worker] Using ollama model: {self.model}")

        elif self.mode == "claude":
            if not os.environ.get("ANTHROPIC_API_KEY"):
                print("[ERROR] ANTHROPIC_API_KEY environment variable not set",
                      file=sys.stderr)
                sys.exit(1)
            try:
                import anthropic  # noqa: F401 — just check it's installed
            except ImportError:
                print("[ERROR] anthropic package not installed. Run: pip install anthropic",
                      file=sys.stderr)
                sys.exit(1)
            print("[worker] Claude API mode: claude-opus-4-6")

        # Register with orchestrator
        retry_count = 0
        while not self.register():
            wait = min(RETRY_DELAY_SECONDS * (2 ** retry_count), MAX_RETRY_BACKOFF)
            print(f"[worker] Registration failed. Retrying in {wait}s...")
            time.sleep(wait)
            retry_count += 1
            if retry_count > 5:
                print("[ERROR] Cannot reach orchestrator after 5 attempts. Exiting.",
                      file=sys.stderr)
                sys.exit(1)

        # Fetch initial strategy
        if not self.fetch_strategy():
            print("[ERROR] Failed to fetch strategy from orchestrator", file=sys.stderr)
            sys.exit(1)

        retry_delay = RETRY_DELAY_SECONDS
        jobs_since_mutation = 0

        while True:
            # Check max-jobs limit
            if self.max_jobs > 0 and self.jobs_completed >= self.max_jobs:
                print(f"\n[worker] Reached max-jobs limit ({self.max_jobs}). Stopping.")
                break

            # Pull next job
            job = self.pull_job()

            if not job:
                # No jobs available — validate mutations or wait
                validated = self.validate_mutations()
                if not validated:
                    self._log(f"No jobs available. Waiting {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 1.5, MAX_RETRY_BACKOFF)
                else:
                    retry_delay = RETRY_DELAY_SECONDS  # reset on activity
                continue

            retry_delay = RETRY_DELAY_SECONDS  # reset on successful job pull

            job_id = job["job_id"]
            case_id = job["case_id"]
            cancer_type = job["cancer_type"]
            complexity = job.get("complexity", 0)
            case_data = job.get("case_data", {})

            print(f"\n[job] {job_id}")
            print(f"      Cancer: {cancer_type} | Stage: {case_data.get('stage', '?')}")
            print(f"      Complexity: {complexity} | Strategy: {job.get('strategy_hash', '?')[:8]}")

            if self.dry_run:
                print(f"      [DRY RUN] Skipping research execution")
                self.jobs_completed += 1
                continue

            # Run research
            t0 = time.monotonic()
            try:
                if self.mode == "claude":
                    report_json = self.run_research_claude(case_data)
                else:
                    report_json = self.run_research_local(case_data)
            except Exception as e:
                self._log(f"Research execution error: {e}", error=True)
                report_json = None

            duration = time.monotonic() - t0

            if not report_json:
                self._log(f"Research returned no valid JSON for {job_id}", error=True)
                self.jobs_failed += 1
                # Submit a failure score so the job doesn't time out
                self.submit_result(job_id, 0.0, {}, None)
                continue

            # Inject metadata if missing
            if "report_metadata" not in report_json:
                report_json["report_metadata"] = {
                    "cancer_type": cancer_type,
                    "generated_date": datetime.utcnow().isoformat(),
                    "stage": case_data.get("stage", ""),
                    "molecular_profile": case_data.get("molecular_markers", []),
                    "disclaimer": (
                        "FOR RESEARCH AND EDUCATIONAL PURPOSES ONLY. "
                        "This report was generated by an automated AI system and "
                        "has not been reviewed by a licensed medical professional."
                    ),
                    "generated_by": f"worker/{self.worker_id}/{self.mode}",
                    "strategy_hash": self.current_strategy_hash,
                }

            # Score the report
            score, quality_dims = evaluate_report_local(report_json)

            print(f"      Score: {score:.1f}/100 | Duration: {duration:.1f}s")
            if quality_dims:
                dim_summary = " | ".join(
                    f"{k[:8]}:{v['score']}/{v['max']}"
                    for k, v in list(quality_dims.items())[:4]
                )
                print(f"      Dims:  {dim_summary}")

            # Submit result
            ok = self.submit_result(job_id, score, quality_dims, report_json)
            if ok:
                self.jobs_completed += 1
                self.total_score += score
                jobs_since_mutation += 1
                print(f"      Submitted OK | Total jobs: {self.jobs_completed} | "
                      f"Mean score: {self.total_score / self.jobs_completed:.1f}")
            else:
                self._log(f"Failed to submit result for {job_id}", error=True)
                self.jobs_failed += 1

            # Propose mutation every N jobs
            if jobs_since_mutation >= MUTATION_PROPOSE_EVERY:
                self._log("Attempting mutation proposal...")
                self.propose_mutation()
                jobs_since_mutation = 0

            # Validate pending mutations opportunistically
            if self.jobs_completed % 3 == 0:
                self.validate_mutations()

        # Final summary
        print(f"\n{'='*60}")
        print(f"  WORKER COMPLETE")
        print(f"  Jobs completed: {self.jobs_completed}")
        print(f"  Jobs failed:    {self.jobs_failed}")
        if self.jobs_completed > 0:
            print(f"  Mean score:     {self.total_score / self.jobs_completed:.1f}/100")
        print(f"{'='*60}\n")


# ── CLI ───────────────────────────────────────────────────────────────────────

def _default_worker_id() -> str:
    """Generate a default worker ID from hostname."""
    hostname = socket.gethostname()
    ts = datetime.utcnow().strftime("%Y%m%d%H%M")
    return f"worker_{hostname}_{ts}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cancer AutoResearch distributed worker client",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--server", default=DEFAULT_SERVER,
        help="Orchestrator server URL",
    )
    parser.add_argument(
        "--mode", required=True, choices=["local", "claude"],
        help="Research mode: 'local' (ollama) or 'claude' (Anthropic API)",
    )
    parser.add_argument(
        "--worker-id", default=None,
        help="Unique worker identifier (auto-generated from hostname if not set)",
    )
    parser.add_argument(
        "--model", default=None,
        help="Ollama model name for local mode (auto-detected if not set)",
    )
    parser.add_argument(
        "--max-jobs", type=int, default=0,
        help="Maximum number of jobs to process (0 = unlimited)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Pull jobs but skip research execution (for testing connectivity)",
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress non-error output",
    )
    args = parser.parse_args()

    worker_id = args.worker_id or _default_worker_id()

    worker = Worker(
        server_url=args.server,
        mode=args.mode,
        worker_id=worker_id,
        model=args.model or "",
        max_jobs=args.max_jobs,
        dry_run=args.dry_run,
        verbose=not args.quiet,
    )
    try:
        worker.run()
    except KeyboardInterrupt:
        print("\n[worker] Interrupted by user. Shutting down.")
        sys.exit(0)


if __name__ == "__main__":
    main()
