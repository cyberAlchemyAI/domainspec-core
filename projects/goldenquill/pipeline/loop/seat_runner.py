"""pipeline.loop.seat_runner — §4.3/§4.4/§4.5 invoke_seat + cascade advance.

Blueprint §5 v6 LOCKED 2026-04-19:

- §4.3 Scribe invocation (v2 tuple return + minimal-env subprocess)
- §4.4 Editor invocation (cross-family != Scribe.actual_landed_family)
- §4.5 Judge invocation (three-way cross-family + inline parse, A-v1-15)
- §4.9 select_cascade_level (live ``run_iteration_families_so_far`` consult)
- §3.2.3 SeatCharter / §3.2.4 ProviderCascade consumer
- §6 F-PIPE-06 (cascade exhausted via timeouts), F-PIPE-08 (cross-family
     violation), F-PIPE-09 (Judge output malformed)
- §8 SCRIBE/EDITOR/JUDGE_SUBPROCESS_TIMEOUT_MS — used as INLINE LITERALS at
  dispatch (V1 discipline: rebind of ``pipeline.loop.config`` constants does
  NOT alter Round-4 runtime behaviour)

Round 4 is the first round that CONSUMES Round 1's ``SeatCharter`` +
``ProviderCascade``. All subprocess launches go through an injected
:class:`SubprocessLauncher` Protocol (E-017 pattern). Production wires
§2 Vault's ``seat_launch``; tests inject a deterministic stub.

**Design decisions (confirmed at Round 4 ORIENT — 2026-04-20)**

1. *One public entry point + three thin per-seat wrappers.*
   :func:`invoke_seat` dispatches on ``seat_kind``. :func:`invoke_scribe`,
   :func:`invoke_editor`, :func:`invoke_judge` pin ``seat_kind`` + forward
   every other argument. Round 5 revision_loop may call either the
   dispatcher or the per-seat wrapper — both are supported.

2. *Timeouts are inline literals.* ``300_000`` / ``180_000`` / ``180_000``
   ms are pinned at the dispatch site. ``pipeline.loop.config.*``
   rebinds cannot change Round-4 runtime behaviour. Consistency with
   §5 Round 2 back-off-schedule discipline (E-023 rebind-resistance).

3. *Minimal-env enforcement is caller-side (A-v1-13).* Round 4 constructs
   the child env dict with EXACTLY the 6 whitelisted keys
   (``PATH``, ``HOME``, ``TILTH_SESSION_ID``, ``TILTH_RUN_ID``,
   ``TILTH_ORG_SLUG``, ``TILTH_SEAT_KIND``) and verifies set-equality via
   an inline-literal frozenset before handing to the launcher. The
   launcher MUST NOT widen.

4. *Cross-family PRE-gate uses the current cascade level's family, not the
   charter's ``allowed_families`` set.* Blueprint §4.9 line 628 explicitly
   consults ``run_state.run_iteration_families_so_far`` live, comparing
   the family of the level ABOUT to be dispatched. On collision we
   ADVANCE the cascade (skip the colliding level) and retry. If the
   cascade exhausts with every remaining level colliding (never observed
   a timeout), we raise :class:`F_PIPE_08` with trigger
   ``same_family_as_scribe`` (editor) or ``same_family_as_scribe_or_editor``
   (judge). — **Deviation from spec-card point 4 (assert-at-dispatch);
   see correction note below.**

5. *Judge parse is inline (A-v1-15).* After a successful subprocess return
   for ``seat_kind="judge"``, Round 4 decodes + parses stdout as JSON via
   the injected :class:`JudgeParseCallable` (default
   :func:`default_judge_parse`) and returns the parsed ``judge_verdict``
   alongside the output hash. Parse failure raises :class:`F_PIPE_09`
   with trigger ``judge_parse_failed``. The success-checkpoint write is
   the revision loop's responsibility (Round 5); Round 4 returns pure
   data.

6. *ProviderCascade is returned fresh on every invocation.* Even though
   the Round-1 dataclass is not technically frozen, Round 4 treats it
   as immutable and returns a new instance via :func:`dataclasses.replace`
   so the caller can persist the post-invocation cascade without
   shared-reference mutation.

7. *``vault_write`` / ``clock`` / ``sleep`` default to ``None``.* They are
   reserved for Round 5 (draft-vault-persistence per blueprint §4.3 step
   5 interim pattern + STR observation emission) and Round 7
   (inter-level jitter per A-v1-09). Round 4 does not invoke them; an
   adversarial test
   (``test_adv_vault_write_clock_sleep_not_called``) pins the contract.
   Signatures stay forward-stable across Rounds 5+7 without breaking.

8. *Context is bundled in :class:`SeatInvocationContext`.* The four
   non-Protocol inputs (``stdin_payload``, ``session_id``, ``path_value``,
   ``home_value``) are collected into a frozen dataclass so future
   rounds can extend invocation context (eval-mode flags, locale
   overrides, trace-id injection) without growing the signature.

9. *AST-lint R2 compliance.* This module lives under ``pipeline/loop/``
   and MUST NOT import :mod:`pipeline.logician`. The Round-1-shipped
   AST-lint ``loop-logician-ban`` rule enforces at lint time.

**Spec-card corrections filed at Round 4 build (2026-04-20)**

The pre-staged Round 4 spec card carried three errors; the canonical
corrections are pinned here (and in
``pipeline/engineering/spec_cards/section_05_round_4_seat_runner.md``
as a post-facto addendum):

- Spec card point 2 referenced ``F_PIPE_17.cascade_exhausted`` for
  timeout-driven cascade exhaustion. Per :mod:`pipeline.loop.errors`,
  F_PIPE_17 is ``bypass_authorization_ledger_write_failed``; F_PIPE_06
  is the documented ``cascade exhausts + retries`` code. Round 4 uses
  :class:`F_PIPE_06` with trigger ``cascade_exhausted`` when any
  timeout was observed during exhaustion.

- Spec card point 4 referenced ``F_PIPE_09.same_family_as_scribe_or_editor``
  for Judge cross-family violation. F_PIPE_09 is ``judge_output_malformed``;
  F_PIPE_08 is ``cross_family_violation``. Round 4 uses :class:`F_PIPE_08`
  for all cross-family outcomes (matches blueprint §4.9 line 646's
  ``F_PIPE_08_cross_family_exhausted``).

- Spec card point 4 framed cross-family as "assert BEFORE any subprocess
  launch." Blueprint §4.9 ``select_cascade_level`` consults the live
  ``run_iteration_families_so_far`` per level and skips colliding
  levels. Round 4 implements level-skipping; F_PIPE_08 fires only when
  the cascade exhausts with every remaining level colliding. This is
  more faithful to the architecture and preserves the timeout-vs-collision
  distinction at the exhaustion site.

**Threat model (§3.11 v5 trusted-operator envelope; E-023 closure)**

Round 4 is an internal orchestrator consumed only by trusted Round-5+
code that supplies a conforming :class:`SubprocessLauncher`. The
following residuals are OUT-OF-SCOPE for v0.1 and documented by explicit
``test_adv_*`` tests rather than defended at this layer:

- **Malformed ``SubprocessLauncher`` return.** Round 4 trusts the
  :class:`SubprocessResult` shape. A launcher that returns
  ``timed_out=False`` alongside a non-zero ``exit_code`` flows through
  as if the seat succeeded; the subprocess's own failure encoding lives
  in stdout/stderr and is (per §4.5 for Judge) parsed by Round 4 for
  Judge only. Non-Judge seats' exit-code semantics are the caller's
  concern (Round 5 revision_loop inspects the result).

- **Adversarial ``stdout`` that JSON-parses to a dict but is semantically
  garbage for Judge.** Round 4's default parser accepts any non-empty
  JSON object. Semantic validation (score ranges, rubric dimensions) is
  a higher-layer concern (§4 Logician POST-gate, §5 revision_loop).

Spec card: ``pipeline/engineering/spec_cards/section_05_round_4_seat_runner.md``.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from typing import Any, Final, Literal, Protocol, runtime_checkable

from pipeline.loop.errors import (
    F_PIPE_06,
    F_PIPE_08,
    F_PIPE_09,
)
from pipeline.loop.state_checkpoint import (
    ClockProtocol,
    SleepCallable,
    VaultWriteCallable,
)
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
            "§4.3 Scribe invocation (A-v1-02 tuple return)",
            "§4.4 Editor invocation (cross-family != Scribe)",
            "§4.5 Judge invocation (three-way cross-family + A-v1-15 parse)",
            "§4.9 select_cascade_level (live families consult)",
            "§6 F-PIPE-06/08/09 failure dispatch",
            "§8 SCRIBE/EDITOR/JUDGE_SUBPROCESS_TIMEOUT_MS (inline-literal)",
        ],
    },
    "section_05_v6_amendment.md": {
        "version": "LOCK-READY",
        "hash_sha3_512_prefix16": "52ae6b3b97b159b5",
        "sections_implemented": [
            "pointer-only: Round 5+ wires STR observation emission via clock",
        ],
    },
}


# ---------------------------------------------------------------------------
# A-v1-13 minimal-env whitelist (inline-literal frozenset + module-load assert)
# ---------------------------------------------------------------------------

MINIMAL_ENV_ALLOWED_KEYS: Final[frozenset[str]] = frozenset(
    {
        "PATH",
        "HOME",
        "TILTH_SESSION_ID",
        "TILTH_RUN_ID",
        "TILTH_ORG_SLUG",
        "TILTH_SEAT_KIND",
    }
)
assert MINIMAL_ENV_ALLOWED_KEYS == frozenset(
    {
        "PATH",
        "HOME",
        "TILTH_SESSION_ID",
        "TILTH_RUN_ID",
        "TILTH_ORG_SLUG",
        "TILTH_SEAT_KIND",
    }
), (
    "MINIMAL_ENV_ALLOWED_KEYS has been rebound at module load; "
    "refusing to load pipeline.loop.seat_runner"
)


# ---------------------------------------------------------------------------
# Public dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class SubprocessResult:
    """One subprocess invocation outcome reported by a :class:`SubprocessLauncher`.

    ``timed_out`` MUST be True iff the subprocess hit ``timeout_ms``. A
    timed-out result MUST have ``exit_code`` reflecting the process's
    kill signal (or 0 if the launcher chose to normalize) — Round 4
    branches purely on ``timed_out``. ``landed_family`` /
    ``landed_model_id`` are what the subprocess reports it actually ran
    on (A-v1-02 trust model: the subprocess is the source of truth
    after any internal fallback).
    """

    exit_code: int
    stdout: bytes
    stderr: bytes
    timed_out: bool
    landed_family: str
    landed_model_id: str


@runtime_checkable
class SubprocessLauncher(Protocol):
    """Inject for deterministic tests; production wires §2 Vault ``seat_launch``.

    The launcher is responsible for:

    - constructing the minimal-env child (keys provided by Round 4);
    - writing ``stdin_payload`` to the child's stdin;
    - enforcing ``timeout_ms`` (SIGKILL on expiry);
    - returning a :class:`SubprocessResult`.

    Round 4 does NOT spawn processes directly — A-v1-13 enforcement.
    """

    def __call__(
        self,
        *,
        seat_kind: str,
        env: dict[str, str],
        stdin_payload: bytes,
        timeout_ms: int,
        family: str,
        model_id: str,
    ) -> SubprocessResult: ...


@runtime_checkable
class JudgeParseCallable(Protocol):
    """Injected Judge stdout parser. Default: :func:`default_judge_parse`.

    On success returns a ``dict[str, Any]`` judge verdict. On failure
    raises any exception; Round 4 catches and wraps as :class:`F_PIPE_09`
    with trigger ``judge_parse_failed``.
    """

    def __call__(self, stdout: bytes) -> dict[str, Any]: ...


@dataclass(frozen=True, kw_only=True, slots=True)
class SeatInvocationContext:
    """Non-Protocol invocation context for :func:`invoke_seat`.

    Bundling four correlated scalar inputs (``stdin_payload`` +
    ``session_id`` + ``path_value`` + ``home_value``) into a frozen
    dataclass keeps the :func:`invoke_seat` signature stable across
    future rounds that need to extend context.

    - ``stdin_payload``: raw bytes the launcher writes to the child's
      stdin (typically a JSON envelope constructed by Round 5).
    - ``session_id``: §2 Vault session binding; populates
      ``TILTH_SESSION_ID`` env.
    - ``path_value`` / ``home_value``: literal values for ``PATH`` /
      ``HOME`` env. Production passes the parent's values; tests inject
      deterministic stubs so the child env is reproducible.
    """

    stdin_payload: bytes
    session_id: str
    path_value: str
    home_value: str


@dataclass(frozen=True, kw_only=True, slots=True)
class SeatInvocationResult:
    """§4.3/§4.4/§4.5 A-v1-02 tuple return, packaged.

    ``output_hash`` is SHA-256 hex of subprocess stdout (pre-parse, raw
    bytes). ``raw_stdout`` is the subprocess stdout bytes verbatim — the
    revision loop (Round 5) uses it to persist Scribe / Editor drafts
    to vault alongside the hash, and to re-parse Judge output downstream
    if needed. For Judge, ``judge_verdict`` is the parsed payload; for
    Scribe and Editor it is None. ``cascade_after`` is a fresh
    :class:`ProviderCascade` instance reflecting ``current_level`` after
    any in-invocation advances. ``level_advances`` counts how many
    cascade levels were burned by timeouts + cross-family collisions
    during this invocation — 0 on first-level success.
    """

    output_hash: str
    raw_stdout: bytes
    landed_family: str
    landed_model_id: str
    cascade_after: ProviderCascade
    level_advances: int
    judge_verdict: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------


def default_judge_parse(stdout: bytes) -> dict[str, Any]:
    """§4.5 default Judge-output parser.

    Decodes UTF-8, ``json.loads``, verifies top-level is a non-empty
    dict. Any deviation raises :class:`ValueError` — Round 4 wraps as
    :class:`F_PIPE_09` with trigger ``judge_parse_failed``.

    Semantic validation (score ranges, rubric dimensions) is
    higher-layer (§4 Logician POST-gate); this parser only enforces
    structural shape.
    """

    text = stdout.decode("utf-8")
    obj = json.loads(text)
    if not isinstance(obj, dict):
        raise ValueError(
            f"judge output must be a JSON object; got {type(obj).__name__}"
        )
    if not obj:
        raise ValueError("judge output must be a non-empty JSON object")
    return obj


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_minimal_env(
    *,
    session_id: str,
    run_id: str,
    org_slug: str,
    seat_kind: str,
    path_value: str,
    home_value: str,
) -> dict[str, str]:
    """A-v1-13 enforcement: construct the exact 6-key child env.

    Inline-literal key list; the final set-equality check uses an inline
    frozenset literal on the RHS so a rebind of
    :data:`MINIMAL_ENV_ALLOWED_KEYS` cannot widen the whitelist at
    runtime.
    """

    env: dict[str, str] = {
        "PATH": path_value,
        "HOME": home_value,
        "TILTH_SESSION_ID": session_id,
        "TILTH_RUN_ID": run_id,
        "TILTH_ORG_SLUG": org_slug,
        "TILTH_SEAT_KIND": seat_kind,
    }
    if frozenset(env.keys()) != frozenset(
        {
            "PATH",
            "HOME",
            "TILTH_SESSION_ID",
            "TILTH_RUN_ID",
            "TILTH_ORG_SLUG",
            "TILTH_SEAT_KIND",
        }
    ):
        raise RuntimeError(
            "seat_runner _build_minimal_env produced a non-whitelisted key set; "
            f"observed={sorted(env.keys())!r}"
        )
    return env


def _level_collides_with_prior(
    *,
    seat_kind: str,
    level_family: str,
    run_state: RunState,
) -> tuple[bool, str | None]:
    """§4.9 live cross-family consult for one cascade level.

    Returns ``(collides, trigger)`` — trigger is the F_PIPE_08
    sub-trigger string on collision, None otherwise.

    - Scribe: never collides (no prior seat in the iteration).
    - Editor: collides iff Scribe's landed family equals ``level_family``
      (trigger ``same_family_as_scribe``).
    - Judge: collides iff Scribe's OR Editor's landed family equals
      ``level_family`` (trigger ``same_family_as_scribe_or_editor``).
    """

    if seat_kind == "scribe":
        return False, None

    scribe_tuple = run_state.run_iteration_families_so_far.get("scribe")
    if seat_kind == "editor":
        if scribe_tuple is not None and scribe_tuple[0] == level_family:
            return True, "same_family_as_scribe"
        return False, None

    if seat_kind == "judge":
        editor_tuple = run_state.run_iteration_families_so_far.get("editor")
        if scribe_tuple is not None and scribe_tuple[0] == level_family:
            return True, "same_family_as_scribe_or_editor"
        if editor_tuple is not None and editor_tuple[0] == level_family:
            return True, "same_family_as_scribe_or_editor"
        return False, None

    # seat_kind == "red_team" — strict 3-way distinct (§10.7 + §5 v7 §4.5a):
    # Red Team's resolved family must differ from BOTH Scribe's AND Judge's.
    # Editor is NOT in the constraint set — Editor's family overlap with
    # Red Team is not a §10.7 violation (§E pairwise applies to Judge↔Scribe
    # only; §10 strict 3-way extends to Red Team↔Scribe + Red Team↔Judge).
    judge_tuple = run_state.run_iteration_families_so_far.get("judge")
    if scribe_tuple is not None and scribe_tuple[0] == level_family:
        return True, "same_family_as_scribe"  # F-RT-FAMILY-OVERLAP.with_scribe
    if judge_tuple is not None and judge_tuple[0] == level_family:
        return True, "same_family_as_judge"  # F-RT-FAMILY-OVERLAP.with_judge
    return False, None


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def invoke_seat(
    *,
    seat_kind: Literal["scribe", "editor", "judge", "red_team"],
    run_state: RunState,
    iteration_number: int,
    charter: SeatCharter,
    cascade: ProviderCascade,
    context: SeatInvocationContext,
    subprocess_launcher: SubprocessLauncher,
    judge_parse: JudgeParseCallable | None = None,
    vault_write: VaultWriteCallable | None = None,
    clock: ClockProtocol | None = None,
    sleep: SleepCallable | None = None,
) -> SeatInvocationResult:
    """§4.3/§4.4/§4.5 per-seat subprocess invocation + cascade advance.

    Dispatch on ``seat_kind``:

    - ``"scribe"``: timeout = ``300_000`` ms (inline literal).
    - ``"editor"``: timeout = ``180_000`` ms (inline literal).
    - ``"judge"``:  timeout = ``180_000`` ms (inline literal) + inline parse.

    For each cascade level starting at ``cascade.current_level``:

    1. Check cross-family collision (§4.9 live consult). On collision,
       ADVANCE level and continue.
    2. Construct minimal env (A-v1-13) + launch subprocess via
       :class:`SubprocessLauncher`.
    3. On timeout, ADVANCE level and continue.
    4. On non-timeout return, compute ``output_hash`` + (for Judge)
       parse. Parse failure raises :class:`F_PIPE_09`. Non-Judge
       returns directly.

    Cascade exhaustion distinguishes two cases:

    - **Any timeout observed** (mixed or pure-timeout): :class:`F_PIPE_06`
      with trigger ``cascade_exhausted``.
    - **Pure cross-family exhaustion** (never observed a timeout):
      :class:`F_PIPE_08` with trigger ``same_family_as_scribe`` or
      ``same_family_as_scribe_or_editor`` (last-collision trigger).

    ``vault_write`` / ``clock`` / ``sleep`` are accepted but not invoked
    by Round 4. They default to ``None``. The pin test
    ``test_adv_vault_write_clock_sleep_not_called`` asserts zero calls.
    """

    # Round-4 unused Protocol inputs — kept in signature for Round-5+7
    # forward-compatibility. Read-only reference tuple silences unused-arg
    # warnings without invoking the callables.
    _ = vault_write, clock, sleep

    if seat_kind not in frozenset({"scribe", "editor", "judge", "red_team"}):
        raise ValueError(
            f"seat_kind must be one of scribe/editor/judge/red_team; got {seat_kind!r}"
        )

    if charter.seat_kind != seat_kind:
        raise ValueError(
            f"charter.seat_kind {charter.seat_kind!r} does not match "
            f"invoke_seat seat_kind {seat_kind!r}"
        )

    if cascade.seat_kind != seat_kind:
        raise ValueError(
            f"cascade.seat_kind {cascade.seat_kind!r} does not match "
            f"invoke_seat seat_kind {seat_kind!r}"
        )

    if iteration_number < 1:
        raise ValueError(
            f"iteration_number must be >= 1; got {iteration_number}"
        )

    # Inline-literal timeout dispatch — V1 rebind-resistance.
    if seat_kind == "scribe":
        timeout_ms: int = 300_000
    elif seat_kind == "editor":
        timeout_ms = 180_000
    elif seat_kind == "judge":
        timeout_ms = 180_000
    else:  # red_team — same default as Judge per §10 R3 GROQ_DEFAULT_TIMEOUT_SEC=60s
        # but seat-runner timeout is wall-clock subprocess ceiling, not provider HTTP.
        # Match Judge's 180_000 ms ceiling for symmetry; per-iteration cost is similar.
        timeout_ms = 180_000

    parser: JudgeParseCallable = (
        judge_parse if judge_parse is not None else default_judge_parse
    )

    start_level = cascade.current_level
    current_level = start_level
    last_collision_trigger: str | None = None
    any_timeout_observed = False

    while current_level < len(cascade.levels):
        level_family, level_model_id = cascade.levels[current_level]

        collides, collision_trigger = _level_collides_with_prior(
            seat_kind=seat_kind,
            level_family=level_family,
            run_state=run_state,
        )
        if collides:
            last_collision_trigger = collision_trigger
            current_level += 1
            continue

        env = _build_minimal_env(
            session_id=context.session_id,
            run_id=run_state.run_id,
            org_slug=run_state.org_slug,
            seat_kind=seat_kind,
            path_value=context.path_value,
            home_value=context.home_value,
        )

        result = subprocess_launcher(
            seat_kind=seat_kind,
            env=env,
            stdin_payload=context.stdin_payload,
            timeout_ms=timeout_ms,
            family=level_family,
            model_id=level_model_id,
        )

        if result.timed_out:
            any_timeout_observed = True
            current_level += 1
            continue

        # Non-timeout return — materialize result.
        output_hash = _sha256_hex(result.stdout)

        judge_verdict: dict[str, Any] | None = None
        if seat_kind == "judge":
            try:
                judge_verdict = parser(result.stdout)
            except Exception as exc:
                raise F_PIPE_09(
                    trigger="judge_parse_failed",
                    details={
                        "iteration_number": iteration_number,
                        "parser_error": type(exc).__name__,
                        "parser_message": str(exc),
                        "landed_family": result.landed_family,
                        "landed_model_id": result.landed_model_id,
                    },
                ) from exc
        elif seat_kind == "red_team":
            # Red Team output parsed via the same path as Judge (JSON dict
            # with total_score/recommendation/criteria/attack_memo per §10.5).
            # Re-uses ``judge_verdict`` field on SeatInvocationResult to
            # avoid widening the result schema; revision_loop reads
            # red_team_result.judge_verdict and threads it as
            # red_team_verdict at the IterationState layer.
            try:
                judge_verdict = parser(result.stdout)
            except Exception as exc:
                raise F_PIPE_09(
                    trigger="red_team_parse_failed",
                    details={
                        "iteration_number": iteration_number,
                        "parser_error": type(exc).__name__,
                        "parser_message": str(exc),
                        "landed_family": result.landed_family,
                        "landed_model_id": result.landed_model_id,
                    },
                ) from exc

        cascade_after = replace(cascade, current_level=current_level)
        level_advances = current_level - start_level

        return SeatInvocationResult(
            output_hash=output_hash,
            raw_stdout=result.stdout,
            landed_family=result.landed_family,
            landed_model_id=result.landed_model_id,
            cascade_after=cascade_after,
            level_advances=level_advances,
            judge_verdict=judge_verdict,
        )

    # Cascade exhausted. Classify:
    #
    # - Any timeout observed (mixed or pure-timeout) → F_PIPE_06
    #   cascade_exhausted. The cascade was actually exercised; treating
    #   this as a timeout exhaustion preserves the revision loop's
    #   ability to distinguish "all providers slow" from "no compatible
    #   provider available."
    # - Pure cross-family exhaustion (never observed a timeout) →
    #   F_PIPE_08 with the most-recent collision trigger. The charter's
    #   cascade was structurally incompatible with the live prior-seat
    #   families.
    if any_timeout_observed:
        raise F_PIPE_06(
            trigger="cascade_exhausted",
            details={
                "seat_kind": seat_kind,
                "iteration_number": iteration_number,
                "start_level": start_level,
                "exhausted_at_level": current_level,
                "cascade_levels": [list(level) for level in cascade.levels],
            },
        )

    # No timeout observed; every advance was a collision.
    assert last_collision_trigger is not None, (
        "cascade loop exited without timeout or collision — unreachable; "
        "ProviderCascade.__post_init__ forbids current_level == len(levels) "
        "at construction, and the while-predicate guards the empty-cascade case"
    )
    raise F_PIPE_08(
        trigger=last_collision_trigger,
        details={
            "seat_kind": seat_kind,
            "iteration_number": iteration_number,
            "start_level": start_level,
            "exhausted_at_level": current_level,
            "scribe_family": (
                run_state.run_iteration_families_so_far.get("scribe", (None,))[0]
            ),
            "editor_family": (
                run_state.run_iteration_families_so_far.get("editor", (None,))[0]
            ),
            "cascade_levels": [list(level) for level in cascade.levels],
        },
    )


# ---------------------------------------------------------------------------
# Per-seat thin wrappers (spec-card point 1)
# ---------------------------------------------------------------------------


def invoke_scribe(
    *,
    run_state: RunState,
    iteration_number: int,
    charter: SeatCharter,
    cascade: ProviderCascade,
    context: SeatInvocationContext,
    subprocess_launcher: SubprocessLauncher,
    judge_parse: JudgeParseCallable | None = None,
    vault_write: VaultWriteCallable | None = None,
    clock: ClockProtocol | None = None,
    sleep: SleepCallable | None = None,
) -> SeatInvocationResult:
    """§4.3 thin wrapper — pins ``seat_kind="scribe"``."""

    return invoke_seat(
        seat_kind="scribe",
        run_state=run_state,
        iteration_number=iteration_number,
        charter=charter,
        cascade=cascade,
        context=context,
        subprocess_launcher=subprocess_launcher,
        judge_parse=judge_parse,
        vault_write=vault_write,
        clock=clock,
        sleep=sleep,
    )


def invoke_editor(
    *,
    run_state: RunState,
    iteration_number: int,
    charter: SeatCharter,
    cascade: ProviderCascade,
    context: SeatInvocationContext,
    subprocess_launcher: SubprocessLauncher,
    judge_parse: JudgeParseCallable | None = None,
    vault_write: VaultWriteCallable | None = None,
    clock: ClockProtocol | None = None,
    sleep: SleepCallable | None = None,
) -> SeatInvocationResult:
    """§4.4 thin wrapper — pins ``seat_kind="editor"``."""

    return invoke_seat(
        seat_kind="editor",
        run_state=run_state,
        iteration_number=iteration_number,
        charter=charter,
        cascade=cascade,
        context=context,
        subprocess_launcher=subprocess_launcher,
        judge_parse=judge_parse,
        vault_write=vault_write,
        clock=clock,
        sleep=sleep,
    )


def invoke_judge(
    *,
    run_state: RunState,
    iteration_number: int,
    charter: SeatCharter,
    cascade: ProviderCascade,
    context: SeatInvocationContext,
    subprocess_launcher: SubprocessLauncher,
    judge_parse: JudgeParseCallable | None = None,
    vault_write: VaultWriteCallable | None = None,
    clock: ClockProtocol | None = None,
    sleep: SleepCallable | None = None,
) -> SeatInvocationResult:
    """§4.5 thin wrapper — pins ``seat_kind="judge"``."""

    return invoke_seat(
        seat_kind="judge",
        run_state=run_state,
        iteration_number=iteration_number,
        charter=charter,
        cascade=cascade,
        context=context,
        subprocess_launcher=subprocess_launcher,
        judge_parse=judge_parse,
        vault_write=vault_write,
        clock=clock,
        sleep=sleep,
    )


def invoke_red_team(
    *,
    run_state: RunState,
    iteration_number: int,
    charter: SeatCharter,
    cascade: ProviderCascade,
    context: SeatInvocationContext,
    subprocess_launcher: SubprocessLauncher,
    judge_parse: JudgeParseCallable | None = None,
    vault_write: VaultWriteCallable | None = None,
    clock: ClockProtocol | None = None,
    sleep: SleepCallable | None = None,
) -> SeatInvocationResult:
    """§4.5a thin wrapper — pins ``seat_kind="red_team"`` (§5 v7 amendment).

    Fires AFTER Judge per iteration. Red Team subprocess parses stdout the
    same way Judge does (via the shared ``judge_parse`` callable; the
    parameter name is preserved from R4 for shape-compatibility — Red Team's
    output is also a JSON dict with ``total_score`` + ``recommendation`` +
    ``criteria`` + ``attack_memo`` per §10.5).

    Cross-family rigor (§10.7 strict 3-way distinct): the caller MUST verify
    Red Team's resolved family ≠ Scribe's AND ≠ Judge's via
    ``run_state.run_iteration_families_so_far`` BEFORE this call. The
    cascade-reorder check + F-RT-FAMILY-OVERLAP PRE-gate live in the caller
    (revision_loop.run_inner_loop §5 v7 §4.5a).
    """

    return invoke_seat(
        seat_kind="red_team",
        run_state=run_state,
        iteration_number=iteration_number,
        charter=charter,
        cascade=cascade,
        context=context,
        subprocess_launcher=subprocess_launcher,
        judge_parse=judge_parse,
        vault_write=vault_write,
        clock=clock,
        sleep=sleep,
    )


__all__ = [
    "BLUEPRINT_DEPS",
    "MINIMAL_ENV_ALLOWED_KEYS",
    "SubprocessResult",
    "SubprocessLauncher",
    "JudgeParseCallable",
    "SeatInvocationContext",
    "SeatInvocationResult",
    "default_judge_parse",
    "invoke_seat",
    "invoke_scribe",
    "invoke_editor",
    "invoke_judge",
    "invoke_red_team",
]
