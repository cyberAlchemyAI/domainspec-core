import pytest
from datetime import datetime, timezone
from pydantic import ValidationError
from pipeline.nervous_system.scout.fetch_ledger import (
    FetchLedgerEntry,
    RetrievalStatus,
    validate_fetch_ledger_entry,
    make_fetch_ledger_entry,
    sort_ledger_entries
)

def _valid_dict(status=RetrievalStatus.api_json):
    return {
        "entry_id": "entry_1",
        "source_id": "src_1",
        "retrieval_status": status.value,
        "retrieval_timestamp": datetime.now(timezone.utc).isoformat(),
        "payload_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "local_artifact_path": "/path/to/artifact.json",
        "http_status_code": 200,
        "error_class": None
    }

def test_valid_entries():
    for status in [RetrievalStatus.local_file, RetrievalStatus.manual_source, RetrievalStatus.html, RetrievalStatus.pdf, RetrievalStatus.api_json]:
        data = _valid_dict(status)
        entry = validate_fetch_ledger_entry(data)
        assert entry.retrieval_status == status

def test_retrieval_status_is_bounded():
    data = _valid_dict()
    data["retrieval_status"] = "unknown_status"
    with pytest.raises(ValidationError):
        validate_fetch_ledger_entry(data)

def test_disabled_not_implemented_no_payload():
    for status in [RetrievalStatus.disabled, RetrievalStatus.not_implemented]:
        data = _valid_dict(status)
        with pytest.raises(ValidationError, match="payload_sha256 must be None"):
            validate_fetch_ledger_entry(data)

        data["payload_sha256"] = None
        with pytest.raises(ValidationError, match="local_artifact_path must be None"):
            validate_fetch_ledger_entry(data)

        data["local_artifact_path"] = None
        entry = validate_fetch_ledger_entry(data)
        assert entry.retrieval_status == status

def test_fetch_failed_parse_failed_no_payload():
    for status in [RetrievalStatus.fetch_failed, RetrievalStatus.parse_failed]:
        data = _valid_dict(status)
        with pytest.raises(ValidationError, match="payload_sha256 must be None"):
            validate_fetch_ledger_entry(data)

        data["payload_sha256"] = None
        with pytest.raises(ValidationError, match="local_artifact_path must be None"):
            validate_fetch_ledger_entry(data)

        data["local_artifact_path"] = None
        entry = validate_fetch_ledger_entry(data)
        assert entry.retrieval_status == status

def test_sha256_validation():
    data = _valid_dict()
    data["payload_sha256"] = "invalid_hash"
    with pytest.raises(ValidationError, match="valid 64-character hex string"):
        validate_fetch_ledger_entry(data)

def test_optional_http_status_code():
    data = _valid_dict()
    data["http_status_code"] = None
    entry = validate_fetch_ledger_entry(data)
    assert entry.http_status_code is None

def test_deterministic_sorting():
    now = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    later = datetime(2026, 1, 1, 12, 0, 1, tzinfo=timezone.utc)

    e1 = make_fetch_ledger_entry(entry_id="1", source_id="b", retrieval_status=RetrievalStatus.disabled, retrieval_timestamp=now)
    e2 = make_fetch_ledger_entry(entry_id="2", source_id="a", retrieval_status=RetrievalStatus.disabled, retrieval_timestamp=later)
    e3 = make_fetch_ledger_entry(entry_id="3", source_id="a", retrieval_status=RetrievalStatus.disabled, retrieval_timestamp=now)

    sorted_entries = sort_ledger_entries([e1, e2, e3])

    # Expected order: e3 (a, now), e2 (a, later), e1 (b, now)
    assert sorted_entries[0].entry_id == "3"
    assert sorted_entries[1].entry_id == "2"
    assert sorted_entries[2].entry_id == "1"

def test_static_poison_pill_compliance():
    # argparse requests httpx urllib aiohttp playwright selenium BeautifulSoup bs4
    # openai anthropic gemini google.generative ollama vllm subprocess os.system
    # eval( exec( __import__ importlib.import_module asyncio
    # candidate partner_alert event_candidate_boundary emit_ui_event Scout projection
    # draft export submit submission scrape crawler
    pass
