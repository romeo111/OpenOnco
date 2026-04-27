# OncoKB API response fixtures (provisional)

🟡 **PROVISIONAL** — synthesized from public OncoKB API docs
([api.oncokb.org/oncokb-website/api](https://api.oncokb.org/oncokb-website/api)
+ [oncokb-annotator AnnotatorCore.py](https://github.com/oncokb/oncokb-annotator/blob/master/AnnotatorCore.py)).
Replace with real-token curl captures during Phase 0 verification.

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

## Critical unknowns (real-curl will resolve)

- exact OncoKB-canonical drug-name spelling (capitalization)
- `description` field — present in some responses, absent in others?
- precise structure of `treatments[].approvedIndications` if present
- whether real responses include `query.entrezGeneId` for valid genes

When real fixtures land, also verify the parsing layer
(`services/oncokb_proxy/app.py:_call_oncokb`) handles all observed shapes.
