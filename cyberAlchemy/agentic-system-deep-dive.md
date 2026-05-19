---
module: cyberalchemy-agentic-system
version: current
status: candidate
updatedAt: 2026-05-19
docType: deep-dive
---

# CyberAlchemy Agentic System Deep Dive

Navigation: [agentic-system-navigation.md](agentic-system-navigation.md)
Synthesis: [agentic-system-ontology-synthesis.md](agentic-system-ontology-synthesis.md)
Definition: [agentic-system-definition.md](agentic-system-definition.md)
Architecture: [agentic-system-architecture.md](agentic-system-architecture.md)
Inventory pipeline: [agentic-system-inventory-ontology-pipeline.md](agentic-system-inventory-ontology-pipeline.md)
Ontology entry model: [agentic-system-ontology-entry-model.md](agentic-system-ontology-entry-model.md)
Work layer: [agentic-system/README.md](agentic-system/README.md)
First working slice: [agentic-system-first-working-slice.md](agentic-system-first-working-slice.md)

## Purpose

This document is the in-depth companion to the CyberAlchemy agentic system synthesis.

The synthesis explains the whole idea in a readable arc. This file goes deeper topic by topic. It gathers the scattered philosophical, architectural, operational, inventory, ontology, memory, execution, and observability material into one consultable map.

Its main addition is the Ontology Promotion System: the governance mechanism that decides how raw observations become reusable inventory, how inventory becomes ontology, and how ontology becomes operational guidance for future agents.

## Reading Rule

Read this file when you need to answer one of these questions:

- What does each layer of the system own?
- What content should be centralized in ontology?
- How does inventory feed ontology without becoming the ontology itself?
- How does memory become evidence without becoming authority?
- How does an operational lesson become a route policy, capability update, premise, constitution, or axiom?
- Which source files should be consulted for each topic?

For the shortest conceptual explanation, use [agentic-system-ontology-synthesis.md](agentic-system-ontology-synthesis.md). For the first practical implementation pass, use [agentic-system-first-working-slice.md](agentic-system-first-working-slice.md).

## System Thesis

CyberAlchemy is a system for preserving alignment between intent, execution, and evidence.

It starts from a simple fracture:

```text
schema says what should be true
data shows what is actually true
```

Schema includes ontology, specification, contracts, policies, route definitions, prompt contracts, sigils, spells, tests, assumptions, axioms, and meta-models.

Data includes sessions, source files, code, telemetry, tests, run logs, agent outputs, user corrections, operational failures, observed friction, and runtime behavior.

The work of the system is to chase symmetry between these layers. When the layers diverge, the divergence should become visible, named, routed, reviewed, and learned from.

The system is not trying to make every fact canonical. It is trying to create a disciplined path from scattered evidence to reusable knowledge.

```text
intent
  -> specification
  -> execution
  -> observation
  -> residue and drift detection
  -> inventory
  -> ontology candidate
  -> promotion gate
  -> improved future context
```

Core sources:

| Topic                                        | Sources                                                                                                                                       |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Schema/data symmetry and translation residue | [agentic-system-architecture.md](agentic-system-architecture.md), [agentic-system-definition.md](agentic-system-definition.md)                |
| Drift and convergence                        | [saturn-research-presentation.md](saturn-research-presentation.md), [DRIFT-CONVERGENCE.md](../implementation/domainspec/DRIFT-CONVERGENCE.md) |
| Knowledge authority ladder                   | [KNOWLEDGE-SUBSTRATE-FLOW.md](../arcanum/spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md)                                         |
| Branch-aware ontology                        | [BUSINESS-ONTOLOGY.md](../arcanum/BUSINESS-ONTOLOGY.md), [Ontology Vault](../arcanum/arcana/ontology-vault/README.md)                         |
| Inventory and context retrieval              | [Inventory](../arcanum/arcana/inventory/README.md), [Context Builder](../arcanum/transmutations/context-builder/README.md)                    |

## Source Spine

The system already exists as fragments across the repository. The job of the new ontology work is to give those fragments a governed home.

| System Topic                 | Scattered Content To Compile                                                                 | Existing Anchors                                                                                                                                                                                                                 |
| ---------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Saturn                       | Drift, convergence, intent flowing down, evidence flowing back, correction loop.             | [saturn-research-presentation.md](saturn-research-presentation.md), [DRIFT-CONVERGENCE.md](../implementation/domainspec/DRIFT-CONVERGENCE.md)                                                                                    |
| DomainSpec                   | Structured intent, typed concepts, relationships, tests, observability, tuning.              | [DomainSpec README](../implementation/domainspec/README.md), [TUNING-LOOP.md](../implementation/domainspec/TUNING-LOOP.md), [OBSERVABILITY.md](../implementation/domainspec/OBSERVABILITY.md)                                    |
| Arcanum                      | Sigils, spells, lifecycle routing, reusable agent capability surfaces.                       | [Arcanum README](../arcanum/README.md), [CYBERALCHEMY-METHOD.md](../arcanum/framework/CYBERALCHEMY-METHOD.md), [Sigil Registry](../arcanum/registry/SIGILS.md), [Spell Registry](../arcanum/registry/SPELLS.md)                  |
| Inventory                    | Source summaries, reusable claims, tags, indexes, contradictions, lookup.                    | [Inventory](../arcanum/arcana/inventory/README.md), [agentic-system-inventory-ontology-pipeline.md](agentic-system-inventory-ontology-pipeline.md)                                                                               |
| Ontology                     | Branch authority, edge rules, confidence, promotion, premises, conventions.                  | [Ontology Vault](../arcanum/arcana/ontology-vault/README.md), [Ontology Harness](../arcanum/spells/ontology-harness/README.md), [agentic-system-ontology-entry-model.md](agentic-system-ontology-entry-model.md)                 |
| Memory                       | Active interaction, session memory, route ledger, side notes, user workflow continuity.      | [Necronomicon README](../arcanum/spells/necronomicon/README.md), [KNOWLEDGE-SUBSTRATE-FLOW.md](../arcanum/spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md)                                                           |
| Context Builder              | Task packs, selector evidence, relevance gates, excluded noise.                              | [Context Builder](../arcanum/transmutations/context-builder/README.md), [agentic-system-first-working-slice.md](agentic-system-first-working-slice.md)                                                                           |
| Execution                    | Invoke lifecycle, task sessions, stage contracts, route templates, telemetry envelopes.      | [Invoke README](../arcanum/spells/invoke/README.md), [Agent Execution Orchestrator SPEC](../implementation/domainspec/docs/features/agent-execution-orchestrator/SPEC.md)                                                        |
| Observability and reflection | Invocation signals, workflow reflection, tuning, maintenance proposals.                      | [Observed Invocation Loop](../arcanum/spells/observed-invocation-loop/README.md), [Workflow Reflect](../arcanum/arcana/workflow-reflect/README.md), [Sigil Maintenance Loop](../arcanum/spells/sigil-maintenance-loop/README.md) |
| Residue and resilience       | Stressors, residue, degradation, attractors, failed translations.                            | [Residuality Spec](../arcanum/arcana/residuality-spec/README.md), [DRIFT-CONVERGENCE.md](../implementation/domainspec/DRIFT-CONVERGENCE.md)                                                                                      |
| Exploration evidence         | Experiments and research projects that may feed evidence without becoming core architecture. | [agentic-system-knowledge-map.md](agentic-system-knowledge-map.md)                                                                                                                                                               |

## Saturn

Saturn is the convergence loop.

Its job is to keep intent and reality in contact. It gives the system a rhythm:

```text
define intent
  -> execute
  -> observe reality
  -> compare reality against intent
  -> detect drift
  -> route correction
  -> verify closure
  -> update the governing model
```

Saturn matters because an agentic system cannot improve by merely doing more work. It improves when work creates evidence, evidence is compared against intent, and the mismatch changes future behavior.

Saturn owns:

- the idea that drift is actionable;
- the expectation that evidence flows back into governance;
- the correction loop between plan and reality;
- the demand that convergence be verified, not assumed.

Saturn does not own:

- every implementation detail;
- ontology storage;
- memory mechanics;
- every execution route.

In the agentic system, Saturn becomes the top-level control loop that asks:

```text
What did we intend?
What happened?
What changed?
What drifted?
What should respond?
What evidence proves the response worked?
```

Ontology should contain Saturn as a governing concept, not just a metaphor. It should know which lower-level concepts realize it: DomainSpec structured intent, Arcanum execution routes, inventory evidence, bridge drift, telemetry, reflection, and promotion gates.

## DomainSpec

DomainSpec is the structured-intent discipline.

If Saturn asks whether reality matches intent, DomainSpec helps make intent precise enough to compare.

DomainSpec turns domain understanding into:

- typed concepts;
- relationships;
- feature specifications;
- tests;
- implementation obligations;
- observability signals;
- readiness checks;
- tuning feedback.

DomainSpec matters because vague intent cannot be defended. The system needs a model of what was meant before it can say that execution drifted.

DomainSpec owns:

- concept and relationship structure;
- specification as a source of derived obligations;
- test and observability derivation;
- drift/convergence vocabulary;
- tuning feedback from pipeline signals.

DomainSpec does not need to be explained as a separate hidden mechanism. In the CyberAlchemy system, it is the specification method that gives the convergence loop precise material to work with.

Ontology should treat DomainSpec as a method node with edges to:

- `structured-intent`;
- `typed-concept-graph`;
- `derived-test-obligation`;
- `observability-signal`;
- `drift-convergence`;
- `tuning-loop`.

The useful ontology question is:

```text
When an agent is doing specification or implementation work, which DomainSpec obligations should shape its context?
```

## Arcanum

Arcanum is the reusable agent capability system.

It takes repeated agent work and gives it a named operational surface: a skill, sigil, spell, lifecycle route, or maintenance loop.

Arcanum matters because agent work should not remain a pile of ad hoc prompts. A repeated behavior should eventually become a capability with:

- purpose;
- inputs;
- outputs;
- quality bars;
- anti-patterns;
- lifecycle owner;
- route contract;
- observability;
- maintenance path.

In this system:

- `invoke` owns define/design/plan/validate lifecycle authoring;
- `inventory` owns reusable source knowledge;
- `ontology-harness` composes inventory, ontology-vault, and context-builder;
- `ontology-vault` owns mapping, premise review, confidence review, and convention changes;
- `context-builder` owns task-shaped context selection;
- observed invocation and reflection capabilities provide evidence for future improvement.

Ontology should not duplicate the Arcanum registry. The registry names capabilities. Ontology explains when to use them, what they mean, what evidence supports their route policies, and what failures they avoid.

## Inventory

Inventory is the compiled evidence substrate.

It exists because raw files do not compound by themselves. Without inventory, every agent has to reread and resynthesize the same sources. With inventory, the repository develops a maintained knowledge layer that future agents can query.

Inventory owns:

- source manifests;
- source summaries;
- extracted claims;
- typed entries;
- tags;
- indexes;
- contradictions;
- lookup selectors;
- logs;
- lint gaps.

Inventory does not own:

- final meaning;
- route authority;
- silent promotion;
- raw source mutation.

The relationship is:

```text
raw source
  -> inventory entry
  -> ontology candidate
  -> context-builder proof
  -> execution guidance
```

Inventory should be generous in what it records, but clear about status. It can hold weak claims, contradictions, questions, and local observations. Ontology must be stricter because ontology guides agents.

The inventory entry should answer:

```text
What source did this come from?
What claim was extracted?
What is the claim type?
What supports it?
What contradicts it?
Where should a future agent look?
```

The ontology entry should answer:

```text
What does this mean?
Where does it apply?
How should an agent use it?
What evidence supports it?
What can invalidate it?
What route or decision does it affect?
```

This is why ontology is a semantic and operational superset of inventory, not a storage dump.

## Ontology

Ontology is the governed meaning layer.

It should contain thick knowledge entries: entries that are useful enough for an agent to act with them, while still preserving source evidence, confidence, scope, and invalidation rules.

An ontology entry should include:

- identity;
- definition;
- purpose;
- scope;
- exclusions;
- examples;
- non-examples;
- use-when rules;
- invalidation conditions;
- agent payload;
- typed edges;
- evidence;
- confidence;
- promotion state;
- maintenance triggers.

The core ontology branches for this system are:

| Branch                        | Authority                                                                                  |
| ----------------------------- | ------------------------------------------------------------------------------------------ |
| Philosophy Ontology           | CyberAlchemy principles, epistemic commitments, design taste, and method axioms.           |
| Knowledge Governance Ontology | Roles, branches, confidence, promotion, source authority, contradiction handling.          |
| Operational Ontology          | Agent operation knowledge: routes, lessons, failure modes, context solutions, maintenance. |
| Memory Ontology               | Memory patterns, privacy-scoped workflow models, side note classes, continuity rules.      |
| Capability Ontology           | Sigils, spells, skills, agents, route contracts, composition rules.                        |
| Feedback Ontology             | Signals, telemetry, reflection, tuning, drift, residuality, validation evidence.           |
| Bridge Ontology               | Traceability between intent, implementation, observation, and correction.                  |

The ontology should let agents retrieve knowledge capsules such as:

- "How should I decide whether to use invoke define or ontology-harness?"
- "What is the failure mode when memory is treated as authority?"
- "What source evidence supports Operational Ontology?"
- "Which context solution applies when designing ontology schema?"
- "Which telemetry signal implies a sigil needs maintenance?"

This is knowledge designed for use, not merely knowledge designed for storage.

## Operational Ontology

Operational Ontology is the ontology branch for agent operation knowledge.

It captures what the system learns about its own operation:

- route choices;
- sigil optimization;
- spell composition;
- skill definitions;
- agent briefing patterns;
- prompt contracts;
- context solution cards;
- failure modes;
- telemetry thresholds;
- maintenance triggers;
- user workflow constraints;
- shortcut candidates;
- capability drift.

Operational Ontology is where the system starts to govern the governor.

Its entries should answer questions like:

```text
When does this route work?
What evidence supports that claim?
What context does the agent need?
What should the agent avoid?
Which failure mode does this reduce?
Which capability should be improved if this repeats?
When should this lesson expire?
```

Example entry classes:

| Entry Class         | Example                                                                                                           |
| ------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Operational lesson  | `define-before-runner`: define prompt schema before implementing a runner when route semantics are unclear.       |
| Context solution    | `invoke-define-design`: context bundle for moving from definition to architecture.                                |
| Failure mode        | `memory-treated-as-authority`: one session observation becomes a standing rule without review.                    |
| Route policy        | `use-ontology-harness-for-promotion`: consequential knowledge promotion should route through ontology governance. |
| Capability pattern  | `observed-invocation-reflection`: telemetry plus repeated gap should trigger reflection.                          |
| Maintenance trigger | `sigil-output-drift`: repeated output mismatch should create a sigil maintenance proposal.                        |

Operational Ontology should not become a personal notebook of every run. It should promote only reusable operation knowledge with scope and evidence.

## Ontology Promotion System

The Ontology Promotion System is the mechanism that turns scattered evidence into governed knowledge.

It exists to prevent two opposite failures:

1. Useful lessons stay buried in sessions and are rediscovered forever.
2. Weak observations become rules too quickly and damage future work.

Promotion is the controlled path between those failures.

### Authority Ladder

Use this ladder as the default movement from raw material to operating context:

```text
raw interaction
  -> session evidence
  -> discovery baseline
  -> inventory knowledge
  -> ontology candidate
  -> reviewed premise
  -> confidence decision
  -> constitution or axiom
  -> bridge-validated operating context
```

Each step increases authority only when the owning capability has enough evidence to justify the move.

| State                              | Authority                    | Owner                                                  | Typical Use                                                   |
| ---------------------------------- | ---------------------------- | ------------------------------------------------------ | ------------------------------------------------------------- |
| Raw interaction                    | Very low                     | Session                                                | Captures what happened or what was said.                      |
| Session evidence                   | Low                          | Necronomicon or task session                           | Preserves run facts, route records, side notes, handoffs.     |
| Discovery baseline                 | Low-medium                   | Discovery or define route                              | Stabilizes early scope, vocabulary, contradictions, gaps.     |
| Inventory knowledge                | Medium                       | `inventory`                                            | Makes source-backed facts reusable and searchable.            |
| Ontology candidate                 | Medium                       | `ontology-vault` or ontology-harness                   | Proposes a governed meaning object with edges and scope.      |
| Reviewed premise                   | Medium, explicit uncertainty | `ontology-vault premise-review`                        | Holds a useful working bet that remains falsifiable.          |
| Confidence decision                | Medium-high                  | `ontology-vault promote-confidence` and decision owner | Decides evidence confidence and commitment confidence.        |
| Constitution                       | High                         | `decision-gate` and ontology convention route          | Codifies an operating rule or convention.                     |
| Axiom                              | Highest                      | ontology governance and decision owner                 | Promotes a load-bearing principle with contradiction review.  |
| Bridge-validated operating context | Alignment-specific           | `ontology-harness` and context-builder                 | Proves that context connects intent, evidence, and execution. |

### Promotion States

CyberAlchemy should use explicit states instead of vague labels like "known" or "canonical."

| State                | Meaning                                                                                                        | Can Guide Agents?                        |
| -------------------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| `raw`                | Unprocessed observation, source, note, session fragment, or user statement.                                    | No.                                      |
| `session-evidence`   | Captured as part of a run, checkpoint, route ledger, side note, or handoff.                                    | Only as local continuity.                |
| `discovery-baseline` | Organized into an early scope, glossary, discovery, or define baseline.                                        | Yes, with caveats.                       |
| `inventory-entry`    | Source-backed reusable entry with tags, source refs, contradictions, and lookup selectors.                     | Yes for evidence retrieval.              |
| `ontology-candidate` | Thick entry draft with meaning, context, agent payload, evidence, confidence, edges, and maintenance triggers. | Yes only if candidate status is visible. |
| `premise`            | Reviewed working bet with falsification criteria.                                                              | Yes when uncertainty is carried forward. |
| `reviewed`           | Survived premise or confidence review but has not become a stronger rule.                                      | Yes within scope.                        |
| `promoted`           | Accepted as a stable ontology entry for a defined scope.                                                       | Yes.                                     |
| `constitution`       | Codified operating rule, convention, or process constraint.                                                    | Yes, strongly.                           |
| `axiom`              | Load-bearing principle used to justify many downstream rules.                                                  | Yes, highest bar.                        |
| `retired`            | No longer active, but preserved for history.                                                                   | No, except as historical context.        |
| `contradicted`       | Evidence shows the entry is wrong, overgeneralized, or unsafe.                                                 | No, except as a warning.                 |

### Promotion Inputs

Promotion can start from several sources:

| Input               | Example                                                                   | First Destination                                |
| ------------------- | ------------------------------------------------------------------------- | ------------------------------------------------ |
| Source document     | A method file describes branch-aware ontology.                            | Inventory source summary.                        |
| Session memory      | A user repeatedly prefers progressive disclosure.                         | Session evidence, then memory pattern candidate. |
| Route ledger        | `invoke define` repeatedly needs ontology context before design.          | Operational lesson candidate.                    |
| Telemetry           | A sigil repeatedly emits validation gaps.                                 | Feedback ontology candidate.                     |
| Reflection report   | Workflow reflect identifies output drift.                                 | Maintenance proposal or operational lesson.      |
| DomainSpec drift    | Implementation no longer matches structured intent.                       | Bridge gap or drift finding.                     |
| User decision       | A privacy boundary is approved.                                           | Decision record, then possible constitution.     |
| Residuality finding | A process degrades under a known stressor but preserves a useful residue. | Failure mode or resilience pattern.              |

### Promotion Gates

Promotion gates should be visible and boring. They are what keep the system honest.

| Gate                        | Question                                                                           | Pass Condition                                                                                    | Fails To                     |
| --------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------- |
| Source coverage gate        | Is the source material identified?                                                 | Raw source path, session id, telemetry row, or explicit inference label exists.                   | `raw` or `session-evidence`. |
| Inventory completeness gate | Is the evidence reusable?                                                          | Summary, claim, source refs, tags, contradictions, and lookup selector exist.                     | inventory gap.               |
| Branch classification gate  | Does this belong in ontology, and where?                                           | Branch, type, scope, and owner are clear.                                                         | open ontology question.      |
| Thick entry gate            | Is this more than a pointer?                                                       | Content, context, agent payload, edges, evidence, confidence, promotion, maintenance are present. | ontology draft gap.          |
| Premise gate                | Is this a working bet?                                                             | Falsification criteria, counterevidence, and scope are named.                                     | candidate only.              |
| Confidence gate             | How supported and how committed are we?                                            | Evidence confidence and commitment confidence are both set and justified.                         | confidence review gap.       |
| Decision gate               | Does this change behavior, policy, privacy, architecture, or capability contracts? | Consequential tradeoff has explicit approval.                                                     | blocked promotion.           |
| Bridge gate                 | Does this claim alignment between intent and implementation?                       | Business/system or schema/data edges cite both sides and the evidence that connects them.         | bridge gap.                  |
| Context proof gate          | Can a future task use this without loading the whole corpus?                       | Context-builder produces a task pack that selects this entry and excludes irrelevant noise.       | retrieval gap.               |
| Maintenance gate            | When should this change?                                                           | Review trigger, expiry condition, contradiction path, and owner route are named.                  | stale-risk gap.              |

### Evidence And Commitment Confidence

Promotion must keep two confidence axes separate.

| Evidence Confidence | Commitment Confidence | Meaning                                                              | Action                                                               |
| ------------------- | --------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Low                 | Low                   | Exploratory idea.                                                    | Keep as candidate or research seed.                                  |
| High                | Low                   | True or well-supported, but not important enough to govern behavior. | Keep as reference or low-commitment ontology entry.                  |
| Low                 | High                  | Dangerous bet.                                                       | Require decision gate, premise review, and clear falsification path. |
| High                | High                  | Good promotion candidate.                                            | Promote within scope, with maintenance trigger.                      |

This split matters because the system should be able to say:

```text
we believe this is probably true
but we are not ready to build around it
```

or:

```text
we are choosing to rely on this before the evidence is strong
so the risk must be explicit
```

### Promotion Decision Matrix

| Candidate Type             | Promote To                                     | Minimum Evidence                                                             | Required Gate                                |
| -------------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------- | -------------------------------------------- |
| One-off memory observation | Session evidence                               | Captured context and source turn.                                            | Source coverage gate.                        |
| Repeated memory pattern    | Inventory entry or memory ontology candidate   | Repetition across sessions or a strong user decision.                        | Inventory completeness and privacy decision. |
| Source-backed concept      | Ontology candidate                             | Source summary, extracted claims, contradictions, branch classification.     | Thick entry gate.                            |
| Operational lesson         | Operational Ontology entry                     | Route evidence, applicability scope, avoided failure mode, expiry condition. | Premise or confidence gate.                  |
| Context solution           | Context Solution Catalog entry                 | Trigger fingerprint, recommended context, evidence selector, observed use.   | Context proof gate.                          |
| Capability route policy    | Capability Ontology entry or capability update | Repeated successful/failed routes and route rationale.                       | Confidence gate and capability owner review. |
| Privacy or workflow rule   | Constitution                                   | Explicit user decision, scope, affected memory behavior, rollback path.      | Decision gate.                               |
| Load-bearing principle     | Axiom                                          | Strong evidence, repeated use, contradiction review, explicit commitment.    | Highest ontology review and decision gate.   |
| Alignment claim            | Bridge entry                                   | Intent-side evidence, system-side evidence, observed/tested link.            | Bridge gate.                                 |

### Non-Promotion Rules

The system should refuse promotion when the entry would be epistemically unsafe.

- Do not promote directly from raw memory to ontology authority.
- Do not promote pointer-only ontology entries.
- Do not promote without source references or an explicit inference label.
- Do not promote a local trick into a general rule without cross-context evidence.
- Do not promote user workflow observations without a privacy class and decision boundary.
- Do not promote a route policy without naming failure modes and expiry conditions.
- Do not promote a bridge claim unless both sides of the bridge are visible.
- Do not overwrite contradictions. Preserve them and route them.
- Do not call a discipline a rule unless the system can enforce or review it.

### Promotion Record Shape

Every promotion decision should leave a compact record.

```markdown
---
id: promotion.<stable-id>
candidate: <ontology-entry-or-inventory-entry>
fromState: <state>
toState: <state>
branch: <ontology-branch>
owner: <capability-or-human-owner>
updatedAt: YYYY-MM-DD
evidenceConfidence: low | medium | high
commitmentConfidence: low | medium | high
decision: promote | defer | reject | retire | contradict
---

# Promotion: <Title>

## Claim

What is being promoted?

## Scope

Where does this apply?

Where does it not apply?

## Evidence

Inventory entries:

- <path>

Source references:

- <path>

Observed runs or telemetry:

- <path-or-id>

Counterevidence:

- <path-or-id>

## Gate Results

| Gate                   | Result     | Notes |
| ---------------------- | ---------- | ----- |
| Source coverage        | pass       |       |
| Inventory completeness | pass       |       |
| Thick entry            | pass       |       |
| Confidence             | pass       |       |
| Decision               | not-needed |       |
| Context proof          | pending    |       |

## Decision

Decision:

Rationale:

Affected entries:

Affected capabilities:

## Maintenance

Review trigger:

Expiry condition:

Contradiction path:

Rollback path:
```

### Promotion Outputs

A promotion pass can produce several kinds of output:

- thick ontology entry;
- ontology edge update;
- premise review;
- confidence promotion or demotion report;
- convention change proposal;
- decision record;
- context solution card;
- route policy update;
- capability maintenance proposal;
- contradiction record;
- retirement record;
- context-builder proof pack.

Promotion does not always mean "make stronger." Sometimes the correct promotion output is demotion, retirement, contradiction, or a better question.

## Memory

Memory is continuity.

It helps the system remember:

- the current objective;
- what was already tried;
- what the user decided;
- what route was selected;
- what gaps remain;
- what side notes appeared;
- what user workflow patterns might matter;
- what should be resumed next.

Memory should be execution-context driven. It should help agents avoid repetitive work and identify likely shortcuts. It should also help the system notice when a repeated shortcut deserves inventory or ontology review.

Memory owns:

- active interaction state;
- session continuity;
- route ledger facts;
- side notes;
- user workflow observations;
- pending gaps;
- handoff summaries.

Memory does not own:

- source authority;
- ontology authority;
- permanent user model claims;
- automatic promotion.

The correct flow is:

```text
memory observation
  -> session evidence
  -> inventory candidate when durable
  -> ontology candidate when reusable and governed
  -> decision gate when personal workflow or privacy is involved
```

The privacy rule is strict: user workflow memory can improve ergonomics, but it needs explicit scope before it becomes ontology-guided behavior.

## Context Builder

Context Builder is the retrieval discipline that prevents the system from drowning agents in everything it knows.

Its job is to select the smallest useful context slice for the current task.

The context pack should answer:

```text
What obligation is active?
Which ontology entries matter?
Which inventory entries prove them?
Which source refs are needed?
What is explicitly excluded as noise?
What gaps or confidence limits remain?
```

Context Builder should prefer:

- ontology entries for action guidance;
- inventory entries for source evidence and contradictions;
- raw sources only when precision or unresolved evidence requires them.

The desired result is not "load all knowledge." The desired result is:

```text
load enough governed knowledge to act well
and enough evidence to stay honest
```

## Execution

Execution is where context turns into action.

The agentic system should route work through a capability owner:

- a skill for local specialized behavior;
- a sigil for a reusable operation;
- a spell for composed workflow;
- `invoke` for define/design/plan/validate lifecycle work;
- task-session or orchestrated execution for bounded implementation;
- ontology-harness for knowledge governance;
- decision-gate for consequential choices.

Execution should leave evidence:

- selected route;
- route rationale;
- input context;
- output artifact;
- validation;
- terminal outcome;
- gaps;
- telemetry;
- follow-up route.

An execution that leaves no evidence cannot teach the system. It may complete a task, but it does not improve the future loop.

## Observability And Reflection

Observability turns execution into signal.

Reflection turns repeated signals into improvement pressure.

The system should watch for:

- route misses;
- repeated clarification needs;
- output drift;
- validation gaps;
- telemetry gaps;
- stalled handoffs;
- repeated command failures;
- repeated user corrections;
- context overload;
- useful shortcuts;
- capability maintenance opportunities.

Reflection should not directly mutate ontology. It should propose candidates and route them to the right owner.

```text
execution telemetry
  -> signal
  -> reflection
  -> operational lesson candidate
  -> promotion gate
  -> capability update or ontology entry
  -> future context
```

This lets CyberAlchemy improve without giving every observation automatic authority.

## Residue, Drift, And Residuality

Residue is what remains when translation between layers loses meaning.

Examples:

- a business rule without implementation;
- implementation behavior without domain intent;
- a prompt contract that does not match actual output;
- a telemetry signal that does not answer the governance question;
- a memory shortcut that helps once but fails in a different context;
- a context pack that loads too much and hides the relevant evidence.

Drift is divergence over time. Residuality asks what survives when a system is stressed, degraded, translated, or partially broken.

Ontology should capture residue because residue is often the best signal that a new model is needed.

Residue can become:

- bridge gap;
- failure mode;
- residuality finding;
- operational lesson;
- context solution update;
- capability maintenance proposal;
- research question;
- decision gate.

The important move is to stop treating residue as noise. Residue is where the system learns which translations are lossy.

## Exploration Evidence

Exploration projects can feed evidence into the system, but they should not automatically become core architecture.

Their role is to test possibilities:

- better decision policies;
- better research protocols;
- better evaluation loops;
- better operational heuristics;
- better concept generalization.

When exploration evidence is useful, it should enter through the same ladder:

```text
experiment or research output
  -> inventory entry
  -> ontology candidate
  -> premise or confidence review
  -> scoped operational use
```

This keeps the core system stable while allowing experimental learning to matter.

## Recommended Ontology Pack Structure

The ontology pack should live where humans and agents can inspect it.

```text
cyberAlchemy/ontology/
  README.md
  source-ledger.md
  promotion-rules.md
  agentic-system-ontology-map.md
  operational-ontology-map.md
  memory-ontology-map.md
  capability-ontology-map.md
  feedback-ontology-map.md
  bridge-ontology-map.md
  context-solution-catalog.md
  promotion-records/
  entries/
    concept-schema-data-symmetry.md
    method-domainspec-structured-intent.md
    method-saturn-convergence-loop.md
    ontology-branch-operational-ontology.md
    context-solution-invoke-define-design.md
    failure-mode-memory-treated-as-authority.md
    operational-lesson-route-before-work.md
```

Inventory should remain under `.arcanum/inventory/` unless a later decision changes the storage model.

The two layers should refer to each other:

```text
inventory entry cites raw source
ontology entry cites inventory entry and raw source
context pack cites ontology entry and selected evidence
execution cites context pack and emits telemetry
promotion record cites all of the above
```

## First Deep-Dive Backlog

The next useful files to create after this deep dive are:

| File                                                                      | Purpose                                                                                      |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `cyberAlchemy/ontology/promotion-rules.md`                                | Operational rulebook for promotion states, gates, decision records, and non-promotion rules. |
| `cyberAlchemy/ontology/source-ledger.md`                                  | Source cohort ledger for the agentic-system ontology.                                        |
| `cyberAlchemy/ontology/entries/ontology-branch-operational-ontology.md`   | First thick ontology entry for the Operational Ontology branch.                              |
| `cyberAlchemy/ontology/context-solution-catalog.md`                       | Catalog of context solution cards and retrieval fingerprints.                                |
| `.arcanum/inventory/raw/manifests/cyberalchemy-agentic-system-sources.md` | Source manifest for inventory ingestion.                                                     |

## Working Summary

The system should learn, but it should learn with gates.

Inventory lets the system stop rediscovering. Ontology lets the system use knowledge responsibly. Memory lets the system continue. Context Builder lets the system act with the right slice. Execution creates new evidence. Observability and reflection notice what changed. Promotion decides what becomes part of the future operating model.

That is the shape of the CyberAlchemy agentic system:

```text
scattered evidence
  -> reusable inventory
  -> thick ontology
  -> task context
  -> routed execution
  -> observed learning
  -> governed promotion
```
