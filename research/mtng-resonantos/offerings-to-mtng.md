# Offerings to MTNG — substance-help (NON-SOURCE, local-only)

What this repository **already owns** that could deepen MTNG's *own* conceptual
and formal thinking. This is the **BRIDGE layer** of the MTNG tower and is
distinct from `improvement-map.md`: that file is **build-help** (which of our
*skills* to adapt to close MTNG's eight gaps); this file is **substance-help**
(which of our *proved results and governance ontology* upgrade MTNG's own
informal ideas). It promotes **nothing** into Arcanum, is advisory to an
**external proposal only**, and obeys **claim ≤ proof** as a hard rule: every
row names the exact file and carries an explicit evidence-status, and no analogy
is dressed as a theorem. Evidence-status vocabulary is fixed to exactly five
tokens, defined once below.

**Evidence-status vocabulary (the only allowed tokens):**

- **proved-and-cited** — a `sorry`-free Lean theorem; the `.lean` file is named.
- **partially-formalized** — the carrier `.lean` file(s) contain `sorry`; treat
  as conjectural support, **not** proof.
- **analogy/conjecture** — a design discipline or framework reading; the repo's
  own claim ≤ proof already marks it non-theorem.
- **owned-and-defined** — a cyberAlchemy-v2 (v2) governance rule that is an
  active, non-candidate definition; the v2 file is cited.
- **candidate** — a v2 asset that **self-marks** `candidate` / `OPEN`; cited as
  scaffolding, not a finished engine.

---

## The headline — MTNG is our pattern on two lanes

MTNG is structurally the **same shape** as our Saturn/spine discipline: *intent
versus reality drift; audit the translation; account the residue.* Because it is
the same shape, what we own lands cleanly on it — but on **two different lanes**,
which is exactly why the two corpus sweepers each declared a different "primary
offer" and why both are right:

- **Validator / residue lane.** MTNG's cleverest informal moves — "a validator
  that passes is good enough" and "leftover becomes a memory candidate" — are
  intuitions. Our **formal residue / clean≠correct** results are the missing
  *conceptual backbone* under that lane: they turn two of MTNG's intuitions into
  structural necessity. (Grothendieck sweep, formal spine.)

- **Promotion / authority lane.** MTNG's biggest open dependency (Phase-0,
  "engine accepts per policy", what gets promoted and by whom) is
  governance-shaped, and v2 has no formal backbone there. Our **v2
  authority/promotion ontology** is the missing *governance backbone* for that
  lane. (Abramsky sweep, governance ontology.)

They do not compete; they deepen **different** MTNG concepts. Offer both, but
keep them on their own lanes and at their own evidence-status.

---

## Table A — Formal offerings (the Lean spine)

| Owned concept (exact file) | MTNG concept it deepens | What it offers | Evidence-status |
|---|---|---|---|
| **schema⊥instance independence** — `m6_strong_refuted_poly`, four-object counterexample (`domainspec-lean-formalization/lean-formalization/M6Counter.lean`, `sorry`=0) | The single "validator passed" obligation | MTNG needs **two** validator obligations, not one: type-preservation on the schema side **and** output round-trip on the instance side. M6-strong proves passing one does **not** imply the other; they are logically independent. | **proved-and-cited** (M6Counter.lean) |
| **bicyclic clean≠correct** — `lanUnit_app_not_mono_bicyclic` (`domainspec-lean-formalization/lean-formalization/Bicyclic.lean`, `sorry`=0; packaged in `DualResidueLossStructure.lean`, `sorry`=0) | "A green validator means correct" | Validator-as-**misrouting-detector**: schema-side audit passes cleanly while the instance op `Lan_Δ` silently merges a torsion object via an L2 equation `ab=1` the audit cannot encode. So a green validator = *no disagreement within its own vocabulary*, **not** correctness. | **proved-and-cited** (Bicyclic.lean) |
| **typed residue η^ins** — Skolem-null witness, existence/independence via `Σ_Δ ⊣ Δ* ⊣ Π_Δ` (`domainspec-lean-formalization/lean-formalization/M6Counter.lean`, `DualResidueLossStructure.lean`) | MTNG "memory candidate" (leftover) | Model the memory candidate as a **named residue with a budget**. The Σ_Δ-vs-Π_Δ question becomes a concrete design fork: did the node **Skolemize** (invent a fresh witness) or **join/enumerate** completions? *(The residue itself is proved to exist and leak; the mapping onto MTNG's "memory candidate" is an analogy.)* | residue **proved**; the MTNG mapping is **analogy/conjecture** |
| **persistence / reflection tower** — `tower_no_finite_closure`, `C_ω_absorption_refuted` (`reflection-tower.md`, `regimes-of-residue.md` Regime 4; carriers `ReflectionTowerAnchored.lean`, `StrangeLoop.lean` — `StrangeLoop.lean` contains `sorry`) | "Promote the leftover and it's handled" | Why **bounded-reroute-then-stop is honest**: promoting residue to the next-level vocabulary *relocates* it, it never closes (the tower never finitely closes; ω-absorption refuted). Argues for log-and-stop, not infinite promotion. | **partially-formalized** (carrier file has `sorry`) — conjectural support, **NOT** proof |
| **bridge = audit surface owning {pair, check, residue, route}** (`bridge-layer.md`) | A validator that "just passes" | A validator must **declare its residue and its route**, not only emit pass/fail. The bridge owns the four-slot contract; a node validator inherits it. | **analogy/conjecture** (design discipline, not a theorem) |

---

## Table B — Governance offerings (cyberAlchemy-v2)

| Owned concept (exact file) | MTNG concept it deepens | What it offers | Evidence-status |
|---|---|---|---|
| **Authority Kinds** (`cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md`) | Who/what carries authority | Type `actor_ref` / `contributor_ref` by governance route, plus `forbidden_collapse`: *"evidence is not authority by itself."* | **candidate** |
| **Authority Postures** (`cyberAlchemy-v2/ontology/AUTHORITY-POSTURES.md`) | "Memory candidate is review-only" | Generalize review-only into `allowed_use` / `blocked_use` postures with a Public/Private rule; *"posture is not confidence"* mirrors our defer-valuation discipline. | **candidate** |
| **Lifecycle Model + Typed-Hole Rule** (`cyberAlchemy-v2/ontology/LIFECYCLE-MODEL.md`) | `closed_result` conflates state, verdict, and projection | Separate axes: workflow-state vs promotion-verdict vs projection-state. The typed-hole rule = a shared **rail → owner profile → verdict**: the ontology *represents* the rail and **must not fill** the verdict hole. Deepens validator-vs-synthesis: the node contract is a **rail**; the verdict is filled by a **separate owner**. | **candidate** (live schema marked Deferred) |
| **Node Model + status axis** (`cyberAlchemy-v2/ontology/NODE-MODEL.md`) | Node has one undifferentiated role | Node `concept_role` ∈ {authority, evidence, workflow, projection, **residue**} with per-node `forbidden_collapse`; **workflow state ≠ maturity status**. `concept.residue` as a first-class node role MTNG currently lacks. | **candidate** (gate = flag) |
| **Branch As View** (`cyberAlchemy-v2/ontology/BRANCH-AS-VIEW.md`) | MTNG branch / synthesis | A branch is an **interpretive VIEW over cited artifacts**, not a forked copy / vault node / lifecycle state / promotion route. `view_role` enum + Forbidden Collapses (branch membership → promotion state, etc.); **branching confers no authority.** | **candidate** |
| **Relation Model + Value-Cycle Guard** (`cyberAlchemy-v2/ontology/RELATION-MODEL.md`) | Recombine / synthesis edges | Per-edge `authority_effect` ∈ {none, staging, projection, owner-decision, blocked}: recombine edges must **declare if they move authority**. Note the boundary: `witnesses_authority_movement` / `promotion_movement_edge` (node → `PromotionRecord`) are schema-evolution-only = **bridge-edge KILL-until-amendment in v2 itself**. Flagged, **not** presented as solved. | **candidate** (movement edges OPEN/blocked) |
| **Promotion Policy + 7-rung Ladder** (`cyberAlchemy-v2/authority/promotion-policy.md`) | Memory/contribution promotion | A ladder: Source → Inventory → Ontology → Local-authority → Implemented → Stable → Extraction, with a **per-rung owner gate** and **Pass/Flag/Block**; *"promotes by owner route, not enthusiasm."* | **owned-and-defined** ladder *shape*; **extraction threshold OPEN** |
| **Boundaries: source-vs-read-model** (`cyberAlchemy-v2/authority/boundaries.md`) | "Synthesis/memory candidate is a thing that gets promoted" | *Raw sources are highest evidence; inventory/ontology/memory are **read models** that do not promote themselves; generated surfaces must trace to canonical before influencing a contract.* So a synthesis/memory candidate is a **READ MODEL, not a promotion.** This is the **one active non-candidate rule** in v2. | **owned-and-defined** (active rule) |
| **Source-ledgered amalgamation + ingest contract** (`cyberAlchemy-v2/README.md`, `cyberAlchemy-v2/SOURCE-MAP.md`) | MTNG synthesis provenance | *Amalgamation by governance, not copying;* ingest rule: *"every claim cites a source path or is labeled synthesis / inference / open-question."* A provenance contract for MTNG synthesis. | **owned-and-defined** method / **candidate** discipline |

---

## Contested: formal backbone vs governance ontology

The Grothendieck sweep called the **formal spine** the primary offer; the
Abramsky sweep called the **governance ontology** the primary offer. They are
**not competing** — each is the right backbone for a *different MTNG lane*:

- Formal results → the **validator/residue lane** (Table A upgrades MTNG's
  DEF-4/DEF-5 intuitions).
- Governance ontology → the **promotion/authority lane** (Table B fills MTNG's
  Phase-0 / "engine accepts per policy" open dependency).

**Ordered recommendation — what to offer MTNG FIRST:**

1. **The two PROVED formal results first** — schema⊥instance independence
   (`M6Counter.lean`) and bicyclic clean≠correct (`Bicyclic.lean`). They upgrade
   MTNG's two *cleverest informal moves* (two-obligation validator;
   green≠correct) from intuition to **structural necessity**, and they **cost
   nothing to state** — they are already `sorry`-free theorems.

2. **Then the two most-owned governance assets** — the v2 **7-rung promotion
   ladder** (`promotion-policy.md`) and **source-vs-read-model**
   (`boundaries.md`) — onto MTNG's promotion gap. The ladder *shape* is owned
   and the read-model rule is the one active non-candidate rule, so this is the
   most-grounded governance offer even though the extraction threshold stays
   OPEN.

3. **Defer the analogy/conjecture items** — three-axis decomposition, the five
   regimes of residue, and persistence — as **"vocabulary to watch, not
   backbone."** Offering them as backbone would be claim > proof inflation.

---

## Honest boundaries (claim ≤ proof)

- **Exactly two offerings are clean Lean proofs:** schema⊥instance independence
  (`m6_strong_refuted_poly`, `M6Counter.lean`, `sorry`=0) and bicyclic
  clean≠correct (`lanUnit_app_not_mono_bicyclic`, `Bicyclic.lean`, `sorry`=0;
  packaged `sorry`-free in `DualResidueLossStructure.lean`). Only these two may
  be offered to MTNG **as proof**.

- **Persistence is partially-formalized.** The reflection-tower / ω-absorption
  story rests on carrier files that contain `sorry` (`StrangeLoop.lean`;
  `ReflectionTowerAnchored.lean` cited alongside). `tower_no_finite_closure` /
  `C_ω_absorption_refuted` could **not** be confirmed `sorry`-free. Offer it as
  **conjectural support, never cite it as proof.**

- **The three-axis decomposition** (vertical-Yoneda / horizontal-Noether-drift /
  diagonal-Lawvere; `regimes-of-residue.md`, `spine-cyberalchemy-relation.md`)
  is the framework's **own unwritten conjecture** — the "Lost in Translation"
  paper is **unwritten** and the horizontal axis is the repo's own *"partially
  analogical."* It is **vocabulary to watch**, not a backbone offer.

- **Nearly every v2 governance asset is `candidate`.** The one exception is the
  source-vs-read-model boundary (`boundaries.md`). And the node →
  `PromotionRecord` movement edge is **KILL-until-amendment in v2 itself**
  (`RELATION-MODEL.md`). So Table B is **candidate scaffolding + forbidden-
  collapse discipline**, not a finished promotion engine — offer it as
  structure, not as a turnkey component.

- **This doc promotes nothing into Arcanum.** It is BRIDGE-layer, NON-SOURCE,
  local-only, and advisory to an **external proposal only**. Every row above
  cites the exact file it draws from.
