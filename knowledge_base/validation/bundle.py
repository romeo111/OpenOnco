"""Validate an intentionally partial package without hiding broken references."""
from dataclasses import replace
import json
from pathlib import Path

from knowledge_base.schemas import ENTITY_BY_DIR
from knowledge_base.validation.loader import load_content


def load_packaged_content(root: Path, *, active_disease=None, core_only=False):
    """Defer only exact, typed IDs listed in the hash-verified bundle manifest.

    Core startup may defer all known disease modules. Before a treatment plan
    or module is accepted, references belonging to the active disease must
    resolve. Source references, schema errors and contracts always block.
    The full-KB loader and its cached result remain unchanged.
    """
    root = Path(root)
    loaded = load_content(root)
    path = root / '_bundle_manifest.json'
    if not path.is_file():
        return loaded
    try:
        deferred = json.loads(path.read_text(encoding='utf-8'))['deferred_entities']
        if not isinstance(deferred, dict) or not all(
            isinstance(eid, str) and isinstance(meta, dict)
            and isinstance(meta.get('disease_id'), str)
            and meta['disease_id'].startswith('DIS-')
            and meta.get('type') in ENTITY_BY_DIR
            for eid, meta in deferred.items()
        ):
            raise ValueError('invalid deferred entity map')
        if core_only and active_disease is not None:
            raise ValueError('core validation cannot validate an active disease')
        if active_disease is not None and loaded.entities_by_id.get(active_disease, {}).get('type') != 'diseases':
            raise ValueError('unknown active disease')
        if not core_only and active_disease is None:
            return loaded
        missing = {(p, msg): (eid, target) for p, msg, eid, target in loaded.missing_refs}
        blocking = []
        for p, msg in loaded.ref_errors:
            eid, target = missing.get((p, msg), (None, None))
            meta = deferred.get(eid)
            if (
                meta is None or target == 'sources' or meta['type'] == 'sources'
                or (active_disease is not None and meta['disease_id'] == active_disease)
                or (target is not None and meta['type'] != target)
            ):
                blocking.append((p, msg))
        return replace(loaded, ref_errors=blocking)
    except (OSError, ValueError, TypeError, KeyError):
        return replace(loaded, ref_errors=loaded.ref_errors + [(path, 'invalid bundle manifest')])
