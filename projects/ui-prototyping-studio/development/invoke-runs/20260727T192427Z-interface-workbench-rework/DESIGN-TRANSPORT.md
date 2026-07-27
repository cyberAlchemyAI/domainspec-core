---
artifact: ui-prototyping-studio-interface-workbench-design-transport
status: ready-for-invoke-plan
source_stage: invoke-design
target_stage: invoke-plan
authority_effect: none
---

# Design Transport

## Passed Forward

- [Define specification](SPEC.md)
- [Architecture](ARCHITECTURE.md)
- [UX Plan](UX-PLAN.md)
- [Witness contracts](WITNESS-CONTRACTS.md)
- [Validation strategy](VALIDATION-STRATEGY.md)
- [Design scope manifest](DESIGN-SCOPE-MANIFEST.json)
- [Design denominator receipt](DESIGN-DENOMINATOR-RECEIPT.json)
- [Design selection result](DESIGN-SELECTION-RESULT.json)
- [Glossary consistency](GLOSSARY-CONSISTENCY.md)
- [Design Distill gate](DESIGN-DISTILL.md)

## Gate State

| Gate | State |
| --- | --- |
| Define | pass |
| Design denominator | pass |
| Two-pass fixed point | pass |
| Required architecture extensions | authored |
| UX Plan | authored |
| Planned witnesses | UPW-FIX-001–024 authored, unexecuted |
| Glossary consistency | pass |
| Design Distill | pass after accepted DDR-01–DDR-05 revisions |
| Plan admission | allowed for non-mutating authoring |

## Frozen Design Choices

- server-owned opaque whole-projection and region versions;
- coherent projection snapshot with same-snapshot compatibility fields;
- exact project-owned canonical JSON with server/contract digest validation;
- stable no-build shell;
- single-flight refresh with one action-aware trailing-refresh slot;
- safe keyed rendering with full rollback on partial commit failure;
- identity-bound local context reconciliation;
- six-region target contract with Plan-owned L0–L3 implementation slicing;
- existing application/store authority unchanged; and
- no framework, streaming transport, durable draft store, or release expansion.

## Next Owner Contract

Invoke Plan may now:

- map the design to L0–L3 layers;
- reduce it to one-behavior SWUs;
- bind exact write scopes and evidence receipts; and
- recommend one narrow first candidate.

It may not select or execute that candidate.
