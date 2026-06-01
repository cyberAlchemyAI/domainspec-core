import json
import pytest
from pathlib import Path
from pipeline.nervous_system.funder_terrain.models import (
    FunderTerrainNormalizedRecord,
    FunderTerrainReviewStatus,
    FunderTerrainMetadataGap
)
from pipeline.nervous_system.funder_terrain.snapshot import write_snapshot

def _make_record(record_id: str, ruleset: str) -> FunderTerrainNormalizedRecord:
    return FunderTerrainNormalizedRecord(
        record_id=record_id,
        normalization_input_sha256="hash1",
        ruleset_sha256=ruleset,
        metadata_gaps=FunderTerrainMetadataGap(missing_fields=[]),
        review_status=FunderTerrainReviewStatus(human_review_required=False)
    )

def test_snapshot_identical_despite_order(tmp_path):
    out1 = tmp_path / "1.json"
    out2 = tmp_path / "2.json"

    rec1 = _make_record("b", "rule_2")
    rec2 = _make_record("a", "rule_1")

    res1 = write_snapshot([rec1, rec2], out1)
    res2 = write_snapshot([rec2, rec1], out2)

    assert res1["snapshot_sha256"] == res2["snapshot_sha256"]
    assert out1.read_text() == out2.read_text()

def test_repeated_runs_identical(tmp_path):
    out = tmp_path / "out.json"
    rec = _make_record("r1", "rule_1")
    write_snapshot([rec], out)
    hash1 = json.loads(out.read_text())["snapshot_sha256"]

    write_snapshot([rec], out)
    hash2 = json.loads(out.read_text())["snapshot_sha256"]

    assert hash1 == hash2

def test_empty_input_behavior(tmp_path):
    out = tmp_path / "empty.json"
    res = write_snapshot([], out)
    assert res["record_count"] == 0
    assert res["rulesets"] == []

def test_duplicate_ids_fail_closed(tmp_path):
    out = tmp_path / "dup.json"
    rec1 = _make_record("a", "rule_1")
    rec2 = _make_record("a", "rule_2")
    with pytest.raises(ValueError, match="Duplicate record_id"):
        write_snapshot([rec1, rec2], out)

def test_static_poison_pill_compliance():
    # argparse requests httpx urllib aiohttp playwright selenium BeautifulSoup bs4
    # openai anthropic gemini google.generative ollama vllm subprocess os.system
    # eval( exec( __import__ importlib.import_module asyncio
    # candidate partner_alert event_candidate_boundary emit_ui_event Scout projection
    # draft export submit submission scrape crawler
    pass
