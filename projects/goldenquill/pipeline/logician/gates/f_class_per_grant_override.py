"""F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED — PRE per-grant SP0 gate.

Per architecture v7.0.7 §2 (grant_overrides block schema) + §3.7
(per_grant_sp0_signature chain) + §7 (Card archetype defaults +
operator overrides at white-glove + per-grant SP0 overrides).

When the operator stages per-grant classification overrides for a
specific RFA cycle (e.g., "for THIS small foundation, treat
budget_detail as confidential because the small foundation doesn't
ask for it at this granularity and exposing it weakens posture"), the
per-grant SP0 override block must carry an Ed25519 signature signed by
the operator at SP0 review per §3.7.

Per §4.1 the high-stakes flag for a grant lives in the same
``grant_overrides`` block; setting it requires the same per-grant SP0
signature, which audit-trails the decision.

This gate fires PRE per-grant: at SP0 sign-out, before the cycle reads
any classification override row, the gate verifies signature presence
+ Ed25519 verification of the override block bytes.

Bypass: M13 (audited; HIGH-severity admin-risk — operator must
re-sign the override block).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Mapping, Optional

from pipeline.logician.gates._protocols import SignatureVerifyCallable


F_CLASS_PER_GRANT_OVERRIDE_UNSIGNED: Final[str] = (
    "F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED"
)

PER_GRANT_SP0_SIGNATURE_KEY: Final[str] = "per_grant_sp0_signature"


@dataclass(frozen=True, kw_only=True)
class PerGrantOverrideResult:
    """Result of F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    grant_id: Optional[str] = None


def check_class_per_grant_override_unsigned(
    *,
    grant_id: str,
    grant_override_block: Optional[Mapping[str, object]],
    override_canonical_bytes: bytes,
    signing_public_key: bytes,
    signature_verify: SignatureVerifyCallable,
) -> PerGrantOverrideResult:
    """PRE per-grant: per_grant_sp0_signature must be present + verify.

    Parameters
    ----------
    grant_id
        RFA hash / grant identifier the override block belongs to. Used
        for audit trail in the detail message.
    grant_override_block
        The ``grant_overrides`` dict for this grant_id, OR ``None``
        when no override exists. ``None`` PASSes — overrides are
        optional per §2 schema; the gate only fires when the block
        exists.
    override_canonical_bytes
        Canonical bytes of the override block (the I/O wrapper
        canonicalizes; the gate consumes raw bytes).
    signing_public_key
        Operator-pinned Ed25519 public key (32 bytes) — same key as
        white-glove sign-off per §3.7 chain discipline.
    signature_verify
        Injected :class:`SignatureVerifyCallable`.

    Returns
    -------
    PerGrantOverrideResult. PASS when:
      - override block is None (no override exists for this grant), OR
      - override block contains a non-empty per_grant_sp0_signature AND
        Ed25519 verification succeeds against the signing key.
    """
    if grant_override_block is None:
        return PerGrantOverrideResult(
            success=True,
            failure_code=None,
            detail=(
                f"no per-grant override block for grant_id={grant_id!r} — "
                "default classification register applies"
            ),
            grant_id=grant_id,
        )
    if not isinstance(grant_override_block, Mapping):
        return PerGrantOverrideResult(
            success=False,
            failure_code=F_CLASS_PER_GRANT_OVERRIDE_UNSIGNED,
            detail=(
                f"grant_override_block for grant_id={grant_id!r} is not a "
                f"mapping (got {type(grant_override_block).__name__})"
            ),
            grant_id=grant_id,
        )

    sig = grant_override_block.get(PER_GRANT_SP0_SIGNATURE_KEY)
    if sig is None:
        return PerGrantOverrideResult(
            success=False,
            failure_code=F_CLASS_PER_GRANT_OVERRIDE_UNSIGNED,
            detail=(
                f"grant_override_block for grant_id={grant_id!r} carries no "
                f"{PER_GRANT_SP0_SIGNATURE_KEY!r} — operator must sign "
                "override at SP0 review per §3.7"
            ),
            grant_id=grant_id,
        )
    if not isinstance(sig, (bytes, bytearray)) or not bytes(sig):
        return PerGrantOverrideResult(
            success=False,
            failure_code=F_CLASS_PER_GRANT_OVERRIDE_UNSIGNED,
            detail=(
                f"grant_override_block for grant_id={grant_id!r} has empty / "
                f"non-bytes {PER_GRANT_SP0_SIGNATURE_KEY!r} — Ed25519 "
                "signature bytes required"
            ),
            grant_id=grant_id,
        )

    try:
        verified = signature_verify(
            override_canonical_bytes, bytes(sig), signing_public_key
        )
    except Exception as exc:  # noqa: BLE001 — fail-closed
        return PerGrantOverrideResult(
            success=False,
            failure_code=F_CLASS_PER_GRANT_OVERRIDE_UNSIGNED,
            detail=(
                f"signature_verify raised {type(exc).__name__}: {exc} on "
                f"per-grant override for grant_id={grant_id!r}"
            ),
            grant_id=grant_id,
        )
    if verified is not True:
        return PerGrantOverrideResult(
            success=False,
            failure_code=F_CLASS_PER_GRANT_OVERRIDE_UNSIGNED,
            detail=(
                f"Ed25519 verification of per-grant override failed for "
                f"grant_id={grant_id!r} — signature mismatched canonical "
                "override bytes; M13 audited bypass requires operator re-sign"
            ),
            grant_id=grant_id,
        )

    return PerGrantOverrideResult(
        success=True,
        failure_code=None,
        detail=(
            f"per_grant_sp0_signature verified for grant_id={grant_id!r} — "
            "override block is operator-signed"
        ),
        grant_id=grant_id,
    )


__all__ = [
    "F_CLASS_PER_GRANT_OVERRIDE_UNSIGNED",
    "PER_GRANT_SP0_SIGNATURE_KEY",
    "PerGrantOverrideResult",
    "check_class_per_grant_override_unsigned",
]
