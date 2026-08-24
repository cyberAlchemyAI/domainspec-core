---
module: animejs-agent-knowledge-api
version: candidate-0.1.0
status: plan-pass-execution-not-admitted
updatedAt: 2026-08-04
docType: work-pack
---

# WORK-PACK: Anime.js Agent Consultation and Work Episodes API

## Control fields

| Field | Value |
| --- | --- |
| workPackGateStatus | artifact-authored; readiness and SWU selection pending |
| complexity | medium |
| outputMode | split |
| activeLayerWindow | none selected; L0 recommended first |
| designEvidence | `design-validator-pass` |
| distillValidationStatus | pass for plan structure |
| swuAtomicityStatus | pass; ten one-behavior units |
| firstUnitNarrownessStatus | pass; `SWU-AKVE-001` |
| closeoutSyncStatus | contract-complete; receipts absent until execution |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) |

## Objective and delivery boundary

Implement a candidate-local, transport-neutral API core that lets agents:

1. consult an allowlisted neutral projection of the Anime.js knowledge vault;
2. append immutable WorkEpisode events bound to exact Task,
   VersionContext, owner, graph, and evidence context; and
3. query deterministic episode snapshots without acquiring authority, truth,
   Task-state, canonical graph, or Lesson-verification effects.

Implementation target:
`projects/animejs/ontology/agent-knowledge-vault/operational/`.

This Work Pack does not ingest documentation, rewrite the existing vault,
integrate ResonantOS/Augmentor, expose HTTP, deploy, promote, or verify Lessons.

## Task board

| Task | Goal | Layer | Wave | Status |
| --- | --- | --- | --- | --- |
| [TASK-AKVE-01](work-pack/tasks/TASK-AKVE-01-CONTRACTS.md) | close projection and episode schemas | L0 | W0 | planned |
| [TASK-AKVE-02](work-pack/tasks/TASK-AKVE-02-TRANSITIONS.md) | implement pure episode state oracle | L0 | W1 | planned |
| [TASK-AKVE-03](work-pack/tasks/TASK-AKVE-03-JOURNAL.md) | implement atomic append/idempotency/recovery port | L1 | W1 | planned |
| [TASK-AKVE-04](work-pack/tasks/TASK-AKVE-04-PROJECTION.md) | implement reducer and isolated overlay compiler | L1 | W1 | planned |
| [TASK-AKVE-05](work-pack/tasks/TASK-AKVE-05-SERVICES.md) | implement consultation and episode services | L2 | W2 | planned |
| [TASK-AKVE-06](work-pack/tasks/TASK-AKVE-06-INTEGRATION-HARDENING.md) | bind capabilities and prove integrated failures | L2 | W3 | planned |

## SWU manifest

| SWU | Parent | Primary behavior | Depends on | Verification surface | Successor |
| --- | --- | --- | --- | --- | --- |
| SWU-AKVE-001 | TASK-AKVE-01 | neutral projection schema, allowlist, leakage fixtures | none | contract tests: projection | 002 |
| SWU-AKVE-002 | TASK-AKVE-01 | episode command/event/result schemas and closed codes | 001 | contract tests: episode | 003 |
| SWU-AKVE-003 | TASK-AKVE-02 | pure closed transition oracle | 002 | transition matrix | 004 |
| SWU-AKVE-004 | TASK-AKVE-03 | atomic journal, idempotency, receipt recovery | 003 | crash/concurrency tests | 005 |
| SWU-AKVE-005 | TASK-AKVE-04 | deterministic version-keyed reducer | 004 | replay/integrity tests | 006 |
| SWU-AKVE-006 | TASK-AKVE-04 | isolated episode overlay and neutral projection compiler | 005 | leakage/zero-write tests | 007 |
| SWU-AKVE-007 | TASK-AKVE-05 | bounded consultation service | 006 | consultation result algebra | 008 |
| SWU-AKVE-008 | TASK-AKVE-05 | episode command service and host resolvers | 007 | lifecycle/evidence tests | 009 |
| SWU-AKVE-009 | TASK-AKVE-06 | disjoint capability adapters and opaque authorization | 008 | security boundary tests | 010 |
| SWU-AKVE-010 | TASK-AKVE-06 | full local validator and operational documentation | 009 | all thirty scenarios | terminal |

Task files are the source of truth for algorithms, exact write inventories,
split analysis, validation, and closeout contracts.

## Atomicity and narrow-first proof

| SWU | Plausible split | Why retained as one unit |
| --- | --- | --- |
| 001 | schema vs leakage cases | an allowlist without negative mutants is not independently trustworthy |
| 002 | command/event/result files | they share one closed status and digest vocabulary; partial acceptance is contradictory |
| 003 | transition table vs oracle | the table is executable only through the pure decision function and its matrix |
| 004 | compare-append vs idempotency vs recovery | they are one atomic commit-observability boundary |
| 005 | replay vs snapshot hashing | deterministic state bytes are the behavior being accepted |
| 006 | overlay vs projection | both enforce the single derived-writer, no-canonical-write boundary |
| 007 | query planning vs result formation | one bounded consultation behavior owns both budgets and tagged results |
| 008 | lifecycle vs host resolution | commands are unsafe unless context/evidence bindings are resolved in the same pre-append decision |
| 009 | four adapters vs denial behavior | route separation is accepted only as one capability matrix |
| 010 | validator vs README | documentation records the exact runnable acceptance surface; neither adds product behavior |

`SWU-AKVE-001` is the narrowest reversible trust-building step: it writes only
projection contract material and proves forbidden fields fail before any
episode mutation mechanism exists.

## Validation strategy

- Use Node's built-in test runner and temporary directories; do not add a
  package root or external dependency.
- Every SWU has a targeted command. `SWU-AKVE-010` runs the aggregate validator
  twice and compares deterministic receipts/digests.
- Fixture assertions cover all scenarios in
  [08-toy-scenarios.md](stages/08-toy-scenarios.md).
- Validation must prove zero writes outside `operational/`, zero modifications
  to current vault nodes/relations/views, zero verified Lessons, and zero Task
  state effects.

## Task Session closeout policy

Every SWU's task contract supplies the exact target inventory, admitted delta
classes, validation command, stable terminal/owner/continuation receipt paths,
and successor. Before mutation, Task Session must:

1. capture presence plus SHA-256 for every declared target;
2. require all currently planned targets to be absent, or stop for an updated
   baseline when repository state has changed;
3. reject any write outside that SWU's inventory;
4. join the targeted validation result and owner closeout receipt; and
5. run Continuation Router verification before naming the unique successor.

Planned receipt root:
`projects/animejs/development/refinement-runs/20260804-agent-consultation-work-episodes-api/task-sessions/<SWU-ID>/`.

No receipt exists yet. A plan path is not a runtime receipt.

## Dispatch technique trace

| Technique | Applied result |
| --- | --- |
| sequence | W0 → W1 → W2 → W3 dependency order |
| scu_swu_reduction | ten atomic SWUs; 001 is the narrow first unit |
| recomposition_proof | [traceability.md](work-pack/shared/traceability.md) maps every design invariant to SWUs |
| validation_loop | targeted command and evidence receipt per SWU |
| owner_boundary_check | candidate vault only; consumer, deployment, and Lesson owners deferred |
| handle_handoff | source paths and opaque Task/Evidence handles, not copied authority |
| residue_ledger | [gaps.md](work-pack/shared/gaps.md) owns all remaining decisions |
| execution_receipt_handoff | stable terminal, owner, and continuation receipts per SWU |

## Execution gate

Planning passes. Mutation does not. The next safe route is
`work-pack-readiness-audit` over this immutable frontier, followed by explicit
selection of exactly one SWU and a fresh `task-session`. No readiness result may
implicitly select or execute a unit.

