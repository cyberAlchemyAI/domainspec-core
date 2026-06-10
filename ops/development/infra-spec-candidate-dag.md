# Infra-Spec Candidate DAG

Dispatch step: `synthesize-infra-spec-map` (DAG view) · Status: candidate-only (no `formulae/infra-spec` creation in this route)

Derived from the tournament winner (R3 evidence substrate, R2 surface, R4 gates, R5 residue) and the lane ledgers. Nodes are candidate concepts; edges are "depends-on / constrains".

## Concept nodes (candidate)

| Node | Definition (candidate) | Status | Source evidence |
| --- | --- | --- | --- |
| N1 runtime_profile | preset env class: dev / single-vps / split-vps / ha | candidate (highest-signal, already enumerated) | `projects/body-war/domainspec/templates/infra-architecture.md` |
| N2 service/component | a deployable unit with owner + dependencies | candidate | infra-architecture templates; L4 |
| N3 boundary object | network / secret / data / tenant / policy / actor / capability / generated-state — each with its own rules | candidate (boundary.kind enum needs infra redefinition) | `dispatch.schema.yml` `$defs.boundary`; L4 |
| N4 state_namespace | explicit source / runtime / generated / local / private / evidence partition | candidate | `dispatch.schema.yml`; L1; L7 unowned-state gaps |
| N5 operational_proof_status | specified → implemented → deployed → observed → validated → reflected → promoted (7 distinct states) | candidate (implementation-backed precedent) | `projects/goldenquill/RUNTIME_MATURITY_MATRIX.md`; L2 4-status rule |
| N6 runtime_instance | the deployed/executable counterpart of a spec | candidate (currently mostly absent → key gap) | L3 atlas; L7 G7 |
| N7 receipt | typed post-run record (identity, outcome, blocked_reason, drift, residue) | candidate (portable model exists) | `arcanum/framework/runtime/templates/RUN.json`/`STATUS.json`; goldenquill `CycleReceipt`; L5 |
| N8 observability_signal / SLO | signal + SLO/error-budget refs (not redefined; referenced) | candidate | `SIGNAL-SCHEMA.md`, `slos.md`; L5 |
| N9 drift | spec-without-deploy / deploy-without-spec / contract-mismatch | candidate | `tools/check_github_drift.sh`, SIGNAL-SCHEMA; L3/L5/L7 |
| N10 typed_residue | what does not cross spec→deploy→telemetry→incident, typed + owned | candidate (first-class output) | L2 typed residue; L5 R1–R5; L7 |
| N11 promotion_gate | fail-closed gate; runtime evidence cannot self-promote | candidate | goldenquill `deployment_posture.py` fail-closed; strategy non-negotiable |
| N12 reversal/lifecycle | rollback / migration / backup / retention obligations | **net-new gap** (absent today) | L7 G5/G6 (explicit absence) |

## Dependency edges

```
N1 runtime_profile ──constrains──> N2 service ──has──> N3 boundary ──partitions──> N4 state_namespace
N2 service ──emits──> N7 receipt ──carries──> N8 signal/SLO, N9 drift, N10 residue
N5 operational_proof_status <──gated-by── N11 promotion_gate <──consumes── N7 receipt
N6 runtime_instance ──realizes──> N2 service ; absence of N6 ──produces──> N10 residue (intent-without-instance)
N12 reversal/lifecycle ──missing-constraint-on──> N5 status (cannot reach "promoted" safely without it)
```

## Critical-path reading

1. **Spine (MVP)**: N1 → N2 → N3 → N4 + N11 gate + N5 status floor. This is the *operational contract* (R2) — buildable now from existing template + dispatch.schema `$defs`.
2. **Evidence layer (R3)**: N7 → N8/N9/N10 — depends on receipts; only goldenquill currently produces them, so this layer is partially blocked on real instances (N6).
3. **Net-new must-add**: N12 reversal/lifecycle — no current evidence; required before any "promoted" state is trustworthy.

## Pruning / merges

- Merge actor + owner into a single `owner` axis with optional `actor` (L4 conflict resolution).
- Drop event/queue/backpressure from the MVP core (no broker artifact exists) → keep as N-future, tracked in residue (L4 R4, L7 G9).

## Boundaries preserved

Every node keeps source (contract) and runtime (receipt/signal) fields distinct; N5/N11 enforce evidence≠authority. No node asserts a built package.
