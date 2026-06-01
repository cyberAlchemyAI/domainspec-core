from uuid import uuid4
from .contracts import RequestEnvelope, StructuredError, GateFailure
from .errors import SubstrateError

def run_pre_gates(envelope: RequestEnvelope) -> None:
    # T04: AI Attempts Evidence Promotion
    if envelope.operation_type == "evidence.promote" and envelope.identity_context.actor_type != "STATE_MACHINE_RUNNER":
        _raise_security_failure(403, "EVIDENCE.PROMOTION_REQUIRES_STATE_MACHINE", "Evidence promotion requires STATE_MACHINE_RUNNER")

    # T10: Final Packet Authorization by Non-Human
    if envelope.operation_type == "packet.authorize_final":
        if envelope.identity_context.actor_type != "HUMAN":
            _raise_security_failure(403, "AUTHORIZATION.HUMAN_REQUIRED", "Final packet authorization requires HUMAN")
        if not envelope.identity_context.is_human_final_authorization_capable():
            _raise_security_failure(403, "AUTHORIZATION.HUMAN_REQUIRED", "Final packet authorization requires HUMAN re-auth")
            
        # GUARD: Check Applied-As match
        if envelope.payload and envelope.identity_context.applied_as_entity_id != envelope.payload.get("target_entity_id"):
            _raise_security_failure(403, "AUTHORIZATION.APPLIED_AS_MISMATCH", "Target entity ID does not match Applied-As scope")

    # T13: Memory Write From Human Directly
    if envelope.operation_type in ("memory.create", "memory.update", "memory.supersede", "memory.retract"):
        if envelope.identity_context.actor_type != "STATE_MACHINE_RUNNER":
            _raise_security_failure(403, "MEMORY.MUTATION_REQUIRES_STATE_MACHINE_RUNNER", "Memory mutations require STATE_MACHINE_RUNNER")

def _raise_security_failure(status_code: int, code: str, message: str) -> None:
    gate_failure = GateFailure(
        failure_id=uuid4(),
        gate_id="logician_gate",
        gate_stage="PRE",
        failure_type="SECURITY_FAILURE",
        code=code,
        message=message
    )
    error = StructuredError(
        error_id=uuid4(),
        status_code=status_code,
        category="UNAUTHORIZED",
        code=code,
        message=message,
        gate_failures=[gate_failure]
    )
    raise SubstrateError(status_code, error)

def raise_blocker_failure(status_code: int, code: str, message: str, category: str = "INTERNAL_INVARIANT_BREACH") -> None:
    gate_failure = GateFailure(
        failure_id=uuid4(),
        gate_id="logician_gate",
        gate_stage="POST",
        failure_type="BLOCKER",
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
    raise SubstrateError(status_code, error)
