"""Tests for ``pipeline.orchestrator.seats.report_generator._cedar_bootstrap``.

Per WS-J Slice 2 (2026-05-11). Verifies:

* All 5 ``report_*.cedar`` skeleton policies load.
* ``CedarEngine.is_ready()`` returns True after bootstrap.
* The Python evaluator DENYs on each F-REPORT-* gate failure.
* The Python evaluator PERMITs when every supplied gate is success.
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from pipeline.orchestrator.seats.report_generator._cedar_bootstrap import (
    F_REPORT_COMMITMENT_MISSED,
    F_REPORT_COMMITMENT_UNTRACED,
    F_REPORT_NUMERIC_DRIFT,
    F_REPORT_OUT_OF_SCOPE_DRIFT,
    F_REPORT_TEMPLATE_MISMATCH,
    REPORT_FAILURE_CODES,
    REQUIRED_REPORT_POLICY_NAMES,
    CedarVerdict,
    CriticalPolicyError,
    _bootstrap_cedar_engine_at,
    evaluate_report_finalize_action,
    get_cedar_engine,
    get_report_policy_texts,
    load_report_cedar_policies,
    report_cedar_policy_dir,
)
from pipeline.orchestrator.seats.report_generator._schemas import (
    BUNDLE_STATE_DRAFT_PENDING,
    BUNDLE_STATE_FINALIZED,
    OPERATOR_SIG_STATUS_PENDING,
    OPERATOR_SIG_STATUS_SIGNED,
    GrantReportBundle,
)


# ---------------------------------------------------------------------------
# Stub gate-result types — mirror the .success + .fired_sub_tags shape
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class _StubResult:
    success: bool
    failure_code: str = ""
    fired_sub_tags: tuple[str, ...] = ()
    findings: tuple = ()


def _pass() -> _StubResult:
    return _StubResult(success=True)


def _fail(code: str, *sub_tags: str) -> _StubResult:
    return _StubResult(
        success=False,
        failure_code=code,
        fired_sub_tags=sub_tags,
    )


def _draft_bundle() -> GrantReportBundle:
    return GrantReportBundle(
        run_id="RUN-1",
        org_slug="myorg",
        grant_id="G1",
        period_n=1,
        draft_path="orgs/myorg/vault/grants/G1/reports/period_1/draft_1.md",
        draft_version=1,
        claim_evidence_map_path="orgs/myorg/vault/grants/G1/reports/period_1/claim_evidence_map.yaml",
        scoring_dir="orgs/myorg/vault/grants/G1/reports/period_1/scoring/",
        proposal_commitments_consumed=("COMMIT-001",),
        reporting_template_content_sha3_512="c" * 128,
        sub_sections_authored=("narrative", "metrics_table"),
        operator_signature_status=OPERATOR_SIG_STATUS_PENDING,
        operator_signature="",
        operator_signed_at_utc="",
        finalized_at_utc="",
        bundle_state=BUNDLE_STATE_DRAFT_PENDING,
    )


# ---------------------------------------------------------------------------
# Policy loader tests
# ---------------------------------------------------------------------------


class TestLoadReportCedarPolicies:
    def test_loads_all_five_policies(self):
        texts = load_report_cedar_policies()
        assert set(texts.keys()) == REQUIRED_REPORT_POLICY_NAMES
        for name, text in texts.items():
            assert text.strip(), f"policy {name!r} empty"
            # Sanity: contains either "permit" or "forbid".
            assert "permit" in text.lower() or "forbid" in text.lower()

    def test_missing_dir_raises(self, tmp_path):
        with pytest.raises(CriticalPolicyError):
            load_report_cedar_policies(policy_dir=tmp_path / "nonexistent")

    def test_missing_required_policy_raises(self, tmp_path):
        # Only place one of the five policies in tmp_path.
        canonical = report_cedar_policy_dir()
        (tmp_path / "report_commitment_untraced.cedar").write_text(
            (canonical / "report_commitment_untraced.cedar").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        with pytest.raises(CriticalPolicyError):
            load_report_cedar_policies(policy_dir=tmp_path)


# ---------------------------------------------------------------------------
# Engine bootstrap tests
# ---------------------------------------------------------------------------


class TestBootstrapCedarEngine:
    def test_module_load_engine_is_ready(self):
        engine = get_cedar_engine()
        assert engine.is_ready() is True
        loaded = frozenset(engine.loaded_policy_names())
        # All 5 report_*.cedar policies must be loaded (engine may have
        # also loaded other vault/policies/*.cedar files).
        assert REQUIRED_REPORT_POLICY_NAMES.issubset(loaded)

    def test_module_load_policy_texts_cached(self):
        texts = get_report_policy_texts()
        assert frozenset(texts.keys()) == REQUIRED_REPORT_POLICY_NAMES

    def test_bootstrap_at_fresh_dir(self):
        engine = _bootstrap_cedar_engine_at(policy_dir=report_cedar_policy_dir())
        assert engine.is_ready() is True


# ---------------------------------------------------------------------------
# Python evaluator tests
# ---------------------------------------------------------------------------


class TestEvaluateReportFinalizeAction:
    def test_permit_when_all_pass(self):
        v = evaluate_report_finalize_action(
            _draft_bundle(),
            commitment_untraced=_pass(),
            numeric_drift=_pass(),
            template_mismatch=_pass(),
            out_of_scope_drift=_pass(),
            commitment_missed=_pass(),
        )
        assert isinstance(v, CedarVerdict)
        assert v.decision == "PERMIT"
        assert v.failure_code is None
        assert v.rule is None

    def test_permit_when_no_gates_supplied(self):
        v = evaluate_report_finalize_action(_draft_bundle())
        assert v.decision == "PERMIT"

    @pytest.mark.parametrize(
        "kwarg,failure_code,sub_tag",
        [
            (
                "commitment_untraced",
                F_REPORT_COMMITMENT_UNTRACED,
                ".claim_text_no_map_entry",
            ),
            (
                "numeric_drift",
                F_REPORT_NUMERIC_DRIFT,
                ".kfr_value_mismatch_above_tolerance",
            ),
            (
                "template_mismatch",
                F_REPORT_TEMPLATE_MISMATCH,
                ".workspace_published_template_drift",
            ),
            (
                "out_of_scope_drift",
                F_REPORT_OUT_OF_SCOPE_DRIFT,
                ".scope_tag_not_in_promoted_set",
            ),
            (
                "commitment_missed",
                F_REPORT_COMMITMENT_MISSED,
                ".commitment_required_subsection_missing",
            ),
        ],
    )
    def test_deny_on_each_failure_code(self, kwarg, failure_code, sub_tag):
        v = evaluate_report_finalize_action(
            _draft_bundle(),
            **{kwarg: _fail(failure_code, sub_tag)},
        )
        assert v.decision == "DENY"
        assert v.failure_code == failure_code
        assert sub_tag in v.sub_tags

    def test_first_firing_gate_wins(self):
        """Multiple gates fail → the first in iteration order wins.
        Iteration order: template → commitment_missed → commitment_untraced →
        out_of_scope_drift → numeric_drift."""
        v = evaluate_report_finalize_action(
            _draft_bundle(),
            commitment_untraced=_fail(F_REPORT_COMMITMENT_UNTRACED, ".x"),
            template_mismatch=_fail(F_REPORT_TEMPLATE_MISMATCH, ".y"),
        )
        # Template comes first.
        assert v.failure_code == F_REPORT_TEMPLATE_MISMATCH

    def test_finalized_bundle_rejected(self):
        # Build a manually-FINALIZED bundle (skipping post_init checks via
        # the legit SIGNED + non-empty signature route).
        bundle = GrantReportBundle(
            run_id="RUN-1",
            org_slug="myorg",
            grant_id="G1",
            period_n=1,
            draft_path="x",
            draft_version=1,
            claim_evidence_map_path="x",
            scoring_dir="x",
            proposal_commitments_consumed=("COMMIT-001",),
            reporting_template_content_sha3_512="c" * 128,
            sub_sections_authored=("narrative",),
            operator_signature_status=OPERATOR_SIG_STATUS_SIGNED,
            operator_signature="aa",
            operator_signed_at_utc="2026-05-11T12:00:00Z",
            finalized_at_utc="2026-05-11T12:00:00Z",
            bundle_state=BUNDLE_STATE_FINALIZED,
        )
        with pytest.raises(ValueError):
            evaluate_report_finalize_action(bundle)

    def test_non_bundle_arg_rejected(self):
        with pytest.raises(TypeError):
            evaluate_report_finalize_action("not a bundle")  # type: ignore[arg-type]


class TestFailureCodesConstants:
    def test_failure_codes_match_expected_set(self):
        assert REPORT_FAILURE_CODES == frozenset(
            {
                F_REPORT_COMMITMENT_UNTRACED,
                F_REPORT_COMMITMENT_MISSED,
                F_REPORT_OUT_OF_SCOPE_DRIFT,
                F_REPORT_NUMERIC_DRIFT,
                F_REPORT_TEMPLATE_MISMATCH,
            }
        )

    def test_required_policy_names_match_failure_codes(self):
        # 5 policies pair 1:1 with 5 F-REPORT-* failure codes.
        assert len(REQUIRED_REPORT_POLICY_NAMES) == len(REPORT_FAILURE_CODES)
