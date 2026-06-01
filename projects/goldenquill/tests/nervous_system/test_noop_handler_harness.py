import pytest
import inspect
from datetime import datetime, timezone
from pydantic import ValidationError

from pipeline.nervous_system.models import (
    StewardAllowedCommand,
    StewardHandlerFamily,
    StewardCommandProposal,
    STEWARD_COMMAND_REGISTRY_BY_COMMAND
)
from pipeline.nervous_system.command_handler_boundary import (
    CommandHandlerValidationResult,
    CommandHandlerValidationStatus
)
from pipeline.nervous_system.noop_handler_harness import (
    NoOpHandlerHarness,
    NoOpHandlerStatus,
    NoOpHandlerDryRunResult
)

def create_proposal(command: StewardAllowedCommand, payload=None) -> StewardCommandProposal:
    return StewardCommandProposal(
        proposal_id="prop-123",
        proposed_command=command,
        proposal_source="TEXT",
        operator_review_summary="Test review",
        rationale="Test rationale",
        posture_at_creation="LOCAL_ONLY_SOVEREIGN",
        created_at=datetime.now(timezone.utc),
        applied_as_entity_id="fit-farms",
        payload=payload or {"route_id": "test"}
    )

def create_valid_result() -> CommandHandlerValidationResult:
    return CommandHandlerValidationResult(
        status=CommandHandlerValidationStatus.VALIDATED_FOR_HANDLER
    )

def create_rejected_result() -> CommandHandlerValidationResult:
    return CommandHandlerValidationResult(
        status=CommandHandlerValidationStatus.REJECTED_POLICY,
        reason="Test rejection"
    )

def test_dry_run_preview_open_route_no_side_effects():
    proposal = create_proposal(StewardAllowedCommand.OPEN_ROUTE)
    res = NoOpHandlerHarness.evaluate(proposal, create_valid_result())

    assert res.status in (NoOpHandlerStatus.DRY_RUN_PREVIEW_READY, NoOpHandlerStatus.DRY_RUN_REQUIRES_OPERATOR_REVIEW)
    assert res.command == StewardAllowedCommand.OPEN_ROUTE
    assert "without side effects" in res.preview_summary

def test_dry_run_preview_generate_email_draft_without_sending():
    proposal = create_proposal(StewardAllowedCommand.GENERATE_EMAIL_DRAFT, payload={"draft_topic": "hello"})
    res = NoOpHandlerHarness.evaluate(proposal, create_valid_result())

    assert res.command == StewardAllowedCommand.GENERATE_EMAIL_DRAFT
    assert "sending prevented" in res.preview_summary

def test_dry_run_preview_prepare_claim_amendment():
    proposal = create_proposal(StewardAllowedCommand.PREPARE_CLAIM_AMENDMENT, payload={"claim_id": "123"})
    res = NoOpHandlerHarness.evaluate(proposal, create_valid_result())

    assert res.command == StewardAllowedCommand.PREPARE_CLAIM_AMENDMENT
    assert "without mutating claim record" in res.preview_summary

def test_dry_run_preview_prepare_risk_override_rationale():
    proposal = create_proposal(StewardAllowedCommand.PREPARE_RISK_OVERRIDE_RATIONALE, payload={"risk_id": "999"})
    res = NoOpHandlerHarness.evaluate(proposal, create_valid_result())

    assert res.command == StewardAllowedCommand.PREPARE_RISK_OVERRIDE_RATIONALE
    assert "signature prevented" in res.preview_summary

def test_dry_run_rejects_canonical_execution_metadata():
    with pytest.raises(ValidationError) as exc:
        NoOpHandlerDryRunResult(
            dry_run_id="123",
            proposal_id="prop-123",
            command=StewardAllowedCommand.OPEN_ROUTE,
            handler_family=StewardHandlerFamily.NAVIGATION,
            status=NoOpHandlerStatus.DRY_RUN_PREVIEW_READY,
            preview_summary="ok",
            event_id="evt-123"
        )
    assert "event_id" in str(exc.value)

    with pytest.raises(ValidationError):
        NoOpHandlerDryRunResult(
            dry_run_id="123", proposal_id="prop", command=StewardAllowedCommand.OPEN_ROUTE,
            handler_family=StewardHandlerFamily.NAVIGATION, status=NoOpHandlerStatus.DRY_RUN_PREVIEW_READY,
            preview_summary="ok", lock_id="lck-123"
        )

def test_every_allowed_command_maps_to_dry_run_preview_path():
    for cmd in StewardAllowedCommand:
        proposal = create_proposal(cmd)
        # Just provide minimal required payload context so validation structure works
        # though the NoOpHandler doesn't enforce payload validation, it passes it through.
        res = NoOpHandlerHarness.evaluate(proposal, create_valid_result())

        assert isinstance(res, NoOpHandlerDryRunResult)
        assert res.command == cmd
        assert "DRY RUN" in str(res.warnings).upper()

def test_dry_run_output_references_handler_family_but_does_not_invoke_real_handler():
    proposal = create_proposal(StewardAllowedCommand.OPEN_ROUTE)
    res = NoOpHandlerHarness.evaluate(proposal, create_valid_result())

    # Structural proof that it references family but has no execution payload
    assert res.handler_family == StewardHandlerFamily.NAVIGATION
    assert not hasattr(res, "execute")

def test_harness_cannot_call_forbidden_functions():
    # We statically assert the module imports to prove it has no capability to execute network/db calls
    import pipeline.nervous_system.noop_handler_harness as harness_module

    forbidden_builtins = ["subprocess", "requests", "db", "portal"]
    module_dict = harness_module.__dict__

    for f in forbidden_builtins:
        assert f not in module_dict, f"Harness cannot import or use {f}"

    # Also assert none of the harness functions have side-effects
    source = inspect.getsource(harness_module)
    forbidden_tokens = [
        "append_event", "db.commit", "requests.post", "subprocess",
        "portal_submit", "export_packet", "commit_evidence"
    ]
    for token in forbidden_tokens:
        assert token not in source, f"Harness source contains forbidden token {token}"
