import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from pipeline.nervous_system.models import CommandRequest
from pipeline.nervous_system.api import app

client = TestClient(app)

def test_command_request_schema_requires_applied_as():
    # 1. Schema includes required applied_as_entity_id
    fields = CommandRequest.model_fields
    assert "applied_as_entity_id" in fields
    assert fields["applied_as_entity_id"].is_required()

    # 2. Missing fails
    with pytest.raises(ValidationError):
        CommandRequest(
            command_type="TEST",
            identity_context={
                "user_id": "u1",
                "applied_as": "org_a"
            }
        )

    # 3. Present succeeds
    req = CommandRequest(
        applied_as_entity_id="org_a",
        command_type="TEST",
        identity_context={
            "user_id": "u1",
            "applied_as": "org_a"
        }
    )
    assert req.applied_as_entity_id == "org_a"

def test_route_4a_bypass_skip_closure():
    # 4a: WITH top-level applied_as, WITHOUT nested org_slug. Should succeed.
    resp = client.post("/api/commands", json={
        "applied_as_entity_id": "org_a",
        "command_type": "TEST",
        "identity_context": {
            "user_id": "u1",
            "applied_as": "org_a",
            "token_validity": True,
            "is_human": False,
            "origin": "system"
        }
    })
    assert resp.status_code == 200

def test_route_4b_pydantic_hard_stop():
    # 4b: missing applied_as_entity_id entirely -> 422
    resp = client.post("/api/commands", json={
        "command_type": "TEST",
        "identity_context": {
            "user_id": "u1",
            "applied_as": "org_a",
            "token_validity": True,
            "is_human": False,
            "origin": "system"
        }
    })
    assert resp.status_code == 422

def test_route_5_nested_context_mismatch():
    # 5: applied_as_entity_id doesn't match payload.context.org_slug -> 400
    resp = client.post("/api/commands", json={
        "applied_as_entity_id": "org_a",
        "command_type": "TEST",
        "identity_context": {
            "user_id": "u1",
            "applied_as": "org_a",
            "token_validity": True,
            "is_human": False,
            "origin": "system"
        },
        "payload": {
            "context": {
                "org_slug": "org_b"
            }
        }
    })
    assert resp.status_code == 400
