# 0004 — Source hosting default is `referenced`, not `hosted`

Every Source enters the KB as `referenced` (linked to its canonical home, not stored in this repo) unless an explicit H1–H5 license-class justification exists for hosting. SOURCE_INGESTION_SPEC §1.4 enumerates the H1–H5 cases (e.g., public-domain primary literature, government-issued protocols, openly licensed datasets); anything else stays `referenced`.

`mixed` hosting (some content cached, some linked) is allowed for compound sources but each component still needs its own classification.

## Why

The project's licence position is non-commercial and free-public-resource (ADR-0001 footnote). Many upstream licences (ESMO CC-BY-NC-ND, OncoKB academic terms, NCCN paywalled access, ATC redistribution rules) prohibit mirroring. Defaulting to `hosted` for ingestion convenience would silently violate these licences.

`referenced` also forces the Indications and RedFlags that cite a Source to keep the citation surface stable: if the upstream URL or DOI moves, we update the Source entity, not 200 cases.

## Consequences

- Refactor proposals that involve "caching" or "mirroring" external databases (PubMed full text, NCCN protocols, ESMO PDFs) into the build artifact or the engine bundle are out of scope unless they fit H1–H5.
- The ingestion clients (`knowledge_base/clients/ctgov_client.py`, `pubmed_client.py`, etc.) are read-only adapters that produce `referenced` Source records by default. A refactor that adds a "download and store" path needs an ADR update.
- A future paid/commercial tier would invalidate this ADR for many sources and trigger a full licence audit. CHARTER §2 currently rules this out.
