"""Tests for ``pipeline.logician.cedar_eval``.

Round 6 capstone — Cedar entity shapes + minimal pure-Python evaluator. The
module is a deterministic leaf with no third-party Cedar engine; tests cover
the §2.6 entity shapes, the minimal compile + sign verifier, the three
per-policy evaluators, and the top-level dispatcher's fail-closed unknown-
policy behavior.
"""

from __future__ import annotations

import dataclasses

import pytest

from pipeline.logician.cedar_eval import (
    F_CEDAR_BYOK_KEY_SCOPE_DENY,
    F_CEDAR_CROSS_ORG_DENY,
    F_CEDAR_ORG_ISOLATION_DENY,
    F_CEDAR_UNKNOWN_POLICY,
    F_PRE_04_CEDAR_UNSIGNED,
    F_PRE_04_LEDGER_MISMATCH,
    F_PRE_17_CEDAR_COMPILE_ERROR,
    KNOWN_POLICY_NAMES,
    VALID_TAGS,
    CedarDecision,
    CedarPolicy,
    ClaimEntity,
    OperatorKeyringKeyEntity,
    SessionEntity,
    VaultPathEntity,
    compile_cedar_policy,
    evaluate,
    evaluate_byok_key_scope,
    evaluate_cross_org_dossier,
    evaluate_org_isolation,
    verify_cedar_policy_signed,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _session(org_slug: str = "mycosymbiotics_cooperative") -> SessionEntity:
    return SessionEntity(
        session_id="sess-1",
        org_slug=org_slug,
        org_root_hash="a" * 128,
        byok_key_id="key-1",
        started_at_utc="2026-04-19T12:00:00Z",
    )


def _vault_path(
    *,
    org_slug_hint: str = "mycosymbiotics_cooperative",
    is_shared: bool = False,
    canonical_path: str = "/vault/orgs/mycosymbiotics_cooperative/runs/r1",
) -> VaultPathEntity:
    return VaultPathEntity(
        canonical_path=canonical_path,
        inode=12345,
        volume_uuid="vol-1",
        org_slug_hint=org_slug_hint,
        is_shared=is_shared,
    )


def _claim(*, cross: bool = False, tag: str = "DOC_SOURCED") -> ClaimEntity:
    return ClaimEntity(
        claim_id="claim-1",
        tag=tag,
        source_kind="rfa",
        cross_org_dossier=cross,
    )


def _key(bound: str = "mycosymbiotics_cooperative") -> OperatorKeyringKeyEntity:
    return OperatorKeyringKeyEntity(key_id="key-1", bound_org_slug=bound)


def _policy(
    *,
    name: str = "org_isolation",
    text: str = "permit(principal, action, resource);",
    sig: bytes = b"\x01\x02",
    head: str = "h" * 128,
) -> CedarPolicy:
    return CedarPolicy(
        name=name,
        text=text,
        operator_signature=sig,
        signed_at_utc="2026-04-19T00:00:00Z",
        m15_ledger_head=head,
    )


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


class TestConstants:
    def test_pre04_codes_pinned(self) -> None:
        assert F_PRE_04_CEDAR_UNSIGNED == "F-PRE-04.cedar_policy_unsigned"
        assert F_PRE_04_LEDGER_MISMATCH == "F-PRE-04.cedar_policy_ledger_mismatch"

    def test_pre17_code_pinned(self) -> None:
        assert F_PRE_17_CEDAR_COMPILE_ERROR == "F-PRE-17.cedar_policy_compile_error"

    def test_cedar_failure_codes_pinned(self) -> None:
        assert F_CEDAR_ORG_ISOLATION_DENY == "F-CEDAR-01.org_isolation_deny"
        assert F_CEDAR_BYOK_KEY_SCOPE_DENY == "F-CEDAR-02.byok_key_scope_deny"
        assert F_CEDAR_CROSS_ORG_DENY == "F-CEDAR-03.cross_org_dossier_deny"
        assert F_CEDAR_UNKNOWN_POLICY == "F-CEDAR-04.unknown_policy"

    def test_known_policy_names(self) -> None:
        assert KNOWN_POLICY_NAMES == frozenset(
            {"org_isolation", "byok_key_scope", "cross_org_dossier_reference"}
        )

    def test_valid_tags(self) -> None:
        assert VALID_TAGS == frozenset({"DOC_SOURCED", "USER_DATA", "UNSOURCED"})


# ---------------------------------------------------------------------------
# Entity shapes
# ---------------------------------------------------------------------------


class TestEntityShapes:
    def test_session_entity_frozen_kw_only(self) -> None:
        s = _session()
        assert dataclasses.is_dataclass(s)
        with pytest.raises(dataclasses.FrozenInstanceError):
            s.org_slug = "other"  # type: ignore[misc]
        with pytest.raises(TypeError):
            SessionEntity(  # type: ignore[call-arg]
                "sess-1", "org", "h", "k", "2026-04-19T00:00:00Z"
            )

    def test_vault_path_entity_frozen_kw_only(self) -> None:
        v = _vault_path()
        assert dataclasses.is_dataclass(v)
        with pytest.raises(dataclasses.FrozenInstanceError):
            v.is_shared = True  # type: ignore[misc]

    def test_claim_entity_frozen_kw_only(self) -> None:
        c = _claim()
        assert dataclasses.is_dataclass(c)
        with pytest.raises(dataclasses.FrozenInstanceError):
            c.cross_org_dossier = True  # type: ignore[misc]

    def test_key_entity_frozen_kw_only(self) -> None:
        k = _key()
        assert dataclasses.is_dataclass(k)
        with pytest.raises(dataclasses.FrozenInstanceError):
            k.bound_org_slug = "other"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# CedarPolicy + CedarDecision shapes
# ---------------------------------------------------------------------------


class TestCedarPolicyShape:
    def test_policy_frozen_kw_only(self) -> None:
        p = _policy()
        assert dataclasses.is_dataclass(p)
        with pytest.raises(dataclasses.FrozenInstanceError):
            p.text = "other"  # type: ignore[misc]


class TestCedarDecisionShape:
    def test_decision_frozen_kw_only(self) -> None:
        d = CedarDecision(
            allow=True, policy_name="org_isolation", failure_code=None, reason="ok"
        )
        assert dataclasses.is_dataclass(d)
        with pytest.raises(dataclasses.FrozenInstanceError):
            d.allow = False  # type: ignore[misc]


# ---------------------------------------------------------------------------
# compile_cedar_policy
# ---------------------------------------------------------------------------


class TestCompileCedarPolicy:
    def test_happy_permit(self) -> None:
        ok, detail = compile_cedar_policy(_policy())
        assert ok is True
        assert detail == ""

    def test_happy_forbid(self) -> None:
        ok, detail = compile_cedar_policy(
            _policy(text="forbid(principal, action, resource);")
        )
        assert ok is True

    def test_unknown_policy_name(self) -> None:
        ok, detail = compile_cedar_policy(_policy(name="bogus_policy"))
        assert ok is False
        assert "unknown policy name" in detail

    def test_empty_text(self) -> None:
        ok, detail = compile_cedar_policy(_policy(text="   "))
        assert ok is False
        assert "empty" in detail

    def test_no_effect_keyword(self) -> None:
        ok, detail = compile_cedar_policy(
            _policy(text="when(principal == Session::sess-1);")
        )
        assert ok is False
        assert "permit" in detail and "forbid" in detail

    def test_non_policy_input_rejected(self) -> None:
        ok, detail = compile_cedar_policy("not a policy")  # type: ignore[arg-type]
        assert ok is False
        assert "CedarPolicy" in detail


# ---------------------------------------------------------------------------
# verify_cedar_policy_signed
# ---------------------------------------------------------------------------


class TestVerifyCedarPolicySigned:
    def test_happy_with_verifier(self) -> None:
        result = verify_cedar_policy_signed(
            _policy(),
            expected_ledger_head="h" * 128,
            signature_verifier=lambda p: True,
        )
        assert result is None

    def test_unsigned_returns_unsigned_code(self) -> None:
        result = verify_cedar_policy_signed(
            _policy(sig=b""),
            expected_ledger_head="h" * 128,
            signature_verifier=lambda p: True,
        )
        assert result == F_PRE_04_CEDAR_UNSIGNED

    def test_none_verifier_raises(self) -> None:
        with pytest.raises(TypeError) as excinfo:
            verify_cedar_policy_signed(
                _policy(),
                expected_ledger_head="h" * 128,
                signature_verifier=None,
            )
        assert "signature_verifier is required" in str(excinfo.value)

    def test_signature_verifier_returns_false(self) -> None:
        result = verify_cedar_policy_signed(
            _policy(),
            expected_ledger_head="h" * 128,
            signature_verifier=lambda p: False,
        )
        assert result == F_PRE_04_CEDAR_UNSIGNED

    def test_signature_verifier_returns_true(self) -> None:
        result = verify_cedar_policy_signed(
            _policy(),
            expected_ledger_head="h" * 128,
            signature_verifier=lambda p: True,
        )
        assert result is None

    def test_ledger_head_mismatch(self) -> None:
        result = verify_cedar_policy_signed(
            _policy(head="h" * 128),
            expected_ledger_head="z" * 128,
            signature_verifier=lambda p: True,
        )
        assert result == F_PRE_04_LEDGER_MISMATCH

    def test_non_policy_input_raises(self) -> None:
        with pytest.raises(TypeError):
            verify_cedar_policy_signed(
                "bogus",  # type: ignore[arg-type]
                expected_ledger_head="h" * 128,
                signature_verifier=lambda p: True,
            )

    def test_non_callable_verifier_raises(self) -> None:
        with pytest.raises(TypeError):
            verify_cedar_policy_signed(
                _policy(),
                expected_ledger_head="h" * 128,
                signature_verifier="not callable",  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# evaluate_org_isolation
# ---------------------------------------------------------------------------


class TestEvaluateOrgIsolation:
    def test_same_org_allow(self) -> None:
        d = evaluate_org_isolation(
            session=_session("orgA"), vault_path=_vault_path(org_slug_hint="orgA")
        )
        assert d.allow is True
        assert d.failure_code is None
        assert d.policy_name == "org_isolation"

    def test_shared_vault_allow(self) -> None:
        d = evaluate_org_isolation(
            session=_session("orgA"),
            vault_path=_vault_path(org_slug_hint="orgB", is_shared=True),
        )
        assert d.allow is True
        assert d.failure_code is None
        assert "shared" in d.reason

    def test_different_org_deny(self) -> None:
        d = evaluate_org_isolation(
            session=_session("orgA"), vault_path=_vault_path(org_slug_hint="orgB")
        )
        assert d.allow is False
        assert d.failure_code == F_CEDAR_ORG_ISOLATION_DENY
        assert "orgA" in d.reason and "orgB" in d.reason

    def test_non_session_raises(self) -> None:
        with pytest.raises(TypeError):
            evaluate_org_isolation(
                session="bogus",  # type: ignore[arg-type]
                vault_path=_vault_path(),
            )

    def test_non_vault_path_raises(self) -> None:
        with pytest.raises(TypeError):
            evaluate_org_isolation(
                session=_session(),
                vault_path="bogus",  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# evaluate_byok_key_scope
# ---------------------------------------------------------------------------


class TestEvaluateByokKeyScope:
    def test_same_org_allow(self) -> None:
        d = evaluate_byok_key_scope(
            session=_session("orgA"), key=_key(bound="orgA")
        )
        assert d.allow is True
        assert d.failure_code is None
        assert d.policy_name == "byok_key_scope"

    def test_different_org_deny(self) -> None:
        d = evaluate_byok_key_scope(
            session=_session("orgA"), key=_key(bound="orgB")
        )
        assert d.allow is False
        assert d.failure_code == F_CEDAR_BYOK_KEY_SCOPE_DENY
        assert "orgA" in d.reason and "orgB" in d.reason

    def test_non_session_raises(self) -> None:
        with pytest.raises(TypeError):
            evaluate_byok_key_scope(
                session="bogus",  # type: ignore[arg-type]
                key=_key(),
            )

    def test_non_key_raises(self) -> None:
        with pytest.raises(TypeError):
            evaluate_byok_key_scope(
                session=_session(),
                key="bogus",  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# evaluate_cross_org_dossier
# ---------------------------------------------------------------------------


class TestEvaluateCrossOrgDossier:
    def test_same_org_allow(self) -> None:
        d = evaluate_cross_org_dossier(
            session=_session(),
            claim=_claim(cross=False),
            operator_confirmation_present=False,
        )
        assert d.allow is True
        assert d.failure_code is None

    def test_cross_org_with_confirmation_allow(self) -> None:
        d = evaluate_cross_org_dossier(
            session=_session(),
            claim=_claim(cross=True),
            operator_confirmation_present=True,
        )
        assert d.allow is True
        assert d.failure_code is None

    def test_cross_org_without_confirmation_deny(self) -> None:
        d = evaluate_cross_org_dossier(
            session=_session(),
            claim=_claim(cross=True),
            operator_confirmation_present=False,
        )
        assert d.allow is False
        assert d.failure_code == F_CEDAR_CROSS_ORG_DENY

    def test_invalid_tag_raises(self) -> None:
        with pytest.raises(ValueError):
            evaluate_cross_org_dossier(
                session=_session(),
                claim=_claim(tag="BOGUS"),
                operator_confirmation_present=True,
            )

    def test_non_session_raises(self) -> None:
        with pytest.raises(TypeError):
            evaluate_cross_org_dossier(
                session="bogus",  # type: ignore[arg-type]
                claim=_claim(),
                operator_confirmation_present=True,
            )

    def test_non_claim_raises(self) -> None:
        with pytest.raises(TypeError):
            evaluate_cross_org_dossier(
                session=_session(),
                claim="bogus",  # type: ignore[arg-type]
                operator_confirmation_present=True,
            )


# ---------------------------------------------------------------------------
# evaluate (top-level dispatcher)
# ---------------------------------------------------------------------------


class TestEvaluateDispatcher:
    def test_org_isolation_dispatch(self) -> None:
        d = evaluate(
            policy_name="org_isolation",
            session=_session("orgA"),
            vault_path=_vault_path(org_slug_hint="orgA"),
        )
        assert d.allow is True
        assert d.policy_name == "org_isolation"

    def test_byok_key_scope_dispatch(self) -> None:
        d = evaluate(
            policy_name="byok_key_scope",
            session=_session("orgA"),
            key=_key(bound="orgA"),
        )
        assert d.allow is True
        assert d.policy_name == "byok_key_scope"

    def test_cross_org_dossier_dispatch(self) -> None:
        d = evaluate(
            policy_name="cross_org_dossier_reference",
            session=_session(),
            claim=_claim(cross=True),
            operator_confirmation_present=True,
        )
        assert d.allow is True
        assert d.policy_name == "cross_org_dossier_reference"

    def test_unknown_policy_fail_closed(self) -> None:
        d = evaluate(policy_name="bogus_policy", session=_session())
        assert d.allow is False
        assert d.failure_code == F_CEDAR_UNKNOWN_POLICY
        assert d.policy_name == "bogus_policy"

    def test_org_isolation_missing_vault_path_raises(self) -> None:
        with pytest.raises(ValueError):
            evaluate(policy_name="org_isolation", session=_session())

    def test_byok_key_scope_missing_key_raises(self) -> None:
        with pytest.raises(ValueError):
            evaluate(policy_name="byok_key_scope", session=_session())

    def test_cross_org_dossier_missing_claim_raises(self) -> None:
        with pytest.raises(ValueError):
            evaluate(
                policy_name="cross_org_dossier_reference",
                session=_session(),
            )

    def test_non_str_policy_name_raises(self) -> None:
        with pytest.raises(TypeError):
            evaluate(policy_name=123, session=_session())  # type: ignore[arg-type]
