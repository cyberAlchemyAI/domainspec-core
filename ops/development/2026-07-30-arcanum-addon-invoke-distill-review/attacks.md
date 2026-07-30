# Verbatim Distill Review Returns

## Abramsky, Samson — Proposer

action_id=spawn-0001
dispatch_id=arcanum-addon-invoke-distill-validation-v1
run_id=run-20260730-f3ada9f1
wave_id=distill-validation
step_id=s1-distill
role=distill-proposer
capability_ref=distill
started_at=2026-07-30T07:02:00Z
finished_at=2026-07-30T07:08:12Z
status=pass
validation=block

artifacts:

- `development/arcanum-addon/define/`
- `development/arcanum-addon/design/`
- `development/arcanum-addon/plan/`
- `development/arcanum-addon/BASELINE-REFRESH.md`

findings:

1. Severity: high — the L0/L1 promotion decision is load-bearing but lacks a persisted acceptance boundary and dependency edge.

   Evidence: `plan/work-pack/tasks/TASK-1-CATALOG-PREVIEW.md:100-103` says L0 closes with an operator decision; `plan/work-pack/waves/W1.md:11` requires “continue,” “preview-only,” or “stop”; but `plan/work-pack/waves/W2.md:6` requires only that W1 “passes,” and `plan/WORK-PACK.md:76-78` moves directly from proposal UI to approval/run work without a decision SWU or receipt.

   Objection: the layer heuristic says every layer unlocks one decision, yet that decision can presently disappear into an informal wave status. W2 could therefore begin without durable proof that the operator chose continuation.

   One-line repair: add an explicit L0 continuation-decision receipt, owner, acceptance condition, and dependency required by APPROVAL-001/W2.

2. Severity: high — the W4 lifecycle schedule composes uninstall and rollback as one linear execution despite their incompatible starting states.

   Evidence: `plan/work-pack/waves/W4.md:5-6` orders `DISABLE -> UNINSTALL -> ROLLBACK`; `plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md:31-38` makes uninstall remove admitted product-owned configuration, while lines 40-46 require rollback to restore a prior product manifest/adapter/profile. No reset, isolated fixture, or branch semantics separates these acceptance runs.

   Objection: after uninstall, rollback is no longer testing rollback from the disabled installed candidate described by its contract. The sequence either introduces hidden restoration glue or conflates two independent lifecycle experiments.

   One-line repair: model UNINSTALL and ROLLBACK as separate branches from the same accepted disabled snapshot, each with isolated/resettable fixtures and receipts before recomposition.

3. Severity: high — degraded compatibility/owner-loss behavior is promised at the layer level but has no independently scheduled SWU acceptance boundary.

   Evidence: `design/ARCHITECTURE.md:168-175` specifies unavailable/incompatible and `Unknown` failure behavior; `plan/IMPLEMENTATION-LAYERING.md:29` says L3 proves degraded modes; but `plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md:21-67` contains only disable, uninstall, rollback, security, and browser SWUs. `plan/WORK-PACK.md:86-90` likewise has no compatibility-drift/owner-loss degradation SWU.

   Objection: status-level unavailable behavior in L0 does not prove an enabled/running product transitions safely when provenance or an owner disappears. Disable and `Unknown` cover different states.

   One-line repair: add or explicitly bind a degradation acceptance boundary covering compatibility drift and owner loss, zero new starts, honest projection, recovery/re-enable rules, and preserved owner history.

4. Severity: medium — the aggregate atomicity proof omits several non-exempt SWUs and therefore overstates complete review coverage.

   Evidence: `plan/WORK-PACK.md:97-112` claims an SWU atomicity review but has no row for BOOT-002, PROPOSAL-UI-001, or RUN-UI-001, even though their task-local split analyses exist at `plan/work-pack/tasks/TASK-0-GOVERNANCE-COMPATIBILITY.md:62-80`, `TASK-1-CATALOG-PREVIEW.md:77-93`, and `TASK-2-APPROVAL-STATE.md:58-74`.

   Objection: the underlying units appear defensible, but the aggregate proof cannot currently demonstrate the dispatch convergence criterion that every non-exempt SWU was checked.

   One-line repair: enumerate every non-exempt SWU in the atomicity table or provide an exact complete mapping to task-local analyses.

Attack attempts completed:

- recomposed Define outcome through Design views, L0-L3, S0-S5, W0-W5, and the literal Strategy/Whisper scenario;
- tested Bootstrap, ResonantOS, Augmentor, archive, acceptance, promotion, and release owner preservation;
- tested hidden third-runtime and fallback substitution;
- tested proposal/approval/registration/start/terminal-state separation;
- tested SWU dependency closure and optional BOOT-002 routing;
- tested first-unit narrowness and mutation ordering;
- tested independent result actions and child isolation;
- tested replay, rollback, uninstall, degradation, and recovery behavior;
- tested planned-witness inflation and readiness/promotion ceilings;
- checked every task-local independent-acceptance statement and aggregate atomicity coverage;
- verified the pinned baseline: worktree `HEAD` and `origin/dev` both equal `80dcd79677ad73b21dbaded12e0e9cd47aace82b`; consumer Strategy remains absent; consumer Whisper SHA-256 is `09529bc...`, while current generated canonical is `f8a5ad1c...`; the four cited bridge capabilities remain present; no `addon.arcanum` manifest was found.

blockers:

- The four objections above require Invoke reconciliation before Distill validation can pass.
- The existing governance, Bootstrap, owner, adapter, and retention blockers remain unaffected.
- This receipt alone cannot satisfy the all-role join gate.

residue:

- Review was read-only; no files were created or edited.
- No SWU was selected.
- No runtime witness, product readiness, promotion, or release is claimed.
- The accepted research topology was treated only as a probe.
- The parent still owns persistence of `development/arcanum-addon/plan/distill/PROPOSER.md`, joining both role receipts, and reconciliation.

handoff_note: Invoke should persist this raw Proposer receipt, join it with the independent Balancer receipt, reconcile each objection as accept/revise/reject/defer/route, and keep the work-pack blocked unless every acceptance-critical objection is closed.

## Ashby, W. Ross — Balancer

action_id: spawn-0002
dispatch_id: arcanum-addon-invoke-distill-validation-v1
run_id: run-20260730-f3ada9f1
wave_id: distill-validation
step_id: s1-distill
role: distill-balancer
capability_ref: distill
started_at: 2026-07-30T07:03:00Z
finished_at: 2026-07-30T07:08:07Z
status: pass
validation: block

artifacts:

- `development/arcanum-addon/define/`
- `development/arcanum-addon/design/`
- `development/arcanum-addon/plan/`
- `development/arcanum-addon/BASELINE-REFRESH.md`
- Current target repository at `80dcd79677ad73b21dbaded12e0e9cd47aace82b`

blockers:

- `BAL-001`: W4 serializes uninstall before rollback even though they require alternative post-disable candidate states.
- `BAL-002`: the validation matrix has no concrete uninstall or rollback separation witnesses.
- `BAL-003`: `BOOT-002` lacks an explicit atomicity review despite potentially refreshing multiple generated packages.
- Existing authored blockers `B-GOV-001`, `B-BOOT-001`, `B-OWNER-001`, `B-ADAPTER-001`, and `B-RETENTION-001` remain valid.

findings:

1. id: `BAL-001`
   severity: high
   objection: Lifecycle recomposition is internally inconsistent.
   failure_trace: `DISABLE-001` → `UNINSTALL-001` removes admitted product state → `ROLLBACK-001` is then expected to restore a prior manifest/adapter/profile on that same linear candidate → security claims coverage over all mutation SWUs. Uninstall and rollback are separate recovery branches, not a safe serial chain.
   evidence:

   - `development/arcanum-addon/plan/work-pack/waves/W4.md:5-6` mandates `DISABLE -> UNINSTALL -> ROLLBACK`.
   - `development/arcanum-addon/plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md:31-46` defines uninstall as removal and rollback as restoration.
   - `development/arcanum-addon/plan/work-pack/shared/CLOSEOUT-SYNC.md:28-30` independently routes both from disable to security, contradicting the wave’s serialization.
   one_line_repair: Model uninstall and rollback as independent post-disable branches with isolated baselines, then require both branch receipts at the security recomposition gate.

2. id: `BAL-002`
   severity: high
   objection: Lifecycle/security gates can pass through authored labels without concrete uninstall or rollback witnesses.
   failure_trace: disable test passes → generic “lifecycle tests” label passes → uninstall deletes Bootstrap-owned or retained history, or rollback mutates generated packages/fails to preserve disable → no specifically bound negative fixture detects the violation → security closure is reported complete.
   evidence:

   - `development/arcanum-addon/design/VALIDATION-CONTRACTS.md:7-18` defines `F-DISABLE` but no uninstall or rollback fixture.
   - `development/arcanum-addon/design/VALIDATION-CONTRACTS.md:31-40` names lifecycle tests only generically.
   - `development/arcanum-addon/plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md:48-56` lets `SECURITY-001` close on “all declared controls,” leaving undeclared lifecycle separations untested.
   - `development/arcanum-addon/plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md:31-46` contains the load-bearing uninstall/rollback claims requiring those witnesses.
   one_line_repair: Add digest-bound uninstall-preservation and rollback/failure/disable fixtures with explicit forbidden-mutation counters and isolated starting states.

3. id: `BAL-003`
   severity: medium
   objection: `BOOT-002` is execution-shaped but omitted from the explicit atomicity table.
   failure_trace: one approved “selected-package refresh” includes Strategy, Whisper, and support packages → one package succeeds and another fails or changes selection → the combined SWU cannot independently accept or retry a bounded package delta → post-refresh compatibility obscures partial mutation.
   evidence:

   - `development/arcanum-addon/plan/work-pack/tasks/TASK-0-GOVERNANCE-COMPATIBILITY.md:62-80` permits an exact selected-package refresh and refers to multiple required packages.
   - `development/arcanum-addon/plan/WORK-PACK.md:71` schedules `BOOT-002`.
   - `development/arcanum-addon/plan/WORK-PACK.md:97-112` provides no `BOOT-002` atomicity row.
   one_line_repair: Add a `BOOT-002` atomicity row binding one exact package selection/delta and specify partial-apply recovery or split package refreshes.

4. id: `BAL-004`
   severity: low
   objection: The governance SWU couples issue acceptance, Project fields, multiple owner appointments, and retention policy into one acceptance boundary.
   failure_trace: issue is accepted but Project synchronization or retention appointment fails → the entire SWU remains open even though independently durable authority evidence exists → later retries risk stale or divergent approvals.
   evidence:

   - `development/arcanum-addon/plan/work-pack/tasks/TASK-0-GOVERNANCE-COMPATIBILITY.md:24-38` combines issue, Project record, seven owner classes, and retention into one SWU.
   - `development/arcanum-addon/plan/WORK-PACK.md:101` defends the coupling only as “one authority decision set.”
   one_line_repair: Define an explicit atomic owner transaction/receipt across both systems or split governing acceptance from Project synchronization and owner/retention binding.

validations_run:

- Read the complete current corpus under `define/`, `design/`, and `plan/`, including both dispatch documents and generated Design selection receipts.
- Verified the worktree and `origin/dev` both resolve to `80dcd79677ad73b21dbaded12e0e9cd47aace82b`.
- Verified consumer-root Subagent Strategy remains absent.
- Verified consumer-root Whisper SHA-256 remains `09529bc080fbed6ca83ad58fea6b349c95a78f5f73f39f3b06a9c28c4dba0446`.
- Confirmed the planning corpus is untracked planning material and does not constitute implementation evidence.
- Attacked Bootstrap drift, absent native owners, stale proposal approval, replay, partial child start, reload truth, artifact side effects, disable, uninstall/rollback separation, secret/path disclosure, witness inflation, SWU coupling, owner assignment, and evidence recomposition.
- Stale approval, replay, partial-child isolation, reload/`Unknown`, artifact action separation, disable rejection, secret/path redaction, absent-owner no-substitution, and planned-witness claim ceilings are materially represented in the current contracts; no additional objection was found for those attacks beyond the lifecycle and atomicity gaps above.

residue:

- Baseline absence/drift checks remain regression probes, not compatibility or execution proof.
- No runtime, browser, lifecycle, readiness, promotion, or release witness was executed.
- No SWU was selected.
- No file was edited or created.
- The current plan remains correctly blocked even after this bounded review completes.

handoff_note: Invoke should preserve this raw Balancer receipt, reconcile `BAL-001` through `BAL-004` explicitly, and keep the Plan blocked. `BAL-001` and `BAL-002` should block Distill validation until the lifecycle branch topology and concrete witnesses are repaired; `BAL-003` requires an explicit atomicity disposition; `BAL-004` may be repaired or formally rejected with authority-transaction evidence.
