---
tags: [cyberalchemy-v2, definitions, canonical-kind, canonical-artifact, process, node-type, edge-catalog, ontology-conventions, review-dispatch, authority-decision]
node_type: conceptual
is_session: true
layer: ontology
nature: explanatory, technical, reference
status: active
created: 2026-07-13
timestamp: 2026-07-13T10:08:06-03:00
expires: 2026-09-11
conversation_id: 2026-07-13-process-retraction-canonical-kind-ruling
decisions_made: true
contradictions_found: true
specs_updated: [cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md, cyberAlchemy-v2/authority/decisions/2026-07-13-canonical-kind-one-label.md, cyberAlchemy-v2/authority/definitions/DEFINITIONS.md, cyberAlchemy-v2/authority/definitions/DEFINITION-DRIFT-AUDIT.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "A five-agent review found that the new CANONICAL-KINDS Edges section silently forks an already-correct consolidated constitution while CAV2-D51's central artifact predicate lost its only referent, and the owner's one-label ruling — previously spoken only in conversation — became the first written record of a decision three attacker findings had to be dropped for lacking."
---

# The `process` retraction, and the `canonical_kind` one-label ruling

## Summary

The session opened by checking what prior sessions had settled about canonical artifacts, and found that `CAV2-D51`'s formal clause — `canonical(a) <-> kind(a) in CanonicalKinds and origin(a) = process(kind(a))` — calls a term the spine never defined, leaving the repository's central artifact predicate undecidable. It promoted `CAV2-D56 process` as a build-from-owned specialization of `CAV2-D32 method`, then **retracted it the same day**: the definition had been reverse-engineered from a single consumer (D51's call site) rather than carved on its own terms, and `make bump-check` is a process that emits no canonical kind, so output-typing was never the essence of one. The owner then issued three corrections — `node_type` and `canonical_kind` are one label, not two orthogonal ones; `derives-from` names a document's **input artifacts** and is *not* `process_origin`, which names the **producer** that generated it; and the type-level edge graph may contain cycles. Eight canonical kinds were added to `CANONICAL-KINDS.md`, closing a genuine hole where four enumerated authority kinds (`Discipline`, `Runtime contract`, `Projection`, `Residue`) had no canonical kind rolling up to them, alongside a candidate edge catalog and an open hom-sets section. A five-agent review dispatch (three attackers, two verifiers) then surfaced the session's most consequential finding: `implementation/domainspec/vault/ontology-conventions.md`, a **consolidated v2.3.0 constitution**, already implements the exact three-way split the owner demanded — `derives-from` for inputs, `creates`/`created-by` for the producer — and the new `## Edges` section silently forks its 22-edge catalog, reviving six edges that catalog explicitly deprecated while omitting `creates` entirely. The review further established that the agent had self-closed its own open question (`OQ-7`) inside one session with no owner gate, and that `CAV2-D51`'s clause is now not merely open but **not truth-evaluable**, since `process(·)` has had no referent since the retraction. Three attacker findings were dropped by the verifiers for a telling reason: the owner's `node_type == canonical_kind` ruling existed nowhere in writing, only in conversation — so agents were reasoning from a rule the tree did not contain. The owner then ratified the ruling: `canonical_kind` is the one label (chosen for explicitness), the enumeration takes 22 values (the 17 existing plus `implementation-plan`, `audit`, `conceptual`, `backlog`, `readme`), a session record's kind is `session`, and **nothing is migrated** — the decision defines, it does not rewrite the corpus. That ruling landed in `authority/decisions/2026-07-13-canonical-kind-one-label.md`, which records plainly that no file in the repository carries a `canonical_kind:` field and that the enumeration is therefore a definition, not a description of the repo; `CANONICAL-KINDS.md` was then corrected to match — the false schema-vs-role claim deleted, the improper `OQ-7` self-closure struck and re-settled by owner decision, acyclicity scoped to the instance graph, and the `## Edges` section flagged as forking a consolidated catalog.

## Contradictions

- validates `implementation/domainspec/vault/ontology-conventions.md` — the review confirmed this consolidated v2.3.0 constitution already implements the exact three-way edge split (`derives-from` for inputs at :570, `creates`/`created-by` for the producer at :599) that the session spent hours re-deriving in ignorance of it.
- contradicts `cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md` — its new `## Edges` section forks that consolidated 22-edge catalog, reviving six edges the catalog explicitly deprecated (`contextualizes`, `depends-on`, `questions`, `updates`, `exemplifies`, `resolves`), promoting `updates` to a morphism, and omitting `creates` entirely; its claim that the verbs are "already in use, not invented here" is false as written.
- questions `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md` — `CAV2-D51`'s formal clause calls `process(·)`, which has had no referent in the spine since the `CAV2-D56` retraction, leaving the canonical-artifact predicate not truth-evaluable rather than merely under-specified.
- questions `cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md` — its `residue` row is a canonical kind with no producer (a by-product, not something authored), which cannot satisfy `CAV2-D51`'s `origin(a) = process(kind(a))` conjunct; either the enumeration or the membership condition is wrong. Owner-parked.
- questions `cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md` — its `## Hom-Sets` section leaves the category undecided between free (every path distinct) and carrying path equations, but composition arrives whether intended or not: given `spec --implements--> constitution` and `constitution --derives-from--> axiom`, a morphism `spec -> axiom` exists and something must say what it is.
- questions `cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md` — its `## Edges` section rules `contradicts` a "defect marker to eliminate, never a relation to compose", but the argument offered (symmetric ⇒ cycles ⇒ infinite hom-sets) licenses only "not admitted as a morphism"; the governance verdict does not follow from the cardinality observation.

## Next steps

- Reconcile `CANONICAL-KINDS.md`'s `## Edges` section with the consolidated catalog in `implementation/domainspec/vault/ontology-conventions.md` — supersede it, import it, or scope out of it. It may not silently fork it. Route: `decision-gate`.
- Eliminate or redefine `process(·)` in `CAV2-D51`'s Formal Interpretation, so an active card's formal voice stops calling an undefined symbol. Only then adjudicate `residue`.
- Reopen `CA-OQ-2` to consider wiring `process_origin` to the vault's existing `created-by` edge before minting any attestation scheme — the fork was drawn without knowing the producer edge already existed.
- Commit the three uncommitted artifacts: the `CANONICAL-KINDS.md` edits, the decision record, and the review findings.

## Recommendation

The keystone is the **edge-catalog collision**, because it is the one place where the correct model already exists and is being overwritten by a worse one authored in ignorance of it. Licensing fact: the review verified `ontology-conventions.md:570` and `:599` directly — that constitution is `status: consolidated`, v2.3.0, and carries `derives-from` (inputs) and `creates`/`created-by` (producer) as typed edges with inverses, which is precisely the split the owner had to correct the agent into twice. Recommend the next session settle that collision through `decision-gate` *before* touching `CAV2-D51`'s clause, since the producer edge it needs may already be defined and the `process_origin` fork may dissolve on contact. That the catalog is authoritative is a validated node, not a hunch; that resolving it will also close `CA-OQ-2` is a hunch.

## Files touched

- cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md
- cyberAlchemy-v2/authority/decisions/2026-07-13-canonical-kind-one-label.md
- cyberAlchemy-v2/authority/definitions/reviews/2026-07-09-post-correction-audit/findings.md
- cyberAlchemy-v2/authority/definitions/DEFINITIONS.md
- cyberAlchemy-v2/authority/definitions/DEFINITION-DRIFT-AUDIT.md
- telemetry/agents/subagents-dispatch.yaml
