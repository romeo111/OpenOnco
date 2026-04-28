"""Biomarker-actionability integration — shared dataclasses (CIViC-pivot).

All types here are pure data containers (no I/O, no logic). They form
the contract between:

  Biomarker.actionability_lookup → normalize_variant → ActionabilityQuery
                                              → ActionabilityClient (lookup)
                                              → ActionabilityResult | ActionabilityError
                                              → ActionabilityLayer (engine output)
                                              → render layer (HCP-only)

These types are source-agnostic. The original implementation targeted
OncoKB; per the 2026-04-27 OncoKB ToS audit (see
docs/reviews/oncokb-public-civic-coverage-2026-04-27.md) OpenOnco
pivoted to CIViC (CC0). The contract here intentionally does not bake
in any source-specific level vocabulary or surfacing rule — callers
(per-source matchers / readers) populate level dictionaries at lookup
time.

Per safe-rollout v3 §0.1 invariant: nothing in this module reads from or
writes to the engine's track-builder. The architectural firewall against
§8.3 violation is enforced by an import-graph test.

See specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md PROPOSAL §18 for the formal
schema spec entry.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal, Optional


# ── Variant + query primitives ───────────────────────────────────────────


@dataclass(frozen=True)
class NormalizedVariant:
    """Output of normalize_variant. Frozen for safe use as dict key.

    `query_string` is the canonical short form (HGVS-p like "V600E" or
    structured like "Exon 19 deletion"). Source-agnostic — both CIViC
    and OncoKB-style consumers accept this shape.
    """

    gene: str  # HGNC symbol, uppercase
    query_string: str
    raw: str  # original input — for traceability in errors/logs
    skip_reason: None = None  # always None on the success path


@dataclass(frozen=True)
class ActionabilityQuery:
    """Single (gene, variant, oncotree) actionability query.

    Composed in engine/actionability_extract.py. Source-agnostic — every
    actionability source (CIViC, OncoKB, future) accepts this triple."""

    gene: str
    variant: str
    oncotree_code: Optional[str]
    source_biomarker_id: str  # for traceability + provenance event metadata


# ── Lookup results ───────────────────────────────────────────────────────


# Per-source level vocabularies are populated at lookup time. CIViC uses
# A/B/C/D/E with direction. Other sources (NCCN/ESMO categories) populate
# their own tokens at lookup time; matchers don't enforce this Literal.
TherapeuticLevel = Literal["A", "B", "C", "D", "E"]

# Per-source surfacing rules: which levels make it into the rendered HCP
# section. Empty by default — matchers (e.g. a CIViC reader, an OncoKB
# reader) populate this set themselves at lookup time. Phase 2 wires the
# CIViC matcher and decides the CIViC surfacing rule (likely A/B with
# direction=Supports + significance in the therapeutic axis).
#
# Rule TBD per source; matchers populate at lookup time.
SURFACED_LEVELS: frozenset[str] = frozenset()

# Resistance levels are likewise source-specific. Empty by default;
# matchers populate (e.g. CIViC: direction=Supports & significance=Resistance).
RESISTANCE_LEVELS: frozenset[str] = frozenset()


@dataclass(frozen=True)
class ActionabilityTherapeuticOption:
    level: str  # source-native level token
    drugs: tuple[str, ...]
    description: Optional[str]
    pmids: tuple[str, ...]
    fda_approved: bool = False
    fda_approval_year: Optional[int] = None


@dataclass(frozen=True)
class ActionabilityResult:
    """Successful lookup. May still have empty therapeutic_options
    (negative result — biomarker is recognised but no actionable evidence)."""

    query: ActionabilityQuery
    source_url: str
    therapeutic_options: tuple[ActionabilityTherapeuticOption, ...]
    cached: bool
    data_version: Optional[str] = None  # populated when source provides it

    @property
    def is_negative(self) -> bool:
        return len(self.therapeutic_options) == 0

    @property
    def highest_level(self) -> Optional[str]:
        if not self.therapeutic_options:
            return None
        # Caller-provided rank table; fall back to lexical ordering.
        # In Phase 2 the per-source reader will own the ranking logic.
        return sorted(
            (opt.level for opt in self.therapeutic_options),
            key=_level_sort_key,
        )[0]


@dataclass(frozen=True)
class ActionabilityError:
    """Failure mode. Engine wraps these in the layer instead of raising —
    fail-open contract per safe-rollout v3 §0 founding principle 3."""

    query: ActionabilityQuery
    error_kind: Literal["timeout", "http_error", "parse_error", "circuit_open", "disabled"]
    detail: str  # human-readable; never contains secrets


# ── Resistance-conflict + layer ──────────────────────────────────────────


@dataclass(frozen=True)
class ResistanceConflict:
    """Detected when an engine-recommended drug appears in the actionability
    source's resistance evidence for one of the patient's biomarkers.

    Per safe-rollout v3 §6 this triggers (a) inline banner in track-card,
    (b) provenance event, (c) MDT role escalation (molecular_geneticist).
    Drug-X-resists-on-biomarker-Y is a source-agnostic pattern (works for
    CIViC `direction=Supports & significance=Resistance` and OncoKB R1/R2
    alike)."""

    track_id: str
    drug: str
    gene: str
    variant: str
    level: str  # source-native level token (e.g. "B" for CIViC, "R1" for OncoKB)
    description: Optional[str]


@dataclass
class ActionabilityLayer:
    """Engine output — surfaces alongside (NEVER inside) the two-track Plan.

    `render_plan_html(mode="hcp")` reads this. `render_plan_html(mode="patient")`
    MUST ignore it entirely (patient-mode HTML must contain zero actionability
    detail)."""

    results: list[ActionabilityResult] = field(default_factory=list)
    errors: list[ActionabilityError] = field(default_factory=list)
    resistance_conflicts: list[ResistanceConflict] = field(default_factory=list)
    pan_tumor_fallback_used: bool = False  # warning badge per Q4

    @property
    def is_empty(self) -> bool:
        """Empty layer = render skips section entirely."""
        if self.resistance_conflicts:
            return False
        if SURFACED_LEVELS:
            for r in self.results:
                if any(opt.level in SURFACED_LEVELS for opt in r.therapeutic_options):
                    return False
            return True
        # No surfacing rule wired yet — treat any therapeutic_options as
        # surface-worthy, so Phase 2 wiring can turn the rule on without
        # the layer disappearing in the meantime.
        for r in self.results:
            if r.therapeutic_options:
                return False
        return True

    def to_dict(self) -> dict:
        return {
            "results": [_result_to_dict(r) for r in self.results],
            "errors": [asdict(e) for e in self.errors],
            "resistance_conflicts": [asdict(c) for c in self.resistance_conflicts],
            "pan_tumor_fallback_used": self.pan_tumor_fallback_used,
        }


# ── Internals ────────────────────────────────────────────────────────────


# Rank dict for highest_level convenience method. CIViC levels A→E
# (lower number = stronger evidence). Source-agnostic: matchers may extend
# or replace it for sources with their own taxonomy.
_LEVEL_RANK: dict[str, int] = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
}


def _level_sort_key(level: str) -> int:
    return _LEVEL_RANK.get(level, 99)


def _result_to_dict(r: ActionabilityResult) -> dict:
    return {
        "query": asdict(r.query),
        "source_url": r.source_url,
        "therapeutic_options": [asdict(o) for o in r.therapeutic_options],
        "cached": r.cached,
        "data_version": r.data_version,
    }


__all__ = [
    "NormalizedVariant",
    "ActionabilityQuery",
    "ActionabilityTherapeuticOption",
    "ActionabilityResult",
    "ActionabilityError",
    "ResistanceConflict",
    "ActionabilityLayer",
    "TherapeuticLevel",
    "SURFACED_LEVELS",
    "RESISTANCE_LEVELS",
]
