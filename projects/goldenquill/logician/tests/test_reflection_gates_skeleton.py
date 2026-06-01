"""Skeleton tests for logician.gates.reflection_gates — v0.1 Beta hook.

Architecture v7.0.9 §2 + §4 + §6 + §7 acceptance criteria.
§4 Logician v2.x.2 sub-amendment §10 + §13 acceptance criteria.
Operator refinement 2026-05-10: 8 BINDING + 8 HORIZON + 1 PROBE-DEPENDENT.

Run from workspace root:
    python3 -m pytest logician/tests/test_reflection_gates_skeleton.py -v
"""
from __future__ import annotations

import hashlib
import inspect
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from logician.gates import reflection_gates as rg


BINDING_CODES = (
    "F-REFLECTION-NO-EXTERNAL-SIGNAL",
    "F-REFLECTION-EVAL-ONLY-GROUNDED",
    "F-REFLECTION-INSUFFICIENT-EVIDENCE",
    "F-REFLECTION-RFA-SPEC-OVERRIDE",
    "F-REFLECTION-DEPTH-EXCEEDED",
    "F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH",
    "F-REFLECTION-WRITE-WITHOUT-COMMIT",
    "F-REFLECTION-COVERAGE-INCOMPLETE",
)

HORIZON_CODES = (
    "F-REFLECTION-INTENT-ANCHOR-DRIFT",
    "F-REFLECTION-CONTENT-LOOP-DETECTED",
    "F-REFLECTION-EVAL-SURROGATE-DIVERGENCE",
    "F-REFLECTION-OPERATOR-OVERRIDE-MASK",
    "F-REFLECTION-INOCULATION-FRAME-MISSING",
    "F-REFLECTION-SELF-REPORTED-CONFIDENCE",
    "F-REFLECTION-FABRICATION-ON-FAILURE",
    "F-REFLECTION-PROBE-COVERAGE-INCOMPLETE",
)

PROBE_DEPENDENT_CODES = (
    "F-REFLECTION-SYCOPHANCY-LOOP-DETECTED",
)

ALL_CODES = BINDING_CODES + HORIZON_CODES + PROBE_DEPENDENT_CODES

# Map gate code → expected function name in the module.
_CODE_TO_FN_NAME: dict[str, str] = {
    "F-REFLECTION-NO-EXTERNAL-SIGNAL": "predicate_no_external_signal",
    "F-REFLECTION-EVAL-ONLY-GROUNDED": "predicate_eval_only_grounded",
    "F-REFLECTION-INSUFFICIENT-EVIDENCE": "predicate_insufficient_evidence",
    "F-REFLECTION-RFA-SPEC-OVERRIDE": "predicate_rfa_spec_override",
    "F-REFLECTION-DEPTH-EXCEEDED": "predicate_depth_exceeded",
    "F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH": "predicate_self_evaluator_family_clash",
    "F-REFLECTION-WRITE-WITHOUT-COMMIT": "predicate_write_without_commit",
    "F-REFLECTION-COVERAGE-INCOMPLETE": "predicate_coverage_incomplete",
    "F-REFLECTION-INTENT-ANCHOR-DRIFT": "predicate_intent_anchor_drift",
    "F-REFLECTION-CONTENT-LOOP-DETECTED": "predicate_content_loop_detected",
    "F-REFLECTION-EVAL-SURROGATE-DIVERGENCE": "predicate_eval_surrogate_divergence",
    "F-REFLECTION-OPERATOR-OVERRIDE-MASK": "predicate_operator_override_mask",
    "F-REFLECTION-INOCULATION-FRAME-MISSING": "predicate_inoculation_frame_missing",
    "F-REFLECTION-SELF-REPORTED-CONFIDENCE": "predicate_self_reported_confidence",
    "F-REFLECTION-FABRICATION-ON-FAILURE": "predicate_fabrication_on_failure",
    "F-REFLECTION-PROBE-COVERAGE-INCOMPLETE": "predicate_probe_coverage_incomplete",
    "F-REFLECTION-SYCOPHANCY-LOOP-DETECTED": "predicate_sycophancy_loop_detected",
}


# ============================================================================
# 17 — predicate signature presence (test_<code>_predicate_signature_present)
# ============================================================================

class TestPredicateSignaturesPresent(unittest.TestCase):
    """Architecture v7.0.9 §2 acceptance criterion 1: all 17 predicate signatures
    importable from `logician.gates.reflection_gates`."""

    def _assert_signature_present(self, code: str) -> None:
        fn_name = _CODE_TO_FN_NAME[code]
        self.assertTrue(
            hasattr(rg, fn_name),
            f"{code} predicate {fn_name} not importable from reflection_gates",
        )
        fn = getattr(rg, fn_name)
        self.assertTrue(callable(fn), f"{code} predicate {fn_name} is not callable")

    # BINDING (8)
    def test_no_external_signal_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-NO-EXTERNAL-SIGNAL")
    def test_eval_only_grounded_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-EVAL-ONLY-GROUNDED")
    def test_insufficient_evidence_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-INSUFFICIENT-EVIDENCE")
    def test_rfa_spec_override_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-RFA-SPEC-OVERRIDE")
    def test_depth_exceeded_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-DEPTH-EXCEEDED")
    def test_self_evaluator_family_clash_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH")
    def test_write_without_commit_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-WRITE-WITHOUT-COMMIT")
    def test_coverage_incomplete_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-COVERAGE-INCOMPLETE")
    # HORIZON (8)
    def test_intent_anchor_drift_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-INTENT-ANCHOR-DRIFT")
    def test_content_loop_detected_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-CONTENT-LOOP-DETECTED")
    def test_eval_surrogate_divergence_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-EVAL-SURROGATE-DIVERGENCE")
    def test_operator_override_mask_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-OPERATOR-OVERRIDE-MASK")
    def test_inoculation_frame_missing_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-INOCULATION-FRAME-MISSING")
    def test_self_reported_confidence_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-SELF-REPORTED-CONFIDENCE")
    def test_fabrication_on_failure_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-FABRICATION-ON-FAILURE")
    def test_probe_coverage_incomplete_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-PROBE-COVERAGE-INCOMPLETE")
    # PROBE-DEPENDENT (1)
    def test_sycophancy_loop_detected_predicate_signature_present(self):
        self._assert_signature_present("F-REFLECTION-SYCOPHANCY-LOOP-DETECTED")


# ============================================================================
# 7 — BINDING (excluding META-gate) NotImplementedError body assertions
# ============================================================================

class TestBindingPredicatesRaiseNotImplementedError(unittest.TestCase):
    """Architecture v7.0.9 §2.1 + §4 v2.x.2 §2 acceptance: 7 BINDING predicates
    (excluding F-REFLECTION-COVERAGE-INCOMPLETE which has live body) raise
    NotImplementedError when invoked at v0.1 hook.

    F-REFLECTION-COVERAGE-INCOMPLETE has its own test class below — the META-
    gate is BINDING but ACTIVE (live body) at v0.1 hook per architecture v7.0.9 §5.
    """

    def _assert_raises_not_implemented(self, code: str, *args) -> None:
        fn = getattr(rg, _CODE_TO_FN_NAME[code])
        with self.assertRaises(NotImplementedError):
            fn(*args)

    def test_no_external_signal_predicate_body_raises_not_implemented_error(self):
        self._assert_raises_not_implemented("F-REFLECTION-NO-EXTERNAL-SIGNAL", None)
    def test_eval_only_grounded_predicate_body_raises_not_implemented_error(self):
        self._assert_raises_not_implemented("F-REFLECTION-EVAL-ONLY-GROUNDED", None)
    def test_insufficient_evidence_predicate_body_raises_not_implemented_error(self):
        self._assert_raises_not_implemented("F-REFLECTION-INSUFFICIENT-EVIDENCE", None, None)
    def test_rfa_spec_override_predicate_body_raises_not_implemented_error(self):
        self._assert_raises_not_implemented("F-REFLECTION-RFA-SPEC-OVERRIDE", None, None)
    def test_depth_exceeded_predicate_body_raises_not_implemented_error(self):
        self._assert_raises_not_implemented("F-REFLECTION-DEPTH-EXCEEDED", None, 1)
    def test_self_evaluator_family_clash_predicate_body_raises_not_implemented_error(self):
        self._assert_raises_not_implemented("F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH", None, None)
    def test_write_without_commit_predicate_body_raises_not_implemented_error(self):
        self._assert_raises_not_implemented("F-REFLECTION-WRITE-WITHOUT-COMMIT", None, None)


# ============================================================================
# 1 — F-REFLECTION-COVERAGE-INCOMPLETE META-gate ACTIVE body assertion
# ============================================================================

class TestCoverageIncompleteMetaGate(unittest.TestCase):
    """Architecture v7.0.9 §5 acceptance: F-REFLECTION-COVERAGE-INCOMPLETE has
    a live body at v0.1 hook that FAIL_CLOSED when any BINDING gate's body is
    unrealized."""

    def test_coverage_incomplete_meta_gate_fires_on_missing_binding_body(self):
        outcome = rg.predicate_coverage_incomplete()
        self.assertEqual(
            outcome,
            rg.GateOutcome.FAIL_CLOSED,
            "F-REFLECTION-COVERAGE-INCOMPLETE should FAIL_CLOSED at v0.1 hook "
            "(7 BINDING predicates currently raise NotImplementedError per architecture v7.0.9 §2.1)",
        )


# ============================================================================
# 9 — HORIZON + PROBE-DEPENDENT signature-only `pass` body assertion
# ============================================================================

class TestHorizonAndProbeDependentSignatureOnly(unittest.TestCase):
    """Architecture v7.0.9 §2.2 + §2.3 acceptance: 8 HORIZON + 1 PROBE-DEPENDENT
    predicates have empty `pass` bodies (no NotImplementedError, no live
    behavior) — signature reservation only at v0.1 hook."""

    def _assert_signature_only_pass_body(self, code: str, *args) -> None:
        """A `pass` body returns None (Python's implicit return). The function
        should NOT raise and should NOT return anything other than None at v0.1 hook."""
        fn = getattr(rg, _CODE_TO_FN_NAME[code])
        result = fn(*args)
        self.assertIsNone(
            result,
            f"{code} has a `pass` body at v0.1 hook per architecture v7.0.9; "
            f"signature reserved, body lands at v0.2 SPEC or v1.x runtime",
        )

    # HORIZON (8)
    def test_intent_anchor_drift_signature_only_no_body(self):
        self._assert_signature_only_pass_body("F-REFLECTION-INTENT-ANCHOR-DRIFT", None)
    def test_content_loop_detected_signature_only_no_body(self):
        self._assert_signature_only_pass_body("F-REFLECTION-CONTENT-LOOP-DETECTED", None, None)
    def test_eval_surrogate_divergence_signature_only_no_body(self):
        self._assert_signature_only_pass_body("F-REFLECTION-EVAL-SURROGATE-DIVERGENCE", None, None)
    def test_operator_override_mask_signature_only_no_body(self):
        self._assert_signature_only_pass_body("F-REFLECTION-OPERATOR-OVERRIDE-MASK", None, None)
    def test_inoculation_frame_missing_signature_only_no_body(self):
        # Cycle-1 RT-04 closure: signature now has 3 params
        # (reflection_prompt_template, expected_digest, exact_match) — 2 have defaults.
        self._assert_signature_only_pass_body("F-REFLECTION-INOCULATION-FRAME-MISSING", None)
    def test_self_reported_confidence_signature_only_no_body(self):
        self._assert_signature_only_pass_body("F-REFLECTION-SELF-REPORTED-CONFIDENCE", "", None)
    def test_fabrication_on_failure_signature_only_no_body(self):
        self._assert_signature_only_pass_body("F-REFLECTION-FABRICATION-ON-FAILURE", None, None)
    def test_probe_coverage_incomplete_signature_only_no_body(self):
        self._assert_signature_only_pass_body("F-REFLECTION-PROBE-COVERAGE-INCOMPLETE", None)
    # PROBE-DEPENDENT (1)
    def test_sycophancy_loop_detected_signature_only_no_body(self):
        self._assert_signature_only_pass_body("F-REFLECTION-SYCOPHANCY-LOOP-DETECTED", None, None)


# ============================================================================
# 5 — F-ARCHIVIST-* sub-tag extensions present in F_ARCHIVIST_SUB_TAG_EXTENSIONS
# ============================================================================

class TestSubTagExtensionsPresent(unittest.TestCase):
    """Architecture v7.0.9 §3 + §4 v2.x.2 §5 acceptance: 5 sub-tag extensions
    on F-ARCHIVIST-* parents present in the F_ARCHIVIST_SUB_TAG_EXTENSIONS
    registry."""

    def _assert_sub_tag_present(self, parent_code: str, sub_tag: str) -> None:
        self.assertIn(
            parent_code,
            rg.F_ARCHIVIST_SUB_TAG_EXTENSIONS,
            f"Parent gate {parent_code} not in F_ARCHIVIST_SUB_TAG_EXTENSIONS",
        )
        self.assertEqual(
            rg.F_ARCHIVIST_SUB_TAG_EXTENSIONS[parent_code],
            sub_tag,
            f"Parent {parent_code} sub-tag should be {sub_tag!r}, "
            f"got {rg.F_ARCHIVIST_SUB_TAG_EXTENSIONS[parent_code]!r}",
        )

    def test_reflection_cross_org_read_present_in_parent_FORBIDDEN_SUB_TAGS(self):
        self._assert_sub_tag_present("F-ARCHIVIST-CROSS-ORG-LEAK", "reflection_cross_org_read")

    def test_reflection_attach_unsigned_present_in_parent_FORBIDDEN_SUB_TAGS(self):
        self._assert_sub_tag_present("F-ARCHIVIST-AUTO-APPLY-ATTEMPTED", "reflection_attach_unsigned")

    def test_reflection_instance_in_pattern_field_present_in_parent_FORBIDDEN_SUB_TAGS(self):
        self._assert_sub_tag_present(
            "F-ARCHIVIST-LESSON-INSTANCE-LEAK", "reflection_instance_in_pattern_field"
        )

    def test_reflection_interval_drift_present_in_parent_FORBIDDEN_SUB_TAGS(self):
        self._assert_sub_tag_present("F-ARCHIVIST-CADENCE-DRIFT", "reflection_interval_drift")

    def test_reflection_evidence_out_of_run_present_in_parent_FORBIDDEN_SUB_TAGS(self):
        self._assert_sub_tag_present(
            "F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT", "reflection_evidence_out_of_run"
        )


# ============================================================================
# 3 — Grounding-signal-class enum + frozenset assertions
# ============================================================================

class TestGroundingSignalClassRegistry(unittest.TestCase):
    """Architecture v7.0.9 §4 + §4 v2.x.2 §6 acceptance: GroundingSignalClass
    enum has the 11 members named in the canonical precedence-ordered table,
    and the PRIMARY_ELIGIBLE_CLASSES + LLM_EVAL_ONLY_CLASSES frozensets resolve
    correctly."""

    def test_grounding_signal_class_enum_has_11_members_across_8_ranks(self):
        # 11 enum members across 8 distinct ranks (rank 8 has 4 members per the
        # LLM-eval-only group). Test name renamed per Cycle-1 J-01 closure to
        # disambiguate the architecture's "Eight signal-class ranks" framing
        # from the enum's 11 named members.
        members = list(rg.GroundingSignalClass)
        self.assertEqual(
            len(members),
            11,
            "GroundingSignalClass should have 11 members "
            "(rank 1-6 = 6 + rank 7 = 1 + rank 8 = 4 LLM-eval variants)",
        )
        # Verify each named member is present by string value
        expected_values = {
            "external_funder_outcome", "operator_approval",
            "logician_gate_outcome", "kfr_drift_event", "admin_risk_event",
            "match_db_outcome", "council_split_event",
            "editor_verdict", "judge_score", "red_team_score",
            "scribe_self_assessment",
        }
        actual_values = {m.value for m in members}
        self.assertEqual(actual_values, expected_values)

    def test_primary_eligible_classes_frozenset_membership(self):
        expected = frozenset({
            rg.GroundingSignalClass.EXTERNAL_FUNDER_OUTCOME,
            rg.GroundingSignalClass.OPERATOR_APPROVAL,
            rg.GroundingSignalClass.LOGICIAN_GATE_OUTCOME,
            rg.GroundingSignalClass.KFR_DRIFT_EVENT,
            rg.GroundingSignalClass.ADMIN_RISK_EVENT,
            rg.GroundingSignalClass.MATCH_DB_OUTCOME,
        })
        self.assertEqual(rg.PRIMARY_ELIGIBLE_CLASSES, expected)

    def test_llm_eval_only_classes_frozenset_membership(self):
        expected = frozenset({
            rg.GroundingSignalClass.EDITOR_VERDICT,
            rg.GroundingSignalClass.JUDGE_SCORE,
            rg.GroundingSignalClass.RED_TEAM_SCORE,
            rg.GroundingSignalClass.SCRIBE_SELF_ASSESSMENT,
        })
        self.assertEqual(rg.LLM_EVAL_ONLY_CLASSES, expected)


# ============================================================================
# 2 — Inoculation frame body + digest assertions
# ============================================================================

class TestInoculationFrame(unittest.TestCase):
    """Architecture v7.0.9 §7 + §4 v2.x.2 §7 acceptance: operator-drafted
    inoculation frame body recorded verbatim + sha3_512 digest is stable +
    matches runtime recomputation."""

    def test_inoculation_frame_body_v1_digest_stable(self):
        recomputed = hashlib.sha3_512(rg.INOCULATION_FRAME_BODY_V1.encode("utf-8")).hexdigest()
        self.assertEqual(
            rg.INOCULATION_FRAME_BODY_V1_SHA3_512,
            recomputed,
            "INOCULATION_FRAME_BODY_V1_SHA3_512 must match the runtime-computed "
            "sha3_512 of INOCULATION_FRAME_BODY_V1; drift in the body string "
            "fails this test (architecture v7.0.9 §7 verbatim wording is load-bearing)",
        )
        self.assertEqual(
            len(rg.INOCULATION_FRAME_BODY_V1_SHA3_512),
            128,
            "sha3_512 hexdigest must be 128 hex characters",
        )

    def test_inoculation_frame_body_v1_verbatim_against_v7_0_9_section_7(self):
        # Architecture v7.0.9 §7 operator-drafted authoritative wording (verbatim).
        # Embedding the expected text here lets drift in either surface fail this test.
        expected = (
            "Reflection is permitted to improve process memory, identify recurring "
            "failure patterns, and propose safer future defaults. Reflection is not "
            "permitted to rewrite facts, override operator judgment, infer commitments, "
            "invent lessons from insufficient evidence, or treat evaluator approval as "
            "real-world success."
        )
        self.assertEqual(
            rg.INOCULATION_FRAME_BODY_V1,
            expected,
            "INOCULATION_FRAME_BODY_V1 must match the operator-drafted authoritative "
            "wording at architecture v7.0.9 §7 verbatim",
        )


# ============================================================================
# 2 — Probe registry assertions (narrowed per operator refinement Q4)
# ============================================================================

class TestProbeRegistry(unittest.TestCase):
    """Architecture v7.0.9 §6 acceptance: probe registry narrowed to three
    families per operator refinement Q4. `loop_divergence_probes` deferred
    entirely."""

    def test_required_probe_families_tuple_matches_v7_0_9_section_6(self):
        expected = (
            "sycophancy_probes",
            "proxy_metric_drift_probes",
            "fabrication_on_failure_probes",
        )
        self.assertEqual(
            rg.REQUIRED_PROBE_FAMILIES,
            expected,
            "REQUIRED_PROBE_FAMILIES must be the three-family narrowed registry "
            "per architecture v7.0.9 §6 (operator refinement Q4)",
        )

    def test_no_predicate_has_loop_divergence_probes_dependency(self):
        # Inspect every predicate's signature (parameter names + default-arg
        # values) for any binding to `loop_divergence_probes`. Documentation /
        # docstring mentions of the deferral are explicitly allowed — they're
        # the audit trail for the operator refinement Q4 decision. What's
        # forbidden is a CODE-LEVEL DEPENDENCY: a parameter named
        # `loop_divergence_probes`, a default value that contains the string
        # at runtime, or a tuple/set runtime-value that registers it.

        # 1. No predicate parameter is named `loop_divergence_probes`.
        for fn_name in _CODE_TO_FN_NAME.values():
            fn = getattr(rg, fn_name)
            sig = inspect.signature(fn)
            for param_name in sig.parameters:
                self.assertNotEqual(
                    param_name,
                    "loop_divergence_probes",
                    f"{fn_name} parameter must not be named `loop_divergence_probes` "
                    f"per operator refinement Q4 deferral (architecture v7.0.9 §6)",
                )
                # No default-arg value carries the string at runtime.
                default = sig.parameters[param_name].default
                if isinstance(default, (str, tuple, list, set, frozenset)):
                    rendered = repr(default)
                    self.assertNotIn(
                        "loop_divergence_probes",
                        rendered,
                        f"{fn_name} parameter `{param_name}` default-value must not "
                        f"reference `loop_divergence_probes` per architecture v7.0.9 §6",
                    )

        # 2. The narrowed probe registry tuple does not include the string.
        self.assertNotIn(
            "loop_divergence_probes",
            rg.REQUIRED_PROBE_FAMILIES,
            "REQUIRED_PROBE_FAMILIES must NOT include `loop_divergence_probes` "
            "per operator refinement Q4 deferral (architecture v7.0.9 §6)",
        )


# ============================================================================
# 1 — Tier-set disjoint + complete coverage assertion
# ============================================================================

class TestTierSetDiscipline(unittest.TestCase):
    """Architecture v7.0.9 §2 + §4 v2.x.2 §10 acceptance: three tier sets
    {BINDING, HORIZON, PROBE-DEPENDENT} are mutually disjoint and cover all
    17 codes."""

    def test_binding_horizon_probe_dependent_tier_disjoint(self):
        binding_set = set(BINDING_CODES)
        horizon_set = set(HORIZON_CODES)
        probe_set = set(PROBE_DEPENDENT_CODES)

        # Pairwise disjointness
        self.assertEqual(
            binding_set & horizon_set, set(),
            "BINDING ∩ HORIZON must be empty",
        )
        self.assertEqual(
            binding_set & probe_set, set(),
            "BINDING ∩ PROBE-DEPENDENT must be empty",
        )
        self.assertEqual(
            horizon_set & probe_set, set(),
            "HORIZON ∩ PROBE-DEPENDENT must be empty",
        )

        # Complete coverage — every gate in GATE_TIERS belongs to exactly one set
        union = binding_set | horizon_set | probe_set
        self.assertEqual(
            union,
            set(rg.GATE_TIERS.keys()),
            "BINDING ∪ HORIZON ∪ PROBE-DEPENDENT must equal GATE_TIERS keys",
        )

        # Count check — 8 + 8 + 1 = 17 per architecture v7.0.9 §2
        self.assertEqual(len(binding_set), 8)
        self.assertEqual(len(horizon_set), 8)
        self.assertEqual(len(probe_set), 1)
        self.assertEqual(len(union), 17)


class TestPredicateSignatureMatchesAmendmentTable(unittest.TestCase):
    """Cycle-1 NP-02 closure: predicate signatures match the §4 v2.x.2 §2/§3/§4
    amendment-table parameter declarations. Any drift in parameter names,
    parameter order, or default values fails this test before the v1.x author
    realizes the predicate body."""

    # Expected signatures per §4 v2.x.2 §2 (BINDING), §3 (HORIZON), §4
    # (PROBE-DEPENDENT). Parameter names + order + presence of default values.
    # Default values themselves are introspected separately for the constants
    # that bind to architectural-primitive layer state.
    _EXPECTED_PARAMS: dict[str, tuple[str, ...]] = {
        "predicate_no_external_signal": ("reflection_input",),
        "predicate_eval_only_grounded": ("reflection_input",),
        "predicate_insufficient_evidence": ("reflection_input", "evidence_count_threshold"),
        "predicate_rfa_spec_override": ("reflection_input", "rfa_context"),
        "predicate_depth_exceeded": ("reflection_invocation_context", "depth_cap"),
        "predicate_self_evaluator_family_clash": ("reflection_invocation_context", "router_config"),
        "predicate_write_without_commit": ("reflection_write_attempt", "journal_state"),
        "predicate_coverage_incomplete": (),
        "predicate_intent_anchor_drift": ("reflection_history", "rolling_window"),
        "predicate_content_loop_detected": ("reflection_input", "similarity_index", "threshold"),
        "predicate_eval_surrogate_divergence": ("class_7_8_ledger", "class_1_ledger", "window"),
        "predicate_operator_override_mask": ("reflection_input", "operator_pin_set"),
        # Cycle-1 RT-04 closure: predicate_inoculation_frame_missing gains
        # `exact_match: bool = True` default kwarg.
        "predicate_inoculation_frame_missing": (
            "reflection_prompt_template", "expected_digest", "exact_match",
        ),
        "predicate_self_reported_confidence": ("reflection_text", "evidence_class_counts"),
        "predicate_fabrication_on_failure": ("reflection_claimed_verdict", "gate_outcome_ledger"),
        "predicate_probe_coverage_incomplete": ("probe_registry", "required_families"),
        "predicate_sycophancy_loop_detected": ("reflection_history", "sycophancy_probes", "n_cycles"),
    }

    def test_predicate_signature_matches_amendment_table(self):
        for fn_name, expected_params in self._EXPECTED_PARAMS.items():
            fn = getattr(rg, fn_name)
            sig = inspect.signature(fn)
            actual_params = tuple(sig.parameters.keys())
            self.assertEqual(
                actual_params,
                expected_params,
                f"{fn_name} signature drift — actual params {actual_params} != "
                f"expected {expected_params} per §4 v2.x.2 amendment table",
            )

    def test_inoculation_frame_predicate_has_exact_match_default_kwarg(self):
        # Cycle-1 RT-04 closure: the `exact_match` parameter default MUST be True.
        sig = inspect.signature(rg.predicate_inoculation_frame_missing)
        self.assertIn("exact_match", sig.parameters)
        self.assertEqual(
            sig.parameters["exact_match"].default,
            True,
            "`exact_match` default value MUST be True per architecture v7.0.9 §7 "
            "+ §4 v2.x.2 §3 row 5 exact-match-semantics binding contract "
            "(Cycle-1 RT-04 closure)",
        )

    def test_inoculation_frame_predicate_expected_digest_default_binds_to_constant(self):
        sig = inspect.signature(rg.predicate_inoculation_frame_missing)
        self.assertEqual(
            sig.parameters["expected_digest"].default,
            rg.INOCULATION_FRAME_BODY_V1_SHA3_512,
            "`expected_digest` default MUST bind to INOCULATION_FRAME_BODY_V1_SHA3_512 "
            "per architecture v7.0.9 §7",
        )

    def test_probe_coverage_incomplete_predicate_required_families_default_binds_to_constant(self):
        sig = inspect.signature(rg.predicate_probe_coverage_incomplete)
        self.assertEqual(
            sig.parameters["required_families"].default,
            rg.REQUIRED_PROBE_FAMILIES,
            "`required_families` default MUST bind to REQUIRED_PROBE_FAMILIES "
            "per architecture v7.0.9 §6",
        )


class TestRequiredProbeFamiliesImmutability(unittest.TestCase):
    """Cycle-1 RT-08 closure: REQUIRED_PROBE_FAMILIES is the operator-pinned
    three-family registry per architecture v7.0.9 §6 + §6.1 immutability
    contract. Drift in either direction (addition, removal, reordering) fails
    this test — operator Ed25519 sign-off + paired-commit + lock_history row
    required for any modification."""

    def test_required_probe_families_immutable_at_v0_1_hook(self):
        expected = (
            "sycophancy_probes",
            "proxy_metric_drift_probes",
            "fabrication_on_failure_probes",
        )
        self.assertEqual(
            rg.REQUIRED_PROBE_FAMILIES,
            expected,
            "REQUIRED_PROBE_FAMILIES drift detected — operator-pinned three-family "
            "registry per architecture v7.0.9 §6 + §6.1 immutability contract "
            "requires paired-commit amendment + operator Ed25519 sign-off + "
            "lock_history row for any modification (Cycle-1 RT-08 closure)",
        )

    def test_required_probe_families_is_tuple_not_list(self):
        # Tuples are immutable at the type level; a list would be silently
        # mutable.
        self.assertIsInstance(
            rg.REQUIRED_PROBE_FAMILIES,
            tuple,
            "REQUIRED_PROBE_FAMILIES MUST be a tuple (immutable) per "
            "architecture v7.0.9 §6.1 immutability contract",
        )

    def test_required_probe_families_does_not_include_loop_divergence(self):
        # Cycle-1 RT-08 — explicit deferral check.
        self.assertNotIn(
            "loop_divergence_probes",
            rg.REQUIRED_PROBE_FAMILIES,
            "`loop_divergence_probes` MUST NOT appear in REQUIRED_PROBE_FAMILIES "
            "per operator refinement Q4 deferral + architecture v7.0.9 §6.1 contract",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
