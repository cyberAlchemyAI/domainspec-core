"""Unit tests for F-CLASS-ROUTING-INDETERMINATE (PRE per-call)."""

from __future__ import annotations

from pipeline.logician.gates.f_class_routing_indeterminate import (
    CLASS_CONFIDENTIAL,
    CLASS_OPERATOR_FLAGGED,
    CLASS_PUBLIC,
    CLASS_SHAREABLE,
    CallInput,
    F_CLASS_ROUTING_INDETERMINATE,
    PERMITTED_CLASSES,
    check_class_routing_indeterminate,
)


def test_failure_code_constant() -> None:
    assert F_CLASS_ROUTING_INDETERMINATE == "F-CLASS-ROUTING-INDETERMINATE"


def test_permitted_classes_membership() -> None:
    assert CLASS_PUBLIC in PERMITTED_CLASSES
    assert CLASS_SHAREABLE in PERMITTED_CLASSES
    assert CLASS_CONFIDENTIAL in PERMITTED_CLASSES
    assert CLASS_OPERATOR_FLAGGED in PERMITTED_CLASSES


def test_all_public_passes() -> None:
    r = check_class_routing_indeterminate(
        inputs=[
            CallInput(field_path="org.name", class_name=CLASS_PUBLIC),
            CallInput(field_path="org.address", class_name=CLASS_PUBLIC),
        ],
    )
    assert r.success is True
    assert r.indeterminate_paths == ()


def test_mix_public_shareable_passes() -> None:
    r = check_class_routing_indeterminate(
        inputs=[
            CallInput(field_path="org.name", class_name=CLASS_PUBLIC),
            CallInput(field_path="org.narrative", class_name=CLASS_SHAREABLE),
        ],
    )
    assert r.success is True


def test_confidential_input_passes_routing_check() -> None:
    # Per §1: any confidential input → route LOCAL. Routing is determinate.
    r = check_class_routing_indeterminate(
        inputs=[
            CallInput(
                field_path="org.revenue", class_name=CLASS_CONFIDENTIAL
            ),
            CallInput(field_path="org.name", class_name=CLASS_PUBLIC),
        ],
    )
    assert r.success is True


def test_unknown_class_fails() -> None:
    r = check_class_routing_indeterminate(
        inputs=[
            CallInput(field_path="org.x", class_name="green"),
        ],
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_ROUTING_INDETERMINATE
    assert r.safe_default_route == "local"


def test_blank_class_fails() -> None:
    r = check_class_routing_indeterminate(
        inputs=[CallInput(field_path="org.x", class_name="")],
    )
    assert r.success is False


def test_pending_review_fails() -> None:
    r = check_class_routing_indeterminate(
        inputs=[
            CallInput(
                field_path="org.new_fact",
                class_name=CLASS_CONFIDENTIAL,
                locked_by="pending_operator_review",
            ),
        ],
    )
    assert r.success is False
    assert "pending_operator_review" in r.detail


def test_empty_inputs_fails() -> None:
    r = check_class_routing_indeterminate(inputs=[])
    assert r.success is False
    assert r.safe_default_route == "local"


def test_multiple_indeterminate_collected() -> None:
    r = check_class_routing_indeterminate(
        inputs=[
            CallInput(field_path="org.a", class_name="??"),
            CallInput(field_path="org.b", class_name=""),
            CallInput(field_path="org.c", class_name=CLASS_PUBLIC),
        ],
    )
    assert r.success is False
    # Two indeterminate; one ok.
    assert len(r.indeterminate_paths) == 2


def test_non_string_class_fails() -> None:
    r = check_class_routing_indeterminate(
        inputs=[CallInput(field_path="org.x", class_name=None)],  # type: ignore[arg-type]
    )
    assert r.success is False


def test_safe_default_route_local_when_indeterminate() -> None:
    r = check_class_routing_indeterminate(
        inputs=[CallInput(field_path="x", class_name="indeterminate")],
    )
    assert r.success is False
    assert r.safe_default_route == "local"
