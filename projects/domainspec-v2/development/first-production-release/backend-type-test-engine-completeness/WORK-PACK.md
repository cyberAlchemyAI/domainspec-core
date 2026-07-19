---
module: backend-type-test-engine-completeness
version: current
status: decision-synchronized-awaiting-task-session
updatedAt: 2026-07-17
docType: work-pack
---

# Work Pack — Backend Type Test Engine Completeness

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | `ready-after-decision-gate` | FPR-02B Decision Gate is accepted; implementation still requires one separately authorized Task Session. FPR-02U is not a dependency. |
| complexity | `high` | Crosses definitions, profile, compiler, engine, execution evidence, and release validation. |
| outputMode | `split` | Task and wave contracts are required. |
| executionPackRef | `EXECUTION-PACK.md` | Cross-task choreography only. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0–L3 governance. |
| dispatchTechniqueTrace | `EXECUTION-DISPATCH.json` | Must validate before handoff. |
| distillValidationStatus | `flag` | Original owner gate is resolved; successor edge/consumer scope requires a bounded Task Session distill before implementation. |
| activeLayerWindow | `n/a` | No SWU selected. |
| lastUpdatedAt | `2026-07-17T15:00:00-03:00` | Apply-approved FPR-02B integrated consumer-proof refresh. |
| readinessProfile | `release-candidate evidence; non-admission` | No production authorization. |

## Objective Summary

Deliver exact, executable, fail-closed structural verification for all 13 active backend meta-types and 16 backend relationship signatures by reusing canonical YAML criteria, one-file-per-node JSON, and independent edge JSON records. The downstream IOLM and Body War consumers are proof surfaces, not authorities.

Success requires `13/13` admitted and exercised kinds, `16/16` admitted and causally exercised backend signatures, `16/16` current criteria represented in an independently owned obligation catalogue, exact `O_spec/O_gen/T_gen/E_run` equality, integrated BTE/IOLM/Body War receipts, zero skip/todo/orphan/unrunnable items, and killed mutations for required obligations.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-000 | Accepted backend profile, source-root, claim, and consumer-proof decision receipt | gate | W0 | FPR-01 closed; FPR-02 lane split closed; FPR-02B decision accepted | Decision record and digest-bound profile contract. |
| S-001 | Shared criterion kernel and representation adapters | L0 | W1 | S-000 | Existing validator parity plus eight rule-form controls. |
| S-002 | Exact 13-kind node/edge profile and corpus | L1 | W2 | S-001 | 13 positive nodes, 16 positive edges, causal mutants, deterministic graph/source manifest. |
| S-003 | Independent obligations and executable derivation | L2 | W3 | S-002 | Exact-set, execution, mutation, and provenance evidence. |
| S-004 | Fail-closed aggregate, consumer manifest, and non-admission receipt | L3 | W4 | S-003 | Clean replay plus BTE/IOLM/Body War parity and seeded missing/empty/stale/surviving-mutant failures. |

## Task Status Board

| Task | Goal | Layer | Waves | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-BTE-CONTRACT](work-pack/tasks/TASK-BTE-CONTRACT.md) | Shared criterion kernel and successor node/edge profile contract | L0/L1 | W1/W2 | ready after S-000 | not-started |
| [TASK-BTE-NODE-COVERAGE](work-pack/tasks/TASK-BTE-NODE-COVERAGE.md) | Apply YAML criteria to node bodies and exercise all 13 kinds | L0/L1 | W1/W2 | ready after S-000 | not-started |
| [TASK-BTE-EDGE-COVERAGE](work-pack/tasks/TASK-BTE-EDGE-COVERAGE.md) | Resolve independent edge roots and exercise all 16 backend signatures causally | L1/L2 | W2/W3 | depends on CONTRACT/NODE | not-started |
| [TASK-BTE-OBLIGATIONS](work-pack/tasks/TASK-BTE-OBLIGATIONS.md) | Create independent `O_spec` catalogue and receipt | L2 | W3 | blocked by S-002 | not-started |
| [TASK-BTE-DERIVATION](work-pack/tasks/TASK-BTE-DERIVATION.md) | Derive graph-backed obligations and executable tests | L2 | W3 | blocked by S-003 catalogue | not-started |
| [TASK-BTE-INTEGRATION](work-pack/tasks/TASK-BTE-INTEGRATION.md) | Fail-closed release validation and receipts | L3 | W4 | blocked by S-003 | not-started |
| [TASK-BTE-INTEGRATED-CONSUMER-MANIFEST](work-pack/tasks/TASK-BTE-INTEGRATED-CONSUMER-MANIFEST.md) | Bind BTE, IOLM, Body War, and Craft evidence into one manifest | L3 | W4 | depends on INTEGRATION | not-started |
| [TASK-BTE-VERIFY](work-pack/tasks/TASK-BTE-VERIFY.md) | Independent closure review across engine and consumers | L3 | W4 | ready-after-implementation | not-started |

## SWU Manifest

| SWU | Parent | Goal | Dependencies | Write scope | Done criteria | Validation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SWU-BTE-001` | [CONTRACT](work-pack/tasks/TASK-BTE-CONTRACT.md) | Extract shared YAML criterion kernel with no behavior drift | S-000 | `impl/tools/lib/meta-type-criteria.ts`; current content/instance validators and tests | One loader/preflight/evaluator; existing surfaces use adapters; parity green | `npm --prefix projects/domainspec-v2/impl run tools:test`; `typecheck` | local-fallback | blocked |
| `SWU-BTE-002` | [CONTRACT](work-pack/tasks/TASK-BTE-CONTRACT.md) | Bind candidate node/edge profile/version to exact schema paths and digests | S-000, 001 | `definitions/minted-project/`; `impl/spec/minted-project/`; contract tests | Exact 13 kinds and 16 backend signatures; independent roots; current v1 preserved; drift and missing-schema fail | tools tests + profile contract test | manual decision + local-fallback | ready-after-selection |
| `SWU-BTE-003` | [NODE COVERAGE](work-pack/tasks/TASK-BTE-NODE-COVERAGE.md) | Normalize minted node bodies and enforce all rule forms | 001, 002 | `impl/tools/minted-project/`; compiler tests | No type-name branches beyond profile/schema selection; eight rule forms pass/fail | tools tests + typecheck | local-fallback | blocked |
| `SWU-BTE-004` | [NODE COVERAGE](work-pack/tasks/TASK-BTE-NODE-COVERAGE.md) | Build 13-positive/16-mutant corpus | 003 | minted-project backend fixture root and conformance tests | Every kind positive; every criterion mutant fails distinctly; deterministic graph | engine:test + tools:test | local-fallback | blocked |
| `SWU-BTE-005` | [OBLIGATIONS](work-pack/tasks/TASK-BTE-OBLIGATIONS.md) | Produce digest-bound independent `O_spec` catalogue | 002, 004 | this package `contracts/`; FPR evidence run; independent catalogue validator/tests | 16 stable obligation IDs, owner/digest/source anchors; mutation invalidates receipt | catalogue validator + receipt replay | manual validation owner | blocked |
| `SWU-BTE-006` | [DERIVATION](work-pack/tasks/TASK-BTE-DERIVATION.md) | Derive `O_gen` from minted graph/source manifest | 003, 005 | engine minted-project adapter/rules/tests | Deterministic keys; exact source anchors; `O_gen = O_spec`; missing graph fails | engine:test + typecheck | local-fallback | blocked |
| `SWU-BTE-007` | [DERIVATION](work-pack/tasks/TASK-BTE-DERIVATION.md) | Emit and execute one structural test and mutant per key | 006 | engine emitters/tests/backend bindings | 16 runnable tests; 16 killed mutants; no skip/todo/orphan/unrunnable | generated-suite run + engine:test | local-fallback | blocked |
| `SWU-BTE-008` | [INTEGRATION](work-pack/tasks/TASK-BTE-INTEGRATION.md) | Add fail-closed aggregate, required-check manifest, and replayable receipt | 004–007 | `impl/package.json`; engine package; this package run evidence | Missing/empty release witness fails; all suites wired; clean replay stable | backend release command + seeded red controls | local-fallback | blocked |
| `SWU-BTE-009` | [EDGE COVERAGE](work-pack/tasks/TASK-BTE-EDGE-COVERAGE.md) | Bind independent edge schema/roots and causal 16-signature witnesses | 002, 003 | successor profile sources, resolver, edge fixtures | Each backend signature has positive edge, traversal, composition, removal, provenance, and typed negative evidence | resolver tests + deterministic graph replay | local-fallback | blocked-by-predecessors |
| `SWU-BTE-010` | [INTEGRATED MANIFEST](work-pack/tasks/TASK-BTE-INTEGRATED-CONSUMER-MANIFEST.md) | Bind BTE, IOLM, Body War, and Craft receipts into one fail-closed manifest | 008, 009 | consumer contracts and receipts | Exact identity/digest/posture comparison; missing, stale, extra, duplicate, skipped, and surviving evidence fails | manifest validator + replay | validation owner | blocked-by-predecessors |

No SWU is selected. A future mutation-capable handoff must select exactly one dependency-ready SWU and build a strict Context Builder runtime pack at execution time.

## Validation Strategy

1. Authority set: profile kind set exactly equals the 13 selected backend IDs/terms and excludes UI/superseded IDs.
2. Schema integrity: every admitted kind maps to one existing YAML criterion schema with bound digest; duplicate or missing mappings fail.
3. Criterion parity: Markdown, instance, and node adapters produce equivalent rule outcomes for the same logical subject.
4. Node formation: one positive per kind and one negative per criterion; discriminating neighbor mutants cannot pass as both kinds.
5. Determinism/provenance: unchanged nodes produce byte-stable graph, manifest, obligations, generated tests, and receipts; every key resolves to source.
6. Denominator independence: a validation owner freezes `O_spec`; engine output is compared to it rather than defining it.
7. Execution: all generated structural tests run, no skip/todo/orphan/unrunnable state exists, and each mutation is killed.
8. False-green controls: missing source, missing graph, empty release witness, schema drift, profile drift, unknown kind, and surviving mutation all fail nonzero.
9. Integration: the required-check manifest proves engine tests, tool tests, instance validation, typecheck, generated-suite execution, and receipt verification all ran.

## Blocker And Gap Ledger

| ID | Type | State | Owner | Repair path |
| --- | --- | --- | --- | --- |
| `R-BTE-001` | resolved dependency | closed | FPR-02 coordination owner | Backend/UI separation is recorded; UI admission and UI completion are not inputs to this package. |
| `B-BTE-001` | blocker | resolved | FPR-02B claim/semantic owners | Accepted by DEC-FPR02-SUPPORTED-PROFILE; no decision blocker remains. |
| `B-BTE-002` | blocker | resolved | FPR-02B + minted-project contract owner | Successor profile `feature-with-independent-node-and-edge-files@1`, node/edge roots, and direct-body/YAML mapping accepted; implementation still needs Task Session. |
| `G-BTE-001` | gap | active | FPR-02B relationship owner | Exact 16 backend signatures are now in scope; all 16 causal witnesses remain to be built. |
| `G-BTE-002` | gap | deferred | FPR-07 semantic owner | Structural executable checks do not establish business correctness or semantic satisfiability. |
| `G-BTE-003` | gap | deferred | future cross-feature owner | Cross-feature traversal remains unsupported until separately designed and witnessed. |
| `G-BTE-004` | gap | accepted | tooling owner | The current minimal YAML subset remains deliberate; broaden only when a concrete schema needs more YAML features. |
| `G-BTE-005` | gap | active | IOLM consumer owner | `G-DSV2-SG` remains blocked; consumer proof cannot claim authoritative FPR graph input until its own gate passes. |
| `G-BTE-006` | gap | active | Body War consumer owner | Read-only fixture/adapter and exact redacted-field allowlist are proposed but not yet executed. |
| `G-BTE-007` | gap | active | Craft + Inventory owners | Scoped and umbrella continuation pointers plus inventory entries require synchronization after this refresh. |
| `G-BTE-008` | gap | needs-review | engine owner | Legacy and v2 engine paths and local source-of-truth wording require explicit canonical-path review. |

## Dispatch Technique Trace

See `EXECUTION-DISPATCH.json`. Each technique is bound to a step, gate, evidence requirement, owner boundary, or residue row; no decorative techniques are cited.

## Distill Validation

The plan’s smallest coherent implementation unit is `SWU-BTE-001`: a shared criterion kernel that preserves existing behavior and enables every later surface. Recomposition passes. Mutation readiness remains blocked only because the owner profile gate and contract version/mapping are unresolved. See `DISTILL-VALIDATION.md`.

## Expected SWU Result Shape

```yaml
swu_id: SWU-BTE-NNN
result: pass | flag | block | interrupted
capability_ref: task-session
receipt_kind: native-stage | local-fallback | blocked
receipt_artifact: <path or none>
files_touched: []
validation: []
blockers: []
residue: []
reroute: <next owner or none>
handoff_note: <synchronization required>
```

## Gate Checks

- `workPackGateStatus` is ready after the accepted Decision Gate; FPR-02U state cannot change this gate.
- `EXECUTION-DISPATCH.json` must validate.
- Distill must be rerun after the owner gate changes the profile or mapping.
- One SWU and one strict runtime context pack are required per Task Session; no SWU is selected by this refresh.
- Passing structural or consumer evidence cannot admit a release or widen the claim beyond the conservative FPR-02B contract.
