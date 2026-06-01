import csv
import hashlib
import io
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

class SamGovParseError(ValueError):
    pass

@dataclass(frozen=True, kw_only=True)
class SamGovRawRow:
    import_id: str
    applied_as_entity_id: Optional[str]
    source_provenance_id: str
    raw_data: dict[str, str]
    imported_at_utc: str

@dataclass(frozen=True, kw_only=True)
class SamGovAssistanceListingRecord:
    listing_id: str
    raw_import_id: str
    assistance_listing_number: str
    program_title: str
    agency: str
    agency_code: str
    subagency: Optional[str]
    assistance_type: Optional[str]
    objectives: Optional[str]
    eligible_applicants: Optional[str]
    beneficiaries: Optional[str]
    use_restrictions: Optional[str]
    application_procedures: Optional[str]
    award_floor: Optional[int]
    award_ceiling: Optional[int]
    last_updated_date: Optional[str]
    url: Optional[str]

@dataclass(frozen=True, kw_only=True)
class SamGovProvenanceRecord:
    source_id: str
    applied_as_entity_id: Optional[str]
    source_system: str
    source_filename: str
    row_number: int
    column_names_used: tuple[str, ...]
    source_hash: str
    imported_at_utc: str
    parser_version: str
    source_record_id: Optional[str] = None

@dataclass(frozen=True, kw_only=True)
class SamGovParseResult:
    raw_rows: tuple[SamGovRawRow, ...]
    listings: tuple[SamGovAssistanceListingRecord, ...]
    provenance_records: tuple[SamGovProvenanceRecord, ...]

def _normalize_header(raw_header: str) -> str:
    s = str(raw_header)
    if s.startswith("\ufeff"):
        s = s[1:]
    s = s.strip().lower()
    s = s.replace("\n", " ").replace("\r", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def _normalize_identity_part(raw_value: object) -> str:
    if raw_value is None:
        return ""
    s = str(raw_value).strip().lower()
    s = s.replace("\n", " ").replace("\r", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def _is_blank_row(row: dict[str, object]) -> bool:
    for val in row.values():
        if val is not None and str(val).strip() != "":
            return False
    return True

def _deterministic_id(prefix: str, *parts: object) -> str:
    hasher = hashlib.sha3_256()
    raw = "|".join(str(p) for p in parts)
    hasher.update(raw.encode("utf-8"))
    return f"{prefix}{hasher.hexdigest()[:16]}"

def _first_present(row: dict[str, str], aliases: set[str]) -> Optional[str]:
    for header, val in row.items():
        if val is None or val.strip() == "":
            continue
        if _normalize_header(header) in aliases:
            return val
    return None

def _parse_int_or_none(val: Optional[str]) -> Optional[int]:
    if not val:
        return None
    cleaned = re.sub(r"[^\d-]", "", val)
    if not cleaned:
        return None
    try:
        return int(cleaned)
    except ValueError:
        return None

def parse_sam_gov_csv_text(
    csv_text: str,
    *,
    source_filename: str,
    imported_at_utc: str,
    applied_as_entity_id: Optional[str] = None,
    parser_version: str = "sam_gov_adapter_v1",
) -> SamGovParseResult:

    if not source_filename or not source_filename.strip():
        raise SamGovParseError("source_filename cannot be blank.")

    # We allow applied_as_entity_id to be blank since it's a reference record
    if applied_as_entity_id is not None and not applied_as_entity_id.strip():
        raise SamGovParseError("applied_as_entity_id cannot be empty string if provided.")

    hasher = hashlib.sha3_256()
    hasher.update(csv_text.encode("utf-8"))
    source_hash = hasher.hexdigest()

    f = io.StringIO(csv_text)
    try:
        reader = csv.DictReader(f, strict=True)
        if reader.fieldnames is None:
            f.seek(0)
            if f.read().strip():
                raise SamGovParseError("Malformed CSV: No fieldnames but file is not empty.")
            rows = []
        else:
            norm_headers = []
            for h in reader.fieldnames:
                if h is None or str(h).strip() == "":
                    raise SamGovParseError("Malformed CSV: Blank or None fieldname found.")
                nh = _normalize_header(h)
                if nh in norm_headers:
                    raise SamGovParseError(f"Malformed CSV: Duplicate normalized header '{nh}'.")
                norm_headers.append(nh)

            rows = []
            for r in reader:
                if None in r:
                    raise SamGovParseError("Malformed CSV: Row has more columns than headers.")
                rows.append(r)
    except csv.Error as e:
        raise SamGovParseError(f"Malformed CSV: {e}")
    except SamGovParseError:
        raise
    except Exception as e:
        raise SamGovParseError(f"Malformed CSV: {e}")

    raw_rows = []
    listings = []
    provenance_records = []

    aln_aliases = {"assistance listing number", "cfda number", "listing number", "assistance listing"}
    title_aliases = {"program title", "title", "assistance listing title"}
    agency_aliases = {"agency", "department/agency", "federal agency"}
    agency_code_aliases = {"agency code", "department code", "federal agency code"}
    subagency_aliases = {"subagency", "sub-agency", "office", "bureau", "sub-tier"}
    type_aliases = {"assistance type", "type of assistance"}
    obj_aliases = {"objectives", "program objectives", "description"}
    elig_aliases = {"eligible applicants", "applicant eligibility", "eligibility"}
    benef_aliases = {"beneficiaries", "beneficiary eligibility"}
    rest_aliases = {"use restrictions", "restrictions"}
    proc_aliases = {"application procedures", "application process"}
    floor_aliases = {"award floor", "minimum award"}
    ceiling_aliases = {"award ceiling", "maximum award"}
    date_aliases = {"last updated date", "updated date", "last modified date"}
    url_aliases = {"url", "program url", "assistance listing url"}

    for idx, row in enumerate(rows, start=2):
        if _is_blank_row(row):
            continue

        aln = _first_present(row, aln_aliases)
        title = _first_present(row, title_aliases)
        agency = _first_present(row, agency_aliases)
        agency_code = _first_present(row, agency_code_aliases)

        if not aln:
            raise SamGovParseError(f"Missing assistance_listing_number on row {idx}")
        if not title:
            raise SamGovParseError(f"Missing program_title on row {idx}")
        if not agency:
            raise SamGovParseError(f"Missing agency on row {idx}")
        if not agency_code:
            raise SamGovParseError(f"Missing agency_code on row {idx}")

        norm_agency_code = _normalize_identity_part(agency_code)
        norm_program_title = _normalize_identity_part(title)

        listing_id = _deterministic_id(
            "ALN-", aln, norm_agency_code, norm_program_title
        )

        import_id = _deterministic_id(
            "IMP-", applied_as_entity_id or "", source_hash, "csv", idx
        )
        source_id = _deterministic_id(
            "SRC-", applied_as_entity_id or "", source_hash, "csv", idx
        )

        raw_rows.append(
            SamGovRawRow(
                import_id=import_id,
                applied_as_entity_id=applied_as_entity_id,
                source_provenance_id=source_id,
                raw_data=row,
                imported_at_utc=imported_at_utc,
            )
        )

        provenance_records.append(
            SamGovProvenanceRecord(
                source_id=source_id,
                applied_as_entity_id=applied_as_entity_id,
                source_system="sam_gov_assistance_listings_download",
                source_filename=source_filename,
                row_number=idx,
                column_names_used=tuple(row.keys()),
                source_hash=source_hash,
                imported_at_utc=imported_at_utc,
                parser_version=parser_version,
                source_record_id=aln,
            )
        )

        listings.append(
            SamGovAssistanceListingRecord(
                listing_id=listing_id,
                raw_import_id=import_id,
                assistance_listing_number=aln,
                program_title=title,
                agency=agency,
                agency_code=agency_code,
                subagency=_first_present(row, subagency_aliases),
                assistance_type=_first_present(row, type_aliases),
                objectives=_first_present(row, obj_aliases),
                eligible_applicants=_first_present(row, elig_aliases),
                beneficiaries=_first_present(row, benef_aliases),
                use_restrictions=_first_present(row, rest_aliases),
                application_procedures=_first_present(row, proc_aliases),
                award_floor=_parse_int_or_none(_first_present(row, floor_aliases)),
                award_ceiling=_parse_int_or_none(_first_present(row, ceiling_aliases)),
                last_updated_date=_first_present(row, date_aliases),
                url=_first_present(row, url_aliases),
            )
        )

    return SamGovParseResult(
        raw_rows=tuple(raw_rows),
        listings=tuple(listings),
        provenance_records=tuple(provenance_records),
    )

def parse_sam_gov_file(
    file_path: str,
    *,
    imported_at_utc: str,
    applied_as_entity_id: Optional[str] = None,
    parser_version: str = "sam_gov_adapter_v1",
) -> SamGovParseResult:

    path = Path(file_path)
    if path.suffix.lower() != ".csv":
        raise SamGovParseError("Only .csv extensions are supported.")

    with open(path, "r", encoding="utf-8") as f:
        csv_text = f.read()

    source_filename = path.name

    return parse_sam_gov_csv_text(
        csv_text,
        source_filename=source_filename,
        imported_at_utc=imported_at_utc,
        applied_as_entity_id=applied_as_entity_id,
        parser_version=parser_version,
    )
