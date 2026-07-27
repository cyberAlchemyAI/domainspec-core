# Invoke Lifecycle Churn Findings

## Goal

Specify the smallest falsifiable repair for repeated Invoke Plan → Task Session → Refresh cycling without weakening exact-byte admission, broadening Task Session beyond one SWU, or converting Arcanum into a workflow platform.

**Verdict: CANDIDATE only.** DS-SFOL is direct causal evidence for the observed loop; BTE is corroborating but not identical. There is no post-repair live execution proof. Inventory, observability, status files, and cursors are discovery/read-model evidence, never transition authority. [Agent 1, `research.md:7-9,30-34`; DS-SFOL `TASK-SESSION-REPORT.md:3-24`, `mutation-admission-receipt.json:14-30`; BTE `REFRESH-REPORT.md:5-40`]

## TL;DR

Two causes interact:

1. An authored-valid Plan can reach Task Session without a mode-capable material producer boundary. Task Session then becomes the first component to discover that its required admission inputs do not exist.
2. Exact byte mismatch is treated as if it necessarily invalidated lifecycle semantics. Exact mismatch must continue to block the old join, but a separate, independently owned classifier must decide whether the changed paths are execution-invalidating, projection-only, unrelated, or unclassified.

The candidate repair issues one immutable `execution_epoch` per selected SWU at Plan time, independently checks handoff readiness before routing, separates producer/validator/consumer roles by execution mode, and records lifecycle progress only as append-only owner-authorized `epoch_transition` entries. [Agent 1, `research.md:13-28,38-42,57-69`; Plan `arcanum/spells/invoke/plan.md:35-58,70-98,125-153`; Task Session `arcanum/arcana/task-session/SKILL.md:220-240`]

## Context and proof boundary

The existing containment gates worked: DS-SFOL stopped before its first write when three material inputs were missing; a later exact-byte mismatch also stopped reuse of an obsolete receipt. The defect is therefore not permissive validation but late producer discovery plus an overloaded refresh/join model. The reflection’s Refresh counts show activity, not causation or progress, and its central projection omits part of the demonstrated cycle. [Agent 1, `research.md:7-15,30-34`; `.arcanum/observability/reflections/20260723T235741Z-invoke-plan-refresh-churn-reflection.md:16-30,47-65,147-153`]

BTE confirms that stale projections and exact-byte repairs can consume lifecycle work while independent blockers remain, but its missing red-manifest owner is not the same causal witness as DS-SFOL’s missing producer boundary. Claims that all Refreshes share one cause, or that the proposed repair works live, are rejected. [Agent 1, `research.md:32-34`; BTE `refresh-report.json:50-59`, `SWU-BTE-L0-001/.../TASK-SESSION-REPORT.md:19-29`, `SWU-BTE-L0A-REPAIR-001/.../TASK-SESSION-REPORT.md:5-40`]

## Connections derived from `research.md`

| Lead | Connection | Bound |
|---|---|---|
| Invoke–Distill enforcement | Plan already checks SWU shape and hidden gaps, so handoff readiness belongs beside Plan activation but must remain a verdict independent of authored-plan validity. | It does not make Distill a producer or execution owner. [Agent 1, `research.md:15,38`; `arcanum/spells/invoke/plan.md:125-153`] |
| BTE Refresh readiness/applied results | A Refresh can validate and apply projection work while the implementation handoff remains gated; “applied” is not runtime readiness. | Corroborating only; not the DS-SFOL causal chain. [Agent 1, `research.md:34`; BTE `REFRESH-REPORT.md:5-40`] |
| Most-used-skills efficiency | Moving falsifiable checks earlier reduces late rediscovery while the unchanged Task Session pre-write gate preserves containment. | Efficiency telemetry cannot authorize a transition. [Agent 1, `research.md:40,42,55`; `.arcanum/observability/reflections/20260723T005559Z-most-used-skills-efficiency-review.md:10-12,39-49,97-106`] |
| Durable execution | Stable instance identity and append-only history support an epoch lineage analogy. | No workflow engine, replay store, or event bus is implied. [Agent 2, `research.md:77-81`; [Azure orchestration versioning](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-orchestration-versioning)] |
| Reproducible builds | Known inputs and retained divergent outputs support exact digest preservation. | No build graph, cache, or sandbox is implied. [Agent 2, `research.md:87`; [Bazel hermeticity](https://docs.bazel.build/versions/main/hermeticity.html); [Nix reproducibility](https://releases.nixos.org/nix/nix-2.15.3/manual/advanced-topics/diff-hook.html)] |

## Demonstrated loop and causal model

```text
authored-valid Plan
  -> selected SWU routed without compatible producer/readiness proof
  -> Task Session pre-write admission
  -> missing package/receipt/schema
  -> blocked, no mutation
  -> Refresh materializes or repairs join targets
  -> exact receipt initially passes
  -> mutable projection bytes change
  -> old exact join blocks
  -> rematerialization / re-entry
```

Cause A is the missing mode-capable producer boundary. Cause B is conflating observed byte drift with semantic invalidation. Exact digest binding is an intentional safety property and remains fail-closed; the repair changes lifecycle interpretation, not digest enforcement. [Agent 1, `research.md:13-15,23-28,32,41`; material schema `arcanum/spells/invoke/schemas/material-package.schema.json:58-75,98-149`; receipt schema `arcanum/spells/invoke/schemas/material-package-receipt.schema.json:7-52`]

## Selected redesign

### Execution epoch

Invoke Plan issues exactly one immutable `execution_epoch` per selected SWU, and only after independently enumerating:

- all mutation-capable handoffs;
- complete controlling-path and non-controlling projection-path digest sets;
- dependencies, allowed writes, validation surface;
- required artifact and receipt classes;
- execution mode and named material roles.

An incomplete enumeration rejects epoch issuance. An epoch binds `goal_id`, `epoch_id`, `unit_id`, plan digest, the enumerated sets, and role identities. A changed plan never rewrites an epoch: it either leaves it usable under a classified non-invalidating change or supersedes it while retaining old and new digests. This is a narrow stable-instance/lineage transfer from Azure, not replay architecture. [Agent 1, `research.md:38-42,50,63,69`; Agent 2, `research.md:77-81`]

### Roles and mode contracts

Three roles are distinct:

- `material_producer`: emits the mode-required material or execution contract.
- `producer_validator`: independently validates completeness, identity, ownership, dependencies, paths, publication class, and validation commands.
- `material_consumer`: verifies the validated input and authors/uses effects.

For local mode, a distinct `local_execution_contract_producer` emits the immutable contract; Task Session consumes and validates that contract and authors implementation effects. It cannot self-produce or self-validate admission. For external, delegated, and reusable modes, retain the exact pre-materialized package plus producer receipt. Assigning one incompatible owner or collapsing producer and validator fails readiness. Existing package validation demonstrates a usable validation boundary, not a complete local-mode design. [Agent 1, `research.md:23-26,39,48,61-62`; `arcanum/spells/invoke/scripts/material_package_validator.py:179-198,202-370`]

### Readiness and drift

`handoff_readiness_receipt` is epoch-bound and has exactly one verdict: `ready`, `gated`, or `blocked`, with exact missing or incompatible requirements. Authored-plan validity remains separate. Only `ready` can route Task Session. The Task Session pre-write gate and exact mismatch behavior remain unchanged. [Agent 1, `research.md:38-40,49,55,69`; `arcanum/arcana/task-session/SKILL.md:220-240`]

`byte_drift` means only an observed digest mismatch and always blocks the old join. `change_impact` is separately computed from the complete controlling paths, non-controlling projection paths, and changed-path set. Its validator is distinct from the projection writer and emits exactly one verdict: `execution_invalidating`, `projection_only`, `unrelated`, or `unclassified`. `unclassified` fails closed. Every rematerialization retains old digest, new digest, reason, and classifier receipt. [Agent 1, `research.md:41,51,64,69`; Agent 2, `research.md:87`; [Nix reproducibility](https://releases.nixos.org/nix/nix-2.15.3/manual/advanced-topics/diff-hook.html)]

### Transition authority and progress

Lifecycle progress is only an append-only `epoch_transition` admitted by one named lifecycle-ledger owner. Receipts are evidence submitted to that owner; Inventory, observability, status, generated projections, and cursors are selectors/read models and cannot advance state. The concrete lifecycle-ledger owner is unresolved and blocks promotion beyond CANDIDATE. [Agent 1, `research.md:27-28,42,53,66`; Agent 2, `research.md:79-81,94-98`]

The independent progress denominator is:

`goal_id + epoch_id + unit_id + authoritative_from_state + authoritative_to_state + mutation_crossed + blocker_fingerprint`.

Define `churn_key = goal_id + epoch_id + unit_id + authoritative_from_state + requested_to_state + blocker_fingerprint`. Repeating the same key without new preconditions admits no transition and yields `churn_blocked`; it is not completion. A cursor may select the next ledger entry but cannot establish progress. [Agent 1, `research.md:42,53,66`]

Refresh reuses existing valid receipts and continuations, declares exactly one `transition_kind` and its postcondition—`plan_repair`, `material_production_validation`, `projection_synchronization`, or `route_selection`—and performs no target implementation. [Agent 1, `research.md:15,52,65,69`; `arcanum/spells/invoke/refresh.md:185-220`]

## Transition table

| State | Admitted transition | Required witness |
|---|---|---|
| `epoch_issued` | Plan issued complete immutable epoch | Plan owner + completeness validator |
| `handoff_gated` | Requirements known but not yet satisfied | readiness receipt with exact gaps |
| `handoff_blocked` | Incompatible/missing owner or contract | readiness receipt with blocker fingerprint |
| `handoff_ready` | All mode inputs and roles independently validated | ready receipt |
| `admission_blocked` | Task Session pre-write gate fails | mutation-admission receipt |
| `admitted` | unchanged pre-write gate passes | admission receipt bound to epoch |
| `mutation_crossed` | first authorized effect occurred | Task Session effect receipt |
| `execution_complete` | SWU effects and live validation complete | execution + validation receipts |
| `closeout_joined` | exact closeout join accepted | join receipt and drift classification if needed |
| `epoch_terminal` | named terminal postcondition accepted | ledger-owner transition |
| `superseded` | replacement epoch accepted; history retained | old/new digests and reason |

The state names above do not themselves authorize movement. The complete allowed-edge relation is:

| From state | To state | Transition kind | Sole admitting owner | Required witness |
|---|---|---|---|---|
| _none_ | `epoch_issued` | `epoch_issue` | `owner_unresolved: promotion_blocked` | complete immutable epoch + Plan owner receipt + independent completeness receipt |
| `epoch_issued` | `handoff_gated` | `readiness_assessment` | `owner_unresolved: promotion_blocked` | epoch-bound readiness receipt naming exact unsatisfied requirements |
| `epoch_issued` | `handoff_blocked` | `readiness_assessment` | `owner_unresolved: promotion_blocked` | epoch-bound readiness receipt naming incompatible/missing owner or contract and blocker fingerprint |
| `epoch_issued` | `handoff_ready` | `readiness_assessment` | `owner_unresolved: promotion_blocked` | epoch-bound `ready` receipt from the independent producer validator |
| `handoff_gated` | `handoff_blocked` | `readiness_assessment` | `owner_unresolved: promotion_blocked` | new evidence proving an incompatible requirement + blocker fingerprint |
| `handoff_gated` | `handoff_ready` | `material_production_validation` or `route_selection` | `owner_unresolved: promotion_blocked` | newly satisfied requirements + epoch-bound `ready` receipt |
| `handoff_blocked` | `handoff_gated` | `plan_repair` or `route_selection` | `owner_unresolved: promotion_blocked` | new preconditions removing incompatibility while listing remaining exact gaps |
| `handoff_blocked` | `handoff_ready` | `plan_repair`, `material_production_validation`, or `route_selection` | `owner_unresolved: promotion_blocked` | new preconditions removing the blocker + epoch-bound `ready` receipt |
| `handoff_ready` | `admission_blocked` | `task_admission` | `owner_unresolved: promotion_blocked` | Task Session mutation-admission receipt bound to the epoch |
| `handoff_ready` | `admitted` | `task_admission` | `owner_unresolved: promotion_blocked` | passing Task Session admission receipt bound to unchanged controls and epoch |
| `admission_blocked` | `admitted` | `task_admission` | `owner_unresolved: promotion_blocked` | new preconditions + a new passing admission receipt; the failed receipt is retained |
| `admitted` | `mutation_crossed` | `execution_effect` | `owner_unresolved: promotion_blocked` | first-effect receipt identifying the authorized effect and epoch |
| `mutation_crossed` | `execution_complete` | `execution_validation` | `owner_unresolved: promotion_blocked` | SWU execution receipt + independent live-validation receipt |
| `execution_complete` | `closeout_joined` | `closeout_join` | `owner_unresolved: promotion_blocked` | exact join receipt + required independent drift classification |
| `closeout_joined` | `epoch_terminal` | `terminalization` | `owner_unresolved: promotion_blocked` | named terminal postcondition + complete retained receipt chain |
| `epoch_issued`, `handoff_gated`, `handoff_blocked`, `handoff_ready`, `admission_blocked`, or `admitted` | `superseded` | `plan_repair` | `owner_unresolved: promotion_blocked` | replacement epoch identity + old/new digests + reason + retained history; an admitted epoch also proves no mutation was crossed |
| `execution_complete` | `superseded` | `plan_repair` | `owner_unresolved: promotion_blocked` | independent `execution_invalidating` classification + replacement epoch identity + old/new digests + reason + retained completed-execution history |

All unlisted edges are rejected, including self-edges, backward edges, skipped edges, transitions out of `epoch_terminal` or `superseded`, direct supersession from `mutation_crossed`, and supersession of `execution_complete` without an independent `execution_invalidating` verdict. A newly satisfied precondition permits only the listed forward edge and never rewrites the earlier receipt. Refresh may submit evidence only under its four declared kinds (`plan_repair`, `material_production_validation`, `projection_synchronization`, `route_selection`); `projection_synchronization` admits no lifecycle state edge by itself. The unresolved sole admitting lifecycle-ledger owner is therefore an explicit promotion blocker, not a role silently assigned to Plan, Refresh, Task Session, a receipt producer, or a read model.

Bare `complete` is forbidden because it obscures whether execution, closeout, or the epoch is complete. Transitions are monotonic; no receipt rewrites an earlier state. [Agent 1, `research.md:50-53`; Agent 2, `research.md:79,87,91-96`]

## Owner–witness–soundness–verdict matrix

| Item | Owner / precedent | Witnessed? | Soundness boundary | Disposition |
|---|---|---:|---|---|
| Plan readiness gate | Invoke Plan / existing Distill activation | Partial | Current Plan lacks admission completeness | CANDIDATE |
| Local execution contract | New producer + independent validator | No | Role split and schema need fixtures | CANDIDATE |
| External/reusable package | Existing package producer/validator | Yes | Preserve exact package/receipt behavior | CANDIDATE retain |
| Immutable epoch | Invoke Plan / Azure stable instance lineage | No local repair proof | Narrow identity transfer only | CANDIDATE |
| Drift impact classifier | Independent classifier / Nix divergence retention | Byte drift yes; classifier no | Must use complete path sets and fail closed | CANDIDATE |
| Append-only transition owner | Unresolved local ledger owner / Azure history analogy | No | Authority cannot be a read model | CANDIDATE, owner-blocked |
| Workflow engine/replay store/event bus | Azure/AWS | No local witness | Cargo-cult expansion | KILL |
| Generic retry/redrive/effect framework | AWS Step Functions | No local witness | Beyond demonstrated causes | KILL |
| Generalized CAS | DynamoDB optimistic locking | No concurrency witness | Useful precedent, absent local need | DEFER |
| Build graph/cache/sandbox | Bazel/Nix | No local witness | Only input/digest lesson transfers | KILL |
| New authoritative current-state projection | Agent 2 inference | No | Risks competing authority | KILL |
| Repository-wide manifest | Internal normalization option | No local denominator | Migration exceeds first slice | DEFER |

The retained/rejected analogy boundary follows Agent 2’s precedents but narrows them using Agent 1’s local causes. [Agent 1, `research.md:57-69`; Agent 2, `research.md:77-98`; [AWS error handling](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html); [DynamoDB optimistic locking](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/BestPractices_OptimisticLocking.html)]

## First slice, migration, and compatibility

Implement only: Plan handoff readiness; compatible producer assignment; execution epoch; unchanged Task Session pre-write gate; unchanged exact mismatch blocking. Preserve one-SWU execution, exact digests, historical receipts, external/delegated/reusable compatibility, and public/private separation. Existing plans become `legacy_unadmitted`; they gain no inferred readiness and must pass the new gate before routing. No receipt is rewritten. [Agent 1, `research.md:46-55,61-69`]

Before any public Arcanum proposal, scan wording and fixtures for private project names, paths, vocabulary, and evidence. Private witnesses remain here; public contracts receive generic invariants only. [Agent 1, `research.md:44-55`]

## Negative fixtures and telemetry

The first slice requires eight independent negative fixtures:

1. authored-valid Plan with no producer → `handoff_blocked`;
2. producer assigned to an incompatible execution mode → `handoff_blocked`;
3. producer equals its required independent validator → reject;
4. epoch missing any mutation-capable handoff or required path/digest set → reject issuance;
5. exact digest mismatch with no classifier receipt → old join blocks as `unclassified`;
6. projection writer acting as drift classifier → reject classification;
7. any edge absent from the allowed-edge table—including backward, skipped, self, terminal-outbound, direct `mutation_crossed` supersession, or unclassified `execution_complete` supersession—→ deterministically reject;
8. repeated `churn_key` without changed preconditions → no-op plus `churn_blocked`, never progress.

Positive controls must show local-contract readiness, unchanged external/reusable exact-package readiness, and a projection-only classification that preserves the old execution result while still recording old/new digests. Telemetry records the progress denominator and transition receipt identity; it never supplies authority. [Agent 1, `research.md:38-42,48-53,61-69`; Agent 2, `research.md:87,94-98`]

## Falsifiable acceptance criteria

The candidate advances only if:

1. all eight negative fixtures fail closed for the stated reason;
2. independently enumerated mutation-capable handoffs and both path sets are complete before epoch issuance;
3. incompatible-owner and producer/validator-collapse cases cannot produce `ready`;
4. Task Session cannot be routed unless readiness is `ready`, and its existing pre-write gate still independently rejects absent/stale/mismatched inputs;
5. an independent drift classifier reproduces all classification fixtures, with `unclassified` blocking;
6. transitions are append-only and monotonic under a named owner;
7. progress computed from the authoritative denominator differs from raw run/Refresh counts and repeated identical blockers produce no progress;
8. a live post-repair DS-SFOL-shaped run crosses admission without repair Refresh, while exact drift still blocks the obsolete join.

Criterion 8 is deliberately unmet today; therefore the verdict cannot exceed CANDIDATE. [Agent 1, `research.md:9,32-42,69`]

## Sanitized public-safe Spellcraft change requests

1. Add a Plan-stage handoff-readiness contract with separate authored-valid and handoff-ready verdicts.
2. Add execution-mode role schemas for producer, independent producer validator, and consumer; define the local execution-contract producer separately.
3. Add immutable selected-unit epoch and append-only transition schemas without prescribing a workflow engine or storage product.
4. Add byte-drift observation and independently validated change-impact classification while retaining exact mismatch failure.
5. Split Refresh postconditions into the four declared transition kinds and prohibit target implementation.
6. Add generic negative fixtures and a public/private leakage check.

These are requests for design/validation work, not claims that canonical Arcanum has changed. [Agent 1, `research.md:44-55,69`]

## Open Questions

- **Lifecycle-ledger owner — owner: Arcanum governance:** Which existing artifact owner may authoritatively admit `epoch_transition` without creating a competing current-state projection?
- **Local contract schema — owner: Invoke Plan + Task Session maintainers:** What is the minimal contract that authorizes Task Session to author effects without making it its own producer/validator?
- **Path-set completeness — owner: Plan/Distill validation:** How is independent completeness proven for controlling and projection paths?
- **Drift classifier — owner: independent validation capability:** Which deterministic rules distinguish execution-invalidating, projection-only, and unrelated changes?
- **Legacy admission — owner: migration designer:** How are `legacy_unadmitted` plans revalidated without silently manufacturing historical readiness?
- **Live proof — owner: bounded Task Session experiment:** Which non-private generic fixture can demonstrate the repaired path before promotion?
