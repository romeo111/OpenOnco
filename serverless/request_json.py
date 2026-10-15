"""Bound HTTP JSON nesting and reject ambiguous duplicate object keys."""
import json

MAX_JSON_NESTING = 256


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            # Do not echo a potentially identifying key or clinical value.
            raise ValueError('Duplicate JSON object key')
        result[key] = value
    return result


def decode_request_json(raw: str):
    depth = 0
    quoted = False
    escaped = False
    for character in raw:
        if quoted:
            if escaped:
                escaped = False
            elif character == '\\':
                escaped = True
            elif character == '"':
                quoted = False
        elif character == '"':
            quoted = True
        elif character in '[{':
            depth += 1
            if depth > MAX_JSON_NESTING:
                raise ValueError('JSON nesting exceeds request limit')
        elif character in ']}':
            depth -= 1
    return json.loads(raw, object_pairs_hook=_unique_object)
