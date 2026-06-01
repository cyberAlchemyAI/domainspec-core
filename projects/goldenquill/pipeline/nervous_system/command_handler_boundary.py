from enum import Enum
from typing import Optional, List, Literal, Any, Dict
from pydantic import BaseModel, Field, ConfigDict, model_validator

from pipeline.nervous_system.models import (
    CommandDispatchIntent,
    StewardCommandProposal,
    STEWARD_COMMAND_REGISTRY_BY_COMMAND,
    StewardHandlerFamily,
    StewardAllowedCommand,
    IdentityContext
)

class CommandHandlerValidationStatus(str, Enum):
    VALIDATED_FOR_HANDLER = "VALIDATED_FOR_HANDLER"
    REJECTED_UNKNOWN_COMMAND = "REJECTED_UNKNOWN_COMMAND"
    REJECTED_HANDLER_FAMILY_MISMATCH = "REJECTED_HANDLER_FAMILY_MISMATCH"
    REJECTED_IDENTITY_BOUNDARY = "REJECTED_IDENTITY_BOUNDARY"
    REJECTED_APPLIED_AS_BOUNDARY = "REJECTED_APPLIED_AS_BOUNDARY"
    REJECTED_POSTURE = "REJECTED_POSTURE"
    REJECTED_OUTPUT_TYPE = "REJECTED_OUTPUT_TYPE"
    REJECTED_ARTIFACT_TYPE = "REJECTED_ARTIFACT_TYPE"
    REJECTED_FINAL_AUTHORITY = "REJECTED_FINAL_AUTHORITY"
    REJECTED_POLICY = "REJECTED_POLICY"

class CommandHandlerValidationRequest(BaseModel):
    intent: CommandDispatchIntent
    proposal: StewardCommandProposal

    model_config = ConfigDict(extra="forbid")

class CommandHandlerValidationResult(BaseModel):
    status: CommandHandlerValidationStatus
    reason: Optional[str] = None

    # Must not contain any canonical execution metadata:
    # event_id, lock_id, signature, canonical_event_hash, committed_at, execution_result, memory mutation proof
    # Pydantic's extra="forbid" enforces this.

    model_config = ConfigDict(extra="forbid")

# Allowed handler families for this boundary phase
ALLOWLISTED_HANDLER_FAMILIES = {
    StewardHandlerFamily.NAVIGATION,
    StewardHandlerFamily.COMMUNICATION_DRAFT,
    StewardHandlerFamily.AUDIT_EXPLANATION,
    StewardHandlerFamily.GATE_EXPLANATION,
    StewardHandlerFamily.RISK_RATIONALE_PREP,
    StewardHandlerFamily.EVIDENCE_REQUEST_PREP,
    StewardHandlerFamily.CLAIM_AMENDMENT_PREP,
    StewardHandlerFamily.DRAFT_REQUEST_PREP,
    StewardHandlerFamily.BUDGET_RECHECK_PREP,
    StewardHandlerFamily.RESCORE_REQUEST_PREP
}

class CommandHandlerBoundary:
    @staticmethod
    def validate(request: CommandHandlerValidationRequest) -> CommandHandlerValidationResult:
        intent = request.intent
        proposal = request.proposal

        # 6. Identity context must be present
        if not intent.identity_context:
            return CommandHandlerValidationResult(
                status=CommandHandlerValidationStatus.REJECTED_IDENTITY_BOUNDARY,
                reason="Identity context is missing from intent."
            )

        identity = intent.identity_context

        # 1. Command must exist in StewardCommandRegistryEntry
        registry_entry = STEWARD_COMMAND_REGISTRY_BY_COMMAND.get(proposal.proposed_command)
        if not registry_entry:
            return CommandHandlerValidationResult(
                status=CommandHandlerValidationStatus.REJECTED_UNKNOWN_COMMAND,
                reason=f"Unknown command: {proposal.proposed_command}"
            )

        # 2. Command must belong to an allowlisted handler family
        if registry_entry.handler_family not in ALLOWLISTED_HANDLER_FAMILIES:
            return CommandHandlerValidationResult(
                status=CommandHandlerValidationStatus.REJECTED_HANDLER_FAMILY_MISMATCH,
                reason=f"Handler family not allowlisted: {registry_entry.handler_family}"
            )

        # 7. Applied As boundary must be preserved
        # The proposal applied_as_entity_id should match the intent's identity context
        if proposal.applied_as_entity_id and proposal.applied_as_entity_id != identity.applied_as:
            return CommandHandlerValidationResult(
                status=CommandHandlerValidationStatus.REJECTED_APPLIED_AS_BOUNDARY,
                reason="Proposal applied_as_entity_id does not match identity context."
            )

        payload = proposal.payload
        artifact_type = payload.get("artifact_type")
        output_types = payload.get("output_types", [])

        # 3. Intent payload must match the registry's expected input contract
        for field in registry_entry.required_context_fields:
            if field not in payload:
                return CommandHandlerValidationResult(
                    status=CommandHandlerValidationStatus.REJECTED_POLICY,
                    reason=f"Missing required context field: {field}"
                )

        # 4. Output type must be allowed
        for ot in output_types:
            if ot in registry_entry.forbidden_outputs:
                return CommandHandlerValidationResult(
                    status=CommandHandlerValidationStatus.REJECTED_OUTPUT_TYPE,
                    reason=f"Output type {ot} is forbidden for command."
                )

        # 5. Artifact type must be allowed
        # (This rule overlaps with consulting doctrine checks below)

        # 8. Consulting node doctrine must be enforced:
        is_fit_farms = identity.applied_as == "fit-farms"

        if artifact_type == "FIT_FARMS_SUBMISSION_PACKET":
            if not is_fit_farms:
                return CommandHandlerValidationResult(
                    status=CommandHandlerValidationStatus.REJECTED_FINAL_AUTHORITY,
                    reason="FIT_FARMS_SUBMISSION_PACKET requires applied_as to be fit-farms."
                )

        if artifact_type == "THIRD_PARTY_DRAFT_DELIVERABLE":
            if "final_submission" in output_types or "export" in output_types:
                return CommandHandlerValidationResult(
                    status=CommandHandlerValidationStatus.REJECTED_FINAL_AUTHORITY,
                    reason="Third-party final submission/export is rejected."
                )

        # "Third-party final submission/export must be rejected."
        if not is_fit_farms:
            if artifact_type == "THIRD_PARTY_FINAL_SUBMISSION" or "final_submission" in output_types or "export" in output_types:
                return CommandHandlerValidationResult(
                    status=CommandHandlerValidationStatus.REJECTED_FINAL_AUTHORITY,
                    reason="Third-party final submission/export is rejected."
                )

        return CommandHandlerValidationResult(
            status=CommandHandlerValidationStatus.VALIDATED_FOR_HANDLER
        )
