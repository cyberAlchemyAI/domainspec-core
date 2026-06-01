from datetime import datetime, timezone
import pytest
from pipeline.nervous_system.event_append_boundary import (
    EventAppendRequest,
    EventAppendReceipt,
    EventAppendStatus,
    EventAppendFamily
)
from pipeline.nervous_system.models import (
    CurrentProjectionResponse,
    ProjectionPosture,
    ProjectionOperator,
    ProjectionAuditState
)
from pipeline.nervous_system.event_candidate_boundary import (
    build_event_candidate,
    SignatureCeremonyRequiredError,
    CandidateAssemblyRejectedError
)
import ast

def get_base_request():
    return EventAppendRequest(
        append_request_id="req_123",
        source_proposal_id="prop_456",
        requested_family=EventAppendFamily.STEWARD_PROPOSAL,
        requested_event_type="PROPOSAL_APPROVED",
        operator_id="operator_789",
        posture_at_request="LOCAL_ONLY_SOVEREIGN",
        operator_review_summary="Looks good",
        rationale="Approved",
        requested_at=datetime.now(timezone.utc),
        last_verified_event_id="evt_001",
        payload_preview={"some_data": 42}
    )

def get_base_receipt():
    return EventAppendReceipt(
        append_request_id="req_123",
        source_proposal_id="prop_456",
        status=EventAppendStatus.APPEND_REQUEST_ACCEPTED_FOR_POLICY_REVIEW,
        reviewed_at=datetime.now(timezone.utc),
        reason="Looks good"
    )

def get_base_projection():
    return CurrentProjectionResponse(
        operator=ProjectionOperator(
            user_id="operator_789",
            display_name="Test Operator",
            role="admin",
            signing_key_fingerprint="fingerprint"
        ),
        posture=ProjectionPosture(
            mode="LOCAL_ONLY_SOVEREIGN",
            changed_mid_cycle=False,
            last_confirmed_by="operator_789",
            last_confirmed_at="2026-05-24T00:00:00Z",
            data_boundary_note="Local"
        ),
        audit_state=ProjectionAuditState(
            last_event="evt_001",
            signature_status="valid",
            last_verified_event_id="evt_001",
            lock_history_count=1,
            unsigned_change_count=0
        )
    )

def test_approved_receipt_creates_candidate():
    req = get_base_request()
    rec = get_base_receipt()
    proj = get_base_projection()

    candidate = build_event_candidate(req, rec, proj)

    assert candidate.operator_id == "operator_789"
    assert candidate.posture == "LOCAL_ONLY_SOVEREIGN"
    assert candidate.last_verified_event_id == "evt_001"
    assert candidate.candidate_hash is not None
    assert candidate.payload == {"some_data": 42}

def test_rejected_receipt_refuses_candidate():
    req = get_base_request()
    rec = get_base_receipt()
    rec.status = EventAppendStatus.REJECTED_BY_POLICY
    proj = get_base_projection()

    with pytest.raises(CandidateAssemblyRejectedError):
        build_event_candidate(req, rec, proj)

def test_ceremony_required_receipt_does_not_become_appendable():
    req = get_base_request()
    rec = get_base_receipt()
    rec.status = EventAppendStatus.REQUIRES_SIGNATURE_CEREMONY
    proj = get_base_projection()

    with pytest.raises(SignatureCeremonyRequiredError):
        build_event_candidate(req, rec, proj)

def test_stale_sync_conflict_refuses_candidate():
    req = get_base_request()
    req.last_verified_event_id = "evt_002" # Mismatch with projection "evt_001"
    rec = get_base_receipt()
    proj = get_base_projection()

    with pytest.raises(CandidateAssemblyRejectedError) as exc:
        build_event_candidate(req, rec, proj)
    assert "sync conflict" in str(exc.value).lower()

def test_posture_mismatch_cannot_be_normalized_away():
    req = get_base_request()
    req.posture_at_request = "FRONTIER_ELIGIBLE" # Mismatch with projection
    rec = get_base_receipt()
    proj = get_base_projection()

    with pytest.raises(CandidateAssemblyRejectedError) as exc:
        build_event_candidate(req, rec, proj)
    assert "posture mismatch" in str(exc.value).lower()

def test_operator_mismatch_cannot_be_normalized_away():
    req = get_base_request()
    req.operator_id = "other_operator" # Mismatch
    rec = get_base_receipt()
    proj = get_base_projection()

    with pytest.raises(CandidateAssemblyRejectedError) as exc:
        build_event_candidate(req, rec, proj)
    assert "operator mismatch" in str(exc.value).lower()

def test_candidate_hash_is_deterministic():
    req = get_base_request()
    rec = get_base_receipt()
    proj = get_base_projection()

    candidate1 = build_event_candidate(req, rec, proj)
    candidate2 = build_event_candidate(req, rec, proj)

    assert candidate1.candidate_hash == candidate2.candidate_hash

def test_source_inspection_pure_boundary():
    """Prove the module is a pure boundary with no side effects."""
    with open("pipeline/nervous_system/event_candidate_boundary.py") as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                assert node.func.id not in [
                    "append_event",
                    "commit",
                    "open",
                    "write",
                    "execute"
                ]
            elif isinstance(node.func, ast.Attribute):
                assert node.func.attr not in [
                    "append",
                    "commit",
                    "write",
                    "execute"
                ]
