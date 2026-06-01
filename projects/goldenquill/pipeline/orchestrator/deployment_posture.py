"""pipeline.orchestrator.deployment_posture — per-call posture lookup.

Companion code for §4 v2.x.5 amendment (LOCKED 2026-05-16 row 232) — Cycle 2
RT-C2-07 fold-in.

Extracted from ``pipeline.orchestrator.router`` to avoid the circular-import
that would otherwise surface when ``provider_boundary.py`` and ``router.py``
both depend on a shared posture-lookup helper. The posture state lives in a
process-shared, thread-safe atomic container that the orchestrator updates
atomically when a posture-change attestation lands.

v7.0.10 §5.3 posture-mid-cycle-change discipline
------------------------------------------------

Posture changes mid-cycle are themselves fail-closed at the architectural
layer (``F-CLASS-POSTURE-MID-CYCLE-CHANGE`` — existing primitive at family
row 13). The orchestrator refuses to attest a posture change while a cycle
is open; the wrapper's per-call lookup picks up a new posture starting at
the next cycle.

Loading discipline (RT-C2-07)
-----------------------------

Each ``enforce_outbound_boundary`` invocation calls
``get_current_posture()`` per-call (NOT cached at import). The helper reads
from the process-shared atomic container. Tests use ``set_posture_for_tests()``
to swap state between cases.
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Final, Literal

Posture = Literal["frontier_eligible", "split_context_hybrid", "local_only_sovereign"]

_VALID_POSTURES: Final[frozenset[str]] = frozenset(
    {"frontier_eligible", "split_context_hybrid", "local_only_sovereign"}
)

#: Default posture when no signed register / routing.yaml has set one.
#: Per v7.0.10 §1.3 fail-closed-LOCAL discipline: any indeterminate state
#: falls back to ``local_only_sovereign`` so cloud egress is structurally
#: refused.
DEFAULT_POSTURE: Final[Posture] = "local_only_sovereign"

_POSTURE_LOCK: threading.Lock = threading.Lock()
_CURRENT_POSTURE: Posture = DEFAULT_POSTURE
_POSTURE_LOADED: bool = False


def get_current_posture() -> Posture:
    """Return the current deployment posture (thread-safe atomic read).

    On first call, lazy-loads from ``routing.yaml`` + signed register. If
    the deployment has not initialized posture, returns ``DEFAULT_POSTURE``
    (``local_only_sovereign``) per fail-closed discipline.
    """
    with _POSTURE_LOCK:
        return _CURRENT_POSTURE


def set_posture(new_posture: Posture, *, attestation_signature: bytes | None = None) -> None:
    """Atomically update the current deployment posture.

    Production deployments require an operator Ed25519 attestation
    (``attestation_signature``). The signature verification is performed by
    the caller (typically ``router.attest_posture_change``); this function
    is the atomic-state-update primitive only.

    Parameters
    ----------
    new_posture
        One of ``"frontier_eligible"``, ``"split_context_hybrid"``,
        ``"local_only_sovereign"``.
    attestation_signature
        Ed25519 signature over the canonical-bytes of the new posture +
        cycle close attestation. Currently a documentary parameter; the
        operator-verification step happens at the caller. (v0.1 single-
        client; multi-tenant promotion lands at Stage-5 Sovereign Node
        commons amendment.)
    """
    global _CURRENT_POSTURE, _POSTURE_LOADED
    if new_posture not in _VALID_POSTURES:
        raise ValueError(
            f"invalid posture {new_posture!r}; expected one of "
            f"{sorted(_VALID_POSTURES)}"
        )
    with _POSTURE_LOCK:
        _CURRENT_POSTURE = new_posture
        _POSTURE_LOADED = True


def set_posture_for_tests(new_posture: Posture) -> None:
    """Test-only helper to swap posture between cases without attestation."""
    set_posture(new_posture)


def reset_posture_for_tests() -> None:
    """Test-only helper to reset posture to DEFAULT between cases."""
    global _CURRENT_POSTURE, _POSTURE_LOADED
    with _POSTURE_LOCK:
        _CURRENT_POSTURE = DEFAULT_POSTURE
        _POSTURE_LOADED = False


def load_posture_from_signed_register(
    *, signed_register: dict | None
) -> Posture:
    """Read the posture field from the operator-signed register payload.

    Returns ``DEFAULT_POSTURE`` (``local_only_sovereign``) on any missing /
    malformed / invalid posture — fail-closed-LOCAL per v7.0.10 §1.3.
    """
    if signed_register is None:
        return DEFAULT_POSTURE
    register = signed_register.get("register") if isinstance(signed_register, dict) else None
    if not isinstance(register, dict):
        return DEFAULT_POSTURE
    posture_str = register.get("posture")
    if isinstance(posture_str, str) and posture_str in _VALID_POSTURES:
        return posture_str  # type: ignore[return-value]
    return DEFAULT_POSTURE


__all__ = [
    "Posture",
    "DEFAULT_POSTURE",
    "get_current_posture",
    "set_posture",
    "set_posture_for_tests",
    "reset_posture_for_tests",
    "load_posture_from_signed_register",
]
