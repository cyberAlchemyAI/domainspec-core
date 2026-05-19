---
module: cyberalchemy-agentic-system
slice: 01-inventory-foundation
status: candidate
updatedAt: 2026-05-19
docType: slice-concepts
---

# Concepts: Inventory Foundation

Work: [README.md](README.md)

## What This Slice Compiles

This slice gathers the repository knowledge about inventory, source manifests, reusable evidence, lookup, and the boundary between raw files and ontology.

The key source idea is simple:

```text
raw sources stay immutable
inventory compiles reusable evidence
ontology governs meaning
context-builder selects the task slice
```

## Inventory As Compiled Evidence

Arcanum defines Inventory as a repository-local compiled knowledge layer.

It is inspired by a wiki pattern:

- raw sources remain read-only;
- generated markdown pages evolve;
- summaries, entity pages, concept pages, architecture notes, pattern entries, contradictions, tags, indexes, and logs accumulate over time;
- later sigils query inventory before reading the whole repository.

Inventory solves a compounding problem. If every question requires rereading raw files, knowledge does not become easier to use. Inventory lets a repository remember what has already been extracted.

## The Three Inventory Layers

Inventory uses three layers:

| Layer          | Responsibility                                                                |
| -------------- | ----------------------------------------------------------------------------- |
| Raw sources    | User-curated evidence that the system reads but does not mutate.              |
| Inventory wiki | Generated markdown pages that summarize, connect, and index source knowledge. |
| Schema         | Local conventions for ingest, tagging, querying, linting, and maintenance.    |

The default package shape is:

```text
.arcanum/inventory/
  README.md
  schema.md
  index.md
  log.md
  tags.md
  raw/
  wiki/
  entries/
  queries/
  lint/
```

For the CyberAlchemy agentic system, the inventory source manifest should live under:

```text
.arcanum/inventory/raw/manifests/cyberalchemy-agentic-system-sources.md
```

## Inventory Operations

Inventory supports these operations:

| Operation  | Meaning                                                                                |
| ---------- | -------------------------------------------------------------------------------------- |
| `install`  | Create or adapt the local inventory package.                                           |
| `ingest`   | Read raw sources, create summaries, update entries, flag contradictions, append log.   |
| `lookup`   | Return relevant inventory pages and selectors for another capability.                  |
| `query`    | Answer against inventory and optionally file a synthesis page.                         |
| `lint`     | Find contradictions, stale claims, missing backlinks, untagged pages, and source gaps. |
| `validate` | Check package structure, index coverage, log parseability, tags, and evidence links.   |
| `backfill` | Build inventory from existing docs, decisions, context packs, and artifacts.           |
| `sync`     | Update conventions after schema changes.                                               |

## Source Cohorts For This System

The CyberAlchemy corpus should be ingested by cohorts, not as one giant sweep.

| Cohort                        | Content                                                                                | Why It Matters                                        |
| ----------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Agentic baseline              | Definition, glossary, architecture, knowledge map, implementation layering.            | Current candidate model and vocabulary.               |
| CyberAlchemy philosophy       | Main product surface, Saturn, Necronomicon product surface.                            | Governing story and convergence language.             |
| Arcanum method                | CyberAlchemy Method, Arcanum README, sigil and spell registries.                       | Capability model and lifecycle ownership.             |
| Knowledge governance          | Business Ontology, Ontology Vault, Ontology Harness, Knowledge Substrate Flow.         | Branches, confidence, authority ladder, promotion.    |
| Memory and repository harness | Necronomicon README and design docs.                                                   | Active interaction, side notes, routing, checkpoints. |
| Operation and execution       | Agent Execution Orchestrator, Observed Invocation Loop, Workflow Reflect, Tuning Loop. | Operational lessons, telemetry, maintenance.          |
| Residue and resilience        | Residuality Spec and Drift-Convergence.                                                | Stressors, residue, drift, convergence.               |

Exploration projects can be inventoried later as evidence sources, but they should not become core architecture by default.

The ontology pack now starts this work through compiled source digests under [source-digests](../../../ontology/source-digests/README.md). These digests are the CyberAlchemy-side inventory of important cross-repository sources: they arrange the content inside the ontology context while preserving links back to the original Arcanum and DomainSpec files.

## Entry Types

This corpus needs inventory entry types beyond generic source summaries.

| Entry Type             | Purpose                                                                       |
| ---------------------- | ----------------------------------------------------------------------------- |
| `philosophy-principle` | Captures an operating belief or epistemic principle.                          |
| `method-primitive`     | Captures reusable CyberAlchemy Method primitives.                             |
| `ontology-branch`      | Captures a candidate branch, its authority, and evidence rule.                |
| `operational-lesson`   | Captures lessons from sigils, spells, agents, prompts, or route optimization. |
| `context-solution`     | Captures task-shaped retrieval shortcuts.                                     |
| `memory-pattern`       | Captures repeated memory, route, side-note, or workflow behavior.             |
| `failure-mode`         | Captures operational risks and anti-patterns.                                 |
| `decision-policy`      | Captures route or agent decision policy.                                      |
| `residuality-finding`  | Captures what survives or degrades under stress.                              |

Default types still matter:

- `source`;
- `concept`;
- `decision`;
- `capability`;
- `workflow`;
- `observability-signal`;
- `question`;
- `contradiction`;
- `synthesis`.

## Inventory And Necronomicon

Necronomicon should expose inventory through three motions:

| Motion      | User Meaning                                  | System Route                                                                 |
| ----------- | --------------------------------------------- | ---------------------------------------------------------------------------- |
| Inventorize | "Keep this so we do not rediscover it later." | checkpoint -> inventory ingest or discovery-to-inventory                     |
| Retrieve    | "What do we already know about this?"         | inventory lookup before broad search                                         |
| Reconcile   | "This conflicts with what we knew."           | inventory lint or contradiction entry, then ontology review if consequential |

The retrieval output should not be a wiki dump. It should be task-shaped:

```text
query
  -> matching inventory entries
  -> source selectors
  -> confidence and gaps
  -> obligation fit
  -> recommended next route
```

## Inventory To Ontology

Inventory can hold more uncertainty than ontology.

Inventory entry:

```text
what source said this?
what claim was extracted?
what type of claim is it?
what supports it?
what contradicts it?
where should a future agent look?
```

Ontology entry:

```text
what does this mean?
where does it apply?
how should an agent use it?
what evidence supports it?
what can invalidate it?
what route or decision does it affect?
```

The correct movement is:

```text
raw source
  -> source summary
  -> typed inventory entry
  -> thick ontology candidate
  -> premise or confidence review
  -> promoted entry or explicit rejection
```

## First Inventory Targets

The first entries should prove the source-to-inventory path:

| Entry                                      | Why                                                        |
| ------------------------------------------ | ---------------------------------------------------------- |
| `concept-schema-data-symmetry`             | Governing lens for the whole system.                       |
| `method-saturn-convergence-loop`           | Top-level convergence method.                              |
| `method-domainspec-structured-intent`      | Specification discipline behind the convergence loop.      |
| `ontology-branch-operational-ontology`     | New branch the user wants to create.                       |
| `context-solution-invoke-define-design`    | First reusable context shortcut.                           |
| `failure-mode-memory-treated-as-authority` | Boundary rule protecting the system from accidental canon. |

## Quality Rule

Inventory is not a dumping ground.

An inventory entry should have:

- summary;
- key claims;
- source references;
- related entries;
- tags;
- contradictions or tensions;
- review trigger;
- status.

If a future agent cannot use it to retrieve evidence faster than rereading raw sources, it is not yet good inventory.
