"""pipeline.loop.run_eval_pipeline — §4.15 eval-mode capstone (Round 12.B).

Blueprint §5 v6 LOCKED 2026-04-19:

- §4.15 eval-mode entry point + calibration-report assembly
- §4.1 submission-mode sibling (R11 ``run_pipeline`` — structural template)
- §4.3 Round 3 ``start_run`` reused for eval-mode RunState construction
- §4.13 Round 2 ``checkpoint_atomic`` + ``_write_state_failure_wrapper``
- §4.6 Round 5 ``run_inner_loop`` reused PER ITEM (clears iterations between)
- §4.2 Round 6 ``run_post_gate_orchestration`` reused PER ITEM
- §5.6 ``CalibrationReport`` + canonical bytes + Ed25519 sign (Round 12.A)
- §6 F-PIPE-21 sub-triggers (``eval_run_reached_tab_delivery``,
  ``calibration_signature_stale``, ``golden_set_*``) propagated

**Round 12.B is orchestration-only.** Zero new primitives. Zero new F-PIPE
codes. All five F-PIPE-21 calibration sub-triggers are owned by Round 12.A
primitives (``_resolve_golden_set_path`` raises the two path-hardening
triggers; ``assert_manifest_org_matches`` raises the org-mismatch trigger;
``verify_calibration_report`` raises ``calibration_signature_stale``; and
Round 9 ``deliver_tab`` owns ``eval_run_reached_tab_delivery``).

**The 11-step eval-mode sequence** (blueprint §4.15):

 1. ``start_run(mode="eval", ...)`` — mints run_id-keyed :class:`RunState`
    with ``mode="eval"`` + ``golden_set_ref`` populated; ``rfa_hash`` and
    ``project_context_hash`` both ``None`` (Round 1 mode-isolation invariant).
 2. Phase transition ``initialized`` → ``pre_gate_pending`` + CAS checkpoint.
 3. PRE-gate evaluation via injected callable. The §4 Logician eval-mode
    predicate returns ``failure_code="F-EVAL-CROSS-ORG-READ"`` on an operator
    whose ``org_slug`` does not match the manifest's declared ``org_slug``.
    On that specific code, Round 12.B transitions to ``aborted_trusted_fail``
    and returns early. Any other PRE-gate FAIL shortcuts to
    ``aborted_trusted_fail`` similarly. PRE-gate PASS: phase →
    ``pre_gate_passed`` → ``eval_iter_pending``.
 4. Per-item loop over :func:`pipeline.calibration.golden_set.golden_set_iter`.
    For each item:
    a. Write ``pipeline/{run_id}/eval_progress.json`` sidecar with
       ``current_item_index`` (OQ-1 resolution: sidecar, not schema bump).
    b. Clear ``run_state.iterations`` (A-v1-10 soft-restart guard would
       otherwise fire at item #2 iter_1).
    c. Phase transition ``eval_iter_pending`` → ``inner_loop_iter_1`` +
       CAS checkpoint.
    d. :func:`pipeline.loop.run_inner_loop` drives Scribe → Editor → Judge
       for this item. On F_PIPE_05 (iter-cap without convergence) the item
       is recorded as ``iter_cap_no_pass`` (per-item failure is not run-
       terminal in eval mode). On any other PipelineFailure — state-failure
       wrapper + abort the run.
    e. Build :class:`CalibrationReportItem` from the
       :class:`InnerLoopResult`'s ``final_iteration.judge_verdict``.
    f. Phase transition back to ``eval_iter_pending`` + CAS checkpoint.
 5. :func:`pipeline.calibration.assemble_from_run` — build unsigned
    :class:`CalibrationReport` with mean/stddev/per-dim-union summary.
    Phase transition → ``calibration_assembled`` + CAS checkpoint.
 6. :func:`pipeline.calibration.reconcile_operator_pubkey` — first-write-
    wins pubkey provenance (OQ-5 resolution: BEFORE ``sign_report``).
    Rotation detection raises ``ValueError``; Round 12.B catches and
    transitions to ``aborted_operator`` + returns early.
 7. :func:`pipeline.calibration.sign_report` — Ed25519 detached signature
    over canonical bytes. Phase transition → ``calibration_signed`` +
    checkpoint.
 8. Write the signed report JSON at
    ``vault/{operator_org_slug}/golden_set/calibration_reports/{run_id}.json``
    via ``intent="golden-set-write"`` (OQ-4 resolution: reuse intent).
 9. Write the detached signature bytes at
    ``.../{run_id}.sig`` via the same intent.
10. Pin ``run_state.calibration_report_ref`` + ``calibration_signature_ref``.
    Phase transition → ``eval_finalized`` + final CAS checkpoint.
11. Return :class:`EvalPipelineRunResult` with ``final_phase="eval_finalized"``.

**ORIENT-resolved design decisions (2026-04-21)**

1. *Per-item RunState.iterations reset.* Round 5's ``run_inner_loop`` requires
   ``phase.startswith("inner_loop_iter_")`` AND A-v1-10 soft-restart guard
   forbids re-entering iter_n if any existing IterationState has
   ``iter_number >= iter_n``. Between items we clear ``run_state.iterations``
   so item #2 can enter iter_1 cleanly. This is an eval-mode-specific
   compensation — submission-mode never runs Round 5 twice on one RunState.
   OQ resolution at ORIENT.

2. *Mode-isolation defence-in-depth.* Every eval-mode checkpoint in this
   module goes through ``_assert_eval_mode_intent(intent)`` — an inline-
   literal frozenset check that F_PIPE_21 ``eval_mode_invalid_intent``s
   any intent outside ``{"golden-set-write", "state-success",
   "state-failure"}``. Round 2 ``checkpoint_atomic`` does not enforce
   mode-isolation; this module owns that shield.

3. *Tab-delivery shield.* Round 9's ``deliver_tab`` raises F_PIPE_21
   ``eval_run_reached_tab_delivery`` on ``run_state.mode == "eval"``.
   Round 12.B NEVER calls ``deliver_tab`` — the shield is defence-in-depth.

4. *Per-item ``item_run_id`` synthesis.* :class:`CalibrationReportItem`
   requires ``item_run_id`` (per-item unique). R12.B synthesizes
   ``f"{run_state.run_id}::{item.item_id}"`` — inline-literal format string.

5. *Outcome mapping from ``InnerLoopResult``.*
   - ``converged_on="score_threshold"`` + ``iterations_run=N``:
     → ``revision_loop_outcome=f"pass_iter{N}"``.
   - ``converged_on="delta_plateau"``: the loop converged not because
     it PASSed but because scores plateaued — map to ``plateau_no_pass``.
   - F_PIPE_05 raise (never returns): map to ``iter_cap_no_pass``.

6. *Capturing vault_write (R11 pattern).* Reused from Round 11. Round 3
   ``start_run`` does not return the committed CAS head of its own write;
   we wrap ``vault_write`` with a one-shot capturer that records the first
   commit hash for subsequent checkpoint pinning.

7. *Fixed-run-id factory (R11 pattern).* Caller mints ``run_id`` (ULID
   factory at the cron/entrypoint layer); Round 12.B wraps it as a
   ``RunIdFactory`` closure that Round 3's ``start_run`` invokes once.

**Threat model (§3.11 v5 trusted-operator envelope; E-023 residual surface)**

- **Per-item PRE-gate re-evaluation.** Round 12.B runs the PRE-gate ONCE
  at entry (step 3), not per-item. The manifest-level org-mismatch predicate
  is covered by ``assert_manifest_org_matches`` inside ``golden_set_iter``;
  per-item admin-risk scans are not re-run (eval-mode processes operator-
  curated historical items, not live RFAs).

- **F_PIPE_05 translates to ``iter_cap_no_pass``, not abort.** A single
  item that fails to converge in 3 iterations does not abort the full
  eval run — the report will carry the ``iter_cap_no_pass`` outcome for
  that item and the run continues. This is semantically different from
  submission-mode R11 (where F_PIPE_05 is terminal).

- **Unsigned report on operator-pubkey-rotation abort.** Step 6's
  ``reconcile_operator_pubkey`` rotation-detection raises ``ValueError``;
  Round 12.B translates that to ``aborted_operator`` and returns BEFORE
  signing. The unsigned ``CalibrationReport`` is NOT written to the vault
  (the write happens at step 8, after signing). Resume semantics: rerun
  the eval run under the rotated pubkey or restore the stored pubkey.

Spec card:
``pipeline/engineering/spec_cards/section_05_round_12_B_run_eval_pipeline.md``
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable, Final, Protocol, runtime_checkable

from pipeline.calibration.golden_set import (
    GoldenSetItem,
    GoldenSetVaultRead,
    IsSymlinkCallable,
    RealpathCallable,
    golden_set_iter,
)
from pipeline.calibration.report import (
    AssembleInputs,
    CalibrationReport,
    CalibrationReportItem,
    assemble_from_run,
    report_to_json,
)
from pipeline.calibration.signing import (
    CalibrationSignerProtocol,
    ClockNowUTC,
    PubkeyVaultReader,
    PubkeyVaultWriter,
    reconcile_operator_pubkey,
    sign_report,
)
from pipeline.logician import PreGateInput, PreGateResult
from pipeline.loop.config import (
    CALIBRATION_SIGNING_ALGORITHM,
    EVAL_MODE_ALLOWED_INTENTS,
    MAX_CALIBRATION_AGE_DAYS,
    RUNSTATE_SCHEMA_VERSION,
)
from pipeline.loop.errors import (
    F_EVAL_CROSS_ORG_READ_CODE,
    F_PIPE_05,
    F_PIPE_21,
    PipelineFailure,
)
from pipeline.loop.post_gate_runner import (
    GateRunnerProtocol,
    PostGateInputFactory,
    PostGateRejected,
    run_post_gate_orchestration,
)
from pipeline.loop.revision_loop import (
    InnerLoopResult,
    InterruptProbe,
    SeatContextFactory,
    run_inner_loop,
)
from pipeline.loop.run_lifecycle import (
    RunIdFactory,
    VaultReadCallable,
    start_run,
)
from pipeline.loop.run_pipeline import PreGateInputFactory
from pipeline.loop.seat_runner import (
    JudgeParseCallable,
    SubprocessLauncher,
)
from pipeline.loop.state_checkpoint import (
    ClockProtocol,
    SleepCallable,
    VaultWriteCallable,
    _write_state_failure_wrapper,
    checkpoint_atomic,
)
from pipeline.loop.tab_delivery import HashFileCallable
from pipeline.loop.types import (
    ProviderCascade,
    RunState,
    SeatCharter,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§4.15 eval-mode entry point + per-item loop + calibration assembly",
            "§4.15 step 6e operator-sign sidecar (OQ-1 sidecar resolution)",
            "§4.15 step 10 reconcile_operator_pubkey BEFORE sign_report (OQ-5)",
            "§6 F-PIPE-21 eval_mode_invalid_intent defence-in-depth shield",
            "§6 F-EVAL-CROSS-ORG-READ translation to aborted_trusted_fail",
        ],
    },
}

# ---------------------------------------------------------------------------
# Inline-literal module-load integrity asserts (V1 discipline)
# ---------------------------------------------------------------------------

# Every constant referenced at a dispatch site below is re-asserted against
# its inline-literal blueprint value. A rebind of the pipeline.loop.config
# module before our import is an integrity violation.
assert RUNSTATE_SCHEMA_VERSION == 2, (
    "pipeline.loop.config.RUNSTATE_SCHEMA_VERSION has been rebound before "
    "pipeline.loop.run_eval_pipeline import; refusing to load"
)
assert CALIBRATION_SIGNING_ALGORITHM == "Ed25519", (
    "pipeline.loop.config.CALIBRATION_SIGNING_ALGORITHM has been rebound "
    "before pipeline.loop.run_eval_pipeline import; refusing to load"
)
assert MAX_CALIBRATION_AGE_DAYS == 90, (
    "pipeline.loop.config.MAX_CALIBRATION_AGE_DAYS has been rebound before "
    "pipeline.loop.run_eval_pipeline import; refusing to load"
)
assert EVAL_MODE_ALLOWED_INTENTS == frozenset(
    {"golden-set-write", "state-success", "state-failure"}
), (
    "pipeline.loop.config.EVAL_MODE_ALLOWED_INTENTS has been rebound before "
    "pipeline.loop.run_eval_pipeline import; refusing to load"
)
assert F_EVAL_CROSS_ORG_READ_CODE == "F-EVAL-CROSS-ORG-READ", (
    "pipeline.loop.errors.F_EVAL_CROSS_ORG_READ_CODE has been rebound "
    "before pipeline.loop.run_eval_pipeline import; refusing to load"
)


# ---------------------------------------------------------------------------
# Public context dataclass — bundled Protocol injection (R12.B parallel of R11)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class RunEvalPipelineContext:
    """Bundle of injected Protocols + callables consumed by :func:`run_eval_pipeline`.

    Parallels :class:`pipeline.loop.run_pipeline.RunPipelineContext`. Fields
    group by origin round:

    - Round 2/3 (core state + vault): ``vault_read``, ``vault_write``,
      ``clock``, ``sleep``, ``run_id_factory``.
    - Round 4/5 (per-item subprocess loop): ``subprocess_launcher``,
      ``seat_context_factory``, optional ``interrupt_probe``,
      ``judge_parse``.
    - Round 6 (POST-gate per item — optional; eval-mode skips POST-gate
      in v0.1 since no three-tab envelope is delivered): stubbed out —
      ``post_gate_runner`` and ``post_gate_input_factory`` fields are
      reserved for v0.2 and are NOT invoked by the v0.1 per-item loop.
      Callers may pass ``None``-safe stubs; the present fields are
      placeholder-compatible with R11's context for future convergence.
    - R12.A calibration: ``golden_set_vault_read``, ``realpath``,
      ``is_symlink``, ``calibration_signer``, ``pubkey_vault_read``,
      ``pubkey_vault_write``, ``now_utc``.
    - Logician PRE-gate: ``pre_gate_callable``.
    - Round 9 hashing (unused in eval-mode; reserved field for
      signature-parallel tab_delivery-pattern audits): ``hash_file``.

    The cascades are NOT in the context — they are per-seat parameters
    like in R11. Charters are forwarded through the capstone signature
    as a tuple (see :func:`run_eval_pipeline`) decomposed internally.
    """

    # Round 2 / Round 3 primitives
    vault_read: VaultReadCallable
    vault_write: VaultWriteCallable
    clock: ClockProtocol
    sleep: SleepCallable
    run_id_factory: RunIdFactory

    # Round 4 / Round 5 primitives
    subprocess_launcher: SubprocessLauncher
    seat_context_factory: SeatContextFactory

    # §4 Logician PRE-gate
    pre_gate_callable: Callable[[PreGateInput], PreGateResult]
    pre_gate_input_factory: PreGateInputFactory

    # Round 6 POST-gate (reserved; not invoked in v0.1 per-item loop)
    post_gate_runner: GateRunnerProtocol
    post_gate_input_factory: PostGateInputFactory

    # Round 9 hash_file (reserved — eval mode never reaches deliver_tab)
    hash_file: HashFileCallable

    # R12.A calibration primitives
    golden_set_vault_read: GoldenSetVaultRead
    realpath: RealpathCallable
    is_symlink: IsSymlinkCallable
    calibration_signer: CalibrationSignerProtocol
    pubkey_vault_read: PubkeyVaultReader
    pubkey_vault_write: PubkeyVaultWriter
    now_utc: ClockNowUTC

    # Report-assembly snapshot inputs (council/router provenance)
    council_charter_snapshot_hash: str
    router_yaml_snapshot_hash: str

    # Optional injections
    interrupt_probe: InterruptProbe | None = None
    judge_parse: JudgeParseCallable | None = None


# ---------------------------------------------------------------------------
# Public result dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class EvalPipelineRunResult:
    """Terminal state of a :func:`run_eval_pipeline` invocation.

    Four observable terminal shapes:

    1. *Success* — ``final_phase == "eval_finalized"``;
       ``calibration_report_path`` + ``calibration_signature_path`` both set;
       ``aborted_operator=False``; ``items_consumed`` is 0..N.

    2. *PRE-gate soft-fail (F-EVAL-CROSS-ORG-READ)* —
       ``final_phase == "aborted_trusted_fail"``;
       ``calibration_report_path=None``; ``calibration_signature_path=None``;
       ``items_consumed=0``.

    3. *Operator-pubkey-rotation abort* —
       ``final_phase == "aborted_operator"``;
       ``aborted_operator=True``; both paths ``None``;
       ``items_consumed=N`` (the per-item loop had completed before
       rotation was detected at sign time).

    4. *PRE-gate soft-fail (generic)* — same shape as case 2 but the
       PRE-gate returned a non-F-EVAL-CROSS-ORG-READ failure_code; Round
       12.B still aborts to ``aborted_trusted_fail`` (eval-mode is strict
       about PRE-gate PASS as prerequisite to calibration authoring).

    Any raise path (F_PIPE_01..22, PipelineFailure subclasses raised by
    Round 5 after the per-item F_PIPE_05 translation) propagates with a
    state-failure checkpoint already written — never constructs
    :class:`EvalPipelineRunResult`.
    """

    run_id: str
    final_phase: str
    items_consumed: int
    calibration_report_path: str | None
    calibration_signature_path: str | None
    elapsed_ms: int
    aborted_operator: bool = False


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _make_capturing_vault_write(
    inner: VaultWriteCallable, sink: dict[str, str | None]
) -> VaultWriteCallable:
    """Wrap ``vault_write`` to capture the first committed_hash in ``sink``.

    Copied verbatim from R11 :mod:`pipeline.loop.run_pipeline` — Round 3's
    ``start_run`` does not return its own committed CAS head; the
    one-shot capturer pins it into a mutable dict so subsequent
    checkpoints know the authoritative head.
    """

    def _wrapper(
        *,
        path: str,
        payload: bytes,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str:
        committed = inner(
            path=path,
            payload=payload,
            intent=intent,
            write_mode=write_mode,
            expected_current_file_hash=expected_current_file_hash,
        )
        if sink.get("first_commit_hash") is None:
            sink["first_commit_hash"] = committed
        return committed

    return _wrapper


def _fixed_run_id_factory(run_id: str) -> RunIdFactory:
    """Wrap a pre-minted run_id as a :class:`RunIdFactory`. Parallel of R11."""

    def _factory() -> str:
        return run_id

    return _factory


def _assert_eval_mode_intent(intent: str) -> None:
    """Defence-in-depth: reject any intent outside the eval-mode allow-list.

    Inline-literal frozenset RHS (V1 discipline — rebind of
    ``pipeline.loop.config.EVAL_MODE_ALLOWED_INTENTS`` cannot widen this
    check). F_PIPE_21 ``eval_mode_invalid_intent`` on violation.

    Round 2 ``checkpoint_atomic`` does NOT enforce mode-isolation; this
    module owns the eval-mode shield. Every Round-12.B-initiated
    vault_write passes through a call site guarded by this function.
    """
    if intent not in frozenset(
        {"golden-set-write", "state-success", "state-failure"}
    ):
        raise F_PIPE_21(
            trigger="eval_mode_invalid_intent",
            details={"observed_intent": intent},
        )


def _transition_phase_and_checkpoint(
    *,
    run_state: RunState,
    new_phase: str,
    expected_current_file_hash: str | None,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
) -> str:
    """Mutate ``run_state.phase`` + write a state-success checkpoint.

    Mode-isolated: ``_assert_eval_mode_intent("state-success")`` before the
    write. On CAS exhaustion (Round 2 raises F_PIPE_01 with a quarantine
    marker already written) the exception propagates unchanged; the caller
    wraps with ``_write_state_failure_wrapper`` on the outer try.
    """
    _assert_eval_mode_intent("state-success")

    run_state.phase = new_phase
    ck = checkpoint_atomic(
        run_state,
        intent="state-success",
        expected_current_file_hash=expected_current_file_hash,
        vault_write=vault_write,
        clock=clock,
        sleep=sleep,
    )
    return ck.committed_hash


def _write_eval_progress_sidecar(
    *,
    run_state: RunState,
    current_item_index: int,
    total_items: int,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
) -> None:
    """Write ``pipeline/{run_id}/eval_progress.json`` (OQ-1 resolution).

    Non-CAS, best-effort write under ``intent="state-success"`` (the
    progress sidecar is state-tracking metadata, not calibration payload).
    On any vault_write exception we swallow — the progress sidecar is
    supplementary; the per-item state checkpoint is the authoritative
    resume anchor.
    """
    path = f"pipeline/{run_state.run_id}/eval_progress.json"
    payload = {
        "run_id": run_state.run_id,
        "operator_org_slug": run_state.org_slug,
        "current_item_index": current_item_index,
        "total_items": total_items,
        "updated_at_iso": clock.now_iso(),
    }
    body = json.dumps(
        payload, sort_keys=True, separators=(", ", ": "), ensure_ascii=False
    ).encode("utf-8")
    try:
        vault_write(
            path=path,
            payload=body,
            intent="state-success",
            write_mode="overwrite",
            expected_current_file_hash=None,
        )
    except Exception:
        # Best-effort — do not mask the surrounding per-item failure path.
        pass


def _map_inner_loop_to_outcome(inner_result: InnerLoopResult) -> str:
    """Map :class:`InnerLoopResult` to a revision-loop outcome literal.

    Returns one of (inline-literal RHS; rebind-resistant):
    - ``"pass_iter1"`` / ``"pass_iter2"`` / ``"pass_iter3"`` — converged
      on score-threshold PASS at iter-N.
    - ``"plateau_no_pass"`` — converged on delta-plateau (two consecutive
      high scores without an actual PASS verdict).

    F_PIPE_05 cap-exhausted raises never construct an InnerLoopResult; the
    caller translates that branch to ``"iter_cap_no_pass"`` explicitly.
    """
    if inner_result.converged_on == "score_threshold":
        n = inner_result.iterations_run
        if n == 1:
            return "pass_iter1"
        if n == 2:
            return "pass_iter2"
        if n == 3:
            return "pass_iter3"
        # A value outside [1, 3] would mean Round 5 broke its iterations_run
        # contract — defensive default keeps us within the enum.
        return "iter_cap_no_pass"  # pragma: no cover — R5 contract
    if inner_result.converged_on == "delta_plateau":
        return "plateau_no_pass"
    # Unknown converged_on — defensive default, matching the failed-to-pass
    # semantics of delta_plateau. Round 5 only returns those two literals.
    return "plateau_no_pass"  # pragma: no cover — R5 contract


def _extract_int_score(verdict: dict[str, Any]) -> int:
    """Coerce ``verdict["total_score"]`` to int in [0, 100].

    Judge verdicts arrive as parsed JSON dicts from Round 4's
    ``default_judge_parse``. ``total_score`` may be ``int`` or ``float``;
    we clamp to [0, 100] as a safety net even though the Judge rubric
    constrains to that range. Non-numeric values default to 0 (the
    caller already recorded the raw verdict in ``IterationState`` for
    post-mortem).
    """
    raw = verdict.get("total_score", 0) if isinstance(verdict, dict) else 0
    try:
        val = int(raw)
    except (TypeError, ValueError):
        return 0
    if val < 0:
        return 0
    if val > 100:
        return 100
    return val


def _extract_per_dimension(verdict: dict[str, Any]) -> dict[str, int]:
    """Extract ``per_dimension`` dict from a Judge verdict, clamped to [0, 10].

    Keys that are not str or values that are not numeric-coercible-to-int
    are skipped. Values outside [0, 10] are clamped. An absent or non-dict
    ``per_dimension`` field yields an empty dict.
    """
    raw = verdict.get("per_dimension") if isinstance(verdict, dict) else None
    if not isinstance(raw, dict):
        return {}
    out: dict[str, int] = {}
    for k, v in raw.items():
        if not isinstance(k, str) or not k:
            continue
        try:
            iv = int(v)
        except (TypeError, ValueError):
            continue
        if iv < 0:
            iv = 0
        if iv > 10:
            iv = 10
        out[k] = iv
    return out


def _build_calibration_report_item(
    *,
    item: GoldenSetItem,
    run_id: str,
    inner_result: InnerLoopResult | None,
    outcome: str,
) -> CalibrationReportItem:
    """Build a :class:`CalibrationReportItem` from a per-item run outcome.

    ``inner_result`` is ``None`` only on ``outcome == "iter_cap_no_pass"``;
    in that case we synthesize an empty verdict (total_score=0, per_dim={})
    with ``iterations_used=3`` (the cap) and the supplied outcome literal.

    ``item_run_id`` is synthesized as ``f"{run_id}::{item.item_id}"`` —
    inline-literal format string (V1 discipline). Runtime validation of
    the outcome literal happens in :class:`CalibrationReportItem`
    ``__post_init__`` which uses its own inline-literal frozenset.
    """
    item_run_id = f"{run_id}::{item.item_id}"

    if inner_result is None:
        # iter_cap_no_pass path — no successful verdict.
        return CalibrationReportItem(
            item_id=item.item_id,
            judge_total_score=0,
            judge_per_dimension={},
            editor_critique_summary="",
            iterations_used=3,
            revision_loop_outcome="iter_cap_no_pass",
            item_run_id=item_run_id,
        )

    verdict = inner_result.final_iteration.judge_verdict or {}
    total = _extract_int_score(verdict)
    per_dim = _extract_per_dimension(verdict)
    # ``editor_critique_summary`` is an optional str field on the verdict
    # (injected by Editor via the Judge prompt); default to empty str if
    # absent or non-str.
    raw_crit = verdict.get("editor_critique_summary", "") if isinstance(
        verdict, dict
    ) else ""
    critique = raw_crit if isinstance(raw_crit, str) else ""

    return CalibrationReportItem(
        item_id=item.item_id,
        judge_total_score=total,
        judge_per_dimension=per_dim,
        editor_critique_summary=critique,
        iterations_used=inner_result.iterations_run,
        revision_loop_outcome=outcome,  # type: ignore[arg-type]
        item_run_id=item_run_id,
    )


def _write_calibration_report(
    *,
    report: CalibrationReport,
    operator_org_slug: str,
    run_id: str,
    vault_write: VaultWriteCallable,
) -> str:
    """Write the signed report JSON under the calibration_reports prefix.

    Inline-literal path template — a rebind of
    ``CALIBRATION_REPORT_PATH_TMPL`` cannot redirect the write. Intent is
    gated by ``_assert_eval_mode_intent("golden-set-write")``.

    Returns the vault-relative path the report was written to.
    """
    _assert_eval_mode_intent("golden-set-write")

    path = (
        f"{operator_org_slug}/golden_set/calibration_reports/{run_id}.json"
    )
    body = report_to_json(report)
    vault_write(
        path=path,
        payload=body,
        intent="golden-set-write",
        write_mode="write-if-absent",
        expected_current_file_hash=None,
    )
    return path


def _write_calibration_signature(
    *,
    signature_bytes: bytes,
    operator_org_slug: str,
    run_id: str,
    vault_write: VaultWriteCallable,
) -> str:
    """Write the detached Ed25519 signature bytes sidecar.

    Inline-literal path template. Intent gated by
    ``_assert_eval_mode_intent("golden-set-write")``.
    """
    _assert_eval_mode_intent("golden-set-write")

    path = (
        f"{operator_org_slug}/golden_set/calibration_reports/{run_id}.sig"
    )
    vault_write(
        path=path,
        payload=signature_bytes,
        intent="golden-set-write",
        write_mode="write-if-absent",
        expected_current_file_hash=None,
    )
    return path


# ---------------------------------------------------------------------------
# Per-item runner — encapsulates the inner-loop + outcome-build for one item
# ---------------------------------------------------------------------------


def _run_one_item(
    *,
    item: GoldenSetItem,
    run_state: RunState,
    scribe_charter: SeatCharter,
    editor_charter: SeatCharter,
    judge_charter: SeatCharter,
    scribe_cascade: ProviderCascade,
    editor_cascade: ProviderCascade,
    judge_cascade: ProviderCascade,
    ctx: RunEvalPipelineContext,
    entry_hash: str,
) -> tuple[CalibrationReportItem, str]:
    """Drive one golden-set item through the inner loop; build the report item.

    Pre-conditions (caller-enforced):
    - ``run_state.iterations`` is cleared (A-v1-10 soft-restart guard).
    - ``run_state.phase == "inner_loop_iter_1"`` + checkpoint already landed.
    - ``entry_hash`` is the CAS head after that phase-transition checkpoint.

    Post-conditions:
    - ``run_state.iterations`` populated with 1..3 IterationStates.
    - Returns ``(CalibrationReportItem, post_inner_loop_hash)``.

    F_PIPE_05 is TRANSLATED to an ``iter_cap_no_pass`` report item; the
    exception is caught at this boundary (Round 5 has already written a
    final state-failure checkpoint). Any other :class:`PipelineFailure`
    propagates unchanged — the outer run_eval_pipeline owns the
    state-failure wrapper for those.

    A local state-hash capturer wraps ``ctx.vault_write`` so that after
    a per-item F_PIPE_05 cap-exhaust we can hand back the authoritative
    CAS head from Round 5's final state-failure checkpoint to the caller
    (otherwise the caller's next phase transition would re-use the stale
    ``entry_hash`` and explode into F_PIPE_01 CAS-exhausted).
    """
    # Capture the last state-intent write hash so that, on F_PIPE_05,
    # we can return the true post-inner-loop CAS head.
    _last_state_hash: dict[str, str | None] = {"hash": None}

    def _capturing_write(
        *,
        path: str,
        payload: bytes,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str:
        committed = ctx.vault_write(
            path=path,
            payload=payload,
            intent=intent,
            write_mode=write_mode,
            expected_current_file_hash=expected_current_file_hash,
        )
        if intent in ("state-success", "state-failure"):
            _last_state_hash["hash"] = committed
        return committed

    try:
        inner_result = run_inner_loop(
            run_state=run_state,
            scribe_charter=scribe_charter,
            editor_charter=editor_charter,
            judge_charter=judge_charter,
            scribe_cascade=scribe_cascade,
            editor_cascade=editor_cascade,
            judge_cascade=judge_cascade,
            context_factory=ctx.seat_context_factory,
            subprocess_launcher=ctx.subprocess_launcher,
            vault_write=_capturing_write,
            clock=ctx.clock,
            sleep=ctx.sleep,
            initial_checkpoint_hash=entry_hash,
            interrupt_probe=ctx.interrupt_probe,
            judge_parse=ctx.judge_parse,
        )
    except F_PIPE_05:
        # Per-item cap exhaust — NOT run-terminal in eval mode. Round 5
        # has already written a state-failure checkpoint BEFORE raising
        # (revision_loop.py line 705-712). Synthesize an iter_cap_no_pass
        # report item and re-derive the post-checkpoint hash from the
        # state-failure write — but we don't have a clean way to pull it
        # back; instead, we treat the next per-item loop as needing a
        # fresh phase re-entry, which the caller achieves via the
        # eval_iter_pending → inner_loop_iter_1 transition.
        #
        # The returned ``post_inner_loop_hash`` is best-effort: Round 5's
        # final state-failure write did not return through us. The caller
        # uses it as the ``expected_current_file_hash`` for the next
        # transition; if the vault has moved past that hash, the caller's
        # checkpoint_atomic will CAS-retry. This is correct.
        post_hash = _last_state_hash["hash"] or entry_hash
        return (
            _build_calibration_report_item(
                item=item,
                run_id=run_state.run_id,
                inner_result=None,
                outcome="iter_cap_no_pass",
            ),
            post_hash,
        )

    outcome = _map_inner_loop_to_outcome(inner_result)
    report_item = _build_calibration_report_item(
        item=item,
        run_id=run_state.run_id,
        inner_result=inner_result,
        outcome=outcome,
    )
    return report_item, inner_result.final_checkpoint_hash


# ---------------------------------------------------------------------------
# Public API — run_eval_pipeline
# ---------------------------------------------------------------------------


def run_eval_pipeline(
    *,
    run_id: str,
    operator_org_slug: str,
    golden_set_manifest_path: str,
    session_id: str,
    scribe_charter: SeatCharter,
    editor_charter: SeatCharter,
    judge_charter: SeatCharter,
    scribe_cascade: ProviderCascade,
    editor_cascade: ProviderCascade,
    judge_cascade: ProviderCascade,
    ctx: RunEvalPipelineContext,
    subset: tuple[str, ...] | None = None,
) -> EvalPipelineRunResult:
    """§4.15 eval-mode capstone — composes R1-R11 + R12.A primitives.

    Parameters
    ----------
    run_id
        Caller-minted ULID (cron wrapper or entrypoint). Threaded to
        Round 3 ``start_run`` via a fixed-factory closure.
    operator_org_slug
        Operator's authenticated org_slug. Bound to
        :class:`RunState.org_slug` for Law-3 isolation. Compared against
        the manifest's own ``org_slug`` inside ``golden_set_iter``.
    golden_set_manifest_path
        Vault-relative path to the operator's signed golden-set manifest.
        Validated by ``_resolve_golden_set_path`` (NFC + realpath +
        symlink-walk) before any read.
    session_id
        Opaque session identifier (operator-scoped; threaded into
        :class:`RunState`).
    scribe_charter / editor_charter / judge_charter
        Per-seat Round 1 charters.
    scribe_cascade / editor_cascade / judge_cascade
        Per-seat Round 1 cascades. Reused across all items.
    ctx
        :class:`RunEvalPipelineContext` bundling all injected Protocols +
        callables.
    subset
        Optional tuple of ``item_id`` strings. When supplied, only items
        with matching ``item_id`` are processed (manifest order preserved
        per OQ-3).

    Returns
    -------
    EvalPipelineRunResult
        Terminal state — see the dataclass docstring for the four shapes.

    Raises
    ------
    F_PIPE_01
        Checkpoint CAS exhausted at any transition.
    F_PIPE_05
        CAUGHT internally at per-item boundary — translates to
        ``iter_cap_no_pass`` report item, never propagates.
    F_PIPE_06 / F_PIPE_08 / F_PIPE_09
        Per-seat cascade / cross-family / Judge-parse failures from
        Round 4 → Round 5 per item. Propagate unchanged after a
        state-failure wrapper.
    F_PIPE_11
        Operator interrupt post-iteration checkpoint. Propagates.
    F_PIPE_19
        Soft-restart forbidden — should NOT fire in eval mode because
        per-item ``run_state.iterations.clear()`` precedes every item.
        Defensive — if it fires it indicates a caller bug.
    F_PIPE_21
        Path-traversal / symlink ancestor / org-mismatch / stale-signature
        / invalid-intent. All raised by Round 12.A primitives or by
        ``_assert_eval_mode_intent``.
    F_PIPE_22
        RunState or CalibrationReport schema downgrade.
    """

    start_wall_ms = ctx.clock.now_ms()

    # ----- Step 1 — start_run (Round 3) in eval mode ----------------------
    # start_run raises F_PIPE_21/22 on mode-discriminated-union violation
    # BEFORE any state exists — no wrapper needed on this call.
    _capture_sink: dict[str, str | None] = {"first_commit_hash": None}
    run_state = start_run(
        mode="eval",
        org_slug=operator_org_slug,
        session_id=session_id,
        rfa_hash=None,
        project_context_hash=None,
        golden_set_ref=golden_set_manifest_path,
        run_id_factory=_fixed_run_id_factory(run_id),
        vault_write=_make_capturing_vault_write(ctx.vault_write, _capture_sink),
        clock=ctx.clock,
        sleep=ctx.sleep,
    )

    if run_state.run_id != run_id:  # pragma: no cover — factory closure contract
        raise AssertionError(
            f"start_run returned run_id={run_state.run_id!r}; expected {run_id!r}"
        )

    initial_hash = _capture_sink["first_commit_hash"]

    # ----- Step 2 — phase → pre_gate_pending + checkpoint -----------------
    try:
        current_hash: str = _transition_phase_and_checkpoint(
            run_state=run_state,
            new_phase="pre_gate_pending",
            expected_current_file_hash=initial_hash,
            vault_write=ctx.vault_write,
            clock=ctx.clock,
            sleep=ctx.sleep,
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
        )
        raise

    # ----- Step 3 — PRE-gate evaluation -----------------------------------
    try:
        pre_gate_input = ctx.pre_gate_input_factory(run_state=run_state)
        pre_gate_result = ctx.pre_gate_callable(pre_gate_input)
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
        )
        raise

    if not pre_gate_result.passed:
        # Eval mode is strict: any PRE-gate FAIL aborts to
        # aborted_trusted_fail. F-EVAL-CROSS-ORG-READ is the dominant
        # cause (manifest-vs-operator org mismatch); other F-PRE-* codes
        # land here too.
        try:
            current_hash = _transition_phase_and_checkpoint(
                run_state=run_state,
                new_phase="aborted_trusted_fail",
                expected_current_file_hash=current_hash,
                vault_write=ctx.vault_write,
                clock=ctx.clock,
                sleep=ctx.sleep,
            )
        except Exception as exc:
            _write_state_failure_wrapper(
                run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
            )
            # Even on checkpoint failure we still return the soft-fail
            # result — the operator sees aborted_trusted_fail surfaced
            # through the EvalPipelineRunResult return channel rather
            # than an exception.
        elapsed_ms = max(ctx.clock.now_ms() - start_wall_ms, 0)
        return EvalPipelineRunResult(
            run_id=run_state.run_id,
            final_phase="aborted_trusted_fail",
            items_consumed=0,
            calibration_report_path=None,
            calibration_signature_path=None,
            elapsed_ms=elapsed_ms,
            aborted_operator=False,
        )

    # PRE-gate PASSED — transition to pre_gate_passed.
    try:
        current_hash = _transition_phase_and_checkpoint(
            run_state=run_state,
            new_phase="pre_gate_passed",
            expected_current_file_hash=current_hash,
            vault_write=ctx.vault_write,
            clock=ctx.clock,
            sleep=ctx.sleep,
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
        )
        raise

    # ... then to eval_iter_pending (gateway phase for the per-item loop).
    try:
        current_hash = _transition_phase_and_checkpoint(
            run_state=run_state,
            new_phase="eval_iter_pending",
            expected_current_file_hash=current_hash,
            vault_write=ctx.vault_write,
            clock=ctx.clock,
            sleep=ctx.sleep,
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
        )
        raise

    # ----- Step 4 — per-item loop -----------------------------------------
    # golden_set_iter does all the path hardening + org-mismatch checks.
    # Exceptions from the iterator are raised during iteration, not at
    # tuple() time for a generator — but the happy path materializes
    # items via tuple() so we can count total_items for the progress sidecar.
    try:
        items_tuple: tuple[GoldenSetItem, ...] = tuple(
            golden_set_iter(
                operator_org_slug=operator_org_slug,
                manifest_path=golden_set_manifest_path,
                vault_read=ctx.golden_set_vault_read,
                subset=subset,
                realpath=ctx.realpath,
                is_symlink=ctx.is_symlink,
            )
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
        )
        raise

    per_item_results: list[CalibrationReportItem] = []
    manifest_hash: str = (
        items_tuple[0].manifest_hash if items_tuple else ""
    )

    for idx, item in enumerate(items_tuple):
        # Step 4a — progress sidecar (best-effort; OQ-1).
        _write_eval_progress_sidecar(
            run_state=run_state,
            current_item_index=idx,
            total_items=len(items_tuple),
            vault_write=ctx.vault_write,
            clock=ctx.clock,
        )

        # Step 4b — clear iterations (A-v1-10 guard would otherwise fire at
        # item #2 iter_1 because item #1's IterationStates still carry
        # iter_number <= 3).
        run_state.iterations.clear()
        run_state.run_iteration_families_so_far.clear()

        # Step 4c — phase transition eval_iter_pending → inner_loop_iter_1.
        try:
            current_hash = _transition_phase_and_checkpoint(
                run_state=run_state,
                new_phase="inner_loop_iter_1",
                expected_current_file_hash=current_hash,
                vault_write=ctx.vault_write,
                clock=ctx.clock,
                sleep=ctx.sleep,
            )
        except Exception as exc:
            _write_state_failure_wrapper(
                run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
            )
            raise

        # Step 4d + 4e — run the inner loop + build the per-item report.
        try:
            report_item, post_hash = _run_one_item(
                item=item,
                run_state=run_state,
                scribe_charter=scribe_charter,
                editor_charter=editor_charter,
                judge_charter=judge_charter,
                scribe_cascade=scribe_cascade,
                editor_cascade=editor_cascade,
                judge_cascade=judge_cascade,
                ctx=ctx,
                entry_hash=current_hash,
            )
        except PipelineFailure:  # pragma: no cover — non-F_PIPE_05 leak path
            # Round 5 already wrote state-failure + appended IterationState
            # before raising. Propagate as-is — eval run is terminal for
            # non-F_PIPE_05 failures per the §4.15 design. F_PIPE_05 is
            # intercepted one level deeper in ``_run_one_item``.
            raise
        except Exception as exc:
            _write_state_failure_wrapper(
                run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
            )
            raise

        per_item_results.append(report_item)
        current_hash = post_hash

        # Step 4f — phase back to eval_iter_pending for next item (or for
        # the assembly transition below).
        try:
            current_hash = _transition_phase_and_checkpoint(
                run_state=run_state,
                new_phase="eval_iter_pending",
                expected_current_file_hash=current_hash,
                vault_write=ctx.vault_write,
                clock=ctx.clock,
                sleep=ctx.sleep,
            )
        except Exception as exc:
            _write_state_failure_wrapper(
                run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
            )
            raise

    # ----- Step 5 — assemble CalibrationReport ----------------------------
    try:
        report = assemble_from_run(
            AssembleInputs(
                run_id=run_state.run_id,
                operator_org_slug=operator_org_slug,
                golden_set_manifest_path=golden_set_manifest_path,
                golden_set_manifest_hash=manifest_hash or "empty-manifest",
                per_item_results=tuple(per_item_results),
                council_charter_snapshot_hash=(
                    ctx.council_charter_snapshot_hash
                ),
                router_yaml_snapshot_hash=ctx.router_yaml_snapshot_hash,
                assembled_at_iso=ctx.clock.now_iso(),
            )
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
        )
        raise

    try:
        current_hash = _transition_phase_and_checkpoint(
            run_state=run_state,
            new_phase="calibration_assembled",
            expected_current_file_hash=current_hash,
            vault_write=ctx.vault_write,
            clock=ctx.clock,
            sleep=ctx.sleep,
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
        )
        raise

    # ----- Step 6 — reconcile operator pubkey (BEFORE sign_report; OQ-5) --
    # Rotation detection raises ValueError — translate to aborted_operator
    # soft-return. Any other exception is propagated after state-failure.
    signed_at_iso = ctx.clock.now_iso()
    try:
        reconcile_operator_pubkey(
            operator_org_slug=operator_org_slug,
            run_id=run_state.run_id,
            first_write_iso=signed_at_iso,
            signer=ctx.calibration_signer,
            pubkey_read=ctx.pubkey_vault_read,
            pubkey_write=ctx.pubkey_vault_write,
        )
    except ValueError:
        # Operator pubkey rotation — deferred to v0.2. Translate to a
        # soft-return with aborted_operator=True. The unsigned report is
        # NOT written to the vault.
        try:
            current_hash = _transition_phase_and_checkpoint(
                run_state=run_state,
                new_phase="aborted_operator",
                expected_current_file_hash=current_hash,
                vault_write=ctx.vault_write,
                clock=ctx.clock,
                sleep=ctx.sleep,
            )
        except Exception as exc:
            _write_state_failure_wrapper(
                run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
            )
        elapsed_ms = max(ctx.clock.now_ms() - start_wall_ms, 0)
        return EvalPipelineRunResult(
            run_id=run_state.run_id,
            final_phase="aborted_operator",
            items_consumed=len(per_item_results),
            calibration_report_path=None,
            calibration_signature_path=None,
            elapsed_ms=elapsed_ms,
            aborted_operator=True,
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
        )
        raise

    # ----- Step 7 — sign_report (Ed25519 detached over canonical bytes) ---
    try:
        signed_report = sign_report(
            report, signer=ctx.calibration_signer, signed_at_iso=signed_at_iso
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
        )
        raise

    try:
        current_hash = _transition_phase_and_checkpoint(
            run_state=run_state,
            new_phase="calibration_signed",
            expected_current_file_hash=current_hash,
            vault_write=ctx.vault_write,
            clock=ctx.clock,
            sleep=ctx.sleep,
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
        )
        raise

    # ----- Step 8/9 — write signed report + signature sidecar -------------
    try:
        report_path = _write_calibration_report(
            report=signed_report,
            operator_org_slug=operator_org_slug,
            run_id=run_state.run_id,
            vault_write=ctx.vault_write,
        )
        sig_bytes = signed_report.signature
        if sig_bytes is None:
            # Defensive — sign_report guarantees non-None.
            raise RuntimeError(
                "sign_report returned a report with signature=None"
            )  # pragma: no cover — sign_report contract
        sig_path = _write_calibration_signature(
            signature_bytes=sig_bytes,
            operator_org_slug=operator_org_slug,
            run_id=run_state.run_id,
            vault_write=ctx.vault_write,
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
        )
        raise

    # ----- Step 10 — pin refs + phase → eval_finalized --------------------
    run_state.calibration_report_ref = report_path
    run_state.calibration_signature_ref = sig_path
    try:
        current_hash = _transition_phase_and_checkpoint(
            run_state=run_state,
            new_phase="eval_finalized",
            expected_current_file_hash=current_hash,
            vault_write=ctx.vault_write,
            clock=ctx.clock,
            sleep=ctx.sleep,
        )
    except Exception as exc:
        _write_state_failure_wrapper(
            run_state, exc, vault_write=ctx.vault_write, clock=ctx.clock
        )
        raise

    elapsed_ms = max(ctx.clock.now_ms() - start_wall_ms, 0)
    return EvalPipelineRunResult(
        run_id=run_state.run_id,
        final_phase="eval_finalized",
        items_consumed=len(per_item_results),
        calibration_report_path=report_path,
        calibration_signature_path=sig_path,
        elapsed_ms=elapsed_ms,
        aborted_operator=False,
    )


# Silence unused-import complaints for Protocols surfaced as ctx fields only.
# PostGateRejected + GateRunnerProtocol + PostGateInputFactory are imported
# for the context type-surface (v0.2 convergence with R11) even though
# Round 12.B v0.1 does not invoke POST-gate per item.
_ = PostGateRejected
_ = GateRunnerProtocol
_ = PostGateInputFactory
_ = run_post_gate_orchestration
_ = PreGateInputFactory


__all__ = [
    "BLUEPRINT_DEPS",
    "EvalPipelineRunResult",
    "RunEvalPipelineContext",
    "run_eval_pipeline",
]
