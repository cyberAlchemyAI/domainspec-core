from datetime import datetime, timezone
import pytest
import ast
from pipeline.nervous_system.event_append_boundary import EventAppendStatus
from pipeline.nervous_system.event_candidate_boundary import EventCandidate
from pipeline.nervous_system.models import (
    CurrentProjectionResponse,
    ProjectionPosture,
    ProjectionOperator,
    ProjectionAuditState
)
from pipeline.nervous_system.signature_ceremony_boundary import (
    build_signature_ceremony_request,
    CeremonyPreparationRejectedError
)
import hashlib
import json

def generate_candidate_hash(candidate_dict):
    canonical_json = json.dumps(candidate_dict, sort_keys=True, separators=(',', ':'))
    return hashlib.sha3_512(canonical_json.encode('utf-8')).hexdigest()

def get_base_candidate():
    candidate_data = {
        "operator_id": "operator_789",
        "applied_as_entity_id": None,
        "posture": "LOCAL_ONLY_SOVEREIGN",
        "route_mode": None,
        "last_verified_event_id": "evt_001",
        "current_projection_epoch": None,
        "command_type": "STANDARD_CMD",
        "event_family": "STANDARD_FAMILY",
        "event_type": "STANDARD_EVENT",
        "payload": {"some_data": 42},
        "policy_receipt_status": "APPEND_REQUEST_ACCEPTED_FOR_POLICY_REVIEW",
        "policy_receipt_reason": "Looks good",
    }
    computed_hash = generate_candidate_hash(candidate_data)

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
        policy_receipt_status=EventAppendStatus.APPEND_REQUEST_ACCEPTED_FOR_POLICY_REVIEW,
        policy_receipt_reason=candidate_data["policy_receipt_reason"],
        candidate_hash=computed_hash,
    )

def get_base_projection():
    return CurrentProjectionResponse(
        operator=ProjectionOperator(
            user_id="operator_789",
            display_name="Test Operator",
            role="admin",
            signing_key_fingerprint="fingerprint_xyz"
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

def test_build_signature_ceremony_request_success():
    candidate = get_base_candidate()
    proj = get_base_projection()

    request = build_signature_ceremony_request(candidate, proj)
    assert request.operator_id == "operator_789"
    assert request.signing_key_fingerprint == "fingerprint_xyz"
    assert request.ceremony_reason == "Standard Event Append Signature"

def test_reject_operator_mismatch():
    candidate = get_base_candidate()
    proj = get_base_projection()
    proj.operator.user_id = "different_operator"

    with pytest.raises(CeremonyPreparationRejectedError) as exc:
        build_signature_ceremony_request(candidate, proj)
    assert "Operator mismatch" in str(exc.value)

def test_reject_missing_signing_key():
    candidate = get_base_candidate()
    proj = get_base_projection()
    proj.operator.signing_key_fingerprint = ""

    with pytest.raises(CeremonyPreparationRejectedError) as exc:
        build_signature_ceremony_request(candidate, proj)
    assert "Missing signing key" in str(exc.value)

def test_reject_posture_mismatch():
    candidate = get_base_candidate()
    proj = get_base_projection()
    proj.posture.mode = "FRONTIER_ELIGIBLE"

    with pytest.raises(CeremonyPreparationRejectedError) as exc:
        build_signature_ceremony_request(candidate, proj)
    assert "Posture mismatch" in str(exc.value)

def test_reject_sync_conflict():
    candidate = get_base_candidate()
    proj = get_base_projection()
    proj.audit_state.last_verified_event_id = "evt_002"

    with pytest.raises(CeremonyPreparationRejectedError) as exc:
        build_signature_ceremony_request(candidate, proj)
    assert "Sync conflict" in str(exc.value)

def test_reject_hash_mismatch():
    candidate = get_base_candidate()
    candidate.candidate_hash = "fake_hash_123"
    proj = get_base_projection()

    with pytest.raises(CeremonyPreparationRejectedError) as exc:
        build_signature_ceremony_request(candidate, proj)
    assert "hash mismatch" in str(exc.value).lower()

def test_risk_override_acknowledgment():
    candidate = get_base_candidate()
    candidate.event_type = "RISK_OVERRIDE"

    # recompute hash because we modified the candidate directly
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
    candidate.candidate_hash = generate_candidate_hash(candidate_data)

    proj = get_base_projection()
    request = build_signature_ceremony_request(candidate, proj)

    assert "Risk Override" in request.ceremony_reason
    assert any("does not convert failed gates to PASS" in ack for ack in request.required_human_acknowledgments)

def test_final_packet_authorization():
    candidate = get_base_candidate()
    candidate.event_type = "FINAL_PACKET_AUTHORIZATION"

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
    candidate.candidate_hash = generate_candidate_hash(candidate_data)

    proj = get_base_projection()
    request = build_signature_ceremony_request(candidate, proj)

    assert request.ceremony_reason == "Final Packet Export"
    assert "Strict/Export Boundary" in request.signature_scope

def test_source_inspection_pure_boundary():
    """Prove the module is a pure boundary with no side effects."""
    with open("pipeline/nervous_system/signature_ceremony_boundary.py") as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                assert node.func.id not in [
                    "append_event",
                    "commit",
                    "open",
                    "write",
                    "execute",
                    "sign",
                    "verify"
                ]
            elif isinstance(node.func, ast.Attribute):
                assert node.func.attr not in [
                    "append",
                    "commit",
                    "write",
                    "execute",
                    "sign",
                    "verify"
                ]
