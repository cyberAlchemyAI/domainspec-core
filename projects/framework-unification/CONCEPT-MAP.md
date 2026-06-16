---
tags: [framework-unification, concept-map, pipeline, artifacts, schema, residue, two-axis]
node_type: discovery
is_session: false
layer: architecture
nature: explanatory
status: draft
version: 0.1.0
last_updated: 2026-06-16
created_by: victorboscaro@gmail.com
---

# Framework Unification — Concept Map

> **What this node is.** The orientation spine of the workspace: it names the *components,
> artifacts, responsibilities, flows* of the intent→code engine and shows how they fit into
> **two axes** — the **pipeline** (what is produced, in order) and the **three mechanisms** that
> apply to every produced thing (typing, provenance, residue/gate). It is a **map, not a build
> order**, and it decides no owner. Everything operational is OPEN and tracked below.
>
> Grounded in **real code** (submodules `implementation/domainspec` + `arcanum` now initialized —
> closes [discovery OQ-5](discovery/discovery.md)), not description. The aspirational boundary and
> the open-questions rule are governed once by [SCOPE.md](SCOPE.md); this node links there instead
> of restating them.

---

## The engine in one sentence

The engine (internal name **CyberAlchemy / agentic-system**) turns user intent into finished
code while keeping **intent, execution, and evidence mutually traceable**: **DomainSpec** says
*what* is meaningful in the domain, **Arcanum** says *how* the work is done, **Saturn** closes the
loop with *evidence* ([RESEARCH.md §pillars](research/RESEARCH.md#the-three-pillars-from-cyberalchemy)).

---

## The two axes (the core of the map)

The mistake to avoid is reading the three `layers/` folders as three pipeline stages. They are
not. There is **one pipeline** (a horizontal sequence of artifacts) and **three mechanisms** that
cut *vertically* through every artifact in it. The three `layers/` folders are those three
mechanisms.

### Axis 1 — the pipeline (horizontal): intent → code, one artifact per stage

Each stage **produces an artifact** the next **consumes**. Cardinality is many-to-one upstream
(one discovery ← many research; one spec ← many discovery; code ← many specs) — i.e. a **graph of
typed nodes**, not a straight line. The pipe need not run to the end, and it **runs on itself**
(research can refine a define) — confirmed by [`domainspec/TUNING-LOOP.md`](../../implementation/domainspec/TUNING-LOOP.md):
*"every stage is the same process at a different altitude."*

| # | Stage | Artifact(s) produced | Schema today | Real home |
|---|---|---|---|---|
| 0 | **define** (interview) | project-overview, initial-definitions, hypotheses | body sections + `Evidence Type` | partial / `review` |
| 1 | **research** | research.md (raw evidence) | frontmatter + section order | `review` |
| 2 | **findings** | findings.md (synthesis + analysis) | frontmatter + verdict matrix | `review` |
| 3 | **discovery** | discovery.md (design space; **load-bearing**) | mandatory sections + Connections | `review` |
| 3b | **paired-views** | ontology-view · system-view · engineer-view | typed nodes/edges · stance→verdict · decision inventory | `review` / `parser` (ontology by-type) |
| 4 | **plan** | execution plan + task list (dependency-ordered) | prose + task list | **none** |
| 5 | **specs** (+glossary / **domain-dictionary**) | SPEC.md, architecture.md, glossary, aspect files | frontmatter + concept table + typed rows | `review` |
| 6 | **stories** | STORIES.md | classic/BDD + coverage matrix | partial |
| 7 | **tests** | TEST-SPEC.md | derivation rows (source→obligation→type) | `review` (claim ≤ proof) |
| 8 | **implement** | code + code-tags.json + drift report | code contracts + tag schema | **no template** / `script` (tag drift) |
| 9 | **verify** | PASS/FLAG/BLOCK verdict | verdict + details | `script` |
| 10 | **emit-signals** | pipeline-signals.jsonl | **Signal Envelope (JSON, typed)** | `parser` |
| — | **promotion** | promotion verdict | gate criteria P1–P8 | governance |

Sources: [SCHEMA-INVENTORY.md §A](layers/domainspec-language/SCHEMA-INVENTORY.md),
[`domainspec/TUNING-LOOP.md`](../../implementation/domainspec/TUNING-LOOP.md),
[`domainspec/CLAUDE.md`](../../implementation/domainspec/CLAUDE.md) Route 3.

> **Canonical order locked** (owner decision 2026-06-16, OQ-A): `define → research → findings →
> discovery → plan → spec → stories → tests → implement → verify → emit-signals`. Confirmed by the
> built orchestrator ([`domainspec-pipeline` SKILL.md](../../implementation/domainspec/.claude/skills/domainspec-pipeline/SKILL.md):
> Step 1 = plan, Step 2 = spec). It is **composable** — runs in parts and on itself (see "Composability"
> invariant I10). The strongest schemas live at the **ends** (signal envelope; ontology-view by-type
> edges); the two true gaps (**plan**, **implement**) are where typing buys the most.

### Axis 2 — the three mechanisms (vertical): they apply to *every* node

These are the three `layers/` folders, and they are exactly the three requirements you named.

| Requirement (your words) | Mechanism = `layers/` folder | What it guarantees on every node |
|---|---|---|
| "objetos tipados e conectados, tudo por schema" | **representation** — [domainspec-language](layers/domainspec-language/) | the **node envelope** (typed identity + body + connections) + a validator |
| "entender de onde cada coisa surgiu" | **communication** — [dispatch-composition-attack](layers/dispatch-composition-attack/) | every transformation emits a **signal** to an append-only ledger, indexed by `dispatch_id` |
| "o que não tiver no schema é o resíduo, trackeado (por hora com open questions)" | **epistemology** — [cyber-alchemy-lean-fusion](layers/cyber-alchemy-lean-fusion/) | **residue** (what wasn't preserved) + the **claim ≤ proof** gate (`pass/flag/block`) that stops drift |

---

## The object that unifies both axes: the node envelope

Your "schema de todas as coisas relevantes" already has a concrete proposed shape
([SCHEMA-INVENTORY.md §C](layers/domainspec-language/SCHEMA-INVENTORY.md)). One envelope governs
~15 artifacts; only `body` changes per stage:

```yaml
node:
  identity:    { kind, version, status }            # representation
  intent:      <=3 sentences
  connections: [{ to, type: derives-from|cites|implements|supersedes }]  # communication (provenance)
  body:        <stage-profile>                       # the per-stage typed tables
  residue:     [{ claim, status: open|closed, ref }] # epistemology (= your "open questions")
  epistemic:   { grade: observed|stated|hypothesized, proof: <ref|null> }  # claim ≤ proof
```

**Drift becomes mechanically checkable:** a `connection` that doesn't resolve, a `grade: observed`
without `proof`, a closed `residue` without a `ref`. The frontmatter already enforced on every
`.md` in `domainspec` (PreToolUse hook) is the `identity` slice of this envelope made real today.

---

## Two distinct edge catalogs (do not conflate them)

"Tipados e conectados" lives at **two levels**, with **two different catalogs**:

1. **Artifact-provenance edges** — between pipeline nodes: `derives-from`, `cites`, `implements`,
   `supersedes` (the envelope's `connections`; the vault ontology-conventions catalog). This is *how
   a spec traces back to its discoveries and research*.
2. **Domain-concept edges** — *inside* a spec's knowledge graph: the **29 typed edges** of
   [`domainspec/RELATIONSHIPS.md`](../../implementation/domainspec/RELATIONSHIPS.md) (`performs`,
   `produces`, `enforces`, `orchestrates`, …). This is *the content the domain is made of*.

The **ontology-view** is where forbidden edges are made *unconstructible* (typed so no catalog edge
admits the endpoint pair) rather than merely asserted — it is the schema floor for **both** levels
([`domainspec/CLAUDE.md`](../../implementation/domainspec/CLAUDE.md) Route 3, "fourth sibling").
Your **dicionário de negócios** is the term-home of this floor: ontology-view + `domain-dictionary`
skill + `domain_knowledge/` + `arcanum/BUSINESS-ONTOLOGY.md`.

---

## Invariants (what must always hold across the graph)

These are the load-bearing rules — the things a validator (or a human gate) checks to keep the graph
honest. Most are *designed, not yet mechanically enforced* (status noted).

| # | Invariant | Owner mechanism | Enforced today? |
|---|---|---|---|
| **I1** | **Envelope presence** — every node carries `identity + intent + connections` (+ `residue`, `epistemic`). | representation | frontmatter slice only (hook) |
| **I2** | **Connection integrity** — every `connections.to` resolves to a real artifact; no dangling provenance. | representation | `review` |
| **I3** | **Residue honesty** — a residue / open-question marked `closed` must carry a `ref` to its evidence. | epistemology | `review` ([SCOPE §3](SCOPE.md)) |
| **I4** | **Claim ≤ proof** — any `grade: observed` claim carries non-null `proof`; no claim exceeds its evidence. | epistemology | designed (Lean-deferred) |
| **I5** | **Single owner** — each concept/term has exactly one canonical home; no term defined twice, every stance decided once. | paired-views | `review` |
| **I6** | **Contract/schema non-collapse** — a contract declares no types/patterns; every schema `validation_rule` traces to a contract `obligation_id`. | representation | designed (B-1 blocker) |
| **I7** | **Forbidden edges unconstructible** — ontology-view types nodes/edges so a forbidden relation can't be *formed*, not merely asserted. | representation | `parser` (by-type) |
| **I8** | **Append-only signals** — ledgers grow monotonically; signals are never edited or deleted. | communication | built |
| **I9** | **Recursive self-application** — every stage is the same process at a different altitude; the pipe runs on itself. | pipeline | built (convention) |
| **I10** | **Composability** ("não é uma coisa só") — the lifecycle runs in parts: the authoring segment (`define→discovery`) and the build segment (`plan→emit-signals`) run independently; partial runs (`--spec-only`, `--test-only`, `--skip-*`) are first-class. | pipeline | built (orchestrator flags) |

> **Drift = an invariant violated.** That is the whole anti-drift thesis: I2/I4/I3 are exactly the
> "objetos conectados / claim≤proof / resíduo rastreado" you named, made checkable. The residue of
> what no invariant yet covers is itself tracked as Open Questions ([SCOPE §3](SCOPE.md)).

---

## Residue & drift, made operational

The "resíduo" is not just a metaphor — the running engine already emits it as **signals**
([`domainspec/TUNING-LOOP.md`](../../implementation/domainspec/TUNING-LOOP.md)): `alignment-gap`
(code drifted from spec), `spec-gap` (spec insufficient), `governance-gap` (framework blind spot),
plus the ADLC **orphan rate** (code-without-spec / spec-without-code). These signals feed back to
tune the pipeline — the recursive loop. **Your "por hora com open questions" is already the
decided convention** ([SCOPE.md §3](SCOPE.md)): the *operational* residue is an `## Open Questions`
section in every node; the *typed/mechanical* residue is Lean-owned and deferred.

So there are **three residue surfaces** at three maturities: prose Open Questions (now) → typed
signals on runs (built, but the central producer is missing, [OQ-3](discovery/discovery.md)) →
mechanical typed-residue gate (Lean, deferred per [SCOPE.md §1](SCOPE.md)).

---

## Real vs aspirational (status floor)

- **Built / mature:** the frontmatter schema; the `delegation-tuning` + `terminal-guard` +
  `pipeline-signals` ledgers; the dispatch ledger; the DomainSpec constitution; the 29-edge relation
  catalog; the signal/threshold/tuning loop (v1.8.0).
- **Designed, not built:** the node envelope + validator; the central observability **producer**
  ([OQ-3](discovery/discovery.md)); the typed-DAG `v0.5.2` ratification ([OQ-1](discovery/discovery.md));
  PermGuard tool-call gate (binary exists, never wired); the typed-residue gate (Lean, deferred).
- **Knowledge-graph path** (discovery → knowledge node instead of → spec) is **planned, out of
  scope** in real code ([`TUNING-LOOP.md`](../../implementation/domainspec/TUNING-LOOP.md) v2.x) —
  this is the closest existing analogue of your "typed connected objects" vision.

---

## Open Questions

### OQ-A. Canonical stage sequence — RESOLVED.
**Decision (owner, 2026-06-16):** the canonical lifecycle is `define → research → findings →
discovery → plan → spec → stories → tests → implement → verify → emit-signals`, composable (runs in
parts and on itself). This is consistent with the built orchestrator (`domainspec-pipeline` SKILL.md:
Step 1 = plan, Step 2 = spec) and with `domainspec/TUNING-LOOP.md` once `define` is prepended (fixed
2026-06-16). **Residual sub-question:** `domainspec/CLAUDE.md` Route 3 says "Spec → Plan" — that
"plan" is the *implementation* plan (`code.md`, after spec, before implement), a likely **distinct**
concept from the orchestrator's Step-1 execution plan. Decide whether there is **one** plan stage or
**two** (plan-execution before spec, plan-implementation after spec). **Status:** RESOLVED (order);
sub-question OPEN (one plan vs two).

### OQ-B. Are the two edge catalogs reconciled under one type system?
**Context:** provenance edges (envelope `connections`) and domain-concept edges
(`RELATIONSHIPS.md`, 29) are typed independently; the ontology-view sits over both but the
relationship between the two catalogs is unstated. **Recommendation:** decide whether the envelope
validator and the ontology-view share one edge-type registry or stay two. **Status:** OPEN.

### OQ-C. Which is the canonical home of the "dicionário de negócios"?
**Context:** candidates are ontology-view, the `domain-dictionary` skill, `domain_knowledge/`, and
`arcanum/BUSINESS-ONTOLOGY.md` — four homes for one concept. **Recommendation:** single-owner
decision in paired-views, alongside the existing duplicated-owner targets. **Status:** OPEN.

### OQ-D. The collapse-test on the node envelope is unrun.
**Context:** the cheapest proof that the unified typing is real (not a rename) is to map
`discovery` + `engineer-view` + `findings` onto the same envelope without torture
([SCHEMA-INVENTORY.md §D](layers/domainspec-language/SCHEMA-INVENTORY.md)). **Recommendation:** run
it before any validator code. **Status:** OPEN.

### OQ-E. Inherited operational seams.
**Context:** dispatch-composition single-owner ([OQ-1](discovery/discovery.md)), `obligation_id`
bridge owner ([OQ-2](discovery/discovery.md)), observability producer gap
([OQ-3](discovery/discovery.md)). **Recommendation:** these are the paired-views / first-build
targets; this map does not decide them. **Status:** OPEN (carried).

---

## What this map does NOT decide / claim

- Does **not** ratify a canonical stage order (OQ-A) or an owner for any duplicated concept (OQ-E).
- Does **not** claim the node envelope, validator, observability producer, or typed-residue gate
  are built — all are designed/aspirational.
- Does **not** treat the Lean proofs as certifying engine runs, nor PermGuard as security
  ([SCOPE.md §2](SCOPE.md)).

---

## Connections

| Document | Type | Description |
|---|---|---|
| [SCOPE.md](SCOPE.md) | `relates-to` | Governs the aspirational boundary (§2) and the open-questions rule (§3) this map obeys. |
| [discovery/discovery.md](discovery/discovery.md) | `derives-from` | The three-layer decisions and OQ-1..5 this map builds the two-axis frame on top of. |
| [research/RESEARCH.md](research/RESEARCH.md) | `derives-from` | The pillars + pipeline + shared-spine synthesis. |
| [layers/domainspec-language/SCHEMA-INVENTORY.md](layers/domainspec-language/SCHEMA-INVENTORY.md) | `cites` | The artifact/stage inventory and the node envelope (§C). |
| [../../implementation/domainspec/TUNING-LOOP.md](../../implementation/domainspec/TUNING-LOOP.md) | `cites` | Real pipeline order, signal types, recursive self-application. |
| [../../implementation/domainspec/RELATIONSHIPS.md](../../implementation/domainspec/RELATIONSHIPS.md) | `cites` | The 29 domain-concept edges (catalog 2). |
| [../../implementation/domainspec/CLAUDE.md](../../implementation/domainspec/CLAUDE.md) | `cites` | Route 3 pipeline ordering + ontology-view as fourth sibling + domain-dictionary. |
