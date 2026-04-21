---
name: domainspec-research-inventory
description: "Inventorize, retrieve, and maintain structured domain model extractions from research sources. Eliminates redundant re-fetching and reconstruction across experiment runs."
argument-hint: "<ingest|lookup|validate|backfill> [--source <source-id>] [--experiment <EX>] [--domain <domain-name>]"
agent: domainspec-research-inventorist
allowed-tools: Read, Write, Bash, Glob, Grep, Fetch, AskQuestions
---

<objective>
Maintain a persistent, structured inventory of **domain model details** extracted from research sources — bounded contexts, concepts, meta-types, cross-context edges, and composition patterns.

This skill exists because:
1. **Re-fetching wastes tokens and time.** Every experiment run re-discovers the same domain models from GitHub READMEs (which return mostly navigation content) and book references. The inventory caches extracted knowledge.
2. **Reconstruction quality degrades across sessions.** Domain models reconstructed from memory vary between sessions. A validated inventory ensures consistency.
3. **SOURCE-CATALOG tracks *where*, not *what*.** The catalog knows URLs and scores but not the actual bounded contexts, entities, events, and cross-context edges. The inventory fills that gap.
4. **Cross-experiment reuse.** E6 and E9 both use the same domains (Cargo Shipping, IDDD, eShop). Without inventory, each experiment re-extracts the same domain models independently.

Data flow:
```
SOURCE-CATALOG (discovery) → INVENTORY (domain models) → EXPERIMENTS (data collection)
```
</objective>

<flags>
- `ingest` — Extract domain model from a source and create/update its inventory entry.
- `lookup` — Retrieve inventoried domain models matching criteria.
- `validate` — Check inventory completeness and freshness against SOURCE-CATALOG.
- `backfill` — Reconstruct inventory entries from completed experiment JSONL data.
- `--source <source-id>` — Target a specific SOURCE-CATALOG entry (e.g., `GH-CargoTracker`).
- `--experiment <EX>` — Scope to sources used by an experiment.
- `--domain <domain-name>` — Lookup by domain name (e.g., "Cargo Shipping").
- `--patterns <P1,P2,...>` — Filter by composition patterns exercised.
- `--min-bcs <n>` — Filter by minimum bounded context count.
</flags>

<context>
**Input:**
- `domainspec/docs/research/sources/SOURCE-CATALOG.md` — master catalog of validated sources.
- `domainspec/docs/research/data/*.jsonl` — raw experiment data (for backfill).
- `domainspec/docs/research/experiments/EX-*.md` — experiment protocols (for requirement matching).
- `domainspec/TAXONOMY.md` — 24 meta-types for concept classification.
- `domainspec/RELATIONSHIPS.md` — 26 relationships + proposed extensions for edge classification.
- External sources (GitHub repos, web pages) — for ingest.

**Output:**
- `domainspec/docs/research/inventory/{source-id}.md` — one file per inventoried source.
- `domainspec/docs/research/inventory/INVENTORY-INDEX.md` — cross-source index with lookup dimensions.
</context>

<principles>
1. **Extract once, use many times.** A domain model extraction should be thorough enough that no experiment ever needs to re-fetch the same source.
2. **Structured over prose.** Inventory entries use tables and typed fields, not free-text descriptions. This enables machine lookup.
3. **Trace to source.** Every concept and edge in the inventory cites its source location (book chapter, file path, code class).
4. **Classify using DomainSpec vocabulary.** Concepts get meta-types from TAXONOMY.md. Edges get relationship types from RELATIONSHIPS.md. This makes inventory directly usable by experiments.
5. **Append-only concepts, updatable metadata.** Once a concept is inventoried, it stays. Metadata (evidence quality, experiment usage) can be updated.
6. **Backfill from experiments.** Completed experiments contain validated domain model data. Backfilling from JSONL captures what we already know.
</principles>

<process>

## Operation: `ingest`

Extract a domain model from a source and create/update its inventory entry.

### Steps

1. **Identify source.** Read SOURCE-CATALOG.md to get source metadata (URL, category, BCs, depth).
2. **Fetch content.** For GitHub repos: fetch repo structure, key domain files (entities, events, aggregates). For books: reference known chapters. For prior experiment data: read JSONL.
3. **Extract bounded contexts.** Identify all bounded contexts with:
   - Name
   - Description (1–2 sentences)
   - Aggregate roots
   - Key domain events
   - Persistence strategy (if known)
4. **Extract concept inventory per BC.** For each bounded context, list:

   | Concept | Meta-Type | Description | Source Location |
   |---------|-----------|-------------|-----------------|

   Use meta-types from TAXONOMY.md: Entity, Value Object, Enum, Operation, Query, Calculation, Rule, Policy, Workflow, Interface, Event, Mapping, State Machine.

5. **Extract cross-context edges.** Identify all known cross-context interactions:

   | Source BC | Target BC | Concept | Concept Type | Edge Type | Pattern | Direction | Source Location |
   |----------|-----------|---------|-------------|-----------|---------|-----------|-----------------|

   Use edge types from RELATIONSHIPS.md + proposed extensions (produces-for, triggers-cross, enforces-cross).
   Use composition patterns: P1-data-handoff, P2-entity-reference, P3-event-trigger, P4-saga, P5-cross-enforcement, P6-shared-context.

6. **Assess completeness.** Rate extraction:
   - **Concept coverage:** How many of the 13 backend meta-types are exercised?
   - **Edge coverage:** How many composition patterns are present?
   - **Confidence:** high (from code/detailed docs), moderate (from book chapters), low (reconstructed from architecture diagrams).

7. **Write inventory file.** Create `inventory/{source-id}.md` using the template below.

### Inventory Entry Template

```markdown
# {Source ID} — {Domain Name}

**Source:** {URL or reference}
**Category:** {A–F from SOURCE-CATALOG}
**Extracted:** {date}
**Confidence:** {high | moderate | low}
**Used in experiments:** {E6, E9, ...}

---

## Bounded Contexts

| # | Context | Description | Aggregate Roots | Key Events | Persistence |
|---|---------|-------------|-----------------|------------|-------------|

---

## Concept Inventory

### {BC Name}

| Concept | Meta-Type | Description | Source Location |
|---------|-----------|-------------|-----------------|

(repeat per BC)

---

## Cross-Context Edges

| # | Source BC | Target BC | Concept | Type | Edge Type | Pattern | Direction |
|---|----------|-----------|---------|------|-----------|---------|-----------|

---

## Composition Patterns Exercised

| Pattern | Present? | Edge Count | Notes |
|---------|:--------:|----------:|-------|
| P1 — Data Handoff | | | |
| P2 — Entity Reference | | | |
| P3 — Event Trigger | | | |
| P4 — Saga | | | |
| P5 — Cross-Enforcement | | | |
| P6 — Shared Context | | | |

---

## Meta-Type Coverage

| Meta-Type | Count | BCs | Notes |
|-----------|------:|-----|-------|

---

## Evidence Notes

- Extraction confidence: {high/moderate/low}
- Known gaps: {what couldn't be extracted}
- Recommended for experiments: {which experiment types benefit from this source}
```

## Operation: `lookup`

Retrieve inventoried domain models matching criteria.

### Steps

1. **Parse criteria.** Accept filters: domain name, min BC count, composition patterns needed, meta-type stress, industry vertical, confidence level.
2. **Read INVENTORY-INDEX.md.** Scan the cross-source index for matching entries.
3. **Load matching entries.** Read the full inventory files for matches.
4. **Return structured results.** For each match, return:
   - Source ID and domain name
   - Bounded context count
   - Concept count by meta-type
   - Cross-context edge count by pattern
   - Confidence level
   - Prior experiment usage

### Lookup Examples

```
# Lookup by domain
lookup --domain "Cargo Shipping"
→ Returns GH-CargoTracker + BOOK-Evans-BlueBook entries

# Lookup by composition patterns needed
lookup --patterns P3,P4,P5 --min-bcs 4
→ Returns sources exercising event triggers, sagas, AND cross-enforcement with 4+ BCs

# Lookup by experiment
lookup --experiment E9
→ Returns all sources used/usable for E9
```

## Operation: `validate`

Check inventory completeness and freshness.

### Steps

1. **Cross-reference SOURCE-CATALOG vs inventory.** Flag catalog entries without inventory files.
2. **Check freshness.** For GitHub sources, check if commit SHAs have changed (if pinned).
3. **Check experiment coverage.** For completed experiments, verify that all sources used have inventory entries.
4. **Report gaps.** Output:
   - Sources in catalog but not inventoried
   - Sources inventoried but not in catalog (orphans)
   - Sources used by experiments but with low-confidence inventory
   - Sources with missing version pins

## Operation: `backfill`

Reconstruct inventory entries from completed experiment JSONL data.

### Steps

1. **Read JSONL.** Parse all experiment data files.
2. **Group by source.** Cluster edges/concepts by `source_reference` and `domain_id`.
3. **Extract domain models.** From each experiment's data:
   - Bounded contexts (from `source_context` / `target_context` fields)
   - Concepts (from `shared_concept` / `concept_type` fields)
   - Cross-context edges (full edge records)
   - Composition patterns (from `pattern_id` field)
4. **Merge with existing inventory.** If an inventory entry exists, add new concepts/edges found in the experiment. If not, create a new entry with confidence = "moderate" (derived from experiment data, not direct source extraction).
5. **Update INVENTORY-INDEX.md.**

</process>

<inventory-index-template>
The INVENTORY-INDEX.md provides a cross-source lookup table:

```markdown
# Research Inventory Index

**Last updated:** {date}
**Entries:** {count}

## Quick Lookup

| Source ID | Domain | BCs | Concepts | Edges | Patterns | Confidence | Experiments |
|-----------|--------|----:|--------:|------:|----------|:----------:|-------------|

## By Industry

| Industry | Sources |
|----------|---------|

## By Composition Pattern

| Pattern | Sources (count) |
|---------|----------------|

## By Meta-Type Stress

| Meta-Type | Sources exercising it |
|-----------|---------------------|
```
</inventory-index-template>

<integration>
### How Other Skills/Agents Use the Inventory

**Research Scientist (experiment execution):**
```
Before running an experiment:
1. lookup --experiment EX → get pre-extracted domain models
2. Use inventory concepts/edges as reconstruction baseline
3. After experiment: backfill --experiment EX → update inventory with new findings
```

**Research Sourcer (source discovery):**
```
When evaluating a candidate source:
1. validate → check if source is already inventoried
2. If inventoried: use depth/quality data for scoring
3. If not: flag as needing ingest before experiment can use it
```

**Research Analyst (analysis):**
```
During triangulation (Step 7):
1. lookup → check how many independent sources support a finding
2. Cross-reference inventory coverage with experiment data coverage
```
</integration>
