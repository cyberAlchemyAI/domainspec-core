import json
import yaml
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from pipeline.nervous_system.api import app

client = TestClient(app)

def test_projection_reads_from_real_vault_state(tmp_path, monkeypatch):
    monkeypatch.delenv("TILTH_DEV_FIXTURE_MODE", raising=False)
    import pipeline.nervous_system.vault_projection_adapter as adapter
    monkeypatch.setattr(adapter, "get_repo_root", lambda: tmp_path)

    org_slug = "test-org-123"
    cycle_id = "cyc_test_001"

    vault_dir = tmp_path / "orgs" / org_slug / "vault" / "classification"
    vault_dir.mkdir(parents=True, exist_ok=True)
    register_path = vault_dir / "register.yaml"

    register_data = {
        "selected_posture": "LOCAL_ONLY"
    }
    with open(register_path, "w") as f:
        yaml.safe_dump(register_data, f)

    identity_context = {
        "user_id": "test_user_001",
        "is_human": True,
        "applied_as": org_slug,
        "active_roles": ["golden_quill_admin"]
    }
    headers = {"X-Identity-Context": json.dumps(identity_context)}

    response = client.get(f"/api/projections/current?cycle_id={cycle_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert data["node"]["organization_slug"] == org_slug
    assert data["cycle"]["cycle_id"] == cycle_id
    assert data["posture"]["mode"] == "LOCAL_ONLY"

    # Assert full projection shape outside fixture mode
    expected_keys = [
        "module_map", "draft_sections", "budget", "judge", "red_team",
        "evidence_items", "blocker_outreach_tasks", "scout_pipeline",
        "audit_state", "logician_gates"
    ]
    for k in expected_keys:
        assert k in data

    # Assert types for lists
    assert isinstance(data["module_map"], list)
    assert isinstance(data["draft_sections"], list)
    assert isinstance(data["evidence_items"], list)
    assert isinstance(data["blocker_outreach_tasks"], list)
    assert isinstance(data["scout_pipeline"], list)
    assert isinstance(data["logician_gates"], list)

    # Assert presence (not missing/None) for objects
    assert data["budget"] is not None
    assert data["judge"] is not None
    assert data["red_team"] is not None
    assert data["audit_state"] is not None

def test_projection_missing_identity_context_returns_400():
    response = client.get("/api/projections/current?cycle_id=cyc_test_001")
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing X-Identity-Context header"}

def test_projection_malformed_identity_context_returns_400():
    headers = {"X-Identity-Context": "not-valid-json"}
    response = client.get("/api/projections/current?cycle_id=cyc_test_001", headers=headers)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Identity-Context header"}

def test_projection_query_param_org_slug_ignored(tmp_path, monkeypatch):
    monkeypatch.delenv("TILTH_DEV_FIXTURE_MODE", raising=False)
    import pipeline.nervous_system.vault_projection_adapter as adapter
    monkeypatch.setattr(adapter, "get_repo_root", lambda: tmp_path)

    identity_context = {
        "user_id": "test_user_001",
        "is_human": True,
        "applied_as": "true-identity-org",
        "active_roles": ["golden_quill_admin"]
    }
    headers = {"X-Identity-Context": json.dumps(identity_context)}

    response = client.get("/api/projections/current?org_slug=fake-org-slug", headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert data["node"]["organization_slug"] == "true-identity-org"
