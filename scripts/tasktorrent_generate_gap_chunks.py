"""Generate sidecar handoffs for the remaining TaskTorrent OpenOnco chunks.

These three shelf chunks are claim-bearing or licensing-sensitive. In this
worktree, many of their candidate entities already exist as hosted drafts or
source stubs, so this generator emits review sidecars instead of duplicating
colliding `target_action: new` entities.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "knowledge_base" / "hosted" / "content"
TODAY = date(2026, 4, 27).isoformat()


BMA_IDS = [
    "BMA-JAK2-V617F-PV",
    "BMA-JAK2-V617F-ET",
    "BMA-JAK2-V617F-PMF",
    "BMA-CALR-ET",
    "BMA-CALR-PMF",
    "BMA-NPM1-AML",
    "BMA-BRAF-V600E-THYROID-ANAPLASTIC",
    "BMA-BRAF-V600E-CHOLANGIO",
    "BMA-IDH1-R132-CHOLANGIO",
    "BMA-HER2-AMP-GASTRIC",
    "BMA-HER2-AMP-CRC",
    "BMA-HER2-AMP-ESOPHAGEAL",
    "BMA-MGMT-METHYLATION-GBM",
    "BMA-HRD-STATUS-OVARIAN",
    "BMA-HRD-STATUS-PROSTATE",
    "BMA-HRD-STATUS-BREAST",
    "BMA-HRD-STATUS-PDAC",
    "BMA-CD30-CHL",
    "BMA-CD30-ALCL",
    "BMA-CXCR4-WHIM-WM",
    "BMA-EZH2-Y641-FL",
    "BMA-IGHV-UNMUTATED-CLL",
    "BMA-ESR1-MUT-BREAST",
]


REDFLAG_IDS = [
    "RF-T-ALL-MEDIASTINAL-AIRWAY",
    "RF-T-ALL-CNS-LEUKEMIA",
    "RF-T-ALL-EMERGENCY-TLS-LEUKOSTASIS",
    "RF-B-ALL-CNS-LEUKEMIA",
    "RF-B-ALL-EMERGENCY-TLS-LEUKOSTASIS",
    "RF-BURKITT-EMERGENCY-TLS",
    "RF-HGBL-DH-EMERGENCY-TLS",
    "RF-HGBL-DH-CNS-PROPHYLAXIS-TRIGGER",
    "RF-PMBCL-SVC-SYNDROME",
    "RF-PMBCL-MEDIASTINAL-AIRWAY",
    "RF-NSCLC-SVC-SYNDROME",
    "RF-NSCLC-BRAIN-METS-EMERGENCY",
    "RF-NSCLC-CORD-COMPRESSION",
    "RF-NSCLC-MALIGNANT-EFFUSION",
    "RF-PROSTATE-CORD-COMPRESSION",
    "RF-MM-CORD-COMPRESSION",
    "RF-MM-HYPERCALCEMIA",
    "RF-MM-HYPERVISCOSITY",
    "RF-ATLL-HYPERCALCEMIA",
    "RF-SCLC-SVC-SYNDROME",
    "RF-SCLC-BRAIN-METS-EMERGENCY",
    "RF-PCNSL-INTRACRANIAL-PRESSURE",
    "RF-MASTOCYTOSIS-FRAILTY-AGE",
    "RF-MASTOCYTOSIS-ORGAN-DYSFUNCTION",
    "RF-MASTOCYTOSIS-INFECTION-SCREENING",
    "RF-MASTOCYTOSIS-HIGH-RISK-BIOLOGY",
    "RF-MASTOCYTOSIS-TRANSFORMATION-PROGRESSION",
    "RF-GLIOMA-LOW-GRADE-FRAILTY-AGE",
    "RF-GLIOMA-LOW-GRADE-HIGH-RISK-BIOLOGY",
    "RF-GLIOMA-LOW-GRADE-TRANSFORMATION-PROGRESSION",
    "RF-GLIOMA-LOW-GRADE-INTRACRANIAL-PRESSURE",
]


INDICATION_IDS = [
    "IND-CERVICAL-METASTATIC-1L-PEMBRO-CHEMO-BEV",
    "IND-GLIOMA-LOW-GRADE-1L-RT-PCV",
]


SOURCE_IDS = [
    "SRC-NCCN-HEPATOBILIARY",
    "SRC-NCCN-MPN-2025",
    "SRC-NCCN-CNS-2025",
    "SRC-NCCN-THYROID-2025",
    "SRC-NCCN-SM-2025",
    "SRC-NCCN-HNSCC-2025",
    "SRC-NCCN-SARCOMA",
    "SRC-NCCN-BONE-SARCOMA",
    "SRC-NCCN-PEDIATRIC-SARCOMA",
    "SRC-NCCN-HEAD-AND-NECK",
    "SRC-ASCO-BTC-2023",
    "SRC-ESMO-BTC-2023",
    "SRC-ESMO-HNSCC-2020",
    "SRC-ESMO-SALIVARY",
    "SRC-ATA-ATC-2021",
    "SRC-ATA-THYROID-2015",
    "SRC-EANO-LGG-2024",
    "SRC-COMBI-D-LONG-2014",
    "SRC-COMBI-V-ROBERT-2015",
    "SRC-COMBI-AD-LONG-2017",
    "SRC-COLUMBUS-DUMMETT-2018",
    "SRC-SOLO1-MOORE-2018",
    "SRC-SOLO2-PUJADE-LAURAINE-2017",
    "SRC-PRIMA-GONZALEZ-MARTIN-2019",
    "SRC-PROFOUND-DEBONO-2020",
    "SRC-AETHERA-MOSKOWITZ-2015",
    "SRC-ECHELON-1-CONNORS-2018",
    "SRC-ECHELON-2-HORWITZ-2019",
    "SRC-KEYNOTE-177-ANDRE-2020",
    "SRC-KEYNOTE-164-LE-2020",
    "SRC-EMERALD-BIDARD-2022",
    "SRC-CAPITELLO291-TURNER-2023",
    "SRC-DESTINY-BREAST03-CORTES-2022",
    "SRC-DESTINY-BREAST04-MODI-2022",
    "SRC-DESTINY-CRC01-SIENA-2021",
    "SRC-DESTINYLUNG01-LI-2022",
    "SRC-DESTINYLUNG02-GOTO-2023",
    "SRC-NCCN-CERVICAL-2025",
    "SRC-ESMO-CERVICAL-2024",
    "SRC-GOG0213-COLEMAN-2017",
]


BLOCKED_BMA_ROWS = [
    ("BIO-HRAS x DIS-HNSCC", "needs source extraction before drafting"),
    ("BIO-AKT1 E17K x DIS-BREAST", "source exists under SRC-CAPITELLO291-TURNER-2023 but BMA requires clinical synthesis"),
    ("BIO-IDH-MUTATION x DIS-GLIOMA-LOW-GRADE", "needs INDIGO/vorasidenib citation review before new BMA"),
    ("BIO-TMB-HIGH pan-tumor", "needs tumor-agnostic pembrolizumab source decision"),
    ("BIO-MSI-STATUS pan-tumor", "deferred until canonical MSI-H vs DMMR representation is chosen"),
]


BLOCKED_REDFLAG_ROWS = [
    ("DIS-IFS", "no in-repo source for infantile fibrosarcoma"),
    ("DIS-IMT", "needs soft-tissue sarcoma source review"),
    ("DIS-MPNST", "needs soft-tissue sarcoma source review"),
    ("DIS-SALIVARY", "needs salivary-specific source review"),
    ("DIS-CHONDROSARCOMA", "needs bone cancer source review"),
    ("DIS-CHOLANGIOCARCINOMA", "needs cholangiocarcinoma-specific source extraction"),
    ("DIS-THYROID-ANAPLASTIC", "needs second source beyond NCCN thyroid"),
    ("DIS-THYROID-PAPILLARY", "needs second source beyond NCCN thyroid"),
    ("DIS-MTC", "needs second MTC source beyond NCCN thyroid"),
    ("DIS-HNSCC airway/hypercalcemia", "needs second source beyond NCCN HNSCC"),
]


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def find_entity(entity_id: str, subdir: str) -> Path:
    base = CONTENT / subdir
    pattern = re.compile(rf"^id:\s*['\"]?{re.escape(entity_id)}['\"]?\s*$", re.M)
    for path in sorted(base.rglob("*.yaml")):
        if pattern.search(path.read_text(encoding="utf-8", errors="ignore")):
            return path
    raise FileNotFoundError(f"{entity_id} under {subdir}")


def slug(entity_id: str) -> str:
    return entity_id.lower().replace("-", "_")


def sidecar_slug(entity_id: str, prefix: str) -> str:
    prefix_map = {"bma": "bma_", "rfx": "rf_", "ind": "ind_"}
    value = slug(entity_id)
    remove = prefix_map.get(prefix)
    if remove and value.startswith(remove):
        return value[len(remove) :]
    return value


def reset_outdir(outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    for path in outdir.glob("*.yaml"):
        path.unlink()
    manifest = outdir / "task_manifest.txt"
    if manifest.exists():
        manifest.unlink()


def contribution_header(chunk_id: str, target_action: str, source_path: Path) -> str:
    return (
        "_contribution:\n"
        f"  chunk_id: {chunk_id}\n"
        "  contributor: codex-agent\n"
        "  ai_tool: codex\n"
        "  ai_model: gpt-5\n"
        '  ai_model_version: ""\n'
        f"  target_action: {target_action}\n"
        f"  source_entity_path: {yaml_quote(rel(source_path))}\n"
        "  notes_for_reviewer: >\n"
        "    Review sidecar generated from an existing hosted draft/stub to avoid\n"
        "    colliding with tracked entities already present on this branch.\n\n"
    )


def write_meta(outdir: Path, chunk_id: str, notes: str) -> None:
    text = (
        f"chunk_id: {chunk_id}\n"
        f"chunk_spec_url: https://github.com/romeo111/task_torrent/blob/main/chunks/openonco/{chunk_id}.md\n"
        "contributor: codex-agent\n"
        f"submission_date: {TODAY}\n"
        "ai_tool: codex\n"
        "ai_model: gpt-5\n"
        'ai_model_version: ""\n'
        "notes_for_reviewer: >\n"
        f"  {notes}\n"
    )
    (outdir / "_contribution_meta.yaml").write_text(text, encoding="utf-8")


def copy_sidecar(chunk_id: str, entity_id: str, subdir: str, outdir: Path, prefix: str, target_action: str) -> str:
    source = find_entity(entity_id, subdir)
    body = source.read_text(encoding="utf-8")
    out = outdir / f"{prefix}_{sidecar_slug(entity_id, prefix)}.yaml"
    out.write_text(contribution_header(chunk_id, target_action, source) + body, encoding="utf-8")
    return f"{entity_id}::{rel(source)}::{out.name}"


def ensure_source_license_fields(text: str, source_id: str) -> str:
    additions: list[str] = []
    is_nccn = source_id.startswith("SRC-NCCN-")
    is_esmo = source_id.startswith("SRC-ESMO-")
    is_asco = source_id.startswith("SRC-ASCO-")
    is_guideline = is_nccn or is_esmo or is_asco or source_id.startswith(("SRC-ATA-", "SRC-EANO-"))

    if "\nlicense:" not in text:
        if is_nccn:
            additions.extend(
                [
                    "license:",
                    "  name: NCCN - clinician-only redistribution prohibited",
                    "  url: https://www.nccn.org/permissions",
                    "  spdx_id: null",
                ]
            )
        elif is_esmo:
            additions.extend(
                [
                    "license:",
                    "  name: ESMO guideline publication license - verify per article",
                    "  url: https://www.annalsofoncology.org/",
                    "  spdx_id: null",
                ]
            )
        elif is_asco:
            additions.extend(
                [
                    "license:",
                    "  name: ASCO publication permissions - redistribution restricted",
                    "  url: https://ascopubs.org/permissions",
                    "  spdx_id: null",
                ]
            )
        else:
            additions.extend(
                [
                    "license:",
                    "  name: Bibliographic metadata only - license requires reviewer verification",
                    "  spdx_id: null",
                ]
            )

    if "\nattribution:" not in text:
        additions.extend(["attribution:", "  required: true", f"  text: {yaml_quote(source_id)}"])

    bool_defaults = {
        "commercial_use_allowed": "false",
        "redistribution_allowed": "false" if is_guideline else "false",
        "modifications_allowed": "false",
        "sharealike_required": "false",
    }
    for key, value in bool_defaults.items():
        if f"\n{key}:" not in text:
            additions.append(f"{key}: {value}")

    if additions:
        text = text.rstrip() + "\n" + "\n".join(additions) + "\n"
    return text


def copy_source_sidecar(outdir: Path, source_id: str) -> str:
    source = find_entity(source_id, "sources")
    body = ensure_source_license_fields(source.read_text(encoding="utf-8"), source_id)
    out = outdir / f"source_stub_{slug(source_id)}.yaml"
    out.write_text(contribution_header("source-stub-ingest-batch", "review_existing_stub", source) + body, encoding="utf-8")
    return f"{source_id}::{rel(source)}::{out.name}"


def write_blocker_report(outdir: Path, chunk_id: str, rows: list[tuple[str, str]]) -> None:
    lines = [
        "_contribution:",
        f"  chunk_id: {chunk_id}",
        "  contributor: codex-agent",
        "  ai_tool: codex",
        "  ai_model: gpt-5",
        '  ai_model_version: ""',
        "blocked_items:",
    ]
    for item, reason in rows:
        lines.extend(
            [
                f"  - item: {yaml_quote(item)}",
                f"    reason: {yaml_quote(reason)}",
                "    disposition: \"not_drafted_without_source_or_clinical_review\"",
            ]
        )
    (outdir / "blocker-report.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_bma() -> tuple[int, int]:
    chunk_id = "bma-drafting-gap-diseases"
    outdir = ROOT / "contributions" / chunk_id
    reset_outdir(outdir)
    write_meta(
        outdir,
        chunk_id,
        "Review sidecar package for 23 already-hosted BMA drafts from docs/reviews/bma-coverage-2026-04-27.md; target_action is review_existing_hosted_draft to avoid collisions.",
    )
    manifest = [
        copy_sidecar(chunk_id, entity_id, "biomarker_actionability", outdir, "bma", "review_existing_hosted_draft")
        for entity_id in BMA_IDS
    ]
    (outdir / "task_manifest.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    write_blocker_report(outdir, chunk_id, BLOCKED_BMA_ROWS)
    return len(manifest), len(BLOCKED_BMA_ROWS)


def generate_redflag() -> tuple[int, int]:
    chunk_id = "redflag-indication-coverage-fill"
    outdir = ROOT / "contributions" / chunk_id
    reset_outdir(outdir)
    write_meta(
        outdir,
        chunk_id,
        "Review sidecar package for HIGH/CRITICAL redflag/indication drafts already present in hosted content; blocked rows list source-gated cells.",
    )
    manifest: list[str] = []
    for entity_id in REDFLAG_IDS:
        manifest.append(copy_sidecar(chunk_id, entity_id, "redflags", outdir, "rfx", "review_existing_hosted_draft"))
    for entity_id in INDICATION_IDS:
        manifest.append(copy_sidecar(chunk_id, entity_id, "indications", outdir, "ind", "review_existing_hosted_draft"))
    (outdir / "task_manifest.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    write_blocker_report(outdir, chunk_id, BLOCKED_REDFLAG_ROWS)
    return len(manifest), len(BLOCKED_REDFLAG_ROWS)


def generate_sources() -> tuple[int, int]:
    chunk_id = "source-stub-ingest-batch"
    outdir = ROOT / "contributions" / chunk_id
    reset_outdir(outdir)
    write_meta(
        outdir,
        chunk_id,
        "Metadata/licensing review sidecars for 40 existing Source stubs or partially verified sources prioritized by BMA/redflag gap reports.",
    )
    manifest = [copy_source_sidecar(outdir, source_id) for source_id in SOURCE_IDS]
    (outdir / "task_manifest.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    return len(manifest), 0


def main() -> None:
    bma_count, bma_blocked = generate_bma()
    rf_count, rf_blocked = generate_redflag()
    src_count, _ = generate_sources()
    print(f"bma sidecars: {bma_count}; blocked rows: {bma_blocked}")
    print(f"redflag/indication sidecars: {rf_count}; blocked rows: {rf_blocked}")
    print(f"source sidecars: {src_count}")


if __name__ == "__main__":
    main()
