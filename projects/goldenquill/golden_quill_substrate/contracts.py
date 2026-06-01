"""
Golden Quill v0.3 Internal Substrate Contracts.

This module defines canonical schema boundaries only.
It does not perform authorization, database access, vector retrieval, model routing,
or state transitions. Those belong to Nervous System, Logician, Archivist,
Model Access Boundary, and State Machine Runner respectively.

Critical doctrine:
- Pydantic validates structure.
- Nervous System validates identity binding, expiration, authorization, and route authority.
- Logician/Gate Runner alone returns GateFailure/GateResult.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


# -----------------------------------------------------------------------------
# BASE MODEL
# -----------------------------------------------------------------------------

class ContractModel(BaseModel):
    """
    Strict base model for all v0.3 contracts.

    extra='forbid' is not optional. It prevents Brain/Judge/model outputs from
    smuggling unauthorized authority fields such as gate_failures, gate_result,
    db_query, route_override, or memory_mutation.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
        str_strip_whitespace=True,
    )


# -----------------------------------------------------------------------------
# CORE ENUMS
# -----------------------------------------------------------------------------

ActorType = Literal[
    "HUMAN",
    "SYSTEM_AGENT",
    "STATE_MACHINE_RUNNER",
    "BRAIN_INTENT_PARSER",
    "BRAIN_SCRIBE",
    "BRAIN_JUDGE",
    "ARCHIVIST",
    "LOGICIAN_GATE_RUNNER",
    "MODEL_ACCESS_BOUNDARY",
    "AUDIT_WRITER",
]

AuthStrength = Literal[
    "SESSION",
    "SIGNED_SERVICE_TOKEN",
    "HARDWARE_BOUND_SESSION",
    "HUMAN_REAUTH",
]

RequestOrigin = Literal[
    "USER_SESSION",
    "INTERNAL_SERVICE",
    "SCHEDULED_JOB",
    "STATE_MACHINE_CALLBACK",
]

RouteMode = Literal[
    "LOCAL_ONLY",
    "HYBRID_PUBLIC_FRONTIER_LOCAL_VAULT",
    "ALL_MODEL_ACCESS",
]

OperationType = Literal[
    "brain.intent.parse",
    "brain.scribe.draft",
    "brain.judge.review",
    "archivist.retrieve",
    "memory.create",
    "memory.update",
    "memory.supersede",
    "memory.retract",
    "packet.prepare",
    "packet.authorize_final",
    "packet.export",
    "evidence.intake",
    "evidence.promote",
    "model.invoke",
    "audit.read",
]

ResourceType = Literal[
    "PROJECT",
    "OPPORTUNITY",
    "RFA",
    "SECTION",
    "DRAFT",
    "EVIDENCE",
    "MEMORY_RECORD",
    "PACKET",
    "MODEL_ROUTE",
    "AUDIT_EVENT",
]

FailureType = Literal[
    "BLOCKER",
    "WARNING",
    "SECURITY_FAILURE",
    "REMEDIATION_HINT",
]

GateStage = Literal[
    "PRE",
    "POST",
    "COMMIT",
]

SensitivityLevel = Literal[
    "PUBLIC",
    "ORG_CONTEXT",
    "SENSITIVE_INTERNAL",
    "RESTRICTED",
]

MemoryState = Literal[
    "ACTIVE",
    "SUPERSEDED",
    "RETRACTED",
    "SEALED",
]

SubstrateStatus = Literal[
    "ACCEPTED",
    "REJECTED",
    "FAILED",
    "COMPLETED",
]

ErrorCategory = Literal[
    "MALFORMED_REQUEST",
    "UNAUTHORIZED",
    "CROSS_BOUNDARY",
    "CANONICAL_STATE_CONFLICT",
    "GATE_FAILURE",
    "DEPENDENCY_FAILURE",
    "CONTRACT_VIOLATION",
    "INTERNAL_INVARIANT_BREACH",
]


# -----------------------------------------------------------------------------
# CANONICAL EXCEPTIONS
# -----------------------------------------------------------------------------

class IdentityExpired(Exception):
    """
    Raised only after structural validation succeeds.

    Do not raise this from Pydantic field/model validators. If raised inside
    Pydantic construction, many callers will treat it as malformed schema and
    accidentally map it to 400. Expired identity is a security failure: 403.
    """


class ContractViolation(Exception):
    """
    Raised when a component violates its own contract boundary.
    Example: Brain attempts DB access or Judge returns GateFailure.
    """


# -----------------------------------------------------------------------------
# IDENTITY CONTRACT
# -----------------------------------------------------------------------------

class IdentityContext(ContractModel):
    session_id: UUID
    principal_id: UUID
    actor_type: ActorType

    licensed_node_id: UUID
    licensed_customer_entity_id: UUID

    # Absolute applicant / beneficiary / retrieval / memory boundary.
    applied_as_entity_id: UUID

    role_ids: list[UUID] = Field(default_factory=list)
    permission_scopes: list[str] = Field(default_factory=list)

    auth_strength: AuthStrength
    auth_token_id: UUID
    actor_binding_hash: str = Field(..., min_length=64, max_length=128)

    issued_at: datetime
    expires_at: datetime

    request_origin: RequestOrigin

    human_present: bool = False
    final_authorization_eligible: bool = False

    @field_validator("issued_at", "expires_at")
    @classmethod
    def must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("datetime must be timezone-aware")
        return value

    @model_validator(mode="after")
    def validate_structural_time_window(self) -> "IdentityContext":
        if self.expires_at <= self.issued_at:
            raise ValueError("expires_at must be after issued_at")
        return self

    def assert_not_expired(self, now: datetime | None = None) -> None:
        """
        Called by Nervous System after structural parsing and identity binding.
        Maps to 403 IDENTITY.EXPIRED, not 400.
        """
        check_time = now or datetime.now(timezone.utc)
        if check_time > self.expires_at:
            raise IdentityExpired("identity_context expired")

    def is_human_final_authorization_capable(self) -> bool:
        return (
            self.actor_type == "HUMAN"
            and self.auth_strength == "HUMAN_REAUTH"
            and self.human_present is True
            and self.final_authorization_eligible is True
        )


# -----------------------------------------------------------------------------
# REQUEST ENVELOPE
# -----------------------------------------------------------------------------

class OperationTarget(ContractModel):
    resource_type: ResourceType
    resource_id: UUID | None = None
    applied_as_entity_id: UUID


class RequestEnvelope(ContractModel):
    request_id: UUID
    correlation_id: UUID

    identity_context: IdentityContext

    operation_type: OperationType
    target: OperationTarget

    payload: dict[str, Any]

    declared_purpose: str = Field(..., min_length=12, max_length=500)
    requested_route_mode: RouteMode

    idempotency_key: str | None = None
    client_timestamp: datetime | None = None
    schema_version: Literal["v0.3"] = "v0.3"

    @field_validator("client_timestamp")
    @classmethod
    def client_timestamp_must_be_timezone_aware(
        cls,
        value: datetime | None,
    ) -> datetime | None:
        if value is not None and value.tzinfo is None:
            raise ValueError("client_timestamp must be timezone-aware")
        return value

    @model_validator(mode="after")
    def enforce_applied_as_target_match(self) -> "RequestEnvelope":
        """
        This is structural boundary enforcement. The full authorization decision
        still belongs to Nervous System + Logician.
        """
        if self.target.applied_as_entity_id != self.identity_context.applied_as_entity_id:
            raise ValueError("target.applied_as_entity_id must match identity_context.applied_as_entity_id")
        return self


# -----------------------------------------------------------------------------
# GATE CONTRACT
# -----------------------------------------------------------------------------

class GateFailure(ContractModel):
    failure_id: UUID
    gate_id: str = Field(..., min_length=1)
    gate_stage: GateStage

    failure_type: FailureType
    code: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)

    violating_target: str | None = None
    remediation_hint: str | None = None

    retryable: bool = False
    safe_to_show_user: bool = True

    # This field is locked. Other components cannot masquerade as gate authority.
    source_component: Literal["LOGICIAN_GATE_RUNNER"] = "LOGICIAN_GATE_RUNNER"

    evidence_ids: list[UUID] = Field(default_factory=list)
    snapshot_ids: list[UUID] = Field(default_factory=list)


class GateResult(ContractModel):
    request_id: UUID
    correlation_id: UUID

    passed: bool
    stage: GateStage

    failures: list[GateFailure] = Field(default_factory=list)
    warnings: list[GateFailure] = Field(default_factory=list)
    remediation_hints: list[GateFailure] = Field(default_factory=list)

    evaluated_gate_ids: list[str]
    policy_pack_version: str
    completed_at: datetime

    @field_validator("completed_at")
    @classmethod
    def completed_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("completed_at must be timezone-aware")
        return value

    @model_validator(mode="after")
    def passed_requires_no_blocking_failures(self) -> "GateResult":
        blocking = [
            failure for failure in self.failures
            if failure.failure_type in ("BLOCKER", "SECURITY_FAILURE")
        ]
        if self.passed and blocking:
            raise ValueError("passed=True is invalid when BLOCKER or SECURITY_FAILURE exists")
        return self


# -----------------------------------------------------------------------------
# STRUCTURED ERRORS / RESPONSE
# -----------------------------------------------------------------------------

class StructuredError(ContractModel):
    error_id: UUID
    status_code: int
    category: ErrorCategory
    code: str
    message: str

    request_id: UUID | None = None
    correlation_id: UUID | None = None

    gate_failures: list[GateFailure] = Field(default_factory=list)

    retryable: bool = False
    audit_event_id: UUID | None = None


class SubstrateResponse(ContractModel):
    request_id: UUID | None = None
    correlation_id: UUID | None = None

    status: SubstrateStatus
    status_code: int

    result: dict[str, Any] | None = None
    error: StructuredError | None = None

    gate_result: GateResult | None = None
    audit_event_id: UUID | None = None


# -----------------------------------------------------------------------------
# BRAIN OUTPUT CONTRACTS
# -----------------------------------------------------------------------------

class CitationAnchor(ContractModel):
    evidence_id: UUID
    anchor_id: str
    source_label: str
    quoted_span_hash: str | None = None


class ProposedClaim(ContractModel):
    claim_id: UUID
    claim_text: str
    support_status: Literal[
        "SUPPORTED",
        "PARTIALLY_SUPPORTED",
        "UNSUPPORTED",
        "NEEDS_HUMAN_CONFIRMATION",
    ]
    citation_anchors: list[CitationAnchor] = Field(default_factory=list)


class RequestedAction(ContractModel):
    action_type: OperationType
    target_hint: str | None = None
    required_payload_fields: list[str] = Field(default_factory=list)
    requires_retrieval: bool = False
    requires_memory_mutation: bool = False
    requires_human_authorization: bool = False


class RiskFinding(ContractModel):
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    risk_vector: str
    description: str
    affected_claim_ids: list[UUID] = Field(default_factory=list)
    recommended_action: str | None = None


class ReviewFinding(ContractModel):
    finding_id: UUID
    finding_type: Literal[
        "MISSING_EVIDENCE",
        "WEAK_ALIGNMENT",
        "INCONSISTENT_CLAIM",
        "RUBRIC_GAP",
        "REGISTER_MISMATCH",
        "STRUCTURAL_WEAKNESS",
        "HUMAN_REVIEW_REQUIRED",
    ]
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    description: str
    suggested_revision: str | None = None
    citation_anchors: list[CitationAnchor] = Field(default_factory=list)


class IntentManifest(ContractModel):
    interpreted_intent: str
    requested_actions: list[RequestedAction]
    ambiguity_flags: list[str] = Field(default_factory=list)
    risk_findings: list[RiskFinding] = Field(default_factory=list)
    proposed_next_operation: OperationType | None = None


class TextDraft(ContractModel):
    draft_text: str
    proposed_claims: list[ProposedClaim]
    citation_anchors_used: list[CitationAnchor]
    unsupported_claims: list[ProposedClaim] = Field(default_factory=list)
    requested_actions: list[RequestedAction] = Field(default_factory=list)
    risk_findings: list[RiskFinding] = Field(default_factory=list)
    output_manifest: dict[str, Any] = Field(default_factory=dict)


class JudgeReview(ContractModel):
    """
    Judge may return review/risk material only.

    Forbidden by extra='forbid':
    - gate_failures
    - gate_result
    - authoritative_pass_fail
    - authorization_decision
    - memory_mutation
    - db_query
    """

    review_findings: list[ReviewFinding]
    risk_findings: list[RiskFinding]
    proposed_claims: list[ProposedClaim] = Field(default_factory=list)
    requested_actions: list[RequestedAction] = Field(default_factory=list)
    review_manifest: dict[str, Any] = Field(default_factory=dict)


# -----------------------------------------------------------------------------
# ARCHIVIST RETRIEVAL CONTRACT
# -----------------------------------------------------------------------------

class RetrievalRequestPayload(ContractModel):
    query_text: str
    purpose: str

    target_resource_type: ResourceType
    target_resource_id: UUID | None = None

    allowed_states: list[Literal["ACTIVE", "APPROVED", "SEALED", "SUPERSEDED", "RETRACTED"]] = Field(
        default_factory=lambda: ["ACTIVE", "APPROVED", "SEALED"]
    )

    max_items: int = Field(default=12, ge=1, le=25)
    max_tokens: int = Field(default=8000, ge=1, le=20000)

    required_sensitivity_ceiling: SensitivityLevel = "SENSITIVE_INTERNAL"


class EvidenceItem(ContractModel):
    evidence_id: UUID
    applied_as_entity_id: UUID

    citation_anchor: CitationAnchor
    content_excerpt: str
    content_hash: str

    source_document_id: UUID
    source_snapshot_id: UUID | None = None

    state: Literal["ACTIVE", "APPROVED", "SEALED"]
    sensitivity_level: SensitivityLevel

    token_count: int = Field(..., ge=0)


class RetrievalBundle(ContractModel):
    retrieval_bundle_id: UUID
    request_id: UUID
    correlation_id: UUID
    applied_as_entity_id: UUID

    query_text_hash: str

    items: list[EvidenceItem]

    retrieval_order_proof: list[Literal[
        "SQL_APPLIED_AS_PREFILTER",
        "STATE_FILTER",
        "SENSITIVITY_CUSTODY_FILTER",
        "VECTOR_SEARCH",
    ]]

    max_items: int = Field(..., ge=1, le=25)
    max_tokens: int = Field(..., ge=1, le=20000)
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")
        return value

    @model_validator(mode="after")
    def validate_retrieval_order_and_bounds(self) -> "RetrievalBundle":
        expected = [
            "SQL_APPLIED_AS_PREFILTER",
            "STATE_FILTER",
            "SENSITIVITY_CUSTODY_FILTER",
            "VECTOR_SEARCH",
        ]
        if self.retrieval_order_proof != expected:
            raise ValueError("retrieval_order_proof must match canonical Archivist order")

        if len(self.items) > self.max_items:
            raise ValueError("retrieval bundle exceeds max_items")

        if sum(item.token_count for item in self.items) > self.max_tokens:
            raise ValueError("retrieval bundle exceeds max_tokens")

        for item in self.items:
            if item.applied_as_entity_id != self.applied_as_entity_id:
                raise ValueError("retrieval bundle contains cross-boundary evidence item")

        return self


# -----------------------------------------------------------------------------
# MEMORY / SNAPSHOT CONTRACT
# -----------------------------------------------------------------------------

class ImmutableSnapshot(ContractModel):
    snapshot_id: UUID
    subject_id: UUID
    subject_type: Literal[
        "MEMORY_RECORD",
        "EVIDENCE",
        "SECTION",
        "DRAFT",
        "PACKET",
        "AUTHORIZATION",
    ]

    applied_as_entity_id: UUID

    canonical_payload: dict[str, Any]
    canonical_payload_hash: str

    previous_snapshot_id: UUID | None = None
    chain_hash: str

    created_by_state_machine_run_id: UUID
    created_at: datetime

    signature_alg: Literal["Ed25519"]
    signature: str

    @field_validator("created_at")
    @classmethod
    def snapshot_created_at_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")
        return value


class MemoryRecord(ContractModel):
    memory_id: UUID
    applied_as_entity_id: UUID

    state: MemoryState
    record_type: str

    current_snapshot_id: UUID

    supersedes_memory_id: UUID | None = None
    superseded_by_memory_id: UUID | None = None

    created_by_state_machine_run_id: UUID
    created_at: datetime
    updated_at: datetime | None = None


class StateMachineContext(ContractModel):
    state_machine_run_id: UUID
    request_id: UUID
    correlation_id: UUID
    identity_context: IdentityContext
    authorized_transition: str
    pre_commit_gate_result: GateResult

    @model_validator(mode="after")
    def require_state_machine_actor(self) -> "StateMachineContext":
        if self.identity_context.actor_type != "STATE_MACHINE_RUNNER":
            raise ValueError("Memory mutation requires STATE_MACHINE_RUNNER actor")
        return self


# -----------------------------------------------------------------------------
# MODEL ACCESS BOUNDARY CONTRACT
# -----------------------------------------------------------------------------

class RouteAuthorization(ContractModel):
    route_mode: RouteMode

    authorized_by_principal_id: UUID | None = None
    authorized_at: datetime | None = None

    explicit_customer_authorization: bool = False

    allowed_frontier_vendors: list[str] = Field(default_factory=list)
    allowed_model_ids: list[str] = Field(default_factory=list)

    max_sensitivity_to_frontier: SensitivityLevel

    authorization_snapshot_id: UUID | None = None

    @model_validator(mode="after")
    def all_model_access_requires_explicit_authorization(self) -> "RouteAuthorization":
        if self.route_mode == "ALL_MODEL_ACCESS":
            if not self.explicit_customer_authorization:
                raise ValueError("ALL_MODEL_ACCESS requires explicit_customer_authorization")
            if self.authorized_by_principal_id is None:
                raise ValueError("ALL_MODEL_ACCESS requires authorized_by_principal_id")
            if self.authorized_at is None:
                raise ValueError("ALL_MODEL_ACCESS requires authorized_at")
            if self.authorization_snapshot_id is None:
                raise ValueError("ALL_MODEL_ACCESS requires authorization_snapshot_id")
        return self


class ModelInvocationPayload(ContractModel):
    model_task: Literal[
        "INTENT_PARSE",
        "DRAFT",
        "REVIEW",
        "STRUCTURAL_PLAN",
        "LOCAL_COMPLETION",
    ]
    route_mode: RouteMode
    prompt_manifest: dict[str, Any]
    retrieval_bundle: RetrievalBundle | None = None
    route_authorization: RouteAuthorization


class ModelInvocationResult(ContractModel):
    model_invocation_id: UUID
    route_mode: RouteMode

    model_id: str
    vendor: str | None
    local: bool

    outbound_payload_hash: str
    inbound_result_hash: str

    result_payload: dict[str, Any]
    audit_event_id: UUID


# -----------------------------------------------------------------------------
# AUDIT CONTRACT
# -----------------------------------------------------------------------------

AuditEventType = Literal[
    "REQUEST_ACCEPTED",
    "REQUEST_REJECTED",
    "GATE_RESULT",
    "MODEL_INVOCATION",
    "RETRIEVAL_BUNDLE_CREATED",
    "MEMORY_MUTATION",
    "EVIDENCE_PROMOTION",
    "PACKET_PREPARED",
    "FINAL_PACKET_AUTHORIZED",
    "PACKET_EXPORTED",
    "CONTRACT_VIOLATION",
]


class AuditEvent(ContractModel):
    audit_event_id: UUID
    event_type: AuditEventType

    request_id: UUID | None = None
    correlation_id: UUID | None = None

    applied_as_entity_id: UUID | None = None
    principal_id: UUID | None = None
    actor_type: ActorType | None = None

    operation_type: OperationType | None = None
    target: OperationTarget | None = None

    event_payload: dict[str, Any]
    event_payload_hash: str

    snapshot_ids: list[UUID] = Field(default_factory=list)
    gate_result_id: UUID | None = None

    previous_audit_event_hash: str | None = None
    audit_chain_hash: str

    created_at: datetime

    signature_alg: Literal["Ed25519"]
    signature: str

    @model_validator(mode="after")
    def forbid_live_ref_audit_proof(self) -> "AuditEvent":
        def contains_live_ref(value: Any) -> bool:
            if isinstance(value, dict):
                for key, nested in value.items():
                    if key == "$ref" and isinstance(nested, str):
                        if "live" in nested or "current" in nested:
                            return True
                    if contains_live_ref(nested):
                        return True
            elif isinstance(value, list):
                return any(contains_live_ref(item) for item in value)
            return False

        if contains_live_ref(self.event_payload):
            raise ValueError("audit proof may not contain live `$ref` joins")

        return self
