"""Production-default registry for Uploader gate Protocol-DI wrappers.

The §4 v2.7 Uploader gate wrappers in
``pipeline/logician/gates/f_uploader_signature_missing.py``,
``pipeline/logician/gates/f_uploader_signature_mismatch.py``, and
``pipeline/logician/gates/f_uploader_org_cross_ref.py`` accept a
Protocol-typed ``check`` callable as a keyword-only injected dependency
(per the §4 v2.2 ``_protocols.py`` pattern, E-017). Tests inject mocks.

Production wiring binds the seat-side single-purpose predicates from
``pipeline/orchestrator/seats/uploader.py`` here, in a single module that
the §4 wrappers consult via ``get_default_X()``. This keeps the wrappers
themselves free of any direct ``pipeline.orchestrator`` import edge —
they import only this registry plus ``_uploader_protocols``.

The registration step runs at first lookup (lazy import). Re-registering
is permitted (tests can swap defaults during a session and reset on
teardown).
"""

from __future__ import annotations

from typing import Optional

from pipeline.logician.gates._uploader_protocols import (
    OrgCrossRefCheck,
    SignatureHashCheck,
    SignaturePresenceCheck,
)


_signature_presence: Optional[SignaturePresenceCheck] = None
_signature_hash: Optional[SignatureHashCheck] = None
_org_cross_ref: Optional[OrgCrossRefCheck] = None


def register_signature_presence_check(check: SignaturePresenceCheck) -> None:
    global _signature_presence
    _signature_presence = check


def register_signature_hash_check(check: SignatureHashCheck) -> None:
    global _signature_hash
    _signature_hash = check


def register_org_cross_ref_check(check: OrgCrossRefCheck) -> None:
    global _org_cross_ref
    _org_cross_ref = check


def _bind_seat_side_defaults() -> None:
    """Lazy-import the seat-side predicates and register them as defaults.

    Deferred to call time so that importing the §4 wrappers does not pull
    ``pipeline.orchestrator.seats.uploader`` into the import graph at
    module-load time. The first ``get_*`` call after process start
    triggers binding; subsequent calls reuse the cached registration.
    """
    # Local import — avoids the module-load edge that the §4 v2.2
    # _protocols.py pattern is structurally trying to keep out of the
    # gates/ package's static dependency surface.
    from pipeline.orchestrator.seats.uploader import (  # noqa: PLC0415
        _check_signature_hash,
        _check_signature_presence,
        f_uploader_org_cross_ref as _seat_org_cross_ref_predicate,
    )

    def _org_check_adapter(uploader_input: object) -> bool:
        # Adapt the GateResult-returning seat predicate to a bool surface
        # suitable for the Protocol contract.
        return _seat_org_cross_ref_predicate(uploader_input).passed  # type: ignore[arg-type]

    register_signature_presence_check(_check_signature_presence)  # type: ignore[arg-type]
    register_signature_hash_check(_check_signature_hash)  # type: ignore[arg-type]
    register_org_cross_ref_check(_org_check_adapter)


def get_default_signature_presence_check() -> SignaturePresenceCheck:
    if _signature_presence is None:
        _bind_seat_side_defaults()
    assert _signature_presence is not None
    return _signature_presence


def get_default_signature_hash_check() -> SignatureHashCheck:
    if _signature_hash is None:
        _bind_seat_side_defaults()
    assert _signature_hash is not None
    return _signature_hash


def get_default_org_cross_ref_check() -> OrgCrossRefCheck:
    if _org_cross_ref is None:
        _bind_seat_side_defaults()
    assert _org_cross_ref is not None
    return _org_cross_ref


__all__ = [
    "register_signature_presence_check",
    "register_signature_hash_check",
    "register_org_cross_ref_check",
    "get_default_signature_presence_check",
    "get_default_signature_hash_check",
    "get_default_org_cross_ref_check",
]
