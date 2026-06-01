"""F-KFR-LEGACY-ACCEPT-RE-ENABLED-UNSIGNED tests (M1 §2.6.3)."""

from __future__ import annotations

from pipeline.logician.canonicalization.legacy_migration import (
    LEGACY_ACCEPT_COMPLETED,
    LEGACY_ACCEPT_DISABLED,
    LEGACY_ACCEPT_ENABLED,
)
from pipeline.logician.gates.f_kfr_legacy_accept_re_enabled_unsigned import (
    F_KFR_LEGACY_ACCEPT_RE_ENABLED_UNSIGNED,
    LEDGER_KIND_LEGACY_RE_ENABLE,
    check_kfr_legacy_accept_re_enabled_unsigned,
)


def _signed_ledger_row(org_slug: str = "ex") -> dict:
    return {
        "ledger_kind": LEDGER_KIND_LEGACY_RE_ENABLE,
        "org_slug": org_slug,
        "operator_key_id": "op1",
        "signed_at_utc": "2026-05-10T00:00:00Z",
        "rationale": "operator-supplied reason",
    }


def test_failure_code_constant() -> None:
    assert (
        F_KFR_LEGACY_ACCEPT_RE_ENABLED_UNSIGNED
        == "F-KFR-LEGACY-ACCEPT-RE-ENABLED-UNSIGNED"
    )


def test_no_transition_passes() -> None:
    r = check_kfr_legacy_accept_re_enabled_unsigned(
        org_slug="ex",
        previous_mode=LEGACY_ACCEPT_DISABLED,
        new_mode=LEGACY_ACCEPT_DISABLED,
        ledger_entries=[],
    )
    assert r.success is True


def test_disable_to_enable_without_signed_ledger_fails() -> None:
    r = check_kfr_legacy_accept_re_enabled_unsigned(
        org_slug="ex",
        previous_mode=LEGACY_ACCEPT_DISABLED,
        new_mode=LEGACY_ACCEPT_ENABLED,
        ledger_entries=[],
    )
    assert r.success is False
    assert r.failure_code == F_KFR_LEGACY_ACCEPT_RE_ENABLED_UNSIGNED


def test_completed_to_enable_without_signed_ledger_fails() -> None:
    r = check_kfr_legacy_accept_re_enabled_unsigned(
        org_slug="ex",
        previous_mode=LEGACY_ACCEPT_COMPLETED,
        new_mode=LEGACY_ACCEPT_ENABLED,
        ledger_entries=[],
    )
    assert r.success is False
    assert r.failure_code == F_KFR_LEGACY_ACCEPT_RE_ENABLED_UNSIGNED


def test_disable_to_enable_with_signed_ledger_passes() -> None:
    r = check_kfr_legacy_accept_re_enabled_unsigned(
        org_slug="ex",
        previous_mode=LEGACY_ACCEPT_DISABLED,
        new_mode=LEGACY_ACCEPT_ENABLED,
        ledger_entries=[_signed_ledger_row("ex")],
    )
    assert r.success is True


def test_signed_ledger_for_other_org_does_not_authorize() -> None:
    r = check_kfr_legacy_accept_re_enabled_unsigned(
        org_slug="ex",
        previous_mode=LEGACY_ACCEPT_DISABLED,
        new_mode=LEGACY_ACCEPT_ENABLED,
        ledger_entries=[_signed_ledger_row("other")],
    )
    assert r.success is False


def test_unsigned_ledger_row_does_not_authorize() -> None:
    bad_row = _signed_ledger_row("ex")
    bad_row["signed_at_utc"] = ""
    r = check_kfr_legacy_accept_re_enabled_unsigned(
        org_slug="ex",
        previous_mode=LEGACY_ACCEPT_DISABLED,
        new_mode=LEGACY_ACCEPT_ENABLED,
        ledger_entries=[bad_row],
    )
    assert r.success is False


def test_empty_rationale_does_not_authorize() -> None:
    bad_row = _signed_ledger_row("ex")
    bad_row["rationale"] = ""
    r = check_kfr_legacy_accept_re_enabled_unsigned(
        org_slug="ex",
        previous_mode=LEGACY_ACCEPT_DISABLED,
        new_mode=LEGACY_ACCEPT_ENABLED,
        ledger_entries=[bad_row],
    )
    assert r.success is False


def test_transition_not_to_enable_passes() -> None:
    r = check_kfr_legacy_accept_re_enabled_unsigned(
        org_slug="ex",
        previous_mode=LEGACY_ACCEPT_ENABLED,
        new_mode=LEGACY_ACCEPT_COMPLETED,
        ledger_entries=[],
    )
    assert r.success is True
