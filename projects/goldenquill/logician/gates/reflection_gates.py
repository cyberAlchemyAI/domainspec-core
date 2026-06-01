"""F-REFLECTION-* Logician gate-family registry (v0.1 Beta hook — SCAFFOLD).

Authority sources:
- architecture v7.0.9 amendment §2 (17 F-REFLECTION-* primitives + 5 F-ARCHIVIST-*
  sub-tag extensions; BINDING-vs-HORIZON-vs-PROBE-DEPENDENT split per operator
  refinement 2026-05-10).
- §4 Logician v2.x.2 sub-amendment (predicate-signature layer realization).
- architecture v7.0.9 §4 (grounding-signal-class registry).
- architecture v7.0.9 §6 (narrowed probe registry — three families).
- architecture v7.0.9 §7 (operator-drafted inoculation frame body, verbatim).
- architecture v7.0.9 §8 (internal-vs-external naming discipline — internal name
  remains `reflection_*`; external surfaces use "Lessons Memory" et al.).

This module is the v0.1 Beta HOOK only — predicate signatures only. The 8 BINDING
predicates raise NotImplementedError (their bodies land at v1.x runtime amendment).
The 8 HORIZON predicates and the 1 PROBE-DEPENDENT predicate have `pass` bodies
(signature-only reservations until v0.2 SPEC §15 v2.x lands NotImplementedError
bodies, and v1.x runtime amendment realizes live bodies). F-REFLECTION-COVERAGE-
INCOMPLETE is the ONE BINDING predicate with a live body at v0.1 hook — it is the
META-gate dormant-binding lever per architecture v7.0.9 §5 (analog of F-CLASS-
COVERAGE-INCOMPLETE per v7.0.7 §5.1 + §4 v2.x rows 193/194).

At v0.1 Beta hook, none of these predicates are invoked by any runtime path. The
reflection_agent does not exist yet. The Reflection cadence (externally:
"Lessons Memory cadence") is dormant. This module exists so that:

1. Architecture v7.0.9 has on-disk evidence for its primitive-layer commitment
   (L-006 compliance — primitives EXIST at lock time).
2. F-REFLECTION-COVERAGE-INCOMPLETE has a live body that fires FAIL_CLOSED when
   any future v1.x deployment tries to invoke the Reflection cadence without all
   8 BINDING bodies realized.
3. The v0.2 SPEC + v1.x runtime amendment authors have a stable signature surface
   to write against.

This is NOT a runtime module. Do NOT import this from any non-test code path
without first reading architecture v7.0.9 §9 ship plan.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# ============================================================================
# Module versioning + amendment cross-references
# ============================================================================

AMENDMENT_VERSION: str = "v7.0.9"
AMENDMENT_FILED: str = "2026-05-10"
PARENT_LOCK_ROW_ARCHITECTURE: int = 180  # v7.0.7 F-CLASS-* dormant-primitive precedent
PARENT_LOCK_ROW_BLUEPRINT: int = 193     # §4 v2.x F-CLASS-COVERAGE-INCOMPLETE precedent
PARENT_LOCK_ROW_SUB_TAG_EXTENSION: int = 198  # §4 v2.x.1 sub-tag-extension precedent


# ============================================================================
# Tier labels — BINDING / HORIZON / PROBE-DEPENDENT
# ============================================================================

class GateTier(str, Enum):
    """Three-tier classification of F-REFLECTION-* primitives at v0.1 Beta hook.

    BINDING:           predicate signature + body realized at v0.1 hook (body =
                       NotImplementedError except F-REFLECTION-COVERAGE-INCOMPLETE
                       which has a live body). v1.x runtime amendment realizes
                       the NotImplementedError bodies.
    HORIZON:           predicate signature reserved at v0.1 hook (body = `pass`).
                       v0.2 SPEC §15 v2.x lands NotImplementedError body.
                       v1.x runtime realizes live body.
    PROBE_DEPENDENT:   predicate signature reserved at v0.1 hook (body = `pass`).
                       Body realizes when the corresponding probe family ships at
                       v1.x runtime per architecture v7.0.9 §6 narrowed registry.
    """
    BINDING = "binding"
    HORIZON = "horizon"
    PROBE_DEPENDENT = "probe_dependent"


# ============================================================================
# Grounding-signal-class registry (architecture v7.0.9 §4)
# ============================================================================

class GroundingSignalClass(str, Enum):
    """Eight signal classes per architecture v7.0.9 §4, precedence-ordered.

    Highest authority (rank 1) → lowest (rank 8).
    F-REFLECTION-NO-EXTERNAL-SIGNAL fail-closes when the set is empty.
    F-REFLECTION-EVAL-ONLY-GROUNDED fail-closes when the set is a subset of
    {EDITOR_VERDICT, JUDGE_SCORE, RED_TEAM_SCORE, SCRIBE_SELF_ASSESSMENT}.
    At least one of classes 1-6 must be present per the precedence rule.
    Class 7 (COUNCIL_SPLIT_EVENT) is admitted only with class-1-6 corroboration.
    """
    # Rank 1 — highest authority
    EXTERNAL_FUNDER_OUTCOME = "external_funder_outcome"
    # Rank 2
    OPERATOR_APPROVAL = "operator_approval"
    # Rank 3
    LOGICIAN_GATE_OUTCOME = "logician_gate_outcome"
    # Rank 4
    KFR_DRIFT_EVENT = "kfr_drift_event"
    # Rank 5
    ADMIN_RISK_EVENT = "admin_risk_event"
    # Rank 6
    MATCH_DB_OUTCOME = "match_db_outcome"
    # Rank 7 — NOT primary alone (admitted only with class-1-6 corroboration)
    COUNCIL_SPLIT_EVENT = "council_split_event"
    # Rank 8 — NEVER primary alone (F-REFLECTION-EVAL-ONLY-GROUNDED fail-closes)
    EDITOR_VERDICT = "editor_verdict"
    JUDGE_SCORE = "judge_score"
    RED_TEAM_SCORE = "red_team_score"
    SCRIBE_SELF_ASSESSMENT = "scribe_self_assessment"


PRIMARY_ELIGIBLE_CLASSES: frozenset[GroundingSignalClass] = frozenset({
    GroundingSignalClass.EXTERNAL_FUNDER_OUTCOME,
    GroundingSignalClass.OPERATOR_APPROVAL,
    GroundingSignalClass.LOGICIAN_GATE_OUTCOME,
    GroundingSignalClass.KFR_DRIFT_EVENT,
    GroundingSignalClass.ADMIN_RISK_EVENT,
    GroundingSignalClass.MATCH_DB_OUTCOME,
})
"""Rank 1-6 — at least one must be present for a reflection to pass
F-REFLECTION-NO-EXTERNAL-SIGNAL + F-REFLECTION-EVAL-ONLY-GROUNDED."""

COUNCIL_SPLIT_CLASS: GroundingSignalClass = GroundingSignalClass.COUNCIL_SPLIT_EVENT
"""Rank 7 — admitted only with class-1-6 corroboration; never primary alone."""

LLM_EVAL_ONLY_CLASSES: frozenset[GroundingSignalClass] = frozenset({
    GroundingSignalClass.EDITOR_VERDICT,
    GroundingSignalClass.JUDGE_SCORE,
    GroundingSignalClass.RED_TEAM_SCORE,
    GroundingSignalClass.SCRIBE_SELF_ASSESSMENT,
})
"""Rank 8 — F-REFLECTION-EVAL-ONLY-GROUNDED fail-closes when the set ⊆ this."""


# ============================================================================
# Narrowed probe registry (architecture v7.0.9 §6)
# ============================================================================

REQUIRED_PROBE_FAMILIES: tuple[str, ...] = (
    "sycophancy_probes",
    "proxy_metric_drift_probes",
    "fabrication_on_failure_probes",
)
"""Three-family probe registry per architecture v7.0.9 §6 (operator refinement Q4).

NOT in the registry: `loop_divergence_probes` — deferred entirely per operator
rationale "insufficient reflection volume in v0.2 to make it meaningful."
v1.x runtime amendment may re-evaluate if reflection volume crosses the
meaningful-measurability threshold; until then, F-REFLECTION-CONTENT-LOOP-DETECTED
(HORIZON) uses similarity-index substrate alone, not probe-based detection.

F-REFLECTION-PROBE-COVERAGE-INCOMPLETE (HORIZON) checks against this tuple.
v1.x deployment shipping all three families realized clears the gate.
"""


# ============================================================================
# Operator-drafted inoculation frame body (architecture v7.0.9 §7 + §4 v2.x.2 §7)
# ============================================================================

# Verbatim operator-drafted wording per architecture v7.0.9 §7.
# UTF-8, LF line endings, no trailing whitespace, no BOM.
# Body is single-paragraph; line breaks in source are for readability and are
# joined by Python's adjacent-string-literal concatenation — the final string
# value has no embedded newlines.
INOCULATION_FRAME_BODY_V1: str = (
    "Reflection is permitted to improve process memory, identify recurring "
    "failure patterns, and propose safer future defaults. Reflection is not "
    "permitted to rewrite facts, override operator judgment, infer commitments, "
    "invent lessons from insufficient evidence, or treat evaluator approval as "
    "real-world success."
)

# Computed once at module load. The test
# `test_inoculation_frame_body_v1_digest_stable` asserts this constant is
# present + computed correctly; drift in the body string above is caught at
# import time (the digest changes) and at test collection (the assertion fails).
INOCULATION_FRAME_BODY_V1_SHA3_512: str = hashlib.sha3_512(
    INOCULATION_FRAME_BODY_V1.encode("utf-8")
).hexdigest()


# ============================================================================
# Gate outcome (minimal v0.1-hook scaffold; full GateOutcome lives at §4 v2.x)
# ============================================================================

class GateOutcome(str, Enum):
    """Three-valued outcome for v0.1 hook scaffold purposes.

    The v0.1 Beta hook does NOT invoke gates at runtime. This minimal scaffold
    exists so the F-REFLECTION-COVERAGE-INCOMPLETE META-gate's live body has a
    return-value vocabulary. v1.x runtime amendment may replace this with the
    full §4 v2.x GateOutcome dataclass + failure-code emission machinery.
    """
    PASS = "pass"
    FAIL_CLOSED = "fail_closed"
    NOT_APPLICABLE = "not_applicable"


# ============================================================================
# Type placeholders (full schemas land at v0.2 SPEC §15 v2.x)
# ============================================================================

# These are intentionally Any-typed at v0.1 hook because the v0.2 SPEC amendment
# is the authority for ReflectionInput / RFAContext / ReflectionInvocationContext
# / etc. Concrete dataclasses with frozen=True kw_only=True land at v0.2 SPEC.
# At v0.1 hook these names just need to be *importable* so the predicate
# signatures resolve.
ReflectionInput = Any
RFAContext = Any
ReflectionInvocationContext = Any
RouterConfig = Any
ReflectionWriteAttempt = Any
JournalState = Any
ReflectionHistory = Any
SimilarityIndex = Any
EvalLedger = Any
FunderOutcomeLedger = Any
OperatorPinSet = Any
ReflectionPromptTemplate = Any
EvidenceClassCounts = Any
ReflectionVerdict = Any
GateOutcomeLedger = Any
ProbeRegistry = Any
SycophancyProbes = Any
EvidenceCountThreshold = Any


# ============================================================================
# Gate-realization registry (META-gate dependency)
# ============================================================================

# Registry of all 17 F-REFLECTION-* primitives at v0.1 hook with their tier label.
# F-REFLECTION-COVERAGE-INCOMPLETE inspects this registry's BINDING entries.
# Order matters for test introspection — keep BINDING set first (rows 1-8 of
# architecture v7.0.9 §2.1), then HORIZON (§2.2), then PROBE-DEPENDENT (§2.3).
_BINDING_F_REFLECTION_CODES: tuple[str, ...] = (
    "F-REFLECTION-NO-EXTERNAL-SIGNAL",
    "F-REFLECTION-EVAL-ONLY-GROUNDED",
    "F-REFLECTION-INSUFFICIENT-EVIDENCE",
    "F-REFLECTION-RFA-SPEC-OVERRIDE",
    "F-REFLECTION-DEPTH-EXCEEDED",
    "F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH",
    "F-REFLECTION-WRITE-WITHOUT-COMMIT",
    "F-REFLECTION-COVERAGE-INCOMPLETE",
)

_HORIZON_F_REFLECTION_CODES: tuple[str, ...] = (
    "F-REFLECTION-INTENT-ANCHOR-DRIFT",
    "F-REFLECTION-CONTENT-LOOP-DETECTED",
    "F-REFLECTION-EVAL-SURROGATE-DIVERGENCE",
    "F-REFLECTION-OPERATOR-OVERRIDE-MASK",
    "F-REFLECTION-INOCULATION-FRAME-MISSING",
    "F-REFLECTION-SELF-REPORTED-CONFIDENCE",
    "F-REFLECTION-FABRICATION-ON-FAILURE",
    "F-REFLECTION-PROBE-COVERAGE-INCOMPLETE",
)

_PROBE_DEPENDENT_F_REFLECTION_CODES: tuple[str, ...] = (
    "F-REFLECTION-SYCOPHANCY-LOOP-DETECTED",
)


# ============================================================================
# F-ARCHIVIST-* sub-tag extensions (5 — additive entries; parent gate owns body)
# ============================================================================

# These five sub-tag entries land in the parent gate's FORBIDDEN_SUB_TAGS table.
# At v0.1 hook the parent gate's predicate body is unchanged (LOCKed at §4 v2.x
# rows 193/194); sub-tag entries are purely declarative. The reflection_agent
# (v1.x scope) wires invocations to surface these sub-tag attributions when the
# parent gate fires on a reflection-attributable path.
F_ARCHIVIST_SUB_TAG_EXTENSIONS: dict[str, str] = {
    # parent_failure_code → sub_tag
    "F-ARCHIVIST-CROSS-ORG-LEAK": "reflection_cross_org_read",
    "F-ARCHIVIST-AUTO-APPLY-ATTEMPTED": "reflection_attach_unsigned",
    "F-ARCHIVIST-LESSON-INSTANCE-LEAK": "reflection_instance_in_pattern_field",
    "F-ARCHIVIST-CADENCE-DRIFT": "reflection_interval_drift",
    "F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT": "reflection_evidence_out_of_run",
}


# ============================================================================
# BINDING predicates (7 — NotImplementedError bodies + 1 ACTIVE META-gate body)
# ============================================================================

def predicate_no_external_signal(reflection_input: ReflectionInput) -> GateOutcome:
    """F-REFLECTION-NO-EXTERNAL-SIGNAL — PRE-write.

    BINDING (v0.1 hook NotImplementedError; v1.x runtime body).

    Fail-closed when reflection_input.grounding_signal_classes is an empty set.
    At v1.x runtime: body inspects the field-presence + emptiness via the
    GroundingSignalClass enum + PRIMARY_ELIGIBLE_CLASSES frozenset.

    See architecture v7.0.9 §2.1 row 1 + §4 grounding-signal-class registry.
    Drift test: tests/logician/gates/test_reflection_no_external_signal_body_drift.py
        ::test_signature_matches_v7_0_9_row_1
    """
    raise NotImplementedError(
        "F-REFLECTION-NO-EXTERNAL-SIGNAL body lands at v1.x runtime per "
        "architecture v7.0.9 §2.1 row 1; signature reserved + "
        "grounding_signal_classes field-presence semantic registered at v0.1 hook"
    )


def predicate_eval_only_grounded(reflection_input: ReflectionInput) -> GateOutcome:
    """F-REFLECTION-EVAL-ONLY-GROUNDED — PRE-write.

    BINDING (v0.1 hook NotImplementedError; v1.x runtime body).

    Fail-closed when grounding_signal_classes ⊆ LLM_EVAL_ONLY_CLASSES.

    See architecture v7.0.9 §2.1 row 2 + §4 precedence rule.
    Drift test: tests/logician/gates/test_reflection_eval_only_grounded_body_drift.py
        ::test_signature_matches_v7_0_9_row_2
    """
    raise NotImplementedError(
        "F-REFLECTION-EVAL-ONLY-GROUNDED body lands at v1.x runtime per "
        "architecture v7.0.9 §2.1 row 2; signature reserved + "
        "grounding_signal_classes set-membership semantic registered at v0.1 hook"
    )


def predicate_insufficient_evidence(
    reflection_input: ReflectionInput,
    evidence_count_threshold: EvidenceCountThreshold,
) -> GateOutcome:
    """F-REFLECTION-INSUFFICIENT-EVIDENCE — PRE-write.

    BINDING (v0.1 hook NotImplementedError; v1.x runtime body).

    Fail-closed when reflection generalizes from < N independent grant cycles.
    Defaults: 3 per-funder, 2 per-CIC, 5 per-CLC. Operator-configurable at
    white-glove onboarding.

    See architecture v7.0.9 §2.1 row 3.
    Drift test: tests/logician/gates/test_reflection_insufficient_evidence_body_drift.py
        ::test_signature_matches_v7_0_9_row_3
    """
    raise NotImplementedError(
        "F-REFLECTION-INSUFFICIENT-EVIDENCE body lands at v1.x runtime per "
        "architecture v7.0.9 §2.1 row 3; signature reserved + "
        "evidence-count threshold semantic registered at v0.1 hook "
        "(default 3 per-funder, 2 per-CIC, 5 per-CLC)"
    )


def predicate_rfa_spec_override(
    reflection_input: ReflectionInput,
    rfa_context: RFAContext,
) -> GateOutcome:
    """F-REFLECTION-RFA-SPEC-OVERRIDE — PRE-write.

    BINDING (v0.1 hook NotImplementedError; v1.x runtime body).

    Fail-closed when reflection text asserts funder intent / RFA scope not
    present in original RFA + PROJECT_CONTEXT. Substrate scan = string-match +
    Law-4 admin-risk-term scanner.

    See architecture v7.0.9 §2.1 row 4 + §7 inoculation frame body.
    Drift test: tests/logician/gates/test_reflection_rfa_spec_override_body_drift.py
        ::test_signature_matches_v7_0_9_row_4
    """
    raise NotImplementedError(
        "F-REFLECTION-RFA-SPEC-OVERRIDE body lands at v1.x runtime per "
        "architecture v7.0.9 §2.1 row 4; signature reserved + "
        "RFA-substrate-scan + Law-4 admin-risk-term semantic registered at v0.1 hook"
    )


def predicate_depth_exceeded(
    reflection_invocation_context: ReflectionInvocationContext,
    depth_cap: int,
) -> GateOutcome:
    """F-REFLECTION-DEPTH-EXCEEDED — PRE-fire.

    BINDING (v0.1 hook NotImplementedError; v1.x runtime body).

    Fail-closed when reflection-of-reflection depth exceeds bound. Hard cap
    depth-1 at v0.2 (no reflection on a reflection); v1.x configurable.

    See architecture v7.0.9 §2.1 row 5.
    Drift test: tests/logician/gates/test_reflection_depth_exceeded_body_drift.py
        ::test_signature_matches_v7_0_9_row_5
    """
    raise NotImplementedError(
        "F-REFLECTION-DEPTH-EXCEEDED body lands at v1.x runtime per "
        "architecture v7.0.9 §2.1 row 5; signature reserved + depth-counter "
        "semantic registered at v0.1 hook (hard cap depth-1 at v0.2; v1.x configurable)"
    )


def predicate_self_evaluator_family_clash(
    reflection_invocation_context: ReflectionInvocationContext,
    router_config: RouterConfig,
) -> GateOutcome:
    """F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH — PRE-fire.

    BINDING (v0.1 hook NotImplementedError; v1.x runtime body).

    Fail-closed when reflection critic and reflection author share model family
    per router.yaml family field comparison. Extends A3 cross-family rigor.

    See architecture v7.0.9 §2.1 row 6.
    Drift test: tests/logician/gates/test_reflection_self_evaluator_family_clash_body_drift.py
        ::test_signature_matches_v7_0_9_row_6
    """
    raise NotImplementedError(
        "F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH body lands at v1.x runtime per "
        "architecture v7.0.9 §2.1 row 6; signature reserved + router.yaml "
        "family-field-comparison semantic registered at v0.1 hook; "
        "extends A3 cross-family rigor"
    )


def predicate_write_without_commit(
    reflection_write_attempt: ReflectionWriteAttempt,
    journal_state: JournalState,
) -> GateOutcome:
    """F-REFLECTION-WRITE-WITHOUT-COMMIT — COMMIT.

    BINDING (v0.1 hook NotImplementedError; v1.x runtime body).

    Fail-closed when reflection write attempted outside output_validator-success
    → commit path. Mirrors §12 Uploader prepare-and-stage discipline.

    See architecture v7.0.9 §2.1 row 7.
    Drift test: tests/logician/gates/test_reflection_write_without_commit_body_drift.py
        ::test_signature_matches_v7_0_9_row_7
    """
    raise NotImplementedError(
        "F-REFLECTION-WRITE-WITHOUT-COMMIT body lands at v1.x runtime per "
        "architecture v7.0.9 §2.1 row 7; signature reserved + "
        "journal/commit-pattern semantic registered at v0.1 hook "
        "(mirrors §12 Uploader prepare-and-stage discipline)"
    )


# F-REFLECTION-COVERAGE-INCOMPLETE — the ONE BINDING predicate with a live body.
# This is the META-gate dormant-binding lever per architecture v7.0.9 §5.

_PREDICATE_FUNCTIONS: dict[str, Callable[..., GateOutcome]]  # forward declaration


def _binding_predicate_has_realized_body(code: str) -> bool:
    """Inspect a BINDING predicate's body and return True iff the body is
    realized (i.e., does NOT raise NotImplementedError on a trivial probe call).

    F-REFLECTION-COVERAGE-INCOMPLETE itself is excluded from the inspection
    set — it's the inspector, not an inspectee.
    """
    if code == "F-REFLECTION-COVERAGE-INCOMPLETE":
        return True  # self-exclusion; the META-gate is always considered realized
    fn = _PREDICATE_FUNCTIONS.get(code)
    if fn is None:
        return False
    # Probe call with sentinel inputs; any NotImplementedError means body
    # has not been realized.
    try:
        # Call with all-None positional args using inspect to count params.
        import inspect
        sig = inspect.signature(fn)
        args = [None] * len(sig.parameters)
        fn(*args)
    except NotImplementedError:
        return False
    except Exception:
        # Body exists but rejects the sentinel input — body is realized.
        return True
    return True


def predicate_coverage_incomplete() -> GateOutcome:
    """F-REFLECTION-COVERAGE-INCOMPLETE — META PRE-cycle.

    BINDING (ACTIVE body at v0.1 hook — META-gate dormant-binding lever).

    Returns FAIL_CLOSED at every cycle attempting Reflection cadence with any
    of the 7 NotImplementedError-bodied BINDING gates lacking realized body.
    Returns PASS only when every BINDING predicate's body is realized (i.e.,
    v1.x runtime amendment has LOCKed and replaced the NotImplementedError
    bodies with live bodies).

    At v0.1 Beta hook, all 7 NotImplementedError-bodied BINDING predicates DO
    raise NotImplementedError, so this gate fires FAIL_CLOSED at every cycle
    start — which is correct: v1.x Beta deployment cannot run Reflection
    cadence until v1.x runtime amendment LOCKs. v0.1 Beta deployment is NOT
    affected because v0.1 Beta does not invoke the Reflection cadence at all.

    Analog of F-CLASS-COVERAGE-INCOMPLETE per v7.0.7 §5.1 + §4 v2.x rows 193/194.
    See architecture v7.0.9 §5.
    """
    for code in _BINDING_F_REFLECTION_CODES:
        if not _binding_predicate_has_realized_body(code):
            return GateOutcome.FAIL_CLOSED
    return GateOutcome.PASS


# ============================================================================
# HORIZON predicates (8 — signature-only `pass` bodies at v0.1 hook)
# ============================================================================

def predicate_intent_anchor_drift(
    reflection_history: ReflectionHistory,
    rolling_window: int = 5,
) -> GateOutcome:
    """F-REFLECTION-INTENT-ANCHOR-DRIFT — POST-write META.

    HORIZON. SIGNATURE-ONLY at v0.1 hook; body lands at v0.2 SPEC §15 v2.x
    (NotImplementedError) and at v1.x runtime (live body).

    See architecture v7.0.9 §2.2 row 1.
    """
    pass  # SIGNATURE-ONLY at v0.1 hook; do not invoke


def predicate_content_loop_detected(
    reflection_input: ReflectionInput,
    similarity_index: SimilarityIndex,
    threshold: float = 0.85,
) -> GateOutcome:
    """F-REFLECTION-CONTENT-LOOP-DETECTED — POST-write.

    HORIZON. SIGNATURE-ONLY at v0.1 hook.

    See architecture v7.0.9 §2.2 row 2.
    """
    pass  # SIGNATURE-ONLY at v0.1 hook; do not invoke


def predicate_eval_surrogate_divergence(
    class_7_8_ledger: EvalLedger,
    class_1_ledger: FunderOutcomeLedger,
    window: int = 8,
) -> GateOutcome:
    """F-REFLECTION-EVAL-SURROGATE-DIVERGENCE — META cycle-level.

    HORIZON. SIGNATURE-ONLY at v0.1 hook.

    See architecture v7.0.9 §2.2 row 3.
    """
    pass  # SIGNATURE-ONLY at v0.1 hook; do not invoke


def predicate_operator_override_mask(
    reflection_input: ReflectionInput,
    operator_pin_set: OperatorPinSet,
) -> GateOutcome:
    """F-REFLECTION-OPERATOR-OVERRIDE-MASK — PRE-write.

    HORIZON. SIGNATURE-ONLY at v0.1 hook.

    See architecture v7.0.9 §2.2 row 4.
    """
    pass  # SIGNATURE-ONLY at v0.1 hook; do not invoke


def predicate_inoculation_frame_missing(
    reflection_prompt_template: ReflectionPromptTemplate,
    expected_digest: str = INOCULATION_FRAME_BODY_V1_SHA3_512,
    exact_match: bool = True,
) -> GateOutcome:
    """F-REFLECTION-INOCULATION-FRAME-MISSING — PRE-fire (template).

    HORIZON. SIGNATURE-ONLY at v0.1 hook. The expected_digest default value
    binds against the operator-drafted authoritative wording per architecture
    v7.0.9 §7. The `exact_match: bool = True` default kwarg (Cycle-1 RT-04
    closure) locks the v1.x body to exact-match hash semantics: the body MUST
    compute `hash = sha3_512(full_prompt.encode("utf-8")).hexdigest()` and
    assert `hash == INOCULATION_FRAME_BODY_V1_SHA3_512` — substring /
    containment checks fail closed. v1.x runtime amendment realizes the body.

    See architecture v7.0.9 §2.2 row 5 + §7 inoculation frame body + §4 v2.x.2
    §3 row 5.
    """
    pass  # SIGNATURE-ONLY at v0.1 hook; do not invoke


def predicate_self_reported_confidence(
    reflection_text: str,
    evidence_class_counts: EvidenceClassCounts,
) -> GateOutcome:
    """F-REFLECTION-SELF-REPORTED-CONFIDENCE — POST-write (rewrites).

    HORIZON. SIGNATURE-ONLY at v0.1 hook.

    See architecture v7.0.9 §2.2 row 6.
    """
    pass  # SIGNATURE-ONLY at v0.1 hook; do not invoke


def predicate_fabrication_on_failure(
    reflection_claimed_verdict: ReflectionVerdict,
    gate_outcome_ledger: GateOutcomeLedger,
) -> GateOutcome:
    """F-REFLECTION-FABRICATION-ON-FAILURE — POST-effect.

    HORIZON. SIGNATURE-ONLY at v0.1 hook. Realized as part of
    `fabrication_on_failure_probes` per architecture v7.0.9 §6.

    See architecture v7.0.9 §2.2 row 7.
    """
    pass  # SIGNATURE-ONLY at v0.1 hook; do not invoke


def predicate_probe_coverage_incomplete(
    probe_registry: ProbeRegistry,
    required_families: tuple[str, ...] = REQUIRED_PROBE_FAMILIES,
) -> GateOutcome:
    """F-REFLECTION-PROBE-COVERAGE-INCOMPLETE — META pre-cycle deployment.

    HORIZON. SIGNATURE-ONLY at v0.1 hook. The required_families default binds
    to the three-family narrowed registry per architecture v7.0.9 §6.

    See architecture v7.0.9 §2.2 row 8.
    """
    pass  # SIGNATURE-ONLY at v0.1 hook; do not invoke


# ============================================================================
# PROBE-DEPENDENT predicates (1 — signature-only `pass` body at v0.1 hook)
# ============================================================================

def predicate_sycophancy_loop_detected(
    reflection_history: ReflectionHistory,
    sycophancy_probes: SycophancyProbes,
    n_cycles: int = 4,
) -> GateOutcome:
    """F-REFLECTION-SYCOPHANCY-LOOP-DETECTED — META cycle-level.

    PROBE-DEPENDENT. SIGNATURE-ONLY at v0.1 hook. Body realizes when the
    `sycophancy_probes` family ships at v1.x runtime per architecture v7.0.9 §6.

    See architecture v7.0.9 §2.3 row 1.
    """
    pass  # SIGNATURE-ONLY at v0.1 hook; do not invoke


# ============================================================================
# Predicate registry — backward-binding for META-gate inspection
# ============================================================================

_PREDICATE_FUNCTIONS = {
    "F-REFLECTION-NO-EXTERNAL-SIGNAL": predicate_no_external_signal,
    "F-REFLECTION-EVAL-ONLY-GROUNDED": predicate_eval_only_grounded,
    "F-REFLECTION-INSUFFICIENT-EVIDENCE": predicate_insufficient_evidence,
    "F-REFLECTION-RFA-SPEC-OVERRIDE": predicate_rfa_spec_override,
    "F-REFLECTION-DEPTH-EXCEEDED": predicate_depth_exceeded,
    "F-REFLECTION-SELF-EVALUATOR-FAMILY-CLASH": predicate_self_evaluator_family_clash,
    "F-REFLECTION-WRITE-WITHOUT-COMMIT": predicate_write_without_commit,
    "F-REFLECTION-COVERAGE-INCOMPLETE": predicate_coverage_incomplete,
    "F-REFLECTION-INTENT-ANCHOR-DRIFT": predicate_intent_anchor_drift,
    "F-REFLECTION-CONTENT-LOOP-DETECTED": predicate_content_loop_detected,
    "F-REFLECTION-EVAL-SURROGATE-DIVERGENCE": predicate_eval_surrogate_divergence,
    "F-REFLECTION-OPERATOR-OVERRIDE-MASK": predicate_operator_override_mask,
    "F-REFLECTION-INOCULATION-FRAME-MISSING": predicate_inoculation_frame_missing,
    "F-REFLECTION-SELF-REPORTED-CONFIDENCE": predicate_self_reported_confidence,
    "F-REFLECTION-FABRICATION-ON-FAILURE": predicate_fabrication_on_failure,
    "F-REFLECTION-PROBE-COVERAGE-INCOMPLETE": predicate_probe_coverage_incomplete,
    "F-REFLECTION-SYCOPHANCY-LOOP-DETECTED": predicate_sycophancy_loop_detected,
}


GATE_TIERS: dict[str, GateTier] = {
    **{c: GateTier.BINDING for c in _BINDING_F_REFLECTION_CODES},
    **{c: GateTier.HORIZON for c in _HORIZON_F_REFLECTION_CODES},
    **{c: GateTier.PROBE_DEPENDENT for c in _PROBE_DEPENDENT_F_REFLECTION_CODES},
}


# ============================================================================
# Public-API exports
# ============================================================================

__all__ = [
    "AMENDMENT_VERSION",
    "AMENDMENT_FILED",
    "GateTier",
    "GateOutcome",
    "GroundingSignalClass",
    "PRIMARY_ELIGIBLE_CLASSES",
    "COUNCIL_SPLIT_CLASS",
    "LLM_EVAL_ONLY_CLASSES",
    "REQUIRED_PROBE_FAMILIES",
    "INOCULATION_FRAME_BODY_V1",
    "INOCULATION_FRAME_BODY_V1_SHA3_512",
    "F_ARCHIVIST_SUB_TAG_EXTENSIONS",
    "GATE_TIERS",
    # 17 predicate functions
    "predicate_no_external_signal",
    "predicate_eval_only_grounded",
    "predicate_insufficient_evidence",
    "predicate_rfa_spec_override",
    "predicate_depth_exceeded",
    "predicate_self_evaluator_family_clash",
    "predicate_write_without_commit",
    "predicate_coverage_incomplete",
    "predicate_intent_anchor_drift",
    "predicate_content_loop_detected",
    "predicate_eval_surrogate_divergence",
    "predicate_operator_override_mask",
    "predicate_inoculation_frame_missing",
    "predicate_self_reported_confidence",
    "predicate_fabrication_on_failure",
    "predicate_probe_coverage_incomplete",
    "predicate_sycophancy_loop_detected",
]
