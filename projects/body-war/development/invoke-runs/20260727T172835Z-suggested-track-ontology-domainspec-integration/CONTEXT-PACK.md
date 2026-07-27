---
module: body-war-suggested-track-ontology-domainspec-integration
version: current
status: authored
updatedAt: 2026-07-27
docType: invoke-context-pack
contextMode: standard
runtimeHandoff: false
---

# Context Pack

## Task

Author an Invoke Define, Design, and Plan package inside Body War for three
independent witnesses:

1. a standalone Body War ontology test;
2. a standalone DomainSpec canonical-node test for SuggestedTrack rule CT-2;
3. a digest-bound integration test that composes the first two.

This pack is authoring context. It is not a Task Session runtime handoff.

## Obligation Matrix

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Keep Body War as the consumer owner. | `.craft/ledger.yml` context `CTX-BODY-WAR-SUGGESTED-TRACKS` | covered |
| O2 | Reuse an implemented SuggestedTrack rule. | `operations.md` rules CT-2 through CT-4; repository implementations | covered |
| O3 | Keep ontology meaning separate from executable DomainSpec logic. | CyberAlchemy ontology candidate rules; DomainSpec node-authority profile | covered |
| O4 | Produce three independently reviewable tests. | User intent in this Invoke activation | covered |
| O5 | Preserve candidate and release claim ceilings. | ontology candidate status; DomainSpec development profile release admission | covered |
| O6 | Route implementation through bounded SWUs. | Invoke Plan and Distill contracts | covered |

## Selected Context

| Source | Selectors | Obligation fit |
| --- | --- | --- |
| `projects/body-war/.craft/ledger.yml` | `CTX-BODY-WAR-SUGGESTED-TRACKS`, active blockers/gaps | O1, O5 |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/DISCOVERY.md` | Current Truth, Decision Inventory, Validation Route | O1, O2 |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/SPEC.md` | SuggestedTrack creation capability and concept graph | O2 |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/operations.md` | `CreateSuggestedTrack`, CT-2 through CT-4 | O2, O4 |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/states.md` | `none -> needs_evidence` transition | O2, O4 |
| `projects/body-war/app/src/auth/memory-repository.ts` | `createSuggestedTrack` | O2, O4 |
| `projects/body-war/app/src/auth/drizzle-repository.ts` | `createSuggestedTrack` | O2, O4 |
| `cyberAlchemy/ontology/README.md` | candidate-entry and non-authority rules | O3, O5 |
| `projects/domainspec-v2/impl/spec/sfol-profile/node-logic-envelope.schema.json` | canonical `body.logic` envelope | O3, O4 |
| `projects/domainspec-v2/impl/spec/sfol-profile/minted-project-profile.json` | admitted kinds, edges, and development ceiling | O3, O5 |
| `.arcanum/inventory/entries/domainspec-v2-spec-ontology-node-layering-dispatch-closeout-synthesis.md` | one graph, candidate sidecar, non-collapse residue | O3 |

## Excluded Context

- Hosted deployment and real Strava activity evidence: unrelated to CT-2
  creation semantics.
- Source-backed geometry and pilot-ready promotion: explicitly outside the
  SuggestedTrack creation rule.
- Financial Settlement business rules: useful engine precedent but not Body
  War domain authority.
- App UI files: no rendered semantic contract changes are planned.

## Context Builder Result

- Mode: standard
- Files selected: 11
- Obligation coverage: 100%
- Strict coverage: pass
- Runtime handoff: none
- Blockers: 0 for authoring

