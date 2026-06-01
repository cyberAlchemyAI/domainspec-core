import pytest
from pipeline.nervous_system.funder_terrain.normalizer import normalize_record
from pipeline.nervous_system.funder_terrain.models import FunderTerrainSourceRecord

def test_missing_source_identifier_fails_closed():
    source = FunderTerrainSourceRecord(source_id="", source_type="api")
    with pytest.raises(ValueError, match="Missing valid source identifier"):
        normalize_record("rec1", "test.txt", "/test.txt", "text", source, {}, "hash")

def test_duplicate_source_document_id():
    with pytest.raises(ValueError, match="Missing valid source identifier"):
        normalize_record("rec1", "test.txt", "/test.txt", "text", None, {}, "hash")
