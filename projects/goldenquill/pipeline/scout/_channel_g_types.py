from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pipeline.scout._types import Candidate

class BoardCategoryEnum(str, Enum):
    NOW = "Now"
    PREPARE = "Prepare"
    MONITOR = "Monitor"
    PARTNER_CONSORTIUM = "Partner / Consortium"
    NEXT_CYCLE = "Next Cycle"
    PARK = "Park"

class ScoringStatusEnum(str, Enum):
    SCORED = "scored"
    UNAVAILABLE = "unavailable"
    NOT_YET_SCORED = "not_yet_scored"
    NOT_APPLICABLE = "not_applicable"

class EvidenceStatusEnum(str, Enum):
    MISSING = "Missing"
    DRAFTING = "Drafting"
    STAGED = "Staged"
    NEEDS_REVIEW = "Needs Review"
    VERIFIED = "Verified"
    NOT_APPLICABLE = "Not Applicable"

class BlockerLevelEnum(str, Enum):
    NONE = "None"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    HARD_BLOCKER = "Hard Blocker"

class EligibilityStatusEnum(str, Enum):
    CONFIRMED_TRUE = "confirmed_true"
    CONFIRMED_FALSE = "confirmed_false"
    UNKNOWN = "unknown"
    NEEDS_CHECK = "needs_check"

class DeadlineStatusEnum(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    UNKNOWN = "unknown"
    ROLLING = "rolling"

class CycleStatusEnum(str, Enum):
    CURRENT = "current"
    RECURRING = "recurring"
    ONE_TIME = "one_time"
    UNKNOWN = "unknown"

class SourceFreshnessStatusEnum(str, Enum):
    CURRENT = "current"
    STALE = "stale"
    UNKNOWN = "unknown"
    NOT_YET_DETERMINED = "not_yet_determined"
    PENDING_SOURCE_CONFIGURATION = "pending_source_configuration"
    UNAVAILABLE = "unavailable"

@dataclass(frozen=True, kw_only=True)
class NormalizedScore:
    scoring_status: ScoringStatusEnum
    raw_value: Optional[str]
    normalized_value: Optional[float]
    score_scale: Optional[str]
    rationale: Optional[str]

@dataclass(frozen=True, kw_only=True)
class RawImportRow:
    import_id: str
    applied_as_entity_id: str
    source_provenance_id: str
    raw_data: dict[str, str]
    imported_at_utc: str

@dataclass(frozen=True, kw_only=True)
class ScoutOpportunityRecord:
    opportunity_id: str
    applied_as_entity_id: str
    raw_import_id: str
    title: str
    funder: str
    url: Optional[str]
    close_date_utc: Optional[str]
    award_ceiling: Optional[int]
    award_floor: Optional[int]
    raw_lane_category: str
    board_category: BoardCategoryEnum
    eligibility_status: EligibilityStatusEnum
    deadline_status: DeadlineStatusEnum
    cycle_status: CycleStatusEnum
    partner_requirement: bool
    partner_confirmed: bool
    has_active_hard_blocker: bool
    source_freshness_status: SourceFreshnessStatusEnum
    tech_fit_score: NormalizedScore
    evidence_fit_score: NormalizedScore
    funding_fit_score: NormalizedScore
    timing_score: NormalizedScore
    eligibility_score: NormalizedScore
    strategic_leverage_score: NormalizedScore
    total_score: NormalizedScore
    next_operator_action: Optional[str]
    last_updated_utc: str

    def to_candidate(self) -> "Candidate":
        raise NotImplementedError("Channel G Candidate projection is not implemented in schema pass.")

@dataclass(frozen=True, kw_only=True)
class EvidenceItem:
    evidence_item_id: str
    applied_as_entity_id: str
    evidence_item: str
    needed_for: str
    current_status: EvidenceStatusEnum
    why_it_matters: str
    minimum_acceptable_artifact: str
    owner: str
    due_date_or_timing: Optional[str]
    sensitivity_classification: str
    source_or_storage_location: Optional[str]
    blocker_level: BlockerLevelEnum
    next_action: str
    linked_project_id: Optional[str]
    can_be_generated_by_tilth: bool
    dependencies: tuple[str, ...]
    verification_notes: Optional[str]
    last_verified_at: Optional[str]
    artifact_hash: Optional[str]
    reusable_across_opportunities: bool

@dataclass(frozen=True, kw_only=True)
class OpportunityEvidenceLink:
    link_id: str
    applied_as_entity_id: str
    opportunity_id: str
    evidence_item_id: str
    needed_for_this_opportunity: str
    requirement_strength: str
    blocker_level_for_this_opportunity: BlockerLevelEnum
    notes: Optional[str]

@dataclass(frozen=True, kw_only=True)
class SourceProvenanceRecord:
    source_id: str
    applied_as_entity_id: str
    source_type: str
    source_filename: str
    sheet_name: str
    row_number: int
    column_names_used: tuple[str, ...]
    source_hash: str
    imported_at_utc: str
    parser_version: str
    source_freshness_status: SourceFreshnessStatusEnum
    last_verified_at_utc: Optional[str]
    verification_method: str
