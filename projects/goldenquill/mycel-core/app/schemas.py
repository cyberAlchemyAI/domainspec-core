from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field, model_validator


class DataPosture(str, Enum):
    LOCAL_ONLY = "LOCAL_ONLY"
    HYBRID = "HYBRID"
    FULL_ACCESS = "FULL_ACCESS"


class ActorKind(str, Enum):
    HUMAN = "human"
    GEM = "gem"
    SYSTEM = "system"


class TopologyType(str, Enum):
    CHAIN = "chain"
    BROADCAST = "broadcast"
    DEBATE = "debate"
    CHORUS = "chorus"
    TOURNAMENT = "tournament"
    RECURSIVE_DEEPENING = "recursive_deepening"
    STAR_HUB = "star_hub"
    FISHBOWL = "fishbowl"


class LineageType(str, Enum):
    ORIGIN = "ORIGIN"
    DIVERGENT = "DIVERGENT"
    SEQUENTIAL = "SEQUENTIAL"
    SYNTHESIZED = "SYNTHESIZED"
    MUTATED = "MUTATED"
    FORKED = "FORKED"


class SystemStatus(str, Enum):
    ACTIVE = "active"
    RESOLVED_WITH_TENSION = "resolved_with_tension"
    UNRESOLVED_TENSIONS = "unresolved_tensions"
    HALTED = "halted"


class ResolutionStatus(str, Enum):
    CLEAN = "clean"
    RESOLVED_WITH_TENSION = "resolved_with_tension"
    CAPPED_BY_POSTURE = "capped_by_posture"
    CAPPED_BY_HARDWARE = "capped_by_hardware"


class GateResult(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    BLOCK = "BLOCK"


class EventType(str, Enum):
    DATABASE_BOOT = "DatabaseBootEvent"
    HUMAN_SEED = "HumanSeed"
    CONTROLLER_STATE_CHANGED = "ControllerStateChanged"
    TENSION = "TensionEvent"
    QUALITY_WARNING = "QualityCapabilityWarning"
    SYSTEM_CONTROL = "SystemControlEvent"
    THOUGHT = "ThoughtObject"
    SEMANTIC_DIFF = "SemanticThoughtDiff"
    SCORE = "ScoreEvent"
    GATE = "GateEvent"
    COMMIT = "CommitEvent"
    CARD_CREATED = "ProjectConceptCardCreated"
    GEM_STARTED = "GemInvocationStarted"
    GEM_COMPLETED = "GemInvocationCompleted"
    GEM_FAILED = "GemInvocationFailed"
    CONTRACT_VIOLATION = "ContractViolationEvent"
    ROUTE_ABORTED = "RouteAbortedEvent"


class Actor(BaseModel):
    kind: ActorKind
    actor_id: str


class MacroControls(BaseModel):
    maturity: float
    divergence: float
    grounding: float
    pressure: float


class StyleControls(BaseModel):
    voice: float = 0.5
    register: Optional[str] = None
    audience: Optional[str] = None


class HumanSeed(BaseModel):
    seed_id: UUID = Field(default_factory=uuid4)
    content: str


class ControllerState(BaseModel):
    model_config = ConfigDict(frozen=True)

    controller_state_id: UUID
    session_id: UUID
    supersedes_state_id: Optional[UUID] = None
    state_sequence_nonce: int

    correlation_id: Optional[UUID] = None
    input_gesture_id: Optional[UUID] = None
    source_surface: str = "browser"

    macro_controls: MacroControls
    data_posture: DataPosture

    selected_topology: TopologyType = TopologyType.CHAIN
    active_gem: Optional[str] = None
    system_status: SystemStatus = SystemStatus.ACTIVE
    resolution_status: ResolutionStatus = ResolutionStatus.CLEAN

    resolved_generation_params: Dict[str, Any] = Field(default_factory=dict)
    resolved_routing_params: Dict[str, Any] = Field(default_factory=dict)
    resolved_agent_weights: Dict[str, float] = Field(default_factory=dict)
    resolved_review_params: Dict[str, Any] = Field(default_factory=dict)

    is_tension_active: bool = False
    tension_event_ids: List[UUID] = Field(default_factory=list)


class TensionEvent(BaseModel):
    tension_id: UUID = Field(default_factory=uuid4)
    tension_type: str
    requested_vectors: Dict[str, Any]
    resolved_vectors: Dict[str, Any]


class ThoughtObject(BaseModel):
    thought_id: UUID
    session_id: UUID
    parent_ids: List[UUID]
    lineage_type: LineageType
    generated_by: str
    topology: TopologyType
    controller_state_id: UUID
    content: str
    summary: str


class SemanticThoughtDiff(BaseModel):
    diff_id: UUID = Field(default_factory=uuid4)
    thought_id: UUID
    vocabulary_shift: str
    strategic_reframing: str
    evidence_grounding: str
    risk_flags_added: str
    claims_softened: str
    anchors_added: str
    anchors_dropped: str


class ScoreEvent(BaseModel):
    score_id: UUID = Field(default_factory=uuid4)
    thought_id: UUID
    rubric_type: str
    novelty: float
    feasibility: float
    coherence: float
    development_potential: float
    resource_fit: float
    evidence_readiness: float
    risk: float

    @model_validator(mode="after")
    def validate_rubric(self):
        # We ensure forbidden fields are not present, which is natively handled by not having them in the model,
        # but just in case, we can enforce no extra fields. We can't really enforce what's not there,
        # but the prompt requires that the base rubric does not include them. 
        # The fields strictly exist as defined above.
        return self


class GateEvent(BaseModel):
    gate_id: UUID = Field(default_factory=uuid4)
    thought_id: UUID
    gate_type: str
    result: GateResult
    reason: str


class CommitEvent(BaseModel):
    actor: Actor
    selected_thought_id: UUID
    controller_state_id: UUID

    @model_validator(mode="after")
    def commit_must_be_human(self):
        if self.actor.kind != ActorKind.HUMAN:
            raise ValueError("CommitEvent.actor.kind must be 'human'")
        return self


class GemInvocationFailed(BaseModel):
    invocation_id: UUID
    gem_name: str
    error: str


class ContractViolationEvent(BaseModel):
    violation_id: UUID = Field(default_factory=uuid4)
    gem_name: str
    error: str
    attempted_payload: Dict[str, Any]


class HardwareCapabilityProfile(BaseModel):
    profile_id: UUID = Field(default_factory=uuid4)
    local_small_capable: bool
    local_large_capable: bool
    memory_gb: int


class QualityCapabilityWarning(BaseModel):
    warning_id: UUID = Field(default_factory=uuid4)
    message: str


class SystemControlEvent(BaseModel):
    control_id: UUID = Field(default_factory=uuid4)
    action: str  # halt_routing, pause_routing, etc.


class ProjectConceptCard(BaseModel):
    card_id: UUID
    schema_version: str = "1.0.0"
    created_from_session_id: UUID
    human_commit_event_id: UUID
    title: str
    human_seed: str
    committed_concept: str
    route_metadata: Dict[str, Any]
    project_context: str
    evidence_readiness: str
    risk_register: str
    next_actions: str
    tilth_handoff: Optional[Dict[str, Any]] = None


class EventEnvelope(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    seq: int = Field(..., ge=1)

    event_type: EventType
    schema_version: str = "1.0.0"
    ts: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    actor: Actor

    controller_state_id: Optional[UUID] = None
    parent_event_id: Optional[UUID] = None
    correlation_id: Optional[UUID] = None
    idempotency_key: Optional[str] = None

    prev_hash: Optional[str] = None
    event_hash: Optional[str] = None

    payload: Dict[str, Any]


class VisualProjectionFrame(BaseModel):
    session_id: UUID
    derived_from_seq: int
    last_updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    latest_controller_state_id: Optional[UUID] = None
    active_topology: Optional[TopologyType] = None
    system_status: SystemStatus = SystemStatus.ACTIVE
    resolved_agent_weights: Dict[str, float] = Field(default_factory=dict)
    
    visible_thought_ids: List[UUID] = Field(default_factory=list)
    score_badges: Dict[UUID, ScoreEvent] = Field(default_factory=dict)
    gate_badges: Dict[UUID, GateEvent] = Field(default_factory=dict)
    tension_badges: List[TensionEvent] = Field(default_factory=list)


class HydrationResponse(BaseModel):
    audit_cursor: int
    latest_visual_projection_frame: VisualProjectionFrame
