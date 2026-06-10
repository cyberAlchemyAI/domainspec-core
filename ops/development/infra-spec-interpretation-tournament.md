# Infra-Spec Interpretation Tournament

Dispatch step: `dialectic-and-tournament` · Inputs: 7 lane ledgers + fanout-receipts
Rule (from strategy stop-conditions): no reading wins unless it preserves source/runtime/evidence boundaries **and** explains actual repo evidence; elegance alone does not win.

## Competing readings of "what infra-spec is"

| # | Reading | What it claims infra-spec primarily IS | Best supporting evidence | Fatal-flaw test |
| --- | --- | --- | --- | --- |
| R1 | Deployment spec | A nicer schema for deployment topology (containers, VPS, Caddy, Pulumi) | body-war/whisky-doses `infra-architecture.md` preset ladder | The repo has **no deploy instances**; a deployment spec with nothing to deploy is intent-only. Fails "explain actual evidence." |
| R2 | Operational contract | The obligation graph (who owns what, gates, SLOs, secrets, networking defaults) | `.github/agents/domainspec-infra-architect.agent.md`; whisky-doses CHANGELOG infra gates | Strong, but doesn't by itself account for the *evidence/promotion* layer that goldenquill actually runs. Partial. |
| R3 | Evidence substrate | A bridge from runtime facts → governance: receipts, drift, validation, promotion status | goldenquill `RUNTIME_MATURITY_MATRIX.md`, `CycleReceipt`/`ReflectionPacket`; Arcanum RUN/STATUS; SIGNAL-SCHEMA drift taxonomy | Explains the most real evidence across L3/L5/L6; preserves source/runtime/evidence boundaries by construction. |
| R4 | Reflection tower for infra | A promotion ladder where runtime evidence climbs only through gates | goldenquill 7-state ladder; Lean promotion-gate principle (L2) | The *gate principle* transfers; the *tower object* is analogy (L2). Wins only its gate aspect, which R3 already subsumes. |
| R5 | Residue-reduction system | Infra-spec as an accounting of what does not cross cleanly (spec→deploy→telemetry→incident) | L7 gaps (no rollback, unowned state); L5 residue types; L2 typed residue | A powerful *property* of infra-spec, but too narrow to be the whole definition; it is a sub-system of R3. |

## Pareto gate

- R1 dominated (fails the evidence test — no instances).
- R4 and R5 are **components** of R3, not independent winners: R4 contributes the promotion-gate discipline; R5 contributes the residue ledger. Both fold in.
- R2 is the **near-term skin**; R3 is the **substrate**.

## Convergence verdict

**Winner: R3 — infra-spec is an evidence substrate** that bridges runtime facts to governance, *with* R2's operational-contract vocabulary as its surface schema, R4's promotion-gate ladder as its status discipline, and R5's residue ledger as a first-class output.

Synthesized one-line definition (candidate, owner-review-gated):

> **infra-spec = a YAML-first, validator-backed evidence substrate that binds a project's operational contract (services, environments, boundaries, secrets, gates) to its runtime evidence (receipts, signals, drift) and governs promotion through typed status and typed residue — distinguishing specified / implemented / deployed / observed / validated / reflected / promoted, and never letting runtime evidence self-promote.**

## Why this preserves the required boundaries

- **source/runtime split**: the contract (source) and the receipts/signals (runtime) are different fields, never merged — inherited from Lean schema≠instance (L2).
- **evidence ≠ authority**: promotion requires a gate + owner review (goldenquill fail-closed model; strategy non-negotiable).
- **explains real evidence**: every clause maps to an existing artifact (goldenquill matrix, dispatch.schema `$defs`, SIGNAL-SCHEMA, Arcanum RUN/STATUS), not to theory.

## Residue from the tournament

- R2-vs-R3 framing tension is resolved by composition, but the **MVP** should likely ship R2 (operational contract schema) first with R3 hooks, because R3's full evidence substrate depends on receipts that only goldenquill currently produces. Carried to candidate DAG.
