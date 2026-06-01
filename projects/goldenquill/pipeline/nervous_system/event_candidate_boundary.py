import json
import hashlib
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict
from pipeline.nervous_system.event_append_boundary import (
    EventAppendRequest,
    EventAppendReceipt,
    EventAppendStatus,
    EVENT_APPEND_FORBIDDEN_FIELDS,
)
from pipeline.nervous_system.models import CurrentProjectionResponse

class EventCandidate(BaseModel):
    operator_id: str
    applied_as_entity_id: Optional[str] = None
    posture: str
    route_mode: Optional[str] = None
    last_verified_event_id: Optional[str] = None
    current_projection_epoch: Optional[str] = None
    command_type: str
    event_family: str
    event_type: str
    payload: dict[str, Any]
    policy_receipt_status: EventAppendStatus
    policy_receipt_reason: Optional[str] = None
    candidate_hash: str

    model_config = ConfigDict(extra="forbid")

class SignatureCeremonyRequiredError(Exception):
    """Raised when an EventCandidate requires a signature ceremony before append."""
    pass

class CandidateAssemblyRejectedError(Exception):
    """Raised when policy receipt is not append-eligible or validation fails."""
    pass

def build_event_candidate(
    request: EventAppendRequest,
    review_receipt: EventAppendReceipt,
    current_projection: CurrentProjectionResponse
) -> EventCandidate:
    """
    Creates an immutable EventCandidate/preimage from a request, receipt, and projection.
    """
    # 1. Reject candidate assembly unless policy receipt is explicitly append-eligible.
    if review_receipt.status == EventAppendStatus.REQUIRES_SIGNATURE_CEREMONY:
        raise SignatureCeremonyRequiredError("Signature ceremony required.")

    if review_receipt.status != EventAppendStatus.APPEND_REQUEST_ACCEPTED_FOR_POLICY_REVIEW:
        raise CandidateAssemblyRejectedError(f"Receipt status {review_receipt.status.value} is not append-eligible.")

    # Validate against projection explicitly
    if current_projection.posture is not None:
        if current_projection.posture.mode != request.posture_at_request:
            raise CandidateAssemblyRejectedError("Posture mismatch cannot be normalized away.")

    if current_projection.operator is not None:
        if current_projection.operator.user_id != request.operator_id:
            raise CandidateAssemblyRejectedError("Operator mismatch cannot be normalized away.")

    last_verified_event_id = request.last_verified_event_id
    if current_projection.audit_state is not None:
        if current_projection.audit_state.last_verified_event_id != request.last_verified_event_id:
            raise CandidateAssemblyRejectedError("Stale/sync conflict: last_verified_event_id mismatch.")
        last_verified_event_id = current_projection.audit_state.last_verified_event_id

    # Enforce payload cleanliness
    payload = dict(request.payload_preview)
    forbidden = EVENT_APPEND_FORBIDDEN_FIELDS.intersection(payload.keys())
    if forbidden:
        raise CandidateAssemblyRejectedError(f"Payload contains forbidden execution fields: {sorted(forbidden)}")

    # Route mode logic (from identity context/models if available, but usually null in Request)
    route_mode = None

    candidate_data = {
        "operator_id": request.operator_id,
        "applied_as_entity_id": request.applied_as_entity_id,
        "posture": request.posture_at_request,
        "route_mode": route_mode,
        "last_verified_event_id": last_verified_event_id,
        "current_projection_epoch": request.read_model_epoch,
        "command_type": request.requested_event_type,
        "event_family": request.requested_family.value,
        "event_type": request.requested_event_type,
        "payload": payload,
        "policy_receipt_status": review_receipt.status.value,
        "policy_receipt_reason": review_receipt.reason,
    }

    canonical_json = json.dumps(candidate_data, sort_keys=True, separators=(',', ':'))
    candidate_hash = hashlib.sha3_512(canonical_json.encode('utf-8')).hexdigest()

    return EventCandidate(
        operator_id=candidate_data["operator_id"],
        applied_as_entity_id=candidate_data["applied_as_entity_id"],
        posture=candidate_data["posture"],
        route_mode=candidate_data["route_mode"],
        last_verified_event_id=candidate_data["last_verified_event_id"],
        current_projection_epoch=candidate_data["current_projection_epoch"],
        command_type=candidate_data["command_type"],
        event_family=candidate_data["event_family"],
        event_type=candidate_data["event_type"],
        payload=candidate_data["payload"],
        policy_receipt_status=review_receipt.status,
        policy_receipt_reason=candidate_data["policy_receipt_reason"],
        candidate_hash=candidate_hash,
    )
