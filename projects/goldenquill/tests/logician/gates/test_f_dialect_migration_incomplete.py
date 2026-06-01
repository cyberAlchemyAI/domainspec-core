"""Unit tests for F-DIALECT-MIGRATION-INCOMPLETE.

Per §4 v2.x apolitical_dialect §4.X.6 (Cycle 1 fold-in FI-7b + Cycle 2
fold-ins C2-H-4 + C2-NEW-MED-2 + C2-NEW-HIGH-3 + C2-NEW-MED-4). LOCKED
2026-05-16T14:00:00Z; lock_history rows 236/249.
"""

from __future__ import annotations

import hashlib
from typing import Iterable

import pytest

from pipeline.logician.gates.f_dialect_migration_incomplete import (
    AUDIT_STATUS_CONFIRMED_AVOID_ALL,
    AUDIT_STATUS_CONFIRMED_PER_CLC,
    AdminRiskRegisterEntry,
    AuditDecisionRow,
    GATE_ID,
    MigrationIncompleteFinding,
    PRE_GATE_ORDER,
    check_predicate_body_deployed,
    run,
)


def _term_hash(term: str, severity: str) -> str:
    return hashlib.sha3_256(
        f"{term}\x00{severity}".encode("utf-8")
    ).hexdigest()


def _always_verify(**_kwargs) -> bool:
    return True


def _never_verify(**_kwargs) -> bool:
    return False


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


def test_gate_id() -> None:
    assert GATE_ID == "F-DIALECT-MIGRATION-INCOMPLETE"


def test_pre_gate_order_between_political_axis_and_match_null() -> None:
    """JD-C2-LOW-1: order 6.56, between F-DIALECT-POLITICAL-AXIS-LEAK at
    6.55 and F-CIC-CLC-MATCH-NULL at 6.6."""
    assert PRE_GATE_ORDER == 6.56


def test_audit_status_constants() -> None:
    assert AUDIT_STATUS_CONFIRMED_AVOID_ALL == "confirmed_avoid_all"
    assert AUDIT_STATUS_CONFIRMED_PER_CLC == "confirmed_per_clc"


# ---------------------------------------------------------------------------
# Empty register passes
# ---------------------------------------------------------------------------


def test_empty_register_passes() -> None:
    r = run(
        admin_risk_register_reader=lambda: iter([]),
        audit_decisions_reader=lambda: iter([]),
        signature_verifier=_always_verify,
    )
    assert r.passed is True
    assert r.findings == ()


# ---------------------------------------------------------------------------
# Term with populated per_clc_register passes
# ---------------------------------------------------------------------------


def test_populated_per_clc_register_passes() -> None:
    entries = [
        AdminRiskRegisterEntry(
            term="equity",
            severity="YELLOW",
            per_clc_register={"public_purpose_works": "OK", "catalytic_change": "PREFERRED"},
        ),
    ]
    r = run(
        admin_risk_register_reader=lambda: iter(entries),
        audit_decisions_reader=lambda: iter([]),
        signature_verifier=_always_verify,
    )
    assert r.passed is True


# ---------------------------------------------------------------------------
# .unaudited_term — no audit row
# ---------------------------------------------------------------------------


def test_unaudited_term_no_audit_row_caught() -> None:
    entries = [
        AdminRiskRegisterEntry(
            term="systemic",
            severity="YELLOW",
            per_clc_register={},
        ),
    ]
    r = run(
        admin_risk_register_reader=lambda: iter(entries),
        audit_decisions_reader=lambda: iter([]),
        signature_verifier=_always_verify,
    )
    assert r.passed is False
    assert any(
        f.subcode == f"{GATE_ID}.unaudited_term" for f in r.findings
    )


# ---------------------------------------------------------------------------
# .unaudited_term — audit row exists but status != confirmed_avoid_all
# ---------------------------------------------------------------------------


def test_audit_status_confirmed_per_clc_with_empty_register_fails() -> None:
    """C2-NEW-MED-2: confirmed_per_clc requires per_clc_register to actually
    be populated; empty per_clc_register with confirmed_per_clc status →
    .unaudited_term."""
    term = "marginalized"
    severity = "YELLOW"
    th = _term_hash(term, severity)
    entries = [
        AdminRiskRegisterEntry(term=term, severity=severity, per_clc_register={}),
    ]
    decisions = [
        AuditDecisionRow(
            term=term,
            term_hash=th,
            audit_status=AUDIT_STATUS_CONFIRMED_PER_CLC,
            operator_ed25519_signature_hex="00" * 64,
            operator_pubkey_ed25519_hex="00" * 32,
        ),
    ]
    r = run(
        admin_risk_register_reader=lambda: iter(entries),
        audit_decisions_reader=lambda: iter(decisions),
        signature_verifier=_always_verify,
    )
    assert r.passed is False
    assert any(
        f.subcode == f"{GATE_ID}.unaudited_term" for f in r.findings
    )


def test_audit_status_confirmed_avoid_all_with_signed_row_passes() -> None:
    """The happy path: empty per_clc_register + confirmed_avoid_all + signed."""
    term = "equity"
    severity = "RED"
    th = _term_hash(term, severity)
    entries = [
        AdminRiskRegisterEntry(term=term, severity=severity, per_clc_register={}),
    ]
    decisions = [
        AuditDecisionRow(
            term=term,
            term_hash=th,
            audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
            operator_ed25519_signature_hex="aa" * 64,
            operator_pubkey_ed25519_hex="bb" * 32,
        ),
    ]
    r = run(
        admin_risk_register_reader=lambda: iter(entries),
        audit_decisions_reader=lambda: iter(decisions),
        signature_verifier=_always_verify,
    )
    assert r.passed is True


# ---------------------------------------------------------------------------
# .per_term_signature_missing — audit row exists but signature absent/invalid
# ---------------------------------------------------------------------------


def test_per_term_signature_missing_caught() -> None:
    """C2-H-4: per-term Ed25519 required — missing signature trips."""
    term = "justice"
    severity = "YELLOW"
    th = _term_hash(term, severity)
    entries = [
        AdminRiskRegisterEntry(term=term, severity=severity, per_clc_register={}),
    ]
    decisions = [
        AuditDecisionRow(
            term=term,
            term_hash=th,
            audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
            operator_ed25519_signature_hex=None,
            operator_pubkey_ed25519_hex=None,
        ),
    ]
    r = run(
        admin_risk_register_reader=lambda: iter(entries),
        audit_decisions_reader=lambda: iter(decisions),
        signature_verifier=_always_verify,
    )
    assert r.passed is False
    assert any(
        f.subcode == f"{GATE_ID}.per_term_signature_missing"
        for f in r.findings
    )


def test_per_term_signature_verification_failure_caught() -> None:
    """C2-H-4: signature present but verifier rejects → same sub-tag."""
    term = "transformative"
    severity = "GREEN"
    th = _term_hash(term, severity)
    entries = [
        AdminRiskRegisterEntry(term=term, severity=severity, per_clc_register={}),
    ]
    decisions = [
        AuditDecisionRow(
            term=term,
            term_hash=th,
            audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
            operator_ed25519_signature_hex="cc" * 64,
            operator_pubkey_ed25519_hex="dd" * 32,
        ),
    ]
    r = run(
        admin_risk_register_reader=lambda: iter(entries),
        audit_decisions_reader=lambda: iter(decisions),
        signature_verifier=_never_verify,
    )
    assert r.passed is False
    assert any(
        f.subcode == f"{GATE_ID}.per_term_signature_missing"
        for f in r.findings
    )


def test_signature_verifier_exception_treated_as_failure() -> None:
    """C2-H-4 + defensive coding: a verifier that raises is treated as fail
    (NOT bubble the exception)."""
    def _exploding_verifier(**_kwargs) -> bool:
        raise RuntimeError("Ed25519 library exploded")

    term = "intersectional"
    severity = "RED"
    th = _term_hash(term, severity)
    entries = [
        AdminRiskRegisterEntry(term=term, severity=severity, per_clc_register={}),
    ]
    decisions = [
        AuditDecisionRow(
            term=term,
            term_hash=th,
            audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
            operator_ed25519_signature_hex="ee" * 64,
            operator_pubkey_ed25519_hex="ff" * 32,
        ),
    ]
    r = run(
        admin_risk_register_reader=lambda: iter(entries),
        audit_decisions_reader=lambda: iter(decisions),
        signature_verifier=_exploding_verifier,
    )
    assert r.passed is False
    assert any(
        f.subcode == f"{GATE_ID}.per_term_signature_missing"
        for f in r.findings
    )


# ---------------------------------------------------------------------------
# .audit_decisions_missing — file absent
# ---------------------------------------------------------------------------


def test_audit_decisions_missing_emits_clean_subtag() -> None:
    """C2-NEW-MED-4: try/except wrap → missing file → clean FAIL with
    .audit_decisions_missing instead of uncaught traceback."""
    def _missing_reader() -> Iterable[AuditDecisionRow]:
        raise FileNotFoundError(
            "admin_risk_register_audit_decisions.md not found"
        )

    entries = [
        AdminRiskRegisterEntry(term="equity", severity="RED", per_clc_register={}),
    ]
    r = run(
        admin_risk_register_reader=lambda: iter(entries),
        audit_decisions_reader=_missing_reader,
        signature_verifier=_always_verify,
    )
    assert r.passed is False
    # Expect both the file-missing sub-tag AND per-term unaudited sub-tags.
    subcodes = {f.subcode for f in r.findings}
    assert f"{GATE_ID}.audit_decisions_missing" in subcodes
    assert f"{GATE_ID}.unaudited_term" in subcodes


def test_audit_decisions_missing_with_no_register_entries_only_emits_missing() -> None:
    def _missing_reader() -> Iterable[AuditDecisionRow]:
        raise FileNotFoundError("audit file absent")

    r = run(
        admin_risk_register_reader=lambda: iter([]),
        audit_decisions_reader=_missing_reader,
        signature_verifier=_always_verify,
    )
    assert r.passed is False
    subcodes = {f.subcode for f in r.findings}
    assert subcodes == {f"{GATE_ID}.audit_decisions_missing"}


# ---------------------------------------------------------------------------
# C2-NEW-HIGH-3 — pre-LOCK predicate body deployment check
# ---------------------------------------------------------------------------


def test_predicate_body_deployed_returns_none_when_live() -> None:
    """The gate module itself is importable and `run` doesn't raise
    NotImplementedError on the empty-source smoke probe."""
    result = check_predicate_body_deployed()
    assert result is None


def test_predicate_body_deployed_detects_unimportable_module() -> None:
    result = check_predicate_body_deployed(
        module_dotted_path="pipeline.logician.gates.f_dialect_does_not_exist",
    )
    assert isinstance(result, MigrationIncompleteFinding)
    assert result.subcode == f"{GATE_ID}.predicate_body_not_deployed"


# ---------------------------------------------------------------------------
# Multiple terms — aggregated findings
# ---------------------------------------------------------------------------


def test_multiple_unaudited_terms_all_surface() -> None:
    """The gate doesn't short-circuit on the first finding — every unaudited
    term surfaces so the operator can fix the batch in one pass."""
    entries = [
        AdminRiskRegisterEntry(
            term=name, severity="YELLOW", per_clc_register={}
        )
        for name in ("equity", "justice", "systemic", "marginalized", "transformative")
    ]
    r = run(
        admin_risk_register_reader=lambda: iter(entries),
        audit_decisions_reader=lambda: iter([]),
        signature_verifier=_always_verify,
    )
    assert r.passed is False
    unaudited = [
        f for f in r.findings
        if f.subcode == f"{GATE_ID}.unaudited_term"
    ]
    assert len(unaudited) == 5
    # Each finding's term matches the entry name.
    found_terms = {f.term for f in unaudited}
    assert found_terms == {
        "equity", "justice", "systemic", "marginalized", "transformative"
    }


# ---------------------------------------------------------------------------
# Mixed — some terms migrated, some audited-avoid, some unaudited
# ---------------------------------------------------------------------------


def test_mixed_state_partial_pass() -> None:
    """Realistic operator state mid-audit: some terms fully migrated, some
    audited-AVOID-everywhere, some still unaudited. The gate fails closed
    but reports only the unaudited terms."""
    migrated_entry = AdminRiskRegisterEntry(
        term="public-private partnership",
        severity="GREEN",
        per_clc_register={"sponsorship_corporate": "PREFERRED"},
    )
    avoid_all_entry = AdminRiskRegisterEntry(
        term="equity", severity="RED", per_clc_register={}
    )
    unaudited_entry = AdminRiskRegisterEntry(
        term="systemic", severity="YELLOW", per_clc_register={}
    )
    avoid_all_decision = AuditDecisionRow(
        term="equity",
        term_hash=_term_hash("equity", "RED"),
        audit_status=AUDIT_STATUS_CONFIRMED_AVOID_ALL,
        operator_ed25519_signature_hex="aa" * 64,
        operator_pubkey_ed25519_hex="bb" * 32,
    )

    r = run(
        admin_risk_register_reader=lambda: iter(
            [migrated_entry, avoid_all_entry, unaudited_entry]
        ),
        audit_decisions_reader=lambda: iter([avoid_all_decision]),
        signature_verifier=_always_verify,
    )
    assert r.passed is False
    # Only the unaudited entry should appear in findings.
    assert len(r.findings) == 1
    assert r.findings[0].term == "systemic"
    assert r.findings[0].subcode == f"{GATE_ID}.unaudited_term"
