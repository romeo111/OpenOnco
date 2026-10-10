# OpenOnco interoperability gap analysis — 2026-10-10

Scope: conceptual mapping of the checked-in synthetic JSON input shape.
This is not a FHIR adapter, mCODE conformance report or OMOP implementation.
Reference: mCODE 4.0.0 STU4, FHIR R4 (current published guide checked today):
https://hl7.org/fhir/us/mcode/

| OpenOnco input | Candidate FHIR/mCODE representation | Missing work |
| --- | --- | --- |
| patient_id | Patient.identifier | Namespace and identity policy; do not export synthetic labels as real identities |
| disease.id / disease_id | PrimaryCancerCondition | Internal DIS identifiers need reviewed code mappings; entity codes alone do not meet profile requirements |
| demographics.age / sex | Patient and relevant observations | Age is not birthDate; administrative gender and clinical sex require explicit semantics |
| demographics.ecog | ECOGPerformanceStatus observation | Coding, effective time, subject references and profile validation |
| biomarkers | GenomicVariant / GenomicReport where applicable | Variant system, assay, specimen, status, dates and missing-value semantics |
| findings | Observation / DiagnosticReport where applicable | Unit normalization, LOINC mapping, dates and provenance; raw flags cannot be promoted to diagnoses |
| line_of_therapy | Context for treatment records | Does not reconstruct CancerRelatedMedicationAdministration or treatment episodes |
| generated regimen IDs | Draft planning context | A draft is not an administered medication event |

Mapping acceptance work: select supported profiles; pin package versions;
create fully synthetic fixtures; validate with the FHIR validator and mCODE
dependencies; test missing/unknown values and round trips; document every
unsupported element; obtain clinical and terminology review. No conformance
claim until this evidence exists. Licensed terminology gates still apply.

OHDSI Oncology WG focuses on observational oncology data in OMOP:
https://ohdsi.github.io/OncologyWG/
https://ohdsi.github.io/OncologyWG/gettingInvolved.html
Ask about the narrow mapping problem, not endorsement. OpenOnco currently
has no OMOP ETL, vocabulary mapping or observational outcomes dataset.
