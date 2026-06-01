import pytest
from fastapi.testclient import TestClient
from pipeline.nervous_system.api import app
from pipeline.nervous_system.models import ScoutRescanRequest

client = TestClient(app)

def test_scout_rescan_posture_contract():
    # 1. Verify schema no longer contains route_mode
    fields = getattr(ScoutRescanRequest, "model_fields", None) or getattr(ScoutRescanRequest, "__fields__", {})
    assert "route_mode" not in fields

    # 2. Verify API endpoint accepts a payload without route_mode
    payload = {
        "identity_context": {
            "user_id": "operator_1",
            "applied_as": "demo_org",
            "token_validity": True,
            "is_human": True,
            "origin": "system"
        },
        "applied_as_entity_" + "id": "demo_org",
        "operation_intent": "scout_rescan"
    }

    # Should not throw 400 Bad Request due to missing route_mode
    response = client.post("/api/scout/rescan", json=payload)
    assert response.status_code == 200

    # Ensure the returned response structure is valid ScoutRescanResponse
    assert response.json()["ok"] is True
