"""Canonical promo/outreach figures, read straight off the live knowledge base.

`promo/README.md` requires every outward-facing asset to quote the same scale
figures. Those numbers were hand-copied and drifted: assets shipped "92
diseases / 444 sources" long after the KB reached 103 / 471, and quoted a
"15 of 806" review ratio after the entity total had grown to 1061 — which
*overstates* how much of the KB is clinically signed off.

Run this before touching any promo copy:

    py -3.12 -m scripts.promo_figures            # human-readable block
    py -3.12 -m scripts.promo_figures --check    # non-zero exit if promo/ is stale

Counts intentionally mirror what /capabilities.html publishes, since
`promo/README.md` designates the capabilities page as canonical. Note red
flags are counted top-level only (the 44 under redflags/universal/ are
cross-disease modifiers and are excluded there too).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
KB = REPO_ROOT / "knowledge_base" / "hosted" / "content"
PROMO = REPO_ROOT / "promo"


def _count(subdir: str, *, recursive: bool = False) -> int:
    p = KB / subdir
    if not p.is_dir():
        return 0
    return len(list(p.rglob("*.yaml") if recursive else p.glob("*.yaml")))


def _line_of_therapy_split() -> tuple[int, int]:
    first = later = 0
    for f in (KB / "indications").glob("*.yaml"):
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        lot = (data.get("applicable_to") or {}).get("line_of_therapy")
        if lot == 1:
            first += 1
        elif isinstance(lot, int) and lot >= 2:
            later += 1
    return first, later


def _signoff_ratio() -> tuple[int, int]:
    """(entities with two-reviewer sign-off, total clinical entities).

    Delegates to knowledge_base.stats so this never diverges from the
    figure the site itself renders."""
    from knowledge_base.stats import collect_stats

    s = collect_stats()
    return s.reviewer_signoffs_reviewed, s.reviewer_signoffs_total


def _full_chain_count() -> tuple[int, int]:
    """(diseases with a full modeled chain, total diseases).

    `coverage_status` is derived by knowledge_base.stats, not a raw YAML
    field — reading the YAML directly yields 0. Mirrors the same predicate
    build_site.py uses for the capabilities page."""
    from knowledge_base.stats import collect_stats

    diseases = collect_stats().diseases
    full = sum(
        1 for d in diseases
        if d.coverage_status in {"stub_full_chain", "reviewed"}
    )
    return full, len(diseases)


def figures() -> dict:
    first, later = _line_of_therapy_split()
    signed, entities = _signoff_ratio()
    full_chain, disease_total = _full_chain_count()
    return {
        "diseases": _count("diseases"),
        "indications": _count("indications"),
        "indications_1l": first,
        "indications_2l_plus": later,
        "regimens": _count("regimens"),
        "drugs": _count("drugs"),
        "redflags": _count("redflags"),
        "sources": _count("sources"),
        "mdt_skills": 16,
        "full_chain": full_chain,
        "disease_total": disease_total,
        "signed_off": signed,
        "entities": entities,
        "as_of": _dt.date.today().isoformat(),
    }


def render(f: dict) -> str:
    return (
        f"Scale (state {f['as_of']}): {f['diseases']} diseases, "
        f"{f['indications']} indications ({f['indications_1l']} first-line, "
        f"{f['indications_2l_plus']} second-line+), {f['regimens']} treatment "
        f"regimens, {f['drugs']} drugs (ATC/RxNorm coded), {f['redflags']} red "
        f"flags, {f['sources']} cited sources, {f['mdt_skills']} virtual MDT "
        f"clinician skills. {f['full_chain']} of {f['disease_total']} diseases "
        f"have a full modeled chain.\n"
        f"Maturity: only {f['signed_off']} of {f['entities']} clinical entities "
        f"have two-reviewer sign-off; the rest are STUB."
    )


# Superseded values, matched as a bare number ANYWHERE on a line that also
# mentions the thing being counted. Phrase matching ("92 diseases") is not
# enough — markdown tables write `| Diseases covered | **92** |`, putting the
# label before the number, and that shape shipped stale figures under a fresh
# date stamp once already.
_SUPERSEDED: list[tuple[str, tuple[str, ...], str]] = [
    ("92", ("disease", "захворюв"), "diseases"),
    ("664", ("indication", "показан"), "indications"),
    ("384", ("regimen", "схем"), "regimens"),
    ("444", ("source", "джерел"), "sources"),
    ("594", ("red flag", "червон"), "redflags"),
    ("298", ("drug", "препарат"), "drugs"),
    ("806", (), "entities"),          # only ever the sign-off denominator
    ("77", ("full modeled chain",), "full_chain"),
    ("2026-06-17", (), "as_of"),
]


def check() -> int:
    """Exit non-zero if any promo asset still quotes a superseded figure.

    Skips lines marked [figures-frozen] — records of what a past review
    verified, which must stay as written.
    """
    current = figures()
    stale: list[str] = []
    for path in sorted(PROMO.glob("*.md")):
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if "[figures-frozen]" in line:
                continue
            low = line.lower()
            for old, context, key in _SUPERSEDED:
                if not re.search(rf"(?<!\d){re.escape(old)}(?!\d)", line):
                    continue
                if context and not any(c in low for c in context):
                    continue
                stale.append(
                    f"{path.relative_to(REPO_ROOT)}:{i}: "
                    f"{old} -> {current[key]} ({key})"
                )
    if stale:
        print("Superseded figures still present in promo/:", file=sys.stderr)
        for s in stale:
            print("  " + s, file=sys.stderr)
        print(
            "\nRefresh them against `py -3.12 -m scripts.promo_figures`, or mark a "
            "line [figures-frozen] if it is a record of a past review.",
            file=sys.stderr,
        )
        return 1
    print("promo/ figures are current.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit non-zero if promo/ still quotes superseded figures")
    args = ap.parse_args()
    if args.check:
        return check()
    print(render(figures()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
