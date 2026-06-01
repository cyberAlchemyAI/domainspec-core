# Spec card — pipeline.loop.run_eval_pipeline (Round 12.B: §4.15 eval-mode capstone)

**STATUS:** PRE-STAGED 2026-04-21 at §5 Round 12.A calibration-package SELF-LOCK

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_05_pipeline.md` v6 LOCKED 2026-04-19
- Principal section: §4.15 `eval_mode entry point and calibration-report assembly`
- Supporting: §4.1 submission-mode capstone (R11 `run_pipeline` — structural sibling), §4.3 (R3), §4.13 (R2), §4.5/§4.6 (R5), §4.2 (R6), §5.6 CalibrationReport schema, §6 F-PIPE-21/F-PIPE-22

**Blueprint hash-at-card:** `34ef007f3ab6d59d` (unchanged since §5 v6 LOCK)

**Spec-card version:** v1 (R12.B split; supersedes the run_eval_pipeline portion of `section_05_round_12_run_eval_pipeline.md`)
**Round:** §5 Round 12.B — `run_eval_pipeline` capstone (R12.A primitives now LOCKED)
**Depends on:** Rounds 1-11 (all LOCKED) + Round 12.A `pipeline.calibration` package (LOCKED 2026-04-21 row 103). §4 Logician v2.2 (LOCKED). §2 Vault v7.1 (LOCKED).

## What R12.A delivered (now inputs)

R12.A shipped the three primitive sub-modules as a standalone surface:

- `pipeline.calibration.golden_set`:
  - `GoldenSetItem` (8-field blueprint-authoritative)
  - `_resolve_golden_set_path` (NFC + realpath + symlink-walk hardening)
  - `golden_set_iter(vault_read, *, operator_org_slug, manifest_path) -> Iterator[GoldenSetItem]`
  - `assert_manifest_org_matches` (F_PIPE_21.golden_set_manifest_org_mismatch gate)
  - Protocols: `GoldenSetVaultRead`, `RealpathCallable`, `IsSymlinkCallable`
- `pipeline.calibration.report`:
  - `CalibrationReport` (15 fields) + `CalibrationReportItem` (7 fields)
  - `canonical_bytes` (§5.6.4 exhaustive; only `signature` + `canonical_sha256` excluded)
  - `assemble_from_run(AssembleInputs) -> CalibrationReport` (mean/stddev/per-dim-union)
  - `compute_canonical_sha256` + `report_to_json` / `report_from_json`
- `pipeline.calibration.signing`:
  - `sign_report(report, *, signer, signed_at_iso) -> CalibrationReport` (intermediate-with-placeholder-sig; updates canonical_sha256 to signed-variant hash)
  - `verify_calibration_report(report, *, pubkey_bytes, now_utc)` (4-stage: unsigned check → 90-day freshness → canonical_sha256 recompute → Ed25519 verify)
  - `reconcile_operator_pubkey(...)` first-write-wins (MA-09)
  - `Ed25519ReferenceSigner` reference implementation
  - Protocols: `CalibrationSignerProtocol`, `PubkeyVaultReader`, `PubkeyVaultWriter`, `ClockNowUTC`

All five F_PIPE_21 sub-triggers for calibration-related path/org/freshness gates are closed at the primitive layer; R12.B composes them.

## Summary (R12.B scope)

Ship `pipeline/loop/run_eval_pipeline.py` — the §4.15 eval-mode entry point. Structural sibling of R11 `run_pipeline`, composing R1-R11 + R12.A primitives.

- Input: operator's curated `golden_set` manifest path (NOT an RFA).
- Per-item loop: iterates `golden_set_iter` items, running each through the SAME R5 `run_inner_loop` + R6 POST-gate stack used by submission-mode.
- Output: signed `CalibrationReport` written under `vault/{operator_org_slug}/golden_set/calibration_reports/{run_id}.json` + sidecar signature at `.../{run_id}.sig` with intent `golden-set-write`.
- Shield: NEVER reaches R9 `deliver_tab`. R9's existing entry-assertion on eval-mode raises F_PIPE_21 `eval_run_reached_tab_delivery` as defence-in-depth.

## Public API (proposed)

```python
@dataclass(frozen=True, kw_only=True, slots=True)
class EvalPipelineRunResult:
    run_id: str
    final_phase: str                         # "eval_finalized" on success
    items_consumed: int
    calibration_report_path: str | None
    calibration_signature_path: str | None
    elapsed_ms: int
    aborted_operator: bool

@dataclass(frozen=True, kw_only=True, slots=True)
class RunEvalPipelineContext:
    vault_read: VaultReadCallable
    vault_write: VaultWriteCallable
    clock: ClockProtocol
    sleep: SleepCallable
    hash_file: HashFileCallable
    # calibration primitives (R12.A) injected as callables to keep R12.B test-only fakes surgical
    golden_set_vault_read: GoldenSetVaultRead     # R12.A Protocol
    realpath: RealpathCallable                    # R12.A Protocol
    is_symlink: IsSymlinkCallable                 # R12.A Protocol
    # submission-mode seams reused from R11
    pre_gate_input_factory: PreGateInputFactory
    pre_gate: Callable[[PreGateInput], PreGateResult]
    post_gate_runner: GateRunnerProtocol
    post_gate_input_factory: PostGateInputFactory
    launcher: SubprocessLauncher
    context_factory: SeatContextFactory
    # R12.A signing surface
    calibration_signer: CalibrationSignerProtocol
    pubkey_vault_read: PubkeyVaultReader
    pubkey_vault_write: PubkeyVaultWriter
    now_utc: ClockNowUTC
    # optional
    interrupt_probe: InterruptProbe | None = None
    judge_parse: JudgeParseFn | None = None

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

## §5 v6 compliance decisions (locked by R12.A; re-affirm at ORIENT)

1. **R5 `run_inner_loop` reused per-item unchanged.** Per-item RunState snapshot with item_id + manifest_hash recorded.
2. **Path validation.** `_resolve_golden_set_path` is LOCKED in R12.A and imported here; AST-grep test asserts no string-prefix-only path check at any R12.B call site.
3. **Operator pubkey provenance.** `reconcile_operator_pubkey` is LOCKED in R12.A; R12.B calls it once at the sign-off step. Rotation still rejected hard in v0.1.
4. **Freshness-window check on verify.** `verify_calibration_report` is LOCKED in R12.A with the 90-day inline-literal RHS; R12.B calls it when resuming a run whose prior checkpoint already holds a signature.
5. **Mode-isolation at every checkpoint.** `_assert_mode_isolation(run_state)` at every transition. Eval-mode writes confined to `{"golden-set-write", "state-success", "state-failure"}`.
6. **PreGateInputFactory reused.** §4 Logician's eval-mode predicate (`operator_org_slug == _read_golden_set_org(golden_set_ref)`) is enforced by the PRE-gate — R12.B injects the same seam from R11.
7. **No R7/R8 direct wiring.** Per-item seat invocations go through R5 which internally composes R4 `invoke_seat`; R7/R8 composed there.
8. **CalibrationReport canonical bytes.** Inherited from R12.A (§5.6.4 exhaustive exclusion table).
9. **Tab-delivery shield.** R9's entry-assertion is the shield; R12.B never calls `deliver_tab`.

## Test plan (target ≥95%)

**Happy paths** (`tests/loop/test_run_eval_pipeline.py`) — ~20 tests:
- Single-item golden-set → PASS → report assembled → signed → `eval_finalized`.
- Multi-item (3 items) → 3-item report.
- Subset filter — manifest has 5 items, subset=2 → 2 processed.
- PRE-gate fail on org mismatch → F_EVAL_CROSS_ORG_READ → `aborted_trusted_fail`.
- Operator refuses to sign → unsigned report written, `aborted_operator=True`, recoverable.
- First-write of operator pubkey → `pubkey_first_write_provenance.json` sibling written + compared on second call.
- Freshness-window verification on pre-existing report.
- Per-item checkpoint cadence pin.
- Mode-isolation at every checkpoint.
- Resume semantics — crash after 2 of 3 items → resume picks up at item 3.
- Golden-set iter ordering preserved (manifest order absent `subset`).

**Adversarial** (`tests/loop/test_adv_run_eval_pipeline.py`) — ~25 × E-024 2× = ~50 effective:
- Eval-mode reaches `deliver_tab` (constructed-reach) → F_PIPE_21 `eval_run_reached_tab_delivery`.
- Submission-mode RunState leaks into entry → F_PIPE_21 or assertion.
- Golden-set path with `..` → F_PIPE_21 `golden_set_path_escapes_prefix` (R12.A closure reached through R12.B).
- Symlink across org boundary → F_PIPE_21 `golden_set_path_traverses_symlink`.
- NFC-variant path component → rejected.
- Stale signature on verify-resume → F_PIPE_21 `calibration_signature_stale`.
- Pubkey rotation attempt → `reconcile_operator_pubkey` ValueError at R12.B's call site.
- Non-`PipelineFailure` mid-item → state-failure wrapper.
- Rebind resistance — `MAX_CALIBRATION_AGE_DAYS`, `CALIBRATION_SIGNING_ALGORITHM`, `CALIBRATION_REPORT_SCHEMA_VERSION`, `RUNSTATE_SCHEMA_VERSION` rebound → no behaviour change (R12.A already pins these at module-load; R12.B re-asserts at composition boundary).

## Done definition

- [ ] `pipeline/loop/run_eval_pipeline.py` ships `run_eval_pipeline` + `EvalPipelineRunResult` + `RunEvalPipelineContext`.
- [ ] `pipeline/loop/__init__.py` re-exports `run_eval_pipeline`.
- [ ] ≥95% coverage on new module.
- [ ] Full suite green (R12.A baseline 4791 → target ≥ 4841 after ~50 tests).
- [ ] AST-lint R1-R7 clean on `pipeline/loop/`.
- [ ] `lock_history.v1.jsonl` entry (row 104).
- [ ] MEMORY.md index + round-recap memory file.
- [ ] Round 13 spec card pre-stage: §5 LOCKED-as-a-whole capstone (analog of §1 Round J).

## LOC target (E-024 2× multiplier)

| File | Target | ±25% | Comment |
|------|--------|------|---------|
| `pipeline/loop/run_eval_pipeline.py` | 700 | 525–875 | Eval-mode sibling of R11 (929 LOC); smaller since R12.A already owns calibration primitives. |
| `tests/loop/test_run_eval_pipeline.py` | 700 | 525–875 | ~20 happy-path with rich fakes. |
| `tests/loop/test_adv_run_eval_pipeline.py` | 1000 | 750–1250 | ~25 adversarial × 2× multiplier. |

Total new LOC estimate R12.B: ~2400 LOC (1 module + 2 test files).

## Self-LOCK eligibility

**Lean toward single-cycle self-LOCK.** R11 composed 10 prior rounds cleanly; R12.A shipped all calibration primitives (134 tests, 99% cov) without cross-module surprises. R12.B is pure composition — per-item loop replaces single-RFA path; no new primitives. Two new Protocol wires (`CalibrationSignerProtocol`, `PubkeyVaultReader`/`PubkeyVaultWriter`) were already invented in R12.A and are now just plumbed. Eleventh consecutive §5 single-cycle self-LOCK target (R3-R12.A = 10; R12.B would be 11).

## Open questions (resolve at ORIENT)

1. **Resume per-item index.** §4.15 step 6e AR-1 save-state-always after each item. ORIENT-decide: add `current_item_index: int | None` to `RunState` (schema bump 2→3) OR sidecar `pipeline/{run_id}/eval_progress.json`. Recommendation unchanged from v1 card: sidecar (avoids mid-v0.1 schema bump).

2. **Operator-sign interrupt.** §4.15 step 9 interactive sign-off in a headless pipeline. Mediate via vault signal (`vault/{slug}/golden_set/sign_approved_{run_id}`) polled through `interrupt_probe`. Recommendation unchanged: poll-mode.

3. **Subset ordering.** Resolved in R12.A (`golden_set_iter` preserves manifest order; subset filters by inclusion).

4. **Calibration report write intent.** §4.15 step 11 writes the report. Confirm `golden-set-write` intent covers both the report and the signature sidecar, OR split into `golden-set-report-write` (new intent). Recommendation: reuse `golden-set-write` (no new intent in v0.1; EVAL_MODE_ALLOWED_INTENTS frozenset already contains it).

5. **Pubkey first-write + sign-off ordering.** Two options: (A) call `reconcile_operator_pubkey` BEFORE `sign_report` (pubkey is authoritative first, then sign covers the current pubkey's signature); (B) sign first, then reconcile. Recommendation: (A) — reconcile first; if rotation detected, abort before signing so we never write a `CalibrationReport` with a mismatched pubkey.

## Precedent

- R12.A single-cycle self-LOCK with 134 tests, 99% cov, zero cross-module surprises → confidence that R12.B pure-composition capstone can self-LOCK.
- R11 composition-heavy capstone self-LOCKed with zero issues composing 10 prior rounds.
- §5 R3-R12.A ten consecutive single-cycle self-LOCKs.
