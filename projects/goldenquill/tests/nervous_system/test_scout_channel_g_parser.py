import ast
import csv
from pathlib import Path

import pytest

from pipeline.scout._channel_g_types import (
    BoardCategoryEnum,
    CycleStatusEnum,
    DeadlineStatusEnum,
    EligibilityStatusEnum,
    ScoringStatusEnum,
)
from pipeline.scout._channel_g_parser import (
    ChannelGParseError,
    _normalize_header,
    parse_channel_g_csv_text,
    parse_channel_g_rows,
)


def _default_row() -> dict[str, str]:
    return {
        "Title": "Test Grant",
        "Funder": "NSF",
    }


def test_parse_csv_preserves_raw_rows():
    csv_text = "Title,Funder,ExtraCol\nTest Grant,NSF,ExtraVal"
    result = parse_channel_g_csv_text(
        csv_text,
        applied_as_entity_id="ENT-123",
        source_filename="test.csv",
        imported_at_utc="2026-05-26T12:00:00Z",
    )
    assert len(result.raw_rows) == 1
    assert result.raw_rows[0].raw_data["ExtraCol"] == "ExtraVal"


def test_applied_as_entity_id_propagated_to_all_records():
    row = _default_row()
    row["Evidence Item"] = "A plan"
    result = parse_channel_g_rows(
        [row],
        applied_as_entity_id="ENT-123",
        source_filename="test.csv",
        source_hash="abcd",
        imported_at_utc="2026-05-26T12:00:00Z",
    )
    assert result.raw_rows[0].applied_as_entity_id == "ENT-123"
    assert result.opportunities[0].applied_as_entity_id == "ENT-123"
    assert result.evidence_items[0].applied_as_entity_id == "ENT-123"
    assert result.evidence_links[0].applied_as_entity_id == "ENT-123"
    assert result.provenance_records[0].applied_as_entity_id == "ENT-123"


def test_missing_title_or_funder_raises_fail_closed_error():
    with pytest.raises(ChannelGParseError, match="Missing title"):
        parse_channel_g_rows(
            [{"Funder": "NSF", "Other": "Val"}],
            applied_as_entity_id="ENT-123",
            source_filename="t.csv",
            source_hash="h",
            imported_at_utc="2026",
        )
    with pytest.raises(ChannelGParseError, match="Missing funder"):
        parse_channel_g_rows(
            [{"Title": "A Grant", "Other": "Val"}],
            applied_as_entity_id="ENT-123",
            source_filename="t.csv",
            source_hash="h",
            imported_at_utc="2026",
        )


def test_trailing_blank_rows_are_skipped():
    rows = [
        {"Title": "Grant 1", "Funder": "Funder 1"},
        {"Title": "", "Funder": None, "Other": "   "},
    ]
    result = parse_channel_g_rows(
        rows,
        applied_as_entity_id="ENT-123",
        source_filename="t.csv",
        source_hash="h",
        imported_at_utc="2026",
    )
    assert len(result.opportunities) == 1
    assert len(result.raw_rows) == 1


def test_missing_score_not_zero_through_parser():
    row = _default_row()
    row["Total Score"] = ""
    result = parse_channel_g_rows(
        [row],
        applied_as_entity_id="ENT-123",
        source_filename="t.csv",
        source_hash="h",
        imported_at_utc="2026",
    )
    score = result.opportunities[0].total_score
    assert score.scoring_status == ScoringStatusEnum.UNAVAILABLE
    assert score.normalized_value is None


def test_unknown_eligibility_not_false_through_parser():
    row = _default_row()
    row["Eligibility"] = ""
    result = parse_channel_g_rows(
        [row],
        applied_as_entity_id="ENT-123",
        source_filename="t.csv",
        source_hash="h",
        imported_at_utc="2026",
    )
    assert result.opportunities[0].eligibility_status == EligibilityStatusEnum.UNKNOWN


def test_closed_recurring_allocates_next_cycle():
    row = _default_row()
    row["Deadline Status"] = "Closed"
    row["Cycle Status"] = "Recurring"
    result = parse_channel_g_rows(
        [row],
        applied_as_entity_id="ENT-123",
        source_filename="t.csv",
        source_hash="h",
        imported_at_utc="2026",
    )
    assert result.opportunities[0].board_category == BoardCategoryEnum.NEXT_CYCLE


def test_hard_blocker_high_fit_allocates_prepare():
    row = _default_row()
    row["Total Score"] = "95/100"
    row["Hard Blocker"] = "Yes"
    result = parse_channel_g_rows(
        [row],
        applied_as_entity_id="ENT-123",
        source_filename="t.csv",
        source_hash="h",
        imported_at_utc="2026",
    )
    assert result.opportunities[0].board_category == BoardCategoryEnum.PREPARE


def test_partner_required_unconfirmed_allocates_partner_consortium():
    row = _default_row()
    row["Partner Required"] = "True"
    row["Partner Confirmed"] = "False"
    result = parse_channel_g_rows(
        [row],
        applied_as_entity_id="ENT-123",
        source_filename="t.csv",
        source_hash="h",
        imported_at_utc="2026",
    )
    assert result.opportunities[0].board_category == BoardCategoryEnum.PARTNER_CONSORTIUM


def test_evidence_deduplication_many_to_many():
    rows = [
        {"Title": "Opp A", "Funder": "Funder A", "Evidence Item": "Commercialization Plan"},
        {"Title": "Opp B", "Funder": "Funder B", "Evidence Item": "Commercialization Plan"},
    ]
    result = parse_channel_g_rows(
        rows,
        applied_as_entity_id="ENT-123",
        source_filename="t.csv",
        source_hash="h",
        imported_at_utc="2026",
    )
    assert len(result.evidence_items) == 1
    assert len(result.evidence_links) == 2


def test_provenance_hash_and_row_number():
    csv_text = "Title,Funder\nA,F1\nB,F2"
    result = parse_channel_g_csv_text(
        csv_text,
        applied_as_entity_id="ENT-123",
        source_filename="t.csv",
        imported_at_utc="2026",
    )
    p1, p2 = result.provenance_records
    assert p1.row_number == 2
    assert p2.row_number == 3
    assert p1.source_hash == p2.source_hash
    assert len(p1.source_hash) == 64


def test_csv_text_parser_source_hash_stable():
    csv_text = "Title,Funder\nA,F1"
    r1 = parse_channel_g_csv_text(
        csv_text,
        applied_as_entity_id="ENT-123",
        source_filename="t.csv",
        imported_at_utc="2026",
    )
    r2 = parse_channel_g_csv_text(
        csv_text,
        applied_as_entity_id="ENT-123",
        source_filename="t.csv",
        imported_at_utc="2027",
    )
    assert r1.provenance_records[0].source_hash == r2.provenance_records[0].source_hash


def test_can_be_generated_by_tilth_static_false():
    row = _default_row()
    row["Evidence Item"] = "Pitch Deck"
    result = parse_channel_g_rows(
        [row],
        applied_as_entity_id="ENT-123",
        source_filename="t.csv",
        source_hash="h",
        imported_at_utc="2026",
    )
    assert result.evidence_items[0].can_be_generated_by_tilth is False


def test_opportunity_id_stable_across_reordered_imports():
    row_a = {"Title": "Grant A", "Funder": "NSF"}
    row_b = {"Title": "Grant B", "Funder": "NIH"}

    res1 = parse_channel_g_rows(
        [row_a, row_b],
        applied_as_entity_id="ENT-1",
        source_filename="f1",
        source_hash="h1",
        imported_at_utc="t1",
    )

    res2 = parse_channel_g_rows(
        [row_b, row_a],
        applied_as_entity_id="ENT-1",
        source_filename="f2",
        source_hash="h2",
        imported_at_utc="t2",
    )

    # row_a opportunity_id should be the same
    id1 = [o.opportunity_id for o in res1.opportunities if o.title == "Grant A"][0]
    id2 = [o.opportunity_id for o in res2.opportunities if o.title == "Grant A"][0]
    assert id1 == id2


def test_opportunity_id_ignores_url_volatility():
    row_a = {"Title": "Grant A", "Funder": "NSF", "URL": "http://nsf.gov/old"}
    row_b = {"Title": "Grant A", "Funder": "NSF", "URL": "https://nsf.gov/new"}

    res1 = parse_channel_g_rows(
        [row_a],
        applied_as_entity_id="ENT-1",
        source_filename="f1",
        source_hash="h",
        imported_at_utc="t",
    )
    res2 = parse_channel_g_rows(
        [row_b],
        applied_as_entity_id="ENT-1",
        source_filename="f1",
        source_hash="h",
        imported_at_utc="t",
    )
    assert res1.opportunities[0].opportunity_id == res2.opportunities[0].opportunity_id


def test_dirty_csv_headers_are_normalized():
    assert _normalize_header(" Funder ") == "funder"
    assert _normalize_header("TOTAL SCORE") == "total score"
    assert _normalize_header("Evidence\nNeeded") == "evidence needed"

    rows = [{" Funder ": "NSF", "TOTAL SCORE": "90", "Program Name\n": "G1"}]
    res = parse_channel_g_rows(
        rows,
        applied_as_entity_id="ENT-1",
        source_filename="f1",
        source_hash="h",
        imported_at_utc="t",
    )
    assert res.opportunities[0].funder == "NSF"
    assert res.opportunities[0].title == "G1"
    assert res.opportunities[0].total_score.normalized_value == 90.0


def test_utf8_bom_header_is_normalized():
    assert _normalize_header("\ufeffProgram Name") == "program name"


def test_close_date_preserved_not_normalized():
    row = _default_row()
    row["Close Date"] = "Spring 2026"
    res = parse_channel_g_rows(
        [row],
        applied_as_entity_id="ENT-1",
        source_filename="f1",
        source_hash="h",
        imported_at_utc="t",
    )
    assert res.opportunities[0].close_date_utc == "Spring 2026"


def test_no_banned_imports_in_parser():
    parser_path = Path(__file__).parent.parent.parent / "pipeline" / "scout" / "_channel_g_parser.py"
    banned = {
        "pathlib", "openpyxl", "pandas", "httpx", "requests",
        "playwright", "selenium", "asyncio", "openai",
        "anthropic", "google.generativeai"
    }

    with open(parser_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(parser_path))

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                base_module = alias.name.split('.')[0]
                assert base_module not in banned, f"Found banned import: {alias.name}"
                assert alias.name not in banned, f"Found banned import: {alias.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                base_module = node.module.split('.')[0]
                assert base_module not in banned, f"Found banned import: {node.module}"
                assert node.module not in banned, f"Found banned import: {node.module}"
