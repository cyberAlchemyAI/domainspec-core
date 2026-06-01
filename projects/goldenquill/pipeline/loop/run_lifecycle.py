"""pipeline.loop.run_lifecycle — §4.1 start_run + resume_run (Round 3).

Blueprint §5 v6 LOCKED 2026-04-19:
- §4.1 run lifecycle (v2 + v5 resume-phase validation + schema-enforcement)
- §3.2.1 RunState (mode-discriminated union construction)
- §6 F-PIPE-18 (resume_phase_mismatch), F-PIPE-22 (runstate_schema_downgrade)

Round 3 ships the two orchestrator entry points that wrap Round 2's
``checkpoint_atomic`` with full lifecycle semantics.

**Core design decisions (reaffirmed at Round 3 build time)**

1. *Zero runtime LLM calls.* All vault I/O via injected Protocols; all
   timestamps via ``ClockProtocol``. Round 2's ``checkpoint_atomic`` is the
   ONLY checkpoint path — ``run_lifecycle`` never touches the vault directly
   for success-path writes. Quarantine-path writes on resume-phase mismatch
   go through ``_write_quarantine_marker`` directly (there's no "last known
   good" checkpoint to CAS-commit on that branch).

2. *v5 MA-07 / MB-05 strict ordering on resume.* Schema check runs BEFORE
   phase check. A downgraded schema may have renamed or removed the ``phase``
   field; validating ``phase`` against a distrusted schema is unsafe. On
   F_PIPE_22, the state-failure wrapper writes BEFORE re-raise.

3. *Allowed resume phase sets are INLINE FROZENSETS.* V1 discipline — a
   module-attribute rebinding cannot broaden the set. Two sets, dispatched
   on ``rs.mode`` per blueprint §4.1 resume path.

4. *No unions; two entry points.* ``start_run`` mints + initializes;
   ``resume_run`` reads + validates. They do not share a private helper
   beyond the Round 2 checkpoint primitive.

5. *RunIdFactory and VaultReadCallable are E-017 Protocols.* Round 3 is the
   first round that needs reads (Round 2 was write-only).

**Threat model (§3.11 v5 trusted-operator envelope; E-023 closure)**

Round 3 is an internal orchestrator consumed only by trusted Round 4+ code
(seat_runner, revision_loop, three_tab_delivery, eval_mode). The following
residuals are OUT-OF-SCOPE for v0.1 and documented by explicit ``test_adv_*``
tests rather than defended at this layer:

- **Malformed ``vault_read`` return.** Round 3 trusts the callable's return
  to be well-formed JSON matching the RunState schema. Garbled bytes raise
  either ``json.JSONDecodeError`` or ``F_PIPE_22`` at RunState construction
  — both terminate resume cleanly.

- **``run_id`` path-segment interpolation.** Same trust as Round 2: the
  ``RunIdFactory`` (ULID charset) and §2 Vault's path validator are the
  guards. Round 3 does not re-validate.

Spec card: ``pipeline/engineering/spec_cards/section_05_round_3_run_lifecycle.md``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Final, Literal, Protocol, runtime_checkable

from pipeline.loop.errors import F_PIPE_18, F_PIPE_22
from pipeline.loop.state_checkpoint import (
    ClockProtocol,
    SleepCallable,
    VaultWriteCallable,
    _assert_runstate_schema_current,
    _write_quarantine_marker,
    _write_state_failure_wrapper,
    checkpoint_atomic,
)
from pipeline.loop.types import (
    IterationState,
    ProviderCascade,
    RateLimiterState,
    RunState,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§4.1 start_run happy path + NFC note (NFC is caller's job)",
            "§4.1 resume_run v5 schema-then-phase ordering",
            "§6 F-PIPE-18 resume_phase_mismatch",
            "§6 F-PIPE-22 runstate_schema_downgrade",
        ],
    },
}


# ---------------------------------------------------------------------------
# Public Protocols (E-017 injected-callable pattern)
# ---------------------------------------------------------------------------


@runtime_checkable
class VaultReadCallable(Protocol):
    """Injected vault-read — mirrors Section 2 v7 ``vault_read`` happy path.

    Returns the raw bytes of the file at ``path``. Failure modes (missing
    file, integrity-tag mismatch) surface as VaultError subclasses — Round 3
    lets those propagate untranslated (the caller is already abandoning the
    resume; no state-failure wrapper on read failure because there's no
    RunState yet).
    """

    def __call__(self, *, path: str) -> bytes: ...


@runtime_checkable
class RunIdFactory(Protocol):
    """Injected run-id source — ULID in production, deterministic stub in tests.

    Must return a non-empty string. Downstream path sanitization is §2
    Vault's job (reject ``..`` segments); Round 3 trusts the factory to
    produce ULID-shaped output.
    """

    def __call__(self) -> str: ...


# ---------------------------------------------------------------------------
# Allowed-resume-phase sets — INLINE FROZENSETS (V1 discipline)
# ---------------------------------------------------------------------------


def _allowed_resume_phases_for(mode: str) -> frozenset[str]:
    """§4.1 resume path — allowed re-entry phases per mode.

    Inline-literal frozensets at the call sites below. A module-attribute
    rebind cannot broaden the set because each call builds a fresh
    frozenset literal. The helper centralizes the dispatch for readability
    but the literals themselves are what close the rebind window.
    """
    if mode == "submission":
        return frozenset(
            {
                "pre_gate_pending",
                "pre_gate_passed",
                "inner_loop_iter_1",
                "inner_loop_iter_2",
                "inner_loop_iter_3",
                "post_gate_pending",
                "signoff_pending",
                "signoff_pending_council_split",  # v7 NEW
                "degraded_paused",
            }
        )
    if mode == "eval":
        return frozenset(
            {
                "eval_iter_pending",
                "calibration_assembled",
            }
        )
    # Unknown mode — caller will already have raised at RunState construction;
    # this branch is defence-in-depth.
    return frozenset()


# ---------------------------------------------------------------------------
# RunState deserialization
# ---------------------------------------------------------------------------


def _deserialize_runstate(payload: bytes) -> RunState:
    """Reverse of Round 2's ``_canonicalize_runstate``.

    ``checkpoint_atomic`` persists ``json.dumps(asdict(rs), sort_keys=True)``.
    Deserialization here reconstructs the top-level ``RunState`` plus the
    nested dataclass fields that ``asdict`` recursively flattened
    (``iterations: list[IterationState]``, ``active_cascade:
    ProviderCascade | None``, ``rate_limiter_snapshot: RateLimiterState |
    None``).

    ``TokenBucketProtocol`` buckets inside ``RateLimiterState.buckets``
    can't be round-tripped through JSON; Round 3 rejects a resumed
    ``rate_limiter_snapshot`` carrying non-empty buckets (Round 7 supplies
    the concrete TokenBucket class and will re-hydrate on that round).
    Round 3 reconstructs an empty-buckets snapshot if the serialized form
    is present with an empty ``buckets`` dict.

    Malformed JSON raises ``json.JSONDecodeError``; structurally-invalid
    RunState fields raise at ``RunState.__post_init__`` (F_PIPE_21 / F_PIPE_22
    / ValueError). Both surface to the ``resume_run`` caller.
    """
    data = json.loads(payload.decode("utf-8"))

    iter_list: list[IterationState] = []
    for it in data.get("iterations", []):
        iter_list.append(IterationState(**it))

    cascade_data = data.get("active_cascade")
    active_cascade: ProviderCascade | None
    if cascade_data is None:
        active_cascade = None
    else:
        levels = tuple(tuple(lvl) for lvl in cascade_data["levels"])
        active_cascade = ProviderCascade(
            seat_kind=cascade_data["seat_kind"],
            levels=levels,
            current_level=cascade_data["current_level"],
        )

    rl_data = data.get("rate_limiter_snapshot")
    rate_limiter_snapshot: RateLimiterState | None
    if rl_data is None:
        rate_limiter_snapshot = None
    else:
        rate_limiter_snapshot = RateLimiterState(
            buckets={},
            last_refill_iso=rl_data.get("last_refill_iso", ""),
            lease_holder_id=rl_data.get("lease_holder_id"),
            lease_expires_at_iso=rl_data.get("lease_expires_at_iso"),
        )

    return RunState(
        schema_version=data["schema_version"],
        run_id=data["run_id"],
        mode=data["mode"],
        rfa_hash=data.get("rfa_hash"),
        project_context_hash=data.get("project_context_hash"),
        golden_set_ref=data.get("golden_set_ref"),
        org_slug=data["org_slug"],
        session_id=data["session_id"],
        phase=data["phase"],
        iterations=iter_list,
        active_cascade=active_cascade,
        rate_limiter_snapshot=rate_limiter_snapshot,
        run_iteration_families_so_far={
            k: tuple(v) for k, v in data.get("run_iteration_families_so_far", {}).items()
        },
        started_at_iso=data.get("started_at_iso", ""),
        last_checkpoint_iso=data.get("last_checkpoint_iso", ""),
        pre_gate_result_hash=data.get("pre_gate_result_hash"),
        post_gate_result_hash=data.get("post_gate_result_hash"),
        signed_claim_evidence_map_hash=data.get("signed_claim_evidence_map_hash"),
        three_tab_envelope_hash=data.get("three_tab_envelope_hash"),
        bypass_authorization_ref=data.get("bypass_authorization_ref"),
        bypass_pending_checkpoint_ref=data.get("bypass_pending_checkpoint_ref"),
        quarantine_marker_ref=data.get("quarantine_marker_ref"),
        calibration_report_ref=data.get("calibration_report_ref"),
        calibration_signature_ref=data.get("calibration_signature_ref"),
    )


# ---------------------------------------------------------------------------
# Public API — start_run
# ---------------------------------------------------------------------------


def start_run(
    *,
    mode: Literal["submission", "eval"],
    org_slug: str,
    session_id: str,
    rfa_hash: str | None,
    project_context_hash: str | None,
    golden_set_ref: str | None,
    run_id_factory: RunIdFactory,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
) -> RunState:
    """§4.1 step 1-2 — mint run_id, construct RunState, checkpoint initial state.

    Construction-time invariants (mode-discriminated union, schema version,
    phase validity) are enforced by ``RunState.__post_init__``; any violation
    surfaces to the caller as a clean ``F_PIPE_21`` or ``F_PIPE_22``
    (or ``ValueError`` for non-F-coded shape violations).

    Parameters mirror the blueprint step 1 inputs. NFC normalization of
    ``rfa_hash`` / ``project_context_hash`` is the caller's job — §4.1
    prose ("B-v1-14 closure") applies to the hash-inputs, not to the hash
    strings themselves which this function accepts pre-computed.

    On success, writes the initial checkpoint via ``checkpoint_atomic`` with
    ``intent="state-success"`` + ``expected_current_file_hash=None`` and
    returns the fully-constructed RunState with ``last_checkpoint_iso``
    populated.
    """
    run_id = run_id_factory()
    started_iso = clock.now_iso()
    rs = RunState(
        schema_version=2,
        run_id=run_id,
        mode=mode,
        rfa_hash=rfa_hash,
        project_context_hash=project_context_hash,
        golden_set_ref=golden_set_ref,
        org_slug=org_slug,
        session_id=session_id,
        phase="initialized",
        started_at_iso=started_iso,
    )
    checkpoint_atomic(
        rs,
        intent="state-success",
        expected_current_file_hash=None,
        vault_write=vault_write,
        clock=clock,
        sleep=sleep,
    )
    return rs


# ---------------------------------------------------------------------------
# Public API — resume_run
# ---------------------------------------------------------------------------


def resume_run(
    run_id: str,
    *,
    vault_read: VaultReadCallable,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    sleep: SleepCallable,
) -> RunState:
    """§4.1 resume path — strict order: schema check → phase check → bypass check.

    Step 1: Read ``pipeline/{run_id}/state.json`` via injected ``vault_read``.
    Deserialization errors propagate to the caller.

    Step 2 (v5 MA-07 / MB-05): ``_assert_runstate_schema_current(rs)`` runs
    FIRST. On ``F_PIPE_22``, write a ``state-failure`` checkpoint wrapper
    BEFORE re-raising.

    Step 3: Validate ``rs.phase`` membership in the mode-dispatched allowed
    set. Inline-literal frozensets at the call site — rebind-resistant. On
    mismatch, write a quarantine marker + raise ``F_PIPE_18.resume_phase_mismatch``.

    Step 4: If ``rs.phase == "degraded_paused"``, require
    ``rs.bypass_pending_checkpoint_ref is not None`` (A-v1-16 closure); else
    raise ``F_PIPE_18.bypass_pending_missing`` + quarantine marker.

    Returns the deserialized + validated RunState.
    """
    path = f"pipeline/{run_id}/state.json"
    payload = vault_read(path=path)

    # Step 2: schema check FIRST (v5 MA-07 / MB-05 strict ordering).
    # Peek at raw dict's schema_version BEFORE calling _deserialize_runstate,
    # because RunState.__post_init__ would raise F_PIPE_22 at construction on
    # a downgraded schema and we need the state-failure wrapper to land FIRST.
    raw = json.loads(payload.decode("utf-8"))
    observed_schema = raw.get("schema_version")
    if observed_schema != 2:
        # Build a skeleton RunState (forced schema_version=2) for the wrapper;
        # the wrapper only uses run_id / org_slug / phase as failure labels.
        observed_run_id = str(raw.get("run_id") or run_id)
        observed_mode_raw = raw.get("mode")
        observed_mode: Literal["submission", "eval"] = (
            "eval" if observed_mode_raw == "eval" else "submission"
        )
        skeleton_kwargs: dict[str, object] = {
            "schema_version": 2,
            "run_id": observed_run_id,
            "mode": observed_mode,
            "org_slug": str(raw.get("org_slug") or "unknown"),
            "session_id": str(raw.get("session_id") or "unknown"),
            "phase": "initialized",
            "started_at_iso": "1970-01-01T00:00:00Z",
        }
        if observed_mode == "submission":
            skeleton_kwargs["rfa_hash"] = "unknown"
            skeleton_kwargs["project_context_hash"] = "unknown"
            skeleton_kwargs["golden_set_ref"] = None
        else:
            skeleton_kwargs["rfa_hash"] = None
            skeleton_kwargs["project_context_hash"] = None
            skeleton_kwargs["golden_set_ref"] = "unknown"
        skeleton = RunState(**skeleton_kwargs)  # type: ignore[arg-type]
        schema_err = F_PIPE_22(
            trigger="runstate_schema_downgrade",
            details={
                "observed": observed_schema,
                "expected": 2,
                "run_id": observed_run_id,
            },
        )
        _write_state_failure_wrapper(
            skeleton,
            schema_err,
            vault_write=vault_write,
            clock=clock,
        )
        raise schema_err

    rs = _deserialize_runstate(payload)
    # Defence-in-depth: schema check again via the Round 2 predicate. Redundant
    # with the raw-dict peek above but closes any dict-vs-RunState drift window.
    _assert_runstate_schema_current(rs)

    # Step 3: phase membership via inline-literal frozenset (V1 discipline).
    if rs.mode == "submission":
        allowed = frozenset(
            {
                "pre_gate_pending",
                "pre_gate_passed",
                "inner_loop_iter_1",
                "inner_loop_iter_2",
                "inner_loop_iter_3",
                "post_gate_pending",
                "signoff_pending",
                "signoff_pending_council_split",  # v7 NEW
                "degraded_paused",
            }
        )
    elif rs.mode == "eval":
        allowed = frozenset(
            {
                "eval_iter_pending",
                "calibration_assembled",
            }
        )
    else:  # pragma: no cover — RunState.__post_init__ already rejected
        allowed = frozenset()

    if rs.phase not in allowed:
        marker_ref = _write_quarantine_marker(
            rs,
            reason="resume_phase_mismatch",
            vault_write=vault_write,
            clock=clock,
        )
        rs.quarantine_marker_ref = marker_ref
        raise F_PIPE_18(
            trigger="resume_phase_mismatch",
            details={
                "run_id": rs.run_id,
                "observed_phase": rs.phase,
                "mode": rs.mode,
                "quarantine_marker_ref": marker_ref,
            },
        )

    # Step 4: degraded_paused requires bypass_pending_checkpoint_ref.
    if rs.phase == "degraded_paused" and rs.bypass_pending_checkpoint_ref is None:
        marker_ref = _write_quarantine_marker(
            rs,
            reason="bypass_pending_missing",
            vault_write=vault_write,
            clock=clock,
        )
        rs.quarantine_marker_ref = marker_ref
        raise F_PIPE_18(
            trigger="bypass_pending_missing",
            details={
                "run_id": rs.run_id,
                "phase": rs.phase,
                "quarantine_marker_ref": marker_ref,
            },
        )

    return rs


__all__ = [
    "BLUEPRINT_DEPS",
    "RunIdFactory",
    "VaultReadCallable",
    "_allowed_resume_phases_for",
    "_deserialize_runstate",
    "resume_run",
    "start_run",
]
