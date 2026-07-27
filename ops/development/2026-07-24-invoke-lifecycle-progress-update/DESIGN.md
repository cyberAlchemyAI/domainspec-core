# Design: Invoke Lifecycle Progress Protocol

Status: approved L1 authoring output

Source contracts: `DEFINE.md`, `GLOSSARY.md`, `GAPS.md`

## 1. Context view

```text
Invoke Plan
  | authors plan + one immutable epoch candidate
  v
epoch/control-graph validator
  | emits completeness receipt
  v
mode producer -> independent producer validator -> readiness receipt
  |                                              |
  +---------------- transition evidence ---------+
                                                 v
                                  transition-admission owner
                                                 |
                                  ready only ----+
                                                 v
                                      Task Session (one SWU)
                                                 |
                         execution + validation + closeout receipts
                                                 v
                                  transition-admission owner

Refresh may submit one typed transition request.
Inventory, observability, projections, and cursors observe only.
```

The protocol adds no background scheduler and no authoritative current-state
projection. State is reconstructed from an immutable epoch plus admitted
append-only transitions.

## 2. High-level structure view

| Component | Owns | Does not own |
| --- | --- | --- |
| `ExecutionEpoch` | immutable selected-unit and control identity | readiness, admission, execution, or completion |
| `ExecutionControlGraph` | declared concrete paths, dependencies, writes, validations, artifact/receipt classes | undisclosed semantic dependencies |
| `LocalExecutionContract` | local-mode authority boundary for Task Session to author effects | output bytes or execution completion |
| existing material package | exact pre-materialized outputs for external/delegated/reusable modes | local Task Session-produced effects |
| `HandoffReadinessReceipt` | `ready`, `gated`, or `blocked` for one epoch | Task Session live admission |
| `ChangeImpactReceipt` | semantic impact of observed changed paths | permission to ignore exact byte mismatch |
| `EpochTransition` | one allowed append-only lifecycle edge | mutable current state or target implementation |
| `LifecycleProgressEvent` | observational projection of admitted transition identity and churn | transition admission |

### Candidate data contracts

```yaml
execution_epoch:
  schema_version: 1
  goal_id: string
  epoch_id: string
  unit_id: string
  plan_ref: path
  plan_digest: sha256
  execution_mode: local | external | delegated | reusable
  roles:
    producer: {role_id, capability_ref}
    producer_validator: {role_id, capability_ref}
    consumer: {role_id, capability_ref}
  controlling_paths: [{path, sha256, class}]
  projection_paths: [{path, sha256, class}]
  dependency_ids: [string]
  allowed_writes: [path-or-prefix]
  validation_surface: [{kind, value}]
  required_artifact_classes: [string]
  required_receipt_classes: [string]
  epoch_control_digest: sha256
```

```yaml
handoff_readiness_receipt:
  epoch_id: string
  epoch_control_digest: sha256
  verdict: ready | gated | blocked
  producer_receipt: path
  producer_receipt_digest: sha256
  satisfied_requirements: [string]
  missing_requirements: [string]
  incompatible_requirements: [string]
  blocker_fingerprint: string | null
  validator_identity: string
```

```yaml
epoch_transition:
  transition_id: string
  goal_id: string
  epoch_id: string
  unit_id: string
  from_state: null | epoch_issued | handoff_gated | handoff_blocked |
    handoff_ready | admission_blocked | admitted | mutation_crossed |
    execution_complete | closeout_joined
  to_state: epoch_issued | handoff_gated | handoff_blocked | handoff_ready |
    admission_blocked | admitted | mutation_crossed | execution_complete |
    closeout_joined | epoch_terminal | superseded
  transition_kind: epoch_issue | readiness_assessment |
    material_production_validation | route_selection | plan_repair |
    task_admission | execution_effect | execution_validation |
    closeout_join | terminalization
  epoch_control_digest: sha256
  mutation_crossed: boolean
  blocker_fingerprint: string | null
  evidence_receipts: [{path, sha256, owner}]
  successor_epoch_id: string | null
  prior_plan_digest: sha256 | null
  next_plan_digest: sha256 | null
  admitted_by: string
```

These schemas are design candidates. Public placement and the
transition-admission owner require `ILP-G01` resolution.

## 3. Low-level component view

### Epoch construction and completeness

1. Resolve exactly one selected SWU from the approved work-pack.
2. Traverse the declared execution-control graph:
   work-pack -> selected task -> SWU -> source contracts -> dependency tasks and
   policies -> validation surface -> closeout targets.
3. Reject unresolved globs, missing paths, duplicate normalized paths, unknown
   dependency IDs, absent owner roles, or overlapping controlling/projection
   classifications.
4. Sort and digest all fields canonically.
5. Emit an epoch candidate and a separate completeness receipt.
6. Submit `_none -> epoch_issued` to the transition-admission owner.

Completeness means complete against the declared graph contract, not omniscient
knowledge of every repository dependency. If execution discovers a previously
undeclared controlling artifact, readiness/admission blocks and a successor
epoch is required.

### Mode-role matrix

| Mode | Producer output | Producer | Independent validator | Consumer |
| --- | --- | --- | --- | --- |
| `local` | immutable `LocalExecutionContract` | Invoke Plan-side contract producer | deterministic local-contract/readiness validator | Task Session |
| `external` | exact material package | external owner named by the plan | existing material-package validator | Task Session |
| `delegated` | exact material package plus delegation receipt | delegated execution owner | existing material-package validator | Task Session |
| `reusable` | exact reusable package and producer receipt | named reusable-package owner | existing material-package validator | Task Session |

For one epoch, producer, producer validator, and consumer role identities must
be pairwise distinct. Capability implementations may share a repository, but
one role cannot attest to its own output.

### Minimal local execution contract

```yaml
local_execution_contract:
  epoch_id: string
  epoch_control_digest: sha256
  unit_id: string
  consumer_capability: task-session
  controlling_paths: [{path, sha256}]
  dependency_ids: [string]
  allowed_writes: [path-or-prefix]
  forbidden_writes: [path-or-prefix]
  validation_surface: [{kind, value}]
  closeout:
    target_inventory: [{path, baseline_digest}]
    allowed_delta_classes: [string]
    owner_validation: [command-or-check]
    expected_owner_receipt_class: string
    successor_policy: string
```

This contract authorizes only execution of the selected unit within the
declared scope. It neither predicts nor contains output bytes.

### Same-epoch versus successor rule

Compute the epoch control digest over every control field. Then:

```text
if proposed change alters any control field:
    reject same-epoch repair
    require successor epoch
    require old -> superseded transition with old/new digests and reason
elif new receipt/material only satisfies an already-declared requirement:
    retain epoch
    permit only an allowed forward readiness edge
else:
    reject as unclassified
```

Examples that always require a successor: plan digest, selected SWU, execution
mode, producer/validator/consumer identity, controlling path set or digest,
projection path set, dependencies, allowed writes, validation surface, or
required artifact/receipt class.

### Change-impact classifier

Inputs:

- immutable epoch;
- changed paths with old/new digests;
- complete controlling path set;
- declared projection path set;
- classifier identity;
- projection-writer identity.

Rules:

1. If classifier identity equals the writer of any changed projection, reject.
2. If a changed path intersects controlling paths, verdict is
   `execution_invalidating`.
3. Else if all changed paths are declared projections and their path set is
   unchanged, verdict is `projection_only`.
4. Else if every changed path is outside both sets, verdict is `unrelated`.
5. Otherwise verdict is `unclassified`.
6. Exact mismatch still rejects the old join for every verdict. The verdict
   only controls successor/retained-execution handling.

### Transition relation

The validator admits only the edge table defined in the source findings and
materialized in `work-pack/shared/DECISIONS.md`. It rejects:

- all self, backward, skipped, or unlisted edges;
- transitions from `epoch_terminal` or `superseded`;
- direct supersession from `mutation_crossed`;
- supersession of `execution_complete` without independent
  `execution_invalidating` evidence;
- `projection_synchronization` as a lifecycle state edge;
- any `plan_repair` that changes control identity without successor fields;
- any same-epoch advancement whose control digest changed;
- repeated churn keys without changed preconditions.

## 4. Workflow process view

```text
Spellcraft ratifies owner and source placement
  -> implement schemas and red fixtures
  -> implement transition validator
  -> implement mode contracts and readiness validator
  -> integrate Plan epoch/readiness output
  -> integrate Refresh typed transitions + drift classification
  -> integrate Task Session ready-epoch consumption
  -> add legacy admission and observational progress
  -> run generic live proof
  -> synchronize generated surfaces through their owners
  -> reflect and decide promotion readiness
```

Every mutation-capable SWU has a predeclared Task Session closeout contract. A
new Task Session is opened for each SWU.

## 5. Decision flow view

```text
Plan authored-valid?
  no -> repair Plan
  yes
   |
   v
epoch candidate complete and independently validated?
  no -> handoff blocked
  yes -> submit epoch_issue
   |
   v
mode producer compatible and producer receipt valid?
  no producer/role incompatible -> handoff blocked
  material merely absent -> handoff gated
  valid -> readiness ready
   |
   v
transition owner admits handoff_ready?
  no -> gated/blocked with owner receipt
  yes -> route exactly one epoch/SWU to Task Session
   |
   v
live pre-write admission passes?
  no -> admission_blocked; retain evidence
  yes -> admitted -> mutation_crossed -> execution_complete
   |
   v
exact closeout join passes?
  yes -> closeout_joined -> epoch_terminal
  no -> classify change impact; old join remains blocked
        control change -> successor + superseded
        projection-only/unrelated -> repair exact join without rewriting epoch
        unclassified -> block
```

## 6. Dependency and interface view

| Producer | Consumer | Interface | Failure rule |
| --- | --- | --- | --- |
| Invoke Plan | epoch completeness validator | epoch candidate + declared control graph | incomplete or unresolved graph rejects issuance |
| mode producer | producer validator | local execution contract or exact material package | missing/incompatible/self-validated output cannot be ready |
| producer validator | transition-admission owner | readiness receipt bound to epoch control digest | stale/mismatched receipt rejects transition |
| transition-admission owner | Task Session | admitted `handoff_ready` transition + readiness receipt | absent owner decision or edge receipt blocks routing |
| Task Session | transition-admission owner | admission/effect/execution receipts | no inferred progress from Task Session prose/status |
| Refresh | transition-admission owner or projection owner | one typed request and exact postcondition | mixed transition kinds or target implementation reject |
| change-impact validator | closeout/transition validator | independent classifier receipt | writer self-classification or `unclassified` blocks |
| admitted transitions | observability | progress event | projection may report but never admit or rewrite |

## Decisions

| ID | Decision | Reason |
| --- | --- | --- |
| ILP-D01 | Use one immutable epoch per selected SWU. | avoids mutable “latest plan” identity and preserves one-unit execution |
| ILP-D02 | Bound completeness to a declared execution-control graph. | makes completeness falsifiable without claiming repository omniscience |
| ILP-D03 | Local mode uses an execution contract; other mutation modes retain exact packages. | removes the local producer/consumer cycle without weakening reusable material proof |
| ILP-D04 | Require pairwise-distinct role identities. | prevents producer self-attestation and Task Session self-admission |
| ILP-D05 | Separate byte drift from change impact. | preserves exact joins while avoiding false semantic conclusions |
| ILP-D06 | Treat the epoch control digest as the same-epoch boundary. | makes plan-repair supersession deterministic |
| ILP-D07 | Append transitions; never rewrite receipts. | preserves causal history and enables an independent progress denominator |
| ILP-D08 | Keep Refresh as one spell mode with four exclusive kinds. | clarifies postconditions without proliferating capabilities |
| ILP-D09 | Do not select the transition-admission owner inside Invoke. | the choice changes cross-capability authority and requires lifecycle/governance ratification |
| ILP-D10 | Keep telemetry observational and derive churn from admitted transitions. | prevents monitoring from becoming shadow authority |

## Risks and controls

| Risk | Control |
| --- | --- |
| epoch schema becomes a workflow platform | include only selected-unit identity and admission controls; no scheduler, retry, replay, or effects log |
| declared graph omits a real control | live Task Session revalidation blocks and requires a successor epoch |
| projection-only label hides semantic drift | complete path sets, independent classifier, and `unclassified` fail-closed |
| plan repair silently changes authority | epoch control digest plus mandatory successor fixture |
| central ledger competes with capability receipts | owner admits edges using receipts; no mutable current-state projection |
| legacy plans are treated as ready | explicit `legacy_unadmitted` default and fresh validation |
| public Arcanum leaks private evidence | sanitized generic fixtures plus path/name scan before owner handoff |
| implementation reintroduces Refresh loops | live proof must cross admission without repair Refresh; repeated churn key is no progress |

## Design gate

- Six required views: complete.
- Glossary consistency: pass.
- Source and evidence boundaries: complete.
- Design Distill: pass; smallest coherent design is the selected-unit epoch and
  readiness protocol. The owner decision remains a named lifecycle gate.
- Upstream/source mutation: none.
- Mutation handoff: gated by `ILP-G01`.
- Next route: Plan.

