import json
import hashlib
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from pipeline.nervous_system.event_candidate_boundary import EventCandidate
from pipeline.nervous_system.models import CurrentProjectionResponse

class SignatureCeremonyRequest(BaseModel):
    candidate_hash: str
    canonical_preimage: str
    operator_id: str
    applied_as_entity_id: Optional[str] = None
    posture: str
    route_mode: Optional[str] = None
    event_family: str
    event_type: str
    signing_key_fingerprint: str
    ceremony_reason: str
    required_human_acknowledgments: List[str]
    signature_scope: str

    model_config = ConfigDict(extra="forbid")

class CeremonyPreparationRejectedError(Exception):
    pass

def build_signature_ceremony_request(
    candidate: EventCandidate,
    current_projection: CurrentProjectionResponse
) -> SignatureCeremonyRequest:
    """
    Converts an EventCandidate into a SignatureCeremonyRequest when eligible.
    Does NOT append, commit, sign, or mutate.
    """
    # Reject if projection is missing required objects
    if not current_projection.operator:
        raise CeremonyPreparationRejectedError("Current projection has no operator.")
    if not current_projection.posture:
        raise CeremonyPreparationRejectedError("Current projection has no posture.")
    if not current_projection.audit_state:
        raise CeremonyPreparationRejectedError("Current projection has no audit state.")

    # 1. Reject if operator_id, posture, route mode, applied-as entity, or sync epoch no longer match
    if current_projection.operator.user_id != candidate.operator_id:
        raise CeremonyPreparationRejectedError("Operator mismatch.")

    if not current_projection.operator.signing_key_fingerprint:
        raise CeremonyPreparationRejectedError("Missing signing key.")

    if current_projection.posture.mode != candidate.posture:
        raise CeremonyPreparationRejectedError("Posture mismatch.")

    if current_projection.audit_state.last_verified_event_id != candidate.last_verified_event_id:
        raise CeremonyPreparationRejectedError("Sync conflict / stale projection.")

    # 2. Reject if candidate hash/preimage is missing, malformed, or inconsistent.
    candidate_data = {
        "operator_id": candidate.operator_id,
        "applied_as_entity_id": candidate.applied_as_entity_id,
        "posture": candidate.posture,
        "route_mode": candidate.route_mode,
        "last_verified_event_id": candidate.last_verified_event_id,
        "current_projection_epoch": candidate.current_projection_epoch,
        "command_type": candidate.command_type,
        "event_family": candidate.event_family,
        "event_type": candidate.event_type,
        "payload": candidate.payload,
        "policy_receipt_status": candidate.policy_receipt_status.value,
        "policy_receipt_reason": candidate.policy_receipt_reason,
    }
    canonical_json = json.dumps(candidate_data, sort_keys=True, separators=(',', ':'))
    computed_hash = hashlib.sha3_512(canonical_json.encode('utf-8')).hexdigest()

    if computed_hash != candidate.candidate_hash:
        raise CeremonyPreparationRejectedError("Candidate hash mismatch / malformed candidate.")

    # Determine reason, acknowledgments, and scope based on candidate
    ceremony_reason = "Standard Event Append Signature"
    required_human_acknowledgments = ["I authorize this action."]
    signature_scope = "Standard"

    # Explicit handling for Risk Overrides
    if candidate.event_type == "RISK_OVERRIDE" or candidate.event_family == "RISK_OVERRIDE":
        required_human_acknowledgments = required_human_acknowledgments + [
            "I acknowledge this override does not convert failed gates to PASS."
        ]
        ceremony_reason = "Risk Override Authorization"
        signature_scope = "Elevated/Risk Override"

    # Explicit handling for Final Packet Authorization / Export
    if candidate.event_type == "FINAL_PACKET_AUTHORIZATION" or candidate.event_family == "EXPORT":
        required_human_acknowledgments = required_human_acknowledgments + [
            "I authorize final packet export and boundary transmission."
        ]
        ceremony_reason = "Final Packet Export"
        signature_scope = "Strict/Export Boundary"

    return SignatureCeremonyRequest(
        candidate_hash=candidate.candidate_hash,
        canonical_preimage=canonical_json,
        operator_id=candidate.operator_id,
        applied_as_entity_id=candidate.applied_as_entity_id,
        posture=candidate.posture,
        route_mode=candidate.route_mode,
        event_family=candidate.event_family,
        event_type=candidate.event_type,
        signing_key_fingerprint=current_projection.operator.signing_key_fingerprint,
        ceremony_reason=ceremony_reason,
        required_human_acknowledgments=required_human_acknowledgments,
        signature_scope=signature_scope
    )
