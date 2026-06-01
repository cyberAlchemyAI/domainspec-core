import csv
import hashlib
import io
import re
from dataclasses import dataclass
from typing import Any, Dict

from pipeline.scout._channel_g_types import (
    BlockerLevelEnum,
    EvidenceItem,
    EvidenceStatusEnum,
    OpportunityEvidenceLink,
    RawImportRow,
    ScoutOpportunityRecord,
    SourceProvenanceRecord,
)
from pipeline.scout._channel_g_normalizer import (
    allocate_board_category,
    normalize_bool,
    normalize_cycle_status,
    normalize_deadline_status,
    normalize_eligibility_status,
    normalize_score,
    normalize_source_freshness_status,
)


class ChannelGParseError(ValueError):
    pass


@dataclass(frozen=True, kw_only=True)
class ChannelGParseResult:
    raw_rows: tuple[RawImportRow, ...]
    opportunities: tuple[ScoutOpportunityRecord, ...]
    evidence_items: tuple[EvidenceItem, ...]
    evidence_links: tuple[OpportunityEvidenceLink, ...]
    provenance_records: tuple[SourceProvenanceRecord, ...]


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


# ALIAS MAPS
OPP_ALIASES = {
    "title": {"program name", "grant title", "opportunity", "title", "name"},
    "funder": {"funder", "agency", "sponsor", "department"},
    "url": {"url", "link", "opportunity url", "website"},
    "close_date_utc": {"due date", "deadline", "timeline", "cycle", "close date"},
    "award_ceiling": {"award ceiling", "max award", "maximum", "up to"},
    "award_floor": {"award floor", "min award", "minimum"},
    "raw_lane_category": {"lane", "category", "status", "priority", "board"},
    "next_operator_action": {"next action", "first move", "next steps"},
    "eligibility_status": {"eligibility status", "eligibility", "eligible"},
    "deadline_status": {"deadline status", "deadline state", "open closed", "status"},
    "cycle_status": {"cycle status", "cycle type", "recurrence"},
    "partner_requirement": {
        "partner requirement",
        "partner required",
        "requires partner",
        "consortium required",
    },
    "partner_confirmed": {
        "partner confirmed",
        "partner secured",
        "consortium confirmed",
    },
    "has_active_hard_blocker": {"hard blocker", "active hard blocker", "blocked"},
    "source_freshness_status": {
        "source freshness",
        "freshness",
        "verification status",
    },
}

SCORE_ALIASES = {
    "tech_fit_score": {"tech fit", "technical fit"},
    "evidence_fit_score": {"evidence fit", "readiness"},
    "funding_fit_score": {"funding fit", "financial fit"},
    "timing_score": {"timing", "schedule fit"},
    "eligibility_score": {"eligibility score", "eligibility fit"},
    "strategic_leverage_score": {"strategic leverage", "strategic fit"},
    "total_score": {"total score", "overall score", "score"},
}

EVD_ALIASES = {
    "evidence_item": {"evidence needed", "evidence item", "requirement"},
    "needed_for": {"needed for", "purpose"},
    "current_status": {"evidence status", "current status"},
    "why_it_matters": {"why it matters", "evidence rationale", "rationale"},
    "minimum_acceptable_artifact": {
        "minimum acceptable artifact",
        "min requirement",
    },
    "owner": {"evidence owner", "owner", "assignee", "responsible"},
    "due_date_or_timing": {"evidence due date", "needed by", "evidence timing"},
    "sensitivity_classification": {"sensitivity", "classification"},
    "source_or_storage_location": {"storage location", "evidence link", "folder"},
    "blocker_level": {"blocker level", "severity"},
    "next_action": {"evidence next action", "evidence to do", "evidence next step"},
}


def _first_present(row: dict[str, str], aliases: set[str]) -> str | None:
    for header, val in row.items():
        if val is None or val.strip() == "":
            continue
        if _normalize_header(header) in aliases:
            return val
    return None


def _parse_int_or_none(val: str | None) -> int | None:
    if not val:
        return None
    cleaned = re.sub(r"[^\d-]", "", val)
    if not cleaned:
        return None
    try:
        return int(cleaned)
    except ValueError:
        return None


def _make_evidence_item(
    row: dict[str, str], applied_as_entity_id: str, opportunity_title: str
) -> EvidenceItem | None:
    ev_item = _first_present(row, EVD_ALIASES["evidence_item"])
    if not ev_item:
        return None

    needed_for = _first_present(row, EVD_ALIASES["needed_for"])
    if not needed_for:
        needed_for = opportunity_title if opportunity_title else "not_yet_determined"

    status_str = _first_present(row, EVD_ALIASES["current_status"])
    if status_str:
        s_norm = status_str.strip().lower()
        if s_norm in {"missing"}:
            status = EvidenceStatusEnum.MISSING
        elif s_norm in {"drafting"}:
            status = EvidenceStatusEnum.DRAFTING
        elif s_norm in {"staged"}:
            status = EvidenceStatusEnum.STAGED
        elif s_norm in {"needs review"}:
            status = EvidenceStatusEnum.NEEDS_REVIEW
        elif s_norm in {"verified"}:
            status = EvidenceStatusEnum.VERIFIED
        elif s_norm in {"not applicable"}:
            status = EvidenceStatusEnum.NOT_APPLICABLE
        else:
            status = EvidenceStatusEnum.MISSING
    else:
        status = EvidenceStatusEnum.MISSING

    blocker_str = _first_present(row, EVD_ALIASES["blocker_level"])
    if blocker_str:
        b_norm = blocker_str.strip().lower()
        if b_norm in {"low"}:
            blocker = BlockerLevelEnum.LOW
        elif b_norm in {"medium"}:
            blocker = BlockerLevelEnum.MEDIUM
        elif b_norm in {"high"}:
            blocker = BlockerLevelEnum.HIGH
        elif b_norm in {"hard blocker"}:
            blocker = BlockerLevelEnum.HARD_BLOCKER
        elif b_norm in {"none"}:
            blocker = BlockerLevelEnum.NONE
        else:
            blocker = BlockerLevelEnum.NONE
    else:
        blocker = BlockerLevelEnum.NONE

    return EvidenceItem(
        evidence_item_id=_deterministic_id(
            "EVD-", applied_as_entity_id, _normalize_identity_part(ev_item)
        ),
        applied_as_entity_id=applied_as_entity_id,
        evidence_item=ev_item,
        needed_for=needed_for,
        current_status=status,
        why_it_matters=_first_present(row, EVD_ALIASES["why_it_matters"])
        or "not_yet_determined",
        minimum_acceptable_artifact=_first_present(
            row, EVD_ALIASES["minimum_acceptable_artifact"]
        )
        or "not_yet_determined",
        owner=_first_present(row, EVD_ALIASES["owner"]) or "not_yet_determined",
        due_date_or_timing=_first_present(row, EVD_ALIASES["due_date_or_timing"]),
        sensitivity_classification=_first_present(
            row, EVD_ALIASES["sensitivity_classification"]
        )
        or "not_yet_determined",
        source_or_storage_location=_first_present(
            row, EVD_ALIASES["source_or_storage_location"]
        ),
        blocker_level=blocker,
        next_action=_first_present(row, EVD_ALIASES["next_action"])
        or "not_yet_determined",
        linked_project_id=None,
        can_be_generated_by_tilth=False,
        dependencies=(),
        verification_notes=None,
        last_verified_at=None,
        artifact_hash=None,
        reusable_across_opportunities=True,
    )


def _make_evidence_link(
    ev_item: EvidenceItem, opportunity_id: str, applied_as_entity_id: str
) -> OpportunityEvidenceLink:
    return OpportunityEvidenceLink(
        link_id=_deterministic_id(
            "LNK-", applied_as_entity_id, opportunity_id, ev_item.evidence_item_id, ev_item.needed_for
        ),
        applied_as_entity_id=applied_as_entity_id,
        opportunity_id=opportunity_id,
        evidence_item_id=ev_item.evidence_item_id,
        needed_for_this_opportunity=ev_item.needed_for,
        requirement_strength="unknown",
        blocker_level_for_this_opportunity=ev_item.blocker_level,
        notes=None,
    )


def parse_channel_g_rows(
    rows: list[dict[str, str]],
    *,
    applied_as_entity_id: str,
    source_filename: str,
    source_hash: str,
    imported_at_utc: str,
    parser_version: str = "channel_g_parser_b1",
    sheet_name: str = "csv",
) -> ChannelGParseResult:

    if not applied_as_entity_id or not applied_as_entity_id.strip():
        raise ChannelGParseError("applied_as_entity_id cannot be blank.")
    if not source_filename or not source_filename.strip():
        raise ChannelGParseError("source_filename cannot be blank.")
    if not source_hash or not source_hash.strip():
        raise ChannelGParseError("source_hash cannot be blank.")

    raw_rows = []
    opportunities = []
    evidence_items_map = {}
    evidence_links = []
    provenance_records = []

    # Row 1 is header, data starts at row 2
    for idx, row in enumerate(rows, start=2):
        if _is_blank_row(row):
            continue

        title = _first_present(row, OPP_ALIASES["title"])
        funder = _first_present(row, OPP_ALIASES["funder"])

        if not title:
            raise ChannelGParseError(f"Missing title on row {idx}")
        if not funder:
            raise ChannelGParseError(f"Missing funder on row {idx}")

        norm_title = _normalize_identity_part(title)
        norm_funder = _normalize_identity_part(funder)

        opportunity_id = _deterministic_id(
            "OPP-", applied_as_entity_id, norm_title, norm_funder
        )

        import_id = _deterministic_id(
            "IMP-", applied_as_entity_id, source_hash, sheet_name, idx
        )
        source_id = _deterministic_id(
            "SRC-", applied_as_entity_id, source_hash, sheet_name, idx
        )

        raw_rows.append(
            RawImportRow(
                import_id=import_id,
                applied_as_entity_id=applied_as_entity_id,
                source_provenance_id=source_id,
                raw_data=row,
                imported_at_utc=imported_at_utc,
            )
        )

        provenance_records.append(
            SourceProvenanceRecord(
                source_id=source_id,
                applied_as_entity_id=applied_as_entity_id,
                source_type="spreadsheet",
                source_filename=source_filename,
                sheet_name=sheet_name,
                row_number=idx,
                column_names_used=tuple(row.keys()),
                source_hash=source_hash,
                imported_at_utc=imported_at_utc,
                parser_version=parser_version,
                source_freshness_status=normalize_source_freshness_status(
                    _first_present(row, OPP_ALIASES["source_freshness_status"])
                ),
                last_verified_at_utc=None,
                verification_method="none",
            )
        )

        eligibility_status = normalize_eligibility_status(
            _first_present(row, OPP_ALIASES["eligibility_status"])
        )
        deadline_status = normalize_deadline_status(
            _first_present(row, OPP_ALIASES["deadline_status"])
        )
        cycle_status = normalize_cycle_status(
            _first_present(row, OPP_ALIASES["cycle_status"])
        )
        partner_req = normalize_bool(
            _first_present(row, OPP_ALIASES["partner_requirement"]), default=False
        )
        partner_conf = normalize_bool(
            _first_present(row, OPP_ALIASES["partner_confirmed"]), default=False
        )
        hard_blocker = normalize_bool(
            _first_present(row, OPP_ALIASES["has_active_hard_blocker"]), default=False
        )
        freshness = normalize_source_freshness_status(
            _first_present(row, OPP_ALIASES["source_freshness_status"])
        )
        total_score = normalize_score(
            _first_present(row, SCORE_ALIASES["total_score"])
        )

        board_cat = allocate_board_category(
            raw_lane_category=_first_present(row, OPP_ALIASES["raw_lane_category"]),
            eligibility_status=eligibility_status,
            deadline_status=deadline_status,
            cycle_status=cycle_status,
            partner_requirement=partner_req,
            partner_confirmed=partner_conf,
            has_active_hard_blocker=hard_blocker,
            source_freshness_status=freshness,
            total_score=total_score,
        )

        opportunities.append(
            ScoutOpportunityRecord(
                opportunity_id=opportunity_id,
                applied_as_entity_id=applied_as_entity_id,
                raw_import_id=import_id,
                title=title,
                funder=funder,
                url=_first_present(row, OPP_ALIASES["url"]),
                close_date_utc=_first_present(row, OPP_ALIASES["close_date_utc"]),
                award_ceiling=_parse_int_or_none(
                    _first_present(row, OPP_ALIASES["award_ceiling"])
                ),
                award_floor=_parse_int_or_none(
                    _first_present(row, OPP_ALIASES["award_floor"])
                ),
                raw_lane_category=_first_present(row, OPP_ALIASES["raw_lane_category"])
                or "",
                board_category=board_cat,
                eligibility_status=eligibility_status,
                deadline_status=deadline_status,
                cycle_status=cycle_status,
                partner_requirement=partner_req,
                partner_confirmed=partner_conf,
                has_active_hard_blocker=hard_blocker,
                source_freshness_status=freshness,
                tech_fit_score=normalize_score(
                    _first_present(row, SCORE_ALIASES["tech_fit_score"])
                ),
                evidence_fit_score=normalize_score(
                    _first_present(row, SCORE_ALIASES["evidence_fit_score"])
                ),
                funding_fit_score=normalize_score(
                    _first_present(row, SCORE_ALIASES["funding_fit_score"])
                ),
                timing_score=normalize_score(
                    _first_present(row, SCORE_ALIASES["timing_score"])
                ),
                eligibility_score=normalize_score(
                    _first_present(row, SCORE_ALIASES["eligibility_score"])
                ),
                strategic_leverage_score=normalize_score(
                    _first_present(row, SCORE_ALIASES["strategic_leverage_score"])
                ),
                total_score=total_score,
                next_operator_action=_first_present(
                    row, OPP_ALIASES["next_operator_action"]
                ),
                last_updated_utc=imported_at_utc,
            )
        )

        ev_item = _make_evidence_item(row, applied_as_entity_id, title)
        if ev_item:
            if ev_item.evidence_item_id not in evidence_items_map:
                evidence_items_map[ev_item.evidence_item_id] = ev_item

            # Create link
            evidence_links.append(
                _make_evidence_link(ev_item, opportunity_id, applied_as_entity_id)
            )

    return ChannelGParseResult(
        raw_rows=tuple(raw_rows),
        opportunities=tuple(opportunities),
        evidence_items=tuple(evidence_items_map.values()),
        evidence_links=tuple(evidence_links),
        provenance_records=tuple(provenance_records),
    )


def parse_channel_g_csv_text(
    csv_text: str,
    *,
    applied_as_entity_id: str,
    source_filename: str,
    imported_at_utc: str,
    parser_version: str = "channel_g_parser_b1",
) -> ChannelGParseResult:
    if not applied_as_entity_id or not applied_as_entity_id.strip():
        raise ChannelGParseError("applied_as_entity_id cannot be blank.")
    if not source_filename or not source_filename.strip():
        raise ChannelGParseError("source_filename cannot be blank.")

    hasher = hashlib.sha3_256()
    hasher.update(csv_text.encode("utf-8"))
    source_hash = hasher.hexdigest()

    f = io.StringIO(csv_text)
    reader = csv.DictReader(f)
    if reader.fieldnames is None:
        rows = []
    else:
        rows = list(reader)

    return parse_channel_g_rows(
        rows,
        applied_as_entity_id=applied_as_entity_id,
        source_filename=source_filename,
        source_hash=source_hash,
        imported_at_utc=imported_at_utc,
        parser_version=parser_version,
        sheet_name="csv",
    )
