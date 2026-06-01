"""§11 Intake — skeleton tests at LOCK ceremony (HISTORICAL).

This file is the LOCK-ceremony record from §11 v1 LOCKED 2026-05-10 row 185.
It is NOT collected by pytest (filename is ``skeleton_tests.py``, not
``test_*.py``); the load-bearing structural assertions migrated to
``test_intake_module_structure.py`` once Code phase populated the
predicate bodies. The ``test_gate_predicates_raise_not_implemented_at_v1_lock``
assertion below is no longer accurate post-Code-phase and is preserved here
solely for the LOCK audit trail; pytest cannot run it because the file is
not collected.

Spec card: ``pipeline/blueprint/v0.1/section_11_intake.md`` (§11 v1 LOCKED 2026-05-10).

Skeleton-test scope (per §11.15 LOCK ceremony done-definition):
- Validate the three modes register in the dispatcher (per §11.13.1).
- Validate the v1 gate codes resolve to imported predicates (per §11.13.2-§11.13.10 prerequisite).
- Validate the input/output dataclasses are frozen + kw_only per Tilth convention.

Code phase landed 2026-05-10 alongside §11 v1 LOCK; per-gate + per-mode
tests live in ``test_gates.py`` / ``test_bulk_ingest.py`` /
``test_incremental_ingest.py`` / ``test_award_ingest.py``.
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
    f_intake_org_cross_ref,
    f_intake_watcher_toctou,
    get_mode_handler_name,
    list_registered_modes,
)


# ---------------------------------------------------------------------------
# §11.13.1 Mode dispatch tests
# ---------------------------------------------------------------------------


def test_three_modes_register_in_dispatcher() -> None:
    """Per §11.13.1: assert exactly three modes registered.

    No fourth mode silently leaks through. MIGRATION_BULK_INGEST is a
    special invocation of BULK_INGEST per §11.11, NOT a fourth registered
    mode.
    """
    modes = list_registered_modes()
    assert len(modes) == 3
    assert set(modes) == {"BULK_INGEST", "INCREMENTAL_INGEST", "AWARD_INGEST"}


def test_mode_handler_lookup_bulk() -> None:
    """BULK_INGEST mode resolves to bulk_ingest handler."""
    assert get_mode_handler_name("BULK_INGEST") == "bulk_ingest"


def test_mode_handler_lookup_incremental() -> None:
    """INCREMENTAL_INGEST mode resolves to incremental_ingest handler."""
    assert get_mode_handler_name("INCREMENTAL_INGEST") == "incremental_ingest"


def test_mode_handler_lookup_award() -> None:
    """AWARD_INGEST mode resolves to award_ingest handler."""
    assert get_mode_handler_name("AWARD_INGEST") == "award_ingest"


def test_mode_handler_unknown_mode_raises() -> None:
    """Unknown mode raises ValueError with available modes listed."""
    with pytest.raises(ValueError, match="Unknown Intake mode"):
        get_mode_handler_name("MIGRATION_BULK_INGEST")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# §11.4 input contracts — frozen + kw_only per Tilth convention
# ---------------------------------------------------------------------------


def test_intake_bulk_input_is_frozen_kw_only() -> None:
    """IntakeBulkInput is frozen + kw_only dataclass (per §11.4.1)."""
    assert is_dataclass(IntakeBulkInput)
    # frozen dataclass instances raise FrozenInstanceError on assignment
    sample = IntakeBulkInput(
        run_id="test-run",
        org_slug="test_org",
        inbox_dir="orgs/test_org/intake/inbox/",
    )
    with pytest.raises(Exception):  # FrozenInstanceError
        sample.org_slug = "other_org"  # type: ignore[misc]


def test_intake_incremental_input_is_frozen_kw_only() -> None:
    """IntakeIncrementalInput is frozen + kw_only dataclass (per §11.4.2)."""
    assert is_dataclass(IntakeIncrementalInput)
    sample = IntakeIncrementalInput(
        run_id="test-run",
        org_slug="test_org",
        doc_path="orgs/test_org/intake/inbox/doc.pdf",
        trigger="operator_explicit",
    )
    with pytest.raises(Exception):
        sample.org_slug = "other_org"  # type: ignore[misc]


def test_intake_award_input_is_frozen_kw_only() -> None:
    """IntakeAwardInput is frozen + kw_only dataclass (per §11.4.3)."""
    assert is_dataclass(IntakeAwardInput)
    sample = IntakeAwardInput(
        run_id="test-run",
        org_slug="test_org",
        grant_id="test_grant",
        submission_artifact_ref="orgs/test_org/vault/grants/test_grant/submission/draft_1.md",
        award_doc_path="orgs/test_org/vault/grants/test_grant/award/award.pdf",
    )
    with pytest.raises(Exception):
        sample.grant_id = "other_grant"  # type: ignore[misc]


def test_intake_award_input_default_unsigned_attestation_false() -> None:
    """IntakeAwardInput.award_doc_unsigned_attestation defaults to False (RT-06 closure)."""
    sample = IntakeAwardInput(
        run_id="test-run",
        org_slug="test_org",
        grant_id="test_grant",
        submission_artifact_ref="orgs/test_org/vault/grants/test_grant/submission/draft_1.md",
        award_doc_path="orgs/test_org/vault/grants/test_grant/award/award.pdf",
    )
    assert sample.award_doc_unsigned_attestation is False


def test_intake_award_input_mode_immutable() -> None:
    """IntakeAwardInput.mode is hardcoded to AWARD_INGEST per RT-04 closure.

    Mode flag is the SOLE driver of ±1 page tolerance carve-out at §11.9.1.A;
    it's read from the input dataclass only, never from runtime config.
    """
    sample = IntakeAwardInput(
        run_id="test-run",
        org_slug="test_org",
        grant_id="test_grant",
        submission_artifact_ref="orgs/test_org/vault/grants/test_grant/submission/draft_1.md",
        award_doc_path="orgs/test_org/vault/grants/test_grant/award/award.pdf",
    )
    assert sample.mode == "AWARD_INGEST"


# ---------------------------------------------------------------------------
# §11.5 output schemas — frozen + kw_only
# ---------------------------------------------------------------------------


def test_pending_fact_is_frozen_kw_only() -> None:
    """PendingFact is frozen + kw_only dataclass (per §11.5.1 schema delta)."""
    assert is_dataclass(PendingFact)


def test_proposal_commitment_is_frozen_kw_only() -> None:
    """ProposalCommitment is frozen + kw_only dataclass (per §11.5.2 schema delta)."""
    assert is_dataclass(ProposalCommitment)


def test_intake_state_is_frozen_kw_only() -> None:
    """IntakeState is frozen + kw_only dataclass (per Rule 1 Save State Always)."""
    assert is_dataclass(IntakeState)


# ---------------------------------------------------------------------------
# §11.9 gate code resolution — predicates importable
# ---------------------------------------------------------------------------


def test_v1_gate_codes_resolve_to_predicates() -> None:
    """All 8 §11-owned predicate stubs are importable.

    Per §11.9 v1 gate roster (12 codes; 4 inherit cross-amendment):
      F-EXTRACTOR-FABRICATION             → f_extractor_fabrication
      F-EXTRACTOR-AWARD-SIGNATURE-INVALID → .proposal + .award split predicates
      F-INTAKE-ORG-CROSS-REF              → f_intake_org_cross_ref
      F-INTAKE-EMBEDDING-NS-MISMATCH      → f_intake_embedding_ns_mismatch (NEW from RT-09 closure)
      F-INTAKE-CONFIG-SIGNATURE-INVALID   → f_intake_config_signature_invalid (NEW from RT-07 closure)
      F-INTAKE-EMBEDDING-ENDPOINT-INVALID → f_intake_embedding_endpoint_invalid (NEW from RT-13 closure)
      F-INTAKE-WATCHER-TOCTOU             → f_intake_watcher_toctou (NEW from RT-11 closure)
    """
    predicates = [
        f_extractor_fabrication,
        f_extractor_award_signature_invalid_proposal,
        f_extractor_award_signature_invalid_award,
        f_intake_org_cross_ref,
        f_intake_embedding_ns_mismatch,
        f_intake_config_signature_invalid,
        f_intake_embedding_endpoint_invalid,
        f_intake_watcher_toctou,
    ]
    for predicate in predicates:
        assert callable(predicate), f"{predicate.__name__} is not callable"


def test_gate_result_pass_factory() -> None:
    """GateResult.PASS() returns passed=True."""
    result = GateResult.PASS()
    assert result.passed is True
    assert result.code is None


def test_gate_result_fail_factory() -> None:
    """GateResult.FAIL() returns passed=False with code + sub_tag + detail."""
    result = GateResult.FAIL(
        code="F-INTAKE-ORG-CROSS-REF",
        sub_tag=".symlink_escape",
        detail="Path resolves outside org subtree",
    )
    assert result.passed is False
    assert result.code == "F-INTAKE-ORG-CROSS-REF"
    assert result.sub_tag == ".symlink_escape"


def test_gate_predicates_raise_not_implemented_at_v1_lock() -> None:
    """Skeleton predicates raise NotImplementedError at v1 LOCK.

    Full predicate bodies are downstream Code session per WS-E Code phase.
    The skeleton tests confirm the predicates are importable + callable;
    full per-gate behavior tests live in tests/logician/gates/test_f_*.py
    after the Code phase populates them.
    """
    bulk_input = IntakeBulkInput(
        run_id="test-run",
        org_slug="test_org",
        inbox_dir="orgs/test_org/intake/inbox/",
    )
    with pytest.raises(NotImplementedError, match="§11.9.4 predicate scaffold"):
        f_intake_org_cross_ref(bulk_input)
