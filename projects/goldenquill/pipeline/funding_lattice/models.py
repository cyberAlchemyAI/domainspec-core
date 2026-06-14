import json
from dataclasses import dataclass, field
from typing import List, Optional, Literal, Dict, Any

@dataclass
class Entity:
    entity_id: str
    display_name: str
    entity_type: str
    legal_status: str
    applicant_roles: List[str] = field(default_factory=list)
    identifiers: Dict[str, str] = field(default_factory=dict)
    authorization_requirements: List[str] = field(default_factory=list)
    permitted_routes: List[str] = field(default_factory=list)
    prohibited_routes: List[str] = field(default_factory=list)
    data_sensitivity_default: str = "Sensitive-Internal"
    guardrails: List[str] = field(default_factory=list)
    notes: str = ""

@dataclass
class RouteLock:
    route_status: str
    applied_as_entity_id: Optional[str] = None
    beneficiary_entity_id: Optional[str] = None
    sponsor_entity_id: Optional[str] = None
    route_type: Optional[str] = None
    authorization_record_required: bool = False
    authorization_record_present: bool = False
    route_blockers: List[str] = field(default_factory=list)

@dataclass
class PacketState:
    draft_ready: bool = False
    review_ready: bool = False
    export_staged: bool = False
    operator_authorization_required: bool = True
    operator_authorization_present: bool = False
    export_blocked: bool = True
    blockers: List[str] = field(default_factory=list)
    human_authority_note: str = "Final export and packet authorization remain entirely human-controlled."

@dataclass
class ContextBundleManifest:
    target_id: str
    applied_as_entity_id: Optional[str] = None
    beneficiary_entity_id: Optional[str] = None
    sponsor_entity_id: Optional[str] = None
    narrative_package_id: Optional[str] = None
    governance_profile_id: Optional[str] = None
    evidence_bundle_id: Optional[str] = None
    allowed_model_posture: Optional[str] = None
    source_notes: str = ""

@dataclass
class OpportunityTarget:
    opportunity_id: str
    title: str
    funder: str
    source_url: str
    verification_status: str
    deadline: str
    lifecycle_stage: str
    route_lock: RouteLock
    packet_state: PacketState
    eligible_applicant_types: List[str] = field(default_factory=list)
    required_documents: List[str] = field(default_factory=list)
    allowable_routes: List[str] = field(default_factory=list)
    fatal_gates: List[str] = field(default_factory=list)
    advisory_warnings: List[str] = field(default_factory=list)
    evidence_requirements: List[str] = field(default_factory=list)
    context_bundle_manifest: Optional[ContextBundleManifest] = None
