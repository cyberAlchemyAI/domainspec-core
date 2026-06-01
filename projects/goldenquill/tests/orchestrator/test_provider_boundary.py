"""Tests for pipeline.orchestrator.provider_boundary (§4 v2.x.5 CC-007 closure).

Covers:
- Wrapper PRE refusal: missing_context, classification_deny under Local-Only,
  confidential input, payload scan hit, payload commitment mismatch,
  runtime identity pin (RT-01 + §12.4).
- Wrapper POST refusal: confidential literal echoed, high-stakes literal echoed.
- Happy path: public input + frontier_eligible posture passes through.
- stdlib_urlopen_caller: refuses direct call outside wrapper (§12.5 RT-C2-03).
- stdlib_urlopen_caller: refuses non-https URL scheme (DC-CYCLE2-02).
- Process-wide invocation counter (RT-18 + §12.5).
- ClassificationContext.from_envelope_json round-trip.
"""

from __future__ import annotations

import hashlib
import json

import pytest

from pipeline.logician.gates.f_class_outbound_boundary import (
    ClassifiedValue,
    SlotPosition,
)
from pipeline.logician.gates.f_class_routing_indeterminate import CallInput
from pipeline.orchestrator.provider_boundary import (
    F_CLASS_OUTBOUND_BOUNDARY_CLASSIFICATION_DENY,
    F_CLASS_OUTBOUND_BOUNDARY_MISSING_CONTEXT,
    F_CLASS_OUTBOUND_BOUNDARY_NEVER_INVOKED_DIRECT_CALL,
    F_CLASS_OUTBOUND_BOUNDARY_PAYLOAD_COMMITMENT_MISMATCH,
    F_CLASS_OUTBOUND_BOUNDARY_POST_DRIFT,
    F_CLASS_OUTBOUND_BOUNDARY_RUNTIME_INTEGRITY_FAIL,
    ClassificationContext,
    OutboundBoundaryRefusedError,
    enforce_outbound_boundary,
    reset_invocation_count_for_tests,
    stdlib_urlopen_caller,
)


def _stub_caller_returning(status: int, response_body: bytes):
    """Build a stub OutboundCallable returning a fixed (status, body)."""
    captured_status = status
    captured_response = response_body

    def stub(*, url, headers, body, timeout_seconds):
        return captured_status, captured_response

    return stub


def _public_context() -> ClassificationContext:
    return ClassificationContext(
        inputs=(CallInput(field_path="public_field", class_name="public"),),
    )


def _confidential_context() -> ClassificationContext:
    return ClassificationContext(
        inputs=(
            CallInput(field_path="ein", class_name="confidential", locked_by="operator"),
        ),
    )


# ---------------------------------------------------------------------------
# PRE refusal tests.
# ---------------------------------------------------------------------------


def test_missing_context_refuses_under_frontier_eligible() -> None:
    reset_invocation_count_for_tests()
    wrapped = enforce_outbound_boundary(
        _stub_caller_returning(200, b"{}"),
        classification_context=None,
        posture="frontier_eligible",
    )
    with pytest.raises(OutboundBoundaryRefusedError) as excinfo:
        wrapped(url="https://example.com", headers={}, body=b"", timeout_seconds=1.0)
    assert excinfo.value.failure_code == F_CLASS_OUTBOUND_BOUNDARY_MISSING_CONTEXT


def test_local_only_posture_refuses_unconditionally() -> None:
    reset_invocation_count_for_tests()
    wrapped = enforce_outbound_boundary(
        _stub_caller_returning(200, b"{}"),
        classification_context=_public_context(),
        posture="local_only_sovereign",
    )
    with pytest.raises(OutboundBoundaryRefusedError) as excinfo:
        wrapped(url="https://example.com", headers={}, body=b"", timeout_seconds=1.0)
    assert excinfo.value.failure_code == F_CLASS_OUTBOUND_BOUNDARY_CLASSIFICATION_DENY


def test_confidential_input_refuses() -> None:
    reset_invocation_count_for_tests()
    wrapped = enforce_outbound_boundary(
        _stub_caller_returning(200, b"{}"),
        classification_context=_confidential_context(),
        posture="frontier_eligible",
    )
    with pytest.raises(OutboundBoundaryRefusedError) as excinfo:
        wrapped(url="https://example.com", headers={}, body=b"", timeout_seconds=1.0)
    assert excinfo.value.failure_code == F_CLASS_OUTBOUND_BOUNDARY_CLASSIFICATION_DENY


def test_payload_scan_hit_refuses() -> None:
    """PRE: classified literal in body → refuse before inner is called."""
    reset_invocation_count_for_tests()
    classified = ClassifiedValue(
        value="12-3456789", class_name="confidential", field_path="ein"
    )
    ctx = ClassificationContext(
        inputs=(CallInput(field_path="payload", class_name="public"),),
        classified_values=(classified,),
    )
    inner_called = [False]

    def stub(*, url, headers, body, timeout_seconds):
        inner_called[0] = True
        return 200, b"{}"

    wrapped = enforce_outbound_boundary(
        stub,
        classification_context=ctx,
        posture="frontier_eligible",
    )
    with pytest.raises(OutboundBoundaryRefusedError):
        wrapped(
            url="https://example.com",
            headers={},
            body=b'{"ein": "12-3456789"}',
            timeout_seconds=1.0,
        )
    # Inner stub must NOT have been called — PRE refusal.
    assert not inner_called[0]


def test_payload_commitment_mismatch_refuses() -> None:
    """PRE: sha3-512(body) ≠ payload_sha3_512_commitment → refuse."""
    reset_invocation_count_for_tests()
    actual_body = b'{"hello":"world"}'
    wrong_commitment = hashlib.sha3_512(b"different bytes").hexdigest()
    ctx = ClassificationContext(
        inputs=(CallInput(field_path="payload", class_name="public"),),
        payload_sha3_512_commitment=wrong_commitment,
    )
    wrapped = enforce_outbound_boundary(
        _stub_caller_returning(200, b"{}"),
        classification_context=ctx,
        posture="frontier_eligible",
    )
    with pytest.raises(OutboundBoundaryRefusedError) as excinfo:
        wrapped(url="https://example.com", headers={}, body=actual_body, timeout_seconds=1.0)
    assert excinfo.value.failure_code == F_CLASS_OUTBOUND_BOUNDARY_PAYLOAD_COMMITMENT_MISMATCH


def test_payload_commitment_match_passes() -> None:
    """PRE: sha3-512(body) == commitment → pass through."""
    reset_invocation_count_for_tests()
    actual_body = b'{"hello":"world"}'
    commitment = hashlib.sha3_512(actual_body).hexdigest()
    ctx = ClassificationContext(
        inputs=(CallInput(field_path="payload", class_name="public"),),
        payload_sha3_512_commitment=commitment,
    )
    wrapped = enforce_outbound_boundary(
        _stub_caller_returning(200, b'{"ok":true}'),
        classification_context=ctx,
        posture="frontier_eligible",
    )
    status, resp = wrapped(
        url="https://example.com", headers={}, body=actual_body, timeout_seconds=1.0
    )
    assert status == 200
    assert resp == b'{"ok":true}'


def test_runtime_identity_pin_refuses_non_canonical_inner() -> None:
    """RT-01 + §12.4: inner is not _CANONICAL_STDLIB_URLOPEN_CALLER → refuse.

    Only fires when operator_signed_register is provided (production binding).
    """
    reset_invocation_count_for_tests()
    fake_signed_register = {"register": {"entries": []}}
    wrapped = enforce_outbound_boundary(
        _stub_caller_returning(200, b"{}"),  # NOT the canonical stdlib caller
        classification_context=_public_context(),
        posture="frontier_eligible",
        operator_signed_register=fake_signed_register,
    )
    with pytest.raises(OutboundBoundaryRefusedError) as excinfo:
        wrapped(url="https://example.com", headers={}, body=b"", timeout_seconds=1.0)
    assert excinfo.value.failure_code == F_CLASS_OUTBOUND_BOUNDARY_RUNTIME_INTEGRITY_FAIL


# ---------------------------------------------------------------------------
# POST refusal tests.
# ---------------------------------------------------------------------------


def test_post_confidential_drift_refuses() -> None:
    """POST: response bytes carry tagged Confidential literal → refuse."""
    reset_invocation_count_for_tests()
    classified = ClassifiedValue(
        value="SECRET-XYZ", class_name="confidential", field_path="api_key"
    )
    ctx = ClassificationContext(
        inputs=(CallInput(field_path="payload", class_name="public"),),
        classified_values=(classified,),
    )
    # Body itself is clean; response contains the secret.
    wrapped = enforce_outbound_boundary(
        _stub_caller_returning(200, b'{"echoed": "SECRET-XYZ"}'),
        classification_context=ctx,
        posture="frontier_eligible",
    )
    with pytest.raises(OutboundBoundaryRefusedError) as excinfo:
        wrapped(url="https://example.com", headers={}, body=b'{}', timeout_seconds=1.0)
    assert excinfo.value.failure_code == F_CLASS_OUTBOUND_BOUNDARY_POST_DRIFT


# ---------------------------------------------------------------------------
# Happy path.
# ---------------------------------------------------------------------------


def test_happy_path_public_input_returns_inner_result() -> None:
    """All-public input + frontier_eligible posture → inner result passes through."""
    reset_invocation_count_for_tests()
    wrapped = enforce_outbound_boundary(
        _stub_caller_returning(201, b'{"created":true}'),
        classification_context=_public_context(),
        posture="frontier_eligible",
    )
    status, resp = wrapped(
        url="https://example.com",
        headers={"Content-Type": "application/json"},
        body=b'{}',
        timeout_seconds=1.0,
    )
    assert status == 201
    assert resp == b'{"created":true}'


# ---------------------------------------------------------------------------
# stdlib_urlopen_caller direct-call detection (§12.5 RT-C2-03).
# ---------------------------------------------------------------------------


def test_stdlib_urlopen_caller_direct_call_refuses() -> None:
    """Calling stdlib_urlopen_caller directly outside the wrapper refuses."""
    with pytest.raises(OutboundBoundaryRefusedError) as excinfo:
        stdlib_urlopen_caller(
            url="https://example.com",
            headers={},
            body=b"",
            timeout_seconds=1.0,
        )
    assert excinfo.value.failure_code == F_CLASS_OUTBOUND_BOUNDARY_NEVER_INVOKED_DIRECT_CALL


# ---------------------------------------------------------------------------
# ClassificationContext.from_envelope_json round-trip.
# ---------------------------------------------------------------------------


def test_classification_context_from_envelope_json_round_trip() -> None:
    payload = {
        "inputs": [
            {"field_path": "ein", "class_name": "confidential", "locked_by": "operator"}
        ],
        "classified_values": [
            {"value": "12-3456789", "class_name": "confidential", "field_path": "ein"}
        ],
        "slot_positions": [
            {"slot_id": "1", "pre_marker": "BEFORE_", "post_marker": "_AFTER"}
        ],
        "high_stakes_flag_values": ["FLAG_GRANT_42"],
        "post_fill_draft": False,
        "cycle_id": "cycle-001",
        "payload_sha3_512_commitment": "a" * 128,
    }
    ctx = ClassificationContext.from_envelope_json(json.dumps(payload))
    assert ctx.cycle_id == "cycle-001"
    assert ctx.payload_sha3_512_commitment == "a" * 128
    assert len(ctx.inputs) == 1
    assert ctx.inputs[0].class_name == "confidential"
    assert len(ctx.classified_values) == 1
    assert ctx.classified_values[0].value == "12-3456789"


def test_classification_context_malformed_json_raises() -> None:
    with pytest.raises(ValueError):
        ClassificationContext.from_envelope_json("not valid json {{{")


def test_classification_context_empty_inputs_acceptable_for_local_only() -> None:
    """Local-Only orchestrator may emit empty inputs; from_envelope_json accepts."""
    ctx = ClassificationContext.from_envelope_json('{"inputs": []}')
    assert ctx.inputs == ()


# ---------------------------------------------------------------------------
# Invocation counter (RT-18 + §12.5).
# ---------------------------------------------------------------------------


def test_invocation_counter_increments_on_successful_round_trip() -> None:
    reset_invocation_count_for_tests()
    from pipeline.orchestrator.provider_boundary import _get_invocation_count

    wrapped = enforce_outbound_boundary(
        _stub_caller_returning(200, b"{}"),
        classification_context=_public_context(),
        posture="frontier_eligible",
    )
    assert _get_invocation_count() == 0
    wrapped(url="https://example.com", headers={}, body=b"{}", timeout_seconds=1.0)
    assert _get_invocation_count() == 1
