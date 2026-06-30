---
tags: [inventory, synthesis, category-theory, formalization, commercialization, defensibility, claim-le-proof, build-from-owned]
node_type: synthesis
is_session: false
layer: architecture, commercialization
nature: explanatory, reference
status: candidate
created: 2026-06-28
boundary: INTERNAL — moat-adjacent (the agent⊨spec verifier IS the moat); do NOT copy into public arcanum/
dispatch_id: kodamai-correctness-layer
dispatch_type: research
working_folder: domainspec-lean-formalization/research-ai/kodamai-correctness-layer/
sources:
  - domainspec-lean-formalization/research-ai/kodamai-correctness-layer/research/findings.md
  - domainspec-lean-formalization/lean-engineer/AgentPermissionKernel.lean
  - domainspec-lean-formalization/lean-formalization/FunctorialResidueStructure.lean
  - domainspec-lean-formalization/SMITHE-2024-AUDIT.md
---

# Kodamai / Smithe — the "agent correctness layer," its moat, and our leapfrog lane

Candidate Inventory synthesis (**promotes nothing**; owners = lean-formalization theorem
route + commercialization). Claim ≤ proof throughout: every verdict below is a public-corpus
read, never a claim about Kodamai's internal state.

## Who Kodamai is
**Kodamai Ltd is Toby St Clere Smithe's company** — he is co-founder/CTO (inc. Feb 2025;
arXiv:2603.09431 carries a "Kodamai Ltd" affiliation; third co-founder **Neil Ghani**,
categorical type theory, resigned Feb 2026 pre-launch). Product: "Kelvingrove." So the
website's math is Smithe's published research program (categorical active inference).

## The claim decomposition (verdict matrix, condensed)
The pitch ("categorical denotational model of AI agents / formal interface contract /
bidirectional control flow / validates agent behavior at scale / provably correct") splits:
- **Substrate = build-from-owned** (Bayesian lenses, poly-functor interfaces) — thesis-grade
  *semantics*, owned on Spivak–Niu / Myers (Categorical Systems Theory) / optics / open-games;
  Smithe owns only the *Bayesian-lens instance*.
- **The verifier = unpublished moat.** A categorical **`agent ⊨ spec` satisfaction judgment +
  soundness theorem** (and anything "at scale") is published **nowhere** — not Smithe, not
  prior ACT, not us. Everywhere the *type* exists and the *certifying judgment* does not.
  "denotational" is honorific (absent from 2406.07577); "provably correct" = "well-typed"
  with the type-soundness theorem deleted.

## What WE own (machine-checked, the leapfrog lane)
Two sorry-free halves, in **provably-disjoint files** (grep-verified, zero cross-reference):
- `lean-engineer/AgentPermissionKernel.lean` — a **sound decidable judgment** on the agent
  tool-call surface (`decidePolicy_sound`:162, `deny_precedence`:170, `layered_not_flattenable`,
  taint/egress monotonicity, layer composition). *More verifier than Smithe has published* — but
  a decidable policy algebra, not a categorical agent denotation.
- `lean-formalization/FunctorialResidueStructure.lean` — a **genuine functor** (`separation_is_functor_action`:513),
  but it denotes *knowledge-residue*, not agents.

**First buildable target:** the bridge — one agent + one property + a categorical denotation +
a sound `⟦A⟧ ⊨ φ` judgment on the *same* object. **Collapse-test:** if `agent ⊨ spec` reduces to
the existing `decidePolicy` check with no functorial content, the categorical framing adds nothing.

## Connections
- The FOL/model-theoretic counterpart of this same `⊨` prize is the cross-rule (Row-2) layer in
  [[fol-constitution-validation-complement-synthesis]] — a **complement**, not a competitor:
  FOL handles the discrete governance layer, categorical handles the residue/behavior layer.
- Moat discipline: cite + demonstrate results, never publish the bridge construction
  (engine-algorithm-proprietary posture).

## Evidence — 2026-04 launch + site security page (corpus re-pass, 2026-06-29)
Kodamai exited stealth ~2026-04-13 with **Kelvingrove** (customer **First Mills**, 4 facilities,
"thousands of decisions/day"). Combined press-release + security-page claim set: "machine-checkable
proofs of correctness for every consequential action," "formal proof generation before any
consequential action," "typed invariants" agents "cannot violate even under adversarial inputs,"
audit logs/traceability storing "the mathematical proof of compliance" as a "proof artifact." **Yet
no specimen proof, no runnable checker, no proof system named, no soundness theorem, no
Lean/Coq/Agda** anywhere in corpus; category theory named only as "denotational model" (honorific,
lines 38–42); no agent count substantiated ("10,000 typed agents" = JS homepage only).

**Tell — mechanism-asymmetry:** where a claim is real & standard they name the mechanism (IAM =
SAML/OIDC; on-prem/VPC; zero-standing-privilege = capability security); where it's the moat (proof
generation) they name only the outcome. That whole IAM / zero-trust / audit-log layer is
**build-from-owned**, already core-formalized in `AgentPermissionKernel.lean` (decidable policy,
deny-precedence, taint/egress monotonicity, no-lateral-movement = layer comp).

**Honest seam — "provably constrained" ≠ "provably correct":** a runtime gate that blocks any action
failing a *decidable* invariant genuinely prevents violation of the **encoded** predicate
(reference-monitor soundness — real, owned). It does NOT establish (a) the invariant *adequately
models* real policy, (b) sequence/aggregate properties a per-action check can't state, or (c) that
the LLM *chose the right action* (proof sits downstream of LLM judgment). Defensible claim =
**constrained**; marketed claim = **correct**; the gap is unshown.

**DomainSpec implications (owner: language design — not this synthesis):** (1) collapse-test risk —
a `decidable invariant` emitting "PROOF VERIFIED"+"proof hash" reproduces the inflation (flat
predicate, zero functorial content); label *register* (decidable-check vs discharged-proof) AND
*scope* (`action ⊨ invariant`, never "agent correct"). (2) Differentiator is **demonstration vs
assertion** — they DO market a stored proof-artifact, so the edge is a *runnable checker + specimen +
soundness theorem*, not "they lack the idea." (3) Plant the flag on the seam: state what's proven
(action satisfies encoded invariant) and what isn't (adequacy, trace-safety, choice-quality).
Sources: cityam/businesswire 2026-04-13; middleeastainews; kodamai.com security page (user-supplied 2026-06-29).

**Executed corroboration (2026-06-29):** the correctness-ownership sweep (research dispatch
`2026-06-29-correctness-ownership-sweep`; `projects/domainspec-v2/research/2026-06-29-correctness-ownership-sweep/findings.md`)
ran our OWN side under scrutiny — `dcb→hash` flip verdict-invariant (freshness guard collapses to
content-hash), an empty-trace "lying run" passes 2/3 saga assertions, `m6Witnesses` executes under
Lean. It confirms from the inside: **neither we nor Kodamai own a behavioral/concurrency verifier.**
Our differentiator is owned honest-labeling discipline + executed *bounded* witnesses + a
self-caught-overclaim trail — artifacts their corpus does not show. Strengthens the well-typed≠proven
residue with executed evidence (claim ≤ proof applied to ourselves).

## Residue
- Unpublished ≠ absent-internally (unknowable from corpus). "At scale" has zero mathematical
  referent in any source. The bridge is intended/buildable, **not built**.

## Boundary
Inventory candidate read-model. Promotes nothing. INTERNAL — moat-adjacent.
