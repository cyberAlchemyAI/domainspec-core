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
