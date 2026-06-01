import os
from fastapi.testclient import TestClient
from pipeline.nervous_system.api import app

client = TestClient(app)

def test_api_health_returns_200():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "Golden Quill Nervous System"

def test_api_scout_demo_returns_fixture_shape():
    response = client.get("/api/scout/demo")
    assert response.status_code == 200
    data = response.json()
    # The fixture DEMO_DATA.json has "scout_pipeline" and "scout_totals" among others
    assert "scout_pipeline" in data
    assert "scout_totals" in data
    assert isinstance(data["scout_pipeline"], list)

def get_valid_rescan_payload():
    return {
        "identity_context": {
            "user_id": "usr_dev_001",
            "applied_as": "fit-farms",
            "token_validity": True,
            "is_human": True
        },
        "route_mode": "ALL_MODEL_ACCESS",
        "applied_as_entity_id": "fit-farms",
        "operation_intent": "rescan_scout_opportunities",
        "human_actor_id": "usr_dev_001"
    }

def test_api_scout_rescan_fails_without_envelope():
    response = client.post("/api/scout/rescan", json={})
    assert response.status_code == 400

def test_api_scout_rescan_fails_invalid_identity():
    payload = get_valid_rescan_payload()
    payload["identity_context"]["token_validity"] = False
    response = client.post("/api/scout/rescan", json=payload)
    assert response.status_code == 403

def test_api_scout_rescan_fails_unauthorized_applied_as():
    payload = get_valid_rescan_payload()
    payload["applied_as_entity_id"] = "other-org"
    response = client.post("/api/scout/rescan", json=payload)
    assert response.status_code == 403


import pytest
from pipeline.nervous_system.audit import global_audit_sink
from pipeline.nervous_system.audit_proof import global_proof_sink

@pytest.fixture(autouse=True)
def clear_audit_sink():
    global_audit_sink.clear()
    global_proof_sink.clear()
    yield

def test_api_scout_rescan_success_returns_fixture():
    payload = get_valid_rescan_payload()
    response = client.post("/api/scout/rescan", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data.get("ok") is True
    assert "scout_pipeline" in data
    assert "scout_totals" in data
    assert isinstance(data["scout_pipeline"], list)
    assert data["meta"]["provider_access"] == "disabled"
    assert data["meta"]["execution_mode"] == "deterministic_fixture"
    assert data["meta"]["boundary"] == "model_access_boundary_stub"
    assert data["meta"]["provider_adapter"] == "none"
    assert data["meta"]["allowed"] is True

    assert data["meta"]["audit_event_count"] >= 2
    assert "scout_rescan_requested" in data["meta"]["audit_event_types"]
    assert "model_access_boundary_invoked" in data["meta"]["audit_event_types"]

    events = global_audit_sink.get_events()
    assert len(events) == 2
    assert events[0].event_type == "scout_rescan_requested"
    assert events[0].outcome == "validated"
    assert events[1].event_type == "model_access_boundary_invoked"
    assert events[1].outcome == "fixture_returned"



def test_api_scout_rescan_live_provider_impossible():
    from pipeline.nervous_system.provider_adapter import DisabledProviderAdapter
    with pytest.raises(NotImplementedError) as excinfo:
        DisabledProviderAdapter.execute_live({})
    assert "Live provider network transport not wired yet" in str(excinfo.value)

def test_fake_deterministic_transport_returns_sealed_response():
    from pipeline.nervous_system.transport import FakeDeterministicTransport
    response = FakeDeterministicTransport.send({})
    assert "scout_pipeline" in response
    assert response["transport_used"] == "FakeDeterministicTransport"



def test_real_transport_fails_closed_on_network_error(monkeypatch):
    from pipeline.nervous_system.transport import DevRealProviderTransport, ProviderTransportError
    from pipeline.nervous_system.route_policy import ModelAccessDecision
    import urllib.request

    def mock_urlopen(*args, **kwargs):
        raise Exception("Mocked network timeout")

    monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen)

    decision = ModelAccessDecision(
        allowed=True, route_mode="ALL_MODEL_ACCESS", execution_mode="dev_real_provider_transport",
        provider_access="enabled", reason="", boundary="mab", provider_adapter="dev"
    )

    os.environ["OPENAI_API_KEY"] = "live_key"
    try:
        with pytest.raises(ProviderTransportError) as excinfo:
            DevRealProviderTransport.send({}, decision=decision)
        assert "Provider transport failed" in str(excinfo.value)

        events = global_audit_sink.get_events()
        event_types = [e.event_type for e in events]
        assert "provider_transport_attempted" in event_types
        assert "provider_transport_failed" in event_types
    finally:
        del os.environ["OPENAI_API_KEY"]

def test_outbound_payload_contains_only_synthetic_prompt(monkeypatch):
    from pipeline.nervous_system.transport import DevRealProviderTransport
    from pipeline.nervous_system.route_policy import ModelAccessDecision
    import urllib.request
    import json
    import io

    captured_payload = {}

    class MockResponse:
        def read(self):
            return json.dumps({"choices": [{"message": {"content": "synthetic_ok"}}]}).encode('utf-8')
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    def mock_urlopen(req, *args, **kwargs):
        nonlocal captured_payload
        captured_payload = json.loads(req.data.decode('utf-8'))
        return MockResponse()

    monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen)

    decision = ModelAccessDecision(
        allowed=True, route_mode="ALL_MODEL_ACCESS", execution_mode="dev_real_provider_transport",
        provider_access="enabled", reason="", boundary="mab", provider_adapter="dev"
    )

    os.environ["OPENAI_API_KEY"] = "live_key"
    try:
        DevRealProviderTransport.send({}, decision=decision)
        assert "messages" in captured_payload
        assert len(captured_payload["messages"]) == 1
        assert captured_payload["messages"][0]["content"] == "Return 'synthetic_ok'. Do not process any sensitive data."
    finally:
        del os.environ["OPENAI_API_KEY"]




# --- Immutable Audit Proof tier ----------------------------------------------
#
# Three guard tests + one end-to-end test. They prove the AuditProofChain is
# behaviorally wired, not just structurally present.

def _build_event(chain, event_type="scout_rescan_requested", outcome="validated", metadata=None):
    from pipeline.nervous_system.audit_proof import AuditProofEvent
    event = AuditProofEvent(
        event_type=event_type,
        request_id=chain.chain_id,
        sequence_number=0,
        outcome=outcome,
        metadata_redacted=metadata or {},
    )
    chain.append_event(event)
    return event


def test_audit_proof_chain_links_sequential_events():
    from pipeline.nervous_system.audit_proof import AuditProofChain
    chain = AuditProofChain(chain_id="link-test")

    e1 = _build_event(chain, event_type="scout_rescan_requested")
    e2 = _build_event(chain, event_type="model_access_boundary_invoked", outcome="fixture_returned")
    e3 = _build_event(chain, event_type="provider_transport_attempted", outcome="pending")

    assert e1.previous_event_hash is None
    assert e2.previous_event_hash == e1.event_hash
    assert e3.previous_event_hash == e2.event_hash
    assert e1.sequence_number == 1 and e2.sequence_number == 2 and e3.sequence_number == 3


def test_audit_proof_event_hash_changes_when_event_mutated():
    from pipeline.nervous_system.audit_proof import AuditProofChain
    chain = AuditProofChain(chain_id="tamper-test")
    e1 = _build_event(chain, event_type="scout_rescan_requested", outcome="validated")
    e2 = _build_event(chain, event_type="model_access_boundary_invoked", outcome="fixture_returned")

    # Honest recompute equals the stored hash on the unmodified event.
    assert e1.compute_hash() == e1.event_hash

    # Mutate e1 after the fact and recompute. The new hash must differ from
    # the stored hash AND from the previous_event_hash carried by e2 — that
    # is the tamper-evidence guarantee of the chain.
    e1.outcome = "TAMPERED"
    recomputed = e1.compute_hash()
    assert recomputed != e1.event_hash
    assert recomputed != e2.previous_event_hash


def test_audit_proof_redacts_sensitive_metadata():
    from pipeline.nervous_system.audit_proof import AuditProofChain, proof_recorder, global_proof_sink
    global_proof_sink.clear()

    event = proof_recorder.record(
        chain_id="redaction-test",
        event_type="provider_transport_attempted",
        request_id="req-1",
        outcome="pending",
        metadata={
            "api_key": "sk-live-NOT-A-REAL-SECRET",
            "Authorization": "Bearer sk-live-NOT-A-REAL-SECRET",
            "bearer_token": "should-also-redact",
            "client_secret": "shhh",
            "session_token": "shhh-2",
            "raw_response": {"choices": [{"message": {"content": "leaked"}}]},
            "synthetic_response": "synthetic_ok",
            "prompt_body": "Return 'synthetic_ok'.",
            "scout_pipeline": [{"opp_id": "o-1"}],
            "scout_totals": {"signals": 1},
            "user_id": "joe",
        },
    )

    redacted = event.metadata_redacted
    for key in ("api_key", "Authorization", "bearer_token", "client_secret", "session_token"):
        assert redacted[key] == "[REDACTED]", f"{key} should be redacted, got {redacted[key]!r}"
    for key in ("raw_response", "synthetic_response", "prompt_body", "scout_pipeline", "scout_totals"):
        assert redacted[key] == "[STRIPPED]", f"{key} should be stripped, got {redacted[key]!r}"
    # Non-sensitive fields survive.
    assert redacted["user_id"] == "joe"
    # And no raw secret ever appears anywhere in the proof event.
    import json as _json
    serialized = _json.dumps(event.model_dump(), sort_keys=True)
    assert "sk-live-NOT-A-REAL-SECRET" not in serialized
    assert "synthetic_ok" not in serialized
    assert "leaked" not in serialized


def test_api_scout_rescan_surfaces_proof_chain_pointer():
    """End-to-end: the API response carries a proof-chain pointer, but not the
    proof payload itself. The pointer is enough to verify execution constraints
    later without leaking authority over the chain to the client."""
    payload = get_valid_rescan_payload()
    response = client.post("/api/scout/rescan", json=payload)
    assert response.status_code == 200
    meta = response.json()["meta"]

    # Three claimed pointer fields are all present.
    assert "proof_chain_id" in meta
    assert "proof_event_count" in meta
    assert "last_event_hash" in meta

    # The pointer references a real, hash-linked chain in the sink.
    chain = global_proof_sink.get_chain(meta["proof_chain_id"])
    assert len(chain.events) == meta["proof_event_count"] >= 2
    assert chain.last_hash == meta["last_event_hash"]
    # SHA-256 hex = 64 chars.
    assert isinstance(meta["last_event_hash"], str) and len(meta["last_event_hash"]) == 64

    # The pointer is a pointer, not the payload — no raw proof events leak.
    assert "events" not in meta
    assert "proof_chain" not in meta
