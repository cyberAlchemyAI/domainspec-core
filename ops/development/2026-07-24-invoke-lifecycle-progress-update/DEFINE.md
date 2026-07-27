# Define: Invoke Lifecycle Progress Protocol

Status: approved authoring baseline

Discovery: research and reflection present; no discovery waiver

Implementation status: not started

## Problem

The current contracts correctly fail closed at the final mutation boundary, but
they permit an authored-valid Plan to route one SWU to Task Session before a
compatible material producer and all required admission inputs exist. Task
Session then becomes the first component to discover the missing inputs.
Refresh is subsequently used for materially different operations—plan repair,
material production and validation, projection synchronization, and route
selection—while mutable planning projections remain exact join targets.

This produces safe local failures but poor lifecycle progress. Repeated valid
runs and Refresh receipts can describe activity without showing that the
selected implementation unit moved from planned to admitted to executed.

## Objective

Add the smallest generic protocol that makes the selected execution unit,
readiness, transition authority, and progress explicit before mutation routing,
while preserving the existing fail-closed gates.

## Required outcomes

| ID | Required outcome |
| --- | --- |
| ILP-R01 | Authored-plan validity and mutation-handoff readiness are separate verdicts. |
| ILP-R02 | One immutable execution epoch binds exactly one selected SWU, execution mode, role identities, complete declared control graph, allowed writes, validation surface, and required artifact/receipt classes. |
| ILP-R03 | Local, external, delegated, and reusable modes assign compatible producer, independent validator, and consumer roles; Task Session is never the first component to discover that no producer exists. |
| ILP-R04 | Only an epoch-bound `ready` receipt permits routing to mutation execution; Task Session's live pre-write gate remains independent and fail-closed. |
| ILP-R05 | Exact byte mismatch always blocks the obsolete join, while independent change-impact classification determines whether a successor epoch is required. |
| ILP-R06 | A `plan_repair` that changes any epoch-control field creates a successor epoch and moves the old epoch to `superseded`; only new evidence/material under an unchanged control digest may advance readiness inside the same epoch. |
| ILP-R07 | Lifecycle progress consists only of allowed append-only epoch transitions admitted by a named owner; read models, cursors, status files, Inventory, and observability cannot advance state. |
| ILP-R08 | Refresh declares exactly one transition kind and postcondition and performs no target implementation. |
| ILP-R09 | Existing plans are `legacy_unadmitted`; path-set completeness, the local contract schema, and migration are proved rather than inferred. |
| ILP-R10 | Generic negative controls and a live post-repair run prove the repaired topology before promotion; private witnesses remain private. |

## Scope

Included:

- candidate generic contracts and schemas for execution epoch, local execution
  contract, handoff readiness, change impact, and epoch transition;
- deterministic validators and red/green fixtures;
- Invoke Plan and Refresh contract integration through Spellcraft;
- Task Session consumption and pre-write epoch binding through Sigil
  Development;
- an owner decision for transition admission;
- legacy admission rules, observational progress fields, churn detection, and a
  live generic proof;
- canonical-first/generated-second synchronization and public/private leakage
  checks.

Excluded:

- a workflow engine, replay store, event bus, retry/redrive framework, effect
  system, build graph, cache, sandbox, or generalized compare-and-swap layer;
- a new authoritative current-state projection;
- a repository-wide execution manifest migration;
- weakening exact digest matching or Task Session live validation;
- multi-SWU execution inside one Task Session;
- target implementation inside Invoke or Refresh;
- private project names, paths, evidence, or product claims in public Arcanum;
- promotion, publication, commit, push, or submodule pointer updates.

## Actors and authority

| Actor/capability | Authority |
| --- | --- |
| Invoke | authors this Define, Design, Plan, and later Plan/Refresh artifacts; it does not execute target work |
| Spellcraft | owns public Invoke spell revision, validation, observation, reflection, and promotion readiness |
| Sigil Development | owns public Task Session sigil revision and validation |
| transition-admission owner | admits allowed epoch transitions; exact owner must be ratified before mutation implementation |
| producer validator | proves only the declared epoch/material/readiness/change-impact axis |
| Task Session | consumes one ready epoch, revalidates live inputs, executes one SWU, and emits its own receipts |
| observability and Inventory | non-authoritative evidence and discovery projections |
| human maintainer | owns consequential authority selection, promotion, publication, commit, and push |

## Behavioral law

```text
approved design + one selected SWU
  -> Plan authors immutable epoch candidate
  -> independent completeness validation
  -> mode-compatible producer emits contract/material
  -> independent readiness validation
  -> named transition owner admits epoch/readiness edge
  -> only ready routes to Task Session
  -> Task Session independently revalidates live controls
  -> one SWU crosses mutation and validates
  -> closeout classifies drift and joins exact evidence
  -> named transition owner admits terminal progress
```

No receipt may rewrite an earlier receipt. No read model may admit a transition.
No approval may turn invalid evidence into valid evidence.

## Epoch-control invariant

The epoch control digest covers:

- `goal_id`, `epoch_id`, and exactly one `unit_id`;
- plan identity and digest;
- execution mode;
- producer, producer-validator, and consumer identities;
- complete controlling-path identities and exact digests;
- declared non-controlling projection-path identities and baseline digests;
- dependencies;
- allowed writes;
- validation commands and reviewable checks;
- required artifact and receipt classes.

The epoch remains immutable. A same-epoch readiness advance is legal only when
the epoch control digest is unchanged and new material/evidence satisfies a
requirement already declared by that epoch.

Any change to the plan digest, selected unit, mode, role identities, controlling
or projection path sets, allowed writes, dependency frontier, validation
surface, or required artifact/receipt classes requires a successor epoch and an
append-only `superseded` transition. A writer cannot label such a change
`plan_repair` and retain the epoch identity.

## Decisions

1. Keep authored validity and handoff readiness independent.
2. Use one epoch per selected SWU; never use “latest plan” as execution identity.
3. Local mode produces an immutable execution contract, not pre-authored output
   bytes; external/delegated/reusable modes retain exact material packages.
4. Keep producer, producer validator, and consumer distinct for one epoch.
5. Preserve exact digest failure and add a separate change-impact classifier.
6. Permit same-epoch readiness advancement only for unchanged-control evidence
   completion; every control change produces a successor epoch.
7. Keep lifecycle authority out of Inventory, telemetry, generated views,
   status files, and cursors.
8. Split Refresh by four declared transition kinds without creating four new
   capabilities.
9. Treat old plans as `legacy_unadmitted`; never synthesize historical
   readiness.
10. Require a generic live proof before any promotion claim.

## Open decision

`ILP-G01`: which existing Arcanum owner admits `epoch_transition` records without
creating a competing current-state authority?

This is an acceptance-critical lifecycle decision. Invoke can complete this
authoring package and route it to Spellcraft, but no mutation-capable Task
Session handoff is ready until that owner and the public source placement are
ratified.

## Acceptance

- ILP-R01 through ILP-R10 each map to a design component, one or more SWUs,
  causal fixtures, and closure evidence.
- The same-epoch supersession invariant is machine-testable and covers all
  epoch-control fields.
- Every execution mode has a complete producer/validator/consumer assignment.
- Path completeness is bounded to an explicit declared execution-control graph
  and is independently checked.
- The transition table rejects all unlisted edges, repeated unchanged churn,
  and unauthorized writers.
- Plan may pass authoring while mutation handoff is gated.
- Public outputs are generic and contain no private witness data.
- The first lifecycle unit resolves authority and source placement before code
  mutation.

## Define-stage trace

- Techniques: `sequence`, `owner_boundary_check`, `authority_split_gate`,
  `artifact_contract_bridge`, `residue_ledger`,
  `concrete_path_evidence`.
- Distill sanity: pass. The coherent definition is a bounded
  selected-unit/epoch protocol, not a durable workflow platform.
- Layering seed: ratify authority at L0; prove epoch/readiness contracts at L1;
  integrate Plan/Refresh/Task Session at L2; migrate, observe, and prove live at
  L3.
- Next route: Design.

