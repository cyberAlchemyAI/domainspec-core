import json
import hashlib
from pathlib import Path
from typing import List, Tuple, Dict, Any, Union
from pipeline.nervous_system.funder_terrain.models import FunderTerrainNormalizedRecord

def write_snapshot(
    records: Union[List[FunderTerrainNormalizedRecord], Tuple[FunderTerrainNormalizedRecord, ...]],
    output_path: Path
) -> Dict[str, Any]:
    if not isinstance(output_path, Path):
        raise ValueError("output_path must be a pathlib.Path instance")

    if not isinstance(records, (list, tuple)):
        raise ValueError("records must be a list or tuple of normalized records")

    # Detect duplicates
    seen_ids = set()
    for r in records:
        if r.record_id in seen_ids:
            raise ValueError(f"Duplicate record_id found: {r.record_id}")
        seen_ids.add(r.record_id)

    # Sort deterministically
    sorted_records = sorted(records, key=lambda x: x.record_id)

    # Collect unique rulesets
    rulesets = sorted(list(set(r.ruleset_sha256 for r in sorted_records if r.ruleset_sha256)))

    # Dump records cleanly
    record_dumps = [r.model_dump(exclude_none=True) for r in sorted_records]

    # Generate snapshot content
    snapshot_content = {
        "version": "1.0",
        "record_count": len(sorted_records),
        "rulesets": rulesets,
        "records": record_dumps
    }

    # Deterministic JSON bytes for hashing
    json_bytes = json.dumps(snapshot_content, sort_keys=True).encode("utf-8")
    snapshot_hash = hashlib.sha256(json_bytes).hexdigest()

    snapshot_content["snapshot_sha256"] = snapshot_hash

    # Write to file
    final_json = json.dumps(snapshot_content, sort_keys=True, indent=2)
    output_path.write_text(final_json, encoding="utf-8")

    return snapshot_content
