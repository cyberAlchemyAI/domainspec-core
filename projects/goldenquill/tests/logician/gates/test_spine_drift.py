"""Tests for ``pipeline.logician.gates.f_logician_spine_drift``.

Coverage:
- Schema loader: valid YAML, missing required fields, bad dialect enum,
  malformed datetime, framing-id collision detection.
- Anchor lookup: section without anchor → silent on framing checks.
- Framing recall: above/below threshold, missing-keyword reporting.
- Anti-contradiction: explicit negation patterns hit, neutral text passes.
- Dialect drift: matching/mismatching/unknown classifications.
- Admin-risk avoid-list: word-boundaried hits, partial-token misses.
- Multi-failure: all reasons coexist in findings list.

YAML fixtures are written to tmp_path inline (no separate fixture files
to maintain).
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from pipeline.logician.gates.f_logician_spine_drift import (
    DEFAULT_KEYWORD_RECALL_THRESHOLD,
    F_LOGICIAN_SPINE_DRIFT,
    NarrativeSpine,
    SpineDriftFinding,
    SpineDriftGateResult,
    SpineFraming,
    SpineSchemaError,
    check_spine_drift,
    load_spine,
)


# --------------------------------------------------------------------------
# YAML fixtures
# --------------------------------------------------------------------------

_VALID_SPINE_YAML = """\
grant_id: vapg_fy26_mycosymbiotics
locked_at: 2026-05-08T14:00:00+00:00
locked_by: operator
version: 1

funder_attractive_framings:
  - id: framing-001
    claim: "Worker-owned cooperative scaling regenerative mushroom production"
    rationale: "VAPG explicitly values value-added activity by producer-owners"
    rfa_anchor: "VAPG FY26 Section 3.A.2"
  - id: framing-002
    claim: "On-farm processing creates measurable economic uplift"
    rationale: "VAPG rewards measurable economic uplift"
    rfa_anchor: "VAPG FY26 Section 3.B.1"

dialect_register: progressive

admin_risk_terms_in_use: []
admin_risk_terms_avoid:
  - "DEI"
  - "equity-centered"

smart_outcome_shape:
  primary: revenue_uplift
  secondary: jobs_created
  tertiary: market_diversification

strategic_emphasis:
  lead_with: workforce_metrics
  de_emphasize: yield_data
  rationale: "VAPG reviewers respond to economic + workforce; yield reads as production-grant noise"

cross_section_anchors:
  - section_id: "1.A"
    methods_must_mirror:
      - framing-001
      - framing-002
    outcomes_must_mirror:
      - framing-001
    budget_justification_must_cite:
      - framing-002
"""


def _write_spine(tmp_path: Path, content: str = _VALID_SPINE_YAML) -> Path:
    p = tmp_path / "spine.locked.yaml"
    p.write_text(content, encoding="utf-8")
    return p


# --------------------------------------------------------------------------
# Loader
# --------------------------------------------------------------------------

class TestLoadSpine:

    def test_valid_yaml_loads(self, tmp_path: Path) -> None:
        spine = load_spine(_write_spine(tmp_path))
        assert isinstance(spine, NarrativeSpine)
        assert spine.grant_id == "vapg_fy26_mycosymbiotics"
        assert spine.version == 1
        assert spine.dialect_register == "progressive"
        assert len(spine.funder_attractive_framings) == 2
        assert spine.framing_by_id("framing-001") is not None
        assert spine.anchor_for_section("1.A") is not None

    def test_keywords_derived_at_load(self, tmp_path: Path) -> None:
        spine = load_spine(_write_spine(tmp_path))
        framing = spine.framing_by_id("framing-001")
        assert framing is not None
        # Content words ≥4 chars in
        # "Worker-owned cooperative scaling regenerative mushroom production"
        # Note: hyphenated 'worker-owned' is split by the regex pattern
        # into 'worker' and 'owned' — both ≥4 chars and pass.
        assert "cooperative" in framing.keywords
        assert "regenerative" in framing.keywords
        assert "mushroom" in framing.keywords
        assert "production" in framing.keywords
        # 'a' / 'and' / 'the' filtered as stopwords
        assert "and" not in framing.keywords

    def test_missing_grant_id_fails(self, tmp_path: Path) -> None:
        bad = _VALID_SPINE_YAML.replace(
            "grant_id: vapg_fy26_mycosymbiotics", "grant_id: ''"
        )
        with pytest.raises(SpineSchemaError, match="grant_id"):
            load_spine(_write_spine(tmp_path, bad))

    def test_invalid_dialect_fails(self, tmp_path: Path) -> None:
        bad = _VALID_SPINE_YAML.replace(
            "dialect_register: progressive", "dialect_register: chaotic"
        )
        with pytest.raises(SpineSchemaError, match="dialect_register"):
            load_spine(_write_spine(tmp_path, bad))

    def test_naive_datetime_fails(self, tmp_path: Path) -> None:
        bad = _VALID_SPINE_YAML.replace(
            "locked_at: 2026-05-08T14:00:00+00:00",
            "locked_at: 2026-05-08T14:00:00",
        )
        with pytest.raises(SpineSchemaError, match="timezone-aware"):
            load_spine(_write_spine(tmp_path, bad))

    def test_empty_framings_fails(self, tmp_path: Path) -> None:
        bad = _VALID_SPINE_YAML.replace(
            "funder_attractive_framings:",
            "funder_attractive_framings: []\n_keep_indent:",
        )
        with pytest.raises(SpineSchemaError, match="funder_attractive_framings"):
            load_spine(_write_spine(tmp_path, bad))

    def test_missing_smart_primary_fails(self, tmp_path: Path) -> None:
        bad = _VALID_SPINE_YAML.replace(
            "primary: revenue_uplift",
            "primary: ''",
        )
        with pytest.raises(SpineSchemaError, match="primary"):
            load_spine(_write_spine(tmp_path, bad))

    def test_missing_file_raises_file_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            load_spine(tmp_path / "nope.yaml")

    def test_keyword_recall_threshold_override(self, tmp_path: Path) -> None:
        custom = _VALID_SPINE_YAML + "\nkeyword_recall_threshold: 0.4\n"
        spine = load_spine(_write_spine(tmp_path, custom))
        assert spine.keyword_recall_threshold == 0.4


# --------------------------------------------------------------------------
# Gate — anchored section happy path + framing recall
# --------------------------------------------------------------------------

class TestFramingRecall:

    def test_section_meets_required_framings(self, tmp_path: Path) -> None:
        spine_path = _write_spine(tmp_path)
        section = (
            "Our worker-owned cooperative will scale regenerative mushroom "
            "production using on-farm processing methods that create "
            "measurable economic uplift across the worker membership."
        )
        result = check_spine_drift(
            section_text=section,
            section_id="1.A",
            section_dialect="progressive",
            spine_path=spine_path,
        )
        assert result.verdict == "PASS"
        assert result.framings_checked == 2

    def test_weak_framing_recall_fails(self, tmp_path: Path) -> None:
        spine_path = _write_spine(tmp_path)
        # Section avoids the framing-001 keywords almost entirely
        section = (
            "We grow specialty crops on a small farm using sustainable "
            "techniques. Our work serves the local community."
        )
        result = check_spine_drift(
            section_text=section,
            section_id="1.A",
            section_dialect="progressive",
            spine_path=spine_path,
        )
        assert result.verdict == "FAIL"
        assert result.failure_code == F_LOGICIAN_SPINE_DRIFT
        weak_findings = [
            f for f in result.findings if f.reason_tag == "spine_framing_weak"
        ]
        assert len(weak_findings) >= 1
        framing_ids = {f.framing_id for f in weak_findings}
        assert "framing-001" in framing_ids

    def test_unanchored_section_silent_on_framings(self, tmp_path: Path) -> None:
        spine_path = _write_spine(tmp_path)
        # section_id "9.Z" not in cross_section_anchors → framing checks skipped
        result = check_spine_drift(
            section_text="Random text with no framing keywords whatsoever.",
            section_id="9.Z",
            section_dialect="progressive",
            spine_path=spine_path,
        )
        assert result.verdict == "PASS"
        assert result.framings_checked == 0


# --------------------------------------------------------------------------
# Gate — anti-contradiction
# --------------------------------------------------------------------------

class TestAntiContradiction:

    def test_explicit_negation_fails(self, tmp_path: Path) -> None:
        spine_path = _write_spine(tmp_path)
        section = (
            "Our worker-owned cooperative will scale regenerative mushroom "
            "production using on-farm processing methods that create "
            "measurable economic uplift. We are not a cooperative in the "
            "traditional sense."
        )
        result = check_spine_drift(
            section_text=section,
            section_id="1.A",
            section_dialect="progressive",
            spine_path=spine_path,
        )
        # 'not a cooperative' should fire spine_framing_contradicted on
        # framing-001 (which has 'cooperative' as a keyword)
        contradiction_findings = [
            f for f in result.findings
            if f.reason_tag == "spine_framing_contradicted"
        ]
        assert len(contradiction_findings) >= 1
        assert result.verdict == "FAIL"

    def test_outside_pattern_fires(self, tmp_path: Path) -> None:
        spine_path = _write_spine(tmp_path)
        section = (
            "Our worker-owned cooperative will scale regenerative mushroom "
            "production. We sit outside of the regenerative agriculture model."
        )
        result = check_spine_drift(
            section_text=section,
            section_id="1.A",
            section_dialect="progressive",
            spine_path=spine_path,
        )
        contradiction_findings = [
            f for f in result.findings
            if f.reason_tag == "spine_framing_contradicted"
        ]
        assert len(contradiction_findings) >= 1


# --------------------------------------------------------------------------
# Gate — dialect drift
# --------------------------------------------------------------------------

class TestDialectDrift:

    def test_matching_dialect_passes(self, tmp_path: Path) -> None:
        spine_path = _write_spine(tmp_path)
        section = (
            "Worker-owned cooperative scaling regenerative mushroom production "
            "with measurable economic uplift through on-farm processing."
        )
        result = check_spine_drift(
            section_text=section,
            section_id="1.A",
            section_dialect="progressive",  # spine says progressive
            spine_path=spine_path,
        )
        assert result.verdict == "PASS"

    def test_mismatched_dialect_fails(self, tmp_path: Path) -> None:
        spine_path = _write_spine(tmp_path)
        section = (
            "Worker-owned cooperative scaling regenerative mushroom production "
            "with measurable economic uplift through on-farm processing."
        )
        result = check_spine_drift(
            section_text=section,
            section_id="1.A",
            section_dialect="conservative",  # mismatch
            spine_path=spine_path,
        )
        assert result.verdict == "FAIL"
        dialect_findings = [
            f for f in result.findings if f.reason_tag == "spine_dialect_drift"
        ]
        assert len(dialect_findings) == 1

    def test_unknown_dialect_skips_check(self, tmp_path: Path) -> None:
        # Low-confidence classification → "unknown" → skip dialect check.
        spine_path = _write_spine(tmp_path)
        section = (
            "Worker-owned cooperative scaling regenerative mushroom production "
            "with measurable economic uplift through on-farm processing."
        )
        result = check_spine_drift(
            section_text=section,
            section_id="1.A",
            section_dialect="unknown",
            spine_path=spine_path,
        )
        assert result.verdict == "PASS"


# --------------------------------------------------------------------------
# Gate — admin-risk avoid-list
# --------------------------------------------------------------------------

class TestAdminRiskAvoidList:

    def test_avoid_term_fires(self, tmp_path: Path) -> None:
        spine_path = _write_spine(tmp_path)
        section = (
            "Worker-owned cooperative scaling regenerative mushroom production "
            "with measurable economic uplift. Our DEI work supports the "
            "membership."
        )
        result = check_spine_drift(
            section_text=section,
            section_id="1.A",
            section_dialect="progressive",
            spine_path=spine_path,
        )
        # spine.admin_risk_terms_avoid includes "DEI"
        violation_findings = [
            f for f in result.findings
            if f.reason_tag == "spine_admin_risk_violation"
        ]
        assert len(violation_findings) == 1
        assert violation_findings[0].detail == "avoid-list term in section: 'DEI'"

    def test_word_boundary_avoids_partial_match(self, tmp_path: Path) -> None:
        # 'DEIcide' should NOT fire on 'DEI' avoid-term thanks to \b
        spine_path = _write_spine(tmp_path)
        section = (
            "Worker-owned cooperative scaling regenerative mushroom production "
            "with measurable economic uplift through on-farm processing. "
            "We oppose DEIcide as a concept."
        )
        result = check_spine_drift(
            section_text=section,
            section_id="1.A",
            section_dialect="progressive",
            spine_path=spine_path,
        )
        violation_findings = [
            f for f in result.findings
            if f.reason_tag == "spine_admin_risk_violation"
        ]
        # No DEI hit (DEIcide is not DEI)
        assert len(violation_findings) == 0


# --------------------------------------------------------------------------
# Gate — structural failures
# --------------------------------------------------------------------------

class TestStructuralFailures:

    def test_missing_spine_file_fails(self, tmp_path: Path) -> None:
        result = check_spine_drift(
            section_text="anything",
            section_id="1.A",
            section_dialect="progressive",
            spine_path=tmp_path / "no-such-file.yaml",
        )
        assert result.verdict == "FAIL"
        assert result.failure_code == F_LOGICIAN_SPINE_DRIFT
        assert result.findings[0].reason_tag == "spine_missing"

    def test_bad_yaml_fails_with_schema_error(self, tmp_path: Path) -> None:
        path = tmp_path / "spine.locked.yaml"
        path.write_text("not: valid: yaml: at all: : :", encoding="utf-8")
        result = check_spine_drift(
            section_text="anything",
            section_id="1.A",
            section_dialect="progressive",
            spine_path=path,
        )
        assert result.verdict == "FAIL"
        assert result.findings[0].reason_tag == "spine_schema_error"
        assert result.schema_error is not None


# --------------------------------------------------------------------------
# Gate — multi-failure
# --------------------------------------------------------------------------

class TestMultiFailure:

    def test_all_reasons_coexist(self, tmp_path: Path) -> None:
        spine_path = _write_spine(tmp_path)
        # Section that drifts on framing, has wrong dialect, contains avoid-term
        section = (
            "We grow some crops on a farm. We are not a cooperative. "
            "Our DEI program is robust."
        )
        result = check_spine_drift(
            section_text=section,
            section_id="1.A",
            section_dialect="conservative",  # mismatch
            spine_path=spine_path,
        )
        assert result.verdict == "FAIL"
        reasons = {f.reason_tag for f in result.findings}
        assert "spine_framing_weak" in reasons
        assert "spine_dialect_drift" in reasons
        assert "spine_admin_risk_violation" in reasons
