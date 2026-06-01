"""Tests for v0.2 wiring of F-LOGICIAN-FABRICATED-ORG into
``pipeline.logician.post_gate.run_post_gate_skeleton``.

Two-axis matrix:
  - draft_text + project_context supplied vs absent (backward-compat axis)
  - clean draft vs fabricated-org draft (gate-decision axis)

Plus interaction tests: F-POST-10 / F-POST-11 / F-LOGICIAN-FABRICATED-ORG
combinations to confirm all three codes coexist in `failure_codes`.

Backward-compat invariant: when `draft_text` or `project_context` is None,
the gate must NOT run and `fabricated_org_result` must remain None — so
existing callers that don't yet thread the v0.2 inputs see identical
Round-2-floor behaviour.

Real spaCy + en_core_web_sm are required; tests are auto-skipped when
the model is unavailable.
"""

from __future__ import annotations

from typing import Any

import pytest

from pipeline.logician.claim_evidence import ClaimEntry, SourceRef, compute_claim_id
from pipeline.logician.post_gate import (
    F_POST_10,
    F_POST_11,
    PostGateResult,
    run_post_gate_skeleton,
)
from pipeline.logician.gates.f_logician_fabricated_org import (
    F_LOGICIAN_FABRICATED_ORG,
)


def _spacy_available() -> bool:
    try:
        import spacy
        spacy.load("en_core_web_sm")
        return True
    except Exception:  # noqa: BLE001
        return False


# Skip this entire module when spaCy isn't ready — the only thing being
# tested here is the wire-in, which requires the gate's deps.
pytestmark = pytest.mark.skipif(
    not _spacy_available(),
    reason="en_core_web_sm not installed; run `python -m spacy download en_core_web_sm`",
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_DRAFT_HASH = "a" * 128
_RFA_HASH = "b" * 128
_RFA_URL_HASH = "c" * 64
_GENERATED_AT = "2026-05-08T12:00:00+00:00"


def _src() -> SourceRef:
    return SourceRef(
        source_kind="RFA",
        canonical_path="/m12/rfa.md",
        inode=12345,
        content_hash="d" * 128,
        grep_string="the quoted ±2 sentences from the RFA",
        window_size_sentences=2,
    )


def _sourced_claim(text: str = "FIT Farms LLC operates 20 acres.") -> ClaimEntry:
    return ClaimEntry(
        claim_id=compute_claim_id(
            draft_hash=_DRAFT_HASH, draft_offset=0, claim_text=text
        ),
        draft_offset=0,
        claim_text=text,
        tag="DOC_SOURCED",
        source_ref=_src(),
        verify_method="grep_windowed_pm2",
        verify_result="PASS",
        verify_detail="matched ±2 sentence window",
        rigor_breach_flag=False,
    )


def _base_kwargs(*, hard_block: int = 0) -> dict[str, Any]:
    return dict(
        draft_hash=_DRAFT_HASH,
        rfa_hash=_RFA_HASH,
        session_id="sess-r6-fab-org",
        org_slug="fit_farms",
        rfa_url_hash=_RFA_URL_HASH,
        claims=(_sourced_claim(),),
        rigor_breach_active=False,
        admin_risk_hard_block_count=hard_block,
        generated_at_utc=_GENERATED_AT,
    )


# ---------------------------------------------------------------------------
# Backward-compat axis — no draft_text/project_context
# ---------------------------------------------------------------------------

class TestBackwardCompat:
    """When v0.2 inputs are absent, behave exactly like Round-2 floor."""

    def test_no_v0_2_inputs_skips_gate(self) -> None:
        result = run_post_gate_skeleton(**_base_kwargs())
        assert isinstance(result, PostGateResult)
        assert result.success is True
        assert result.failure_codes == ()
        assert result.fabricated_org_result is None  # gate not invoked

    def test_only_draft_text_provided_skips_gate(self) -> None:
        # Missing project_context → gate must not run (avoid partial inputs)
        result = run_post_gate_skeleton(
            **_base_kwargs(),
            draft_text="In partnership with Imaginary Org.",
        )
        assert result.success is True
        assert result.fabricated_org_result is None
        assert F_LOGICIAN_FABRICATED_ORG not in result.failure_codes

    def test_only_project_context_provided_skips_gate(self) -> None:
        result = run_post_gate_skeleton(
            **_base_kwargs(),
            project_context={"applicant_name": "FIT Farms LLC"},
        )
        assert result.success is True
        assert result.fabricated_org_result is None
        assert F_LOGICIAN_FABRICATED_ORG not in result.failure_codes


# ---------------------------------------------------------------------------
# Gate-decision axis — both v0.2 inputs supplied
# ---------------------------------------------------------------------------

class TestGateInvoked:
    """When draft_text + project_context supplied, gate runs and surfaces verdict."""

    def test_clean_draft_passes(self) -> None:
        result = run_post_gate_skeleton(
            **_base_kwargs(),
            draft_text=(
                "FIT Farms LLC will lead the project in partnership with "
                "Penn State Extension."
            ),
            project_context={
                "applicant_name": "FIT Farms LLC",
                "partners": ["Penn State Extension"],
            },
        )
        assert result.success is True
        assert result.fabricated_org_result is not None
        assert result.fabricated_org_result.verdict == "PASS"
        assert F_LOGICIAN_FABRICATED_ORG not in result.failure_codes

    def test_fabricated_org_fails(self) -> None:
        result = run_post_gate_skeleton(
            **_base_kwargs(),
            draft_text=(
                "FIT Farms LLC will lead the project in partnership with "
                "Imaginary Institute of Soil Sciences."
            ),
            project_context={
                "applicant_name": "FIT Farms LLC",
                "partners": [],  # Imaginary Institute deliberately absent
            },
        )
        assert result.success is False
        assert result.fabricated_org_result is not None
        assert result.fabricated_org_result.verdict == "FAIL"
        assert F_LOGICIAN_FABRICATED_ORG in result.failure_codes
        # Existing codes are unaffected (no admin-risk, no unsourced)
        assert F_POST_10 not in result.failure_codes
        assert F_POST_11 not in result.failure_codes

    def test_rfa_issuer_threads_through(self) -> None:
        # When rfa_issuer is set, the funder is auto-allowed even if not
        # in PROJECT_CONTEXT partners.
        result = run_post_gate_skeleton(
            **_base_kwargs(),
            draft_text="Funded by USDA Rural Development under VAPG.",
            project_context={"applicant_name": "FIT Farms LLC"},
            rfa_issuer="USDA Rural Development",
        )
        assert result.success is True
        assert result.fabricated_org_result.verdict == "PASS"


# ---------------------------------------------------------------------------
# Interaction — multiple failure codes coexist
# ---------------------------------------------------------------------------

class TestInteraction:
    """F-POST-10 + F-LOGICIAN-FABRICATED-ORG both surface when both fire."""

    def test_admin_risk_plus_fabricated_org(self) -> None:
        # Use the same fabricated-org phrasing the standalone gate test
        # already proved spaCy reliably tags as ORG.
        result = run_post_gate_skeleton(
            **_base_kwargs(hard_block=2),  # F-POST-10 will fire
            draft_text=(
                "In partnership with Imaginary Institute of Soil Sciences "
                "we will proceed with the project."
            ),
            project_context={"applicant_name": "FIT Farms LLC", "partners": []},
        )
        assert result.success is False
        # Both codes present, ordering is: F-POST-10, then fabricated-org
        # (admin-risk is checked before the v0.2 gate per the existing
        # skeleton's check ordering).
        assert F_POST_10 in result.failure_codes
        assert F_LOGICIAN_FABRICATED_ORG in result.failure_codes
        assert result.hard_block_count == 2
        assert result.fabricated_org_result.verdict == "FAIL"


# ---------------------------------------------------------------------------
# Empty-draft edge case
# ---------------------------------------------------------------------------

class TestEdgeCases:

    def test_empty_draft_text_passes_gate(self) -> None:
        result = run_post_gate_skeleton(
            **_base_kwargs(),
            draft_text="",
            project_context={"applicant_name": "FIT Farms LLC"},
        )
        # Empty string + present project_context: gate runs and emits PASS
        # (per gate's empty-draft semantics)
        assert result.success is True
        assert result.fabricated_org_result is not None
        assert result.fabricated_org_result.verdict == "PASS"
