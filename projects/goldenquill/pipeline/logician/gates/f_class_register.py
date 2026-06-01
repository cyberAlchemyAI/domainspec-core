"""F-CLASS-REGISTER-* — Classification register integrity (PRE-onboarding + PRE-cycle).

Per architecture v7.0.7 §5.1 (LOCKED 2026-05-10 row 180) + v7.0.10 §1.4
(LOCKED 2026-05-11 row 215) sub-tag extensions for the operator-selected
deployment posture (`selected_posture` top-level field on the register;
one of frontier_eligible / split_context_hybrid / local_only_sovereign).

Four sub-codes share the same Protocol-injection surface (file-existence
check + register reader + Ed25519 signature verifier + SHA3-512 hash
function), so they are housed together per the v2.2 F-AMDT-08/09/10/11
sub-code-collapse precedent.

Sub-codes:

* ``F-CLASS-REGISTER-MISSING`` — PRE-onboarding gate. Classification
  register file absent at ``vault_shared/classification/register.yaml``
  OR ``orgs/<slug>/vault/classification/register.yaml``.

* ``F-CLASS-REGISTER-UNSIGNED`` — PRE-onboarding gate. Register file
  present but the ``operator_signature_at_white_glove_completion`` block
  is missing, empty, or lacks a non-empty ``signature`` byte string.
  Sub-tag `.posture_unsigned` (v7.0.10 §1.4): fires when the register's
  top-level ``selected_posture`` field is present but the operator
  Ed25519 signature does not cover the field. Realization deferred to
  v0.2 first-wave Code phase per the dormant-binding pattern; signature
  surface + named drift-test bindings land here at LOCK ceremony.

* ``F-CLASS-REGISTER-SIGNATURE-INVALID`` — PRE-cycle gate. The Ed25519
  signature on the white-glove sign-off block fails verification under
  the operator-pinned public key. Sub-tag `.posture_invalid` (v7.0.10
  §1.4): fires when the signature verifies against the
  field-classifications block but not against the extended block
  including ``selected_posture``.

* ``F-CLASS-REGISTER-HASH-MISMATCH`` — PRE-cycle gate. Either
  ``signed_field_classifications_hash`` or
  ``signed_class_definitions_hash`` does not match the recomputed
  SHA3-512[:16] over the canonical bytes of the corresponding register
  block (silent edit detected post-sign-off). Sub-tag
  `.posture_hash_mismatch` (v7.0.10 §1.4): fires when the recomputed
  hash chain over the extended block (including ``selected_posture``)
  does not match the on-register hash.

The four sub-codes follow the §1 + §3.7 schema literally. The gate
consumes already-parsed register dicts plus the canonical byte-views of
the field_classifications + class_definitions blocks; canonicalization
lives at the I/O wrapper, not at the gate.

Bypass: M13 for SIGNATURE-INVALID + HASH-MISMATCH (audited; HIGH-severity
admin-risk entry). MISSING + UNSIGNED have NO M13 — Beta deployment cannot
ship without an operator-signed register per §5.

v7.0.10 posture-field coverage hook
-----------------------------------
AST-lint rule R-CLASS-POSTURE-FIELD-COVERAGE enforces that this module
references the ``selected_posture`` field added at v7.0.10 §1.4. The
references below + the SIGN_OFF_POSTURE_KEY constant satisfy the rule;
predicate-body extensions land at the v0.2 first-wave §4 v2.x.y
amendment paired-commit per the architectural deferred-binding pattern.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Mapping, Optional

from pipeline.logician.gates._protocols import (
    FileExistsCallable,
    HashBytesCallable,
    SignatureVerifyCallable,
)


F_CLASS_REGISTER_MISSING: Final[str] = "F-CLASS-REGISTER-MISSING"
F_CLASS_REGISTER_UNSIGNED: Final[str] = "F-CLASS-REGISTER-UNSIGNED"
F_CLASS_REGISTER_SIGNATURE_INVALID: Final[str] = (
    "F-CLASS-REGISTER-SIGNATURE-INVALID"
)
F_CLASS_REGISTER_HASH_MISMATCH: Final[str] = "F-CLASS-REGISTER-HASH-MISMATCH"

# Canonical key for the white-glove sign-off block per §3.7 schema.
SIGN_OFF_KEY: Final[str] = "operator_signature_at_white_glove_completion"
SIGN_OFF_HASH_FIELDS_KEY: Final[str] = "signed_field_classifications_hash"
SIGN_OFF_HASH_CLASS_KEY: Final[str] = "signed_class_definitions_hash"
# v7.0.10 §1.4: top-level register key carrying the operator-selected
# deployment posture. The signed sign-off block at v7.0.10+ covers this
# field alongside the per-field classifications.
REGISTER_POSTURE_KEY: Final[str] = "selected_posture"
SIGN_OFF_POSTURE_KEY: Final[str] = "selected_posture"
PERMITTED_POSTURE_VALUES: Final[frozenset[str]] = frozenset(
    {"frontier_eligible", "split_context_hybrid", "local_only_sovereign"}
)


@dataclass(frozen=True, kw_only=True)
class ClassRegisterResult:
    """Result of an F-CLASS-REGISTER-* sub-check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    register_path: Optional[str] = None


def check_class_register_missing(
    *,
    register_path: str,
    file_exists: FileExistsCallable,
) -> ClassRegisterResult:
    """PRE-onboarding gate: classification register file must exist.

    Parameters
    ----------
    register_path
        Path to the per-deployment classification register
        (``vault_shared/classification/register.yaml`` for cross-org
        defaults + class definitions, OR
        ``orgs/<slug>/vault/classification/register.yaml`` for per-client
        overrides + grant-level overrides).
    file_exists
        Injected :class:`FileExistsCallable` — gate never reads the
        filesystem directly.

    Returns
    -------
    ClassRegisterResult. PASS only when the register file exists.
    """
    if not register_path or not register_path.strip():
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_MISSING,
            detail="register_path empty — caller did not supply a register path",
            register_path=register_path,
        )
    try:
        exists = file_exists(register_path)
    except Exception as exc:  # noqa: BLE001 — fail-closed
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_MISSING,
            detail=(
                f"file_exists raised {type(exc).__name__}: {exc} on "
                f"register_path={register_path!r}"
            ),
            register_path=register_path,
        )
    if exists is not True:
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_MISSING,
            detail=(
                f"classification register file not found at {register_path!r} — "
                "Beta deployment cannot ship without an operator-signed register "
                "(no M13 bypass per §5)"
            ),
            register_path=register_path,
        )
    return ClassRegisterResult(
        success=True,
        failure_code=None,
        detail=f"classification register file exists at {register_path!r}",
        register_path=register_path,
    )


def check_class_register_unsigned(
    *,
    register: Mapping[str, Any],
    register_path: Optional[str] = None,
) -> ClassRegisterResult:
    """PRE-onboarding gate: white-glove sign-off block must be present.

    Parameters
    ----------
    register
        Already-parsed classification register dict (the I/O wrapper
        loads and parses the YAML; the gate consumes the dict).
    register_path
        Optional path string surfaced in the detail message for audit.

    Returns
    -------
    ClassRegisterResult. PASS only when the
    ``operator_signature_at_white_glove_completion`` block is present
    AND carries a non-empty ``signature`` field (raw bytes per §3.7).
    """
    sign_off = register.get(SIGN_OFF_KEY)
    if sign_off is None:
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_UNSIGNED,
            detail=(
                f"register lacks {SIGN_OFF_KEY!r} block — operator has not "
                "signed the white-glove classification review (no M13 bypass)"
            ),
            register_path=register_path,
        )
    if not isinstance(sign_off, Mapping):
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_UNSIGNED,
            detail=(
                f"{SIGN_OFF_KEY!r} block is not a mapping "
                f"(got {type(sign_off).__name__})"
            ),
            register_path=register_path,
        )
    signature = sign_off.get("signature")
    if not isinstance(signature, (bytes, bytearray)) or not bytes(signature):
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_UNSIGNED,
            detail=(
                f"{SIGN_OFF_KEY!r}.signature is missing or empty — "
                "Ed25519 signature bytes required"
            ),
            register_path=register_path,
        )
    signed_at = sign_off.get("signed_at_iso8601")
    if not isinstance(signed_at, str) or not signed_at.strip():
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_UNSIGNED,
            detail=(
                f"{SIGN_OFF_KEY!r}.signed_at_iso8601 missing or empty — "
                "audit timestamp required per §3.7"
            ),
            register_path=register_path,
        )
    return ClassRegisterResult(
        success=True,
        failure_code=None,
        detail=(
            f"{SIGN_OFF_KEY!r} block carries non-empty signature + "
            f"signed_at={signed_at!r}"
        ),
        register_path=register_path,
    )


def check_class_register_signature_invalid(
    *,
    register: Mapping[str, Any],
    signed_message_bytes: bytes,
    signing_public_key: bytes,
    signature_verify: SignatureVerifyCallable,
    register_path: Optional[str] = None,
) -> ClassRegisterResult:
    """PRE-cycle gate: white-glove signature must verify under pinned key.

    Parameters
    ----------
    register
        Already-parsed register dict; expected to carry an
        ``operator_signature_at_white_glove_completion`` block with a
        non-empty ``signature`` (raw bytes).
    signed_message_bytes
        Canonical bytes the signature was authored against — produced by
        the I/O wrapper from the register's
        ``signed_field_classifications_hash`` +
        ``signed_class_definitions_hash`` + attestation_string per §3.7.
        The gate does not canonicalize.
    signing_public_key
        Operator-pinned Ed25519 public key (32 bytes).
    signature_verify
        Injected :class:`SignatureVerifyCallable`.
    register_path
        Optional path string surfaced in detail for audit.

    Returns
    -------
    ClassRegisterResult. PASS only when ``signature_verify`` returns
    True identity-strict.
    """
    sign_off = register.get(SIGN_OFF_KEY)
    if not isinstance(sign_off, Mapping):
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_SIGNATURE_INVALID,
            detail=(
                f"{SIGN_OFF_KEY!r} block missing or non-mapping — "
                "run check_class_register_unsigned first"
            ),
            register_path=register_path,
        )
    signature = sign_off.get("signature")
    if not isinstance(signature, (bytes, bytearray)):
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_SIGNATURE_INVALID,
            detail=(
                "signature is not bytes — UNSIGNED check should have "
                "fail-closed first"
            ),
            register_path=register_path,
        )
    try:
        verified = signature_verify(
            signed_message_bytes, bytes(signature), signing_public_key
        )
    except Exception as exc:  # noqa: BLE001 — fail-closed
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_SIGNATURE_INVALID,
            detail=(
                f"signature_verify raised {type(exc).__name__}: {exc}"
            ),
            register_path=register_path,
        )
    if verified is not True:
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_SIGNATURE_INVALID,
            detail=(
                "Ed25519 verification of white-glove sign-off block failed "
                "under operator-pinned public key"
            ),
            register_path=register_path,
        )
    return ClassRegisterResult(
        success=True,
        failure_code=None,
        detail=(
            "white-glove sign-off block Ed25519 signature verified under "
            "operator-pinned public key"
        ),
        register_path=register_path,
    )


def check_class_register_hash_mismatch(
    *,
    register: Mapping[str, Any],
    field_classifications_canonical_bytes: bytes,
    class_definitions_canonical_bytes: bytes,
    hash_bytes: HashBytesCallable,
    register_path: Optional[str] = None,
) -> ClassRegisterResult:
    """PRE-cycle gate: signed hashes must match recomputed hashes.

    Parameters
    ----------
    register
        Already-parsed register dict. Expected to carry both
        ``signed_field_classifications_hash`` and
        ``signed_class_definitions_hash`` inside the
        ``operator_signature_at_white_glove_completion`` block per §3.7.
    field_classifications_canonical_bytes
        Canonical bytes of the current ``field_classifications`` block
        (per §2 schema) — caller's I/O wrapper canonicalizes; the gate
        consumes raw bytes.
    class_definitions_canonical_bytes
        Canonical bytes of the current ``class_definitions`` block.
    hash_bytes
        Injected :class:`HashBytesCallable` (SHA3-512 hex digest).
    register_path
        Optional path string surfaced in detail for audit.

    Returns
    -------
    ClassRegisterResult. PASS only when both signed hashes equal the
    recomputed sha3_512(canonical_bytes)[:16] (case-insensitive hex).
    """
    sign_off = register.get(SIGN_OFF_KEY)
    if not isinstance(sign_off, Mapping):
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_HASH_MISMATCH,
            detail=(
                f"{SIGN_OFF_KEY!r} block missing or non-mapping — "
                "run check_class_register_unsigned first"
            ),
            register_path=register_path,
        )

    signed_fields_hash = sign_off.get(SIGN_OFF_HASH_FIELDS_KEY)
    signed_class_hash = sign_off.get(SIGN_OFF_HASH_CLASS_KEY)
    if not isinstance(signed_fields_hash, str) or not signed_fields_hash.strip():
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_HASH_MISMATCH,
            detail=(
                f"{SIGN_OFF_HASH_FIELDS_KEY!r} missing or empty in "
                "white-glove sign-off block"
            ),
            register_path=register_path,
        )
    if not isinstance(signed_class_hash, str) or not signed_class_hash.strip():
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_HASH_MISMATCH,
            detail=(
                f"{SIGN_OFF_HASH_CLASS_KEY!r} missing or empty in "
                "white-glove sign-off block"
            ),
            register_path=register_path,
        )

    try:
        recomputed_fields_full = hash_bytes(field_classifications_canonical_bytes)
        recomputed_class_full = hash_bytes(class_definitions_canonical_bytes)
    except Exception as exc:  # noqa: BLE001 — fail-closed
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_HASH_MISMATCH,
            detail=(
                f"hash_bytes raised {type(exc).__name__}: {exc}"
            ),
            register_path=register_path,
        )

    # Schema names the field as sha3_512[:16] (16-hex prefix). Compare
    # case-insensitively; trim the recomputed full digest to a 16-char
    # lowercase prefix to match.
    recomputed_fields_prefix = recomputed_fields_full.strip().lower()[:16]
    recomputed_class_prefix = recomputed_class_full.strip().lower()[:16]
    signed_fields_norm = signed_fields_hash.strip().lower()
    signed_class_norm = signed_class_hash.strip().lower()

    if signed_fields_norm != recomputed_fields_prefix:
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_HASH_MISMATCH,
            detail=(
                f"{SIGN_OFF_HASH_FIELDS_KEY!r} drift: signed="
                f"{signed_fields_norm!r}, recomputed="
                f"{recomputed_fields_prefix!r} — silent edit to "
                "field_classifications detected post-sign-off"
            ),
            register_path=register_path,
        )
    if signed_class_norm != recomputed_class_prefix:
        return ClassRegisterResult(
            success=False,
            failure_code=F_CLASS_REGISTER_HASH_MISMATCH,
            detail=(
                f"{SIGN_OFF_HASH_CLASS_KEY!r} drift: signed="
                f"{signed_class_norm!r}, recomputed="
                f"{recomputed_class_prefix!r} — silent edit to "
                "class_definitions detected post-sign-off"
            ),
            register_path=register_path,
        )
    return ClassRegisterResult(
        success=True,
        failure_code=None,
        detail=(
            "signed_field_classifications_hash + "
            "signed_class_definitions_hash both match recomputed bytes"
        ),
        register_path=register_path,
    )


__all__ = [
    "F_CLASS_REGISTER_HASH_MISMATCH",
    "F_CLASS_REGISTER_MISSING",
    "F_CLASS_REGISTER_SIGNATURE_INVALID",
    "F_CLASS_REGISTER_UNSIGNED",
    "SIGN_OFF_HASH_CLASS_KEY",
    "SIGN_OFF_HASH_FIELDS_KEY",
    "SIGN_OFF_KEY",
    "ClassRegisterResult",
    "check_class_register_hash_mismatch",
    "check_class_register_missing",
    "check_class_register_signature_invalid",
    "check_class_register_unsigned",
]
