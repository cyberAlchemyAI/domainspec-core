from __future__ import annotations

import csv
import json
import zipfile
from pathlib import Path

from pipeline.funder_corpus.pa_foundations import (
    aggregate_funder_priorities,
    build_regenerative_shortlist,
    build_pa_foundation_candidates,
    extract_pf_grants_from_xml,
    extract_pf_grants_from_zip,
    is_out_of_scope_text,
    is_scholarship_text,
    normalize_ein,
    normalize_name,
)


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_normalize_ein_strips_punctuation_and_pads() -> None:
    assert normalize_ein("12-3456789") == "123456789"
    assert normalize_ein("123") == "000000123"


def test_normalize_name_removes_punctuation_and_collapses_spaces() -> None:
    assert normalize_name("The A.B. Foundation, Inc.") == "THE A B FOUNDATION INC"


def test_out_of_scope_terms_match_religious_ethnic_and_international_focus() -> None:
    assert is_out_of_scope_text("Example Jewish Community Foundation")
    assert is_out_of_scope_text("Christian Mission to Africa")
    assert is_out_of_scope_text("Friends of Israel Fund")
    assert is_out_of_scope_text("Religion and faith education")
    assert is_scholarship_text("Regional Scholarship Fund")
    assert not is_out_of_scope_text("Regional Scholarship Fund")
    assert not is_out_of_scope_text("Western Pennsylvania Food Fund")


def test_build_candidates_filters_and_links_latest_filing(tmp_path: Path) -> None:
    bmf_path = tmp_path / "eo_pa.csv"
    index_path = tmp_path / "index.csv"
    output_dir = tmp_path / "out"

    bmf_fields = [
        "EIN",
        "NAME",
        "ICO",
        "STREET",
        "CITY",
        "STATE",
        "ZIP",
        "SUBSECTION",
        "DEDUCTIBILITY",
        "FOUNDATION",
        "RULING",
        "STATUS",
        "TAX_PERIOD",
        "ASSET_AMT",
        "INCOME_AMT",
        "REVENUE_AMT",
        "NTEE_CD",
        "PF_FILING_REQ_CD",
    ]
    _write_csv(
        bmf_path,
        bmf_fields,
        [
            {
                "EIN": "111111111",
                "NAME": "Example Family Foundation",
                "ICO": "",
                "STREET": "1 Main",
                "CITY": "Pittsburgh",
                "STATE": "PA",
                "ZIP": "15222",
                "SUBSECTION": "03",
                "DEDUCTIBILITY": "1",
                "FOUNDATION": "04",
                "RULING": "199901",
                "STATUS": "01",
                "TAX_PERIOD": "202412",
                "ASSET_AMT": "1000000",
                "INCOME_AMT": "100000",
                "REVENUE_AMT": "90000",
                "NTEE_CD": "T20",
                "PF_FILING_REQ_CD": "1",
            },
            {
                "EIN": "222222222",
                "NAME": "Service Charity",
                "ICO": "",
                "STREET": "2 Main",
                "CITY": "Erie",
                "STATE": "PA",
                "ZIP": "16501",
                "SUBSECTION": "03",
                "DEDUCTIBILITY": "1",
                "FOUNDATION": "15",
                "RULING": "200101",
                "STATUS": "01",
                "TAX_PERIOD": "202412",
                "ASSET_AMT": "10000",
                "INCOME_AMT": "1000",
                "REVENUE_AMT": "1000",
                "NTEE_CD": "P20",
                "PF_FILING_REQ_CD": "0",
            },
            {
                "EIN": "333333333",
                "NAME": "New York Foundation",
                "ICO": "",
                "STREET": "3 Main",
                "CITY": "New York",
                "STATE": "NY",
                "ZIP": "10001",
                "SUBSECTION": "03",
                "DEDUCTIBILITY": "1",
                "FOUNDATION": "04",
                "RULING": "199901",
                "STATUS": "01",
                "TAX_PERIOD": "202412",
                "ASSET_AMT": "1000000",
                "INCOME_AMT": "100000",
                "REVENUE_AMT": "100000",
                "NTEE_CD": "T20",
                "PF_FILING_REQ_CD": "1",
            },
            {
                "EIN": "444444444",
                "NAME": "Example Christian Foundation",
                "ICO": "",
                "STREET": "4 Main",
                "CITY": "Pittsburgh",
                "STATE": "PA",
                "ZIP": "15222",
                "SUBSECTION": "03",
                "DEDUCTIBILITY": "1",
                "FOUNDATION": "04",
                "RULING": "199901",
                "STATUS": "01",
                "TAX_PERIOD": "202412",
                "ASSET_AMT": "1000000",
                "INCOME_AMT": "100000",
                "REVENUE_AMT": "100000",
                "NTEE_CD": "T20",
                "PF_FILING_REQ_CD": "1",
            },
            {
                "EIN": "555555555",
                "NAME": "Tiny Family Foundation",
                "ICO": "",
                "STREET": "5 Main",
                "CITY": "Pittsburgh",
                "STATE": "PA",
                "ZIP": "15222",
                "SUBSECTION": "03",
                "DEDUCTIBILITY": "1",
                "FOUNDATION": "04",
                "RULING": "199901",
                "STATUS": "01",
                "TAX_PERIOD": "202412",
                "ASSET_AMT": "499999",
                "INCOME_AMT": "100000",
                "REVENUE_AMT": "100000",
                "NTEE_CD": "T20",
                "PF_FILING_REQ_CD": "1",
            },
            {
                "EIN": "666666666",
                "NAME": "Regional Scholarship Fund",
                "ICO": "",
                "STREET": "6 Main",
                "CITY": "Pittsburgh",
                "STATE": "PA",
                "ZIP": "15222",
                "SUBSECTION": "03",
                "DEDUCTIBILITY": "1",
                "FOUNDATION": "04",
                "RULING": "199901",
                "STATUS": "01",
                "TAX_PERIOD": "202412",
                "ASSET_AMT": "1000000",
                "INCOME_AMT": "100000",
                "REVENUE_AMT": "100000",
                "NTEE_CD": "B82",
                "PF_FILING_REQ_CD": "1",
            },
        ],
    )
    _write_csv(
        index_path,
        [
            "RETURN_ID",
            "FILING_TYPE",
            "EIN",
            "TAX_PERIOD",
            "SUB_DATE",
            "TAXPAYER_NAME",
            "RETURN_TYPE",
            "DLN",
            "OBJECT_ID",
            "XML_BATCH_ID",
        ],
        [
            {
                "RETURN_ID": "1",
                "FILING_TYPE": "EFILE",
                "EIN": "111111111",
                "TAX_PERIOD": "202312",
                "SUB_DATE": "2025",
                "TAXPAYER_NAME": "Old Name",
                "RETURN_TYPE": "990PF",
                "DLN": "1",
                "OBJECT_ID": "old",
                "XML_BATCH_ID": "old_batch",
            },
            {
                "RETURN_ID": "2",
                "FILING_TYPE": "EFILE",
                "EIN": "111111111",
                "TAX_PERIOD": "202412",
                "SUB_DATE": "2026",
                "TAXPAYER_NAME": "Example Family Foundation",
                "RETURN_TYPE": "990PF",
                "DLN": "2",
                "OBJECT_ID": "new",
                "XML_BATCH_ID": "new_batch",
            },
        ],
    )

    result = build_pa_foundation_candidates(
        bmf_csv=bmf_path,
        teos_index_csvs=[index_path],
        output_dir=output_dir,
    )

    assert result.source_bmf_rows == 6
    assert result.source_index_rows == 2
    assert result.pa_501c3_rows == 5
    assert result.candidate_rows == 2
    assert result.linked_filing_rows == 1

    records = [
        json.loads(line)
        for line in result.output_ndjson.read_text(encoding="utf-8").splitlines()
    ]
    records_by_ein = {record["ein"]: record for record in records}
    assert records_by_ein["111111111"]["latest_filing"]["object_id"] == "new"
    assert "private_foundation_indicator" in records_by_ein["111111111"]["candidate_reasons"]
    assert "666666666" in records_by_ein


def test_extract_pf_grants_from_xml_reads_grants_paid_group() -> None:
    xml = b"""<?xml version="1.0"?>
    <Return xmlns="http://www.irs.gov/efile">
      <ReturnHeader>
        <TaxPeriodEndDt>2024-12-31</TaxPeriodEndDt>
        <ReturnTypeCd>990PF</ReturnTypeCd>
        <Filer>
          <EIN>111111111</EIN>
          <BusinessName><BusinessNameLine1Txt>Example Foundation</BusinessNameLine1Txt></BusinessName>
        </Filer>
        <TaxYr>2024</TaxYr>
      </ReturnHeader>
      <ReturnData>
        <IRS990PF>
          <GrantOrContributionPdDurYrGrp>
            <RecipientBusinessName>
              <BusinessNameLine1Txt>Recipient Charity</BusinessNameLine1Txt>
            </RecipientBusinessName>
            <RecipientUSAddress>
              <AddressLine1Txt>1 Charity Way</AddressLine1Txt>
              <CityNm>Pittsburgh</CityNm>
              <StateAbbreviationCd>PA</StateAbbreviationCd>
              <ZIPCd>15222</ZIPCd>
            </RecipientUSAddress>
            <RecipientRelationshipTxt>N/A</RecipientRelationshipTxt>
            <RecipientFoundationStatusTxt>PC</RecipientFoundationStatusTxt>
            <GrantOrContributionPurposeTxt>General support</GrantOrContributionPurposeTxt>
            <Amt>25000</Amt>
          </GrantOrContributionPdDurYrGrp>
        </IRS990PF>
      </ReturnData>
    </Return>
    """

    grants = extract_pf_grants_from_xml(xml, object_id="object1", xml_batch_id="batch1")

    assert len(grants) == 1
    assert grants[0]["foundation_ein"] == "111111111"
    assert grants[0]["recipient_name"] == "Recipient Charity"
    assert grants[0]["amount"] == 25000
    assert grants[0]["recipient_address"]["city"] == "Pittsburgh"


def test_extract_grants_from_xml_reads_form_990_schedule_i() -> None:
    xml = b"""<?xml version="1.0"?>
    <Return xmlns="http://www.irs.gov/efile">
      <ReturnHeader>
        <TaxPeriodEndDt>2024-12-31</TaxPeriodEndDt>
        <ReturnTypeCd>990</ReturnTypeCd>
        <Filer>
          <EIN>111111111</EIN>
          <BusinessName><BusinessNameLine1Txt>Example Foundation</BusinessNameLine1Txt></BusinessName>
        </Filer>
        <TaxYr>2024</TaxYr>
      </ReturnHeader>
      <ReturnData>
        <IRS990ScheduleI>
          <RecipientTable>
            <RecipientBusinessName>
              <BusinessNameLine1Txt>Recipient Charity</BusinessNameLine1Txt>
            </RecipientBusinessName>
            <RecipientUSAddress>
              <AddressLine1Txt>1 Charity Way</AddressLine1Txt>
              <CityNm>Pittsburgh</CityNm>
              <StateAbbreviationCd>PA</StateAbbreviationCd>
              <ZIPCd>15222</ZIPCd>
            </RecipientUSAddress>
            <RecipientEIN>222222222</RecipientEIN>
            <CashGrantAmt>50000</CashGrantAmt>
            <PurposeOfGrantTxt>Program support</PurposeOfGrantTxt>
          </RecipientTable>
        </IRS990ScheduleI>
      </ReturnData>
    </Return>
    """

    grants = extract_pf_grants_from_xml(xml, object_id="object1", xml_batch_id="batch1")

    assert len(grants) == 1
    assert grants[0]["return_type"] == "990"
    assert grants[0]["recipient_ein"] == "222222222"
    assert grants[0]["amount"] == 50000
    assert grants[0]["source_schedule"] == "IRS990ScheduleI.RecipientTable"


def test_extract_pf_grants_from_zip_uses_candidate_object_ids(tmp_path: Path) -> None:
    candidates = tmp_path / "candidates.csv"
    _write_csv(
        candidates,
        ["latest_xml_batch_id", "latest_return_type", "latest_object_id"],
        [
            {
                "latest_xml_batch_id": "2026_TEOS_XML_03A",
                "latest_return_type": "990PF",
                "latest_object_id": "object1",
            }
        ],
    )
    archive_path = tmp_path / "returns.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr(
            "object1_public.xml",
            """<?xml version="1.0"?>
            <Return xmlns="http://www.irs.gov/efile">
              <ReturnHeader>
                <ReturnTypeCd>990PF</ReturnTypeCd>
                <Filer><EIN>111111111</EIN><BusinessName><BusinessNameLine1Txt>Example Foundation</BusinessNameLine1Txt></BusinessName></Filer>
                <TaxYr>2024</TaxYr>
              </ReturnHeader>
              <ReturnData><IRS990PF><GrantOrContributionPdDurYrGrp><RecipientBusinessName><BusinessNameLine1Txt>Recipient Charity</BusinessNameLine1Txt></RecipientBusinessName><GrantOrContributionPurposeTxt>Support</GrantOrContributionPurposeTxt><Amt>100</Amt></GrantOrContributionPdDurYrGrp></IRS990PF></ReturnData>
            </Return>
            """,
        )

    result = extract_pf_grants_from_zip(
        candidates_csv=candidates,
        teos_zip=archive_path,
        xml_batch_id="2026_TEOS_XML_03A",
        output_dir=tmp_path / "out",
    )

    assert result.candidate_filings_selected == 1
    assert result.xml_files_found == 1
    assert result.grant_rows == 1
    assert "Recipient Charity" in result.output_ndjson.read_text(encoding="utf-8")


def test_aggregate_funder_priorities_sums_annual_giving_and_keywords(tmp_path: Path) -> None:
    grants_csv = tmp_path / "grants.csv"
    _write_csv(
        grants_csv,
        [
            "foundation_ein",
            "foundation_name",
            "tax_year",
            "tax_period_end",
            "object_id",
            "recipient_name",
            "recipient_city",
            "recipient_state",
            "recipient_zip",
            "amount",
            "purpose",
            "recipient_foundation_status",
            "source_schedule",
        ],
        [
            {
                "foundation_ein": "111111111",
                "foundation_name": "Example Foundation",
                "tax_year": "2024",
                "tax_period_end": "2024-12-31",
                "object_id": "object1",
                "recipient_name": "City Food Bank",
                "recipient_city": "Pittsburgh",
                "recipient_state": "PA",
                "recipient_zip": "15222",
                "amount": "1000",
                "purpose": "Food pantry support",
                "recipient_foundation_status": "PC",
                "source_schedule": "IRS990PF.GrantOrContributionPdDurYrGrp",
            },
            {
                "foundation_ein": "111111111",
                "foundation_name": "Example Foundation",
                "tax_year": "2024",
                "tax_period_end": "2024-12-31",
                "object_id": "object1",
                "recipient_name": "Neighborhood School",
                "recipient_city": "Pittsburgh",
                "recipient_state": "PA",
                "recipient_zip": "15222",
                "amount": "2500",
                "purpose": "Student education program",
                "recipient_foundation_status": "PC",
                "source_schedule": "IRS990PF.GrantOrContributionPdDurYrGrp",
            },
            {
                "foundation_ein": "222222222",
                "foundation_name": "Example Religious Foundation",
                "tax_year": "2024",
                "tax_period_end": "2024-12-31",
                "object_id": "object2",
                "recipient_name": "Church School",
                "recipient_city": "Pittsburgh",
                "recipient_state": "PA",
                "recipient_zip": "15222",
                "amount": "5000",
                "purpose": "Christian education",
                "recipient_foundation_status": "PC",
                "source_schedule": "IRS990PF.GrantOrContributionPdDurYrGrp",
            },
            {
                "foundation_ein": "333333333",
                "foundation_name": "Mixed Community Foundation",
                "tax_year": "2024",
                "tax_period_end": "2024-12-31",
                "object_id": "object3",
                "recipient_name": "Neighborhood Church",
                "recipient_city": "Pittsburgh",
                "recipient_state": "PA",
                "recipient_zip": "15222",
                "amount": "500",
                "purpose": "Church repair",
                "recipient_foundation_status": "PC",
                "source_schedule": "IRS990PF.GrantOrContributionPdDurYrGrp",
            },
            {
                "foundation_ein": "333333333",
                "foundation_name": "Mixed Community Foundation",
                "tax_year": "2024",
                "tax_period_end": "2024-12-31",
                "object_id": "object3",
                "recipient_name": "Community Food Bank",
                "recipient_city": "Pittsburgh",
                "recipient_state": "PA",
                "recipient_zip": "15222",
                "amount": "1200",
                "purpose": "Food access program",
                "recipient_foundation_status": "PC",
                "source_schedule": "IRS990PF.GrantOrContributionPdDurYrGrp",
            },
            {
                "foundation_ein": "333333333",
                "foundation_name": "Mixed Community Foundation",
                "tax_year": "2024",
                "tax_period_end": "2024-12-31",
                "object_id": "object3",
                "recipient_name": "County Scholarship Program",
                "recipient_city": "Pittsburgh",
                "recipient_state": "PA",
                "recipient_zip": "15222",
                "amount": "800",
                "purpose": "Scholarships",
                "recipient_foundation_status": "PC",
                "source_schedule": "IRS990PF.GrantOrContributionPdDurYrGrp",
            },
            {
                "foundation_ein": "444444444",
                "foundation_name": "Named Scholarship Fund",
                "tax_year": "2024",
                "tax_period_end": "2024-12-31",
                "object_id": "object4",
                "recipient_name": "Neighborhood School",
                "recipient_city": "Pittsburgh",
                "recipient_state": "PA",
                "recipient_zip": "15222",
                "amount": "1500",
                "purpose": "Operating support",
                "recipient_foundation_status": "PC",
                "source_schedule": "IRS990PF.GrantOrContributionPdDurYrGrp",
            },
        ],
    )

    result = aggregate_funder_priorities(
        grants_csv=grants_csv,
        output_dir=tmp_path / "out",
        top_n=3,
    )

    assert result.grant_rows_read == 7
    assert result.funder_year_rows == 2
    rows = [json.loads(line) for line in result.output_ndjson.read_text(encoding="utf-8").splitlines()]
    by_name = {row["foundation_name"]: row for row in rows}
    assert by_name["Example Foundation"]["annual_grant_total"] == 3500
    assert by_name["Example Foundation"]["grant_count"] == 2
    categories = {item["category"] for item in by_name["Example Foundation"]["top_priority_categories"]}
    assert {"food_security", "education"} <= categories
    output_text = result.output_ndjson.read_text(encoding="utf-8")
    assert "Example Religious Foundation" not in output_text
    assert "County Scholarship Program" not in output_text
    assert "Named Scholarship Fund" not in output_text
    assert by_name["Mixed Community Foundation"]["annual_grant_total"] == 1200
    assert by_name["Mixed Community Foundation"]["grant_count"] == 1
    summary = json.loads(result.output_summary.read_text(encoding="utf-8"))
    assert summary["excluded_scholarship_funder_year_rows"] == 1


def test_build_regenerative_shortlist_ranks_nonblank_priorities(tmp_path: Path) -> None:
    priorities_csv = tmp_path / "funder_priorities.csv"
    _write_csv(
        priorities_csv,
        [
            "foundation_ein",
            "foundation_name",
            "tax_year",
            "annual_grant_total",
            "grant_count",
            "top_priority_categories",
            "top_priority_keywords",
        ],
        [
            {
                "foundation_ein": "111111111",
                "foundation_name": "Land Food Arts Foundation",
                "tax_year": "2024",
                "annual_grant_total": "100000",
                "grant_count": "20",
                "top_priority_categories": "environment:8; food_security:5; arts_culture:3",
                "top_priority_keywords": "PITTSBURGH:5; FOOD:4; LAND:3",
            },
            {
                "foundation_ein": "222222222",
                "foundation_name": "Generic Attached Foundation",
                "tax_year": "2024",
                "annual_grant_total": "900000",
                "grant_count": "1",
                "top_priority_categories": "",
                "top_priority_keywords": "SEE:1; ATTACHED:1",
            },
            {
                "foundation_ein": "333333333",
                "foundation_name": "Health Only Foundation",
                "tax_year": "2024",
                "annual_grant_total": "500000",
                "grant_count": "10",
                "top_priority_categories": "health:10",
                "top_priority_keywords": "HOSPITAL:10",
            },
        ],
    )

    result = build_regenerative_shortlist(
        priorities_csv=priorities_csv,
        output_dir=tmp_path / "out",
        max_rows=10,
    )

    assert result.funder_rows_read == 3
    assert result.shortlist_rows == 2
    rows = [json.loads(line) for line in result.output_ndjson.read_text(encoding="utf-8").splitlines()]
    assert rows[0]["foundation_name"] == "Land Food Arts Foundation"
    assert rows[0]["fit_tier"] in {"medium", "high"}
    assert "generic_priority_text" not in rows[0]["review_flags"]
    assert rows[1]["review_flags"] == ["health_only_or_cancer_only"]
