import csv
import hashlib
import io
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

class GrantsGovParseError(ValueError):
    pass

@dataclass(frozen=True, kw_only=True)
class GrantsGovRawRow:
    import_id: str
    applied_as_entity_id: str
    source_provenance_id: str
    raw_data: dict[str, str]
    imported_at_utc: str

@dataclass(frozen=True, kw_only=True)
class GrantsGovOpportunityRecord:
    opportunity_id: str
    applied_as_entity_id: str
    raw_import_id: str
    title: str
    funder: str
    close_date_utc: Optional[str]
    posted_date_utc: Optional[str]
    opportunity_number: Optional[str]
    description: Optional[str]
    eligibility_text: Optional[str]
    award_ceiling: Optional[int]
    award_floor: Optional[int]
    url: Optional[str]

@dataclass(frozen=True, kw_only=True)
class GrantsGovProvenanceRecord:
    source_id: str
    applied_as_entity_id: str
    source_system: str
    source_filename: str
    row_number: int
    column_names_used: tuple[str, ...]
    source_hash: str
    imported_at_utc: str
    parser_version: str
    source_record_id: Optional[str] = None

@dataclass(frozen=True, kw_only=True)
class GrantsGovParseResult:
    raw_rows: tuple[GrantsGovRawRow, ...]
    opportunities: tuple[GrantsGovOpportunityRecord, ...]
    provenance_records: tuple[GrantsGovProvenanceRecord, ...]

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

def parse_grants_gov_csv_text(
    csv_text: str,
    *,
    applied_as_entity_id: Optional[str] = None,
    identity_scope: Optional[str] = None,
    source_filename: str,
    imported_at_utc: str,
    parser_version: str = "grants_gov_adapter_v1",
) -> GrantsGovParseResult:

    if identity_scope != "public_corpus":
        if not applied_as_entity_id or not applied_as_entity_id.strip():
            raise GrantsGovParseError("applied_as_entity_id cannot be blank.")

    if not source_filename or not source_filename.strip():
        raise GrantsGovParseError("source_filename cannot be blank.")

    hasher = hashlib.sha3_256()
    hasher.update(csv_text.encode("utf-8"))
    source_hash = hasher.hexdigest()

    f = io.StringIO(csv_text)
    try:
        reader = csv.DictReader(f, strict=True)
        if reader.fieldnames is None:
            # Check if file had any data
            f.seek(0)
            if f.read().strip():
                raise GrantsGovParseError("Malformed CSV: No fieldnames but file is not empty.")
            rows = []
            fieldnames_tuple = tuple()
        else:
            norm_headers = []
            for h in reader.fieldnames:
                if h is None or str(h).strip() == "":
                    raise GrantsGovParseError("Malformed CSV: Blank or None fieldname found.")
                nh = _normalize_header(h)
                if nh in norm_headers:
                    raise GrantsGovParseError(f"Malformed CSV: Duplicate normalized header '{nh}'.")
                norm_headers.append(nh)

            rows = []
            for r in reader:
                if None in r:
                    raise GrantsGovParseError("Malformed CSV: Row has more columns than headers.")
                rows.append(r)
            fieldnames_tuple = tuple(reader.fieldnames)
    except csv.Error as e:
        raise GrantsGovParseError(f"Malformed CSV: {e}")
    except GrantsGovParseError:
        raise
    except Exception as e:
        raise GrantsGovParseError(f"Malformed CSV: {e}")

    raw_rows = []
    opportunities = []
    provenance_records = []

    title_aliases = {"opportunity title", "title"}
    funder_aliases = {"agency", "funder"}
    close_date_aliases = {"close date", "deadline"}
    posted_date_aliases = {"posted date"}
    opp_number_aliases = {"opportunity number"}
    description_aliases = {"description", "synopsis"}
    eligibility_aliases = {"eligibility", "additional information on eligibility"}
    ceiling_aliases = {"award ceiling"}
    floor_aliases = {"award floor"}
    url_aliases = {"additional information url", "url"}

    # Start at row 2 to account for header
    for idx, row in enumerate(rows, start=2):
        if _is_blank_row(row):
            continue

        title = _first_present(row, title_aliases)
        funder = _first_present(row, funder_aliases)

        if not title:
            raise GrantsGovParseError(f"Missing title on row {idx}")
        if not funder:
            raise GrantsGovParseError(f"Missing funder/agency on row {idx}")

        opportunity_number = _first_present(row, opp_number_aliases)

        if identity_scope == "public_corpus" and not opportunity_number:
            raise GrantsGovParseError(f"Missing opportunity number on row {idx}")

        norm_title = _normalize_identity_part(title)
        norm_funder = _normalize_identity_part(funder)

        if identity_scope == "public_corpus":
            norm_opp_num = _normalize_identity_part(opportunity_number)
            opportunity_id = _deterministic_id(
                "OPP-", "public_corpus", norm_opp_num, norm_title, norm_funder
            )
        else:
            opportunity_id = _deterministic_id(
                "OPP-", applied_as_entity_id, norm_title, norm_funder
            )

        import_id = _deterministic_id(
            "IMP-", applied_as_entity_id, source_hash, "csv", idx
        )
        source_id = _deterministic_id(
            "SRC-", applied_as_entity_id, source_hash, "csv", idx
        )

        raw_rows.append(
            GrantsGovRawRow(
                import_id=import_id,
                applied_as_entity_id=applied_as_entity_id,
                source_provenance_id=source_id,
                raw_data=row,
                imported_at_utc=imported_at_utc,
            )
        )

        provenance_records.append(
            GrantsGovProvenanceRecord(
                source_id=source_id,
                applied_as_entity_id=applied_as_entity_id,
                source_system="grants_gov_download",
                source_filename=source_filename,
                row_number=idx,
                column_names_used=tuple(row.keys()),
                source_hash=source_hash,
                imported_at_utc=imported_at_utc,
                parser_version=parser_version,
                source_record_id=opportunity_number,
            )
        )

        opportunities.append(
            GrantsGovOpportunityRecord(
                opportunity_id=opportunity_id,
                applied_as_entity_id=applied_as_entity_id,
                raw_import_id=import_id,
                title=title,
                funder=funder,
                close_date_utc=_first_present(row, close_date_aliases),
                posted_date_utc=_first_present(row, posted_date_aliases),
                opportunity_number=opportunity_number,
                description=_first_present(row, description_aliases),
                eligibility_text=_first_present(row, eligibility_aliases),
                award_ceiling=_parse_int_or_none(_first_present(row, ceiling_aliases)),
                award_floor=_parse_int_or_none(_first_present(row, floor_aliases)),
                url=_first_present(row, url_aliases),
            )
        )

    return GrantsGovParseResult(
        raw_rows=tuple(raw_rows),
        opportunities=tuple(opportunities),
        provenance_records=tuple(provenance_records),
    )

def parse_grants_gov_file(
    file_path: str,
    *,
    applied_as_entity_id: Optional[str] = None,
    identity_scope: Optional[str] = None,
    imported_at_utc: str,
    parser_version: str = "grants_gov_adapter_v1",
) -> GrantsGovParseResult:

    path = Path(file_path)
    if path.suffix.lower() != ".csv":
        raise GrantsGovParseError("Only .csv extensions are supported.")

    with open(path, "r", encoding="utf-8") as f:
        csv_text = f.read()

    # Extract filename from path using pathlib
    source_filename = path.name

    return parse_grants_gov_csv_text(
        csv_text,
        applied_as_entity_id=applied_as_entity_id,
        identity_scope=identity_scope,
        source_filename=source_filename,
        imported_at_utc=imported_at_utc,
        parser_version=parser_version,
    )
