import pytest
from fastapi.testclient import TestClient
from pipeline.nervous_system.api import app
from pipeline.nervous_system.models import RouteMode

client = TestClient(app)

def get_valid_identity():
    return {
        "user_id": "usr_dev_001",
        "applied_as": "fit-farms",
        "token_validity": True,
        "is_human": True,
        "origin": "human_direct"
    }

def test_action_unknown_returns_400():
    payload = {
        "identity_context": get_valid_identity(),
        "action": "SOME_UNKNOWN_ACTION",
        "label": "Do something weird",
        "route_mode": RouteMode.LOCAL_ONLY.value
    }
    response = client.post("/api/actions/run", json=payload)
    assert response.status_code == 400
    assert "unknown or unregistered" in response.json()["detail"].lower()

def test_action_mutate_memory_returns_403():
    payload = {
        "identity_context": get_valid_identity(),
        "action": "MUTATE_MEMORY",
        "label": "Inject fabricated memory",
        "route_mode": RouteMode.LOCAL_ONLY.value
    }
    response = client.post("/api/actions/run", json=payload)
    assert response.status_code == 403
    assert "mutate memory directly" in response.json()["detail"].lower()

def test_action_stage_packet_requires_human():
    identity = get_valid_identity()
    identity["is_human"] = False  # Model initiated
    payload = {
        "identity_context": identity,
        "action": "STAGE_PACKET",
        "label": "Stage packet for export",
        "route_mode": RouteMode.ALL_MODEL_ACCESS.value,
        "applied_as_entity_id": "fit-farms"
    }
    response = client.post("/api/actions/run", json=payload)
    assert response.status_code == 403
    assert "human" in response.json()["detail"].lower()

def test_action_stage_packet_requires_applied_as():
    payload = {
        "identity_context": get_valid_identity(),
        "action": "STAGE_PACKET",
        "label": "Stage packet for export",
        "route_mode": RouteMode.ALL_MODEL_ACCESS.value,
        # Missing applied_as_entity_id
    }
    response = client.post("/api/actions/run", json=payload)
    assert response.status_code == 400
    assert "requires applied_as_entity_id" in response.json()["detail"].lower()

def test_action_dismiss_notice_allowed():
    payload = {
        "identity_context": get_valid_identity(),
        "action": "DISMISS_NOTICE",
        "label": "acknowledge warning",
        "route_mode": RouteMode.LOCAL_ONLY.value
    }
    response = client.post("/api/actions/run", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "accepted"
