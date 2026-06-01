"""Gate-runner state machine + 13-step POST-gate capstone. [§4.2 + §4.4 + §4.4.1]

Round 6 capstone — the entry point Section 5 wires for PRE / POST gate
invocations. Composes:

* :func:`pipeline.logician.pre_gate.run_pre_gate` (§4.2.1 18-check sequence).
* The §4.4.1 13-step POST-gate sequence, delegating artifact assembly to
  Round 2's :func:`pipeline.logician.post_gate.run_post_gate_skeleton`.
* The state-machine invariant from §4.2.3 (PRE → BETWEEN → POST → DONE) so
  that any mid-loop Section 4 call raises ``F-PRE-19``.

The runner is a class-with-state (one instance per pipeline run). Each
``run_pre_gate`` / ``run_post_gate`` call advances the state machine and is
rejected if the current state is wrong. After ``run_post_gate`` completes
(success or fail) the state transitions to ``DONE`` and the runner cannot be
re-used. A re-drafted POST is a new runner instance.

The runner does NOT perform any I/O. Callers (Section 5 orchestrator) supply
pre-computed inputs derived from Section 1 / Section 2 / Section 3 primitives
and from the per-round Section 4 verifiers (Rounds 1-5).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from pipeline.logician.types import gate_should_block

from pipeline.logician.claim_evidence import ClaimEntry, ClaimEvidenceMap
from pipeline.logician.post_gate import (
    F_POST_10,
    F_POST_11,
    PostGateResult,
    run_post_gate_skeleton,
)
from pipeline.logician.pre_gate import (
    F_PRE_19_LOGICIAN_MID_LOOP_CALL,
    PreGateInput,
    PreGateResult,
    run_pre_gate,
)


# ---------------------------------------------------------------------------
# Failure-code constants (§6.2 + §6.5)
# ---------------------------------------------------------------------------


F_POST_01_DRAFT_NOT_READY: str = "F-POST-01.draft_not_ready"
F_POST_01_DRAFT_SIGNAL_UNSIGNED: str = "F-POST-01.draft_signal_unsigned"
F_POST_02_PRE_INVARIANT_DRIFT: str = "F-POST-02.pre_invariant_drift"
F_POST_03_CLAIM_EXTRACTION_FAILED: str = "F-POST-03.claim_extraction_failed"
F_POST_12_VAULT_WRITE_FAILED: str = "F-POST-12.vault_write_failed"
F_POST_14_CLAIM_EVIDENCE_VERSION_COLLISION: str = (
    "F-POST-14.claim_evidence_version_collision"
)


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------


STATE_PRE: str = "PRE"
STATE_BETWEEN: str = "BETWEEN"
STATE_POST: str = "POST"
STATE_DONE: str = "DONE"

VALID_STATES: frozenset[str] = frozenset(
    {STATE_PRE, STATE_BETWEEN, STATE_POST, STATE_DONE}
)


class LogicianMidLoopCall(RuntimeError):
    """Raised when run_pre_gate / run_post_gate is invoked mid-loop.

    Carries failure code ``F-PRE-19`` per §4.2.3 secondary enforcement.
    """

    code: str = F_PRE_19_LOGICIAN_MID_LOOP_CALL

    def __init__(self, current_state: str, attempted_transition: str) -> None:
        super().__init__(
            f"{F_PRE_19_LOGICIAN_MID_LOOP_CALL}: cannot transition "
            f"{current_state!r} -> {attempted_transition!r}"
        )
        self.current_state = current_state
        self.attempted_transition = attempted_transition


# ---------------------------------------------------------------------------
# POST-gate input + per-step outcome shapes
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class PostGateStepOutcome:
    """One step's outcome in the §4.4.1 13-step sequence."""

    step_number: int
    step_name: str
    passed: bool
    failure_code: Optional[str]
    failure_detail: str


POST_GATE_STEP_NAMES: dict[int, str] = {
    1: "draft_ready_signal_signed",
    2: "pre_invariants_still_hold",
    3: "claim_extraction_succeeded",
    4: "source_tag_verification",
    5: "dossier_s11c_bt11_verification",
    6: "admin_risk_term_scan",
    7: "structural_compliance",
    8: "rigor_breach_enumeration",
    9: "claim_evidence_map_assembled",
    10: "rails_report_assembled",
    11: "lessons_delta_assembled",
    12: "vault_write_atomic",
    13: "section_5_signal_emitted",
}

POST_GATE_STEP_ORDER: tuple[int, ...] = tuple(range(1, 14))


@dataclass(frozen=True, kw_only=True)
class PostGateInput:
    """Aggregate input to :meth:`LogicianGateRunner.run_post_gate`.

    Steps 1, 2, 3, 7, 12, 13 are evaluated by the caller (Section 5 / Section 1
    / Section 2 primitives) and supplied as pre-computed step outcomes via
    ``caller_step_outcomes``. Step 4 (source-tag) is run upstream (Round 3's
    ``source_tag_verify`` pre-classifies each claim's tag); the orchestrator
    reads ``ClaimEntry.tag`` to surface step 4's outcome. Step 5 (dossier
    verify) is run upstream by the caller composing Round 5's
    ``verify_dossier_cite`` per cited dossier; the caller passes the resulting
    failure-code list. Step 6 reduces to the M8 hard-block count from Round 1.
    Steps 8-11 are status-bearing artefacts the caller pre-assembles. Step 12
    is the vault-write outcome.
    """

    # Caller-evaluated steps (1, 2, 3, 7, 8, 10, 11, 12, 13)
    caller_step_outcomes: dict[int, PostGateStepOutcome]

    # Step 4 — claims pre-classified by Round 3 source_tag_verify
    draft_hash: str
    rfa_hash: str
    session_id: str
    org_slug: str
    rfa_url_hash: str
    claims: tuple[ClaimEntry, ...]
    generated_at_utc: str

    # Step 5 — dossier verify failure codes per claim (Round 5 verify_dossier_cite)
    dossier_verify_failure_codes: tuple[str, ...] = ()

    # Step 6 — admin-risk hard-block count (Round 1 verify_admin_risk_ledger surface)
    admin_risk_hard_block_count: int = 0

    # Step 8 — rigor-breach flag presence
    rigor_breach_active: bool = False


@dataclass(frozen=True, kw_only=True)
class GateRunnerPostResult:
    """Aggregate result of running the POST-gate sequence."""

    passed: bool
    failed_step_number: Optional[int]
    failure_code: Optional[str]
    failure_detail: str
    failure_codes: tuple[str, ...]
    completed_steps: tuple[PostGateStepOutcome, ...]
    claim_evidence_map: Optional[ClaimEvidenceMap]
    underlying_post_gate_result: Optional[PostGateResult]


# ---------------------------------------------------------------------------
# Step taxonomies
# ---------------------------------------------------------------------------


_CALLER_PROVIDED_STEPS: frozenset[int] = frozenset(
    {1, 2, 3, 7, 8, 10, 11, 12, 13}
)
_INLINE_STEPS: frozenset[int] = frozenset({4, 5, 6, 9})


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LogicianGateRunner:
    """Per-run state machine. Single PRE invocation, single POST invocation.

    Frozen dataclass closes finding (c) of §4 Logician Group 7 Batch A
    committee dispatch (gpt_oss F-1 HIGH; L-005 narrow-fix landed 2026-04-29).
    A non-frozen dataclass exposed ``state`` as a publicly-mutable field so a
    caller could reset ``runner.state = "PRE"`` after ``state == "DONE"`` and
    re-fire ``run_pre_gate``, bypassing the F-PRE-19 mid-loop guard. With
    frozen=True, every state transition routes through ``object.__setattr__``
    inside the documented transition methods (``mark_between`` / ``run_pre_gate``
    / ``run_post_gate``); external mutation raises ``dataclasses.FrozenInstanceError``.
    """

    state: str = STATE_PRE
    pre_gate_result: Optional[PreGateResult] = None
    post_gate_result: Optional[GateRunnerPostResult] = None

    def __post_init__(self) -> None:
        if self.state not in VALID_STATES:
            raise ValueError(
                f"state must be one of {sorted(VALID_STATES)}, got {self.state!r}"
            )

    def mark_between(self) -> None:
        """Section 5 calls this after PRE-gate PASS, before mid-loop work begins."""

        if self.state != STATE_PRE:
            raise LogicianMidLoopCall(self.state, STATE_BETWEEN)
        if self.pre_gate_result is None or not self.pre_gate_result.passed:
            raise RuntimeError(
                "mark_between requires a PASS pre_gate_result; current state "
                "transitioned without successful PRE-gate"
            )
        object.__setattr__(self, "state", STATE_BETWEEN)

    def run_pre_gate(self, input_: PreGateInput) -> PreGateResult:
        if self.state != STATE_PRE:
            raise LogicianMidLoopCall(self.state, STATE_PRE)
        result = run_pre_gate(input_)
        object.__setattr__(self, "pre_gate_result", result)
        if not result.passed:
            object.__setattr__(self, "state", STATE_DONE)
        return result

    def run_post_gate(self, input_: PostGateInput) -> GateRunnerPostResult:
        if self.state != STATE_BETWEEN:
            raise LogicianMidLoopCall(self.state, STATE_POST)
        object.__setattr__(self, "state", STATE_POST)
        result = self._execute_post_gate(input_)
        object.__setattr__(self, "post_gate_result", result)
        object.__setattr__(self, "state", STATE_DONE)
        return result

    # ------------------------------------------------------------------ POST

    def _execute_post_gate(self, input_: PostGateInput) -> GateRunnerPostResult:
        if not isinstance(input_, PostGateInput):
            raise TypeError("input_ must be PostGateInput")
        # Validate caller_step_outcomes shape
        for step_num in _CALLER_PROVIDED_STEPS:
            if step_num not in input_.caller_step_outcomes:
                raise ValueError(
                    f"caller_step_outcomes is missing required step #{step_num} "
                    f"({POST_GATE_STEP_NAMES[step_num]!r})"
                )
            outcome = input_.caller_step_outcomes[step_num]
            if not isinstance(outcome, PostGateStepOutcome):
                raise TypeError(
                    f"caller_step_outcomes[{step_num}] must be PostGateStepOutcome"
                )
            if outcome.step_number != step_num:
                raise ValueError(
                    f"caller_step_outcomes[{step_num}].step_number is "
                    f"{outcome.step_number}, must match key"
                )

        completed: list[PostGateStepOutcome] = []
        failure_codes: list[str] = []
        first_failure_step: Optional[int] = None
        first_failure_code: Optional[str] = None
        first_failure_detail: str = ""
        underlying: Optional[PostGateResult] = None
        cmap: Optional[ClaimEvidenceMap] = None

        for step_num in POST_GATE_STEP_ORDER:
            if step_num in _CALLER_PROVIDED_STEPS:
                outcome = input_.caller_step_outcomes[step_num]
            elif step_num == 4:
                outcome = self._evaluate_step_4_source_tag(input_.claims)
            elif step_num == 5:
                outcome = self._evaluate_step_5_dossier(
                    input_.dossier_verify_failure_codes
                )
            elif step_num == 6:
                outcome = self._evaluate_step_6_admin_risk(
                    input_.admin_risk_hard_block_count
                )
            elif step_num == 9:
                # Step 9 invokes Round 2's run_post_gate_skeleton which
                # produces both the ClaimEvidenceMap and the F-POST-10 /
                # F-POST-11 hard-floor predicates. Steps 4 and 6 above are
                # surface-level pre-checks; step 9 is the authoritative
                # artifact-assembly + predicate evaluation.
                underlying = run_post_gate_skeleton(
                    draft_hash=input_.draft_hash,
                    rfa_hash=input_.rfa_hash,
                    session_id=input_.session_id,
                    org_slug=input_.org_slug,
                    rfa_url_hash=input_.rfa_url_hash,
                    claims=input_.claims,
                    rigor_breach_active=input_.rigor_breach_active,
                    admin_risk_hard_block_count=input_.admin_risk_hard_block_count,
                    generated_at_utc=input_.generated_at_utc,
                )
                cmap = underlying.claim_evidence_map
                if not gate_should_block(underlying):
                    outcome = _step_outcome(9, None, "")
                else:
                    # Surface every Round-2 failure code into the aggregate
                    # list; pick the first as the step-9 failure_code.
                    detail = (
                        f"unsourced_count={underlying.unsourced_count}, "
                        f"hard_block_count={underlying.hard_block_count}"
                    )
                    primary = underlying.failure_codes[0]
                    outcome = _step_outcome(9, primary, detail)
                    for fc in underlying.failure_codes:
                        if fc not in failure_codes:
                            failure_codes.append(fc)
            else:  # pragma: no cover — exhaustive
                raise AssertionError(f"unhandled step number {step_num}")

            completed.append(outcome)

            if gate_should_block(outcome):
                if outcome.failure_code and outcome.failure_code not in failure_codes:
                    failure_codes.append(outcome.failure_code)
                if first_failure_step is None:
                    first_failure_step = step_num
                    first_failure_code = outcome.failure_code
                    first_failure_detail = outcome.failure_detail

        return GateRunnerPostResult(
            passed=first_failure_step is None,
            failed_step_number=first_failure_step,
            failure_code=first_failure_code,
            failure_detail=first_failure_detail,
            failure_codes=tuple(failure_codes),
            completed_steps=tuple(completed),
            claim_evidence_map=cmap,
            underlying_post_gate_result=underlying,
        )

    # ------------------------------------------------------------------ steps

    def _evaluate_step_4_source_tag(
        self, claims: tuple[ClaimEntry, ...]
    ) -> PostGateStepOutcome:
        if not isinstance(claims, tuple):
            raise TypeError("claims must be tuple of ClaimEntry")
        unsourced = sum(1 for c in claims if c.tag == "UNSOURCED")
        if unsourced > 0:
            return _step_outcome(
                4,
                F_POST_11,
                f"{unsourced} claim(s) classified UNSOURCED at source-tag verification",
            )
        return _step_outcome(4, None, "")

    def _evaluate_step_5_dossier(
        self, failure_codes: tuple[str, ...]
    ) -> PostGateStepOutcome:
        if not isinstance(failure_codes, tuple):
            raise TypeError("dossier_verify_failure_codes must be tuple")
        if failure_codes:
            return _step_outcome(
                5,
                failure_codes[0],
                f"dossier verify failed: {list(failure_codes)}",
            )
        return _step_outcome(5, None, "")

    def _evaluate_step_6_admin_risk(self, hard_block_count: int) -> PostGateStepOutcome:
        if not isinstance(hard_block_count, int) or hard_block_count < 0:
            raise ValueError("admin_risk_hard_block_count must be non-negative int")
        if hard_block_count > 0:
            return _step_outcome(
                6,
                F_POST_10,
                f"{hard_block_count} unresolved 🔴 admin-risk hard-block term(s)",
            )
        return _step_outcome(6, None, "")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _step_outcome(
    step_number: int, code: Optional[str], detail: str
) -> PostGateStepOutcome:
    return PostGateStepOutcome(
        step_number=step_number,
        step_name=POST_GATE_STEP_NAMES[step_number],
        passed=code is None,
        failure_code=code,
        failure_detail=detail,
    )


__all__ = [
    "F_POST_01_DRAFT_NOT_READY",
    "F_POST_01_DRAFT_SIGNAL_UNSIGNED",
    "F_POST_02_PRE_INVARIANT_DRIFT",
    "F_POST_03_CLAIM_EXTRACTION_FAILED",
    "F_POST_12_VAULT_WRITE_FAILED",
    "F_POST_14_CLAIM_EVIDENCE_VERSION_COLLISION",
    "STATE_PRE",
    "STATE_BETWEEN",
    "STATE_POST",
    "STATE_DONE",
    "VALID_STATES",
    "POST_GATE_STEP_NAMES",
    "POST_GATE_STEP_ORDER",
    "LogicianMidLoopCall",
    "PostGateStepOutcome",
    "PostGateInput",
    "GateRunnerPostResult",
    "LogicianGateRunner",
]
