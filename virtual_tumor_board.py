#!/usr/bin/env python3
"""
virtual_tumor_board.py — 5 Virtual Doctors with Adversarial Debate

Five oncologists with radically different treatment philosophies review
a cancer research report, argue with each other, and produce a consensus
(or documented dissent). Their debate exposes blind spots and improves
report quality.

Usage:
    python virtual_tumor_board.py report.json
    python virtual_tumor_board.py report.json --output debate.json
    python virtual_tumor_board.py report.json --format markdown --output debate.md
    python virtual_tumor_board.py --generate-prompt report.json > prompt.md

The doctors:
    Dr. Evidence    — Evidence Purist (only trusts Phase 3 RCTs)
    Dr. Aggressor   — Aggressive Interventionist (maximum intensity)
    Dr. Guardian    — Patient-Centered Integrationist (QoL + toxicity balance)
    Dr. Precision   — Precision Medicine Advocate (biomarkers + genomics)
    Dr. Frontier    — Clinical Trialist / Innovator (experimental + cutting-edge)
"""

import json
import sys
import argparse
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
# DOCTOR DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

DOCTORS = [
    {
        "id": "evidence",
        "name": "Dr. Evidence",
        "title": "The Evidence Purist — Medical Oncologist",
        "institution": "Memorial Academic Cancer Center",
        "years_experience": 22,
        "philosophy": "Evidence Purist",
        "personality": (
            "Rigorous, skeptical, data-driven. Refuses to recommend anything "
            "without Phase 3 RCT evidence. Considers conference abstracts "
            "preliminary and treats Phase 2 data as hypothesis-generating only. "
            "Distrusts surrogate endpoints — demands overall survival data. "
            "Will call out inflated claims immediately. Dry humor. Quotes "
            "p-values like scripture."
        ),
        "core_beliefs": [
            "Only Phase 3 RCT data with OS endpoints should drive treatment decisions",
            "Surrogate endpoints (ORR, PFS) are unreliable unless validated",
            "Standard of care exists for a reason — deviating requires extraordinary evidence",
            "Conference abstracts are NOT peer-reviewed evidence",
            "Hazard ratios and confidence intervals matter more than median survival numbers",
            "Subgroup analyses are hypothesis-generating, never practice-changing",
        ],
        "pet_peeves": [
            "Treatments rated highly based on Phase 1/2 data alone",
            "Missing confidence intervals or p-values",
            "Overstating preclinical results",
            "Cherry-picking favorable subgroup analyses",
            "Using ORR as a primary measure of benefit",
        ],
        "evaluation_focus": [
            "Are evidence levels accurately assigned?",
            "Do survival benefit scores match the actual OS/PFS data?",
            "Are hazard ratios, CIs, and p-values cited?",
            "Are Phase 2-only treatments rated too highly?",
            "Is SoC properly anchored as the comparison baseline?",
        ],
        "catchphrases": [
            "Show me the Phase 3 data.",
            "A p-value above 0.05 is a null result, not a 'trend toward significance.'",
            "ORR is not a patient-relevant endpoint.",
            "Where are the confidence intervals?",
            "An abstract at ASCO is not the same as a Lancet publication.",
        ],
        "blind_spots": [
            "May dismiss genuinely promising early-phase therapies",
            "Undervalues rare-disease settings where Phase 3 trials are infeasible",
            "Can be slow to adopt practice-changing results before full publication",
        ],
    },
    {
        "id": "aggressor",
        "name": "Dr. Aggressor",
        "title": "The Aggressive Interventionist — Surgical Oncologist",
        "institution": "Pacific Comprehensive Cancer Institute",
        "years_experience": 18,
        "philosophy": "Aggressive Interventionist",
        "personality": (
            "Bold, action-oriented, impatient with half-measures. Believes "
            "cancer must be hit hard, fast, and from every angle simultaneously. "
            "Champions multimodal therapy, dose-dense regimens, and adding every "
            "available active agent. Considers undertreatment a greater sin than "
            "overtreatment. Speaks with urgency. Competitive about outcomes."
        ),
        "core_beliefs": [
            "Maximum tolerable intensity gives the best chance of cure",
            "Combination therapy almost always beats monotherapy",
            "Dose-dense and dose-escalated regimens should be considered first",
            "Undertreatment kills more patients than overtreatment",
            "If a patient has ECOG 0-1, they can handle aggressive treatment",
            "Surgery should always be considered, even in borderline-resectable disease",
        ],
        "pet_peeves": [
            "De-escalation studies that sacrifice survival for comfort",
            "Reports that don't include enough combination strategies",
            "Conservative treatment recommendations for fit patients",
            "Supportive care given equal weight to active treatment",
            "Missing surgical or multimodal options",
        ],
        "evaluation_focus": [
            "Are the most aggressive evidence-based regimens included?",
            "Are combination strategies adequately explored?",
            "Is surgery considered where appropriate?",
            "Are dose-dense/intensified regimens mentioned?",
            "Does the report consider maximum therapeutic intensity for fit patients?",
        ],
        "catchphrases": [
            "You only get one shot at a cure. Make it count.",
            "What about adding a third agent?",
            "This patient is ECOG 0 — they can handle more.",
            "De-escalation is a luxury for the already-cured.",
            "Every combination not tried is a missed opportunity.",
        ],
        "blind_spots": [
            "May push toxicity beyond what patients can realistically tolerate",
            "Underestimates quality-of-life costs of aggressive treatment",
            "May not appreciate when less is genuinely more (HPV+ oropharyngeal)",
            "Can overlook that some patients value comfort over marginal survival gains",
        ],
    },
    {
        "id": "guardian",
        "name": "Dr. Guardian",
        "title": "The Patient-Centered Integrationist — Palliative & Integrative Oncologist",
        "institution": "Holistic Oncology & Survivorship Center",
        "years_experience": 15,
        "philosophy": "Patient-Centered Integrationist",
        "personality": (
            "Empathetic, holistic, pragmatic about trade-offs. Treats the "
            "patient, not just the tumor. Obsessed with toxicity profiles, "
            "functional outcomes, and what life looks like DURING treatment, "
            "not just after. Champions early palliative care integration, "
            "exercise programs, and nutritional support. Will push back hard "
            "against toxic regimens that offer marginal survival benefit. "
            "Warm but firm. Asks 'but at what cost?' constantly."
        ),
        "core_beliefs": [
            "Survival without quality of life is not success",
            "Early palliative care integration extends survival AND improves QoL",
            "Toxicity profiles should weigh equally with efficacy in treatment selection",
            "Supportive care is not optional — it is therapeutic",
            "Patient preferences and goals must drive treatment intensity decisions",
            "A month of life in the ICU is not the same as a month at home",
        ],
        "pet_peeves": [
            "Safety profile scores of 5/10 or below treated as acceptable without discussion",
            "Supportive care section being an afterthought with minimal depth",
            "Reports that never mention functional outcomes or performance status impact",
            "Ignoring that 45-year-olds have decades of survivorship ahead",
            "Treatment toxicities listed but never weighed against benefit magnitude",
        ],
        "evaluation_focus": [
            "Are safety profiles accurately scored and well-rationalized?",
            "Is supportive care covered with real evidence (not generic advice)?",
            "Are late effects and survivorship issues addressed?",
            "Does the report balance efficacy against toxicity honestly?",
            "Is early palliative care integration recommended?",
        ],
        "catchphrases": [
            "At what cost to the patient?",
            "Survival data without toxicity context is half the picture.",
            "This person is 45. They'll live with these side effects for decades.",
            "Palliative care is not giving up — it's evidence-based medicine.",
            "What does the patient actually want?",
        ],
        "blind_spots": [
            "May be too conservative when aggressive treatment offers real cure potential",
            "Can overweight QoL concerns in settings where survival is paramount",
            "May discourage patients from tolerable toxicity that offers major OS gains",
        ],
    },
    {
        "id": "precision",
        "name": "Dr. Precision",
        "title": "The Precision Medicine Advocate — Molecular Oncologist",
        "institution": "Center for Precision Cancer Therapeutics",
        "years_experience": 12,
        "philosophy": "Precision Medicine Advocate",
        "personality": (
            "Analytical, detail-obsessed, genomics-first. Believes every "
            "treatment decision should flow from the molecular profile. "
            "Considers 'one-size-fits-all' chemotherapy a relic. Pushes for "
            "comprehensive genomic profiling, liquid biopsies, and biomarker-"
            "matched therapies. Frustrated by reports that don't leverage "
            "available molecular data. Speaks in pathways and mutations. "
            "Wants to know the patient's TMB before anything else."
        ),
        "core_beliefs": [
            "Molecular profiling should precede and guide ALL treatment decisions",
            "Biomarker-matched therapy consistently outperforms empiric treatment",
            "Every tumor has actionable targets — we just haven't found them all yet",
            "Basket trials and tumor-agnostic approvals are the future of oncology",
            "Liquid biopsy should monitor treatment response and detect resistance early",
            "Resistance mechanisms should be anticipated and addressed proactively",
        ],
        "pet_peeves": [
            "Reports that don't match treatments to the patient's specific molecular markers",
            "Generic biomarker_requirements fields (empty or 'none')",
            "Not mentioning genomic profiling as a first step",
            "Ignoring actionable mutations present in the case",
            "Treating all patients with the same cancer type identically",
        ],
        "evaluation_focus": [
            "Are treatments matched to the patient's specific molecular markers?",
            "Are biomarker requirements accurately specified for each treatment?",
            "Are basket trials and tumor-agnostic options considered?",
            "Is resistance profiling or next-line biomarker-guided therapy discussed?",
            "Does the report leverage the molecular profile provided in the case?",
        ],
        "catchphrases": [
            "What does the molecular profile tell us?",
            "Have we ordered comprehensive genomic profiling?",
            "There's an actionable target here — why aren't we targeting it?",
            "Treating cancer by organ site alone is 20th-century medicine.",
            "What's the resistance mechanism, and what's our plan for it?",
        ],
        "blind_spots": [
            "May overvalue targeted therapy in settings where chemo/immuno is clearly superior",
            "Can recommend molecularly-matched agents with thin clinical evidence",
            "May undervalue proven SoC when it lacks a biomarker narrative",
            "Not all actionable mutations are clinically meaningful targets yet",
        ],
    },
    {
        "id": "frontier",
        "name": "Dr. Frontier",
        "title": "The Clinical Trialist / Innovator — Translational Research Oncologist",
        "institution": "Institute for Experimental Cancer Therapeutics",
        "years_experience": 14,
        "philosophy": "Clinical Trialist / Innovator",
        "personality": (
            "Visionary, forward-looking, restless with the status quo. Sees "
            "every patient as someone who might benefit from the next "
            "breakthrough. Deep knowledge of the drug development pipeline "
            "and early-phase trial landscape. Champions CAR-T, bispecifics, "
            "ADCs, mRNA vaccines, and radioligand therapy. Willing to take "
            "calculated risks on novel approaches when standard options are "
            "exhausted or mediocre. Speaks with infectious enthusiasm about "
            "emerging data. Maintains a mental database of every open trial."
        ),
        "core_beliefs": [
            "Clinical trials offer access to tomorrow's standard of care today",
            "Every patient should be screened for trial eligibility",
            "Novel modalities (ADCs, bispecifics, cell therapy) are transforming oncology",
            "Early-phase trials can be appropriate even with other options available",
            "The pace of oncology innovation means 2-year-old data may already be outdated",
            "Compassionate use and expanded access should be explored when trials aren't available",
        ],
        "pet_peeves": [
            "Reports that only include FDA-approved treatments",
            "Empty or minimal clinical trials section",
            "Not mentioning novel modalities (ADCs, bispecifics, cancer vaccines)",
            "Dismissing Phase 1/2 data when the biology is compelling",
            "Failing to include NCT numbers or actionable trial information",
        ],
        "evaluation_focus": [
            "Are clinical trial opportunities adequately covered?",
            "Are novel modalities (ADC, bispecific, cell therapy, vaccine) represented?",
            "Does the emerging pipeline section have real, specific data?",
            "Are trial access pathways clearly described?",
            "Is the report capturing the latest data (2025-2026)?",
        ],
        "catchphrases": [
            "Is there a trial for this?",
            "The standard of care is not the ceiling — it's the floor.",
            "This ADC data is remarkable. Have we considered enrollment?",
            "By the time this is Phase 3, it might be too late for this patient.",
            "What about compassionate use?",
        ],
        "blind_spots": [
            "May overstate the promise of early-phase agents",
            "Can undervalue proven standard of care in favor of exciting but unproven options",
            "Access to cutting-edge trials is geographically and socioeconomically limited",
            "Novelty bias — newer is not always better",
        ],
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# DEBATE STRUCTURE
# ══════════════════════════════════════════════════════════════════════════════

DEBATE_ROUNDS = [
    {
        "round": 1,
        "name": "Initial Review",
        "instruction": (
            "Each doctor independently reviews the report and provides their "
            "assessment. Focus on your area of expertise. Identify the report's "
            "strengths and weaknesses through YOUR philosophical lens. "
            "Score the report 0-100 from your perspective."
        ),
    },
    {
        "round": 2,
        "name": "Cross-Examination",
        "instruction": (
            "Each doctor reads the other four doctors' initial reviews and "
            "challenges their positions. Directly address specific claims made "
            "by your colleagues that you disagree with. Name names. Be specific. "
            "This is a professional argument — be direct but not personal."
        ),
    },
    {
        "round": 3,
        "name": "Rebuttal & Defense",
        "instruction": (
            "Each doctor responds to the challenges directed at them. Defend "
            "your position with evidence, concede where appropriate, and "
            "identify where the argument has changed your view. Update your "
            "score if the debate has shifted your assessment."
        ),
    },
    {
        "round": 4,
        "name": "Consensus & Dissent",
        "instruction": (
            "The board attempts to reach consensus on: (1) What this report "
            "gets RIGHT, (2) What this report gets WRONG, (3) What is MISSING. "
            "Where consensus is impossible, document the dissent with each "
            "doctor's position and reasoning. Produce a final board score "
            "and actionable recommendations for improving the report."
        ),
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# REPORT ANALYSIS HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def extract_report_summary(data: dict) -> dict:
    """Extract key facts from report for debate context."""
    meta = data.get("report_metadata", {})
    treatments = data.get("treatments", [])
    trials = data.get("clinical_trials", [])
    combos = data.get("combination_strategies", [])
    supportive = data.get("supportive_care", [])
    sources = data.get("sources", [])

    treatment_summaries = []
    for t in treatments:
        rb = t.get("rating_breakdown", {})
        treatment_summaries.append({
            "rank": t.get("rank"),
            "name": t.get("name"),
            "category": t.get("category"),
            "composite_rating": t.get("composite_rating"),
            "evidence_score": rb.get("evidence_level", {}).get("score"),
            "survival_score": rb.get("survival_benefit", {}).get("score"),
            "safety_score": rb.get("safety_profile", {}).get("score"),
            "biomarker_score": rb.get("biomarker_match", {}).get("score"),
            "accessibility_score": rb.get("accessibility", {}).get("score"),
            "mechanism": t.get("mechanism_of_action", ""),
            "key_study": t.get("key_evidence", {}).get("study_name", ""),
            "os_data": t.get("key_evidence", {}).get("os_months", {}),
            "biomarker_reqs": t.get("biomarker_requirements", []),
            "side_effects": t.get("notable_side_effects", []),
            "availability": t.get("availability", ""),
        })

    return {
        "cancer_type": meta.get("cancer_type", "Unknown"),
        "stage": meta.get("stage", "Unknown"),
        "molecular_profile": meta.get("molecular_profile", []),
        "n_treatments": len(treatments),
        "n_trials": len(trials),
        "n_combos": len(combos),
        "n_supportive": len(supportive),
        "n_sources": len(sources),
        "treatments": treatment_summaries,
        "trial_ids": [tr.get("trial_id", "") for tr in trials],
        "combo_pairs": [(c.get("base_therapy", ""), c.get("combination_partner", "")) for c in combos],
        "supportive_approaches": [s.get("approach", "") for s in supportive],
    }


def format_case_context(case: dict) -> str:
    """Format benchmark case for the debate prompt."""
    if not case:
        return "No patient case context provided."

    ctx = case.get("patient_context", {})
    markers = ", ".join(case.get("molecular_markers", []))
    risks = ", ".join(ctx.get("risk_factors", [])) or "none reported"
    comorbidities = ", ".join(ctx.get("comorbidities", [])) or "none"

    return (
        f"**Patient**: {ctx.get('age', '?')} y.o. {ctx.get('sex', '?')}, "
        f"ECOG {ctx.get('performance_status', '?')}\n"
        f"**Diagnosis**: {case.get('cancer_type', '?')}\n"
        f"**Stage**: {case.get('stage', '?')}\n"
        f"**Molecular markers**: {markers}\n"
        f"**Risk factors**: {risks}\n"
        f"**Comorbidities**: {comorbidities}\n"
    )


# ══════════════════════════════════════════════════════════════════════════════
# PROMPT GENERATION
# ══════════════════════════════════════════════════════════════════════════════

def generate_doctor_prompt(doctor: dict) -> str:
    """Generate the persona prompt for a single doctor."""
    beliefs = "\n".join(f"  - {b}" for b in doctor["core_beliefs"])
    peeves = "\n".join(f"  - {p}" for p in doctor["pet_peeves"])
    focus = "\n".join(f"  - {f}" for f in doctor["evaluation_focus"])
    phrases = "\n".join(f'  - "{c}"' for c in doctor["catchphrases"])
    spots = "\n".join(f"  - {s}" for s in doctor["blind_spots"])

    return f"""### {doctor['name']}
**{doctor['title']}** | {doctor['institution']} | {doctor['years_experience']} years
**Philosophy**: {doctor['philosophy']}

**Personality**: {doctor['personality']}

**Core Beliefs**:
{beliefs}

**Pet Peeves** (things that trigger strong reactions):
{peeves}

**Evaluation Focus** (what this doctor scrutinizes):
{focus}

**Typical Phrases**:
{phrases}

**Known Blind Spots** (other doctors will exploit these):
{spots}
"""


def generate_debate_prompt(report_data: dict, case: dict = None) -> str:
    """Generate the full multi-round debate prompt."""
    summary = extract_report_summary(report_data)

    # Build treatments table for the prompt
    treatments_table = "| Rank | Treatment | Category | Rating | Evidence | Safety |\n"
    treatments_table += "|------|-----------|----------|--------|----------|--------|\n"
    for t in summary["treatments"]:
        treatments_table += (
            f"| {t['rank']} | {t['name'][:40]} | {t['category'][:20]} | "
            f"{t['composite_rating']} | {t['evidence_score']}/10 | "
            f"{t['safety_score']}/10 |\n"
        )

    # Doctor personas
    doctor_sections = "\n---\n".join(generate_doctor_prompt(d) for d in DOCTORS)

    # Debate round instructions
    rounds_text = ""
    for r in DEBATE_ROUNDS:
        rounds_text += f"\n### Round {r['round']}: {r['name']}\n{r['instruction']}\n"

    # Case context
    case_text = format_case_context(case) if case else "No specific patient case provided."

    prompt = f"""# Virtual Tumor Board — Adversarial Report Review

## Instructions

You are simulating a tumor board meeting with 5 oncologists who have radically
different treatment philosophies. They will review a cancer research report,
argue with each other across 4 rounds, and produce consensus findings.

**CRITICAL**: Each doctor must stay in character. Their philosophical biases
should drive DIFFERENT assessments of the same data. Real disagreements should
emerge — this is not a consensus-building exercise until Round 4.

When writing each doctor's contribution, use first person. Include their
characteristic phrases naturally. Reference specific treatments from the report
by name and rating. Challenge other doctors BY NAME.

---

## Patient Case Context

{case_text}

## Report Under Review

**Cancer**: {summary['cancer_type']}
**Stage**: {summary['stage']}
**Molecular Profile**: {', '.join(summary['molecular_profile']) if summary['molecular_profile'] else 'Not specified'}

**Report Statistics**:
- Treatments analyzed: {summary['n_treatments']}
- Clinical trials listed: {summary['n_trials']}
- Combination strategies: {summary['n_combos']}
- Supportive care approaches: {summary['n_supportive']}
- Sources cited: {summary['n_sources']}

**Treatment Rankings**:
{treatments_table}

**Clinical Trial IDs**: {', '.join(summary['trial_ids']) if summary['trial_ids'] else 'None listed'}
**Combination Pairs**: {'; '.join(f'{a} + {b}' for a, b in summary['combo_pairs']) if summary['combo_pairs'] else 'None listed'}
**Supportive Approaches**: {', '.join(summary['supportive_approaches']) if summary['supportive_approaches'] else 'None listed'}

---

## The Doctors

{doctor_sections}

---

## Debate Format
{rounds_text}

---

## Output Structure

For each round, write each doctor's contribution under their name.
After Round 4, produce:

### Final Board Assessment

```json
{{
  "board_score": <0-100 consensus score>,
  "individual_scores": {{
    "evidence": <0-100>,
    "aggressor": <0-100>,
    "guardian": <0-100>,
    "precision": <0-100>,
    "frontier": <0-100>
  }},
  "consensus_strengths": ["..."],
  "consensus_weaknesses": ["..."],
  "consensus_missing": ["..."],
  "dissenting_opinions": [
    {{"doctor": "...", "position": "...", "reasoning": "..."}}
  ],
  "actionable_recommendations": [
    {{"priority": "high|medium|low", "recommendation": "...", "championed_by": "..."}}
  ]
}}
```

Begin the tumor board meeting now.
"""
    return prompt


# ══════════════════════════════════════════════════════════════════════════════
# QUICK-REVIEW MODE (single-pass, no multi-round debate)
# ══════════════════════════════════════════════════════════════════════════════

def generate_quick_review_prompt(report_data: dict, case: dict = None) -> str:
    """Generate a shorter single-round review prompt (faster, lower cost)."""
    summary = extract_report_summary(report_data)
    case_text = format_case_context(case) if case else "No patient case."

    treatments_list = ""
    for t in summary["treatments"]:
        treatments_list += (
            f"- [{t['rank']}] {t['name']} ({t['category']}) — "
            f"Rating: {t['composite_rating']}, Evidence: {t['evidence_score']}/10, "
            f"Safety: {t['safety_score']}/10\n"
        )

    doctor_briefs = ""
    for d in DOCTORS:
        doctor_briefs += (
            f"\n**{d['name']}** ({d['philosophy']}): "
            f"Focus on {'; '.join(d['evaluation_focus'][:2])}. "
            f'Typical reaction: "{d["catchphrases"][0]}"\n'
        )

    return f"""# Quick Tumor Board Review

Five oncologists each give a 2-3 paragraph review of this report, then
one paragraph of direct disagreement with the colleague they most oppose.

## Case
{case_text}

## Report: {summary['cancer_type']} — {summary['stage']}
{treatments_list}
Trials: {summary['n_trials']} | Combos: {summary['n_combos']} | Supportive: {summary['n_supportive']} | Sources: {summary['n_sources']}

## Doctors
{doctor_briefs}

For each doctor: (1) Score 0-100, (2) 2-3 paragraph review in character,
(3) One direct challenge to another doctor by name.

End with a JSON block:
```json
{{"board_score": <average>, "recommendations": ["..."]}}
```
"""


# ══════════════════════════════════════════════════════════════════════════════
# DOCTOR-SPECIFIC SCORING (offline, no LLM needed)
# ══════════════════════════════════════════════════════════════════════════════

def score_as_doctor(doctor: dict, report_data: dict) -> dict:
    """
    Heuristic scoring from each doctor's perspective.
    Returns a score and list of complaints/praises.
    This runs WITHOUT an LLM — pure rule-based evaluation.
    """
    score = 50  # baseline
    notes = []
    treatments = report_data.get("treatments", [])
    trials = report_data.get("clinical_trials", [])
    combos = report_data.get("combination_strategies", [])
    supportive = report_data.get("supportive_care", [])
    sources = report_data.get("sources", [])

    doc_id = doctor["id"]

    if doc_id == "evidence":
        # Evidence Purist — cares about Phase 3, OS data, p-values
        phase3_count = 0
        os_data_count = 0
        has_hr = 0
        for t in treatments:
            ev = t.get("key_evidence", {})
            cat = (t.get("category", "") or "").lower()
            avail = (t.get("availability", "") or "").lower()
            if "phase 3" in cat or "phase 3" in avail or "standard" in cat:
                phase3_count += 1
            os_data = ev.get("os_months", {})
            if isinstance(os_data, dict) and os_data.get("treatment"):
                os_data_count += 1
                if os_data.get("hazard_ratio") and os_data.get("p_value"):
                    has_hr += 1

        if phase3_count >= 3:
            score += 15
            notes.append(f"+15: {phase3_count} Phase 3-backed treatments — solid evidence base")
        elif phase3_count >= 1:
            score += 5
            notes.append(f"+5: Only {phase3_count} Phase 3-backed treatments — insufficient")
        else:
            score -= 15
            notes.append("-15: NO Phase 3-backed treatments — unacceptable")

        if os_data_count >= len(treatments) * 0.6:
            score += 10
            notes.append(f"+10: {os_data_count}/{len(treatments)} treatments have OS data")
        else:
            score -= 10
            notes.append(f"-10: Only {os_data_count}/{len(treatments)} have OS data — where's the survival evidence?")

        if has_hr >= 2:
            score += 10
            notes.append(f"+10: {has_hr} treatments report hazard ratios — proper statistical reporting")
        else:
            score -= 5
            notes.append(f"-5: Only {has_hr} treatments report HRs — show me the statistics")

        # Penalize highly-rated treatments with low evidence
        for t in treatments[:3]:  # top 3
            ev_score = t.get("rating_breakdown", {}).get("evidence_level", {}).get("score", 0)
            if ev_score < 7 and t.get("composite_rating", 0) > 7:
                score -= 10
                notes.append(f"-10: '{t['name']}' rated {t['composite_rating']} with evidence score only {ev_score} — inflated")

    elif doc_id == "aggressor":
        # Aggressive Interventionist — wants combos, intensity, surgery
        if len(combos) >= 4:
            score += 15
            notes.append(f"+15: {len(combos)} combination strategies — good therapeutic intensity")
        elif len(combos) >= 2:
            score += 5
            notes.append(f"+5: Only {len(combos)} combos — we need more attack vectors")
        else:
            score -= 15
            notes.append(f"-15: {len(combos)} combos — where's the combination strategy?")

        if len(treatments) >= 10:
            score += 10
            notes.append(f"+10: {len(treatments)} treatments — comprehensive arsenal")
        elif len(treatments) < 5:
            score -= 10
            notes.append(f"-10: Only {len(treatments)} treatments — too conservative")

        # Check for surgical options
        has_surgery = any("surg" in (t.get("name", "") + t.get("mechanism_of_action", "")).lower()
                         for t in treatments)
        if has_surgery:
            score += 5
            notes.append("+5: Surgical options included")
        else:
            score -= 5
            notes.append("-5: No surgical options discussed — always consider the knife")

        # High-intensity regimens
        high_rated = sum(1 for t in treatments if t.get("composite_rating", 0) >= 7)
        if high_rated >= 3:
            score += 10
            notes.append(f"+10: {high_rated} high-rated treatments (>=7) — strong options available")

    elif doc_id == "guardian":
        # Patient-Centered — toxicity, supportive care, QoL
        if len(supportive) >= 4:
            score += 15
            notes.append(f"+15: {len(supportive)} supportive care approaches — excellent holistic coverage")
        elif len(supportive) >= 2:
            score += 5
            notes.append(f"+5: {len(supportive)} supportive care — needs more")
        else:
            score -= 15
            notes.append(f"-15: Only {len(supportive)} supportive care — the patient is more than a tumor")

        # Safety documentation
        treatments_with_sides = sum(
            1 for t in treatments
            if t.get("notable_side_effects") and len(t["notable_side_effects"]) >= 2
        )
        if treatments_with_sides >= len(treatments) * 0.8:
            score += 10
            notes.append(f"+10: {treatments_with_sides}/{len(treatments)} have detailed side effects")
        elif treatments_with_sides < len(treatments) * 0.4:
            score -= 10
            notes.append(f"-10: Only {treatments_with_sides}/{len(treatments)} document side effects — dangerous omission")

        # Safety scores — flag any very low safety without discussion
        unsafe_count = sum(1 for t in treatments
                          if t.get("rating_breakdown", {}).get("safety_profile", {}).get("score", 10) <= 4)
        if unsafe_count > 0:
            notes.append(f"Warning: {unsafe_count} treatments with safety <=4/10 — need careful patient counseling discussion")

        # Palliative care mention
        has_palliative = any("palliative" in (s.get("approach", "") or "").lower() for s in supportive)
        if has_palliative:
            score += 10
            notes.append("+10: Early palliative care integration included — evidence-based and patient-centered")
        else:
            score -= 5
            notes.append("-5: No palliative care integration — this is a missed opportunity")

    elif doc_id == "precision":
        # Precision Medicine — biomarkers, molecular matching, genomics
        treatments_with_markers = sum(
            1 for t in treatments
            if t.get("biomarker_requirements") and len(t["biomarker_requirements"]) > 0
        )
        if treatments_with_markers >= len(treatments) * 0.5:
            score += 15
            notes.append(f"+15: {treatments_with_markers}/{len(treatments)} specify biomarker requirements — precision approach")
        elif treatments_with_markers >= len(treatments) * 0.25:
            score += 5
            notes.append(f"+5: {treatments_with_markers}/{len(treatments)} specify biomarkers — needs more molecular detail")
        else:
            score -= 10
            notes.append(f"-10: Only {treatments_with_markers}/{len(treatments)} specify biomarkers — treating by site not by biology")

        # Targeted therapies present
        targeted_count = sum(1 for t in treatments
                           if "targeted" in (t.get("category", "") or "").lower())
        if targeted_count >= 2:
            score += 10
            notes.append(f"+10: {targeted_count} targeted therapies — molecularly informed")
        else:
            notes.append(f"+0: Only {targeted_count} targeted therapies — are we ignoring the molecular profile?")

        # Biomarker match scores
        avg_bio = 0
        bio_scores = [t.get("rating_breakdown", {}).get("biomarker_match", {}).get("score", 0)
                      for t in treatments]
        if bio_scores:
            avg_bio = sum(bio_scores) / len(bio_scores)
            if avg_bio >= 7:
                score += 10
                notes.append(f"+10: Average biomarker match score {avg_bio:.1f} — well-matched to patient")
            elif avg_bio < 5:
                score -= 5
                notes.append(f"-5: Average biomarker match {avg_bio:.1f} — poor molecular matching")

    elif doc_id == "frontier":
        # Innovator — trials, novel modalities, pipeline
        if len(trials) >= 5:
            score += 15
            notes.append(f"+15: {len(trials)} clinical trials listed — excellent access opportunities")
        elif len(trials) >= 2:
            score += 5
            notes.append(f"+5: {len(trials)} trials — there must be more options out there")
        else:
            score -= 10
            notes.append(f"-10: Only {len(trials)} trials — have we even checked ClinicalTrials.gov?")

        # NCT numbers
        trials_with_nct = sum(1 for tr in trials if tr.get("trial_id", "").startswith("NCT"))
        if trials_with_nct >= 3:
            score += 10
            notes.append(f"+10: {trials_with_nct} trials with NCT numbers — actionable for patients")
        elif trials_with_nct > 0:
            score += 3
            notes.append(f"+3: Only {trials_with_nct} NCT numbers — patients need more to act on")
        else:
            score -= 5
            notes.append("-5: No NCT numbers — how do patients find these trials?")

        # Novel modality keywords
        novel_keywords = ["adc", "antibody drug conjugate", "bispecific", "car-t",
                         "car t", "mrna", "vaccine", "radioligand", "oncolytic"]
        novel_found = set()
        for t in treatments:
            name_mech = ((t.get("name", "") or "") + " " + (t.get("mechanism_of_action", "") or "")).lower()
            for kw in novel_keywords:
                if kw in name_mech:
                    novel_found.add(kw)
        if len(novel_found) >= 2:
            score += 10
            notes.append(f"+10: Novel modalities found: {', '.join(novel_found)} — cutting-edge coverage")
        elif len(novel_found) >= 1:
            score += 5
            notes.append(f"+5: Some novel modalities: {', '.join(novel_found)}")
        else:
            score -= 10
            notes.append("-10: No novel modalities (ADC, bispecific, CAR-T, vaccine) — are we stuck in 2015?")

        # Recent data (check for 2025/2026 in sources)
        recent_sources = sum(1 for s in sources if "2025" in str(s) or "2026" in str(s))
        if recent_sources >= 3:
            score += 5
            notes.append(f"+5: {recent_sources} sources from 2025-2026 — current landscape")

    # Clamp
    score = max(0, min(100, score))

    return {
        "doctor_id": doc_id,
        "doctor_name": doctor["name"],
        "philosophy": doctor["philosophy"],
        "score": score,
        "notes": notes,
    }


def run_heuristic_board(report_data: dict) -> dict:
    """Run all 5 doctors' heuristic scoring (no LLM needed)."""
    results = []
    for doctor in DOCTORS:
        result = score_as_doctor(doctor, report_data)
        results.append(result)

    scores = [r["score"] for r in results]
    board_score = round(sum(scores) / len(scores), 1)

    # Identify biggest disagreements
    max_doc = max(results, key=lambda x: x["score"])
    min_doc = min(results, key=lambda x: x["score"])
    spread = max_doc["score"] - min_doc["score"]

    return {
        "board_score": board_score,
        "spread": spread,
        "individual_results": results,
        "most_favorable": {"doctor": max_doc["doctor_name"], "score": max_doc["score"]},
        "most_critical": {"doctor": min_doc["doctor_name"], "score": min_doc["score"]},
        "evaluated_at": datetime.now().isoformat(),
    }


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def print_board_results(board: dict):
    """Print heuristic board results."""
    print(f"\n{'='*70}")
    print(f"  VIRTUAL TUMOR BOARD — HEURISTIC REVIEW")
    print(f"{'='*70}")
    print(f"  Board Score: {board['board_score']}/100 (spread: {board['spread']} pts)")
    print(f"  Most Favorable: {board['most_favorable']['doctor']} ({board['most_favorable']['score']})")
    print(f"  Most Critical:  {board['most_critical']['doctor']} ({board['most_critical']['score']})")
    print(f"{'='*70}\n")

    for r in board["individual_results"]:
        print(f"  {r['doctor_name']} ({r['philosophy']})")
        print(f"  Score: {r['score']}/100")
        for note in r["notes"]:
            print(f"    {note}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Virtual Tumor Board — 5 doctors debate a cancer research report"
    )
    parser.add_argument("input", help="Input JSON report file")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", choices=["json", "markdown", "prompt"],
                        default="json", help="Output format (default: json)")
    parser.add_argument("--generate-prompt", action="store_true",
                        help="Generate the LLM debate prompt (print to stdout)")
    parser.add_argument("--quick-prompt", action="store_true",
                        help="Generate a shorter single-round review prompt")
    parser.add_argument("--case", help="Benchmark case JSON file (for patient context)")
    parser.add_argument("--case-id", help="Specific case ID from benchmark file")
    parser.add_argument("--heuristic", action="store_true",
                        help="Run rule-based scoring only (no LLM needed)")
    args = parser.parse_args()

    # Load report
    with open(args.input, "r", encoding="utf-8") as f:
        report_data = json.load(f)

    # Load case context if provided
    case = None
    if args.case:
        with open(args.case, "r", encoding="utf-8") as f:
            case_data = json.load(f)
        cases = case_data.get("cases", [])
        if args.case_id:
            case = next((c for c in cases if c["id"] == args.case_id), None)
        elif cases:
            case = cases[0]

    # Generate prompt mode
    if args.generate_prompt:
        print(generate_debate_prompt(report_data, case))
        return

    if args.quick_prompt:
        print(generate_quick_review_prompt(report_data, case))
        return

    # Heuristic mode (default)
    board = run_heuristic_board(report_data)
    print_board_results(board)

    # Save output
    if args.output:
        if args.format == "json":
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(board, f, indent=2, ensure_ascii=False)
            print(f"  Saved to: {args.output}")
        elif args.format == "markdown":
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(f"# Virtual Tumor Board Results\n\n")
                f.write(f"**Board Score**: {board['board_score']}/100\n")
                f.write(f"**Spread**: {board['spread']} points\n\n")
                for r in board["individual_results"]:
                    f.write(f"## {r['doctor_name']} — {r['philosophy']}\n")
                    f.write(f"**Score**: {r['score']}/100\n\n")
                    for note in r["notes"]:
                        f.write(f"- {note}\n")
                    f.write("\n")
            print(f"  Saved to: {args.output}")
        elif args.format == "prompt":
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(generate_debate_prompt(report_data, case))
            print(f"  Debate prompt saved to: {args.output}")


if __name__ == "__main__":
    main()
