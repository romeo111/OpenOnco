# OncoKB API response fixtures

Renamed from `oncokb_responses/` → `actionability_responses/` during the
CIViC pivot (see
`docs/reviews/oncokb-public-civic-coverage-2026-04-27.md`). The fixtures
remain in OncoKB IndicatorQueryResp shape — they are useful for parser-
shape testing if a Phase 4 OncoKB-compatible reader ever ships, and they
document the upstream wire format for reference.

🟡 **SYNTHESIZED** — these JSONs were synthesized from the public OncoKB
API docs ([api.oncokb.org/oncokb-website/api](https://api.oncokb.org/oncokb-website/api)
+ [oncokb-annotator AnnotatorCore.py](https://github.com/oncokb/oncokb-annotator/blob/master/AnnotatorCore.py))
during Phase 0 mock-mode work. **No real-token capture is planned** —
the OncoKB ToS forbids redistribution of OncoKB Content (audit
2026-04-27), and OpenOnco's primary actionability source is now CIViC
(CC0). The `_provisional: true` flag on every fixture stays as a
documentation marker that this data is synthesized, not captured.

## Shape (verified by public docs)

```jsonc
{
  "query": {
    "hugoSymbol": "BRAF",
    "entrezGeneId": 673,
    "alteration": "V600E",
    "tumorType": "MEL",
    "consequence": "missense_variant",
    "proteinStart": 600,
    "proteinEnd": 600
  },
  "geneExist": true,
  "variantExist": true,
  "alleleExist": true,
  "oncogenic": "Oncogenic",
  "mutationEffect": {
    "knownEffect": "Gain-of-function",
    "description": "...",
    "citations": {"pmids": ["..."], "abstracts": []}
  },
  "highestSensitiveLevel": "LEVEL_1",
  "highestResistanceLevel": null,
  "highestDiagnosticImplicationLevel": null,
  "highestPrognosticImplicationLevel": null,
  "otherSignificantSensitiveLevels": [],
  "otherSignificantResistanceLevels": [],
  "hotspot": true,
  "geneSummary": "...",
  "variantSummary": "...",
  "tumorTypeSummary": "...",
  "prognosticSummary": "",
  "diagnosticSummary": "",
  "diagnosticImplications": null,
  "prognosticImplications": null,
  "treatments": [
    {
      "level": "LEVEL_1",
      "drugs": [{"drugName": "Vemurafenib"}, {"drugName": "Cobimetinib"}],
      "pmids": ["28891423", "29320654"],
      "abstracts": [],
      "description": "...",
      "alterations": ["V600E"],
      "approvedIndications": [...]   // OPTIONAL — not always present
    }
  ],
  "dataVersion": "v4.21",
  "lastUpdate": "2026-04-15",
  "vus": false
}
```

## Critical knowns

- `treatments[].level` format = `LEVEL_1`, `LEVEL_3A`, `LEVEL_R1`, etc.
  (our parser strips `LEVEL_` prefix)
- `treatments[].drugs[]` are objects with `drugName` (not flat strings)
- `treatments[].pmids` is a flat list of strings
- `treatments[].abstracts` is a separate list (not folded into pmids)
- **`fdaApproved` field DOES NOT EXIST** at treatment level — Q8 FDA badge
  needs alternative source (look up Drug entity in our KB)

## Critical unknowns (would have been resolved by real-curl, now moot)

- exact OncoKB-canonical drug-name spelling (capitalization)
- `description` field — present in some responses, absent in others?
- precise structure of `treatments[].approvedIndications` if present
- whether real responses include `query.entrezGeneId` for valid genes

The proxy code that consumed these (`services/oncokb_proxy/app.py`) was
deleted in Phase 1 of the CIViC pivot. The fixture-shape tests in
`tests/test_actionability_contract_fixtures.py` still run as pure-data
contract checks.
