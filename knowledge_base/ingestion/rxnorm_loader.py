"""RxNorm loader — stub.

RxNorm ships as monthly RRF (Rich Release Format) files from NLM.
Requires UMLS Terminology Services license (free, academic).

Full implementation parses RXNCONSO.RRF + RXNREL.RRF and emits YAML
with `{rxcui, name, tty, ingredient_rxcui}` per SOURCE_INGESTION_SPEC
§13.4.

**Status:** not implemented in MVP. For HCV-MZL seed we hand-enter
RxNorm IDs in Drug entities (see `knowledge_base/hosted/content/drugs/*.yaml`).

TODO: implement when we add another disease area with dozens of new
drugs and hand-curation becomes impractical.
"""

import sys


def main() -> int:
    print("rxnorm_loader: not yet implemented — see module docstring.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
