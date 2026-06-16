# L2 — Carry-set plan + fanout plan

Step `scaffold-operational-tower`. The candidate carry-set the operational branch should record,
and the 5-role fanout that will validate it. Confirmed set lands in [CARRY-SET.md](../CARRY-SET.md)
after analysis. Tags: **[SB]**, **[H]**.

## Candidate carry-set (to confirm / refute)

**Node types** [SB operational-ontology slice owns: route patterns, lessons, failure modes,
context solutions, prompt/capability contracts, telemetry thresholds, maintenance triggers]:

| Node | Source today | Status |
| ---- | ------------ | ------ |
| route / dispatch | `*.dispatch.json` (63) | SB |
| sigil / capability | `necronomicon/capabilities.json`, by-sigil indexes | SB |
| prompt-contract | sigil SKILL.md output contracts | SB |
| discipline | `DISCIPLINES.md` | SB |
| decision | `decision-gate` signals (9), dispatch gates | SB |
| invocation | envelopes / signals (401) | SB |
| lesson | `workflow-reflect` output | SB (sparse) |
| failure-mode | observer.workflow_gaps in envelopes | SB |
| context-solution | context-builder outputs | SB |
| telemetry-threshold | `observability/config.json` thresholds | SB |
| maintenance-trigger | reflection_trigger, sigil-maintenance-loop | SB |
| operational-axiom / operational-constitution | — | **H (the proposal)** |

**Edge types** — reuse the existing single edge catalog
([DAG-AND-METRICS.md §3](../../DAG-AND-METRICS.md), branch-aware): `triggers`, `derived_from`,
`governed_by`, `realized_by`, `observed_by`, `drifts_from`, `contradicts`. **Do not invent a new
catalog.** [SB]

**Mutation types** the branch records: route run recorded · capability invoked · decision gated ·
reflection triggered · gap found · discipline hardened [H, no stream yet] · lesson promoted to
policy/constitution [H, no stream yet].

## Branch boundary [SB RECONCILIATION.md §1]

Operational branch = knowledge about **agent operation** (routes, sigils, prompts, disciplines).
Distinct from **`run-context` (B3)** = per-run denominators (run id, org scope, deadline,
lifecycle state). Keep them separate; the seed must not re-collide these.

## Fanout plan (step 4 — 5 role-bound lanes, parallel, parent_synthesis)

| Role | Reads | Returns |
| ---- | ----- | ------- |
| `authority-hierarchy-reader` | ONTOLOGY-ARCHITECTURE, BUSINESS-ONTOLOGY, PROMOTION-LIFECYCLE | can a discipline reach L6/L7? evidence + verdict-input |
| `discipline-authority-reader` | DISCIPLINES.md, README, HIDDEN-DISCIPLINE-SCAN | what promotion a discipline can/can't drive; the canonical-discipline precedent |
| `telemetry-derivation-reader` | observability envelopes, dispatch files, reflection-state | which carry-set nodes/edges are derivable, at what authority |
| `branch-schema-reader` | ontology-vault SKILL + branch-aware candidates, edge catalog | operational branch schema shape + run-context boundary |
| `axiom-coherence-adversary` | all of the above | strongest refutation of H0; failure conditions |

Each lane returns: source claims w/ concrete paths · candidate nodes/edges marked · confidence ·
missing-source residue. Synthesis → `sessions/operational-analysis-receipts.md`.
