# Hypothesis, sub-questions, and corpus

Grounding for [operational-ontology-research.dispatch.json](operational-ontology-research.dispatch.json).
Tags: **[SB]** source-backed (cited path) · **[H]** hypothesis · **[T]** tension to adjudicate.
All findings are *candidate* — nothing here is promoted.

## Hypothesis

**H0:** `arcanum/disciplines/DISCIPLINES.md` should be the **highest knowledge category**
for an **operational ontology branch** of domainspec-core, on the same authority tier as
**axioms** and **constitutions**. [H]

## Sub-questions the route must answer

- **Q1 — Authority:** Where do axioms, constitutions, and disciplines actually sit today, and
  can a discipline rise to L6/L7? [T]
- **Q2 — Carry-set:** Which **node, edge, and mutation types** should the operational branch
  carry (routes, sigils, prompts, disciplines, decisions, lessons, failure modes, telemetry
  thresholds, maintenance triggers)?
- **Q3 — Literature:** What governance/operational literature already exists to build on?
- **Q4 — Telemetry:** What can be **derived from scattered telemetry**, and at what authority?
- **Q5 — Branch:** Can we seed a candidate operational branch now, kept distinct from
  `run-context` (B3)?

## Q1 — The existing authority hierarchy (the core tension) [T]

The repo already ranks knowledge. Treating disciplines as axiom-level collides with this.

| Level | Category | Meaning | Evidence bar |
| ----- | -------- | ------- | ------------ |
| L7 | **Axiom** | Load-bearing behavior invariant downstream governance depends on. | Strong evidence, dependency + contradiction review, explicit commitment. |
| L6 | **Constitution** | Enforceable governance for form/model/transformations/review gates that *preserve* axioms. | Affected artifacts, allowed transformations, review gates, rollback. |
| L5 | Promoted entry / policy | Approved knowledge within a use scope. | Confidence review, approval, rollback. |
| L4 | Reviewed premise | Falsifiable working bet. | Falsification criteria, contradiction path. |
| L3 | Ontology candidate | Thick draft with branch/scope/evidence/confidence. | Visible candidate status. |
| L0–L2 | Raw → cataloged → reviewable signal | Logs, inventory, lifecycle envelopes. | Support / review-input only. |

[SB] `arcanum/development/cyberalchemy-ontology-lifecycle/ONTOLOGY-ARCHITECTURE.md` (Authority Levels §, L0–L7; ladder `axiom > constitution > policy > entry > candidate`).
[SB] `arcanum/BUSINESS-ONTOLOGY.md`: *"Axioms are the load-bearing truths… treated as indisputable constraints until overwhelming empirical evidence forces revision."* *"Constitutions are the codified governance rules… derived from Axioms… An Axiom explains the why, a Constitution mandates the how."*

**Where disciplines sit:** [SB] `arcanum/disciplines/DISCIPLINES.md` — a *catalog* of reusable
operating practices (statuses `candidate` → `active-pattern` → `implemented` → `canonical`).
The whole catalog is marked **`Status: candidate`**. Growth Rule: *"Discipline evidence can
recommend a route, but it cannot directly promote registry, ontology, glossary, sigil, or
spell knowledge."* README boundary: disciplines *"must not claim promotion authority for
sigils or spells"* and *"must not treat execution evidence as canonical knowledge without the
relevant owner review."*

**The tension [T]:** axioms/constitutions are *load-bearing authority*; disciplines are
*forbidden from claiming authority*. They are not the same tier today. Note though that some
disciplines (`schema`, `artifact-constitution`, `quality-bar`, `validation-experiment`) are
already `canonical` with steward **Constitution Governance** — i.e. **a discipline can
*require/feed* a constitution**, which is the most likely coherent reframing of H0.

**Candidate verdict to test [H]:** disciplines are the *discovery/evidence layer* that feeds
an operational **constitution + axiom** layer; the "highest category" of the operational
branch is an *operational axiom/constitution set*, with `DISCIPLINES.md` as its disciplined
**source**, not its authority. The decision-gate step adjudicates this.

## Q2/Q5 — What the operational branch carries [SB candidate / H]

[SB] `arcanum/development/cyberalchemy-ontology-lifecycle/` operational-ontology slice
(`04-operational-ontology/concepts.md`): the Operational Ontology **owns** route patterns,
operational lessons, failure modes, context solutions, capability/prompt contracts, telemetry
thresholds, maintenance triggers — and is a **candidate extension branch**, *"not a permanent
fourth branch until user or ontology-harness review accepts that branch shape"*
([ONTOLOGY-ARCHITECTURE.md]). It does **not** own raw memory, raw logs, unreviewed telemetry,
or canonical capability mutation.

Candidate **carry-set** for the seed (to be confirmed in `CARRY-SET.md`):

- **Node types:** route / dispatch, sigil (capability), prompt-contract, discipline, decision,
  lesson, failure-mode, context-solution, telemetry-threshold, maintenance-trigger.
- **Edge types:** `triggers`, `derived_from`, `governed_by`, `refutes/contradicts`,
  `realized_by` (reuse the branch-aware edge catalog, not a new one).
- **Mutation types:** route run recorded, capability invoked, decision gated, reflection
  triggered, discipline hardened, lesson promoted to policy/constitution.

[SB] Branch-aware model + edge catalog already exist:
`arcanum/arcana/ontology-vault/development/BRANCH-AWARE-ONTOLOGY-CANDIDATE.md` and
`projects/ontologize/DAG-AND-METRICS.md §3` (single edge catalog = source of truth). The
operational branch must stay **distinct from `run-context` (B3)** —
[RECONCILIATION.md](../RECONCILIATION.md) §1 already renamed B3 to avoid exactly this collision.

## Q3 — Literature corpus (read-only)

| Path | What it gives |
| ---- | ------------- |
| `arcanum/BUSINESS-ONTOLOGY.md` | Axiom & constitution definitions; the why/how split. |
| `arcanum/development/cyberalchemy-ontology-lifecycle/ONTOLOGY-ARCHITECTURE.md` | L0–L7 authority levels; operational branch as candidate extension. |
| `arcanum/development/cyberalchemy-ontology-lifecycle/PROMOTION-LIFECYCLE.md` | How knowledge rises through tiers. |
| `arcanum/disciplines/DISCIPLINES.md` + `README.md` + `development/HIDDEN-DISCIPLINE-SCAN.md` | Discipline model, boundary, growth rule, current statuses. |
| `arcanum/arcana/ontology-vault/SKILL.md` + `development/BRANCH-AWARE-ONTOLOGY-CANDIDATE.md` | Branch-aware ontology, edge rules, confidence/premise model. |
| `projects/ontologize/RECONCILIATION.md`, `ONTOLOGY-BRANCHES.md`, `DAG-AND-METRICS.md` | The operational-vs-run-context naming split; edge catalog. |

## Q4 — Telemetry corpus (candidate, non-authoritative) [SB]

Richest stream first. Shapes captured while authoring; see step `inventory-operational-telemetry`.

| Stream (path) | Volume | Key fields → operational use |
| ------------- | ------ | ---------------------------- |
| `arcanum/.arcanum/observability/signals/sigil-invocations.jsonl` | **~390 meaningful executions** | `sigil`, `tier`, `mode`, `capability.id`, `execution.status`, `observer.{quality_bar_status, workflow_gaps[], reflection_trigger, recommendation}`, `target_artifact` → invocation nodes, mode-transition + gap + reflection edges. |
| `arcanum/.arcanum/observability/reflection-state.json` | aggregates | per-sigil execution/output/gap counters → maturity & reflection-trigger evidence. |
| `arcanum/.arcanum/observability/by-sigil/*.jsonl` | 17 indexes | per-sigil invocation index (invoke 95, task-session 85, context-builder 55…). |
| `arcanum/.arcanum/observability/envelopes/` + `runs/` | full records | request/intent, validation sequences, run open→close lifecycle. |
| `arcanum/.arcanum/observability/hooks/hook-operations.jsonl` | ~1.2M | observability pipeline meta-events (session→hook→signal). |
| `**/*.dispatch.json` (60+) | routes | `subagent_strategy.roles[]`, `techniques`, `native_stage_receipts`, `trace_events` → route + delegation + receipt nodes. |
| `.arcanum/necronomicon/capabilities.json` | install state | selected sigils/spells/harness commands → capability inventory. |
| `docs/signals/{terminal-guard,delegation-tuning}.jsonl` | aux | command risk, delegation profile/outcome. |

**Authority note [SB]:** by the operational-ontology slice's own rule, unreviewed telemetry is
**not** owned by the branch — it is L0–L2 evidence that can *seed candidate nodes* (L3) but
must be reviewed before any promotion. This is exactly the `telemetry-non-authoritative` gate.

## Open residue carried into execution

- Decision pending: does the verdict reframe H0 (disciplines feed, not are, the axiom layer)? → `decision-gate`.
- Carry-set is candidate only; node/edge schema must reuse the existing edge catalog. → `definitions-governance` / `ontology-vault`.
- Operational branch acceptance is a `user or ontology-harness review` gate per ONTOLOGY-ARCHITECTURE. → handoff.
