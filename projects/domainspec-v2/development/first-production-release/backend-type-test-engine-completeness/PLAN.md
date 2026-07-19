---
title: Invoke Plan - Backend Type Test Engine Completeness
status: decision-synchronized-awaiting-task-session
updatedAt: 2026-07-17
docType: invoke-plan
observedCapability: invoke
invokeMode: plan
targetOwner: DomainSpec-v2 FPR-02B, FPR-04, and FPR-07
---

# Invoke Plan — Backend Type Test Engine Completeness

## Invoke Result

- Mode: `plan`
- Spell: `invoke`
- Canonical ID: `invoke`
- Scope: library authoring for the private DomainSpec-v2 lifecycle
- Phase status: `pass` — the FPR-02B Decision Gate is accepted; implementation still requires a separate authorized Task Session and `FPR-02U` remains independent
- Mode contract: `.agents/skills/invoke/plan.md`
- Outputs: `PLAN.md`, `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`, `EXECUTION-PACK.md`, `EXECUTION-DISPATCH.json`, `DISTILL-VALIDATION.md`, `transport-report.json`, `observability.json`, and split work-pack contracts
- Design views: node JSON remains canonical meaning, YAML remains formation authority, and independent edge JSON records are now required by the accepted successor-profile decision
- Glossary consistency: `pass` for existing terms; no definitions are promoted
- Dispatch techniques: full route document, validator required
- Distill validation: refresh required for the successor edge/consumer scope; no SWU is selected and no implementation is authorized by this refresh
- Implementation layering: L0–L3 in `IMPLEMENTATION-LAYERING.md`
- Work-pack: split, high complexity
- Implementation detail: task contracts complete
- Smallest working units: eight SWUs defined; none selected
- Template/profile selection: Invoke standalone layering/work-pack templates plus the DomainSpec execution-pack template; current node-package layout retained
- Next route: select exactly one dependency-ready BTE SWU through an authorized `task-session`; do not join the UI lane

## Intent Interpretation

"All backend types" means the exact FPR-01 backend set, not every staged or UI type:

`Entity`, `Value Object`, `Enum`, `Operation`, `Query`, `Calculation`, `Rule`, `Policy`, `Workflow`, `Interface`, `Event`, `Mapping`, and `State Machine`.

The source formation contract is the 13 per-type `impl/spec/meta-types/**/*.schema.yml` files. The consumer authoring form is one canonical JSON file per node plus one canonical JSON file per edge. Same-feature edges live under `specs/<feature>/edges`; cross-feature edges live under project-level `specs/edges`. Generated graph, Markdown, tests, and receipts remain read/evidence models only.

## Problem Statement

The current minted-project profile proves four kinds (`Entity`, `Event`, `Operation`, `Rule`) with four hand-authored JSON body schemas. The broader backend authority already contains 13 YAML criterion schemas and eight decidable criterion rule forms. The test-derivation engine is green in its bounded prototype scope, but the release path still lacks:

1. one profile contract that admits and positively exercises all 13 backend kinds;
2. one shared criterion evaluator used consistently by Markdown, generated instances, and minted nodes;
3. a profile-owned obligation denominator independent from engine output;
4. deterministic graph-to-obligation derivation for minted nodes;
5. executable, non-skipped checks and killed criterion mutants for every admitted obligation; and
6. a fail-closed integration gate that rejects missing/empty release witnesses.

## Approved Source Design References

- Current release ordering and gates: [ROADMAP.md](../ROADMAP.md)
- In-progress backend choice and closed lane split: [FPR-02B Decision Gate](../decisions/2026-07-17-fpr02-supported-profile-decision.md)
- Machine lane contract: [FPR-02 lanes](../profile-lanes/fpr02-lanes.yml)
- Engine residue and false-green inventory: [engine-gap findings](../../../research/2026-07-14-engine-gap-inventory/findings.md)
- Backend type authority/read model: [meta-types.yml](../../../definitions/meta-types/meta-types.yml)
- Existing profile admission: [supported-profiles.yml](../../../definitions/minted-project/supported-profiles.yml)
- Existing node envelope: [node.schema.json](../../../impl/spec/minted-project/node.schema.json)
- Existing compiler: [compiler.ts](../../../impl/tools/minted-project/compiler.ts)
- Existing YAML instance evaluator: [instances.ts](../../../impl/tools/instances.ts)
- Selected node-package layout: [selected-design.json](../../../development/refinement-runs/20260714-minted-project-node-package-toy-game/stages/S08-distill-repair/selected-design.json)

## Delivery Boundary

Included:

- exact 13-kind backend-only candidate profile;
- all 13 YAML formation schemas and all 16 current criterion entries;
- one shared YAML subset loader, preflight, canonical criterion model, evaluator, and stable violation contract;
- adapters for Markdown tables, generated instance YAML, and minted-node JSON bodies;
- one positive minted-node witness per kind and one killed mutant per criterion;
- independent `O_spec` catalogue and engine-derived `O_gen` exact-set comparison;
- deterministic obligation keys, source anchors, executable structural tests, execution evidence, and a zero-gap receipt;
- missing source, empty release witness, stale digest, unsupported kind, malformed formation, orphan obligation, skip/todo, and surviving-mutant negatives;
- release-profile validation command and required-check manifest.

Explicitly excluded:

- UI meta-types `DS-D1.15..25`, which continue independently under `FPR-02U`;
- UI/cross-layer signatures; FPR-02B admits and positively exercises exactly the 16 backend signatures selected by the Decision Gate;
- semantic satisfiability, business-correctness inference, application generation, or universal code/spec equivalence;
- semantic satisfiability, business-correctness inference, application generation, or universal code/spec equivalence;
- changes to the accepted FPR-02B decision, the independent FPR-02U lane, Craft authority, or production status from this plan refresh.

## Proposed Contract

### Authority flow

```text
FPR-02B selected backend profile
  + meta-types.yml exact backend set
  + 13 *.schema.yml formation criteria
  + minted node JSON sources
        |
        v
shared criterion kernel + node-body adapter
        |
        +--> minted graph/source manifest
        +--> independent O_spec catalogue and receipt
        +--> engine O_gen obligations and executable tests
                     |
                     v
        exact-set + execution + mutation comparison
```

The accepted successor profile is `feature-with-independent-node-and-edge-files@1` with candidate posture. The existing `feature-with-independent-node-files@1` remains unchanged historical evidence and must not be widened in place.

Independent edge records carry stable identity, governed signature, endpoints,
scope, ownership, and lifecycle metadata. The resolver must reject duplicate IDs,
wrong-root declarations, missing endpoint ownership, path escape, stale digest,
and an edge declared in both feature-local and project-level roots.

### Canonical criterion subject

A shared internal `CriterionSubject` normalizes representations without replacing their authority:

```ts
type CriterionSubject = {
  kind: string;
  fields?: Array<Record<string, unknown>>;
  values?: unknown[];
  attributes?: Record<string, unknown>;
  text?: Record<string, string>;
};
```

Adapters are explicit:

- Markdown adapter: tables/sections to `CriterionSubject`;
- instance adapter: existing generated-instance keys to `CriterionSubject`;
- minted-node adapter: `body.fields`, `body.values`, direct scalar body keys, and named text such as `body.equality` to `CriterionSubject`.

The YAML schemas remain the rule authority. Adapters may normalize syntax; they may not invent missing semantics or type-specific exceptions.

### Completeness equation

For the selected backend profile:

```text
Kinds_profile = Kinds_exercised = 13
Criteria_profile = O_spec = O_gen = T_gen = E_run = 16
skips = todos = orphans = unrunnable = surviving_mutants = 0
```

Counts are current-plan expectations, not promoted authority. Any schema edit changes the digest and reopens the denominator receipt.

## Execution Order

1. Bind the accepted FPR-02B decision to the candidate successor profile and freeze its source roots and digests.
2. Extract the shared criterion kernel without changing current validator behavior.
3. Prove the node adapter across all eight criterion rule forms.
4. Bind the 13-kind profile and build the positive/mutant corpus.
5. Produce an independently owned, digest-bound `O_spec` catalogue.
6. Derive `O_gen` from compiled minted graphs and emit executable structural tests.
7. Enforce exact-set, execution, mutation, missing-input, and aggregate release gates.
8. Run independent closure verification, IOLM consumer proof, Body War consumer proof, and the integrated non-admission receipt.

## Dispatch Technique Trace

| Technique | Plan effect |
| --- | --- |
| `sequence` | FPR-02B decision → kernel → adapter/profile → corpus → obligations/tests → integration → verification |
| `scu_swu_reduction` | Eight bounded SWUs; execution selects one at a time |
| `recomposition_proof` | Kernel, profile, corpus, catalogue, engine, and gates recompose into FPR-04/FPR-07 evidence |
| `validation_loop` | Every SWU has positive, negative, deterministic, or receipt validation |
| `owner_boundary_check` | Invoke authors; Decision Gate selects; Task Session executes; owners admit/promote |
| `handle_handoff` | Runtime context uses exact artifact handles instead of copied authority prose |
| `residue_ledger` | UI, relationship breadth, semantic satisfiability, and cross-feature work stay explicit |
| `execution_receipt_handoff` | Every later SWU returns artifacts, checks, blockers, residue, and reroute |
| `authority_split_gate` | YAML definitions, consumer nodes, generated graphs/tests, and release admission do not collapse |
| `concrete_path_evidence` | Validation and receipts cite exact source and output paths |
| `state_namespace_boundary` | Plan, authority, source, generated evidence, and runtime receipts have separate owners |

## Navigation

1. Start with [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md).
2. Use [WORK-PACK.md](WORK-PACK.md) as the executable planning authority.
3. Read the task contract linked from the task board before selecting an SWU.
4. Use [EXECUTION-PACK.md](EXECUTION-PACK.md) for wave gates.
5. Do not start execution while `workPackGateStatus = block`.
