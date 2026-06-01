"""Tests for v0.2 wiring of F-LOGICIAN-SPINE-DRIFT + F-LOGICIAN-FACT-DRIFT
into ``pipeline.logician.post_gate.run_post_gate_skeleton``.

Backward-compat invariants checked here:
- When spine inputs (spine_path / section_id / section_dialect) are not
  all supplied, the spine gate is NOT invoked (spine_drift_result stays None).
- When fact-drift inputs (kfr_path / grant_funding_period) are not both
  supplied, the fact gate is NOT invoked (fact_drift_result stays None).
- Both gates can fire independently in the same run.
- All v0.2 gates can coexist alongside F-POST-10 / F-POST-11 in the same
  failure_codes tuple.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from pipeline.logician.claim_evidence import ClaimEntry, SourceRef, compute_claim_id
from pipeline.logician.gates.f_logician_fact_drift import F_LOGICIAN_FACT_DRIFT
from pipeline.logician.gates.f_logician_spine_drift import F_LOGICIAN_SPINE_DRIFT
from pipeline.logician.post_gate import (
    F_POST_10,
    PostGateResult,
    run_post_gate_skeleton,
)


# --------------------------------------------------------------------------
# Common fixtures
# --------------------------------------------------------------------------

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


def _claim(text: str = "FIT Farms LLC operates the program.") -> ClaimEntry:
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
        verify_detail="matched",
        rigor_breach_flag=False,
    )


def _base_kwargs(*, hard_block: int = 0):
    return dict(
        draft_hash=_DRAFT_HASH,
        rfa_hash=_RFA_HASH,
        session_id="sess-v0_2-wire",
        org_slug="dogwood_school",
        rfa_url_hash=_RFA_URL_HASH,
        claims=(_claim(),),
        rigor_breach_active=False,
        admin_risk_hard_block_count=hard_block,
        generated_at_utc=_GENERATED_AT,
    )


_SPINE_YAML = """\
grant_id: vapg_fy26_dogwood
locked_at: 2026-05-08T14:00:00+00:00
locked_by: operator
version: 1

funder_attractive_framings:
  - id: framing-001
    claim: "Worker-owned cooperative scaling regenerative mushroom production"
    rationale: "VAPG values value-added activity by producer-owners"
    rfa_anchor: "VAPG FY26 Section 3.A.2"

dialect_register: progressive
admin_risk_terms_in_use: []
admin_risk_terms_avoid: ["DEI"]

smart_outcome_shape:
  primary: revenue_uplift

cross_section_anchors:
  - section_id: "1.A"
    methods_must_mirror:
      - framing-001
"""


_KFR_YAML = """\
schemaVersion: "1.0"
org_slug: dogwood_school

facts:
  - id: enrollment_2025_2026
    who: Dogwood Charter School
    what: Student enrollment
    when:
      period: 2025-2026
      as_of: 2025-10-01
      expiry: 2026-10-01
    where: PA
    why: PA DOE official count
    how: PIMS submission
    value: 247
    unit: students_FTE
    projection_or_actual: actual
    validation:
      confirmed_by: operator
      confirmed_at: 2026-04-15
      source_doc: orgs/dogwood/PIMS.pdf
    confidence: HIGH
"""


@pytest.fixture
def spine_path(tmp_path: Path) -> Path:
    p = tmp_path / "spine.locked.yaml"
    p.write_text(_SPINE_YAML, encoding="utf-8")
    return p


@pytest.fixture
def kfr_path(tmp_path: Path) -> Path:
    p = tmp_path / "key_facts_register.yaml"
    p.write_text(_KFR_YAML, encoding="utf-8")
    return p


_GRANT_PERIOD = (date(2026, 1, 1), date(2026, 12, 31))


# --------------------------------------------------------------------------
# Backward-compat — gates skipped when inputs absent
# --------------------------------------------------------------------------

class TestBackwardCompatSpine:

    def test_no_spine_inputs_skips_gate(self) -> None:
        result = run_post_gate_skeleton(**_base_kwargs())
        assert isinstance(result, PostGateResult)
        assert result.spine_drift_result is None

    def test_partial_spine_inputs_skips_gate(self, spine_path: Path) -> None:
        # spine_path provided but no section_id / section_dialect
        result = run_post_gate_skeleton(
            **_base_kwargs(),
            draft_text="Anything",
            spine_path=spine_path,
        )
        assert result.spine_drift_result is None
        assert F_LOGICIAN_SPINE_DRIFT not in result.failure_codes


class TestBackwardCompatFact:

    def test_no_fact_inputs_skips_gate(self) -> None:
        result = run_post_gate_skeleton(**_base_kwargs())
        assert result.fact_drift_result is None

    def test_partial_fact_inputs_skips_gate(self, kfr_path: Path) -> None:
        # kfr_path provided but no grant_funding_period
        result = run_post_gate_skeleton(
            **_base_kwargs(),
            draft_text="247 students.",
            kfr_path=kfr_path,
        )
        assert result.fact_drift_result is None
        assert F_LOGICIAN_FACT_DRIFT not in result.failure_codes


# --------------------------------------------------------------------------
# Spine-drift wire-in
# --------------------------------------------------------------------------

class TestSpineDriftWire:

    def test_clean_section_passes(self, spine_path: Path) -> None:
        result = run_post_gate_skeleton(
            **_base_kwargs(),
            draft_text=(
                "Our worker-owned cooperative will scale regenerative "
                "mushroom production with on-farm processing."
            ),
            spine_path=spine_path,
            section_id="1.A",
            section_dialect="progressive",
        )
        assert result.success is True
        assert result.spine_drift_result is not None
        assert result.spine_drift_result.verdict == "PASS"
        assert F_LOGICIAN_SPINE_DRIFT not in result.failure_codes

    def test_drifted_section_fails(self, spine_path: Path) -> None:
        result = run_post_gate_skeleton(
            **_base_kwargs(),
            draft_text=(
                "We grow some crops on a farm. We are not a cooperative."
            ),
            spine_path=spine_path,
            section_id="1.A",
            section_dialect="progressive",
        )
        assert result.success is False
        assert result.spine_drift_result is not None
        assert result.spine_drift_result.verdict == "FAIL"
        assert F_LOGICIAN_SPINE_DRIFT in result.failure_codes


# --------------------------------------------------------------------------
# Fact-drift wire-in
# --------------------------------------------------------------------------

class TestFactDriftWire:

    def test_clean_numeric_claim_passes(self, kfr_path: Path) -> None:
        result = run_post_gate_skeleton(
            **_base_kwargs(),
            draft_text=(
                "Dogwood Charter School currently enrolls 247 students "
                "for the 2025-2026 academic year."
            ),
            kfr_path=kfr_path,
            grant_funding_period=_GRANT_PERIOD,
        )
        assert result.success is True
        assert result.fact_drift_result is not None
        assert result.fact_drift_result.verdict == "PASS"
        assert F_LOGICIAN_FACT_DRIFT not in result.failure_codes

    def test_drifted_numeric_claim_fails(self, kfr_path: Path) -> None:
        result = run_post_gate_skeleton(
            **_base_kwargs(),
            draft_text=(
                "Dogwood Charter School currently enrolls 250 students this year."
            ),
            kfr_path=kfr_path,
            grant_funding_period=_GRANT_PERIOD,
        )
        assert result.success is False
        assert result.fact_drift_result is not None
        assert result.fact_drift_result.verdict == "FAIL"
        assert F_LOGICIAN_FACT_DRIFT in result.failure_codes


# --------------------------------------------------------------------------
# Multi-gate coexistence
# --------------------------------------------------------------------------

class TestMultiGateCoexistence:

    def test_spine_and_fact_both_fire(
        self, spine_path: Path, kfr_path: Path
    ) -> None:
        # Section drifts on spine AND has wrong number for KFR fact.
        result = run_post_gate_skeleton(
            **_base_kwargs(),
            draft_text=(
                "We grow generic crops. We are not a cooperative. "
                "Dogwood Charter School currently enrolls 250 students."
            ),
            spine_path=spine_path,
            section_id="1.A",
            section_dialect="progressive",
            kfr_path=kfr_path,
            grant_funding_period=_GRANT_PERIOD,
        )
        assert result.success is False
        assert F_LOGICIAN_SPINE_DRIFT in result.failure_codes
        assert F_LOGICIAN_FACT_DRIFT in result.failure_codes

    def test_post10_plus_spine_plus_fact(
        self, spine_path: Path, kfr_path: Path
    ) -> None:
        # F-POST-10 (admin-risk hard-block) + spine + fact all fire
        result = run_post_gate_skeleton(
            **_base_kwargs(hard_block=1),
            draft_text=(
                "We grow generic crops. We are not a cooperative. "
                "Dogwood Charter School currently enrolls 250 students."
            ),
            spine_path=spine_path,
            section_id="1.A",
            section_dialect="progressive",
            kfr_path=kfr_path,
            grant_funding_period=_GRANT_PERIOD,
        )
        assert result.success is False
        assert F_POST_10 in result.failure_codes
        assert F_LOGICIAN_SPINE_DRIFT in result.failure_codes
        assert F_LOGICIAN_FACT_DRIFT in result.failure_codes
