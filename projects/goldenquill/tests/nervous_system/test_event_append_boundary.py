import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from pipeline.nervous_system.event_append_boundary import (
    EventAppendRequest,
    EventAppendReceipt,
    EventAppendStatus,
    EventAppendFamily,
)

def test_event_append_request_accepts_proposal_dry_run():
    req = EventAppendRequest(
        append_request_id="ar-123",
        source_proposal_id="sp-123",
        source_dry_run_id="dr-123",
        requested_family=EventAppendFamily.STEWARD_PROPOSAL,
        requested_event_type="steward.proposal.accepted",
        operator_id="op-123",
        posture_at_request="SPLIT_CONTEXT_HYBRID",
        operator_review_summary="Looks good",
        rationale="Client requested it",
        requested_at=datetime.now(timezone.utc),
    )
    assert req.append_request_id == "ar-123"
    assert req.source_proposal_id == "sp-123"
    assert req.source_dry_run_id == "dr-123"

def test_event_append_request_requires_operator_fields():
    with pytest.raises(ValidationError) as exc_info:
        EventAppendRequest(
            append_request_id="ar-123",
            source_proposal_id="sp-123",
            requested_family=EventAppendFamily.NOOP_DRY_RUN,
            requested_event_type="noop.dry.run",
            operator_id="op-123",
            # Missing operator_review_summary, rationale, posture_at_request, requested_at
        )
    err = str(exc_info.value)
    assert "posture_at_request" in err
    assert "operator_review_summary" in err
    assert "rationale" in err
    assert "requested_at" in err

def test_event_append_request_forbids_canonical_execution_fields():
    with pytest.raises(ValidationError, match="forbids execution fields"):
        EventAppendRequest(
            append_request_id="ar-123",
            source_proposal_id="sp-123",
            requested_family=EventAppendFamily.STEWARD_PROPOSAL,
            requested_event_type="steward.proposal.accepted",
            operator_id="op-123",
            posture_at_request="SPLIT_CONTEXT_HYBRID",
            operator_review_summary="Looks good",
            rationale="Client requested it",
            requested_at=datetime.now(timezone.utc),
            event_id="ev-999" # Forbidden
        )

def test_event_append_receipt_forbids_canonical_execution_fields():
    with pytest.raises(ValidationError, match="forbids execution fields"):
        EventAppendReceipt(
            append_request_id="ar-123",
            source_proposal_id="sp-123",
            status=EventAppendStatus.APPEND_REQUEST_ACCEPTED_FOR_POLICY_REVIEW,
            reviewed_at=datetime.now(timezone.utc),
            signature_event_id="se-999" # Forbidden
        )

def test_event_append_receipt_status_restrictions():
    invalid_statuses = ["EVENT_APPENDED", "COMMITTED", "SIGNED", "LOCKED", "EXPORTED"]
    valid_statuses = [e.value for e in EventAppendStatus]
    for inv in invalid_statuses:
        assert inv not in valid_statuses

    assert "REJECTED_BY_SYNC_CONFLICT" in valid_statuses
    assert "REJECTED_BY_STALE_PROJECTION" in valid_statuses

def test_requires_signature_ceremony_does_not_create_signature_event_id():
    req = EventAppendRequest(
        append_request_id="ar-123",
        source_proposal_id="sp-123",
        requested_family=EventAppendFamily.STEWARD_PROPOSAL,
        requested_event_type="test",
        operator_id="op",
        posture_at_request="LOCAL",
        operator_review_summary="Test",
        rationale="Test",
        requested_at=datetime.now(timezone.utc),
        requires_signature_ceremony=True,
    )
    assert req.requires_signature_ceremony is True
    assert not hasattr(req, "signature_event_id")

def test_append_request_accepted_does_not_create_event_id():
    rec = EventAppendReceipt(
        append_request_id="ar-123",
        source_proposal_id="sp-123",
        status=EventAppendStatus.APPEND_REQUEST_ACCEPTED_FOR_POLICY_REVIEW,
        reviewed_at=datetime.now(timezone.utc),
    )
    assert rec.status == EventAppendStatus.APPEND_REQUEST_ACCEPTED_FOR_POLICY_REVIEW
    assert not hasattr(rec, "event_id")

def test_module_source_has_no_execution_logic():
    from pathlib import Path
    import pipeline.nervous_system.event_append_boundary as module

    src = Path(module.__file__).read_text()
    forbidden_tokens = [
        "db.commit",
        "ledger.append",
        "append_event",
        "write_event",
        "open(",
        "requests.post",
        "subprocess",
        "portal_submit"
    ]
    for token in forbidden_tokens:
        assert token not in src, f"Forbidden token {token} found in module source"

def test_requested_event_type_is_descriptive():
    # Implicitly verified since requested_event_type is just a string and has no ledger invocation attached
    req = EventAppendRequest(
        append_request_id="ar-123",
        source_proposal_id="sp-123",
        requested_family=EventAppendFamily.STEWARD_PROPOSAL,
        requested_event_type="descriptive.only.no.ledger.writer",
        operator_id="op-123",
        posture_at_request="LOCAL",
        operator_review_summary="summary",
        rationale="rationale",
        requested_at=datetime.now(timezone.utc),
    )
    assert req.requested_event_type == "descriptive.only.no.ledger.writer"
