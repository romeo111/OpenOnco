"""Content withdrawal is independent of patient eligibility and clinical approval."""


def planning_block_reason(indication, regimen=None):
    for record in (indication, regimen):
        if not isinstance(record, dict):
            continue
        if record.get('planning_status', 'active') != 'active':
            reason = record.get('planning_status_reason')
            return str(reason) if isinstance(reason, str) and reason.strip() else 'Record withheld from planning pending source review.'
    return None
