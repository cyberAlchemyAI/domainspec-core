schema_version: `arcanum.native-dispatch-runner.receipt.v0.1`  
action_id: `spawn-0002`  
dispatch_id: `2026-07-30-arcanum-addon-plan-revalidation`  
run_id: `arcanum-addon-plan-revalidation-cc655251`  
wave_id: `revalidation`  
step_id: `s1-revalidate`  
role: `Balancer`  
capability_ref: `distill`  
agent_id: `/root/revalidation_balancer_spawn_0002`  
status: `block`  
validation: `block`  
started_at: `2026-07-30T13:43:00-03:00`  
finished_at: `2026-07-30T13:47:08-03:00`  
corpus_digest: `bb0a6f31cf1142902693d30c53ecc2ee08b6747e14ea12f7dff5b81d08d64b14`  
source_commit: `80dcd79677ad73b21dbaded12e0e9cd47aace82b`

artifacts:

- Every file recursively under `development/arcanum-addon/define/`
- Every file recursively under `development/arcanum-addon/design/`
- Every file recursively under `development/arcanum-addon/plan/`
- `development/arcanum-addon/BASELINE-REFRESH.md`
- Regression checklist: `ops/development/2026-07-30-arcanum-addon-invoke-distill-review/findings.md`
- Skill contract: `.agents/skills/distill/SKILL.md`
- No files produced or edited

blockers:

- `NEW-BAL-001`: `V-LIFECYCLE-BRANCHES` imposes one disabled-snapshot binding on degradation and lifecycle branches even though DEGRADE-001 starts from an enabled/running candidate.
- Existing execution blockers remain intentionally open: `B-GOV-001`, `B-BOOT-001`, `B-OWNER-001`, `B-ADAPTER-001`, and `B-RETENTION-001`.
- No SWU is selected; no implementation, browser evidence, readiness, promotion, or release is authorized.

## Review verdict

**BLOCK**

All six prior findings are materially closed in the literal planning contracts, but one new MAJOR validator-contract defect survives. Under the required acceptance rule, a new MAJOR finding prevents PASS.

## Corpus binding

- Product worktree HEAD independently resolved to `80dcd79677ad73b21dbaded12e0e9cd47aace82b`.
- All named corpus files were enumerated and byte-hashed.
- The frozen dispatch admits aggregate digest `bb0a6f31cf1142902693d30c53ecc2ee08b6747e14ea12f7dff5b81d08d64b14`.
- Residue: the dispatch artifacts do not state the aggregate serialization algorithm, so the admitted aggregate value was checked against the frozen dispatch/strategy binding rather than reconstructed from an independently specified canonical hashing procedure.

## Prior-finding closure matrix

| Finding | Result | Current-byte evidence |
| --- | --- | --- |
| F-001 durable continuation decision | CLOSED | `WORK-PACK.md:76-79` makes L0-DECISION-001 a distinct SWU and APPROVAL-001 depend on its exact `continue` disposition. `TASK-1-CATALOG-PREVIEW.md:95-109`, `W1.md:7-12`, `W2.md:7-10`, and `CLOSEOUT-SYNC.md:18-19` preserve its owner receipt and successor ceiling. |
| F-002 isolated uninstall/rollback | CLOSED | `TASK-4-LIFECYCLE-ACCEPTANCE.md:49-72,98-104` requires separate isolated copies of one accepted disabled snapshot. `W4.md:5-13` joins both receipts before security. `CLOSEOUT-SYNC.md:31-33` preserves separate branch bindings. |
| F-003 missing lifecycle witnesses | CLOSED | `VALIDATION-CONTRACTS.md:18-21` defines degradation, uninstall-preservation, and rollback-failure fixtures. `PLANNED-WITNESSES.json:19-37` keeps them explicitly `planned-only`. |
| F-004 absent degradation SWU | CLOSED | `WORK-PACK.md:87,121` and `TASK-4-LIFECYCLE-ACCEPTANCE.md:23-39` schedule DEGRADE-001 with drift, owner-loss, zero-start, honest projection, history, and recovery acceptance. |
| F-005 incomplete atomicity/BOOT-002 partial apply | CLOSED | `WORK-PACK.md:99-125` maps the complete non-exempt SWU set. `TASK-0-GOVERNANCE-COMPATIBILITY.md:67-89` requires staged validation plus all-or-nothing apply/restoration, otherwise pre-execution splitting. |
| F-006 partial governance synchronization | CLOSED | `TASK-0-GOVERNANCE-COMPATIBILITY.md:24-45` requires one digest-bound complete receipt; partial synchronization is non-pass and authorizes no successor. `WORK-PACK.md:103` repeats that ceiling. |

## New finding

### NEW-BAL-001 — MAJOR — Contradictory lifecycle-validator baseline

Failure trace:

1. `VALIDATION-CONTRACTS.md:18-19` defines degradation fixtures over an **enabled/running candidate**.
2. `TASK-4-LIFECYCLE-ACCEPTANCE.md:25-37` likewise starts DEGRADE-001 from an enabled/running accepted TASK-3 candidate with compatibility/owner baselines.
3. `VALIDATION-CONTRACTS.md:33` defines `V-LIFECYCLE-BRANCHES` over all “degradation/uninstall/rollback receipts” but gives the accepted binding as the **same accepted disabled snapshot digest**.
4. That disabled baseline is appropriate only for uninstall and rollback; `TASK-4-LIFECYCLE-ACCEPTANCE.md:81-83` correctly limits the shared disabled digest to those two branch receipts.
5. A validator implementing line 33 literally must either reject valid degradation evidence because it lacks the disabled-snapshot digest, or incorrectly relabel degradation as originating from disabled state. Either path makes SECURITY-001 recomposition ambiguous.

One-line repair: split the validator binding into `(a)` DEGRADE-001’s accepted enabled/running candidate plus compatibility/owner baseline digests and `(b)` UNINSTALL/ROLLBACK’s shared accepted disabled-snapshot digest and isolated branch IDs, then require SECURITY-001 to join both binding classes explicitly.

## Attacks attempted

- Bootstrap selection drift and consumer-package presence masquerading as compatibility
- BOOT-002 partial apply, restoration, and pre-execution split behavior
- Missing Strategy/Whisper native owners and fallback substitution
- Stale, expired, or changed proposal approval
- Replay duplication, crash admission, and partial-child start state
- Reload projection versus owner truth and explicit `Unknown`
- Artifact read, attach, consume, and archive-intake side effects
- Compatibility degradation and owner-loss recovery
- Disable and cached-launch rejection
- Uninstall/rollback state contamination and branch recomposition
- Retention-policy ambiguity
- Secret, raw-path, argv, diagnostic, and screenshot disclosure
- Planned-witness inflation into executed evidence
- Ambiguous successor routing
- Browser admission before deterministic/security closure
- Readiness, promotion, and release inference
- Full SWU atomicity coverage
- Governance/Project/owner partial synchronization
- Lifecycle validator baseline coherence

All attacks except lifecycle validator baseline coherence were either closed by literal contracts or remain honestly blocked as future execution/owner decisions.

## Validations run

- Enumerated the complete named corpus: 5,525 lines across the recursive file set plus baseline refresh.
- Independently resolved product source commit.
- Read and hashed every corpus file.
- Parsed every corpus JSON file successfully with `jq`.
- Searched the entire corpus for the attack vocabulary and inspected exact surrounding contracts.
- Confirmed browser admission requires SECURITY-001 and deterministic gates at `TASK-4-LIFECYCLE-ACCEPTANCE.md:87-95`, `VALIDATION-CONTRACTS.md:36-45`, and `CLOSEOUT-SYNC.md:33-34`.
- Confirmed planned witnesses remain explicitly non-executed.
- No browser, network mutation, repository mutation, SWU selection, or implementation occurred.

## Distill technique trace

- Abstraction-level guard: reviewed planning-contract closure, not product implementation.
- Recomposition proof: BLOCK; the lifecycle aggregate validator cannot coherently recompose degradation and disabled-snapshot branches under its present single binding.
- Evolution profile: not triggered; this is validation of a fixed planning corpus.
- Frame-expiry: any corpus-byte, source-commit, owner, or baseline change invalidates this receipt.
- Navigable result: repair `V-LIFECYCLE-BRANCHES`, then rerun both current-byte validators before considering B-DESIGN-001 closed.
- Premortem: a future validator follows the literal disabled-snapshot rule, silently excludes degradation evidence, and still allows SECURITY/BROWSER routing. Guardrail: typed distinct baseline fields plus mandatory presence checks.

## Residue

- Aggregate digest serialization is not specified in the reviewed corpus or dispatch strategy; the frozen admitted digest is therefore not independently reproducible from a documented canonical algorithm.
- The new MAJOR finding prevents B-DESIGN-001 closure.
- Existing governance, Bootstrap, owner, adapter, and retention blockers remain unaffected.
- Telemetry emission is caller-owned; this worker made no telemetry mutation.

## Handoff

Return this receipt to the parent as a blocking Balancer result. The parent should preserve `selectedSWU: none`, reject the revalidation join as PASS, route `NEW-BAL-001` to the Plan/Design authoring owner for bounded correction, and require fresh independent literal-byte revalidation afterward.
