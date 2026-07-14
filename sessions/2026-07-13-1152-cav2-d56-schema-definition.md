---
tags: [definitions-governance, schema, cyberalchemy-v2, ontology, arcanum, domainspec, non-collapse]
node_type: discovery
is_session: true
layer: ontology, architecture
nature: explanatory, technical
status: active
created: 2026-07-13
timestamp: 2026-07-13T11:52:39-03:00
expires: 2026-09-11
conversation_id: 2026-07-13-cav2-d56-schema-definition
decisions_made: true
contradictions_found: true
specs_updated: [cyberAlchemy-v2/authority/definitions/DEFINITIONS.md, cyberAlchemy-v2/authority/definitions/DEFINITIONS-INDEX.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "Mints CAV2-D56 generic schema on a four-part kinds/constraints/relations/connection-rules structure, but does so by overturning the 2026-06-22 13-agent review verdict that said do NOT mint a generic schema, without filing the CAV2-D25 witness that verdict required — so the definition currently stands on owner direction, not on discharged evidence."
---

# CAV2-D56 — Schema Defined Locally, Overturning the MINIMAL Verdict

## Summary

The session opened as a lookup — does a canonical definition of `schema` exist — and
became a rewrite of it. Tracing the term established that Arcanum owned it
(`DEF-ARC-SCHEMA`), CyberAlchemy v2 referenced it under two boundary clauses,
DomainSpec instantiated it per meta-type, and the sibling `domainspec-lean-formalization`
repo had already resolved a three-way `Schema` name collision via `SchemaTaxonomy.lean`;
all three registers independently assert the same non-collapse law — schema is shape
evidence, never authority. Testing DomainSpec's meta-type system against v2's "subtype
only if authority behavior differs" trigger showed it fails the trigger, so no subtype
was warranted on that branch. The operator then rejected `DEF-ARC-SCHEMA`'s formal voice
as notation-bound: it enumerated fields, enums, and row families, and so could not
describe a Spivak schema — a category of objects and morphisms, and one of the system's
own carriers. Three assistant errors were corrected by the operator, each yielding a
finding: that `Customer` is schema and `José` the instance, exposing `instance` as a
second, unowned cross-register collision; that a constraint on an occupant's values and a
rule on how kinds may connect are separate parts, a split DomainSpec already ratifies as
`domainspec-v2-D8` (formal criterion) versus `domainspec-v2-D9` (edge-participation
signature); and that v2 does re-author Arcanum-owned terms, since `CAV2-D51` and
`CAV2-D32` already do so under non-normative ancestral provenance. On that precedent, and
on repeated operator direction, `schema` was defined locally as `CAV2-D56` with a
four-part normative structure — kinds, constraints, relations, connection rules —
asserting that constraints and connection rules do not reduce to one another, that
conformance is decidable by inspection alone, and that a schema is relative to a level.
The boundary clauses in `CAV2-D21` and `CAV2-D25` that had asserted schema was
Arcanum-owned were amended to cite `CAV2-D56`, and the index was synced. Only at close
did the 2026-06-22 session surface, whose 13-agent tension-gated review had already
ruled MINIMAL depth and "do NOT mint a generic schema" — so CAV2-D56 stands as an
overturn of a review-verified decision, not an increment on it. An interim three-part
rewrite of Arcanum's `DEF-ARC-SCHEMA` was made and then reverted by the operator;
Arcanum is unchanged, and nothing was committed.

## Contradictions

- contradicts `sessions/2026-06-22-1945-cav2-definitions-schema-governance.md` — its
  13-agent review returned MINIMAL depth and the next-step "Do NOT mint a generic/Fuller
  `schema`; if pursued, only a narrow Arcanum-subtyped handle ... gated on a filed D25
  witness." CAV2-D56 is generic, not a subtype, and no D25 witness was filed. The verdict
  is overturned by owner direction, not discharged. The overturn was pursued on new
  evidence that review did not hold: `DEF-ARC-SCHEMA`'s formal voice enumerates fields,
  enums, and row families, and therefore cannot describe a Spivak schema — a carrier the
  system itself relies on.
- validates `sessions/2026-06-22-1945-cav2-definitions-schema-governance.md` — its own
  Open Question, "Is `schema` worth defining locally at all, or stay referenced-to-Arcanum?
  → definitions-governance", routes the ownership decision to definitions-governance, the
  venue that ran this session. The overturn is therefore procedurally licensed even though
  substantively unearned.
- questions `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md` — that same review held
  that objects+morphisms are already owned by `CAV2-D16`/`CAV2-D19` and `DS-D8`. Whether
  CAV2-D56's `relations` and `connection rules` parts duplicate that ownership was never
  engaged in this session.
- contradicts `cyberAlchemy-v2/authority/definitions/DEFINITION-DRIFT-AUDIT.md` — its
  `pass` row asserts "Arcanum-wide `contract` and `schema` semantics are not redefined
  locally." CAV2-D56 redefines `schema` locally; the row is now false and was not updated.
- contradicts `cyberAlchemy-v2/development/research/2026-06-21-schema-taxonomy-view-primitives/findings.md` —
  its verdict matrix ruled generic Schema "reference-only; subtype only if needed."
  CAV2-D56 departs from reference-only while still honoring build-from-owned.
- questions `projects/domainspec-v2/definitions/DEFINITIONS.md` — `domainspec-v2-D11`
  (`instance` = concept normalized to YAML) collides with the Spivak/Lean sense
  (`instance` = the population below the schema). The two sit one altitude apart and no
  spine owns the term.
- validates `projects/domainspec-v2/definitions/DEFINITIONS.md` — `domainspec-v2-D8`
  (formal criterion, per-occupant predicate) and `domainspec-v2-D9` (edge-participation
  signature, who-may-connect-to-whom) already separate occupancy from connection,
  ratifying CAV2-D56's refusal to merge constraints with connection rules.

## Open questions

- Is `schema`/`instance` a *relation* between adjacent levels rather than an absolute
  kind — and if so, must every structural term in the spine carry a level index to be
  well-formed? CAV2-D56 asserts the relativity in its Formal Interpretation, but the
  general obligation it implies was neither derived nor tested.

## Next steps

- File the `CAV2-D25` amendment record and witness covering CAV2-D56 and the amended
  `CAV2-D21`/`CAV2-D25` boundary clauses. This is required by CAV2-D25's own normative
  rule (an authority-affecting shape change carries an amendment + witness) and was the
  explicit gate named by the 2026-06-22 verdict.
- Engage the MINIMAL verdict's substantive argument: determine whether CAV2-D56's
  `relations`/`connection rules` duplicate `CAV2-D16`/`CAV2-D19`/`DS-D8`, and either cite
  them as the owners or justify the local re-ownership.
- Update the false `pass` row in `DEFINITION-DRIFT-AUDIT.md`.
- Add the `### Schema` section to CAV2-D56 and its row in `DEFINITION-SCHEMAS.md` — its
  formal voice asserts the tuple `S = (K, C, R, N)`, which the index governance note
  requires to be tracked.
- Decide the disposition of the `instance` collision: which spine, if any, owns the term.

## Recommendation

The keystone is the redundancy challenge — the `questions` edge on `DEFINITIONS.md` — not
the overturn itself. The overturn is procedurally licensed: the `validates` edge above
shows the 2026-06-22 node routed the schema-ownership decision to definitions-governance,
the venue that ran here, and the operator directed the outcome. What was *not* done is
engage that review's **substantive** claim: that objects+morphisms are already owned by
`CAV2-D16`/`CAV2-D19`/`DS-D8`, making a generic schema redundant. Nothing found here
touches it. The Spivak-coverage failure cited in the first edge, and the D8/D9 split in
the last, both defeat the *old wording* — neither defeats the *redundancy argument*. Next
session should attack that claim head-on before CAV2-D56 is committed; if it survives,
file the D25 witness and the definition is earned rather than merely directed. Self-labeled
hunch on the outcome: a 13-agent tension-gated review is the strongest standing evidence in
this lineage, and it has not yet been answered.

## Files touched

- cyberAlchemy-v2/authority/definitions/DEFINITIONS.md
- cyberAlchemy-v2/authority/definitions/DEFINITIONS-INDEX.md
