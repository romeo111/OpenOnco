"""Normalized disease-level actionability coverage report.

This is an observability report, not a clinical-content generator. It answers
why diseases like NSCLC look over-covered in raw YAML counts by separating:

  - raw BMA records from normalized biomarker/driver families
  - standard-care or approved actionability from lower-tier / investigational
    / resistance-only rows
  - unique drugs and regimens referenced by indication/regimen wiring
  - clinical signoff state

Run:
    py -3.12 -m scripts.normalized_actionability_coverage
    py -3.12 -m scripts.normalized_actionability_coverage --json
    py -3.12 -m scripts.normalized_actionability_coverage --rank-fill-next
    py -3.12 -m scripts.normalized_actionability_coverage --rank-fill-next --top 10
    py -3.12 -m scripts.normalized_actionability_coverage --chunk-specs --top 5
    py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease DIS-ENDOMETRIAL
    py -3.12 -m scripts.normalized_actionability_coverage --review-packet --inventory-disease DIS-ENDOMETRIAL --inventory-queue soc_dmmr_family
    py -3.12 -m scripts.normalized_actionability_coverage --out docs/reviews/...
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"

STANDARD_ESCAT = {"IA", "IB"}
MID_ESCAT = {"IIA", "IIB"}
LOW_ESCAT = {"IIIA", "IIIB", "IV", "V", "X"}
RESISTANCE_VARIANT_TOKENS = ("c797s", "t790m", "g1202r", "l1196m", "g2032r", "f691l")
INVESTIGATIONAL_WORDS = ("trial", "investigational", "research", "candidate", "emerging", "off-label", "not approved")

FREEZE_EXPANSION = {"DIS-NSCLC"}
MAJOR_SOLID = {
    "DIS-BREAST",
    "DIS-CRC",
    "DIS-PROSTATE",
    "DIS-OVARIAN",
    "DIS-GASTRIC",
    "DIS-UROTHELIAL",
    "DIS-RCC",
    "DIS-HCC",
    "DIS-PDAC",
    "DIS-ENDOMETRIAL",
    "DIS-MELANOMA",
    "DIS-HNSCC",
    "DIS-GBM",
}
HIGH_VALUE_SOLID_THIN = {
    "DIS-CHOLANGIOCARCINOMA",
    "DIS-CERVICAL",
    "DIS-ESOPHAGEAL",
    "DIS-THYROID-ANAPLASTIC",
    "DIS-THYROID-PAPILLARY",
    "DIS-MTC",
}
HEME_DISEASE_PREFIXES = ("DIS-AML", "DIS-APL", "DIS-CML", "DIS-MDS", "DIS-PV", "DIS-ET", "DIS-PMF")
HEME_DISEASES = {
    "DIS-MM",
    "DIS-DLBCL-NOS",
    "DIS-FL",
    "DIS-CLL",
    "DIS-MCL",
    "DIS-SPLENIC-MZL",
    "DIS-NODAL-MZL",
    "DIS-HCV-MZL",
    "DIS-BURKITT",
    "DIS-HCL",
    "DIS-WM",
    "DIS-HGBL-DH",
    "DIS-PTCL-NOS",
    "DIS-ALCL",
    "DIS-AITL",
    "DIS-MF-SEZARY",
    "DIS-CHL",
    "DIS-NLPBL",
    "DIS-PMBCL",
    "DIS-PCNSL",
    "DIS-B-ALL",
    "DIS-T-ALL",
    "DIS-PTLD",
    "DIS-EATL",
    "DIS-HSTCL",
    "DIS-NK-T-NASAL",
    "DIS-ATLL",
    "DIS-T-PLL",
}

PLANNING_TIERS = (
    "freeze_expand",
    "major_solid",
    "high_value_solid_thin",
    "heme",
    "rare_or_thin",
)


@dataclass
class DiseaseCoverage:
    disease_id: str
    name: str
    archetype: str | None = None
    molecular_subtypes_count: int = 0
    bma_total: int = 0
    normalized_families: set[str] = field(default_factory=set)
    standard_families: set[str] = field(default_factory=set)
    approved_or_guideline_families: set[str] = field(default_factory=set)
    resistance_bmas: int = 0
    investigational_or_low_bmas: int = 0
    unique_drugs: set[str] = field(default_factory=set)
    unique_regimens: set[str] = field(default_factory=set)
    linked_regimen_refs: set[str] = field(default_factory=set)
    missing_regimen_record_ids: set[str] = field(default_factory=set)
    indications: int = 0
    redflags: int = 0
    signed_bmas: int = 0
    signed_indications: int = 0

    @property
    def normalized_family_count(self) -> int:
        return len(self.normalized_families)

    @property
    def standard_family_count(self) -> int:
        return len(self.standard_families)

    @property
    def approved_or_guideline_family_count(self) -> int:
        return len(self.approved_or_guideline_families)

    @property
    def unique_drug_count(self) -> int:
        return len(self.unique_drugs)

    @property
    def unique_regimen_count(self) -> int:
        return len(self.unique_regimens)

    @property
    def bma_variant_inflation_ratio(self) -> float | None:
        if not self.normalized_families:
            return None
        return round(self.bma_total / len(self.normalized_families), 2)

    @property
    def bma_signed_pct(self) -> float | None:
        if self.bma_total == 0:
            return None
        return round(100.0 * self.signed_bmas / self.bma_total, 1)

    def to_jsonable(self) -> dict[str, Any]:
        data = asdict(self)
        for key in (
            "normalized_families",
            "standard_families",
            "approved_or_guideline_families",
            "unique_drugs",
            "unique_regimens",
            "linked_regimen_refs",
            "missing_regimen_record_ids",
        ):
            data[key] = sorted(data[key])
        data["normalized_family_count"] = self.normalized_family_count
        data["standard_family_count"] = self.standard_family_count
        data["approved_or_guideline_family_count"] = self.approved_or_guideline_family_count
        data["unique_drug_count"] = self.unique_drug_count
        data["unique_regimen_count"] = self.unique_regimen_count
        data["linked_regimen_ref_count"] = len(self.linked_regimen_refs)
        data["missing_regimen_record_count"] = len(self.missing_regimen_record_ids)
        data["bma_variant_inflation_ratio"] = self.bma_variant_inflation_ratio
        data["bma_signed_pct"] = self.bma_signed_pct
        return data

    def to_compact_jsonable(self) -> dict[str, Any]:
        return {
            "disease_id": self.disease_id,
            "archetype": self.archetype,
            "bma": self.bma_total,
            "families": self.normalized_family_count,
            "soc_families": self.standard_family_count,
            "approved_or_guideline_families": self.approved_or_guideline_family_count,
            "low_or_investigational_bma": self.investigational_or_low_bmas,
            "resistance_bma": self.resistance_bmas,
            "drugs": self.unique_drug_count,
            "regimens": self.unique_regimen_count,
            "linked_regimen_refs": len(self.linked_regimen_refs),
            "missing_regimen_records": len(self.missing_regimen_record_ids),
            "indications": self.indications,
            "redflags": self.redflags,
            "inflation": self.bma_variant_inflation_ratio,
            "bma_signed_pct": self.bma_signed_pct,
        }


@dataclass
class FillBacklogRow:
    disease_id: str
    name: str
    tier: str
    score: int
    review_readiness_pct: float
    workflow_lane: str
    soc_gap: int
    indication_gap: int
    regimen_gap: int
    drug_gap: int
    redflag_gap: int
    recommended_chunk: str
    quality_flags: list[str] = field(default_factory=list)
    current_bma: int = 0
    current_families: int = 0
    current_soc_families: int = 0
    current_indications: int = 0
    current_regimens: int = 0
    current_drugs: int = 0
    current_redflags: int = 0

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)

    def to_compact_jsonable(self) -> dict[str, Any]:
        return {
            "disease_id": self.disease_id,
            "tier": self.tier,
            "score": self.score,
            "review_readiness_pct": self.review_readiness_pct,
            "workflow_lane": self.workflow_lane,
            "gaps": {
                "soc": self.soc_gap,
                "ind": self.indication_gap,
                "reg": self.regimen_gap,
                "drug": self.drug_gap,
                "rf": self.redflag_gap,
            },
            "current": {
                "bma": self.current_bma,
                "families": self.current_families,
                "soc": self.current_soc_families,
                "ind": self.current_indications,
                "reg": self.current_regimens,
                "drug": self.current_drugs,
                "rf": self.current_redflags,
            },
            "chunk": self.recommended_chunk,
            "flags": self.quality_flags,
        }


@dataclass
class DiseaseInventory:
    disease_id: str
    disease_path: str | None
    name: str
    coverage: DiseaseCoverage | None
    backlog: FillBacklogRow | None
    bmas: list[dict[str, Any]]
    bma_families: list[dict[str, Any]]
    bma_review_blockers: dict[str, Any]
    bma_metadata_consistency: dict[str, Any]
    bma_review_queue: list[dict[str, Any]]
    regimen_wiring_consistency: dict[str, Any]
    indications: list[dict[str, Any]]
    regimens: list[dict[str, Any]]
    redflags: list[dict[str, Any]]
    sources: list[dict[str, Any]]
    stale_sources: list[dict[str, Any]]

    def to_jsonable(self, *, compact: bool = False) -> dict[str, Any]:
        if compact:
            return {
                "disease_id": self.disease_id,
                "path": self.disease_path,
                "coverage": self.coverage.to_compact_jsonable() if self.coverage else None,
                "backlog": self.backlog.to_compact_jsonable() if self.backlog else None,
                "counts": {
                    "bma": len(self.bmas),
                    "ind": len(self.indications),
                    "reg": len(self.regimens),
                    "rf": len(self.redflags),
                    "src": len(self.sources),
                    "stale_src": len(self.stale_sources),
                },
                "bma_review_blockers": self.bma_review_blockers,
                "bma_metadata_consistency": self.bma_metadata_consistency,
                "bma_families": self.bma_families,
                "bma_review_queue": self.bma_review_queue,
                "regimen_wiring_consistency": self.regimen_wiring_consistency,
                "paths": {
                    "bma": [item["path"] for item in self.bmas],
                    "ind": [item["path"] for item in self.indications],
                    "reg": [item["path"] for item in self.regimens],
                    "rf": [item["path"] for item in self.redflags],
                    "src": [item["path"] for item in self.sources],
                },
                "stale_source_ids": [item["id"] for item in self.stale_sources],
            }
        return {
            "disease_id": self.disease_id,
            "path": self.disease_path,
            "name": self.name,
            "coverage": self.coverage.to_jsonable() if self.coverage else None,
            "backlog": self.backlog.to_jsonable() if self.backlog else None,
            "bmas": self.bmas,
            "bma_families": self.bma_families,
            "bma_review_blockers": self.bma_review_blockers,
            "bma_metadata_consistency": self.bma_metadata_consistency,
            "bma_review_queue": self.bma_review_queue,
            "regimen_wiring_consistency": self.regimen_wiring_consistency,
            "indications": self.indications,
            "regimens": self.regimens,
            "redflags": self.redflags,
            "sources": self.sources,
            "stale_sources": self.stale_sources,
        }


@dataclass
class BmaReviewPacket:
    disease_id: str
    disease_path: str | None
    name: str
    queue: dict[str, Any] | None
    bmas: list[dict[str, Any]]
    metadata_consistency: dict[str, Any]
    indications: list[dict[str, Any]]
    regimens: list[dict[str, Any]]
    sources: list[dict[str, Any]]

    def to_jsonable(self, *, compact: bool = False) -> dict[str, Any]:
        if compact:
            return {
                "disease_id": self.disease_id,
                "path": self.disease_path,
                "queue": self.queue,
                "counts": {
                    "bma": len(self.bmas),
                    "ind": len(self.indications),
                    "reg": len(self.regimens),
                    "src": len(self.sources),
                },
                "shared_primary_sources": _shared_primary_sources(self.bmas),
                "metadata_consistency": self.metadata_consistency,
                "records": self.bmas,
                "linked": {
                    "indication_ids": [item["id"] for item in self.indications],
                    "regimen_ids": [item["id"] for item in self.regimens],
                    "source_ids": [item["id"] for item in self.sources],
                },
            }
        return {
            "disease_id": self.disease_id,
            "path": self.disease_path,
            "name": self.name,
            "queue": self.queue,
            "shared_primary_sources": _shared_primary_sources(self.bmas),
            "metadata_consistency": self.metadata_consistency,
            "bmas": self.bmas,
            "indications": self.indications,
            "regimens": self.regimens,
            "sources": self.sources,
        }


def _load_yaml_dir(subdir: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    folder = KB_ROOT / subdir
    if not folder.is_dir():
        return out
    for path in sorted(folder.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data["__path"] = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
            out.append(data)
    return out


def _walk(node: Any):
    if isinstance(node, dict):
        for value in node.values():
            yield from _walk(value)
    elif isinstance(node, list):
        for item in node:
            yield from _walk(item)
    else:
        yield node


def _collect_ids(node: Any, prefix: str) -> set[str]:
    ids: set[str] = set()
    for item in _walk(node):
        if isinstance(item, str) and item.startswith(prefix):
            ids.add(item)
    return ids


def _signoff_count(value: Any) -> int:
    if isinstance(value, list):
        return len(value)
    if isinstance(value, int):
        return value
    return 0


def _is_signed(data: dict[str, Any]) -> bool:
    if _signoff_count(data.get("reviewer_signoffs")) >= 2:
        return True
    return data.get("ukrainian_review_status") in {"signed_off", "signed_off_2reviewer"}


def _text_blob(data: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in (
        "id",
        "evidence_summary",
        "notes",
        "regulatory_approval",
        "recommended_combinations",
        "contraindicated_monotherapy",
    ):
        value = data.get(key)
        if value is not None:
            parts.append(json.dumps(value, ensure_ascii=False, default=str).lower())
    return " ".join(parts)


def _is_resistance_bma(bma: dict[str, Any]) -> bool:
    # Classify the BMA row itself, not every CIViC evidence item attached to
    # it. Many standard-care rows (EGFR ex19del, KRAS G12C) carry a mixed
    # CIViC bundle with resistance evidence to unrelated drugs; that should not
    # demote the whole family from standard-care coverage.
    identity = " ".join(
        str(bma.get(key) or "").lower()
        for key in ("id", "variant_qualifier")
    )
    if any(token in identity for token in RESISTANCE_VARIANT_TOKENS):
        return True

    saw_resistance = False
    saw_sensitivity = False
    for entry in bma.get("evidence_sources") or []:
        if not isinstance(entry, dict):
            continue
        lane = str(entry.get("evidence_lane") or "").lower()
        significance = str(entry.get("significance") or "").lower()
        direction = str(entry.get("direction") or "").lower()
        if lane == "resistance_or_avoidance_signal":
            return True
        if "resistance" in significance or "does_not_support" in direction:
            saw_resistance = True
        if "sensitivity" in significance or "response" in significance:
            saw_sensitivity = True
    return saw_resistance and not saw_sensitivity


def _is_investigational_or_low_bma(bma: dict[str, Any]) -> bool:
    tier = str(bma.get("escat_tier") or "")
    if tier in LOW_ESCAT:
        return True
    text = _text_blob(bma)
    if any(word in text for word in INVESTIGATIONAL_WORDS):
        return True
    for entry in bma.get("evidence_sources") or []:
        if isinstance(entry, dict) and entry.get("evidence_lane") == "trial_research_option":
            return True
    return False


def _has_approval_or_guideline_signal(bma: dict[str, Any]) -> bool:
    reg = bma.get("regulatory_approval")
    if isinstance(reg, dict):
        for value in reg.values():
            if isinstance(value, list) and value:
                return True
            if isinstance(value, str) and value.strip():
                return True
    sources = set(bma.get("primary_sources") or [])
    if any(src.startswith(("SRC-NCCN", "SRC-ESMO", "SRC-ESGO")) for src in sources):
        return True
    return False


def _bma_family(bma: dict[str, Any]) -> str:
    """Collapse variant-specific BMA rows into a stable family bucket.

    Prefer biomarker_id, then apply targeted suffix collapsing for common
    mutation/fusion aggregate IDs. This intentionally preserves clinically
    distinct families like BIO-KRAS-G12C while collapsing EGFR/ALK/ROS1
    resistance and partner rows authored under aggregate biomarker IDs.
    """
    biomarker = str(bma.get("biomarker_id") or "")
    if biomarker:
        return biomarker

    bid = str(bma.get("id") or "")
    m = re.match(r"^BMA-([A-Z0-9]+)", bid)
    if m:
        return f"BIO-{m.group(1)}"
    return bid or "(unknown)"


def build_report() -> list[DiseaseCoverage]:
    diseases = _load_yaml_dir("diseases")
    bmas = _load_yaml_dir("biomarker_actionability")
    indications = _load_yaml_dir("indications")
    redflags = _load_yaml_dir("redflags")
    regimens = {r.get("id"): r for r in _load_yaml_dir("regimens") if r.get("id")}

    rows: dict[str, DiseaseCoverage] = {}
    for disease in diseases:
        did = disease.get("id")
        if not isinstance(did, str):
            continue
        names = disease.get("names") or {}
        rows[did] = DiseaseCoverage(
            disease_id=did,
            name=names.get("english") or names.get("preferred") or did,
            archetype=disease.get("archetype"),
            molecular_subtypes_count=len(disease.get("molecular_subtypes") or []),
        )

    for bma in bmas:
        did = bma.get("disease_id")
        if did not in rows:
            continue
        row = rows[did]
        family = _bma_family(bma)
        row.bma_total += 1
        row.normalized_families.add(family)
        if _is_signed(bma):
            row.signed_bmas += 1
        if _is_resistance_bma(bma):
            row.resistance_bmas += 1
        if _is_investigational_or_low_bma(bma):
            row.investigational_or_low_bmas += 1
        if bma.get("escat_tier") in STANDARD_ESCAT and not _is_resistance_bma(bma):
            row.standard_families.add(family)
        if _has_approval_or_guideline_signal(bma):
            row.approved_or_guideline_families.add(family)

    for ind in indications:
        applicable = ind.get("applicable_to") or {}
        did = applicable.get("disease_id") if isinstance(applicable, dict) else None
        did = did or ind.get("disease_id")
        if did not in rows:
            continue
        row = rows[did]
        row.indications += 1
        if _is_signed(ind):
            row.signed_indications += 1
        reg_id = ind.get("recommended_regimen")
        if isinstance(reg_id, str):
            row.linked_regimen_refs.add(reg_id)
            regimen = regimens.get(reg_id)
            if regimen:
                row.unique_regimens.add(reg_id)
                row.unique_drugs |= _collect_ids(regimen, "DRUG-")
            else:
                row.missing_regimen_record_ids.add(reg_id)
        row.unique_drugs |= _collect_ids(ind, "DRUG-")

    for rf in redflags:
        rel = rf.get("relevant_diseases") or []
        if not isinstance(rel, list):
            continue
        for did in rel:
            if did in rows:
                rows[did].redflags += 1

    return sorted(rows.values(), key=lambda r: (-r.bma_total, r.disease_id))


def _is_heme(disease_id: str) -> bool:
    return disease_id in HEME_DISEASES or disease_id.startswith(HEME_DISEASE_PREFIXES)


def _planning_tier(row: DiseaseCoverage) -> str:
    if row.disease_id in FREEZE_EXPANSION:
        return "freeze_expand"
    if row.disease_id in MAJOR_SOLID:
        return "major_solid"
    if row.disease_id in HIGH_VALUE_SOLID_THIN:
        return "high_value_solid_thin"
    if _is_heme(row.disease_id):
        return "heme"
    return "rare_or_thin"


def _targets_for(row: DiseaseCoverage) -> dict[str, int]:
    """Return pragmatic fill targets for the next planning wave.

    Targets are intentionally not "match NSCLC". They describe enough
    normalized coverage for a truthful vertical:
      - major solid tumors need broad SOC/actionable family and line coverage
      - heme and high-value thin solid tumors need moderate breadth
      - rare/thin diseases need a minimal chain rather than forced biomarkers
    """
    tier = _planning_tier(row)
    if tier == "freeze_expand":
        return {"soc": 0, "ind": 0, "reg": 0, "drug": 0, "rf": 0}
    if tier == "major_solid":
        soc = 6 if row.archetype == "biomarker_driven" else 2
        return {"soc": soc, "ind": 10, "reg": 8, "drug": 8, "rf": 7}
    if tier == "high_value_solid_thin":
        soc = 3 if row.archetype == "biomarker_driven" else 1
        return {"soc": soc, "ind": 5, "reg": 4, "drug": 4, "rf": 5}
    if tier == "heme":
        soc = 2 if row.archetype in {"biomarker_driven", "risk_stratified"} else 1
        return {"soc": soc, "ind": 5, "reg": 4, "drug": 4, "rf": 5}
    soc = 1 if row.archetype == "biomarker_driven" or row.bma_total > 0 else 0
    return {"soc": soc, "ind": 2, "reg": 2, "drug": 2, "rf": 5}


def _gap(value: int, target: int) -> int:
    return max(0, target - value)


def _quality_flags(row: DiseaseCoverage) -> list[str]:
    flags: list[str] = []
    if row.bma_total > 0 and row.signed_bmas == 0:
        flags.append("signoff_cold")
    if row.indications > 0 and row.signed_indications == 0:
        flags.append("indication_signoff_cold")
    ratio = row.bma_variant_inflation_ratio or 0
    if row.bma_total >= 5 and ratio >= 3.0:
        flags.append(f"variant_inflation_{ratio:.2f}x")
    if row.investigational_or_low_bmas > row.standard_family_count and row.bma_total >= 3:
        flags.append("low_tier_dominant")
    if row.missing_regimen_record_ids:
        flags.append("missing_regimen_records")
    return flags


def _review_readiness_pct(row: DiseaseCoverage, targets: dict[str, int]) -> float:
    weights = {"soc": 5, "ind": 3, "reg": 2, "drug": 1, "rf": 1}
    current = {
        "soc": row.standard_family_count,
        "ind": row.indications,
        "reg": row.unique_regimen_count,
        "drug": row.unique_drug_count,
        "rf": row.redflags,
    }
    weighted_target = sum(targets[key] * weights[key] for key in weights)
    if weighted_target == 0:
        return 100.0
    weighted_current = sum(min(current[key], targets[key]) * weights[key] for key in weights)
    return round(100.0 * weighted_current / weighted_target, 1)


def _workflow_lane(row: DiseaseCoverage, *, tier: str, review_readiness_pct: float) -> str:
    if tier == "freeze_expand":
        return "freeze_expand"
    if review_readiness_pct >= 80.0 and not row.missing_regimen_record_ids:
        return "review_ready"
    return "fill_first"


def _recommended_chunk(row: DiseaseCoverage, gaps: dict[str, int], *, workflow_lane: str) -> str:
    if _planning_tier(row) == "freeze_expand":
        return "Freeze expansion; run signoff, ESCAT/source audit, and dedupe only."
    if row.missing_regimen_record_ids:
        return (
            f"Create or backfill {len(row.missing_regimen_record_ids)} linked regimen records "
            "referenced by existing indications."
        )
    if workflow_lane == "review_ready":
        return "Eligible for disease-level review/signoff; defer more fill unless review finds a blocking gap."
    if gaps["soc"] > 0:
        return f"Add {gaps['soc']} guideline-backed SOC/actionable biomarker family or document no biomarker axis."
    if gaps["ind"] > 0:
        return f"Add {gaps['ind']} indication records to close line-of-therapy sequencing."
    if gaps["reg"] > 0:
        return f"Add {gaps['reg']} regimen records and wire them from indications."
    if gaps["drug"] > 0:
        return f"Add {gaps['drug']} drug records or regimen components for existing indications."
    if gaps["rf"] > 0:
        return f"Add {gaps['rf']} red flags to meet minimal safety/emergency coverage."
    return "No content-fill chunk needed; prioritize quality/signoff."


def build_fill_backlog(rows: list[DiseaseCoverage]) -> list[FillBacklogRow]:
    backlog: list[FillBacklogRow] = []
    for row in rows:
        tier = _planning_tier(row)
        targets = _targets_for(row)
        review_readiness_pct = _review_readiness_pct(row, targets)
        workflow_lane = _workflow_lane(row, tier=tier, review_readiness_pct=review_readiness_pct)
        gaps = {
            "soc": _gap(row.standard_family_count, targets["soc"]),
            "ind": _gap(row.indications, targets["ind"]),
            "reg": _gap(row.unique_regimen_count, targets["reg"]),
            "drug": _gap(row.unique_drug_count, targets["drug"]),
            "rf": _gap(row.redflags, targets["rf"]),
        }

        if tier == "freeze_expand":
            score = 0
        elif workflow_lane == "review_ready":
            score = 0
        else:
            score = (
                gaps["soc"] * 5
                + gaps["ind"] * 3
                + gaps["reg"] * 2
                + gaps["drug"]
                + gaps["rf"]
            )
            if row.bma_total == 0 and targets["soc"] > 0:
                score += 4
            if row.indications == 0 and targets["ind"] > 0:
                score += 4

        backlog.append(
            FillBacklogRow(
                disease_id=row.disease_id,
                name=row.name,
                tier=tier,
                score=score,
                review_readiness_pct=review_readiness_pct,
                workflow_lane=workflow_lane,
                soc_gap=gaps["soc"],
                indication_gap=gaps["ind"],
                regimen_gap=gaps["reg"],
                drug_gap=gaps["drug"],
                redflag_gap=gaps["rf"],
                recommended_chunk=_recommended_chunk(row, gaps, workflow_lane=workflow_lane),
                quality_flags=_quality_flags(row),
                current_bma=row.bma_total,
                current_families=row.normalized_family_count,
                current_soc_families=row.standard_family_count,
                current_indications=row.indications,
                current_regimens=row.unique_regimen_count,
                current_drugs=row.unique_drug_count,
                current_redflags=row.redflags,
            )
        )
    return sorted(backlog, key=lambda r: (-r.score, r.tier, r.disease_id))


def _filter_coverage_rows(
    rows: list[DiseaseCoverage],
    *,
    diseases: list[str] | None = None,
    tiers: list[str] | None = None,
    top: int | None = None,
) -> list[DiseaseCoverage]:
    out = rows
    if diseases:
        wanted = {d.upper() for d in diseases}
        out = [row for row in out if row.disease_id.upper() in wanted]
    if tiers:
        wanted_tiers = set(tiers)
        out = [row for row in out if _planning_tier(row) in wanted_tiers]
    if top is not None:
        out = out[: max(0, top)]
    return out


def _filter_backlog_rows(
    rows: list[FillBacklogRow],
    *,
    diseases: list[str] | None = None,
    tiers: list[str] | None = None,
    workflow_lanes: list[str] | None = None,
    top: int | None = None,
    active_only: bool = False,
) -> list[FillBacklogRow]:
    out = rows
    if active_only:
        out = [row for row in out if row.score > 0 and row.workflow_lane == "fill_first"]
    if diseases:
        wanted = {d.upper() for d in diseases}
        out = [row for row in out if row.disease_id.upper() in wanted]
    if tiers:
        wanted_tiers = set(tiers)
        out = [row for row in out if row.tier in wanted_tiers]
    if workflow_lanes:
        wanted_lanes = set(workflow_lanes)
        out = [row for row in out if row.workflow_lane in wanted_lanes]
    if top is not None:
        out = out[: max(0, top)]
    return out


def _disease_id_from_indication(indication: dict[str, Any]) -> str | None:
    applicable = indication.get("applicable_to") or {}
    if isinstance(applicable, dict) and isinstance(applicable.get("disease_id"), str):
        return applicable["disease_id"]
    did = indication.get("disease_id")
    return did if isinstance(did, str) else None


def _summarize_record(data: dict[str, Any], *, fields: tuple[str, ...]) -> dict[str, Any]:
    out = {
        "id": data.get("id"),
        "path": data.get("__path"),
    }
    for field_name in fields:
        if field_name in data:
            out[field_name] = data[field_name]
    return out


def _is_stale_source(source: dict[str, Any]) -> bool:
    status = str(source.get("currency_status") or "").lower()
    return bool(source.get("superseded_by")) or status in {"superseded", "stale", "outdated"}


def _tier_rank(tier: str | None) -> int:
    order = {
        "IA": 0,
        "IB": 1,
        "IIA": 2,
        "IIB": 3,
        "IIIA": 4,
        "IIIB": 5,
        "IV": 6,
        "V": 7,
        "X": 8,
    }
    return order.get(str(tier or "").upper(), 99)


def _bma_family_summary(disease_bmas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in disease_bmas:
        grouped[str(item.get("biomarker_id") or "(unknown)")].append(item)

    out: list[dict[str, Any]] = []
    for family, records in sorted(grouped.items()):
        tiers = [str(record.get("escat_tier") or "") for record in records if record.get("escat_tier")]
        highest_tier = min(tiers, key=_tier_rank) if tiers else None
        out.append(
            {
                "biomarker_id": family,
                "count": len(records),
                "highest_escat_tier": highest_tier,
                "record_ids": [str(record.get("id")) for record in records if record.get("id")],
            }
        )
    return out


def _bma_review_blockers(disease_bmas: list[dict[str, Any]]) -> dict[str, Any]:
    pending_ids = [
        str(item.get("id"))
        for item in disease_bmas
        if item.get("ukrainian_review_status") == "pending_clinical_signoff"
    ]
    review_required_ids = [
        str(item.get("id"))
        for item in disease_bmas
        if bool(item.get("actionability_review_required"))
    ]
    return {
        "pending_clinical_signoff_count": len(pending_ids),
        "pending_clinical_signoff_ids": pending_ids,
        "actionability_review_required_count": len(review_required_ids),
        "actionability_review_required_ids": review_required_ids,
    }


def _bma_metadata_consistency(disease_bmas: list[dict[str, Any]]) -> dict[str, Any]:
    issue_ids: dict[str, set[str]] = {
        "missing_primary_sources_ids": set(),
        "missing_evidence_sources_ids": set(),
        "missing_contraindicated_monotherapy_ids": set(),
        "guideline_evidence_order_mismatch_ids": set(),
    }
    guideline_prefixes = ("SRC-NCCN", "SRC-ESMO", "SRC-ESGO")
    all_ids: list[str] = []

    for item in disease_bmas:
        record_id = str(item.get("id") or "")
        if not record_id:
            continue
        all_ids.append(record_id)

        has_primary_sources = bool(item.get("primary_sources"))
        has_legacy_sources = bool(item.get("sources"))
        if not has_primary_sources and not has_legacy_sources:
            issue_ids["missing_primary_sources_ids"].add(record_id)
        if not item.get("evidence_sources"):
            issue_ids["missing_evidence_sources_ids"].add(record_id)
        contra_expected = "recommended_combinations" in item
        if contra_expected and "contraindicated_monotherapy" not in item:
            issue_ids["missing_contraindicated_monotherapy_ids"].add(record_id)

        primary_guideline_sources = [
            str(source_id)
            for source_id in (item.get("primary_sources") or [])
            if isinstance(source_id, str) and source_id.startswith(guideline_prefixes)
        ]
        evidence_guideline_sources = [
            str(entry.get("source"))
            for entry in (item.get("evidence_sources") or [])
            if isinstance(entry, dict)
            and isinstance(entry.get("source"), str)
            and str(entry.get("source")).startswith(guideline_prefixes)
        ]
        if (
            primary_guideline_sources
            and evidence_guideline_sources
            and set(evidence_guideline_sources) == set(primary_guideline_sources)
            and evidence_guideline_sources != primary_guideline_sources
        ):
            issue_ids["guideline_evidence_order_mismatch_ids"].add(record_id)

    touched_ids = set().union(*issue_ids.values()) if issue_ids else set()
    metadata_ready_ids = [record_id for record_id in all_ids if record_id not in touched_ids]
    return {
        "missing_primary_sources_count": len(issue_ids["missing_primary_sources_ids"]),
        "missing_primary_sources_ids": sorted(issue_ids["missing_primary_sources_ids"]),
        "missing_evidence_sources_count": len(issue_ids["missing_evidence_sources_ids"]),
        "missing_evidence_sources_ids": sorted(issue_ids["missing_evidence_sources_ids"]),
        "missing_contraindicated_monotherapy_count": len(issue_ids["missing_contraindicated_monotherapy_ids"]),
        "missing_contraindicated_monotherapy_ids": sorted(issue_ids["missing_contraindicated_monotherapy_ids"]),
        "guideline_evidence_order_mismatch_count": len(issue_ids["guideline_evidence_order_mismatch_ids"]),
        "guideline_evidence_order_mismatch_ids": sorted(issue_ids["guideline_evidence_order_mismatch_ids"]),
        "metadata_ready_count": len(metadata_ready_ids),
        "metadata_ready_ids": metadata_ready_ids,
    }


def _filter_bma_metadata_consistency(
    consistency: dict[str, Any],
    *,
    wanted_ids: set[str],
    all_ids: list[str],
) -> dict[str, Any]:
    def _filtered(key: str) -> list[str]:
        return [
            record_id
            for record_id in consistency.get(key, [])
            if isinstance(record_id, str) and record_id in wanted_ids
        ]

    missing_primary = _filtered("missing_primary_sources_ids")
    missing_evidence = _filtered("missing_evidence_sources_ids")
    missing_contra = _filtered("missing_contraindicated_monotherapy_ids")
    order_mismatch = _filtered("guideline_evidence_order_mismatch_ids")
    touched_ids = set(missing_primary) | set(missing_evidence) | set(missing_contra) | set(order_mismatch)
    metadata_ready_ids = [record_id for record_id in all_ids if record_id not in touched_ids]
    return {
        "missing_primary_sources_count": len(missing_primary),
        "missing_primary_sources_ids": missing_primary,
        "missing_evidence_sources_count": len(missing_evidence),
        "missing_evidence_sources_ids": missing_evidence,
        "missing_contraindicated_monotherapy_count": len(missing_contra),
        "missing_contraindicated_monotherapy_ids": missing_contra,
        "guideline_evidence_order_mismatch_count": len(order_mismatch),
        "guideline_evidence_order_mismatch_ids": order_mismatch,
        "metadata_ready_count": len(metadata_ready_ids),
        "metadata_ready_ids": metadata_ready_ids,
    }


def _bma_review_queue(disease_bmas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    family_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in disease_bmas:
        family_groups[str(item.get("biomarker_id") or "(unknown)")].append(item)

    queue: list[dict[str, Any]] = []

    dmmr_records = family_groups.get("BIO-DMMR-IHC", [])
    if dmmr_records:
        queue.append(
            {
                "queue_id": "soc_dmmr_family",
                "priority": "high",
                "reason": "Largest family block; IA evidence; highest review leverage.",
                "biomarker_ids": ["BIO-DMMR-IHC"],
                "record_count": len(dmmr_records),
                "record_ids": [str(item.get("id")) for item in dmmr_records if item.get("id")],
            }
        )

    intermediate_families = {"BIO-CTNNB1", "BIO-FGFR2", "BIO-PIK3R1"}
    intermediate_records = [
        item
        for family, records in family_groups.items()
        if family in intermediate_families
        for item in records
    ]
    if intermediate_records:
        queue.append(
            {
                "queue_id": "intermediate_family_audit",
                "priority": "medium",
                "reason": "Single-record actionable families with IIA/IIB evidence that need clean review packets.",
                "biomarker_ids": sorted(intermediate_families & set(family_groups)),
                "record_count": len(intermediate_records),
                "record_ids": [str(item.get("id")) for item in intermediate_records if item.get("id")],
            }
        )

    low_tier_records = [
        item
        for item in disease_bmas
        if str(item.get("escat_tier") or "") in LOW_ESCAT
    ]
    if low_tier_records:
        queue.append(
            {
                "queue_id": "low_tier_tail",
                "priority": "low",
                "reason": "Low-tier exploratory/prognostic rows; review after core SOC and intermediate families.",
                "biomarker_ids": sorted({str(item.get("biomarker_id") or "(unknown)") for item in low_tier_records}),
                "record_count": len(low_tier_records),
                "record_ids": [str(item.get("id")) for item in low_tier_records if item.get("id")],
            }
        )

    return queue


def _regimen_wiring_consistency(
    disease_indications: list[dict[str, Any]],
    disease_regimens: list[dict[str, Any]],
    regimen_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    linked_regimen_ids = sorted(
        {
            str(item.get("recommended_regimen"))
            for item in disease_indications
            if isinstance(item.get("recommended_regimen"), str)
        }
    )
    missing_regimen_record_ids = [
        regimen_id for regimen_id in linked_regimen_ids if regimen_id not in regimen_by_id
    ]
    regimens_missing_sources_ids = sorted(
        str(item.get("id"))
        for item in disease_regimens
        if item.get("id") and not item.get("sources")
    )
    wired_regimen_ids = sorted(
        str(item.get("id"))
        for item in disease_regimens
        if item.get("id") and item.get("sources")
    )
    return {
        "linked_regimen_ids": linked_regimen_ids,
        "linked_regimen_count": len(linked_regimen_ids),
        "missing_regimen_record_count": len(missing_regimen_record_ids),
        "missing_regimen_record_ids": missing_regimen_record_ids,
        "regimens_missing_sources_count": len(regimens_missing_sources_ids),
        "regimens_missing_sources_ids": regimens_missing_sources_ids,
        "wired_regimen_count": len(wired_regimen_ids),
        "wired_regimen_ids": wired_regimen_ids,
    }


def build_inventory(disease_ids: list[str]) -> list[DiseaseInventory]:
    wanted = {disease_id.upper() for disease_id in disease_ids}
    diseases = _load_yaml_dir("diseases")
    bmas = _load_yaml_dir("biomarker_actionability")
    indications = _load_yaml_dir("indications")
    redflags = _load_yaml_dir("redflags")
    regimens = _load_yaml_dir("regimens")
    sources = _load_yaml_dir("sources")

    disease_by_id = {item.get("id"): item for item in diseases if item.get("id")}
    regimen_by_id = {item.get("id"): item for item in regimens if item.get("id")}
    source_by_id = {item.get("id"): item for item in sources if item.get("id")}
    coverage_by_id = {row.disease_id: row for row in build_report()}
    backlog_by_id = {row.disease_id: row for row in build_fill_backlog(list(coverage_by_id.values()))}

    inventories: list[DiseaseInventory] = []
    for disease_id in sorted(wanted):
        disease = disease_by_id.get(disease_id)
        disease_bmas = [item for item in bmas if item.get("disease_id") == disease_id]
        disease_indications = [item for item in indications if _disease_id_from_indication(item) == disease_id]
        linked_regimen_ids = {
            item.get("recommended_regimen")
            for item in disease_indications
            if isinstance(item.get("recommended_regimen"), str)
        }
        disease_regimens = [regimen_by_id[reg_id] for reg_id in sorted(linked_regimen_ids) if reg_id in regimen_by_id]
        disease_redflags = [
            item
            for item in redflags
            if disease_id in (item.get("relevant_diseases") or [])
        ]

        source_ids: set[str] = set()
        for record in [disease, *disease_bmas, *disease_indications, *disease_regimens, *disease_redflags]:
            if record:
                source_ids |= _collect_ids(record, "SRC-")
        disease_sources = [source_by_id[source_id] for source_id in sorted(source_ids) if source_id in source_by_id]
        stale_sources = [source for source in disease_sources if _is_stale_source(source)]

        names = disease.get("names") if isinstance(disease, dict) else {}
        if not isinstance(names, dict):
            names = {}
        inventories.append(
            DiseaseInventory(
                disease_id=disease_id,
                disease_path=disease.get("__path") if isinstance(disease, dict) else None,
                name=names.get("english") or names.get("preferred") or disease_id,
                coverage=coverage_by_id.get(disease_id),
                backlog=backlog_by_id.get(disease_id),
                bmas=[
                    _summarize_record(
                        item,
                        fields=(
                            "biomarker_id",
                            "variant_qualifier",
                            "escat_tier",
                            "ukrainian_review_status",
                            "last_verified",
                            "actionability_review_required",
                        ),
                    )
                    for item in disease_bmas
                ],
                bma_families=_bma_family_summary(disease_bmas),
                bma_review_blockers=_bma_review_blockers(disease_bmas),
                bma_metadata_consistency=_bma_metadata_consistency(disease_bmas),
                bma_review_queue=_bma_review_queue(disease_bmas),
                regimen_wiring_consistency=_regimen_wiring_consistency(
                    disease_indications,
                    disease_regimens,
                    regimen_by_id,
                ),
                indications=[
                    _summarize_record(
                        item,
                        fields=("recommended_regimen", "line_of_therapy", "nccn_category", "reviewer_signoffs"),
                    )
                    for item in disease_indications
                ],
                regimens=[
                    _summarize_record(
                        item,
                        fields=("name", "components", "sources", "reviewer_signoffs", "last_verified"),
                    )
                    for item in disease_regimens
                ],
                redflags=[
                    _summarize_record(
                        item,
                        fields=("title", "severity", "last_verified"),
                    )
                    for item in disease_redflags
                ],
                sources=[
                    _summarize_record(
                        item,
                        fields=("source_type", "title", "version", "currency_status", "superseded_by", "last_verified"),
                    )
                    for item in disease_sources
                ],
                stale_sources=[
                    _summarize_record(
                        item,
                        fields=("title", "currency_status", "superseded_by", "last_verified"),
                    )
                    for item in stale_sources
                ],
            )
        )
    return inventories


def build_review_packets(disease_ids: list[str], *, queue_id: str | None = None) -> list[BmaReviewPacket]:
    inventories = {item.disease_id: item for item in build_inventory(disease_ids)}
    bmas = _load_yaml_dir("biomarker_actionability")

    packets: list[BmaReviewPacket] = []
    for disease_id in disease_ids:
        inventory = inventories.get(disease_id.upper())
        if inventory is None:
            continue

        raw_bmas = [item for item in bmas if item.get("disease_id") == inventory.disease_id]
        queue = None
        if queue_id:
            queue = next((item for item in inventory.bma_review_queue if item["queue_id"] == queue_id), None)
            if queue is not None:
                wanted_ids = set(queue["record_ids"])
                raw_bmas = [item for item in raw_bmas if item.get("id") in wanted_ids]
            inventory = _filter_inventory_by_queue(inventory, queue_id)

        packets.append(
            BmaReviewPacket(
                disease_id=inventory.disease_id,
                disease_path=inventory.disease_path,
                name=inventory.name,
                queue=queue or (inventory.bma_review_queue[0] if len(inventory.bma_review_queue) == 1 else None),
                bmas=[_summarize_review_bma(item) for item in raw_bmas],
                metadata_consistency=inventory.bma_metadata_consistency,
                indications=inventory.indications,
                regimens=inventory.regimens,
                sources=inventory.sources,
            )
        )
    return packets


def _filter_inventory_by_queue(inventory: DiseaseInventory, queue_id: str) -> DiseaseInventory:
    target = next((item for item in inventory.bma_review_queue if item["queue_id"] == queue_id), None)
    if target is None:
        return inventory

    wanted_ids = set(target["record_ids"])
    filtered_bmas = [item for item in inventory.bmas if item.get("id") in wanted_ids]
    wanted_families = {str(item.get("biomarker_id")) for item in filtered_bmas if item.get("biomarker_id")}
    filtered_families = [item for item in inventory.bma_families if item["biomarker_id"] in wanted_families]
    filtered_bma_ids = [str(item.get("id")) for item in filtered_bmas if item.get("id")]

    return DiseaseInventory(
        disease_id=inventory.disease_id,
        disease_path=inventory.disease_path,
        name=inventory.name,
        coverage=inventory.coverage,
        backlog=inventory.backlog,
        bmas=filtered_bmas,
        bma_families=filtered_families,
        bma_review_blockers={
            "pending_clinical_signoff_count": len(
                [item for item in filtered_bmas if item.get("ukrainian_review_status") == "pending_clinical_signoff"]
            ),
            "pending_clinical_signoff_ids": [
                str(item.get("id"))
                for item in filtered_bmas
                if item.get("ukrainian_review_status") == "pending_clinical_signoff"
            ],
            "actionability_review_required_count": len(
                [item for item in filtered_bmas if bool(item.get("actionability_review_required"))]
            ),
            "actionability_review_required_ids": [
                str(item.get("id"))
                for item in filtered_bmas
                if bool(item.get("actionability_review_required"))
            ],
        },
        bma_metadata_consistency=_filter_bma_metadata_consistency(
            inventory.bma_metadata_consistency,
            wanted_ids=wanted_ids,
            all_ids=filtered_bma_ids,
        ),
        bma_review_queue=[target],
        regimen_wiring_consistency=inventory.regimen_wiring_consistency,
        indications=inventory.indications,
        regimens=inventory.regimens,
        redflags=inventory.redflags,
        sources=inventory.sources,
        stale_sources=inventory.stale_sources,
    )


def render_markdown(rows: list[DiseaseCoverage], *, top: int | None = None) -> str:
    total_bmas = sum(r.bma_total for r in rows)
    total_families = sum(r.normalized_family_count for r in rows)
    signed_bmas = sum(r.signed_bmas for r in rows)
    high_inflation = [r for r in rows if (r.bma_variant_inflation_ratio or 0) >= 2.0]

    lines: list[str] = [
        "# Normalized Actionability Coverage",
        "",
        "This report separates raw YAML volume from normalized disease-level clinical coverage.",
        "It is an observability layer only; it does not change clinical recommendations.",
        "",
        "## Summary",
        "",
        f"- Diseases: {len(rows)}",
        f"- Raw BMA records: {total_bmas}",
        f"- Normalized disease x biomarker-family buckets: {total_families}",
        f"- BMA records with >=2 signoffs or signed status: {signed_bmas}",
        f"- Diseases with variant-family inflation >=2.0x: {len(high_inflation)}",
        "",
        "## Top Diseases By Raw BMA Volume",
        "",
        "| Disease | Archetype | BMA | Families | Inflation | SOC families | Approved/guideline families | Low/investigational BMA | Resistance BMA | Drugs | Regimens | IND | RF | BMA signed |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    limit = 30 if top is None else max(0, top)
    for row in rows[:limit]:
        ratio = row.bma_variant_inflation_ratio
        ratio_s = f"{ratio:.2f}x" if ratio is not None else "-"
        signed = f"{row.bma_signed_pct:.1f}%" if row.bma_signed_pct is not None else "-"
        lines.append(
            "| "
            f"{row.disease_id} | {row.archetype or '-'} | {row.bma_total} | "
            f"{row.normalized_family_count} | {ratio_s} | "
            f"{row.standard_family_count} | {row.approved_or_guideline_family_count} | "
            f"{row.investigational_or_low_bmas} | {row.resistance_bmas} | "
            f"{row.unique_drug_count} | {row.unique_regimen_count} | "
            f"{row.indications} | {row.redflags} | {signed} |"
        )

    lines.extend([
        "",
        "## Variant Inflation Flags",
        "",
        "| Disease | BMA | Families | Inflation | Interpretation |",
        "|---|---:|---:|---:|---|",
    ])
    for row in sorted(high_inflation, key=lambda r: (-(r.bma_variant_inflation_ratio or 0), r.disease_id))[:30]:
        ratio = row.bma_variant_inflation_ratio or 0
        lines.append(
            f"| {row.disease_id} | {row.bma_total} | {row.normalized_family_count} | "
            f"{ratio:.2f}x | Raw BMA count likely overstates independent driver coverage. |"
        )

    lines.extend([
        "",
        "## Notes",
        "",
        "- `Families` collapses BMA rows by `biomarker_id`, so EGFR/ALK/ROS1 partner and resistance variants do not each count as independent disease-level coverage.",
        "- `SOC families` counts ESCAT IA/IB families that are not classified as resistance rows.",
        "- `Approved/guideline families` means the BMA carries regulatory approval text or NCCN/ESMO/ESGO primary sources; it is still not a substitute for clinical signoff.",
        "- `Low/investigational BMA` is heuristic: ESCAT III/IV/X or text/evidence-lane signals such as trial, candidate, emerging, off-label, or not approved.",
        "- `Resistance BMA` is heuristic: resistance-specific variant IDs/qualifiers or resistance-only evidence lanes, avoiding mixed CIViC bundles that also support sensitivity.",
    ])
    return "\n".join(lines) + "\n"


def render_json(rows: list[DiseaseCoverage], *, compact: bool = False) -> str:
    payload = (
        [row.to_compact_jsonable() for row in rows]
        if compact
        else [row.to_jsonable() for row in rows]
    )
    return json.dumps(
        {"diseases": payload},
        indent=2,
        ensure_ascii=False,
    ) + "\n"


def render_backlog_markdown(backlog: list[FillBacklogRow], *, top: int | None = None) -> str:
    active = [row for row in backlog if row.score > 0 and row.workflow_lane == "fill_first"]
    review_ready = [row for row in backlog if row.workflow_lane == "review_ready"]
    frozen = [row for row in backlog if row.tier == "freeze_expand"]
    quality_only = [
        row
        for row in backlog
        if row.score == 0 and row.quality_flags and row.tier != "freeze_expand" and row.workflow_lane != "review_ready"
    ]

    lines: list[str] = [
        "# Normalized Coverage Fill Backlog",
        "",
        "This backlog ranks disease fill work from normalized clinical coverage, not raw YAML counts.",
        "NSCLC is frozen for expansion by policy here; it should receive quality/signoff work only.",
        "",
        "## Summary",
        "",
        f"- Active fill candidates: {len(active)}",
        f"- Ready-for-review diseases (>80%): {len(review_ready)}",
        f"- Freeze-expansion diseases: {len(frozen)}",
        f"- Quality-only candidates: {len(quality_only)}",
        "",
        "## Highest Priority Fill Chunks",
        "",
        "| Rank | Disease | Tier | Readiness | Score | SOC gap | IND gap | REG gap | Drug gap | RF gap | Current SOC/IND/REG/Drug/RF | Recommended chunk | Quality flags |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|",
    ]
    limit = 40 if top is None else max(0, top)
    for idx, row in enumerate(active[:limit], start=1):
        current = (
            f"{row.current_soc_families}/"
            f"{row.current_indications}/"
            f"{row.current_regimens}/"
            f"{row.current_drugs}/"
            f"{row.current_redflags}"
        )
        flags = ", ".join(row.quality_flags) if row.quality_flags else "-"
        lines.append(
            "| "
            f"{idx} | {row.disease_id} | {row.tier} | {row.review_readiness_pct:.1f}% | {row.score} | "
            f"{row.soc_gap} | {row.indication_gap} | {row.regimen_gap} | "
            f"{row.drug_gap} | {row.redflag_gap} | {current} | "
            f"{row.recommended_chunk} | {flags} |"
        )

    lines.extend([
        "",
        "## Ready For Review",
        "",
        "| Disease | Tier | Readiness | Current SOC/IND/REG/Drug/RF | Next step | Quality flags |",
        "|---|---|---:|---|---|---|",
    ])
    for row in review_ready:
        current = (
            f"{row.current_soc_families}/"
            f"{row.current_indications}/"
            f"{row.current_regimens}/"
            f"{row.current_drugs}/"
            f"{row.current_redflags}"
        )
        flags = ", ".join(row.quality_flags) if row.quality_flags else "-"
        lines.append(
            "| "
            f"{row.disease_id} | {row.tier} | {row.review_readiness_pct:.1f}% | "
            f"{current} | Eligible for disease-level review/signoff workflow. | {flags} |"
        )

    lines.extend([
        "",
        "## Freeze Expansion",
        "",
        "| Disease | Readiness | Current BMA | Families | SOC families | IND | Drugs | Regimens | RF | Required work |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ])
    for row in frozen:
        lines.append(
            f"| {row.disease_id} | {row.review_readiness_pct:.1f}% | {row.current_bma} | {row.current_families} | "
            f"{row.current_soc_families} | {row.current_indications} | "
            f"{row.current_drugs} | {row.current_regimens} | {row.current_redflags} | "
            f"{row.recommended_chunk} |"
        )

    lines.extend([
        "",
        "## Quality-Only Blockers",
        "",
        "| Disease | Tier | Readiness | Current SOC/IND/REG/Drug/RF | Next step | Quality flags |",
        "|---|---|---:|---|---|---|",
    ])
    for row in quality_only:
        current = (
            f"{row.current_soc_families}/"
            f"{row.current_indications}/"
            f"{row.current_regimens}/"
            f"{row.current_drugs}/"
            f"{row.current_redflags}"
        )
        flags = ", ".join(row.quality_flags) if row.quality_flags else "-"
        lines.append(
            "| "
            f"{row.disease_id} | {row.tier} | {row.review_readiness_pct:.1f}% | "
            f"{current} | {row.recommended_chunk} | {flags} |"
        )

    lines.extend([
        "",
        "## Planning Rules",
        "",
        "- Do not normalize every disease toward NSCLC raw BMA volume.",
        "- Diseases above 80% target completion move to `review_ready` and should go through review/signoff before more fill.",
        "- Diseases below 80% stay in `fill_first` and should not consume clinician review bandwidth yet.",
        "- Major solid tumors target broader SOC/actionable family and line-of-therapy coverage.",
        "- Heme and high-value thin solid tumors target moderate breadth.",
        "- Rare/thin diseases target a minimal truthful vertical: core indications, regimens, drugs, red flags, and only real actionable biomarkers.",
        "- Quality flags are not expansion instructions; use them for signoff, attribution, ESCAT audit, and dedupe chunks.",
    ])
    return "\n".join(lines) + "\n"


def render_backlog_json(backlog: list[FillBacklogRow], *, compact: bool = False) -> str:
    payload = (
        [row.to_compact_jsonable() for row in backlog]
        if compact
        else [row.to_jsonable() for row in backlog]
    )
    return json.dumps(
        {"fill_backlog": payload},
        indent=2,
        ensure_ascii=False,
    ) + "\n"


def render_chunk_specs(backlog: list[FillBacklogRow], *, top: int | None = None) -> str:
    active = [row for row in backlog if row.score > 0 and row.workflow_lane == "fill_first"]
    limit = 10 if top is None else max(0, top)
    selected = active[:limit]

    lines: list[str] = [
        "# Generated Normalized Fill Chunk Specs",
        "",
        "These are compact task skeletons for low-token delegation. They intentionally avoid clinical claims.",
        "Each chunk should be filled only from existing or newly ingested source-grounded `SRC-*` evidence.",
        "",
    ]

    for idx, row in enumerate(selected, start=1):
        gaps = (
            f"SOC {row.soc_gap}, IND {row.indication_gap}, REG {row.regimen_gap}, "
            f"Drug {row.drug_gap}, RF {row.redflag_gap}"
        )
        current = (
            f"SOC/IND/REG/Drug/RF = {row.current_soc_families}/"
            f"{row.current_indications}/{row.current_regimens}/"
            f"{row.current_drugs}/{row.current_redflags}"
        )
        flags = ", ".join(row.quality_flags) if row.quality_flags else "none"
        lines.extend([
            f"## Chunk {idx}: {row.disease_id}",
            "",
            f"- Tier: `{row.tier}`",
            f"- Score: `{row.score}`",
            f"- Review readiness: `{row.review_readiness_pct:.1f}%`",
            f"- Workflow lane: `{row.workflow_lane}`",
            f"- Current: `{current}`",
            f"- Gaps: `{gaps}`",
            f"- Recommended work: {row.recommended_chunk}",
            f"- Quality flags: `{flags}`",
            "",
            "Scope:",
            "- Inventory existing disease-specific YAML before authoring.",
            "- Prefer indication/regimen/drug/redflag fill when the disease is not biomarker-driven.",
            "- Add BMA only for a real guideline-backed actionable biomarker family, or document why no biomarker axis is appropriate.",
            "- Do not copy NSCLC-style variant splitting unless resistance/variant handling is clinically required and source-grounded.",
            "",
            "Low-token inventory commands:",
            "```powershell",
            f"py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease {row.disease_id} --compact-json",
            "```",
            "",
            "Validation:",
            "```powershell",
            "py -3.12 -m knowledge_base.validation.loader knowledge_base/hosted/content",
            "py -3.12 -m pytest tests/test_normalized_actionability_coverage.py",
            f"py -3.12 -m scripts.normalized_actionability_coverage --rank-fill-next --disease {row.disease_id} --compact-json",
            "```",
            "",
            "Suggested cheaper-model prompt:",
            "```text",
            f"Switch to GPT-5.4-Mini medium. For {row.disease_id}, do inventory/skeleton only: existing YAML paths, source IDs, normalized gaps, and validation commands. Do not author clinical claims or edit YAML.",
            "```",
            "",
        ])

    return "\n".join(lines).rstrip() + "\n"


def _record_line(item: dict[str, Any], fields: tuple[str, ...]) -> str:
    cells = [str(item.get("id") or "-")]
    for field_name in fields:
        value = item.get(field_name)
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        elif isinstance(value, dict):
            value = json.dumps(value, ensure_ascii=False, sort_keys=True)
        cells.append(str(value) if value not in (None, "") else "-")
    cells.append(str(item.get("path") or "-"))
    return "| " + " | ".join(cells) + " |"


def _inventory_command(inventory: DiseaseInventory) -> str:
    command = f"py -3.12 -m scripts.normalized_actionability_coverage --inventory-disease {inventory.disease_id}"
    if (
        len(inventory.bma_review_queue) == 1
        and inventory.coverage
        and len(inventory.bmas) < inventory.coverage.bma_total
    ):
        command += f" --inventory-queue {inventory.bma_review_queue[0]['queue_id']}"
    return command


def _review_packet_command(packet: BmaReviewPacket) -> str:
    command = f"py -3.12 -m scripts.normalized_actionability_coverage --review-packet --inventory-disease {packet.disease_id}"
    if packet.queue:
        command += f" --inventory-queue {packet.queue['queue_id']}"
    return command


def _shared_primary_sources(records: list[dict[str, Any]]) -> list[str]:
    primary_sets = [
        {source_id for source_id in (record.get("primary_sources") or []) if isinstance(source_id, str)}
        for record in records
        if record.get("primary_sources")
    ]
    if not primary_sets:
        return []
    shared = set.intersection(*primary_sets)
    return sorted(shared)


def _summarize_review_bma(data: dict[str, Any]) -> dict[str, Any]:
    evidence_source_ids: list[str] = []
    for entry in data.get("evidence_sources") or []:
        if isinstance(entry, dict) and isinstance(entry.get("source"), str):
            source_id = str(entry["source"])
            if source_id not in evidence_source_ids:
                evidence_source_ids.append(source_id)
    return {
        "id": data.get("id"),
        "path": data.get("__path"),
        "biomarker_id": data.get("biomarker_id"),
        "variant_qualifier": data.get("variant_qualifier"),
        "escat_tier": data.get("escat_tier"),
        "ukrainian_review_status": data.get("ukrainian_review_status"),
        "actionability_review_required": data.get("actionability_review_required"),
        "last_verified": data.get("last_verified"),
        "primary_sources": data.get("primary_sources") or [],
        "evidence_source_ids": evidence_source_ids,
        "evidence_source_count": len(data.get("evidence_sources") or []),
    }


def render_inventory_markdown(inventories: list[DiseaseInventory]) -> str:
    lines: list[str] = [
        "# Disease Fill Inventory",
        "",
        "This is a low-token inventory for planning source-grounded disease fill work.",
        "It does not author clinical claims or change YAML content.",
        "",
    ]

    for inventory in inventories:
        coverage = inventory.coverage
        backlog = inventory.backlog
        lines.extend([
            f"## {inventory.disease_id}",
            "",
            f"- Disease file: `{inventory.disease_path or '-'}`",
            f"- Name: {inventory.name}",
        ])
        if coverage:
            lines.append(
                "- Current normalized coverage: "
                f"SOC/IND/REG/Drug/RF = {coverage.standard_family_count}/"
                f"{coverage.indications}/{coverage.unique_regimen_count}/"
                f"{coverage.unique_drug_count}/{coverage.redflags}; "
                f"BMA/families = {coverage.bma_total}/{coverage.normalized_family_count}; "
                f"inflation = {coverage.bma_variant_inflation_ratio or '-'}"
            )
        if backlog:
            flags = ", ".join(backlog.quality_flags) if backlog.quality_flags else "none"
            lines.append(
                "- Backlog: "
                f"tier `{backlog.tier}`, score `{backlog.score}`, "
                f"gaps SOC/IND/REG/Drug/RF = {backlog.soc_gap}/"
                f"{backlog.indication_gap}/{backlog.regimen_gap}/"
                f"{backlog.drug_gap}/{backlog.redflag_gap}; flags `{flags}`"
            )
            lines.append(f"- Recommended next chunk: {backlog.recommended_chunk}")
        blockers = inventory.bma_review_blockers
        lines.append(
            "- BMA review blockers: "
            f"pending_signoff={blockers['pending_clinical_signoff_count']}, "
            f"review_required={blockers['actionability_review_required_count']}"
        )
        consistency = inventory.bma_metadata_consistency
        lines.append(
            "- BMA metadata consistency: "
            f"ready={consistency['metadata_ready_count']}, "
            f"missing_primary={consistency['missing_primary_sources_count']}, "
            f"missing_evidence={consistency['missing_evidence_sources_count']}, "
            f"missing_contra={consistency['missing_contraindicated_monotherapy_count']}, "
            f"guideline_order_mismatch={consistency['guideline_evidence_order_mismatch_count']}"
        )
        family_summary = ", ".join(
            f"{item['biomarker_id']} x{item['count']}"
            for item in inventory.bma_families
        )
        if family_summary:
            lines.append(f"- BMA family groups: {family_summary}")
        if inventory.bma_review_queue:
            queue_summary = ", ".join(
                f"{item['queue_id']}[{item['priority']}] x{item['record_count']}"
                for item in inventory.bma_review_queue
            )
            lines.append(f"- BMA review queue: {queue_summary}")
        regimen_consistency = inventory.regimen_wiring_consistency
        lines.append(
            "- Regimen wiring consistency: "
            f"linked={regimen_consistency['linked_regimen_count']}, "
            f"missing_records={regimen_consistency['missing_regimen_record_count']}, "
            f"missing_sources={regimen_consistency['regimens_missing_sources_count']}, "
            f"wired={regimen_consistency['wired_regimen_count']}"
        )
        if inventory.stale_sources:
            stale = ", ".join(
                f"{item['id']} -> {item.get('superseded_by') or 'review'}"
                for item in inventory.stale_sources
            )
            lines.append(f"- Stale source refs detected: {stale}")

        lines.extend([
            "",
            "### BMA Files",
            "",
            "| ID | Biomarker | ESCAT | Review | Review Required | Verified | Path |",
            "|---|---|---|---|---|---|---|",
        ])
        for item in inventory.bmas:
            lines.append(
                _record_line(
                    item,
                    (
                        "biomarker_id",
                        "escat_tier",
                        "ukrainian_review_status",
                        "actionability_review_required",
                        "last_verified",
                    ),
                )
            )

        lines.extend([
            "",
            "### BMA Families",
            "",
            "| Biomarker | Records | Highest ESCAT | Record IDs |",
            "|---|---:|---|---|",
        ])
        for item in inventory.bma_families:
            lines.append(
                "| "
                f"{item['biomarker_id']} | {item['count']} | "
                f"{item.get('highest_escat_tier') or '-'} | "
                f"{', '.join(item['record_ids'])} |"
            )

        lines.extend([
            "",
            "### BMA Review Queue",
            "",
            "| Queue | Priority | Records | Biomarkers | Reason |",
            "|---|---|---:|---|---|",
        ])
        for item in inventory.bma_review_queue:
            lines.append(
                "| "
                f"{item['queue_id']} | {item['priority']} | {item['record_count']} | "
                f"{', '.join(item['biomarker_ids'])} | {item['reason']} |"
            )

        lines.extend([
            "",
            "### BMA Metadata Consistency",
            "",
            "| Check | Count | IDs |",
            "|---|---:|---|",
            f"| Metadata-ready rows | {consistency['metadata_ready_count']} | {', '.join(consistency['metadata_ready_ids']) or '-'} |",
            f"| Missing `primary_sources` | {consistency['missing_primary_sources_count']} | {', '.join(consistency['missing_primary_sources_ids']) or '-'} |",
            f"| Missing `evidence_sources` | {consistency['missing_evidence_sources_count']} | {', '.join(consistency['missing_evidence_sources_ids']) or '-'} |",
            f"| Missing `contraindicated_monotherapy` | {consistency['missing_contraindicated_monotherapy_count']} | {', '.join(consistency['missing_contraindicated_monotherapy_ids']) or '-'} |",
            f"| Guideline evidence order mismatch | {consistency['guideline_evidence_order_mismatch_count']} | {', '.join(consistency['guideline_evidence_order_mismatch_ids']) or '-'} |",
            "",
            "### Regimen Wiring Consistency",
            "",
            "| Check | Count | IDs |",
            "|---|---:|---|",
            f"| Linked regimens from indications | {regimen_consistency['linked_regimen_count']} | {', '.join(regimen_consistency['linked_regimen_ids']) or '-'} |",
            f"| Missing regimen records | {regimen_consistency['missing_regimen_record_count']} | {', '.join(regimen_consistency['missing_regimen_record_ids']) or '-'} |",
            f"| Existing linked regimens missing `sources` | {regimen_consistency['regimens_missing_sources_count']} | {', '.join(regimen_consistency['regimens_missing_sources_ids']) or '-'} |",
            f"| Fully wired linked regimens | {regimen_consistency['wired_regimen_count']} | {', '.join(regimen_consistency['wired_regimen_ids']) or '-'} |",
            "",
            "### Indications",
            "",
            "| ID | Regimen | Line | NCCN | Signoffs | Path |",
            "|---|---|---|---|---|---|",
        ])
        for item in inventory.indications:
            lines.append(_record_line(item, ("recommended_regimen", "line_of_therapy", "nccn_category", "reviewer_signoffs")))

        lines.extend([
            "",
            "### Linked Regimens",
            "",
            "| ID | Name | Sources | Signoffs | Verified | Path |",
            "|---|---|---|---|---|---|",
        ])
        for item in inventory.regimens:
            lines.append(_record_line(item, ("name", "sources", "reviewer_signoffs", "last_verified")))

        lines.extend([
            "",
            "### Redflags",
            "",
            "| ID | Title | Severity | Verified | Path |",
            "|---|---|---|---|---|",
        ])
        for item in inventory.redflags:
            lines.append(_record_line(item, ("title", "severity", "last_verified")))

        lines.extend([
            "",
            "### Sources",
            "",
            "| ID | Type | Version | Currency | Superseded By | Verified | Path |",
            "|---|---|---|---|---|---|---|",
        ])
        for item in inventory.sources:
            lines.append(_record_line(item, ("source_type", "version", "currency_status", "superseded_by", "last_verified")))

        lines.extend([
            "",
            "### Next Low-Token Commands",
            "",
            "```powershell",
            f"{_inventory_command(inventory)} --compact-json",
            f"py -3.12 -m scripts.normalized_actionability_coverage --rank-fill-next --disease {inventory.disease_id} --compact-json",
            "py -3.12 -m pytest tests/test_normalized_actionability_coverage.py",
            "```",
            "",
            "Suggested cheaper-model command:",
            "```text",
            f"Switch to GPT-5.4-Mini medium. Use `{_inventory_command(inventory)} --compact-json` as the only inventory input. Produce a source-grounded YAML edit plan only; do not author clinical claims.",
            "```",
            "",
        ])

    return "\n".join(lines).rstrip() + "\n"


def render_inventory_json(inventories: list[DiseaseInventory], *, compact: bool = False) -> str:
    return json.dumps(
        {"inventories": [inventory.to_jsonable(compact=compact) for inventory in inventories]},
        indent=2,
        ensure_ascii=False,
    ) + "\n"


def render_review_packet_markdown(packets: list[BmaReviewPacket]) -> str:
    lines: list[str] = [
        "# Clinical Review Packet",
        "",
        "This packet is a signoff-oriented review surface built from existing YAML and source links.",
        "It does not author new clinical claims or modify signoff state.",
        "",
    ]

    for packet in packets:
        lines.extend([
            f"## {packet.disease_id}",
            "",
            f"- Disease file: `{packet.disease_path or '-'}`",
            f"- Name: {packet.name}",
        ])
        if packet.queue:
            lines.append(
                f"- Queue: `{packet.queue['queue_id']}` [{packet.queue['priority']}] "
                f"for {packet.queue['record_count']} records; {packet.queue['reason']}"
            )
        shared_primary = _shared_primary_sources(packet.bmas)
        lines.append(f"- Shared primary sources: {', '.join(shared_primary) if shared_primary else '-'}")
        consistency = packet.metadata_consistency
        lines.append(
            "- Metadata consistency: "
            f"ready={consistency['metadata_ready_count']}, "
            f"missing_primary={consistency['missing_primary_sources_count']}, "
            f"missing_evidence={consistency['missing_evidence_sources_count']}, "
            f"missing_contra={consistency['missing_contraindicated_monotherapy_count']}, "
            f"guideline_order_mismatch={consistency['guideline_evidence_order_mismatch_count']}"
        )
        lines.extend([
            "",
            "### Record Matrix",
            "",
            "| ID | Biomarker | ESCAT | Review | Verified | Primary Sources | Evidence Sources | Path |",
            "|---|---|---|---|---|---|---|---|",
        ])
        for record in packet.bmas:
            lines.append(
                "| "
                f"{record['id']} | {record.get('biomarker_id') or '-'} | {record.get('escat_tier') or '-'} | "
                f"{record.get('ukrainian_review_status') or '-'} | {record.get('last_verified') or '-'} | "
                f"{', '.join(record.get('primary_sources') or []) or '-'} | "
                f"{', '.join(record.get('evidence_source_ids') or []) or '-'} | "
                f"{record.get('path') or '-'} |"
            )

        lines.extend([
            "",
            "### Linked Context",
            "",
            f"- Indications: {', '.join(item['id'] for item in packet.indications) if packet.indications else '-'}",
            f"- Regimens: {', '.join(item['id'] for item in packet.regimens) if packet.regimens else '-'}",
            f"- Source IDs: {', '.join(item['id'] for item in packet.sources) if packet.sources else '-'}",
            "",
            "### Review Tasks",
            "",
            "- Confirm claim language against the already-cited guideline and study sources.",
            "- Preserve `pending_clinical_signoff` and `actionability_review_required` until clinician review is complete.",
            "- Use metadata-ready status to avoid reopening structural cleanup unless the reviewer requests it.",
            "",
            "### Low-Token Command",
            "",
            "```powershell",
            f"{_review_packet_command(packet)} --compact-json",
            "```",
            "",
            "Suggested cheaper-model prompt:",
            "```text",
            f"Switch to GPT-5.4-Mini medium. Use `{_review_packet_command(packet)} --compact-json` as the only input. Produce a source-grounded clinical review packet plan and YAML edit plan. Do not author new clinical claims. Do not edit files.",
            "```",
            "",
        ])

    return "\n".join(lines).rstrip() + "\n"


def render_review_packet_json(packets: list[BmaReviewPacket], *, compact: bool = False) -> str:
    return json.dumps(
        {"review_packets": [packet.to_jsonable(compact=compact) for packet in packets]},
        indent=2,
        ensure_ascii=True,
    ) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    parser.add_argument("--compact-json", action="store_true", help="Emit reduced JSON fields")
    parser.add_argument(
        "--rank-fill-next",
        action="store_true",
        help="Emit normalized fill backlog instead of the coverage report",
    )
    parser.add_argument(
        "--chunk-specs",
        action="store_true",
        help="Emit compact delegation chunk specs from the fill backlog",
    )
    parser.add_argument(
        "--review-packet",
        action="store_true",
        help="Emit a signoff-oriented review packet for a disease or disease queue",
    )
    parser.add_argument(
        "--inventory-disease",
        action="append",
        help="Emit a low-token inventory for a disease id. May be repeated.",
    )
    parser.add_argument(
        "--inventory-queue",
        help="When used with --inventory-disease, narrow BMA output to one review queue id.",
    )
    parser.add_argument("--top", type=int, help="Limit rendered rows/chunks")
    parser.add_argument(
        "--disease",
        action="append",
        help="Filter to a disease id, e.g. DIS-ENDOMETRIAL. May be repeated.",
    )
    parser.add_argument(
        "--tier",
        action="append",
        choices=PLANNING_TIERS,
        help="Filter to a planning tier. May be repeated.",
    )
    parser.add_argument(
        "--workflow-lane",
        action="append",
        choices=("fill_first", "review_ready", "freeze_expand"),
        help="Filter backlog rows to a workflow lane. May be repeated.",
    )
    parser.add_argument("--out", type=Path, help="Write report to a file")
    args = parser.parse_args()

    rows = build_report()
    if args.review_packet:
        packets = build_review_packets(args.inventory_disease or [], queue_id=args.inventory_queue)
        text = (
            render_review_packet_json(packets, compact=args.compact_json)
            if args.json or args.compact_json
            else render_review_packet_markdown(packets)
        )
    elif args.inventory_disease:
        inventories = build_inventory(args.inventory_disease)
        if args.inventory_queue:
            inventories = [_filter_inventory_by_queue(item, args.inventory_queue) for item in inventories]
        text = (
            render_inventory_json(inventories, compact=args.compact_json)
            if args.json or args.compact_json
            else render_inventory_markdown(inventories)
        )
    elif args.chunk_specs:
        backlog = build_fill_backlog(rows)
        backlog = _filter_backlog_rows(
            backlog,
            diseases=args.disease,
            tiers=args.tier,
            workflow_lanes=args.workflow_lane,
            top=args.top,
            active_only=True,
        )
        text = render_chunk_specs(backlog, top=args.top)
    elif args.rank_fill_next:
        backlog = build_fill_backlog(rows)
        backlog = _filter_backlog_rows(
            backlog,
            diseases=args.disease,
            tiers=args.tier,
            workflow_lanes=args.workflow_lane,
            top=args.top,
        )
        text = (
            render_backlog_json(backlog, compact=args.compact_json)
            if args.json or args.compact_json
            else render_backlog_markdown(backlog, top=args.top)
        )
    else:
        rows = _filter_coverage_rows(
            rows,
            diseases=args.disease,
            tiers=args.tier,
            top=args.top,
        )
        text = (
            render_json(rows, compact=args.compact_json)
            if args.json or args.compact_json
            else render_markdown(rows, top=args.top)
        )
    if args.out:
        target = args.out if args.out.is_absolute() else REPO_ROOT / args.out
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
