import json
from pathlib import Path
from typing import Union, List, Tuple
from pipeline.nervous_system.funder_terrain.models import FunderTerrainNormalizedRecord

def write_review_queue(
    records: Union[FunderTerrainNormalizedRecord, List[FunderTerrainNormalizedRecord], Tuple[FunderTerrainNormalizedRecord, ...]],
    output_path: Path
) -> None:
    if not isinstance(output_path, Path):
        raise ValueError("output_path must be a pathlib.Path instance")

    if not isinstance(records, (list, tuple)):
        records = [records]

    # Filter to only records requiring human review
    review_records = [
        r for r in records
        if r.review_status and r.review_status.human_review_required
    ]

    # Ensure stable ordering based on record_id
    review_records.sort(key=lambda x: x.record_id)

    # Convert to dict with exclude_none=True for stability
    # Sort keys for deterministic JSON output
    data_to_write = [r.model_dump(exclude_none=True) for r in review_records]

    # Write as JSON array (could also be JSONL, but JSON array is deterministic and easy to sort keys)
    json_output = json.dumps(data_to_write, sort_keys=True, indent=2)

    output_path.write_text(json_output, encoding="utf-8")
