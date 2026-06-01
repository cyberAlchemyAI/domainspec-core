"""Section 2 Vault failure-code registry + base exception classes.

Every failure code raised by the Vault layer carries a ``code`` attribute on
its exception so the rails-report emitter can include it verbatim without
string parsing. Constants are canonical and referenced by both the Vault
implementation and the Section 4 Logician predicates.

Blueprint §6.1–§6.12 (section_02_vault_topology.md).
"""

from __future__ import annotations

from typing import Final


BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§6.1 F-VAULT-* failure-code registry",
            "§6.2 F-GATE-* failure-code registry",
            "§6.3 F-MIRROR-* failure-code registry",
            "§6.4 F-WRAPPER-* failure-code registry",
            "§6.5 F-UUID-* failure-code registry",
            "§6.6 F-SECCOMP-* / F-SANDBOX-* failure-code registry",
            "§6.7 F-DIRECT-* failure-code registry",
            "§6.8 F-FD-* failure-code registry",
            "§6.9 F-M15-* failure-code registry",
            "§6.10 F-NS-* / F-FREEZE-* failure-code registry",
            "§6.11 F-INIT-* failure-code registry",
            "§6.12 F-CEDAR-* failure-code registry",
            "§4.2 VaultXattrStripIncomplete bound to F-VAULT-05 (canonical)",
            "Option-B compound-txn codes F-VAULT-24..F-VAULT-28 (lines 1112-1116)",
        ],
    },
}


# ---------------------------------------------------------------------------
# Failure-code constants (string literals, one per blueprint row)
# ---------------------------------------------------------------------------

# §6.1 F-VAULT-*
F_VAULT_01 = "F-VAULT-01"  # VaultReadDenied
F_VAULT_02 = "F-VAULT-02"  # VaultWriteDenied
F_VAULT_03 = "F-VAULT-03"  # VaultSlugUnknown
F_VAULT_04 = "F-VAULT-04"  # VaultCrossOrgAccess
F_VAULT_05 = "F-VAULT-05"  # VaultXattrStripIncomplete (canonical per §2 v7.1 §6.1 + §4.2)
F_VAULT_06 = "F-VAULT-06"  # VaultMachPortDenied (A-11 regression)
F_VAULT_07 = "F-VAULT-07"  # VaultCopyfileOutOfScope (A-18 regression)
F_VAULT_24 = "F-VAULT-24"  # CompoundTxnCapExceeded
F_VAULT_25 = "F-VAULT-25"  # CompoundHashBindingMismatch (§2 v7.1 line 1113)
F_VAULT_26 = "F-VAULT-26"  # CompoundSessionMismatch (§2 v7.1 line 1114)
F_VAULT_27 = "F-VAULT-27"  # CompoundCommitUndoFailed (§2 v7.1 line 1115)
F_VAULT_28 = "F-VAULT-28"  # CompoundTxnProtocolViolation
F_VAULT_WRITE_EXISTS = "F-VAULT-WRITE-EXISTS"
F_VAULT_CAS_HEAD_MISMATCH = "F-VAULT-CAS-HEAD-MISMATCH"
F_VAULT_COMPOUND_INTEGRITY = "F-VAULT-COMPOUND-INTEGRITY"
F_VAULT_COMPOUND_OVERSIZE = "F-VAULT-COMPOUND-OVERSIZE"
F_VAULT_COMPOUND_TTL_EXPIRED = "F-VAULT-COMPOUND-TTL-EXPIRED"

# §6.2 F-GATE-*
F_GATE_01 = "F-GATE-01"  # openat2-unavailable / ELOOP / path-too-deep
F_GATE_02 = "F-GATE-02"  # identity-tuple pinning drift at post-open fstat
F_GATE_03 = "F-GATE-03"  # mount-over detected mid-walk (A-02 regression)
F_GATE_04 = "F-GATE-04"  # magic-link (/proc/self/fd/*) denied
F_GATE_05 = "F-GATE-05"  # embedded null byte in path (A-12 regression)
F_GATE_06 = "F-GATE-06"  # /dev/fd/* denied (A-15 regression)
F_GATE_07 = "F-GATE-07"  # non-NFC Unicode in path (B-03 regression)
F_GATE_08 = "F-GATE-08"  # bidi control / zero-width char in path (C-03 v3)
F_GATE_09 = "F-GATE-09"  # percent-encoded null in path (C-03 v3)
F_GATE_10 = "F-GATE-10"  # NFC-vs-NFKC ambiguity (C-06 v3)

# §6.3 F-MIRROR-*
F_MIRROR_01 = "F-MIRROR-01"  # TrustRootMirrorIdentityMismatch
F_MIRROR_02 = "F-MIRROR-02"  # TrustRootMirrorContentMismatch
F_MIRROR_03 = "F-MIRROR-03"  # TrustRootMirrorSignatureMismatch
F_MIRROR_04 = "F-MIRROR-04"  # TrustRootMirrorImmutabilityMissing
F_MIRROR_05 = "F-MIRROR-05"  # TrustRootMirrorStaleReverify

# §6.4 F-WRAPPER-*
F_WRAPPER_01 = "F-WRAPPER-01"  # WrapperHashMismatchAtBoot
F_WRAPPER_02 = "F-WRAPPER-02"  # WrapperHashMismatchAtExec
F_WRAPPER_03 = "F-WRAPPER-03"  # WrapperManifestSignatureInvalid
F_WRAPPER_04 = "F-WRAPPER-04"  # WrapperModeIncorrect

# §6.5 F-UUID-*
F_UUID_01 = "F-UUID-01"  # UuidFloorRejected

# §6.6 F-SECCOMP-* / F-SANDBOX-*
F_SECCOMP_01 = "F-SECCOMP-01"  # SeccompFilterUnavailable
F_SECCOMP_02 = "F-SECCOMP-02"  # SeccompFilterHashMismatch
F_SECCOMP_06 = "F-SECCOMP-06"  # SeccompDupFamilyDenied (C-01 v3)
F_SANDBOX_01 = "F-SANDBOX-01"  # SandboxProfileHashMismatch
F_SANDBOX_04 = "F-SANDBOX-04"  # SandboxDyldInterposerMissing (A-06)

# §6.7 F-DIRECT-*
F_DIRECT_01 = "F-DIRECT-01"  # DirectFSTouchDetected
F_DIRECT_02 = "F-DIRECT-02"  # DirectOpenbyidDenied (A-10)
F_DIRECT_03 = "F-DIRECT-03"  # DirectIOUringInherit (A-13 / C-05)
F_DIRECT_04 = "F-DIRECT-04"  # DirectProcPidDenied (A-16)
F_DIRECT_05 = "F-DIRECT-05"  # DirectNSURLBookmarkDenied (C-02 v3)

# §6.8 F-FD-*
F_FD_01 = "F-FD-01"  # FdBrokerUnknownSkill
F_FD_02 = "F-FD-02"  # FdBrokerNonceReplayed
F_FD_03 = "F-FD-03"  # FdBrokerCedarVeto
F_FD_04 = "F-FD-04"  # FdBrokerTimeout
F_FD_05 = "F-FD-05"  # FdBrokerHmacChallengeFailed (A-05 / C-04)
F_FD_06 = "F-FD-06"  # FdBrokerSocketIdentityInvalid (A-14)
F_FD_07 = "F-FD-07"  # FdBrokerMountOverAtHandout (A-17)

# §6.9 F-M15-*
F_M15_01 = "F-M15-01"  # SeedManifestFileMismatch
F_M15_02 = "F-M15-02"  # SeedManifestSignatureInvalid
F_M15_03 = "F-M15-03"  # SeedManifestLedgerHeadDrift

# §6.10 F-NS-* / F-FREEZE-*
F_NS_01 = "F-NS-01"  # MountNamespaceUnavailable
F_FREEZE_01 = "F-FREEZE-01"  # AtomicFreezeFailed
F_FREEZE_04 = "F-FREEZE-04"  # SnapshotRetentionCleanupFailed (A-09)

# §6.11 F-INIT-*
F_INIT_01 = "F-INIT-01"  # VaultInitMissing
F_INIT_02 = "F-INIT-02"  # VaultInitHmacMismatch
F_INIT_03 = "F-INIT-03"  # VaultInitIdentityDrift

# §6.12 F-CEDAR-*
F_CEDAR_01 = "F-CEDAR-01"  # CedarPolicyLoadFailed
F_CEDAR_02 = "F-CEDAR-02"  # CedarDecisionDenied
F_CEDAR_SECTION4_WRITE_PATH_DENIED = "F-CEDAR-SECTION4-WRITE-PATH-DENIED"


# ---------------------------------------------------------------------------
# Base exception taxonomy (E-014)
# ---------------------------------------------------------------------------


class VaultError(Exception):
    """Parent of every Vault-layer failure. `code` is the rails-report string."""

    code: str = "F-VAULT"


class VaultAccessDenied(VaultError):
    code = F_VAULT_01


class VaultWriteDenied(VaultError):
    code = F_VAULT_02


class VaultSlugUnknown(VaultError):
    code = F_VAULT_03


class VaultCrossOrgAccess(VaultError):
    code = F_VAULT_04


class VaultWriteExists(VaultError):
    code = F_VAULT_WRITE_EXISTS


class VaultCASHeadMismatch(VaultError):
    code = F_VAULT_CAS_HEAD_MISMATCH

    def __init__(
        self,
        message: str = "",
        *,
        expected_current_file_hash: str = "",
        actual_current_file_hash: str = "",
    ) -> None:
        super().__init__(message)
        self.expected_current_file_hash = expected_current_file_hash
        self.actual_current_file_hash = actual_current_file_hash


class VaultCompoundIntegrityError(VaultError):
    code = F_VAULT_COMPOUND_INTEGRITY


class VaultCompoundOversize(VaultError):
    code = F_VAULT_COMPOUND_OVERSIZE


class VaultCompoundTTLExpired(VaultError):
    code = F_VAULT_COMPOUND_TTL_EXPIRED


class VaultCompoundProtocolViolation(VaultError):
    code = F_VAULT_28

    def __init__(
        self,
        message: str = "",
        *,
        sub_reason: str = "",
    ) -> None:
        super().__init__(message)
        self.sub_reason = sub_reason


class VaultCompoundCapExceeded(VaultError):
    code = F_VAULT_24


class VaultCompoundHashBindingMismatch(VaultError):
    """Blueprint §2 v7.1 line 1113: compound-txn hash-binding mismatch at commit."""

    code = F_VAULT_25


class VaultCompoundSessionMismatch(VaultError):
    """Blueprint §2 v7.1 line 1114: compound-txn session-ID mismatch at commit."""

    code = F_VAULT_26


class VaultCompoundCommitUndoFailed(VaultError):
    """Blueprint §2 v7.1 line 1115: compound-commit undo path failed post-partial-commit."""

    code = F_VAULT_27


class VaultXattrStripIncomplete(VaultError):
    code = F_VAULT_05

    def __init__(self, message: str = "", *, residual_keys: tuple[str, ...] = ()) -> None:
        super().__init__(message)
        self.residual_keys = residual_keys


class GateError(VaultError):
    code = F_GATE_01

    def __init__(
        self,
        message: str = "",
        *,
        path: str = "",
        reason: str = "",
        detail: str = "",
    ) -> None:
        super().__init__(message)
        self.path = path
        self.reason = reason
        self.detail = detail


class GateOpenRejected(GateError):
    code = F_GATE_01


class GateIdentityTupleMismatch(GateError):
    code = F_GATE_02


class GateAncestorMountMismatch(GateError):
    code = F_GATE_03


class GateMagicLinkRejected(GateError):
    code = F_GATE_04


class GatePathNullByte(GateError):
    code = F_GATE_05


class GateDevFdRejected(GateError):
    code = F_GATE_06


class GatePathUnicodeNonNormal(GateError):
    code = F_GATE_07


class GatePathUnicodeForbidden(GateError):
    code = F_GATE_08


class GatePercentNullRejected(GateError):
    code = F_GATE_09


class GateNFCNFKCDivergence(GateError):
    code = F_GATE_10


class MirrorError(VaultError):
    code = F_MIRROR_01


class WrapperError(VaultError):
    code = F_WRAPPER_01


class UUIDFloorError(VaultError):
    code = F_UUID_01


class SeccompError(VaultError):
    code = F_SECCOMP_01


class SandboxError(VaultError):
    code = F_SANDBOX_01


class DirectFSError(VaultError):
    code = F_DIRECT_01


class FDBrokerError(VaultError):
    code = F_FD_01


class M15Error(VaultError):
    code = F_M15_01


class NamespaceError(VaultError):
    code = F_NS_01


class FreezeError(VaultError):
    code = F_FREEZE_01


class VaultInitError(VaultError):
    code = F_INIT_01


class VaultInitHMACMismatch(VaultError):
    code = F_INIT_02


class VaultInitIdentityDrift(VaultError):
    code = F_INIT_03


class CedarError(VaultError):
    code = F_CEDAR_01


class CedarSection4WritePathDenied(VaultError):
    code = F_CEDAR_SECTION4_WRITE_PATH_DENIED

    def __init__(
        self,
        message: str = "",
        *,
        attempted_path: str = "",
        attempted_intent: str = "",
        cedar_decision_id: str = "",
        reason: str = "",
        type_error: str = "",
    ) -> None:
        super().__init__(message)
        self.attempted_path = attempted_path
        self.attempted_intent = attempted_intent
        self.cedar_decision_id = cedar_decision_id
        self.reason = reason
        self.type_error = type_error


__all__ = [name for name in globals() if name.startswith(("F_", "Vault", "Gate", "Mirror", "Wrapper", "UUID", "Seccomp", "Sandbox", "DirectFS", "FDBroker", "M15", "Namespace", "Freeze", "Cedar"))]
