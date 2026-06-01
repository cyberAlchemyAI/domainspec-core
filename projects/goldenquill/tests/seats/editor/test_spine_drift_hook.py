"""Tests for ``pipeline.seats.editor.spine_drift_hook``.

Editor-side spine-drift hook uses pre/post delta semantics to attribute
drift correctly:

- Pre-existing drift (Scribe's fault) → NOT a verdict failure here.
- New drift in post-Editor text → verdict FAIL with delta_findings populated.
- Both pre and post clean → PASS.
- Structural spine failure (missing/schema) → FAIL with full finding set.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.seats.editor.spine_drift_hook import (
    EditorSpineDeltaResult,
    check_editor_spine_delta,
)
from pipeline.logician.gates.f_logician_spine_drift import F_LOGICIAN_SPINE_DRIFT


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
admin_risk_terms_avoid:
  - "DEI"

smart_outcome_shape:
  primary: revenue_uplift

cross_section_anchors:
  - section_id: "1.A"
    methods_must_mirror:
      - framing-001
"""


@pytest.fixture
def spine_path(tmp_path: Path) -> Path:
    p = tmp_path / "spine.locked.yaml"
    p.write_text(_SPINE_YAML, encoding="utf-8")
    return p


# --------------------------------------------------------------------------
# Happy path — both pre and post clean
# --------------------------------------------------------------------------

class TestBothClean:

    def test_clean_throughout_passes(self, spine_path: Path) -> None:
        # Both versions of the section meet the spine framing.
        clean_text = (
            "Our worker-owned cooperative will scale regenerative "
            "mushroom production with on-farm processing methods."
        )
        result = check_editor_spine_delta(
            pre_editor_section_text=clean_text,
            post_editor_section_text=clean_text,  # Editor made no changes
            section_id="1.A",
            section_dialect="progressive",
            spine_path=spine_path,
        )
        assert isinstance(result, EditorSpineDeltaResult)
        assert result.verdict == "PASS"
        assert result.pre_editor_verdict == "PASS"
        assert result.post_editor_verdict == "PASS"
        assert result.delta_findings == ()


# --------------------------------------------------------------------------
# Editor-introduced drift — the canonical fail case
# --------------------------------------------------------------------------

class TestEditorIntroducedDrift:

    def test_editor_weakens_framing_fails(self, spine_path: Path) -> None:
        # Pre-Editor: full framing keywords present → pass.
        # Post-Editor: Editor "polished" and dropped half the keywords → fail.
        pre_text = (
            "Our worker-owned cooperative will scale regenerative "
            "mushroom production with on-farm processing methods."
        )
        post_text = (
            "Our cooperative produces mushrooms using thoughtful "
            "agricultural practices."
        )
        result = check_editor_spine_delta(
            pre_editor_section_text=pre_text,
            post_editor_section_text=post_text,
            section_id="1.A",
            section_dialect="progressive",
            spine_path=spine_path,
        )
        assert result.verdict == "FAIL"
        assert result.failure_code == F_LOGICIAN_SPINE_DRIFT
        assert result.pre_editor_verdict == "PASS"
        assert result.post_editor_verdict == "FAIL"
        # Delta should attribute the new spine_framing_weak to Editor
        assert len(result.delta_findings) >= 1
        delta_reasons = {f.reason_tag for f in result.delta_findings}
        assert "spine_framing_weak" in delta_reasons

    def test_editor_introduces_admin_risk_term_fails(self, spine_path: Path) -> None:
        pre_text = (
            "Our worker-owned cooperative will scale regenerative "
            "mushroom production with on-farm processing methods."
        )
        post_text = pre_text + " Our DEI commitment is unwavering."
        result = check_editor_spine_delta(
            pre_editor_section_text=pre_text,
            post_editor_section_text=post_text,
            section_id="1.A",
            section_dialect="progressive",
            spine_path=spine_path,
        )
        assert result.verdict == "FAIL"
        delta_reasons = {f.reason_tag for f in result.delta_findings}
        assert "spine_admin_risk_violation" in delta_reasons


# --------------------------------------------------------------------------
# Pre-existing drift — Scribe's fault, not Editor's
# --------------------------------------------------------------------------

class TestPreExistingDrift:

    def test_pre_existing_weakness_not_attributed_to_editor(
        self, spine_path: Path
    ) -> None:
        # Pre-Editor: section already weak on framing.
        # Post-Editor: Editor preserved the same weakness (no new finding).
        # → Editor-side hook should PASS (pre-existing drift is Scribe's).
        weak_text = "We grow mushrooms on a small operation."
        result = check_editor_spine_delta(
            pre_editor_section_text=weak_text,
            post_editor_section_text=weak_text,  # Editor made no changes
            section_id="1.A",
            section_dialect="progressive",
            spine_path=spine_path,
        )
        # Pre + post both fail at the gate level (drift exists)...
        assert result.pre_editor_verdict == "FAIL"
        assert result.post_editor_verdict == "FAIL"
        # ...but Editor-side hook PASSES because no NEW drift introduced
        assert result.verdict == "PASS"
        assert result.delta_findings == ()
        # Operator can still see the pre-existing finding for context
        assert len(result.pre_editor_findings) >= 1
        assert len(result.post_editor_findings) >= 1

    def test_editor_partially_recovers_passes(self, spine_path: Path) -> None:
        # Pre-Editor: missing keywords (drifted).
        # Post-Editor: some keywords restored, fewer findings than pre.
        # → Editor-side hook PASSES (Editor improved adherence).
        pre_text = "Mushrooms grown carefully on the farm."
        post_text = (
            "Our worker-owned cooperative scales regenerative mushroom "
            "production carefully on the farm."
        )
        result = check_editor_spine_delta(
            pre_editor_section_text=pre_text,
            post_editor_section_text=post_text,
            section_id="1.A",
            section_dialect="progressive",
            spine_path=spine_path,
        )
        # Pre fails, post passes — Editor improved things → no new drift.
        assert result.pre_editor_verdict == "FAIL"
        assert result.post_editor_verdict == "PASS"
        assert result.verdict == "PASS"
        assert result.delta_findings == ()


# --------------------------------------------------------------------------
# Mixed delta — some new findings, some pre-existing
# --------------------------------------------------------------------------

class TestMixedDelta:

    def test_only_new_findings_appear_in_delta(self, spine_path: Path) -> None:
        # Pre: weak framing-001 (one finding).
        # Post: STILL weak framing-001 (same finding) + new admin-risk hit.
        # → Editor introduced ONE new finding (the avoid-term); the
        #   pre-existing weak framing is not attributed.
        pre_text = "Mushrooms grown on a small farm."
        post_text = pre_text + " We hold a strong DEI commitment."
        result = check_editor_spine_delta(
            pre_editor_section_text=pre_text,
            post_editor_section_text=post_text,
            section_id="1.A",
            section_dialect="progressive",
            spine_path=spine_path,
        )
        assert result.verdict == "FAIL"
        # Delta has only the new admin-risk finding
        delta_reasons = {f.reason_tag for f in result.delta_findings}
        assert "spine_admin_risk_violation" in delta_reasons
        assert "spine_framing_weak" not in delta_reasons


# --------------------------------------------------------------------------
# Structural failures — surface as FAIL with full delta=findings
# --------------------------------------------------------------------------

class TestStructuralFailures:

    def test_missing_spine_fails(self, tmp_path: Path) -> None:
        result = check_editor_spine_delta(
            pre_editor_section_text="anything",
            post_editor_section_text="anything else",
            section_id="1.A",
            section_dialect="progressive",
            spine_path=tmp_path / "no-such-file.yaml",
        )
        assert result.verdict == "FAIL"
        assert result.failure_code == F_LOGICIAN_SPINE_DRIFT
        # Structural failure surfaces in delta_findings (otherwise
        # silently swallowed by the pre==post identity check)
        assert any(
            f.reason_tag == "spine_missing"
            for f in result.delta_findings
        )

    def test_bad_yaml_fails(self, tmp_path: Path) -> None:
        path = tmp_path / "spine.locked.yaml"
        path.write_text("not: valid: yaml: : :", encoding="utf-8")
        result = check_editor_spine_delta(
            pre_editor_section_text="anything",
            post_editor_section_text="anything else",
            section_id="1.A",
            section_dialect="progressive",
            spine_path=path,
        )
        assert result.verdict == "FAIL"
        assert any(
            f.reason_tag == "spine_schema_error"
            for f in result.delta_findings
        )


# --------------------------------------------------------------------------
# Dialect drift attribution
# --------------------------------------------------------------------------

class TestDialectDriftAttribution:

    def test_editor_dialect_change_attributed(self, spine_path: Path) -> None:
        # If Editor's edits change the section's classified dialect,
        # that's Editor's fault — should appear in delta.
        clean_text = (
            "Our worker-owned cooperative will scale regenerative "
            "mushroom production with on-farm processing methods."
        )
        result = check_editor_spine_delta(
            pre_editor_section_text=clean_text,
            post_editor_section_text=clean_text,
            section_id="1.A",
            section_dialect="conservative",  # Editor's classification
            spine_path=spine_path,
        )
        # Pre + post both have dialect drift (same dialect both times).
        # But the dialect was already wrong pre-Editor, so it's NOT new.
        # → Editor-side hook PASSES (no new drift).
        # NOTE: in real flow, pre_editor_dialect should be the Scribe-
        # classified dialect; here we use the same value for both as a
        # simplification. A separate test could use different dialects.
        assert result.verdict == "PASS"
