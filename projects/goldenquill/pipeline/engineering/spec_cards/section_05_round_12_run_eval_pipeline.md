# Spec card — pipeline.loop.run_eval_pipeline (Round 12: §4.15 eval-mode sibling capstone)

**STATUS:** PRE-STAGED 2026-04-21 at §5 Round 11 run_pipeline SELF-LOCK

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-19
- Principal section: §4.15 `eval_mode entry point and calibration-report assembly` — per-operator local calibration harness
- Supporting sections: §4.1 submission-mode capstone (R11 `run_pipeline` — structural sibling), §4.3 run-lifecycle (R3 `start_run` — eval-mode variant), §4.13 atomic CAS (R2 `checkpoint_atomic`), §4.5/§4.6 revision loop (R5 `run_inner_loop` — reused unchanged per-item), §4.2 POST-gate (R6 `run_post_gate_orchestration` — reused for per-item scoring), §5.6 CalibrationReport schema, §6 F-PIPE-21 `calibration_report_in_submission_bundle` + F-EVAL-CROSS-ORG-READ

**Blueprint hash-at-card:** `34ef007f3ab6d59d` (unchanged since §5 v6 LOCK 2026-04-19)

**Spec-card version:** v1 (pre-staged at Round 11 SELF-LOCK)
**Round:** §5 Round 12 — run_eval_pipeline (eval-mode sibling of R11)
**Depends on:** Rounds 1-11 (all LOCKED). §4 Logician v2.2 (LOCKED; includes F-EVAL-CROSS-ORG-READ PRE-gate predicate). §2 Vault v7.1 (LOCKED; `golden-set-read` / `golden-set-write` intents). Not yet landed: `pipeline.calibration` package (`report.py` + `signing.py` + `golden_set.py`) — R12 may either pre-land those as sub-modules within R12 scope OR depend on a prior R11.5 mini-round. ORIENT-decide.

## Summary

Ship `pipeline/loop/run_eval_pipeline.py` — the §4.15 eval-mode entry point. Structural sibling of R11 `run_pipeline`, but with:
- Input: operator's curated `golden_set` manifest (NOT an RFA).
- Per-item loop: iterates manifest items, runs each through the SAME R5 `run_inner_loop` + R6 POST-gate stack used by submission-mode.
- Output: signed `CalibrationReport` detached-signed with BT13-style Ed25519; written under `vault/{operator_org_slug}/golden_set/calibration_reports/{run_id}.json` with intent `golden-set-write`.
- Shield: NEVER produces a three-tab envelope. Every checkpoint asserts mode-isolation via `_assert_mode_isolation(run_state)`; F_PIPE_21 trigger `eval_run_reached_tab_delivery` is the defence-in-depth shield (R9 `deliver_tab` already raises it on eval-mode entry).

Capstone is orchestration + calibration-assembly, NOT primitives. Reuses R2-R6 unchanged. Adds:
- `pipeline.calibration.golden_set.golden_set_iter(org_slug, manifest_path) -> Iterator[GoldenSetItem]` (thin vault_read wrapper).
- `pipeline.calibration.report.assemble_from_run(run_state, per_item_results) -> CalibrationReport`.
- `pipeline.calibration.signing.sign_report(...) -> bytes` + `verify_calibration_report(...)` (BT13 Ed25519 detached, freshness-window-checked).
- `pipeline.loop.run_eval_pipeline.run_eval_pipeline(...) -> EvalPipelineRunResult`.

## Public API (proposed)

```python
@dataclass(frozen=True, kw_only=True, slots=True)
class EvalPipelineRunResult:
    run_id: str
    final_phase: str                         # "eval_finalized" on success
    items_consumed: int                      # golden-set items processed
    calibration_report_path: str | None      # vault-relative path; None iff aborted pre-assembly
    calibration_signature_path: str | None   # vault-relative path; None iff unsigned
    elapsed_ms: int
    aborted_operator: bool                   # True iff operator refused to sign

@dataclass(frozen=True, kw_only=True, slots=True)
class RunEvalPipelineContext:
    # Mirrors R11 RunPipelineContext, minus scribe/editor/judge specifics that only apply per-item
    vault_read: VaultReadCallable
    vault_write: VaultWriteCallable
    clock: ClockProtocol
    sleep: SleepCallable
    golden_set_iter: GoldenSetIterCallable         # new Protocol (injected for tests)
    pre_gate_input_factory: PreGateInputFactory    # same seam as R11
    pre_gate: Callable[[PreGateInput], PreGateResult]
    post_gate_runner: GateRunnerProtocol           # reused per-item
    post_gate_input_factory: PostGateInputFactory
    launcher: SubprocessLauncher                   # per-item seat invocations
    context_factory: SeatContextFactory
    calibration_signer: CalibrationSignerProtocol  # new Protocol: sign(canonical_bytes) -> signature_bytes
    operator_pubkey_reader: OperatorPubkeyReader   # new Protocol: reads stored pubkey for first-write-wins
    now_iso: Callable[[], str]                     # for signed_at_iso freshness stamping
    interrupt_probe: InterruptProbe | None = None

def run_eval_pipeline(
    *,
    operator_org_slug: str,
    golden_set_manifest_path: str,
    session_id: str,
    seat_charters: tuple[SeatCharter, ...],
    subset: tuple[str, ...] | None = None,
    ctx: RunEvalPipelineContext,
) -> EvalPipelineRunResult: ...
```

## §5 v6 compliance decisions (confirm at ORIENT)

1. **Reuse R5 `run_inner_loop` per-item unchanged.** R5's state-failure checkpointing is submission-mode-agnostic. R12 wraps each golden-set item in a per-item `RunState` snapshot (item_id + manifest_hash recorded) and feeds R5 `run_inner_loop` the item as if it were a mini-RFA.

2. **Path validation: `_resolve_golden_set_path`.** §4.15 step 1 prescribes realpath-hardened path validation. R12 imports or inlines this helper — AST-grep test asserts no string-prefix-only path check at compute sites. Closes MB-02 / MB-03.

3. **Operator pubkey provenance.** §4.15 step 10 v5 hardening: pubkey at `CALIBRATION_KEY_PATH_TMPL.format(operator_org_slug=...)` written once via `state-success` write-if-absent. R12 ships the first-write + compare-on-subsequent-write path. Rotation deferred to v0.2 (no `key-rotation-write` intent in v0.1 scope).

4. **Freshness-window check on verify.** §4.15 step 10 v5 hardening: verify asserts `(now - signed_at_iso) < MAX_CALIBRATION_AGE_DAYS (90 days default)`. F-PIPE-21 subcode `calibration_signature_stale`. R12 ships this check in `verify_calibration_report`.

5. **Mode-isolation at every checkpoint.** `_assert_mode_isolation(run_state)` at every transition. Eval-mode writes confined to intents `{"golden-set-write", "state-success", "state-failure"}`. Any deviation raises F_PIPE_21.

6. **PreGateInputFactory reused.** §4 Logician PRE-gate includes an eval-mode-aware predicate that asserts `operator_org_slug == _read_golden_set_org(golden_set_ref)`. R12 passes the same `PreGateInputFactory` Protocol from R11 (no new seam).

7. **No rate-limiter (R7) / cascade (R8) direct wiring.** Per-item seat invocations go through R5 `run_inner_loop` which internally composes R4 `invoke_seat`. R7/R8 are already composed at that layer. R12 does NOT re-compose them.

8. **CalibrationReport canonical bytes.** Signed payload excludes ONLY the `signature` field; `signed_at_iso` IS included (freshness verification depends on it). R12 ships canonical_bytes helper + AST-grep test for exhaustiveness (§9.9.30 test).

9. **Tab-delivery shield.** R12 never calls R9 `deliver_tab`. R9's existing entry assertion `assert run_state.mode == "submission"` is the shield; R12's mode is `"eval"`, so the assertion would fire if somehow reached (defence-in-depth).

## Test plan (target coverage ≥95%)

**Happy paths** (`tests/loop/test_run_eval_pipeline.py`) — ~20 tests:
- Single-item golden-set → PASS → CalibrationReport assembled → signed → `eval_finalized`.
- Multi-item (3 items) → all score → report has 3 per-item records.
- Subset filter — manifest has 5 items, subset=2 → only 2 processed.
- PRE-gate fail on org mismatch → F_EVAL_CROSS_ORG_READ → `aborted_trusted_fail`.
- Operator refuses to sign → unsigned report written, signature path None, `aborted_operator=True`, recoverable.
- First-write of operator pubkey → `pubkey_first_write_provenance.json` sibling written + compared on second call.
- Freshness-window verification on pre-existing report.
- Per-item checkpoint cadence pin.
- Mode-isolation at every checkpoint (R11 parallel verifies `_assert_mode_isolation` fires on deviation).
- Resume-run semantics — crash after 2 of 3 items → resume picks up at item 3.
- Golden-set iter ordering preserved (manifest order respected absent `subset`).
- Calibration canonical bytes sort-keys deterministic across Python dict insertion-order changes.

**Adversarial** (`tests/loop/test_adv_run_eval_pipeline.py`) — ~25 tests × E-024 2× = ~50 effective:
- Eval-mode reaches `deliver_tab` (constructed-reach path) → F_PIPE_21 `eval_run_reached_tab_delivery`.
- Submission-mode run_state leaks into run_eval_pipeline entry → F_PIPE_21 or assertion.
- Golden-set path with `..` traversal → F_PIPE_21 `golden_set_path_escapes_prefix`.
- Symlink across org boundary → F_PIPE_21 `golden_set_path_traverses_symlink`.
- NFC variant of path component → rejected before realpath.
- Stale signature on verify → F_PIPE_21 `calibration_signature_stale`.
- Pubkey rotation attempt (second write differs) → first-write-wins assertion fails hard.
- CalibrationReport signature field included in canonical bytes (negative — caught by AST-grep test).
- Non-`PipelineFailure` mid-item propagated through state-failure wrapper.
- Rebind resistance — `MAX_CALIBRATION_AGE_DAYS`, `CALIBRATION_SIGNING_ALGORITHM`, `CALIBRATION_REPORT_SCHEMA_VERSION` rebound → no behaviour change.

## Done definition

- [ ] `pipeline/loop/run_eval_pipeline.py` ships `run_eval_pipeline` + `EvalPipelineRunResult` + `RunEvalPipelineContext`.
- [ ] `pipeline/calibration/` package landed: `report.py` (assemble + canonical bytes), `signing.py` (BT13 Ed25519 + freshness), `golden_set.py` (iter wrapper).
- [ ] ≥95% coverage on all new modules.
- [ ] Full suite green (baseline 4651 → target ≥ 4701 after ~50 tests).
- [ ] AST-lint R1-R7 on `pipeline/loop/` + `pipeline/calibration/` clean.
- [ ] `pipeline/loop/__init__.py` re-exports run_eval_pipeline.
- [ ] `pipeline/calibration/__init__.py` re-exports report + signing + golden_set primitives.
- [ ] `lock_history.v1.jsonl` entry (row 103).
- [ ] MEMORY.md index + round-recap memory file.
- [ ] Round 13 spec card pre-stage: §5 LOCKED-as-a-whole capstone (analog of §1 Round J: integration + BT-property + fuzz across R1-R12).

## Lines-of-code target (E-024 2× multiplier)

| File | Target | Target ±25% | Comment |
|------|--------|-------------|---------|
| `pipeline/loop/run_eval_pipeline.py` | 700 | 525–875 | Eval-mode sibling of R11 run_pipeline (929 LOC) — slightly smaller since no R7/R8 direct wiring. |
| `pipeline/calibration/report.py` | 350 | 260–440 | CalibrationReport dataclass + canonical_bytes + parse + per-item record. |
| `pipeline/calibration/signing.py` | 250 | 185–315 | Ed25519 sign + verify + freshness check + first-write-wins pubkey handler. |
| `pipeline/calibration/golden_set.py` | 150 | 110–190 | golden_set_iter + path realpath hardening helper. |
| `tests/loop/test_run_eval_pipeline.py` | 700 | 525–875 | ~20 happy-path tests w/ rich fakes for every Protocol. |
| `tests/loop/test_adv_run_eval_pipeline.py` | 1000 | 750–1250 | ~25 adversarial × 2× multiplier. |
| `tests/calibration/test_report.py` | 400 | 300–500 | Canonical-bytes exhaustiveness + parse round-trip. |
| `tests/calibration/test_signing.py` | 400 | 300–500 | Sign/verify + freshness + first-write-wins pubkey. |
| `tests/calibration/test_golden_set.py` | 350 | 260–440 | Path hardening: symlink cross-org, `..`, NFC, realpath. |

## Self-LOCK eligibility

**Ambiguous — lean toward single-cycle self-LOCK.** R11 composed 10 prior rounds cleanly; R12 composes the SAME underlying R1-R10 plus R11's capstone patterns (RunPipelineContext, PreGateInputFactory, `_make_capturing_vault_write`) with a single structural delta: per-item loop replaces single-RFA path. Two NEW Protocols (`CalibrationSignerProtocol`, `OperatorPubkeyReader`) and one new deterministic artifact (CalibrationReport canonical bytes) are the only new primitives. If ORIENT surfaces ambiguity at the calibration-signing boundary (e.g., how BT13 canonical-bytes enumeration composes with §5.6.4's exclusion table), escalate to Thesis Team under L-005 two-cycle.

## Round 13+ preview

**Round 13** — §5 LOCKED-as-a-whole capstone (analog of §1 Round J). Three sub-rounds:
- J.1 integration: end-to-end submission-mode + eval-mode runs through the full R1-R12 stack with realistic fakes.
- J.2 BT-property: bounded-time properties over phase transitions, mode-isolation invariants, CalibrationReport canonicalisation.
- J.3 fuzz: randomised golden-set manifests, malformed vault reads, operator-interrupt timing.

Unblocks §5 sign-off as a whole; promotes R1-R12 per-module LOCKs to section-LOCK.

## Open questions (resolve at ORIENT)

1. **`pipeline.calibration` package scope.** ORIENT-decide: land the three sub-modules (`report.py`, `signing.py`, `golden_set.py`) as part of Round 12, OR break into Round 11.5 pre-rounds (per-module LOCK each). Recommendation: LAND WITHIN R12 — the three sub-modules are tightly coupled, all driven by §4.15 step 7-10, and splitting creates three separate LOCK rows for <1000 combined LOC. §1 G.1-G.4 precedent supports in-round sub-module landing.

2. **BT13 Ed25519 library binding.** §4.15 step 10 specifies "BT13-style detached Ed25519". Python stdlib has no Ed25519; options: `cryptography` (third-party, preferred, already a dependency via other vault primitives?), `PyNaCl`, or pure-Python `ed25519` (sovereignty concern if third-party drift). Confirm at ORIENT which library is the v0.1 dependency.

3. **Subset ordering determinism.** §4.15 step 6 allows `subset: list[str] | None`. ORIENT-decide: preserve manifest order (filter-by-subset) OR respect subset order (operator-supplied). Recommendation: manifest order (filter), with subset supplying only the inclusion predicate. Deterministic replay relies on manifest order.

4. **Resume semantics — per-item checkpointing.** §4.15 step 6e prescribes "AR-1 save-state-always" after each item. R3 `resume_run` already reads the last checkpoint's phase. For eval-mode resume, R12 needs to read the per-item index out of the checkpointed state. ORIENT-decide: add `current_item_index: int | None` to RunState as a new eval-only field (schema bump), OR stash it in a sidecar `pipeline/{run_id}/eval_progress.json` file. Recommendation: sidecar (avoids RUNSTATE_SCHEMA_VERSION bump from 2 → 3 mid-v0.1).

5. **Operator-sign interrupt.** §4.15 step 9 places an interactive sign-off prompt. In a headless v0.1 pipeline (no UI), this is mediated via a vault-checked operator signal (operator writes `vault/{slug}/golden_set/sign_approved_{run_id}` with intent `golden-set-write`). ORIENT-decide: poll-mode vs event-mode; Recommendation: poll-mode via `interrupt_probe` Protocol (same seam as R5 inner loop).

## Precedent

- R11 single-cycle self-LOCK with zero cross-round issues → confidence that composition-heavy capstones can self-LOCK when the primitive round toolkit is LOCKED.
- §1 Round J capstone self-LOCKed as a whole after per-module LOCKs; R13 (LOCKED-as-a-whole) can follow the same ritual once R12 lands.
- §5 R3-R11 nine consecutive single-cycle self-LOCKs; no committee correction needed in §5 below R1.
