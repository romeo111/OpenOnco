# Patient watchpoints — authoring queue

**Stamp:** 2026-05-01-0100 · **Status:** queue open · **Spec:** [`specs/PATIENT_MODE_SPEC.md`](../../specs/PATIENT_MODE_SPEC.md) §3.4 + §6 · **Schema landed in:** Phase 4 of the patient-mode v2.1 plan

## What this queue is

Phase 4 of the patient-mode iteration shipped the `Regimen.between_visit_watchpoints` schema + renderer + fallback. The remaining work — and what this doc tracks — is **authoring the actual content** for each of the 253 regimens currently in the KB.

Each `BetweenVisitWatchpoint` is a clinically-loaded statement (it tells a patient at home when to log a symptom vs call the clinic vs go to ER). Per CHARTER §6.1 + PATIENT_MODE_SPEC §6, each regimen's watchpoint list needs **two Clinical Co-Lead sign-offs** before it is considered authored. Until then, the renderer surfaces the placeholder string:

> Список того, на що звернути увагу між візитами, для цього курсу ще не узгоджено клінічною командою. Запитайте лікаря на наступному візиті, які симптоми треба занотовувати, а які — приводи дзвонити в клініку.

This is honest by design: the patient is told the list isn't ready, not given fabricated content.

## Estimated content volume

| Tier | Watchpoints/regimen | Regimens × tier | Subtotal |
|---|---:|---:|---:|
| `log_at_next_visit` | 2-3 | 253 | ~625 |
| `call_clinic_same_day` | 2-3 | 253 | ~625 |
| `er_now` | 1-2 | 253 | ~380 |
| **Total** | **5-8 / regimen** | | **~1,000–1,500** |

`er_now` items often dedupe with the existing emergency-RedFlag layer (renderer auto-handles via `_emergency_trigger_keys`), so net new ER-tier content ≈ 50% of nominal.

## Anchor regimens — Wave 1 priority

These 12 regimens are used in many tracks across diseases and have well-known AE profiles. Authoring them first delivers the biggest patient-bundle coverage per session:

| Priority | Regimen ID | Why first |
|---|---|---|
| 1 | `REG-CHOP` | DLBCL + several T-cell lymphomas; cytopenia / nadir watchpoint pattern |
| 2 | `REG-RCHOP` | Same as CHOP + rituximab infusion-reaction watchpoint |
| 3 | `REG-FOLFOX` | 1L mCRC + adjuvant CRC; oxaliplatin neuropathy + cold sensitivity |
| 4 | `REG-FOLFOX-BEV` | Same + bevacizumab BP / proteinuria watchpoints |
| 5 | `REG-DAA-SOF-VEL` | HCV-MZL standard; mostly mild watchpoints — good "easy first" template |
| 6 | `REG-BR-STANDARD` | HCV-MZL aggressive + iNHL salvage; bendamustine cytopenia + opportunistic infections |
| 7 | `REG-VRD` | MM 1L standard; bortezomib neuropathy + lenalidomide thrombosis |
| 8 | `REG-DARA-VRD` | MM 1L aggressive; same + daratumumab infusion / immunosuppression |
| 9 | `REG-A-AVD` | cHL 1L; brentuximab neuropathy |
| 10 | `REG-ATRA-ATO-APL` | APL emergency archetype; differentiation-syndrome watchpoint critical |
| 11 | `REG-VEN-AZA-AML` | AML unfit 1L; tumor-lysis-syndrome window |
| 12 | `REG-PEMBROLIZUMAB-MONO` | pan-tumor checkpoint; immune-related AE watchpoints — pattern reusable for nivolumab, atezolizumab, durvalumab |

**Wave 1 = ~80–100 watchpoints across 12 regimens.** Achievable in a single co-lead review session; covers ~30-40% of KB plan paths because anchor regimens repeat across diseases.

## Wave 2 — disease-anchor regimens (~50 regimens)

After Wave 1, broaden to one regimen per disease where Wave 1 doesn't already cover. Goal: every disease in the KB has ≥1 fully-authored regimen so every plan-track surfaces real watchpoints for at least one option.

## Wave 3 — long tail (~190 regimens)

Less common regimens (rare-tumor 2L+, salvage, etc.). Prioritize by curated-case usage from `scripts/site_cases.py` — regimens that appear in ≥1 published case go before regimens that don't.

## Authoring workflow

1. **Pick a regimen** from the priority list (Wave 1 first).
2. **Draft watchpoints** — between-visit clinically meaningful events grouped by urgency. Reference: ESMO patient guides, NCI-PDQ patient versions, NCCN patient information, FDA Med Guides for the constituent drugs.
3. **Review tier mapping:**
   - `log_at_next_visit` — annoying but not dangerous; mention at next visit.
   - `call_clinic_same_day` — call clinic, don't wait.
   - `er_now` — go to ER. Often duplicates an existing RedFlag — that's OK, the renderer dedupes against emergency banner so the patient doesn't see the same thing twice.
4. **Fill `cycle_day_window`** when the symptom is cycle-phase specific (cytopenia nadir, post-infusion reaction, etc.). Skip when not applicable.
5. **Cite sources** — `SRC-*` entity IDs from existing KB Sources. New sources need `source_stub_<id>.yaml` per SOURCE_INGESTION_SPEC §8.
6. **CHARTER §6.1 sign-off** — two Clinical Co-Leads append `reviewer_signoffs_v2` entries to the regimen YAML. Until both sign, the watchpoint list still loads (schema accepts it) but the patient bundle could optionally surface a "🟡 ще одна перевірка" badge on the regimen card. **(Render-side feature for follow-up — not in Phase 4.)**

## Tracking

Each authored regimen lands as a separate small PR (`feat(kb): patient watchpoints for REG-FOLFOX` etc.) or is bundled with other clinical-content updates. The queue is consumed top-down via the priority list above; status flips as PRs merge.

| Wave | Status | Authored / target |
|---|---|---|
| Wave 1 (12 anchor regimens) | not started | 0 / 12 |
| Wave 2 (~50 disease anchors) | not started | 0 / ~50 |
| Wave 3 (~190 long tail) | not started | 0 / ~190 |

Update this file when the first regimens land — flip Wave 1 to `in progress`, increment the counters as PRs merge.

## Out of scope for this queue

- **Translation to EN** — patient bundle is UA-only (PATIENT_MODE_SPEC §9).
- **Re-authoring AE_PLAIN_UA vocabulary** — separate vocabulary contract (§5.1); changes flow through `knowledge_base/engine/_patient_vocabulary.py`, not regimen YAMLs.
- **Regimen-specific monitoring schedules** — already lives in `MonitoringSchedule.phases` and renders via `_render_monitoring_phases` for the clinician bundle. The patient-mode "between-visits" section is complementary, not a duplicate: monitoring-schedule = labs and visits the clinic schedules; between-visits = patient-driven self-monitoring at home.

## Open questions for Clinical Co-Leads

1. **Tier consistency** — should the same trigger always map to the same urgency tier across regimens (e.g. "лихоманка >38°C" → always `call_clinic_same_day`)? Or can it shift based on regimen-specific risk (e.g. higher-risk regimens upgrade to `er_now`)? Plan currently allows per-regimen variation.
2. **Source-anchor floor** — should every watchpoint require ≥1 `SRC-*` citation, or is the regimen-level source list (already required by Pydantic) sufficient?
3. **Rare-event reporting** — should we surface watchpoints for events with <5% incidence, or keep the list focused on common events the patient is likely to encounter? Plan currently leans toward the latter (≥5% as a soft threshold).
