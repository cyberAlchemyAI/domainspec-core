from datetime import datetime, timezone
from pipeline.nervous_system.models import CurrentProjectionResponse
from pipeline.nervous_system.event_append_boundary import (
    EventAppendRequest,
    EventAppendReceipt,
    EventAppendStatus,
)

def evaluate_event_policy(
    request: EventAppendRequest,
    current_projection: CurrentProjectionResponse,
) -> EventAppendReceipt:
    """
    Evaluates an EventAppendRequest against the CurrentProjectionResponse
    to enforce Policy, Identity, Posture, and Sync boundaries.
    """

    # 1. Identity Boundary (Operator Check)
    if not current_projection.operator:
        return EventAppendReceipt(
            append_request_id=request.append_request_id,
            source_proposal_id=request.source_proposal_id,
            status=EventAppendStatus.REJECTED_BY_IDENTITY_BOUNDARY,
            reviewed_at=datetime.now(timezone.utc),
            reason="Current projection has no operator."
        )
    if current_projection.operator.user_id != request.operator_id:
        return EventAppendReceipt(
            append_request_id=request.append_request_id,
            source_proposal_id=request.source_proposal_id,
            status=EventAppendStatus.REJECTED_BY_IDENTITY_BOUNDARY,
            reviewed_at=datetime.now(timezone.utc),
            reason=f"Operator mismatch. Request: {request.operator_id}, Projection: {current_projection.operator.user_id}"
        )

    # 2. Posture Check
    if not current_projection.posture:
        return EventAppendReceipt(
            append_request_id=request.append_request_id,
            source_proposal_id=request.source_proposal_id,
            status=EventAppendStatus.REJECTED_BY_POSTURE,
            reviewed_at=datetime.now(timezone.utc),
            reason="Current projection has no posture."
        )
    if current_projection.posture.mode != request.posture_at_request:
        return EventAppendReceipt(
            append_request_id=request.append_request_id,
            source_proposal_id=request.source_proposal_id,
            status=EventAppendStatus.REJECTED_BY_POSTURE,
            reviewed_at=datetime.now(timezone.utc),
            reason=f"Posture mismatch. Request: {request.posture_at_request}, Projection: {current_projection.posture.mode}"
        )

    # 3. Sync/Stale Check
    if not current_projection.audit_state:
        return EventAppendReceipt(
            append_request_id=request.append_request_id,
            source_proposal_id=request.source_proposal_id,
            status=EventAppendStatus.REJECTED_BY_STALE_PROJECTION,
            reviewed_at=datetime.now(timezone.utc),
            reason="Current projection has no audit_state."
        )
    if current_projection.audit_state.last_verified_event_id != request.last_verified_event_id:
        return EventAppendReceipt(
            append_request_id=request.append_request_id,
            source_proposal_id=request.source_proposal_id,
            status=EventAppendStatus.REJECTED_BY_SYNC_CONFLICT,
            reviewed_at=datetime.now(timezone.utc),
            reason=f"Sync conflict. Request last verified: {request.last_verified_event_id}, Projection last verified: {current_projection.audit_state.last_verified_event_id}"
        )

    # 4. Ceremony Check
    if request.requires_signature_ceremony:
        return EventAppendReceipt(
            append_request_id=request.append_request_id,
            source_proposal_id=request.source_proposal_id,
            status=EventAppendStatus.REQUIRES_SIGNATURE_CEREMONY,
            reviewed_at=datetime.now(timezone.utc),
            required_next_surface="SIGNATURE_CEREMONY"
        )

    return EventAppendReceipt(
        append_request_id=request.append_request_id,
        source_proposal_id=request.source_proposal_id,
        status=EventAppendStatus.APPEND_REQUEST_ACCEPTED_FOR_POLICY_REVIEW, # Or we could add an ACCEPTED_BY_POLICY status
        reviewed_at=datetime.now(timezone.utc),
        reason="Policy evaluation passed."
    )
