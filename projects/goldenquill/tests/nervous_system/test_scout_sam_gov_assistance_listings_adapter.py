import ast
import os
import tempfile
from pathlib import Path

import pytest

from pipeline.nervous_system.scout_adapters.sam_gov_assistance_listings import (
    SamGovParseError,
    parse_sam_gov_csv_text,
    parse_sam_gov_file,
)


def test_parses_valid_sam_gov_assistance_listings_csv_fixture():
    csv_text = (
        "Assistance Listing Number,Program Title,Agency,Agency Code,Sub-Tier,Assistance Type,Objectives,Eligible Applicants,Beneficiaries,Use Restrictions,Application Procedures,Award Floor,Award Ceiling,Last Updated Date,URL\n"
        "12.345,Good Program,NSF,123,Sub NSF,Grant,Help people,Anyone,Everyone,None,Apply,100000,500000,2026-01-01,http://example.com"
    )
    result = parse_sam_gov_csv_text(
        csv_text,
        source_filename="test.csv",
        imported_at_utc="2026-05-27T12:00:00Z"
    )
    assert len(result.listings) == 1
    listing = result.listings[0]
    assert listing.assistance_listing_number == "12.345"
    assert listing.program_title == "Good Program"
    assert listing.agency == "NSF"
    assert listing.agency_code == "123"
    assert listing.subagency == "Sub NSF"
    assert listing.assistance_type == "Grant"
    assert listing.objectives == "Help people"
    assert listing.eligible_applicants == "Anyone"
    assert listing.beneficiaries == "Everyone"
    assert listing.use_restrictions == "None"
    assert listing.application_procedures == "Apply"
    assert listing.award_floor == 100000
    assert listing.award_ceiling == 500000
    assert listing.last_updated_date == "2026-01-01"
    assert listing.url == "http://example.com"


def test_preserves_raw_row_and_source_provenance():
    csv_text = "Assistance Listing Number,Program Title,Agency,Agency Code\n12.345,A,F1,C1"
    result = parse_sam_gov_csv_text(
        csv_text,
        source_filename="test.csv",
        imported_at_utc="2026-05-27T12:00:00Z"
    )
    assert len(result.raw_rows) == 1
    assert result.raw_rows[0].raw_data["Program Title"] == "A"

    assert len(result.provenance_records) == 1
    prov = result.provenance_records[0]
    assert prov.source_system == "sam_gov_assistance_listings_download"
    assert prov.source_filename == "test.csv"
    assert prov.row_number == 2
    assert "Program Title" in prov.column_names_used
    assert prov.source_hash
    assert prov.parser_version == "sam_gov_adapter_v1"
    assert prov.source_record_id == "12.345"


def test_listing_identity_does_not_use_applied_as_entity_id():
    csv_text = "Assistance Listing Number,Program Title,Agency,Agency Code\n12.345,A,F1,C1"

    r1 = parse_sam_gov_csv_text(
        csv_text,
        applied_as_entity_id="ENT-1",
        source_filename="test.csv",
        imported_at_utc="2026"
    )
    r2 = parse_sam_gov_csv_text(
        csv_text,
        applied_as_entity_id="ENT-2",
        source_filename="test.csv",
        imported_at_utc="2026"
    )
    assert r1.listings[0].listing_id == r2.listings[0].listing_id
    assert not hasattr(r1.listings[0], "applied_as_entity_id")


def test_listing_identity_uses_only_allowed_reference_inputs():
    csv_1 = "Assistance Listing Number,Program Title,Agency,Agency Code,URL\n12.345,Same,F1,C1,url1"
    csv_2 = "Assistance Listing Number,Program Title,Agency,Agency Code,URL\n12.345,Same,F1,C1,url2"

    r1 = parse_sam_gov_csv_text(
        csv_1,
        source_filename="test.csv",
        imported_at_utc="2026"
    )
    r2 = parse_sam_gov_csv_text(
        csv_2,
        source_filename="test2.csv",
        imported_at_utc="2026"
    )
    assert r1.listings[0].listing_id == r2.listings[0].listing_id


def test_missing_assistance_listing_number_fails_closed():
    csv_text = "Program Title,Agency,Agency Code\nTitle,Funder,C1"
    with pytest.raises(SamGovParseError, match="Missing assistance_listing_number"):
        parse_sam_gov_csv_text(
            csv_text,
            source_filename="test.csv",
            imported_at_utc="2026"
        )


def test_missing_program_title_fails_closed():
    csv_text = "Assistance Listing Number,Agency,Agency Code\n12.345,Funder,C1"
    with pytest.raises(SamGovParseError, match="Missing program_title"):
        parse_sam_gov_csv_text(
            csv_text,
            source_filename="test.csv",
            imported_at_utc="2026"
        )


def test_missing_agency_fails_closed():
    csv_text = "Assistance Listing Number,Program Title,Agency Code\n12.345,Title,C1"
    with pytest.raises(SamGovParseError, match="Missing agency"):
        parse_sam_gov_csv_text(
            csv_text,
            source_filename="test.csv",
            imported_at_utc="2026"
        )


def test_missing_agency_code_fails_closed():
    csv_text = "Assistance Listing Number,Program Title,Agency\n12.345,Title,Funder"
    with pytest.raises(SamGovParseError, match="Missing agency_code"):
        parse_sam_gov_csv_text(
            csv_text,
            source_filename="test.csv",
            imported_at_utc="2026"
        )


def test_invalid_extension_fails_before_file_open():
    with pytest.raises(SamGovParseError, match="Only .csv extensions are supported"):
        parse_sam_gov_file(
            "/does_not_exist/test.txt",
            imported_at_utc="2026"
        )


def test_pathlib_filename_extraction():
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        f.write(b"Assistance Listing Number,Program Title,Agency,Agency Code\n12.345,A,F1,C1")
        f.close()
        result = parse_sam_gov_file(
            f.name,
            imported_at_utc="2026"
        )
        assert result.provenance_records[0].source_filename == Path(f.name).name
        os.unlink(f.name)


def test_extra_unheadered_csv_column_fails_closed():
    csv_text = "Assistance Listing Number,Program Title,Agency,Agency Code\n12.345,A,F1,C1,EXTRA"
    with pytest.raises(SamGovParseError, match="Malformed CSV: Row has more columns than headers."):
        parse_sam_gov_csv_text(
            csv_text,
            source_filename="test.csv",
            imported_at_utc="2026"
        )


def test_duplicate_normalized_headers_fails_closed():
    csv_text = "Program Title, program title, Assistance Listing Number, Agency, Agency Code\nA,B,12.345,Funder,C1"
    with pytest.raises(SamGovParseError, match="Malformed CSV: Duplicate normalized header 'program title'"):
        parse_sam_gov_csv_text(
            csv_text,
            source_filename="test.csv",
            imported_at_utc="2026"
        )


def test_malformed_quoted_csv_fails_closed_if_detected():
    csv_text = 'Assistance Listing Number,Program Title,Agency,Agency Code\n12.345,"Unclosed,Funder,C1'
    with pytest.raises(SamGovParseError, match="Malformed CSV"):
        parse_sam_gov_csv_text(
            csv_text,
            source_filename="test.csv",
            imported_at_utc="2026"
        )


def test_missing_required_columns_with_non_empty_rows_fails_closed():
    csv_text = "Not ALN,Not Title\n12.345,A"
    with pytest.raises(SamGovParseError, match="Missing assistance_listing_number"):
        parse_sam_gov_csv_text(
            csv_text,
            source_filename="test.csv",
            imported_at_utc="2026"
        )


def test_header_only_csv_behavior_is_explicit():
    csv_text = "Assistance Listing Number,Program Title,Agency,Agency Code\n"
    result = parse_sam_gov_csv_text(
        csv_text,
        source_filename="test.csv",
        imported_at_utc="2026"
    )
    assert len(result.listings) == 0
    assert len(result.raw_rows) == 0


def test_url_fields_are_inert_metadata_only():
    csv_text = "Assistance Listing Number,Program Title,Agency,Agency Code,URL\n12.345,A,F1,C1,http://example.com"
    result = parse_sam_gov_csv_text(
        csv_text,
        source_filename="test.csv",
        imported_at_utc="2026"
    )
    assert result.listings[0].url == "http://example.com"


def test_award_amount_parsing():
    csv_text = 'Assistance Listing Number,Program Title,Agency,Agency Code,Award Floor,Award Ceiling\n12.345,A,F1,C1,"$100,000",\n'
    result = parse_sam_gov_csv_text(
        csv_text,
        source_filename="test.csv",
        imported_at_utc="2026"
    )
    assert result.listings[0].award_floor == 100000
    assert result.listings[0].award_ceiling is None


def test_zero_forbidden_network_imports_in_sam_gov_adapter():
    adapter_path = Path(__file__).parent.parent.parent / "pipeline" / "nervous_system" / "scout_adapters" / "sam_gov_assistance_listings.py"
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
    adapter_path = Path(__file__).parent.parent.parent / "pipeline" / "nervous_system" / "scout_adapters" / "sam_gov_assistance_listings.py"
    with open(adapter_path, "r", encoding="utf-8") as f:
        content = f.read()
    banned = ["importlib", "__import__", "eval(", "exec("]
    for b in banned:
        assert b not in content


def test_no_authority_expansion_language_in_adapter():
    adapter_path = Path(__file__).parent.parent.parent / "pipeline" / "nervous_system" / "scout_adapters" / "sam_gov_assistance_listings.py"
    with open(adapter_path, "r", encoding="utf-8") as f:
        content = f.read().lower()
    banned = [
        "crawl", "scrape", "discover urls", "discover_url", "autonomous",
        "submit", "portal upload", "partner_alert", "outreach",
        "candidate_generation", "drafting", "all_model_access", "frontier_eligible"
    ]
    for b in banned:
        assert b not in content
