# Operational ontology branch — candidate seed for domainspec-core

Step `seed-operational-branch` (`ontology-vault`). **Status: candidate extension, pending
user/ontology-harness review.** Not a promoted branch. Reuses the branch-aware node-schema shape
and the single edge catalog; assigns no authority. Tags **SB/TD/H**.

## Branch descriptor

| Field | Value |
| ----- | ----- |
| `branch_id` | `B-op` (operational) |
| owns | agent-operation knowledge: routes, capabilities, prompts, disciplines, decisions, lessons, failure modes, maintenance triggers |
| must NOT own | per-run denominators / lifecycle state (that is `run-context` B3); raw memory / unreviewed telemetry as truth |
| node types | see [CARRY-SET.md](../CARRY-SET.md) |
| edge catalog | reuse [DAG-AND-METRICS.md §3](../../DAG-AND-METRICS.md) — no new catalog |
| apex (highest category) | `operational_constitution` (L6) + `operational_axiom` (L7), owned by Constitution Governance |
| acceptance gate | user / ontology-harness review accepts the branch shape [ONTOLOGY-ARCHITECTURE.md:79,139] |

## Candidate nodes (telemetry-seeded, L3 candidate — illustrative, not promoted)

Derived from measured telemetry 2026-06-12. `veracidade` reflects evidence strength; all `status: candidate`.

| node_id | node_type | label | evidence_refs | veracidade |
| ------- | --------- | ----- | ------------- | ---------- |
| `node.op.cap-invoke` | capability | `invoke` spell, tier=spell | by-sigil/invoke.jsonl (98 invocations) | high |
| `node.op.cap-task-session` | capability | `task-session` sigil | by-sigil/task-session.jsonl (85) | high |
| `node.op.cap-context-builder` | capability | `context-builder` sigil | by-sigil/context-builder.jsonl (56) | high |
| `node.op.inv-invoke-runs` | invocation | invoke runs observed | signals/sigil-invocations.jsonl | high |
| `node.op.gap-cluster` | workflow_gap | 33 related + 5 severe gaps recorded | reflection-state.json counters | medium |
| `node.op.trig-reflect` | maintenance_trigger | reflection trigger on gap/usage thresholds | observability/config.json thresholds | medium |
| `node.op.disc-dispatch` | operational_discipline | `dispatch` discipline (active-pattern) | DISCIPLINES.md:30 | high |
| `node.op.disc-observability` | operational_discipline | `observability` discipline (implemented) | DISCIPLINES.md:29 | high |

Candidate edges (illustrative): `node.op.inv-invoke-runs --observed_by--> node.op.gap-cluster`;
`node.op.gap-cluster --triggers--> node.op.trig-reflect`; `node.op.cap-invoke --governed_by-->`
(no operational_constitution node exists yet → **evidence gap**, see residue).

## Seed boundaries (binding)

1. Every node carries `status: candidate` and a cited `evidence_refs`. No node is promoted.
2. Telemetry nodes max out at L3. Promotion → Constitution Governance + ontology-harness.
3. No `operational_constitution` / `operational_axiom` node is created here — those require
   PromotionRecord and the owner. The apex slots are declared but **empty** by design.
4. Branch stays distinct from `run-context` (B3).

## What this seed demonstrates

The operational branch is **structurally seedable today** from existing telemetry + literature, and
the highest-category slots (constitution/axiom) are real but **deliberately empty pending governance**
— which is exactly the verdict: disciplines feed the apex, they are not the apex.
