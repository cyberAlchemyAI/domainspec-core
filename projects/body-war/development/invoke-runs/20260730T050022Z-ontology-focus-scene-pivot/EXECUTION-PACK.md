# Execution Pack — Body War Ontology Focus Scene And Portal Pivot

## Planning Control

| Field | Value |
| --- | --- |
| `planningGateStatus` | `pass` |
| `complexity` | `high` |
| `baselineWave` | `W0` |
| `activePlanRef` | `WORK-PACK.md` |
| `workPackManifest` | `WORK-PACK.md` |
| `layeringArtifact` | `IMPLEMENTATION-LAYERING.md` |
| `specRef` | `SPEC.md` |
| `activeLayerWindow` | `L0` |
| `readinessProfile` | `pilot` |
| `selected_swu` | `none` |

## Wave Schedule

| Wave | Layer | Units | Gate evidence | Unlocks |
| --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | L0 foundation | 001–004 | fixture, overlay, materializer/verifier tooling-readiness receipts | L0 feature source |
| [W1](work-pack/waves/W1.md) | L0 POC | 005–016 | exact projection/state/UI, verified build, browser receipt | L1 repeatability |
| [W2](work-pack/waves/W2.md) | L1 | 017–023 | one-hop/tour/literal verified build + browser regression | L2 hardening |
| [W3](work-pack/waves/W3.md) | L2/L3 | 024–025, closure audits, 026 | degraded-mode audits and clean reproduction | local prototype handoff |

All SWUs execute sequentially because the successor overlay lock/manifest and
native patches are shared ownership surfaces. No parallel wave is admitted by
this Plan.

## Execution Rules

1. The parent explicitly selects exactly one dependency-ready SWU.
2. Context Builder derives a strict task pack from the linked task heading,
   shared context, traceability, and predecessor receipts.
3. One Task Session executes only that SWU's write scope.
4. Scoped validation and the exact result shape are mandatory.
5. Invoke Refresh applies only the declared closeout contract.
6. No successor is automatically executed.

## Gate Checks

| Gate | Condition | Failure route |
| --- | --- | --- |
| selection | one explicit SWU and no sibling mutation | return to parent |
| source ownership | private ontology read-only; successor overlay source only | block and audit files |
| overlay admission | exact upstream preimages/destinations/digests | repair current SWU |
| validation | named positive/negative commands pass | repair current SWU |
| handle handoff | producer and independent verifier bindings pass | invalidate attempt |
| browser | exact native route/runtime/assertions/teardown pass | invalidate attempt |
| authority | `authority_effect:none`, no release/comprehension claim | block closeout |
| closeout | exact baselines/deltas/receipt/successor policy pass | keep SWU open |

## Completion Verification

`TASK-VERIFY` confirms every acceptance contract has an exact executed selector
and no planned witness is mistaken for evidence. `TASK-AUDIT-ALIGNMENT` compares
spec/design/source/receipts. `TASK-AUDIT-LAYERING` proves:

- ontology and adapter authority stayed outside UI projection;
- pinned upstream/archive and historical evidence stayed immutable;
- source changes entered only through the successor overlay;
- generated outputs were new evidence attempts;
- no new package root or Playwright dependency appeared.

## Dispatch

Future execution route:

- `EXECUTION-DISPATCH.json`
- validation: `pass`
- mode: sequential
- subagent strategy: none
- execution owner: one Task Session after explicit selection

## Evidence State

- authored plan: pass
- executed implementation: not started
- Plan evidence: pending
- selected SWU: none
- implementation authority: not granted
