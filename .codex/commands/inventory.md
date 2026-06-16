# Arcanum Sigil: inventory

<!-- arcanum:capability-id inventory -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command inventory -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-inventory-<UTC timestamp>`.
- `capability.id`: `inventory`
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

Run the installed Arcanum sigil `inventory` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `inventory`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/inventory/README.md

````markdown
# Inventory

Inventory is an Arcana sigil for installing and maintaining a repository-local compiled knowledge layer.

It is inspired by the wiki pattern: raw sources remain immutable, while an LLM-maintained markdown inventory accumulates summaries, entity pages, concept pages, architecture notes, pattern entries, contradictions, tags, indexes, and logs. The repository stops treating knowledge as something to rediscover from raw documents every time and starts treating it as a maintained asset.

## Problem It Solves

Retrieval from raw files is useful, but it does not compound. Every question asks the agent to rediscover and resynthesize knowledge from scattered sources.

Inventory solves this by creating a maintained intermediate layer between raw sources and task execution. New sources are ingested once, integrated into existing pages, cross-linked, tagged, and logged. Later sigils can query the inventory before searching the whole repository.

## Evidence-Card Layer

Inventory can also maintain source-backed `evidence-card` records for reusable, selector-level knowledge.

An evidence-card is a compact unit with `source_refs`, authority state, captured provenance, optional `trace`, optional `residue`, and promotion metadata such as `promotion_owner`. Cards are designed for task-shaped lookup, linting, and downstream handoff packets without making Inventory the owner of ontology relations or canonical definitions.

Use evidence-cards when a source detail needs to be:

- inspected quickly through stable selectors,
- reused in more than one task,
- grouped into retrieval output,
- linted for authority or schema gaps,
- handed to Ontology Vault or Definitions Governance as candidate evidence.

Evidence-card handoffs must include a non-authority notice: downstream owners decide promotion, not Inventory.

## EvidenceSet Candidate Layer

Inventory may maintain candidate `EvidenceSet` records when the same evidence-card group needs to be reused across retrieval or handoff assembly.

An EvidenceSet is a flat grouped-evidence artifact: it stores included evidence-card IDs, excluded card IDs, reasons, index terms, handoff intent, a short synthesis note, residue, status, and promotion owner. It references evidence-cards rather than copying source excerpts, summaries, trace arrays, or captured metadata.

EvidenceSets are candidate-level until an explicit later promotion decision. They do not replace Context Builder packs, own ontology or definition authority, implement a ledger, or add a human UI surface.

## Use When

- a repository accumulates knowledge across many files, docs, conversations, or source captures,
- agents repeatedly rediscover the same architecture, terminology, decisions, or patterns,
- `context-builder` needs better selector-level evidence,
- `architecture-pattern-inventory` needs a broader knowledge substrate,
- a team wants a local markdown wiki that an LLM maintains,
- raw sources should stay immutable while generated summaries evolve.

## Do Not Use When

- the repository is too small to need a maintained knowledge layer,
- raw sources are not available or cannot be cited,
- the user wants one temporary answer rather than reusable inventory,
- the repository already has a maintained inventory and only needs a narrow lookup,
- the workflow cannot tolerate generated markdown updates.

## Architecture

Inventory uses three layers:

1. Raw sources: user-curated source material that the sigil reads but does not modify.
2. Inventory wiki: generated markdown pages the sigil creates and updates.
3. Schema: local conventions that tell future agents how to ingest, tag, query, lint, and maintain the inventory.

## Default Package

The recommended install root is:

```text
.arcanum/inventory/
```

The default package contains:

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

Install mode may adapt to an existing docs, wiki, notes, or architecture package instead of creating a competing structure.

## Operations

- `install`: detect existing knowledge systems, ask setup questions, and create or adapt the inventory package.
- `ingest`: read raw sources, create source summaries, update related entries, flag contradictions, and append the log.
- `lookup`: return relevant inventory pages, evidence-cards, EvidenceSets, source refs, selectors, excluded matches, and gaps for another sigil.
- `query`: answer against the inventory and optionally file the answer as a synthesis page.
- `lint`: find contradictions, stale claims, orphan pages, missing backlinks, untagged pages, source coverage gaps, invalid evidence-card enums, unsafe owner/status pairs, missing `source_refs`, missing `trace`, and unresolved `residue`.
- `validate`: check package structure, index coverage, log parseability, tag consistency, evidence links, evidence-card schema fields, EvidenceSet references, and downstream non-authority packet language.
- `backfill`: build entries from existing docs, architecture packages, context packs, decisions, or generated artifacts.
- `sync`: update package conventions after schema changes.

## Integration

[context-builder](../../transmutations/context-builder/) should consume inventory lookups before broad source search when building a task context pack.

[architecture-pattern-inventory](../architecture-pattern-inventory/) can read the inventory before mapping architecture and can contribute entries such as architecture layers, implementation patterns, dependency rules, test patterns, and observability signals.

Use the [repository observability package](../../framework/observability/REPOSITORY-PACKAGE.md) when available to record install decisions, ingests, contradictions, lint gaps, and validation results.

Ontology Vault and Definitions Governance may consume evidence-card handoff packets or candidate EvidenceSets, but those packets and sets are read models. `promotion_owner`, `governed_ref`, and non-authority notices must make clear when evidence is only captured or candidate-level.

## Why This Is Arcana

Inventory coordinates installation, local schema design, source ingestion, cross-page maintenance, lookup contracts, linting, and integration with other sigils. It is a long-lived repository knowledge system, not a one-time synthesis artifact.

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/inventory/SKILL.md

````markdown
---
name: inventory
description: "Use when: installing or maintaining a repository-local compiled knowledge inventory that lets agents ingest once, index, tag, query, lint, and reuse context across sigils."
argument-hint: "<install|ingest|lookup|query|lint|validate|backfill|sync> [--path <repo-root>] [--root <inventory-root>] [--source <path>] [--type <entry-type>] [--query <text>] [--dry-run]"
tier: arcana
domain: knowledge-inventory
version: 0.1.0
origin: generalized from recurring inventory and compiled-wiki maintenance practice
allowed-tools: Read, Write, Glob, Grep, Bash, AskQuestions, Task
---

# Sigil: Inventory

<objective>
Install and maintain a repository-local compiled knowledge layer that keeps raw sources immutable, generated inventory pages current, and reusable context available to other sigils.
</objective>

<logic-type>
Arcana: long-lived knowledge maintenance, local schema governance, ingestion, linting, and cross-sigil integration.
</logic-type>

<core-promise>
Inventorize once, reuse many times.
</core-promise>

<modes>
- `install`: create or adapt the local inventory package.
- `ingest`: process raw sources into generated inventory pages and optional source-backed evidence-cards.
- `lookup`: return matching entries, evidence-cards, candidate EvidenceSets, source refs, selectors, exclusions, and gaps for another sigil.
- `query`: answer from inventory pages and optionally file the answer as a synthesis page.
- `lint`: health-check contradictions, staleness, orphans, missing links, tags, source coverage, evidence-card fields, EvidenceSet references, owner/status pairs, trace, residue, and non-authority handoff language.
- `validate`: check package structure, index coverage, log parseability, tag consistency, evidence links, evidence-card schema fields, EvidenceSet references, and downstream packet boundaries.
- `backfill`: build inventory entries from existing repository artifacts.
- `sync`: update inventory files after schema or convention changes.
</modes>

<default-package>
Use `.arcanum/inventory/` unless the user chooses an existing docs, wiki, or knowledge-base location.

Default layout:

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
</default-package>

<install-process>
1. Detect existing repository knowledge systems before asking questions:
   - docs folders,
   - wiki or notes folders,
   - architecture packages,
   - existing indexes,
   - generated context packs,
   - decision records,
   - observability packages.
2. Ask only unanswered setup questions:
   - inventory root path,
   - raw source location,
   - generated wiki or entry location,
   - whether existing docs should be adopted or left separate,
   - tagging style,
   - frontmatter preference,
   - wiki-link preference,
   - source immutability policy,
   - observability integration preference.
3. Create or adapt the inventory package from templates.
4. Record the local schema and selected conventions.
5. Append an install entry to the log.
6. Return the package path, selected conventions, and next recommended ingest.
</install-process>

<ingest-process>
1. Resolve source path or source set.
2. Confirm raw sources are read-only inputs.
3. Read each source and extract reusable knowledge:
   - source summary,
   - entities,
   - concepts,
   - decisions,
   - workflows,
   - architecture layers,
   - implementation patterns,
   - interfaces,
   - dependency rules,
   - test patterns,
   - observability signals,
   - contradictions,
   - open questions.
4. When the source detail needs selector-level reuse, draft an `evidence-card` with `source_refs`, authority level, captured metadata, `promotion_owner`, and optional `trace` or `residue`.
5. Create or update generated inventory pages.
6. Link related entries and update backlinks when the local schema uses them.
7. Flag contradictions and stale claims instead of silently overwriting them.
8. Update `index.md`, `tags.md`, and `log.md`.
9. Emit observability signals when the observability package exists.
</ingest-process>

<lookup-process>
1. Read `index.md` first.
2. Search entries by type, tag, source, title, summary, and query text.
3. Include matching evidence-cards when they provide better selector-level evidence than a broad page.
4. Include candidate EvidenceSets when a stable group of card IDs answers the task faster than independent card matches.
5. Return selector-level matches suitable for downstream sigils.
6. Include why each match is relevant and which task or obligation it can satisfy.
7. Include excluded matches when they clarify why nearby evidence was not selected.
8. Report gaps when inventory does not cover the requested topic.
</lookup-process>

<query-process>
1. Resolve the question and search the inventory index first.
2. Read relevant generated pages and their source references.
3. Synthesize an answer with citations to inventory pages and raw source references when available.
4. Ask whether the answer should be filed as a synthesis page when it has durable value.
5. If filed, update index, tags, and log.
</query-process>

<lint-process>
Check for:

- contradictions between pages,
- stale claims superseded by newer sources,
- orphan pages with no incoming or outgoing links,
- important concepts mentioned but lacking pages,
- missing cross-references,
- untagged pages,
- invalid frontmatter when frontmatter is enabled,
- raw sources not yet inventoried,
- generated pages without source coverage,
- log entries that do not match the configured heading pattern,
- evidence-cards missing `source_refs`,
- evidence-cards with unknown controlled vocabulary values,
- EvidenceSets with unknown controlled vocabulary values,
- EvidenceSets that reference missing evidence-card IDs,
- EvidenceSets that duplicate evidence-card source excerpts or summaries,
- full evidence-cards missing `trace`,
- terminal promotion status with `promotion_owner: none`,
- relation candidates missing a non-authority notice,
- unresolved `residue` that should be surfaced in lookup or validation output.
</lint-process>

<evidence-card-contract>
Evidence-cards are source-backed Inventory records. They may capture candidate claims, concepts, methods, questions, relation candidates, contradictions, and operational lessons.

Required authoring behavior:

- every material claim points to `source_refs` or is explicitly marked as inference, synthesis, or open question,
- `trace` records field-level extraction or assignment decisions for full cards,
- `residue` preserves schema or instance ambiguity instead of hiding it,
- `promotion_owner` records who owns terminal promotion decisions,
- downstream packets include non-authority language and do not imply ontology or definition promotion,
- `governed_ref` appears only after the downstream owner creates a real governed artifact.
</evidence-card-contract>

<evidence-set-contract>
EvidenceSets are candidate Inventory records that group evidence-card IDs for repeated retrieval and handoff assembly.

Required authoring behavior:

- reference evidence-card IDs instead of copying card content,
- include `card_refs` with inclusion reasons,
- include `excluded_card_refs` with boundary reasons,
- include `index_terms` for shell plus `jq` lookup,
- include `handoff_target`, `synthesis_note`, and `residue`,
- keep `status` candidate-level unless a later explicit promotion decision exists,
- do not imply ontology, definition, ledger, or Context Builder authority.
</evidence-set-contract>

<entry-types>
Default entry types:

- `source`,
- `entity`,
- `concept`,
- `architecture-layer`,
- `implementation-pattern`,
- `decision`,
- `capability`,
- `workflow`,
- `interface`,
- `dependency-rule`,
- `test-pattern`,
- `observability-signal`,
- `question`,
- `contradiction`,
- `synthesis`.

Repositories may add custom entry types in `schema.md` when they define required fields, evidence rules, tag rules, and update behavior.
</entry-types>

<integration-contract>
For `context-builder`, lookup output should include:

- inventory page path,
- evidence-card ID when available,
- selector or heading,
- summary,
- tags,
- confidence,
- source references,
- task obligation fit,
- excluded matches when useful,
- unresolved gaps.

For `architecture-pattern-inventory`, inventory output should support entries for:

- architecture layers,
- implementation patterns,
- dependency rules,
- test patterns,
- observability signals,
- relationship notes.
</integration-contract>

<authority-rule>
Raw sources are read-only inputs. Generated inventory pages may evolve, but every material claim should point back to source evidence or be marked as inference, synthesis, or open question.

Inventory owns evidence-cards, indexes, lint findings, and handoff projections. Ontology Vault owns governed meaning, relations, confidence, and promotion. Definitions Governance owns canonical definitions. Evidence-card handoff packets are non-authority read models until a downstream owner accepts them.
</authority-rule>

<observability>
When `.arcanum/observability/` exists, emit post-run signals for:

- mode,
- install decisions,
- source count,
- entries created,
- entries updated,
- contradictions found,
- lint gaps,
- validation result,
- downstream sigil lookups,
- filed query syntheses.
</observability>

<quality-bar>
A successful execution must:

- preserve raw source immutability,
- create or respect a local schema,
- maintain both `index.md` and `log.md`,
- tag generated pages consistently,
- link generated knowledge to source evidence,
- flag contradictions instead of hiding them,
- expose lookup results that other sigils can consume,
- avoid creating a competing system when a repository already has a usable wiki or inventory.
</quality-bar>

<anti-patterns>
Avoid:

- editing raw sources during ingest,
- making generated pages the sole authority for source facts,
- dumping source summaries without updating related pages,
- creating tags ad hoc without recording them,
- answering queries from raw files while ignoring the inventory,
- overwriting contradictions instead of recording them,
- installing a new package when existing repository conventions can be adapted,
- letting inventory maintenance replace human source curation.
</anti-patterns>

<output-contract>
Return:

```markdown
## Inventory Result

- Mode: install | ingest | lookup | query | lint | validate | backfill | sync
- Repository: <path>
- Inventory root: <path>
- Files changed: <paths or none>
- Sources processed: <count>
- Entries created: <count>
- Entries updated: <count>
- Index updated: yes | no
- Log updated: yes | no
- Contradictions flagged: <count>
- Lint gaps: <count>
- Validation: pass | fail | not run
- Downstream lookup output: <summary or none>
- Next action: <action>
```
</output-contract>

````
