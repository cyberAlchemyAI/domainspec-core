"""PRE-gate orchestrator — strict-order 18-check sequence. [§4.2 + §4.2.1]

Round 6 capstone. Pure-function leaf composing predicates from earlier rounds:

* Check #4 + #17 — :mod:`pipeline.logician.cedar_eval` (Round 6).
* Check #10 — :func:`pipeline.logician.admin_risk.verify_admin_risk_ledger`
  (Round 1) caller-invoked; this orchestrator consumes the pre-computed
  :class:`MonotonicityResult`.
* Check #14 — dossier signoff presence walk (caller assembles the
  ``(entity_slug, has_signoff)`` tuples by reading via Section 2
  ``vault_read(intent="dossier-signoff-read")``).
* Check #15 — corpus completeness regex over PROJECT_CONTEXT.md.
* Checks #1, #2, #3, #5, #6, #7, #8, #9, #11, #12, #13, #16, #18 — caller
  supplies pre-computed :class:`CheckOutcome` per check from Section 1 / 2 / 3
  primitives that this Round 6 module does not import directly (keeps
  ``pre_gate.py`` a pure leaf testable without filesystem coupling).

Strict-order semantics: per §4.2.1 ("each check in the list below must pass
before the next runs"), the orchestrator short-circuits at the first failure.
The result includes the list of completed-check outcomes so rails-report
assembly (Round 6 ``gate_runner.py``) can render them.

Mid-loop call rejection (§4.2.3 / `F-PRE-19`) is a state-machine concern
owned by ``gate_runner.py``; this module only enforces the 18-check sequence.

Scope note — v2.1 rows 19/20 deferred. Blueprint §4.2.1 v2.1 adds row 19
(``F-PRE-INDEX-STALE``, partner with §2 Vault `index_amendment` ledger) and
row 20 (``F-PRE-CROSS-ORG-READ``, declared-intent Cedar check, partner with
the §4.13 cross_org_guard runtime predicate). v0.1 substrate enforces those
two predicates at their own anchors — index-staleness via §2 Vault
admin-risk-ledger emit, cross-org via :func:`pipeline.logician.cedar_eval.
evaluate_cross_org_dossier` plus seat-side caller-supplied checks (§7
Scribe / §8 Editor / §9 Judge LOCKED wiring). Threading them as inline
checks #19/#20 inside this orchestrator is a v0.2 work item; per §4.2.1
("Adding a 19th check is a Section 4 blueprint amendment, not a quiet
insertion at implementation time.") the inline-thread requires a v0.2
amendment round, not an implementation-time edit.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable, Optional

from pipeline.logician.types import gate_should_block

from pipeline.logician.cedar_eval import (
    CedarPolicy,
    F_PRE_04_CEDAR_UNSIGNED,
    F_PRE_04_LEDGER_MISMATCH,
    F_PRE_17_CEDAR_COMPILE_ERROR,
    compile_cedar_policy,
    verify_cedar_policy_signed,
)
from pipeline.logician.dossier_verify import F_PRE_14_DOSSIER_UNSIGNED


# ---------------------------------------------------------------------------
# Failure-code constants (§6.1)
# ---------------------------------------------------------------------------


F_PRE_01_LOCK_MISSING: str = "F-PRE-01.section_2_lock_missing"
F_PRE_01_LOCK_UNSIGNED: str = "F-PRE-01.section_2_lock_unsigned"
F_PRE_01_LOCK_LEDGER_MISMATCH: str = "F-PRE-01.section_2_lock_ledger_mismatch"

F_PRE_02_ROUTER_UNSIGNED: str = "F-PRE-02.router_yaml_unsigned"
F_PRE_02_ROUTER_SIG_INVALID: str = "F-PRE-02.router_yaml_signature_invalid"

F_PRE_03_VAULT_SHARED_SEED_UNSIGNED: str = "F-PRE-03.vault_shared_seed_unsigned"

F_PRE_05_WRAPPER_HASH_MISMATCH: str = "F-PRE-05.wrapper_hash_mismatch"
F_PRE_05_WRAPPER_SIG_INVALID: str = "F-PRE-05.wrapper_signature_invalid"

F_PRE_06_TRUST_ROOT_UNSIGNED: str = "F-PRE-06.trust_root_unsigned"
F_PRE_06_TRUST_ROOT_INODE_MISMATCH: str = "F-PRE-06.trust_root_inode_mismatch"
F_PRE_06_TRUST_ROOT_MOUNT_OVER: str = "F-PRE-06.trust_root_mount_over_detected"

F_PRE_07_RFA_HASH_MISSING: str = "F-PRE-07.rfa_hash_missing"
F_PRE_07_RFA_HASH_INVALID: str = "F-PRE-07.rfa_hash_invalid"
F_PRE_07_RFA_UNSIGNED: str = "F-PRE-07.rfa_unsigned"

F_PRE_08_SESSION_UNBOUND: str = "F-PRE-08.session_unbound"
F_PRE_08_PROJECT_CONTEXT_ORG_MISMATCH: str = "F-PRE-08.project_context_org_mismatch"

F_PRE_09_BYOK_KEY_WRONG_ORG: str = "F-PRE-09.byok_key_wrong_org"
F_PRE_09_BYOK_KEY_MISSING: str = "F-PRE-09.byok_key_missing"

F_PRE_10_ADMIN_RISK_NON_MONOTONIC: str = "F-PRE-10.admin_risk_non_monotonic"
F_PRE_10_ADMIN_RISK_CHAIN_BREAK: str = "F-PRE-10.admin_risk_chain_break"
F_PRE_10_ADMIN_RISK_REPLAYED_SEQ_ID: str = "F-PRE-10.admin_risk_replayed_seq_id"

F_PRE_11_RLIMIT_CORE_NONZERO: str = "F-PRE-11.rlimit_core_nonzero"
F_PRE_11_STDIO_NOT_NULL: str = "F-PRE-11.stdio_not_null"

F_PRE_12_HEALTH_TUPLE_MALFORMED: str = "F-PRE-12.health_tuple_malformed"
F_PRE_12_HEALTH_TUPLE_SIG_INVALID: str = "F-PRE-12.health_tuple_signature_invalid"
F_PRE_12_HEALTH_ABORT_THRESHOLD: str = "F-PRE-12.health_tuple_abort_threshold_reached"

F_PRE_13_VOLUME_UUID_ABSENT: str = "F-PRE-13.volume_uuid_absent"

F_PRE_15_CORPUS_INCOMPLETE: str = "F-PRE-15.corpus_incomplete"

F_PRE_16_INTERRUPTED_UNSOURCED_UNRESOLVED: str = (
    "F-PRE-16.interrupted_unsourced_unresolved"
)

F_PRE_18_SCOUT_PRE_VERIFY_UNSIGNED: str = "F-PRE-18.scout_pre_verify_unsigned"

F_PRE_19_LOGICIAN_MID_LOOP_CALL: str = "F-PRE-19.logician_mid_loop_call"


# Ordered tuple of the 18 check numbers. Adding a 19th check is a blueprint
# amendment per §4.2.1 ("Adding a nineteenth check is a Section 4 blueprint
# amendment, not a quiet insertion at implementation time.").
PRE_GATE_CHECK_ORDER: tuple[int, ...] = tuple(range(1, 19))

PRE_GATE_CHECK_NAMES: dict[int, str] = {
    1: "section_2_lock_marker",
    2: "router_yaml_signed",
    3: "vault_shared_seeds_signed",
    4: "cedar_policy_signed",
    5: "process_wrapper_signed",
    6: "trust_root_mirror_intact",
    7: "rfa_dual_hash_signed",
    8: "session_org_root_bound",
    9: "byok_key_scoped",
    10: "admin_risk_ledger_intact",
    11: "rlimits_inherited",
    12: "scout_health_tuple_signed",
    13: "volume_uuid_stable",
    14: "dossier_signoffs_present",
    15: "corpus_complete",
    16: "no_unresolved_interrupted_unsourced",
    17: "cedar_policy_compiles",
    18: "scout_pre_verify_signed",
}


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class CheckOutcome:
    """Result of one PRE-gate check.

    ``failure_code`` is None on PASS; on FAIL it carries the F-PRE-NN.* code.
    """

    check_number: int
    check_name: str
    passed: bool
    failure_code: Optional[str]
    failure_detail: str


@dataclass(frozen=True, kw_only=True)
class PreGateResult:
    """Aggregate result of running the PRE-gate sequence."""

    passed: bool
    failed_check_number: Optional[int]
    failure_code: Optional[str]
    failure_detail: str
    completed_checks: tuple[CheckOutcome, ...]


# ---------------------------------------------------------------------------
# Per-check predicate helpers (inline-evaluated checks)
# ---------------------------------------------------------------------------


def _outcome(check_number: int, code: Optional[str], detail: str) -> CheckOutcome:
    name = PRE_GATE_CHECK_NAMES[check_number]
    return CheckOutcome(
        check_number=check_number,
        check_name=name,
        passed=code is None,
        failure_code=code,
        failure_detail=detail,
    )


def evaluate_check_15_corpus_complete(project_context_text: str) -> CheckOutcome:
    """Check #15 — PROJECT_CONTEXT.md must contain zero ``[NEEDED]`` tokens."""

    if not isinstance(project_context_text, str):
        raise TypeError("project_context_text must be str")
    matches = re.findall(r"\[NEEDED\]", project_context_text)
    if matches:
        return _outcome(
            15,
            F_PRE_15_CORPUS_INCOMPLETE,
            f"{len(matches)} [NEEDED] token(s) present in PROJECT_CONTEXT.md",
        )
    return _outcome(15, None, "")


def evaluate_check_17_cedar_policy_compiles(policy: CedarPolicy) -> CheckOutcome:
    """Check #17 — Cedar ``org_isolation`` policy compiles."""

    ok, detail = compile_cedar_policy(policy)
    if not ok:
        return _outcome(17, F_PRE_17_CEDAR_COMPILE_ERROR, detail)
    return _outcome(17, None, "")


def evaluate_check_04_cedar_policy_signed(
    policy: CedarPolicy,
    *,
    expected_ledger_head: str,
    signature_verifier: Callable[[CedarPolicy], bool],
) -> CheckOutcome:
    """Check #4 — Cedar policy file signed + M15 ledger entry present.

    ``signature_verifier`` is REQUIRED (Section 1 keyring callable); passing
    ``None`` violates the §4.2.1 row 4 fail-closed mandate (per
    :func:`pipeline.logician.cedar_eval.verify_cedar_policy_signed`).
    """

    code = verify_cedar_policy_signed(
        policy,
        expected_ledger_head=expected_ledger_head,
        signature_verifier=signature_verifier,
    )
    if code is None:
        return _outcome(4, None, "")
    if code == F_PRE_04_CEDAR_UNSIGNED:
        return _outcome(4, code, f"policy {policy.name!r} signature missing or invalid")
    if code == F_PRE_04_LEDGER_MISMATCH:
        return _outcome(
            4,
            code,
            f"policy {policy.name!r} m15_ledger_head does not match expected head",
        )
    return _outcome(4, code, "cedar policy verification failed")


def evaluate_check_14_dossier_signoffs_present(
    dossier_signoff_states: tuple[tuple[str, bool], ...],
) -> CheckOutcome:
    """Check #14 — every cited DOC_SOURCED entity dossier has an operator sign-off.

    ``dossier_signoff_states`` is a tuple of ``(entity_slug, has_signoff)``
    tuples assembled by the caller from Section 2 ``vault_read`` of each cited
    dossier's signoff JSON.
    """

    if not isinstance(dossier_signoff_states, tuple):
        raise TypeError("dossier_signoff_states must be tuple")
    unsigned = sorted(slug for slug, signed in dossier_signoff_states if not signed)
    if unsigned:
        return _outcome(
            14,
            F_PRE_14_DOSSIER_UNSIGNED,
            f"unsigned dossiers: {unsigned}",
        )
    return _outcome(14, None, "")


def evaluate_check_10_admin_risk_ledger(
    *,
    ok: bool,
    sub_failure_code: Optional[str],
    failure_detail: str,
) -> CheckOutcome:
    """Check #10 — admin-risk ledger integrity.

    Caller pre-computes ``ok`` + ``sub_failure_code`` via Round 1's
    :func:`pipeline.logician.admin_risk.verify_admin_risk_ledger` (which
    raises ``AdminRiskMonotonicityFailed`` carrying ``sub_tag``). The caller
    converts the ``sub_tag`` to a ``F-PRE-10.<sub_tag>`` code (or maps from
    Round 1's exposed sub-tag set) and passes it here.
    """

    if ok:
        return _outcome(10, None, "")
    return _outcome(10, sub_failure_code, failure_detail)


# Caller-provided outcomes ---------------------------------------------------
#
# Checks 1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 16, 18 are evaluated by the
# caller (Section 1 / Section 2 / Section 3 primitives) and supplied as
# pre-computed ``CheckOutcome`` instances. The orchestrator validates the
# check_number matches and feeds them into the strict-order sequence.

_CALLER_PROVIDED_CHECK_NUMBERS: frozenset[int] = frozenset(
    {1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 16, 18}
)

_INLINE_CHECK_NUMBERS: frozenset[int] = frozenset({4, 10, 14, 15, 17})


# ---------------------------------------------------------------------------
# PreGateInput + orchestrator
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class PreGateInput:
    """Aggregate input to :func:`run_pre_gate`.

    Caller-provided checks (1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 16, 18) are
    each supplied as a :class:`CheckOutcome` via ``caller_outcomes``, keyed by
    check number. Inline checks (4, 10, 14, 15, 17) consume the typed fields
    below.
    """

    caller_outcomes: dict[int, CheckOutcome]

    # Check #4 + #17 — Cedar policy
    cedar_policy: CedarPolicy
    cedar_expected_ledger_head: str
    # REQUIRED — passing None at runtime triggers TypeError in
    # cedar_eval.verify_cedar_policy_signed per §4.2.1 row 4 fail-closed mandate.
    cedar_signature_verifier: Callable[[CedarPolicy], bool]

    # Check #10 — Admin-risk ledger
    admin_risk_ok: bool
    admin_risk_sub_failure_code: Optional[str]
    admin_risk_failure_detail: str

    # Check #14 — Dossier signoffs
    dossier_signoff_states: tuple[tuple[str, bool], ...]

    # Check #15 — PROJECT_CONTEXT.md text
    project_context_text: str


def run_pre_gate(input_: PreGateInput) -> PreGateResult:
    """Run the §4.2.1 18-check sequence in strict order; short-circuit on first FAIL.

    Returns :class:`PreGateResult` with ``passed=True`` on full sequence pass
    or ``passed=False`` carrying the failed-check number + failure code +
    detail. ``completed_checks`` carries every outcome up to and including
    the failure (or all 18 on PASS).
    """

    if not isinstance(input_, PreGateInput):
        raise TypeError("input_ must be PreGateInput")

    # Validate caller_outcomes shape
    for check_num in _CALLER_PROVIDED_CHECK_NUMBERS:
        if check_num not in input_.caller_outcomes:
            raise ValueError(
                f"caller_outcomes is missing required check #{check_num} "
                f"({PRE_GATE_CHECK_NAMES[check_num]!r})"
            )
        outcome = input_.caller_outcomes[check_num]
        if not isinstance(outcome, CheckOutcome):
            raise TypeError(
                f"caller_outcomes[{check_num}] must be CheckOutcome"
            )
        if outcome.check_number != check_num:
            raise ValueError(
                f"caller_outcomes[{check_num}].check_number is "
                f"{outcome.check_number}, must match key"
            )

    completed: list[CheckOutcome] = []

    for check_num in PRE_GATE_CHECK_ORDER:
        if check_num in _CALLER_PROVIDED_CHECK_NUMBERS:
            outcome = input_.caller_outcomes[check_num]
        elif check_num == 4:
            outcome = evaluate_check_04_cedar_policy_signed(
                input_.cedar_policy,
                expected_ledger_head=input_.cedar_expected_ledger_head,
                signature_verifier=input_.cedar_signature_verifier,
            )
        elif check_num == 10:
            outcome = evaluate_check_10_admin_risk_ledger(
                ok=input_.admin_risk_ok,
                sub_failure_code=input_.admin_risk_sub_failure_code,
                failure_detail=input_.admin_risk_failure_detail,
            )
        elif check_num == 14:
            outcome = evaluate_check_14_dossier_signoffs_present(
                input_.dossier_signoff_states
            )
        elif check_num == 15:
            outcome = evaluate_check_15_corpus_complete(input_.project_context_text)
        elif check_num == 17:
            outcome = evaluate_check_17_cedar_policy_compiles(input_.cedar_policy)
        else:  # pragma: no cover — exhaustive
            raise AssertionError(f"unhandled check number {check_num}")

        completed.append(outcome)

        if gate_should_block(outcome):
            return PreGateResult(
                passed=False,
                failed_check_number=check_num,
                failure_code=getattr(outcome, "failure_code", None),
                failure_detail=getattr(outcome, "failure_detail", ""),
                completed_checks=tuple(completed),
            )

    return PreGateResult(
        passed=True,
        failed_check_number=None,
        failure_code=None,
        failure_detail="",
        completed_checks=tuple(completed),
    )


__all__ = [
    "F_PRE_01_LOCK_MISSING",
    "F_PRE_01_LOCK_UNSIGNED",
    "F_PRE_01_LOCK_LEDGER_MISMATCH",
    "F_PRE_02_ROUTER_UNSIGNED",
    "F_PRE_02_ROUTER_SIG_INVALID",
    "F_PRE_03_VAULT_SHARED_SEED_UNSIGNED",
    "F_PRE_05_WRAPPER_HASH_MISMATCH",
    "F_PRE_05_WRAPPER_SIG_INVALID",
    "F_PRE_06_TRUST_ROOT_UNSIGNED",
    "F_PRE_06_TRUST_ROOT_INODE_MISMATCH",
    "F_PRE_06_TRUST_ROOT_MOUNT_OVER",
    "F_PRE_07_RFA_HASH_MISSING",
    "F_PRE_07_RFA_HASH_INVALID",
    "F_PRE_07_RFA_UNSIGNED",
    "F_PRE_08_SESSION_UNBOUND",
    "F_PRE_08_PROJECT_CONTEXT_ORG_MISMATCH",
    "F_PRE_09_BYOK_KEY_WRONG_ORG",
    "F_PRE_09_BYOK_KEY_MISSING",
    "F_PRE_10_ADMIN_RISK_NON_MONOTONIC",
    "F_PRE_10_ADMIN_RISK_CHAIN_BREAK",
    "F_PRE_10_ADMIN_RISK_REPLAYED_SEQ_ID",
    "F_PRE_11_RLIMIT_CORE_NONZERO",
    "F_PRE_11_STDIO_NOT_NULL",
    "F_PRE_12_HEALTH_TUPLE_MALFORMED",
    "F_PRE_12_HEALTH_TUPLE_SIG_INVALID",
    "F_PRE_12_HEALTH_ABORT_THRESHOLD",
    "F_PRE_13_VOLUME_UUID_ABSENT",
    "F_PRE_15_CORPUS_INCOMPLETE",
    "F_PRE_16_INTERRUPTED_UNSOURCED_UNRESOLVED",
    "F_PRE_18_SCOUT_PRE_VERIFY_UNSIGNED",
    "F_PRE_19_LOGICIAN_MID_LOOP_CALL",
    "PRE_GATE_CHECK_ORDER",
    "PRE_GATE_CHECK_NAMES",
    "CheckOutcome",
    "PreGateResult",
    "PreGateInput",
    "evaluate_check_04_cedar_policy_signed",
    "evaluate_check_10_admin_risk_ledger",
    "evaluate_check_14_dossier_signoffs_present",
    "evaluate_check_15_corpus_complete",
    "evaluate_check_17_cedar_policy_compiles",
    "run_pre_gate",
]
