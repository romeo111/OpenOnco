"""Optional content review records for the solo-maintainer workflow.

Publication has no reviewer quota. A current eligible review is enough to
record that a content review exists; it does not validate the tool or approve
an individual treatment. Identity, scope, revision and independence checks
remain in schemas._review_readiness. Raw counters confer no authority.
"""
MIN_ELIGIBLE_CONTENT_REVIEWS = 1
