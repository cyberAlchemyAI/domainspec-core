"""Router-level enforcement for v7.0.7 classification routing.

These tests close the raw-router bypass: a cloud provider may not be reached
unless ``call_seat`` receives a per-call classification proof. Updated for
§4 v2.x.6 OD-5 router dedup (LOCKED 2026-05-16T16:30:00Z row 234) — the
F-CLASS PRE/POST chain now fires inside the wrapper composed at dispatch.
The translation layer at ``_dispatch_with_classification_boundary`` preserves
the public ``ClassificationBoundaryError`` exception contract.
"""

from __future__ import annotations

import inspect
import json
from typing import Any, Mapping

import pytest

from pipeline.logician.gates.f_class_outbound_boundary import (
    F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL,
    F_CLASS_CLOUD_RECEIVED_OPAQUE_SLOT_FILLED,
    F_CLASS_SLOT_ID_NON_OPAQUE,
    SlotPosition,
)
from pipeline.logician.gates.f_class_routing_indeterminate import (
    CLASS_CONFIDENTIAL,
    CLASS_PUBLIC,
    CallInput,
    F_CLASS_ROUTING_INDETERMINATE,
)
from pipeline.orchestrator import provider_boundary, router


def _public_context() -> router.ClassificationContext:
    return router.ClassificationContext(
        inputs=(CallInput(field_path="prompt", class_name=CLASS_PUBLIC),)
    )


def _ok_dispatch(calls: list[str]):
    """Bypass-style mock _dispatch: ignores http_post; returns canned ok dict.

    Used by tests that exercise router-layer pre-checks (CC absent / post-fill /
    local path / fallback) — the wrapper never fires because _dispatch never
    invokes http_post.
    """
    def _dispatch(
        provider_cfg: dict, seat_cfg: dict, messages: list, system: str | None,
        *, http_post=None,
    ) -> dict:
        calls.append(str(seat_cfg["provider"]))
        return {
            "content": "ok [SLOT_001]",
            "model": seat_cfg["model"],
            "family": seat_cfg["family"],
            "usage": None,
            "raw": {},
        }

    return _dispatch


# ---------------------------------------------------------------------------
# Fixtures for tests that exercise the wrapper end-to-end.
# ---------------------------------------------------------------------------


@pytest.fixture
def frontier_posture(monkeypatch):
    """Override _load_router_posture_and_register to return frontier_eligible / no register.

    With operator_signed_register=None the wrapper's identity-pin (RT-01) and
    raw-bytes register scan (RT-04) are skipped, but PRE-3.x classification
    gates on inputs + body content still fire. Canonical setup for exercising
    the wrapper PRE/POST chain without a real signed YAML fixture.
    """
    monkeypatch.setattr(
        router,
        "_load_router_posture_and_register",
        lambda: ("frontier_eligible", None),
    )


@pytest.fixture
def stub_api_key(monkeypatch):
    """Stub router.load_api_key so cloud-style call helpers don't hit the keyring."""
    monkeypatch.setattr(router, "load_api_key", lambda env_name: "stub-key" if env_name else None)


@pytest.fixture
def stub_canonical_caller(monkeypatch):
    """Replace the wrapper's inner canonical urlopen caller with a controllable stub.

    Returns a list onto which each (url, body_bytes) tuple is appended; tests
    can also override the response_bytes via ``stub_canonical_caller_with(...)``.
    """
    invocations: list[dict[str, Any]] = []
    state = {
        "response_bytes": (
            b'{"choices":[{"message":{"content":"ok [SLOT_001]"}}],'
            b'"content":[{"type":"text","text":"ok [SLOT_001]"}]}'
        ),
        "status": 200,
    }

    def stub(*, url: str, headers: Mapping[str, str], body: bytes, timeout_seconds: float):
        invocations.append({"url": url, "headers": dict(headers), "body": body})
        return state["status"], state["response_bytes"]

    monkeypatch.setattr(provider_boundary, "_CANONICAL_STDLIB_URLOPEN_CALLER", stub)
    # Expose state so tests can mutate response bytes.
    return type(
        "Stub",
        (),
        {"invocations": invocations, "state": state},
    )()


# ===========================================================================
# Router-layer pre-check tests (wrapper not invoked).
# ===========================================================================


def test_cloud_seat_without_classification_context_fails_before_dispatch(monkeypatch) -> None:
    """Cloud seat with no classification_context → router-layer fail-closed."""
    calls: list[str] = []
    monkeypatch.setattr(router, "_dispatch", _ok_dispatch(calls))

    with pytest.raises(router.ClassificationBoundaryError) as exc:
        router.call_seat(
            "editor",
            [{"role": "user", "content": "public prompt"}],
            system="system",
        )

    assert exc.value.failure_code == F_CLASS_ROUTING_INDETERMINATE
    assert calls == []


def test_cloud_seat_with_public_context_dispatches(monkeypatch) -> None:
    """Cloud seat with public classification → wrapper allows → mock returns ok."""
    calls: list[str] = []
    monkeypatch.setattr(router, "_dispatch", _ok_dispatch(calls))

    response = router.call_seat(
        "editor",
        [{"role": "user", "content": "public prompt"}],
        system="system",
        classification_context=_public_context(),
    )

    assert response["content"] == "ok [SLOT_001]"
    assert calls == ["groq"]


def test_post_fill_draft_cannot_route_to_cloud(monkeypatch) -> None:
    """post_fill_draft=True → router-layer fail-closed (v7.0.7 sovereignty rule).

    Implementation note: the wrapper PRE chain does not currently inspect
    post_fill_draft (provider_boundary.py is LOCKed at §4 v2.x.5). The router
    layer preserves this check until a future amendment lifts it into the
    wrapper.
    """
    calls: list[str] = []
    monkeypatch.setattr(router, "_dispatch", _ok_dispatch(calls))

    with pytest.raises(router.ClassificationBoundaryError) as exc:
        router.call_seat(
            "judge",
            [{"role": "user", "content": "post-fill draft"}],
            classification_context=router.ClassificationContext(
                inputs=(CallInput(field_path="draft", class_name=CLASS_PUBLIC),),
                post_fill_draft=True,
            ),
        )

    assert exc.value.failure_code == F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL
    assert "post-fill" in exc.value.detail
    assert calls == []


def test_local_provider_can_dispatch_without_classification_context(monkeypatch) -> None:
    """Local providers (ollama) take the no-wrapper shim path."""
    calls: list[str] = []
    monkeypatch.setattr(router, "_dispatch", _ok_dispatch(calls))

    response = router.call_seat(
        "scout",
        [{"role": "user", "content": "local prompt"}],
    )

    assert response["content"] == "ok [SLOT_001]"
    assert calls == ["ollama"]


def test_local_primary_failure_cannot_fall_back_to_cloud_without_context(monkeypatch) -> None:
    """Local primary fails → fallback to cloud must still have a classification_context."""
    calls: list[str] = []

    def _dispatch(
        provider_cfg: dict, seat_cfg: dict, messages: list, system: str | None,
        *, http_post=None,
    ) -> dict:
        calls.append(str(seat_cfg["provider"]))
        if seat_cfg["provider"] == "ollama":
            raise OSError("ollama unavailable")
        return {
            "content": "cloud fallback should not run",
            "model": seat_cfg["model"],
            "family": seat_cfg["family"],
            "usage": None,
            "raw": {},
        }

    monkeypatch.setattr(router, "_dispatch", _dispatch)

    with pytest.raises(router.ClassificationBoundaryError) as exc:
        router.call_seat(
            "scout",
            [{"role": "user", "content": "local prompt"}],
        )

    assert exc.value.failure_code == F_CLASS_ROUTING_INDETERMINATE
    assert calls == ["ollama"]


# ===========================================================================
# Wrapper-invocation tests (real dispatch + stubbed canonical caller).
# ===========================================================================


def test_cloud_seat_with_confidential_input_fails_via_wrapper(
    frontier_posture, stub_api_key, stub_canonical_caller,
) -> None:
    """Wrapper PRE-3.2 — blocking-class input refuses cloud egress.

    Translation layer at _dispatch_with_classification_boundary preserves
    the ClassificationBoundaryError contract; failure_code carries the
    sub-tag string ``F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL.outbound_boundary_classification_deny``.
    """
    with pytest.raises(router.ClassificationBoundaryError) as exc:
        router.call_seat(
            "editor",
            [{"role": "user", "content": "prompt with slot"}],
            classification_context=router.ClassificationContext(
                inputs=(
                    CallInput(
                        field_path="org.annual_revenue",
                        class_name=CLASS_CONFIDENTIAL,
                    ),
                )
            ),
        )

    assert exc.value.failure_code.startswith("F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL")
    assert "annual_revenue" in exc.value.detail
    # Wrapper refused before invoking the inner stdlib caller.
    assert stub_canonical_caller.invocations == []


def test_cloud_seat_with_semantic_slot_name_fails_via_wrapper(
    frontier_posture, stub_api_key, stub_canonical_caller,
) -> None:
    """Wrapper PRE-3.3 — semantic slot name in body refuses cloud egress."""
    with pytest.raises(router.ClassificationBoundaryError) as exc:
        router.call_seat(
            "editor",
            [{"role": "user", "content": "Revenue: [SLOT_ANNUAL_REVENUE]"}],
            classification_context=_public_context(),
        )

    assert exc.value.failure_code.startswith("F-CLASS-SLOT-ID-NON-OPAQUE")
    assert stub_canonical_caller.invocations == []


def test_cloud_response_must_preserve_registered_opaque_slots(
    frontier_posture, stub_api_key, stub_canonical_caller,
) -> None:
    """Wrapper POST — opaque-slot pattern leaked in response refuses egress."""
    # Override the response bytes to include the leaked literal content.
    stub_canonical_caller.state["response_bytes"] = (
        b'{"choices":[{"message":{"content":"Annual revenue: $1,234,567."}}],'
        b'"content":[{"type":"text","text":"Annual revenue: $1,234,567."}]}'
    )

    with pytest.raises(router.ClassificationBoundaryError) as exc:
        router.call_seat(
            "editor",
            [{"role": "user", "content": "Annual revenue: [SLOT_001]."}],
            classification_context=router.ClassificationContext(
                inputs=(CallInput(field_path="prompt", class_name=CLASS_PUBLIC),),
                slot_positions=(SlotPosition(slot_id="001"),),
            ),
        )

    assert exc.value.failure_code.startswith("F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED")
    # Inner stub was called — PRE passed; POST raised on response drift.
    assert len(stub_canonical_caller.invocations) == 1


# ===========================================================================
# §8 — five new tests for the OD-5 refactor.
# ===========================================================================


def test_dispatch_via_wrapper_invokes_enforce_outbound_boundary(
    frontier_posture, stub_api_key, stub_canonical_caller,
) -> None:
    """Cloud dispatch constructs the wrapper exactly once per call."""
    construction_count = {"n": 0}
    real_factory = provider_boundary.enforce_outbound_boundary

    def counting_factory(*args, **kwargs):
        construction_count["n"] += 1
        return real_factory(*args, **kwargs)

    # Patch the factory on the router's import path (the module reference is
    # what router uses at construction time).
    import pipeline.orchestrator.router as router_module
    original_factory = router_module.enforce_outbound_boundary
    router_module.enforce_outbound_boundary = counting_factory
    try:
        response = router.call_seat(
            "editor",
            [{"role": "user", "content": "public prompt"}],
            classification_context=_public_context(),
        )
    finally:
        router_module.enforce_outbound_boundary = original_factory

    assert construction_count["n"] == 1
    assert len(stub_canonical_caller.invocations) == 1
    assert response["content"] == "ok [SLOT_001]"


def test_outbound_boundary_refused_translates_to_classification_boundary_error(
    frontier_posture, stub_api_key, stub_canonical_caller,
) -> None:
    """OutboundBoundaryRefusedError → ClassificationBoundaryError translation.

    Per §4 v2.x.6 §4 the router catches OutboundBoundaryRefusedError raised by
    the wrapper and re-raises as ClassificationBoundaryError with the same
    failure_code + detail (`__cause__` chain preserved).
    """
    with pytest.raises(router.ClassificationBoundaryError) as exc:
        router.call_seat(
            "editor",
            [{"role": "user", "content": "prompt with [SLOT_SEMANTIC_NAME] leak"}],
            classification_context=_public_context(),
        )

    # The original OutboundBoundaryRefusedError is preserved in the cause chain.
    assert isinstance(exc.value.__cause__, provider_boundary.OutboundBoundaryRefusedError)
    # failure_code + detail are passed through unchanged.
    assert exc.value.failure_code == exc.value.__cause__.failure_code
    assert exc.value.detail == exc.value.__cause__.detail


def test_posture_mid_cycle_change_fails_closed(monkeypatch, stub_api_key) -> None:
    """Envelope-posture mismatch with register-posture surfaces as ClassificationBoundaryError.

    The wrapper compares the supplied ``posture`` against the
    ``register_posture`` extracted from the operator-signed register. A
    mismatch raises ``F-CLASS-POSTURE-MID-CYCLE-CHANGE`` (sub-tag
    .outbound_boundary_posture_mismatch). The translation layer surfaces it.
    """
    # Forge a signed-register-bearing load helper: register posture =
    # split_context_hybrid while envelope posture = frontier_eligible.
    fake_register = {
        "register": {
            "posture": "split_context_hybrid",
            "org_slug": "fixture",
            "entries": [],
        },
        "signature": {"algorithm": "ed25519", "public_key_b64": "x", "signature_b64": "y"},
    }
    monkeypatch.setattr(
        router,
        "_load_router_posture_and_register",
        lambda: ("frontier_eligible", fake_register),
    )

    with pytest.raises(router.ClassificationBoundaryError) as exc:
        router.call_seat(
            "editor",
            [{"role": "user", "content": "public prompt"}],
            classification_context=_public_context(),
        )

    assert exc.value.failure_code.startswith("F-CLASS-POSTURE-MID-CYCLE-CHANGE")


def test_signed_register_absent_in_local_only_posture(monkeypatch) -> None:
    """Under local_only_sovereign the register is unused; absence is acceptable.

    The wrapper PRE-1 refuses cloud egress unconditionally under
    local_only_sovereign, so the register would not be consulted. The router
    short-circuits the loader call to avoid spurious failures in test/dev
    environments that have not seeded a signed register.
    """
    from pipeline.orchestrator import deployment_posture

    monkeypatch.setattr(deployment_posture, "get_current_posture", lambda: "local_only_sovereign")
    # Loader would raise (no file on disk); the helper must NOT call it under Local-Only.
    def _explode():
        raise AssertionError("load_signed_register should not be called under local_only_sovereign")
    monkeypatch.setattr(
        "pipeline.vault.classification.signed_register_loader.load_signed_register",
        _explode,
    )

    posture, register = router._load_router_posture_and_register()
    assert posture == "local_only_sovereign"
    assert register is None


def test_local_provider_bypasses_wrapper(monkeypatch) -> None:
    """Local providers do NOT construct or invoke the wrapper.

    The router's local-fast-path short-circuits before any wrapper
    construction. Asserted by patching enforce_outbound_boundary and
    confirming zero invocations.
    """
    import pipeline.orchestrator.router as router_module

    construction_count = {"n": 0}
    original_factory = router_module.enforce_outbound_boundary

    def counting_factory(*args, **kwargs):
        construction_count["n"] += 1
        return original_factory(*args, **kwargs)

    router_module.enforce_outbound_boundary = counting_factory

    calls: list[str] = []
    monkeypatch.setattr(router, "_dispatch", _ok_dispatch(calls))
    try:
        response = router.call_seat(
            "scout",
            [{"role": "user", "content": "local prompt"}],
        )
    finally:
        router_module.enforce_outbound_boundary = original_factory

    assert construction_count["n"] == 0
    assert calls == ["ollama"]
    assert response["content"] == "ok [SLOT_001]"
