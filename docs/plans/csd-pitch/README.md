# OpenOnco × CSD Lab — Pitch Pack

🇬🇧 English · 🇺🇦 [Українська](uk/README.md)

Assembled 2026-04-27. KB snapshot: 2 413 entities. Site: https://openonco.info ·
GitHub: https://github.com/romeo111/OpenOnco

## What's in this folder

| # | File | What it shows |
|---|---|---|
| 01 | `01_clinician_demo.html` | End-to-end clinician demo: BRAF V600E + mCRC NGS report → ESCAT/OncoKB tier badges + NSZU availability + sign-off status. ~63 KB, A4-printable. |
| 02 | `02_patient_demo.html` | Patient-mode render with QR code. UA plain-language, emergency-RF banner, "what to ask your doctor" section. ~50 KB. |
| 03 | `03_drug_registration_completion.md` | 167/167 oncology drugs with verified UA registration + NSZU reimbursement (100% acceptance). |
| 04 | `04_solid_tumor_audit.md` | Solid-tumor expansion plan: gap audit + categorization. |
| 05 | `05_bundle_architecture.md` | Lazy-load bundle architecture: core 1.99 MB + per-disease modules. |
| 06 | `06_signoff_status.md` | Clinical sign-off coverage dashboard (CHARTER §6.1). |
| 07 | `07_clinical_signoff_workflow.md` | Guide for Clinical Co-Leads: CLI + dashboard + audit log. |
| 08 | `08_engine_lazy_load.md` | Bundle architecture (technical detail). |
| 09 | `09_clinical_questions.md` | 64 yes/no/clarify questions for a haematologist — grouped across 32 diagnoses. |
| — | `EMAIL.md` | Draft email to CSD Lab (UA, two versions — full + short). |

## KB snapshot (2026-04-27)

| Category | Count |
|---|---:|
| Total entities | **2 413** |
| Diseases | 65 |
| Indications | 302 |
| Algorithms | 110 |
| Regimens | 244 |
| Drugs | 216 (167 with verified UA registration) |
| RedFlags | 462 |
| BiomarkerActionability cells (ESCAT/OncoKB) | 399 |
| Biomarkers | 111 |
| Sources | 268 |
| Reviewer profiles (placeholders) | 3 |
| Tests | 1 450+ |

## What we offer CSD Lab

1. **Free clinical-interpretation overlay for your MyAction panels.**
   You provide wet lab + variant calling. We add ESCAT/OncoKB tier mapping +
   drug recommendations + UA NSZU availability + UA/EN patient-mode render.
   Open-source, MIT-style attribution. CHARTER §2 — non-commercial always.

2. **Coverage audit of your 4 panels** (MyAction BRCA1/2 / 18&18 / Solid 67 / 32 HRR).
   We show gene-by-gene: what is actionable, which ESCAT tier in which tumor type,
   and gaps (e.g. MSI-H/MMR not in Solid 67 — a potential panel extension).

3. **Sample interpretation report** for 3 anonymised test cases.
   1 haematological via M398 CLL, 1 solid via M396, 1 breast via M420.
   Side-by-side comparison of the current MyAction report vs the OpenOnco-augmented version.

4. **Pyodide widget** for embedding in your report PDF as a QR code.
   Patient scans → openonco.info/try.html opens with a pre-filled profile
   (browser-only state, nothing sent to a server).

## In exchange

One of your molecular oncologists becomes a **Clinical Co-Lead** for solid-tumor
content (CHARTER §6.1 requires 2 reviewers). This closes our sole existential
blocker — currently `reviewer_signoffs: []` on 100% of entities.
The infrastructure (CLI + dashboard + audit log) is ready — only a real
clinician is needed for ratification. Co-authorship credit on the open-source standard
for UA genomics.

## Technical implementation

- **Engine**: rule-based declarative system (not an LLM, not black-box AI). CHARTER §8.3 —
  LLMs are not clinical decision-makers. A clinician can audit why a given recommendation
  was made — every step is traceable to a KB entity with ≥2 sources.
- **Render**: Pyodide runtime in the browser. PHI never leaves the client browser
  (CHARTER §9.3). Lazy-load: ~1.4 MB core + ~30 KB per-disease modules.
- **Sign-off**: CLI + audit log + render badges. A real Co-Lead adds a profile YAML
  + bulk-approves via `scripts/clinical_signoff.py`.
- **License**: open-source MIT-style. CSD Lab attribution in every interpretation
  report while the partnership is active.

---

Contact: GitHub Issues — https://github.com/romeo111/OpenOnco/issues
