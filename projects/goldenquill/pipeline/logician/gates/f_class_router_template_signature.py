"""F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID — PRE router-template-update gate.

Per architecture v7.0.7 §6.1 (SN-LLC router-template integrity).

When the operator opts to take a router-template update from
Sovereign Node LLC, the Golden Quill verifies the Ed25519 signature
against SN-LLC's pinned public key BEFORE applying the new template.
Failure to verify → fail-closed: the update is REJECTED, the
deployment stays on the previous pinned version, an admin-risk ledger
entry with HIGH severity is appended, and the operator is notified.

Per §6.1 #3 the public-key pinning + rotation discipline binds:

  * SN-LLC's signing key fingerprint is pinned at white-glove
    onboarding to the operator's classification register sign-off
    artifact (§3.7).
  * Key rotation requires the new key co-signed by the previous key
    OR explicitly re-pinned at operator discretion (Trust-On-First-Use
    rotation, audited).
  * A signature signed by a non-pinned key fail-closes regardless of
    provenance claims.

Per §6.1 #4 the A12 crypto-agility binding admits:

  * v0.1 — Ed25519 only.
  * v0.2+ — hybrid Ed25519 + ML-DSA-65 verifier requires BOTH legs
    verify, with `legacy_v0_1_migration_tail: true` exception for
    v0.1-era templates pre-dating ML-DSA rollout.

This gate fires PRE router.yaml derivation. If verification fails the
deployment stays on the previous pinned version (caller responsibility);
this gate produces only the fail-closed signal.

Bypass: NO direct M13 — operator may explicitly re-pin a new key via
the documented `tilth router-template rotate-signing-key` flow per
§6.1 operator-visible touchpoints (rotation is the audited unbypass).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional

from pipeline.logician.gates._protocols import SignatureVerifyCallable


F_CLASS_ROUTER_TEMPLATE_SIGNATURE_INVALID: Final[str] = (
    "F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID"
)


@dataclass(frozen=True, kw_only=True)
class RouterTemplateSignatureResult:
    """Result of F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    template_version: Optional[str] = None


def check_class_router_template_signature_invalid(
    *,
    template_version: str,
    template_canonical_bytes: bytes,
    template_signature: bytes,
    pinned_signing_public_key: bytes,
    signature_verify: SignatureVerifyCallable,
) -> RouterTemplateSignatureResult:
    """PRE-update gate: SN-LLC router-template signature must verify.

    Parameters
    ----------
    template_version
        The router-template version identifier (e.g., the release tag).
        Surfaced in detail for audit trail.
    template_canonical_bytes
        Canonical bytes of the router-template the I/O wrapper just
        downloaded. The gate does not parse YAML — the caller
        canonicalizes; the gate verifies bytes.
    template_signature
        Detached Ed25519 signature shipped alongside the template.
        Empty / non-bytes → fail-closed.
    pinned_signing_public_key
        Operator-pinned SN-LLC Ed25519 public key (32 bytes) per §6.1
        white-glove pinning. Mismatched-key signatures fail-close
        regardless of provenance claims.
    signature_verify
        Injected :class:`SignatureVerifyCallable`.

    Returns
    -------
    RouterTemplateSignatureResult. PASS only when ``signature_verify``
    returns True identity-strict against the pinned public key.
    """
    if not isinstance(template_version, str) or not template_version.strip():
        return RouterTemplateSignatureResult(
            success=False,
            failure_code=F_CLASS_ROUTER_TEMPLATE_SIGNATURE_INVALID,
            detail=(
                "template_version empty — refusing to apply unidentified "
                "router-template"
            ),
            template_version=template_version,
        )
    if not isinstance(template_canonical_bytes, (bytes, bytearray)) or not bytes(
        template_canonical_bytes
    ):
        return RouterTemplateSignatureResult(
            success=False,
            failure_code=F_CLASS_ROUTER_TEMPLATE_SIGNATURE_INVALID,
            detail=(
                f"router-template {template_version!r} canonical bytes empty "
                "or non-bytes — refusing to apply"
            ),
            template_version=template_version,
        )
    if not isinstance(template_signature, (bytes, bytearray)) or not bytes(
        template_signature
    ):
        return RouterTemplateSignatureResult(
            success=False,
            failure_code=F_CLASS_ROUTER_TEMPLATE_SIGNATURE_INVALID,
            detail=(
                f"router-template {template_version!r} signature missing or "
                "empty — fail-closed; deployment stays on previous pinned "
                "version"
            ),
            template_version=template_version,
        )
    if not isinstance(pinned_signing_public_key, (bytes, bytearray)) or not bytes(
        pinned_signing_public_key
    ):
        return RouterTemplateSignatureResult(
            success=False,
            failure_code=F_CLASS_ROUTER_TEMPLATE_SIGNATURE_INVALID,
            detail=(
                "pinned SN-LLC public key empty or non-bytes — operator must "
                "re-run white-glove key-pinning before applying any update"
            ),
            template_version=template_version,
        )

    try:
        verified = signature_verify(
            bytes(template_canonical_bytes),
            bytes(template_signature),
            bytes(pinned_signing_public_key),
        )
    except Exception as exc:  # noqa: BLE001 — fail-closed
        return RouterTemplateSignatureResult(
            success=False,
            failure_code=F_CLASS_ROUTER_TEMPLATE_SIGNATURE_INVALID,
            detail=(
                f"signature_verify raised {type(exc).__name__}: {exc} on "
                f"router-template {template_version!r}"
            ),
            template_version=template_version,
        )
    if verified is not True:
        return RouterTemplateSignatureResult(
            success=False,
            failure_code=F_CLASS_ROUTER_TEMPLATE_SIGNATURE_INVALID,
            detail=(
                f"Ed25519 verification of router-template "
                f"{template_version!r} failed under pinned SN-LLC public "
                "key — UPDATE REJECTED; deployment stays on previous pinned "
                "version per §6.1 #2"
            ),
            template_version=template_version,
        )

    return RouterTemplateSignatureResult(
        success=True,
        failure_code=None,
        detail=(
            f"router-template {template_version!r} Ed25519 signature "
            "verified under pinned SN-LLC public key — update may apply"
        ),
        template_version=template_version,
    )


__all__ = [
    "F_CLASS_ROUTER_TEMPLATE_SIGNATURE_INVALID",
    "RouterTemplateSignatureResult",
    "check_class_router_template_signature_invalid",
]
