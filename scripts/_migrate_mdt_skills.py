"""One-shot migration: dump _SKILL_REGISTRY (Python dict in
mdt_orchestrator.py) → YAML files under hosted/content/mdt_skills/.

Run once:
    python -m scripts._migrate_mdt_skills

Idempotent — overwrites existing files. Used during candidate #7a.
"""

from __future__ import annotations

import sys
from dataclasses import asdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from knowledge_base.engine.mdt_orchestrator import _SKILL_REGISTRY  # noqa: E402

OUT_DIR = REPO_ROOT / "knowledge_base" / "hosted" / "content" / "mdt_skills"


def _dump(skill_role_id: str, skill) -> None:
    payload = {
        "id": f"MDT-SKILL-{skill_role_id.upper().replace('_', '-')}",
        "role_id": skill_role_id,
        "name": skill.name,
        "version": skill.version,
        "last_reviewed": skill.last_reviewed,
        "clinical_lead": skill.clinical_lead,
        "verified_by": skill.verified_by,
        "sources": skill.sources,
        "domain": skill.domain,
        "notes": skill.notes,
    }
    # Drop optional None values so the YAML stays clean (Pydantic defaults
    # them on load anyway).
    payload = {k: v for k, v in payload.items() if v is not None and v != [] and v != {}}
    out_path = OUT_DIR / f"{skill_role_id}.yaml"
    with out_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            payload,
            f,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=100,
        )
    print(f"  wrote {out_path.relative_to(REPO_ROOT)}")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Migrating {len(_SKILL_REGISTRY)} skills -> {OUT_DIR.relative_to(REPO_ROOT)}/")
    for role_id, skill in _SKILL_REGISTRY.items():
        _dump(role_id, skill)
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
