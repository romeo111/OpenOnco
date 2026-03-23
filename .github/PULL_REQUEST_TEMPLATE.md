## Report Submission Checklist

**What cancer type / case ID is this?**
<!-- e.g. BRE-001 — Triple-negative breast cancer, Stage II -->

**How was this report generated?**
- [ ] Claude Opus 4.6 via API
- [ ] Claude Sonnet via API
- [ ] Local LLM (specify model: _______)
- [ ] Manual research

**Strategy version used:** `strategy.md` seed-____

---

### Pre-submission checks

- [ ] Report file is at the correct path: `research_db/{category}/{subtype}/reports/{CASE_ID}_report.json`
- [ ] JSON is valid (no parse errors)
- [ ] `report_metadata.case_id` matches the benchmark case ID
- [ ] At least 8 treatments with full `rating_breakdown` fields
- [ ] At least 3 clinical trials with NCT IDs
- [ ] At least 4 combination strategies
- [ ] At least 4 supportive care entries
- [ ] At least 10 sources with URLs
- [ ] All treatments have `intent` field set (curative/adjuvant/neoadjuvant/palliative/salvage/maintenance)
- [ ] Composite ratings computed correctly (verify with `python cancer_research_scorer.py <file> --validate-only`)

### Local score (run before submitting)

```
python evaluate.py research_db/.../reports/CASE-ID_report.json --verbose
```

**Score:** ___/100
**Weakest dimension:** _______________

> **Minimum accepted score: 80/100.** The CI bot will re-score and block merge if below threshold.

---

### Notes

<!-- Anything unusual about this case, data gaps, or known limitations -->
