"""F-AWARD-INGEST-ATTN-UNVERIFIED tests (M1 §7.1)."""

from __future__ import annotations

from pipeline.logician.gates.f_award_ingest_attn_unverified import (
    F_AWARD_INGEST_ATTN_UNVERIFIED,
    LEDGER_KIND_AWARD_INGEST_ATTESTATION,
    check_award_ingest_attn_unverified,
)


def _signed_ledger(grant_id: str, path: str, rationale: str) -> dict:
    return {
        "ledger_kind": LEDGER_KIND_AWARD_INGEST_ATTESTATION,
        "grant_id": grant_id,
        "award_doc_path": path,
        "attestation_rationale": rationale,
        "operator_key_id": "op1",
        "signed_at_utc": "2026-05-10T00:00:00Z",
    }


def test_failure_code_constant() -> None:
    assert F_AWARD_INGEST_ATTN_UNVERIFIED == "F-AWARD-INGEST-ATTN-UNVERIFIED"


def test_no_attestation_passes() -> None:
    r = check_award_ingest_attn_unverified(
        grant_id="G1",
        award_doc_path="/tmp/award.pdf",
        attest_unsigned_award_doc=False,
        rationale=None,
        ledger_entries=[],
    )
    assert r.success is True


def test_attestation_without_rationale_fails() -> None:
    r = check_award_ingest_attn_unverified(
        grant_id="G1",
        award_doc_path="/tmp/award.pdf",
        attest_unsigned_award_doc=True,
        rationale=None,
        ledger_entries=[],
    )
    assert r.success is False
    assert r.failure_code == F_AWARD_INGEST_ATTN_UNVERIFIED


def test_attestation_with_empty_rationale_fails() -> None:
    r = check_award_ingest_attn_unverified(
        grant_id="G1",
        award_doc_path="/tmp/award.pdf",
        attest_unsigned_award_doc=True,
        rationale="   ",
        ledger_entries=[],
    )
    assert r.success is False


def test_attestation_with_rationale_no_ledger_fails() -> None:
    r = check_award_ingest_attn_unverified(
        grant_id="G1",
        award_doc_path="/tmp/award.pdf",
        attest_unsigned_award_doc=True,
        rationale="funder publishes no signing keys",
        ledger_entries=[],
    )
    assert r.success is False
    assert r.failure_code == F_AWARD_INGEST_ATTN_UNVERIFIED


def test_attestation_with_signed_ledger_passes() -> None:
    rationale = "funder publishes no signing keys"
    r = check_award_ingest_attn_unverified(
        grant_id="G1",
        award_doc_path="/tmp/award.pdf",
        attest_unsigned_award_doc=True,
        rationale=rationale,
        ledger_entries=[
            _signed_ledger("G1", "/tmp/award.pdf", rationale)
        ],
    )
    assert r.success is True


def test_ledger_for_other_grant_does_not_authorize() -> None:
    rationale = "reason"
    r = check_award_ingest_attn_unverified(
        grant_id="G1",
        award_doc_path="/tmp/award.pdf",
        attest_unsigned_award_doc=True,
        rationale=rationale,
        ledger_entries=[
            _signed_ledger("G2", "/tmp/award.pdf", rationale)
        ],
    )
    assert r.success is False


def test_ledger_with_different_path_does_not_authorize() -> None:
    rationale = "reason"
    r = check_award_ingest_attn_unverified(
        grant_id="G1",
        award_doc_path="/tmp/award.pdf",
        attest_unsigned_award_doc=True,
        rationale=rationale,
        ledger_entries=[
            _signed_ledger("G1", "/tmp/other.pdf", rationale)
        ],
    )
    assert r.success is False
