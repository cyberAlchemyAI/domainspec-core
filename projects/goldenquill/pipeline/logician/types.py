from typing import Literal

OutputType = Literal[
    "FIT_FARMS_SUBMISSION_PACKET",
    "THIRD_PARTY_DRAFT_DELIVERABLE",
]

ArtifactType = Literal[
    "working_draft",
    "draft_handoff_packet_pdf",
    "missing_info_list",
    "review_packet",
    "compliance_checklist",
    "final_submission_pdf",
    "submission_ready_packet",
    "final_packet_authorization",
    "applicant_certification",
    "operator_signed_submission_packet",
    "pdf",  # Legacy fallback for existing tests
]

GateStage = Literal[
    "draft_generation",
    "draft_review",
    "draft_handoff",
    "internal_review",
    "final_packet_authorization",
    "final_export",
    "final_export_attempt",
]

FINAL_OR_SUBMISSION_STAGES = frozenset({
    "final_packet_authorization",
    "final_export",
    "final_export_attempt",
})

THIRD_PARTY_FINAL_BLOCKED_ARTIFACTS = frozenset({
    "final_submission_pdf",
    "submission_ready_packet",
    "final_packet_authorization",
    "applicant_certification",
    "operator_signed_submission_packet",
})

THIRD_PARTY_HANDOFF_ARTIFACTS = frozenset({
    "working_draft",
    "draft_handoff_packet_pdf",
    "missing_info_list",
    "review_packet",
    "compliance_checklist",
})

def gate_should_block(result: object) -> bool:
    """Determine if a gate result should halt the runner.

    Prefers the 'blocking' attribute if present, otherwise falls back to
    'success' or 'passed' for legacy compatibility.
    """
    if hasattr(result, "blocking"):
        return bool(result.blocking)

    if hasattr(result, "success"):
        return not bool(result.success)

    if hasattr(result, "passed"):
        return not bool(result.passed)

    return False
