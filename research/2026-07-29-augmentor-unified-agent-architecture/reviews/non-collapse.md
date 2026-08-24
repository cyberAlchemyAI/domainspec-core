# Definitional and authority non-collapse review

- Action: `spawn-0007`
- Reviewer: `Quine, Willard Van Orman`
- Verdict: `REPAIR`
- Mutation: none

The following separations pass: graph ≠ memory/source; inference ≠ fact;
retrieval ≠ reasoning; judgment ≠ approval; effort ≠ evidence; proposal ≠
execution; Run ≠ session/thread; Inventory ≠ authority; ontology map ≠
decision; model ≠ promoter; Saturn ≠ runtime/store. Consumption ≠ intake passes
at the object level but the lifecycle edge needs repair.

## Defects

1. The catalog says `AuthorityDecision` and `PromotionRecord` are distinct with
   cardinality unresolved (`synthesis.md:71`), but C20 and later sequences use
   `decision/promotion record` as one artifact/edge (`synthesis.md:101,136`).
   Canonical authority requires explicit scope, owner, surface, operation,
   basis, effect, and challenge route
   (`cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:2180,3193`).
2. `MemoryIntakeRequest -> Inventory EvidenceSet` skips provider acceptance and
   evidence conversion (`synthesis.md:136`). An intake request cannot
   manufacture evidence.
3. Explorer residue says `OntologyCandidate plus PromotionRecord initially
   block` (`research.md:185`). C19 wisely removed this; writing must not
   reintroduce it.

## Required repair

- Split C20 provisionally into a named authority owner producing an
  `AuthorityDecision`, then an owner-routed transition/audit registrar producing
  a PromotionRecord-compatible record, then a canonical authority artifact,
  then an optional governed projection.
- Keep identity/cardinality/schema unresolved; do not claim two durable schemas
  exist.
- Use:
  `MemoryIntakeRequest -> provider review/accepted source change or admitted
  evidence -> Inventory EvidenceSet -> OntologyCandidate -> owner
  AuthorityDecision -> PromotionRecord-compatible record -> canonical authority
  artifact -> optional governed projection`.
- PromotionRecord is transition/audit evidence, never the canonical authority
  artifact.
- Preserve the existing public/private boundary.
