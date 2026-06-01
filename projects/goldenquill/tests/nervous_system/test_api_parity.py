import os
import pytest
from fastapi.testclient import TestClient
from pipeline.nervous_system.api import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def set_fixture_mode(monkeypatch):
    monkeypatch.setenv("TILTH_DEV_FIXTURE_MODE", "1")

def test_commands_missing_identity():
    # 400 when missing identity envelope
    # applied_as_entity_id is required by CommandRequest schema.
    # identity_context is intentionally absent — governance handler returns 400.
    response = client.post("/api/commands", json={"command_type": "TEST", "applied_as_entity_id": "org_default"})
    assert response.status_code == 400
    assert "Missing identity_context" in response.text

def test_commands_invalid_identity():
    # 403 when token is invalid
    payload = {
        "command_type": "TEST",
        "applied_as_entity_id": "org_default",
        "identity_context": {
            "user_id": "u1",
            "applied_as": "org_default",
            "token_validity": False
        }
    }
    response = client.post("/api/commands", json=payload)
    assert response.status_code == 403
    assert "Expired/invalid identity token" in response.text

def test_commands_applied_as_violation():
    # 403 when trying to act on an org you aren't applied_as
    payload = {
        "command_type": "TEST",
        "applied_as_entity_id": "org_forbidden",
        "identity_context": {
            "user_id": "u1",
            "applied_as": "org_default",
            "token_validity": True
        },
        "payload": {
            "context": {"org_slug": "org_forbidden"}
        }
    }
    response = client.post("/api/commands", json=payload)
    assert response.status_code == 403
    assert "Unauthorized applied_as context" in response.text

def test_final_packet_auth_requires_human():
    payload = {
        "command_type": "FINAL_PACKET_AUTHORIZATION",
        "applied_as_entity_id": "org_default",
        "identity_context": {
            "user_id": "u1",
            "applied_as": "org_default",
            "token_validity": True,
            "is_human": False
        },
        "payload": {
            "context": {"org_slug": "org_default"}
        }
    }
    response = client.post("/api/commands", json=payload)
    assert response.status_code == 403
    assert "requires human re-auth" in response.text

def test_valid_command_accepted():
    payload = {
        "command_type": "TEST_COMMAND",
        "applied_as_entity_id": "org_default",
        "identity_context": {
            "user_id": "u1",
            "applied_as": "org_default",
            "token_validity": True,
            "is_human": True
        },
        "payload": {
            "context": {"org_slug": "org_default"}
        }
    }
    response = client.post("/api/commands", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "accepted"

def test_action_route_mode_enforcement():
    # action requires identity
    payload = {
        "action": "DISMISS_NOTICE",
        "label": "test",
        "route_mode": "LOCAL_ONLY",
        "identity_context": {
            "user_id": "u1",
            "applied_as": "org_default",
            "token_validity": True
        }
    }
    response = client.post("/api/actions/run", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "accepted"

def test_projections_current():
    import json
    headers = {
        "X-Identity-Context": json.dumps({
            "user_id": "u1",
            "applied_as": "org_default",
            "token_validity": True,
            "is_human": True,
            "origin": "system",
            "active_roles": []
        })
    }
    response = client.get("/api/projections/current", headers=headers)
    assert response.status_code == 200
    data = response.json()

    required_slices = [
        "node",
        "operator",
        "cycle",
        "posture",
        "audit_state",
        "logician_gates",
        "draft_sections",
        "budget",
        "judge",
        "red_team",
        "evidence_items",
        "module_map",
        "scout_pipeline",
        "blocker_outreach_tasks"
    ]

    for slice_name in required_slices:
        assert slice_name in data

def test_projections_current_schema_depth():
    import json
    headers = {
        "X-Identity-Context": json.dumps({
            "user_id": "u1",
            "applied_as": "org_default",
            "token_validity": True,
            "is_human": True,
            "origin": "system",
            "active_roles": []
        })
    }
    response = client.get("/api/projections/current", headers=headers)
    assert response.status_code == 200
    data = response.json()

    cycle = data["cycle"]
    assert cycle["status"] == "GATE_FAILED_CLOSED"
    assert cycle["scribe_access"] == "LOCKED"

    logician_gates = {g["gate_id"]: g for g in data["logician_gates"]}
    assert logician_gates["E-102"]["verdict"] == "FAIL_CLOSED"
    assert logician_gates["E-103"]["verdict"] == "UNTESTED_DUE_TO_BLOCK"
    assert logician_gates["E-104"]["verdict"] == "UNTESTED_DUE_TO_BLOCK"

    assert data["audit_state"]["signature_status"] == "UNSIGNED_CHANGES_PENDING"
    assert data["budget"]["validation_state"] == "FAIL"
    assert data["judge"]["score_state"] == "STALE"
