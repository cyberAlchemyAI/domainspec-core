"""§11 Intake — module-structure tests.

Per Blueprint §11 v1 LOCKED 2026-05-10 row 185 + WS-E Code phase done-definition.

These structural tests preserve the LOCK-ceremony invariants from
``skeleton_tests.py`` that are still load-bearing post-Code-phase: the
three-mode dispatcher, frozen kw_only dataclasses, and gate-predicate
import surface. The Code-phase-specific assertion that predicates raise
``NotImplementedError`` is deliberately NOT present here — predicates now
have full bodies and are exercised by ``test_gates.py`` /
``test_*_ingest.py``.
"""

from __future__ import annotations

from dataclasses import is_dataclass

import pytest

from pipeline.orchestrator.seats.intake import (
    GateResult,
    IntakeAwardInput,
    IntakeBulkInput,
    IntakeIncrementalInput,
    IntakeState,
    PendingFact,
    ProposalCommitment,
    f_extractor_award_signature_invalid_award,
    f_extractor_award_signature_invalid_proposal,
    f_extractor_fabrication,
    f_intake_config_signature_invalid,
    f_intake_embedding_endpoint_invalid,
    f_intake_embedding_ns_mismatch,
    f_intake_input_missing,
    f_intake_org_cross_ref,
    f_intake_queue_integrity_post_write,
    f_intake_queue_integrity_pre_run,
    f_intake_unsupported_format,
    f_intake_watcher_toctou,
    get_mode_handler_name,
    list_registered_modes,
)


def test_three_modes_register_in_dispatcher() -> None:
    """Per §11.13.1: exactly three modes registered, no fourth leak."""
    modes = list_registered_modes()
    assert len(modes) == 3
    assert set(modes) == {"BULK_INGEST", "INCREMENTAL_INGEST", "AWARD_INGEST"}


@pytest.mark.parametrize(
    "mode,handler",
    [
        ("BULK_INGEST", "bulk_ingest"),
        ("INCREMENTAL_INGEST", "incremental_ingest"),
        ("AWARD_INGEST", "award_ingest"),
    ],
)
def test_mode_handler_lookup(mode: str, handler: str) -> None:
    assert get_mode_handler_name(mode) == handler  # type: ignore[arg-type]


def test_mode_handler_unknown_raises() -> None:
    with pytest.raises(ValueError, match="Unknown Intake mode"):
        get_mode_handler_name("MIGRATION_BULK_INGEST")  # type: ignore[arg-type]


def test_intake_bulk_input_is_frozen_kw_only() -> None:
    assert is_dataclass(IntakeBulkInput)
    sample = IntakeBulkInput(
        run_id="t", org_slug="o",
        inbox_dir="orgs/o/intake/inbox/",
    )
    with pytest.raises(Exception):
        sample.org_slug = "other"  # type: ignore[misc]


def test_intake_incremental_input_is_frozen_kw_only() -> None:
    assert is_dataclass(IntakeIncrementalInput)
    sample = IntakeIncrementalInput(
        run_id="t", org_slug="o",
        doc_path="orgs/o/intake/inbox/doc.pdf",
        trigger="operator_explicit",
    )
    with pytest.raises(Exception):
        sample.org_slug = "other"  # type: ignore[misc]


def test_intake_award_input_is_frozen_kw_only_default_attestation_false() -> None:
    assert is_dataclass(IntakeAwardInput)
    sample = IntakeAwardInput(
        run_id="t", org_slug="o", grant_id="g",
        submission_artifact_ref="orgs/o/vault/grants/g/submission/draft_1.md",
        award_doc_path="orgs/o/vault/grants/g/award/award.pdf",
    )
    assert sample.mode == "AWARD_INGEST"
    assert sample.award_doc_unsigned_attestation is False
    with pytest.raises(Exception):
        sample.grant_id = "other"  # type: ignore[misc]


def test_pending_fact_proposal_commitment_state_are_dataclasses() -> None:
    assert is_dataclass(PendingFact)
    assert is_dataclass(ProposalCommitment)
    assert is_dataclass(IntakeState)


def test_v1_gate_codes_resolve_to_callables() -> None:
    for predicate in (
        f_extractor_fabrication,
        f_extractor_award_signature_invalid_proposal,
        f_extractor_award_signature_invalid_award,
        f_intake_org_cross_ref,
        f_intake_input_missing,
        f_intake_unsupported_format,
        f_intake_embedding_ns_mismatch,
        f_intake_config_signature_invalid,
        f_intake_embedding_endpoint_invalid,
        f_intake_watcher_toctou,
        f_intake_queue_integrity_pre_run,
        f_intake_queue_integrity_post_write,
    ):
        assert callable(predicate)


def test_gate_result_factories() -> None:
    p = GateResult.PASS()
    assert p.passed is True
    assert p.code is None
    f = GateResult.FAIL(code="X", sub_tag=".y", detail="z")
    assert f.passed is False
    assert f.code == "X"
    assert f.sub_tag == ".y"
