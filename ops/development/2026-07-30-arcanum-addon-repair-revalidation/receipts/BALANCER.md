schema_version: `arcanum.native-dispatch-runner.receipt.v0.1`  
action_id: `spawn-0002`  
dispatch_id: `2026-07-30-arcanum-addon-repair-revalidation`  
run_id: `arcanum-addon-repair-revalidation-a850483e`  
wave_id: `repair-revalidation`  
step_id: `s1-revalidate-repair`  
role: `Balancer`  
capability_ref: `distill`  
agent_id: `/root/repair_revalidation_balancer_spawn_0002`  
status: `BLOCK`  
validation: `BLOCK`  
started_at: `2026-07-30T15:39:00-03:00`  
finished_at: `2026-07-30T15:47:48-03:00`

## Exact-byte baseline

- Corpus roots: `development/arcanum-addon/{define,design,plan}`
- File count: `75`
- Aggregate algorithm: sorted absolute-path `sha256sum` stream, then SHA-256 of that stream
- Aggregate digest: `5b5e79f5632b2e29e7a20e7ac4d9e92addef6f707e9525c71e7266c24349e4b0`
- `HEAD`: `80dcd79677ad73b21dbaded12e0e9cd47aace82b`
- `origin/dev`: `80dcd79677ad73b21dbaded12e0e9cd47aace82b`
- JSON parse: `25/25` JSON files passed
- Corpus review: all 75 files were byte-read by the digest computation; semantic falsification covered authority, state, lifecycle, evidence, blockers, status synchronization, and route topology.

## Verdict

`BLOCK`.

Seven findings are literally closed. `NEW-001` is not closed at the machine-route level: exact SWU nodes and complete wave joins now exist, but the static `mode: sequence` dependency graph still admits successors from prior receipts without a fresh operator-selection input or dependency. The prose-only `g-swu-reentry` condition does not structurally gate any step.

A conforming dependency scheduler can therefore execute:

`W0-COMPLETE -> CATALOG-001 -> STATUS-001 -> PROPOSAL-001 -> ...`

without an intervening selection receipt. This contradicts the route intent to execute one explicitly selected SWU per Task Session and the closeout contract that a successor is only a candidate.

## Eight-finding closure matrix

| Finding | Result | Literal evidence | Disposition |
| --- | --- | --- | --- |
| F-001 durable L0 continuation decision | PASS | `plan/work-pack/tasks/TASK-1-CATALOG-PREVIEW.md:95-113`; `plan/work-pack/waves/W1.md:6-13`; `plan/DISPATCH.json:169-203` and the later L0 decision/join nodes | Durable owner-issued `continue`, `preview-only`, or `stop` receipt is required; only current `continue` admits approval. |
| F-002 isolated uninstall/rollback branches | PASS | `plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md:53-81,114-119`; `plan/DISPATCH.json:1127-1212` | Both branches depend on DISABLE, consume isolated copies of one accepted snapshot, use distinct branch IDs, and cannot consume sibling mutation. |
| F-003 lifecycle witnesses and counters | PASS | `design/VALIDATION-CONTRACTS.md:17-22,33-35`; `plan/work-pack/shared/CLOSEOUT-SYNC.md:29-33`; `plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md:38-43,62-66,76-81` | Required zero-start, history, forbidden Bootstrap/history mutation, recovery, digest, and branch witnesses are explicit. |
| F-004 degradation SWU and acceptance | PASS | `design/VALIDATION-CONTRACTS.md:18-19,33`; `plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md:23-43`; `plan/DISPATCH.json:1047-1083` | Compatibility drift and owner absence have one dedicated enabled/running degradation boundary with separate fixtures and fail-closed acceptance. |
| F-005 complete atomicity and BOOT-002 transactionality | PASS | `plan/work-pack/tasks/TASK-0-GOVERNANCE-COMPATIBILITY.md:31-42,67-89` | Partial governance cannot pass; BOOT-002 must validate the complete staged selection and either commit all or restore the exact before-inventory. |
| F-006 atomic governance receipt | PASS | `plan/work-pack/tasks/TASK-0-GOVERNANCE-COMPATIBILITY.md:24-45`; `plan/work-pack/shared/CLOSEOUT-SYNC.md:11,37-39` | One complete owner-issued receipt binds issue, Project snapshot, owners, retention, source, and disposition; stale/partial receipts fail closed. |
| NEW-001 implementation dispatch bypasses complete closure | BLOCK | Exact joins exist at `plan/DISPATCH.json:126-166,1215-1264,1360-1424`; however the route is a static sequence at `:4-9`, CATALOG depends only on W0 join at `:169-203`, STATUS depends only on CATALOG at `:205-213`, and `g-swu-reentry` is only an unattached condition at `:1534-1538`. Machine inspection found `selection_bound_steps: []`; only L0 continuation, BOOT-002 approval, and retention are decision inputs. | Exact receipts fixed the old generic-receipt defect, but no machine-enforced per-SWU re-entry/selection gate exists. |
| NEW-BAL-001 lifecycle baseline conflation | PASS | `design/VALIDATION-CONTRACTS.md:33-35`; `plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md:40-43,65-81,90-97`; `plan/work-pack/shared/CLOSEOUT-SYNC.md:29-33`; `plan/DISPATCH.json:1215-1318` | Enabled/running degradation and later disabled-snapshot branches are typed separately and joined at SECURITY-001 without equating their digests. |

## Surviving finding

### NEW-001 — MAJOR — Per-SWU operator re-entry remains prose-only

Counter-example:

1. `s03-catalog-001` completes and emits `receipts/CATALOG-001.json`.
2. `s04-status-001` has that step as its only dependency.
3. It consumes no operator-selection decision and references no `g-swu-reentry` binding.
4. A sequence/dependency runner can schedule it immediately.
5. The same pattern repeats across W1-W4, so exact receipt joins prevent missing work but do not enforce one-SWU-per-Task-Session admission.

One-line repair: model every exact SWU as a separately selected one-shot route, or require a fresh source-bound operator-selection receipt/input between every SWU and successor, with the selected SWU ID matched literally before admission.

No additional CRITICAL or MAJOR defect survived beyond this unresolved regression.

## Failure traces attempted

- Degradation from a disabled-only baseline: rejected by `V-DEGRADATION-BASELINE`.
- Compatibility drift: zero starts, incompatible projection, history preservation, explicit recovery required.
- Owner absence: no fallback substitution; zero starts; blocked/unknown owner truth.
- Uninstall consuming rollback-mutated state: rejected by isolated snapshot and branch-ID contract.
- Rollback consuming uninstall-mutated state: rejected symmetrically.
- Shared snapshot lineage drift: rejected by common accepted disabled-snapshot digest.
- Missing/distorted branch IDs or receipt digests: rejected by disabled-lifecycle validator.
- Forbidden Bootstrap/history mutation counters nonzero: branch validation fails.
- Stale/edited/expired approval: rejected with zero starts.
- Replay: second action starts nothing.
- Partial child start: child states remain independent; HTTP success cannot fabricate running/terminal truth.
- Reload cache inflation: projection must be exact owner truth or `Unknown`.
- Receipt inflation: planned witnesses and partial receipt sets cannot count as complete execution evidence.
- Security without both typed lifecycle validators: `V-SECURITY-LIFECYCLE-JOIN` fails.
- Browser before deterministic/security closure: browser node depends on SECURITY-001 and explicitly blocks early start.
- Verification without W4 closure: VERIFY consumes `W4-COMPLETE`.
- `selectedSWU: none` status drift: no non-none selection was found in the corpus.
- Per-SWU re-entry bypass: succeeded as a counter-example because no step consumes a selection binding; this causes the BLOCK verdict.

## Zero-finding attack defense

Not applicable as a zero-finding claim: a MAJOR counter-example survived. The review did not treat repair labels, authored status, the prior findings report, or the refresh report as proof. Only current target bytes and mechanically derived graph properties were admitted.

## Commands run

- `find ... -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum`
- `git -C <repo> rev-parse HEAD`
- `git -C <repo> rev-parse origin/dev`
- `find ... | sort`, `wc -l`
- `nl -ba` over the checklist, repair lead, validators, work pack, task, wave, closeout, and dispatch evidence
- `rg -n` over lifecycle, degradation, security, approval, replay, owner, reload, browser, blocker, digest, branch, receipt, and `selectedSWU` terms
- `jq -e .` over all 25 corpus JSON files
- Node structural inspection of step IDs, dependencies, decision inputs, selection-bound inputs, and gates
- Negative searches for legacy `L0`-`L3-selected-swu` receipts and `V-LIFECYCLE-BRANCHES`

## Blockers

- Artifact blocker: `NEW-001` remains MAJOR.
- No inspection blocker.
- No external authority, browser, network, or implementation action was attempted.

## Residue

- No target corpus, repository, network, browser, SWU selection, or external state was mutated.
- One host-local temporary checksum-stream file was inadvertently created during the first digest pass and immediately removed. The digest was then independently reproduced with a direct pipeline; `/tmp/arcanum-addon-75.sha256` is absent.
- `B-DESIGN-001` must remain open.
- `workPackGateStatus` must remain `block`.
- `selectedSWU` must remain `none`.
- This receipt proves planning defects only; it does not establish implementation, readiness, promotion, deployment, or release.

## Handoff note

Persist this receipt as `ops/development/2026-07-30-arcanum-addon-repair-revalidation/receipts/BALANCER.md`. Route the surviving MAJOR finding back to the dispatch-plan owner for a machine-enforced per-SWU selection/re-entry repair, then repeat exact-byte independent revalidation.
