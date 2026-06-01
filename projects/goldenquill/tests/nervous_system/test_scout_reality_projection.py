import pytest
from fastapi.testclient import TestClient
from pipeline.nervous_system.api import app
from pipeline.nervous_system.models import ScoutRescanRequest, IdentityContext, CommandRequest
from pipeline.nervous_system.scout_source_roster import list_enabled_sources

client = TestClient(app)

def test_scout_reality_projection_includes_report():
    request = ScoutRescanRequest(
        identity_context=IdentityContext(
            user_id="usr_123",
            applied_as="org_test"
        ),
        applied_as_entity_id="org_test",
        operation_intent="scout_rescan"
    )

    response = client.post("/api/scout/rescan", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()

    # 1. Scout response includes scout_reality_report
    assert "scout_reality_report" in data
    report = data["scout_reality_report"]

    # 2. Contains required keys
    assert "fixture_mode" in report
    assert "channel_coverage" in report
    assert "available_now" in report
    assert "impending" in report
    assert "stale_or_needs_recheck" in report
    assert "blocked" in report

    # 3. With no configured sources, fixture_mode is true
    # Currently the default is no enabled sources, let's verify
    enabled = list_enabled_sources()
    if len(enabled) == 0:
        assert report["fixture_mode"] is True

        # 4. channel list is not empty, includes source_not_configured
        assert len(report["channel_coverage"]) > 0
        statuses = [ch.get("source_status") for ch in report["channel_coverage"].values()]
        assert "source_not_configured" in statuses or "not_implemented" in statuses

        # 12. all opportunity buckets are empty
        assert report["available_now"] == []
        assert report["impending"] == []
        assert report["stale_or_needs_recheck"] == []
        assert report["blocked"] == []

    # 5. Empty channel list with fixture_mode false is impossible
    if not report["fixture_mode"]:
        assert len(report["channel_coverage"]) > 0

    # 6. No fake opportunity records
    assert len(report["available_now"]) == 0
    assert len(report["impending"]) == 0

def test_scout_schema_invariants():
    scout_fields = ScoutRescanRequest.model_fields
    # 8. ScoutRescanRequest has no route_mode
    assert "route_mode" not in scout_fields

    command_fields = CommandRequest.model_fields
    # 9. CommandRequest requires applied_as_entity_id
    assert "applied_as_entity_id" in command_fields
    assert command_fields["applied_as_entity_id"].is_required()

def test_no_forbidden_strategy_language():
    request = ScoutRescanRequest(
        identity_context=IdentityContext(
            user_id="usr_123",
            applied_as="org_test"
        ),
        applied_as_entity_id="org_test",
        operation_intent="scout_rescan"
    )

    response = client.post("/api/scout/rescan", json=request.model_dump())
    assert response.status_code == 200

    output_lower = response.text.lower()

    forbidden = [
        "grant" + " stacking",
        "award" + " probability",
        "win" + " probability",
        "partner" + " committed",
        "ready" + " to apply",
        "final" + " submission allowed",
        "project" + " finance",
        "capital" + " sequencing"
    ]

    # 7. No forbidden strategy language appears in serialized report output
    for word in forbidden:
        assert word not in output_lower
