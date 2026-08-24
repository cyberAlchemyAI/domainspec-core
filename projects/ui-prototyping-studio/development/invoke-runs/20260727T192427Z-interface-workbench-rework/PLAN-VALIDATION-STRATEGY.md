# Plan Validation Strategy

Status: `remediated-planned-evidence-only`

## Evidence Boundary

Design witness contracts and this matrix are planned, unexecuted evidence. Plan
artifact validation can prove structural completeness; it cannot prove product,
human, accessibility-certification, release, or deployment outcomes.

## Per-SWU Gate

For each selected SWU:

1. scope IDs and exact targets match `SWU-SCOPE-INVENTORY.json`;
2. Task Session preflight SHA-256/`ABSENT` bindings match;
3. the exact positive assertion and negative mutant in
   `SWU-ACCEPTANCE-MATRIX.json` pass;
4. the named receipt field is present in `task-session.swu-result.v1`;
5. all semantic dependencies and serialization predecessors are terminal;
6. Invoke Refresh changes only the exact targets/fields in
   `CLOSEOUT-SYNC-INVENTORY.json`;
7. the `invoke.refresh.v1` receipt leaves the successor unselected.

## Slice Gates

| Slice | Required assertions | Additional regression |
| --- | --- | --- |
| S-001/W0 | 001–003 | current governed projection E2E |
| S-002/W1 | 004–007 | zero reload; navigation/update accounting |
| S-003/W2 | 008–013 | recomposed region page and current governance |
| S-004/W3 | 014–015 | desktop non-regression and state matrix |
| S-005/W4 | 016–019 | bounded interaction/visual/security negatives |
| S-006/W5 | all 19 | TypeScript, all unit, all Playwright, exact closure inventory |

## Exact Plan-Artifact Checks

- Parse all JSON artifacts.
- Set equality across the four 19-SWU inventories.
- Unique IDs, known task/wave refs, known dependencies, acyclic semantic graph.
- `serialization_after` acyclic and earlier in candidate order.
- One primary acceptance assertion and receipt field per SWU.
- One primary owner per assertion ID; shared witnesses non-primary.
- Every closeout row includes work-pack, manifest, task, wave,
  `EXECUTION-PACK.md`, `PLAN-TRANSPORT.md`, execution receipt, refresh receipt,
  and deterministic successor.
- W5 report path/schema/writable fields/inventory exact.
- No selected SWU; all status values `not-started`.
- No stale 17-SWU or repaired-finding claims in current Plan surfaces.

## Full Closure Commands

From `projects/ui-prototyping-studio/backend`:

```bash
./node_modules/.bin/tsc -p tsconfig.json --noEmit
./node_modules/.bin/tsx --test "src/**/*.test.ts"
./node_modules/.bin/playwright test --reporter=list
```

These commands run only after implementation. Current Plan remediation runs
only artifact parsers/integrity checks plus a fresh governed Plan Distill.

## Claim Ceilings

A complete automated closure may support a separate human-study/readiness
route. It cannot establish first-use comprehension, task success, trust,
delight, cross-browser generalization, accessibility certification, release,
deployment, or production readiness.
