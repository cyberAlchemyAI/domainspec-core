---
tags: [inventory, cav2, authority, non-collapse, build-from-owned, synthesis]
node_type: synthesis
is_session: false
layer: governance
nature: reference, contradiction-record
status: candidate
created: 2026-06-26
boundary: INTERNAL — cav2 private governance vocabulary; not for public arcanum/
sources:
  - cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d22-orthogonal-classification
  - cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d29-axis-orthogonality-invariant
  - cyberAlchemy-v2/authority/AUTHORITY-MODEL.md#non-collapse-rules
  - cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md#cav2-c17-precedent-sweep-before-net-new-build-from-owned
  - cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d48-authority-promotion-lifecycle
---

# Where `non-collapse` and `build-from-owned` are actually defined (definitions map)

Candidate Inventory reference (lookup filing; **promotes nothing**; owners = definitions-governance /
constitution-governance). Answers the recurring question *"what are the definitions for non-collapse
and build-from-owned?"* The key finding: **they are formalized asymmetrically.**

## NON-COLLAPSE — an undefined umbrella over a rule-family (no standalone CAV2-D term)
No `CAV2-D` term is named "non-collapse." It is the umbrella over four surfaces:
1. **`CAV2-D22` Orthogonal Classification** — a classification axis is admissible only if it adds a
   distinction *not silently redundant* with an existing axis; orthogonal = changing it doesn't
   secretly change another axis; dependency must be typed via `CAV2-D16`.
2. **`CAV2-D29` Axis Orthogonality Invariant** — two authority dimensions are *independently variable*
   unless an explicit typed relation relates them; advancing one must not silently advance/validate/
   authorize another. *(This is the one the SMT validator handoff cites.)* Gloss: "moving one slider
   shouldn't secretly move another; if it does, name the wire."
3. **`AUTHORITY-MODEL` → "Non-Collapse Rules"** — 7 numbered cross-layer rules (evidence≠authority;
   ontology can't decide; inventory can't promote; discipline can't define/author-constitution;
   constitution doesn't prove the source claim; a run doesn't redefine; public mustn't inherit private
   by proximity).
4. **Operational form** — the "Must not collapse into" column in the Authority-Kinds table + the
   `forbidden_collapse` field on every discipline/concept card.

→ `D22`/`D29` = the *definitions*; the 7 rules = the *governance applications*; `forbidden_collapse`
= the *per-artifact instantiation*. **Gap:** "non-collapse" the word is load-bearing but undefined —
candidate to either define it or formally declare it an umbrella pointing to D22/D29.

## BUILD-FROM-OWNED — defined as a constitution rule (deliberately not a term)
- **`CAV2-C17` Precedent Sweep Before Net-New (Build-From-Owned)** — *candidate*, validation mode
  *review*, derives from `CAV2-D48`. "Before any KILL/net-new verdict, sweep for an existing owner
  in-repo; a found owner is a **positive** result (relabel build-from-owned, cite owner, deploy,
  never claim novelty); only a clean sweep admits net-new." (`C16` is a retired number.)
- **`CAV2-D48`'s definition** names the principle ("build-from-owned generalization inference").
- The **research-skill precedent gate** already enforces it (review-mode).
- **C17 lists "re-defining build-from-owned itself" as a *non-example*** → intentionally a *rule*,
  not a standalone term (defining it as a term would violate it).

## The relationship (grounded in the texts)
- **Non-collapse (`D29`):** *given two declared dimensions, prove they're independent.*
- **Build-from-owned (`C17`):** *given one candidate, search the corpus for an owner it is NOT
  independent from* (coincides-with / specializes).
- Same independence relation, **opposite polarity** → why the validator handoff says they share one
  SMT core (with closure = 3 siblings).

## Contradiction recorded (not silently fixed)
The build-from-owned validator handoff
(`cyberAlchemy-v2/disciplines/development/2026-06-26-build-from-owned-validator-HANDOFF.md`, "Why now")
states *"the precedent-sweep was a habit, not a gate."* **This is inaccurate:** `C17` makes it a
*candidate constitution rule* and the research skill *enforces it* (both review-mode). The accurate
gap is the absence of **deterministic, cross-capability enforcement** (the SMT validator). The
handoff's target stands; its framing needs the fix. **Owner:** invoke/handoff author (correct the
line + cite `C17` as the owned rule the validator hardens).

## Boundary
Inventory candidate read-model. Promotes nothing. Owners: definitions-governance (any "non-collapse"
term decision), constitution-governance (`C17` number-confirm + promotion), handoff author (the
correction). Cross-links: [[cav2-ontology-authority-organizing-synthesis]]. INTERNAL.
