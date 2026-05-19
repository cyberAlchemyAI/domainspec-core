---
module: cyberalchemy-agentic-system
slice: 02-ontology-entry-contract
status: candidate
updatedAt: 2026-05-19
docType: slice-concepts
---

# Concepts: Ontology Entry Contract

Work: [README.md](README.md)

## What This Slice Compiles

This slice gathers the ontology material scattered across:

- Arcanum Business Ontology;
- Ontology Vault;
- Ontology Harness;
- the agentic-system ontology entry model;
- the inventory-to-ontology pipeline;
- DomainSpec graph thinking.

The purpose is to make ontology entries self-sufficient enough to guide agents.

## Ontology As Governed Meaning

Ontology is not a list of terms.

Ontology is the governed meaning layer. It explains:

- what something is;
- why it exists;
- where it applies;
- where it does not apply;
- what evidence supports it;
- what confidence it has;
- what other concepts it depends on;
- what invalidates it;
- how an agent should use it.

The difference:

```text
thin ontology:
  "Operational Ontology: see other file"

thick ontology:
  definition, scope, exclusions, examples, agent payload,
  edges, evidence, confidence, promotion state, maintenance trigger
```

Agents need thick entries because execution context must be usable, not only referential.

## Business, System, And Bridge Ontology

Arcanum's Business Ontology defines a branch-aware model with three layers.

| Branch            | Authority                                                                                            | Typical Claims                                                                                              |
| ----------------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Business Ontology | Domain intent, language, rules, policies, premises, value, expected outcomes.                        | What the system should mean, who it serves, what value it provides, and how success is judged.              |
| System Ontology   | Implementation reality: codebase, runtime evidence, infrastructure, architecture, APIs, data, tests. | What exists, how it behaves, where it runs, and how it is measured.                                         |
| Bridge Layer      | Traceability between intent and realization.                                                         | Which implementation realizes which intent, where tests and telemetry prove alignment, where drift appears. |

The bridge is required when a claim says the system realizes an intent.

Business intent without system evidence is aspiration. System behavior without business traceability is orphan implementation. The bridge names the relationship between them.

## Business Ontology Building Blocks

Business Ontology uses knowledge roles to express different authority levels.

| Role             | Meaning                                                                                   |
| ---------------- | ----------------------------------------------------------------------------------------- |
| Axiom            | Load-bearing truth or epistemic foundation. It explains why downstream governance exists. |
| Constitution     | Codified governance rule or process convention. It tells humans and agents how to act.    |
| Premise          | Working bet, hypothesis, or unverified assumption under review.                           |
| Confidence level | Evidence and commitment status attached to a claim.                                       |

Axioms should be rare. Constitutions should be deliberate. Premises should remain visibly uncertain until evidence and commitment justify promotion.

## Via Negativa Promotion Discipline

The Business Ontology source uses a Via Negativa principle: do not formalize rules too early.

In practical terms:

```text
formalize a rule when the absence of the rule has proven costly
```

Cost can appear as:

- drift;
- architectural bug;
- repeated miscommunication;
- route miss;
- repeated agent failure;
- brittle implementation;
- untracked technical debt.

This matters for CyberAlchemy because the system should not turn every elegant idea into an axiom. It should promote rules when the lack of a rule is creating measurable harm or repeated residue.

## Confidence Split

Ontology separates two questions:

| Confidence Axis       | Question                                                              |
| --------------------- | --------------------------------------------------------------------- |
| Evidence confidence   | How well does source evidence or observed reality support this claim? |
| Commitment confidence | How strongly should the project rely on this claim right now?         |

The split prevents a common error: treating "probably true" and "safe to build around" as the same thing.

Examples:

| Evidence | Commitment | Interpretation                                     |
| -------- | ---------- | -------------------------------------------------- |
| High     | Low        | Well-supported but not strategically load-bearing. |
| Low      | Low        | Exploratory candidate.                             |
| Low      | High       | Risky bet requiring explicit gate.                 |
| High     | High       | Strong promotion candidate.                        |

## Hierarchical Policy Resolution

The Business Ontology source describes domain rules as hierarchical.

Policies may live at multiple levels:

- global rule;
- regional rule;
- domain-specific rule;
- local exception;
- leaf-level operational constraint.

The system resolves the applicable rule by traversing the hierarchy and applying specificity.

This is important for agentic operation too. A general route rule may apply broadly, but a local repository, privacy boundary, task type, or user workflow pattern may override it.

Operational Ontology should therefore distinguish:

- global principle;
- repository-local convention;
- route-specific rule;
- user-workflow preference;
- one-session observation.

## Ontology Vault Concepts

Ontology Vault provides the governance surface for:

- ontology maps;
- branch maps;
- session distillation;
- premise review;
- confidence promotion or demotion;
- convention changes;
- delegated research records;
- synthesis findings;
- validation reports;
- drift reports;
- traceability matrices.

It exists when scattered notes, sessions, discoveries, premises, and conventions need explicit roles, maturity states, confidence, edge rules, and promotion decisions.

## Branch Edges

Existing branch-aware edge types include:

| Edge             | Meaning                                                                          |
| ---------------- | -------------------------------------------------------------------------------- |
| `realized_by`    | A business concept, rule, or behavior is implemented by a system artifact.       |
| `depends_on`     | A business behavior depends on a system capability.                              |
| `constrained_by` | A business rule or outcome is limited by a technical constraint.                 |
| `observed_by`    | A business outcome or behavior is measured by a metric, log, event, or trace.    |
| `tested_by`      | A claim, rule, or behavior is verified by a test.                                |
| `drifts_from`    | Observed behavior diverges from intended behavior.                               |
| `traced_to`      | A system artifact links back to a premise, decision, discovery, rule, or source. |

CyberAlchemy can extend these with operational edges:

| Edge             | Meaning                                                                                    |
| ---------------- | ------------------------------------------------------------------------------------------ |
| `learned_from`   | A lesson came from a run, source, session, or telemetry pattern.                           |
| `applies_to`     | A lesson or context solution applies to an execution context or capability.                |
| `avoids`         | A lesson reduces a failure mode.                                                           |
| `improves`       | A lesson improves a route, capability, or workflow.                                        |
| `generalizes_to` | A local lesson may become a broader meta-model.                                            |
| `promotes_to`    | A candidate moves to a premise, promoted entry, constitution, axiom, or capability update. |

## Thick Entry Shape

Every CyberAlchemy ontology entry should have these parts:

| Section       | Purpose                                                                               |
| ------------- | ------------------------------------------------------------------------------------- |
| Identity      | Stable id, title, type, branch, owner, dates, status.                                 |
| Content       | Definition, purpose, scope, exclusions, examples, non-examples.                       |
| Context       | Use-when rules, do-not-use rules, applicability, invalidation conditions.             |
| Agent Payload | Compact guidance an agent can use during execution.                                   |
| Edges         | Typed relationships to entries, inventory, sources, capabilities, signals, decisions. |
| Evidence      | Inventory and source references.                                                      |
| Confidence    | Evidence confidence, commitment confidence, scope, expiry.                            |
| Promotion     | Current state, next gate, required evidence, contradiction path.                      |
| Maintenance   | Review trigger, owner route, stale condition, open questions.                         |

## Entry Types

The agentic-system ontology needs several entry classes.

| Entry Type           | Must Carry                                                                                       |
| -------------------- | ------------------------------------------------------------------------------------------------ |
| `OntologyBranch`     | Authority, allowed claim types, excluded claim types, edge rules, promotion route.               |
| `AuthorityLadder`    | Ordered authority states, promotion owners, allowed transitions, skip rules, contradiction path. |
| `OperationalLesson`  | Lesson, source context, applicability, failure avoided, route impact, expiry.                    |
| `ContextSolution`    | Trigger fingerprint, compact payload, recommended route, evidence, pitfalls, invalidation.       |
| `MemoryPattern`      | Memory behavior, ergonomics value, privacy class, promotion boundary.                            |
| `CapabilityPattern`  | Capability owner, input/output contract, composition rule, telemetry expectation.                |
| `FailureMode`        | Stressor, degradation path, detection signal, recovery route.                                    |
| `MethodPrimitive`    | Rule, phase, operational use, anti-pattern, route owner, source reference.                       |
| `MetaModelCandidate` | Generalization, source examples, scope, recomposition proof, contradiction trigger.              |

## Ontology As Superset Of Inventory

Ontology is a semantic and operational superset of inventory.

It can classify inventory entries, relate them to higher concepts, give them scope, and turn selected entries into usable agent guidance.

It is not a storage superset:

- it should not copy every source summary;
- it should not absorb weak claims as authority;
- it should not replace inventory tags and logs;
- it should not treat generated inventory as raw source authority.

The relationship is:

```text
inventory prepares evidence
ontology owns usable meaning
context-builder extracts the task slice
```

## First Entry Candidates

The first ontology entries should include:

| Entry                                      | Branch                             | Why                                                                                             |
| ------------------------------------------ | ---------------------------------- | ----------------------------------------------------------------------------------------------- |
| `method-saturn-convergence-loop`           | philosophy or knowledge-governance | Governs the intent/reality feedback loop.                                                       |
| `method-domainspec-structured-intent`      | philosophy or capability           | Explains how intent becomes traceable obligations.                                              |
| `knowledge-governance-authority-ladder`    | knowledge-governance               | Owns the ladder that prevents raw evidence, memory, or telemetry from skipping promotion gates. |
| `ontology-branch-operational-ontology`     | knowledge-governance               | Defines the branch for agent operation knowledge.                                               |
| `failure-mode-memory-treated-as-authority` | feedback or memory                 | Protects against accidental canon.                                                              |
| `context-solution-invoke-define-design`    | operational or memory              | Provides the first reusable context shortcut.                                                   |

## Agent-Usable Rule

An ontology entry can guide an agent only when it can answer:

```text
what is this?
when should I use it?
what should I avoid?
what evidence supports it?
how confident is the system?
what changes if this is wrong?
```
