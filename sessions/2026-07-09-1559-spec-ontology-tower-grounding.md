---
tags: [domainspec-v2, craft-state, ontology-tower, metamodeling, spec-vs-ontology, asymmetric-tower, edge-law, node-vocabulary, claim-le-proof, subagents-dispatch]
node_type: conceptual
is_session: true
layer: architecture, ontology
nature: explanatory, technical
status: active
created: 2026-07-09
timestamp: 2026-07-09T15:59:38-03:00
expires: 2026-09-07
conversation_id: 2026-07-09-spec-ontology-tower-grounding
decisions_made: false
contradictions_found: true
specs_updated: [telemetry/agents/subagents-dispatch.yaml]
promoted_candidates: []
expected_importance: 5
importance_rationale: "Falsifies two of my own glosses against the sibling formalization and predicts-then-grounds a real edge-law tension (clean-widening vs D3), but the session mutated only the telemetry ledger — no discovery doc, spec edit, or checker was written — so this session node is the sole durable record of the finding."
---

# Spec vs ontology — the schema/instance tower is asymmetric, and Lane-Z stays open

## Summary

This session began as a read-only `/craft state` over the DomainSpec-v2 ledger and turned into a conceptual audit of what a spec *is* relative to an ontology. Working from the user's proposal that "the spec is the rules of an ontology and a running ontology is its instances," we refined it to: spec = the intensional/rule layer, running ontology = instances under *live enforcement*, plus a metamodeling tower (meta-schema → spec → instances) in which each middle layer is an instance looking up and a schema looking down. The user asked to check that tower against the sibling repo `../domainspec-lean-formalization`, where it proved real but **not symmetric**: the V-axis is Spivak's typing (schema = small category, instance = functor out of it, retrofitted onto the live `DomainSpecSystem`), while `AsymmetricTower*` and `ReflectionTowerPromotion` prove promotions are faithful but never equivalences and that residue is irreducible (`defectNoise_empty_iff_fullyFaithful`). That falsified both the user's "same arrow reversed" gloss and my own "one object, two roles" gloss; the corrected substrate is two objects per level (a schema and an instance joined by conform-with-residue) plus a *separate* cross-level promotion arrow. On the categorical question we concluded the spec is not a category but a finitely presented category ⟨generators = the 31 edge signatures | relations = the edge-law⟩, naming the ladder quiver → reflexive quiver → semicategory → category. From that framing I predicted a defect: a "clean-widening" (same target, same semantics) is a *relation*, not a generator, so admitting it as a new edge type contradicts the "composes into different code" rule. A registered two-agent read-only grounding dispatch (`2026-07-08-ontology-tower-grounding`, closed resolved) confirmed the prediction against canon and surfaced two further drifts, while fixing the inventory: 25 meta-types = 14 backend formalized + 11 UI deferred across structural/behavioral/connective/lifecycle, 31 active edge signatures, and `D3`/`D4`/`D5` active but the whole node vocabulary `D6`–`D15` still candidate. I then retracted my own repeated claim that this framing "dissolves" the Lane-Z/A decision: the layering *is* `domainspec-v2-D5`, already ratified, whose own note calls it an interim stance pending an agent-cost experiment — Lane-Z/A is an economics question about fusing artifacts, not an ontology question, so nothing in this session moved it. Three independent routes (categorical reasoning, the Lean residue spine, and the live noncollapse research node) converged on the same clean-widening fault, which is evidence but not novelty. No definitions, code, or specs were mutated; the only file written was the telemetry dispatch ledger.

## Contradictions

- validates `projects/domainspec-v2/definitions/DEFINITIONS.md` (domainspec-v2-D5) — the two-plane boundary was independently re-derived from first principles before reading it, confirming the ratified framing.
- questions `projects/domainspec-v2/definitions/DEFINITIONS.md` (domainspec-v2-D3) — the "clean-widening = clean" corollary admits an edge that does not compose into different code, an edge-law admissibility gap reconciled only via D23, not within D3 itself.
- questions `projects/domainspec-v2/definitions/DEFINITIONS.md` (domainspec-v2-D11) — never states which semantics "instance" carries (functor-into-`Set` for data vs term-in-`Type` for code), an ambiguity underlying OQ-B's "authority-resolved vs exercised instance".
- questions `projects/domainspec-v2/definitions/DEFINITIONS.md` (domainspec-v2-D4) — quotes 29 typed edges where the active DS-D8 authority holds 31; the stale count is also present in the research layer.

## Open questions

- Does the non-collapse property recur at every rung of the schema/instance tower (meta-schema / meta-type schema / spec / instance), or is it specific to the meta-type rung where it has been tested?
- Are the engineering, mathematical, and empirical views literally the same structure or only analogous — does the running DomainSpec system actually *instantiate* the asymmetric tower the Lean models, rather than merely resembling it?

## Next steps

- Run the three verification checks that `projects/domainspec-v2/development/meta-type-formalization/research/2026-07-08-open-questions-noncollapse/findings.md` declares still-open: re-run the noncollapse checker CLI under each T-B2 resolution key (verb-id / +`feature_scope` / +endpoints); locate and read the DS-D8 resolver to confirm what it keys on; re-read `projects/domainspec-v2/definitions/relationships/relationships.yml:17` to confirm the `attribute-equals` opaque-token semantics.
- Once those land, apply the six queued edits enumerated under "Implications for the D6 residue note" in that same `findings.md`, and the clean-widening non-separation fix to `projects/domainspec-v2/impl/tools/lib/meta-type-noncollapse.ts`.
- Raise the `instance` (domainspec-v2-D11) semantics ambiguity to `definitions-governance` as a proposal — declare per rung whether "instance" means a functor into `Set` (data) or a term in `Type` (code).
- Reconcile the stale 29-edge count in `domainspec-v2-D4` and the research layer against the 31 active DS-D8 signatures.

## Recommendation

Keystone is the three still-open verification checks, not the Lane-Z/A experiment. The license is a documented self-declared gap, not a hunch: `2026-07-08-open-questions-noncollapse/findings.md` itself states the checks are "cheap and should run before any number is quoted" while the same resolved-status artifact already quotes the 91 / 27 / 28× magnitudes. Running them is also the cheapest test of this session's only non-derivative contribution, since T-B1 (proxy divergence) and T-B2 (resolution-key sensitivity) are precisely the tests of whether clean-widened edges manufacture phantom distinctions. Lane-Z/A should stay deferred — its default is `defer`, it is non-blocking, and nothing in this session bears on the cost claim that decides it.

## Files touched

- telemetry/agents/subagents-dispatch.yaml
