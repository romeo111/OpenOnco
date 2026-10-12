"""Bound HTTP JSON nesting before decoding, independently of Python's limits."""
import json

MAX_JSON_NESTING = 256


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
    return json.loads(raw)
