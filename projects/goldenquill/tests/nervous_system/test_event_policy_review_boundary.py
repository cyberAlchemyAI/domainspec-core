import pytest
from datetime import datetime, timezone
from pipeline.nervous_system.event_append_boundary import (
    EventAppendRequest,
    EventAppendFamily,
    EventAppendStatus,
)
from pipeline.nervous_system.models import (
    CurrentProjectionResponse,
    ProjectionOperator,
    ProjectionPosture,
    ProjectionAuditState,
)
from pipeline.nervous_system.event_policy_review_boundary import evaluate_event_policy

def get_valid_request():
    return EventAppendRequest(
        append_request_id="ar-123",
        source_proposal_id="sp-123",
        requested_family=EventAppendFamily.STEWARD_PROPOSAL,
        requested_event_type="test",
        operator_id="op-123",
        posture_at_request="FRONTIER_ELIGIBLE",
        last_verified_event_id="ev-1",
        operator_review_summary="Looks good",
        rationale="Client requested it",
        requested_at=datetime.now(timezone.utc),
    )

def get_valid_projection():
    return CurrentProjectionResponse(
        operator=ProjectionOperator(
            user_id="op-123",
            display_name="Test Operator",
            role="Admin",
            signing_key_fingerprint="abc"
        ),
        posture=ProjectionPosture(
            mode="FRONTIER_ELIGIBLE",
            changed_mid_cycle=False,
            last_confirmed_by="op-123",
            last_confirmed_at="2026-05-24T00:00:00Z",
            data_boundary_note=""
        ),
        audit_state=ProjectionAuditState(
            last_event="ev-1",
            signature_status="valid",
            last_verified_event_id="ev-1",
            lock_history_count=0,
            unsigned_change_count=0
        )
    )

def test_evaluate_event_policy_accepts_valid_request():
    req = get_valid_request()
    proj = get_valid_projection()
    receipt = evaluate_event_policy(req, proj)
    assert receipt.status == EventAppendStatus.APPEND_REQUEST_ACCEPTED_FOR_POLICY_REVIEW

def test_evaluate_event_policy_rejects_identity_mismatch():
    req = get_valid_request()
    req.operator_id = "op-999" # Mismatch
    proj = get_valid_projection()
    receipt = evaluate_event_policy(req, proj)
    assert receipt.status == EventAppendStatus.REJECTED_BY_IDENTITY_BOUNDARY

def test_evaluate_event_policy_rejects_missing_operator():
    req = get_valid_request()
    proj = get_valid_projection()
    proj.operator = None
    receipt = evaluate_event_policy(req, proj)
    assert receipt.status == EventAppendStatus.REJECTED_BY_IDENTITY_BOUNDARY

def test_evaluate_event_policy_rejects_posture_mismatch():
    req = get_valid_request()
    req.posture_at_request = "LOCAL_ONLY_SOVEREIGN" # Mismatch
    proj = get_valid_projection()
    receipt = evaluate_event_policy(req, proj)
    assert receipt.status == EventAppendStatus.REJECTED_BY_POSTURE

def test_evaluate_event_policy_rejects_missing_posture():
    req = get_valid_request()
    proj = get_valid_projection()
    proj.posture = None
    receipt = evaluate_event_policy(req, proj)
    assert receipt.status == EventAppendStatus.REJECTED_BY_POSTURE

def test_evaluate_event_policy_rejects_sync_conflict():
    req = get_valid_request()
    req.last_verified_event_id = "ev-stale" # Mismatch
    proj = get_valid_projection()
    receipt = evaluate_event_policy(req, proj)
    assert receipt.status == EventAppendStatus.REJECTED_BY_SYNC_CONFLICT

def test_evaluate_event_policy_rejects_stale_projection():
    req = get_valid_request()
    proj = get_valid_projection()
    proj.audit_state = None
    receipt = evaluate_event_policy(req, proj)
    assert receipt.status == EventAppendStatus.REJECTED_BY_STALE_PROJECTION

def test_evaluate_event_policy_ceremony_check():
    req = get_valid_request()
    req.requires_signature_ceremony = True
    proj = get_valid_projection()
    receipt = evaluate_event_policy(req, proj)
    assert receipt.status == EventAppendStatus.REQUIRES_SIGNATURE_CEREMONY
    assert receipt.required_next_surface == "SIGNATURE_CEREMONY"

def test_module_source_has_no_execution_logic():
    from pathlib import Path
    import pipeline.nervous_system.event_policy_review_boundary as module

    src = Path(module.__file__).read_text()
    forbidden_tokens = [
        "db.commit",
        "ledger.append",
        "append_event",
        "write_event",
        "open(",
        "requests.post",
        "subprocess",
        "portal_submit"
    ]
    for token in forbidden_tokens:
        assert token not in src, f"Forbidden token {token} found in module source"
