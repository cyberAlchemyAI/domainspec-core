# Context Pack: DomainSpec v2 Remaining Meta-Type Implementations

## Control metadata

- Pack ID: `WP-RMT-002-META-TYPE-IMPLEMENTATIONS`
- Source Work Pack: `WP-RMT-002`
- Mode: explicit full-stream one-shot
- Status: `live-selected; context-ready; mutation-admission-pending`
- Exact order: `OP -> RULE -> IFACE -> MAP -> EVENT -> SM -> WF`, ten SWUs per type
- Current selected unit: `RMT-OP-001`
- Plan epoch: `epoch-2cd4b2d98d05cb62ea719a74`
- Runtime owner: native Codex Goal
- Selection owner: `implementation-readiness:execute`
- Execution owner: one fresh Task Session per selected SWU
- Authority effect: none
- Decision profile: none
- Subagents: not authorized by this profile

## Outcome and evidence ceiling

Finish bounded native TypeScript, Python, and Rust candidate implementations for Operation, Rule, Interface, Mapping, Event, State Machine, and Workflow. Each type crosses admission, hostile-family, TypeScript, Python, Rust, parity, fresh-process replay, REL-A relation, canonical-registry-negative, and candidate-projection gates.

Completion requires 70 exact passing terminal receipts and a fresh whole-stream audit. The maximum result is candidate-local implementation and proof evidence. It is not ontology admission, a PromotionRecord, authority, canonical registry membership, promotion, publication, release, deployment, production readiness, or cross-language native byte equality.

## Current live state

- The exact accepted refresh is live. `LIVE-APPLY-RECEIPT.json` is `pass`; 33/33 postimages match, seven of seven post-apply commands passed, public/private material packages remained partitioned, and no implementation SWU was selected or executed by that apply.
- The fresh readiness audit is `pass` / `PLAN_SEMANTIC_READY`, has no blockers or flags, reports no source-snapshot drift, and names `implementation-readiness:execute` as next owner. It deliberately executed no product commands and kept `mutation_ready: false`, `selected_unit: null` at the audit ceiling.
- The live selection receipt then selects only `RMT-OP-001` with `SELECTION_READY`, no reasons, authority none, unit-contract digest `fbb88dbf86d74616c627705c7727a634a59fc9282dfb48699338d242dcb310af`, and `mutationReady: false`.
- The context-ready outer-loop state is `phase: ready`, `steps_used: 0`, current route `task-session:rmt-op-001`, selected unit `RMT-OP-001`, and no pending Task Session. Its captured sequence contains all 70 units in the required order.
- `mutationReady: false` is intentional at this boundary. Selection permits the native Goal to start the fresh Task Session; it does not permit material writes. Task Session owns selected-unit context construction, material-package binding, mutation admission, execution, and the terminal receipt.
- The config-normalization sidecar is governance-only. It repaired only a derived run-local allowed-routes digest, changed no accepted/live plan or product semantics, and the required re-audit passed. It grants no selection or mutation authority.

## Exact bound sources

Runtime must use these repository-relative paths and exact SHA-256 values. Any drift blocks the affected edge and requires a named-gap refresh.

| Source | SHA-256 | Role |
|---|---|---|
| `projects/domainspec-v2/development/remaining-meta-types/readiness/20260820T173252Z-wp-rmt-002-live-post-refresh/audit-config.json` | `521c4dcfc5077d22ca5435164b28060007c400b791622299ee4412d254c62399` | Live normalized audit configuration |
| `projects/domainspec-v2/development/remaining-meta-types/readiness/20260820T173252Z-wp-rmt-002-live-post-refresh/audit-2/work-pack-readiness-report-v2.json` | `7f8933c6c5ce32cb462fa5f45293686f2c846d3c70445997cbe4f79c641a47b6` | Fresh semantic-readiness verdict |
| `projects/domainspec-v2/development/remaining-meta-types/readiness/20260820T173252Z-wp-rmt-002-live-post-refresh/audit-2/plan-semantic-manifest.json` | `919e51c82bcabde5490cdb7da98d533325dc2ed32b24f78bc34bf16703b27631` | Plan epoch and 70 contract digests |
| `projects/domainspec-v2/development/remaining-meta-types/readiness/20260820T173252Z-wp-rmt-002-live-post-refresh/CONFIG-NORMALIZATION-SIDECAR.json` | `6924da49f1b6615253185c0bae58262318290b4337bed8f5167aa6bb66cc06f3` | Governance-only normalization disposition |
| `projects/domainspec-v2/development/remaining-meta-types/readiness/20260820T173252Z-wp-rmt-002-live-post-refresh/execution/execution-policy.json` | `ca0f7eaa70278a6b6571dd5d97fe767884f56063d4e1890a05023d98e93e0c9a` | Finite route, stop, and validation policy |
| `projects/domainspec-v2/development/remaining-meta-types/readiness/20260820T173252Z-wp-rmt-002-live-post-refresh/execution/outer-loop-state-context-ready.json` | `fb223cb173d7aca800a0736b7113790ab69094ee615088f300050d55199c94cc` | Context-ready current binding |
| `projects/domainspec-v2/development/remaining-meta-types/readiness/20260820T173252Z-wp-rmt-002-live-post-refresh/execution/selection-request.json` | `5e3ab3484be7df8fe00931e173b8f366ea34c1bd20c7dbb5ce841fb8ad7bcab2` | Explicit RMT-OP-001 selection request |
| `projects/domainspec-v2/development/remaining-meta-types/readiness/20260820T173252Z-wp-rmt-002-live-post-refresh/execution/selection-receipt.json` | `93f2397800902dd3a3057a84b3779ce2a0a446955b674a88119c791c9b27e6e5` | Live selection receipt |
| `projects/domainspec-v2/development/architecture-pattern-enforcement/refreshes/20260820T171212Z-wp-rmt-002-task-session-api-live-apply/LIVE-APPLY-RECEIPT.json` | `53eaaa0666b0e7328c69fa11746f08a6d02c759ebafe900e0d3866c6808d76e2` | Accepted-byte live apply and validation |
| `projects/domainspec-v2/development/refinement-runs/20260814T193343Z-active-meta-type-implementations/stages/09-invoke-plan/WORK-PACK.md` | `e96b5d414279fdd7ad1689bcac70e9292adbbae588a8705e1bb73b2174f7ef37` | Outcome, lifecycle, graph, and claim ceiling |
| `projects/domainspec-v2/development/refinement-runs/20260814T193343Z-active-meta-type-implementations/stages/09-invoke-plan/tasks/TASK-RMT-OP.md` | `5297b49cbf8344d66699e02a3fe3b47eb074648a4a63146042ca74853f0365d1` | Current Operation semantics and minimum acceptance |
| `projects/domainspec-v2/development/refinement-runs/20260814T193343Z-active-meta-type-implementations/stages/09-invoke-plan/SWU-MANIFEST.json` | `c7e8129bc72c447acbc4062c740ed3019b41c2f4e273016ea965c1751d83e9d0` | Canonical 70-unit order and 74-edge graph |
| `projects/domainspec-v2/development/refinement-runs/20260814T193343Z-active-meta-type-implementations/stages/09-invoke-plan/SWU-CONTRACTS.json` | `089f52e39a2e4ba01ff056e1368a1c98226e5788870b93f6dd5983d18aa588b2` | Atomic scopes, commands, receipts, and closeout |
| `projects/domainspec-v2/development/refinement-runs/20260814T193343Z-active-meta-type-implementations/stages/09-invoke-plan/WRITE-SCOPE-BASELINE.json` | `990ffc79aaf16bbf1beb563a2eadbe8699aeaaabec9a6373a24d70e64b79a767` | 189 planned paths and exact owners |
| `projects/domainspec-v2/development/refinement-runs/20260814T193343Z-active-meta-type-implementations/stages/09-invoke-plan/HOSTILE-CATALOGUE.json` | `961b39276e9290f85d275b2f5ff0872ce09ca6ba39338c914387ecc3bbab73ec` | 98 executable hostile controls |
| `projects/domainspec-v2/development/refinement-runs/20260814T193343Z-active-meta-type-implementations/stages/09-invoke-plan/RELATION-CONTRACTS.json` | `a2537eb3f233aa65f51c2cd8892be284b6ac2ba7b849060fbc9137978643cd0c` | 18 REL-A translations and endpoint rules |

## Closed order and per-type cycle

Execute exactly:

1. `RMT-OP-001..010`
2. `RMT-RULE-001..010`
3. `RMT-IFACE-001..010`
4. `RMT-MAP-001..010`
5. `RMT-EVENT-001..010`
6. `RMT-SM-001..010`
7. `RMT-WF-001..010`

Within every type, the suffixes mean: `001` admission, `002` hostiles, `003` TypeScript, `004` Python, `005` Rust, `006` normalized parity, `007` fresh-process replay, `008` REL-A relations or deferred blueprints, `009` canonical-registry non-membership, and `010` candidate projection. Manifest dependencies remain semantic authority; array order supplies the deterministic one-shot successor and deliberately serializes wave peers.

## Current selected-unit contract

`RMT-OP-001` binds the active Operation row, criterion schema, read-only Operation/W3 precedent inventory, target forms, proof denominator, and authority-none ceiling.

- Exact allowed write partition: material directory `projects/domainspec-v2/development/remaining-meta-types/active-types/operation/admission/` plus durable execution output `projects/domainspec-v2/development/remaining-meta-types/active-types/operation/admission/RECEIPT.json`.
- Baseline: the material directory was captured absent and is owned only by `RMT-OP-001`; Task Session must revalidate current state before admission.
- Material producer: `task-session:selected-unit-materialization`; package state remains pending until the fresh Task Session binds it.
- Acceptance: exact active row, exact criterion schema, exact read-only precedent inventory, declared target forms, declared proof denominator, and authority none.
- Declared validation: `node projects/domainspec-v2/development/remaining-meta-types/active-types/operation/admission/validate-admission.mjs "$PWD"`; timeout 120 seconds; maximum output 1 MiB; runtime executable/version/hash captured before run.
- Verification: exact input rehash, focused-before-broad execution, preserved failure status, exact output inventory, independent read-only audit, lifecycle-owner pass, no undeclared delta, and terminal receipt written last.
- Successor: `RMT-OP-002`, only after the live `RMT-OP-001` receipt is `pass` and hashes match.

## Per-unit execution algorithm

1. Rehash this Markdown pack, its JSON index, and every exact bound source.
2. Confirm the current Implementation Readiness selection. For the first iteration it must be the bound `RMT-OP-001` receipt above.
3. Start one fresh Task Session for only that unit. Bind the exact manifest row, unit-contract digest, source inputs, current path baseline, runtime identities, write partition, and expected terminal receipt.
4. Let Task Session construct the selected-unit context and material package, then require a passing mutation-admission receipt before any material write. Selection `mutationReady: false` never authorizes a write.
5. Execute only the admitted materialization and declared commands. Preserve the first failure; remove declared transient outputs; prove no undeclared delta; run the required independent read-only audit; validate through the lifecycle owner; write the terminal receipt last.
6. Accept only a `pass` receipt bound to live hashes and authority none. Recompute the canonical successor plus dependencies, obtain a fresh Implementation Readiness selection, and start a new Task Session. Never reuse a Task Session across SWUs or pre-admit a later unit.
7. Stop on any failure. Do not skip the unit, infer a successor, rewrite the immutable manifest, or widen scope.

## Capability and fallback policy

- Allowed: native Goal continuation; Implementation Readiness for exact next-unit selection; one fresh Task Session per unit.
- Stop/report only: `decision-gate` for a blocker-level human decision.
- Named-gap only: `invoke:refresh` for an explicitly missing or drifted source, scope, contract, or handoff. A refresh candidate is not authority to apply it.
- Not authorized: subagents, ambient `refine`, `craft` mutation, Git mutation, network, dependency installation, publication, promotion, deployment, or scope expansion.
- Pack-first context is mandatory. Extra exploration is allowed only for a named uncovered obligation. The final report must name the gap, every extra source, and whether it changed the result.

## Strict Markdown coverage

| Obligation | Status | Coverage |
|---|---|---|
| Explicit one-shot selection | covered | 70-unit stream and exact type order |
| Current live selection | covered | `RMT-OP-001`, selection receipt and outer-loop binding |
| Mutation gate | covered | selection-only `mutationReady: false`; Task Session admission required before writes |
| Dependencies and successor | covered | manifest graph plus array-order successor |
| Per-type semantics | covered | Work Pack, current Operation task card, manifest type contracts |
| Selected-unit scope | covered | OP-001 contract and write baseline |
| Whole-stream write scope | covered | 189 paths, one owner per path |
| Done criteria and receipts | covered | 70 atomic contracts and terminal-receipt rules |
| Validation | covered | exact selected command plus 112 stream commands |
| Hostile controls | covered | 98 exact executable controls |
| Relation contracts | covered | 18 REL-A translations and deferred-blueprint fallback |
| Capability policy | covered | allowed, stop-only, named-gap-only, and forbidden lanes |
| Fallback exploration | covered | named uncovered obligations only |
| Extra-source reporting | covered | gap, source, and result impact required |
| Stop conditions | covered | drift, admission, validation, receipt, human, effect, and scope boundaries |
| Claim ceiling | covered | candidate-local evidence; authority none |

The structured `coverageMatrix` in `context-index.json` carries these same 16 obligation IDs and statuses. Strict Markdown and JSON coverage therefore pass together.

## Whole-stream completion and stop conditions

Complete only when a fresh audit proves 70/70 exact passing terminal receipts, all declared language/parity/replay/hostile/relation/registry-negative/candidate gates, all 189 owned paths reconciled, all transients absent, no undeclared delta, protected precedent unchanged except through an accepted refresh, and authority none.

Stop before mutation if Task Session materialization or mutation admission is missing. Stop thereafter on any source/hash/semantic drift, no or multiple valid next units, failed command or lifecycle validation, invalid or missing terminal receipt, undeclared/shared-source pressure, product or semantic choice, destructive or irreversible effect, credential or secret need, network/external effect, Git mutation, cost/risk decision, or authority/promotion/publication/deployment pressure. Preserve the safe state and report the exact unblock owner and evidence needed.
