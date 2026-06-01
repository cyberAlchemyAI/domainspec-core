"""Unit tests for F-EXTRACTOR-AWARD-SIGNATURE-INVALID (PRE-AWARD_INGEST, P0).

Per architecture v7.0.4 §5.3.
"""

from __future__ import annotations

from pipeline.logician.gates.f_extractor_award_signature_invalid import (
    F_EXTRACTOR_AWARD_SIGNATURE_INVALID,
    F_EXTRACTOR_AWARD_SIGNATURE_INVALID_AWARD,
    F_EXTRACTOR_AWARD_SIGNATURE_INVALID_PROPOSAL,
    AwardSignatureLeg,
    check_extractor_award_signature_invalid,
)


def _accept_all(message: bytes, signature: bytes, public_key: bytes) -> bool:
    return True


def _reject_all(message: bytes, signature: bytes, public_key: bytes) -> bool:
    return False


def _selective(
    accepted_pubkeys: set[bytes],
):
    def _verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
        return public_key in accepted_pubkeys
    return _verify


def _proposal_leg(unsigned: bool = False) -> AwardSignatureLeg:
    return AwardSignatureLeg(
        signature=b"prop-sig",
        message_bytes=b"prop-msg",
        public_key=b"prop-pub",
        unsigned_with_attestation=unsigned,
    )


def _award_leg(unsigned: bool = False) -> AwardSignatureLeg:
    return AwardSignatureLeg(
        signature=b"award-sig",
        message_bytes=b"award-msg",
        public_key=b"award-pub",
        unsigned_with_attestation=unsigned,
    )


def test_failure_code_constants() -> None:
    assert F_EXTRACTOR_AWARD_SIGNATURE_INVALID == "F-EXTRACTOR-AWARD-SIGNATURE-INVALID"
    assert F_EXTRACTOR_AWARD_SIGNATURE_INVALID_PROPOSAL == (
        "F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal"
    )
    assert F_EXTRACTOR_AWARD_SIGNATURE_INVALID_AWARD == (
        "F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award"
    )


def test_both_legs_verify_passes() -> None:
    r = check_extractor_award_signature_invalid(
        proposal_leg=_proposal_leg(),
        award_leg=_award_leg(),
        signature_verify=_accept_all,
    )
    assert r.success is True
    assert r.proposal_verified is True
    assert r.award_verified is True
    assert r.award_unsigned_attested is False


def test_proposal_signature_invalid_fails_with_proposal_subcode() -> None:
    r = check_extractor_award_signature_invalid(
        proposal_leg=_proposal_leg(),
        award_leg=_award_leg(),
        signature_verify=_reject_all,
    )
    assert r.success is False
    assert r.failure_code == F_EXTRACTOR_AWARD_SIGNATURE_INVALID_PROPOSAL
    assert r.proposal_verified is False


def test_proposal_attestation_forbidden_fails() -> None:
    # Proposal leg cannot use unsigned-with-attestation per §4.5 discipline
    r = check_extractor_award_signature_invalid(
        proposal_leg=_proposal_leg(unsigned=True),
        award_leg=_award_leg(),
        signature_verify=_accept_all,
    )
    assert r.success is False
    assert r.failure_code == F_EXTRACTOR_AWARD_SIGNATURE_INVALID_PROPOSAL
    assert "may not use unsigned_with_attestation" in r.detail


def test_award_unsigned_attestation_passes_after_proposal_verifies() -> None:
    r = check_extractor_award_signature_invalid(
        proposal_leg=_proposal_leg(),
        award_leg=_award_leg(unsigned=True),
        signature_verify=_selective({b"prop-pub"}),
    )
    assert r.success is True
    assert r.proposal_verified is True
    assert r.award_verified is False
    assert r.award_unsigned_attested is True


def test_award_signature_invalid_fails_with_award_subcode() -> None:
    # Proposal verifies but award does not.
    r = check_extractor_award_signature_invalid(
        proposal_leg=_proposal_leg(),
        award_leg=_award_leg(),
        signature_verify=_selective({b"prop-pub"}),
    )
    assert r.success is False
    assert r.failure_code == F_EXTRACTOR_AWARD_SIGNATURE_INVALID_AWARD
    assert r.proposal_verified is True
    assert r.award_verified is False


def test_signature_verify_raising_treated_as_failure() -> None:
    def raising_verify(*_args: object, **_kwargs: object) -> bool:
        raise RuntimeError("verifier blew up")

    r = check_extractor_award_signature_invalid(
        proposal_leg=_proposal_leg(),
        award_leg=_award_leg(),
        signature_verify=raising_verify,
    )
    assert r.success is False
    assert r.failure_code == F_EXTRACTOR_AWARD_SIGNATURE_INVALID_PROPOSAL
    assert "RuntimeError" in r.detail


def test_signature_verify_returning_truthy_non_bool_fails() -> None:
    # Gate uses strict ``is True`` per Protocol contract.
    def truthy_non_bool(*_args: object, **_kwargs: object) -> bool:
        return 1  # type: ignore[return-value]

    r = check_extractor_award_signature_invalid(
        proposal_leg=_proposal_leg(),
        award_leg=_award_leg(),
        signature_verify=truthy_non_bool,
    )
    assert r.success is False
    assert r.failure_code == F_EXTRACTOR_AWARD_SIGNATURE_INVALID_PROPOSAL


def test_award_verifier_called_with_award_inputs() -> None:
    captured: list[tuple[bytes, bytes, bytes]] = []

    def capturing(message: bytes, signature: bytes, public_key: bytes) -> bool:
        captured.append((message, signature, public_key))
        return True

    check_extractor_award_signature_invalid(
        proposal_leg=_proposal_leg(),
        award_leg=_award_leg(),
        signature_verify=capturing,
    )
    # Two calls expected — proposal first, then award.
    assert captured[0] == (b"prop-msg", b"prop-sig", b"prop-pub")
    assert captured[1] == (b"award-msg", b"award-sig", b"award-pub")
