import pytest
from fastapi.testclient import TestClient
from pipeline.nervous_system.api import app
from pipeline.nervous_system.governance import enforce_route_mode
from pipeline.nervous_system.models import RouteMode
from fastapi import HTTPException

client = TestClient(app)

def get_valid_identity():
    return {
        "user_id": "usr_dev_001",
        "applied_as": "fit-farms",
        "token_validity": True,
        "is_human": True,
        "origin": "human_direct"
    }

def test_canonical_route_modes_accepted():
    # Calling enforce_route_mode with a canonical mode that is allowed does not raise
    enforce_route_mode(RouteMode.ALL_MODEL_ACCESS.value, [RouteMode.ALL_MODEL_ACCESS.value])

def test_enforce_route_mode_unauthorized_returns_403():
    with pytest.raises(HTTPException) as excinfo:
        enforce_route_mode(RouteMode.ALL_MODEL_ACCESS.value, [RouteMode.LOCAL_ONLY.value])
    assert excinfo.value.status_code == 403

def test_enforce_route_mode_malformed_returns_400():
    with pytest.raises(HTTPException) as excinfo:
        enforce_route_mode("INVALID_MODE", [RouteMode.LOCAL_ONLY.value])
    assert excinfo.value.status_code == 400

def test_command_final_packet_auth_requires_human():
    identity = get_valid_identity()
    identity["is_human"] = False  # Model-initiated
    payload = {
        "identity_context": identity,
        "command_type": "FINAL_PACKET_AUTHORIZATION",
        "applied_as_entity_id": "fit-farms",
        "payload": {"context": {"org_slug": "fit-farms"}}
    }
    response = client.post("/api/commands", json=payload)
    assert response.status_code == 403
    assert "human" in response.json()["detail"].lower()

def test_projection_endpoint_is_read_only():
    response = client.post("/api/projections/current", json={})
    assert response.status_code == 405

    response = client.put("/api/projections/current", json={})
    assert response.status_code == 405

def test_action_endpoint_blocks_direct_memory_mutation():
    payload = {
        "identity_context": get_valid_identity(),
        "action": "MUTATE_MEMORY",
        "label": "Inject fabricated memory"
    }
    response = client.post("/api/actions/run", json=payload)
    assert response.status_code == 403
    assert "mutate memory" in response.json()["detail"].lower()

def test_identity_context_malformed_returns_400():
    payload = {
        "route_mode": RouteMode.ALL_MODEL_ACCESS.value,
        "applied_as_entity_id": "fit-farms",
    }
    response = client.post("/api/scout/rescan", json=payload)
    assert response.status_code == 400

def test_identity_context_invalid_returns_403():
    identity = get_valid_identity()
    identity["token_validity"] = False
    payload = {
        "identity_context": identity,
        "route_mode": RouteMode.ALL_MODEL_ACCESS.value,
        "applied_as_entity_id": "fit-farms",
    }
    response = client.post("/api/scout/rescan", json=payload)
    assert response.status_code == 403

def test_scout_rescan_without_operation_intent_does_not_fail():
    payload = {
        "identity_context": get_valid_identity(),
        "applied_as_entity_id": "fit-farms",
        # operation_intent omitted entirely
    }
    response = client.post("/api/scout/rescan", json=payload)
    # The response is 200 and it defaults operation_intent to "none", returning fixture.
    assert response.status_code == 200
    assert response.json()["meta"]["operation_intent"] == "none"

def test_scout_rescan_with_explicit_operation_intent_preserves_value():
    payload = {
        "identity_context": get_valid_identity(),
        "applied_as_entity_id": "fit-farms",
        "operation_intent": "rescan_scout_opportunities"
    }
    response = client.post("/api/scout/rescan", json=payload)
    assert response.status_code == 200
    assert response.json()["meta"]["operation_intent"] == "rescan_scout_opportunities"
