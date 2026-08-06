# Non-Vacuity Reviewer Report — `spawn-0006`

`NON_VACUITY_GATE: FAIL`

The synthesis contains executable negative witnesses, but it does not contain the required exact normal-path witness from an Invoke output through final synchronized evidence. It also omits a witnessed Orchestrate cross-wave action-ID collision.

## Gate result

Scoped validation executed successfully:

- Plan-once selection/end-to-end: 7/7 tests passed.
- Pre-execution prerequisite integration/resume: 7/7 passed.
- Continuation Router: 14 normal fixtures passed; 3 adversarial fixtures rejected.
- Selected Orchestrate suites: 17/17 passed.

Those successes do not close the gate. The plan-once “end-to-end” test stops at mutation admission, while Task Session requires terminal execution, `CloseoutSync`, a joined Invoke Refresh owner receipt, and a continuity cursor for synchronized completion.

## Finite traces

### Normal trace — candidate only, not a qualifying witness

Attacks: `TRACE-NORMAL-001`, `SYS-006`, `LIN-006`, `PLAY-001`, `ATTACK-004`.

- Inputs: fixture plan config for `TASK-U1`/`SWU-U1`, Work Pack execution binding, validation contract, material package, exact artifact references, and execution-intent binding.
- Ordered gates:

  1. Invoke-authored Plan/Work Pack — represented by a fixture, not an exact Invoke result receipt.
  2. WPRA audit → `plan-semantic-manifest.json` plus `selection-handoff.json`.
  3. Selection recomputes the epoch and emits `selection-receipt.json`.
  4. Material producer validation.
  5. Task Session mutation admission → `admissionVerdict=admit`, `mutationReady=true`.
  6. Required but unwitnessed: fast-entry binding, Context Builder, closeout preflight, single-use consumption, execution ticket, bounded mutation, critical validation, terminal Task Session receipt.
  7. Required but unwitnessed: `CloseoutSync` revalidation, Continuation Router dispatch of `invoke:refresh:apply-approved`, joined owner receipt, synchronized result, continuity cursor.

- Expected receipts: semantic manifest, selection receipt, fast-entry receipt, context pack, closeout preflight, mutation-admission receipt, consumption ledger, execution ticket, terminal Task Session receipt, closeout owner receipt, continuity cursor.
- First evidentiary stop: `test_plan_once_end_to_end.py:144-150` ends immediately after admission. No terminal execution or synchronization evidence follows.
- Forbidden effects: mutation before admission; Task Session impersonating Invoke Refresh; synchronized completion without a joined owner receipt; executing the successor SWU during closeout.
- Proof status: `EXECUTED` only through admission; fixture input is not bound to an exact Invoke output receipt; terminal execution and real-owner closeout are `UNVERIFIED`.

Verdict: **kill** `TRACE-NORMAL-001` as an “exact normal trace.” It may remain only as an explicitly expected contract trace. **Sustain** `ATTACK-004`.

### Failure trace 1 — stale plan-once selection

Attacks: `GATE-005`, `TRACE-FAIL-001`.

- Inputs: exact audited manifest, current audit config, selection request for `TASK-U1`/`SWU-U1`, execution-intent binding, dependency inventory, and lifecycle evidence.
- Fault: change `execution_bindings[0].command.cwd` after audit.
- Ordered gates:

  1. Re-read exact manifest and config.
  2. Recompute plan semantics.
  3. Compare canonical semantic digest, component digests, and unit-contract digests.
  4. Emit blocked selection receipt.

- Expected receipt: selection receipt with `selectionVerdict=block`, `mutationReady=false`, `authorityEffect=none`, and `terminalCode=PLAN_EPOCH_STALE` or `PLAN_COMPONENT_CHANGED`.
- First stop: `verify_plan_selection.py:165-183`, before Context Builder, material admission, or mutation.
- Forbidden effects: selection, execution entry, admission, mutation, or guessed continuation.
- Proof status: `EXECUTED`; `test_plan_once_selection.py:278-291` passed live.

Verdict: **sustain**.

### Failure trace 2 — unjoined pre-execution prerequisite owner

Attacks: `GATE-007`, `TRACE-FAIL-002`.

- Inputs: classifier receipt, exact authorization evidence, v2 continuation-route receipt, owner receipt and schema, target inventory, validation contract, satisfaction predicate, attempt ID/fingerprint, one-hop budget, and same-attempt control handle.
- Fault: route declares `helper_closeout=block`.
- Ordered gates:

  1. Classify the prerequisite as unmet.
  2. Match exact authorization and the sole owner route.
  3. Require exactly one completed dispatch and join.
  4. Validate route, owner receipt reference, control handle, and helper closeout.
  5. Only then rehash baselines and consume the attempt/fingerprint.

- Expected receipt: a passing `pre-execution-resume-receipt.json` only after the chain passes; for this negative, that receipt must not exist.
- First stop: `task-session-governance-runner.py:767-800`, raising `RunnerBlock("continuation route is not a joined one-hop prerequisite result")`.
- Forbidden effects: no consumption ledger, resume receipt, Context Builder entry, mutation admission, target hashing/mutation, or recursive Task Session route.
- Proof status: `EXECUTED`; the adversarial matrix passed and asserted that no resume receipt exists.
- Evidence defect: `TRACE-FAIL-002` bundles several faults and diagnostic names into one row. The inspected executable path proves a `RunnerBlock` message, not a durable receipt carrying all synthesis-listed codes.

Verdict: **repair** the trace into separate one-fault witnesses with exact emitted diagnostics; sustain the underlying fail-closed behavior.

### Failure trace 3 — missing or failing closeout owner join

Attacks: `GATE-011`, `TRACE-FAIL-004`, `BUG-011`, `ATTACK-004`.

- Inputs: terminal Task Session receipt, current closeout preflight, `CloseoutSync`, declared target inventory/baselines/deltas, exact `invoke:refresh:apply-approved` authorization, expected owner receipt contract, and successor policy.
- Fault: no terminal owner receipt joins, or the owner returns failure.
- Ordered gates:

  1. Revalidate closeout preflight against live targets.
  2. Admit only declared synchronization deltas and exact owner route.
  3. Continuation Router dispatches one owner hop.
  4. Require helper closeout and a separate validated terminal owner receipt.
  5. Only after join may Task Session emit synchronized status and a continuity cursor.

- Expected receipt: blocked continuation-route receipt such as `route-work-pack-missing-join-block.json` or `route-work-pack-owner-failure-block.json`; no executable returned route and no continuity cursor.
- First stop: owner join/validation. Task Session preserves execution evidence but returns `BLOCK`.
- Forbidden effects: Task Session editing owner targets, reporting synchronized completion, emitting an executable next route, or starting the next SWU.
- Proof status: static route fixtures were `EXECUTED` through semantic validation; a product-through-real-owner closeout remains `UNVERIFIED`.

Verdict: **sustain** `GATE-011`, `BUG-011`, and `ATTACK-004`; **repair** `TRACE-FAIL-004` so its fixture-level proof cannot be mistaken for runtime E2E proof.

## Newly observed Orchestrate defects

### Shared receipt-directory scope defect

Attacks: `BUG-012`, `BUG-013`, `ATTACK-011`.

Finite witness: **yes**.

- Exact three explorer receipts produce zero reducer blockers.
- Adding `check-tension.json` and `confirmation.json` produces 30 shape blockers.
- `_load_receipts_directory()` reads every `*.json`; it does not select required action receipts.
- The actual failed reduction emitted `gate_block`; the action-only repaired reduction emitted `gate_pass` without retry or respawn.

Validator detection: **misclassified detection only**. Receipt admission fails closed on the unrelated documents, but no validator recognizes that the reducer’s input scope is wrong. Existing reducer tests contain no unrelated-JSON directory case.

Verdict: **sustain** `BUG-012`, `BUG-013`, and `ATTACK-011`.

### Cross-wave action-ID collision

Synthesis claim/attack ID: **none; omitted defect**.

Finite witness: **yes**.

- Prior run IDs were `spawn-0001` through `spawn-0004`.
- Stock wave-02 reduction emitted reviewer actions `spawn-0002`, `spawn-0003`, and `spawn-0004`.
- Cause: `_compile_named_wave_actions(... start_action_number=len(actions)+1)` uses only the current wave’s action count.
- The stock action set passes its JSON schema despite all three IDs colliding.
- The coordinator therefore has no pre-spawn global-uniqueness stop.
- An in-memory stock `spawn-0002` attempt appended to the complete prior event prefix is detected later by `validate_run_evidence.py` as `duplicate_action_attempt`.
- The current run required the manual deterministic remap to `spawn-0005` through `spawn-0007`.

Validator detection: **too late**. Evidence validation detects the collision only after an attempted action is journaled. Compile/reduce schemas and the passing two-wave regression suite do not detect it before host effects.

Verdict: **repair** the synthesis Bug Map and Attack Ledger; the candidate holistic map cannot pass while this defect is absent.

## Claim verdicts

| Synthesis IDs | Verdict | Reason |
|---|---|---|
| `TRACE-NORMAL-001` | **kill** | No finite Invoke-output-to-synchronized-evidence witness. |
| `SYS-006`, `LIN-006`, `PLAY-001` | **repair** | Coherent contracts, but must be labelled normative/expected rather than executed E2E. |
| `GATE-005`, `TRACE-FAIL-001` | **sustain** | Exact stale-plan negative is executable and discriminating. |
| `GATE-007`, `TRACE-FAIL-002` | **repair** | Fail-closed behavior is executable; bundled codes and receipt claims need one-fault bindings. |
| `GATE-011`, `BUG-011` | **sustain** | Contract and static negative fixtures preserve execution while blocking synchronization. |
| `TRACE-FAIL-004` | **repair** | Fixture-level proof is not real-owner E2E proof. |
| `ATTACK-004` | **sustain** | Correctly records the missing normal witness. |
| `BUG-012`, `BUG-013`, `ATTACK-011` | **sustain** | Actual run evidence supplies a finite witness. |
| `GATE-012`, `TRACE-FAIL-005`, `ATTACK-010` | **sustain** | Event-contract timeout evidence is correctly bounded; it does not repair the normal trace. |
| `ATTACK-013`, `ATTACK-014` | **sustain** | Evidence ceilings remain necessary. |
| Bug Map and Attack Ledger completeness | **repair** | Missing cross-wave action-ID collision and pre-spawn validator gap. |

## Bounded repairs

1. Add one exact fixture from a bound Invoke result through WPRA, selection, fast entry, admission, terminal Task Session receipt, real owner-adapter closeout join, and continuity cursor. Assert every digest and forbid owner impersonation.
2. Give the reducer explicit required receipt paths or an exact action-only input set. Preserve rejection of unexpected valid action receipts without parsing unrelated governance JSON as receipts.
3. Carry a run-global next action number or immutable action-ID registry in state. Validate uniqueness against historical actions before emitting or attempting the next wave.
4. Add a three-wave regression where a one-action middle wave is followed by multiple actions.
5. Add an evidence-order `duplicate_action_attempt` fixture, but retain a separate pre-spawn validator; post-attempt detection is not sufficient.
6. Split `TRACE-FAIL-002` into individual stale, non-pass, replay, and unjoined-owner witnesses with exact receipt/error bindings.

## Evidence gaps

- No exact Invoke output receipt is bound to the positive plan-once fixture.
- No terminal Task Session receipt follows the tested mutation admission.
- No real product-through-Invoke-Refresh closeout join and continuity cursor witness.
- Owner-resume failures raise `RunnerBlock` without a durable negative resume receipt.
- No existing test exercises unrelated JSON in the reducer receipt directory.
- No existing compile/reduce test exercises three waves or run-global action-ID uniqueness.

## `ACTION_RECEIPT`

```json
{
  "action_id": "spawn-0006",
  "dispatch_id": "2026-08-05-arcanum-building-system-research-route",
  "run_id": "arcanum-building-system-research-run-01",
  "wave_id": "reviewers",
  "step_id": "s3-review",
  "role": "skeptic-non-vacuity",
  "capability_ref": "research",
  "agent_id": "/root/skeptic_non_vacuity_spawn_0006",
  "status": "pass",
  "validation": "fail",
  "blockers": [
    "No exact normal-path witness binds an Invoke output through terminal Task Session execution, joined closeout owner receipt, and continuity cursor.",
    "The synthesis omits the witnessed cross-wave action-ID collision and the absence of pre-spawn global uniqueness validation.",
    "TRACE-FAIL-002 bundles faults and diagnostics without one exact durable receipt binding per fault."
  ],
  "artifacts": [
    "native-agent-return:/root/skeptic_non_vacuity_spawn_0006#returned-reviewer-report"
  ]
}
```
