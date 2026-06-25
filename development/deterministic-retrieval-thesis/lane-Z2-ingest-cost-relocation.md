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
