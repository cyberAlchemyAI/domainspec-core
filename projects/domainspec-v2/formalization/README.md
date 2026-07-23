# formalization/ — imported formal artifacts

Status: **import snapshot** (evidence + candidate instrument), not authority and not built in this repo.
Imported: 2026-07-14, from the sibling repo `../../../../domainspec-lean-formalization/lean-formalization/`
(selection rationale: [`research/lean-formalization-implications/findings.md`](../../../research/lean-formalization-implications/findings.md)).

Relationship authority stays in [`definitions/relationships/relationships.yml`](../definitions/relationships/relationships.yml).
Nothing in this folder defines or amends a signature.

## What is here

### `DomainSpecEdgeSignature.lean`

A **decidable, executable type-checker** for a DomainSpec concept graph, written in Lean 4
(Mathlib), with fidelity theorems proved by `decide`. Zero `sorry`. In DomainSpec wording:

- **σ table** (`sig`, :150-185) — the DS-D8 signature operator: each edge label maps to its
  admissible (source, target) meta-types. Finite, total, executable.
- **`WellTyped` is decidable** (:219) — DS-P1 well-typedness compiles to a runnable check,
  the "Morphism typing" candidate law of the
  [category-law formalization route](../definitions/reviews/2026-07-12-category-law-formalization-route.md)
  in mechanized form.
- **Two typed objects, separated** — the point of the file:
  - **`residue`** (:226) — edges mis-typed *between known meta-types*: genuine modeling
    errors, rejected. "Was the spec built right?"
  - **`escapes`** (:230) — edges the vocabulary *cannot classify* (`opaque` node / `other`
    edge): accepted (graceful degradation) but **counted**. "Is the vocabulary enough?" —
    the adequacy meter. Where escapes concentrate on a real corpus is which meta-type or
    edge the vocabulary is missing.
- **Proved, not just implemented** (all by `decide`, no `sorry`):
  - `wellTyped_iff_residue_empty` (:234) — the residue/escape/valid trichotomy is exhaustive
    and exclusive: the meter has no silently-missed case. This is what a plain validator
    script cannot give — a property of the *rule set*, for all graphs, not only the graphs
    a test happened to run.
  - `dsP2_disjoint` / `dsP2_cover` (:251-256) — backend/UI partition holds and the
    extensions are exactly what falls outside it.
  - `sig_family_scoped` + `dsP3_crosslayer_direction` (:270-282) — every backend edge is
    backend↔backend, intra-UI is UI↔UI, cross-layer is UI→backend; a mistyped σ row makes
    the proof fail.
  - Count theorems (:303-318) and non-vacuity witnesses (:341-391) — the checker rejects a
    real error, accepts and tracks escapes, integrates the extensions.
- **Marked extensions (NON-spec candidates)** — `aggregate`, `boundedContext`, `associates`
  with `Cardinality` (entity↔entity multiplicity), and the escape hatch (`opaque`/`other`).
  Candidates to test against real domain models, not vocabulary.

## Why it is useful here

1. **Route evidence.** The morphism-typing row of the category-law route asks for exactly
   this consolidation; this file is the existence proof that the finite DS-D8 rule can be
   stated formally and checked decidably, with the σ-consistency meta-theorems that a
   validator script only samples.
2. **Adequacy instrument (escapes).** The escapes counter operationalizes promotion-rubric
   criterion 8 — *witnessed decision pressure*
   ([first-class-category-boundary findings](../research/2026-07-02-first-class-category-boundary/findings.md)) —
   as a measurable quantity: run the checker over a corpus, watch where escapes concentrate,
   and that concentration is the witness for the next first-class candidate. The file itself
   is honest about the epistemic status: this is *"an empirical, measurable question …, not
   a proof"* (:18-20).
3. **Drift-gate candidate.** The σ table here is a *transcription* and is already **stale
   against root authority** (see below). That staleness is the argument for the derivation
   candidate: generate the formal table (and the runtime validator) from
   `relationships.yml`, so the fidelity theorems become an executable drift gate instead of
   a second hand-maintained copy. Not implemented; route through the category-law research
   tower.

## Known drift vs root authority (intentional — do not silently fix)

The Lean spec core transcribes an earlier 25-meta-type / 29-edge vocabulary. Root
[`relationships.yml`](../definitions/relationships/relationships.yml) has since reconciled to
**31 active signatures**. Verified divergences:

| Lean σ table | Root `relationships.yml` |
| --- | --- |
| `enforcesCross` active as its own edge (:156) | `enforces-cross` **deprecated**; use `enforces` + cross-feature scope |
| no `owns` / `belongs-to` | `owns`, `belongs-to` first-class (Entity↔Entity family) |
| `applies`: policy → operation only (:162) | `applies` targets both `Operation` and `Calculation` |
| `queries`: query → entity (:165) | `queries` source-widened to read-capable behavioral concepts |
| no `creates` | `creates`: same-feature Operation → Entity with exact `creation_targets` source-effect binding |
| `associates` + `Cardinality` extension (:184, :320-339) | not a root signature; overlaps the promoted Entity↔Entity family — reconciliation is an open question |

This drift is **the exhibit** for use 3 above, so it is preserved as-is. Any update to the
σ table should come from the generate-from-root decision, not from hand-editing this copy.

## Boundaries and caveats (claim ≤ proof)

- **Not built here.** No lakefile/toolchain in this repo; the file compiles in the sibling
  repo (Lean 4 + Mathlib). The sibling's own README flags a global build-gate re-verify as
  pending; treat "proved" as *proved at source, snapshot here*.
- **Not authority.** DS-D8 authority is `definitions/relationships/relationships.yml`;
  DS-D1 meta-type authority is `definitions/meta-types/`. This file is evidence and
  instrument design.
- **Escapes ≠ proof of adequacy.** No finite fixed vocabulary is provably complete for the
  open class "any code that models a domain" (:18-20); the meter makes adequacy measurable,
  never certified.
- The sibling repo remains the proof source of record; upstream changes do not propagate
  here automatically.
