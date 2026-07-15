# 0005 — Structured condition clauses (AST) for Algorithm decision trees and RedFlag triggers

`Algorithm.decision_tree[].evaluate` and `RedFlag.trigger` clauses become a versioned, Pydantic-typed clause AST. The current free-text `condition: "<prose>"` form survives only as an explicit `TextClause` leaf that the engine evaluates to **False with a warning** — preserving clinical nuance for genuinely MDT-evaluated cases without letting prose silently dead-end the auditor at every algorithm's `default_indication`.

## Context

The state audit `docs/reviews/openonco-state-audit-2026-05-17.md` quantified the prose-clause problem:

- **376 of 443 (85%)** indication / algorithm clauses are authored as free-text `condition: "..."` strings.
- **45 of 152 (30%)** algorithms have no machine-evaluable step at all, so `scripts/audit_example_plan_coverage.py` reports they always fall through to `default_indication` regardless of patient.

The mechanism is concrete. `Algorithm.decision_tree[].evaluate` is typed today as `dict` (free-form — see `knowledge_base/schemas/algorithm.py`, `DecisionStep.evaluate: dict`). The engine evaluator at `knowledge_base/engine/redflag_eval.py::_eval_clause` reads:

```python
finding_key = clause.get("finding") or clause.get("condition")
...
actual = _resolve_finding(findings, finding_key)
```

`condition: "≥1 prior systemic line failed (post-CHOEP/CHP-Bv)"` is therefore looked up as a finding-name in the patient dict — there is no finding by that name, the lookup returns `None`, the clause evaluates False, and the step either falls to `next_step` or the algorithm exhausts and returns its default. ALGO-AITL-2L is a worked example: three prose-only `any_of` clauses in step 1 mean step 1 always evaluates False on every patient.

Two responses are on the table:

1. **Per-algorithm RF / finding authoring** (PR #594, PR #597 — the AITL-2L step-2 worked example). Roughly 5-line YAML diffs against 52 algorithms; mechanical but slow, and each PR invents its own ad-hoc clause shape.
2. **AST migration** (this ADR). Single schema change with a one-shot mechanical translator for the well-formed cases, surfacing the genuinely-MDT-only residue for clinical signoff.

The plan in `docs/plans/kb_algorithm_branch_authoring_backlog_2026-05-18.md` enumerates 89 distinct backlog clause signatures across the 376 prose clauses. Migrating the schema lets the engine evaluate all 89 the moment they are authored, instead of after 52 separate per-algorithm PRs land.

## Decision

Replace `evaluate: dict` and `trigger: dict` with a typed, recursive `Clause` AST.

### Schema shape

A single Pydantic model with an "exactly one of" model validator, rather than a discriminated union. Reason: existing YAML uses sibling keys (`finding: stage_group` and `value: "II"` on the same dict) — a discriminator field would force a flatter rewrite. The XOR-validator preserves the current authoring style and lets the loader keep its current shape:

```python
# knowledge_base/schemas/clause.py  (new module)
from typing import Optional, Union, Literal
from pydantic import Field, model_validator
from .base import Base

Comparator = Literal[">", ">=", "<", "<=", "==", "!="]
SetOp      = Literal["in", "not_in"]

class ValueSource(Base):
    """Exactly one of finding / biomarker / demographic / context."""
    finding:     Optional[str] = None  # e.g. "stage_group", "ecog"
    biomarker:   Optional[str] = None  # BIO-* id, e.g. "BIO-HER2"
    demographic: Optional[str] = None  # e.g. "age_years", "sex"
    context:     Optional[str] = None  # e.g. "platinum_free_interval_months"

    @model_validator(mode="after")
    def _exactly_one(self) -> "ValueSource":
        n = sum(x is not None for x in
                (self.finding, self.biomarker, self.demographic, self.context))
        if n != 1:
            raise ValueError(f"ValueSource needs exactly one of finding/biomarker/demographic/context (got {n})")
        return self

class Clause(Base):
    # ── Atomic leaves (exactly one populated) ──
    red_flag: Optional[str] = None                   # RefClause: RF-* id
    source:   Optional[ValueSource] = None           # ValueClause subject
    op:       Optional[Union[Comparator, SetOp]] = None
    threshold: Optional[float] = None                # numeric comparator RHS
    value:     Optional[Union[str, bool, int, float]] = None  # equality RHS
    values:    Optional[list[Union[str, int]]] = None         # in / not_in RHS

    text: Optional[str] = None                       # TextClause fallback — MDT prose

    # ── Boolean composition (existing surface, unchanged) ──
    all_of:  Optional[list["Clause"]] = None
    any_of:  Optional[list["Clause"]] = None
    none_of: Optional[list["Clause"]] = None

    @model_validator(mode="after")
    def _exactly_one_kind(self) -> "Clause":
        kinds = [
            self.red_flag is not None,
            self.source   is not None,
            self.text     is not None,
            self.all_of   is not None,
            self.any_of   is not None,
            self.none_of  is not None,
        ]
        if sum(kinds) != 1:
            raise ValueError("Clause must be exactly one of: red_flag | value (source+op+rhs) | text | all_of | any_of | none_of")
        if self.source is not None:
            if self.op is None:
                raise ValueError("ValueClause requires `op`")
            rhs = sum(x is not None for x in (self.threshold, self.value, self.values))
            if rhs != 1:
                raise ValueError("ValueClause requires exactly one of threshold | value | values")
        return self
```

Then `DecisionStep.evaluate: Clause` (was `dict`) and `RedFlag.trigger: Clause` (was `dict`).

### What this preserves

- **Comparators:** `>= < == != in not_in` (and `> <=`).
- **Value sources:** `finding.<field>` / `biomarker.<id>` / `demographic.<field>` / `context.<field>`. `context` is added explicitly for derived per-patient values like `platinum_free_interval_months` (ALGO-OVARIAN-2L step 1 notes call out this exact case).
- **Composition:** `all_of` / `any_of` / `none_of` survive verbatim — the engine already handles them in `algorithm_eval.py::_eval_step_clause`.
- **Free-text fallback:** `TextClause` (`text: "..."`) is the explicit, typed home for prose clauses that depend on MDT judgement and cannot be wired to a finding. The engine evaluates it as `False` and emits a warning trace event with the literal text, so the render layer can surface it in the MDT brief alongside the chosen branch. This is the contract that lets us keep prose nuance without letting it silently route to `default_indication`.

### Verification against representative YAML

`knowledge_base/hosted/content/algorithms/algo_breast_1l.yaml` step 2 mixes all three leaf kinds — `{red_flag: RF-BREAST-EARLY-STAGE}`, eight `{finding: stage_group, value: "II"}` siblings, and `{condition: "Stage I-III (early)"}`. Under the AST: `Clause(any_of=[Clause(red_flag="RF-..."), Clause(source=ValueSource(finding="stage_group"), op="==", value="II"), ..., Clause(text="Stage I-III (early)")])`. Direct, no information loss, no rewrite of authoring style required.

## Migration plan

**Phase 0 — Schema + engine, dual-read.** Add `knowledge_base/schemas/clause.py`. Loader accepts BOTH the new `Clause` shape AND the legacy `dict` shape; legacy dicts are coerced to `Clause` at load time by a `model_validator(mode="before")` on `DecisionStep` / `RedFlag` that maps `{condition: "X"}` → `Clause(text="X")`, `{finding: F, value: V}` → `Clause(source=ValueSource(finding=F), op="==", value=V)`, etc. The engine evaluator (`algorithm_eval.py`, `redflag_eval.py`) is reimplemented against `Clause` and the legacy `_eval_clause(dict, findings)` path is kept as a thin adapter. **No YAML touched.** Tests + KB validator must stay green. One reviewer (code change only).

**Phase 1 — Mechanical translator.** A script `scripts/migrate_clauses_phase1.py` walks every algorithm + redflag YAML and rewrites well-formed `condition: "..."` strings into structured clauses where the prose maps unambiguously to a known finding / biomarker / demographic (e.g. ALGO-AITL-2L step 2 `"HDAC-inhibitor-naive"` → `{source: {finding: prior_hdaci_exposure}, op: ==, value: false}` once that finding exists in the questionnaire schema). Ambiguous cases are left as `{text: "..."}` and reported. Output is a per-PR diff per algorithm, each ≤ ~20 lines, suitable for two-Clinical-Co-Lead review (CHARTER §6.1 / ADR-0002). Estimated coverage from the audit's 89 distinct signatures: ~40–50 are mechanical.

**Phase 2 — Maintainer-driven migration.** The residue (~40 signatures × ~3 algorithms each) is genuinely MDT-evaluated. Each conversion is a clinical-content change requiring two Clinical Co-Lead signoffs per ADR-0002. The scope of this phase is bounded by the audit, not open-ended.

**Phase 3 — Deprecate raw prose.** Once the KB validator reports zero un-typed `condition:` strings outside `TextClause`, the loader's legacy-shape coercion is gated behind a deprecation warning, then removed in a subsequent release. New YAML written after Phase 3 cuts in cannot use the legacy form.

`Regimen.dose_adjustments[].condition` (e.g. `"FIB-4 > 3.25 OR cirrhosis"` in the schema spec §6) is a parallel call site with the same shape problem. It is **out of scope for this ADR** — addressed in a follow-up once the algorithm/RF AST has stabilized through Phase 1.

## Consequences

**Pros**
- One schema change, evaluated uniformly. The 89 backlog signatures in `kb_algorithm_branch_authoring_backlog_2026-05-18.md` become reachable as soon as their finding / biomarker is named in the AST, not after 52 hand-authored PRs.
- The auditor in `scripts/audit_example_plan_coverage.py` can now distinguish three cases per algorithm: machine-evaluable hit, explicit `TextClause` (MDT-only), absent. The 30% "always-default" finding becomes actionable.
- Authoring is type-checked. A typo in a comparator (`>== ` etc.) fails at load time, not silently as a False clause.
- `TextClause` makes the "we deliberately punt to MDT here" decision explicit and visible in render — currently this is indistinguishable from a wiring bug.

**Cons**
- Every algorithm YAML is touched by Phase 1 (140 files per CLAUDE.md current state). Loader-side coercion in Phase 0 makes this a no-op at load time, but git history grows.
- Pydantic schema churn (`knowledge_base/schemas/algorithm.py`, `red_flag.py`, new `clause.py`). Schema-17 was the last major churn (see `docs/plans/schema_17_refactor_2026-05-07.md`); the team has done this before.
- The render layer (`knowledge_base/engine/render_*`) currently reads `evaluate: dict` directly to print debug traces in some places. Must be migrated to read `Clause`. Audit before Phase 0 lands.
- Existing tests under `tests/` referencing `evaluate: {any_of: [{red_flag: ...}]}` literals are dict-shaped fixtures; they still parse (Phase 0 loader coerces them), but assertions on the in-memory shape must be updated.

## Alternatives considered

**Per-algorithm RF / finding authoring** (PR #594 + PR #597 worked examples). Strengths: each diff is small, each branch gets a real disease-scoped RF named in the redflag catalog, no engine churn. Weaknesses: 52 algorithms × two-Clinical-Co-Lead review = the dominant cost is reviewer time, and each PR re-litigates the clause shape ad hoc. Worked example PR #597 (ALGO-AITL-2L step 2) is the textbook case of a clause that *needs* clinician judgement — a structured AST cannot replace that. The per-algorithm path is the right answer for the ~40 MDT-only residue clauses Phase 2 surfaces; the AST path is the right answer for the ~40–50 mechanically-translatable signatures. The two paths are complementary, not exclusive.

**Status quo (free-text only)**. The 376/443 number is the cost.

**Move to a full expression language (e.g. CEL, JEXL, JsonLogic)**. Rejected: the existing YAML surface (`all_of` / `any_of` / `red_flag` / `finding` / threshold / value) is already a clause AST in everything but type. Adopting a third-party expression language is a much larger change and breaks the clinician-author contract (CHARTER §8.3 ADR-0001) — the audit trail "this Indication was selected because clause X evaluated True" is harder to render from an opaque expression than from a typed Clause tree.

## Open questions

1. **Should `condition.text` survive alongside the AST as a human-readable rendering hint, or be auto-generated from the AST?** I.e., when a clause is `Clause(source=ValueSource(finding="ecog"), op=">=", value=2)`, should the YAML also carry `text: "ECOG ≥ 2"` for the render layer, or is the render layer expected to format the AST itself? Both are workable; the choice affects whether the migration script writes `text:` on every translated clause or only on `TextClause` leaves.

2. **Should the engine emit a warning, an error, or a structured trace event for `TextClause` evaluation post-migration?** Today a prose clause silently False-routes. Phase 0 will at minimum trace it. Post-Phase-3, do we keep `TextClause` as a permanent first-class citizen (MDT punt is a valid clinical state), or treat any remaining `TextClause` after Phase 2 as a KB-validator failure?

3. **How should the AST represent compound thresholds like `"platelet < 50 OR creatinine > 2"`?** The natural form is `Clause(any_of=[Clause(source=ValueSource(finding="platelet"), op="<", threshold=50), Clause(source=ValueSource(finding="creatinine"), op=">", threshold=2)])` — two nested ValueClauses inside `any_of`. Confirm this is preferred over a "compound expression" shorthand. The schema-spec §6.1 example `dose_adjustments[].condition: "FIB-4 > 3.25 OR cirrhosis"` is the canonical case.
