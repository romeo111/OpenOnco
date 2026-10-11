"""Explicitly synthetic reviewer authority, used only in temporary test contexts."""


def authorized_profiles(*reviewer_ids, disease_id="DIS-CRC", verified_on="2026-08-03"):
    return {
        reviewer_id: {
            "id": reviewer_id, "name": {"preferred": "Synthetic reviewer " + reviewer_id},
            "specialty": "Synthetic test only", "qualifications": ["Synthetic credential"],
            "last_active": verified_on,
            "sign_off_scope": {"entity_types": ["BiomarkerActionability", "Indication"],
                               "diseases_explicit": [disease_id]},
            "authorization": {"status": "approved", "verified_on": verified_on,
                              "identity_key": "synthetic-person-" + reviewer_id,
                              "decision_reference": "https://example.org/synthetic-review-decision"},
        }
        for reviewer_id in reviewer_ids
    }
