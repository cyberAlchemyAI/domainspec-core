from typing import Dict, List
from pipeline.nervous_system.funder_terrain.models import (
    FunderTerrainNormalizedRecord, FunderTerrainProgramStatus,
    FunderTerrainSourceRecord, FunderTerrainReviewStatus, FunderTerrainMetadataGap
)
from pipeline.nervous_system.funder_terrain.rules import FunderTerrainRule, check_rules
from pipeline.nervous_system.funder_terrain.provenance import compute_input_hash, compute_record_hash

def normalize_record(
    record_id: str,
    filename: str,
    original_path: str,
    text_window: str,
    source_record: FunderTerrainSourceRecord,
    rules_dict: Dict[str, List[FunderTerrainRule]],
    ruleset_sha256: str
) -> FunderTerrainNormalizedRecord:

    if not source_record or not source_record.source_id:
        raise ValueError("Missing valid source identifier for normalization.")

    input_hash = compute_input_hash(text_window)

    # Funder Family
    funder = None
    f_match = check_rules(filename, rules_dict.get("funder_family", []))
    if not f_match:
        f_match = check_rules(original_path, rules_dict.get("funder_family", []))
    if not f_match:
        f_match = check_rules(text_window, rules_dict.get("funder_family", []))

    if f_match:
        funder = f_match[0].output_value

    # Doc Type
    dtype = None
    d_match = check_rules(filename, rules_dict.get("document_type", []))
    if not d_match:
        d_match = check_rules(text_window, rules_dict.get("document_type", []))
    if d_match:
        dtype = d_match[0].output_value

    # Project
    project = None
    p_match = check_rules(filename, rules_dict.get("project", []))
    if not p_match:
        p_match = check_rules(text_window, rules_dict.get("project", []))
    if p_match:
        project = p_match[0].output_value

    # Geography
    geography = None
    g_match = check_rules(filename, rules_dict.get("geography", []))
    if not g_match:
        g_match = check_rules(text_window, rules_dict.get("geography", []))
    if g_match:
        geography = g_match[0].output_value

    missing_fields = []
    if not funder: missing_fields.append("funder_family")
    if not dtype: missing_fields.append("document_type")
    if not project: missing_fields.append("related_project")
    if not geography: missing_fields.append("geography_scope")

    review_required = False
    review_reason = None
    if missing_fields:
        review_required = True
        review_reason = f"Missing fields: {', '.join(missing_fields)}"

    program_status = FunderTerrainProgramStatus.unknown
    if funder and dtype:
        program_status = FunderTerrainProgramStatus.known_active

    rec = FunderTerrainNormalizedRecord(
        record_id=record_id,
        funder_family=funder,
        document_type=dtype,
        related_project=project,
        geography_scope=geography,
        program_status=program_status,
        source_provenance=source_record,
        metadata_gaps=FunderTerrainMetadataGap(missing_fields=missing_fields),
        review_status=FunderTerrainReviewStatus(human_review_required=review_required, reason=review_reason),
        normalization_input_sha256=input_hash,
        ruleset_sha256=ruleset_sha256
    )

    rec.record_sha256 = compute_record_hash(rec.model_dump())
    return rec
