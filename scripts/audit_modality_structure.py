"""Audit prose-only surgery/radiation mentions and structured modality rows.

This keeps the local-therapy schema gap measurable. It does not author
clinical modality records; it produces a candidate queue for surgical and
radiation oncology reviewers.

Usage:
    python scripts/audit_modality_structure.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTENT = REPO_ROOT / "knowledge_base" / "hosted" / "content"
INDICATIONS = CONTENT / "indications"
SURGERY = CONTENT / "surgery"
RADIATION = CONTENT / "radiation"
OUT = REPO_ROOT / "docs" / "audits" / "modality_structure_audit.json"

SURGERY_RE = re.compile(
    r"\b(surgery|surgical|resection|mastectomy|lumpectomy|colectomy|"
    r"prostatectomy|metastasectomy|biopsy|debulking)\b",
    re.IGNORECASE,
)
RADIATION_RE = re.compile(
    r"\b(radiation|radiotherapy|RT|CRT|chemoradiation|IMRT|SBRT|"
    r"brachytherapy|proton)\b",
    re.IGNORECASE,
)


def _load_yaml(path: Path) -> dict[str, Any] | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    return data if isinstance(data, dict) else None


def _modality_rows(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not root.is_dir():
        return rows
    for path in sorted(root.glob("*.yaml")):
        data = _load_yaml(path)
        if data:
            rows.append(data)
    return rows


def _indication_candidates() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(INDICATIONS.glob("*.yaml")):
        data = _load_yaml(path)
        if not data:
            continue
        ind_id = data.get("id")
        applicable = data.get("applicable_to") or {}
        disease_id = applicable.get("disease_id") if isinstance(applicable, dict) else None
        text = path.read_text(encoding="utf-8", errors="ignore")
        kinds: list[str] = []
        surgery_terms = sorted({m.group(0).lower() for m in SURGERY_RE.finditer(text)})
        radiation_terms = sorted({m.group(0).lower() for m in RADIATION_RE.finditer(text)})
        if surgery_terms:
            kinds.append("surgery")
        if radiation_terms:
            kinds.append("radiation")
        if not kinds:
            continue
        rows.append(
            {
                "indication_id": ind_id,
                "disease_id": disease_id,
                "candidate_modalities": kinds,
                "surgery_terms": surgery_terms,
                "radiation_terms": radiation_terms,
                "path": str(path.relative_to(REPO_ROOT)),
            }
        )
    return rows


def main() -> int:
    surgery_rows = _modality_rows(SURGERY)
    radiation_rows = _modality_rows(RADIATION)
    candidates = _indication_candidates()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(
            {
                "generated_by": "scripts/audit_modality_structure.py",
                "structured_surgery_records": len(surgery_rows),
                "structured_radiation_records": len(radiation_rows),
                "prose_candidate_count": len(candidates),
                "quality_gate": (
                    "Convert prose candidates into structured surgery/radiation "
                    "YAML only after modality-specialist review and source anchoring."
                ),
                "candidates": candidates,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
