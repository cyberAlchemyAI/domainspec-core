# Governance Flow Revision

> Deterministically derived from `GOVERNANCE-FLOW-REVISION.yml`. The machine
> proposal is authoritative for this design package. This human view grants no
> mutation, acceptance, execution, publication, or deployment authority.

## Outcome

The current system safely refuses to stretch exact acceptance across repaired bytes, but it discovers too many deterministic governance blockers only after an owner prompt. Producer-local PASS receipts are being mistaken for terminal closure, so safe repairs create serial approval loops. The correction is a three-mode flow that collects every reachable no-effect blocker before one frozen owner decision, then preserves fail-fast behavior once effects can occur.

- Status: `proposal_ready`
- Authority effect: `none`
- Terminal fixture in plan: `true`
- Claim ceiling: Evidence-backed design and exact implementation proposal only. No owner request, acceptance, selection, admission, product mutation, canonical public change, generated-package change, publication, Git action, deployment, or external effect is authorized or claimed.

## Evidence boundary

The formal Workflow Reflect threshold is not met: 1 directly matched signal. The proposal is justified as a severe-incident correction by 7 durable incidents and at least 4 renewed-acceptance cycles.

| Source | Use | Strength |
| --- | --- | --- |
| AGENTS.md | Repository-local authority boundaries, background-helper rule, governance sidecar choreography, public/private boundary, and propose-before-mutation rule. | canonical_instruction |
| .agents/skills/workflow-reflect/SKILL.md | Reflection method, evidence-strength limits, proposal shape, compatibility disclosure, and no direct observed-capability mutation during reflection. | canonical_instruction |
| .arcanum/observability/reflections/2026-08-24-evf-smt-approval-loop.md | Incident corpus proving producer-local PASS, late consumer discovery, repeated exact-byte reprompts, and the need for preacceptance consumer closure. | incident_supported |
| ops/development/2026-07-24-invoke-lifecycle-progress-update/machine-view-lifecycle-runtime/execution-entry-consumer-repair-v1/ADOPTION-RECEIPT.json | Adopted evidence for deterministic rehearsal, request/acceptance separation, exact consumer bindings, run-all validation, and authority-free preparation. | adopted_repair_evidence |
| ops/development/2026-07-24-invoke-lifecycle-progress-update/machine-view-lifecycle-runtime/execution-entry-consumer-repair-v1/CONSUMER-REPAIR-INDEPENDENT-REVIEW.json | Independent confirmation of machine-first projection, ordered consumer closure, no-effect rehearsal, one-request ceiling, and the remaining request-eligibility block. | independent_review_evidence |

## Practical before / after

### Before

| Step | Behavior | Authority |
| --- | --- | --- |
| 1. prepare local artifacts | Each producer validates its own output and can report PASS. | No execution authority, but local PASS is often treated as request-ready. |
| 2. prompt owner | An exact candidate is presented before all real downstream consumers have exercised it. | Owner acceptance binds exact bytes and correctly cannot cover later repairs. |
| 3. discover downstream blocker | A later validator, schema, runner, locator, projection, or closeout consumer finds a deterministic defect. | Effectful work stops safely. |
| 4. repair and reprompt | Acceptance-bound bytes change, the old decision becomes unusable, and the owner is asked again. | Safety is preserved at the cost of serial approval loops. |

### After

| Step | Behavior | Authority |
| --- | --- | --- |
| 1. schema-valid machine source | The model emits one versioned source containing the complete decision envelope and terminal outcome contract. | Preparation only; no authority effect. |
| 2. deterministically derived graph and human view | The compiler normalizes the source into the owner decision graph; the renderer derives the human view from that validated graph. | Derived artifacts cannot widen the source ceiling. |
| 3. collect-all rehearsal | Every reachable actual consumer runs in isolation; all blockers are accumulated and mechanically safe retries continue without prompting. | Only isolated run-local evidence writes are permitted. |
| 4. freeze | A zero-blocker rehearsal freezes the exact decision graph and terminal predicate. | Freeze grants no selection, admission, or execution authority. |
| 5. independent review | A distinct reviewer checks the frozen graph, complete rehearsal, privacy boundary, and request eligibility. | Review can only permit one request emission. |
| 6. single owner request | The request emitter publishes at most one idempotent question for the immutable graph and then stops. | The request itself grants no downstream authority. |
| 7. acceptance | The owner accepts or rejects the exact decision graph; revisions create a new graph rather than mutating the frozen one. | Acceptance is necessary but does not bypass selection or admission gates. |
| 8. fail-fast execution to terminal boundary | The admitted slice executes effects in order, stops at the first failed effect, and completes only when the terminal contract is satisfied. | Limited to the accepted, selected, admitted envelope; no automatic successor. |

## Required invariants

### GFR-01

Preacceptance is deterministic and no-effect except for isolated run-local evidence writes.

Enforcement: Deny repository target mutation, selection, admission, publication, deployment, credentials, external calls, and successor execution; hash protected inputs before and after every rehearsal.

### GFR-02

Preacceptance collects every reachable blocker and continues automatically.

Enforcement: Run all independent checks, preserve the first nonzero for process status, record later failures too, and mark dependency-blocked checks not_evaluable with causal blocker references.

### GFR-03

Human-decision mode stops exactly once on one immutable owner decision graph.

Enforcement: Use persistent idempotency keyed by decision_graph_digest; a repeat emission returns the original request identity and bytes and increments no prompt counter.

### GFR-04

Effectful execution fails fast.

Enforcement: After acceptance, stop at the first failed or blocked effect and prove that no later effect or successor ran.

### GFR-05

A terminal outcome contract dominates component PASS receipts.

Enforcement: Aggregate completion is false until the required terminal receipt validates and its observed effects, prohibited effects, final postimage, and successor state satisfy the frozen terminal predicate.

### GFR-06

Bounded means the smallest complete vertical slice.

Enforcement: A slice is bounded only if it crosses every required real consumer and reaches the promised terminal boundary without adding unrelated targets, authority, risk, or effects.

### GFR-07

Preparation is not authority.

Enforcement: Compilation, rehearsal, freeze, review, and request emission must state authority_effect none and keep selection, admission, execution, publication, deployment, and external effects false.

### GFR-08

Models provide schema-valid machine views; human views are deterministic projections.

Enforcement: Reject the source before rendering when schema validation fails; render only from the validated machine graph and bind source digest, graph digest, renderer digest, and visibility policy.

### GFR-09

The evidence chain is monotonic: source to graph to rehearsal to freeze to review to request to acceptance to execution.

Enforcement: Each descendant binds the exact predecessor digest; source or decision-envelope mutation invalidates all descendants and no receipt may rebind backward to different bytes.

### GFR-10

Retry policy distinguishes environmental, mechanical evidence-only, and semantic or authority changes.

Enforcement: Apply machine predicates over target-byte, decision-envelope, executable-authority, evidence, and environment digests; never infer the retry class from prose.

### GFR-11

A governance-only sidecar auto-resumes its suspended chain after a passing repair.

Enforcement: Resume exactly once at the recorded continuation point only when repair review passes, decision and target digests are unchanged, the defect is mechanical evidence-only, and no authority-bearing executable changed.

### GFR-12

Exact-byte, owner, risk, authority, privacy, publication, Git, deployment, external-effect, and independent-review protections remain intact.

Enforcement: Keep these fields inside the immutable decision envelope and require a new graph and decision whenever any one changes.

## Three-mode contract

| Mode | Effect ceiling | Stop | Continuation | Completion |
| --- | --- | --- | --- | --- |
| preacceptance_no_effect | Isolated run-local evidence only; zero repository-target, selection, admission, publication, deployment, credential, external-system, or successor effects. | Do not stop on an ordinary reachable validation failure; record it and continue. Stop only when safe evaluation itself is impossible or a semantic or authority decision is required. | Automatically rerun bounded environmental and mechanical evidence-only repairs while retry budget and graph identity remain valid. | Complete only when all required checks are pass, no check is not_evaluable, blocker set is empty, two-run evidence is byte-stable, and protected inputs are unchanged. |
| human_decision | One idempotent owner request for one frozen decision graph; no selection, admission, or execution. | Stop immediately after returning the one request or its existing idempotent identity. | Continue only from an explicit owner response bound to that request; revisions create a new graph. | Mode closes with exact accept or reject evidence; absence of a response remains pending, not failed. |
| effectful_execution | Exactly the accepted, selected, and admitted target, write, executable, risk, and external-effect envelope. | Fail fast at the first effectful failure or governance blocker and prove later effects did not run. | Resume only through a passing governance-only sidecar predicate or a new admitted graph after semantic or authority change. | Complete only when the promised terminal receipt validates and its terminal predicate is true. |

## Immutable decision graph

The immutable owner decision graph is the normalized, schema-valid envelope of exact target bytes and all fields whose change can alter owner intent, authority, risk, privacy, publication, deployment, external effects, executable authority, or the promised terminal outcome.

Included fields:

- exact target postimages and baselines
- owner and lifecycle route
- authority and write ceilings
- risk and request budget
- public/private and publication class
- deployment, credential, destructive, and external-effect policy
- authority-bearing executable path, digest, argv, mode, cwd, and environment allowlist
- terminal outcome contract
- admitted frontier, route, selection, and successor policy

Excluded non-authoritative descendants:

- non-authoritative run identifiers and timestamps
- mechanical evidence receipts whose replacement proves the decision graph and target-byte digests unchanged

- Freeze rule: Freeze only after a complete zero-blocker rehearsal; record graph digest and exact rehearsal predecessor without allowing later graph mutation.
- Request rule: Persist request identity by decision_graph_digest and enforce request_count <= 1; retries return the same bytes and prompt identity.
- Descendant rule: Rehearsal, freeze, review, request, acceptance, execution, sidecar, and terminal receipts bind predecessor digests. A decision-envelope or target-byte change invalidates descendants and requires a new graph.

## Terminal outcome contract

The aggregate result is incomplete or blocked unless the terminal predicate is true, even when every local component receipt reports PASS.

- `promised_boundary_id`
- `required_terminal_receipt_path_and_schema`
- `required_effects_and_exact_postimages`
- `prohibited_effects_and_successors`
- `completion_predicate`
- `authority_and_write_ceiling`
- `terminal_observer_identity`

- Local PASS: Component PASS means only that component's bounded claim succeeded; it never synthesizes terminal completion.
- Bounded: The smallest complete vertical slice that traverses every required real consumer and can satisfy the promised terminal predicate without unrelated scope.

## Retry and sidecar resumption

| Class | Predicate | Action | Graph | Prompt |
| --- | --- | --- | --- | --- |
| environmental | Decision graph, target bytes, semantic inputs, authority-bearing executable, and required evidence schema are unchanged; failure is attributable to a declared transient runtime condition. | Retry automatically within an explicit budget and record every attempt; exhaustion blocks without an owner prompt. | Preserve the same graph and descendants that remain exact. | none |
| mechanical_evidence_only | Repair changes only validator, wrapper, locator, receipt consistency, formatting, or run-local evidence mechanics and proves the decision graph, target-byte, semantic, authority, risk, privacy, publication, deployment, external-effect, and authority-bearing executable digests unchanged. | Run one bounded governance sidecar, independently review the repair, revalidate the suspended edge, and auto-resume once from its recorded continuation point. | Preserve the accepted decision graph; append exact repair and resume receipts. | none |
| semantic_or_authority | Any target byte, terminal effect, owner, route, risk, write, privacy, publication, deployment, credential, external-effect, successor, or authority-bearing executable identity changes. | Stop, supersede the old chain, compile and rehearse a new graph, independently review it, and request one new owner decision. | New decision_graph_digest required; old acceptance cannot be reused. | exactly one for the new immutable graph |

- Suspend: Capture the failed stage, first nonzero status, complete diagnostics, accepted decision_graph_digest, target_byte_digest, predecessor receipt, and exact continuation point before repair.
- Repair ceiling: The sidecar may change only separately staged mechanical evidence or already-authorized validator/workflow tests; it may not change accepted target bytes, semantics, authority, promotion, publication, deployment, credentials, external effects, or authority-bearing executable identity.
- Resume predicate: `repair_classification == mechanical_evidence_only AND repair_review == pass AND decision_graph_digest unchanged AND target_byte_digest unchanged AND revalidation == pass AND resume_count == 0`
- Do not resume when:

  - repair review fails or is missing
  - decision graph or target-byte digest changes
  - semantic, owner, risk, authority, privacy, publication, deployment, external-effect, or executable-authority boundary changes
  - resume already consumed

## Success metrics

| Metric | Definition | Target | Event |
| --- | --- | --- | --- |
| postacceptance_consumer_defects | Count of deterministic consumer-contract defects first discovered after acceptance for a graph when the responsible consumer was declared or required preacceptance. | 0 | governance_flow.consumer_defect.v1 |
| prompts_per_immutable_graph | Owner decision prompts emitted divided by immutable decision graphs that reached human-decision mode; each such graph must have exactly one prompt identity and at most one presentation. | 1 | governance_flow.owner_prompt.v1 |
| unchanged_byte_approval_retries | Count of new owner request identities emitted after a prior request when both decision-envelope digest and exact target-byte digest are unchanged. | 0 | governance_flow.request_retry.v1 |
| blockers_discovered_after_request | Count of governance blockers first observed after request emission that the declared deterministic no-effect consumers could have discovered before request. | 0 | governance_flow.late_blocker.v1 |
| manual_receipt_transfers | Count of receipt edges requiring a human to copy, rewrite, translate, or manually relocate machine evidence between declared consumers. | 0 | governance_flow.receipt_transfer.v1 |

## Exact changed-path proposal

### Current non-overlapping package

Apply now: `true`

- `ops/development/2026-08-25-governance-flow-revision/governance-flow-revision.schema.yml`
- `ops/development/2026-08-25-governance-flow-revision/GOVERNANCE-FLOW-REVISION.yml`
- `ops/development/2026-08-25-governance-flow-revision/materialize_revision.py`
- `ops/development/2026-08-25-governance-flow-revision/GOVERNANCE-FLOW-REVISION.md`
- `ops/development/2026-08-25-governance-flow-revision/AGENTS-PATCH-PROPOSAL.diff`
- `ops/development/2026-08-25-governance-flow-revision/VALIDATION-RECEIPT.yml`

Non-overlapping private design package only. The YAML source is durable schema-valid proposal material; the derived YAML receipt is a durable proposal-package validation artifact, not run-local telemetry. No current governance runtime or canonical source mutation.

### Later root policy

Apply now: `false`

- `AGENTS.md`

Add the three-mode choreography and amend the governance-only sidecar with deterministic auto-resume and collect-all preacceptance semantics using the derived exact patch proposal.

### Later canonical public contract and tests

Apply now: `false`

- `arcanum/framework/GOVERNANCE-FLOW-CONTRACT.md`
- `arcanum/framework/README.md`
- `arcanum/framework/CYBERALCHEMY-METHOD.md`
- `arcanum/framework/QUALITY-BAR.md`
- `arcanum/framework/OUTCOME-BRIEF-CONTRACT.md`
- `arcanum/framework/governance-flow/schemas/governance-flow-source-v1.schema.yml`
- `arcanum/framework/governance-flow/schemas/governance-flow-graph-v1.schema.yml`
- `arcanum/framework/governance-flow/schemas/governance-flow-stage-receipt-v1.schema.yml`
- `arcanum/framework/governance-flow/schemas/governance-flow-owner-request-v1.schema.yml`
- `arcanum/framework/governance-flow/scripts/compile_governance_flow.py`
- `arcanum/framework/governance-flow/scripts/render_governance_flow.py`
- `arcanum/framework/governance-flow/scripts/run_governance_flow.py`
- `arcanum/framework/governance-flow/development/run-validation-fixtures.sh`
- `arcanum/framework/governance-flow/development/test_governance_flow.py`
- `arcanum/framework/governance-flow/development/fixtures/positive/terminal-boundary-source.json`
- `arcanum/framework/governance-flow/development/fixtures/positive/terminal-boundary-executor.py`
- `arcanum/framework/governance-flow/development/fixtures/positive/expected-human-view.md`
- `arcanum/framework/governance-flow/development/fixtures/positive/expected-terminal-receipt.json`
- `arcanum/framework/governance-flow/development/fixtures/negative-cases.json`

Create the public, project-agnostic contract, machine schemas, deterministic compiler/renderer/runner, positive end-to-end terminal fixture, and negative regression suite.

### Later adapters after the MVLR concurrency edge closes

Apply now: `false`

- `arcanum/spells/invoke/README.md`
- `arcanum/spells/invoke/preacceptance-closure.md`
- `arcanum/spells/invoke/schemas/preacceptance-closure-manifest-v1.schema.json`
- `arcanum/spells/invoke/schemas/preacceptance-closure-receipt-v1.schema.json`
- `arcanum/spells/invoke/schemas/owner-acceptance-request-v2.schema.json`
- `arcanum/spells/invoke/scripts/preacceptance_closure.py`
- `arcanum/spells/invoke/development/preacceptance-closure/test_preacceptance_closure.py`
- `arcanum/spells/invoke/development/run-preacceptance-closure-fixtures.sh`
- `arcanum/arcana/task-session/SKILL.md`
- `arcanum/arcana/task-session/README.md`
- `arcanum/arcana/task-session/scripts/task-session-governance-runner.py`
- `arcanum/arcana/task-session/development/run-validation-fixtures.sh`
- `arcanum/arcana/task-session/development/test_governance_flow_execution.py`
- `arcanum/transmutations/context-builder/SKILL.md`
- `arcanum/transmutations/context-builder/README.md`
- `arcanum/transmutations/context-builder/scripts/compile_native_context_projection.py`
- `arcanum/transmutations/context-builder/development/test_native_context_projection.py`

Adapt existing request emission, machine/human projection, execution fail-fast behavior, terminal verification, and sidecar resumption only after the active MVLR work is frozen and independently re-inventoried.

Generated surface policy: Do not hand-edit generated packages. After canonical adapter changes pass and only with separate authorization, run package-specific sync for each changed sigil/spell, inventory exact generated outputs, validate parity, and independently review privacy markers before any publication step.

The exact proposed root-policy diff is in `AGENTS-PATCH-PROPOSAL.diff`; it is not applied.

## Compatibility impact

| Surface | Impact |
| --- | --- |
| existing accepted records | Remain readable historical evidence and keep their original authority. They are not retroactively promoted into governance-flow v1 closure or reinterpreted as request-ready. |
| new or regenerated owner requests | Require a schema-valid decision graph, complete collect-all rehearsal, freeze, independent review, and idempotent request record before presentation. |
| legacy split projections | Need an explicit adapter that composes one machine graph and proves field equality or subset relations; prose cannot repair stale machine arrays. |
| validators and wrappers | Preacceptance wrappers change from early exit to run-all-reachable while preserving the first nonzero. Effectful runners retain fail-fast semantics. |
| human-facing documents | Human views become derived outputs with source, graph, and renderer digests; hand-authored views are non-authoritative and cannot be request inputs. |
| sidecar repairs | Mechanical evidence-only repairs can resume without a new owner prompt only when machine predicates prove the decision graph and target bytes unchanged. Semantic or authority repair still requires a new graph. |
| public/private boundary | The public contract is project-agnostic and contains no private project prose, paths, examples, or identifiers. Private adapters and evidence remain outside Arcanum. |
| generated packages | No generated bytes change in this stage. Later changes are regenerated from canonical sources and independently inventoried, never hand-edited. |

## Migration plan

| Phase | Action | Gate | Authority effect |
| --- | --- | --- | --- |
| M0-proposal | Materialize and validate this non-overlapping design package; preserve the active MVLR and dirty-worktree bytes. | Only the six package paths change; all forbidden paths remain byte-identical. | none |
| M1-owner-selection | After the active MVLR chain is closed or handed off, rehash live target files and ask the owner to accept, revise, or reject the exact root/public change set and decision-envelope boundary. | Explicit owner decision over the refreshed proposal; no older digest is stretched over new bytes. | proposal selection only |
| M2-framework-vertical | Implement the framework contract, YAML schemas, deterministic compiler, renderer, runner, metrics events, one positive terminal fixture, and the full negative matrix in one smallest complete public vertical. | The positive fixture reaches its promised terminal boundary and every negative case fails at its intended boundary. | public candidate bytes only |
| M3-root-policy | Apply the exact AGENTS patch rebased onto the live file without disturbing the existing publication-policy change. | Patch check passes, policy statements do not conflict, and root diff contains only the proposed choreography changes plus pre-existing bytes. | repository-local instruction change |
| M4-adapters | Adapt Invoke, Task Session, and Context Builder only after their concurrent MVLR changes are frozen; preserve their current exact-byte and authority contracts while routing them through the framework graph. | Rebased exact inventory, all existing suites, new cross-capability terminal fixture, public privacy scan, and independent review pass. | canonical public candidate bytes; no execution authority |
| M5-generated-parity | Regenerate only the packages owned by the changed canonical capabilities and validate source/generated parity. | Exact generated inventory, zero unexplained files, zero private markers, all validation suites pass. | generated candidate bytes only |
| M6-enforcement-and-observation | Enable the new gate for new request versions, keep legacy records historical, emit the five metric events, and observe a bounded rollout before broader adoption. | Positive terminal fixture remains green and observed metrics meet targets; failures do not downgrade safeguards. | enforcement only after separate acceptance; no publication or deployment authority |

## Regression matrix

| Case | Polarity | Assertion |
| --- | --- | --- |
| P01-TERMINAL-VERTICAL | positive | One schema-valid source compiles, renders byte-stably, rehearses every real fixture consumer, freezes, reviews, emits one request, consumes fixture acceptance, executes in an isolated root, and reaches the promised terminal receipt with no successor. |
| N01-INVALID-MACHINE-SOURCE | negative | A schema-invalid model source emits no graph, human view, rehearsal, or owner request. |
| N02-HUMAN-VIEW-DRIFT | negative | A hand-edited human view or renderer/source digest mismatch is rejected and cannot influence authority. |
| N03-MULTI-BLOCKER-COLLECT | negative | At least three independent preacceptance failures are all reported, later checks run, and process exit preserves the first nonzero. |
| N04-NOT-EVALUABLE-CAUSALITY | negative | A dependency-blocked consumer is marked not_evaluable with exact causal blockers, never PASS or omitted. |
| N05-PREPARATION-NO-AUTHORITY | negative | Compilation, rehearsal, freeze, review, and request evidence cannot set selection, admission, execution, publication, deployment, or external-effect permissions. |
| N06-STALE-DESCENDANT | negative | Any source or decision-envelope mutation invalidates rehearsal, freeze, review, request, acceptance, and execution descendants. |
| N07-DUPLICATE-REQUEST | negative | A second emission attempt for the same decision_graph_digest returns the original request identity and bytes and creates no second prompt event. |
| N08-MISSING-REVIEW | negative | Missing, stale, non-independent, or non-passing review blocks request emission. |
| N09-LOCAL-PASS-NO-TERMINAL | negative | All component receipts may PASS but aggregate completion remains false when the required terminal receipt is missing. |
| N10-WRONG-TERMINAL | negative | A schema-valid terminal receipt with the wrong boundary, postimage, effect, or successor state fails completion. |
| N11-EFFECTFUL-FAIL-FAST | negative | The first effectful failure stops execution and proves no later effect or successor ran. |
| N12-ENVIRONMENTAL-RETRY | negative | A declared environmental failure retries within budget without graph change or owner prompt; exhaustion blocks. |
| N13-MECHANICAL-AUTO-RESUME | negative | A passing independently reviewed evidence-only repair with unchanged decision and target digests consumes one resume token and resumes the suspended stage without a prompt. |
| N14-SIDECAR-NO-RESUME | negative | Failed review, changed decision or target digest, changed authority-bearing executable, or a consumed resume token leaves the chain suspended. |
| N15-SEMANTIC-NEW-GRAPH | negative | A semantic, owner, risk, authority, write, privacy, publication, deployment, external-effect, successor, or executable-authority change requires a new graph and forbids auto-resume. |
| N16-EXACT-BYTE-ACCEPTANCE | negative | A changed target-byte digest rejects the old acceptance even when prose and path names are unchanged. |
| N17-MANUAL-RECEIPT-TRANSFER | negative | A consumer that requires manual copying, path translation, or prose extraction fails the automatic receipt-edge contract and increments the manual-transfer metric. |
| N18-LATE-DISCOVERABLE-BLOCKER | negative | A governance blocker introduced after request that a declared preacceptance consumer could detect fails the blocker-timing metric. |
| N19-PRIVATE-MARKER-PUBLIC | negative | Private project identifiers, paths, prose, or authority names in proposed public additions fail the privacy scan. |
| N20-GRAPH-WIDENING | negative | A derived graph or human view that widens target, owner, risk, write, publication, deployment, external-effect, or successor scope relative to the source fails. |
| N21-BOUNDLESS-SLICE | negative | A small task that does not traverse every required consumer or cannot reach its terminal predicate is not considered bounded or complete. |

## Positive terminal-boundary fixture

- Source: `arcanum/framework/governance-flow/development/fixtures/positive/terminal-boundary-source.json`
- Executor: `arcanum/framework/governance-flow/development/fixtures/positive/terminal-boundary-executor.py`
- Promised boundary: An isolated fixture output reaches its exact accepted postimage, a schema-valid terminal receipt records complete, protected inputs remain unchanged, and no successor or external effect occurs.

Steps:

1. validate one model-produced machine source
1. compile one normalized decision graph
1. render the human view twice and compare exact bytes
1. run every declared consumer in collect-all isolated rehearsal
1. freeze the zero-blocker graph
1. independently review the graph and full rehearsal
1. emit one idempotent fixture owner request and prove the second call returns the same request
1. consume one exact fixture acceptance after proving selection, admission, and execution were previously false
1. select and admit the sandboxed fixture executor
1. execute the allowed local effect and fail fast on any error
1. validate the terminal receipt and exact postimage
1. assert aggregate completion from the terminal predicate and prove no successor ran

Required assertions:

- source, graph, renderer, rehearsal, freeze, review, request, acceptance, execution, and terminal digests form one monotonic chain
- human output is byte-identical across two renders
- all required consumers were evaluated
- preacceptance blocker set is empty
- preacceptance protected-input before and after digests are equal
- preacceptance created only declared run-local evidence
- request count for the graph is one
- prompt event count for the graph is one
- no selection, admission, or execution precedes acceptance
- execution writes only the accepted sandboxed target
- terminal receipt matches the promised boundary and exact postimage
- no prohibited effect, external call, or successor execution occurs
- a paired all-local-PASS but missing-terminal variant fails aggregate completion
- all five metric values satisfy their targets for the fixture run

## Owner decision surface

- Decision: `GFR-DECISION-ENVELOPE-001`
- Remains: `false`
- Status: `selected`
- Selected: `A` — Immutable decision-envelope graph
- Selected at: `2026-08-25T21:40:40Z`
- Selection source: `direct_user_selection` response `A`
- Decision effect: `design-binding-selected`
- Selection rationale: The owner selected the recommended boundary that binds every consequential and exact-byte field in one immutable decision graph while allowing independently reviewed mechanical evidence-only descendants to be replaced only when graph and target digests remain unchanged.
- Question: Should owner acceptance bind the immutable decision graph while independently reviewed mechanical evidence remains a digest-bound descendant, or bind every replaceable evidence receipt into the owner digest?
- Recommendation: Bind acceptance to the immutable decision graph: exact target bytes, terminal outcome, owner, authority, risk, writes, privacy, publication, deployment, external-effect scope, successor policy, and authority-bearing executable identity. Require exact independent review of evidence, but allow a mechanical evidence-only descendant to be replaced and auto-resumed only after machine proof that the decision graph and target-byte digests are unchanged.

- recommended decision-envelope graph: Preserves every consequential and exact-byte safeguard while preventing validator or receipt-only repairs from manufacturing another owner prompt.
- entire evidence graph: Stronger byte coupling but mechanically guarantees renewed approval whenever a non-authoritative receipt or validator evidence changes, recreating the loop this revision is intended to remove.
- high-level intent only: Rejected because it would not bind exact target bytes, executable authority, or risk/write/effect ceilings and would weaken existing protections.

- Admissibility request digest: `3835a581e114044c4df5b35c2b5c456013cf8b4792121fa06f44501fba0911b4`
- Admissible options: `A, B`
- Decision Gate blockers remaining: `0`
- Downstream gates:

  - active MVLR work must release the protected adapter surfaces
  - the refreshed exact root and public candidate requires separate explicit apply authorization
  - the end-to-end positive fixture must be implemented and reach its promised terminal boundary before completion

Apply boundary: Selection A resolves only the decision-graph binding model. It does not authorize applying AGENTS.md, canonical public contracts, adapters, generated packages, Git changes, publication, deployment, or external effects; those remain blocked until the active MVLR task releases the protected surfaces and the owner separately authorizes the refreshed exact change set.

## Background helper receipt

- Helper: `/root/governance_flow_challenge`
- Status: `joined`
- Writes: `none`
- Material challenge adopted into this proposal: Define no-effect as run-local evidence only, represent dependency-blocked checks as not_evaluable, distinguish the immutable decision graph from replaceable evidence descendants, make one-request idempotency persistent, and require an actual sandboxed positive fixture to reach the promised terminal boundary.
- Claim ceiling: Read-only design challenge based on the named five-file evidence set; no implementation, adoption, metric achievement, or execution claim.

## Governance sidecar receipts

- `format-aware-diff-whitespace` via `/root/gfr_whitespace_sidecar`: The first package hygiene check was format-blind and treated the required single-space prefix for an unchanged empty unified-diff context record as trailing content whitespace; the package bytes were not malformed. Permanent fix: Parse unified-diff hunk records, allow exactly one space only for an empty context record, reject real trailing whitespace everywhere else, and preserve the first nonzero across the complete validation suite.
- `ignored-machine-artifact-visibility` via `/root/gfr_whitespace_sidecar`: The repository intentionally ignores ops/development JSON machine proof, so the JSON source and receipt existed but were not durable Git-visible candidates in the declared six-path package. Permanent fix: Use schema-valid YAML for the durable proposal source and its derived proposal-package validation receipt; classify the receipt as durable proposal validation rather than run-local telemetry, and reject force-add or shared .gitignore exceptions.
- `check-ignore-exit-classification` via `/root/gfr_whitespace_sidecar`: A multi-path `git check-ignore -q` invocation returned usage error 129, and the aggregator incorrectly treated every nonzero as the expected no-match status 1. Permanent fix: Run multi-path `git check-ignore --no-index` without quiet mode and branch explicitly on status 0 ignored, status 1 with empty stdout unignored, and every other status validator_error; preserve stderr and the original status.

## Current lifecycle status

The exact design, paths, compatibility, migration, regression matrix, and positive terminal-boundary fixture are specified and machine-validated, but no canonical contract, adapter, or terminal fixture has been implemented or run.

This package is proposal-ready, not implementation-complete.
