"""Smoke tests for biomarker-aware track filtering in generate_plan().

The filter is lenient: tracks are dropped only when the patient profile
EXPLICITLY violates an Indication's `biomarker_requirements_excluded`
list. Missing biomarker data does NOT drop tracks. See
`knowledge_base/engine/_track_filter.py` for rationale.

We exercise the filter on the mCRC 2L algorithm because it has multiple
output_indications with `BIO-MSI-STATUS: MSI-H` on their exclusion list
(KRAS-G12C-sotorasib, FOLFIRI-bev, HER2-amp-tucatinib, …) plus
indications that have no exclusions (MSI-H-pembro, BRAF-BEACON).
"""

from __future__ import annotations

from pathlib import Path

from knowledge_base.engine import generate_plan
from knowledge_base.engine._track_filter import is_track_excluded


REPO_ROOT = Path(__file__).parent.parent
KB_ROOT = REPO_ROOT / "knowledge_base" / "hosted" / "content"


# ── unit-level checks for the helper ──────────────────────────────────


def test_helper_no_exclusions_returns_false():
    ind = {"applicable_to": {"biomarker_requirements_excluded": []}}
    assert is_track_excluded(ind, {"BRAF": "V600E"}) is False


def test_helper_missing_patient_biomarker_is_lenient():
    ind = {
        "applicable_to": {
            "biomarker_requirements_excluded": [
                {"biomarker_id": "BIO-MSI-STATUS", "value_constraint": "MSI-H"},
            ]
        }
    }
    # Patient has no MSI data at all → must NOT drop the track.
    assert is_track_excluded(ind, {"BRAF": "V600E"}) is False
    assert is_track_excluded(ind, {}) is False


def test_helper_explicit_match_drops():
    ind = {
        "applicable_to": {
            "biomarker_requirements_excluded": [
                {"biomarker_id": "BIO-MSI-STATUS", "value_constraint": "MSI-H"},
            ]
        }
    }
    # Patient explicitly MSI-H → drop this track.
    assert is_track_excluded(ind, {"MSI-STATUS": "MSI-H"}) is True
    assert is_track_excluded(ind, {"BIO-MSI-STATUS": "MSI-H"}) is True
    assert is_track_excluded(ind, {"MSI": "MSI-High"}) is True


def test_helper_negative_value_does_not_drop():
    ind = {
        "applicable_to": {
            "biomarker_requirements_excluded": [
                {"biomarker_id": "BIO-MSI-STATUS", "value_constraint": "MSI-H"},
            ]
        }
    }
    # Patient explicitly negative / wildtype → do NOT drop.
    assert is_track_excluded(ind, {"MSI": "negative"}) is False
    assert is_track_excluded(ind, {"MSI-STATUS": "MSS"}) is False


def test_helper_gene_level_positive_does_not_satisfy_qualifier():
    """Patient reports gene-level positive (e.g. 'positive', True) but the
    exclusion is qualified by a specific value_constraint. The patient has
    NOT reported the qualifying condition, so the track must not be dropped.

    Regression for the S1 NSCLC T790M case (PR #150 KB-drift signal #1):
    IND-NSCLC-2L-EGFR-POST-OSI-AMI-LAZ excludes 'histologic transformation'
    on BIO-EGFR-MUTATION. Patient with BIO-EGFR-MUTATION='positive' has not
    reported transformation status — track must remain available.
    """
    ind = {
        "applicable_to": {
            "biomarker_requirements_excluded": [
                {
                    "biomarker_id": "BIO-EGFR-MUTATION",
                    "value_constraint": "histologic transformation",
                },
            ]
        }
    }
    assert is_track_excluded(ind, {"BIO-EGFR-MUTATION": "positive"}) is False
    assert is_track_excluded(ind, {"EGFR": "positive"}) is False
    assert is_track_excluded(ind, {"BIO-EGFR-MUTATION": True}) is False


def test_helper_gene_level_positive_still_drops_unqualified_exclusion():
    """Counter-case: when the exclusion has NO value_constraint (gene-level
    only), gene-level positive in the patient should still drop the track.
    Confirms the fix only affects qualified exclusions."""
    ind = {
        "applicable_to": {
            "biomarker_requirements_excluded": [
                {"biomarker_id": "BIO-MSI-STATUS"},
            ]
        }
    }
    assert is_track_excluded(ind, {"MSI-STATUS": "positive"}) is True
    assert is_track_excluded(ind, {"MSI": True}) is True


def test_helper_handles_none_and_non_dict():
    assert is_track_excluded(None, {"X": "Y"}) is False
    assert is_track_excluded({}, {"X": "Y"}) is False
    assert is_track_excluded({"applicable_to": None}, {"X": "Y"}) is False


# ── end-to-end smoke through generate_plan ────────────────────────────


def test_track_kept_when_biomarker_unknown():
    """Patient without biomarker data should retain all algorithm tracks
    (lenient mode: missing data is not an exclusion match)."""
    patient = {
        "patient_id": "TEST-CRC-LENIENT",
        "disease": {"id": "DIS-CRC"},
        "line_of_therapy": 2,
        "biomarkers": {},  # nothing tested
    }

    result = generate_plan(patient, kb_root=KB_ROOT)
    assert result.plan is not None, f"plan should generate; warnings={result.warnings}"

    # No filter warnings should appear when the patient has no biomarker data.
    filter_warnings = [
        w for w in result.warnings if "biomarker_requirements_excluded" in w
    ]
    assert filter_warnings == [], (
        f"lenient mode must not drop tracks for empty biomarkers: {filter_warnings}"
    )

    # mCRC 2L algorithm has 10 output_indications — all should survive.
    assert len(result.plan.tracks) >= 5, (
        f"expected ≥5 tracks for mCRC 2L without biomarkers; got {len(result.plan.tracks)}"
    )


def test_msi_h_patient_drops_msi_excluded_tracks():
    """Patient with MSI-H should NOT see tracks that explicitly exclude
    MSI-H (e.g. KRAS-G12C-sotorasib, FOLFIRI-bev). They should still see
    the MSI-H-pembro track (no exclusions) and BRAF-BEACON (no exclusions)."""
    patient = {
        "patient_id": "TEST-CRC-MSI-H",
        "disease": {"id": "DIS-CRC"},
        "line_of_therapy": 2,
        "biomarkers": {"MSI-STATUS": "MSI-H"},
    }

    result = generate_plan(patient, kb_root=KB_ROOT)
    assert result.plan is not None, f"plan should generate; warnings={result.warnings}"

    track_ids = {t.indication_id for t in result.plan.tracks}

    # Tracks that explicitly exclude MSI-H must be dropped:
    msi_excluded_tracks = {
        "IND-CRC-METASTATIC-2L-KRAS-G12C-SOTORASIB-CETUXIMAB",
        "IND-CRC-METASTATIC-2L-FOLFIRI-BEV",
        "IND-CRC-METASTATIC-2L-HER2-AMP-TUCATINIB",
        "IND-CRC-METASTATIC-2L-HER2-AMP-T-DXD",
        "IND-CRC-METASTATIC-2L-EGFRI-RECHALLENGE",
    }
    leaked = track_ids & msi_excluded_tracks
    assert not leaked, (
        f"MSI-H patient should not see MSI-H-excluded tracks; leaked={leaked}"
    )

    # MSI-H-pembro has no exclusions and must remain available
    assert "IND-CRC-METASTATIC-2L-MSI-H-PEMBRO" in track_ids, (
        f"MSI-H-pembro must remain; got {track_ids}"
    )

    # Filter should have produced explicit warnings for dropped tracks
    filter_warnings = [
        w for w in result.warnings if "biomarker_requirements_excluded" in w
    ]
    assert filter_warnings, (
        "expected filter warnings logging the dropped tracks"
    )
