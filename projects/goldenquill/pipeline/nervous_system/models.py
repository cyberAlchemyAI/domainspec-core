from enum import Enum
from typing import Optional, Dict, Any, List, Literal
from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime

class RouteMode(str, Enum):
    LOCAL_ONLY = "LOCAL_ONLY"
    HYBRID_PUBLIC_FRONTIER_LOCAL_VAULT = "HYBRID_PUBLIC_FRONTIER_LOCAL_VAULT"
    ALL_MODEL_ACCESS = "ALL_MODEL_ACCESS"

class IdentityContext(BaseModel):
    user_id: str
    applied_as: str
    token_validity: bool = True
    is_human: bool = False
    origin: Literal["human_direct", "conversation_agent", "scheduled", "system"] = "system"

class BaseRequestEnvelope(BaseModel):
    identity_context: Optional[IdentityContext] = None
    correlation_id: Optional[str] = None

class CommandRequest(BaseRequestEnvelope):
    applied_as_entity_id: str
    command_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)

class ActionRequest(BaseRequestEnvelope):
    action: str
    label: str
    route_mode: Optional[str] = None
    applied_as_entity_id: Optional[str] = None
    operation_intent: Optional[str] = None

class BaseResponseEnvelope(BaseModel):
    status: str
    reason: Optional[str] = None

class ScoutRescanRequest(BaseRequestEnvelope):
    applied_as_entity_id: Optional[str] = None
    operation_intent: Optional[str] = None
    human_actor_id: Optional[str] = None

class ScoutRescanResponse(BaseModel):
    ok: bool = True
    scout_pipeline: list = Field(default_factory=list)
    scout_totals: Dict[str, Any] = Field(default_factory=dict)
    meta: Optional[Dict[str, Any]] = None
    scout_reality_report: Optional[Dict[str, Any]] = None

# --- Projection Hardening Models ---

class ProjectionNode(BaseModel):
    node_id: str
    node_name: str
    organization_slug: str
    machine_fingerprint: str
    local_status: str
    network_mode: str
    model_config = ConfigDict(extra="allow")

class ProjectionOperator(BaseModel):
    user_id: str
    display_name: str
    role: str
    signing_key_fingerprint: str
    model_config = ConfigDict(extra="allow")

class ProjectionPosture(BaseModel):
    mode: str
    changed_mid_cycle: bool
    last_confirmed_by: str
    last_confirmed_at: str
    data_boundary_note: str
    model_config = ConfigDict(extra="allow")

class ProjectionAuditState(BaseModel):
    last_event: str
    signature_status: str
    last_verified_event_id: str
    lock_history_count: int
    unsigned_change_count: int
    model_config = ConfigDict(extra="allow")

class ProjectionCycle(BaseModel):
    cycle_id: str
    status: str
    created_at: str
    updated_at: str
    active_surface: str
    scribe_access: str
    model_config = ConfigDict(extra="allow")

class LogicianGate(BaseModel):
    gate_id: str
    gate_class: str
    description: str
    verdict: str
    evidence_ref: Optional[str] = None
    source_excerpt: Optional[str] = None
    operator_warning: Optional[str] = None
    remediation: Optional[str] = None
    blocks_scribe: bool
    model_config = ConfigDict(extra="allow")

class ProjectionOverride(BaseModel):
    state: str
    allowed: bool
    copy_text: str = Field(alias="copy")
    required_fields: List[str]
    model_config = ConfigDict(extra="allow")

class BlockerOutreachTask(BaseModel):
    task_id: str
    blocker_id: str
    title: str
    owner_name: str
    owner_role: str
    owner_email: str
    severity: str
    route: str
    due_label: str
    email_subject: str
    email_body: str
    model_config = ConfigDict(extra="allow")

class LeaseState(BaseModel):
    status: str
    current_lease_owner: Optional[str] = None
    is_leased_by_me: bool
    locked_by_gate_id: Optional[str] = None
    model_config = ConfigDict(extra="allow")

class DraftSection(BaseModel):
    section_id: str
    title: str
    content: str
    lease_state: LeaseState
    eligibility_risk_mark: bool
    signature_status: str
    autosave_status: str
    conjecture_count: int
    evidence_links: List[str]
    model_config = ConfigDict(extra="allow")

class BudgetViolation(BaseModel):
    rule_id: str
    severity: str
    message: str
    model_config = ConfigDict(extra="allow")

class BudgetLineItem(BaseModel):
    line_id: str
    category: str
    description: str
    requested_amount: float
    match_amount: float
    source_evidence: str
    model_config = ConfigDict(extra="allow")

class ProjectionBudget(BaseModel):
    currency: str
    max_request: float
    requested_total: float
    match_required: bool
    validation_state: str
    violations: List[BudgetViolation]
    line_items: List[BudgetLineItem]
    model_config = ConfigDict(extra="allow")

class JudgeReviewer(BaseModel):
    reviewer_id: str
    label: str
    score: float
    max_score: float
    status: str
    rationale: str
    model_config = ConfigDict(extra="allow")

class JudgeCriterion(BaseModel):
    criterion_id: str
    label: str
    score: float
    max_score: float
    weight: float
    evidence_tier: str
    rationale: str
    model_config = ConfigDict(extra="allow")

class ProjectionJudge(BaseModel):
    score_state: str
    stale_reason: str
    predicted_score: float
    max_score: float
    reviewers: List[JudgeReviewer]
    criteria: List[JudgeCriterion]
    model_config = ConfigDict(extra="allow")

class RedTeamProbe(BaseModel):
    probe_id: str
    label: str
    verdict: str
    severity: str
    attack_vector: str
    required_response: Optional[str] = None
    model_config = ConfigDict(extra="allow")

class ProjectionRedTeam(BaseModel):
    status: str
    probes: List[RedTeamProbe]
    model_config = ConfigDict(extra="allow")

class EvidenceConflict(BaseModel):
    conflict_id: str
    description: str
    requires_operator_resolution: bool
    model_config = ConfigDict(extra="allow")

class EvidenceItem(BaseModel):
    evidence_id: str
    title: str
    filename: str
    classification: str
    commit_state: str
    hash: str
    linked_claims: List[str]
    conflicts: Optional[List[EvidenceConflict]] = None
    model_config = ConfigDict(extra="allow")

class ModuleMapItem(BaseModel):
    section_id: str
    title: str
    word_limit: int
    rubric_weight: float
    required_evidence: List[str]
    sensitivity: str
    recommended_posture: str
    model_config = ConfigDict(extra="allow")

# --- End Projection Hardening Models ---

class CurrentProjectionResponse(BaseModel):
    node: Optional[ProjectionNode] = None
    operator: Optional[ProjectionOperator] = None
    cycle: Optional[ProjectionCycle] = None
    posture: Optional[ProjectionPosture] = None
    audit_state: Optional[ProjectionAuditState] = None
    logician_gates: Optional[List[LogicianGate]] = None
    override: Optional[ProjectionOverride] = None
    blocker_outreach_tasks: Optional[List[BlockerOutreachTask]] = None

    draft_sections: Optional[List[DraftSection]] = None
    budget: Optional[ProjectionBudget] = None
    judge: Optional[ProjectionJudge] = None
    red_team: Optional[ProjectionRedTeam] = None
    evidence_items: Optional[List[EvidenceItem]] = None
    module_map: Optional[List[ModuleMapItem]] = None

    scout_pipeline: Optional[list] = None
    meta: Optional[Dict[str, Any]] = None
    participants: Optional[list] = None
    annotations: Optional[list] = None
    audit_events: Optional[list] = None
    amendments: Optional[list] = None
    ui_test_routes: Optional[list] = None
    node_sync: Optional[Dict[str, Any]] = None
    quarantine_items: Optional[list] = None
    portal_staging: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="allow")

# --- Steward Command Proposal Contract ---

class StewardProposalStatus(str, Enum):
    PENDING_OPERATOR_REVIEW = "PENDING_OPERATOR_REVIEW"
    ACCEPTED_FOR_DISPATCH = "ACCEPTED_FOR_DISPATCH"
    REJECTED_BY_OPERATOR = "REJECTED_BY_OPERATOR"
    REJECTED_BY_POLICY = "REJECTED_BY_POLICY"
    EXPIRED = "EXPIRED"
    SUPERSEDED = "SUPERSEDED"


class StewardProposalSource(str, Enum):
    TEXT = "TEXT"
    VOICE_TRANSCRIPT = "VOICE_TRANSCRIPT"
    SYSTEM_NARRATION = "SYSTEM_NARRATION"
    OPERATOR_SELECTION = "OPERATOR_SELECTION"


class StewardRiskClass(str, Enum):
    LOW = "LOW"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    POLICY_SENSITIVE = "POLICY_SENSITIVE"
    FORBIDDEN = "FORBIDDEN"


class StewardAllowedCommand(str, Enum):
    OPEN_ROUTE = "open_route"
    GENERATE_EMAIL_DRAFT = "generate_email_draft"
    SUMMARIZE_AUDIT = "summarize_audit"
    EXPLAIN_GATE = "explain_gate"
    PREPARE_RISK_OVERRIDE_RATIONALE = "prepare_risk_override_rationale"
    PREPARE_EVIDENCE_REQUEST = "prepare_evidence_request"
    PREPARE_CLAIM_AMENDMENT = "prepare_claim_amendment"
    PREPARE_SECTION_DRAFT_REQUEST = "prepare_section_draft_request"
    PREPARE_BUDGET_RECHECK = "prepare_budget_recheck"
    PREPARE_RESCORE_REQUEST = "prepare_rescore_request"


class StewardCommandProposal(BaseModel):
    proposal_id: str
    proposed_by: Literal["STEWARD"] = "STEWARD"

    proposed_command: StewardAllowedCommand

    proposal_source: StewardProposalSource
    transcript_id: Optional[str] = None

    cycle_id: Optional[str] = None
    source_route: Optional[str] = None
    target_route: Optional[str] = None
    target_artifact_id: Optional[str] = None
    target_gate_ids: list[str] = Field(default_factory=list)
    target_section_ids: list[str] = Field(default_factory=list)
    target_evidence_ids: list[str] = Field(default_factory=list)

    applied_as_entity_id: Optional[str] = None
    licensed_node_id: Optional[str] = None
    posture_at_creation: str
    read_model_epoch: Optional[str] = None
    last_verified_event_id: Optional[str] = None
    source_event_ids: list[str] = Field(default_factory=list)

    operator_review_summary: str
    rationale: str
    policy_basis: list[str] = Field(default_factory=list)

    risk_class: StewardRiskClass = StewardRiskClass.REVIEW_REQUIRED
    requires_operator_review: Literal[True] = True
    requires_signature: bool = False
    dispatch_allowed: bool = False

    payload_schema_version: str = "0.1.0"
    payload: Dict[str, Any] = Field(default_factory=dict)
    payload_hash: Optional[str] = None

    status: StewardProposalStatus = StewardProposalStatus.PENDING_OPERATOR_REVIEW
    created_at: datetime
    expires_at: Optional[datetime] = None

    model_config = ConfigDict(extra="forbid")

class StewardProposalSubmissionRequest(BaseRequestEnvelope):
    proposal: StewardCommandProposal


class CommandDispatchStatus(str, Enum):
    ACCEPTED_FOR_HANDLER_REVIEW = "ACCEPTED_FOR_HANDLER_REVIEW"
    REJECTED_BY_POLICY = "REJECTED_BY_POLICY"
    REJECTED_BY_IDENTITY_BOUNDARY = "REJECTED_BY_IDENTITY_BOUNDARY"
    REJECTED_BY_POSTURE = "REJECTED_BY_POSTURE"
    REJECTED_BY_APPLIED_AS_BOUNDARY = "REJECTED_BY_APPLIED_AS_BOUNDARY"
    REJECTED_BY_STALE_PROJECTION = "REJECTED_BY_STALE_PROJECTION"
    REJECTED_BY_SYNC_CONFLICT = "REJECTED_BY_SYNC_CONFLICT"
    REJECTED_BY_UNKNOWN_PROPOSAL = "REJECTED_BY_UNKNOWN_PROPOSAL"
    REQUIRES_SIGNATURE_CEREMONY = "REQUIRES_SIGNATURE_CEREMONY"


class CommandDispatchIntent(BaseRequestEnvelope):
    proposal_id: str
    proposal_status_at_acceptance: Literal["ACCEPTED_FOR_DISPATCH"]
    proposal_payload_hash: Optional[str] = None
    accepted_at: datetime
    operator_acceptance_signature: Optional[str] = None
    override_rationale: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class CommandDispatchReceipt(BaseModel):
    receipt_id: str
    proposal_id: str
    status: CommandDispatchStatus
    handler_assigned: Optional[str] = None
    reviewed_at: datetime
    error_message: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

class StewardHandlerFamily(str, Enum):
    NAVIGATION = "NAVIGATION"
    COMMUNICATION_DRAFT = "COMMUNICATION_DRAFT"
    AUDIT_EXPLANATION = "AUDIT_EXPLANATION"
    GATE_EXPLANATION = "GATE_EXPLANATION"
    RISK_RATIONALE_PREP = "RISK_RATIONALE_PREP"
    EVIDENCE_REQUEST_PREP = "EVIDENCE_REQUEST_PREP"
    CLAIM_AMENDMENT_PREP = "CLAIM_AMENDMENT_PREP"
    DRAFT_REQUEST_PREP = "DRAFT_REQUEST_PREP"
    BUDGET_RECHECK_PREP = "BUDGET_RECHECK_PREP"
    RESCORE_REQUEST_PREP = "RESCORE_REQUEST_PREP"

STEWARD_FORBIDDEN_OUTPUTS = {
    "event_id",
    "signature_event_id",
    "lock_id",
    "export_id",
    "submitted_at",
    "artifact_hash",
    "operator_signature_event_id",
    "canonical_mutation_result",
}

class StewardCommandRegistryEntry(BaseModel):
    command: StewardAllowedCommand
    handler_family: StewardHandlerFamily
    default_risk_class: StewardRiskClass
    required_context_fields: list[str] = Field(default_factory=list)
    allowed_target_fields: list[str] = Field(default_factory=list)
    may_require_signature_ceremony: bool = False
    dispatch_review_allowed: Literal[True] = True
    forbidden_outputs: list[str] = Field(
        default_factory=lambda: sorted(STEWARD_FORBIDDEN_OUTPUTS)
    )

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def require_forbidden_outputs(self):
        missing = STEWARD_FORBIDDEN_OUTPUTS.difference(self.forbidden_outputs)
        if missing:
            raise ValueError(f"registry entry missing forbidden outputs: {sorted(missing)}")
        return self

STEWARD_COMMAND_REGISTRY: tuple[StewardCommandRegistryEntry, ...] = (
    StewardCommandRegistryEntry(
        command=StewardAllowedCommand.OPEN_ROUTE,
        handler_family=StewardHandlerFamily.NAVIGATION,
        default_risk_class=StewardRiskClass.LOW,
    ),
    StewardCommandRegistryEntry(
        command=StewardAllowedCommand.GENERATE_EMAIL_DRAFT,
        handler_family=StewardHandlerFamily.COMMUNICATION_DRAFT,
        default_risk_class=StewardRiskClass.LOW,
    ),
    StewardCommandRegistryEntry(
        command=StewardAllowedCommand.SUMMARIZE_AUDIT,
        handler_family=StewardHandlerFamily.AUDIT_EXPLANATION,
        default_risk_class=StewardRiskClass.LOW,
    ),
    StewardCommandRegistryEntry(
        command=StewardAllowedCommand.EXPLAIN_GATE,
        handler_family=StewardHandlerFamily.GATE_EXPLANATION,
        default_risk_class=StewardRiskClass.LOW,
    ),
    StewardCommandRegistryEntry(
        command=StewardAllowedCommand.PREPARE_RISK_OVERRIDE_RATIONALE,
        handler_family=StewardHandlerFamily.RISK_RATIONALE_PREP,
        default_risk_class=StewardRiskClass.POLICY_SENSITIVE,
        may_require_signature_ceremony=True,
    ),
    StewardCommandRegistryEntry(
        command=StewardAllowedCommand.PREPARE_EVIDENCE_REQUEST,
        handler_family=StewardHandlerFamily.EVIDENCE_REQUEST_PREP,
        default_risk_class=StewardRiskClass.REVIEW_REQUIRED,
    ),
    StewardCommandRegistryEntry(
        command=StewardAllowedCommand.PREPARE_CLAIM_AMENDMENT,
        handler_family=StewardHandlerFamily.CLAIM_AMENDMENT_PREP,
        default_risk_class=StewardRiskClass.POLICY_SENSITIVE,
        may_require_signature_ceremony=True,
    ),
    StewardCommandRegistryEntry(
        command=StewardAllowedCommand.PREPARE_SECTION_DRAFT_REQUEST,
        handler_family=StewardHandlerFamily.DRAFT_REQUEST_PREP,
        default_risk_class=StewardRiskClass.REVIEW_REQUIRED,
    ),
    StewardCommandRegistryEntry(
        command=StewardAllowedCommand.PREPARE_BUDGET_RECHECK,
        handler_family=StewardHandlerFamily.BUDGET_RECHECK_PREP,
        default_risk_class=StewardRiskClass.REVIEW_REQUIRED,
    ),
    StewardCommandRegistryEntry(
        command=StewardAllowedCommand.PREPARE_RESCORE_REQUEST,
        handler_family=StewardHandlerFamily.RESCORE_REQUEST_PREP,
        default_risk_class=StewardRiskClass.REVIEW_REQUIRED,
    ),
)

STEWARD_COMMAND_REGISTRY_BY_COMMAND = {
    entry.command: entry for entry in STEWARD_COMMAND_REGISTRY
}
