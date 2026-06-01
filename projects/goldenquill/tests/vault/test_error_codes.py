"""Unit tests for pipeline.vault.error_codes (§2 Vault §6.1–§6.12 failure-code registry + E-014 exception taxonomy).

Promotes error_codes.py from transitively-covered status (Batch 1 disclosure D-01)
to dedicated coverage. Exercises:

* Every ``F_*`` failure-code string constant matches its canonical ``F-…`` literal
  exactly (no silent drift of the rails-report emission surface).
* Every exception class exposes the ``code`` class attribute wired to the
  correct ``F_*`` constant — the rails-report emitter depends on this mapping.
* Structured-field exceptions (``VaultCASHeadMismatch``, ``VaultXattrStripIncomplete``,
  ``GateError``, ``CedarSection4WritePathDenied``) surface their keyword init
  arguments as instance attributes with sensible defaults.
* ``VaultError`` is the common parent; every subclass is isinstance-traceable back
  to it so the Section 4 Logician's broad ``except VaultError:`` handlers hold.
* ``__all__`` contains every public symbol and no internal names — the re-export
  surface in ``pipeline/vault/__init__.py`` depends on this being exhaustive.
"""

from __future__ import annotations

import pipeline.vault.error_codes as error_codes
from pipeline.vault.error_codes import (
    F_CEDAR_01,
    F_CEDAR_02,
    F_CEDAR_SECTION4_WRITE_PATH_DENIED,
    F_DIRECT_01,
    F_DIRECT_02,
    F_DIRECT_03,
    F_DIRECT_04,
    F_DIRECT_05,
    F_FD_01,
    F_FD_02,
    F_FD_03,
    F_FD_04,
    F_FD_05,
    F_FD_06,
    F_FD_07,
    F_FREEZE_01,
    F_FREEZE_04,
    F_GATE_01,
    F_GATE_02,
    F_GATE_03,
    F_GATE_04,
    F_GATE_05,
    F_GATE_06,
    F_GATE_07,
    F_GATE_08,
    F_GATE_09,
    F_GATE_10,
    F_INIT_01,
    F_INIT_02,
    F_INIT_03,
    F_M15_01,
    F_M15_02,
    F_M15_03,
    F_MIRROR_01,
    F_MIRROR_02,
    F_MIRROR_03,
    F_MIRROR_04,
    F_MIRROR_05,
    F_NS_01,
    F_SANDBOX_01,
    F_SANDBOX_04,
    F_SECCOMP_01,
    F_SECCOMP_02,
    F_SECCOMP_06,
    F_UUID_01,
    F_VAULT_01,
    F_VAULT_02,
    F_VAULT_03,
    F_VAULT_04,
    F_VAULT_05,
    F_VAULT_06,
    F_VAULT_07,
    F_VAULT_24,
    F_VAULT_25,
    F_VAULT_26,
    F_VAULT_27,
    F_VAULT_28,
    F_VAULT_CAS_HEAD_MISMATCH,
    F_VAULT_COMPOUND_INTEGRITY,
    F_VAULT_COMPOUND_OVERSIZE,
    F_VAULT_COMPOUND_TTL_EXPIRED,
    F_VAULT_WRITE_EXISTS,
    F_WRAPPER_01,
    F_WRAPPER_02,
    F_WRAPPER_03,
    F_WRAPPER_04,
    CedarError,
    CedarSection4WritePathDenied,
    DirectFSError,
    FDBrokerError,
    FreezeError,
    GateAncestorMountMismatch,
    GateDevFdRejected,
    GateError,
    GateIdentityTupleMismatch,
    GateMagicLinkRejected,
    GateNFCNFKCDivergence,
    GateOpenRejected,
    GatePathNullByte,
    GatePathUnicodeForbidden,
    GatePathUnicodeNonNormal,
    GatePercentNullRejected,
    M15Error,
    MirrorError,
    NamespaceError,
    SandboxError,
    SeccompError,
    UUIDFloorError,
    VaultAccessDenied,
    VaultCASHeadMismatch,
    VaultCompoundCapExceeded,
    VaultCompoundCommitUndoFailed,
    VaultCompoundHashBindingMismatch,
    VaultCompoundIntegrityError,
    VaultCompoundOversize,
    VaultCompoundProtocolViolation,
    VaultCompoundSessionMismatch,
    VaultCompoundTTLExpired,
    VaultCrossOrgAccess,
    VaultError,
    VaultInitError,
    VaultInitHMACMismatch,
    VaultInitIdentityDrift,
    VaultSlugUnknown,
    VaultWriteDenied,
    VaultWriteExists,
    VaultXattrStripIncomplete,
    WrapperError,
)


# ---------------------------------------------------------------------------
# §6.1–§6.12 failure-code string constants
# ---------------------------------------------------------------------------


_EXPECTED_CONSTANTS: dict[str, str] = {
    # §6.1 F-VAULT-*
    "F_VAULT_01": "F-VAULT-01",
    "F_VAULT_02": "F-VAULT-02",
    "F_VAULT_03": "F-VAULT-03",
    "F_VAULT_04": "F-VAULT-04",
    "F_VAULT_05": "F-VAULT-05",
    "F_VAULT_06": "F-VAULT-06",
    "F_VAULT_07": "F-VAULT-07",
    "F_VAULT_24": "F-VAULT-24",
    "F_VAULT_25": "F-VAULT-25",
    "F_VAULT_26": "F-VAULT-26",
    "F_VAULT_27": "F-VAULT-27",
    "F_VAULT_28": "F-VAULT-28",
    "F_VAULT_WRITE_EXISTS": "F-VAULT-WRITE-EXISTS",
    "F_VAULT_CAS_HEAD_MISMATCH": "F-VAULT-CAS-HEAD-MISMATCH",
    "F_VAULT_COMPOUND_INTEGRITY": "F-VAULT-COMPOUND-INTEGRITY",
    "F_VAULT_COMPOUND_OVERSIZE": "F-VAULT-COMPOUND-OVERSIZE",
    "F_VAULT_COMPOUND_TTL_EXPIRED": "F-VAULT-COMPOUND-TTL-EXPIRED",
    # §6.2 F-GATE-*
    "F_GATE_01": "F-GATE-01",
    "F_GATE_02": "F-GATE-02",
    "F_GATE_03": "F-GATE-03",
    "F_GATE_04": "F-GATE-04",
    "F_GATE_05": "F-GATE-05",
    "F_GATE_06": "F-GATE-06",
    "F_GATE_07": "F-GATE-07",
    "F_GATE_08": "F-GATE-08",
    "F_GATE_09": "F-GATE-09",
    "F_GATE_10": "F-GATE-10",
    # §6.3 F-MIRROR-*
    "F_MIRROR_01": "F-MIRROR-01",
    "F_MIRROR_02": "F-MIRROR-02",
    "F_MIRROR_03": "F-MIRROR-03",
    "F_MIRROR_04": "F-MIRROR-04",
    "F_MIRROR_05": "F-MIRROR-05",
    # §6.4 F-WRAPPER-*
    "F_WRAPPER_01": "F-WRAPPER-01",
    "F_WRAPPER_02": "F-WRAPPER-02",
    "F_WRAPPER_03": "F-WRAPPER-03",
    "F_WRAPPER_04": "F-WRAPPER-04",
    # §6.5 F-UUID-*
    "F_UUID_01": "F-UUID-01",
    # §6.6 F-SECCOMP-* / F-SANDBOX-*
    "F_SECCOMP_01": "F-SECCOMP-01",
    "F_SECCOMP_02": "F-SECCOMP-02",
    "F_SECCOMP_06": "F-SECCOMP-06",
    "F_SANDBOX_01": "F-SANDBOX-01",
    "F_SANDBOX_04": "F-SANDBOX-04",
    # §6.7 F-DIRECT-*
    "F_DIRECT_01": "F-DIRECT-01",
    "F_DIRECT_02": "F-DIRECT-02",
    "F_DIRECT_03": "F-DIRECT-03",
    "F_DIRECT_04": "F-DIRECT-04",
    "F_DIRECT_05": "F-DIRECT-05",
    # §6.8 F-FD-*
    "F_FD_01": "F-FD-01",
    "F_FD_02": "F-FD-02",
    "F_FD_03": "F-FD-03",
    "F_FD_04": "F-FD-04",
    "F_FD_05": "F-FD-05",
    "F_FD_06": "F-FD-06",
    "F_FD_07": "F-FD-07",
    # §6.9 F-M15-*
    "F_M15_01": "F-M15-01",
    "F_M15_02": "F-M15-02",
    "F_M15_03": "F-M15-03",
    # §6.10 F-NS-* / F-FREEZE-*
    "F_NS_01": "F-NS-01",
    "F_FREEZE_01": "F-FREEZE-01",
    "F_FREEZE_04": "F-FREEZE-04",
    # §6.11 F-INIT-*
    "F_INIT_01": "F-INIT-01",
    "F_INIT_02": "F-INIT-02",
    "F_INIT_03": "F-INIT-03",
    # §6.12 F-CEDAR-*
    "F_CEDAR_01": "F-CEDAR-01",
    "F_CEDAR_02": "F-CEDAR-02",
    "F_CEDAR_SECTION4_WRITE_PATH_DENIED": "F-CEDAR-SECTION4-WRITE-PATH-DENIED",
}


class TestFailureCodeConstants:
    def test_every_constant_matches_canonical_literal(self) -> None:
        for name, expected in _EXPECTED_CONSTANTS.items():
            observed = getattr(error_codes, name)
            assert observed == expected, (name, observed, expected)

    def test_every_constant_is_a_str(self) -> None:
        for name in _EXPECTED_CONSTANTS:
            assert isinstance(getattr(error_codes, name), str)

    def test_no_duplicate_failure_code_values(self) -> None:
        values = [getattr(error_codes, n) for n in _EXPECTED_CONSTANTS]
        assert len(values) == len(set(values))


# ---------------------------------------------------------------------------
# E-014 exception taxonomy: class → code attribute mapping
# ---------------------------------------------------------------------------


_EXPECTED_EXCEPTION_CODE_MAP: dict[type, str] = {
    # §6.1 Vault-layer taxonomy
    VaultError: "F-VAULT",
    VaultAccessDenied: F_VAULT_01,
    VaultWriteDenied: F_VAULT_02,
    VaultSlugUnknown: F_VAULT_03,
    VaultCrossOrgAccess: F_VAULT_04,
    VaultWriteExists: F_VAULT_WRITE_EXISTS,
    VaultCASHeadMismatch: F_VAULT_CAS_HEAD_MISMATCH,
    VaultCompoundIntegrityError: F_VAULT_COMPOUND_INTEGRITY,
    VaultCompoundOversize: F_VAULT_COMPOUND_OVERSIZE,
    VaultCompoundTTLExpired: F_VAULT_COMPOUND_TTL_EXPIRED,
    VaultCompoundProtocolViolation: F_VAULT_28,
    VaultCompoundCapExceeded: F_VAULT_24,
    VaultCompoundHashBindingMismatch: F_VAULT_25,
    VaultCompoundSessionMismatch: F_VAULT_26,
    VaultCompoundCommitUndoFailed: F_VAULT_27,
    VaultXattrStripIncomplete: F_VAULT_05,
    # §6.2 Gate taxonomy
    GateError: F_GATE_01,
    GateOpenRejected: F_GATE_01,
    GateIdentityTupleMismatch: F_GATE_02,
    GateAncestorMountMismatch: F_GATE_03,
    GateMagicLinkRejected: F_GATE_04,
    GatePathNullByte: F_GATE_05,
    GateDevFdRejected: F_GATE_06,
    GatePathUnicodeNonNormal: F_GATE_07,
    GatePathUnicodeForbidden: F_GATE_08,
    GatePercentNullRejected: F_GATE_09,
    GateNFCNFKCDivergence: F_GATE_10,
    # §6.3–§6.10 first-row representatives
    MirrorError: F_MIRROR_01,
    WrapperError: F_WRAPPER_01,
    UUIDFloorError: F_UUID_01,
    SeccompError: F_SECCOMP_01,
    SandboxError: F_SANDBOX_01,
    DirectFSError: F_DIRECT_01,
    FDBrokerError: F_FD_01,
    M15Error: F_M15_01,
    NamespaceError: F_NS_01,
    FreezeError: F_FREEZE_01,
    # §6.11 init taxonomy
    VaultInitError: F_INIT_01,
    VaultInitHMACMismatch: F_INIT_02,
    VaultInitIdentityDrift: F_INIT_03,
    # §6.12 Cedar taxonomy
    CedarError: F_CEDAR_01,
    CedarSection4WritePathDenied: F_CEDAR_SECTION4_WRITE_PATH_DENIED,
}


class TestExceptionCodeAttribute:
    def test_every_class_has_expected_code(self) -> None:
        for cls, expected in _EXPECTED_EXCEPTION_CODE_MAP.items():
            assert cls.code == expected, (cls.__name__, cls.code, expected)

    def test_instances_carry_code_through_raising(self) -> None:
        for cls, expected in _EXPECTED_EXCEPTION_CODE_MAP.items():
            if cls is VaultError:
                continue
            if cls in {
                VaultCASHeadMismatch,
                VaultXattrStripIncomplete,
                CedarSection4WritePathDenied,
            }:
                inst = cls("msg")
            elif issubclass(cls, GateError):
                inst = cls("msg")
            else:
                inst = cls("msg")
            assert inst.code == expected
            assert isinstance(inst, VaultError)


# ---------------------------------------------------------------------------
# Inheritance hygiene — every concrete class is a VaultError subclass
# ---------------------------------------------------------------------------


class TestInheritanceHygiene:
    def test_vault_error_is_parent_of_every_concrete_class(self) -> None:
        for cls in _EXPECTED_EXCEPTION_CODE_MAP:
            assert issubclass(cls, VaultError), cls.__name__

    def test_vault_error_inherits_from_exception(self) -> None:
        assert issubclass(VaultError, Exception)

    def test_gate_subclasses_inherit_from_gate_error(self) -> None:
        gate_subclasses = [
            GateOpenRejected,
            GateIdentityTupleMismatch,
            GateAncestorMountMismatch,
            GateMagicLinkRejected,
            GatePathNullByte,
            GateDevFdRejected,
            GatePathUnicodeNonNormal,
            GatePathUnicodeForbidden,
            GatePercentNullRejected,
            GateNFCNFKCDivergence,
        ]
        for cls in gate_subclasses:
            assert issubclass(cls, GateError), cls.__name__

    def test_vault_error_default_code_is_f_vault_family_marker(self) -> None:
        assert VaultError.code == "F-VAULT"


# ---------------------------------------------------------------------------
# Structured-field exception classes — keyword args surface as attributes
# ---------------------------------------------------------------------------


class TestVaultCASHeadMismatchFields:
    def test_default_field_values_are_empty_strings(self) -> None:
        exc = VaultCASHeadMismatch()
        assert exc.expected_current_file_hash == ""
        assert exc.actual_current_file_hash == ""
        assert exc.code == F_VAULT_CAS_HEAD_MISMATCH

    def test_keyword_args_surface_as_attributes(self) -> None:
        exc = VaultCASHeadMismatch(
            "bad head",
            expected_current_file_hash="abc123",
            actual_current_file_hash="def456",
        )
        assert exc.expected_current_file_hash == "abc123"
        assert exc.actual_current_file_hash == "def456"
        assert str(exc) == "bad head"


class TestVaultXattrStripIncompleteFields:
    def test_default_residual_keys_is_empty_tuple(self) -> None:
        exc = VaultXattrStripIncomplete()
        assert exc.residual_keys == ()
        assert exc.code == F_VAULT_05

    def test_residual_keys_surfaces_as_tuple(self) -> None:
        exc = VaultXattrStripIncomplete(
            "residual found",
            residual_keys=("user.foo", "com.apple.quarantine"),
        )
        assert exc.residual_keys == ("user.foo", "com.apple.quarantine")


class TestGateErrorFields:
    def test_default_field_values_are_empty_strings(self) -> None:
        exc = GateError()
        assert exc.path == ""
        assert exc.reason == ""
        assert exc.detail == ""
        assert exc.code == F_GATE_01

    def test_keyword_args_surface_as_attributes(self) -> None:
        exc = GateError(
            "gate blocked",
            path="/var/tmp/danger",
            reason="ELOOP",
            detail="path-too-deep (>40)",
        )
        assert exc.path == "/var/tmp/danger"
        assert exc.reason == "ELOOP"
        assert exc.detail == "path-too-deep (>40)"

    def test_gate_subclass_inherits_field_surface(self) -> None:
        exc = GateIdentityTupleMismatch(
            "identity drift",
            path="/seed",
            reason="dev-ino",
            detail="post-open fstat drift",
        )
        assert exc.path == "/seed"
        assert exc.reason == "dev-ino"
        assert exc.detail == "post-open fstat drift"
        assert exc.code == F_GATE_02


class TestCedarSection4WritePathDeniedFields:
    def test_default_field_values_are_empty_strings(self) -> None:
        exc = CedarSection4WritePathDenied()
        assert exc.attempted_path == ""
        assert exc.attempted_intent == ""
        assert exc.cedar_decision_id == ""
        assert exc.code == F_CEDAR_SECTION4_WRITE_PATH_DENIED

    def test_keyword_args_surface_as_attributes(self) -> None:
        exc = CedarSection4WritePathDenied(
            "write denied",
            attempted_path="/orgs/x/draft.md",
            attempted_intent="draft-write",
            cedar_decision_id="dec-42",
        )
        assert exc.attempted_path == "/orgs/x/draft.md"
        assert exc.attempted_intent == "draft-write"
        assert exc.cedar_decision_id == "dec-42"


# ---------------------------------------------------------------------------
# BLUEPRINT_DEPS pin (F-5: vault_batch_1_redispatch_2026-04-22)
# ---------------------------------------------------------------------------


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        deps = error_codes.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"


# ---------------------------------------------------------------------------
# __all__ hygiene — public re-export surface is exhaustive + no leakage
# ---------------------------------------------------------------------------


class TestAllExportSurface:
    def test_every_failure_constant_is_exported(self) -> None:
        for name in _EXPECTED_CONSTANTS:
            assert name in error_codes.__all__, name

    def test_every_exception_class_is_exported(self) -> None:
        for cls in _EXPECTED_EXCEPTION_CODE_MAP:
            assert cls.__name__ in error_codes.__all__, cls.__name__

    def test_all_contains_no_private_or_dunder_names(self) -> None:
        for name in error_codes.__all__:
            assert not name.startswith("_"), name

    def test_every_all_entry_resolves(self) -> None:
        for name in error_codes.__all__:
            assert hasattr(error_codes, name), name
