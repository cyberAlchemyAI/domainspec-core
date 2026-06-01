from fastapi.testclient import TestClient
from pipeline.nervous_system.api import app
from pipeline.nervous_system.models import ScoutRescanResponse

client = TestClient(app)

def test_scout_rescan_accepts_valid_payload(monkeypatch):
    import pipeline.nervous_system.scout_service as scout_service
    monkeypatch.setattr(scout_service.ScoutService, "rescan", lambda *args, **kwargs: ScoutRescanResponse(ok=True))

    payload = {
        "identity_context": {
            "user_id": "user1",
            "applied_as": "test-org",
            "token_validity": True,
            "is_human": True,
            "origin": "human_direct"
        },
        "route_mode": "ALL_MODEL_ACCESS",
        "applied_as_entity_id": "test-org",
        "operation_intent": "rescan_scout_opportunities",
        "human_actor_id": "user1"
    }

    resp = client.post("/api/scout/rescan", json=payload)
    assert resp.status_code == 200
    assert resp.json()["ok"] is True

def test_scout_rescan_applied_as_mismatch_fails_closed(monkeypatch):
    payload = {
        "identity_context": {
            "user_id": "user1",
            "applied_as": "test-org",
            "token_validity": True,
            "is_human": True,
            "origin": "human_direct"
        },
        "route_mode": "ALL_MODEL_ACCESS",
        "applied_as_entity_id": "wrong-org",
        "operation_intent": "rescan_scout_opportunities",
        "human_actor_id": "user1"
    }
    resp = client.post("/api/scout/rescan", json=payload)
    # Could be 400 or 403 depending on governance rules
    assert resp.status_code in [400, 403]

def test_scout_rescan_missing_identity_context_fails_closed(monkeypatch):
    payload = {
        "route_mode": "ALL_MODEL_ACCESS",
        "applied_as_entity_id": "test-org",
        "operation_intent": "rescan_scout_opportunities",
        "human_actor_id": "user1"
    }
    resp = client.post("/api/scout/rescan", json=payload)
    assert resp.status_code == 400
