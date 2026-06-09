# Gap 4 — Current → target transition plan

> **Candidate. Not a contract.** Claims tagged `[proven]` / `[hypothesis]`. Closes the fourth inherited
> GoldenQuill gap: GoldenQuill described a target state but no explicit path from where the client is
> today to where the system should land. No pricing or named-client commitments.

## Current state (filled in assessment)

`[PLACEHOLDER — current state per dimension, from assessment]`:

| Dimension | Today (typical) |
| --- | --- |
| BI | dashboards exist, denominators undocumented, trust is by instinct |
| Knowledge | lessons in staff memory and stale docs |
| Data boundaries | implicit; no signed register |
| Learning loop | none — outcomes are not wired back to the next run |
| Agents | absent or ungoverned |

## Target state

| Dimension | Target |
| --- | --- |
| BI | every key metric evidence-linked + graded (`veracidade` + `evidence_refs`) |
| Knowledge | governed promotion DAG; reuse only after an owner decision |
| Data boundaries | signed classification register, fail-closed |
| Learning loop | events → candidate → review → decision → promoted, with an audit ledger |
| Agents | routed by ontology, deterministically gated, self-validating |

## The path — staged, layer-gated

**[proven]** layer-gating (`G-layer`): a layer installs only after the prior layer produced its evidence.
This makes the transition incremental, not big-bang.

| Stage | What lands | Gate to advance | Honesty posture |
| --- | --- | --- | --- |
| **0 — Assessment** | ontology axes, data/agent inventory, lane choice, run boundary, proof metric | decisions D1–D7 answered | nothing installed yet |
| **1 — BI lever** | one metric rebuilt evidence-linked + graded on real data | the proof metric reproduces from its evidence chain, grades `high` | first measurable value |
| **2 — Boundaries** | classification register signed | register signed before any agent runs | **register is advisory + manual hash in pilot-1** `[hypothesis]` |
| **3 — Loop** | promotion DAG + 11-gate validator + append-only ledger | gate dry-run passes on sample historical runs; a deliberate violation is blocked | **owner decision stays human** `[proven]` |
| **4 — Agents** | ontology-routed, gated agents | per-agent self-validation passes; cross-family review | propose-only on client data `[hypothesis]` |
| **5 — Self-maintenance** | autonomous promotion scorer, cryptographic register signing | accumulated history justifies it | **post-pilot target, not pilot deliverable** `[hypothesis]` |

## What is explicitly NOT in the pilot

**[hypothesis]** stated plainly so the target is not over-sold:

- The **autonomous promotion scorer** runs as a **manual periodic review** in pilot-1 — we do not sell
  autonomous scoring.
- The **classification register** runs **advisory with a manual operator hash** — cryptographic signing
  is a later stage when agent volume justifies it.
- The **owner decision** is **never** automated.

**The honest one-line target:** *pilot-1 ships a deterministic gate runner + intake + append-only ledger
that automate ingestion and gating, with a proposal-only scorer and a human owner decision; the
self-maintaining pipeline is the post-pilot horizon.*

## Per-vertical note

The transition runs in parallel across cap factory and logistics; Stage 1 (the BI lever) is reached
independently per vertical, then compared to test generalization. **[hypothesis]**.
