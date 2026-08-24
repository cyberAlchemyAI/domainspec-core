# Invoke Design — Cohesive Modular Arcanum

Status: private candidate design; no source or lifecycle mutation.  
Selected architecture: owner-native modules + bilateral OBTC adapters + non-authoritative causal journal.  
Migration strategy: prove one boundary before extracting common protocol fields.

## 1. Context view

Arcanum is a public capability library whose building path crosses authoring, design validation, planning, readiness, semantic selection, consumer entry, material production, mutation admission, execution, closeout mutation, receipt joining, synchronized-result derivation, continuity, ordered-series coordination, capability lifecycle, registry release, projections, and generated runtime packaging.

The architecture must make that path feel like one system without making it one owner.

### System boundary

Inside the candidate design:

- versioned OBTC envelopes and a pure structural validator;
- owner-specific bilateral adapters;
- non-authoritative causal-event projection, optionally persisted by an existing runtime/observability owner as an append-only journal;
- conformance and negative-trace witness harness;
- compatibility declarations and parity receipts.

Outside its authority:

- owner-native semantic decisions and effects;
- Work-Pack, selection, admission, execution, Refresh, lifecycle, registry, Craft, and Inventory state;
- public release and generated package installation.

## 2. High-level structure view

```text
owner-native artifact/receipt
        |
        v
bilateral adapter --projects--> OBTC envelope --structural check--> consumer owner gate
        |                              |
        |                              +--append handle/status--> causal journal
        v
native artifact remains authoritative

consumer owner pass -> owner effect -> owner-native receipt -> next bilateral adapter
consumer owner block -> typed stop + forbidden effects + residue/reroute
effect outcome unknown -> no retry -> effect-owner reconciliation
```

### Module catalog

| Module | Sole owned responsibility | Explicit non-role |
|---|---|---|
| Protocol Schema Steward | Version OBTC envelope and structural schema with `authority_effect:none`. | Cannot make owner policy current; each consumer declares accepted versions. |
| OBTC Structural Validator | Check fields, identities, digests, version declarations, role singularity, receipt references, and transition-shape invariants. | Cannot select, admit, execute, retry, synchronize, advance, promote, or release. |
| Bilateral Adapter | Project one named producer's native artifact into one named consumer's expected envelope and preserve the native handle. | Cannot become a second authoritative writer or invent absent fields. |
| Causal Event Projection | Define hash-linked attempt, native receipt handle, join, reconciliation, residue, and projection events; an existing local owner may persist them. | Cannot mandate a new global store, determine semantic state, or replace native owner receipts. |
| Witness Harness | Replay synthetic protocol traces and verify first-stop/forbidden-effect rules. | Cannot establish real product E2E or production correctness. |
| Invoke | Author Define, Design, Plan, and Refresh artifacts under mode contracts. | Cannot execute SWUs or imply registry/runtime readiness. |
| WPRA | Freeze/audit the authored Work Pack and verify semantic selection without authority effect. | Cannot admit mutation or execute. |
| Material Producer Port | Require one bound producer-native package and receipt per selected SWU. | The port is not an owner; unbound producer blocks admission planning. |
| Task Session | Own consumer entry, one-attempt admission, one-SWU execution terminal, synchronized result, and current continuity cursor. | Cannot execute a series or impersonate material/Refresh owners. |
| Continuation Router | Admit, dispatch, correlate, and join one exact owner hop. | Cannot perform owner work or reinterpret owner verdicts. |
| Invoke Refresh | Own exact closeout mutation/no-op evidence under apply gates. | Phase pass alone is not apply authority. |
| Implementation Readiness | Candidate sole runtime owner of ordered frontier, visited set, action correlation, retry, join, and stop state. | Cannot complete an SWU from an owner receipt or replace Task Session. |
| Task Session Until Blocker | Proposed stateless compatibility spell/profile for `until-real-blocker`. | Must not retain a second frontier, cursor set, retry ledger, or reducer after migration. |
| Craft | Own scoped `.craft/ledger.yml` recursive local state and derived views. | Cannot select/admit/execute/synchronize/promote/release. |
| Dispatch Spec + Orchestrate | Validate and execute approved delegated capability-bound routes. | Cannot establish semantic or lifecycle correctness. |
| Sigil Development / Spellcraft | Own type-specific capability lifecycle judgment. | Cannot imply registry release. |
| Registry Release Port | Require an exact release-owner receipt. | Unbound port cannot release anything. |
| Inventory / Observability | Own native discovery/projection and behavior-signal facts. | Cannot become source, execution, or promotion authority. |
| Package Parity | Prove canonical/generated provenance, byte expectations, and behavioral parity. | Generated provenance alone is not currentness. |

## 3. Low-level component view

### OBTC envelope

```yaml
protocol_version: <semver>
transition_kind: <stable id>
transition_id: <stable id>
attempt_id: <stable id>
caused_by: <transition or approval receipt id>
roles:
  producer: <owner id>
  effect_owner: <exactly one owner id or none for pure projection>
  validator: <validator id>
  router: <router id or none>
  consumer: <owner id>
  evidence_store: <store id or none>
source:
  native_kind: <owner-native artifact kind>
  native_ref: <path or handle>
  digest: <sha256>
  epoch_or_version: <value>
preconditions:
  - gate_id: <id>
    owner: <owner id>
    required_receipt: <schema id>
    on_fail: <block|ask|defer|reroute>
    forbidden_effects: [<effect>]
freshness:
  baseline_digest: <digest or none>
  prior_receipt_digest: <digest or none>
  concurrency_scope: <scope or none>
  lease_or_cas: <binding or none>
replay:
  idempotency_key: <key>
  single_use: <boolean>
  retry_policy: <none|declared-one-shot>
  indeterminate_outcome_route: <owner reconciliation route>
expected_native_receipt:
  producer: <owner id>
  schema: <schema id>
  authority_effect: <effect or none>
owner_declared_next:
  route: <route or none>
  hint_only: true
residue: [<id>]
reroute: <owner route or none>
```

Structural validation may check that roles, references, digests, bindings, and required fields are coherent. Only the consumer/effect owner evaluates the semantic precondition and issues its native decision receipt.

### Causal event projection

Each event contains event ID, previous event digest when persisted, dispatch/run/attempt/transition IDs, event kind, producer, native receipt handle/digest, projected status, timestamp/sequence, and residue. Persistence is local-owner policy, not a mandatory global store. The projection never stores private payloads by default and never changes the native result.

### Compatibility declaration

Each semantic owner publishes or generates a local declaration:

- accepted OBTC versions;
- accepted adapter versions;
- native artifact/receipt schemas;
- unknown-field behavior;
- downgrade/rollback behavior;
- single authoritative write path;
- shadow-read comparison window;
- cutover and retirement evidence.

## 4. Workflow process view

### Normal owner chain

1. Invoke emits `AuthoredWorkPack`.
2. WPRA consumes it and emits `FrozenWorkPackSnapshot` with `authority_effect:none`.
3. WPRA selection verifier emits non-authoritative `SelectedUnitReceipt`.
4. Task Session consumes current selection and emits `ConsumerEntryReceipt`.
5. The bound material producer emits its native `MaterialPackageReceipt`; absence blocks.
6. Task Session rehashes live state, performs effect-boundary CAS/lease checks, and emits one-use `MutationAdmissionReceipt`.
7. Task Session executes one SWU and emits `ExecutionTerminalReceipt`, or `OutcomeUnknownReceipt` if an effect may have occurred without durable terminal proof.
8. An unknown outcome routes to the effect owner for reconciliation; no automatic retry is legal.
9. For known execution terminal, Task Session prepares closeout from immutable pre-execution state.
10. Continuation Router dispatches exactly one Refresh owner hop.
11. Refresh emits `CloseoutMutationReceipt` or validated no-op.
12. Continuation Router emits `OwnerJoinReceipt` referring to the Refresh receipt.
13. Task Session emits `SynchronizedResultReceipt`, then its continuity cursor from the post-Refresh snapshot.
14. The series owner consumes the cursor and decides frontier advancement under its own reducer.

Every step may project an OBTC and journal event; neither projection causes the next step.

### Crash/concurrency workflow

- Before effect: baseline/lease mismatch blocks with no effect.
- During effect with no durable result: record `outcome_unknown`; prohibit retry.
- Effect owner reconciles observed reality using the idempotency key and exact scope.
- Reconciliation returns `effect_absent`, `effect_committed`, or `manual_resolution_required`.
- Only a receipt-backed result can reopen closeout or a bounded retry.

## 5. Decision flow view

| Question | Owner | Result |
|---|---|---|
| Is the envelope structurally valid? | OBTC validator | pass/block; no effect authority |
| Is the protocol version supported? | consumer semantic owner | owner-native compatibility receipt |
| Is the Work Pack frozen and semantically selectable? | WPRA | audit/selection receipt, authority none |
| Can this exact unit enter and mutate now? | Task Session | entry and admission receipts |
| Is the material package valid? | producer validates production; Task Session validates consumption | separate receipts |
| Did the effect complete? | Task Session/effect owner under its native contract | terminal or outcome-unknown receipt |
| May closeout mutate planning state? | Refresh | closeout mutation/no-op receipt |
| Was owner work joined? | Continuation Router | correlation/join receipt |
| Is the Task Session synchronized? | Task Session | synchronized result and continuity cursor |
| May the ordered frontier advance? | proposed Implementation Readiness owner | series transition receipt |
| May a capability change lifecycle status? | Sigil Development or Spellcraft | lifecycle decision receipt |
| May it enter a registry? | unresolved registry owner | block until bound |

### Required Decision Gate packet

Recommend `Implementation Readiness` as the sole ordered-series runtime owner and convert `task-session-until-blocker` to a stateless compatibility profile. This recommendation requires explicit owner/lifecycle acceptance before implementation.

Material-producer, registry-release, and protocol-steward bindings remain separate decision packets. Protocol stewardship may be assigned with `authority_effect:none`; consumer version acceptance remains owner-local.

## 6. Dependency and interface view

| Interface | Producer-native authority | Projection/transport | Consumer-native decision |
|---|---|---|---|
| Invoke → WPRA | Invoke Plan artifact receipt | bilateral adapter + OBTC | WPRA audit/freeze |
| WPRA → Task Session | WPRA selection receipt, authority none | bilateral adapter + OBTC | Task Session entry/admission |
| Material Producer → Task Session | producer package receipt | bilateral adapter + OBTC | Task Session consumption/admission |
| Task Session → Refresh | execution terminal + closeout package | Continuation Router transport | Refresh apply/no-op |
| Refresh → Task Session | Refresh owner receipt | Continuation Router join | Task Session synchronized result |
| Task Session → Series Owner | continuity cursor | bilateral adapter + causal event | Implementation Readiness frontier advance |
| Lifecycle → Registry | lifecycle receipt | blocked adapter slot | registry owner release decision |
| Canonical → Generated | canonical package identity | sync generator + parity manifest | runtime package parity verifier |

### No-cycle rule

Closeout binds an immutable pre-execution snapshot. Refresh produces a separate post-refresh snapshot. Task Session derives synchronization/cursor only from the joined post-refresh identity. The series owner advances only after that cursor. No transition may require an artifact produced by a later transition in the same attempt.

## Decisions

| ID | Decision | Status |
|---|---|---|
| `DESIGN-ABP-001` | Use hybrid protocol plus non-authoritative causal journal. | candidate accepted for planning |
| `DESIGN-ABP-002` | Migrate bilateral adapter first; no universal flag day. | candidate accepted for planning |
| `DESIGN-ABP-003` | Kernel validation is structural only. | invariant |
| `DESIGN-ABP-004` | Native owner receipt remains authoritative during shadow comparison. | invariant |
| `DESIGN-ABP-005` | Task Session produces synchronized result and current continuity cursor; series owner only consumes it. | preserves current contract |
| `DESIGN-ABP-006` | No automatic retry after indeterminate effects. | invariant |
| `DESIGN-ABP-007` | Implementation Readiness is recommended series owner; spell becomes facade. | pending Decision Gate/lifecycle acceptance |

## Critic repair matrix

| Counterexample | Design response | Status |
|---|---|---|
| `CRITIC-AUTH-001` | Structural-only validator; owner-native semantic receipt. | repaired in design |
| `CRITIC-AUTH-002` | Non-authoritative steward plus owner-local version acceptance. | repaired; steward identity pending |
| `CRITIC-OWNER-001` | Split authored and frozen Work-Pack records. | repaired |
| `CRITIC-OWNER-002` | Material producer remains blocking port. | preserved residue |
| `CRITIC-OWNER-003` | Split terminal, closeout effect, join, synchronized result, cursor, and series advance. | repaired; series decision pending |
| `CRITIC-OWNER-004` | Type lifecycle route; registry remains blocked. | preserved residue |
| `CRITIC-FRESH-001` | One immutable operator approval receipt. | repaired in design; current run binding is separately evidenced by `receipts/operator-approval.json` |
| `CRITIC-REPLAY-001` | Outcome-unknown and owner reconciliation; no exactly-once claim. | repaired in design; evidence pending |
| `CRITIC-REPLAY-002` | Effect-boundary CAS/lease and concurrency scope. | repaired in design; evidence pending |
| `CRITIC-CYCLE-001` | Immutable pre-state, post-Refresh snapshot, then cursor and series advance. | repaired |
| `CRITIC-PROOF-001` | Separate toy-game and real witness obligations. | preserved proof ceiling |
| `CRITIC-MIG-001` | Bilateral adapters, shadow reads, one writer, version rules. | repaired in design |
| `CRITIC-PRIV-001` | Handles/digests only by default; classification and scan gate. | repaired in design; evidence pending |

## Risks and residue

- exact material producer, registry owner, and protocol steward identity remain unbound;
- series-owner lifecycle acceptance remains pending;
- crash/concurrency design is unexecuted;
- journal semantics and retention need owner review;
- adapter extraction could still over-generalize after one boundary;
- canonical/generated parity and both Orchestrate repairs remain open;
- real positive E2E remains unverified;
- private payload scans are planned, not executed.

## Design selection evidence

- Scope manifest: `stages/06-design-scope-manifest.json`
- Denominator receipt: `stages/06-design-denominator-receipt.json`
- Selection result: `stages/06-design-selection-result.json`
- Verdict: `pass`
- Fixed point: true
- Evidence state: `design-validator-pass`
- Diagnostics: none
- Plan evidence: `plan-evidence-pending`

## Dispatch technique trace

`frame_handoff`, `handle_handoff`, `x_ray`, `component_descriptor`, `entity_component_reference`, `unique_standard_component`, `owner_boundary_check`, `validation_loop`, `residue_ledger`, and `protected_context_flag` directly shape the six views, module catalog, owner matrix, repair table, and private/public gate.

## Invoke Result

- Mode: design
- Spell: invoke
- Canonical ID: invoke
- Scope: library authoring applied to a private Refine candidate
- Phase status: pass
- Mode contract: `spells/invoke/design.md`
- Outputs: `stages/06-invoke-design.md`, `stages/06-glossary-consistency.md`, `stages/06-design-transport.md`
- Design views: all six present
- Design selection receipt: `stages/06-design-selection-result.json`
- Design evidence state: design-validator-pass
- Evidence ceiling: Design validation only; Plan and execution evidence are separate
- Plan evidence: plan-evidence-pending
- Template/profile selection: DomainSpec architecture profile with architecture, failure, persistence/concurrency, state/event, integration/versioning, data lifecycle, quality, and validation companions
- Distill validation: pass from Stage 5 with critic repairs carried forward
- Implementation layering: `stages/06-layering-seed.md`
- Work-pack: n/a
- Decisions: hybrid D target, bilateral-adapter-first migration, structural-only kernel
- Unresolved gaps: owner identities, series lifecycle acceptance, implementation evidence, parity, real E2E
- Next route: refine-design-review
