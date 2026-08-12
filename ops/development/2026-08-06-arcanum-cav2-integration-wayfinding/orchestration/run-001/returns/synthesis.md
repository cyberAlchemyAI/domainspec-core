# Synthesis return — Beer, Stafford

## Synthesis verdict

`SYNTHESIS_PASS / NO_VERTICAL_WITNESS / DECISION_READY_ONLY`.

The three explorer returns support a modular route to a first semantic witness, but they do not support claims of current implementation readiness, synchronization, release, publication, deployment, or whole integration.

The leading semantic candidate is the **intent-route resolver (`VS-IRO-001`)**, conditionally selected for planning comparison only. An existing-package delivery canary is a required reusable predecessor proof, not itself a meaningful CAV2 vertical integration.

### Evidence binding

- `P = 9fb9fa9abba389fe49bc07867222541107840af0` — parent/CAV2 current identity.
- `A = a5c8bc5c010711721063e258ee92559f02dfc504` — Arcanum current identity.
- `R1` — `research.md`, Agent 1, authority admission, lines 7–169; receipt `spawn-0001`, pass.
- `R2` — `research.md`, Agent 2, lifecycle/control, lines 172–354; receipt `spawn-0002`, pass.
- `R3` — `research.md`, Agent 3, runtime delivery, lines 356–582; receipt `spawn-0003`, pass.
- CAV2 and `ops/` selectors below bind to `P`; `arcanum/` selectors bind to `A`, unless an artifact digest is stated.

## Integration-state vocabulary

These are candidate operational definitions, not canonical definitions.

| Claim ID | State | Exact definition | Evidence, privacy, owner, non-effects and ceiling |
|---|---|---|---|
| `DEF-PARTIAL-001` | **Partial** | At least one declared integration edge has evidence, while one or more required edges for the frozen scope remain absent, blocked, stale, or unjoined. Every use must name both proved and missing edges. | `R1:A0-A8`, `R2` verdict and S0–S14. Privacy follows each artifact. No implied admission or downstream transition. Ceiling: named edges only. |
| `DEF-OPERATIONAL-001` | **Operational** | The exact installed package/adapter identity is host-callable and passes frozen positive, boundary, invalid, replay, mismatch, zero-effect, and rollback checks in its declared environment. | `R3:398-411`, especially stages 3–8. Host/runtime and semantic owners remain separate. Does not imply synchronization, authority, release, deployment, or publication. |
| `DEF-SYNC-001` | **Synchronized** | Terminal execution evidence has been separately joined by Invoke Refresh/Continuation Router, Craft, CAV2 Inventory, and Signal Observer, with common correlation identities and verified pre/post digests. | `R2:S10-S14`, direct selectors `task-session/SKILL.md:351-401`, `invoke/refresh.md:185-255`, `craft/ARCHITECTURE.md:138-178,245-260`, `cyberAlchemy-v2/inventory/README.md:1-19`, `signal-observer/SKILL.md:12-115`. Private. Read models do not gain semantic authority. |
| `DEF-VERTICAL-001` | **Vertical integration** | One selected, finite consumer use case is authority-admitted, lifecycle-executed, operational, evidence-closed, synchronized, and reversibly dispositioned across all owners required by that slice. Release and publication are outside this state unless explicitly included. | Composition of `R1:A0-A7`, `R2:S0-S14`, `R3` stages 0–9. No current instance exists. Ceiling after a pass: “one synchronized CAV2 lifecycle slice passed.” |
| `DEF-RELEASED-001` | **Released** | A separately named release owner accepts a versioned immutable artifact, provenance closure, distribution boundary, and rollback policy. | `R1:A8`; `boundaries.md:6-14,58-75`, `promotion-policy.md:16-18,41-45`. Release is neither deployment nor publication. No witness exists. |
| `DEF-PUBLISHED-001` | **Published** | A public-boundary owner and publisher approve scrubbed bytes and those exact bytes are verified on the declared public surface. | `R1:A8`. Private-to-public review is mandatory. Publication does not prove runtime operation, release, or deployment. No witness exists. |
| `DEF-WHOLE-001` | **Whole integration** | Closure over a frozen scope manifest, not a monolithic boolean: every in-scope module has an explicit required target state; all required inter-module edges and negative controls pass; all unresolved blockers are zero; release, deployment, and publication are each explicitly included or excluded. | Dispatch goal plus `R1:A0-A8`, `R2` no-witness verdict, and `R3` modular contract. A bounded “whole internal integration” may explicitly exclude release/publication, but must say so. No witness exists. |

Deployment remains an independent state: authorized operation in a target environment plus health and rollback evidence.

## “You are here” matrix

| ID | Dimension and current state | Binding and explorer proof | Owner, privacy, non-effects and ceiling |
|---|---|---|---|
| `CS-AUTH-001` | Documentary/import consumer only; no locally admitted import. | `R1:A0-A4`; `SOURCE-MAP.md:10-33`, `authority/imports/README.md:3-32`. | CAV2 import and semantic owners; private ledger referencing public sources. Manifest or Git presence does not admit authority. |
| `CS-CONST-001` | Stable Repository Constitution has mixed candidate/project-local signals; selected rules are not uniformly canonical. | `R1` edge-case 3; `STABLE-REPOSITORY-CONSTITUTION.md:1-12,371-405`; `AUTHORITY-MODEL.md:144-151`. | Constitution Governance plus Decision Gate. Cannot support a governing adapter until adjudicated. |
| `CS-LIFE-001` | No CAV2 S0–S14 full-chain witness. | `R2` verdict; FSM `S0-S14`. OAVA-002 is near-full generic precedent; OEWFR and IOLM are bounded CAV2 partials. | Invoke, readiness, Task Session, Router, Craft, Inventory, and observer retain distinct ownership. Ceiling: precedent and requirements only. |
| `CS-IRO-001` | IRO has private candidate behavior and browser parity, but `SWU-IRO-004` is blocked by a source-frontier mismatch. | `R3:455-479`; manifest closure `5ff017...ab8f`, file SHA-256 `ebc019...a32`, boundary `b17d50...a835`, source/license/API receipt `ebd67b...1f3b`. | Private CAV2 plus future public/package owners. Current ceiling: portable candidate behavior; no canonical or installed package. |
| `CS-DELIVERY-001` | Orchestrate/Inventory provide canary material; parity and installation closure are incomplete or uneven. | `R3:373-396`; Orchestrate manifests `1fb591...7e0`; Inventory manifest `15e764...5146`; repo config `b69c71...5df`. | Arcanum generator and host owners. Byte parity is not install/callability proof. |
| `CS-DRIFT-001` | Generated Discipline Governance drift and observability-version drift remain. | `R3` evidence table; canonical `0.2.2` vs host `0.2.1`; installed observer `0.1.0` vs guidance `0.2`. | Projection/observability owners. Drift blocks exact-identity claims but does not alter canonical authority. |
| `CS-SYNC-001` | Craft automation contract and local CAV2 machine Inventory are absent. | `R2:S12-S13`; `craft/ARCHITECTURE.md:138-178,245-260`; `cyberAlchemy-v2/inventory/README.md:1-19`. | Craft and Inventory owners. Existing receipts or README cannot manufacture synchronized state. |
| `CS-RELEASE-001` | No release, deployment, or publication witness. | `R1:A8`; `R3` stages 9 and candidate ceilings. | Separate release, deployment, boundary, and publisher owners. All corresponding claims are forbidden. |
| `CS-WHOLE-001` | Whole integration is absent. | Intersection of `CS-AUTH-001`, `CS-LIFE-001`, `CS-SYNC-001`, and `CS-RELEASE-001`. | No meta-owner is created. Ceiling: qualified documentary/partial integration only. |

## Typed owner-and-artifact dependency graph

The type names below are logical handoff labels, not proposed canonical schemas.

```text
[P] SourceLock
 → [P] ImportDisposition
 → [P] SemanticAcceptance / DecisionGateVerdict
 → [P] InvokeArtifacts + finite WorkPack
 → [P] ReadinessReport + SelectionReceipt
 → [P] TaskSession admission → execution → reconciliation
 → [P] GeneratedClosure → InstalledClosure → CallabilityReceipt
 → [P] PrivateAdapter + BehavioralReceipt
 → [P] RouterJoin + InvokeRefreshReceipt
 → [P] CraftReceipt + InventoryProjectionReceipt + ObserverReceipt
 → [P] VerticalDisposition

[O] VerticalDisposition → ReleaseReceipt
[O] Release/accepted private state → PublicBoundaryReview → PublicationReceipt

[L] source/license review, disposable-target preparation, fixture closure,
    receipt-supplement design, and observability privacy review

[X] Inventory/Craft/ontology/test/Git/installed bytes → semantic admission
[X] Task Session → semantic ownership or promotion
[X] Refresh success → successor execution
[X] generated parity → installation or callability
[X] operational evidence → synchronized/released/published/deployed
```

`[P]` is a required predecessor, `[L]` parallelizable preparation, `[O]` optional later extension, and `[X]` forbidden shortcut.

The owner bindings come directly from `R1:A0-A8`, `R2:S0-S14`, and `R3:398-411`. No new meta-owner, registry, validator, adapter authority, or lifecycle controller is introduced.

## Candidate verdict matrix

| Rank / ID | Candidate verdict | Why | Current blockers and ceiling |
|---|---|---|---|
| 0 / `CAN-CANARY-001` | **Required predecessor preparation** | Existing Orchestrate or Inventory can prove generation/install/callability/rollback mechanics cheaply. | Run-global action-ID residue, incomplete install provenance, config/presence drift. Ceiling: reversible read-only delivery canary, never CAV2 semantic integration. |
| 1 / `VS-IRO-001` | **Leading semantic candidate; conditionally selected for Invoke comparison** | Strongest bounded behavior, exact closure digests, Node/Chromium parity, zero forbidden effects. | Blocked IRO-004 frontier, no public canonical admission, host install, consumer/orchestrator gate, private CAV2 admission, or synchronized lifecycle. Not selected for execution. |
| 2 / `CAN-AOV-001` | **Defer** | An authority-object validator could become a semantic keystone. | Conceptual node model, unresolved lifecycle/status axes, no canonical schema or executable validator. Ceiling: ontology proposal. |
| 3 / `CAN-AGI-001` | **Hold** | Useful artifact-form enforcement if owners and fixtures are repaired. | Stale imports, mixed constitution status, metadata conflict, absent local rules/tools, nondiscriminating malformed-YAML negative. Ceiling: committed unexecuted plan. |

## Critical path for `VS-IRO-001`

1. **Source/residue lock.** Bind `P`, `A`, IRO closure/member hashes, privacy boundary, exact current plan epoch, and live baseline. Rebind the Task Session dirty-runtime residue before portable execution claims.

2. **Selection and semantic gate.** A named CAV2 runtime-contract semantic owner must accept the intended meaning and claim ceiling. The current missing owner is a hard stop.

3. **Resolve IRO-004 frontier.** The controlling source owner must return a fresh accepted frontier. The current blocked mutation receipt cannot be bypassed.

4. **Public canonical admission.** The public package owner independently accepts the public-safe source/package. No private prose or authority crosses outward.

5. **Invoke/readiness.** Invoke may author the candidate Work Pack and exact closeout inventory; WPRA audits immutable bytes; a separate selector may choose one unit. None of these steps supplies semantic authority.

6. **Task Session execution.** Consume one single-use admission, produce exact postimages and discriminating validations, reconcile planned writes, and stop on any critical failure.

7. **Generated/runtime delivery.** Prove both-host generated closure, disposable installation, exact installed identity, callability, invalid/missing-package negatives, disable/uninstall, and exact baseline restoration.

8. **Consumer/orchestrator predecessor.** Preserve the current plan’s ResonantOS plan and orchestrator-adapter gates. Reordering private CAV2 admission earlier requires a plan-owner decision.

9. **Private CAV2 adapter admission and behavior.** Admit only a thin private adapter with explicit authority kind and effect ceiling. Run the frozen IRO behavior and host integration suite.

10. **Evidence closure.** Continuation Router selects only the declared Invoke Refresh owner, joins exactly one receipt, and emits an unexecuted successor cursor.

11. **Synchronization.** Craft, CAV2 Inventory, and Signal Observer separately bind the same tuple and verify their own pre/post state.

12. **Disposition.** Public/package and private/CAV2 owners independently admit, revise, reject, or defer the layers they own. Optional release/publication remains later.

Parallel lanes after candidate selection: source/license/privacy review, fixture closure, disposable target preparation, rollback bundle design, receipt-correlation supplement, and observer privacy review.

## Finite acceptance contract: `AC-IRO-001`

`VS-IRO-001` passes only if every `AC-*` row passes and no `STOP-*` condition fires.

| ID | Required proof | Single-fault negative / stop | Binding and owner |
|---|---|---|---|
| `AC-01` | Frozen parent, Arcanum, package, plan epoch, source and fixture closure. | Stale source, changed digest or epoch must fail before planning. | `R1:A0-A2`; `R2:S0-S5`; source/import owners. |
| `AC-02` | Named CAV2 runtime-contract semantic-owner acceptance with privacy and claim ceiling. | Missing, ambiguous or refusing owner stops. | `R1:A3`; `R2:S1`. Task Session, tests and ontology are forbidden substitutes. |
| `AC-03` | Fresh accepted IRO source frontier replacing the blocked IRO-004 prerequisite. | Existing mismatch continues to produce no mutation. | `R3:455-479`; controlling source owner. |
| `AC-04` | Public canonical package acceptance and exact public-safe closure. | Private leakage or unapproved public bytes fail closed. | IRO hashes in `CS-IRO-001`; public package and boundary owners. |
| `AC-05` | Invoke Plan binds finite writes, validations, rollback, terminal output, Craft, Inventory and observer closeout. | Missing closeout target or excess effect blocks readiness. | `R2:S2`; `invoke/plan.md:167-238,361-417`. |
| `AC-06` | WPRA semantic-ready report plus one explicit selection receipt. | Failed readiness, stale unit digest or ambiguous selection blocks entry. | `R2:S3-S5`. |
| `AC-07` | Clean Task Session fast entry, exact baselines and one atomically consumed admission token. | Reused token, wrong owner, write overlap or baseline drift produces no mutation. | `R2:S5-S7`; `task-session/SKILL.md:148-199,260-319`. |
| `AC-08` | Reconciled execution with exact postimages and no undeclared writes. | Critical validation failure or postimage mismatch prevents successful closeout. | `R2:S8-S9`; `task-session/SKILL.md:321-349`. |
| `AC-09` | Generated Codex/Claude closures equal the accepted canonical package and manifest. | Version/member/hash drift fails before installation. | `R3` stages 1–2 and current drift evidence. |
| `AC-10` | Disposable install binds source ref, archive/stage digest, host profile, installed closure and durable restoration material. | Wrong installed identity or missing member fails callability. | `R3` stages 3–4. Current synchronizer/installer receipts are insufficient alone. |
| `AC-11` | Positive entrypoint plus invalid payload, missing capability and zero-undeclared-effect tests. | Any effect call or missing-package success is failure. | `R3` stages 4–6. |
| `AC-12` | Frozen IRO suite reruns: current 23 Node and 6 Chromium cases, including the 17 fixed cases, comparison/browser parity, ambiguity/invalidity and zero-effect behavior. | Any parity difference, replay/mismatch acceptance or forbidden call fails. | `R3:455-471`; private CAV2 semantic/evidence owners. |
| `AC-13` | Disable/uninstall proves unavailability and restores exact pre-state with no residual files/process/config. | Restoration digest mismatch blocks disposition. | `R3` stage 8; host owner. |
| `AC-14` | Router/Refresh binds exact targets, one fingerprint, one dispatch/join, and `successor_executed:false`. | Duplicate fingerprint, excess target or missing join fails closure. | `R2:S10-S11`; Router and Invoke owners. |
| `AC-15` | Craft receipt binds ledger pre/post digests and row IDs; Inventory receipt binds local machine-index pre/post digest and sources. | Invalid Craft row or unsupported Inventory source fails synchronization only; prior authority is unchanged. | `R2:S12-S13`. Current machinery is absent/underspecified. |
| `AC-16` | Observer receipt binds the exact appended event, package/input/output digests, privacy class and dedupe key. | Append failure or duplicate event prevents “observed/synchronized.” | `R2:S14`; `R3` stage 7. |
| `AC-17` | Multi-wave Orchestrate action identities are unique and correlate target/input/output/package digests. | Duplicate or mismatched action identity stops Orchestrate-dependent acceptance. | `R3` defects 1–2. No implementation repair is selected here. |
| `AC-18` | Separate owner disposition states precisely which public and private layers are admitted. | Missing release/deployment/publisher owner keeps those dimensions false. | `R1:A6-A8`; `R3` stage 9. |

## Modular phases and claim ceilings

| Phase | Output | Maximum claim |
|---|---|---|
| `PH-0 Source lock` | Immutable identities, closure, privacy boundary, residue register | Source-qualified candidate |
| `PH-1 Owner admission` | Semantic verdict, import disposition, public/private owner routes | Admitted meaning or classified candidate only |
| `PH-2 Invoke/readiness` | Candidate Work Pack, closeout inventory, readiness and selection receipts | Ready selected task; no execution |
| `PH-3 Task Session` | Admission, postimages, validation and reconciliation receipts | Bounded validated execution |
| `PH-4 Delivery` | Generated/staged/installed/callable/rollback closures | Operational delivery |
| `PH-5 Evidence closure` | Router join, exact Refresh, successor cursor | Lifecycle-closed execution |
| `PH-6 Synchronization` | Craft, Inventory and observer owner receipts | One synchronized slice |
| `PH-7 Disposition` | Independent public/private owner decisions | One vertical integration witness, if all prior phases passed |
| `PH-8 Optional release/publication` | Release, deployment and/or publication receipts | Only the specifically approved later state |

## Stop, rollback and demotion routes

| Stop ID | Trigger | Required route |
|---|---|---|
| `STOP-AUTH-001` | Stale import, duplicate owner, mixed constitution status, missing semantic owner | Stop before planning; defer/reference/skip or route to the existing owner/Decision Gate. |
| `STOP-READY-001` | Failed readiness, epoch drift, ambiguous selection | No admission or mutation; repair authoring inputs and re-audit. |
| `STOP-EXEC-001` | Replay, overlap, critical failure, postimage mismatch | Fail transaction; restore implementation bytes. Do not demote semantic authority automatically. |
| `STOP-DELIV-001` | Generated or installed identity mismatch | Delete isolated stage or disable/uninstall; restore exact pre-state. |
| `STOP-PRIV-001` | Private material enters a public candidate | Reject public transition and restore public boundary; require explicit scrub review. |
| `STOP-JOIN-001` | Missing Router/Refresh join | Retain only executed/validated claim; emit no synchronized state or successor execution. |
| `STOP-SYNC-001` | Craft, Inventory or observer failure | Keep canonical and execution evidence intact; rebuild/expire only the projection owned by the failing system. |
| `STOP-REL-001` | No release/deployment/publication owner | End at the admitted or synchronized slice; prohibit later-state language. |

There is no verified generic demotion runner. Governing authority demotion must return through its owning governance route; candidate adapters can simply be removed if never promoted.

## Conflicts, disagreements and missing owners

- `D-AUTH-001`: CAV2 runtime-contract semantic ownership is unnamed. Hard blocker.
- `D-CONST-001`: Stable Repository Constitution mixes candidate and project-local authority signals.
- `D-ORDER-001`: The generic lifecycle requires early semantic acceptance, while the current IRO plan places private CAV2 admission after consumer/orchestrator gates. The bounded reconciliation is early acceptance of intended meaning plus later admission of exact adapter bytes; any other reordering needs the plan owner.
- `D-SLICE-001`: The delivery canary is technically shortest but semantically insufficient. It remains a predecessor, not the selected semantic slice.
- `D-CRAFT-001`: Craft lacks a stable deterministic route-exchange/update contract for automated closeout.
- `D-INV-001`: CAV2 has no local machine Inventory index/owner receipt route.
- `D-RUN-001`: Run-global Orchestrate action-ID allocation can collide across waves. The explorer reports `len(current_actions)+1`, but provides no direct allocator-file selector. This remains runtime residue and an evidence gap; no code change is proposed or treated as repaired.
- `D-CORR-001`: Current receipt correlation omits target, input/output references, package identity and digests.
- `D-ID-001`: Seed dispatch ID is `2026-08-06-arcanum-cav2-integration-wayfinding`; persisted route receipts use `...-wayfinding-route`. The run must retain the persisted route identity and explicitly relate it to the seed.
- `D-TASK-001`: Current Task Session portable-ID repair exists only as unattributed dirty bytes; clean committed correctness is unverified.
- `D-REL-001`: Slice-specific release, deployment and publisher owners are absent.
- `D-DEMOTE-001`: No generic deterministic authority-demotion mechanism exists.

## Skeptic-gate verdicts

| Gate | Verdict | Reason |
|---|---|---|
| `G-PRECEDENT-001` | `PASS_WITH_BLOCKS` | Every proposed transition routes to an existing narrow owner. Missing owners/contracts are blockers, not newly invented authority. |
| `G-NONVACUITY-001` | `KILL_IMPLEMENTATION_READY / RETAIN_DECISION_READY` | `AC-IRO-001` is finite and discriminating, but cannot currently instantiate because authority, frontier, Craft, Inventory, and runtime residues remain. |
| `G-DEFINITION-001` | `PASS_CANDIDATE` | Documentary, admitted, executable, operational, synchronized, released, deployed, published and whole states remain non-collapsed with explicit ceilings. |

## Invoke-ready candidate boundary

`H-INVOKE-IRO-001` is ready for **Invoke Define/Design intake**, but blocked for approved Plan selection or Task Session admission.

```yaml
intent_id: H-INVOKE-IRO-001
candidate: VS-IRO-001
candidate_status: leading-semantic-candidate-not-execution-selected
goal: >
  Produce one reversible, authority-admitted, operational and synchronized
  CAV2 intent-route witness without external, model, filesystem-persistence,
  dispatch or other undeclared effects.
source_locks:
  parent: 9fb9fa9abba389fe49bc07867222541107840af0
  arcanum: a5c8bc5c010711721063e258ee92559f02dfc504
  iro_closure: 5ff017abf7bf98880b4a0dab7095a7dc59a9aac08993e04fbaa31b808e09ab8f
required_owner_decisions:
  - CAV2 runtime-contract semantic owner
  - IRO source-frontier owner
  - public canonical package owner
  - current ResonantOS/orchestrator plan owner
  - private CAV2 adapter owner
required_predecessor:
  - CAN-CANARY-001 delivery and rollback proof
acceptance_contract: AC-IRO-001
required_closeout:
  - Invoke Refresh and Router join
  - Craft owner receipt
  - CAV2 Inventory owner receipt
  - Signal Observer receipt
forbidden_effects:
  - implicit promotion or authority transfer
  - private-to-public leakage
  - successor execution from a cursor
  - release, deployment, publication or production claims
claim_ceiling: one synchronized CAV2 intent-route slice
plan_authority_effect: none
```

Invoke remains the authoring owner; this synthesis neither authors nor approves its plan.

## Compact receipt proposal

```json
{
  "action_id": "spawn-0004",
  "dispatch_id": "2026-08-06-arcanum-cav2-integration-wayfinding-route",
  "run_id": "arcanum-cav2-wayfinding-20260806-r1",
  "wave_id": "synthesis",
  "step_id": "s2-synthesize",
  "role": "synthesizer",
  "capability_ref": "research",
  "status": "pass",
  "artifacts": [
    "native agent result: exact-binding candidate wayfinding atlas",
    "ops/development/2026-08-06-arcanum-cav2-integration-wayfinding/research.md",
    "ops/development/2026-08-06-arcanum-cav2-integration-wayfinding/receipts/explorer-authority.json",
    "ops/development/2026-08-06-arcanum-cav2-integration-wayfinding/receipts/explorer-lifecycle.json",
    "ops/development/2026-08-06-arcanum-cav2-integration-wayfinding/receipts/explorer-runtime.json"
  ],
  "validation": "pass: all three explorer receipts passed; synthesis preserves direct selectors, privacy, owners, non-effects, claim ceilings, disagreements, stop routes and reviewer-gate IDs; no repository writes",
  "blockers": [],
  "started_at": "2026-08-06T18:56:51Z",
  "finished_at": "2026-08-06T18:57:33Z"
}
```
