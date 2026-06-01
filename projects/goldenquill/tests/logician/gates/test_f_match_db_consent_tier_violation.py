"""Unit tests for F-MATCH-DB-CONSENT-TIER-VIOLATION (PRE-write, P1).

Per architecture v7.0.5 §5.5.
"""

from __future__ import annotations

from datetime import datetime, timezone

from pipeline.logician.gates.f_match_db_consent_tier_violation import (
    CONSENT_TIER_SIGNATURE_KIND,
    F_MATCH_DB_CONSENT_TIER_VIOLATION,
    PERMITTED_CONSENT_TIERS,
    check_match_db_consent_tier_violation,
)


def _signature_row() -> dict:
    return {
        "kind": CONSENT_TIER_SIGNATURE_KIND,
        "operator_key_id": "ed25519:abc",
        "signed_at_utc": datetime.now(timezone.utc).isoformat(),
        "reason": "operator opted-in to broader sharing",
    }


def test_failure_code_constant() -> None:
    assert F_MATCH_DB_CONSENT_TIER_VIOLATION == "F-MATCH-DB-CONSENT-TIER-VIOLATION"


def test_unchanged_tier_passes() -> None:
    r = check_match_db_consent_tier_violation(
        prior_entry={"consent_tier": "my_eyes_only"},
        new_entry={"consent_tier": "my_eyes_only"},
        audit_chain=[],
    )
    assert r.success is True


def test_tier_change_with_signature_passes() -> None:
    r = check_match_db_consent_tier_violation(
        prior_entry={"consent_tier": "my_eyes_only"},
        new_entry={"consent_tier": "matchable_to_opportunities"},
        audit_chain=[_signature_row()],
    )
    assert r.success is True


def test_tier_change_without_signature_fails() -> None:
    r = check_match_db_consent_tier_violation(
        prior_entry={"consent_tier": "my_eyes_only"},
        new_entry={"consent_tier": "composable_with_others"},
        audit_chain=[],
    )
    assert r.success is False
    assert r.failure_code == F_MATCH_DB_CONSENT_TIER_VIOLATION


def test_tier_change_with_unrelated_audit_row_fails() -> None:
    # Audit row of a different kind doesn't satisfy the consent-tier
    # mutation requirement
    other_row = {
        "kind": "operator_signature_per_match_action",
        "signed_at_utc": "2026-05-10T10:00:00Z",
    }
    r = check_match_db_consent_tier_violation(
        prior_entry={"consent_tier": "my_eyes_only"},
        new_entry={"consent_tier": "composable_with_others"},
        audit_chain=[other_row],
    )
    assert r.success is False
    assert r.failure_code == F_MATCH_DB_CONSENT_TIER_VIOLATION


def test_signature_with_empty_timestamp_fails() -> None:
    bad_sig = {
        "kind": CONSENT_TIER_SIGNATURE_KIND,
        "signed_at_utc": "   ",  # whitespace-only
    }
    r = check_match_db_consent_tier_violation(
        prior_entry={"consent_tier": "my_eyes_only"},
        new_entry={"consent_tier": "matchable_to_opportunities"},
        audit_chain=[bad_sig],
    )
    assert r.success is False


def test_new_entry_without_consent_tier_fails() -> None:
    r = check_match_db_consent_tier_violation(
        prior_entry=None,
        new_entry={"funder_doc_id": "x"},
        audit_chain=[_signature_row()],
    )
    assert r.success is False
    assert r.failure_code == F_MATCH_DB_CONSENT_TIER_VIOLATION


def test_new_entry_with_invalid_consent_tier_fails() -> None:
    r = check_match_db_consent_tier_violation(
        prior_entry=None,
        new_entry={"consent_tier": "shared_with_world"},
        audit_chain=[_signature_row()],
    )
    assert r.success is False
    assert r.failure_code == F_MATCH_DB_CONSENT_TIER_VIOLATION


def test_brand_new_entry_with_my_eyes_only_default_passes_without_sig() -> None:
    # New entry from None → my_eyes_only (default) is technically a tier change
    # (None → my_eyes_only) — operator signature still required to create the
    # entry. This is by design: no silent tier-set on entry creation.
    r = check_match_db_consent_tier_violation(
        prior_entry=None,
        new_entry={"consent_tier": "my_eyes_only"},
        audit_chain=[_signature_row()],
    )
    assert r.success is True


def test_permitted_tiers_constant() -> None:
    assert PERMITTED_CONSENT_TIERS == frozenset({
        "my_eyes_only",
        "matchable_to_opportunities",
        "composable_with_others",
    })


def test_signature_kind_constant() -> None:
    assert CONSENT_TIER_SIGNATURE_KIND == "operator_signature_per_consent_tier_change"
