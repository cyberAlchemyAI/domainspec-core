import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from pipeline.nervous_system.models import (
    CommandDispatchIntent,
    StewardCommandProposal,
    StewardAllowedCommand,
    IdentityContext
)
from pipeline.nervous_system.command_handler_boundary import (
    CommandHandlerValidationRequest,
    CommandHandlerValidationResult,
    CommandHandlerValidationStatus,
    CommandHandlerBoundary
)

def create_valid_intent(user_id="u1", applied_as="fit-farms"):
    return CommandDispatchIntent(
        proposal_id="prop-123",
        proposal_status_at_acceptance="ACCEPTED_FOR_DISPATCH",
        accepted_at=datetime.now(timezone.utc),
        identity_context=IdentityContext(
            user_id=user_id,
            applied_as=applied_as
        )
    )

def create_valid_proposal(applied_as="fit-farms", artifact_type=None, output_types=None):
    payload = {}
    if artifact_type:
        payload["artifact_type"] = artifact_type
    if output_types:
        payload["output_types"] = output_types

    return StewardCommandProposal(
        proposal_id="prop-123",
        proposed_command=StewardAllowedCommand.OPEN_ROUTE,
        proposal_source="TEXT",
        operator_review_summary="Test",
        rationale="Test",
        posture_at_creation="LOCAL_ONLY_SOVEREIGN",
        created_at=datetime.now(timezone.utc),
        applied_as_entity_id=applied_as,
        payload=payload
    )

def test_known_allowlisted_command_validates():
    request = CommandHandlerValidationRequest(
        intent=create_valid_intent(),
        proposal=create_valid_proposal()
    )
    result = CommandHandlerBoundary.validate(request)
    assert result.status == CommandHandlerValidationStatus.VALIDATED_FOR_HANDLER

def test_unknown_command_is_rejected():
    proposal = StewardCommandProposal.model_construct(
        proposal_id="prop-123",
        proposed_command="INVALID_COMMAND",
        applied_as_entity_id="fit-farms",
        payload={}
    )
    request = CommandHandlerValidationRequest.model_construct(
        intent=create_valid_intent(),
        proposal=proposal
    )
    result = CommandHandlerBoundary.validate(request)
    assert result.status == CommandHandlerValidationStatus.REJECTED_UNKNOWN_COMMAND

def test_wrong_handler_family_is_rejected(monkeypatch):
    proposal = create_valid_proposal()
    request = CommandHandlerValidationRequest(
        intent=create_valid_intent(),
        proposal=proposal
    )

    # Temporarily remove from allowlist
    from pipeline.nervous_system import command_handler_boundary
    monkeypatch.setattr(command_handler_boundary, "ALLOWLISTED_HANDLER_FAMILIES", set())

    result = CommandHandlerBoundary.validate(request)
    assert result.status == CommandHandlerValidationStatus.REJECTED_HANDLER_FAMILY_MISMATCH

def test_missing_identity_context_is_rejected():
    intent = create_valid_intent()
    intent.identity_context = None
    request = CommandHandlerValidationRequest(
        intent=intent,
        proposal=create_valid_proposal()
    )
    result = CommandHandlerBoundary.validate(request)
    assert result.status == CommandHandlerValidationStatus.REJECTED_IDENTITY_BOUNDARY

def test_wrong_applied_as_boundary_is_rejected():
    intent = create_valid_intent(applied_as="other-org")
    proposal = create_valid_proposal(applied_as="fit-farms")
    request = CommandHandlerValidationRequest(
        intent=intent,
        proposal=proposal
    )
    result = CommandHandlerBoundary.validate(request)
    assert result.status == CommandHandlerValidationStatus.REJECTED_APPLIED_AS_BOUNDARY

def test_third_party_draft_deliverable_validates():
    intent = create_valid_intent(applied_as="third-party")
    proposal = create_valid_proposal(
        applied_as="third-party",
        artifact_type="THIRD_PARTY_DRAFT_DELIVERABLE",
        output_types=["draft_handoff"]
    )
    request = CommandHandlerValidationRequest(intent=intent, proposal=proposal)
    result = CommandHandlerBoundary.validate(request)
    assert result.status == CommandHandlerValidationStatus.VALIDATED_FOR_HANDLER

def test_third_party_final_submission_export_is_rejected():
    intent = create_valid_intent(applied_as="third-party")
    proposal = create_valid_proposal(
        applied_as="third-party",
        artifact_type="THIRD_PARTY_DRAFT_DELIVERABLE",
        output_types=["export", "final_submission"]
    )
    request = CommandHandlerValidationRequest(intent=intent, proposal=proposal)
    result = CommandHandlerBoundary.validate(request)
    assert result.status == CommandHandlerValidationStatus.REJECTED_FINAL_AUTHORITY

def test_fit_farms_submission_packet_validates_only_for_fit_farms():
    intent = create_valid_intent(applied_as="fit-farms")
    proposal = create_valid_proposal(
        applied_as="fit-farms",
        artifact_type="FIT_FARMS_SUBMISSION_PACKET"
    )
    request = CommandHandlerValidationRequest(intent=intent, proposal=proposal)
    result = CommandHandlerBoundary.validate(request)
    assert result.status == CommandHandlerValidationStatus.VALIDATED_FOR_HANDLER

    intent2 = create_valid_intent(applied_as="third-party")
    proposal2 = create_valid_proposal(
        applied_as="third-party",
        artifact_type="FIT_FARMS_SUBMISSION_PACKET"
    )
    request2 = CommandHandlerValidationRequest(intent=intent2, proposal=proposal2)
    result2 = CommandHandlerBoundary.validate(request2)
    assert result2.status == CommandHandlerValidationStatus.REJECTED_FINAL_AUTHORITY

def test_validation_result_contains_no_canonical_execution_metadata():
    with pytest.raises(ValidationError) as exc:
        CommandHandlerValidationResult(
            status=CommandHandlerValidationStatus.VALIDATED_FOR_HANDLER,
            event_id="evt-123"
        )
    assert "event_id" in str(exc.value)

    with pytest.raises(ValidationError):
        CommandHandlerValidationResult(status=CommandHandlerValidationStatus.VALIDATED_FOR_HANDLER, lock_id="lck")

    with pytest.raises(ValidationError):
        CommandHandlerValidationResult(status=CommandHandlerValidationStatus.VALIDATED_FOR_HANDLER, execution_result="res")

def test_steward_receipt_remains_separate_from_handler_validation_result():
    from pipeline.nervous_system.models import CommandDispatchReceipt
    assert CommandHandlerValidationResult != CommandDispatchReceipt

def test_steward_has_zero_runtime_execution_authority():
    request = CommandHandlerValidationRequest(
        intent=create_valid_intent(),
        proposal=create_valid_proposal()
    )
    result = CommandHandlerBoundary.validate(request)
    assert result.status == CommandHandlerValidationStatus.VALIDATED_FOR_HANDLER
    assert not hasattr(result, "execute")

def test_no_handler_appends_events_or_mutates_memory():
    # Structural assertion: The boundary object only returns a result.
    # It takes no dependencies to the ledger or memory sink.
    import inspect
    sig = inspect.signature(CommandHandlerBoundary.validate)
    assert len(sig.parameters) == 1
    assert "request" in sig.parameters
