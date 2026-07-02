---
artifact_id: domainspec-v2-metatype-workflow
artifact_type: companion-doc
companion_to: workflow.schema.yml
intent: Human companion to the Workflow meta-type machine criterion.
owner: definitions-governance
lifecycle_status: candidate
constitution_selectors: [schema-constitution, meta-type-formalization]
validation_profile: meta-type-card
boundary: PUBLIC shape criterion; the engine src/rules δ-derivation is never referenced (moat).
---

# Workflow — meta-type card (Behavioral)

**Companion to** [`workflow.schema.yml`](./workflow.schema.yml). Prose is non-normative.

## Formal criterion
A concept declared **Workflow** is well-formed IFF its `Attribute | Value` table declares
`scope = intra-feature` (it orchestrates operations within a single feature).

## Distinguisher vs Saga
A Workflow stays within one feature (`scope=intra-feature`); a Saga spans features.

## Edge participation (DS-D8 slice)
- SOURCE of: `performs`
- TARGET of: `applies`

## Fixtures
- positive: [`spec/__fixtures__/mt/workflow-ok.md`](../../__fixtures__/mt/workflow-ok.md)
- negative: [`spec/__fixtures__/mt/workflow-bad.md`](../../__fixtures__/mt/workflow-bad.md) — cross-feature → rejected.

## Boundary
Shape only: the declared `scope` is checked, not the actual reachability of orchestrated operations (moat).
