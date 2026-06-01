"""Build a Pennsylvania philanthropic-foundation candidate dataset.

The first pass deliberately stays on official IRS inputs:

* EO/BMF state extract for the Pennsylvania exempt-organization roster.
* TEOS Form 990 XML indexes for filing metadata and XML object IDs.

This module does not depend on pandas or network access. Downloading current
raw files is the CLI's job; parsing and normalization are deterministic here.
"""

from __future__ import annotations

import csv
import json
import math
import re
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree

_ZIP_DEFLATE64_DEPS = Path("/private/tmp/pa_zip_deps")
if _ZIP_DEFLATE64_DEPS.exists() and str(_ZIP_DEFLATE64_DEPS) not in sys.path:
    sys.path.insert(0, str(_ZIP_DEFLATE64_DEPS))

try:  # Adds ZIP method 9 support used by some recent IRS TEOS archives.
    import zipfile_deflate64  # noqa: F401
except ImportError:
    zipfile_deflate64 = None


FOUNDATION_NAME_TERMS = (
    "FOUNDATION",
    " FUND",
    "TRUST",
    "ENDOWMENT",
    "CHARITABLE",
    "PHILANTHROP",
    "GIVING",
    "GRANT",
)

PRIVATE_FOUNDATION_CODES = {"02", "03", "04"}
GRANTMAKING_NTEE_PREFIXES = ("T",)
MIN_ASSET_AMOUNT = 500_000
PRIORITY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "animals": ("ANIMAL", "SHELTER", "RESCUE", "VETERINARY", "SPCA", "HUMANE"),
    "arts_culture": ("ART", "ARTS", "CULTURE", "MUSEUM", "THEATER", "THEATRE", "MUSIC"),
    "cancer": ("CANCER", "ONCOLOGY", "TUMOR", "LEUKEMIA", "LYMPHOMA"),
    "community_services": ("COMMUNITY", "NEIGHBORHOOD", "UNITED WAY", "GENERAL SUPPORT"),
    "education": ("SCHOOL", "EDUCATION", "SCHOLARSHIP", "STUDENT", "UNIVERSITY", "COLLEGE", "ACADEMY"),
    "environment": ("ENVIRONMENT", "CONSERVATION", "WATER", "FOREST", "LAND", "NATURE"),
    "faith": ("CHURCH", "MINISTRY", "SYNAGOGUE", "PARISH", "RELIGIOUS", "FAITH"),
    "food_security": ("FOOD", "HUNGER", "MEAL", "PANTRY", "FOODBANK", "FOOD BANK"),
    "health": ("HEALTH", "HOSPITAL", "MEDICAL", "CLINIC", "DISEASE", "PATIENT"),
    "housing": ("HOUSING", "HOMELESS", "SHELTER", "HABITAT"),
    "human_services": ("HUMAN SERVICES", "FAMILY", "FAMILIES", "CHILDREN", "YOUTH", "SENIOR"),
    "public_safety": ("FIRE", "POLICE", "EMS", "AMBULANCE", "SAFETY"),
    "workforce": ("WORKFORCE", "JOB", "JOBS", "TRAINING", "EMPLOYMENT"),
}
STOPWORDS = {
    "AND",
    "FOR",
    "THE",
    "THIS",
    "THAT",
    "WITH",
    "FROM",
    "USE",
    "USES",
    "SUPPORT",
    "GENERAL",
    "UNRESTRICTED",
    "PURPOSES",
    "ORGANIZATION",
    "ORGANIZATIONS",
    "TAX",
    "EXEMPT",
    "CHARITABLE",
    "FOUNDATION",
    "FUND",
    "INC",
    "TRUST",
}
OUT_OF_SCOPE_TERMS = (
    "AFRICA",
    "BAPTIST",
    "BIBLE",
    "CATHOLIC",
    "CHRIST",
    "CHRISTIAN",
    "CHURCH",
    "CLERGY",
    "EPISCOPAL",
    "FAITH",
    "GOSPEL",
    "HINDU",
    "ISLAM",
    "ISLAMIC",
    "ISRAEL",
    "JEWISH",
    "JUDAIC",
    "JUDAISM",
    "MINISTRIES",
    "MINISTRY",
    "MISSIONARY",
    "MOSQUE",
    "MUSLIM",
    "PARISH",
    "PRESBYTERIAN",
    "RABBI",
    "RELIGION",
    "RELIGIOUS",
    "SYNAGOGUE",
    "TEMPLE",
    "TORAH",
    "YESHIVA",
    "ZION",
    "ZIONIST",
)
SCHOLARSHIP_TERMS = ("SCHOLARSHIP", "SCHOLARSHIPS")
FOREIGN_FOCUS_TERMS = (
    "AFRICA",
    "ISRAEL",
    "MISSIONARY",
    "ZION",
    "ZIONIST",
)


@dataclass(frozen=True)
class CandidateBuildResult:
    """Summary of a completed candidate build."""

    source_bmf_rows: int
    source_index_rows: int
    pa_501c3_rows: int
    candidate_rows: int
    linked_filing_rows: int
    output_ndjson: Path
    output_csv: Path
    output_summary: Path


@dataclass(frozen=True)
class GrantExtractionResult:
    """Summary of a completed grants extraction pass."""

    candidate_rows_read: int
    candidate_filings_selected: int
    xml_files_found: int
    grant_rows: int
    output_ndjson: Path
    output_csv: Path
    output_summary: Path


@dataclass(frozen=True)
class FunderPriorityResult:
    """Summary of a completed funder-priority aggregation pass."""

    grant_rows_read: int
    funder_year_rows: int
    output_ndjson: Path
    output_csv: Path
    output_summary: Path


@dataclass(frozen=True)
class RegenerativeShortlistResult:
    """Summary of a completed regenerative-fit shortlist pass."""

    funder_rows_read: int
    shortlist_rows: int
    output_ndjson: Path
    output_csv: Path
    output_summary: Path


def normalize_ein(value: str | None) -> str:
    digits = re.sub(r"\D", "", value or "")
    return digits.zfill(9) if digits else ""


def normalize_name(value: str | None) -> str:
    cleaned = re.sub(r"[^A-Z0-9 ]+", " ", (value or "").upper())
    return re.sub(r"\s+", " ", cleaned).strip()


def is_out_of_scope_text(value: str | None) -> bool:
    normalized = normalize_name(value)
    return any(term in normalized for term in OUT_OF_SCOPE_TERMS)


def is_scholarship_text(value: str | None) -> bool:
    normalized = normalize_name(value)
    return any(term in normalized for term in SCHOLARSHIP_TERMS)


def is_out_of_scope_funder_name(value: str | None) -> bool:
    normalized = normalize_name(value)
    religious = any(term in normalized for term in OUT_OF_SCOPE_TERMS if term not in FOREIGN_FOCUS_TERMS)
    foreign_focus = any(term in normalized for term in FOREIGN_FOCUS_TERMS)
    return religious or foreign_focus


def parse_int(value: str | None) -> int | None:
    if value is None:
        return None
    stripped = value.strip()
    if stripped == "":
        return None
    try:
        return int(stripped)
    except ValueError:
        return None


def parse_tax_period(value: str | None) -> int:
    parsed = parse_int(value)
    return parsed or 0


def classify_bmf_row(row: dict[str, str]) -> tuple[bool, list[str], int]:
    """Return candidate inclusion, reason list, and confidence score."""

    name = normalize_name(row.get("NAME"))
    ntee = (row.get("NTEE_CD") or "").upper().strip()
    foundation_code = (row.get("FOUNDATION") or "").zfill(2)
    pf_filing_req = (row.get("PF_FILING_REQ_CD") or "").strip()

    reasons: list[str] = []
    core_signal = False
    score = 0

    if foundation_code in PRIVATE_FOUNDATION_CODES or pf_filing_req == "1":
        reasons.append("private_foundation_indicator")
        core_signal = True
        score += 45

    if any(term in name for term in FOUNDATION_NAME_TERMS):
        reasons.append("grantmaker_name_term")
        core_signal = True
        score += 25

    if ntee.startswith(GRANTMAKING_NTEE_PREFIXES):
        reasons.append("grantmaking_ntee")
        core_signal = True
        score += 25

    asset_amount = parse_int(row.get("ASSET_AMT")) or 0
    revenue_amount = parse_int(row.get("REVENUE_AMT")) or parse_int(row.get("INCOME_AMT")) or 0
    if asset_amount >= 250_000:
        reasons.append("asset_floor_250k")
        score += 5
    if revenue_amount >= 100_000:
        reasons.append("revenue_floor_100k")
        score += 5

    return core_signal, reasons, min(score, 100)


def _read_latest_filings(index_paths: Iterable[Path]) -> tuple[dict[str, dict[str, str]], int]:
    latest_by_ein: dict[str, dict[str, str]] = {}
    rows_read = 0

    for index_path in index_paths:
        with index_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                rows_read += 1
                ein = normalize_ein(row.get("EIN"))
                if not ein:
                    continue
                current_period = parse_tax_period(row.get("TAX_PERIOD"))
                prior = latest_by_ein.get(ein)
                if prior is None or current_period > parse_tax_period(prior.get("TAX_PERIOD")):
                    latest_by_ein[ein] = row

    return latest_by_ein, rows_read


def _address_from_bmf(row: dict[str, str]) -> dict[str, str]:
    return {
        "care_of": (row.get("ICO") or "").strip(),
        "street": (row.get("STREET") or "").strip(),
        "city": (row.get("CITY") or "").strip(),
        "state": (row.get("STATE") or "").strip(),
        "zip": (row.get("ZIP") or "").strip(),
    }


def _candidate_record(
    row: dict[str, str],
    filing: dict[str, str] | None,
    reasons: list[str],
    score: int,
) -> dict[str, object]:
    ein = normalize_ein(row.get("EIN"))
    return {
        "ein": ein,
        "legal_name": (row.get("NAME") or "").strip(),
        "normalized_name": normalize_name(row.get("NAME")),
        "address": _address_from_bmf(row),
        "subsection": (row.get("SUBSECTION") or "").strip(),
        "deductibility_code": (row.get("DEDUCTIBILITY") or "").strip(),
        "foundation_code": (row.get("FOUNDATION") or "").strip(),
        "pf_filing_req_code": (row.get("PF_FILING_REQ_CD") or "").strip(),
        "ruling_yyyymm": (row.get("RULING") or "").strip(),
        "ntee_code": (row.get("NTEE_CD") or "").strip(),
        "tax_period_bmf": (row.get("TAX_PERIOD") or "").strip(),
        "asset_amount": parse_int(row.get("ASSET_AMT")),
        "income_amount": parse_int(row.get("INCOME_AMT")),
        "revenue_amount": parse_int(row.get("REVENUE_AMT")),
        "candidate_reasons": reasons,
        "candidate_confidence": score,
        "latest_filing": {
            "tax_period": (filing or {}).get("TAX_PERIOD", ""),
            "submission_year": (filing or {}).get("SUB_DATE", ""),
            "return_type": (filing or {}).get("RETURN_TYPE", ""),
            "object_id": (filing or {}).get("OBJECT_ID", ""),
            "xml_batch_id": (filing or {}).get("XML_BATCH_ID", ""),
            "taxpayer_name": (filing or {}).get("TAXPAYER_NAME", ""),
        },
        "source": {
            "bmf": "IRS EO/BMF Pennsylvania state extract",
            "filing_index": "IRS TEOS Form 990 XML index" if filing else "",
        },
    }


def build_pa_foundation_candidates(
    *,
    bmf_csv: Path,
    teos_index_csvs: Iterable[Path],
    output_dir: Path,
) -> CandidateBuildResult:
    """Build PA 501(c)(3) grantmaker candidates from local IRS CSV inputs."""

    output_dir.mkdir(parents=True, exist_ok=True)
    index_paths = [Path(path) for path in teos_index_csvs]
    latest_filings, index_rows = _read_latest_filings(index_paths)

    bmf_rows = 0
    pa_501c3_rows = 0
    candidates: list[dict[str, object]] = []

    with bmf_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            bmf_rows += 1
            if (row.get("STATE") or "").upper() != "PA":
                continue
            if (row.get("SUBSECTION") or "").zfill(2) != "03":
                continue
            if (row.get("STATUS") or "").zfill(2) != "01":
                continue
            pa_501c3_rows += 1
            if (parse_int(row.get("ASSET_AMT")) or 0) < MIN_ASSET_AMOUNT:
                continue
            funder_name = row.get("NAME")
            if is_out_of_scope_funder_name(funder_name) and not is_scholarship_text(funder_name):
                continue

            include, reasons, score = classify_bmf_row(row)
            filing = latest_filings.get(normalize_ein(row.get("EIN")))
            if filing and (filing.get("RETURN_TYPE") or "").upper() == "990PF":
                include = True
                if "990pf_latest_return" not in reasons:
                    reasons.append("990pf_latest_return")
                score = min(score + 35, 100)

            if include:
                candidates.append(_candidate_record(row, filing, reasons, score))

    candidates.sort(
        key=lambda item: (
            -int(item["candidate_confidence"]),
            str(item["normalized_name"]),
            str(item["ein"]),
        )
    )

    ndjson_path = output_dir / "pa_foundation_candidates.ndjson"
    csv_path = output_dir / "pa_foundation_candidates.csv"
    summary_path = output_dir / "pa_foundation_summary.json"

    with ndjson_path.open("w", encoding="utf-8") as handle:
        for candidate in candidates:
            handle.write(json.dumps(candidate, sort_keys=True) + "\n")

    fieldnames = [
        "ein",
        "legal_name",
        "city",
        "zip",
        "ntee_code",
        "foundation_code",
        "pf_filing_req_code",
        "ruling_yyyymm",
        "asset_amount",
        "revenue_amount",
        "candidate_confidence",
        "candidate_reasons",
        "latest_return_type",
        "latest_tax_period",
        "latest_object_id",
        "latest_xml_batch_id",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for candidate in candidates:
            latest = candidate["latest_filing"]
            assert isinstance(latest, dict)
            address = candidate["address"]
            assert isinstance(address, dict)
            writer.writerow(
                {
                    "ein": candidate["ein"],
                    "legal_name": candidate["legal_name"],
                    "city": address.get("city", ""),
                    "zip": address.get("zip", ""),
                    "ntee_code": candidate["ntee_code"],
                    "foundation_code": candidate["foundation_code"],
                    "pf_filing_req_code": candidate["pf_filing_req_code"],
                    "ruling_yyyymm": candidate["ruling_yyyymm"],
                    "asset_amount": candidate["asset_amount"],
                    "revenue_amount": candidate["revenue_amount"],
                    "candidate_confidence": candidate["candidate_confidence"],
                    "candidate_reasons": "|".join(candidate["candidate_reasons"]),
                    "latest_return_type": latest.get("return_type", ""),
                    "latest_tax_period": latest.get("tax_period", ""),
                    "latest_object_id": latest.get("object_id", ""),
                    "latest_xml_batch_id": latest.get("xml_batch_id", ""),
                }
            )

    linked_rows = sum(1 for candidate in candidates if candidate["latest_filing"].get("object_id"))  # type: ignore[union-attr]
    summary = {
        "source_bmf_rows": bmf_rows,
        "source_index_rows": index_rows,
        "pa_501c3_rows": pa_501c3_rows,
        "candidate_rows": len(candidates),
        "linked_filing_rows": linked_rows,
        "outputs": {
            "ndjson": str(ndjson_path),
            "csv": str(csv_path),
        },
        "inclusion_rules": [
            "PA headquarters in IRS EO/BMF",
            "SUBSECTION == 03",
            "STATUS == 01",
            f"ASSET_AMT >= {MIN_ASSET_AMOUNT}",
            "private foundation indicator, 990-PF latest return, grantmaker name term, or grantmaking NTEE",
        ],
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return CandidateBuildResult(
        source_bmf_rows=bmf_rows,
        source_index_rows=index_rows,
        pa_501c3_rows=pa_501c3_rows,
        candidate_rows=len(candidates),
        linked_filing_rows=linked_rows,
        output_ndjson=ndjson_path,
        output_csv=csv_path,
        output_summary=summary_path,
    )


def _strip_ns(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _first_text(parent: ElementTree.Element, names: Iterable[str]) -> str:
    wanted = set(names)
    for element in parent.iter():
        if _strip_ns(element.tag) in wanted and element.text:
            return element.text.strip()
    return ""


def _business_name(parent: ElementTree.Element, container_name: str) -> str:
    for element in parent.iter():
        if _strip_ns(element.tag) != container_name:
            continue
        lines = [
            _first_text(element, ("BusinessNameLine1Txt",)),
            _first_text(element, ("BusinessNameLine2Txt",)),
        ]
        return " ".join(line for line in lines if line).strip()
    return ""


def _us_address(parent: ElementTree.Element, container_name: str) -> dict[str, str]:
    for element in parent.iter():
        if _strip_ns(element.tag) != container_name:
            continue
        return {
            "street": _first_text(element, ("AddressLine1Txt",)),
            "street2": _first_text(element, ("AddressLine2Txt",)),
            "city": _first_text(element, ("CityNm",)),
            "state": _first_text(element, ("StateAbbreviationCd",)),
            "zip": _first_text(element, ("ZIPCd",)),
        }
    return {"street": "", "street2": "", "city": "", "state": "", "zip": ""}


def extract_pf_grants_from_xml(xml_bytes: bytes, *, object_id: str, xml_batch_id: str) -> list[dict[str, object]]:
    """Extract itemized grants from one IRS XML return.

    Covers 990-PF grants paid during the year and Form 990 Schedule I recipient
    rows. The function name is retained for backward compatibility with the
    first 990-PF-only pass.
    """

    root = ElementTree.fromstring(xml_bytes)
    funder_ein = _first_text(root, ("EIN",))
    funder_name = _business_name(root, "BusinessName")
    tax_year = _first_text(root, ("TaxYr",))
    tax_period_end = _first_text(root, ("TaxPeriodEndDt",))
    return_type = _first_text(root, ("ReturnTypeCd",))

    grants: list[dict[str, object]] = []
    for element in root.iter():
        if _strip_ns(element.tag) != "GrantOrContributionPdDurYrGrp":
            continue
        amount = parse_int(_first_text(element, ("Amt",)))
        recipient_name = _business_name(element, "RecipientBusinessName")
        purpose = _first_text(element, ("GrantOrContributionPurposeTxt",))
        if amount is None and not recipient_name and not purpose:
            continue
        grants.append(
            {
                "foundation_ein": normalize_ein(funder_ein),
                "foundation_name": funder_name,
                "tax_year": tax_year,
                "tax_period_end": tax_period_end,
                "return_type": return_type,
                "object_id": object_id,
                "xml_batch_id": xml_batch_id,
                "recipient_name": recipient_name,
                "recipient_ein": "",
                "recipient_address": _us_address(element, "RecipientUSAddress"),
                "amount": amount,
                "purpose": purpose,
                "recipient_relationship": _first_text(element, ("RecipientRelationshipTxt",)),
                "recipient_foundation_status": _first_text(element, ("RecipientFoundationStatusTxt",)),
                "source_schedule": "IRS990PF.GrantOrContributionPdDurYrGrp",
                "confidence": "high_xml_direct",
            }
        )

    for element in root.iter():
        if _strip_ns(element.tag) != "RecipientTable":
            continue
        cash_amount = parse_int(_first_text(element, ("CashGrantAmt",)))
        noncash_amount = parse_int(_first_text(element, ("NonCashAssistanceAmt",))) or 0
        amount = cash_amount if cash_amount is not None else noncash_amount
        recipient_name = _business_name(element, "RecipientBusinessName")
        purpose = _first_text(element, ("PurposeOfGrantTxt",))
        if amount is None and not recipient_name and not purpose:
            continue
        grants.append(
            {
                "foundation_ein": normalize_ein(funder_ein),
                "foundation_name": funder_name,
                "tax_year": tax_year,
                "tax_period_end": tax_period_end,
                "return_type": return_type,
                "object_id": object_id,
                "xml_batch_id": xml_batch_id,
                "recipient_name": recipient_name,
                "recipient_ein": normalize_ein(_first_text(element, ("RecipientEIN",))),
                "recipient_address": _us_address(element, "RecipientUSAddress"),
                "amount": amount,
                "purpose": purpose,
                "recipient_relationship": "",
                "recipient_foundation_status": _first_text(element, ("IRCSectionDesc",)),
                "source_schedule": "IRS990ScheduleI.RecipientTable",
                "confidence": "high_xml_direct",
            }
        )
    return grants


def extract_pf_grants_from_zip(
    *,
    candidates_csv: Path,
    teos_zip: Path,
    xml_batch_id: str,
    output_dir: Path,
    limit_filings: int | None = None,
) -> GrantExtractionResult:
    """Extract itemized grant rows for candidate filings present in one TEOS zip."""

    output_dir.mkdir(parents=True, exist_ok=True)
    selected: dict[str, dict[str, str]] = {}
    candidate_rows_read = 0
    with candidates_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            candidate_rows_read += 1
            if row.get("latest_xml_batch_id") != xml_batch_id:
                continue
            if row.get("latest_return_type") not in {"990PF", "990"}:
                continue
            object_id = row.get("latest_object_id", "")
            if not object_id:
                continue
            selected[object_id] = row
            if limit_filings is not None and len(selected) >= limit_filings:
                break

    grants: list[dict[str, object]] = []
    xml_files_found = 0
    with zipfile.ZipFile(teos_zip) as archive:
        names = set(archive.namelist())
        for object_id in selected:
            member = f"{object_id}_public.xml"
            if member not in names:
                continue
            xml_files_found += 1
            grants.extend(
                extract_pf_grants_from_xml(
                    _read_zip_member_bytes(teos_zip, archive, member),
                    object_id=object_id,
                    xml_batch_id=xml_batch_id,
                )
            )

    ndjson_path = output_dir / f"{xml_batch_id.lower()}_pf_grants.ndjson"
    csv_path = output_dir / f"{xml_batch_id.lower()}_pf_grants.csv"
    summary_path = output_dir / f"{xml_batch_id.lower()}_pf_grants_summary.json"

    with ndjson_path.open("w", encoding="utf-8") as handle:
        for grant in grants:
            handle.write(json.dumps(grant, sort_keys=True) + "\n")

    fieldnames = [
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
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for grant in grants:
            address = grant["recipient_address"]
            assert isinstance(address, dict)
            writer.writerow(
                {
                    "foundation_ein": grant["foundation_ein"],
                    "foundation_name": grant["foundation_name"],
                    "tax_year": grant["tax_year"],
                    "tax_period_end": grant["tax_period_end"],
                    "object_id": grant["object_id"],
                    "recipient_name": grant["recipient_name"],
                    "recipient_city": address.get("city", ""),
                    "recipient_state": address.get("state", ""),
                    "recipient_zip": address.get("zip", ""),
                    "amount": grant["amount"],
                    "purpose": grant["purpose"],
                    "recipient_foundation_status": grant["recipient_foundation_status"],
                    "source_schedule": grant["source_schedule"],
                }
            )

    summary = {
        "candidate_rows_read": candidate_rows_read,
        "candidate_filings_selected": len(selected),
        "xml_files_found": xml_files_found,
        "grant_rows": len(grants),
        "xml_batch_id": xml_batch_id,
        "source_zip": str(teos_zip),
        "outputs": {
            "ndjson": str(ndjson_path),
            "csv": str(csv_path),
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return GrantExtractionResult(
        candidate_rows_read=candidate_rows_read,
        candidate_filings_selected=len(selected),
        xml_files_found=xml_files_found,
        grant_rows=len(grants),
        output_ndjson=ndjson_path,
        output_csv=csv_path,
        output_summary=summary_path,
    )


def _read_zip_member_bytes(teos_zip: Path, archive: zipfile.ZipFile, member: str) -> bytes:
    try:
        with archive.open(member) as handle:
            return handle.read()
    except NotImplementedError:
        completed = subprocess.run(
            ["unzip", "-p", str(teos_zip), member],
            check=True,
            capture_output=True,
        )
        return completed.stdout


def _category_hits(text: str) -> dict[str, int]:
    normalized = normalize_name(text)
    hits: dict[str, int] = {}
    for category, terms in PRIORITY_KEYWORDS.items():
        count = sum(1 for term in terms if term in normalized)
        if count:
            hits[category] = count
    return hits


def _keyword_tokens(text: str) -> list[str]:
    tokens = re.findall(r"[A-Z][A-Z0-9]{2,}", normalize_name(text))
    return [token for token in tokens if token not in STOPWORDS]


def _parse_count_pairs(value: str) -> dict[str, int]:
    pairs: dict[str, int] = {}
    for part in (value or "").split(";"):
        stripped = part.strip()
        if not stripped or ":" not in stripped:
            continue
        key, count = stripped.rsplit(":", 1)
        parsed = parse_int(count)
        if parsed is not None:
            pairs[key.strip()] = parsed
    return pairs


REGENERATIVE_CATEGORY_WEIGHTS = {
    "environment": 5,
    "food_security": 5,
    "arts_culture": 4,
    "community_services": 4,
    "workforce": 4,
    "housing": 4,
    "human_services": 3,
    "animals": 2,
    "education": 2,
    "health": 1,
}
GENERIC_PRIORITY_KEYWORDS = {"ATTACHED", "SEE", "STATEMENT", "SCHEDULE"}
DONOR_ADVISED_KEYWORDS = {"DAF", "DONOR", "DESIGNATED"}
MATCHING_GIFT_KEYWORDS = {"MATCHING", "GIFTS"}
INTERMEDIARY_NAME_TERMS = (
    "CHARITABLE GIVING",
    "FIDELITY CHARITABLE",
    "NATIONAL PHILANTHROPIC TRUST",
    "VANGUARD CHARITABLE",
)
PA_PLACE_KEYWORDS = {
    "ALLEGHENY",
    "HARRISBURG",
    "PENNSYLVANIA",
    "PHILADELPHIA",
    "PITTSBURGH",
    "SCRANTON",
}


def build_regenerative_shortlist(
    *,
    priorities_csv: Path,
    output_dir: Path,
    max_rows: int = 3000,
) -> RegenerativeShortlistResult:
    """Rank priority rows for regenerative PA project relevance."""

    output_dir.mkdir(parents=True, exist_ok=True)
    rows_read = 0
    records: list[dict[str, object]] = []

    with priorities_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows_read += 1
            categories = _parse_count_pairs(row.get("top_priority_categories", ""))
            keywords = _parse_count_pairs(row.get("top_priority_keywords", ""))
            if not categories:
                continue

            annual_total = parse_int(row.get("annual_grant_total")) or 0
            grant_count = parse_int(row.get("grant_count")) or 0
            foundation_name = row.get("foundation_name", "")
            normalized_funder_name = normalize_name(foundation_name)
            category_score = sum(
                min(count, 50) * REGENERATIVE_CATEGORY_WEIGHTS.get(category, 0)
                for category, count in categories.items()
            )
            keyword_set = set(keywords)
            generic_hits = GENERIC_PRIORITY_KEYWORDS & keyword_set
            donor_advised_hits = DONOR_ADVISED_KEYWORDS & keyword_set
            matching_gift_hits = MATCHING_GIFT_KEYWORDS & keyword_set
            intermediary_name_hit = any(
                term in normalized_funder_name for term in INTERMEDIARY_NAME_TERMS
            )
            score = round(
                category_score
                + math.log10(max(annual_total, 0) + 1) * 2
                + math.log10(max(grant_count, 0) + 1) * 2
                + (3 if PA_PLACE_KEYWORDS & keyword_set else 0)
                - (8 if generic_hits else 0)
                - (15 if donor_advised_hits or intermediary_name_hit else 0)
                - (10 if matching_gift_hits else 0),
                2,
            )

            flags: list[str] = []
            if generic_hits:
                flags.append("generic_priority_text")
            if donor_advised_hits:
                flags.append("donor_advised_or_designated_grants")
            if intermediary_name_hit:
                flags.append("donor_advised_or_intermediary_funder")
            if matching_gift_hits:
                flags.append("matching_gift_program")
            if set(categories) <= {"health", "cancer"}:
                flags.append("health_only_or_cancer_only")

            if score >= 80:
                tier = "high"
            elif score >= 35:
                tier = "medium"
            else:
                tier = "low"

            regenerative_categories = {
                category: count
                for category, count in categories.items()
                if category in REGENERATIVE_CATEGORY_WEIGHTS
            }
            records.append(
                {
                    "foundation_ein": normalize_ein(row.get("foundation_ein")),
                    "foundation_name": foundation_name,
                    "tax_year": row.get("tax_year", ""),
                    "annual_grant_total": annual_total,
                    "grant_count": grant_count,
                    "regenerative_fit_score": score,
                    "fit_tier": tier,
                    "confidence": "high" if grant_count >= 5 and not generic_hits else "review",
                    "review_flags": flags,
                    "regenerative_priority_categories": regenerative_categories,
                    "top_priority_categories": categories,
                    "top_priority_keywords": keywords,
                }
            )

    records.sort(
        key=lambda item: (
            -float(item["regenerative_fit_score"]),
            -int(item["annual_grant_total"]),
            str(item["foundation_name"]),
        )
    )
    records = records[:max_rows]

    ndjson_path = output_dir / "regenerative_funder_shortlist.ndjson"
    csv_path = output_dir / "regenerative_funder_shortlist.csv"
    summary_path = output_dir / "regenerative_funder_shortlist_summary.json"

    with ndjson_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "foundation_ein",
            "foundation_name",
            "tax_year",
            "annual_grant_total",
            "grant_count",
            "regenerative_fit_score",
            "fit_tier",
            "confidence",
            "review_flags",
            "regenerative_priority_categories",
            "top_priority_categories",
            "top_priority_keywords",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "foundation_ein": record["foundation_ein"],
                    "foundation_name": record["foundation_name"],
                    "tax_year": record["tax_year"],
                    "annual_grant_total": record["annual_grant_total"],
                    "grant_count": record["grant_count"],
                    "regenerative_fit_score": record["regenerative_fit_score"],
                    "fit_tier": record["fit_tier"],
                    "confidence": record["confidence"],
                    "review_flags": "; ".join(record["review_flags"]),  # type: ignore[arg-type]
                    "regenerative_priority_categories": "; ".join(
                        f"{category}:{count}"
                        for category, count in record[
                            "regenerative_priority_categories"
                        ].items()  # type: ignore[union-attr]
                    ),
                    "top_priority_categories": "; ".join(
                        f"{category}:{count}"
                        for category, count in record["top_priority_categories"].items()  # type: ignore[union-attr]
                    ),
                    "top_priority_keywords": "; ".join(
                        f"{keyword}:{count}"
                        for keyword, count in record["top_priority_keywords"].items()  # type: ignore[union-attr]
                    ),
                }
            )

    summary = {
        "funder_rows_read": rows_read,
        "shortlist_rows": len(records),
        "max_rows": max_rows,
        "source_priorities_csv": str(priorities_csv),
        "method": "Rank nonblank priority rows using weighted regenerative categories, annual giving, grant count, PA place keywords, and review penalties for generic or donor-advised signals.",
        "category_weights": REGENERATIVE_CATEGORY_WEIGHTS,
        "outputs": {"csv": str(csv_path), "ndjson": str(ndjson_path)},
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return RegenerativeShortlistResult(
        funder_rows_read=rows_read,
        shortlist_rows=len(records),
        output_ndjson=ndjson_path,
        output_csv=csv_path,
        output_summary=summary_path,
    )


def aggregate_funder_priorities(
    *,
    grants_csv: Path,
    output_dir: Path,
    top_n: int = 8,
) -> FunderPriorityResult:
    """Aggregate annual giving and priority signals from extracted grant rows."""

    output_dir.mkdir(parents=True, exist_ok=True)
    grouped: dict[tuple[str, str], dict[str, object]] = {}
    excluded_funder_keys: set[tuple[str, str]] = set()
    excluded_scholarship_funder_keys: set[tuple[str, str]] = set()
    excluded_grant_count = 0
    excluded_grant_amount = 0
    rows_read = 0

    with grants_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows_read += 1
            ein = normalize_ein(row.get("foundation_ein"))
            year = (row.get("tax_year") or "").strip()
            key = (ein, year)
            amount = parse_int(row.get("amount")) or 0
            if is_out_of_scope_funder_name(row.get("foundation_name")):
                excluded_funder_keys.add(key)
                excluded_grant_count += 1
                excluded_grant_amount += amount
                continue
            if is_scholarship_text(row.get("foundation_name")):
                excluded_scholarship_funder_keys.add(key)
                excluded_grant_count += 1
                excluded_grant_amount += amount
                continue

            grant_scope_text = " ".join(
                part
                for part in (
                    row.get("purpose") or "",
                    row.get("recipient_name") or "",
                )
                if part
            )
            if is_out_of_scope_text(grant_scope_text):
                excluded_grant_count += 1
                excluded_grant_amount += amount
                continue
            if is_scholarship_text(grant_scope_text):
                excluded_grant_count += 1
                excluded_grant_amount += amount
                continue

            bucket = grouped.setdefault(
                key,
                {
                    "foundation_ein": ein,
                    "foundation_name": row.get("foundation_name", ""),
                    "tax_year": year,
                    "annual_grant_total": 0,
                    "grant_count": 0,
                    "category_counts": {},
                    "keyword_counts": {},
                    "sample_grants": [],
                },
            )
            bucket["annual_grant_total"] = int(bucket["annual_grant_total"]) + amount
            bucket["grant_count"] = int(bucket["grant_count"]) + 1

            category_counts = bucket["category_counts"]
            assert isinstance(category_counts, dict)
            for category, count in _category_hits(grant_scope_text).items():
                category_counts[category] = int(category_counts.get(category, 0)) + count

            keyword_counts = bucket["keyword_counts"]
            assert isinstance(keyword_counts, dict)
            for token in _keyword_tokens(grant_scope_text):
                keyword_counts[token] = int(keyword_counts.get(token, 0)) + 1

            sample_grants = bucket["sample_grants"]
            assert isinstance(sample_grants, list)
            if len(sample_grants) < 5:
                sample_grants.append(
                    {
                        "recipient_name": row.get("recipient_name", ""),
                        "amount": amount,
                        "purpose": row.get("purpose", ""),
                    }
                )

    records: list[dict[str, object]] = []
    for bucket in grouped.values():
        category_counts = bucket.pop("category_counts")
        keyword_counts = bucket.pop("keyword_counts")
        assert isinstance(category_counts, dict)
        assert isinstance(keyword_counts, dict)
        top_categories = [
            {"category": category, "count": count}
            for category, count in sorted(
                category_counts.items(), key=lambda item: (-int(item[1]), str(item[0]))
            )[:top_n]
        ]
        top_keywords = [
            {"keyword": keyword, "count": count}
            for keyword, count in sorted(
                keyword_counts.items(), key=lambda item: (-int(item[1]), str(item[0]))
            )[:top_n]
        ]
        record = dict(bucket)
        record["top_priority_categories"] = top_categories
        record["top_priority_keywords"] = top_keywords
        records.append(record)

    records.sort(
        key=lambda item: (
            -int(item["annual_grant_total"]),
            str(item["foundation_name"]),
            str(item["tax_year"]),
        )
    )

    ndjson_path = output_dir / "funder_priorities.ndjson"
    csv_path = output_dir / "funder_priorities.csv"
    summary_path = output_dir / "funder_priorities_summary.json"

    with ndjson_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "foundation_ein",
            "foundation_name",
            "tax_year",
            "annual_grant_total",
            "grant_count",
            "top_priority_categories",
            "top_priority_keywords",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "foundation_ein": record["foundation_ein"],
                    "foundation_name": record["foundation_name"],
                    "tax_year": record["tax_year"],
                    "annual_grant_total": record["annual_grant_total"],
                    "grant_count": record["grant_count"],
                    "top_priority_categories": "; ".join(
                        f"{item['category']}:{item['count']}"
                        for item in record["top_priority_categories"]  # type: ignore[index]
                    ),
                    "top_priority_keywords": "; ".join(
                        f"{item['keyword']}:{item['count']}"
                        for item in record["top_priority_keywords"]  # type: ignore[index]
                    ),
                }
            )

    summary = {
        "grant_rows_read": rows_read,
        "funder_year_rows": len(records),
        "source_grants_csv": str(grants_csv),
        "outputs": {
            "ndjson": str(ndjson_path),
            "csv": str(csv_path),
        },
        "excluded_funder_year_rows": len(excluded_funder_keys),
        "excluded_scholarship_funder_year_rows": len(excluded_scholarship_funder_keys),
        "excluded_grant_rows": excluded_grant_count,
        "excluded_grant_amount": excluded_grant_amount,
        "excluded_terms": list(OUT_OF_SCOPE_TERMS),
        "excluded_scholarship_terms": list(SCHOLARSHIP_TERMS),
        "priority_method": "Keyword/category counts from in-scope grant purpose text plus recipient name. Annual giving is sum(amount) by foundation EIN and tax year for in-scope extracted grant rows; mixed funders remain listed when they have in-scope grants.",
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return FunderPriorityResult(
        grant_rows_read=rows_read,
        funder_year_rows=len(records),
        output_ndjson=ndjson_path,
        output_csv=csv_path,
        output_summary=summary_path,
    )
