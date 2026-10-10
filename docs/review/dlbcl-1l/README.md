# DLBCL first-line clinician review packet

Synthetic review only. Engineering checks are not clinical approval. No treatment decision should be based on this packet.

Open index.html through the published site. Inspect each input, actual plan, trace and source. Assess each scenario and export feedback as JSON. Browser feedback is not a clinical sign-off. No real patient data is included or accepted by the builder.

Rebuild: `python -m scripts.build_clinician_review`. Technical contracts: `--check`. The builder reads existing public synthetic seeds and does not change clinical YAML.
