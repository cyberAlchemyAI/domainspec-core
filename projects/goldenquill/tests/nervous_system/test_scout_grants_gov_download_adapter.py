import ast
import os
import tempfile
from pathlib import Path

import pytest

from pipeline.nervous_system.scout_adapters.grants_gov_download import (
    GrantsGovParseError,
    parse_grants_gov_csv_text,
    parse_grants_gov_file,
)


def test_parses_valid_grants_gov_csv_fixture():
    csv_text = (
        "Opportunity Title,Agency,Close Date,Posted Date,Opportunity Number,Description,Additional Information on Eligibility,Award Ceiling,Award Floor,Additional Information URL\n"
        "Research Grant,NSF,2026-12-31,2026-01-01,NSF-123,Great grant,Anyone,100000,50000,http://example.com"
    )
    result = parse_grants_gov_csv_text(
        csv_text,
        applied_as_entity_id="ENT-1",
        source_filename="test.csv",
        imported_at_utc="2026-05-27T12:00:00Z"
    )
    assert len(result.opportunities) == 1
    opp = result.opportunities[0]
    assert opp.title == "Research Grant"
    assert opp.funder == "NSF"
    assert opp.close_date_utc == "2026-12-31"
    assert opp.posted_date_utc == "2026-01-01"
    assert opp.opportunity_number == "NSF-123"
    assert opp.description == "Great grant"
    assert opp.eligibility_text == "Anyone"
    assert opp.award_ceiling == 100000
    assert opp.award_floor == 50000
    assert opp.url == "http://example.com"


def test_preserves_raw_row_and_source_provenance():
    csv_text = "Title,Agency\nA,F1\nB,F2"
    result = parse_grants_gov_csv_text(
        csv_text,
        applied_as_entity_id="ENT-1",
        source_filename="test.csv",
        imported_at_utc="2026-05-27T12:00:00Z"
    )
    assert len(result.raw_rows) == 2
    assert result.raw_rows[0].raw_data["Title"] == "A"
    assert result.raw_rows[0].raw_data["Agency"] == "F1"

    assert len(result.provenance_records) == 2
    prov = result.provenance_records[0]
    assert prov.source_system == "grants_gov_download"
    assert prov.source_filename == "test.csv"
    assert prov.row_number == 2
    assert "Title" in prov.column_names_used
    assert "Agency" in prov.column_names_used
    assert prov.source_hash


def test_applied_as_entity_id_propagates_to_all_records():
    csv_text = "Title,Agency\nA,F1"
    result = parse_grants_gov_csv_text(
        csv_text,
        applied_as_entity_id="ENT-XYZ",
        source_filename="test.csv",
        imported_at_utc="2026-05-27T12:00:00Z"
    )
    assert result.opportunities[0].applied_as_entity_id == "ENT-XYZ"
    assert result.raw_rows[0].applied_as_entity_id == "ENT-XYZ"
    assert result.provenance_records[0].applied_as_entity_id == "ENT-XYZ"


def test_identity_hash_uses_only_allowed_identity_inputs():
    csv_1 = "Title,Agency,Opportunity Number\nSame,Funder,123"
    csv_2 = "Title,Agency,Opportunity Number\nSame,Funder,456"

    r1 = parse_grants_gov_csv_text(
        csv_1,
        applied_as_entity_id="ENT-1",
        source_filename="test.csv",
        imported_at_utc="2026"
    )
    r2 = parse_grants_gov_csv_text(
        csv_2,
        applied_as_entity_id="ENT-1",
        source_filename="test.csv",
        imported_at_utc="2026"
    )
    assert r1.opportunities[0].opportunity_id == r2.opportunities[0].opportunity_id


def test_missing_title_fails_closed():
    csv_text = "Title,Agency\n,Funder"
    with pytest.raises(GrantsGovParseError, match="Missing title"):
        parse_grants_gov_csv_text(
            csv_text,
            applied_as_entity_id="ENT-1",
            source_filename="test.csv",
            imported_at_utc="2026"
        )


def test_missing_funder_or_agency_fails_closed():
    csv_text = "Title,Agency\nTitle,"
    with pytest.raises(GrantsGovParseError, match="Missing funder/agency"):
        parse_grants_gov_csv_text(
            csv_text,
            applied_as_entity_id="ENT-1",
            source_filename="test.csv",
            imported_at_utc="2026"
        )


def test_empty_file_behavior_is_explicit():
    # An empty file string has no fieldnames. We chose to return 0 records if completely empty.
    result = parse_grants_gov_csv_text(
        "",
        applied_as_entity_id="ENT-1",
        source_filename="test.csv",
        imported_at_utc="2026"
    )
    assert len(result.opportunities) == 0


def test_invalid_extension_fails_before_file_open():
    with pytest.raises(GrantsGovParseError, match="Only .csv extensions are supported"):
        parse_grants_gov_file(
            "/does_not_exist/test.txt",
            applied_as_entity_id="ENT-1",
            imported_at_utc="2026"
        )


def test_pathlib_filename_extraction():
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        f.write(b"Title,Agency\nA,F1")
        f.close()
        result = parse_grants_gov_file(
            f.name,
            applied_as_entity_id="ENT-1",
            imported_at_utc="2026"
        )
        assert result.provenance_records[0].source_filename == Path(f.name).name
        os.unlink(f.name)


def test_url_fields_are_inert_metadata_only():
    csv_text = "Title,Agency,URL\nA,F1,http://example.com"
    result = parse_grants_gov_csv_text(
        csv_text,
        applied_as_entity_id="ENT-1",
        source_filename="test.csv",
        imported_at_utc="2026"
    )
    assert result.opportunities[0].url == "http://example.com"


def test_extra_unheadered_csv_column_fails_closed():
    csv_text = "Title,Agency\nGood,Funder,EXTRA"
    with pytest.raises(GrantsGovParseError, match="Malformed CSV: Row has more columns than headers."):
        parse_grants_gov_csv_text(
            csv_text,
            applied_as_entity_id="ENT-1",
            source_filename="test.csv",
            imported_at_utc="2026"
        )


def test_duplicate_normalized_headers_fail_closed():
    csv_text = "Title, title, Agency\nA,B,Funder"
    with pytest.raises(GrantsGovParseError, match="Malformed CSV: Duplicate normalized header 'title'"):
        parse_grants_gov_csv_text(
            csv_text,
            applied_as_entity_id="ENT-1",
            source_filename="test.csv",
            imported_at_utc="2026"
        )


def test_malformed_quoted_csv_fails_closed():
    csv_text = 'Title,Agency\n"Unclosed,Funder'
    with pytest.raises(GrantsGovParseError, match="Malformed CSV"):
        parse_grants_gov_csv_text(
            csv_text,
            applied_as_entity_id="ENT-1",
            source_filename="test.csv",
            imported_at_utc="2026"
        )


def test_missing_required_columns_with_non_empty_rows_fails_closed():
    csv_text = "Not Title,Not Agency\nA,B"
    with pytest.raises(GrantsGovParseError, match="Missing title"):
        parse_grants_gov_csv_text(
            csv_text,
            applied_as_entity_id="ENT-1",
            source_filename="test.csv",
            imported_at_utc="2026"
        )


def test_header_only_csv_behavior_is_explicit():
    csv_text = "Title,Agency\n"
    result = parse_grants_gov_csv_text(
        csv_text,
        applied_as_entity_id="ENT-1",
        source_filename="test.csv",
        imported_at_utc="2026"
    )
    assert len(result.opportunities) == 0
    assert len(result.raw_rows) == 0


def test_source_record_id_opportunity_number_provenance_is_preserved():
    csv_text = "Title,Agency,Opportunity Number\nA,F1,OPP-123"
    result = parse_grants_gov_csv_text(
        csv_text,
        applied_as_entity_id="ENT-1",
        source_filename="test.csv",
        imported_at_utc="2026"
    )
    assert result.opportunities[0].opportunity_number == "OPP-123"
    assert result.provenance_records[0].source_record_id == "OPP-123"


def test_zero_forbidden_network_imports_in_grants_gov_adapter():
    adapter_path = Path(__file__).parent.parent.parent / "pipeline" / "nervous_system" / "scout_adapters" / "grants_gov_download.py"
    banned = {
        "requests", "httpx", "urllib", "aiohttp", "socket",
        "playwright", "selenium", "openai", "anthropic", "google.generativeai"
    }
    with open(adapter_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(adapter_path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                base_module = alias.name.split('.')[0]
                assert base_module not in banned
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                base_module = node.module.split('.')[0]
                assert base_module not in banned


def test_zero_dynamic_import_or_eval_escape_hatches():
    adapter_path = Path(__file__).parent.parent.parent / "pipeline" / "nervous_system" / "scout_adapters" / "grants_gov_download.py"
    with open(adapter_path, "r", encoding="utf-8") as f:
        content = f.read()
    banned = ["importlib", "__import__", "eval(", "exec("]
    for b in banned:
        assert b not in content


def test_no_authority_expansion_language_in_adapter():
    adapter_path = Path(__file__).parent.parent.parent / "pipeline" / "nervous_system" / "scout_adapters" / "grants_gov_download.py"
    with open(adapter_path, "r", encoding="utf-8") as f:
        content = f.read().lower()
    banned = [
        "crawl", "scrape", "discover urls", "discover_url", "autonomous",
        "submit", "portal upload", "partner_alert", "outreach",
        "candidate_generation", "drafting", "all_model_access", "frontier_eligible"
    ]
    for b in banned:
        assert b not in content
