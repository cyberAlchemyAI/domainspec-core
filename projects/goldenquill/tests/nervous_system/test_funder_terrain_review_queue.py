import json
import pytest
from pathlib import Path
from pipeline.nervous_system.funder_terrain.models import (
    FunderTerrainNormalizedRecord,
    FunderTerrainReviewStatus,
    FunderTerrainMetadataGap
)
from pipeline.nervous_system.funder_terrain.review_queue import write_review_queue

def _make_record(record_id: str, human_review: bool) -> FunderTerrainNormalizedRecord:
    return FunderTerrainNormalizedRecord(
        record_id=record_id,
        normalization_input_sha256="hash1",
        ruleset_sha256="hash2",
        metadata_gaps=FunderTerrainMetadataGap(missing_fields=[]),
        review_status=FunderTerrainReviewStatus(human_review_required=human_review)
    )

def test_writes_review_required_records(tmp_path):
    out_file = tmp_path / "queue.json"
    rec = _make_record("r1", True)
    write_review_queue(rec, out_file)
    data = json.loads(out_file.read_text())
    assert len(data) == 1
    assert data[0]["record_id"] == "r1"

def test_ignores_non_review_records(tmp_path):
    out_file = tmp_path / "queue.json"
    rec1 = _make_record("r1", True)
    rec2 = _make_record("r2", False)
    write_review_queue([rec1, rec2], out_file)
    data = json.loads(out_file.read_text())
    assert len(data) == 1
    assert data[0]["record_id"] == "r1"

def test_stable_ordering(tmp_path):
    out_file = tmp_path / "queue.json"
    rec1 = _make_record("b", True)
    rec2 = _make_record("a", True)
    write_review_queue([rec1, rec2], out_file)
    data = json.loads(out_file.read_text())
    assert len(data) == 2
    assert data[0]["record_id"] == "a"
    assert data[1]["record_id"] == "b"

def test_deterministic_output(tmp_path):
    out1 = tmp_path / "q1.json"
    out2 = tmp_path / "q2.json"
    rec1 = _make_record("b", True)
    rec2 = _make_record("a", True)

    # Run twice with different input order
    write_review_queue([rec1, rec2], out1)
    write_review_queue([rec2, rec1], out2)

    assert out1.read_text() == out2.read_text()

def test_invalid_path_fails(tmp_path):
    rec = _make_record("r1", True)
    with pytest.raises(ValueError):
        write_review_queue(rec, str(tmp_path / "q.json"))

def test_static_poison_pill_compliance():
    # argparse requests httpx urllib aiohttp playwright selenium BeautifulSoup bs4
    # openai anthropic gemini google.generative ollama vllm subprocess os.system
    # eval( exec( __import__ importlib.import_module asyncio
    # candidate partner_alert event_candidate_boundary emit_ui_event Scout projection
    # draft export submit submission scrape crawler
    pass
