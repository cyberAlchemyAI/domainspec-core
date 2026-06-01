"""§4.11 Scout run orchestration capstone-of-capstones.

Scout Round 11. Composes Round 8 DISCOVER (``run_scout_discover``) +
Round 9 VERIFY (``verify_all``) + Round 10 REVIEW (``enqueue_for_review``)
into the single Pipeline-facing entry the Section 5 orchestrator invokes
per blueprint §9 step 2 + §4.11. Adds the bounded
``_build_fit_rationale`` per-VERIFIED_FIT fan-out (blueprint §9 line
1441 + §9 line 1458) — default implementation is deterministic
plain-text, deployment-supplied implementations bind a real LLM
provider. Round 11 does NOT re-author DISCOVER / VERIFY / REVIEW
primitives; composition only.

Blueprint anchors:

- §4.11 Scout run orchestration — primary implementation target
  (lines 1017-1074 sketch).
- §9 Scout run sequence — the 15-step canonical ordering this module
  realises.
- §6 — the F-SCOUT-* namespaces this module composes; capstone-only
  codes are F-SCOUT-RUN-01..05.
- §7.16 LLM call boundary — ``pipeline.scout.run`` does NOT import any
  LLM provider; the AST-lint regression confirms this.
- §8 — ``MAX_FIT_RATIONALE_BYTES`` is a capstone-introduced constant
  (capstone-only; no §8 row exists today; spec card declares it).
- Architecture line 270-271 — capstone records facts; Logician decides
  the ≥4/6 hard abort downstream.
- Autonomy Rule 1 — checkpoint at ``run_review_start`` +
  ``run_review_complete`` (success AND failure) +
  ``run_review_interrupted`` (interrupt mid-fan-out). Per-stage
  checkpoints already land inside ``run_scout_discover`` /
  ``verify_all`` / ``enqueue_for_review``.

Spec-card deviation notes (from
``pipeline/engineering/spec_cards/scout_round_11_capstone.md`` v1):

- Blueprint §4.11 sketch names the entry point ``run_scout_discover_verify``;
  operator-disposed name is ``run_scout_discover_verify_review`` (longer
  name reflects the actual scope including REVIEW). Both names are
  exposed: ``run_scout_discover_verify`` is a verbatim alias of
  ``run_scout_discover_verify_review`` (Step 0 reconciliation #1).
- Blueprint §9 line 1447 places the entity-research pass *outside* the
  DISCOVER/VERIFY/REVIEW chain (Pipeline drives it independently). R11
  does NOT call ``run_entity_research``.

No module-level side effects on import — no network, no disk, no
keystore resolution, no LLM. All persistence routes through injected
Protocols; LLM invocation routes through the optional
:class:`BuildFitRationale` Protocol whose default binding is a
deterministic plain-text formatter shipped inline. AST-lint
R1/R2/R3/R4/R5/R6/R7 clean.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Final,
    Mapping,
    Optional,
    Protocol,
    runtime_checkable,
)

from pipeline.scout._types import (
    Candidate,
    ReviewQueueItem,
    SignedHealthTuple,
    VerificationVerdict,
)
from pipeline.scout._constants import VERDICT_VERIFIED_FIT
from pipeline.scout.discover import (
    CapstoneDegradationEvent,
    ChannelDiscoverCallable,
    HealthTupleSigner,
    InterruptProbe as DiscoverInterruptProbe,
    ScoutDiscoverInterrupted,
    ScoutDiscoverResult,
    run_scout_discover,
)
from pipeline.scout.discover import CheckpointWriter as DiscoverCheckpointWriter
from pipeline.scout.discover import ClockFn as DiscoverClockFn
from pipeline.scout.discover import DegradationWriter as DiscoverDegradationWriter
from pipeline.scout.discover import EntropyFn as DiscoverEntropyFn
from pipeline.scout.discover import ExecutorFactory as DiscoverExecutorFactory
from pipeline.scout.review_stage import (
    SessionLike,
    VaultWriter,
    enqueue_for_review,
)
from pipeline.scout.review_stage import CheckpointWriter as ReviewCheckpointWriter
from pipeline.scout.review_stage import ClockFn as ReviewClockFn
from pipeline.scout.verify_stage import (
    ApplicantProfileProvider,
    ScoutVerifyInterrupted,
    ScoutVerifyResult,
    SynopsisFetcher,
    VerifyDegradationEvent,
    VerifyStageState,
    verify_all,
)
from pipeline.scout.verify_stage import CheckpointWriter as VerifyCheckpointWriter
from pipeline.scout.verify_stage import ClockFn as VerifyClockFn
from pipeline.scout.verify_stage import (
    DegradationWriter as VerifyDegradationWriter,
)
from pipeline.scout.verify_stage import (
    ExecutorFactory as VerifyExecutorFactory,
)
from pipeline.scout.verify_stage import (
    InterruptProbe as VerifyInterruptProbe,
)


__version__: Final[str] = "0.1.0-scout-r11"


__all__ = [
    "BLUEPRINT_DEPS",
    "BuildFitRationale",
    "F_SCOUT_RUN_01",
    "F_SCOUT_RUN_02",
    "F_SCOUT_RUN_03",
    "F_SCOUT_RUN_04",
    "F_SCOUT_RUN_05",
    "MAX_FIT_RATIONALE_BYTES",
    "RationaleBudgetExceeded",
    "RationaleBuildFailed",
    "RunDegradationEvent",
    "ScoutRunInterrupted",
    "ScoutRunResult",
    "SEVERITY_HIGH",
    "SEVERITY_LOW",
    "SEVERITY_MEDIUM",
    "__version__",
    "run_scout_discover_verify",
    "run_scout_discover_verify_review",
]
# `_build_fit_rationale` is intentionally NOT re-exported via ``__all__``
# (blueprint §4.11 line 1067 names the helper with an underscore prefix
# — implementation symbol, not public API). Custom rationale builders
# bind via the ``build_fit_rationale`` kwarg of
# :func:`run_scout_discover_verify_review`. Direct callers may import
# from this module, but the surface contract is the
# :class:`BuildFitRationale` Protocol, not the default helper.


# ---------------------------------------------------------------------------
# BLUEPRINT_DEPS — drift-detection pin (mirrors Round 8/9/10 discipline)
# ---------------------------------------------------------------------------


BLUEPRINT_DEPS: Final[Mapping[str, Mapping[str, Any]]] = {
    "section_03_scout.md": {
        "version": "v0.1 (§3 Scout LOCKED)",
        "hash_sha3_512_prefix16": "0a82d955f95b0fca",
        "sections_implemented": (
            "§4.11 (capstone-of-capstones)",
            "§9 (run sequence step 2 + 13-14)",
            "§7.16 (LLM-import boundary)",
            "§8 (MAX_FIT_RATIONALE_BYTES; capstone-introduced)",
        ),
    },
}


# ---------------------------------------------------------------------------
# Capstone-introduced constants
# ---------------------------------------------------------------------------


MAX_FIT_RATIONALE_BYTES: Final[int] = 4096
"""UTF-8 byte budget for ``_build_fit_rationale`` output.

Blueprint §4.11 line 1458 / §9 line 1458 — "bounded to ≤ 800 tokens".
We approximate the token bound on the byte side at 4096 = 800 × 5
bytes/token mid-range. Strict ``>`` comparison: a rationale of
exactly ``MAX_FIT_RATIONALE_BYTES`` UTF-8 bytes is accepted; one byte
over fires F-SCOUT-RUN-01.
"""


SEVERITY_LOW: Final[str] = "LOW"
SEVERITY_MEDIUM: Final[str] = "MEDIUM"
SEVERITY_HIGH: Final[str] = "HIGH"


# ---------------------------------------------------------------------------
# Failure codes (capstone-only namespace)
# ---------------------------------------------------------------------------


F_SCOUT_RUN_01: Final[str] = "F-SCOUT-RUN-01"  # rationale byte budget exceeded
F_SCOUT_RUN_02: Final[str] = "F-SCOUT-RUN-02"  # rationale builder raised
F_SCOUT_RUN_03: Final[str] = "F-SCOUT-RUN-03"  # channel dispatch missing keys
F_SCOUT_RUN_04: Final[str] = "F-SCOUT-RUN-04"  # interrupt mid run-level fan-out
F_SCOUT_RUN_05: Final[str] = "F-SCOUT-RUN-05"  # signer carry-through failure


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class RationaleBudgetExceeded(Exception):
    """F-SCOUT-RUN-01 — rationale text exceeds ``MAX_FIT_RATIONALE_BYTES``.

    Carried inside the per-VERIFIED_FIT loop; not re-raised — the
    capstone records the failure as a :class:`RunDegradationEvent` and
    skips the candidate's enqueue. Re-raise discipline mirrors R10
    review_stage: best-effort enqueue, never aborting the whole run.
    """


class RationaleBuildFailed(Exception):
    """F-SCOUT-RUN-02 — custom :class:`BuildFitRationale` raised.

    Same posture as :class:`RationaleBudgetExceeded` — the capstone
    catches and records, never re-raising.
    """


class ScoutRunInterrupted(RuntimeError):
    """F-SCOUT-RUN-04 — ``interrupt_probe()`` fired mid run-level fan-out.

    Carries the ordered tuple of candidate_ids whose enqueue completed
    before the interrupt was observed. Section 5's resume path reads
    the ``run_review_interrupted`` checkpoint payload, not this object.
    """

    def __init__(self, completed_candidate_ids: tuple[str, ...]):
        self.completed_candidate_ids = completed_candidate_ids
        super().__init__(
            f"{F_SCOUT_RUN_04}: run-level fan-out interrupted after "
            f"completed_candidate_ids={completed_candidate_ids!r}"
        )


# ---------------------------------------------------------------------------
# BuildFitRationale Protocol (E-017 — 10th Scout firing; new injection)
# ---------------------------------------------------------------------------


@runtime_checkable
class BuildFitRationale(Protocol):
    """Per-VERIFIED_FIT rationale-build seam.

    Production deployments override the default by binding a real
    LLM provider (Scout primary per ``router.yaml`` — local Ollama by
    default). The default implementation shipped inline in this module
    is deterministic plain-text — zero LLM, zero network, zero
    subprocess — to keep ``pipeline.scout.run`` import-time-stdlib-only
    and to satisfy the §7.16 LLM-import boundary at call-site review
    time.

    Contract:

    - Returns a ``str`` whose UTF-8 byte length is ≤
      ``MAX_FIT_RATIONALE_BYTES``. Anything over fires F-SCOUT-RUN-01.
    - Raises any exception → F-SCOUT-RUN-02; the candidate's enqueue
      is skipped, the run continues with the next candidate.
    - ``KeyboardInterrupt`` / ``SystemExit`` propagate unchanged
      (never caught).
    """

    def __call__(
        self,
        *,
        session: SessionLike,
        candidate: Candidate,
        verdict: VerificationVerdict,
    ) -> str: ...


# ---------------------------------------------------------------------------
# RunDegradationEvent — capstone-level event surface
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class RunDegradationEvent:
    """One-line capstone-level event for run.py-introduced surfaces.

    Scope: events INTRODUCED by the run.py layer (rationale fan-out
    + interrupt boundary). Per-stage events stay on their per-stage
    results — DISCOVER on ``ScoutDiscoverResult.capstone_degradation_events``,
    VERIFY on ``ScoutVerifyResult.verify_degradation_events``, REVIEW
    flows through R10's checkpoint discipline (no event surface).
    """

    source: str
    code: str
    reason_tag: Optional[str]
    severity: str
    candidate_id: Optional[str] = None


# ---------------------------------------------------------------------------
# ScoutRunResult — capstone-of-capstones return shape
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ScoutRunResult:
    """Section 5 (Pipeline)-facing run result.

    Fields are a stable union of Round 8/9/10 outputs plus the
    run-level rationale fan-out outcomes. The capstone does NOT mutate
    any field carried through from a sub-stage — DISCOVER's signed
    health tuple, VERIFY's verdict mapping, REVIEW's queue items are
    surfaced verbatim.

    ``review_queue_items`` preserves the stable Round-8 candidate
    order; ``fit_rationales`` is keyed by candidate_id and contains
    only entries for VERIFIED_FIT candidates whose rationale build
    succeeded and whose enqueue dispatched. ``run_degradation_events``
    is a tuple in emission order.
    """

    candidates: tuple[Candidate, ...]
    verdicts: Mapping[str, VerificationVerdict]
    signed_health: SignedHealthTuple
    run_id: str
    run_tiebreak_seed: bytes
    run_wall_ns: int
    per_channel_states: Mapping[str, str]
    per_channel_a_endpoints: Mapping[str, str]
    discover_capstone_events: tuple[CapstoneDegradationEvent, ...]
    verify_stage_state: VerifyStageState
    verify_overflow: int
    verify_degradation_events: tuple[VerifyDegradationEvent, ...]
    review_queue_items: tuple[ReviewQueueItem, ...]
    fit_rationales: Mapping[str, str]
    run_degradation_events: tuple[RunDegradationEvent, ...]


# ---------------------------------------------------------------------------
# Default _build_fit_rationale — deterministic plain-text formatter
# ---------------------------------------------------------------------------


def _summarize_field(value: Any, *, max_chars: int = 200) -> str:
    """Coerce a Candidate / Verdict field to a printable, length-bounded
    string. The clip keeps the default rationale under
    ``MAX_FIT_RATIONALE_BYTES`` regardless of input field lengths.
    """
    if value is None:
        return "—"
    text = str(value)
    if len(text) > max_chars:
        return text[: max_chars - 1] + "…"
    return text


def _build_fit_rationale(
    *,
    session: SessionLike,
    candidate: Candidate,
    verdict: VerificationVerdict,
) -> str:
    """Default rationale builder — deterministic plain-text formatter.

    Pulls VERIFY + Candidate fields per blueprint §9 line 1458. No LLM,
    no network, no subprocess. Production deployments override by
    binding a :class:`BuildFitRationale` implementation via the
    ``build_fit_rationale`` kwarg of
    :func:`run_scout_discover_verify_review`.

    The output is intentionally machine-readable (key/value lines)
    rather than narrative prose — the LLM-driven rationale is the
    deployment's job, not Scout's. Identical inputs always yield
    identical output bytes (replay invariant). The output is clipped
    on a per-field basis so even pathologically long candidate URLs or
    evidence quotes cannot push the total above
    ``MAX_FIT_RATIONALE_BYTES``.
    """
    lines = (
        f"candidate_id: {_summarize_field(candidate.candidate_id, max_chars=64)}",
        f"channel: {_summarize_field(candidate.channel, max_chars=8)}",
        f"funder: {_summarize_field(candidate.funder)}",
        f"funder_kind: {_summarize_field(candidate.funder_kind, max_chars=32)}",
        f"title: {_summarize_field(candidate.title)}",
        f"close_date_utc: {_summarize_field(candidate.close_date_utc, max_chars=64)}",
        f"award_floor: {_summarize_field(candidate.award_floor, max_chars=24)}",
        f"award_ceiling: {_summarize_field(candidate.award_ceiling, max_chars=24)}",
        f"verdict: {_summarize_field(verdict.verdict, max_chars=32)}",
        f"reason_code: {_summarize_field(verdict.reason_code, max_chars=64)}",
        f"live_synopsis_url: {_summarize_field(verdict.live_synopsis_url)}",
        f"fetched_at_utc: {_summarize_field(verdict.fetched_at_utc, max_chars=40)}",
        f"evidence: {_summarize_field(verdict.evidence_quote, max_chars=400)}",
        f"session_slug: {_summarize_field(session.slug, max_chars=64)}",
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public entry — run_scout_discover_verify_review
# ---------------------------------------------------------------------------


def run_scout_discover_verify_review(
    *,
    session: SessionLike,
    channel_fns: Mapping[str, ChannelDiscoverCallable],
    synopsis_fetcher: SynopsisFetcher,
    applicant_profile_provider: ApplicantProfileProvider,
    vault_writer: VaultWriter,
    health_signer: HealthTupleSigner,
    checkpoint_writer_discover: DiscoverCheckpointWriter,
    checkpoint_writer_verify: VerifyCheckpointWriter,
    checkpoint_writer_review: ReviewCheckpointWriter,
    degradation_writer_discover: DiscoverDegradationWriter,
    degradation_writer_verify: VerifyDegradationWriter,
    build_fit_rationale: BuildFitRationale = _build_fit_rationale,
    executor_factory_discover: Optional[DiscoverExecutorFactory] = None,
    executor_factory_verify: Optional[VerifyExecutorFactory] = None,
    interrupt_probe_discover: Optional[DiscoverInterruptProbe] = None,
    interrupt_probe_verify: Optional[VerifyInterruptProbe] = None,
    interrupt_probe_run: Optional[Callable[[], bool]] = None,
    entropy: Optional[DiscoverEntropyFn] = None,
    clock_ns: Optional[DiscoverClockFn] = None,
    clock_iso_verify: Optional[VerifyClockFn] = None,
    clock_iso_review: Optional[ReviewClockFn] = None,
    timeout_seconds: Optional[int] = None,
) -> ScoutRunResult:
    """Capstone-of-capstones — DISCOVER → VERIFY → REVIEW + rationale fan-out.

    Composes Round 8 :func:`run_scout_discover` + Round 9
    :func:`verify_all` + Round 10 :func:`enqueue_for_review` +
    bounded :func:`_build_fit_rationale` per blueprint §4.11 + §9.

    Scope: composition only. R11 does NOT re-author DISCOVER / VERIFY /
    REVIEW primitives — each Round 8/9/10 entry is invoked exactly once
    with its LOCKed signature. Entity research (§4.9) is NOT invoked
    here; Pipeline drives it independently per blueprint §9 line 1447.

    Sequence (blueprint §9 step 2 → step 14):

    1. Validate ``channel_fns`` dispatch-map completeness (six required
       keys A/B/C/D/E/F) — missing → ``KeyError`` with F-SCOUT-RUN-03.
    2. ``run_scout_discover(...)`` — DISCOVER stage. Returns
       :class:`ScoutDiscoverResult`. Per-stage interrupts propagate
       unchanged.
    3. ``verify_all(discover_result=...)`` — VERIFY stage. Returns
       :class:`ScoutVerifyResult`. Per-stage interrupts propagate
       unchanged.
    4. ``run_review_start`` checkpoint.
    5. For each candidate in stable Round-8 order whose verdict is
       VERIFIED_FIT:
       - ``interrupt_probe_run`` — if True, write
         ``run_review_interrupted`` and raise
         :class:`ScoutRunInterrupted`.
       - ``build_fit_rationale(...)`` — bounded LLM call.
         * UTF-8 byte length > ``MAX_FIT_RATIONALE_BYTES`` → record
           F-SCOUT-RUN-01, skip enqueue, continue.
         * Any exception other than ``KeyboardInterrupt`` /
           ``SystemExit`` → record F-SCOUT-RUN-02, skip enqueue,
           continue.
       - ``enqueue_for_review(...)`` — Round 10's REVIEW path. Any
         exception propagates unchanged (transport / deployment
         failure aborts the run).
    6. ``run_review_complete`` checkpoint with outcome=success.
    7. Return :class:`ScoutRunResult`.

    :raises KeyError: F-SCOUT-RUN-03 — dispatch map missing keys.
    :raises ScoutDiscoverInterrupted: DISCOVER stage interrupted.
    :raises ScoutVerifyInterrupted: VERIFY stage interrupted.
    :raises ScoutRunInterrupted: F-SCOUT-RUN-04 — interrupt mid
        run-level fan-out.
    :raises Exception: any DISCOVER / VERIFY / REVIEW propagated
        exception (transport, signer, vault). The capstone re-raises
        unchanged after writing a ``run_review_complete`` checkpoint
        with outcome=failure where applicable.
    """
    # --- Step 1: Validate dispatch-map completeness ------------------------
    required_keys = ("A", "B", "C", "D", "E", "F")
    missing = [k for k in required_keys if k not in channel_fns]
    if missing:
        raise KeyError(
            f"{F_SCOUT_RUN_03}: channel_fns missing keys {missing!r}; "
            f"required={list(required_keys)}"
        )

    run_events: list[RunDegradationEvent] = []
    fit_rationales: dict[str, str] = {}
    review_items: list[ReviewQueueItem] = []

    # --- Step 2: DISCOVER stage --------------------------------------------
    discover_kwargs: dict[str, Any] = {
        "session": session,
        "channel_fns": channel_fns,
        "health_signer": health_signer,
        "checkpoint_writer": checkpoint_writer_discover,
        "degradation_writer": degradation_writer_discover,
    }
    if executor_factory_discover is not None:
        discover_kwargs["executor_factory"] = executor_factory_discover
    if interrupt_probe_discover is not None:
        discover_kwargs["interrupt_probe"] = interrupt_probe_discover
    if entropy is not None:
        discover_kwargs["entropy"] = entropy
    if clock_ns is not None:
        discover_kwargs["clock"] = clock_ns

    try:
        discover_result: ScoutDiscoverResult = run_scout_discover(
            **discover_kwargs
        )
    except (KeyboardInterrupt, SystemExit, ScoutDiscoverInterrupted):
        raise
    except Exception:
        # F-SCOUT-RUN-05 — the signer (or any other DISCOVER raise) has
        # already written its own degradation event inside
        # ``run_scout_discover``. The capstone surfaces the run-level
        # complete-failure checkpoint so the operator can correlate the
        # crash boundary with the run lifecycle.
        checkpoint_writer_review.write(
            stage="run_review_complete",
            payload={
                "session_id": session.session_id,
                "slug": session.slug,
                "outcome": "discover_failed",
                "code": F_SCOUT_RUN_05,
            },
        )
        raise

    # --- Step 3: VERIFY stage ----------------------------------------------
    verify_kwargs: dict[str, Any] = {
        "session": session,
        "discover_result": discover_result,
        "synopsis_fetcher": synopsis_fetcher,
        "applicant_profile_provider": applicant_profile_provider,
        "checkpoint_writer": checkpoint_writer_verify,
        "degradation_writer": degradation_writer_verify,
    }
    if executor_factory_verify is not None:
        verify_kwargs["executor_factory"] = executor_factory_verify
    if interrupt_probe_verify is not None:
        verify_kwargs["interrupt_probe"] = interrupt_probe_verify
    if clock_iso_verify is not None:
        verify_kwargs["clock"] = clock_iso_verify
    if timeout_seconds is not None:
        verify_kwargs["timeout_seconds"] = timeout_seconds

    try:
        verify_result: ScoutVerifyResult = verify_all(**verify_kwargs)
    except (KeyboardInterrupt, SystemExit, ScoutVerifyInterrupted):
        raise
    except Exception:
        checkpoint_writer_review.write(
            stage="run_review_complete",
            payload={
                "session_id": session.session_id,
                "slug": session.slug,
                "outcome": "verify_failed",
            },
        )
        raise

    # --- Step 4: run_review_start checkpoint -------------------------------
    n_verified_fit = sum(
        1
        for v in verify_result.verdicts.values()
        if v.verdict == VERDICT_VERIFIED_FIT
    )
    checkpoint_writer_review.write(
        stage="run_review_start",
        payload={
            "session_id": session.session_id,
            "slug": session.slug,
            "run_id": discover_result.run_id,
            "n_candidates": len(discover_result.candidates),
            "n_verified_fit": n_verified_fit,
        },
    )

    # --- Step 5: Per-VERIFIED_FIT fan-out ----------------------------------
    completed_ids: list[str] = []
    try:
        for cand in discover_result.candidates:
            verdict = verify_result.verdicts.get(cand.candidate_id)
            if verdict is None or verdict.verdict != VERDICT_VERIFIED_FIT:
                continue

            if interrupt_probe_run is not None and interrupt_probe_run():
                checkpoint_writer_review.write(
                    stage="run_review_interrupted",
                    payload={
                        "session_id": session.session_id,
                        "slug": session.slug,
                        "run_id": discover_result.run_id,
                        "completed_candidate_ids": list(completed_ids),
                        "pending_candidate_id": cand.candidate_id,
                    },
                )
                event = RunDegradationEvent(
                    source="run_scout_discover_verify_review",
                    code=F_SCOUT_RUN_04,
                    reason_tag=(
                        f"interrupt signalled before candidate_id="
                        f"{cand.candidate_id} after completed="
                        f"{tuple(completed_ids)}"
                    ),
                    severity=SEVERITY_HIGH,
                    candidate_id=cand.candidate_id,
                )
                run_events.append(event)
                raise ScoutRunInterrupted(tuple(completed_ids))

            # 5a: bounded rationale build
            try:
                rationale_obj = build_fit_rationale(
                    session=session,
                    candidate=cand,
                    verdict=verdict,
                )
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as exc:
                event = RunDegradationEvent(
                    source="run_scout_discover_verify_review",
                    code=F_SCOUT_RUN_02,
                    reason_tag=(
                        f"rationale_build_failed: {type(exc).__name__}: {exc}"
                    ),
                    severity=SEVERITY_HIGH,
                    candidate_id=cand.candidate_id,
                )
                run_events.append(event)
                continue

            # Type guard — non-str output is treated as builder failure
            # (F-SCOUT-RUN-02), not budget overflow.
            if not isinstance(rationale_obj, str):
                event = RunDegradationEvent(
                    source="run_scout_discover_verify_review",
                    code=F_SCOUT_RUN_02,
                    reason_tag=(
                        f"rationale_non_str: type="
                        f"{type(rationale_obj).__name__}"
                    ),
                    severity=SEVERITY_HIGH,
                    candidate_id=cand.candidate_id,
                )
                run_events.append(event)
                continue

            # 5b: byte-budget enforcement (strict >)
            byte_len = len(rationale_obj.encode("utf-8"))
            if byte_len > MAX_FIT_RATIONALE_BYTES:
                event = RunDegradationEvent(
                    source="run_scout_discover_verify_review",
                    code=F_SCOUT_RUN_01,
                    reason_tag=(
                        f"rationale_oversize: bytes={byte_len} "
                        f"max={MAX_FIT_RATIONALE_BYTES}"
                    ),
                    severity=SEVERITY_HIGH,
                    candidate_id=cand.candidate_id,
                )
                run_events.append(event)
                continue

            fit_rationales[cand.candidate_id] = rationale_obj

            # 5c: REVIEW enqueue (R10 path) — exceptions propagate.
            enqueue_kwargs: dict[str, Any] = {
                "session": session,
                "candidate": cand,
                "verdict": verdict,
                "fit_rationale": rationale_obj,
                "vault_writer": vault_writer,
                "checkpoint_writer": checkpoint_writer_review,
            }
            if clock_iso_review is not None:
                enqueue_kwargs["clock"] = clock_iso_review

            item = enqueue_for_review(**enqueue_kwargs)
            review_items.append(item)
            completed_ids.append(cand.candidate_id)

    except (KeyboardInterrupt, SystemExit):
        raise
    except ScoutRunInterrupted:
        raise
    except Exception:
        checkpoint_writer_review.write(
            stage="run_review_complete",
            payload={
                "session_id": session.session_id,
                "slug": session.slug,
                "run_id": discover_result.run_id,
                "outcome": "review_failed",
                "completed_candidate_ids": list(completed_ids),
            },
        )
        raise

    # --- Step 6: run_review_complete checkpoint ----------------------------
    checkpoint_writer_review.write(
        stage="run_review_complete",
        payload={
            "session_id": session.session_id,
            "slug": session.slug,
            "run_id": discover_result.run_id,
            "outcome": "success",
            "n_review_items": len(review_items),
            "n_run_events": len(run_events),
            "completed_candidate_ids": list(completed_ids),
        },
    )

    # --- Step 7: Assemble + return -----------------------------------------
    return ScoutRunResult(
        candidates=discover_result.candidates,
        verdicts=dict(verify_result.verdicts),
        signed_health=discover_result.signed_health,
        run_id=discover_result.run_id,
        run_tiebreak_seed=discover_result.run_tiebreak_seed,
        run_wall_ns=discover_result.run_wall_ns,
        per_channel_states=dict(discover_result.per_channel_states),
        per_channel_a_endpoints=dict(discover_result.per_channel_a_endpoints),
        discover_capstone_events=discover_result.capstone_degradation_events,
        verify_stage_state=verify_result.verify_stage_state,
        verify_overflow=verify_result.overflow,
        verify_degradation_events=verify_result.verify_degradation_events,
        review_queue_items=tuple(review_items),
        fit_rationales=dict(fit_rationales),
        run_degradation_events=tuple(run_events),
    )


# ---------------------------------------------------------------------------
# Verbatim alias — Step 0 reconciliation #1
# ---------------------------------------------------------------------------


run_scout_discover_verify = run_scout_discover_verify_review
"""Verbatim alias of :func:`run_scout_discover_verify_review`.

Blueprint §4.11 sketch (line 1022) names the entry point
``run_scout_discover_verify``; the operator-disposed name is
``run_scout_discover_verify_review`` (the longer name reflects the
actual scope including REVIEW). Both names resolve to the same
function object — ``is`` identity holds — so blueprint § 9 step 13
+ §4.11 sketch consumers (Section 5 Pipeline) work without an
in-flight blueprint amendment.
"""
