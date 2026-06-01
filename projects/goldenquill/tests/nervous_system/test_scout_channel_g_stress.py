from pathlib import Path

import pytest

from pipeline.nervous_system.scout_adapters.channel_g_local import (
    ingest_local_channel_g_csv,
)
from pipeline.scout._channel_g_parser import ChannelGParseError


FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "scout" / "channel_g"
STRESS_FIXTURE = FIXTURES_DIR / "stress_test_dirty.csv"
MISSING_TITLE_FIXTURE = FIXTURES_DIR / "malformed_missing_title.csv"
MISSING_FUNDER_FIXTURE = FIXTURES_DIR / "malformed_missing_funder.csv"


def test_stress_fixture_parsing_and_deduplication():
    csv_text = STRESS_FIXTURE.read_text(encoding="utf-8")
    result = ingest_local_channel_g_csv(
        csv_text,
        applied_as_entity_id="fit_farms_llc",
        source_filename="stress_test_dirty.csv",
        imported_at_utc="2026-05-27T00:00:00Z",
    )

    # 4 data rows, 1 blank row -> 4 substantive rows
    assert len(result.raw_rows) == 4

    # Check deduplication
    unique_ids = {op.opportunity_id for op in result.opportunities}
    assert len(unique_ids) == 2

    # Check evidence deduplication
    evidence_names = {item.evidence_item for item in result.evidence_items}
    assert "Hardware BOM" in evidence_names
    assert "Letters of Support" in evidence_names
    assert len(result.evidence_items) == 2
    assert len(result.evidence_links) == 4


def test_stress_fixture_is_deterministic():
    csv_text = STRESS_FIXTURE.read_text(encoding="utf-8")
    first = ingest_local_channel_g_csv(
        csv_text,
        applied_as_entity_id="fit_farms_llc",
        source_filename="stress_test_dirty.csv",
        imported_at_utc="2026-05-27T00:00:00Z",
    )
    second = ingest_local_channel_g_csv(
        csv_text,
        applied_as_entity_id="fit_farms_llc",
        source_filename="stress_test_dirty.csv",
        imported_at_utc="2026-05-27T00:00:00Z",
    )
    assert first == second


def test_missing_required_title_fails_closed():
    csv_text = MISSING_TITLE_FIXTURE.read_text(encoding="utf-8")
    with pytest.raises(ChannelGParseError, match="Missing title"):
        ingest_local_channel_g_csv(
            csv_text,
            applied_as_entity_id="fit_farms_llc",
            source_filename="malformed_missing_title.csv",
            imported_at_utc="2026-05-27T00:00:00Z",
        )


def test_missing_required_funder_fails_closed():
    csv_text = MISSING_FUNDER_FIXTURE.read_text(encoding="utf-8")
    with pytest.raises(ChannelGParseError, match="Missing funder"):
        ingest_local_channel_g_csv(
            csv_text,
            applied_as_entity_id="fit_farms_llc",
            source_filename="malformed_missing_funder.csv",
            imported_at_utc="2026-05-27T00:00:00Z",
        )


def test_no_forbidden_runtime_imports():
    source = Path("pipeline/scout/_channel_g_parser.py").read_text(encoding="utf-8")
    adapter_source = Path("pipeline/nervous_system/scout_adapters/channel_g_local.py").read_text(encoding="utf-8")

    banned = [
        "requests", "httpx", "urllib", "aiohttp",
        "playwright", "selenium", "BeautifulSoup", "bs4",
        "openai", "anthropic", "gemini", "google.generative",
        "ollama", "vllm", "subprocess", "os.system"
    ]

    for term in banned:
        assert term.lower() not in source.lower(), f"Forbidden import found: {term}"
        assert term.lower() not in adapter_source.lower(), f"Forbidden import found: {term}"
