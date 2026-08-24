# Invoke Define — Cohesive Modular Arcanum

## Specification baseline

### Problem

Arcanum already has substantial owner-specific contracts, but their transitions use partially overlapping terms, duplicate series reducers, missing concrete owner bindings, stale generated surfaces, and incomplete end-to-end proof. Users experience this as one confusing building system even though no single component owns the whole system.

### Definition objective

Create cohesion through one shared transition grammar while preserving modularity through sovereign effect ownership.

### Normative invariants

1. Every effectful transition has exactly one sovereign effect owner.
2. Producer, validator, router, consumer, state recorder, and lifecycle owner may be different roles; their receipts remain distinct.
3. Every nontrivial handoff uses an OBTC or an owner-specific contract that can be losslessly projected into one.
4. A failed gate names the first stop and forbidden downstream effects.
5. Receipts bind identity, inputs, state epoch or digest, result, evidence, authority effect, and replay/freshness conditions.
6. Shared protocol validation is pure: it may classify but never cause owner effects.
7. Read models and ledgers may reference owner evidence but never upgrade it.
8. Compatibility facades delegate to exactly one canonical state owner.
9. Generated runtime packages must prove provenance plus byte/behavioral parity before being called current.
10. Evidence labels remain `OBSERVED`, `EXECUTED`, and `UNVERIFIED`; fixture success cannot establish product E2E.

### Explicit non-goals

- one universal build runner;
- replacing Invoke, WPRA, Task Session, Continuation Router, Refresh, Craft, lifecycle capabilities, or Inventory;
- selecting an unknown material producer or registry owner by invention;
- implementing source changes in Refine;
- treating a route or receipt as promotion authority;
- publishing private parent evidence into public Arcanum.

### Candidate system boundary

The candidate ABP owns only shared transition schemas, a pure conformance validator, compatibility mapping rules, and trace fixtures. Owner capabilities retain their artifacts, decisions, state, effects, and lifecycle.

## Template and discovery selection

- Discovery evidence: approved `findings.md` plus evidence closure; discovery gate passes.
- Template: DomainSpec specification baseline, compressed into this stage-local private artifact because Refine owns the run folder.
- Glossary: `stages/02-glossary.md`; candidate-only, no canonical promotion.
- Implementation layering: deferred to Stage 9 as required by Invoke Plan; this Define records the explicit gap.

## Dispatch technique trace

| Technique | Activation | Effect |
|---|---|---|
| `sequence` | owner chain is ordered | definitions distinguish legal predecessor/successor states |
| `frame_handoff` | Context Builder precedes Define | source claims are consumed by frame, not copied as authority |
| `owner_boundary_check` | shared-kernel risk | every definition includes an explicit non-role |
| `unique_standard_component` | same record terms recur | one meaning for gate, receipt, owner, and transition |
| `residue_ledger` | three owners and E2E remain open | unresolved items remain named rather than guessed |

Full dispatch: `REFINE-DISPATCH.json`; validation `pass` with zero blocks and flags before execution.

## Definition-scope Distill sanity check

- Candidate split: protocol vocabulary, module catalog, migration plan.
- Decision: keep vocabulary and invariants in one Define artifact because they share one responsibility—fix the semantic grammar consumed by Design.
- Further split: glossary is separated for navigation but remains referenced, not independently authoritative.
- Verdict: `pass`; the design alternatives remain for the Stage 5 tournament.

## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: library authoring applied to a private Refine candidate
- Phase status: pass
- Mode contract: `spells/invoke/define.md`
- Outputs: `stages/02-invoke-define.md`, `stages/02-glossary.md`, layering gap in this artifact
- Template selection: DomainSpec baseline, stage-local private rendering
- Dispatch techniques: sequence, frame_handoff, owner_boundary_check, unique_standard_component, residue_ledger
- Distill validation: pass; one coherent definition baseline with a separate navigational glossary
- Decisions: cohesion is shared grammar; modularity is sovereign effect ownership
- Unresolved gaps: loop owner, material producer, registry owner, canonical Orchestrate repairs, generated parity, real E2E
- Next route: Refine Interrogation then Distill tournament

