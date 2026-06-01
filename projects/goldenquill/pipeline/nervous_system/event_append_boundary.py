from enum import Enum
from typing import Any, Literal
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, model_validator

class EventAppendStatus(str, Enum):
    APPEND_REQUEST_ACCEPTED_FOR_POLICY_REVIEW = "APPEND_REQUEST_ACCEPTED_FOR_POLICY_REVIEW"
    REJECTED_BY_POLICY = "REJECTED_BY_POLICY"
    REJECTED_BY_IDENTITY_BOUNDARY = "REJECTED_BY_IDENTITY_BOUNDARY"
    REJECTED_BY_POSTURE = "REJECTED_BY_POSTURE"
    REJECTED_BY_APPLIED_AS_BOUNDARY = "REJECTED_BY_APPLIED_AS_BOUNDARY"
    REJECTED_BY_STALE_PROJECTION = "REJECTED_BY_STALE_PROJECTION"
    REJECTED_BY_SYNC_CONFLICT = "REJECTED_BY_SYNC_CONFLICT"
    REJECTED_BY_MISSING_OPERATOR_AUTHORIZATION = "REJECTED_BY_MISSING_OPERATOR_AUTHORIZATION"
    REQUIRES_SIGNATURE_CEREMONY = "REQUIRES_SIGNATURE_CEREMONY"

class EventAppendFamily(str, Enum):
    STEWARD_PROPOSAL = "STEWARD_PROPOSAL"
    COMMAND_VALIDATION = "COMMAND_VALIDATION"
    NOOP_DRY_RUN = "NOOP_DRY_RUN"
    OPERATOR_REVIEW = "OPERATOR_REVIEW"

EVENT_APPEND_FORBIDDEN_FIELDS = {
    "event_id",
    "signature_event_id",
    "lock_id",
    "export_id",
    "submitted_at",
    "artifact_hash",
    "operator_signature_event_id",
    "canonical_mutation_result",
    "ledger_offset",
    "committed_at",
    "written_at",
    "db_row_id",
}

class EventAppendRequest(BaseModel):
    append_request_id: str
    source_proposal_id: str
    source_dry_run_id: str | None = None
    requested_family: EventAppendFamily
    requested_event_type: str

    operator_id: str
    applied_as_entity_id: str | None = None
    licensed_node_id: str | None = None
    posture_at_request: str

    read_model_epoch: str | None = None
    last_verified_event_id: str | None = None
    source_event_ids: list[str] = Field(default_factory=list)

    operator_review_summary: str
    rationale: str
    policy_basis: list[str] = Field(default_factory=list)

    requires_signature_ceremony: bool = False
    requested_at: datetime

    payload_schema_version: str = "0.1.0"
    payload_preview: dict[str, Any] = Field(default_factory=dict)
    payload_hash: str | None = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="before")
    @classmethod
    def check_forbidden_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            forbidden = EVENT_APPEND_FORBIDDEN_FIELDS.intersection(data.keys())
            if forbidden:
                raise ValueError(f"EventAppendRequest forbids execution fields: {sorted(forbidden)}")
        return data

class EventAppendReceipt(BaseModel):
    append_request_id: str
    source_proposal_id: str
    status: EventAppendStatus
    reviewed_at: datetime
    reviewer: Literal["EVENT_APPEND_BOUNDARY"] = "EVENT_APPEND_BOUNDARY"
    reason: str | None = None
    required_next_surface: str | None = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="before")
    @classmethod
    def check_forbidden_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            forbidden = EVENT_APPEND_FORBIDDEN_FIELDS.intersection(data.keys())
            if forbidden:
                raise ValueError(f"EventAppendReceipt forbids execution fields: {sorted(forbidden)}")
        return data
