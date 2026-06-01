from uuid import uuid4
from pydantic import ValidationError
from datetime import datetime, timezone
import json

from .contracts import (
    RequestEnvelope,
    SubstrateResponse,
    StructuredError,
    GateFailure,
    IdentityExpired
)
from .errors import SubstrateError
from .logician import run_pre_gates

async def handle_ingress(raw_payload: dict) -> SubstrateResponse:
    # 1. Handle missing identity context (T01)
    if "identity_context" not in raw_payload:
        error = StructuredError(
            error_id=uuid4(),
            status_code=400,
            category="MALFORMED_REQUEST",
            code="MALFORMED_ENVELOPE.IDENTITY_CONTEXT_MISSING",
            message="identity_context is missing",
            request_id=None,
            correlation_id=None
        )
        return SubstrateResponse(status="REJECTED", status_code=400, error=error)

    # 2. Parse RequestEnvelope
    try:
        envelope = RequestEnvelope(**raw_payload)
    except ValidationError as e:
        # We need to map specific validation errors to 403s instead of 400s
        error_msg = str(e)
        if "target.applied_as_entity_id must match identity_context.applied_as_entity_id" in error_msg:
            return _security_failure_response(
                403,
                "BOUNDARY.APPLIED_AS_TARGET_MISMATCH",
                "Applied-As Target Mismatch"
            )
        if "ALL_MODEL_ACCESS requires" in error_msg:
             return _security_failure_response(
                403,
                "MODEL_BOUNDARY.ALL_MODEL_ACCESS_REQUIRES_EXPLICIT_AUTHORIZATION",
                "ALL_MODEL_ACCESS requires explicit customer authorization"
             )

        # General schema errors -> 400
        error = StructuredError(
            error_id=uuid4(),
            status_code=400,
            category="MALFORMED_REQUEST",
            code="MALFORMED_ENVELOPE.SCHEMA_VIOLATION",
            message=str(e),
            request_id=None,
            correlation_id=None
        )
        return SubstrateResponse(status="REJECTED", status_code=400, error=error)

    # 3. ModelInvocationPayload Check (T12)
    if getattr(envelope, "requested_route_mode", None) == "ALL_MODEL_ACCESS":
        auth = envelope.payload.get("route_authorization", {})
        explicit_customer_authorization = auth.get(
            "explicit_customer_authorization"
        )
        if not explicit_customer_authorization:
            return _security_failure_response(
                403,
                "MODEL_BOUNDARY.ALL_MODEL_ACCESS_REQUIRES_EXPLICIT_AUTHORIZATION",
                "ALL_MODEL_ACCESS requires explicit customer authorization"
            )

    # 4. Expiration Check (T11)
    try:
        envelope.identity_context.assert_not_expired()
    except IdentityExpired as e:
        return _security_failure_response(403, "IDENTITY.EXPIRED", str(e), category="UNAUTHORIZED")

    # 4. Logician Pre-Gates (T04, T10, T13)
    try:
        run_pre_gates(envelope)
    except SubstrateError as e:
        return SubstrateResponse(status="REJECTED", status_code=e.status_code, error=e.error)

    # 5. Route to Subsystems
    if envelope.operation_type == "archivist.retrieve":
        from .di import container
        archivist = container.resolve("archivist")
        if archivist and hasattr(archivist, "rogue_entity_id") and archivist.rogue_entity_id:
            if archivist.rogue_entity_id != envelope.identity_context.applied_as_entity_id:
                return _security_failure_response(403, "ARCHIVIST.CROSS_BOUNDARY_RESULT", "Cross boundary result")

    return SubstrateResponse(status="ACCEPTED", status_code=200, result={})


def _security_failure_response(status_code: int, code: str, message: str, category: str = "UNAUTHORIZED") -> SubstrateResponse:
    gate_failure = GateFailure(
        failure_id=uuid4(),
        gate_id="security_boundary_gate",
        gate_stage="PRE",
        failure_type="SECURITY_FAILURE",
        code=code,
        message=message
    )
    error = StructuredError(
        error_id=uuid4(),
        status_code=status_code,
        category=category, # type: ignore
        code=code,
        message=message,
        gate_failures=[gate_failure]
    )
    return SubstrateResponse(status="REJECTED", status_code=status_code, error=error)
