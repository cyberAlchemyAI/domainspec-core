---
id: refine-seed-mutation-execution-mechanics
project: ui-prototyping-studio
title: "Refine Seed — Mutation Execution Mechanics"
status: seed
node_type: refine-seed
run_id: 20260615-mutation-execution-mechanics
updatedAt: 2026-06-15
---

# Refine Seed — Mutation Execution Mechanics

## Target

How `ApplyApprovedBatch` turns an approved `MutationBatch` (a set of `MutationTask`s) into the **next
revision's prototype HTML** — the one step in the studio loop that currently has no design. Get the
**model and architecture** right, evaluating each candidate approach.

## Grounded finding (evidence baseline)

- **Apply does not mutate HTML today.** `apply-approved-batch.ts` validates gates (`AUTO_APPLY_FORBIDDEN`,
  `BASELINE_GATE_UNSATISFIED`, `BATCH_APPROVAL_REQUIRED`, staleness) and appends one
  `RevisionManifestEntry`. There is **no HTML transformation engine**.
- **`MutationTask` is a description, not a patch:** `{taskId, target, intent, changeType, acceptanceText,
  priority}`. **`DiffSummary` is counts-only:** `{added, changed, removed}`.
- So "execution" is currently bookkeeping; the actual prototype edit is unspecified.
- Runtime is **Claude Code-native** (`DEC-RUNTIME-CLAUDE-CODE-011`, `DEC-CLI-NOT-MCP-012`): Claude Code is
  the generation/mutation engine; the `studio` CLI is the seam; the core owns gates + determinism.
- Synthesis (comment→task) is **deterministic by design** (sha1 task IDs, no timestamps) — intent is
  sacred; the engine must not reinterpret it.
- Annotation targets carry a stable `data-od-id` (`DEC-ATOMIC-IDS-014`) — mutations should preserve/track it.

## Candidate approaches to evaluate

- **A — Deterministic patch.** `MutationTask` carries machine-applicable, typed change params; a
  deterministic transformer edits the HTML at `target`. *Auditable, reproducible; limited expressiveness;
  pushes burden onto synthesis to fully specify changes.*
- **B — Agentic regeneration.** Claude Code reads the tasks (`intent`, `acceptanceText`) + current HTML and
  produces the new HTML. *Flexible, handles fuzzy intent; non-deterministic, weaker audit, drift risk.*
- **C — Hybrid: agentic-propose + deterministic-validate** (operator hypothesis). Claude Code proposes the
  mutated HTML; **deterministic validators** then check it honors the `MutationTask` contract before it
  becomes a revision. *Agentic flexibility behind deterministic guardrails.*

## Core tensions (for the dialectic)

Determinism / auditability / reproducibility (governance ethos, INV-6 append-only) **vs** expressiveness of
changes **vs** "generation is free" in a Claude Code-native runtime **vs** `data-od-id` stability **vs** the
"saw-the-diff" apply-gate ergonomics (`OQ-2`).

## What this run must produce

A chosen **execution model + architecture**: the `MutationTask`/`DiffSummary` schema (do they need to grow?),
the apply state machine, **where determinism lives** (synthesis? validators? both?), the **validator set** (and
how each is deterministic), the engine contract (what Claude Code does, if anything), and a **non-executed
implementation plan** — with each approach evaluated and a **toy-game** falsification before the decision.

## Run parameters

- **Preset:** `full` (operator: "get the model and architecture right").
- **Research:** `research-if-gap-appears` (local-first; one bounded external pass only if a named gap appears,
  e.g. prior art on AI-edit + deterministic-validation patterns).
- **Write scope:** this run folder; on synthesis, *proposed* updates to SPEC / operations / architecture
  (proposals only — no canonical mutation without approval).
- **Validation surface:** toy-game (apply a sample `MutationTask` to sample HTML under each approach), the
  existing e2e/ACs, and the determinism/auditability invariants.

## Planned stage configuration (canonical 10-stage loop)

Context Builder → Invoke Define → Interrogation (refine-review) → Research decision → Distill **[tournament:
A vs B vs C]** → Invoke Design **[dialectic: determinism vs flexibility]** → Interrogation
(refine-design-review) → Distill Repair **[toy-game falsification]** → Invoke Plan → Final Interrogation +
synthesis. Subagents **recommended** (one advocate per approach + a validator-designer + a toy-game runner +
parent synthesis).
