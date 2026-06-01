import pytest
import json
from pydantic import ValidationError
from pipeline.nervous_system.scout_source_roster import (
    SourceRecord,
    SourceType,
    SourceStatus,
    list_configured_sources,
    summarize_source_coverage
)
from pipeline.nervous_system.scout_fetch_ledger import (
    FetchLedgerRecord,
    FetchMethod
)

def test_source_roster_requires_core_fields():
    with pytest.raises(ValidationError):
        SourceRecord(name="Missing stuff")

    record = SourceRecord(
        source_id="test_id",
        name="Test Source",
        source_type=SourceType.api,
        source_status=SourceStatus.verified
    )
    assert record.source_id == "test_id"
    assert record.name == "Test Source"

def test_source_status_cannot_be_blank():
    with pytest.raises(ValidationError):
        SourceRecord(
            source_id="test_id",
            name="Test Source",
            source_type=SourceType.api,
            source_status=""
        )

def test_disabled_unconfigured_represented_explicitly():
    sources = list_configured_sources()
    # Ensure they are not silently omitted and use source_not_configured
    assert any(s.source_status == SourceStatus.source_not_configured for s in sources)

def test_source_type_other_requires_notes():
    with pytest.raises(ValidationError, match="requires non-empty notes"):
        SourceRecord(
            source_id="test_other",
            name="Test Other",
            source_type=SourceType.other,
            source_status=SourceStatus.not_implemented,
            notes=""
        )

    # valid
    record = SourceRecord(
        source_id="test_other",
        name="Test Other",
        source_type=SourceType.other,
        source_status=SourceStatus.not_implemented,
        notes="A valid note"
    )
    assert record.notes == "A valid note"

def test_summarize_source_coverage_fixture_mode_logic():
    summary = summarize_source_coverage()
    fixture_mode = summary.get("fixture_mode")
    channels = summary.get("channels", [])

    # Requirement: fixture_mode == True OR (fixture_mode == False AND len(channels) > 0)
    assert fixture_mode is True or (fixture_mode is False and len(channels) > 0)

    # Must not be False and empty
    assert not (fixture_mode is False and len(channels) == 0)

def test_no_forbidden_strategy_language():
    record = SourceRecord(
        source_id="test_strategy",
        name="Test Name",
        source_type=SourceType.manual_seed,
        source_status=SourceStatus.source_not_configured,
        notes="A safe note."
    )

    ledger = FetchLedgerRecord(
        fetch_id="fetch_1",
        source_id="test_strategy",
        checked_at="2026-05-26T00:00:00Z",
        method=FetchMethod.api,
        result_status=SourceStatus.verified,
        notes="A safe ledger note."
    )

    output = record.model_dump_json() + " " + ledger.model_dump_json()
    output_lower = output.lower()

    forbidden = [
        "grant" + " stacking",
        "award" + " probability",
        "win" + " probability",
        "partner" + " committed",
        "ready" + " to apply",
        "final" + " submission allowed",
        "project" + " finance",
        "capital" + " sequencing"
    ]

    for word in forbidden:
        assert word not in output_lower

def test_no_fabricated_opportunities():
    summary = summarize_source_coverage()
    dump = json.dumps(summary)
    # Check that there are no "opportunities" keys
    assert "opportunities" not in dump.lower()
    assert "opportunity_list" not in dump.lower()
