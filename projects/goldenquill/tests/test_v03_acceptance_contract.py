"""
Golden Quill v0.3 Acceptance Tests.

These tests encode the locked T01-T15 adversarial boundary cases.

The implementation is expected to provide:
- golden_quill_substrate.ingress.handle_ingress
- golden_quill_substrate.errors.SubstrateError
- test fixtures for DI, Archivist, Model Boundary, Memory, and Packet Engine

Do not weaken these tests to fit implementation shortcuts.
Implementation must conform to the tests, not the other way around.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from golden_quill_substrate.contracts import (
    GateFailure,
    IdentityContext,
    JudgeReview,
    OperationTarget,
    RequestEnvelope,
)
from golden_quill_substrate.errors import SubstrateError
from golden_quill_substrate.ingress import handle_ingress


# -----------------------------------------------------------------------------
# TEST HELPERS
# -----------------------------------------------------------------------------

def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def valid_identity_context(
    *,
    actor_type: str = "HUMAN",
    applied_as_entity_id: UUID | None = None,
    auth_strength: str = "SESSION",
    human_present: bool = False,
    final_authorization_eligible: bool = False,
    issued_at: datetime | None = None,
    expires_at: datetime | None = None,
) -> IdentityContext:
    issued = issued_at or now_utc()
    expires = expires_at or (issued + timedelta(hours=1))

    return IdentityContext(
        session_id=uuid4(),
        principal_id=uuid4(),
        actor_type=actor_type,
        licensed_node_id=uuid4(),
        licensed_customer_entity_id=uuid4(),
        applied_as_entity_id=applied_as_entity_id or uuid4(),
        role_ids=[],
        permission_scopes=["*"],
        auth_strength=auth_strength,
        auth_token_id=uuid4(),
        actor_binding_hash="a" * 64,
        issued_at=issued,
        expires_at=expires,
        request_origin="USER_SESSION" if actor_type == "HUMAN" else "INTERNAL_SERVICE",
        human_present=human_present,
        final_authorization_eligible=final_authorization_eligible,
    )


def build_valid_envelope(
    *,
    identity: IdentityContext | None = None,
    operation: str = "brain.intent.parse",
    route_mode: str = "LOCAL_ONLY",
    target_entity: UUID | None = None,
    payload: dict | None = None,
) -> RequestEnvelope:
    identity = identity or valid_identity_context()
    applied_as = target_entity or identity.applied_as_entity_id

    return RequestEnvelope(
        request_id=uuid4(),
        correlation_id=uuid4(),
        identity_context=identity,
        operation_type=operation,
        target=OperationTarget(
            resource_type="DRAFT",
            resource_id=uuid4(),
            applied_as_entity_id=applied_as,
        ),
        payload=payload or {},
        declared_purpose="Contract acceptance test",
        requested_route_mode=route_mode,
        schema_version="v0.3",
    )


# -----------------------------------------------------------------------------
# T01-T15 ACCEPTANCE SUITE
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_t01_missing_identity_context_maps_to_400():
    raw_payload = {
        "request_id": str(uuid4()),
        "correlation_id": str(uuid4()),
        "operation_type": "brain.intent.parse",
        "target": {
            "resource_type": "DRAFT",
            "resource_id": str(uuid4()),
            "applied_as_entity_id": str(uuid4()),
        },
        "payload": {},
        "declared_purpose": "Test missing identity",
        "requested_route_mode": "LOCAL_ONLY",
        "schema_version": "v0.3",
    }

    response = await handle_ingress(raw_payload)

    assert response.status_code == 400
    assert response.error.code == "MALFORMED_ENVELOPE.IDENTITY_CONTEXT_MISSING"
    assert response.error.category == "MALFORMED_REQUEST"


@pytest.mark.asyncio
async def test_t02_wrong_applied_as_entity_id_maps_to_403_security_failure():
    identity = valid_identity_context()
    target_entity = uuid4()

    raw_payload = {
        "request_id": str(uuid4()),
        "correlation_id": str(uuid4()),
        "identity_context": identity.model_dump(mode="json"),
        "operation_type": "brain.intent.parse",
        "target": {
            "resource_type": "DRAFT",
            "resource_id": str(uuid4()),
            "applied_as_entity_id": str(target_entity),
        },
        "payload": {},
        "declared_purpose": "Cross boundary test",
        "requested_route_mode": "LOCAL_ONLY",
        "schema_version": "v0.3",
    }

    response = await handle_ingress(raw_payload)

    assert response.status_code == 403
    assert response.error.code == "BOUNDARY.APPLIED_AS_TARGET_MISMATCH"
    assert any(
        failure.failure_type == "SECURITY_FAILURE"
        for failure in response.error.gate_failures
    )


@pytest.mark.asyncio
async def test_t03_brain_attempts_db_access_is_blocked_by_di(di_container):
    with pytest.raises(Exception) as exc:
        di_container.resolve("database_client", context="brain")

    assert "BRAIN.DB_ACCESS_FORBIDDEN" in str(exc.value)


@pytest.mark.asyncio
async def test_t04_ai_attempts_evidence_promotion_rejected():
    identity = valid_identity_context(actor_type="BRAIN_SCRIBE")
    envelope = build_valid_envelope(
        identity=identity,
        operation="evidence.promote",
    )

    response = await handle_ingress(envelope.model_dump(mode="json"))

    assert response.status_code == 403
    assert response.error.code == "EVIDENCE.PROMOTION_REQUIRES_STATE_MACHINE"
    assert any(
        failure.failure_type == "SECURITY_FAILURE"
        for failure in response.error.gate_failures
    )


@pytest.mark.asyncio
async def test_t05_vector_search_before_sql_prefilter_fails_hard(mock_archivist_pipeline):
    mock_archivist_pipeline.force_execution_order([
        "VECTOR_SEARCH",
        "SQL_APPLIED_AS_PREFILTER",
    ])

    with pytest.raises(SubstrateError) as exc:
        await mock_archivist_pipeline.execute_search()

    assert exc.value.status_code == 500
    assert exc.value.code == "ARCHIVIST.RETRIEVAL_ORDER_VIOLATION"


@pytest.mark.asyncio
async def test_t06_hybrid_attempts_to_send_vault_data_to_frontier(mock_model_boundary):
    response = await mock_model_boundary.invoke(
        route_mode="HYBRID_PUBLIC_FRONTIER_LOCAL_VAULT",
        outbound_payload={
            "draft_content": "Project requires NON_PUBLIC_CANARY_ID_77"
        },
        known_non_public_canaries=["NON_PUBLIC_CANARY_ID_77"],
    )

    assert response.status_code == 403
    assert response.error.code == "MODEL_BOUNDARY.HYBRID_VAULT_EGRESS_ATTEMPT"
    assert response.error.gate_failures[0].failure_type == "SECURITY_FAILURE"
    assert mock_model_boundary.frontier_call_count == 0


@pytest.mark.asyncio
async def test_t07_judge_attempts_to_return_gate_failure_is_schema_violation():
    invalid_judge_output = {
        "review_findings": [],
        "risk_findings": [],
        "gate_failures": [
            {
                "failure_id": str(uuid4()),
                "gate_id": "fake",
                "gate_stage": "POST",
                "failure_type": "BLOCKER",
                "code": "FAKE_GATE",
                "message": "Judge is not allowed to emit this.",
            }
        ],
    }

    with pytest.raises(ValidationError) as exc:
        JudgeReview(**invalid_judge_output)

    assert "Extra inputs are not permitted" in str(exc.value)


@pytest.mark.asyncio
async def test_t08_sealed_section_mutation_returns_409(mock_memory_store, sm_context):
    section_id = mock_memory_store.seed_section(state="SEALED")

    response = await mock_memory_store.update_memory(
        sm_context,
        section_id,
        {"new_text": "illegal update"},
    )

    assert response.status_code == 409
    assert response.error.code == "STATE.SEALED_SECTION_MUTATION"
    assert any(
        failure.failure_type == "BLOCKER"
        for failure in response.error.gate_failures
    )


@pytest.mark.asyncio
async def test_t09_packet_hash_from_live_draft_returns_409(mock_packet_engine):
    response = await mock_packet_engine.prepare_packet(
        source_ref="drafts/live/current"
    )

    assert response.status_code == 409
    assert response.error.code == "PACKET.HASH_REQUIRES_IMMUTABLE_SNAPSHOT"
    assert any(
        failure.failure_type == "BLOCKER"
        for failure in response.error.gate_failures
    )


@pytest.mark.asyncio
async def test_t10_final_packet_authorization_by_non_human_actor_rejected():
    identity = valid_identity_context(actor_type="STATE_MACHINE_RUNNER")
    envelope = build_valid_envelope(
        identity=identity,
        operation="packet.authorize_final",
    )

    response = await handle_ingress(envelope.model_dump(mode="json"))

    assert response.status_code == 403
    assert response.error.code == "AUTHORIZATION.HUMAN_REQUIRED"
    assert response.error.gate_failures[0].failure_type == "SECURITY_FAILURE"


@pytest.mark.asyncio
async def test_t11_expired_identity_context_maps_to_403_not_400():
    issued = now_utc() - timedelta(hours=2)
    expired = now_utc() - timedelta(hours=1)

    identity = valid_identity_context(
        issued_at=issued,
        expires_at=expired,
    )

    envelope = build_valid_envelope(identity=identity)

    response = await handle_ingress(envelope.model_dump(mode="json"))

    assert response.status_code == 403
    assert response.error.code == "IDENTITY.EXPIRED"
    assert response.error.category == "UNAUTHORIZED"
    assert response.error.gate_failures[0].failure_type == "SECURITY_FAILURE"


@pytest.mark.asyncio
async def test_t12_all_model_access_without_explicit_authorization_rejected():
    identity = valid_identity_context()
    envelope = build_valid_envelope(
        identity=identity,
        route_mode="ALL_MODEL_ACCESS",
        operation="model.invoke",
        payload={
            # Deliberately missing explicit RouteAuthorization snapshot.
            "model_task": "DRAFT",
            "prompt_manifest": {},
        },
    )

    response = await handle_ingress(envelope.model_dump(mode="json"))

    assert response.status_code == 403
    assert response.error.code == (
        "MODEL_BOUNDARY.ALL_MODEL_ACCESS_REQUIRES_EXPLICIT_AUTHORIZATION"
    )
    assert response.error.gate_failures[0].failure_type == "SECURITY_FAILURE"


@pytest.mark.asyncio
async def test_t13_memory_write_from_human_directly_rejected():
    identity = valid_identity_context(actor_type="HUMAN")
    envelope = build_valid_envelope(
        identity=identity,
        operation="memory.create",
    )

    response = await handle_ingress(envelope.model_dump(mode="json"))

    assert response.status_code == 403
    assert response.error.code == "MEMORY.MUTATION_REQUIRES_STATE_MACHINE_RUNNER"
    assert response.error.gate_failures[0].failure_type == "SECURITY_FAILURE"


@pytest.mark.asyncio
async def test_t14_superseded_memory_update_returns_409(mock_memory_store, sm_context):
    memory_id = mock_memory_store.seed_record(state="SUPERSEDED")

    response = await mock_memory_store.update_memory(
        sm_context,
        memory_id,
        {"payload": "update attempt"},
    )

    assert response.status_code == 409
    assert response.error.code == "MEMORY.UPDATE_SUPERSEDED_RECORD"
    assert any(
        failure.failure_type == "BLOCKER"
        for failure in response.error.gate_failures
    )


@pytest.mark.asyncio
async def test_t15_retrieval_bundle_cross_boundary_item_rejected(mock_archivist):
    identity = valid_identity_context()
    rogue_entity_id = uuid4()

    mock_archivist.inject_rogue_result(
        applied_as_entity_id=rogue_entity_id
    )

    envelope = build_valid_envelope(
        identity=identity,
        operation="archivist.retrieve",
        payload={
            "query_text": "retrieve evidence",
            "purpose": "Cross boundary retrieval test",
            "target_resource_type": "EVIDENCE",
            "max_items": 10,
            "max_tokens": 5000,
        },
    )

    response = await handle_ingress(envelope.model_dump(mode="json"))

    assert response.status_code == 403
    assert response.error.code == "ARCHIVIST.CROSS_BOUNDARY_RESULT"
    assert response.error.gate_failures[0].failure_type == "SECURITY_FAILURE"
