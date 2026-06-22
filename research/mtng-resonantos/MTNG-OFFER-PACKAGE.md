# MTNG Offer Package — everything we can contribute (NON-SOURCE, local-only)

A single consolidated handoff: **what this repository can offer the MTNG v2
proposal**, in both registers — *implementation* (which of our capabilities help
MTNG get built) and *corpus/substance* (which of our governance concepts deepen
MTNG's own ideas). It is **advisory to an external proposal**, **promotes nothing
into Arcanum**, and obeys **claim ≤ proof**: every recommendation carries an
explicit status, and every concept is defined inline so the package is
**self-contained** — no reader needs access to a private file to use it.

This package consolidates three governed dispatches and the MTNG research tower:

| Source | What it carries |
|---|---|
| [`improvement-map.md`](improvement-map.md) | **Build-help** — repo *skills* mapped to MTNG's 8 gaps (Part 1 below) |
| `offerings-to-mtng.md` (internal) | **Substance-help** source — the governance concepts, now **inlined self-contained** in Part 2 below |
| [`REVIEW.md`](REVIEW.md) | The red-team that produced the 8 consolidated gaps C1–C8 |
| [`definitions.md`](definitions.md) / [`distill.md`](distill.md) | MTNG's own vocabulary (Signal→Mode→Node→Validator→Synthesis) |

> **Two kinds of offer, kept apart.** *Build-help* answers "what helps MTNG ship."
> *Substance-help* answers "what makes MTNG's own thinking deeper." A reader who
> only wants to act should read Part 1 + the Unified First Moves; a reader who
> wants the conceptual backbone should read Part 2.

---

# Part 1 — Implementation offerings (repo capabilities → MTNG's 8 gaps)

MTNG's eight consolidated gaps come from `REVIEW.md` (C1–C8). Each maps to the
single best already-built capability in this repo, with a borrow / adapt / block
verdict.

| Gap | Sev | Best repo capability | Verdict | Concrete adaptation for MTNG |
|-----|-----|----------------------|---------|------------------------------|
| **C1** value prop untested | blocker | `experiment` + `research-evidence-harness` | adapt | Freeze a `criterion.md` (baseline = flat summary+template), build dry-run fixtures + a validator-recall metric, one live run → SURVIVED/FALSIFIED. See contested lever below. |
| **C2** Phase-0 integration unmapped | blocker | `architecture-pattern-inventory` | adapt | *Is* Phase 0: its structure/layer/pattern/testing/observability mappers produce the integration table against the real ResonantOS repo — or its non-mutating gate forces the "declare standalone CLI" fork if the repo is absent. |
| **C3** mode detection unmeasured | major | `research-evidence-harness` | adapt | Pre-register "recall ≥ X on N labelled routing-signature fixtures" (categories fixed before seeing data); compute with the reviewer-rubric calculator. Measure to *falsify*, not to bless substrings. |
| **C4** recombination has no algorithm | major | `residuality-spec` | adapt | Audit §17 for merge-under-failure stressors → desired residue = emit-with-`blocked` section → a `conflicts[]` degradation field. Produces the spec, not the merge predicate (that's an `engineer-view` contract job). |
| **C5** engine authority undefined | major | `engineer-view` | borrow | Author the acceptance policy as a `decision_inventory` (one verdict/stance, RESOLVED/OPEN/CRITICAL, cited authority); pin `actor_ref` to a closed enum via the contracts/enums lane. |
| **C6** apparatus over-scoped | minor | `implementation-layering` | adapt | Value/cost layering: L0 = the 3 kept artifacts (issue-packet + validator-report + audit-log) as the minimum-working-unit; defer contribution-records + OKF until a named consumer exists. |
| **C7** overhead unbudgeted | minor | `research-evidence-harness` | adapt | Add a `RunProfile.budget` field (no-unlimited-default, the `dispatch-spec` discipline); the harness's calculators measure per-signal cost against it. |
| **C8** node-schema drift / OKF | minor | `definitions-governance` | borrow | Make one canonical BranchNode the canonical source; run the drift audit to fix §14/§22/§23 contradictions. OKF half needs the external spec (not in repo). |

**Contested lever — C1.** Two of our skills both claim "primary": `experiment`
(freeze the criterion) vs `research-evidence-harness` (build the harness +
measure). They collapse to the **same ordered pair**: (1) freeze the criterion
first — cheap, irreversible-by-policy so the yardstick can't be bent; (2) build
the harness to feed it; (3) run once, live. **Until that run exists, C1 stays a
blocker** — neither freezing nor building, alone, discharges it.

**Where repo reuse does NOT help (build side):** C2 if the ResonantOS repo is
absent (no codebase to map); the OKF half of C8 (needs the external spec);
whether C6's trim is *sufficient* (a product decision, only sequenced); and the
dispatch-tension skills (`check-tension`/`anti-bias`/`register-dispatch`) are
empty for a single-developer, no-fan-out tool.

---

# Part 2 — Corpus / substance offerings (what deepens MTNG's own ideas)

**The headline.** MTNG is structurally *our own pattern* — intent-vs-reality
drift; audit the translation; account what's left over (the same shape as
Saturn). Our **v2 governance ontology** lands directly on MTNG's biggest open
dependency — the **promotion / authority lane**: Phase-0, "engine accepts per
policy", and what gets promoted and by whom.

## Governance offerings (definitions, self-contained)

Each concept below is **handed over in full** — the actual model content, not a
pointer to a private file. These come from our CyberAlchemy-v2 governance
ontology; unless marked *active*, each is a **candidate** concept (a reviewable
model, not promoted authority). MTNG can adopt the *shape*; it does not inherit a
finished engine.

### G1 · Authority Kinds → MTNG's `actor_ref` / output typing
**Definition.** A way to classify *what sort of authority* an artifact carries, to
route review — **not** a content tag and not a "canonical" marker. Each kind
records: `kind_id`, `label`, `owner_route` (who owns promotion),
`authority_surface` (where it counts if promoted), `candidate_inputs`, and
**`forbidden_collapse`** (what it must not be confused with). Candidate kinds
include `kind.definition`, `kind.constitution`, `kind.decision`, `kind.spec`,
`kind.runtime_contract`, `kind.projection`, **`kind.evidence`** (*"not authority by
itself"*), and **`kind.residue`** (*"not defect by default"*).
**Offers MTNG.** A type for `actor_ref` / each node output by *what governs it*,
plus the `forbidden_collapse` discipline MTNG's contribution records gesture at but
never state (evidence ≠ authority, residue ≠ defect). **Use rule:** kinds *route* a
candidate to an owner; they do not *decide* it. — **candidate**

### G2 · Authority Postures → MTNG's "memory candidate is review-only"
**Definition.** A description of *how* a source/candidate/artifact may be relied on
— "reviewable model concepts, not tags that grant trust." Each posture records
`allowed_use` and `blocked_use`. Examples: `posture.evidence` (allowed: *support
candidates and gates*; blocked: *replace owner decision*); `posture.research`
(allowed: *support design and review*; blocked: *become spec/definition
automatically*); `posture.generated` (allowed: *navigation after trace*; blocked:
*canonical source*). **Confidence boundary:** *"posture is not confidence —
confidence records strength; posture records allowed reliance and boundary."*
**Offers MTNG.** A vocabulary that generalizes "memory candidate, review-only" into
typed `allowed_use`/`blocked_use` postures plus a Public/Private rule; *"posture is
not confidence"* directly mirrors MTNG's defer-valuation move. — **candidate**

### G3 · Lifecycle + Typed-Hole Rule → MTNG's `closed_result`
**Definition.** Separate the axes MTNG conflates in `closed_result`:
*workflow-state* (review/promotion flow) vs *maturity status* vs *promotion
verdict* (pass / flag / block / defer / reject / supersede) vs *projection state*
(read model). The **Typed-Hole Rule** is the load-bearing piece:
```text
shared rail → owner profile → verdict
```
The shared envelope (the "rail") may carry status, sources, conflicts, drift owner,
refs — but the **verdict hole is filled only by the owner profile**; the
representation layer "must not fill the verdict hole." A **Multi-Provenance Rule**
adds: many sources may support one artifact; the owner decides canonical synthesis;
the model only *shows the support graph and residue*.
**Offers MTNG.** The node contract is a **rail** carrying status/sources/conflicts;
the pass/fail **verdict** is filled by a *separate owner profile* — sharpening
MTNG's validator-vs-synthesis split, and giving synthesis (DEF-5) a rule: show the
support graph, don't let the recombiner hold authority. — **candidate** (live
schema deferred by design)

### G4 · Node Model + status axis → MTNG's node contract
**Definition.** Every node concept records a **`concept_role`** ∈ {authority,
evidence, workflow, projection, **residue**} plus a per-node **`forbidden_collapse`**.
E.g. `concept.promotion_record` is *"not the authority artifact it approves"*;
**`concept.residue`** is a first-class role, *"not proof of novelty or automatic
promotion."* The **Node Status Axis** rule: a node's workflow `candidate_status`
**must not collapse into** maturity status.
**Offers MTNG.** Type each node by its *governance role* (not just its I/O) and
state what it must not be confused with; make **workflow state ≠ maturity status**
explicit; adopt **residue as a first-class node role** — a concept MTNG currently
lacks. — **candidate** (gate = flag: live `node_type` changes are schema work)

### G5 · Branch As View → MTNG's branch / synthesis
**Definition.** *"A branch is an interpretive view over cited artifacts and
evidence — not a canonical branch, vault node type, lifecycle state, schema
namespace, or promotion route by itself."* Each branch records a `view_role`
(meaning / system / bridge / evidence / projection / promotion-staging),
`allowed_readings`, `forbidden_authority_moves`, and `residue`. **Forbidden
collapses:** branch membership → promotion state; branch view → node type; bridge
branch → movement edge. **Use rule:** *"use branch views to ask better questions;
do not use them to answer authority questions without an owner gate."*
**Offers MTNG.** The discipline its DEF-1 ("a graph, not a tree") never states: a
branch is a **reinterpretation under a contract, not a forked copy**, and
**branching confers no authority** — deepening the branch-only-on-named-boundary
invariant (DEF-3). — **candidate**

### G6 · Relation Model → MTNG's recombine / synthesis edges
**Definition.** Every relation declares an **`authority_effect`** ∈ {none, staging,
projection, owner-decision, blocked} — so an edge says whether it *moves authority*.
Allowed candidate relations include `requests_promotion_gate` (staging, *"not a
verdict"*), `decides_transition` (owner-decision → a PromotionRecord-compatible
record), `emits_projection_when_allowed`, and `records_residue`. **Boundary to
flag, not solve:** the movement relations `witnesses_authority_movement` and
`promotion_movement_edge` (node → `PromotionRecord`) are **schema-evolution-only —
not allowed as live edges** until schema governance + an append-only
authority-ledger validator exist. That is the **KILL-until-amendment** boundary in
v2 itself.
**Offers MTNG.** Make every recombine/synthesis edge **declare if it moves
authority**; stage promotion as *request → owner-decision → projection-when-allowed*
(the precise shape of MTNG's "engine accepts per policy" question) — and inherit the
honest open boundary rather than a faked mechanism. — **candidate** (movement edges
OPEN / blocked-by-design)

### G7 · Promotion Ladder → MTNG's memory / contribution promotion
**Definition.** A 7-rung ladder — **Source evidence → Inventory candidate →
Ontology candidate → Local authority → Implemented behavior → Stable asset →
Extraction** — where each rung names what it *may* promote to, with a **per-rung
owner gate** (definitions-governance, decision-gate, task-session, …) and a **Pass /
Flag / Block** verdict (Block = "promotion must stop until a decision, evidence, or
validation gap is closed"). Core stance: *"promotes evidence by owner route, not by
enthusiasm."*
**Offers MTNG.** A concrete ladder + gate-per-rung for "memory candidate,
review-only" and contribution-record promotion — which MTNG names but never
structures; the owner-route stance is a direct donor to MTNG's
capture-don't-score discipline. — **ladder shape owned-and-defined; the extraction
threshold is OPEN**

### G8 · Source-vs-Read-Model boundary → MTNG's synthesis / memory candidates
**Definition.** *"Raw sources remain the highest evidence for their own claims.
Inventory pages, evidence cards, ontology maps, **memory summaries**, sessions, and
observability signals are read models … they help search and context selection.
They do not promote themselves."* Plus generated-vs-canonical: generated surfaces
are projections whose canonical source *"must be traced before they influence a
capability contract."*
**Offers MTNG.** The cleanest statement of MTNG's central worry: a synthesis/memory
candidate is a **READ MODEL, not a promotion**, and a generated output must trace to
its source before it can influence anything. This is the **one active, non-candidate
rule** in the set. — **active boundary rule**

### G9 · Source-ledgered amalgamation + ingest contract → MTNG's synthesis provenance
**Definition.** *"Amalgamation by governance, not by copying — source systems stay
in their homes."* The ingest rule: **"every imported claim must cite a source path
or be labeled synthesis, inference, or open question."**
**Offers MTNG.** A ready-made provenance contract for MTNG synthesis (DEF-5's
"honest dossier"): a recombined artifact's every claim must cite its source or be
explicitly labeled inference/open-question. — **owned method; the discipline card
itself is a candidate**

---

# Unified first moves (both lanes, cheapest-leverage first)

1. **Freeze C1's `criterion.md`** (`experiment`) — gates everything that claims
   value; baseline = disciplined flat summary + issue template.
2. **Pick the canonical BranchNode + run the drift audit** (C8,
   `definitions-governance`) — removes the §14/§22/§23 contradictions.
3. **Offer the v2 promotion ladder + source-vs-read-model** (`promotion-policy.md`,
   `boundaries.md`) onto MTNG's promotion gap — the two most-grounded governance
   assets.
4. **Author the engine-policy `decision_inventory` + `actor_ref` enum** (C5,
   `engineer-view`).
5. **Layer the 8 artifacts** (C6, `implementation-layering`) to L0's three.
6. **Build the C1 harness and run once** (`research-evidence-harness`) — renders
   C1's verdict and produces C3 accuracy + C7 cost in one pass.
7. **Map the integration surface** (C2, `architecture-pattern-inventory`) — once
   the ResonantOS repo is in hand.
8. **Residue-audit §17 for C4** (`residuality-spec`).

---

# Honest boundaries (claim ≤ proof)

- **Nearly every governance concept (G1–G9) is `candidate`**; the one active rule
  is source-vs-read-model (G8). The node→`PromotionRecord` movement edge is
  KILL-until-amendment in v2 itself (G6). The governance offerings are candidate
  scaffolding + forbidden-collapse discipline, not a finished promotion engine.
- **External blockers this repo cannot supply:** the ResonantOS codebase (C2) and
  the OKF spec (C8 OKF half).
- **This package promotes nothing into Arcanum.** BRIDGE-layer, NON-SOURCE,
  local-only, advisory to an external proposal. Part 1 capabilities carry their
  public-or-local surface; Part 2 concepts are defined inline, self-contained.

---

# Appendix A — Definitions of the Arcanum capabilities cited above

So the package is self-contained: each capability named in Part 1 (and the
unified moves) defined in one line. **Public** ones are reusable Arcanum sigils —
indexed at `arcanum/registry/SIGILS.md`, full instructions in the folder shown
(the Arcanum submodule is public). **Local** ones are domainspec dispatch/authoring
skills not in the public registry; their definition here is the whole surface.

| Capability | What it does (one line) | Surface |
|---|---|---|
| **experiment** | Pre-registers a *falsifiable* success/failure criterion, frozen **before** any run (a designer authors it, a skeptic validity-checks it); verdict vocabulary SURVIVED / FALSIFIED / INVALID. The criterion's immutability is the point — no moving the goalposts. | **local** (domainspec dispatch skill). Public run-mechanics analog = *Experiment Harness*, `arcanum/arcana/experiment-harness/`. |
| **research-evidence-harness** | Turns a protocol into a validated run schema + append-only JSONL fixtures + objective/metric calculators, requires a **dry-run before any live run**, and holds an *evidence-status guard* that blocks upgrading a claim from synthetic fixture data. | **local** (domainspec skill). |
| **architecture-pattern-inventory** | Maps a repository's architecture into a reusable pattern-inventory package (concept cards, dependency rules, testing + observability alignment), keeping *observed* separate from *recommended*. | **public sigil** → `arcanum/arcana/architecture-pattern-inventory/` |
| **residuality-spec** | Hardens a spec by stressor analysis → *desired residue* (what must survive / may degrade / may stop) → attractor discovery → concrete degradation-behavior spec lines. | **public sigil** → `arcanum/arcana/residuality-spec/` |
| **engineer-view** | Authors the mechanics-and-verdicts view of a target: a `decision_inventory` (one verdict per stance, RESOLVED/OPEN/CRITICAL + cited authority) and a `contracts` lane (schemas, record fields, enums, failure-code families). Half of the ontology/system/engineer **paired-views** triad, under single-owner discipline (each term/stance defined once, decided once). | **local** (domainspec authoring skill). |
| **implementation-layering** | Turns an implementation goal into staged layers, from the smallest useful proof (minimum working unit) through value/cost-gated hardening. | **public sigil** → `arcanum/transmutations/implementation-layering/` |
| **definitions-governance** | Maintains canonical definitions with a single *canonical source*, synchronized indexes, and a *drift audit* (conflicting wording, stale anchors, undefined terms, narrative that redefines authority) that emits remediation items with target files. | **public sigil** → `arcanum/arcana/definitions-governance/` |
| **decision-gate** | Resolves blocker-level multi-option decisions before consequential work continues, persisting a reusable record (question / options / selected / rationale / source / timestamp) with a Pass / Flag / Block verdict. | **public sigil** → `arcanum/arcana/decision-gate/` |
| **dispatch-spec** (discipline) | Validates/designs a dispatch route; cited here only for its `token_budget` "no-unlimited-default" discipline (every step declares a cost ceiling). | **public** (Arcanum dispatch-spec, used by the `goal` spell). |

> **Part 2 (governance) concepts** — Authority Kinds/Postures, the Typed-Hole
> Rule, Node Model, Branch-As-View, Relation Model, the Promotion Ladder, and
> source-vs-read-model — are **defined in full inline** as G1–G9 (the actual model
> content, not a path). They are **candidate** governance concepts of private
> origin, handed over here as definitions rather than pointed at any file — so the
> package needs no access to a private repo to be used.

---

# Provenance

| Dispatch | Type | Outcome | Produced |
|---|---|---|---|
| `2026-06-22-mtng-v2-review` | review | resolved | `REVIEW.md` (8 gaps C1–C8) |
| `2026-06-22-mtng-improvement-sweep` | research | resolved | `improvement-map.md` (Part 1) |
| `2026-06-22-mtng-owned-concept-offerings` | research | resolved | `offerings-to-mtng.md` (Part 2) |

All three: check-tension PASS/PASS, human-confirmed, P8-verified. Rows in
`telemetry/agents/subagents-dispatch.yaml`. This package presents the
**implementation** and **governance** offerings only; it carries no formal/proof
content.
