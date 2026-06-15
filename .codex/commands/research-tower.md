# Arcanum Sigil: research tower

<!-- arcanum:capability-id research-tower -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command research-tower -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-research-tower-<UTC timestamp>`.
- `capability.id`: `research-tower`
- `capability.kind`: `sigil`
- `capability.tier`: `arcana`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum sigil `research-tower` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `research-tower`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/research-tower/README.md

````markdown
# Research Tower

Research Tower is a draft Arcana sigil for turning a paper, source corpus, or
research question into a reproducible local learning tower. It generalizes the
AutoBayes research run into a standard contract: source-first claims, notation
translation, local glossary, governed definitions, distilled knowledge,
related-work crosswalks, bridge decisions, residue, validation, and final
operator-facing learning packs.

Status: draft candidate, not promoted.

## Problem Solved

One strong research run can be hard to repeat. The Research Tower sigil makes
the research method reusable by requiring every learning artifact to carry:

- source evidence or an explicit inference label;
- local-vs-canonical promotion status;
- notation explanations when symbols matter;
- reusable definitions and glossary entries;
- distilled operator knowledge;
- unresolved residue and follow-up routes;
- validation evidence that the tower can be trusted by a later agent.

## When To Use

Use this sigil when the target is more than a quick summary:

- a paper needs to become durable Arcanum-facing understanding;
- related papers must be mapped without losing source boundaries;
- notation, definitions, and examples must become teachable;
- a future sigil, spell, runtime, or ontology decision needs a research basis;
- subagents are useful, but their outputs must be closed and reconciled.

## When Not To Use

Do not use this sigil for:

- a one-paragraph paper summary;
- canonical term promotion without a separate governance decision;
- implementation work that already has an approved task-session route;
- unbounded literature review with no artifact contract;
- replacing the source paper with an Arcanum analogy.

## Standard Artifact Set

A standard research tower should produce or update:

- `README.md` - local orientation and artifact index;
- `TOWER.md` - layer model, gates, and closure state;
- `levels/L0-corpus.md` - source inventory and evidence boundary;
- `levels/L1-residue-map.md` - open questions and research lanes;
- `levels/L2-closure-plan.md` - closure tasks and validation route;
- `NOTATION.md` - local notation bridge to shared notation terms;
- `GLOSSARY.md` - local glossary with promotion status;
- `DEFINITIONS.md` - governed definitions with intuition and misuse warnings;
- `DISTILLED-KNOWLEDGE.md` - compact operator knowledge;
- `tracks/paper-claim-ledger.md` - claim/source/inference ledger;
- `tracks/related-framework-crosswalk.md` - related paper/framework map;
- `tracks/*-definition-card.md` - reusable cards for important concepts;
- `tracks/*-worked-example.md` - symbolic or concrete examples when needed;
- `tracks/*-bridge-decision.md` - borrow/block/analogy-only/promotion decision;
- `residue/open-residue.md` - remaining questions and future tasks;
- `FINAL-LEARNING-PACK.md` - final source-backed operator pack;
- `work-pack/*-RESULT.md` - execution evidence when routed by task-session.

## Extraction Source

This candidate was extracted from the AutoBayes research tower. The AutoBayes
run proved the useful artifact spine: claim ledger, notation bridge, glossary,
definitions, related-framework crosswalk, definition cards, worked example,
implementation residue note, bridge decision, final learning pack, and explicit
local-only promotion boundary.

## Lifecycle

Research Tower is an Arcana candidate because it governs a multi-artifact,
multi-source learning workflow and coordinates other capabilities. It should
compose with:

- `refine` for shaping the research question and candidate route;
- `dispatch-spec` for route and subagent strategy design;
- `context-builder` for compact source/evidence packs;
- `feature-glossary` for local glossary extraction;
- `definitions-governance` for definition authority and drift checks;
- `distill` for compact concept units and operator knowledge;
- `task-session` for bounded execution;
- `codex-goal-profile` for long-running native Codex research goals;
- `experiment-harness` for replay validation before promotion.

## Evidence Execution Handoff

Research Tower should hand off instead of expanding when the next blocker is
empirical evidence production rather than durable source understanding.

Route to `research-evidence-harness` when the tower or target project needs:

- append-only run schemas;
- JSONL fixture validation;
- objective-vector or metric calculators;
- reviewer-rubric ingestion;
- result summaries;
- claim-adjudication readiness from measured runs.

This preserves the tower's local-learning authority while letting a dedicated
evidence harness own data mechanics and publication-safe evidence boundaries.

## Promotion Rule

This sigil may create local research knowledge. It may recommend promotion
candidates, but it must not promote source terms into Inventory, Ontology,
canonical glossary, sigils, spells, or runtime contracts without a later
governed decision.

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/research-tower/SKILL.md

````markdown
---
name: research-tower
description: "Use when: turning a paper, source corpus, or research question into a governed local research tower with source-first claims, notation bridge, glossary, definitions, distills, related-work map, bridge decisions, residue, and a final learning pack."
argument-hint: "<source-or-topic> [--target <folder>] [--preset compact|standard|full|deep] [--with-subagents] [--promotion-check]"
tier: arcana
domain: research-governance
version: 0.1.0
origin: extracted from the AutoBayes research tower closure
allowed-tools: Read, Write, Bash, Glob, Grep, Task
---

# Sigil: Research Tower

<objective>
Transform a paper, source corpus, or research question into a reproducible,
source-backed local learning tower that another agent can inspect, reuse, and
extend without rediscovering the same conceptual work.
</objective>

<logic-type>
Arcana: governed research synthesis with evidence boundaries, local semantic
authority, subagent closeout, and promotion guardrails.
</logic-type>

<applicability>
Use this sigil when:

- the user wants durable understanding rather than a short summary;
- source claims, related papers, notation, and definitions need separation;
- the result should teach Arcanum operators in the user's design language;
- a future sigil, spell, ontology, runtime, or implementation decision depends
  on the research;
- subagents may be spawned and must be reconciled before closure.
</applicability>

<inputs>
Expected inputs, when available:

- primary source URL, PDF path, paper title, corpus path, or research target;
- intended output folder;
- desired depth: `compact`, `standard`, `full`, or `deep`;
- known related papers or concepts;
- existing local research artifacts;
- target audience or operator lens;
- promotion boundaries and non-goals;
- subagent strategy or delegation preference.
</inputs>

<process>
1. Resolve the research target and output root.
2. Verify whether related artifacts already exist before creating new ones.
3. Create or update a source record with version, URL/path, date checked, and
   source boundary.
4. Build the tower scaffold:
   - `README.md`,
   - `TOWER.md`,
   - `levels/L0-corpus.md`,
   - `levels/L1-residue-map.md`,
   - `levels/L2-closure-plan.md`,
   - `gates/closure-gates.md`,
   - `residue/open-residue.md`.
5. If route complexity is high, design a dispatch route with a mandatory
   subagent closeout ledger.
6. Build a notation bridge before deep synthesis when the source uses formal
   symbols. Link reusable symbols to `research/shared-notation-glossary.md`
   when a repository-level shared glossary exists.
7. Build a paper/source claim ledger that separates direct source claims,
   related-source claims, local inference, analogy, and open residue.
8. Create the local glossary. Every entry must include source kind, local
   meaning, Arcanum reading, promotion status, and misuse warning when relevant.
9. Create governed definitions for concepts that later artifacts will depend
   on. Keep formal expression, notation meaning, intuition, and anti-misuse
   guidance together.
10. Distill the target into compact operator knowledge:
    - one-sentence model,
    - compositional spine,
    - what to borrow,
    - what to keep analogy-only,
    - what to block.
11. Map related papers or frameworks only as far as they close named residue.
12. Produce definition cards and worked examples for the concepts that carry
    the most reasoning load.
13. Produce bridge decisions using explicit statuses:
    - `borrow-carefully`,
    - `analogy-only`,
    - `block`,
    - `promotion-candidate`,
    - `future-work`.
14. Reconcile all subagent outputs. Mark each spawned lane `closed`,
    `integrated`, `rejected`, or `blocked`; no hidden open subagent work may
    remain at closure.
15. Create the final learning pack with source-backed claims, notation entry
    point, operator model, borrow/block decisions, closed residue, and honest
    cutoff.
16. Validate structure, links, required artifacts, source labels, promotion
    guardrails, and subagent closeout.
17. Return a concise closure summary with produced artifacts, validation, open
    residue, and next governed route.
</process>

<evidence-execution-handoff>
Research Tower must hand off when the next blocker is empirical evidence
production rather than source-backed understanding.

Route to `research-evidence-harness` when the target needs:

- append-only run schemas;
- JSONL fixture validation;
- objective-vector, scoring, or reviewer-rubric checks;
- dry-run result summaries;
- live-run data integrity;
- claim-adjudication readiness from measured results.

The handoff should name the source/tower artifacts that support the experiment,
the evidence mechanics still missing, and the claim or paper section blocked by
missing run data.
</evidence-execution-handoff>

<source-kind-taxonomy>
Use these labels consistently:

- `primary-source`: stated by the main source;
- `related-source`: stated by a related paper or external source;
- `local-inference`: inferred from source-backed material;
- `analogy`: useful Arcanum mapping, not source meaning;
- `operator-reading`: practical design interpretation for the user;
- `open-residue`: unresolved question or future task.
</source-kind-taxonomy>

<subagent-closeout-rule>
When subagents are spawned, closure requires a visible ledger with:

- subagent/lane name;
- assigned question;
- evidence returned;
- integration decision;
- rejected or blocked material;
- final status;
- owner of follow-up residue.

A research tower cannot be marked closed while any subagent lane is implicit,
unreviewed, or missing an integration decision.
</subagent-closeout-rule>

<promotion-rule>
Research Tower outputs are local research artifacts by default. They may teach,
compare, and recommend, but they must not promote vocabulary or behavior into
Inventory, Ontology, sigils, spells, runtime contracts, or canonical definitions
without a separate governed promotion decision.
</promotion-rule>

<quality-bar>
A successful execution must:

- verify existing artifacts before creating new ones;
- cite or path-link the source evidence used;
- distinguish source claims from Arcanum readings;
- make important notation learnable before using it heavily;
- produce glossary, definitions, distilled knowledge, and final learning pack;
- close named residue or move it into explicit future work;
- reconcile every subagent lane;
- preserve local-only promotion boundaries;
- hand off to an evidence harness when data mechanics, metrics, or claim
  adjudication become the blocker;
- validate required artifacts and links;
- leave another agent able to reproduce or audit the learning path.
</quality-bar>

<anti-patterns>
Avoid:

- summarizing the paper without a reusable artifact spine;
- turning analogies into source claims;
- promoting terminology because it sounds useful;
- skipping notation until the final pack;
- hiding uncertainty inside polished prose;
- using related papers as unbounded background;
- spawning subagents without a closeout ledger;
- calling the tower closed while residue is unnamed;
- producing final recommendations without borrow/block decisions.
</anti-patterns>

<output-contract>
Return:

```markdown
## Research Tower Summary

- Target: <source-or-topic>
- Output root: <path>
- Depth: compact | standard | full | deep
- Source record: pass | partial | block
- Existing artifacts checked: yes | no
- Required artifacts: pass | partial | block
- Notation bridge: pass | not-needed | block
- Glossary/definitions: pass | partial | block
- Related work: pass | not-needed | partial | block
- Subagent closeout: pass | not-used | block
- Promotion boundary: local-only | promotion-candidates-listed | block
- Validation: pass | partial | fail | not-run
- Final learning pack: <path or none>
- Open residue: <count>

### Produced Or Updated

- <path> - <role>

### Next Governed Route

1. <next action>
```
</output-contract>

````
