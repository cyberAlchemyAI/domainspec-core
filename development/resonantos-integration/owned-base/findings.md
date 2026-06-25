---
tags: [resonantos, living-archive, cav2, arcanum, owned-base, importance, salience, promotion, synthesis]
node_type: synthesis
status: candidate
created: 2026-06-24
sources:
  - development/resonantos-integration/owned-base/research.md (E1 arcanum harvest, E2 Living-Archive salience, E3 govern-importance design — verbatim explorer returns)
  - arcanum/spells/necronomicon/README.md (+ development/)
  - arcanum/arcana/inventory/ (templates/, scripts/, .arcanum/inventory/, development/pilot/evidence-card/)
  - arcanum/arcana/definitions-governance/
  - arcanum/arcana/ontology-vault/
  - arcanum/spells/ontology-harness/
  - arcanum/tools/install_arcanum.sh, bootstrap_arcanum.sh, build-skill-registry.py
  - arcanum/spells/observed-invocation-loop/, arcanum/formulae/observability-setup/
  - "Agent Memory Architecture v7.1" (PDF, 11pp — Living Archive)
  - resonantos-vnext/examples/living-archive-mcp.mjs (placeholder substring rank, L465)
  - development/authority-triage/ (PRIVATE — referenced as boundary, NOT a handoff source)
---

# findings.md — owned arcanum base + the two senses of importance (cav2 ↔ resonantOS)

## 1. One-line answer

**The base:** a substantial, MIT/public OWNED governance base exists in `arcanum/` (necronomicon
substrate-loop, inventory evidence-card/EvidenceSet schemas+validators, definitions-governance,
ontology-vault, ontology-harness, arcanum-bootstrap, observability) — but it is **overwhelmingly
markdown design** with a thin runnable surface of **validators + installers + schemas only** (E1).
**The importance answer:** the Living Archive **already solves recall-importance** (utility_score,
JEPA, Aspirational Model, Self-Model gate), so "tell it what's important to recall" is **REDUNDANT**
(E2); the **non-redundant** opening is **GOVERN/promote-importance** — specifically top-down
**authored / provenance-weighted priors** that override low statistical mass plus authority over the
thresholds, realized as the **evidence-confidence vs commitment-confidence split** (E3), which
**feeds** the substrate's salience signals rather than duplicating them.

## 2. Owned-base harvest table (E1)

| Artifact | What it is | Runnable code vs markdown design | Action | Public-safe? |
|---|---|---|---|---|
| **Necronomicon** (`arcanum/spells/necronomicon/README.md` + `development/`) | Repo-local working-memory + routing-desk: "Inventory And Ontology Substrate Loop"; classifies output, machine-readable gap ledger, owner handoffs, NO-PROMOTION guardrails, active_interaction state | **Markdown design/contract** (46KB README, no runtime) | **PORT-THE-DESIGN** | YES |
| **Inventory sigil** (`arcanum/arcana/inventory/`) | Immutable raw sources + LLM-maintained pages + machine `index.json`; defines **evidence-card** primitive (source_refs, authority state, provenance, trace, residue, promotion_owner) + candidate **EvidenceSet** | **Markdown skill + RUNNABLE validators** | **COPY-THIS** (schemas+validators) / port skill prose | YES |
| ↳ validators | `scripts/validate-index-json.sh`, `validate-evidence-card-slice.sh`, `validate-evidence-card-fixtures.sh` | **Runnable bash/jq** (drop-in) | **COPY-THIS** | YES |
| ↳ schemas/templates | `templates/evidence-card.schema.yml`, `evidence-set.schema.yml`, `index.schema.yml`, `evidence-card-schema.md`, `index.json`, `entry.md`, `log.md`, `tags.md` | **Copyable data contracts** (drop-in) | **COPY-THIS** | YES |
| **Definitions Governance** (`arcanum/arcana/definitions-governance/`) | Canonical definitions, synced indexes, drift checks — the "promote candidate to canonical" owner Necronomicon hands off to | Markdown skill + corpus + validators (`arcanum/tools/validate-artifact-metadata.py`, `validate-artifact-constitution.sh`) | **PORT-THE-DESIGN** (+ copy validators) | YES |
| **Ontology Vault** (`arcanum/arcana/ontology-vault/`) | Roles, confidence, premises, edge rules, branch-aware ontology — promotion target for ontology/premise candidates | Markdown skill + 13 copyable templates (confidence-promotion.md, premise-review.md, ontology-drift-report.md, traceability-matrix.md) | **PORT-THE-DESIGN** (+ copy templates) | YES |
| **Ontology Harness** (`arcanum/spells/ontology-harness/`) | Composes inventory + ontology-vault + context-builder | Markdown | **PORT-THE-DESIGN** | YES |
| **Arcanum Bootstrap** (`arcanum/tools/install_arcanum.sh`, `bootstrap_arcanum.sh`, `build-skill-registry.py`) | Installs the above into a consuming repo (`.arcanum/inventory/`, `.arcanum/observability/`, optional `.arcanum/necronomicon/`) | **Markdown spec + RUNNABLE installers** | **COPY-THIS** (installers) | YES |
| **Observability / Observed-Invocation-Loop** (`arcanum/spells/observed-invocation-loop/`, `arcanum/formulae/observability-setup/`) | One telemetry signal per managed invocation + reflection counters | Markdown | **PORT-THE-DESIGN** | YES |
| **Live inventory instance** (`arcanum/.arcanum/inventory/`, `arcanum/arcana/inventory/development/pilot/evidence-card/`) | Populated reference impl + fixtures the validators run on | Data (reference) | **COPY-THIS** (as reference) | YES |

**Honest runnable accounting (E1):** the WHOLE runnable surface is **validators + installers +
schemas/templates** — NOT a memory engine. Necronomicon, Inventory, Definitions-Governance,
Ontology-Vault, Ontology-Harness bodies are **LLM-executed skill prose**. Victor gets
format + lifecycle + guardrails + validators; he still builds the runtime.

## 3. CRITICAL boundary correction (E1)

**`authority-triage` is PRIVATE.** It lives at **repo-root `development/authority-triage`**, NOT in
public `arcanum/` (E1 boundary correction, research.md:60–65). Only its **evidence-card residue**
surfaces under `arcanum/.arcanum/inventory/entries/`. It must **NOT** be handed to Victor by name or
source.

**The public analog** for "triage the authority of a knowledge claim" is the **inventory
evidence-card authority-state + promotion_owner model** (plus definitions-governance drift audit) —
all MIT/public (E1, research.md:64–65).

**Flag (radical candor):** the prior dispatch's teammate-facing material leaned on `authority-triage`
by name (see prior `findings.md` §4 "authority-triage front door", §3 "authority-triage decision",
§4 table rows). The public/teammate path here must be **scrubbed** to use the **inventory
evidence-card / promotion_owner analog** instead — never the private codename or source. This is a
correction to the seam framing, not a new claim.

## 4. THE IMPORTANCE ANSWER — two senses (the heart of this dispatch)

The dispatch goal hinges on separating **two distinct things both called "importance,"** and seeing
that the Living Archive already owns one of them.

### (a) RECALL / salience-importance — ALREADY SOLVED → telling it what to recall is REDUNDANT (E2)

The Living Archive's machinery answers the **recall/curation axis** at three timescales, bottom-up
from graph statistics and embedding geometry (E2, research.md:80–104):

- **`utility_score`** — first-class per-edge property (p.3); Fast Loop "filter by utility threshold"
  (p.5); Dream PRUNING tombstones `utility<threshold` (p.7). A recall + retention gate.
- **JEPA Relevance Predictor** (~110M) — per chunk/function, "score semantic relevance" (p.4);
  produces a relevance score at write (p.6). The content-importance scorer.
- **Aspirational Model — directional "wanted" importance** — shared-JEPA encoder; "directional
  relevance — what the agent WANTS to know, not just what it HAS" (p.4); emits a directional score
  distinct from JEPA's (p.6). **The substrate already has a notion of desired/wanted importance** —
  but **inferred/learned, not declared.**
- **Self-Model density / "I don't know" gate** — graph-stat logic gating mind-waking on density,
  preventing hallucination in sparse regimes (p.1, p.4); percolation threshold empirically learned
  per-deployment (p.11 §10.6). Meta-importance: do I know enough.
- Recency/utility/structural signals, Dream REPLAY re-scoring, temporal-validity filtering (p.7–8).

**Conclusion:** naive "tell it what's important to retrieve/keep" is **REDUNDANT** — do not re-coin
it (E2, research.md:124).

### (b) GOVERN / promote-importance — the NON-REDUNDANT opening (E2 + E3)

Every E2 signal is derived **bottom-up**. There is **NO authored, top-down importance assertion**
(E2, research.md:106–110). E2 names three gaps:

1. **Authored priors with no statistical mass** — a net-new/rarely-accessed concept the operator
   KNOWS matters has low utility (prunes) and may sit under the percolation floor → "I don't know";
   no channel to **INJECT** importance the graph hasn't earned. The Aspirational Model is the nearest
   thing but is **inferred, not declared** (research.md:111–114).
2. **Threshold calibration is per-deployment and ungoverned** — percolation/utility cutoffs named,
   but **no authority over their values** (research.md:115–116).
3. **No claim≤proof / provenance weighting on importance** — importance is purely relevance+utility;
   no notion that importance should track source **AUTHORITY/PROVENANCE** (research.md:117–118).

E3 supplies the matching design: this is a **different importance — about reliance and promotion
("can we stand on this?"), not relevance-to-a-query ("bring this forward")** (research.md:135–137).
The substrate "measures AUTHORITY EARNED AGAINST GUARDRAILS." The mechanism that nails it is the
**confidence split** (necronomicon KSF:164–177): **evidence confidence** ("how well supported") vs
**commitment confidence** ("how strongly should we rely now"). "High evidence, low commitment: true
but not strategically important" — a fact can be **well-supported (recall-findable) yet NOT important
to rely on** (E3, research.md:147–150).

### The map-vs-decision line, and composition

**The substrate governs the recall MAP of facts; govern-importance governs the DECISION of what to
rely on / promote.** Crucially, govern-importance **COMPOSES WITH (feeds) the salience signals — it
does not duplicate them.** Frame the contribution as **authored / provenance-weighted priors feeding
the existing utility / Aspirational signals, not replacing them** (E2, research.md:127–129; E3
"they compose … neither subsumes the other," research.md:176). Concretely: an authored prior can
inject importance the graph hasn't earned (overriding low statistical mass), and authority over the
thresholds calibrates the substrate's own ungoverned cutoffs — both feed inward.

## 5. Honest status — neither side has this running (E2 + E3)

Claim ≤ proof, both ways:

- **Our base is mostly markdown design (PORT-THE-DESIGN).** The runnable surface is **only
  validators + installers + schemas** — there is NO compiled memory-governance service to lift
  (E1, research.md:51–58). necronomicon/inventory/definitions-governance/ontology-vault bodies run
  via an LLM agent following skill prose.
- **The Living Archive's OWN scoring machinery is mostly SPEC, NOT SHIPPED.** The shipped code's
  retrieval rank is a **placeholder substring score `max(1,1000-matchIndex)`** at
  `living-archive-mcp.mjs:465` — **NONE of the PDF scoring machinery (utility/JEPA/Aspirational/
  Self-Model) is implemented yet; the importance spine is SPEC, NOT SHIPPED** (E2,
  research.md:119–121).
- **E3's govern-importance layer is markdown design, status `strategy-proposal`/`draft`** — no
  fixture shows a candidate actually promoted; `DESIGN.md` lists R-DES-001..005 incl. the risk that
  "Necronomicon becomes a thin inventory wrapper" (the govern-layer collapsing back into retrieval),
  flagged unproven (E3, research.md:178–185).

So **neither side has importance running** — do not present design as runnable on either side.

## 6. Residue / open

- **Govern-importance runtime is unbuilt** on both sides (no promoted-candidate fixture; substrate
  scoring is placeholder). The notion is consistently encoded; the runtime is not (E2, E3).
- **Threshold-authority surface is undesigned** — E2 gap 2 (ungoverned percolation/utility cutoffs)
  has no owner or schema yet; it is the cleanest unclaimed slice for authored calibration.
- **Provenance-weighting of importance** (E2 gap 3) needs a concrete bridge from evidence-card
  provenance/authority-state to a weight the substrate's signals can consume — designed in prose,
  not specified as a field contract.
- **Teammate-facing framing must be re-scrubbed** to drop the private `authority-triage` codename in
  favor of the inventory evidence-card / promotion_owner analog (see §3) — carried into BASE-FOR-VICTOR.md.
- **Necronomicon ↔ Review-Queue match is structural, not demonstrated** — intake→classify→promote
  maps onto resonantOS intake→Review-Queue→promote (E3, research.md:169–176), but no end-to-end run
  proves the composition. (S1 precedent fix applied: the LOOP itself is YOU-ALREADY-HAVE-THIS; only
  the NO-PROMOTION guardrail + gap-ledger + receipt-debt are the portable residue — corrected in
  BASE-FOR-VICTOR.md §1.)
- **`living-archive-mcp.mjs:465` placeholder cite is an external-source read** (S2 non-vacuity): the
  file is in the resonantOS repo, not this one; the placeholder-rank claim is internally consistent
  across E2/findings but rests on the explorer's read, not independently re-verified here.
