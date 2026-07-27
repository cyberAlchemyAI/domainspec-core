---
module: body-war-suggested-track-ontology-domainspec-integration
version: current
status: pass
updatedAt: 2026-07-27
docType: invoke-define-transport
---

# Invoke Define Transport

## Intent Record

- Target: Body War SuggestedTrack child context.
- Approved action: author Define, Design, and Plan artifacts.
- Required witnesses: ontology standalone, DomainSpec standalone, integration.
- Concrete rule: CT-2, with CT-3 and CT-4 guardrails.
- Mutation boundary: this Invoke run only; no implementation or upstream
  authority mutation.

No interview question was required. The user supplied the target, three-test
shape, location, and request to author all three Invoke stages.

## Discovery Gate

- Discovery source:
  `projects/body-war/docs/features/parque-taquaral-online-mvp/DISCOVERY.md`
- Result: pass; no discovery waiver used.

## Template Selection

| Candidate | Eligibility | Selection |
| --- | --- | --- |
| DomainSpec spec family | Existing Body War feature uses the DomainSpec aspect-doc contract; target includes typed nodes, rules, edges, and derived tests. | selected |
| Generic architecture family | Usable, but weaker than the DomainSpec six-view profile for node and edge contracts. | not selected |
| UX plan | No rendered semantic contract changes. | not applicable |
| Research family | Core architecture choice is already bounded; implementation unknowns are plan gaps, not research blockers. | not selected |

Inventory lookup used the repository machine index. Lookup readiness passed;
the selected ontology-layering synthesis remains a candidate Inventory read
model and does not grant authority.

## Define Result

- Spec: `SPEC.md`
- Glossary: `GLOSSARY.md`
- Layering: deferred to mandatory Plan companion
- Glossary linking: linked to existing Body War rule names; local additions
  remain candidate
- Distill: not run at Define; the target is already split into three explicit
  witnesses and Plan will run mandatory validation
- Unresolved blockers: none for Define authoring
- Next route: Invoke Design

