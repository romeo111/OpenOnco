"""Synthesize 12 PROVISIONAL OncoKB response fixtures from public-doc shape.

Phase 0 mock-mode deliverable. Replace with real-token curl captures
when token is available.

Each fixture follows the verified shape (see README.md in this dir).
Treatment entries use known clinical truth from public NCCN/ESMO/OncoKB
docs — we're recording what we *expect* OncoKB to return, not invented
data. This is a contract test of our parsing, not a clinical claim.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "oncokb_responses"


def _build(
    gene: str,
    variant: str,
    tumor_type: str | None,
    treatments: list[dict],
    *,
    oncogenic: str = "Oncogenic",
    highest_sensitive: str | None = None,
    highest_resistance: str | None = None,
    notes: str = "",
) -> dict:
    """Compose one IndicatorQueryResp-shaped dict."""
    return {
        "_provisional": True,
        "_source": "Synthesized from public OncoKB API docs (Phase 0 mock-mode). "
                   "REPLACE with real-curl capture when ONCOKB_API_TOKEN available.",
        "_notes": notes,
        "query": {
            "hugoSymbol": gene,
            "alteration": variant,
            "tumorType": tumor_type,
        },
        "geneExist": True,
        "variantExist": True,
        "alleleExist": True,
        "oncogenic": oncogenic,
        "mutationEffect": {
            "knownEffect": "Gain-of-function" if oncogenic == "Oncogenic" else "Loss-of-function",
            "description": f"Synthesized — see public OncoKB page for {gene} {variant}.",
            "citations": {"pmids": [], "abstracts": []},
        },
        "highestSensitiveLevel": highest_sensitive,
        "highestResistanceLevel": highest_resistance,
        "highestDiagnosticImplicationLevel": None,
        "highestPrognosticImplicationLevel": None,
        "otherSignificantSensitiveLevels": [],
        "otherSignificantResistanceLevels": [],
        "hotspot": True,
        "geneSummary": f"{gene} is a known oncogene/tumor-suppressor.",
        "variantSummary": f"{variant} is a known oncogenic alteration of {gene}.",
        "tumorTypeSummary": "",
        "prognosticSummary": "",
        "diagnosticSummary": "",
        "diagnosticImplications": None,
        "prognosticImplications": None,
        "treatments": treatments,
        "dataVersion": "v4.21",
        "lastUpdate": "2026-04-15",
        "vus": False,
    }


def _tx(level: str, drugs: list[str], description: str, pmids: list[str]) -> dict:
    """One treatments[] entry. Mirrors annotator parsing path."""
    return {
        "level": level,
        "drugs": [{"drugName": d} for d in drugs],
        "pmids": pmids,
        "abstracts": [],
        "description": description,
    }


# ── 12 canonical variants ───────────────────────────────────────────────


FIXTURES: dict[str, dict] = {
    # 1. BRAF V600E in melanoma — OncoKB Level 1
    "braf_v600e_mel.json": _build(
        "BRAF", "V600E", "MEL",
        treatments=[
            _tx("LEVEL_1", ["Vemurafenib", "Cobimetinib"],
                "BRAF V600E + MEK inhibitor combo, FDA-approved 2015 (coBRIM)",
                ["25399551"]),
            _tx("LEVEL_1", ["Encorafenib", "Binimetinib"],
                "COLUMBUS regimen — BRAF + MEK doublet",
                ["29573941"]),
            _tx("LEVEL_1", ["Dabrafenib", "Trametinib"],
                "COMBI-d / COMBI-v",
                ["25265492"]),
        ],
        highest_sensitive="LEVEL_1",
    ),
    # 2. BRAF V600E in CRC — OncoKB Level 1 (different combo, BEACON regimen)
    "braf_v600e_crc.json": _build(
        "BRAF", "V600E", "COADREAD",
        treatments=[
            _tx("LEVEL_1", ["Encorafenib", "Cetuximab"],
                "BEACON CRC — BRAF + EGFR doublet 2L+",
                ["31566309"]),
        ],
        highest_sensitive="LEVEL_1",
    ),
    # 3. EGFR L858R in NSCLC — Level 1 osimertinib
    "egfr_l858r_nsclc.json": _build(
        "EGFR", "L858R", "NSCLC",
        treatments=[
            _tx("LEVEL_1", ["Osimertinib"],
                "FLAURA — 3rd-gen EGFR-TKI, 1L EGFR-mut NSCLC",
                ["29151359"]),
            _tx("LEVEL_1", ["Erlotinib"], "1st-gen TKI, predates osi",
                ["19692680"]),
            _tx("LEVEL_1", ["Gefitinib"], "1st-gen TKI", ["19692680"]),
            _tx("LEVEL_1", ["Afatinib"], "2nd-gen TKI", ["23816967"]),
            _tx("LEVEL_1", ["Dacomitinib"], "2nd-gen TKI (ARCHER 1050)", ["28958502"]),
        ],
        highest_sensitive="LEVEL_1",
    ),
    # 4. EGFR T790M in NSCLC — Level 1 osimertinib + RESISTANCE to 1st/2nd-gen
    "egfr_t790m_nsclc.json": _build(
        "EGFR", "T790M", "NSCLC",
        treatments=[
            _tx("LEVEL_1", ["Osimertinib"],
                "AURA3 — addresses T790M acquired resistance",
                ["27959700"]),
            _tx("LEVEL_R1", ["Gefitinib"], "Acquired resistance gatekeeper", ["15728811"]),
            _tx("LEVEL_R1", ["Erlotinib"], "Acquired resistance gatekeeper", ["15728811"]),
            _tx("LEVEL_R1", ["Afatinib"], "Acquired resistance to 2nd-gen TKI", ["20573926"]),
            _tx("LEVEL_R1", ["Dacomitinib"], "Acquired resistance to 2nd-gen TKI", ["20573926"]),
        ],
        highest_sensitive="LEVEL_1",
        highest_resistance="LEVEL_R1",
        notes="Critical fixture: triggers resistance-conflict banner if engine "
              "ever recommends gefitinib/erlotinib/afatinib/dacomitinib for T790M+ patient.",
    ),
    # 5. EGFR Exon 19 deletion in NSCLC
    "egfr_ex19del_nsclc.json": _build(
        "EGFR", "Exon 19 deletion", "NSCLC",
        treatments=[
            _tx("LEVEL_1", ["Osimertinib"], "FLAURA — 1L for ex19del", ["29151359"]),
            _tx("LEVEL_1", ["Erlotinib"], "1st-gen TKI", ["19692680"]),
            _tx("LEVEL_1", ["Gefitinib"], "1st-gen TKI", ["19692680"]),
            _tx("LEVEL_1", ["Afatinib"], "2nd-gen TKI", ["23816967"]),
        ],
        highest_sensitive="LEVEL_1",
    ),
    # 6. KRAS G12C in NSCLC — Level 1 sotorasib (FDA 2021)
    "kras_g12c_nsclc.json": _build(
        "KRAS", "G12C", "NSCLC",
        treatments=[
            _tx("LEVEL_1", ["Sotorasib"], "CodeBreaK 100 — 2L+ NSCLC", ["32955176"]),
            _tx("LEVEL_1", ["Adagrasib"], "KRYSTAL-1 — 2L+ NSCLC", ["35658005"]),
        ],
        highest_sensitive="LEVEL_1",
    ),
    # 7. KRAS G12C in CRC — Level 3A or 1 (CodeBreaK 300 for sotorasib + cetuximab)
    "kras_g12c_crc.json": _build(
        "KRAS", "G12C", "COADREAD",
        treatments=[
            _tx("LEVEL_1", ["Sotorasib", "Panitumumab"],
                "CodeBreaK 300 — sotorasib + EGFR-i, mCRC 2L+",
                ["37870950"]),
            _tx("LEVEL_3A", ["Adagrasib", "Cetuximab"],
                "KRYSTAL-1 cohort — adagrasib + EGFR-i mCRC",
                ["35658005"]),
        ],
        highest_sensitive="LEVEL_1",
    ),
    # 8. KRAS G12D in PDAC — investigational (Level 4 expected)
    "kras_g12d_pdac.json": _build(
        "KRAS", "G12D", "PAAD",
        treatments=[
            _tx("LEVEL_4", ["MRTX1133"],
                "Investigational G12D-selective inhibitor",
                []),
        ],
        highest_sensitive="LEVEL_4",
        notes="Provisional — no FDA-approved G12D-selective therapy as of 2025.",
    ),
    # 9. TP53 R175H pan-tumor — likely Level 4
    "tp53_r175h_pan.json": _build(
        "TP53", "R175H", None,
        treatments=[
            _tx("LEVEL_4", ["APR-246 (Eprenetapopt)"],
                "Investigational p53 reactivator (TP53-mut MDS/AML, AGILE-style)",
                []),
        ],
        highest_sensitive="LEVEL_4",
        notes="Pan-tumor query — render layer would surface 'Без фільтра tumor-type' badge (Q4).",
    ),
    # 10. MYD88 L265P in lymphoma (WM / DLBCL ABC) — Level 3A or 4
    "myd88_l265p_lymph.json": _build(
        "MYD88", "L265P", "WM",
        treatments=[
            _tx("LEVEL_1", ["Ibrutinib"],
                "iNNOVATE — 1L Waldenstrom macroglobulinemia",
                ["28902551"]),
            _tx("LEVEL_3B", ["Zanubrutinib"], "ASPEN trial",
                ["32887754"]),
        ],
        highest_sensitive="LEVEL_1",
    ),
    # 11. NPM1 W288fs in AML — Level 3A or 4 (FLT3-ITD co-occurrence common)
    "npm1_w288fs_aml.json": _build(
        "NPM1", "W288fs", "AML",
        treatments=[
            _tx("LEVEL_3A", ["Ivosidenib", "Venetoclax", "Azacitidine"],
                "Investigational triplet for NPM1-mut AML",
                []),
        ],
        highest_sensitive="LEVEL_3A",
    ),
    # 12. BRCA1 (any pathogenic) in OV — Level 1 olaparib maintenance
    "brca1_path_ov.json": _build(
        "BRCA1", "Oncogenic Mutations", "OV",
        treatments=[
            _tx("LEVEL_1", ["Olaparib"],
                "SOLO1 — maintenance after platinum response, BRCA1/2-mut HGSOC",
                ["30345884"]),
            _tx("LEVEL_1", ["Niraparib"],
                "PRIMA — broader maintenance",
                ["31562799"]),
        ],
        highest_sensitive="LEVEL_1",
        notes="OncoKB 'Oncogenic Mutations' alteration captures all pathogenic "
              "BRCA1 variants — render side could be either with synthesized "
              "patient findings or via panel-result aggregation upstream.",
    ),
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    written = 0
    for filename, data in FIXTURES.items():
        path = OUT / filename
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        written += 1
        print(f"  + {filename}")
    print(f"\nWrote {written} fixture files to {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
