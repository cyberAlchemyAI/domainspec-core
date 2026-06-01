"""Shared runtime-checkable Protocols for the §4 v2.7 Uploader gate family.

Per the §4 v2.2 ``_protocols.py`` pattern (E-017 injected-callable). The
three Uploader-paired gate wrappers that previously imported predicate
implementations from ``pipeline.orchestrator.seats.uploader`` directly —

  * ``f_uploader_signature_missing``    (PRE-31)
  * ``f_uploader_signature_mismatch``   (PRE-32)
  * ``f_uploader_org_cross_ref``        (PRE-36)

— now consume injected Protocol-typed callables instead. Production wiring
binds the seat-side single-purpose predicates (``_check_signature_presence``,
``_check_signature_hash``, ``f_uploader_org_cross_ref``) at module import
time; tests inject mocks.

Rationale: keeps Logician gate modules free of any ``pipeline.orchestrator``
import edge, mirroring the §4 v2.2 / v2.3 /v2.4 / v2.5 / v2.6 amendment
discipline. AST-lint R1 / R3 already prohibit LLM-client and direct file
I/O at module load; this Protocols seam is the only sanctioned reach into
seat-side predicates.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Signature presence — PRE-31
# ---------------------------------------------------------------------------


@runtime_checkable
class SignaturePresenceCheck(Protocol):
    """Returns True iff the input bundle carries an operator signature.

    The §4 PRE-31 wrapper invokes this and emits
    ``F-UPLOADER-SIGNATURE-MISSING`` when the call returns False. No I/O,
    no hash computation; presence-only.
    """

    def __call__(self, uploader_input: object) -> bool: ...


# ---------------------------------------------------------------------------
# Signature hash — PRE-32
# ---------------------------------------------------------------------------


@runtime_checkable
class SignatureHashCheck(Protocol):
    """Returns True iff the operator signature hash matches the bundle bytes.

    The §4 PRE-32 wrapper invokes this and emits
    ``F-UPLOADER-SIGNATURE-MISMATCH`` when the call returns False *and*
    presence has already been confirmed. Returning False when no signature
    is present is acceptable (PRE-31 owns that surface).
    """

    def __call__(self, uploader_input: object, bundle_bytes: bytes) -> bool: ...


# ---------------------------------------------------------------------------
# Org cross-ref — PRE-36
# ---------------------------------------------------------------------------


@runtime_checkable
class OrgCrossRefCheck(Protocol):
    """Returns True iff the input bundle references a single ``orgs/<slug>/``.

    The §4 PRE-36 wrapper invokes this and emits
    ``F-UPLOADER-ORG-CROSS-REF`` when the call returns False. Sweeps are
    expected to cover the declared ``org_slug``, every attachment path,
    and the submission bundle ref itself.
    """

    def __call__(self, uploader_input: object) -> bool: ...


__all__ = [
    "SignaturePresenceCheck",
    "SignatureHashCheck",
    "OrgCrossRefCheck",
]
