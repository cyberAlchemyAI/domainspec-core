from pipeline.nervous_system.funder_terrain.normalizer import normalize_record
from pipeline.nervous_system.funder_terrain.models import FunderTerrainSourceRecord, FunderTerrainProgramStatus
from pipeline.nervous_system.funder_terrain.rules import FunderTerrainRule

def test_normalizer_unknown_routes_to_human_review():
    source = FunderTerrainSourceRecord(source_id="src1", source_type="api")
    rules = {
        "funder_family": [FunderTerrainRule(rule_id="f1", target_field="text", priority=1, regex_patterns=["usda"], output_value="USDA", confidence="C", review_required=False, rationale="test")]
    }
    record = normalize_record("rec1", "test.txt", "/test.txt", "nothing here", source, rules, "fake_hash")

    assert record.funder_family is None
    assert record.review_status.human_review_required is True
    assert "funder_family" in record.metadata_gaps.missing_fields

def test_normalizer_fake_opportunity_no_candidates():
    source = FunderTerrainSourceRecord(source_id="src1", source_type="api")
    rules = {
        "document_type": [FunderTerrainRule(rule_id="d1", target_field="text", priority=1, regex_patterns=["active opportunity"], output_value="Guidelines", confidence="C", review_required=False, rationale="test")]
    }
    record = normalize_record("rec1", "test.txt", "/test.txt", "this is an active opportunity", source, rules, "fake_hash")

    assert record.document_type == "Guidelines"
    assert record.program_status == FunderTerrainProgramStatus.unknown
    assert "Candidate" not in str(type(record))
