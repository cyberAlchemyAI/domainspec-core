---
name: domainspec-research-sources
description: "Discover, validate, and catalog external data sources for DomainSpec research experiments. Produces a scored SOURCE-CATALOG.md with diversity analysis and feasibility checks before experiment execution begins."
argument-hint: "<experiment-id | --all-pending> [--claim <C1-C4>] [--min-sources <n>] [--diversity-target <n>]"
agent: domainspec-research-sourcer
allowed-tools: Read, Write, Bash, Glob, Grep, Fetch, AskQuestions
---

<objective>
Systematically discover, validate, and score external data sources BEFORE running experiments. This skill fills the gap between "experiment protocol defined" and "experiment execution started" — ensuring that the agent uses high-quality, diverse, accessible, and reproducible sources rather than ad-hoc selections.

This skill exists because:
1. **Source quality determines experiment quality.** An experiment run on poorly-documented domains produces weak evidence. Garbage in, garbage out.
2. **Diversity must be deliberate.** Without a structured sourcing process, domain selection clusters around familiar examples (the "Evans Cargo Shipping" trap — everyone uses the same 3 DDD examples).
3. **Accessibility failures waste execution time.** Discovering mid-experiment that a repo is archived, a paper is paywalled, or a domain model is too shallow to analyze forces protocol deviations.
4. **Reproducibility requires source pinning.** External sources change — repos get deleted, books go out of print, APIs break. Sources must be versioned/archived.
</objective>

<flags>
- `--all-pending`: Discover sources for all experiments with status "not started" in EXPERIMENTS.md.
- `--claim <C1-C4>`: Focus on experiments supporting a specific claim.
- `--min-sources <n>`: Minimum candidate sources to discover before filtering (default: 3× the number needed by the experiment).
- `--diversity-target <n>`: Minimum number of distinct source categories to cover (default: 4).
</flags>

<context>
**Input:**
- `domainspec/docs/research/EXPERIMENTS.md` — experiment index with status and protocols.
- `domainspec/docs/research/experiments/EX-*.md` — individual experiment protocols with data requirements.
- `domainspec/docs/research/domainspec-paper.md` — paper claims that need evidence.
- `domainspec/TAXONOMY.md`, `domainspec/RELATIONSHIPS.md` — meta-model vocabulary (what the sources need to exercise).

**Output:**
- `domainspec/docs/research/sources/SOURCE-CATALOG.md` — master catalog of validated sources.
- `domainspec/docs/research/sources/EX-sources.md` — per-experiment source selection with rationale.

**Existing data (learn from prior runs):**
- `domainspec/docs/research/data/*.jsonl` — check which sources were already used in completed experiments.
- `domainspec/docs/research/results/*.md` — check which sources produced good vs weak evidence.
</context>

<principles>
1. **Over-discover, then filter.** Find 3× more candidates than needed, score them, pick the best. Don't stop at the first N that seem reasonable.
2. **Diversity is a first-class metric.** Score source sets on orthogonality — industry vertical, domain complexity, documentation depth, bounded context count, and interaction pattern variety.
3. **Verify before committing.** Every source must pass an accessibility check (can we actually read/fetch the content?) and a depth check (does it contain enough detail for the experiment's data schema?).
4. **Pin versions.** Record commit SHA for repos, edition/year for books, DOI for papers, archive.org snapshot for web pages. If a source can't be pinned, flag it as fragile.
5. **Learn from prior experiments.** If a source category worked well in E6/E9, prefer it. If a source was too shallow, document why and avoid similar sources.
6. **Bias toward public, structured, well-referenced sources.** In order of preference: (a) open-source reference implementations with tests, (b) published DDD books with code samples, (c) system design repos with domain models, (d) academic case studies, (e) industry whitepapers, (f) reconstructed domain models from documentation.
</principles>

<process>

## Step 1 — Identify Source Requirements

1. Read `EXPERIMENTS.md` and identify target experiments (by `--all-pending` or specific ID).
2. For each target experiment, read its protocol file (`experiments/EX-*.md`).
3. Extract **source requirements** — what kind of external data does the experiment need?
   - Domain models? Code implementations? Architecture diagrams? User stories? Test suites?
   - How many distinct sources are needed?
   - What diversity dimensions matter? (industry, complexity tier, bounded context count, meta-type stress)
4. Check existing completed experiments — what sources were already used? What worked?
   - Read `data/*.jsonl` to extract `source_reference` fields from prior runs.
   - Read `results/*.md` to identify sources that produced strong vs weak evidence.
5. Output: **Source Requirements Brief** — a structured summary of what we need, how many, and what constraints apply.

## Step 2 — Discover Candidate Sources

Search broadly across these **source categories** (in priority order):

### Category A — Open-Source Reference Implementations
- GitHub search for DDD/clean architecture repos with domain models
- Look for: bounded context separation, entity/value object distinctions, event-driven patterns
- Quality signals: star count (≥500), test coverage, documentation, recent activity
- Key repos to check: eShopOnContainers, Eclipse CargoTracker, IDDD_Samples, ddd-by-examples/library, eventuate-tram-examples, axon-trader, ftgo-application

### Category B — DDD Canonical Literature
- Evans "Blue Book" domain examples (Cargo Shipping, etc.)
- Vernon "Red Book" domain examples (Collaboration, Agile PM)
- Wlaschin "Domain Modeling Made Functional" (Order-Taking)
- Vaughn Vernon "Strategic Monoliths and Microservices" examples
- Quality signals: published, peer-reviewed, cited in academic work

### Category C — System Design Interview Corpus
- system-design-primer (343k★), karanpratapsingh/system-design (43k★)
- ByteByteGo, Grokking the System Design Interview
- Quality signals: well-structured domain decomposition, named bounded contexts, documented data flows
- Caution: these are architecture-focused, not domain-model-focused — verify domain depth before using

### Category D — Academic Case Studies
- Search arXiv, Semantic Scholar, ACM DL for "domain-driven design case study", "bounded context", "aggregate pattern"
- Software engineering venues: ICSE, FSE, ASE, TSE, ESEM
- Quality signals: peer-reviewed, reproducible, includes domain model diagrams/tables

### Category E — Event Modeling / Event Storming Artifacts
- eventmodeling.org canonical examples (Hotel Booking)
- Published event storming workshop outputs
- Quality signals: explicit event flows, command/query separation, aggregate boundaries

### Category F — Industry Whitepapers & Documentation
- Cloud provider reference architectures (AWS, Azure, GCP)
- Domain-specific standards (HL7 FHIR for healthcare, ISO 20022 for banking, ACORD for insurance)
- Quality signals: formal data models, process flows, compliance requirements

6. For each candidate, record:
   - `source_id`: unique identifier (e.g., `GH-eShopOnContainers`, `BOOK-Evans-Ch7`, `PAPER-Smith2023`)
   - `category`: A–F
   - `name`: human-readable name
   - `url_or_reference`: where to access it
   - `domain`: business domain it represents
   - `bounded_contexts`: named bounded contexts (if known)
   - `estimated_depth`: shallow / moderate / deep (based on initial scan)
   - `accessibility`: public / restricted / paywalled
   - `version_pin`: commit SHA, edition, DOI, or archive URL

## Step 3 — Validate Source Quality

For each candidate source, perform these checks:

### Accessibility Check
7. Can the source actually be fetched/read?
   - For repos: `git ls-remote` or GitHub API check — is it public? archived? deleted?
   - For books: is the relevant chapter available via the experiment operator?
   - For papers: fetch abstract and check if full text is accessible
   - For websites: fetch and verify content is present (not 404, not behind paywall)
8. **Result:** accessible / restricted / unavailable. Drop unavailable sources immediately.

### Depth Check
9. Does the source contain enough structured domain information for the experiment?
   - Does it have named entities, value objects, or aggregates?
   - Does it have explicit business rules or policies?
   - Does it have state transitions or workflows?
   - Does it have events or commands?
   - Does it have relationships between bounded contexts?
10. Score depth: **deep** (≥4 of the above) / **moderate** (2–3) / **shallow** (0–1).
11. **Drop shallow sources** unless no alternatives exist for that domain.

### Stress Score
12. Rate how well this source exercises the DomainSpec vocabulary:
    - **Meta-type breadth:** How many of the 13 backend meta-types would this domain exercise? (Score: count / 13)
    - **Relationship variety:** How many of the 12 backend edge types would appear? (Score: count / 12)
    - **Complexity tier:** Simple (1 BC), Moderate (2–3 BCs), Complex (4+ BCs)
    - **Interaction density:** Estimated cross-context edges per bounded context pair
13. Compute **stress score** = (meta-type breadth × 0.3) + (relationship variety × 0.3) + (complexity tier × 0.2) + (interaction density × 0.2). Normalize to 0–1.

## Step 4 — Score Diversity

14. For the candidate set, compute diversity across these dimensions:
    - **Industry vertical:** Count distinct industries (finance, healthcare, logistics, retail, etc.)
    - **Domain complexity:** Count sources per complexity tier (simple / moderate / complex)
    - **Documentation type:** Count source categories (A–F) represented
    - **Interaction pattern variety:** Which of the 6 composition patterns would be exercised? (read-reference, write-back, shared ownership, cross-feature trigger, cross-feature enforcement, infrastructure provision)
    - **Geographic/cultural spread:** Any domain-specific regional patterns? (e.g., banking regulations differ by country)

15. Compute **diversity score** for the candidate set:
    - Count distinct industries covered: I
    - Count distinct complexity tiers: T (max 3)
    - Count distinct source categories used: C (max 6)
    - Count composition patterns exercised: P (max 6)
    - Diversity = (I/target_industries × 0.3) + (T/3 × 0.2) + (C/6 × 0.2) + (P/6 × 0.3)

16. If diversity score < 0.6, the source set has **clustering risk** — actively search for sources that fill the gaps.

## Step 5 — Select & Rank

17. For the experiment's required number of sources N:
    - Rank candidates by: stress_score × 0.4 + depth_score × 0.3 + accessibility × 0.2 + diversity_contribution × 0.1
    - Select top N, but **enforce diversity constraints**: no more than 2 sources from the same industry vertical, at least 2 source categories represented.
18. For each selected source, write a **selection rationale**: why this source over alternatives, what unique dimension it adds.
19. Identify **backup sources** (next 2–3 in ranking) in case a primary source fails during execution.

## Step 6 — Produce Source Catalog

20. Create or update `domainspec/docs/research/sources/SOURCE-CATALOG.md` with the master list of all validated sources, scores, and metadata.
21. Create `domainspec/docs/research/sources/EX-sources.md` for the target experiment with:
    - Selected sources (with rationale)
    - Backup sources
    - Diversity analysis
    - Version pins
    - Known limitations

## Step 7 — Pre-Experiment Feasibility Check

22. For each selected source, perform a **mini-extraction test**:
    - Extract 3–5 concepts from the source and classify against TAXONOMY.md meta-types.
    - Extract 2–3 relationships and classify against RELATIONSHIPS.md edge types.
    - Confirm the source produces data that fits the experiment's JSONL schema.
23. If any source fails the mini-extraction (can't produce ≥3 classifiable concepts), replace with backup.
24. Record feasibility results in the experiment's source file.

</process>

<session-learnings>
These are patterns discovered from the E6 + E9 experiment sessions that informed this skill's design:

### What worked well (preserve these patterns):
1. **Multi-tier domain organization** (Tier 1: DDD canonical, Tier 2: system design interview, Tier 3: enterprise SaaS) — created natural diversity.
2. **Star count as credibility signal** for GitHub repos — quick proxy for community validation.
3. **Feature selection guide** (one workflow-heavy + one data-model-heavy per domain) — ensured meta-type breadth per domain.
4. **Cross-experiment dependency tracking** (E6 → E9) — domain specs from E6 directly fed E9 run-2 concept inventories.
5. **Explicit stress descriptors** per domain ("Workflow-heavy, itinerary as Value Object graph") — helped target vocabulary gaps.

### What was missing (this skill fills these gaps):
1. **No formal source discovery step** — domains were selected based on researcher knowledge, not systematic search. Could miss important domains.
2. **No source quality validation** — we cited repos but didn't verify the domain models actually exist in the code. Some sources could be architecture diagrams without domain detail.
3. **No diversity scoring** — diversity was achieved by manual tier organization, not measured. No way to detect clustering.
4. **No prior art survey for benchmarks** — other meta-model papers likely have benchmark domain sets. We should survey what domains they use and ensure our set is at least as diverse.
5. **No version pinning** — if eShopOnContainers changes its domain model, our E9 run-2 data becomes non-reproducible.
6. **No pre-experiment feasibility check** — we didn't validate that enough public information exists for each domain before committing to the full 36-feature analysis.
7. **No backup source identification** — if a source failed mid-experiment, we'd need to re-plan.
8. **No learning loop** — the agent doesn't record which sources produced strong vs weak evidence for future runs.
</session-learnings>

<output-contract>

### Source catalog output:

```
## SOURCE-CATALOG.md — DomainSpec Research Sources

### Source: {source_id}
- Category: A–F
- Domain: {domain}
- URL/Reference: {url}
- Bounded Contexts: {list}
- Depth: deep / moderate / shallow
- Accessibility: public / restricted
- Stress Score: {0–1}
- Version Pin: {SHA / edition / DOI}
- Used In: {experiment IDs}
- Evidence Quality: {strong / moderate / weak} (post-experiment, if available)
```

### Per-experiment source selection:

```
## EX-sources.md — Source Selection for Experiment {EX}

### Requirements
- Sources needed: N
- Source type: {domain models / code / papers / ...}
- Diversity target: {dimensions}

### Selected Sources (ranked)
| # | Source ID | Domain | Category | Stress | Depth | Rationale |
|---|----------|--------|----------|--------|-------|-----------|

### Backup Sources
| # | Source ID | Replaces | Reason |
|---|----------|----------|--------|

### Diversity Analysis
- Industries covered: {N} — {list}
- Complexity tiers: {simple / moderate / complex counts}
- Source categories: {A–F counts}
- Composition patterns exercisable: {N/6}
- Diversity score: {0–1}
- Clustering risks: {identified gaps}

### Feasibility Check Results
| Source ID | Concepts Extracted | Relationships Extracted | Schema Fit | Status |
|-----------|-------------------|----------------------|------------|--------|

### Version Pins
| Source ID | Pin Type | Value | Date Verified |
|-----------|----------|-------|---------------|
```

### Discovery summary output:

```
## Source Discovery — Run Summary
- Experiment: EX
- Candidates discovered: N
- Passed accessibility: N
- Passed depth check: N
- Selected: N (+ M backups)
- Diversity score: {0–1}
- Estimated experiment feasibility: high / medium / low
- Sources requiring operator action: {list, e.g., "need access to BOOK-Vernon-Ch5"}
```

</output-contract>
