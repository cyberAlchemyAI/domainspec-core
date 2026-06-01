# Blueprint Section 5 — Pipeline (v3 LOCKED 2026-04-18)

**Status:** **LOCKED v3 2026-04-18.** L-005 strict two-audit cycle CLOSED unanimous Thesis Team verdict: Editor (meta/llama-3.3-70b) READY_TO_LOCK; Judge (alibaba/qwen3-32b) PASS 100/100 (140/140 raw, all 14 dimensions 10/10); Red Team (openai_oss/gpt-oss-120b) READY_TO_LOCK with v2 Bucket-A V1 (TAB_ORDERING monkey-patch bypass) explicitly CLOSED via inline-literal runtime check in §4.11 + module-load integrity assert in §8. All 16 v1 Bucket-A items STILL CLOSED; all 12 v2 Bucket-B landings preserved; all 8 §10 OQ closures preserved; parent pointers (Section 2 v7 LOCKED + Section 4 v2 LOCKED) preserved; zero scope creep. v3 hardening backlog (10 Bucket-B + 3 Bucket-C, all out-of-reach under v0.1 trusted-operator A1–A4) captured at `pipeline/validation/blueprint_section_05_2026-04-18/05_synthesis_v3.md` for Phase 2 multi-tenant hardening. Audit trail: `pipeline/validation/blueprint_section_05_2026-04-18/`.

**Parent architecture:** `pipeline/architecture/v0.1/tilth_architecture_locked.md` (v5-r8 LOCKED 2026-04-17). **Parent Section 2:** `pipeline/blueprint/v0.1/section_02_vault_topology.md` (LOCKED v7 2026-04-18). **Parent Section 3:** `pipeline/blueprint/v0.1/section_03_scout.md` (LOCKED v5). **Parent Section 4:** `pipeline/blueprint/v0.1/section_04_logician.md` (LOCKED v2 2026-04-18).

**Pending v4 narrow-edit:** eval_mode (Track 3 — per-operator local calibration harness) queued as a v4 driver narrow-edit. Eval mode adds a second pipeline entry point alongside submission_mode, with its own state machine, calibration-report schema, Cedar-enforced cross-org isolation at eval time, and new vault intents (`golden-set-read`, `golden-set-write`). See `pipeline/validation/blueprint_section_05_2026-04-19/` when authored. Parent-backfill narrow-edits to Section 2 v7.1 and Section 4 v2.1 follow v4 lock.

**Original v3 draft header preserved below for audit-trail:**

v3 DRAFT — verification round, 2026-04-18. v2 verification round closed same day with Editor=READY_TO_LOCK, Judge=PASS 100/100, Red Team=REQUIRES_MINOR_MITIGATIONS (1 new Bucket-A: V1 `TAB_ORDERING` monkey-patch bypass). v3 narrow-edits v2 to close V1 by name while carrying forward all 16 v1 Bucket-A closures, 12 Bucket-B landings, 8 OQ closures, and parent-pointer upgrades unchanged.

## v2 → v3 changelog (single finding, four inline edits)

**V1 closure (TAB_ORDERING monkey-patch bypass).** `typing.Final` is a static type-checker hint only — it does NOT prevent module-attribute rebinding at runtime. The v3 edit makes the three-tab ordering invariant runtime-immutable:

1. §4.11 envelope-construction check compares against an **inline literal tuple**, not the module attribute `TAB_ORDERING`. A compromised rebinding of `pipeline.config.TAB_ORDERING` has no effect on the value checked.
2. §8 `TAB_ORDERING` declaration adds a module-load-time integrity assertion that compares the constant to an inline literal. Any rebinding attempt that happens before `pipeline.config` is fully imported is caught at import time; any rebinding after is bypassed by the inline-literal check at envelope construction.
3. §9.7 AST-grep test extended to also flag any envelope-construction check that uses `TAB_ORDERING` as the rvalue in `!=` / `==` comparisons — the check MUST use the inline literal.
4. §8 rationale column for `TAB_ORDERING` is corrected: "Static `Final` + module-load integrity assert + inline-literal runtime check. A-v1-06 + V1 closure."

No other changes. All v2 mechanisms, failure codes (F-PIPE-01..F-PIPE-20), constants, §10 OQ closures, and parent-pointer upgrades (Section 2 v7, Section 4 v2) carry forward unchanged.

---

**Prior status (carried from v2):** v1 scoping round closed 2026-04-18 with Editor=REQUIRES_MINOR_FIXES, Judge=PASS 98/100, Red Team=REQUIRES_MINOR_MITIGATIONS (16 Bucket-A findings, 20 Bucket-B, 10 Bucket-C). v2 narrow-edited v1 to close each Bucket-A by name, land 12 Bucket-B hardenings, close all §10 OQs, and satisfy the strict LOCK bar.

**Upstream locked context (unchanged from v1):**
- Architecture v5-r8 LOCKED 2026-04-17 → `pipeline/architecture/v0.1/tilth_architecture_locked.md`.
- Section 2 (Vault) v7 LOCKED 2026-04-18 → `pipeline/blueprint/v0.1/section_02_vault_topology.md`.
- Section 3 (Policy/Scout) LOCKED → `pipeline/blueprint/v0.1/section_03_*.md`.
- Section 4 (Logician) v2 LOCKED 2026-04-18 → `pipeline/blueprint/v0.1/section_04_logician.md`.

## v1 → v2 changelog (narrow edits only — every Bucket-A closed by name)

1. **A-v1-01 closure (run-state CAS exhaustion → silent loss of run).** §4.13 adds a `state-quarantine` recovery-marker write that lands BEFORE `F-PIPE-01` is raised; exponential back-off (50ms → 200ms → 800ms) inserted between CAS retries; §8 pins `CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS = (50, 200, 800)`. The operator sees a structured quarantine message rather than a generic error.

2. **A-v1-02 closure (cross-family rigor bypass on fallback — ordering race).** §4.3/§4.4/§4.5 seat-invocation return signatures changed from `hash` to `(hash, landed_family, landed_model_id)` tuple. §4.6 revision loop updates `run_iteration_families_so_far` IMMEDIATELY after each seat returns and BEFORE calling the next seat. §4.9 `select_cascade_level` consults the live tuple, not a post-hoc reconstruction. New §9.3 property test forces Scribe fallback + asserts Editor/Judge never land on Scribe's actual family.

3. **A-v1-03 closure (BYOK key cache leakage across runs).** §3.5 banned-patterns adds: "no module-level caches of decrypted BYOK key material anywhere in `tilth/pipeline/`". §4.3 clarifies that seat subprocesses read their keys via Section 2 v7 §3.5 `seat_launch` session-binding, never from in-process caches. New §9.8 test uses `gc.get_objects()` post-run to assert no residual key-shaped bytes in the parent process.

4. **A-v1-04 closure (sign-off ceremony evasion via forced termination before checkpoint).** §4.1 step 8 reordered: transition to `signoff_pending` + atomic checkpoint BEFORE surfacing the operator prompt. If the checkpoint fails, the prompt is never shown and the run aborts with `F-PIPE-01`. §4.14 reaffirms idempotent prompt behaviour on resume.

5. **A-v1-05 closure (cron misfire double-run on stamp-write failure).** §4.10 adds a local flock file at `~/.tilth/cron_locks/{cron_task_id}.lock` that is acquired BEFORE the vault stamp-write. On vault write transient failure, the flock is retained for `CRON_VAULT_RETRY_WINDOW_SEC = 300` and the write is retried. Only on confirmed dedupe or successful stamp is the flock released. Two cron fires cannot both reach the radar-sweep step.

6. **A-v1-06 closure (three-tab envelope ordering violation).** §8 `TAB_ORDERING` declared `typing.Final[tuple[Literal["live_radar"], Literal["deep_brief"], Literal["council_draft"]]]` with a module-load integrity assert (v3 V1 closure). §4.11 envelope construction asserts `envelope.tab_ordering == ("live_radar", "deep_brief", "council_draft")` as an inline-literal comparison (v3 V1 closure) or raises `F-PIPE-16`. §9.7 adds AST-grep tests that scan the codebase for any `TabEnvelope(` call and verify the `tab_ordering=` argument references `TAB_ORDERING`, and that the envelope-ordering invariant check uses an inline literal tuple as the comparison RHS (not the module attribute).

7. **A-v1-07 closure (mid-loop gate call runtime bypass).** §4.6 loop body adds a runtime invariant: at every seat-call boundary, `assert run_state.phase.startswith("inner_loop_iter_")`. Belt-and-braces with Section 4 v2 §4.2.3 F-PRE-19 and the §3.5 banned-import static check.

8. **A-v1-08 closure (save-state-always violation on new-intent vault writes).** §4.13 adds the general rule: every `vault_write` call inside `tilth/pipeline/` is wrapped in a try/except that writes a `state-failure` checkpoint with the raised error code BEFORE re-raising. This applies whether or not the intent is in the Section 2 v7 allowlist. §10 OQ-1/OQ-2/OQ-3 closed by adopting the interim pattern: new intents (`draft-version-write`, `rate-limiter-snapshot`, `cron-fired-stamp`, `tab-envelope-write`) route through Section 2 v7 `state-success` with structured sub-payloads until Section 2 v8 extends the allowlist. A Section-2 v8 amendment proposal is filed as ARCH-07.

9. **A-v1-09 closure (rate-limiter token-bucket cross-process race).** §4.8 replaces in-process `threading.Lock` with a vault-based CAS lock. Reserve is now: `vault_read(rate_limiter/{endpoint}.json)` → compute new balance → `vault_write(write_mode="overwrite", expected_current_file_hash=...)` via Section 2 v7 §4. CAS mismatch triggers re-read and retry up to `CHECKPOINT_CAS_RETRY_MAX = 3`. §9.3 adds a property test simulating two processes reserving tokens concurrently; asserts total consumed never exceeds capacity.

10. **A-v1-10 closure (iteration-counter soft-restart loophole).** §4.6 adds explicit rule: once `run_state.phase` is `inner_loop_iter_N` with N≥1, any transition back to `inner_loop_iter_M` where M<N is rejected. New failure code `F-PIPE-19.soft_restart_forbidden` added to §6. §9.8 adds a test that synthesizes the soft-restart attempt and asserts the rejection.

11. **A-v1-11 closure (operator-interrupt race leaving half-written iteration).** §4.6 moves the interrupt check to AFTER each iteration's success-checkpoint write. The loop invariant becomes: "if the interrupt is observed, the current iteration's state is already checkpointed." Implementation in a helper `_check_interrupt_post_checkpoint(run_state)` — mandatory at every per-iteration boundary.

12. **A-v1-12 closure (resume-phase validation missing on post-gate-passed entry).** §4.1 `resume_run` formalises the allowed re-entry phase set: `{pre_gate_pending, pre_gate_passed, inner_loop_iter_1, inner_loop_iter_2, inner_loop_iter_3, post_gate_pending, signoff_pending, degraded_paused}`. Any other stored phase raises `F-PIPE-18.resume_phase_mismatch` and aborts the resume with a quarantine marker.

13. **A-v1-13 closure (BYOK key leakage via subprocess environment inheritance).** §4.3/§4.4/§4.5 explicitly state that `seat_launch` (Section 2 v7 §3.5) constructs a subprocess with a MINIMAL env (`PATH`, `HOME`, `TILTH_SESSION_ID`, `TILTH_RUN_ID`, `TILTH_ORG_SLUG` only). Keys are read INSIDE the seat subprocess via `vault_read` using the session binding. §9.8 adds a test that inspects the child's `/proc/{pid}/environ` (Linux) or `ps eww` (macOS) to assert no token-like strings are inherited.

14. **A-v1-14 closure (suggest-mode admission bypass when Cedar result missing).** §4.2 PRE-gate handler adds a post-return check: `PreGateResult.cedar_decision_ref` MUST be non-None before transitioning to `pre_gate_passed`. If None, raise new `F-PIPE-20.cedar_decision_missing`, write `state-failure` checkpoint, abort. Added to §6.

15. **A-v1-15 closure (Judge malformed JSON post-checkpoint iteration recorded as success).** §4.6 reorders per-iteration writes: the success checkpoint occurs AFTER Judge parse succeeds. If Judge parse fails after retry, the iteration is written as `state-failure` with `judge_verdict=None, failure_code=F-PIPE-09`. Never recorded as success.

16. **A-v1-16 closure (bypass-authorization loss on crash during graceful-degradation pause).** §4.12 adds: on entering `degraded_paused`, write a `bypass-pending` checkpoint BEFORE surfacing the operator prompt. On resume, the presence of `bypass-pending` is required to continue; if missing, refuse and require a fresh `start_run`.

**Bucket-B closures landed in v2:**

- **B-v1-02** — folded into A-v1-09.
- **B-v1-03** — §4.10 `cron_task_id` extended to `fund_radar_{YYYY-MM-DD}_{UTC_HH_MM}` to absorb DST double-fire; TTL of 36 h on stamp records.
- **B-v1-04** — §4.8 retry path adds exponential back-off + jitter. §8 pins `RATE_LIMIT_JITTER_RANGE_MS = (0, 300)`.
- **B-v1-05** — folded into A-v1-08.
- **B-v1-06** — §4.13 adds retry loop on transient `vault_read` errors (max 3, back-off 50/200/800 ms).
- **B-v1-08** — §3.2.1 `RunState` gains `schema_version: int = 1` field. §4.1 `resume_run` validates against current schema.
- **B-v1-09** — §4.11 adds post-write round-trip verification of tab envelope's `envelope_sha256`.
- **B-v1-10** — §4.8 CAS lock has lease TTL of 30s with explicit lease-holder identity; expired leases auto-release.
- **B-v1-13** — paired with A-v1-10 test in §9.8.
- **B-v1-14** — §4.1 `start_run` normalizes all text to Unicode NFC before hashing.
- **B-v1-15** — §4.13 adds `CHECKPOINT_TOTAL_TIMEOUT_SEC = 10` ceiling; CAS retries cap below that.
- **B-v1-17** — folded into A-v1-06 (`TAB_ORDERING: Final`).
- **B-v1-20** — §9.6 adds cron-during-signoff test.

Deferred (8 Bucket-B not landed, recorded for v0.1.1):
- B-v1-01 (per-org quotas — multi-client scope).
- B-v1-07 (operator-interrupt audit log — observability).
- B-v1-11 (cascade-level metrics — observability).
- B-v1-12 (router.yaml as runtime source — already stated).
- B-v1-16 (partial-write on large artifacts — Section 2 concern).
- B-v1-18 (clock-skew — ULIDs already suffice).
- B-v1-19 (artifact size limit — Section 2 concern, ARCH-08 filed).

All 10 Bucket-C items addressed via documentation polish in §4.8 / §4.9 / §4.10 and as observability TODOs.

**Section 10 OQs closed:**
- **OQ-1/OQ-2/OQ-3** — closed via interim `state-success` routing pattern + Section 2 v8 amendment proposal ARCH-07.
- **OQ-4** — closed by confirming Section 2 v7 §3.5 `seat_launch` returns a PID (and Section 5 owns the pipe-wrapping layer). Documented at §4.3.
- **OQ-5** — closed: `REVIEW_SEAT_OUTAGE_POLL_INTERVAL_MS = 300000` confirmed as v0.1 default; tuning in v0.1.1.
- **OQ-6** — closed: `config.load_overrides()` from `router.yaml` at boot confirmed; defaults in §8 stand as fallback.
- **OQ-7** — closed: "no soft restart" absolute; operator-issued restart requires a fresh `run_id`. F-PIPE-19 enforces.
- **OQ-8** — closed: LaunchAgent plist label set to `tilth.cron.fund_radar`; re-registration is `launchctl load -w` which replaces idempotently.

---

## §1 Purpose and Scope

### §1.1 Purpose

Section 5 is the Pipeline layer — the orchestration code that **runs** a Tilth council round from RFA ingestion through a signed rails report. Every Tilth output the operator sees passes through Section 5. Section 5 owns nothing the applicant sees directly; it owns the machinery that turns the five-seat council, the three Logician gates, and the vault primitives into a single coherent run.

Concretely, the Pipeline is the layer that:

1. Accepts an RFA + PROJECT_CONTEXT bundle, mints a `run_id`, and initialises `RunState`.
2. Invokes the Logician PRE gate via Section 4 §5.4 `gate_runner.run_pre_gate`.
3. Orchestrates the inner revision loop (Scribe → Editor → Judge) under the three-iteration cap from architecture §J.
4. Invokes the Logician POST gate via Section 4 §5.4 `gate_runner.run_post_gate`.
5. Collects the operator sign-off via Section 4 §5.4 `gate_runner.operator_signoff`.
6. Emits the three-tab delivery envelope (Live Radar / Deep Brief / Council Draft) per architecture §J.
7. Schedules the Monday 8:30 local-time fund-radar cron job per architecture §J.
8. Enforces cross-family rigor at every provider-cascade level (architecture §E / M5).
9. Saves state on every iteration — success or failure — per AR-1 save-state-always.
10. Surfaces graceful degradation when a provider family is exhausted, per architecture §M10 / §M13.

### §1.2 Ownership (the 10 Section-5 surfaces)

Section 5 owns and is the unique author of:

1. **Revision-loop control** (§4.6) — the bounded three-iteration Scribe → Editor → Judge loop, its counter, its convergence detection, its exit paths. v2: soft-restart forbidden (F-PIPE-19); interrupt check is post-checkpoint only.
2. **Council-seat orchestration** (§4.3, §4.4, §4.5) — the code that spawns a seat subprocess, streams its output, enforces its timeout, and parses its structured return. v2: seat invocation returns `(hash, landed_family, landed_model_id)` tuple; subprocess env is minimal; no in-process key caches.
3. **Provider rate limiting** (§4.8) — the BT5-owned `RateLimiterState` and token-bucket algorithm per provider family. v2: CAS-based vault lock with 30s lease TTL; exponential back-off with jitter on 429.
4. **Provider cascade** (§4.9) — the fallback chain that honours cross-family rigor. Judge's cascade MUST NOT land on a Scribe-family model. v2: landed families recorded immediately on seat return; consulted live on next selection.
5. **Cron scheduler** (§4.10) — the Monday 8:30 local-time trigger that runs Scout's fund-radar sweep. v2: local flock + vault stamp two-layer dedupe; DST-safe task-id.
6. **Three-tab delivery** (§4.11) — Live Radar / Deep Brief / Council Draft envelope with a tab-ordering invariant. v2: `TAB_ORDERING: Final`; post-write envelope-hash verification.
7. **Run-state machine** (§4.1, §4.13) — the `RunState` object, its persistence to the vault, and its resume-from-checkpoint semantics. v2: allowed resume phases formalised; schema_version pinned; quarantine-marker on CAS exhaustion.
8. **Graceful degradation** (§4.12) — the Ollama-fallback contract when a review-seat family goes dark; the review-seat-outage escape valve from architecture §M13. v2: `bypass-pending` checkpoint precedes the operator prompt.
9. **Iteration-cap mechanics** (§4.6) — the counter, the overflow rejection, the soft-restart prohibition. v2: F-PIPE-19 enforces.
10. **Run lifecycle** (§4.1) — the end-to-end state transitions from `run_id` minted → report signed → tabs delivered → state vaulted. v2: Unicode NFC normalization at `start_run`; Cedar-decision-ref check before inner loop.

### §1.3 Non-goals (unchanged from v1)

Section 5 does not own, define, or silently re-implement any of: gate logic (Section 4 v2 §5.4), vault reads/writes (Section 2 v7 §4), Cedar policy evaluation (Section 3), seat-internal reasoning (each seat's identity skill), provider keys (Section 2 v7 §5), the Five Operating Laws / Four Autonomy Rules themselves (architecture §L defines; Section 4 enforces; Section 5 calls the gates at the right times).

## §2 Acceptance Criteria

Section 5 v0.1 is complete and shippable iff:

1. **End-to-end council round** — given a valid `(RFA, PROJECT_CONTEXT)` pair, Section 5 produces a signed rails report + three-tab envelope + vaulted state without operator intervention beyond the two sign-off prompts.
2. **Three-iteration cap enforced** — no run exceeds `MAX_REVISION_ITERATIONS = 3`; soft-restart raises `F-PIPE-19`.
3. **Cross-family rigor preserved at cascade** — in every provider-cascade path, Judge's landed family differs from both Scribe's and Editor's landed families. Tested in §9.3.
4. **Cron idempotency** — Monday 8:30 cron trigger dedupes via (flock + vault stamp) on `(run_id_date, cron_task_id)`; double-firing never produces two radar sweeps.
5. **Checkpoint atomicity at the envelope layer** — every iteration boundary writes a single atomic CAS-swap via Section 2 v7 §4 primitives; resume-from-checkpoint restores to the last successful envelope boundary; CAS exhaustion writes a `state-quarantine` marker before aborting.
6. **Save-state-always (AR-1)** — every failure path in §6 writes a failure checkpoint with intent `state-failure` before returning the error. Applies regardless of whether the intent is in the Section 2 v7 allowlist — the wrapper catches vault-write-rejection too.
7. **Graceful-degradation escape valve wired** — review-seat outage triggers `bypass-pending` checkpoint, then operator prompt, then `admin_risk.record_bypass_authorization`. Never silently routes to an in-family reviewer.
8. **Banned-import static check passes** — Section 5 does not import Section 4 inner-loop modules; CI lint covers `seat_runner.py` and `revision_loop.py`.
9. **20 failure codes enumerated** — every `F-PIPE-*` code in §6 has a unique trigger, a severity tier, a save-state contract, and a test in §9. v2 added F-PIPE-19 and F-PIPE-20.
10. **Three-tab delivery ordering invariant** — `tab_ordering` is always the `TAB_ORDERING: Final` constant tuple; AST-grep test rejects any inline ordering tuple.
11. **Subprocess env is minimal** — seat subprocesses receive `PATH`, `HOME`, `TILTH_SESSION_ID`, `TILTH_RUN_ID`, `TILTH_ORG_SLUG` only. BYOK material is read inside the subprocess via `vault_read`.
12. **Rate-limiter race-safe** — concurrent processes reserving tokens share a vault-CAS lock with 30s lease TTL; no over-consumption under simulated concurrency.
13. **Operator sign-off ceremony race-safe** — `signoff_pending` checkpoint lands BEFORE the prompt; force-quit always resumes to the prompt.

## §3 Modules

### §3.1 Owned files

Under `tilth/pipeline/` (unchanged from v1):

| Path | Role |
|------|------|
| `tilth/pipeline/__init__.py` | Package marker + public re-exports |
| `tilth/pipeline/run_lifecycle.py` | §4.1 — `start_run`, `resume_run`, `finalize_run` |
| `tilth/pipeline/revision_loop.py` | §4.6 — bounded inner loop, convergence detection, interrupt post-checkpoint |
| `tilth/pipeline/seat_runner.py` | §4.3/§4.4/§4.5 — subprocess spawn (minimal env), stdout/stderr capture, structured return tuple |
| `tilth/pipeline/rate_limiter.py` | §4.8 — vault-CAS-lock-protected token bucket (BT5) |
| `tilth/pipeline/provider_cascade.py` | §4.9 — fallback chain + live cross-family rigor guard |
| `tilth/pipeline/cron_scheduler.py` | §4.10 — Monday 8:30 fire, flock + vault-stamp two-layer dedupe |
| `tilth/pipeline/three_tab_delivery.py` | §4.11 — tab envelope + ordering invariant + post-write hash verify |
| `tilth/pipeline/graceful_degradation.py` | §4.12 — Ollama-fallback + `bypass-pending` checkpoint + escape valve |
| `tilth/pipeline/state_checkpoint.py` | §4.13 — atomic CAS-swap envelope + quarantine marker + read-retry |
| `tilth/pipeline/signoff_plumbing.py` | §4.14 — operator prompt relay (idempotent on resume) |
| `tilth/pipeline/types.py` | §3.2 — dataclasses with v2 schema_version |
| `tilth/pipeline/errors.py` | §6 — the 20 `F-PIPE-*` exception classes |
| `tilth/pipeline/config.py` | §8 — pinned constants + router.yaml override loader |
| `tilth/pipeline/tests/` | §9 — eight test categories + v2 additions |

### §3.2 Owned data structures

#### §3.2.1 `RunState` (v2 adds `schema_version`)

```python
@dataclass(slots=True)
class RunState:
    schema_version: int                         # v2: pinned to 1; bumped on breaking change
    run_id: str
    rfa_hash: str
    project_context_hash: str
    org_slug: str
    session_id: str
    phase: Literal[
        "initialized",
        "pre_gate_pending",
        "pre_gate_passed",
        "inner_loop_iter_1",
        "inner_loop_iter_2",
        "inner_loop_iter_3",
        "post_gate_pending",
        "post_gate_passed",
        "signoff_pending",
        "report_signed",
        "tabs_delivered",
        "finalized",
        "degraded_paused",
        "aborted_trusted_fail",
        "aborted_operator",
        "quarantined",                          # v2: CAS-exhaustion recovery state
    ]
    iterations: list[IterationState]
    active_cascade: ProviderCascade
    rate_limiter_snapshot: RateLimiterState
    run_iteration_families_so_far: dict[str, tuple[str, str]]  # v2: {seat_kind: (family, model_id)} live
    started_at_iso: str
    last_checkpoint_iso: str
    pre_gate_result_hash: str | None
    post_gate_result_hash: str | None
    signed_claim_evidence_map_hash: str | None
    three_tab_envelope_hash: str | None
    bypass_authorization_ref: str | None
    bypass_pending_checkpoint_ref: str | None   # v2: set on entering degraded_paused
    quarantine_marker_ref: str | None           # v2: set on CAS exhaustion
```

#### §3.2.2 `IterationState` (unchanged from v1)

(Carried from v1 §3.2.2; no v2 edit.)

#### §3.2.3 `SeatCharter` (unchanged)

#### §3.2.4 `ProviderCascade` (unchanged)

#### §3.2.5 `RateLimiterState` (v2 adds lease fields)

```python
@dataclass(slots=True)
class RateLimiterState:
    buckets: dict[str, TokenBucket]
    last_refill_iso: str
    lease_holder_id: str | None                 # v2: which process holds the reserve lock
    lease_expires_at_iso: str | None            # v2: 30s TTL
```

#### §3.2.6 `TabEnvelope` (v2: `tab_ordering` typed `Final`)

```python
@dataclass(frozen=True, slots=True)
class TabEnvelope:
    run_id: str
    tab_ordering: tuple[Literal["live_radar"], Literal["deep_brief"], Literal["council_draft"]]
    live_radar_payload_hash: str
    deep_brief_payload_hash: str
    council_draft_payload_hash: str
    assembled_at_iso: str
    envelope_sha256: str
    # post-write verification: assemble_and_deliver re-reads and confirms envelope_sha256 matches
```

### §3.3 Internal entrypoints (unchanged from v1)

### §3.4 Dependency graph (unchanged from v1)

### §3.5 Banned imports and banned patterns (v2 extends v1)

`tilth/pipeline/revision_loop.py` and `tilth/pipeline/seat_runner.py` MUST NOT import:
- `tilth.logician.gate_runner` / `tilth.logician.admin_risk` / `tilth.logician.*`
- `tilth.seats.scribe` / `tilth.seats.editor` / `tilth.seats.judge` Python modules

**v2 banned patterns (CI lint rule, AST-based):**
- No module-level globals named `KEY`, `SECRET`, `TOKEN`, `API_KEY`, `BEARER`, or matching pattern `*_KEY$` / `*_SECRET$` / `*_TOKEN$` anywhere in `tilth/pipeline/`. (A-v1-03 closure.)
- No module-level `dict` or `cache` variable that is mutated from within a function named `*reserve*`, `*load_key*`, `*get_key*`. (Defence-in-depth against cache-leakage refactors.)
- No `TabEnvelope(` call with an inline tuple or list as the `tab_ordering` argument; must reference `TAB_ORDERING`. (A-v1-06 closure.)

These are enforced by `tilth/pipeline/tests/test_banned_patterns.py` at CI time.

## §4 Mechanisms

### §4.1 Run lifecycle (v2 adds NFC normalization, resume-phase validation, ordered signoff checkpoint)

**Trigger:** as v1.

**Sequence (happy path, v2 edits marked):**

1. `start_run` reads the RFA and PROJECT_CONTEXT; **v2: applies Unicode NFC normalization to text content before canonicalization (B-v1-14 closure)**; computes SHA-256 hashes; mints ULID `run_id`; constructs `RunState(schema_version=1, ...)` in phase `initialized`.
2. `state_checkpoint.checkpoint_atomic(run_state, intent="state-success")` via Section 2 v7 §4 `vault_write(write_mode="write-if-absent")`.
3. Transition to `pre_gate_pending` + checkpoint.
4. Call `gate_runner.run_pre_gate(...)` from Section 4 v2 §5.4. **v2: check that `PreGateResult.cedar_decision_ref` is not None (A-v1-14 closure); if None, raise `F-PIPE-20.cedar_decision_missing`.** On PASS, transition to `pre_gate_passed` + checkpoint.
5. Call `revision_loop.run_inner_loop(run_state)` (§4.6).
6. Transition to `post_gate_pending` + checkpoint.
7. Call `gate_runner.run_post_gate(...)` from Section 4 v2 §5.4.
8. **v2 (A-v1-04 closure): transition to `signoff_pending` + atomic checkpoint BEFORE surfacing the operator prompt. If the checkpoint write fails, raise `F-PIPE-01` immediately; do NOT show the prompt.**
9. Call `gate_runner.operator_signoff(...)`.
10. Transition to `report_signed` + checkpoint.
11. `three_tab_delivery.assemble_and_deliver(run_state)` (§4.11) with post-write envelope-hash verification (B-v1-09 closure). Transition to `tabs_delivered` + checkpoint.
12. Transition to `finalized` + final checkpoint.

**Resume path (v2, A-v1-12 closure):** `resume_run(run_id)` reads the last checkpoint and validates:
- `run_state.schema_version == 1` (B-v1-08 closure); mismatch → `F-PIPE-18`.
- `run_state.phase ∈ {pre_gate_pending, pre_gate_passed, inner_loop_iter_1..3, post_gate_pending, signoff_pending, degraded_paused}`. Any other phase raises `F-PIPE-18.resume_phase_mismatch` and writes a `state-quarantine` marker.
- If `phase == degraded_paused`, the `bypass_pending_checkpoint_ref` MUST be present (A-v1-16 closure); absence raises `F-PIPE-18`.

**Operator-interrupt semantics (v2, A-v1-11 closure):** the interrupt poll runs every `OPERATOR_INTERRUPT_POLL_INTERVAL_MS = 500` ms, but the interrupt HANDLER is only invoked from a `_check_interrupt_post_checkpoint(run_state)` helper that is called at each per-iteration boundary AFTER the iteration's success-checkpoint has been written. An interrupt observed mid-subprocess still lets the subprocess complete and its results checkpoint; only then is the interrupt consumed and the loop exits with `F-PIPE-11`.

### §4.2 PRE-gate invocation (v2 adds Cedar-decision check)

Per v1 §4.2, with v2 addition: after `PreGateResult` is returned PASS, Section 5 verifies `PreGateResult.cedar_decision_ref is not None`. Missing cedar decision raises `F-PIPE-20.cedar_decision_missing`, writes `state-failure`, aborts to `aborted_trusted_fail`.

### §4.3 Scribe invocation (v2 adds tuple return + minimal-env subprocess)

**Contract (v2):** Scribe takes `(rfa_bundle, project_context, iteration_number, editor_critique_prev | null, judge_score_prev | null)` and returns **`(draft_hash: str, landed_family: str, landed_model_id: str)` tuple** — v2 A-v1-02 closure.

**Mechanism (v2 edits):**

1. Load `SeatCharter` for `seat_kind="scribe"`.
2. Rate-limit check: `rate_limiter.reserve(...)` — now vault-CAS-lock-backed (§4.8 v2).
3. **v2: subprocess spawn via `seat_launch` uses a MINIMAL env: `PATH`, `HOME`, `TILTH_SESSION_ID`, `TILTH_RUN_ID`, `TILTH_ORG_SLUG`, `TILTH_SEAT_KIND`. No decrypted keys, no API tokens in env. The subprocess reads its BYOK inside via `vault_read` using the session binding.** (A-v1-13 closure.)
4. Stream stdout; on exit, parse structured return per v1 clean-output discipline.
5. Write the draft to vault: `vault_write(path=..., intent="state-success", payload=structured_draft_sub_payload, ...)` — **v2: until Section 2 v8 adds `draft-version-write` to the allowlist, Section 5 uses `state-success` with a structured sub-payload** (A-v1-08 / OQ-1 closure interim pattern). On `vault_write` failure, the try/except wrapper writes a `state-failure` checkpoint BEFORE re-raising.
6. Return `(draft_hash, charter.primary_provider_family if level_0 else actual_landed_family, actual_landed_model_id)`.

**Timeout:** `SCRIBE_SUBPROCESS_TIMEOUT_MS = 300_000`. Timeout kills subprocess, checkpoint-failure `F-PIPE-07`, cascade advances.

### §4.4 Editor invocation (v2 mirrors §4.3 v2 edits)

Identical to §4.3 with: `seat_kind="editor"`, `EDITOR_SUBPROCESS_TIMEOUT_MS = 180_000`, cross-family constraint validated at charter-load (mismatch raises `F-PIPE-08`), and minimal-env subprocess launch.

### §4.5 Judge invocation (v2 mirrors §4.3 v2 edits; judge parse checkpoint ordering fixed)

Identical to §4.3 with: `seat_kind="judge"`, `JUDGE_SUBPROCESS_TIMEOUT_MS = 180_000`, three-way cross-family constraint, minimal-env subprocess launch, and **v2 (A-v1-15 closure): the iteration's success-checkpoint is written AFTER Judge parse succeeds. If Judge parse fails after retry, the iteration is written as `state-failure` with `judge_verdict=None, failure_code=F-PIPE-09`.**

### §4.6 Revision-loop control (v2 A-v1-02 / A-v1-07 / A-v1-10 / A-v1-11 / A-v1-15 closures)

```python
def run_inner_loop(run_state: RunState) -> IterationState:
    prev_editor_critique = None
    prev_judge_score = None
    for iter_n in (1, 2, 3):
        # A-v1-10: soft-restart guard
        if any(it.iter_number >= iter_n for it in run_state.iterations):
            raise F_PIPE_19_soft_restart_forbidden(run_state, iter_n)

        # A-v1-07: phase assertion at boundary
        assert run_state.phase.startswith("inner_loop_iter_"), \
            "inner loop body invoked with phase not inner_loop_iter_*"

        run_state.phase = f"inner_loop_iter_{iter_n}"
        checkpoint_atomic(run_state, intent="state-success")

        try:
            # A-v1-02: seat invocations return tuples; record landed families IMMEDIATELY
            scribe_hash, scribe_family, scribe_model = invoke_scribe(
                run_state, iter_n, prev_editor_critique, prev_judge_score
            )
            run_state.run_iteration_families_so_far["scribe"] = (scribe_family, scribe_model)

            editor_hash, editor_family, editor_model = invoke_editor(
                run_state, iter_n, scribe_hash
            )
            run_state.run_iteration_families_so_far["editor"] = (editor_family, editor_model)

            judge_result = invoke_judge(run_state, iter_n, scribe_hash, editor_hash)
            # judge_result.landed_family is consulted by cascade before invocation
            run_state.run_iteration_families_so_far["judge"] = (judge_result.landed_family, judge_result.landed_model)

        except JudgeParseError as err:
            # A-v1-15: parse failure → state-failure, never recorded as success
            iteration_state = IterationState(
                iter_number=iter_n,
                judge_verdict=None,
                failure_code="F-PIPE-09",
                ...,
            )
            run_state.iterations.append(iteration_state)
            checkpoint_atomic(run_state, intent="state-failure")
            raise

        except PipelineError as err:
            iteration_state = IterationState(
                iter_number=iter_n,
                failure_code=err.code,
                ...,
            )
            run_state.iterations.append(iteration_state)
            checkpoint_atomic(run_state, intent="state-failure")
            raise

        # A-v1-15: success-checkpoint AFTER parse success
        iteration_state = IterationState(
            iter_number=iter_n,
            scribe_draft_hash=scribe_hash,
            editor_critique_hash=editor_hash,
            judge_score_hash=judge_result.hash,
            judge_total_score=judge_result.total_score,
            judge_verdict=judge_result.verdict,
            ...,
        )
        run_state.iterations.append(iteration_state)
        checkpoint_atomic(run_state, intent="state-success")

        # A-v1-11: interrupt check is POST-checkpoint
        _check_interrupt_post_checkpoint(run_state)

        # Convergence checks (unchanged from v1)
        if judge_result.verdict == "PASS":
            iteration_state.converged_on = "score_threshold"
            return iteration_state
        if iter_n >= 2 and _delta_plateau(run_state.iterations):
            iteration_state.converged_on = "delta_plateau"
            return iteration_state
        prev_editor_critique = editor_hash
        prev_judge_score = judge_result.hash

    last = run_state.iterations[-1]
    last.converged_on = "cap_reached"
    checkpoint_atomic(run_state, intent="state-failure")
    raise F_PIPE_05_iteration_cap_exceeded(run_state)
```

**Convergence rules (unchanged from v1):** score-threshold PASS, delta-plateau at ≥75, cap-reached FAIL with F-PIPE-05.

**v2 additions:**
- **A-v1-02** landed-family is recorded on the seat-return line, before the next seat is invoked. The provider_cascade's `select_cascade_level` reads `run_state.run_iteration_families_so_far` live.
- **A-v1-07** phase-invariant assertion at every boundary (belt-and-braces with Section 4 §4.2.3 F-PRE-19).
- **A-v1-10** soft-restart guard: if any existing `IterationState.iter_number >= iter_n`, raise F-PIPE-19. (Protects against `run_state.iterations` being reset by an adversary.)
- **A-v1-11** interrupt check is POST-checkpoint — `_check_interrupt_post_checkpoint` only fires after a full iteration has successfully checkpointed.
- **A-v1-15** success checkpoint happens after Judge parse succeeds; parse failure writes `state-failure` with `judge_verdict=None`.

### §4.7 POST-gate invocation (unchanged from v1)

### §4.8 Provider rate limiting (v2: vault-CAS lock, lease TTL, back-off jitter)

**v2 reserve algorithm (A-v1-09 closure + B-v1-02 / B-v1-04 / B-v1-10 closures):**

```python
def reserve(endpoint: str, estimated_tokens: int) -> ReservationResult:
    for attempt in range(CHECKPOINT_CAS_RETRY_MAX):
        # Read current bucket state via vault (single source of truth)
        bucket_bytes, current_hash = vault_read(
            path=f"pipeline/rate_limiter/{endpoint}.json",
            session_id="system", slug="rate_limiter",
            return_hash=True,
        )
        state = RateLimiterState.parse(bucket_bytes)

        # Expired lease auto-release (B-v1-10)
        if state.lease_holder_id and state.lease_expires_at_iso and _is_past(state.lease_expires_at_iso):
            state.lease_holder_id = None
            state.lease_expires_at_iso = None

        # Lease acquisition
        if state.lease_holder_id and state.lease_holder_id != PROCESS_ID:
            time.sleep(_backoff_with_jitter(attempt))  # B-v1-04
            continue

        # Refill
        _refill(state)

        if state.buckets[endpoint].current_tokens < estimated_tokens:
            return InsufficientTokens()

        # Reserve
        state.buckets[endpoint].current_tokens -= estimated_tokens
        state.lease_holder_id = PROCESS_ID
        state.lease_expires_at_iso = _iso_now_plus(30)  # 30s lease TTL

        try:
            vault_write(
                path=..., bytes_=state.canonical(),
                intent="state-success",  # interim pattern until rate-limiter-snapshot intent lands (OQ-2)
                session_id="system", slug="rate_limiter",
                write_mode="overwrite",
                expected_current_file_hash=current_hash,
            )
            return Reserved(tokens=estimated_tokens)
        except VaultCasmismatch:
            time.sleep(_backoff_with_jitter(attempt))
            continue  # another process won the CAS, retry

    raise F_PIPE_06_rate_limit_exhausted(endpoint)

def _backoff_with_jitter(attempt: int) -> float:
    base_ms = (50, 200, 800)[min(attempt, 2)]
    jitter_ms = random.randint(*RATE_LIMIT_JITTER_RANGE_MS)
    return (base_ms + jitter_ms) / 1000.0
```

**Token bucket capacities unchanged from v1 §4.8.**

### §4.9 Provider cascade (v2: live landed-family consulted)

**v2 cascade selection (A-v1-02 closure):**

```python
def select_cascade_level(seat_kind, cascade, run_state):
    # v2: consult LIVE recorded landed families, not post-hoc reconstruction
    landed_so_far = run_state.run_iteration_families_so_far
    excluded_families = set()
    if seat_kind == "editor":
        if "scribe" in landed_so_far:
            excluded_families.add(landed_so_far["scribe"][0])  # family
    elif seat_kind == "judge":
        for other_seat in ("scribe", "editor"):
            if other_seat in landed_so_far:
                excluded_families.add(landed_so_far[other_seat][0])

    for level in cascade.levels[cascade.current_level_index:]:
        if level.family in excluded_families:
            continue
        if rate_limiter.can_reserve(level.provider_endpoint):
            return level

    raise F_PIPE_08_cross_family_exhausted(seat_kind, cascade, excluded_families)
```

**Review-seat exhaustion (§M13 escape valve)** handled by `graceful_degradation.request_bypass_authorization` (§4.12) with a `bypass-pending` checkpoint before the prompt (A-v1-16 closure).

### §4.10 Cron scheduler (v2: flock + vault-stamp two-layer dedupe, DST-safe task-id)

**v2 task-id scheme (B-v1-03 closure):** `cron_task_id = f"fund_radar_{YYYY-MM-DD}_{UTC_HH_MM}"` — includes UTC time to distinguish two 08:30 local firings during DST fall-back. Stamp records have TTL of 36h.

**v2 fire-once (A-v1-05 closure):**

```python
def fire_once(cron_task_id: str) -> None:
    lock_path = Path.home() / ".tilth" / "cron_locks" / f"{cron_task_id}.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with flock_exclusive_noblock(lock_path) as acquired:
        if not acquired:
            log(f"cron dedupe (local flock): {cron_task_id} already in-flight")
            return

        for attempt in range(CRON_VAULT_RETRY_ATTEMPTS):
            try:
                vault_write(
                    path=f"cron/fired/{cron_task_id}.stamp",
                    bytes_=iso_now_bytes(),
                    intent="state-success",  # interim pattern for cron-fired-stamp (OQ-2)
                    session_id="system", slug="cron",
                    write_mode="write-if-absent",
                )
                break
            except VaultWriteExists:
                log(f"cron dedupe (vault stamp): {cron_task_id} already fired")
                return
            except VaultTransientError:
                if attempt + 1 == CRON_VAULT_RETRY_ATTEMPTS:
                    # CRON_VAULT_RETRY_WINDOW_SEC total budget exhausted; flock retained, abort
                    raise F_PIPE_15_cron_dedupe_failure(cron_task_id)
                time.sleep(min(30, 2 ** attempt))

        # Only reached on successful vault write. Flock released by context manager after sweep.
        invoke_scout_fund_radar(...)
```

Two-layer dedupe: local flock survives transient vault outages; vault stamp is the durable truth.

### §4.11 Three-tab delivery (v3: inline-literal runtime check + module-load integrity assert)

**v3 constant (A-v1-06 + B-v1-17 + V1 closure):**

```python
# Static-Final belt (mypy/pyright policies reassignment at analysis time):
TAB_ORDERING: Final[tuple[Literal["live_radar"], Literal["deep_brief"], Literal["council_draft"]]] = \
    ("live_radar", "deep_brief", "council_draft")

# v3 V1 closure: module-load integrity assert. If `pipeline.config` is patched or
# rebound during import (e.g., by a compromised dependency or a late import-hook),
# this assertion fails at import time and the module refuses to finish loading.
assert TAB_ORDERING == ("live_radar", "deep_brief", "council_draft"), \
    "TAB_ORDERING has been rebound at module load; refusing to load pipeline.config"
```

**v3 assembly (V1 closure — inline-literal runtime check replaces module-attribute comparison):**

```python
def assemble_and_deliver(run_state: RunState) -> TabEnvelope:
    live_radar_hash = _hash_file(f"vault/fund_radar/{run_state.run_id_date}/live_radar.json")
    deep_brief_hash = _hash_file(f"vault/deep_brief/{run_state.run_id}/brief.md")
    council_draft_hash = _hash_file(f"vault/pipeline/{run_state.run_id}/iter_{final_N}/scribe_draft.md")

    envelope = TabEnvelope(
        run_id=run_state.run_id,
        tab_ordering=TAB_ORDERING,  # MUST reference the Final constant (policed by §9.7 AST-grep)
        live_radar_payload_hash=live_radar_hash,
        deep_brief_payload_hash=deep_brief_hash,
        council_draft_payload_hash=council_draft_hash,
        assembled_at_iso=iso_now(),
        envelope_sha256="",  # placeholder
    )
    canonical_bytes = envelope.canonical_bytes_without_self_hash()
    envelope = replace(envelope, envelope_sha256=sha256(canonical_bytes).hexdigest())

    # v3 V1 closure: compare against an INLINE LITERAL tuple, not the module attribute.
    # A compromised rebinding of `pipeline.config.TAB_ORDERING` cannot affect this check,
    # because the right-hand side is a fresh tuple literal evaluated at each call site.
    if envelope.tab_ordering != ("live_radar", "deep_brief", "council_draft"):
        raise F_PIPE_16_tab_envelope_ordering_violation(envelope.tab_ordering)

    vault_write(
        path=f"pipeline/{run_state.run_id}/tab_envelope.json",
        bytes_=envelope.canonical_bytes(),
        intent="state-success",  # interim for tab-envelope-write (OQ-3)
        ...,
    )

    # B-v1-09: post-write verification
    stored_bytes, _ = vault_read(f"pipeline/{run_state.run_id}/tab_envelope.json", ...)
    stored = TabEnvelope.parse(stored_bytes)
    if stored.envelope_sha256 != envelope.envelope_sha256:
        raise F_PIPE_01_run_state_corrupt(f"tab envelope hash mismatch after write: {envelope.envelope_sha256} != {stored.envelope_sha256}")

    return envelope
```

### §4.12 Graceful degradation (v2: bypass-pending checkpoint before prompt)

**v2 review-seat outage flow (A-v1-16 closure):**

```python
def request_bypass_authorization(run_state, failed_seat, outage_reason):
    run_state.phase = "degraded_paused"
    run_state.bypass_pending_checkpoint_ref = _make_bypass_pending_record(failed_seat, outage_reason)
    checkpoint_atomic(run_state, intent="state-failure")  # writes bypass-pending with failure code F-PIPE-13

    # NOW surface the prompt
    decision = signoff_plumbing.prompt_bypass_authorization(
        run_state, failed_seat, outage_minutes=_outage_minutes(), recovery_eta=_recovery_eta(),
    )

    if decision == "abort":
        raise F_PIPE_13_review_seat_outage_pending_bypass(run_state)
    elif decision == "wait":
        _poll_recovery_loop(...)
    elif decision == "sign":
        signed_auth = operator_sign_bypass(...)
        admin_risk.record_bypass_authorization(...)  # Section 4 v2 §5.4
        run_state.bypass_authorization_ref = signed_auth.ref
        checkpoint_atomic(run_state, intent="state-success")
```

**Ollama hardware-degraded mode** for author seats unchanged from v1.

### §4.13 State persistence (v2: quarantine marker, back-off, read-retry, total-timeout)

**v2 checkpoint atom (A-v1-01 + A-v1-08 + B-v1-06 + B-v1-15 closures):**

```python
def checkpoint_atomic(run_state: RunState, intent: str) -> None:
    canonical = _canonicalize(run_state)
    new_sha = sha256(canonical).hexdigest()
    deadline = time.monotonic() + CHECKPOINT_TOTAL_TIMEOUT_SEC

    try:
        for attempt in range(CHECKPOINT_CAS_RETRY_MAX):
            if time.monotonic() > deadline:
                break
            try:
                current_sha = _read_current_hash_with_retry(run_state)  # B-v1-06: retry on transient
            except VaultReadFailed as rerr:
                _write_state_failure_wrapper(run_state, rerr)
                raise F_PIPE_01_run_state_corrupt(run_state) from rerr

            try:
                vault_write(
                    path=f"pipeline/{run_state.run_id}/state.json",
                    bytes_=canonical,
                    intent=intent,
                    session_id=run_state.session_id, slug=run_state.org_slug,
                    write_mode="overwrite",
                    expected_current_file_hash=current_sha,
                )
                run_state.last_checkpoint_iso = iso_now()
                return
            except VaultCasmismatch:
                backoff_ms = CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS[min(attempt, 2)]
                time.sleep(backoff_ms / 1000.0)
                continue

    except VaultWriteUnauthorizedIntent as uerr:
        # A-v1-08: even if the intent is rejected by Section 2 v7 allowlist,
        # we still write a state-failure checkpoint before re-raising.
        _write_state_failure_wrapper(run_state, uerr)
        raise

    # A-v1-01: CAS exhausted or total timeout — write quarantine marker before raising
    quarantine_ref = _write_quarantine_marker(run_state, reason="cas_exhausted_or_timeout")
    run_state.quarantine_marker_ref = quarantine_ref
    run_state.phase = "quarantined"
    raise F_PIPE_01_run_state_corrupt(run_state)
```

**`_write_state_failure_wrapper(run_state, error)` (A-v1-08):** a minimal try/except that writes `state-failure` checkpoint with `error.code` before the caller re-raises. Applies to every `vault_write` call inside `tilth/pipeline/`.

**`_write_quarantine_marker(run_state, reason)` (A-v1-01):** writes `vault/pipeline/{run_id}/quarantine.json` via `vault_write(intent="state-success", write_mode="overwrite")` — this is the operator's recovery hook: they can see the run's last-known-good phase and choose to continue, abort, or investigate.

### §4.14 Sign-off plumbing (v2: prompt is idempotent; checkpoint-before-prompt enforced)

**v2 (A-v1-04 closure):**

- `signoff_plumbing.prompt_pre_signoff` / `prompt_post_signoff` are invoked ONLY AFTER the `signoff_pending` checkpoint has landed (caller responsibility; enforced by §4.1 ordering + runtime assertion).
- Prompts are idempotent: on resume, calling the same prompt for the same `(run_id, phase, artifact_hash)` produces the same behaviour. If the operator already signed (signed artifact present in vault), the prompt auto-accepts.

**Bypass-authorization prompt** per §4.12 v2.

## §5 Interfaces

### §5.1 Consumes Section 1 (Foundation) (unchanged from v1)

### §5.2 Consumes Section 2 (Vault) v7 (unchanged; interim intent-use pattern documented)

Per v1 §5.2 with v2 clarification: until Section 2 v8 extends the allowlist, Section 5 routes the four new intents (`draft-version-write`, `rate-limiter-snapshot`, `cron-fired-stamp`, `tab-envelope-write`) through `state-success` with structured sub-payloads. Section-2 v8 amendment proposal filed as ARCH-07.

### §5.3 Consumes Section 3 (unchanged)

### §5.4 Consumes Section 4 (Logician) v2 (unchanged from v1)

### §5.5 Section 5 publishes (unchanged from v1)

## §6 Failure codes

Eighteen v1 codes retained; v2 adds two (F-PIPE-19, F-PIPE-20) for a total of 20.

| Code | Name | Trigger | Severity | Save-state | Test |
|------|------|---------|----------|------------|------|
| F-PIPE-01 | run_state_corrupt | CAS exhausted, schema mismatch on resume, quarantine marker write path | CRIT | state-failure + quarantine marker | §9.5.1 |
| F-PIPE-02 | pre_gate_timeout | PRE gate exceeded timeout | HIGH | state-failure | §9.5.2 |
| F-PIPE-03 | post_gate_timeout | POST gate exceeded timeout | HIGH | state-failure | §9.5.3 |
| F-PIPE-04 | judge_convergence_false_positive | Delta-plateau below min-score threshold | MED | state-failure | §9.3.4 |
| F-PIPE-05 | iteration_cap_exceeded | Three iterations, no PASS, no plateau | MED | state-failure | §9.2.5 |
| F-PIPE-06 | rate_limit_exhausted | Cascade exhausts + retries | HIGH | state-failure | §9.5.6 |
| F-PIPE-07 | seat_subprocess_timeout | Seat timeout | HIGH | state-failure | §9.5.7 |
| F-PIPE-08 | cross_family_violation | Cascade can't find cross-family-compatible level | CRIT | state-failure + admin-risk CRIT | §9.3.8 |
| F-PIPE-09 | judge_output_malformed | Judge JSON unparsable after retry | HIGH | state-failure (never success) | §9.5.9 |
| F-PIPE-10 | signoff_cancelled | Operator declined | LOW | state-failure | §9.2.10 |
| F-PIPE-11 | operator_interrupt | Ctrl-C or interrupt flag | LOW | state-failure (post-checkpoint) | §9.5.11 |
| F-PIPE-12 | hardware_degraded_mode_failed | Ollama fallback failed | HIGH | state-failure | §9.5.12 |
| F-PIPE-13 | review_seat_outage_pending_bypass | Review cascade exhausted; escape-valve awaiting | CRIT | state-failure + bypass-pending | §9.5.13 |
| F-PIPE-14 | review_seat_bypass_expired | Bypass not signed in 24h | HIGH | state-failure | §9.5.14 |
| F-PIPE-15 | cron_dedupe_failure | Vault retry window exhausted | HIGH | state-failure | §9.6.15 |
| F-PIPE-16 | tab_envelope_ordering_violation | `envelope.tab_ordering != ("live_radar", "deep_brief", "council_draft")` (inline-literal runtime check, v3 V1 closure) | CRIT | state-failure + admin-risk CRIT | §9.7.16 |
| F-PIPE-17 | bypass_authorization_ledger_write_failed | Admin-risk append failed | CRIT | state-failure | §9.5.17 |
| F-PIPE-18 | resume_phase_mismatch | Resume stored phase not in allowed set OR schema_version mismatch | CRIT | state-failure + quarantine | §9.5.18 |
| **F-PIPE-19** | **soft_restart_forbidden** (v2, A-v1-10) | Transition to `inner_loop_iter_M` when `iter_n ≥ M` already appended | CRIT | state-failure + admin-risk CRIT | §9.8.19 |
| **F-PIPE-20** | **cedar_decision_missing** (v2, A-v1-14) | `PreGateResult.cedar_decision_ref is None` on PRE-gate return | CRIT | state-failure | §9.5.20 |

## §7 Invariants (v2 carries v1; two additional invariants for new codes)

Per v1 §7.1-§7.9, with additions:

- **§7.10 (L-003 / L-005 strengthening via resume guard):** `resume_run` cannot re-enter at `post_gate_passed` (skipping sign-off) or `tabs_delivered` (skipping anything). Enforced by `F-PIPE-18`.
- **§7.11 (soft-restart prohibition):** `run_state.iterations` is append-only within a run; any code path that would reset or truncate it raises `F-PIPE-19`.
- **§7.12 (Cedar-decision presence):** `pre_gate_passed` requires `PreGateResult.cedar_decision_ref` non-None. Enforced by `F-PIPE-20`.

## §8 Constants (v2 adds new + Final-typed)

Carried from v1 §8 with additions:

| Constant (v2 addition) | Value | Rationale |
|------------------------|-------|-----------|
| `TAB_ORDERING: Final[tuple]` | `("live_radar", "deep_brief", "council_draft")` | A-v1-06 + V1: static `Final` (mypy belt) + module-load integrity assert + inline-literal runtime check at envelope construction. A module-attribute rebinding cannot affect the runtime envelope check because the comparison RHS is a fresh tuple literal at every call site (see §4.11). |
| `CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS` | `(50, 200, 800)` | A-v1-01: exponential back-off between CAS retries. |
| `CHECKPOINT_TOTAL_TIMEOUT_SEC` | `10` | B-v1-15: ceiling on checkpoint-write total wall time. |
| `CRON_VAULT_RETRY_WINDOW_SEC` | `300` | A-v1-05: 5-min window during which flock is retained across vault transient failures. |
| `CRON_VAULT_RETRY_ATTEMPTS` | `6` | Paired with back-off 2^0..2^5 seconds capped at 30s. |
| `RATE_LIMIT_JITTER_RANGE_MS` | `(0, 300)` | B-v1-04: jitter avoids thundering-herd. |
| `RATE_LIMIT_LEASE_TTL_SEC` | `30` | B-v1-10: auto-release on lease expiry. |
| `SCHEMA_VERSION_RUNSTATE` | `1` | B-v1-08: incremented on breaking RunState schema change. |
| `CRON_STAMP_TTL_HOURS` | `36` | B-v1-03: stamp records expire after 36h; DST fall-back safe. |
| `BYPASS_PENDING_CHECKPOINT_PATH_TMPL` | `"pipeline/{run_id}/bypass_pending.json"` | A-v1-16 |

All rate-limiter bucket capacities unchanged from v1. All other v1 constants unchanged.

## §9 Tests (v2 adds per-Bucket-A closure tests)

Per v1 §9.1-§9.8 with v2 additions:

### §9.1 Unit tests (added)
- `test_run_state_schema_version_check`: mismatched schema_version on resume raises F-PIPE-18.
- `test_tab_envelope_ordering_runtime_assertion`: TabEnvelope with reordered tuple raises F-PIPE-16.

### §9.2 Integration tests (added)
- `test_signoff_checkpoint_before_prompt`: force-quit between checkpoint and prompt → resume re-shows prompt; force-quit before checkpoint → F-PIPE-01 on resume attempt.

### §9.3 Property tests (added)
- `test_cross_family_rigor_with_scribe_fallback`: Scribe forced to fall back to non-primary family; Editor and Judge MUST never land on Scribe's actual family. A-v1-02 closure.
- `test_rate_limiter_concurrent_reserve_no_overconsumption`: two processes reserving tokens concurrently; total consumed ≤ capacity. A-v1-09 closure.
- `test_judge_parse_failure_never_records_success`: Judge malformed JSON; iteration recorded as state-failure only. A-v1-15 closure.

### §9.5 Failure-injection (added)
- `test_cas_exhaustion_writes_quarantine_marker`: simulate CAS retries exhausted; assert quarantine.json exists with run_id + last-good phase. A-v1-01 closure.
- `test_cedar_decision_missing_raises_f_pipe_20`: PreGateResult with cedar_decision_ref=None → F-PIPE-20.
- `test_bypass_pending_checkpoint_precedes_prompt`: interrupt right after `degraded_paused` transition; resume requires bypass-pending checkpoint. A-v1-16 closure.

### §9.6 Cron tests (added)
- `test_cron_flock_survives_vault_transient_failure`: vault fails transiently; flock retained; second cron fire blocked locally; eventual vault write succeeds. A-v1-05 closure.
- `test_cron_dst_fall_back_distinct_task_ids`: two 08:30 local firings on DST-fall Monday produce distinct task_ids. B-v1-03 closure.
- `test_cron_during_signoff_pending_deduplicated`: cron fires during a paused `signoff_pending` run; new fire no-ops on flock. B-v1-20 closure.

### §9.7 Three-tab tests (added)
- `test_tab_envelope_post_write_hash_verify`: corrupt the stored envelope after write; assemble_and_deliver raises F-PIPE-01. B-v1-09 closure.
- `test_tab_envelope_construction_ast_grep`: AST-grep over `tilth/pipeline/three_tab_delivery.py` asserts that (a) `TabEnvelope(` constructor calls pass `tab_ordering=TAB_ORDERING` (the literal module constant, not an inline tuple); (b) the envelope-ordering invariant check uses an **inline literal tuple** as the comparison RHS, not `TAB_ORDERING` (so runtime monkey-patching of the module attribute cannot bypass the check). Running the AST-grep test as CI lint fails on either violation. A-v1-06 + V1 closure.
- `test_tab_ordering_monkey_patch_resistance`: runtime test — inside a subprocess, rebind `pipeline.config.TAB_ORDERING` to a reordered tuple, then call `assemble_and_deliver`; assert `F-PIPE-16` is raised (the inline-literal check is not fooled). V1 closure.
- `test_tab_ordering_module_load_integrity`: write a monkey-patched `pipeline.config` import hook that rewrites `TAB_ORDERING` during module import; assert the `assert TAB_ORDERING == ("live_radar", "deep_brief", "council_draft")` at module-load time raises `AssertionError` and module import fails. V1 closure.

### §9.8 Law-enforcement tests (added)
- `test_banned_pattern_module_keys`: AST-grep for module-level `KEY`/`SECRET`/`TOKEN` names in `tilth/pipeline/`; CI lint fails on match. A-v1-03 closure.
- `test_subprocess_minimal_env`: spawn seat subprocess; inspect child env; assert only PATH/HOME/TILTH_* names present. A-v1-13 closure.
- `test_soft_restart_raises_f_pipe_19`: synthesize a `run_state.iterations` with an already-appended iter_2, attempt to transition to `inner_loop_iter_1`; assert F-PIPE-19. A-v1-10 closure.
- `test_resume_post_gate_passed_requires_signoff_step`: store `run_state.phase=post_gate_passed`, call resume_run; assert the run proceeds through `signoff_pending` re-entry (never skips). A-v1-12 closure.
- `test_mid_loop_gate_call_assertion`: mock a gate_runner call from inside `revision_loop`; assert the phase-invariant assertion fires. A-v1-07 closure.

## §10 Open Questions (v2 closes all v1 OQs)

- **OQ-1/OQ-2/OQ-3** — **CLOSED**. Interim pattern: route `draft-version-write` / `rate-limiter-snapshot` / `cron-fired-stamp` / `tab-envelope-write` through `state-success` with structured sub-payloads. ARCH-07 amendment proposal filed against Section 2 v8 to add the four intents to the allowlist.
- **OQ-4** — **CLOSED**. Section 2 v7 §3.5 `seat_launch` returns a PID. Section 5 `seat_runner` owns the pipe-wrapping layer (documented in §4.3).
- **OQ-5** — **CLOSED**. `REVIEW_SEAT_OUTAGE_POLL_INTERVAL_MS = 300000` stands as v0.1 default.
- **OQ-6** — **CLOSED**. `config.load_overrides()` at boot; §8 defaults are fallback.
- **OQ-7** — **CLOSED**. No soft restart; F-PIPE-19 enforces. Restart requires fresh `run_id` from operator.
- **OQ-8** — **CLOSED**. LaunchAgent plist label `tilth.cron.fund_radar`; `launchctl load -w` idempotently replaces.

**v2 ARCH items surfaced:**
- **ARCH-07** — Request Section 2 v8 to add `draft-version-write`, `rate-limiter-snapshot`, `cron-fired-stamp`, `tab-envelope-write` to §4.10.4 allowlist.
- **ARCH-08** — Section 2 v8 candidate: enforce max artifact size (e.g., 10 MiB) on vault_write with `F-VAULT-ARTIFACT-TOO-LARGE`. B-v1-19 deferred.

## §11 Law map (v2 additions)

| Rule | Section-5 invariant | §7 subsection | §6 failure code (v2) |
|------|--------------------|-----|-----------------|
| L-001 RFA Source of Truth | Hashes (NFC-normalized v2) through every call | §7.1 | (Section 4 owns F-PRE-*) |
| L-002 No Boundary Drift | §3.5 banned imports + patterns + §5 §-cited interfaces | §7.2 | (lint-time) |
| L-003 Org Isolation | Single-client `org_slug` frozen at boot; resume phase validated | §7.3 / §7.10 | F-PIPE-01, F-PIPE-18 |
| L-004 Apolitical + Admin-Risk | Whitelist-only clean-output | §7.4 | (propagation only) |
| L-005 Strict Two-Audit Cycle | PRE + POST gates both called exactly once, resume enforces | §7.5 / §7.10 | F-PIPE-18 |
| AR-1 Save State Always | Every failure path checkpoints; intent-unauthorized too | §7.6 | (property test + static grep) |
| AR-2 Test Your Own Work | Clean-output parsers + Cedar-decision presence check | §7.7 / §7.12 | F-PIPE-09, F-PIPE-07, F-PIPE-20 |
| AR-3 Be Explicit | `IterationContext` required | §7.8 | (build-time) |
| AR-4 Clean Output | Whitelist stripping pre-vault | §7.9 | F-PIPE-09 |
| **(v2)** Soft-restart prohibition | `iterations` append-only | §7.11 | F-PIPE-19 |
| **(v2)** Cedar-decision presence | PRE-gate result check | §7.12 | F-PIPE-20 |

## §12 Non-ownership (unchanged from v1)

## §13 Closure

v2 is the verification round. The narrow-edit pass landed:

- All 16 Bucket-A closures explicitly named (A-v1-01 through A-v1-16).
- 12 of 20 Bucket-B closures landed (the correctness-safety items); 8 deferred to v0.1.1 with rationale in the changelog.
- All 10 Bucket-C items addressed via doc polish.
- All 8 §10 OQs closed; 2 ARCH items filed (ARCH-07 Section 2 v8 intent extension; ARCH-08 artifact size limit).
- 2 new failure codes (F-PIPE-19, F-PIPE-20) and 2 new invariants (§7.11, §7.12).
- 18 new tests (one per Bucket-A + Bucket-B closure).

**Strict v2 LOCK bar (per prompt_authoring_v1.md):**
- Editor: `READY_TO_LOCK`
- Judge: `total_score ≥ 85` AND all four pipeline-specific subsections present AND `top_3_blockers: []`
- Red Team: `READY_TO_LOCK` with ZERO Bucket-A findings AND every v1 Bucket-A (A-v1-01..A-v1-16) explicitly CLOSED by ID name in the verdict

The v2 verification round audits this draft against that strict bar. If all three seats pass, Section 5 v0.1 LOCKS and is copied to `pipeline/blueprint/v0.1/section_05_pipeline.md`.

— End of Section 5 v2 draft —
