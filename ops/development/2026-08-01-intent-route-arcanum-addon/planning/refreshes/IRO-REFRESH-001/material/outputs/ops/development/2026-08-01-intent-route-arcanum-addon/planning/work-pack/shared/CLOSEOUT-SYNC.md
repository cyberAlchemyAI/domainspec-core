# Closeout sync contract

## Authority

Every SWU terminal receipt is immutable. Task Session never edits Invoke-owned
planning targets. Invoke Refresh owns the one-hop closeout mutation and must
return a separately validated owner receipt.

## Receipt contracts

- Terminal receipt:
  `work-pack/shared/TERMINAL-RECEIPT.schema.json`.
- Decision bundle for IRO-001:
  `work-pack/shared/DECISION-BUNDLE.schema.json`.
- Closeout owner receipt:
  `work-pack/shared/CLOSEOUT-OWNER-RECEIPT.schema.json`.
- Unit paths, commands, baselines, successors, and pause gates:
  `work-pack/shared/EXECUTION-CONTRACT.json`.

## Exact closeout target inventory

For every unit, the closeout request must enumerate an exact subset of:

1. `planning/WORK-PACK.md` — evidence, blocker, status, or route fields only;
2. `planning/EXECUTION-PACK.md` — current frontier or pause status only;
3. `planning/work-pack/shared/CROSS-TASK-GAPS.md` — resolved/open owner bindings only;
4. `planning/work-pack/shared/CROSS-TASK-DECISIONS.md` — durable selected/deferred decision state only;
5. `planning/work-pack/shared/TRACEABILITY.md` — exact evidence links only;
6. the current unit's fixed session-evidence receipt paths.

No target is admitted by directory inference. Each request records the path,
pre-mutation SHA-256 or an explicit `absent` sentinel, admitted delta class,
validation command, and expected post-state. The target list may be empty only
for a receipt-backed no-op.

## Admitted deltas

- `evidence_added`
- `blocker_opened`
- `blocker_resolved`
- `status_changed`
- `route_changed`

The following are never closeout deltas: implementation, API/scope/authority
changes, new write paths, promotion, publication, deployment, destructive
cleanup, policy/cost/risk acceptance, or next-unit execution.

## Baseline and owner validation

Before dispatch, Task Session must bind current target SHA-256 values and the
source terminal receipt digest. Invoke Refresh must re-read them immediately
before mutation, apply only the declared deltas, then run:

```text
python3 planning/work-pack/shared/validate-execution-contract.py --root .
python3 -m json.tool <terminal-or-owner-receipt>
git diff --check -- <exact-closeout-targets>
```

Owner receipt validation requires schema conformance, exact target equality,
baseline equality, admitted deltas only, zero forbidden scopes, joined owner
status, and the deterministic successor result.

## Successor policy

Every unit has exactly one canonical successor, including the terminal
`__complete__` sentinel. Closeout may project that successor only when the
current unit passes and the successor is dependency-ready. Projection never
selects or executes the successor.

The stream must pause before IRO-002, IRO-004, IRO-006, IRO-007, IRO-008, and
IRO-009. Each pause requires the exact approval/owner receipt named in
`EXECUTION-CONTRACT.json`. Missing or ambiguous approval returns `BLOCK`.

## Failure policy

Missing target inventory, stale baseline, absent schema, invalid owner receipt,
forbidden delta, ambiguous successor, or unjoined owner hop returns `BLOCK`
without mutation. A second repair cycle for the same unit pauses the Goal and
reports the owner; it does not enter another automatic Refresh loop.

