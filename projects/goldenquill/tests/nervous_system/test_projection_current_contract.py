import pytest
import json
import base64
import os
from fastapi.testclient import TestClient
from pathlib import Path
from unittest.mock import patch, mock_open
from pipeline.nervous_system.api import app

client = TestClient(app)

def create_valid_identity():
    return {
        "schema_version": "identity_context.v1",
        "org_slug": "test-org",
        "operator_id": "test-operator",
        "applied_as": "test-org",
        "node_fingerprint": "test-node",
        "origin": "local_ui",
        "token_validity": "valid",
        "is_human": True,
        "roles": ["operator"],
        "posture": "hybrid"
    }

def encode_identity(identity_dict):
    return base64.b64encode(json.dumps(identity_dict).encode('utf-8')).decode('utf-8')

def test_missing_identity_returns_401():
    response = client.get("/api/projections/current")
    assert response.status_code == 401
    assert "Missing" in response.json()["detail"]

def test_malformed_base64_returns_401():
    response = client.get("/api/projections/current", headers={"X-Identity-Context": "not-base64!"})
    assert response.status_code == 401

def test_malformed_json_returns_401():
    bad_json = base64.b64encode(b"not-json").decode('utf-8')
    response = client.get("/api/projections/current", headers={"X-Identity-Context": bad_json})
    assert response.status_code == 401

def test_schema_invalid_identity_returns_401():
    identity = create_valid_identity()
    del identity["org_slug"]  # Missing required field
    response = client.get("/api/projections/current", headers={"X-Identity-Context": encode_identity(identity)})
    assert response.status_code == 401

def test_invalid_token_validity_returns_401():
    identity = create_valid_identity()
    identity["token_validity"] = "expired"
    response = client.get("/api/projections/current", headers={"X-Identity-Context": encode_identity(identity)})
    assert response.status_code == 401

def test_valid_identity_returns_200_with_empty_pipeline_if_no_source():
    # Patch Path to simulate no files existing
    with patch("pipeline.nervous_system.api.Path") as MockPath:
        mock_repo = MockPath.return_value.resolve.return_value.parent.parent.parent
        mock_repo.__truediv__.return_value.__truediv__.return_value.__truediv__.return_value.exists.return_value = False
        
        response = client.get("/api/projections/current", headers={"X-Identity-Context": encode_identity(create_valid_identity())})
        assert response.status_code == 200
        data = response.json()
        assert "scout_pipeline" in data
        assert data["scout_pipeline"] == []

def test_production_response_does_not_contain_demo_sentinel():
    with patch("pipeline.nervous_system.api.Path") as MockPath:
        mock_repo = MockPath.return_value.resolve.return_value.parent.parent.parent
        mock_repo.__truediv__.return_value.__truediv__.return_value.__truediv__.return_value.exists.return_value = False
        
        response = client.get("/api/projections/current", headers={"X-Identity-Context": encode_identity(create_valid_identity())})
        assert response.status_code == 200
        data = response.json()
        assert "USDA SARE" not in json.dumps(data)

def test_valid_identity_reads_from_source_with_provenance(tmp_path):
    csv_dir = tmp_path / "pipeline" / "db"
    csv_dir.mkdir(parents=True, exist_ok=True)
    csv_file = csv_dir / "funders.csv"
    csv_content = "id,title,agency\nfnd_001,Test Fund,Test Agency\n"
    csv_file.write_text(csv_content)
    
    with patch("pipeline.nervous_system.api.Path") as MockPath:
        # Make the mocked Path's parent chain resolve to our tmp_path
        mock_resolve = MockPath.return_value.resolve.return_value
        mock_resolve.parent.parent.parent = tmp_path
        
        response = client.get("/api/projections/current", headers={"X-Identity-Context": encode_identity(create_valid_identity())})
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["scout_pipeline"]) == 1
        row = data["scout_pipeline"][0]
        assert row["id"] == "fnd_001"
        assert row["source_kind"] == "staging_csv"
        assert row["source_path"] == "pipeline/db/funders.csv"
        assert row["source_record_id"] == "fnd_001"

def test_fixture_mode_returns_demo_data():
    os.environ["TILTH_DEV_FIXTURE_MODE"] = "1"
    try:
        response = client.get("/api/projections/current", headers={"X-Identity-Context": encode_identity(create_valid_identity())})
        assert response.status_code == 200
        data = response.json()
        assert "USDA SARE" in json.dumps(data)
    finally:
        if "TILTH_DEV_FIXTURE_MODE" in os.environ:
            del os.environ["TILTH_DEV_FIXTURE_MODE"]
