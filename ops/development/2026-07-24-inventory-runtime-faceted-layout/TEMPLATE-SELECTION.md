# Invoke Template Selection

## Selection

| Stage | Template/profile | Eligibility | Result |
|---|---|---|---|
| Define | DomainSpec `SPEC.md` baseline | Typed capability, state, operation, and acceptance contracts are required. | selected |
| Design | DomainSpec architecture bundle | The target needs all six required design views. | selected |
| Design | Sigil companion | The target is an update to the existing Inventory sigil. | selected |
| Plan | Standalone `IMPLEMENTATION-LAYERING.md` | Mandatory for Invoke Plan. | selected |
| Plan | Standalone split `WORK-PACK.md` | Runtime, schema, generated payload, and consumer proof exceed low complexity. | selected |
| Plan | DomainSpec `EXECUTION-PACK.md` | Medium complexity requires waves and one-SWU routing. | selected |

## Considered And Rejected

- Generic template: rejected because it lacks the required six-view and SWU
  contracts.
- Deprecated module-formulae family: rejected because it is retained only for
  historical fixtures and one legacy research project.
- Research companion: not selected because the accepted research dispatch
  already resolved the candidate design.
- UX-plan companion: not selected because this slice has no human interaction
  surface; operator receipt ergonomics are a CLI contract inside architecture.
- New template family: not required.

## Inventory Evidence

The current Inventory package and existing canonical Inventory development
package were selected as evidence, not authority to approve this plan. The
generated `.agents` packages for Inventory, Dispatch Spec,
Implementation Layering, and Context Builder are absent; canonical public
contracts were used and the generated-runtime gap remains visible.

