import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from pipeline.nervous_system.models import (
    StewardCommandProposal,
    StewardProposalStatus,
    StewardProposalSource,
    StewardRiskClass,
    StewardAllowedCommand,
    StewardCommandRegistryEntry,
    STEWARD_COMMAND_REGISTRY,
    STEWARD_COMMAND_REGISTRY_BY_COMMAND,
    STEWARD_FORBIDDEN_OUTPUTS,
    StewardHandlerFamily
)

def build_valid_base_proposal(overrides=None):
    base = {
        "proposal_id": "test-prop-123",
        "proposed_command": "open_route",
        "proposal_source": "TEXT",
        "operator_review_summary": "Test summary",
        "rationale": "Test rationale",
        "posture_at_creation": "SPLIT_CONTEXT_HYBRID",
        "created_at": datetime.now(timezone.utc)
    }
    if overrides:
        base.update(overrides)
    return base

def test_steward_proposal_defaults():
    data = build_valid_base_proposal()
    proposal = StewardCommandProposal(**data)

    # defaults to PENDING_OPERATOR_REVIEW
    assert proposal.status == StewardProposalStatus.PENDING_OPERATOR_REVIEW
    # does not default dispatch_allowed to true
    assert proposal.dispatch_allowed is False
    # requires_operator_review should be true
    assert proposal.requires_operator_review is True
    # risk class should be REVIEW_REQUIRED
    assert proposal.risk_class == StewardRiskClass.REVIEW_REQUIRED

def test_rejects_forbidden_commands():
    FORBIDDEN_COMMANDS = [
        "commit_evidence",
        "export_packet",
        "submit_application",
        "sign_override",
        "final_packet_authorization",
        "change_posture",
        "resolve_sync_conflict",
        "delete_audit_event",
        "change_applied_as_entity",
        "draft_section_saved",
        "gate_pass",
        "signature_verified",
    ]

    for cmd in FORBIDDEN_COMMANDS:
        data = build_valid_base_proposal({"proposed_command": cmd})
        with pytest.raises(ValidationError) as exc_info:
            StewardCommandProposal(**data)
        assert "proposed_command" in str(exc_info.value)

def test_requires_operator_review_summary():
    data = build_valid_base_proposal()
    del data["operator_review_summary"]

    with pytest.raises(ValidationError) as exc_info:
        StewardCommandProposal(**data)
    assert "operator_review_summary" in str(exc_info.value)

def test_requires_posture_at_creation():
    data = build_valid_base_proposal()
    del data["posture_at_creation"]

    with pytest.raises(ValidationError) as exc_info:
        StewardCommandProposal(**data)
    assert "posture_at_creation" in str(exc_info.value)

def test_preserves_target_ids():
    data = build_valid_base_proposal({
        "target_gate_ids": ["gate-1", "gate-2"],
        "target_section_ids": ["sec-1"],
        "target_evidence_ids": ["ev-1", "ev-2", "ev-3"]
    })
    proposal = StewardCommandProposal(**data)

    assert proposal.target_gate_ids == ["gate-1", "gate-2"]
    assert proposal.target_section_ids == ["sec-1"]
    assert proposal.target_evidence_ids == ["ev-1", "ev-2", "ev-3"]

def test_forbids_extra_fields():
    data = build_valid_base_proposal({"extra_unexpected_field": "value"})

    with pytest.raises(ValidationError) as exc_info:
        StewardCommandProposal(**data)
    assert "extra_unexpected_field" in str(exc_info.value)
    assert "Extra inputs are not permitted" in str(exc_info.value)

def test_accepts_transcript_id_as_context():
    data = build_valid_base_proposal({
        "transcript_id": "transcript-456",
        "proposal_source": "VOICE_TRANSCRIPT"
    })
    proposal = StewardCommandProposal(**data)
    assert proposal.transcript_id == "transcript-456"

def test_accepted_for_dispatch_forbids_canonical_event_fields():
    # If a proposal is accepted, it is still a proposal.
    # It must not include event_id, lock_id, etc.
    data = build_valid_base_proposal({
        "status": "ACCEPTED_FOR_DISPATCH",
        "event_id": "evt-123"
    })
    with pytest.raises(ValidationError) as exc_info:
        StewardCommandProposal(**data)
    assert "event_id" in str(exc_info.value)

    data = build_valid_base_proposal({
        "status": "ACCEPTED_FOR_DISPATCH",
        "signature_event_id": "sig-123"
    })
    with pytest.raises(ValidationError) as exc_info:
        StewardCommandProposal(**data)
    assert "signature_event_id" in str(exc_info.value)

    data = build_valid_base_proposal({
        "status": "ACCEPTED_FOR_DISPATCH",
        "lock_id": "lock-123"
    })
    with pytest.raises(ValidationError) as exc_info:
        StewardCommandProposal(**data)
    assert "lock_id" in str(exc_info.value)

def test_rejects_requires_operator_review_false():
    data = build_valid_base_proposal({
        "requires_operator_review": False
    })

    with pytest.raises(ValidationError) as exc_info:
        StewardCommandProposal(**data)
    # Pydantic will complain that False is not True (since it's Literal[True])
    assert "requires_operator_review" in str(exc_info.value)

# --- Phase 5C Tests ---

from pipeline.nervous_system.models import (
    CommandDispatchIntent,
    CommandDispatchReceipt,
    CommandDispatchStatus
)

def build_valid_dispatch_intent(overrides=None):
    base = {
        "proposal_id": "test-prop-123",
        "proposal_status_at_acceptance": "ACCEPTED_FOR_DISPATCH",
        "accepted_at": datetime.now(timezone.utc),
    }
    if overrides:
        base.update(overrides)
    return base

def build_valid_dispatch_receipt(overrides=None):
    base = {
        "receipt_id": "rec-123",
        "proposal_id": "test-prop-123",
        "status": "ACCEPTED_FOR_HANDLER_REVIEW",
        "reviewed_at": datetime.now(timezone.utc),
    }
    if overrides:
        base.update(overrides)
    return base

def test_command_dispatch_intent_requires_accepted_status():
    data = build_valid_dispatch_intent({
        "proposal_status_at_acceptance": "PENDING_OPERATOR_REVIEW"
    })
    with pytest.raises(ValidationError) as exc_info:
        CommandDispatchIntent(**data)
    assert "proposal_status_at_acceptance" in str(exc_info.value)

def test_command_dispatch_intent_forbids_extra_fields():
    data = build_valid_dispatch_intent({
        "extra_unexpected_field": "value"
    })
    with pytest.raises(ValidationError) as exc_info:
        CommandDispatchIntent(**data)
    assert "extra_unexpected_field" in str(exc_info.value)

def test_command_dispatch_receipt_rejects_canonical_fields():
    forbidden_fields = [
        ("event_id", "evt-123"),
        ("signature_event_id", "sig-123"),
        ("lock_id", "lock-123"),
        ("export_id", "exp-123"),
        ("submitted_at", datetime.now(timezone.utc).isoformat()),
        ("artifact_hash", "hash-123"),
        ("operator_signature_event_id", "sig-456")
    ]

    for field, val in forbidden_fields:
        data = build_valid_dispatch_receipt({field: val})
        with pytest.raises(ValidationError) as exc_info:
            CommandDispatchReceipt(**data)
        assert field in str(exc_info.value)

def test_command_dispatch_receipt_can_reject_by_stale_projection():
    data = build_valid_dispatch_receipt({
        "status": CommandDispatchStatus.REJECTED_BY_STALE_PROJECTION
    })
    receipt = CommandDispatchReceipt(**data)
    assert receipt.status == CommandDispatchStatus.REJECTED_BY_STALE_PROJECTION

def test_command_dispatch_receipt_can_reject_by_sync_conflict():
    data = build_valid_dispatch_receipt({
        "status": CommandDispatchStatus.REJECTED_BY_SYNC_CONFLICT
    })
    receipt = CommandDispatchReceipt(**data)
    assert receipt.status == CommandDispatchStatus.REJECTED_BY_SYNC_CONFLICT

def test_accepted_for_handler_review_may_include_handler_assigned():
    data = build_valid_dispatch_receipt({
        "status": CommandDispatchStatus.ACCEPTED_FOR_HANDLER_REVIEW,
        "handler_assigned": "handler-1"
    })
    receipt = CommandDispatchReceipt(**data)
    assert receipt.handler_assigned == "handler-1"

def test_rejected_by_policy_does_not_require_handler_assigned():
    data = build_valid_dispatch_receipt({
        "status": CommandDispatchStatus.REJECTED_BY_POLICY
    })
    receipt = CommandDispatchReceipt(**data)
    assert receipt.handler_assigned is None

def test_operator_acceptance_signature_does_not_create_signature_event_id():
    data = build_valid_dispatch_intent({
        "operator_acceptance_signature": "sig-123"
    })
    intent = CommandDispatchIntent(**data)
    assert intent.operator_acceptance_signature == "sig-123"
    assert not hasattr(intent, "signature_event_id")

def test_every_steward_allowed_command_appears_exactly_once():
    commands_in_registry = [entry.command for entry in STEWARD_COMMAND_REGISTRY]
    assert len(commands_in_registry) == len(StewardAllowedCommand)
    assert set(commands_in_registry) == set(StewardAllowedCommand)

def test_registry_by_command_has_same_cardinality():
    assert len(STEWARD_COMMAND_REGISTRY_BY_COMMAND) == len(StewardAllowedCommand)
    for cmd in StewardAllowedCommand:
        assert cmd in STEWARD_COMMAND_REGISTRY_BY_COMMAND

def test_every_registry_entry_includes_all_forbidden_outputs():
    for entry in STEWARD_COMMAND_REGISTRY:
        assert set(entry.forbidden_outputs) == set(STEWARD_FORBIDDEN_OUTPUTS)

def test_constructing_entry_with_missing_forbidden_outputs_raises():
    with pytest.raises(ValidationError) as exc:
        StewardCommandRegistryEntry(
            command=StewardAllowedCommand.OPEN_ROUTE,
            handler_family=StewardHandlerFamily.NAVIGATION,
            default_risk_class=StewardRiskClass.LOW,
            forbidden_outputs=["event_id"]  # deliberately missing others
        )
    assert "registry entry missing forbidden outputs" in str(exc.value)

def test_dispatch_review_allowed_false_is_rejected():
    with pytest.raises(ValidationError):
        StewardCommandRegistryEntry(
            command=StewardAllowedCommand.OPEN_ROUTE,
            handler_family=StewardHandlerFamily.NAVIGATION,
            default_risk_class=StewardRiskClass.LOW,
            dispatch_review_allowed=False
        )

def test_no_registry_entry_defaults_to_forbidden():
    for entry in STEWARD_COMMAND_REGISTRY:
        assert entry.default_risk_class != StewardRiskClass.FORBIDDEN

def test_may_require_signature_ceremony_does_not_create_artifacts():
    # Proof by structural absence: we cannot pass signature artifacts because they are forbidden
    entry = STEWARD_COMMAND_REGISTRY_BY_COMMAND[StewardAllowedCommand.PREPARE_RISK_OVERRIDE_RATIONALE]
    assert entry.may_require_signature_ceremony is True
    assert "signature_event_id" in entry.forbidden_outputs
    assert "operator_signature_event_id" in entry.forbidden_outputs

def test_steward_command_proposal_rejects_forbidden_execution_commands_via_enum():
    with pytest.raises(ValidationError):
        StewardCommandProposal(**build_valid_base_proposal(overrides={"proposed_command": "commit_evidence"}))
