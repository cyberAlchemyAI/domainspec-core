---
artifact_id: domainspec-v2-metatype-saga
artifact_type: companion-doc
companion_to: saga.schema.yml
intent: Human companion to the Saga meta-type machine criterion.
owner: definitions-governance
lifecycle_status: candidate
constitution_selectors: [schema-constitution, meta-type-formalization]
validation_profile: meta-type-card
boundary: PUBLIC shape criterion; the engine src/rules δ-derivation is never referenced (moat).
---

# Saga — meta-type card (Behavioral)

**Companion to** [`saga.schema.yml`](./saga.schema.yml). Prose is non-normative.

## Formal criterion
A concept declared **Saga** is well-formed IFF its `Attribute | Value` table declares
`scope = cross-feature` (long-running orchestration across features / bounded contexts).

## Distinguisher vs Workflow
A Saga spans features (`scope=cross-feature`); a Workflow stays within one feature.

## Edge participation (DS-D8 slice)
- SOURCE of: `performs`
- TARGET of: `applies`

## Fixtures
- positive: [`spec/__fixtures__/mt/saga-ok.md`](../../__fixtures__/mt/saga-ok.md)
- negative: [`spec/__fixtures__/mt/saga-bad.md`](../../__fixtures__/mt/saga-bad.md) — single feature → rejected.

## Boundary
Shape only: the declared `scope` is checked, not cross-context consistency semantics (moat).
