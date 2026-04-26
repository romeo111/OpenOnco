# 0003 — No real patient data in public artifacts

No patient-identifying data may flow into the public repo, the build artifacts, the gallery, or any third-party system the project integrates with. CHARTER §9.3 requires informed consent + de-identification + ethics approval before any patient data can be made public, and the project does not currently have those.

The two Ukrainian HTML files at the repo root (`*план лікування.html`) are real first-patient deliverables. They are gitignored on purpose — never stage them, never move them without explicit user instruction, never include them in synthetic-fixture batches.

All gallery cases under `examples/patient_*.json` are synthetic profiles authored for demonstration; they do not represent any real patient.

## Why

The project's value depends on clinicians trusting that uploading a patient profile to the system does not put that patient's data on the public internet. A single leak — even an "anonymised" one without informed consent — undermines the trust the system is built on.

## Consequences

- Refactor proposals that "ingest" patient data from clinical sources into the build pipeline, the engine, or any cached layer must show the consent / de-identification / ethics-approval chain. Without it, the proposal is a non-starter.
- The `try.html` Pyodide demo runs entirely in the user's browser; refactors that move engine execution server-side must keep patient data off any logged or persisted layer.
- Test fixtures live under `examples/` and `tests/fixtures/`; both must remain synthetic.
