# OpenOnco

> **Open-source clinical decision support for oncology tumor boards.**
> Лікар завантажує профіль пацієнта → отримує два альтернативні плани
> лікування (стандартний + агресивний) із повними цитуваннями. Плани
> оновлюються при появі нових даних. Усе на rule engine + curated
> knowledge base, без LLM-судження.

🌐 **Live demo:** [openonco.info](https://openonco.info)
📖 **Specifications-first:** all clinical content under
[CHARTER §6.1](specs/CHARTER.md) dual-review per Clinical Co-Lead
🏥 **FDA non-device CDS positioning** per
[CHARTER §15](specs/CHARTER.md) — information support, not a medical device
📜 **License:** Code MIT · Content / specs CC BY 4.0

---

## Status — v0.1.0-alpha

First public alpha release covering **16 lymphoma diseases (Tier 1)**
and multiple myeloma 1L end-to-end. Knowledge base infrastructure, rule
engine, MDT orchestrator, render layer, and live Pyodide-powered
in-browser demo all functional. Clinical content is **STUB** pending
two-of-three Clinical Co-Lead sign-offs per CHARTER §6.1 — visible on
every rendered Plan as an explicit badge.

| Metric | Count |
|---|---|
| Knowledge-base entities | 251 |
| Diseases (full chain disease→indication→regimen→algorithm) | 18 |
| Standalone biomarker entities | 32 |
| Tier 1 lymphomas covered | 16 (DLBCL NOS, FL, CLL/SLL, MCL, HCV-MZL, SMZL, NMZL, Burkitt, HCL, WM, HGBL-DH, PTCL NOS, ALCL, AITL, MF/Sézary, cHL, NLPBL — ~80% NHL+HL by incidence) |
| Drug entities | 33 |
| Treatment regimens | 17 |
| Source citations (NCCN, ESMO, EHA, BSH, EASL, МОЗ, etc.) | 19 |
| Tests | 304 (all passing) |
| Specifications | 10 |

---

## What it does

**Two-track plan generator (CHARTER §2):** for any newly-diagnosed
case in the KB, the engine produces at least two alternative treatment
tracks side-by-side — never a single "system-prescribes-X" directive.
HCP makes the actual choice; the engine surfaces transparent rationale,
red-flag triggers, hard contraindications, supportive care, monitoring
schedule, expected outcomes with sourced numbers, and "what NOT to do"
prohibitive bullets per indication.

**Versioned skill registry (16 specialists):** hematologist,
hematopathologist, infectious-disease/hepatology, radiologist,
molecular geneticist, clinical pharmacist, radiation oncologist,
surgical oncologist, transplant specialist, cellular-therapy (CAR-T)
specialist, psychologist, palliative care, social worker / case
manager, primary care, medical oncologist (placeholder), pathologist
(generic). Each skill is a versioned rule bundle with `last_reviewed`,
`clinical_lead`, `verified_by` sign-offs, and source citations.

**Diagnostic-phase MDT (CHARTER §15.2 C7):** when histology is not yet
confirmed, the engine generates a Workup Brief (Indications: which
tests to run, biopsy approach, IHC panel, mandatory questions) instead
of a treatment Plan — mechanical hard gate that prevents premature
treatment recommendations.

**Plan revisions / supersedes loop:** new patient data → new Plan
version via `revise_plan(...)` (polymorphic across diagnostic→diagnostic,
diagnostic→treatment promotion, treatment→treatment); refuses illegal
treatment→diagnostic downgrade. Immutable supersedes/superseded_by
audit chain (CHARTER §10.2).

**Cross-disease biomarker entities (32 standalone):** every clinically
significant marker — TP53, IGHV, MYC, BCL2, BCL6 rearrangements, double-
hit, MYD88 L265P, CXCR4-WHIM, BRAF V600E, EZH2 Y641, ALK, RHOA G17V,
NOTCH1, CD20, CD30, CD52, CD79b, PD-L1, Ki-67, EBV, etc. — is a
citable single entity with cross-disease decision impact documented in
notes. Composites (CLL high-risk genetics, MM cytogenetics-HR, double-
hit) reference standalone components via `related_biomarkers`.

**FDA Criterion 4 metadata on every Plan:** `intended_use`,
`hcp_user_specification`, `patient_population_match`,
`algorithm_summary`, `data_sources_summary`, `data_limitations`,
`automation_bias_warning`, `time_critical` flag. Full algorithm
decision trace in every output.

**HTML render layer:** single-file A4-printable HTML per Plan /
Diagnostic Brief / Revision Note. Embedded CSS, no external assets
beyond Google Fonts. Sections: etiological driver (for
etiologically_driven archetype), pre-treatment investigations table,
RedFlag PRO/CONTRA categorization, "Що НЕ робити", monitoring schedule
phases, timeline, MDT skill catalog with version + sign-off status.
Both UA and EN render via `target_lang` parameter.

**Live in-browser demo (Pyodide):** the actual Python engine runs in
the browser at [openonco.info/try.html](https://openonco.info/try.html)
— no backend. Visitor pastes patient JSON, clicks Generate, sees
rendered Plan inline.

**Translation infrastructure:** DeepL Free + LibreTranslate self-hosted
fallback + on-disk cache + glossary protection (entity IDs, doses,
codes never sent to translator). Per CHARTER §8.3 every translation is
flagged `machine_translated: true` for clinical review.

---

## Repository layout

```
openonco/
├── specs/                          # 10 specifications (UA primary)
├── knowledge_base/
│   ├── schemas/                    # Pydantic schemas
│   ├── engine/                     # rule engine, MDT, render, revisions
│   ├── validation/                 # YAML loader + ref-integrity checker
│   ├── clients/                    # source-API + translate clients
│   ├── stats.py                    # KB info dashboard
│   └── hosted/content/             # YAML knowledge base (251 entities)
├── examples/                       # synthetic patient profiles
├── scripts/build_site.py           # static-site builder (GitHub Pages)
├── docs/                           # generated site → openonco.info
├── tests/                          # 304 tests
└── legacy/                         # retired autoresearch pipeline
```

## Quick start

```bash
# Install
pip install -e .

# Run engine on a synthetic patient
python -m knowledge_base.engine.cli examples/patient_zero_indolent.json --mdt --render plan.html

# Run tests
pytest tests/

# Build the site locally
python -m scripts.build_site --clean
python -m http.server 8000 --directory docs/
# → open http://localhost:8000

# View KB stats
python -m knowledge_base.stats
```

## Specifications

All specs are in [`specs/`](specs/). Read `CHARTER.md` first — it
governs scope, FDA positioning, dual-review process, and what the
project explicitly does NOT do.

- [`CHARTER.md`](specs/CHARTER.md) — governance, scope, FDA non-device CDS positioning
- [`CLINICAL_CONTENT_STANDARDS.md`](specs/CLINICAL_CONTENT_STANDARDS.md) — content editorial standards
- [`KNOWLEDGE_SCHEMA_SPECIFICATION.md`](specs/KNOWLEDGE_SCHEMA_SPECIFICATION.md) — KB schema
- [`DATA_STANDARDS.md`](specs/DATA_STANDARDS.md) — patient data model (FHIR R4/R5, mCODE)
- [`REFERENCE_CASE_SPECIFICATION.md`](specs/REFERENCE_CASE_SPECIFICATION.md) — reference HCV-MZL "Patient Zero"
- [`SOURCE_INGESTION_SPEC.md`](specs/SOURCE_INGESTION_SPEC.md) — licensing, ingestion, conflict resolution, freshness
- [`MDT_ORCHESTRATOR_SPEC.md`](specs/MDT_ORCHESTRATOR_SPEC.md) — tumor-board brief: roles, open questions, provenance
- [`DIAGNOSTIC_MDT_SPEC.md`](specs/DIAGNOSTIC_MDT_SPEC.md) — pre-biopsy mode (no histology → DiagnosticPlan, not treatment)
- [`WORKUP_METHODOLOGY_SPEC.md`](specs/WORKUP_METHODOLOGY_SPEC.md) — reusable methodology for any oncology domain
- [`SKILL_ARCHITECTURE_SPEC.md`](specs/SKILL_ARCHITECTURE_SPEC.md) — MDT roles as clinically-verified skills

## Contributing

Clinical content needs **two-of-three Clinical Co-Lead sign-offs** per
CHARTER §6.1 before STUB status flips to `reviewed`. Found a clinical
inaccuracy or want to contribute a disease, drug, or regimen? Open an
issue with the `tester-feedback` or `clinical-content` label —
templates available at:

- [Open an issue](https://github.com/romeo111/OpenOnco/issues/new) (after rename)
- [Site feedback (auto-prefilled)](https://openonco.info)

Code contributions: standard PR workflow. Tests must pass; new
clinical content must cite at least one Source entity. Spec changes
require Charter §6 review.

## Medical disclaimer

This project is an **informational resource** to support tumor-board
discussion. It is **not** a system that makes clinical decisions, not a
medical device, and not for use without a qualified oncologist. Every
recommendation must be verified by the treating physician with access
to the full clinical picture and discussed by a multidisciplinary team.
See [`specs/CHARTER.md`](specs/CHARTER.md) §11 + §15 for full
positioning.

## License

- **Code:** MIT
- **Specifications & content:** CC BY 4.0
- **Source citations** retain their original licenses (NCCN, ESMO, etc.
  are referenced not redistributed — see SOURCE_INGESTION_SPEC §3 for
  hosting modes per source)

## Acknowledgements

Built with: Pydantic, httpx, PyYAML, Pyodide. Standards-driven by NCCN,
ESMO, EHA, BSH, EASL, МОЗ України НСЗУ, WHO Classification of Tumours
5th ed., FDA Clinical Decision Software Guidance.
