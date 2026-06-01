from pathlib import Path

import pytest

from pipeline.nervous_system.scout_adapters.channel_g_local import (
    ingest_local_channel_g_csv,
)
from pipeline.scout._channel_g_parser import ChannelGParseResult


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "scout"
    / "channel_g"
    / "phantom_robotix_dirty_intake.csv"
)

APPLIED_AS_ENTITY_ID = "fit_farms_llc"
SOURCE_FILENAME = "phantom_robotix_dirty_intake.csv"
IMPORTED_AT_UTC = "2026-05-27T00:00:00Z"


def _load_fixture() -> str:
    return FIXTURE_PATH.read_text(encoding="utf-8")


def _ingest_fixture() -> ChannelGParseResult:
    return ingest_local_channel_g_csv(
        _load_fixture(),
        applied_as_entity_id=APPLIED_AS_ENTITY_ID,
        source_filename=SOURCE_FILENAME,
        imported_at_utc=IMPORTED_AT_UTC,
    )


def test_adapter_returns_parse_result():
    result = _ingest_fixture()

    assert isinstance(result, ChannelGParseResult)
    assert result.raw_rows
    assert result.opportunities
    assert result.evidence_items
    assert result.evidence_links
    assert result.provenance_records


def test_adapter_skips_blank_rows():
    result = _ingest_fixture()

    # Fixture has 4 data rows after header: 1 blank row + 3 substantive rows.
    assert len(result.raw_rows) == 3


def test_adapter_deduplicates_opportunities():
    result = _ingest_fixture()

    titles = {op.title for op in result.opportunities}
    unique_ids = {op.opportunity_id for op in result.opportunities}

    # Parser B1 yields one opportunity per row, but IDs deduplicate to 2.
    assert len(unique_ids) == 2
    assert "  AI Foraging Robotics Phase II" in titles
    assert "AgriTech Subsurface Detection " in titles


def test_adapter_deduplicates_evidence_but_preserves_links():
    result = _ingest_fixture()

    evidence_names = {item.evidence_item for item in result.evidence_items}

    assert "Hardware BOM" in evidence_names
    assert "Letters of Support" in evidence_names
    assert len({item.evidence_item_id for item in result.evidence_items}) == 2
    assert len(result.evidence_links) >= 3


def test_adapter_propagates_applied_as_entity_id():
    result = _ingest_fixture()

    for opportunity in result.opportunities:
        assert opportunity.applied_as_entity_id == APPLIED_AS_ENTITY_ID

    for item in result.evidence_items:
        if hasattr(item, "applied_as_entity_id"):
            assert item.applied_as_entity_id == APPLIED_AS_ENTITY_ID

    for record in result.provenance_records:
        if hasattr(record, "applied_as_entity_id"):
            assert record.applied_as_entity_id == APPLIED_AS_ENTITY_ID


def test_adapter_is_deterministic():
    first = _ingest_fixture()
    second = _ingest_fixture()

    assert first == second


def test_non_string_csv_text_rejected():
    with pytest.raises(TypeError):
        ingest_local_channel_g_csv(
            None,  # type: ignore[arg-type]
            applied_as_entity_id=APPLIED_AS_ENTITY_ID,
            source_filename=SOURCE_FILENAME,
            imported_at_utc=IMPORTED_AT_UTC,
        )


def test_empty_applied_as_entity_id_rejected():
    with pytest.raises(ValueError):
        ingest_local_channel_g_csv(
            _load_fixture(),
            applied_as_entity_id=" ",
            source_filename=SOURCE_FILENAME,
            imported_at_utc=IMPORTED_AT_UTC,
        )


def test_empty_source_filename_rejected():
    with pytest.raises(ValueError):
        ingest_local_channel_g_csv(
            _load_fixture(),
            applied_as_entity_id=APPLIED_AS_ENTITY_ID,
            source_filename=" ",
            imported_at_utc=IMPORTED_AT_UTC,
        )


def test_empty_imported_at_utc_rejected():
    with pytest.raises(ValueError):
        ingest_local_channel_g_csv(
            _load_fixture(),
            applied_as_entity_id=APPLIED_AS_ENTITY_ID,
            source_filename=SOURCE_FILENAME,
            imported_at_utc=" ",
        )


def test_banned_imports_in_adapter():
    source = Path(
        "pipeline/nervous_system/scout_adapters/channel_g_local.py"
    ).read_text(encoding="utf-8")

    forbidden_terms = [
        "requests",
        "httpx",
        "urllib",
        "aiohttp",
        "playwright",
        "selenium",
        "BeautifulSoup",
        "bs4",
        "openai",
        "anthropic",
        "gemini",
        "google.generative",
        "ollama",
        "vllm",
        "subprocess",
        "os.system",
        "sqlite",
        "sqlalchemy",
        "session.commit",
        "insert(",
        "update(",
        "delete(",
        "fetch(",
        "scrape",
        "crawler",
        "browser",
        "export",
        "submit",
        "submission",
        "drafting",
        "partner_alert",
        "candidate_generation",
    ]

    lowered = source.lower()
    for term in forbidden_terms:
        assert term.lower() not in lowered
