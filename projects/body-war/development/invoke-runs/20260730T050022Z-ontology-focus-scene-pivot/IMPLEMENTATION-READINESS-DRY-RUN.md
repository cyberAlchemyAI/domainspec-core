---
module: body-war-ontology-focus-scene-pivot
version: current
status: block-before-execution
updatedAt: 2026-07-30
docType: implementation-readiness-dry-run
---

# Implementation Readiness Dry Run

## Result

The architecture and ordered dependency graph are coherent, but the current
work pack is not executable through the installed Task Session runtime.

- numeric SWUs reviewed: 26
- closure tasks reviewed: 3
- captured frontier: 29 unique units, deterministic from `001` through `026`
- plan-contract result: 1 ready, 3 conditional, 22 blocked
- closure-contract result: 3 blocked
- current-runtime result: 0 of 29 executable
- product tasks executed: 0
- selected SWU: none
- product files changed: none

`SWU-OFSP-001` is dependency-ready and has a complete local task description,
but it is still runtime-blocked because the current Task Session mutation
admission requires a producer-validated material package that this Invoke run
does not contain.

## Method

This was a non-mutating frontier preflight, not a Task Session execution chain.
Each unit was checked against:

1. dependency and successor determinism;
2. exact live inputs and ownership;
3. declared write scope;
4. executable validation command and working directory;
5. mutation-admission feasibility;
6. expected outputs and attempt naming;
7. terminal receipt semantics;
8. closeout owner receipt and successor feasibility.

The `task-session-until-blocker` execution chain was not invoked because its
contract excludes planning and discovery audits.

## Live Substrate

| Check | Result |
| --- | --- |
| Frozen presentation graph | pass; SHA-256 `e8f754e6aed7b05759439df82db421eb51fa050c78b86b37d5d689e89a751433` |
| Graph shape | pass; 237 nodes, 231 edges, five tour steps |
| Literal portal | pass; `Identity and Consent` to `Authentication and Consent`, `direction:forward`, `type:related`, `description:owns` |
| Pinned upstream archive | pass; commit `2cda14e89535049e49120198886bc0b82e9e630f`, archive SHA-256 `1e00e541b494cb5538ba4ef19e1661e80312b128be5d32a89ae8a6ad56b40e16` |
| Native logical sources | pass; all eight planned native paths exist in the archive |
| Node | pass; `v22.12.0`, pinned bytes match |
| Pinned pnpm | pass; direct Node invocation of pnpm `10.6.2`, pinned bytes match |
| Bare `pnpm` | block; active Corepack resolves pnpm `11.11.0` and raises `ERR_VM_DYNAMIC_IMPORT_CALLBACK_MISSING` |
| Global Playwright | pass; active CLI `1.59.1` |
| Chromium | pass; revision `1217`, executable resolves |
| Existing package root | pass; no new package root or dependency is needed |
| Historical build scripts | absent as expected; `materialize-l1-build.mjs`, `verify-l1-build.mjs`, and `verify-browser-acceptance.mjs` are not present |

The existing `scripts/materialize-l1-workroot.mjs` already verifies the pinned
Node/pnpm entrypoints, creates an isolated store and outside-repository
workroot, applies one exact patch, and cleans in `finally`. It is a useful
substrate, but its overlay validator is hard-coded to the bootstrap README
probe. The focus-scene route should generalize or extend this substrate rather
than independently reimplementing its lifecycle.

## Systemic Blockers

### B1 — Mutation admission is absent

Installed Task Session `0.8.0` requires routed mutations to bind:

- at least three current controlling artifacts;
- exact dependency receipt references;
- a producer-validated Invoke material package and material receipt;
- material writes, execution outputs, and their exact allowed-write union;
- executable validation commands;
- lifecycle, authority, and publication classes.

This run contains none of the material-package or mutation-admission artifacts.
Therefore every mutating or receipt-producing unit blocks before its first
write, including otherwise dependency-ready `SWU-OFSP-001`.

### B2 — Twenty-one SWUs lack executable validation commands

Only `001`, `002`, `003`, `004`, and `015` name exact executable commands.
The remaining 21 numeric SWUs name outcomes such as “materialized tests pass,”
“browser receipt verification passes,” or “all regressions pass” without an
exact command, working directory, required inputs, or expected output files.

This contradicts the [work-pack handoff claim](WORK-PACK.md) that every task
file provides complete validation.

### B3 — Output-only units do not fit current admission

`014`, `016`, `022`, and `023`, plus the three closure tasks, are intended to
produce immutable evidence rather than pre-authored material files. Current
Task Session routed-mutation admission nevertheless requires at least one
`materialWrites` entry and a materialized Invoke package whose output bytes
already exist.

A lifecycle owner must resolve this contract mismatch before those seven units
can run. A fake placeholder material write is not an acceptable repair.

### B4 — Closeout conflates two owners

The [closeout contract](work-pack/shared/CLOSEOUT-CONTRACT.md) names
`work-pack/closeout/<UNIT>.receipt.json` as the expected closeout receipt while
also requiring the Task Session terminal receipt schema. That schema fixes
`capability_ref` to `task-session`.

Task Session `0.8.0` requires two distinct receipts when synchronization is
needed:

1. the terminal Task Session receipt;
2. a separately owned and joined `invoke:refresh:apply-approved` closeout
   receipt.

The plan does not provide distinct destinations, schemas, or owner validation
commands for those receipts.

### B5 — The terminal receipt schema is fail-open

Adversarial validation showed that the current
[`TASK-SESSION-RECEIPT.schema.json`](TASK-SESSION-RECEIPT.schema.json) accepts:

- `status: pass` with `validation_result: not-run`;
- `status: pass` with non-empty blockers;
- `status: pass` with empty validation and artifacts;
- `status: block` with `validation_result: pass`;
- a non-string `unit_id`;
- a non-string artifact SHA-256;
- unowned extra fields inside artifact and validation rows;
- any valid unit with any dispatch step.

Schema presence therefore does not prove a valid terminal result. A semantic
validator and unit-to-step binding are required.

### B6 — Closure tasks are rows, not executable task contracts

`TASK-VERIFY`, `TASK-AUDIT-ALIGNMENT`, and `TASK-AUDIT-LAYERING` have owners,
receipt destinations, and order, but no exact:

- controlling input inventory;
- dependency receipt digest requirements;
- write/output classification;
- validation commands;
- acceptance assertions;
- blocker/residue rules;
- separate Task Session and closeout receipt contracts.

All three block packaging.

### B7 — Build and browser attempts are underspecified

`014`, `016`, `022`, `023`, and `026` lack some or all of:

- exact producer and verifier invocations;
- attempt-ID generation and collision policy;
- exact output inventory and schemas;
- native route/gateway invocation;
- retained-versus-temporary artifact policy;
- teardown verification command.

The existing `L1-BUILD.lock.json` binds the historical `?oew=1` feature
inputs. A successor focus-scene build lock must reuse only the admitted
upstream/toolchain/execution substrate and bind the new native overlay.

### B8 — Source selectors and directory creation are ambiguous

The shared context names bare `findings.md` and `synthesis.md`, but the Body War
tree contains multiple `findings.md` files. The accepted inputs must be bound
to:

- `projects/body-war/development/reviews/20260730-ontology-ui-black-box/findings.md`;
- `projects/body-war/development/reviews/20260730-ontology-ui-black-box/synthesis.md`.

`work-pack/closeout/` is absent. This is minor only after the owner contract
states who creates it, when, and with what atomic/permission behavior.

## Per-Unit Matrix

Status meanings:

- `PLAN-READY`: task description and live prerequisites are sufficient before
  applying the separate mutation-admission gate;
- `CONDITIONAL`: task description is sufficient but a predecessor must first
  produce its receipt;
- `BLOCK`: the task itself lacks an execution-critical contract;
- every row remains `RUNTIME-BLOCKED` by B1 until admission is repaired.

| Unit | Plan preflight | Main missing condition |
| --- | --- | --- |
| 001 | PLAN-READY | Runtime material package/admission only |
| 002 | CONDITIONAL | Passing 001 receipt; runtime admission |
| 003 | CONDITIONAL | Passing 002 receipt; define extension/generalization of existing materializer |
| 004 | CONDITIONAL | Passing 003 receipt; runtime admission |
| 005 | BLOCK | Exact materialized-dashboard command/cwd/output set |
| 006 | BLOCK | Exact materialized test and oracle-comparison commands |
| 007 | BLOCK | Exact reducer/serializer commands |
| 008 | BLOCK | Exact portal/Back commands |
| 009 | BLOCK | Exact patch/materialized store-test commands |
| 010 | BLOCK | Exact renderer commands |
| 011 | BLOCK | Exact landmark/focus commands |
| 012 | BLOCK | Exact relation-control parity commands |
| 013 | BLOCK | Exact focus/motion commands |
| 014 | BLOCK | Successor build lock, producer/verifier commands, attempt/output inventory; output-only admission mismatch |
| 015 | CONDITIONAL-BLOCKED | Own Node test command is exact, but 014 cannot deterministically supply its handle |
| 016 | BLOCK | Gateway/browser/validator commands, attempt/output inventory; output-only admission mismatch |
| 017 | BLOCK | Exact one-hop and oracle-regression commands |
| 018 | BLOCK | Exact tour reducer commands |
| 019 | BLOCK | Exact materialized LearnPanel/tour commands |
| 020 | BLOCK | Exact literal-surface commands |
| 021 | BLOCK | Exact forced-colors component/browser commands |
| 022 | BLOCK | L1 producer/verifier commands, attempt/output inventory; output-only admission mismatch |
| 023 | BLOCK | Browser-regression command and output inventory; output-only admission mismatch |
| 024 | BLOCK | Exact negative-fixture commands |
| 025 | BLOCK | Exact component/browser/full-regression commands |
| TASK-VERIFY | BLOCK | Full task, validation, terminal receipt, and closeout contract |
| TASK-AUDIT-ALIGNMENT | BLOCK | Full task, validation, terminal receipt, and closeout contract |
| TASK-AUDIT-LAYERING | BLOCK | Full task, validation, terminal receipt, and closeout contract |
| 026 | BLOCK | Clean-reproduction command, successor build/receipt selection, attempt algorithm, output schema |

## Deterministic Parts That Passed

- `001` is the unique first dependency-ready numeric SWU.
- Numeric dependency references are complete and point backward.
- The closeout successor chain is finite, unique, acyclic, and exactly:
  `001..025 -> TASK-VERIFY -> TASK-AUDIT-ALIGNMENT ->
  TASK-AUDIT-LAYERING -> 026`.
- No planned output currently collides with an existing focus-scene file.
- Historical locks, archive artifacts, package metadata, and current overlay
  files are clean.
- Global Playwright is usable without adding a package.

## Smallest Repair Route

Before selecting `SWU-OFSP-001`:

1. Decide the runtime contract for pre-authored material mutations versus
   output-only evidence tasks.
2. Produce the required material-package/material-receipt/admission inputs for
   each mutating SWU, or change the owning runtime contract through its own
   lifecycle.
3. Add one exact command matrix for all 26 SWUs: cwd, argv/executable, inputs,
   dependency receipts, material writes, execution outputs, allowed-write
   union, output schemas, attempt algorithm, and teardown.
4. Generalize the existing L1 materializer/verifier substrate and add a
   successor focus-scene build lock; do not import the historical `?oew=1`
   feature inputs.
5. Turn the three closure rows into full task contracts with distinct terminal
   and Invoke Refresh closeout receipts.
6. Harden the terminal receipt schema and add a semantic validator with
   unit-to-step/status/evidence rules.
7. Replace bare review names with exact paths and define closeout-directory
   creation.
8. Rerun this 29-unit dry run. Require 29 preflight-pass rows before beginning
   implementation.

## Decision Gate

No implementation decision was silently selected by this audit. Two
blocker-level choices remain for the repair:

1. extend/generalize the verified existing materializer/verifier substrate, or
   author an entirely new lifecycle;
2. evolve Task Session admission to support output-only governed tasks, or
   route those tasks to a capability whose contract already supports them.

Recommendation: extend the verified substrate, and repair the owner runtime
contract for output-only tasks rather than fabricating material writes.

## Helper Receipt

- helper: `/root/ofsp_dry_run_verifier`
- scope: read-only independent per-unit contract and live-prerequisite review
- status: completed and joined
- files changed: none
- independent result: 1 ready, 3 conditional, 22 blocked; all three closure
  tasks blocked

## Observability Receipt

- capability: `implementation-readiness`
- mode: `dry-run`
- result: recorded
- central ledger:
  `.arcanum/observability/signals/sigil-invocations.jsonl`
- ledger line: 427
- reflection trigger: `severe-gap`
- recommendation: `repair-work-pack-before-selection`

## Open Questions

The two Decision Gate choices above remain open. They do not change the
finding that current execution readiness is `BLOCK`.
