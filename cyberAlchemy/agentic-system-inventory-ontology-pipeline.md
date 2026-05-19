---
module: cyberalchemy-agentic-system
version: current
status: candidate
updatedAt: 2026-05-19
docType: inventory-ontology-pipeline
---

# Agentic System Inventory To Ontology Pipeline

Navigation: [agentic-system-navigation.md](agentic-system-navigation.md)
Definition: [agentic-system-definition.md](agentic-system-definition.md)
Glossary: [agentic-system-glossary.md](agentic-system-glossary.md)
Ontology entry model: [agentic-system-ontology-entry-model.md](agentic-system-ontology-entry-model.md)

## Purpose

Define how CyberAlchemy can use Arcanum's existing `inventory`, `ontology-harness`, `ontology-vault`, and `context-builder` capabilities to collect scattered philosophical, content, operational, and research knowledge into a reusable agentic-system ontology.

The core move is:

```text
raw repository sources
  -> inventory source summaries, extracted claims, indexes, tags, contradictions, and provenance
  -> thick ontology entries with content, context, edges, confidence, and agent payloads
  -> ontology-harness and ontology-vault branch maps, confidence reviews, and promotion gates
  -> context-builder task packs selected from ontology entries and evidence selectors
  -> future agent execution context
```

Inventory is the ingestion and evidence substrate. Ontology is the governed, agent-usable knowledge layer. Memory and telemetry feed candidates into both, but they do not become authority by themselves.

## Corrected Layering

Ontology should be a semantic and operational superset of inventory, but not a storage dump of inventory.

| Layer           | Role                                                                                                                                       |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Raw sources     | Preserve original evidence and authored context.                                                                                           |
| Inventory       | Captures source summaries, extracted claims, tags, contradictions, lookup indexes, and provenance.                                         |
| Ontology        | Owns thick knowledge entries: meaning, context, applicability, agent payloads, edges, confidence, promotion state, and retrieval guidance. |
| Context Builder | Extracts the smallest task-specific slice from ontology plus the evidence selectors needed for proof.                                      |

Use [agentic-system-ontology-entry-model.md](agentic-system-ontology-entry-model.md) as the entry contract. Do not create pointer-only ontology nodes.

## Arcanum Capabilities To Use

| Capability               | Role In This Work                                                                                                                                 | Existing Contract                                                            |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `inventory`              | Install or adapt `.arcanum/inventory/`, ingest sources, create source summaries, typed entries, tags, indexes, contradictions, and lookup output. | [Inventory README](../arcanum/arcana/inventory/README.md)                    |
| `discovery-to-inventory` | Convert early discovery, glossary, and scope material into durable inventory entries.                                                             | [Discovery To Inventory](../arcanum/spells/discovery-to-inventory/README.md) |
| `ontology-harness`       | Compose inventory, ontology-vault, and context-builder into ontology maps and validation output.                                                  | [Ontology Harness](../arcanum/spells/ontology-harness/README.md)             |
| `ontology-vault`         | Govern ontology roles, branches, edges, confidence, premises, promotion, drift, and conventions.                                                  | [Ontology Vault](../arcanum/arcana/ontology-vault/README.md)                 |
| `context-builder`        | Prove future agents can retrieve only the context needed for a task obligation.                                                                   | [Context Builder](../arcanum/transmutations/context-builder/README.md)       |
| `definitions-governance` | Stabilize terms that become load-bearing across artifacts.                                                                                        | [Sigil Registry](../arcanum/registry/SIGILS.md)                              |
| `decision-gate`          | Resolve promotion, privacy, branch, or convention choices that change behavior.                                                                   | [Sigil Registry](../arcanum/registry/SIGILS.md)                              |

## Storage Model

Use Arcanum's default package for inventory and a CyberAlchemy-visible ontology pack for the agentic system.

```text
.arcanum/inventory/
  README.md
  schema.md
  index.md
  log.md
  tags.md
  raw/
    manifests/
      cyberalchemy-agentic-system-sources.md
  wiki/
    cyberalchemy-agentic-system/
  entries/
    cyberalchemy-agentic-system/
  queries/
  lint/

cyberAlchemy/ontology/
  README.md
  agentic-system-ontology-map.md
  operational-ontology-map.md
  memory-ontology-map.md
  capability-ontology-map.md
  feedback-ontology-map.md
  entries/
    operational-ontology.md
    context-solution-invoke-define-design.md
    method-primitive-route-before-work.md
    failure-mode-memory-treated-as-authority.md
  context-payloads/
  source-ledger.md
  promotion-rules.md
  context-solution-catalog.md
```

Rationale:

- `.arcanum/inventory/` is the repository-local compiled knowledge system used by Arcanum sigils.
- `cyberAlchemy/ontology/` is the human-visible ontology pack for thick CyberAlchemy agentic-system knowledge entries.
- Raw sources are not copied or rewritten; the inventory records source summaries and references.
- Ontology entries contain usable content and cite inventory/source evidence.

## Source Corpus

Start with source cohorts instead of one huge ingest. This keeps contradictions and gaps easier to see.

| Cohort                                          | Sources                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Primary Knowledge Extracted                                                                            | Inventory Entry Types                                                                  |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| C1: Agentic baseline                            | [agentic-system-definition.md](agentic-system-definition.md), [agentic-system-glossary.md](agentic-system-glossary.md), [agentic-system-architecture.md](agentic-system-architecture.md), [agentic-system-knowledge-map.md](agentic-system-knowledge-map.md), [agentic-system-implementation-layering.md](agentic-system-implementation-layering.md)                                                                                                                                                | Current candidate model, terms, gaps, layers, design decisions.                                        | `source`, `concept`, `decision`, `workflow`, `question`, `synthesis`                   |
| C2: CyberAlchemy philosophy and product surface | [main.html](main.html), [saturn-research-presentation.md](saturn-research-presentation.md), [necronomicon.html](necronomicon.html), [mars.html](mars.html), [mogt.html](mogt.html)                                                                                                                                                                                                                                                                                                                  | Cybernetics^2, drift/convergence, research governance, decision policy, knowledge substrate narrative. | `philosophy-principle`, `concept`, `workflow`, `research-claim`                        |
| C3: Arcanum method and capability model         | [CYBERALCHEMY-METHOD.md](../arcanum/framework/CYBERALCHEMY-METHOD.md), [Arcanum README](../arcanum/README.md), [Sigil Registry](../arcanum/registry/SIGILS.md), [Spell Registry](../arcanum/registry/SPELLS.md)                                                                                                                                                                                                                                                                                     | Method loop, primitives, lifecycle ownership, sigil/spell tiers, selected capability surface.          | `method-primitive`, `capability`, `workflow`, `decision`                               |
| C4: Knowledge governance                        | [BUSINESS-ONTOLOGY.md](../arcanum/BUSINESS-ONTOLOGY.md), [Ontology Vault](../arcanum/arcana/ontology-vault/README.md), [Ontology Harness](../arcanum/spells/ontology-harness/README.md), [KNOWLEDGE-SUBSTRATE-FLOW.md](../arcanum/spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md)                                                                                                                                                                                                      | Branches, confidence, authority ladder, promotion gates, ontology edge rules.                          | `ontology-branch`, `concept`, `dependency-rule`, `decision`                            |
| C5: Memory and repository harness               | [Necronomicon README](../arcanum/spells/necronomicon/README.md), [Necronomicon Design](../arcanum/spells/necronomicon/development/DESIGN.md), [USAGE-VISION.md](../arcanum/spells/necronomicon/development/USAGE-VISION.md)                                                                                                                                                                                                                                                                         | Session memory, active interaction, side notes, routes, continuation behavior, ergonomics.             | `memory-pattern`, `workflow`, `context-solution`, `question`                           |
| C6: Operation and execution                     | [Agent Execution Orchestrator SPEC](../implementation/domainspec/docs/features/agent-execution-orchestrator/SPEC.md), [capability-sequence-lessons.md](../implementation/domainspec/docs/features/agent-execution-orchestrator/work-pack/context/capability-sequence-lessons.md), [TUNING-LOOP.md](../implementation/domainspec/TUNING-LOOP.md), [Observed Invocation Loop](../arcanum/spells/observed-invocation-loop/README.md), [Workflow Reflect](../arcanum/arcana/workflow-reflect/README.md) | Stage contracts, telemetry envelopes, operational lessons, tuning thresholds, reflection.              | `operational-lesson`, `capability`, `workflow`, `observability-signal`, `failure-mode` |
| C7: Research and decision policy                | [MARS README](../research/projects/mars/README.md), [MARS Pipeline](../research/projects/mars/definitions/MARS-PIPELINE.md), [MOGT README](../research/projects/mogt-agentic-conversation/README.md), [MOGT Methodology](../research/projects/mogt-agentic-conversation/foundations/METHODOLOGY-AND-THEORY.md)                                                                                                                                                                                      | Research lifecycle, evidence status, objective vectors, policy regimes, overhead constraints.          | `research-claim`, `workflow`, `decision-policy`, `observability-signal`                |
| C8: Residue and resilience                      | [Residuality Spec](../arcanum/arcana/residuality-spec/README.md), [DRIFT-CONVERGENCE.md](../implementation/domainspec/DRIFT-CONVERGENCE.md)                                                                                                                                                                                                                                                                                                                                                         | Stressors, residue, degradation, attractors, drift, convergence.                                       | `residuality-finding`, `failure-mode`, `concept`, `workflow`                           |

## Custom Inventory Entry Types

Add these to `.arcanum/inventory/schema.md` for this project namespace.

| Entry Type             | Purpose                                                                             | Required Fields                                                                                  |
| ---------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `philosophy-principle` | Captures a CyberAlchemy operating belief or epistemic principle.                    | statement, source, implication, contradiction trigger                                            |
| `method-primitive`     | Captures reusable CyberAlchemy Method primitives.                                   | primitive, phase, rule, source, operational use                                                  |
| `ontology-branch`      | Captures a branch in the agentic-system ontology.                                   | branch name, authority, allowed claims, evidence rule                                            |
| `operational-lesson`   | Captures lessons from agent, sigil, spell, route, prompt, or workflow optimization. | lesson, source run or source doc, applies_to, avoids, evidence confidence, commitment confidence |
| `context-solution`     | Captures a reusable context/retrieval card for a recognized execution context.      | trigger fingerprint, recommended context, recommended route, evidence, pitfalls, expiry          |
| `memory-pattern`       | Captures a repeated memory, side-note, route, or user workflow pattern.             | pattern, scope, privacy class, promotion rule, source                                            |
| `failure-mode`         | Captures repeated operational risk or anti-pattern.                                 | failure, stressor, affected route, detection signal, recovery route                              |
| `decision-policy`      | Captures a routing or agent-decision policy.                                        | objectives, policy regime, tradeoffs, evidence, overhead limit                                   |
| `residuality-finding`  | Captures what survives or degrades when translation or operation fails.             | stressor, residue, degradation, attractor, recovery                                              |

Keep default inventory types too: `source`, `concept`, `decision`, `capability`, `workflow`, `observability-signal`, `question`, `contradiction`, and `synthesis`.

## Ontology Branches

Use ontology-harness to map inventory entries into thick ontology entries in these candidate branches.

| Branch                        | Authority                                                                                                | Inputs From Inventory                                                      | Output Map                                              |
| ----------------------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------- |
| Philosophy Ontology           | CyberAlchemy principles, epistemic commitments, design taste, and method axioms.                         | `philosophy-principle`, `method-primitive`, `concept`                      | `cyberAlchemy/ontology/agentic-system-ontology-map.md`  |
| Knowledge Governance Ontology | Knowledge roles, confidence, promotion, branches, source authority, and contradiction rules.             | `ontology-branch`, `concept`, `decision`, `dependency-rule`                | `cyberAlchemy/ontology/agentic-system-ontology-map.md`  |
| Operational Ontology          | Agent operation knowledge: lessons, route patterns, failure modes, capability updates, prompt contracts. | `operational-lesson`, `capability`, `failure-mode`, `observability-signal` | `cyberAlchemy/ontology/operational-ontology-map.md`     |
| Memory Ontology               | Execution-context memory, side notes, active interaction, shortcuts, user workflow model.                | `memory-pattern`, `context-solution`, `workflow`, `question`               | `cyberAlchemy/ontology/memory-ontology-map.md`          |
| Capability Ontology           | Sigils, spells, skills, agents, routes, lifecycle owners, and composition rules.                         | `capability`, `workflow`, `method-primitive`                               | `cyberAlchemy/ontology/capability-ontology-map.md`      |
| Feedback Ontology             | Signals, telemetry, reflection, tuning thresholds, drift, residuality, validation evidence.              | `observability-signal`, `residuality-finding`, `failure-mode`              | `cyberAlchemy/ontology/feedback-ontology-map.md`        |
| Research Ontology             | MARS/MOGT claims, hypotheses, protocols, evidence, decision-policy experiments.                          | `research-claim`, `decision-policy`, `workflow`                            | future `cyberAlchemy/ontology/research-ontology-map.md` |
| Bridge Ontology               | Traceability across philosophy, operation, memory, capability, feedback, and system artifacts.           | all entry types with explicit edges                                        | future bridge map                                       |

## Edge Vocabulary

Use existing ontology-vault edge rules where possible and add operational edges only where needed.

| Edge             | Source Types                               | Target Types                                     | Validation Rule                                         |
| ---------------- | ------------------------------------------ | ------------------------------------------------ | ------------------------------------------------------- |
| `traced_to`      | any ontology node                          | source or inventory entry                        | Must cite repository path or inventory page.            |
| `learned_from`   | operational lesson, context solution       | source, telemetry, session, decision             | Must identify the run, source doc, or session evidence. |
| `applies_to`     | lesson, method primitive, context solution | execution context, capability, workflow          | Must state scope of validity.                           |
| `improves`       | lesson, proposal, context solution         | capability, route, workflow                      | Must name the improvement mechanism.                    |
| `avoids`         | lesson, context solution, policy           | failure mode, residuality finding                | Must name the failure mode reduced.                     |
| `observed_by`    | claim, lesson, route policy                | signal, metric, telemetry                        | Must cite signal source or record gap.                  |
| `tested_by`      | claim, route, capability                   | test, validation, experiment                     | Must cite test/evidence or remain candidate.            |
| `drifts_from`    | observed behavior, failure mode            | expected contract, principle, route              | Must preserve both expectation and observation.         |
| `generalizes_to` | local lesson                               | meta-model candidate                             | Must cite at least one cross-context reuse argument.    |
| `constrained_by` | route, memory pattern, context solution    | privacy, safety, cost, latency, evidence policy  | Must state constraint owner.                            |
| `promotes_to`    | candidate                                  | premise, reviewed node, capability update, axiom | Requires ontology-vault or decision-gate record.        |

## Pipeline Phases

### Phase 0: Source Manifest

Create `.arcanum/inventory/raw/manifests/cyberalchemy-agentic-system-sources.md`.

The manifest should list cohorts, source paths, source role, expected entry types, and ingest priority. It is a pointer list, not a copy of the sources.

Gate: every source must have a role and branch hypothesis before ingest.

### Phase 1: Inventory Install Or Adapt

Install `.arcanum/inventory/` using the existing `inventory` package model.

Local conventions:

- Markdown links, not wiki links.
- Frontmatter allowed for generated pages.
- Raw sources immutable.
- Generated entries cite source paths and headings.
- Tags use `area/<area>`, `branch/<branch>`, `source/<system>`, and `status/<status>`.

Gate: `index.md`, `schema.md`, `tags.md`, and `log.md` exist before ingest.

### Phase 2: Source Summary Ingest

For each source in a cohort:

1. Create a source summary page.
2. Extract reusable claims.
3. Extract concepts, decisions, workflows, capabilities, questions, contradictions, and operational lessons.
4. Update index, tags, and log.

Gate: every material claim points to a source path or is marked `inference`, `synthesis`, or `open-question`.

### Phase 3: Typed Inventory Pages

Create typed entries under:

```text
.arcanum/inventory/entries/cyberalchemy-agentic-system/
```

Suggested first entries:

- `concept-schema-layer.md`
- `concept-evidence-layer.md`
- `concept-translation-residue.md`
- `knowledge-governance-authority-ladder.md`
- `ontology-branch-operational-ontology.md`
- `context-solution-invoke-define-design.md`
- `operational-lesson-define-before-runner.md`
- `memory-pattern-active-interaction.md`
- `method-primitive-route-before-work.md`
- `feedback-loop-observed-invocation-loop.md`
- `failure-mode-memory-treated-as-authority.md`

Gate: each entry has summary, key claims, sources, related pages, contradictions/tensions, and review trigger.

### Phase 4: Thick Ontology Entry Creation

Run ontology-harness against the inventory namespace and source cohorts, then create ontology entries that carry usable content, context, agent payloads, edges, evidence, confidence, and promotion state.

Outputs should live in:

```text
cyberAlchemy/ontology/
```

Required maps:

- `agentic-system-ontology-map.md`
- `operational-ontology-map.md`
- `memory-ontology-map.md`
- `capability-ontology-map.md`
- `feedback-ontology-map.md`
- `source-ledger.md`
- `promotion-rules.md`
- `context-solution-catalog.md`

Required thick entries for the first slice:

- `entries/operational-ontology.md`
- `entries/knowledge-governance-authority-ladder.md`
- `entries/context-solution-invoke-define-design.md`
- `entries/method-primitive-route-before-work.md`
- `entries/failure-mode-memory-treated-as-authority.md`

Gate: entries must distinguish inventory facts, ontology candidates, reviewed premises, decisions, contradictions, and open questions. Pointer-only entries fail the gate.

### Phase 5: Context Builder Proof

Use `context-builder` to prove the inventory and ontology can support future work without whole-repo rereading.

Sample tasks:

- "Prepare context to design Operational Ontology schema."
- "Prepare context to decide user workflow memory privacy policy."
- "Prepare context to plan Context Solution Card retrieval."
- "Prepare context to improve an Arcanum sigil from repeated telemetry."

Gate: context pack selects only obligation-linked ontology content and the evidence selectors needed to prove it. It records excluded noise.

### Phase 6: Maintenance Loop

Use observability and workflow reflection to keep the inventory current.

Trigger inventory updates when:

- a new agentic-system artifact is added,
- a repeated route miss appears,
- a term becomes load-bearing,
- a contradiction appears between design and operation,
- telemetry supports or contradicts an operational lesson,
- a context solution expires.

Gate: generated pages update index and log; contradictions are recorded, not overwritten.

## Command Routes

Use the repository command surface when running the actual capabilities.

```bash
arcanum/tools/arcanum inventory install --path . --root .arcanum/inventory
arcanum/tools/arcanum inventory backfill --path . --root .arcanum/inventory --source cyberAlchemy
arcanum/tools/arcanum inventory ingest --path . --root .arcanum/inventory --source cyberAlchemy/agentic-system-definition.md
arcanum/tools/arcanum ontology-harness --path . --source .arcanum/inventory/entries/cyberalchemy-agentic-system
arcanum/tools/arcanum context-builder --path . --query "design Operational Ontology schema"
```

Use `--exec` only when the local Codex command surface should actually run the managed command and append Observed Invocation Loop telemetry.

## Inventory To Ontology Promotion Rule

Do not promote directly from raw source to ontology authority.

Use this sequence:

```text
raw source
  -> source summary and typed inventory entry
  -> thick ontology candidate
  -> premise review or confidence review
  -> promoted ontology node or explicit rejection
```

This keeps the epistemic ladder clean:

- Raw sources remain source authority.
- Inventory is reusable evidence map and synthesis substrate.
- Ontology is governed meaning and agent-usable context.
- Memory is continuity and candidate evidence.
- Telemetry is observed behavior.
- Promotion requires review.

## First Working Slice

The smallest useful implementation is:

1. Install `.arcanum/inventory/`.
2. Add source manifest for the eight cohorts above.
3. Backfill only C1 and C3 first.
4. Create typed entries:
   - `concept-translation-residue`
   - `knowledge-governance-authority-ladder`
   - `ontology-branch-operational-ontology`
   - `method-primitive-route-before-work`
   - `context-solution-invoke-define-design`
   - `failure-mode-memory-treated-as-authority`
5. Create matching thick ontology entries for the entries that need to guide agents.
6. Run ontology-harness to produce the first `agentic-system-ontology-map.md`.
7. Run context-builder on one sample task.

After that slice, we know whether the inventory and ontology path works before ingesting the whole repository.

## Open Questions

| Question                                                                                            | Why It Matters                                                              | Suggested Route                             |
| --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------- |
| Should `cyberAlchemy/ontology/` be canonical or should `.arcanum/ontology/` own all generated maps? | Affects visibility, ownership, and future runtime assumptions.              | `decision-gate`                             |
| What privacy class applies to User Workflow Model entries?                                          | Prevents personal workflow memory from becoming accidental public ontology. | `decision-gate`                             |
| Should philosophical principles be a first-class branch or tagged business/method concepts?         | Affects ontology branch complexity.                                         | `ontology-harness`                          |
| What evidence threshold promotes an operational lesson into a route policy?                         | Prevents one-off wins from becoming brittle automation.                     | `ontology-vault` premise review             |
| How often should inventory lint run?                                                                | Keeps entries from becoming stale.                                          | `workflow-reflect` or scheduled maintenance |
