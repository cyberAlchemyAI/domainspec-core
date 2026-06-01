from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict
import uuid

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

class NoOpHandlerStatus(str, Enum):
    DRY_RUN_PREVIEW_READY = "DRY_RUN_PREVIEW_READY"
    DRY_RUN_REJECTED_BY_VALIDATION = "DRY_RUN_REJECTED_BY_VALIDATION"
    DRY_RUN_REQUIRES_SIGNATURE_CEREMONY = "DRY_RUN_REQUIRES_SIGNATURE_CEREMONY"
    DRY_RUN_REQUIRES_OPERATOR_REVIEW = "DRY_RUN_REQUIRES_OPERATOR_REVIEW"

class NoOpHandlerDryRunResult(BaseModel):
    dry_run_id: str
    proposal_id: str
    command: StewardAllowedCommand
    handler_family: StewardHandlerFamily
    status: NoOpHandlerStatus
    preview_summary: str
    proposed_next_surface: Optional[str] = None
    proposed_payload_preview: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class NoOpHandlerHarness:
    @staticmethod
    def evaluate(proposal: StewardCommandProposal, validation_result: CommandHandlerValidationResult) -> NoOpHandlerDryRunResult:
        registry_entry = STEWARD_COMMAND_REGISTRY_BY_COMMAND.get(proposal.proposed_command)

        # If the command isn't in registry at all, or validation failed fundamentally
        if not registry_entry or validation_result.status != CommandHandlerValidationStatus.VALIDATED_FOR_HANDLER:
            # Note: For unknown commands we just fallback safely to avoid crashes during dry-run rejects
            cmd_enum = proposal.proposed_command if isinstance(proposal.proposed_command, StewardAllowedCommand) else StewardAllowedCommand.OPEN_ROUTE
            family = registry_entry.handler_family if registry_entry else StewardHandlerFamily.NAVIGATION

            return NoOpHandlerDryRunResult(
                dry_run_id=f"dry-{uuid.uuid4()}",
                proposal_id=proposal.proposal_id,
                command=cmd_enum,
                handler_family=family,
                status=NoOpHandlerStatus.DRY_RUN_REJECTED_BY_VALIDATION,
                preview_summary=f"Validation failed: {validation_result.status.value}",
                warnings=[validation_result.reason] if validation_result.reason else []
            )

        cmd = proposal.proposed_command
        family = registry_entry.handler_family
        payload = proposal.payload

        # Determine no-op preview status based on the entry policy
        if registry_entry.may_require_signature_ceremony:
            status = NoOpHandlerStatus.DRY_RUN_REQUIRES_SIGNATURE_CEREMONY
            summary = f"Signature ceremony required for {cmd.value}"
            surface = "CEREMONY_UI"
        elif proposal.requires_operator_review:
            status = NoOpHandlerStatus.DRY_RUN_REQUIRES_OPERATOR_REVIEW
            summary = f"Operator review required for {cmd.value}"
            surface = "REVIEW_UI"
        else:
            status = NoOpHandlerStatus.DRY_RUN_PREVIEW_READY
            summary = f"Dry-run ready for {cmd.value}"
            surface = "EXECUTION_PREVIEW_UI"

        # Special casing purely for preview paths based on command
        if cmd == StewardAllowedCommand.OPEN_ROUTE:
            summary = "Dry-run: Navigation intent verified without side effects."
            surface = "NAV_PREVIEW"
        elif cmd == StewardAllowedCommand.GENERATE_EMAIL_DRAFT:
            summary = "Dry-run: Email draft generated in preview memory, sending prevented."
            surface = "DRAFT_PREVIEW"
        elif cmd == StewardAllowedCommand.PREPARE_CLAIM_AMENDMENT:
            summary = "Dry-run: Claim amendment structures verified without mutating claim record."
            surface = "AMENDMENT_PREVIEW"
        elif cmd == StewardAllowedCommand.PREPARE_RISK_OVERRIDE_RATIONALE:
            summary = "Dry-run: Risk override rationale prepared, signature prevented."
            surface = "RISK_PREVIEW"

        return NoOpHandlerDryRunResult(
            dry_run_id=f"dry-{uuid.uuid4()}",
            proposal_id=proposal.proposal_id,
            command=cmd,
            handler_family=family,
            status=status,
            preview_summary=summary,
            proposed_next_surface=surface,
            proposed_payload_preview=payload,
            warnings=["DRY RUN ONLY. No execution occurred."]
        )
