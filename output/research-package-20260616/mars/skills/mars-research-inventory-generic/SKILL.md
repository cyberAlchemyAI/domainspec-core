---
name: mars-research-inventory-generic
description: "Extract, retrieve, and maintain structured knowledge entries from research sources. Supports domain models, paper abstracts, tool evaluations, framework architectures, role specifications. Eliminates redundant re-fetching across experiment runs."
argument-hint: "<ingest|lookup|validate|backfill> [--entry-type <type>] [--source <source-id>] [--experiment <EX>] [--query <search>]"
agent: mars-research-inventorist
allowed-tools: Read, Write, Bash, Glob, Grep, Fetch, AskQuestions
---

<objective>
Maintain a persistent, structured inventory of knowledge entries extracted from research sources — supporting ANY experiment data requirement, not just domain models.

If the target project defines canonical semantics in `definitions/DEFINITIONS.md`, inventory entries should map extracted terms to IDs in `definitions/DEFINITIONS-INDEX.md`.

**Knowledge entry types supported:**

- `domain-model` — bounded contexts, concepts, relationships (for E1-E10, E15, E20)
- `paper-abstract` — title, authors, contributions, methodology, key findings (for E4, E7, E8, E11-E20)
- `tool-evaluation` — features, performance, cost, integration points (for E17, E15)
- `framework-architecture` — layers, feedback loops, governance model, roles (for E11-E13, E19)
- `role-definition` — agent contract, capabilities, communication protocol, success criteria (for E13, E16, E18)

This skill exists because:

1. **Re-extraction wastes tokens and time.** Both domain models and papers have been extracted once; re-extracting them in later experiments consumes tokens needlessly.
2. **Extraction quality degrades.** Models reconstructed from memory vary between sessions. A validated inventory ensures consistency across experiments.
3. **SOURCE-CATALOG only tracks WHERE sources are, not WHAT they contain.** The catalog records URLs and scores; the inventory stores the actual extracted knowledge.
4. **Cross-experiment reuse.** E6, E9, E11, E15 may all need the same domain models or papers. Without inventory, each extracts independently.
5. **Cross-entry-type consistency.** Papers about domain models, tool docs about agent roles, architecture specs about governance — all live in the same searchable inventory.
   </objective>

<flags>
- `ingest` — Extract a knowledge entry from a source; create or update inventory file.
- `lookup` — Retrieve inventory entries matching criteria (entry type, domain, topic, experiment, meta-type).
- `validate` — Check inventory completeness against SOURCE-CATALOG.
- `backfill` — Reconstruct inventory entries from completed experiment JSONL data.
- `--entry-type <type>` — Filter by type: `domain-model | paper-abstract | tool-evaluation | framework-architecture | role-definition`
- `--source <source-id>` — Target specific source (e.g., `GH-CargoTracker`, `PAPER-AuthorityAgent`).
- `--experiment <EX>` — Scope to sources used by experiment (e.g., E11, E9).
- `--query <search>` — Full-text search on entry contents (e.g., "governance signals", "multi-agent negotiation").
- `--domain <name>` — Filter domain-model entries by domain name.
- `--meta-type <type>` — Filter domain-model entries by meta-type (Entity, Event, etc).
- `--topic <topic>` — Filter paper entries by topic (e.g., "agent systems", "test derivation").
</flags>

<context>
**Input:**
- Optional project semantic contracts (when present):
  - `research/projects/<project>/definitions/DEFINITIONS.md`
  - `research/projects/<project>/definitions/DEFINITIONS-INDEX.md`
- `sources/SOURCE-CATALOG.md` — master catalog of validated sources (for ingest/validate).
- `data/*.jsonl` — raw experiment data (for backfill).
- `experiments/EX-*.md` — experiment protocols (for requirement matching).
- `TAXONOMY.md`, `RELATIONSHIPS.md` — DomainSpec vocabulary (for domain-model classification).
- External sources (GitHub, arXiv, tool docs, etc.) — for ingest operations.

**Output:**

- `inventory/library/{source-id}.md` — one file per inventoried source containing extracted reusable knowledge.
- `inventory/raw/{source-id}/...` — raw retrieved or user-provided provenance artifacts backing the library entry.
- `inventory/INVENTORY-INDEX.md` — master index with lookup tables across all entry types and raw-coverage status.
- `inventory/INVENTORY-SCHEMA.md` — local chain contract and data model definitions.
  </context>

<principles>
1. **Extract once, use many times.** An extraction should be thorough enough that no experiment re-fetches the same source. Structured tables, complete concept inventories, full cross-reference mappings.
2. **Structured over prose.** Inventory entries use tables and typed fields. This enables machine lookup and cross-experiment reuse.
3. **Trace to source.** Every piece of extracted information cites its original location: book chapter, GitHub file path, code line number, paper page, tool version.
4. **Classify using DomainSpec vocabulary (where applicable).** For domain-models: concepts get meta-types (Entity, Event, etc). Edges get relationship types. For papers/frameworks: topics get mapped to DomainSpec claims (C1-C4, CM1-CM4).
5. **Append-only facts, updatable metadata.** Extracted concepts/facts don't change. But metadata (experiment usage, evidence quality, relevance tags) can be updated as we learn.
6. **Backfill from completed experiments.** Experiments validate domain models and extract new knowledge. Backfill captures that validated knowledge into inventory.
7. **Entry-type-specific templates.** Each entry type has its own data model; templates enforce consistency within a type while supporting flexible lookups.
8. **Definition authority discipline.** When canonical definitions files exist, map extracted terms to definition IDs and explicitly flag unmapped semantics.
9. **Provenance chain is mandatory for library-grade status.** A library-grade entry links source catalog -> reference ledger -> inventory index -> per-source library file -> raw content artifact.
10. **User-provided raw files are first-class.** If web retrieval is not possible, request raw files from the user and store them under `inventory/raw/<source-id>/` before calling the entry library-grade.
</principles>

<process>

## Data Model: Knowledge Entry Types

### Entry Type: `domain-model`

**File:** `inventory/library/{source-id}.md`

**Contains:**

- Bounded contexts (name, description, aggregate roots, key events)
- Concept inventory per BC (concept name, meta-type, description, source location)
- Cross-context edges (source BC, target BC, concept, relationship type, pattern, original derivation status)
- Composition pattern checklist (which of P1-P6 patterns are present?)

**Template:**

```markdown
# [Domain Name] — Domain Model Inventory

**Source:** [Source ID from SOURCE-CATALOG]
**Category:** [Category A-F]
**Extracted:** [Date]
**Confidence:** high | moderate | low
**Used in experiments:** [E6, E9, E15, ...]

## Bounded Contexts

| #   | Context | Description | Aggregate Roots | Key Events |
| --- | ------- | ----------- | --------------- | ---------- |

## Concept Inventory

| Concept | Meta-Type | BC  | Description | Source Location |
| ------- | --------- | --- | ----------- | --------------- |

## Cross-Context Edges

| #   | Source BC | Target BC | Concept | Relationship | Pattern | Status |
| --- | --------- | --------- | ------- | ------------ | ------- | ------ |
```

### Entry Type: `paper-abstract`

**File:** `inventory/library/{source-id}.md`

**Contains:**

- Citation info (title, authors, year, venue, DOI)
- Abstract + key contributions
- Relevance to DomainSpec claims (C1-C4 or CM1-CM4)
- Key methodological insights (used in experiments E4, E7, E8, etc.)
- Threat assessment (what are the limitations?)

**Template:**

```markdown
# [Paper Title] — Paper Abstract Inventory

**Citation:** [Authors]. "[Title]." [Venue], [Year]. DOI: [...]
**URL:** [Link to paper or PDF]
**Retrieved:** [Date]
**Confidence:** high | moderate | low
**Relevance:** [C2, CM1, CM3, ...]
**Used in experiments:** [E4, E11, ...]

## Bibliographic Info

| Field      | Value |
| ---------- | ----- |
| Authors    | ...   |
| Title      | ...   |
| Venue      | ...   |
| Year       | ...   |
| DOI / Link | ...   |

## Abstract & Contributions

[Full abstract]

### Key Contributions

- Contribution 1
- Contribution 2

## Relevance to DomainSpec Claims

| Claim           | Relation | Details                                                                         |
| --------------- | -------- | ------------------------------------------------------------------------------- |
| C2 (Derivation) | supports | Paper on automatic test generation validates deterministic derivation principle |

## Threat Assessment

| Threat Type         | Assessment                                         | Implication for DomainSpec                        |
| ------------------- | -------------------------------------------------- | ------------------------------------------------- |
| Internal validity   | Authors use lab subjects, not real developers      | May overestimate derivation benefits              |
| External validity   | Study on Java only                                 | Unclear if findings transfer to Python/TypeScript |
| Construct validity  | "Developer productivity" measured by lines of code | Questionable proxy for software quality           |
| Conclusion validity | Small sample (N=12)                                | Effect size may not be statistically significant  |

## Key Findings

[Bullet points summarizing results]

## Related Work References

[Other papers cited that might be useful]
```

### Entry Type: `tool-evaluation`

**File:** `inventory/library/{source-id}.md`

**Contains:**

- Tool metadata (name, version, GitHub, docs)
- Feature inventory (capabilities, APIs, integrations)
- Performance characteristics (latency, throughput, cost)
- Integration with DomainSpec pipeline (how does this tool fit?)

**Template:**

```markdown
# [Tool Name] — Tool Evaluation Inventory

**Tool:** [Name, version, GitHub/URL]
**Category:** [Test Derivation | Observability | Agent Framework | Knowledge Base | ...]
**Retrieved:** [Date]
**Confidence:** high | moderate | low
**Pipeline role:** [Where does this fit in DomainSpec pipeline?]
**Used in experiments:** [E3, E7, E17, ...]

## Metadata

| Field       | Value |
| ----------- | ----- |
| Name        | ...   |
| Version     | ...   |
| Repository  | ...   |
| Stars       | ...   |
| Last Update | ...   |
| License     | ...   |

## Feature Inventory

| Feature           | Supported | Notes                  |
| ----------------- | --------- | ---------------------- |
| Coverage tracking | ✅        | Line + branch coverage |
| Mutation testing  | ✅        | 15+ mutation operators |
| Cost tracking     | ❌        | Not built-in           |

## Performance Characteristics

| Metric               | Value | Context              |
| -------------------- | ----- | -------------------- |
| Latency per mutation | 50ms  | On 100 KLOC project  |
| Memory footprint     | 500MB | Baseline + mutations |
| Cost per analysis    | $0.05 | If using cloud API   |

## Integration with DomainSpec

| Pipeline Stage       | Integration                                | Notes                                    |
| -------------------- | ------------------------------------------ | ---------------------------------------- |
| Test Derivation (E3) | Mutates derived tests to validate coverage | Stryker plugin validates E2 test quality |
| Observability (E7)   | Exports metrics as OpenTelemetry           | Cost attributed per mutation class       |

## Constraints & Cautions

- Language support: [JS/TS only, no Python]
- Requires: [Node.js ≥18, npm ≥8]
- Learning curve: [Moderate]
```

### Entry Type: `framework-architecture`

**File:** `inventory/library/{source-id}.md`

**Contains:**

- Framework metadata (name, origin, documentation)
- Architecture layers (observer, executor, meta-loop)
- Feedback mechanisms (what signals flow where?)
- Governance model (how are decisions made?)

**Template:**

```markdown
# [Framework Name] — Architecture Inventory

**Framework:** [Name, source paper/GitHub]
**Origin:** [Paper title, GitHub repo, ...]
**Retrieved:** [Date]
**Confidence:** high | moderate | low
**Relevance to meta-meta claims:** [CM1, CM2, CM3, CM4]
**Used in experiments:** [E11, E12, E19, ...]

## Architecture Layers

| Layer | Purpose                        | Signals In         | Signals Out         | Implementation     |
| ----- | ------------------------------ | ------------------ | ------------------- | ------------------ |
| Inner | Execute tasks, collect metrics | Goal → task        | Completion, metrics | [Agent/code]       |
| Outer | Monitor, intervene, adjust     | Metrics            | Task adjustments    | [Feedback loop]    |
| Meta  | Self-tune, specialize roles    | Performance trends | Role specs          | [Self-improvement] |

## Governance Model

[Description of decision-making, who adjusts what, under what conditions]

## Signal Flow Diagram

[ASCII art or reference to paper figure]

## Comparison with DomainSpec

| Aspect        | This Framework | DomainSpec         | Relation                                         |
| ------------- | -------------- | ------------------ | ------------------------------------------------ |
| Layer count   | 5              | 7                  | DomainSpec extends with test + validation layers |
| Feedback type | Empirical      | Formal + empirical | Both use signals; DomainSpec more structured     |
```

### Entry Type: `role-definition`

**File:** `inventory/library/{source-id}.md`

**Contains:**

- Role metadata (name, responsibilities, stakeholders it serves)
- Role contract (interfaces, inputs, outputs, decision authority)
- Communication protocol (how does this role interact with others?)
- Success criteria (how do we measure role effectiveness?)

**Template:**

```markdown
# [Role Name] Agent — Role Definition Inventory

**Role:** [Name: Product Owner, QA, Dev, Stakeholder, etc.]
**Source:** [Paper title, GitHub agent framework, industry spec, ...]
**Retrieved:** [Date]
**Confidence:** high | moderate | low
**Relevance:** [Which DomainSpec phases/agents does this inform?]
**Used in experiments:** [E13, E16, E18, ...]

## Role Metadata

| Field                  | Value |
| ---------------------- | ----- |
| Name                   | ...   |
| Primary Responsibility | ...   |
| Stakeholders Served    | ...   |
| Decision Authority     | ...   |

## Role Contract
```

interface [RoleName]Agent {
inputs: {
domain_spec: DomainSpec,
prior_decisions: Decision[],
peer_proposals: Proposal[]
},
outputs: {
recommendation: Proposal,
rationale: string,
confidence: 0-1
},
sla: {
max_latency_ms: 5000,
cost_budget_tokens: 10000
}
}

```

## Communication Protocol
[How does this role communicate with other roles?]

## Success Criteria
| Metric | Target | Evidence from |
|--------|--------|---|
| Decision alignment | ≥80% agreement with human expert | E18 user study |
| Cost efficiency | ≤5000 tokens per decision | E17 cost audit |
| Recommendation quality | ≥4/5 human rating | E16 adversarial study |

## Implementation Examples
[Links to reference implementations: GitHub agents, LangChain examples, etc.]
```

---

## Operation: `ingest`

Extract a knowledge entry from a source and create/update its inventory file.

### Steps

1. **Identify source:** Read SOURCE-CATALOG.md to get metadata (URL, category, depth assessment).
2. **Determine entry type:** Inspect source to decide type (domain-model if GitHub code; paper-abstract if PDF; tool-evaluation if docs; etc.). If unclear, ask.
3. **Fetch content:**
   - GitHub repos: Fetch README, architecture diagrams, key domain files (entity definitions, events, aggregates, boundaries)
   - Papers: Fetch PDF, read abstract + introduction + evaluation
   - Tool docs: Fetch official documentation, GitHub repo, examples
   - Frameworks: Fetch paper + source code (if open source)
   - Roles: Fetch paper + reference implementations or standards
4. **Extract structured data:** Follow the template for the identified entry type. Fill in tables, not prose.
5. **Resolve definition anchors (if definitions exist):** map extracted terms to IDs in `definitions/DEFINITIONS-INDEX.md`; list gaps for terms not yet canonically defined.
6. **Trace every fact:** Record source location for every extracted piece (GitHub file path, paper page, tool version, etc).
7. **Write inventory file:** `inventory/{source-id}.md` (source ID comes from SOURCE-CATALOG)
8. **Update INVENTORY-INDEX.md:** Add row to the master lookup table.

### Example: Ingest domain-model

```bash
inventorist ingest --source GH-CargoTracker --entry-type domain-model
  → Fetches GitHub repo
  → Identifies 5 bounded contexts (Booking, Routing, Tracking, Handling, Billing)
  → Extracts 13 concepts with meta-types from TAXONOMY.md
  → Identifies 15 cross-context edges with relationship types
  → Writes inventory/cargo-shipping.md
  → Updates INVENTORY-INDEX.md with row: GH-CargoTracker | domain-model | Cargo Shipping | 5 BCs | 13 concepts | E6, E9, E15 |
```

---

## Operation: `lookup`

Retrieve inventory entries matching criteria. Returns structured results for immediate use in experiments.

### Query patterns

```bash
# Find domain models for E11
inventorist lookup --experiment E11 --entry-type domain-model
  → Returns top-3 domain-model entries used or suitable for E11 (E11 needs 3 domains for signal extraction)
  → Format: table with file paths, BCs, concepts, composition patterns

# Find papers on agent governance
inventorist lookup --entry-type paper-abstract --query "agent governance" --claim CM2
  → Returns papers matching topic + relevant to CM2 (Outer Loop Intervention)
  → Format: table with titles, venues, relevance scores, threat assessment

# Find tool evaluations for E17 (cost attribution)
inventorist lookup --entry-type tool-evaluation --query "cost tracking" --experiment E17
  → Returns tools with cost tracking capabilities
  → Format: table with features, latency, cost, pipeline integration

# Find role definitions for adversarial agent design (E16)
inventorist lookup --entry-type role-definition --query "conflict resolution" --claim CM4
  → Returns roles designed for negotiation/disagreement
  → Format: table with role names, decision authority, communication protocols
```

### Output format

Results return as structured tables ready to paste into experiment data or decisions:

```
| Entry ID | Type | Source | Title | Key Finding | Experiment Usage |
|---|---|---|---|---|---|
| GH-eShopOnContainers | domain-model | GitHub | eShop microservices | 6 BCs, complex payment flow | E11 signal extraction |
| PAPER-GovernanceFeedback | paper-abstract | arXiv | "Governance Feedback in Multi-Agent Systems" | Outer-loop intervention improves convergence | E12 intervention effectiveness |
```

---

## Operation: `validate`

Check inventory completeness against SOURCE-CATALOG.

### Steps

1. Read SOURCE-CATALOG.md — get list of validated sources.
2. For each source in catalog:
   - Is there an inventory file? (`inventory/{source-id}.md`)
   - If yes: Is it complete (all fields present)? Is metadata up-to-date (retrieved date, experiment usage)?
   - If no: Flag for backfill or ingest.
3. Output validation report:
   - Total sources: N
   - Inventoried: M (M/N %)
   - Missing: [list]
   - Stale (>3 months): [list]

### Example output

```markdown
## Inventory Validation Report

**Coverage:** 12 / 20 sources inventoried (60%)

**Missing (need ingest):**

- PAPER-AgentNegotiation (Category D)
- TOOL-Pinecone (Category B)
- GH-CrewAI-examples (Category A)

**Stale (need refresh):**

- GH-CargoTracker (last retrieved 2026-02-15, 2 months old)

**Recommendations:**

1. Backfill 8 missing sources from E6/E9 JSONL data (if available)
2. Ingest 3 critical sources before E11 execution
3. Refresh CargoTracker before E15 (cross-domain reuse)
```

---

## Operation: `backfill`

Reconstruct inventory entries from completed experiment JSONL data.

### Use case

Experiments extract knowledge directly from sources. That extracted knowledge is valuable and should be cached in inventory.

Example: E6 ran analysis on 18 domains; each domain's extracted model is in `data/E6-*.jsonl`. Backfill converts JSONL entries into formal inventory entries.

### Steps

1. Read experiment JSONL (`data/EX-*.jsonl`).
2. For each row with extracted knowledge:
   - Identify entry type (usually `domain-model` in data schema)
   - Extract structured fields (BCs, concepts, edges, etc.)
   - Create inventory file using template
   - Trace back to source (usually in JSONL metadata)
3. Output: new inventory files + INVENTORY-INDEX.md update

### Example

```bash
inventorist backfill --experiment E9
  → Reads data/E9-run2-rerun-2026-04-20.jsonl
  → Extracts 6 domain models (Cargo, Collaboration, RideHailing, Ecommerce, Banking, FoodDelivery)
  → Creates inventory/cargo-shipping.md, inventory/collaboration-agilepm.md, etc.
  → Updates INVENTORY-INDEX.md with 6 new rows
  → Output: "Backfilled 6 domain-model entries from E9"
```

---

## Integration with Researcher Scientist Agent

The inventorist bridges SOURCE-CATALOG (validated sources) and EXPERIMENT execution (data needs).

**Workflow:**

```
1. Scientist reads experiment protocol (EX-*.md)
2. Scientist calls sourcer → produces EX-sources.md (validated external sources)
3. Scientist calls inventorist lookup --experiment EX
   → Returns pre-extracted entries (if available)
4. For sources not yet inventoried:
   → Scientist calls inventorist ingest --source <source-id>
5. Scientist executes experiment using:
   - EX-sources.md (external sources to fetch)
   - inventory/{source-id}.md files (pre-extracted knowledge to reuse)
6. After experiment completes:
   → Scientist calls inventorist backfill --experiment EX
   → Inventory captures any new knowledge extracted during experiment
```

This flow ensures:

- ✅ No source is re-fetched across experiments
- ✅ Pre-extracted knowledge is reused (token savings)
- ✅ New discoveries feed inventory (cross-experiment learning)
