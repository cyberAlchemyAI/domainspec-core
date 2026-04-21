---
name: domainspec-research-sources-generic
description: "Discover, validate, and catalog external data sources for any research experiment. Produces SOURCE-CATALOG.md with typed knowledge entries, diversity analysis, and feasibility checks before experiment execution."
argument-hint: "<experiment-id | --all-pending> [--entry-type <type1,type2>] [--min-sources <n>] [--diversity-target <n>]"
agent: domainspec-research-sourcer
allowed-tools: Read, Write, Bash, Glob, Grep, Fetch, AskQuestions
---

<objective>
Systematically discover, validate, and score external data sources BEFORE running experiments, supporting ANY experiment data requirement — domain models, research papers, tool evaluations, framework architectures, role specifications, or domain-specific codebases.

This skill exists because:
1. **Source quality determines experiment quality.** An experiment run on poorly-vetted sources produces weak evidence. Garbage in, garbage out.
2. **Diversity must be deliberate.** Without structured sourcing, selection clusters around the familiar (everyone uses the same 3 DDD books, nobody reads systems papers, etc).
3. **Accessibility failures waste execution time.** Discovering mid-experiment that a repo is archived, a paper is paywalled, or a codebase is too minimal forces protocol deviations.
4. **Reproducibility requires source pinning.** Sources change — repos get deleted, papers move, APIs evolve. Versions must be recorded.
5. **Knowledge entry types are meta-independent.** Both "domain models from GitHub" and "governance papers from arXiv" and "tool configs from documentation" are sources; same discovery, validation, and cataloging logic applies.
</objective>

<flags>
- `--all-pending`: Discover sources for all experiments with "not started" status in EXPERIMENTS.md and EXPERIMENTS-META.md.
- `--experiment <EX>`: Target a specific experiment ID (e.g., E1, E11, E20).
- `--entry-type <types>`: Comma-separated list of knowledge entry types needed (e.g., `domain-model,paper-abstract,tool-evaluation`). If omitted, infer from experiment protocol.
- `--claim <CX | CMX>`: Focus on experiments supporting a specific DomainSpec claim (C1-C4) or meta-meta claim (CM1-CM4).
- `--min-sources <n>`: Minimum candidate sources to discover before filtering (default: 3× the number needed).
- `--diversity-target <n>`: Minimum number of distinct source categories to cover (default: 4).
</flags>

<context>
**Input:**
- `EXPERIMENTS.md` — DomainSpec experiment index (E1-E10).
- `EXPERIMENTS-META.md` — Meta-Meta framework experiment index (E11-E20).
- `experiments/EX-*.md` — individual experiment protocols with data requirements.
- `domainspec-paper.md`, `meta-meta-paper.md` — paper claims needing evidence.
- `TAXONOMY.md`, `RELATIONSHIPS.md` — DomainSpec vocabulary (for domain-model entry types).
- `results/*.md` — prior experiment results (which sources produced strong evidence).

**Output:**
- `sources/SOURCE-CATALOG.md` — master catalog of validated sources (all entry types, all experiments).
- `sources/EX-sources.md` — per-experiment source selection with rationale.

**Existing data (learn from prior runs):**
- `data/*.jsonl` — check which sources were already used and their evidence quality.
- `inventory/INVENTORY-INDEX.md` — check which sources are already inventoried (avoid re-discovery).
</context>

<principles>
1. **Over-discover, then filter.** Find 3× more candidates than needed, score them, pick the best. Don't stop at first N that seem reasonable.
2. **Diversity is first-class.** Score source sets on orthogonality: entry type, domain/topic, documentation depth, complexity, evidence quality rating from prior experiments.
3. **Verify before committing.** Every source must pass: (a) accessibility check (can we actually fetch it?), (b) depth check (does it have enough detail for the experiment's needs?), (c) version-ability check (can we pin it for reproducibility?).
4. **Pin versions meticulously.** Record: GitHub repo commit SHA + date, book edition/year, paper DOI, archive.org snapshot date, website last-fetch date. If a source can't be pinned, flag as "fragile" and find alternatives.
5. **Learn from prior experiments.** Check `results/EX-results.md` — which sources produced strong evidence in E6/E9? Prefer similar sources. Which were too shallow? Avoid similar ones.
6. **Bias toward public, structured, accessible sources.** Preference order depends on entry type:
   - **domain-model** (E6, E9): (a) open-source reference implementations with tests, (b) published books with code samples, (c) system design blogs with domain decompositions, (d) event modeling examples, (e) academic case studies
   - **paper-abstract** (E11-E20): (a) peer-reviewed SE venues (ICSE, FSE, ASE), (b) arXiv preprints, (c) workshop papers, (d) industry white papers, (e) blogs/talks
   - **tool-evaluation** (E17, E15): (a) official tool documentation, (b) academic benchmarks, (c) GitHub repos using the tool, (d) comparative studies
   - **framework-architecture** (E11-E13): (a) published papers, (b) open-source reference implementations, (c) technical blog posts, (d) design documents
   - **role-definition** (E13, E16, E18): (a) academic papers on agent systems, (b) industry standards/protocols, (c) GitHub agent frameworks, (d) published role models
</principles>

<process>

## Step 1 — Identify Source Requirements

1. Read target experiment protocol (`experiments/EX-*.md`).
2. Extract **source requirements:**
   - What entry types are needed? (domain-model, paper-abstract, tool-eval, framework-arch, role-def, etc.)
   - How many distinct sources?
   - What diversity dimensions matter? (for domain-models: industry, BC count, pattern variety; for papers: venue, year, methodology; for tools: maturity, community size, etc.)
3. Check existing completed experiments — what sources worked well?
   - Read `results/EX-results.md` for evidence quality ratings.
   - Check if sources are already inventoried (`inventory/INVENTORY-INDEX.md`).
4. Output: **Source Requirements Brief** — structured summary of what we need, how many, constraints.

## Step 2 — Discover Candidate Sources

### Entry Type: `domain-model` (for E1-E10, E15, E20)
**Search across these source categories:**

| Category | Source Examples | Quality Signals | Caution |
|----------|-----------------|-----------------|---------|
| **A** — Ref Implementations | eShopOnContainers, CargoTracker, IDDD_Samples | ≥500 stars, tests, docs, recent | Check code quality, not just domain structure |
| **B** — DDD Literature | Evans Blue Book, Vernon IDDD, Wlaschin DMMF | Peer-reviewed, widely cited, with examples | Limited to ~20 canonical domains |
| **C** — System Design Corpus | system-design-primer, karanpratapsingh, ByteByteGo | Well-decomposed architecture, named contexts | More architecture than domain model |
| **D** — Event Modeling Artifacts | eventmodeling.org, published workshops | Explicit events, command/query, aggregates | Small sample size |
| **E** — Academic Case Studies | ICSE/FSE papers with domain case studies | Peer-reviewed, reproducible, diagrams | Smaller domains, limited code |
| **F** — Industry Architecture | Cloud provider ref archs, financial services whitepapers | Large-scale, battle-tested, documented | Proprietary or generic, may lack detail |

**Search commands:**
```bash
GitHub: search:"bounded context" OR "aggregate root" language:java stars:>500
arXiv: "domain-driven design" OR "event sourcing" 
Books: Evans Blue Book, Vernon IDDD, search WorldCat
```

### Entry Type: `paper-abstract` (for E11-E20, E4, E7, E8)
**Search across venues:**

| Venue | Years | Focus | Access |
|-------|-------|-------|--------|
| ICSE, FSE, ASE | 2020+ | SE methodology, tools, empirical | ACM DL, author preprints |
| arXiv:cs.SE, cs.MA, cs.AI | 2018+ | Preprints, broader scope | Open access |
| IEEE TSE, JSS | 2020+ | Software engineering theory | Paywalled (check university access) |
| Workshops (ASE demos, etc) | 2019+ | Early-stage ideas, tools | Often open |
| Tech blogs, Medium | recent | Practitioner insights | Variable quality |

**Search strategy:**
- "multi-agent systems", "self-improving", "governance feedback"
- "test derivation", "specification testing"
- "agent specialization", "role-based coordination"
- "knowledge reuse", "domain transfer learning"

### Entry Type: `tool-evaluation` (for E17, E15)
**Evaluate tools used in pipeline:**

| Tool Category | Examples | Discovery | Evaluation Criteria |
|---|---|---|---|
| **Test Derivation** | Stryker, PIT, ArchUnit | GitHub + docs | Coverage, mutation kill rate, cost |
| **Observability** | OpenTelemetry, Prometheus, Grafana | docs + benchmarks | Signal richness, overhead, exporters |
| **Agent Frameworks** | LangChain, CrewAI, AutoGen | GitHub docs, tutorials | Agent communication, conversation patterns, cost tracking |
| **Knowledge Bases** | Pinecone, Weaviate, Milvus | docs + benchmarks | Retrieval speed, scalability, reranking |

### Entry Type: `framework-architecture` (for E11-E13, E19)
**Sources describing multi-agent governance architectures:**

| Source Type | Examples | Search |
|---|---|---|
| Papers | "Multi-Agent Reinforcement Learning", "Hierarchical Planning" | arXiv + ACM DL |
| GitHub | LangChain architecture, CrewAI design, AutoGen patterns | GitHub search + README mining |
| Books | "Designing Distributed Systems" (Burns), "Patterns of Enterprise..." | O'Reilly, publisher searches |
| Specifications | OpenAI APIs, LLM provider architectures | Official docs |

### Entry Type: `role-definition` (for E13, E16, E18)
**Sources defining agent roles and contracts:**

| Source Type | Examples | Search |
|---|---|---|
| Papers | "Agent Negotiation Protocols", "Role-Based Access Control" | arXiv + ACM |
| GitHub | LangChain agents, CrewAI roles, AutoGen groupchat | Repository examples |
| Industry Specs | FIPA agent communication standards | W3C, OMG specs |
| Frameworks | Conversation design patterns | Documentation + blogs |

## Step 3 — Validate Each Candidate

For each discovered source:

1. **Accessibility check:**
   - Can the URL be fetched?
   - Is it behind a paywall? (if yes, check university/library access)
   - Is it archived/deleted? (use archive.org if needed)
   - Return `status: accessible | paywalled | archived | deleted`

2. **Depth check:**
   - Does it contain the minimum detail needed for the experiment's data schema?
   - For domain-models: ≥3 bounded contexts? ≥10 concepts? Explicit relationships?
   - For papers: ≥4 pages? Includes evaluation/case study? Peer-reviewed?
   - For tools: ≥1000 GitHub stars OR published paper? Active maintenance?
   - Return `depth: sufficient | marginal | insufficient`

3. **Version-ability check:**
   - GitHub: Record commit SHA + date. Is the repo archived/read-only? ✓
   - Books: Edition + year. In print? Can be ordered? ✓
   - Papers: DOI + date. Can we access via academic repository? ✓
   - Web: Archive.org snapshot date. Is it stable? ✓
   - Return `versionable: yes | fragile | no`

4. **Evidence quality (for sources used in prior experiments):**
   - Check `results/EX-results.md` — did this source produce strong evidence?
   - Rate: `strong | moderate | weak | untested`

## Step 4 — Score & Select

Score each source:
```
score = accessibility (0-1) × depth (0-1) × versionability (0-1) × prior_evidence (0-1) + diversity_bonus (0-0.3)
```

**Diversity bonus:**
- +0.1 for each source category not yet represented in the selection
- +0.05 for cross-sector sources (if domain-models: academia, industry, books all represented)

Select top-N sources satisfying:
- All selected sources score ≥ 0.6
- Diversity target met (≥4 distinct categories)
- At least 1 per entry type (if multiple needed)

## Step 5 — Output: SOURCE-CATALOG.md & EX-sources.md

**SOURCE-CATALOG.md** format:

```markdown
# Research Source Catalog

| ID | Source | Type | Category | URL | Details | Version | Accessible | Depth | Evidence | Score |
|----|--------|------|----------|-----|---------|---------|------------|-------|----------|-------|
| GH-CargoTracker | Eclipse CargoTracker | domain-model | A-RefImpl | github.com/... | Jakarta EE ref impl, 5 BCs | commit abc123 (2026-01-15) | ✅ | sufficient | strong | 0.95 |
| PAPER-AuthorityAgent | "Authority-Based Agent Negotiation" | role-definition | D-Paper | arxiv.org/... | ICSE 2023, agent protocols | DOI:... | ✅ | sufficient | untested | 0.85 |
| TOOL-Stryker | Stryker Mutation Testing | tool-evaluation | B-Tool | stryker-mutator.io | Mutation framework, JS/TS | v7.3.1 | ✅ | sufficient | moderate | 0.80 |
```

**EX-sources.md** format:

```markdown
# E11 — Governance Signal Extraction — Source Selection

## Requirements
- Entry types: `domain-model` (3 different domains), `paper-abstract` (2 recent governance papers)
- Diversity: 3 distinct domain industries, 2+ paper venues
- Success criteria: all sources must be ≥ accessible + sufficient

## Selected Sources

| Source ID | Justification | Experiment Usage |
|-----------|---|---|
| GH-eShopOnContainers | Microservices domain model, 6 BCs, multi-layer (addresses E11 signal extraction across layers) | Extract governance signals per BC + cross-BC |
| PAPER-AuthorityAgent | 2024 ICSE paper on agent governance, peer-reviewed | Informed signal schema design |
| PAPER-SelfImprovingML | 2023 FSE case study on system optimization | Prior art on feedback loop fidelity |
```

See [TEMPLATE.md](TEMPLATE-SOURCE-CATALOG.md) for full format.

</process>

---

## Integration with Researcher Scientist Agent

The sourcer skill bridges `EXPERIMENTS.md` (experiment protocols) and `SOURCE-CATALOG.md` (validated sources).

**When to invoke sourcer:**
```
Before experiment execution:
  Scientist reads EX-*.md protocol
  ↓
  Calls sourcer --experiment EX --entry-type [inferred from protocol]
  ↓
  Sourcer produces EX-sources.md
  ↓
  Scientist checks inventory (inventorist lookup) for already-extracted models
  ↓
  Scientist executes experiment using EX-sources.md + inventory data
```

If a source isn't in inventory yet:
```
  Scientist delegates to inventorist ingest --source <source-id>
  ↓
  Inventorist produces inventory/{source-id}.md
  ↓
  Scientist uses inventory data in experiment
```
