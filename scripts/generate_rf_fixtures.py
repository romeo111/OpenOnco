"""Auto-generate golden positive/negative fixtures for every active
(non-draft) RedFlag that doesn't yet have fixtures.

For each RF.trigger, the generator:
- positive.yaml: picks one any_of clause and produces findings that
  satisfy it (all_of: every clause; for nested any_of, satisfies one).
- negative.yaml: produces findings that satisfy NONE of the clauses
  (booleans → False, "positive" string → "negative", numeric thresholds
  → safely below comparator, etc.).

Skips RFs that already have at least one fixture YAML.

Verifies each generated fixture by running it through
evaluate_redflag_trigger before writing — if generated findings don't
actually fire (or fail to NOT-fire) the trigger, the fixture is skipped
with a warning so the test suite stays green.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))
from knowledge_base.engine.redflag_eval import evaluate_redflag_trigger  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent
RF_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "redflags"
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "redflags"


def _existing_fixture_rf_ids() -> set[str]:
    out: set[str] = set()
    if not FIXTURE_ROOT.is_dir():
        return out
    for d in FIXTURE_ROOT.iterdir():
        if d.is_dir() and any(d.glob("*.yaml")):
            out.add(d.name)
    return out


def _load_yaml(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


# ── Generators ──────────────────────────────────────────────────────────


def _findings_satisfying_clause(clause: dict) -> dict:
    """Return findings dict that makes a single clause evaluate True."""
    if "any_of" in clause:
        # Pick first sub-clause
        for sub in clause["any_of"]:
            return _findings_satisfying_clause(sub)
        return {}
    if "all_of" in clause:
        out: dict = {}
        for sub in clause["all_of"]:
            out.update(_findings_satisfying_clause(sub))
        return out
    if "none_of" in clause:
        # Force the contained clauses to be False (don't add any findings)
        return {}

    finding = clause.get("finding") or clause.get("condition")
    if finding is None:
        return {}

    if "threshold" in clause:
        threshold = clause["threshold"]
        comparator = clause.get("comparator", ">=")
        if comparator == ">":
            return {finding: threshold + 1}
        if comparator == ">=":
            return {finding: threshold}
        if comparator == "<":
            return {finding: threshold - 1}
        if comparator == "<=":
            return {finding: threshold}
        if comparator == "==":
            return {finding: threshold}
        if comparator == "!=":
            return {finding: threshold + 1}
        return {finding: threshold}

    if "value" in clause:
        return {finding: clause["value"]}

    return {finding: True}


def _findings_satisfying_trigger(trigger: dict) -> dict:
    """Find findings dict that fires this trigger."""
    if not isinstance(trigger, dict):
        return {}

    if "any_of" in trigger:
        for sub in trigger["any_of"]:
            f = _findings_satisfying_clause(sub)
            if f:
                return f
        return {}

    if "all_of" in trigger:
        out: dict = {}
        for sub in trigger["all_of"]:
            out.update(_findings_satisfying_clause(sub))
        return out

    return _findings_satisfying_clause(trigger)


def _opposite(value):
    if value is True:
        return False
    if value is False:
        return True
    if value == "positive":
        return "negative"
    if value == "negative":
        return "positive"
    if isinstance(value, (int, float)):
        return value  # caller adjusts numerically below
    return None


def _findings_violating_clause(clause: dict, accumulator: dict) -> None:
    """Add findings to `accumulator` such that a single clause is False."""
    if "any_of" in clause:
        for sub in clause["any_of"]:
            _findings_violating_clause(sub, accumulator)
        return
    if "all_of" in clause:
        # For all_of: satisfying False of just the first sub-clause is enough
        for sub in clause["all_of"]:
            _findings_violating_clause(sub, accumulator)
            return
    if "none_of" in clause:
        return

    finding = clause.get("finding") or clause.get("condition")
    if finding is None:
        return

    if "threshold" in clause:
        threshold = clause["threshold"]
        comparator = clause.get("comparator", ">=")
        if comparator in (">", ">="):
            accumulator[finding] = threshold - 5
        elif comparator in ("<", "<="):
            accumulator[finding] = threshold + 5
        elif comparator == "==":
            accumulator[finding] = threshold + 1
        elif comparator == "!=":
            accumulator[finding] = threshold
        return

    if "value" in clause:
        v = clause["value"]
        opp = _opposite(v)
        if opp is not None:
            accumulator[finding] = opp
        return

    accumulator[finding] = False


def _findings_violating_trigger(trigger: dict) -> dict:
    """Findings that make every any_of clause / all_of clause / etc False."""
    out: dict = {}
    if not isinstance(trigger, dict):
        return out

    if "any_of" in trigger:
        for sub in trigger["any_of"]:
            _findings_violating_clause(sub, out)
        return out

    if "all_of" in trigger:
        # Just one any one made False is enough
        for sub in trigger["all_of"]:
            _findings_violating_clause(sub, out)
            return out

    _findings_violating_clause(trigger, out)
    return out


# ── Driver ──────────────────────────────────────────────────────────────


def main() -> int:
    existing = _existing_fixture_rf_ids()
    generated = 0
    skipped_existing = 0
    skipped_invalid = 0

    for p in sorted(RF_DIR.rglob("*.yaml")):
        rf = _load_yaml(p)
        rid = rf.get("id")
        if not rid:
            continue
        if rf.get("draft"):
            continue
        if rid in existing:
            skipped_existing += 1
            continue

        trigger = rf.get("trigger") or {}

        pos_findings = _findings_satisfying_trigger(trigger)
        neg_findings = _findings_violating_trigger(trigger)

        # Verify with the actual evaluator to make sure they fire / don't fire
        if not evaluate_redflag_trigger(trigger, pos_findings):
            print(f"SKIP {rid}: positive-fixture findings don't fire trigger", file=sys.stderr)
            skipped_invalid += 1
            continue
        if evaluate_redflag_trigger(trigger, neg_findings):
            print(f"SKIP {rid}: negative-fixture findings unexpectedly fire trigger", file=sys.stderr)
            skipped_invalid += 1
            continue

        target_dir = FIXTURE_ROOT / rid
        target_dir.mkdir(parents=True, exist_ok=True)

        pos_yaml = (
            f"red_flag: {rid}\n"
            "findings:\n"
            + "".join(f"  {k}: {_yaml_value(v)}\n" for k, v in pos_findings.items())
            + "expected_fires: true\n"
        )
        neg_yaml = (
            f"red_flag: {rid}\n"
            "findings:\n"
            + "".join(f"  {k}: {_yaml_value(v)}\n" for k, v in neg_findings.items())
            + "expected_fires: false\n"
        )

        (target_dir / "positive.yaml").write_text(pos_yaml, encoding="utf-8")
        (target_dir / "negative.yaml").write_text(neg_yaml, encoding="utf-8")
        generated += 1
        print(f"generated fixtures for {rid}")

    print(
        f"\nDone. Generated {generated} fixture pairs, "
        f"skipped {skipped_existing} (already had), "
        f"{skipped_invalid} (invalid)."
    )
    return 0


def _yaml_value(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, str):
        # Quote strings that look like keywords or contain special chars
        if v in ("true", "false", "null", "") or any(c in v for c in ":#"):
            return f'"{v}"'
        if v.replace(".", "").replace("-", "").isdigit():
            return f'"{v}"'
        # By default, quote to be safe
        return f'"{v}"'
    return str(v)


if __name__ == "__main__":
    sys.exit(main())
