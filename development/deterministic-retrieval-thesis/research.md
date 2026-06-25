# research.md — collected Lane-Z explorer returns (verbatim)

Dispatch `2026-06-24-deterministic-retrieval-thesis` (research). Three Lane-Z explorers,
each deepening one leg AND running its own counterexample (Lane-Z honesty).
Cited synthesis + Lane-A adjudication is in findings.md.

---

## (file: Z1-typed-intent-discrete-vector.md)

# Lane Z / Explorer Z1 — TYPED-INTENT / DISCRETE-VECTOR

Dispatch: `2026-06-24-deterministic-retrieval-thesis`. Role: explorer. Leg: typed
intent gives each agent a *discrete vector* start point. This is the verbatim
return value.

## The claim, deepened

The thesis' three legs are (1) typed-intent → discrete vector, (2)
ingest-relocation, (3) governance-determinism. Z1 argues leg 1 is the **keystone**:
it is the only one that produces an *entry point* into the ontology that is cheap
because it is already-typed and already-linked.

The DomainSpec move is to refuse the implicit spec→code mapping. The seed states it
plainly: "The mapping from spec to code is implicit, so implementation agents are
expensive and drift-prone" (`spec-ontology-unification/SEED.md:8-12`). An implicit
mapping forces the agent to *reconstruct* the link at query time — which is exactly
the retrieval problem (embed the query, nearest-neighbor over a code corpus, hope
the grounding is right). The seed's hypothesis removes the reconstruction step:
spec and ontology are "the same object in two forms" (`SEED.md:16`), where "A
**node maps to a code pattern**; an **edge maps to a composition rule**"
(`SEED.md:21-22`).

The deepened claim is about *what the agent receives*. In a RAG world the query is
an untyped string and the system must guess its neighborhood. In DomainSpec the
query arrives as a **node already sitting in a typed graph**. The agent does not
search for its start point — it *is handed* one. That handed-over object is the
discrete vector: not a continuous embedding the model has to denoise, but a small
enumerable subgraph (the node + its typed in/out edges). The seed names this
directly: ephemeral agents whose "system-prompt constitution is the architecture +
code patterns; their context is the spec subgraph" (`SEED.md:23-27`). The spec
subgraph *is* the seed — node→pattern tells the agent which code shape to emit, and
the edges tell it how to compose with neighbors.

**Why keystone.** Strip leg 1 and the other two collapse. Ingest-relocation (leg 2)
only buys economy if there is a discrete address to relocate *to*; without a typed
node as the landing site, relocated context is still dumped as undifferentiated
prose and you are back to stuffing a prompt. Governance-determinism (leg 3) can
only be deterministic over a *closed, enumerable* surface — a typed node with a
finite edge set is checkable (`enforces-cross` either resolves to a real target or
it does not); an embedding neighborhood is not, because "did we retrieve the right
chunk" has no ground truth. So leg 1 supplies the discrete substrate the other two
*operate on*. Ontology traversal with no typed seed has no economical entry: you
would have to embed-and-search to find where to begin, which re-imports the cost the
thesis claims to remove. Hence keystone, not merely first-among-equals.

## Precedent — honest verdict: build-from-owned, novelty demoted

This is **build-from-owned** of the `spec-ontology-unification` tower, not net-new.
The owner exists and is explicit:

- The node→pattern / edge→composition model is *stated* at `SEED.md:18-22`.
- The ephemeral-bounded-agent framing ("their context is the spec subgraph") is
  *stated* at `SEED.md:23-27`.
- The typed-graph substrate it leans on is **already real in v1**, which the seed
  flags as its primary evidence source: confirm the spec "already has nodes, edges,
  and cross-feature edges" (`SEED.md:34-36`). My skim confirms it:
  `implementation/domainspec/TAXONOMY.md` enumerates the node types (Entity,
  Operation, Query, Rule, Event, Mapping, Workflow — `TAXONOMY.md:11-23`), and
  `implementation/domainspec/RELATIONSHIPS.md` enumerates 29 typed edges including
  the **cross-feature** ones: `produces-for` Operation@A→Entity@B,
  `triggers-cross` Event@A→Operation@B, `enforces-cross` Rule@A→Operation@B
  (`RELATIONSHIPS.md:15-17`, detailed `RELATIONSHIPS.md:75-100`).

So the discrete-vector framing does not invent the substrate; it *re-describes an
existing typed graph as a retrieval seed*. The contribution Z1 can honestly claim is
narrow: the **reframing** that the already-typed query is what makes ontology
traversal economical — i.e. positioning leg 1 as the keystone of a retrieval thesis.
The graph itself, the node/edge types, and the ephemeral-agent idea are all owned by
the seed and by v1. Per the precedent-sweep rule, a found owner is a build-from-owned
**win**, but it **demotes any novelty claim**: do not market "discrete vector start
point" as a new mechanism. It is a new *lens* on `SEED.md:16-27` + v1's
`RELATIONSHIPS.md`. The strongest defensible sentence is: "DomainSpec's existing
typed graph, when read as a retrieval substrate, gives each bounded agent a discrete
typed seed instead of an embedding neighborhood." Everything past that is borrowed.

## MANDATORY counterexample (Lane Z honesty)

Take the seed's own open residue verbatim: "What carries cross-feature context into
a bounded agent without leaking the whole graph into its prompt?"
(`SEED.md:68-70`). And the seed's own Lane Z attack instruction: "what breaks when a
pattern needs cross-cutting context the subgraph doesn't carry?" (`SEED.md:46-47`).

**The counterexample I actually hit.** Consider implementing the Operation
`GenerateSettlement`. Its node is discrete. But `RELATIONSHIPS.md:77` says
`GenerateSettlement` **produces-for** `Player` (bankroll/makeup updates) — a foreign
entity owned by another feature. To emit correct code the agent must know Player's
shape, its invariants, and possibly the rules that gate writes to it. Following one
`enforces-cross` edge (`KYCVerificationRule enforces-cross OpenAccount`,
`RELATIONSHIPS.md:97`) drags in a Rule node from a *different* feature, which itself
has `enforces`/`calculates` edges, whose targets have further edges. Transitive
closure over cross-feature edges does not obviously terminate before it has pulled in
a large fraction of the graph. If the agent must expand the closure to ground its
output, the "discrete vector" has silently re-inflated into the whole-graph dump —
**which is precisely the RAG/grounding problem leg 1 claims to delete.** The discrete
seed becomes discrete-in-name-only.

**Where the leg HOLDS.** The leak is bounded *if and only if* cross-feature edges are
**typed, named, single-target, and the foreign node exposes a contract, not its
body.** The evidence is encouraging here: every cross-feature edge in v1 is a named
edge resolving to exactly one foreign node, with a registry query that returns that
one target — `produces-for` answers "*Which* foreign entity does {Operation}
update?" (singular, `RELATIONSHIPS.md:82`); `triggers-cross` answers "*Which*
operation is activated…" (`RELATIONSHIPS.md:91`); `enforces-cross` answers "*Which*
external rule gates {Operation}?" (`RELATIONSHIPS.md:100`). So the agent does not
need Player's whole subgraph — it needs Player's *node contract* (its code pattern's
public shape) plus the *name* of the gating rule. The edge carries a pointer, not a
payload. Under that discipline the seed for `GenerateSettlement` is: its own node +
N typed edges + the *contracts* (not bodies) of the ≤N foreign nodes those edges
name. That stays discrete and enumerable.

**Where the leg BREAKS.** It breaks the moment the foreign node's *contract is not
sufficient* and the agent needs the foreign node's *internals* to be correct — i.e.
when node→pattern is **not 1:1**, the exact failure the seed told Lane Z to hunt
("where does node↔pattern fail to be 1:1?", `SEED.md:46`). Three concrete break
points: (a) an invariant of Player that is enforced *inside* Player's operations, not
expressed as a crossing Rule node — the writing agent can violate it because the edge
never surfaced it; (b) transitive cross-cutting concerns (a `calculates` chain behind
the foreign rule) where one hop is insufficient and two hops re-open closure growth;
(c) shared mutable state where correctness depends on *ordering* across features,
which no single edge encodes (this is exactly the seam the seed flags as overlapping
`dcb-correctness`, `SEED.md:71-72`, and the test-engine HANDOFF re-flags as G2
read-set/freshness, `test-engine/HANDOFF.md:43,87-89`).

So the honest verdict: the discrete vector **stays discrete only under a contract
boundary on foreign nodes** — the edge must carry a typed pointer to a node that is
sufficient at its public contract. That is a real, falsifiable design obligation, not
a given. Where features have clean contracts the leg holds and retrieval is genuinely
a one-hop typed lookup, beating embedding search. Where a foreign node's correctness
leaks through its contract (hidden invariants, ordering, deep calculation chains) the
closure re-expands and leg 1's economy degrades toward the RAG cost it claimed to
remove. The leg is not false; it is **conditional on contract-completeness of nodes**,
and that condition is unproven — it is the seed's own open residue (`SEED.md:68-70`)
and overlaps the unresolved dcb seam.

## Net for the synthesis

- Leg 1 is the keystone: it is the only leg producing an economical typed entry
  point; legs 2 and 3 have no discrete substrate to act on without it. Keep this
  framing.
- Provenance honesty: build-from-owned of `spec-ontology-unification` (`SEED.md:16-27`)
  over v1's real typed graph (`TAXONOMY.md:11-23`, `RELATIONSHIPS.md:15-17,75-100`).
  Novelty claim demoted to the *reframing*, not the mechanism.
- Counterexample is real and unresolved: discreteness survives **only** under a
  node-contract boundary on cross-feature edges. Recommended bridge decision:
  `borrow-carefully` — adopt the discrete-seed framing but make
  "foreign nodes are referenced by contract, not by subgraph" an explicit
  promotion-blocking obligation, and route the leak-closure question to whoever owns
  the dcb-correctness seam (`SEED.md:71-72`, `test-engine/HANDOFF.md:G2`).

---

## (file: lane-Z2-ingest-cost-relocation.md)

---
lane: Z
explorer: Z2
leg: INGEST-TIME COST RELOCATION
methodology: adversarial cost-accounting
date: 2026-06-24
dispatch: 2026-06-24-deterministic-retrieval-thesis
corpus:
  - "Agent Memory Architecture v7.1" (PDF, 11pp; read via E2 page-by-page return in development/resonantos-integration/research.md:85-116)
  - development/cyberalchemy-integration-sdk/findings.md
  - development/resonantos-integration/findings.md
status: explorer return (verbatim — collected into research.md)
---

# Lane Z2 — The cheap deterministic read is PURCHASED, not free. Who pays, and is the bill bounded?

## 0. The leg in one line

The thesis ("deterministic, sub-50ms, no-LLM reads") does not *eliminate* semantic
comprehension cost — it **relocates** it from query-time to ingest-time. The fast read
loop is cheap only because a slow, model-heavy, *governed* write loop already paid the
comprehension bill and left behind typed nodes/edges the reader can traverse without
thinking. The PDF makes this split structural and non-negotiable: retrieval is "fast,
deterministic, no neural models… only one GPU call per query… everything before Bonsai
is CPU/disk" (v7.1 p.2, p.5; research.md:90), while every neural model — REPLAY's MoE
SSM (Mamba-class), JEPA re-scoring, the Bonsai 8B ternary verifier — runs ONLY in the
async slow loop, per ingestion event (p.1, p.4, p.6–7; research.md:90,102). **The read is
no-LLM precisely because the write was all-LLM.**

So the load-bearing question the other two legs assume away: **what is the purchase price
of a cheap read, and is that price BOUNDED?** This leg accounts for it adversarially.

## 1. EXACTLY what CyberAlchemy must do at governed write-time to earn a cheap read

The PDF's substrate already pays the *fact*-comprehension half (extraction into typed
edges, contradiction resolution, validity windows). CyberAlchemy's claim is to add the
*authority*-comprehension half on top of the slow loop's write step (resonantos
findings.md §3; research.md:91,116). Spell out the full ingest-time bill — the work that
must complete BEFORE any deterministic read can be cheap:

1. **Extraction into typed nodes/edges.** Raw capture → typed directed edges with
   required properties enforced by a GraphQL schema (v7.1 p.3; research.md:94). This is
   GLiNER2/tree-sitter-class neural extraction in the write loop — the comprehension that
   the reader skips. *Cost:* one model pass per ingest event (~25–90ms, p.1/p.6,
   research.md:90), and it must produce schema-valid output or the read finds nothing.
2. **Scope-tagging.** Every captured record MUST be stamped with exactly one scope tag
   (`user-memory` / `project-instructions` / `runtime-rules` / `knowledge-store`) at the
   capture port; "one port may span all four only by tagging scope, never by melting them"
   (cyberalchemy findings.md §4). A mis-tag is a silent authority error — a `user-memory`
   capture that leaks to `knowledge-store` short-circuits authority on capture alone,
   which §4 forbids. *Cost:* a classification decision per record, and it is NOT free —
   it is exactly the "does writing here govern future work?" comprehension.
3. **Promotion / governance metadata.** The write must land the CAV2 b2 overlay:
   `promotion_owner`, `promotion_trace`, `residue`, `status: candidate`, and the
   kind/status enums (cyberalchemy findings.md §2,§8; inventory SKILL.md:160-194). The
   PDF substrate has NO field for any of this — "no `authority_kind`, `decision_id`,
   `promotion_stage`, `owner`" (v7.1 p.3; research.md:95). CyberAlchemy must *write the
   authority dimension the substrate has no column for* (research.md:116). *Cost:* a
   governed decision (authority-triage front door, the needs-authority test) per
   promotable candidate, plus an owner-routed gated review (the Review Queue / D48 / D49;
   resonantos findings.md §2). This is human-in-the-loop by design — the G4 gate default
   is "human reviews the diff" (cyberalchemy findings.md §2). **The read is cheap because
   a human (or a gated owner) already adjudicated authority at write-time.**
4. **Provenance.** sha256-stamped `.metadata.json` per intake record, `INTAKE/review-queue/`
   request records stamped `trustedKnowledgeWrite:false, requiresStrategistOwnedIngest:true`
   (resonantos research.md:60-61; findings.md §2 row 2). *Cost:* provenance capture is
   mechanical and bounded — this is the cheapest line item.
5. **Ontology maintenance.** The typed graph the reader traverses must STAY coherent:
   contradiction resolution (LUCID DREAM: supersede/merge/annotate via Bonsai 8B, v7.1
   p.7; research.md:102), utility-thresholded pruning/merge of redundant facts (p.7),
   stale-edge flagging (`validity_end < now`, p.7), JEPA re-scoring of replayed traces
   (p.4). On the authority side, CyberAlchemy adds: keeping Authority Kinds, the
   Narrowest-Owner routing, and the promotion lifecycle vocabulary in sync as the domain
   grows (resonantos findings.md §4; research.md:133-134). *Cost:* this is the recurring,
   open-ended line — see §3.

**The BET, stated sharply:** items 1–4 are per-ingest costs that are *amortized* — you pay
once at write, then every future read is free. That amortization is the whole thesis. The
deterministic read is *purchased* at write-time, and the price is real engineering: a
model pass, a classification, a gated human decision, a provenance stamp. The other two
legs (assume the read is "just there") **assume this purchase already happened and never
price it.** Z2's claim: the ingest leg is load-bearing because *if the purchase is too
expensive or never bounded, the cheap read is a cheap read of an empty or rotten graph.*

## 2. Where the relocation PAYS OFF (the bet wins)

Relocation is a genuine win — not a shell game — under three conditions the corpus supports:

- **Read/write ratio is high.** Pay comprehension once per fact; read it thousands of
  times. The PDF's two-loop split exists precisely to exploit this asymmetry — the
  invariant "only one GPU call per query, everything before Bonsai is CPU/disk" (p.2,p.5)
  is only worth enforcing if reads vastly outnumber writes. For a knowledge store this
  holds. **Win.**
- **The comprehension is STABLE once paid.** A fact's typed edges and authority tag don't
  need re-deriving on every read. Provenance (item 4) and a promoted authority record are
  write-once. **Win** — and this is the part RAG cannot match: RAG re-pays semantic
  retrieval cost on *every* query because it never commits a typed, governed result.
- **Authority is genuinely orthogonal to fact-validity.** The relocation pays off *most*
  on the authority dimension because the substrate has no field for it at all
  (research.md:115-116) — there is nothing to re-derive at read-time because the answer
  ("is this canonical / promoted / who decided?") was *written down as data* by the gated
  decision. A deterministic read of `promotion_stage` is a column lookup, not a judgment.
  **Win, and it is the cleanest win** — authority is the one axis where write-time
  relocation is provably complete, because authority is a decision (a fact-about-a-fact),
  and decisions, once made, are static.

## 3. RUN THE COUNTEREXAMPLE (mandatory Lane Z honesty) — is the write-time cost UNBOUNDED?

The accusation against my own leg: **I have not removed the RAG/comprehension problem; I
have MOVED it to write-time. If the write-time + ontology-maintenance cost is unbounded,
the relocation is an accounting trick — the bill is the same, just paid at a different
desk.** Press on every seam where the cost fails to amortize:

### 3a. Messy real-world inputs — the PDF's own §10.3 synthetic-vs-real caveat
The PDF's clean ~25–90ms write cost and its tidy contradiction-resolution numbers are
measured on **synthetic** corpora. The §10.3 synthetic-vs-real caveat is the PDF
confessing its own evaluation gap: real ingest is dirtier than the benchmark. Two
corroborating tells in the corpus: the "I don't know" percolation threshold is
"empirically learned… domain-dependent" (p.11; research.md:106) — i.e. NOT a fixed
constant, it must be *re-tuned per domain*, which is unpriced write-time labor. And the
extraction step's cost is bounded only if inputs are clean enough for one model pass to
yield schema-valid edges. On messy real input, extraction *fails or mis-types*, which
either (a) drops the fact (read finds nothing — the cheap read is cheap because it returns
nothing) or (b) writes a malformed edge that the reader faithfully, deterministically,
**returns wrong**. **The relocation does NOT remove the comprehension problem here — it
moves it to write-time AND makes its failures silent at read-time.** Determinism is not
correctness: a deterministic read of a mis-extracted graph is reliably wrong.

### 3b. Non-1:1 node→pattern mapping
The bet assumes each fact maps to a stable typed node the reader can address. Real
knowledge is not 1:1: one source statement may shatter into many edges, or many statements
may collapse to one; the same real-world entity may surface under different node
identities across ingests. The PDF *acknowledges* this is hard work, not free — PRUNING
must "merge redundant facts" and "remove orphans" (p.7; research.md:102), and LUCID DREAM
must adjudicate "two documents claim X and not-X" (research.md:103). That merge/dedup IS
the non-1:1 problem, and it runs **a model (Bonsai 8B) per contradiction at write-time**
(p.4,7). So the mapping cost is real and model-priced. **Where it blows up:** merge/dedup
is not a one-time cost — every *new* ingest can create a contradiction with an *old* fact,
so the write cost of fact N is O(its interactions with the existing graph), not O(1). The
amortization assumption (§1: "pay once per fact") **leaks**: you pay once to *write* fact
N, but you may re-pay to *reconcile* facts 1..N-1 against it. The bill is super-linear in
the worst case, not constant.

### 3c. Schema / ontology drift over time
The deterministic read is cheap *only against a fixed schema*. The GraphQL schema "enforces
node/edge types and required properties" (p.3) and CyberAlchemy's authority overlay pins
Authority Kinds, kind/status enums, and the scope-tag vocabulary (cyberalchemy findings.md
§4,§8). The moment the domain needs a *new* authority kind or a *new* scope, the schema
changes — and CAV2's own default-deny posture (D49) **forces** this: "unenumerated kinds
stay blocked until a decision adds them" (resonantos findings.md §3.B; research.md:143).
That is a feature for safety and a *cost engine* for maintenance: every genuinely novel
authority shape requires a governed schema-evolution decision. **The ontology is not
static; it is a living artifact with its own promotion lifecycle**, and maintaining it is
exactly the comprehension labor the thesis claimed to have eliminated — now wearing a
governance hat. The relocation did not delete ontology comprehension; it *renamed* it
"ontology maintenance" and made it recurring.

### 3d. Re-ingestion when the ontology changes — the unbounded tail
This is where the relocation can genuinely **blow up**. When the schema/ontology changes
(§3c), every already-ingested fact may need RE-tagging or RE-extraction against the new
shape. A new authority kind means old candidates must be re-triaged; a changed scope
vocabulary means old captures must be re-scoped; a re-typed edge means old graph regions
must be re-derived. **This re-ingestion cost is NOT amortized — it is paid again, in
full, every time the ontology shifts**, and it scales with the *whole accumulated corpus*,
not the delta. The PDF's slow loop has a bounded analogue (dream-state re-scores high-
utility traces, p.7) but it is *utility-thresholded* — it re-touches a sample, not the
whole graph. CyberAlchemy's authority overlay has **no such threshold named in the
corpus**: a default-deny schema change implies a full-corpus re-triage with no sampling
bound. **Honest verdict: the write-time bill is bounded per-ingest (1–4) but UNBOUNDED
across ontology epochs (3d).** The relocation pays off within a stable schema epoch and
blows up at every epoch boundary.

## 4. Z2 net verdict (claim ≤ proof)

- **The thesis's load-bearing leg is ingest, and it is real, not assumed.** The cheap
  deterministic read is *purchased* by a model-heavy, gated, governed write loop (PDF
  two-loop split p.1–7; CyberAlchemy b2 overlay + Review Queue). The other two legs price
  the read and assume the purchase. **Z2 confirms the purchase is genuine engineering and
  names its five line items (§1).**
- **The relocation is NOT a pure shell game — but it is not free either.** It PAYS OFF on
  the authority dimension cleanly (authority is a static decision, write-once, no field in
  the substrate to re-derive — §2) and on any high read/write-ratio, stable-schema regime.
- **It BLOWS UP on three seams the optimistic framing hides:** (3a) messy real inputs make
  extraction failures *silent and deterministic* — determinism ≠ correctness, and the
  PDF's §10.3 synthetic-vs-real caveat is the PDF admitting this; (3b) non-1:1
  reconciliation makes per-fact write cost super-linear, not O(1); (3d) **ontology drift +
  full-corpus re-ingestion is the genuinely unbounded tail** — the comprehension problem
  is not removed, it is moved to write-time AND multiplied by the number of ontology epochs.
- **The honest synthesis:** the deterministic-retrieval thesis is true *within a stable
  schema epoch and for clean-enough inputs*, and its cheapness is bought by amortizing
  comprehension over a high read/write ratio. It is FALSE as an unconditional claim,
  because the purchase price is bounded per-ingest but unbounded across ontology change.
  **Whoever sells "cheap deterministic reads" must also own — and price — the ingest BET
  and the ontology-maintenance treadmill.** That treadmill is the real cost the other two
  legs assume away.

---

## (file: Z3-governance-needs-determinism.md)

## Z3 — EXPLORER (formal/architectural) — leg: GOVERNANCE-NEEDS-DETERMINISM

Position to deepen: **determinism-at-read is a PRECONDITION for authority-at-read** — and the GOVERNANCE leg, not efficiency, is the actual point of the thesis. Then the mandatory self-counterexample. Citations are `file:section`. Claim ≤ proof.

---

### 1. The deepen — why governance needs the deterministic substrate, mapped onto VSM

**The hinge claim, stated sharply.** You cannot attest, authorize, or promote a cosine similarity. A vector lookup returns a *ranked neighbourhood* — fuzzy, threshold-dependent, non-reproducible across index rebuilds and embedding-model versions. There is no stable referent to which an owner, a decision ID, or a promotion stage can attach. A **typed edge with provenance**, by contrast, *is* a nameable object: `e/{edge_id}` with required properties (`development/resonantos-integration/research.md` §E2.2 — "Typed directed edges (`e/{edge_id}`) carry … `validity_start`, `validity_end`, `utility_score`, `confidence`"; "GraphQL schema enforces node/edge types and required properties"). An edge can be cited; a neighbourhood cannot. Therefore **a governable referent is exactly what determinism-at-read manufactures**, and authority-at-read is parasitic on it.

This lines up precisely with the substrate's own two-loop split. Retrieval is "fast, deterministic, no neural models … pure Gremlin graph traversal" (`research.md` §E2.1), and the meaning-evolving model work is quarantined into the slow write-side loop. The read path is deterministic *by construction*. That is the property authority needs: the same query yields the same edge set, so a `pass`/`flag`/`block`/`defer` gate verdict (`cyberAlchemy-v2/authority/AUTHORITY-MODEL.md` §Gate Vocabulary) is **reproducible** — re-running the gate on the same store reaches the same decision. A gate over a cosine neighbourhood is not reproducible, so its verdict is not auditable, so it is not a gate. **Determinism-at-read → stable referent → reproducible gate → authority-at-read.** Each arrow is load-bearing; drop the first and the chain collapses.

**The VSM mapping.** The machine-map already names the structure: the memory substrate is a strong **S4 (intelligence/environment sensing) + S2 (coordination)** organ that is **missing its S5** (`development/machine-map/findings.md` §1 table, §5 — "System-5 missing"; the substrate "evolves meaning" and senses the environment but carries no policy/identity that says what may *count*). cav2 is the candidate **S5** — the policy organ that decides which *kinds* of thing may exercise authority (`AUTHORITY-MODEL.md` §Authority Kinds, the closed default-deny enumeration §Closure). The deepen adds one structural constraint the machine-map implies but does not state: **the S5 must attach to the deterministic ontology, not to the vectors.**

Why: Beer's S5 regulates S1 through S3; regulation requires that the regulated variety be *addressable*. Conant-Ashby — "every good regulator of a system must be (contain) a model of that system" (`machine-map/findings.md` §1, the Conant-Ashby cite) — means cav2's model of the archive must map 1:1 onto referents the archive actually exposes. The deterministic typed-edge graph *is* such a model (typed, finite, enumerable); the vector space is not (continuous, neighbourhood-relative). So cav2-as-S5 can only regulate the part of the substrate that is deterministically addressable. **This is structural attenuation, not statistical attenuation** (`findings.md` §1 distinguishes the two): cav2 attenuates the archive's variety by *typing* (a structural reduction that preserves identity of the referent), not by *thresholding similarity* (a statistical reduction that discards identity). Structural attenuation is the one a regulator can be built on, because it leaves a referent standing. Statistical attenuation dissolves the referent — there is nothing left to govern.

This is exactly the gap E2 found in the substrate's data model: it has `validity`/`confidence`/`utility` but **"no `authority_kind`, `decision_id`, `promotion_stage`, `owner`"** field (`research.md` §E2.2, §E2 Bottom line). The fact-vs-authority partition *is* the S4-vs-S5 partition. The substrate governs facts-over-time (S4 sensing + S2 temporal coordination); it has no organ that governs which assertions are *canonical/promoted/owned* (S5 policy). cav2 is precisely the missing field set, and those fields are only meaningful if they attach to a stable, deterministic referent — `decision_id → e/{edge_id}`, not `decision_id → neighbourhood@threshold=0.82`.

**Therefore the GOVERNANCE leg is the point, efficiency is the side effect.** The thesis is usually pitched on latency (~10–50ms, one GPU call per query, `research.md` §E2.1). But latency is a *consequence* of the read path being model-free; the model-free read path was chosen so retrieval is deterministic; determinism was needed so the result is a citable, gateable referent. Run the causal order forward: **govern → therefore make read deterministic → which incidentally makes it fast.** Efficiency falls out of the same architectural commitment that makes authority-at-read possible. A team optimizing purely for speed could have shipped a faster vector cache and gotten the milliseconds without ever getting governability. They are not the same axis. The governance leg is load-bearing; efficiency is the by-product that makes the load-bearing choice also cheap — which is why it is easy to mistake the side effect for the point.

**Tie-back to the Gödel tension (`machine-map/findings.md` §2 Preserve-the-Gödel-tension, E2(b)).** A generative S5 that enumerated its own admissible kinds could not detect the kind it is structurally blind to. The AUTHORITY-MODEL already encodes the humble form: the kind enumeration is **closed / default-deny** (`AUTHORITY-MODEL.md` §Closure, CAV2-D49) — an unenumerated kind is *blocked*, not silently admitted. This is the read-only, non-generative S5 the machine-map demands. It also shows *why* the S5 sits on the deterministic ontology: default-deny requires a **decidable membership test** ("is this artifact's kind a row in the table?"). Membership in a finite typed enumeration is decidable; "is this cosine cluster a governance kind?" is not. **Determinism is the precondition for the closure rule even being checkable.** This is the formal core of the leg: governance-by-default-deny is only well-defined over a deterministic, enumerable referent space.

---

### 2. RUN ITS OWN COUNTEREXAMPLE (Lane Z honesty, mandatory)

I now attack my own leg on the two fronts the dispatch names. Where it holds, where it breaks.

**(a) Is PROVENANCE — not determinism — the real governance precondition?**

This is the strongest attack and it lands a real hit. Auditors attest non-deterministic processes constantly: a SOC2/ITGC trail attests *that a reviewer approved at time T against version V* — it does not require the review to be reproducible. The attestable object is the **record of what ran on what inputs**, not the determinism of the run. By analogy: a pipeline `query → vector-recall(top-k) → typed-rerank → gate` is fully attestable if you log the embedding-model version, index hash, k, threshold, and the returned edge IDs. You then attest *the recorded execution*, not *the function*. On this reading determinism is sufficient-but-not-necessary, and the true precondition is **provenance + a fixed, citable output referent**.

Where the leg survives this: the attack actually **narrows** the claim rather than killing it. Note what the attestable pipeline still requires — *a fixed citable output referent* (the returned edge IDs). Even the vector step is only attestable because it terminates in deterministic referents (edges), and because you froze the non-deterministic part by *recording* its inputs/version, i.e. you converted it into a reproducible-given-the-record artifact. So the corrected claim is: **governance requires a stable referent + reproducibility-given-provenance.** Pure determinism is one way to get reproducibility-given-provenance (the trivial way: no hidden inputs to record). Provenance-logging is another way (record the hidden inputs). My original "determinism is THE precondition" is **too strong** and I withdraw it. The defensible form: *determinism-at-read is the cheapest and most robust way to satisfy the real precondition, which is reproducible-citable-referent.* The substrate's choice to make the read path model-free (`research.md` §E2.1) is then an **engineering dominance argument, not a logical necessity**: it removes the entire class of "embedding-version drift" provenance you'd otherwise have to log and re-verify on every index rebuild. Determinism collapses the provenance surface to near-zero; provenance-logging keeps the surface large and re-auditable. So the leg holds as *"determinism minimizes the governance attestation burden"* and **breaks as** *"only determinism can be governed."* Honest verdict: the dispatch's framing of determinism as PRECONDITION is **overstated**; the survivable claim is determinism as the **dominant cost-structure** for governance, with provenance as the genuine logical precondition.

**(b) Is the ontology itself non-deterministic — so determinism is only pushed back to write-time, not achieved?**

This is the deeper attack and it also lands. The typed edges are not given; they are **produced by model-driven extraction at write-time** — the slow loop's "model-driven … evolves meaning," with JEPA re-scoring and the verifier (Bonsai) adjudicating supersede/merge/annotate (`research.md` §E2.1, §E2.4). GLiNER2/JEPA-class extraction is a neural process: run it twice on the same document, or with a new model version, and you can get different edges, different types, different `confidence`. So the deterministic read path traverses a graph whose *contents* were non-deterministically authored. Determinism at read is real but **local**: it is determinism *of traversal over a fixed snapshot*, not determinism *of the knowledge*. The fuzziness I claimed to exile from the read path was merely **relocated to write-time**, where it is harder to see.

Where this breaks the leg, and where it doesn't: it breaks the naïve story that "the ontology is the deterministic ground truth." It is not — it is a non-deterministically-extracted artifact. **But** — and this is exactly why the substrate's two-loop architecture is the right shape — relocating the non-determinism to write-time is *precisely what makes it governable*, and this is where my leg and the AUTHORITY-MODEL reconverge. At write-time, the non-deterministic extraction produces a **candidate**, and the AUTHORITY-MODEL's whole apparatus exists to gate exactly this: "capture = evidence, `status: candidate`, never short-circuits to authority" (`research.md` §E3.B); the Core Flow `source evidence → import candidate → … → owner-routed local authority` (`AUTHORITY-MODEL.md` §Core Flow); default-deny on un-promoted kinds (§Closure). **The non-determinism of extraction is admitted as a candidate and frozen into a typed referent by a promotion decision.** Once promoted, the edge is a fixed object with a `decision_id` and an owner — its *content* was non-deterministically proposed, but its *authority* was deterministically conferred by a recorded gate. So the determinism that governance needs is **not** determinism-of-extraction (impossible — that's the model's job, E2(b)'s Gödel blindness lives here too) but **determinism-of-the-promoted-referent-and-the-gate-over-it**. The write-time model proposes; the deterministic read-time graph + the recorded promotion decision dispose.

Net on (b): the dispatch's worry is **correct and important** — determinism is pushed back to write-time, not achieved end-to-end, and anyone claiming "deterministic knowledge" is overclaiming. The leg survives in *corrected* form: governance never needed the *knowledge* to be deterministic; it needed the *referent and the gate* to be deterministic, and it needed the model's non-determinism to be **quarantined behind a candidate-then-promote boundary** so it never silently becomes authority. The substrate's two-loop split (`research.md` §E2.1) and cav2's candidate→promotion ladder (§E3.B; `AUTHORITY-MODEL.md` §Core Flow) are *the same architectural move under two names*: isolate the non-deterministic generator, then govern its output through a deterministic gate. **Where the leg holds:** determinism of the governed referent and the gate verdict is real, necessary, and is what makes default-deny decidable. **Where it breaks:** "deterministic ontology" is a misnomer — the ontology's *content* is non-deterministically authored; only its *post-promotion referent identity* is deterministic. Determinism is a property of the gate and the snapshot, not of the meaning.

---

### 3. Compressed verdict (for the synthesizer)

- **Leg holds, narrowed:** the GOVERNANCE leg is the actual point; efficiency is a by-product of the same model-free-read commitment (causal order: govern → make read deterministic → incidentally fast). The fact-vs-authority gap (`research.md` §E2 Bottom line: no `authority_kind`/`decision_id`/`promotion_stage`/`owner`) *is* the S4-vs-S5 gap (`machine-map/findings.md` §1, §5); cav2 is the missing S5 and must attach to the typed ontology because **structural attenuation preserves a citable referent and statistical attenuation dissolves it** (`findings.md` §1). Default-deny (`AUTHORITY-MODEL.md` §Closure) is only *decidable* over a deterministic enumerable referent space — that is the formal core.
- **Counterexample (a) wins partially:** "determinism is THE precondition" is **overstated**. The true logical precondition is **reproducible-citable-referent**, satisfiable by provenance-logging *or* determinism. Determinism's real status is **dominant cost-structure** (it collapses the attestation/provenance surface to ~zero), not logical necessity. Withdraw the strong form; keep the cost-dominance form.
- **Counterexample (b) wins on framing:** "deterministic ontology" is a misnomer — typed edges are **non-deterministically extracted at write-time** (`research.md` §E2.1/§E2.4, JEPA/Bonsai). Determinism is only pushed back, not achieved. The leg survives because governance never needed deterministic *knowledge*, only a deterministic *gate over a frozen referent*; cav2's candidate→promotion ladder (`AUTHORITY-MODEL.md` §Core Flow; `research.md` §E3.B) is exactly the quarantine that converts non-deterministic extraction into deterministically-conferred authority. The Gödel-blindness of a generative S5 (`findings.md` §2, E2(b)) lives at write-time extraction, which is *why* the S5 must be read-only/default-deny, not generative.
- **One open tension for synthesis:** if provenance-logging can attest a vector pipeline (a), and the ontology is itself model-authored (b), then the honest thesis is **not** "deterministic retrieval enables governance" but "**a quarantined non-deterministic generator + a deterministic gate over typed referents** enables governance." Determinism is the property of the *gate*, not the *retrieval* — the dispatch leg's name slightly misnames its own strongest claim.

---

