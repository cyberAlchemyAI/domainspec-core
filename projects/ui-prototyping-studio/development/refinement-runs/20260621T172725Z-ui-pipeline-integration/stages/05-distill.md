# Distill - Smallest Coherent Integration Unit

Status: `pass`
Capability: `distill`
Mode: `standard`
Proposal tracks: `3`
Recursive rounds: `2/2`

## Broad Layer

The broad layer is **UI delivery governance**:

```text
feature definition -> UI specs -> prototype evidence -> app implementation -> browser validation
```

## Candidate Units

| Candidate | Decision | Reason |
| --- | --- | --- |
| Pipeline replacement | reject | Overbuilt and violates spec ownership. Studio would become a second source of truth. |
| BodyWar-only spike | defer | Useful, but too narrow to answer the reusable integration question. |
| Prototype gate contract | select | Smallest unit that preserves all owners and gives immediate BodyWar value. |

## Selected Smallest Coherent Unit

**Studio Prototype Gate Contract**

Responsibility: define how UI Prototyping Studio consumes `UI-SPEC.md` and
`TEST-SPEC.md`, runs a bounded prototype session, and returns handoff evidence
without mutating canonical specs or target app source.

## Closure Test

| Closure Criterion | Result |
| --- | --- |
| Named inputs | `UI-SPEC.md`, `TEST-SPEC.md`, visual definitions, target constraints. |
| Named outputs | session record, variants, annotations, accepted revision, handoff export. |
| Single owner | Studio owns gate execution; upstream/downstream owners remain separate. |
| No hidden target mutation | pass; only future task-session mutates target app. |
| Can execute independently | pass; Studio preview does not require BodyWar Playwright wiring. |
| Recombines upward | pass; handoff feeds target-app implementation and browser audit. |

## Recomposition Proof

The selected unit recomposes into the larger system because it fills the gap
between spec authoring and app hardening:

1. DomainSpec UI pipeline produces the contract.
2. Studio makes the contract visible and commentable in a browser.
3. Handoff export packages the chosen prototype evidence.
4. Target app task-session implements the evidence in production source.
5. Playwright/visual audit checks the real app, not just the prototype.

## Deferred Complexity

- Full Studio SPA remains deferred.
- External design-tool comparison remains deferred.
- Automatic spec refresh from prototype evidence remains deferred.
- BodyWar source mutation remains deferred to task-session.

## Verdict

`pass`: the prototype gate contract is small enough to execute and large enough
to preserve the intended UI-pipeline meaning.

## Receipt

```json
{
  "stage": "05-distill",
  "status": "pass",
  "artifacts": [
    "stages/05-distill.md"
  ],
  "validation_result": "pass",
  "blockers": [],
  "residue": [
    "First execution should prove the contract with TROQAR before making it a repo-wide UI pipeline obligation."
  ]
}
```
