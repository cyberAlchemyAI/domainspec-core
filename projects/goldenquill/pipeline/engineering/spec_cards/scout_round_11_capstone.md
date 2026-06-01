# Spec card — pipeline.scout Round 11 (capstone-of-capstones — DISCOVER → VERIFY → REVIEW + bounded `_build_fit_rationale`)

**Blueprint anchor:** `pipeline/blueprint/v0.1/section_03_scout.md` §4.11 (capstone) + §9 (run sequence) + §6 (failure taxonomy) + §7.16 (AST invariants) + §8 (numeric pins). Section §3 v5 LOCKED 2026-04-17.
**Blueprint hash-at-card:** `0a82d955f95b0fca` (sha3_512(section_03_scout.md)[:16]) — re-verified at build time, unchanged from Rounds 1–10.
**Spec-card version:** v1
**Round:** Scout R11 of 11 — closes Section 3 implementation; unblocks §3 LOCKED-as-a-whole-section consolidation round.
**Futureproofing scope:** §4.11 capstone composes Rounds 8/9/10 primitives (DISCOVER + VERIFY + REVIEW + `_build_fit_rationale`); applies E-017 injected-Protocol pattern (10th Scout firing — every seam reused, zero new Protocol surface), E-024 1.5× multiplier (composition-heavy capstone), E-025 range-check version pin `rN ≥ 11`, E-026 `__module__` lineage checks (no `sys.modules` identity), E-027 directory-lint contract, E-028 `# pragma: no cover` doctrine for contract-unreachable defensive branches, V1 inline-literal rebind-resistance (§7.16 AST-lint regression).

## Status

**STATUS: READY** (committee dispatch required per handoff — R11 ends Scout's 10-round self-LOCK streak intentionally; composition surface = real review risk).

## Step 0 reconciliations (operator-disposed, irreversible)

1. **Naming:** Blueprint §4.11 sketch (line 1022) defines `run_scout_discover_verify`; §9 step 13 (line 1441) confirms the same entry includes the REVIEW enqueue + `_build_fit_rationale`. Operator-disposed name is `run_scout_discover_verify_review` (handoff line 14) — the longer name reflects the actual scope. Disposition: **expose both names**. Primary public entry is `run_scout_discover_verify_review`; `run_scout_discover_verify` is exported as a verbatim alias (`run_scout_discover_verify = run_scout_discover_verify_review`) so blueprint §9 step 13 / §4.11 sketch consumers (Section 5 Pipeline) work without an in-flight blueprint amendment. No blueprint micro-amend filed; the alias closes the surface gap with zero blueprint-semantic delta. (§8b carve-out style.)

2. **Entity-research composition boundary:** Blueprint §9 line 1447 explicitly states "Pipeline invokes `run_entity_research(session, roster, force_refresh=False)` at project init and on operator-triggered refresh. **Independent of DISCOVER/VERIFY flow.**" Disposition: **R11 does NOT call `run_entity_research`** — the entity-research pass remains R10's surface, driven by Pipeline outside the DISCOVER/VERIFY/REVIEW chain. This keeps R11's composition boundary clean and matches the blueprint verbatim. The handoff prompt's "(R10)" parenthetical that read "REVIEW+entity_research" is interpreted as round-membership ("Round 10 contains both REVIEW and entity_research"), not "compose both into R11."

3. **§0.5 interface index:** No row exists today for `ScoutRunResult` / `run_scout_discover_verify_review`. Per handoff line 23 (the `[NEEDED from §0.5]` carve-out), R11 lands the names at module level via `pipeline/scout/run.py` + re-exports from `pipeline/scout/__init__.py`; an §0.5 index-row delta is filed concurrently in the next §0.5 amendment cycle (mirrors the §0.5 v6 pattern flagged in the Logician v2.2 close-out). The names are stable surface; index is documentation-of-record.

## Public API (goes in `__all__`)

`pipeline/scout/run.py` exports:

- `run_scout_discover_verify_review(*, session, channel_fns, synopsis_fetcher, applicant_profile_provider, vault_writer, checkpoint_writer, degradation_writer, build_fit_rationale=_default_build_fit_rationale, health_signer, executor_factory_discover=None, executor_factory_verify=None, interrupt_probe=None, entropy=None, clock_ns=None, clock_iso=None, timeout_seconds=None) -> ScoutRunResult` — §4.11 / §9 capstone-of-capstones.
- `run_scout_discover_verify` — alias of `run_scout_discover_verify_review` (Step 0 reconciliation #1).
- `ScoutRunResult` frozen kw-only dataclass — §4.11 line 1070 return shape, extended with the REVIEW enqueue list and the run-level fit-rationale fan-out outcomes.
- `_build_fit_rationale(session, candidate, verdict) -> str` — bounded LLM-callable helper. **Default** is a deterministic plain-text formatter (zero LLM, zero network, zero subprocess) that pulls VERIFY + Candidate fields per blueprint §9 line 1458; production deployments override by binding a `BuildFitRationale` Protocol implementation. The default keeps `pipeline.scout.run` import-time-stdlib-only.
- `BuildFitRationale` runtime-checkable Protocol — the `_build_fit_rationale` injection seam.
- `RationaleBudgetExceeded` exception — fires when a custom `BuildFitRationale` returns text whose UTF-8 byte length exceeds `MAX_FIT_RATIONALE_BYTES`. Blueprint §4.11 line 1458 / §9 line 1458 — "bounded to ≤ 800 tokens"; we approximate this on the byte side at `MAX_FIT_RATIONALE_BYTES = 4096` (≈ 800 tokens × 5 bytes/token mid-range).
- `RationaleBuildFailed` exception — fires when a custom `BuildFitRationale` raises any other exception inside the per-VERIFIED_FIT loop. The capstone records the failure as a degradation event and continues — REVIEW enqueue is best-effort per VERIFIED_FIT verdict, never aborting the whole run.
- `MAX_FIT_RATIONALE_BYTES: Final[int] = 4096` — UTF-8 byte budget for `_build_fit_rationale` output.
- `F_SCOUT_RUN_01..05: Final[str]` — capstone-introduced failure codes (rationale budget, rationale build failure, missing channel keys, interrupt mid-pipeline, signer carry-through).
- `RunDegradationEvent` frozen kw-only dataclass — capstone-level degradation events emitted at the run.py layer (rationale-build / interrupt boundary).
- `ScoutRunInterrupted(RuntimeError)` — propagated when a stage interrupt fires.
- `__version__: Final[str] = "0.1.0-scout-r11"` — bumps the package version per `pipeline/scout/__init__.py` re-export pattern.
- Re-exports: every existing R8/R9/R10 public name preserved; `ScoutRunResult`, `run_scout_discover_verify_review`, `run_scout_discover_verify`, `BuildFitRationale`, `RationaleBudgetExceeded`, `RationaleBuildFailed`, `MAX_FIT_RATIONALE_BYTES`, the five `F_SCOUT_RUN_*` codes, `RunDegradationEvent`, `ScoutRunInterrupted` added. **`_build_fit_rationale` is intentionally NOT re-exported** — blueprint §4.11 line 1067 names the helper with an underscore prefix (implementation symbol, not public API). The R1 `TestPackageSurface::test_no_private_name_exported` invariant requires that no underscore-prefixed name (other than `__version__`) appears in `pipeline.scout.__all__`. Custom rationale builders bind via the `build_fit_rationale` kwarg + the `BuildFitRationale` Protocol; deployments that need to import the default helper directly do so via `from pipeline.scout.run import _build_fit_rationale`.

## Data structures

```python
@dataclass(frozen=True, kw_only=True)
class ScoutRunResult:
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
    run_degradation_events: tuple["RunDegradationEvent", ...]


@dataclass(frozen=True, kw_only=True)
class RunDegradationEvent:
    source: str
    code: str
    reason_tag: Optional[str]
    severity: str
    candidate_id: Optional[str] = None


class BuildFitRationale(Protocol):
    def __call__(
        self,
        *,
        session: SessionLike,
        candidate: Candidate,
        verdict: VerificationVerdict,
    ) -> str: ...
```

`SessionLike` is the merged duck-type shape (`session_id: str`, `slug: str`, `operator_id: str`) — all three fields required because `enqueue_for_review` dispatches under R10's `SessionLike` which requires `operator_id`.

## Algorithms

Per blueprint §4.11 sketch (lines 1017–1074) + §9 step list (lines 1429–1444):

1. **Validate channel-dispatch map completeness.** All six keys A/B/C/D/E/F must be present; missing → `KeyError` (`F_SCOUT_RUN_03`). Mirror Round 8's pre-fan-out validation.
2. **DISCOVER stage.** Delegate to `pipeline.scout.discover.run_scout_discover` with the injected `channel_fns`, `health_signer`, `executor_factory_discover`, `interrupt_probe`, `entropy`, `clock_ns`, `checkpoint_writer`, `degradation_writer`. The capstone does **not** re-run any Round 8 logic — it consumes the returned `ScoutDiscoverResult`.
3. **VERIFY stage.** Delegate to `pipeline.scout.verify_stage.verify_all` with the `discover_result`, `synopsis_fetcher`, `applicant_profile_provider`, `executor_factory_verify`, `interrupt_probe`, `clock_iso`, `checkpoint_writer`, `degradation_writer`, `timeout_seconds`. Returns `ScoutVerifyResult`. Per-stage checkpoints already land inside `verify_all`; the capstone adds its own `run_review_start` / `run_review_complete` boundary.
4. **Run-level checkpoint** — `checkpoint_writer.write(stage="run_review_start", ...)` opens the §4.11 line 1065 per-VERIFIED_FIT loop. Autonomy Rule 1 — landmark on every run, not only on the rationale-fan-out path.
5. **Per-VERIFIED_FIT fan-out.** Iterate `discover_result.candidates` in their stable Round-8-truncation order; for each candidate whose verdict is `VERIFIED_FIT`:
   - Call `build_fit_rationale(session=, candidate=, verdict=)`. Bound the output: if it exceeds `MAX_FIT_RATIONALE_BYTES` UTF-8 bytes, raise `RationaleBudgetExceeded(F_SCOUT_RUN_01)` and emit `RunDegradationEvent` (severity HIGH, reason_tag `rationale_oversize`); SKIP this candidate's enqueue.
   - On any other exception inside the rationale call, emit `RunDegradationEvent` (severity HIGH, reason_tag `rationale_build_failed: {exc_type}: {exc_msg}`); SKIP this candidate's enqueue. Wrap as `RationaleBuildFailed(F_SCOUT_RUN_02)` only if the operator wants the chain to abort — default is `continue`.
   - On success, store `fit_rationales[candidate_id] = rationale_text`.
   - Call `enqueue_for_review(session=, candidate=, verdict=, fit_rationale=, vault_writer=, checkpoint_writer=, clock=clock_iso)`. Any `ReviewEnqueueRejected` propagates unwrapped (those are programmer / deployment errors — F-SCOUT-R-01 should be unreachable here because the loop guard already filters non-VERIFIED_FIT, but defence-in-depth surfaces a deployment bug fast). Any other exception from the injected `vault_writer` propagates unwrapped (transport failures abort the run; the upstream cap on enqueue retries belongs to Section 2 and Pipeline, not Scout).
   - The candidate's `ReviewQueueItem` is appended to the result tuple in stable order.
6. **Run-level checkpoint** — `checkpoint_writer.write(stage="run_review_complete", ...)` lands on every exit path (success, interrupt, rationale-budget). Autonomy Rule 1.
7. **Interrupt handling.** Stage-internal interrupts (raised by `run_scout_discover` or `verify_all`) propagate unwrapped — they already wrote their own `*_interrupted` checkpoint. The capstone wraps the per-VERIFIED_FIT loop in its own probe: between candidates, if `interrupt_probe()` returns True, write `run_review_interrupted` checkpoint with the `completed_candidate_ids` so far + the pending candidate, then raise `ScoutRunInterrupted`. Reason code: `F_SCOUT_RUN_04`.
8. **Result assembly.** Bundle the discover + verify + review outputs into a `ScoutRunResult`. `signed_health` is carried through unchanged (Scout does not re-sign at the run-level boundary — Section 1's HMAC is cryptographically anchored at the §4.10 step). `run_degradation_events` carries only events introduced at the run.py layer (rationale fan-out + interrupt); per-stage events stay on their per-stage results.
9. **Return.**

**No re-authoring discipline.** R11 calls each Round 8/9/10 entry exactly once with their LOCKed signatures. No primitive logic is reimplemented at run.py — the spec card line 19 carve-out forbids it explicitly. Coverage of the Round 8/9/10 internals lives in their own test suites; R11 tests assert composition-level invariants only.

**LLM-import boundary.** The default `_build_fit_rationale` is deterministic plaintext (no LLM, no network, no subprocess). Production deployments override via the `build_fit_rationale` kwarg to bind a real LLM provider. The AST-lint regression in §7.16 (which is enforced via the existing `pipeline.linting.ast_lint.lint_tree` over the `pipeline` directory) confirms `pipeline.scout.run` does NOT import `anthropic`, `openai`, `google.generativeai`, or any LLM provider module — the LLM imports are confined to the *deployment-supplied* `BuildFitRationale` implementation, which lives outside the Scout package. This keeps `pipeline.scout.run` LLM-import-free at every layer.

## Failure codes

All R11 codes are namespace `F-SCOUT-RUN-*` (capstone-of-capstones). They do not collide with the eight existing Scout namespaces (`A`, `B`, `C`, `CHD`, `E`, `F`/`BT12`, `V`, `R`, `D`, `H`, `CAPSTONE`).

| Code | Trigger | Severity | Recovery |
|------|---------|----------|----------|
| `F-SCOUT-RUN-01` | `_build_fit_rationale` returned text with UTF-8 byte length > `MAX_FIT_RATIONALE_BYTES` (`= 4096`) | HIGH | Skip this candidate's enqueue; emit `RunDegradationEvent`; continue to next VERIFIED_FIT candidate. |
| `F-SCOUT-RUN-02` | Custom `BuildFitRationale` raised any exception other than `RationaleBudgetExceeded` | HIGH | Skip this candidate's enqueue; emit `RunDegradationEvent` carrying `{exc_type}: {exc}`; continue. |
| `F-SCOUT-RUN-03` | `channel_fns` dispatch map missing one or more of the six required channel keys | HIGH | Raise `KeyError` before any work; the capstone refuses to run with an incomplete dispatch map. |
| `F-SCOUT-RUN-04` | `interrupt_probe()` fired between two VERIFIED_FIT candidates inside the run-level fan-out | HIGH | Write `run_review_interrupted` checkpoint with completed + pending ids; raise `ScoutRunInterrupted`. |
| `F-SCOUT-RUN-05` | DISCOVER signer raised (per Round 8 F-SCOUT-CAPSTONE-06 already wrote its own degradation event); the capstone re-raises unchanged but additionally writes a `run_review_complete` checkpoint with `outcome=signer_failed` | HIGH | Reraise; the run cannot proceed without a signed health tuple. |

## Test surface

All tests live at `tests/scout/test_round_11_capstone.py`. Floor-≥-30 + adversarial-≥-5 per handoff. Composition-heavy capstone — the per-stage primitives carry their own suites; this suite targets composition invariants only.

### Composition / sequencing tests

1. `TestRunHappyPathEndToEnd` — 6-channel fixture + 3-candidate VERIFY pool + 1 VERIFIED_FIT → DISCOVER → VERIFY → REVIEW chain produces a `ScoutRunResult` with the expected verdict count + 1 `ReviewQueueItem`.
2. `TestRunPropagatesDiscoverResultUnchanged` — Capstone does NOT mutate the candidates / per_channel_states / signed_health / run_id / run_tiebreak_seed / run_wall_ns coming back from `run_scout_discover` (assert reference / value equality where appropriate).
3. `TestRunPropagatesVerifyResultUnchanged` — `verify_stage_state`, `verify_overflow`, `verify_degradation_events` carried through verbatim.
4. `TestRunStageOrderDiscoverThenVerifyThenReview` — Instrumented Round 8/9/10 stubs record call order; assert `discover` → `verify_all` → per-VERIFIED_FIT enqueue, never reordered.
5. `TestRunNoEnqueueForVerifiedNotFit` — VERIFIED_NOT_FIT verdict is filtered before the rationale call; `enqueue_for_review` is not called for that candidate; no `ReviewQueueItem` emitted.
6. `TestRunNoEnqueueForUnverified` — same for UNVERIFIED.
7. `TestRunNoEnqueueForVerificationFailed` — same for VERIFICATION_FAILED.
8. `TestRunRationaleBuiltOncePerVerifiedFit` — Two VERIFIED_FIT candidates → `build_fit_rationale` called exactly twice, each with the right `(candidate, verdict)` pair.
9. `TestRunDefaultBuildFitRationaleIsDeterministic` — Default `_build_fit_rationale` returns identical bytes for identical inputs across two calls; output contains the candidate_id, the verdict reason code, and the candidate funder kind.
10. `TestRunDefaultBuildFitRationaleIsImportTimeDeterministic` — Default `_build_fit_rationale` returns ≤ `MAX_FIT_RATIONALE_BYTES` for any `(Candidate, VerificationVerdict)` pair regardless of the input lengths (the formatter clips long synopsis fields).
11. `TestRunRationaleBudgetExceededIsLogged` — Custom `BuildFitRationale` returns a string of `MAX_FIT_RATIONALE_BYTES + 1` UTF-8 bytes → run completes successfully, candidate is NOT enqueued, `RunDegradationEvent` with code `F_SCOUT_RUN_01` and reason_tag `rationale_oversize` is emitted, `fit_rationales` dict does not contain that candidate's id.
12. `TestRunRationaleExactlyAtBudgetIsAccepted` — Custom builder returns exactly `MAX_FIT_RATIONALE_BYTES` UTF-8 bytes → enqueue happens; no degradation event.
13. `TestRunRationaleBuildFailedIsLogged` — Custom builder raises ValueError → run completes successfully, candidate is NOT enqueued, `RunDegradationEvent` with code `F_SCOUT_RUN_02` and reason_tag containing `ValueError` and the error message is emitted.
14. `TestRunRationaleKeyboardInterruptPropagates` — Custom builder raises `KeyboardInterrupt` → propagates; no `run_review_complete` checkpoint with success outcome. (Mirrors R10's `KeyboardInterrupt` path: bare-rethrow, no failure-complete-checkpoint per Round 9/10 pattern.)
15. `TestRunRationaleSystemExitPropagates` — same for `SystemExit`.
16. `TestRunChannelDispatchMapMissingKeyRaises` — Dispatch map missing channel C → `KeyError` raised before DISCOVER stage submits any work; checkpoint writer never called.
17. `TestRunCheckpointDisciplineSuccess` — `run_review_start` + `run_review_complete` (outcome=success) checkpoints emitted in order; carry `run_id` + completion stats.
18. `TestRunCheckpointDisciplineFailureAtVerify` — `verify_all` raises a non-Interrupt exception → run-level `run_review_complete` checkpoint with outcome=failure lands; per-stage checkpoints from `verify_all` already wrote.
19. `TestRunInterruptBetweenVerifiedFitCandidates` — `interrupt_probe()` flips True after the first VERIFIED_FIT enqueue → `ScoutRunInterrupted` raised; `run_review_interrupted` checkpoint payload carries `completed_candidate_ids=[cid1]`, `pending_candidate_id=cid2`; F_SCOUT_RUN_04 reason tag in the run_degradation_events tuple.
20. `TestRunInterruptDoesNotEnqueueAfterPending` — Same as #19, assert `enqueue_for_review` was called exactly once (the first candidate); the second-candidate path was short-circuited before rationale fan-out.
21. `TestRunSignerFailurePropagates` — `make_default_health_signer` raised → DISCOVER's F-SCOUT-CAPSTONE-06 wrote its own degradation event in `run_scout_discover`; capstone re-raises unchanged; assert no VERIFY / REVIEW work attempted.
22. `TestRunVersionPin` — `pipeline.scout.run.__version__` parses to a tuple where the rN-suffix integer ≥ 11 (E-025 range-check, future-proofs against r12+).
23. `TestRunModuleLineage` — `run_scout_discover_verify_review.__module__ == "pipeline.scout.run"` (E-026 `__module__` lineage; survives `sys.modules` eviction).
24. `TestRunAliasIdentity` — `run_scout_discover_verify is run_scout_discover_verify_review` — verbatim alias, no shim.
25. `TestRunResultIsFrozen` — `ScoutRunResult` cannot be mutated post-construction (FrozenInstanceError on field assignment).
26. `TestRunResultPreservesCandidateOrder` — Two VERIFIED_FIT candidates with stable Round-8-truncation order → `review_queue_items` tuple maintains that order.
27. `TestPublicSurfaceReachableViaScoutInit` — Every R11 public name is importable via `pipeline.scout` (re-export).
28. `TestPublicSurfaceCount` — `pipeline.scout.run.__all__` matches the documented surface; no rogue export.
29. `TestRunResultRunDegradationEventsAreFrozen` — `RunDegradationEvent` instances are frozen kw_only dataclasses; field assignment raises FrozenInstanceError.
30. `TestRunFitRationalesMappingExcludesNonFit` — Only VERIFIED_FIT candidate ids appear as keys in `fit_rationales`.

### AST regression invariants (§7.16)

31. `TestASTNoLLMImportsInRun` — `ast.parse('pipeline/scout/run.py')` finds no import of `anthropic`, `openai`, `google.generativeai`, or any other deployment-LLM provider module. The module imports only stdlib + intra-package modules.
32. `TestASTLintCleanRun` — Copy `pipeline/scout/run.py` into `tmp_path / "pipeline" / "scout" / "run.py"` with empty `__init__.py` and run `lint_tree(tmp_path, DEFAULT_RULES)` — zero violations across R1/R2/R3/R4/R5/R6/R7. Mirrors Round 10's E-027 directory-contract pattern.
33. `TestASTNoSetattrOperatorDecisionInRun` — `ast.parse` confirms `pipeline/scout/run.py` contains zero attribute-stores whose attribute string is `"operator_decision"` and zero `setattr(..., "operator_decision", ...)` call sites. (Defence-in-depth — only `record_operator_decision` may write that field, per R10 §7.16.)
34. `TestASTNoEvalExecCompileInRun` — `ast.parse` confirms zero calls to `eval`, `exec`, or `compile`.
35. `TestASTNoOpenInRun` — `ast.parse` confirms zero `open(` / `Path.read_text` / `Path.write_text` / `os.open` call sites in `pipeline/scout/run.py`. All persistence flows through injected `vault_writer` / `checkpoint_writer` / `degradation_writer` / `health_signer` Protocols.

### Adversarial tests (≥ 5 per handoff)

36. `TestAdv_RationaleBudgetByteCountOverNotChar` — Custom builder returns a string whose **character count** is below `MAX_FIT_RATIONALE_BYTES` but whose UTF-8 byte count exceeds it (e.g., 1500 emoji, each 4 bytes UTF-8 → 6000 bytes); assert `F_SCOUT_RUN_01` fires.
37. `TestAdv_InterruptDuringStageBoundary` — `interrupt_probe()` flips True between DISCOVER complete and VERIFY start (i.e., inside `verify_all`'s pre-pool check) → `ScoutVerifyInterrupted` propagates; capstone re-raises unchanged with no run-level state change.
38. `TestAdv_SimultaneousRationaleAndEnqueueFailure` — Custom builder raises ValueError on candidate A; `vault_writer.write` raises RuntimeError on candidate B's enqueue → run aborts on the second failure (B's enqueue raises), candidate A's `RunDegradationEvent` is recorded, candidate A is NOT enqueued, the FAILURE checkpoint lands at `run_review_complete`.
39. `TestAdv_RationaleEmittedWithStableSeedTextSurvivesRunReplay` — Two consecutive runs with identical session + identical Round-8 seed produce identical default-`_build_fit_rationale` outputs for identical `(Candidate, VerificationVerdict)` pairs (deterministic rationale baseline; required for the run-replay invariant).
40. `TestAdv_AllVerifiedFitCandidatesGetRationaleFanOutEvenIfOneFails` — Three VERIFIED_FIT candidates; the middle one's rationale build raises → first + third are enqueued; only middle hits the degradation log; the run completes successfully.
41. `TestAdv_ChannelDispatchMapWithExtraKeysIsAccepted` — Dispatch map has all six required keys plus a phantom `"X"` key → run completes; the phantom key is silently ignored (the validation refuses missing keys, not extras).
42. `TestAdv_RationaleReturningNonStrIsTreatedAsBuildFailed` — Custom builder returns a `bytes` object instead of `str` → caught at the byte-count check → recorded as `F_SCOUT_RUN_02` (NOT 01 — bytes don't have `.encode()` in the expected sense; the type guard catches this before the budget check).

### Shared-Protocol lineage checks (E-026 formal)

43. `TestSharedProtocolReuse_SessionLike_Origin` — `SessionLike.__module__ == "pipeline.scout.review_stage"` (the merged shape with `operator_id` lives on review_stage; verify_stage's narrower SessionLike is a subset). The capstone duck-types from review_stage's surface to keep enqueue dispatch type-safe.
44. `TestSharedProtocolReuse_Candidate_Origin` — `Candidate.__module__ == "pipeline.scout._types"`.
45. `TestSharedProtocolReuse_VerificationVerdict_Origin` — same.
46. `TestSharedProtocolReuse_ReviewQueueItem_Origin` — same.

## Test-count and LOC sizing (E-024 formal — 1.5× multiplier)

E-024 trident applies (E-017 reused 10× + V1 inline-literal rebind-resistance + E-023 deferred-scope `test_adv_*` docs). Naive floor = 30 (handoff). Expected ceiling = 1.5 × 30 = **~45 tests**. Spec-card LOC target: ~600 LOC for `pipeline/scout/run.py` (composition-heavy, no re-authored primitives) at ±25% (450–750). Test file expected ~1500 LOC at ±25% based on Round 8/9/10 ratios.

## Futureproofing commitments

- **Public-API surface declared** at `__all__` in `pipeline/scout/run.py` + re-exported via `pipeline/scout/__init__.py`; new names: `run_scout_discover_verify_review`, `run_scout_discover_verify` (alias), `ScoutRunResult`, `_build_fit_rationale`, `BuildFitRationale`, `RationaleBudgetExceeded`, `RationaleBuildFailed`, `MAX_FIT_RATIONALE_BYTES`, `RunDegradationEvent`, `ScoutRunInterrupted`, `F_SCOUT_RUN_01..05`. `__version__` bumped to `"0.1.0-scout-r11"`.
- **Schema version (artifact-producing):** none new. The `ScoutRunResult` dataclass is in-process Python; `ReviewQueueItem` records continue to use Round 10's canonical-JSON path under R10's existing `vault_write` intent `"review-queue-write"`. The signed health tuple is unchanged from Round 8 / §2 §4.10.
- **Crypto-agile types:** none new. The capstone consumes the signed health tuple opaquely.
- **Drift detection BLUEPRINT_DEPS:** populated at module top with `section_03_scout.md` v0.1 hash prefix `0a82d955f95b0fca`; mirrors Round 8/9/10 pin discipline.

## Done definition

- All pytest green via `.venv/bin/python3 -m pytest tests/scout/test_round_11_capstone.py` (pinned interpreter — system Python 3.9 cannot collect `@dataclass(frozen=True, kw_only=True)` modules; CLAUDE.md §"Running tests — PINNED INTERPRETER").
- All five `F-SCOUT-RUN-*` codes covered with dedicated tests.
- Spec-card every row satisfied or justified.
- Lines-of-code within target ±25% (target ≈ 600 LOC at 1.5× — ±25% = 450–750).
- Shared-Protocol lineage tests use `__module__` not `is` (E-026).
- Live-tree smoke pass — `lint_tree(Path('pipeline'), DEFAULT_RULES)` returns 0 violations after R11 lands.
- Full suite green: `.venv/bin/python3 -m pytest` reports **6219 + Δ pass**, 0 unexpected fails, ≤ 4 skip/xfail (matching baseline). Δ ≈ 30–46 new tests.
- AST-lint R1/R2/R3/R4/R5/R6/R7 clean across `pipeline/scout/run.py`.
- Committee 5/5 PASS or explicit L-005 narrow-fix carve-out disposition (see below).

## Lessons-applied-from-start

- **E-017** (injected-Protocol pattern) — 10th Scout firing. **Zero new Protocol surface.** Every seam reused: `SessionLike` (R10) + `VaultWriter` (R10) + `CheckpointWriter` (R8/R9/R10) + `DegradationWriter` (R8/R9) + `HealthTupleSigner` (R8) + `InterruptProbe` (R8/R9) + `ExecutorFactory` (R8/R9) + `EntropyFn` (R8) + `ClockFn` (R8/R9 ns vs R10 iso) + `SynopsisFetcher` (R9) + `ApplicantProfileProvider` (R9) + `BuildFitRationale` (NEW — but `BuildFitRationale` is an interface for the rationale-build callable, not a new I/O seam, and the default implementation is shipped inside `run.py` itself).
- **E-024** (1.5× multiplier) — naive floor 30 → expected ~45 tests. LOC target ±25% of 1.5× figure.
- **E-025** (range-check version pin) — `test_run_version_pin_rN_ge_11` via tuple comparison. **Applied from start.**
- **E-026** (`sys.modules`-reload fragility) — shared-Protocol lineage tests use `__module__` attribute. **Applied from start.**
- **E-027** (lint_tree directory-required) — AST-lint test passes a directory tmp_path with empty `__init__.py`. **Applied from start.**
- **E-028** (`# pragma: no cover` doctrine) — applied to any contract-unreachable defensive branch (e.g., `# pragma: no cover` on a defensive `isinstance` guard against a deployment-broken `BuildFitRationale` returning a non-string non-bytes object, where the byte-count check has already raised `RationaleBuildFailed`).

## Committee dispatch (handoff-required)

5-family Code Thesis Committee per `router.yaml` `code_reviewer_{1..5}`. Cross-family rigor enforced (L-003, A3): author family Anthropic; the five reviewer slots resolve via router.yaml today as

- `code_reviewer_1` → `openai/codex` (OpenAI family) — fallback `openai/gpt-4o`
- `code_reviewer_2` → `alibaba/qwen3-32b` (Alibaba family) — self-fallback (Groq Dev tier catalogue constraint)
- `code_reviewer_3` → `meta/llama-3.3-70b` (Meta family) — self-fallback
- `code_reviewer_4` → `openai_oss/gpt-oss-120b` (OpenAI-OSS family) — fallback `openai_oss/gpt-oss-20b`
- `code_reviewer_5` → `moonshot/kimi-k2-instruct-0905` (Moonshot family) — fallback `google/gemini-2.5-pro` (Google family) when the operator lacks a Moonshot key.

Five distinct families resolve in production: OpenAI, Alibaba, Meta, OpenAI-OSS, Moonshot. Author family Anthropic is distinct from all five. EN-003 substitution contract applies: any swap is logged in `committee_summary.md` for the round.

L-005 discipline: Audit #1 scoping → narrow-fix (≤ ~5 LOC, zero public-API, zero blueprint-semantic delta per §8b carve-out) → Audit #2 verification → LOCK or escalate. No silent third round. Transport-retry carve-out (L-011) applies — a single 60s backoff on infrastructure-class transport failure is admissible inside a single audit cycle.

PASS condition: 5/5 reviewer verdicts equal `"LOCKED"` or `"READY_TO_LOCK"` after the verification audit.

## Spec-card version history

- **v1 (2026-04-29)** — initial draft per handoff `pipeline/handoffs/scout_round_11_capstone_dispatch_2026-04-21.md`. Step 0 reconciliations 1–3 above. Blueprint hash pinned `0a82d955f95b0fca`. Re-verify Round 8/9/10 public surface at build-time before Step 1.
