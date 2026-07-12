---
id: ide-extension-operations-v1-design-transport
project: ide-extension
title: "Operations V1 Design Transport"
status: pass
node_type: design-transport
updatedAt: 2026-07-12
observed_capability: invoke
invoke_mode: design
---

# Design Transport: Operations V1

## Provenance

| Field | Value |
| --- | --- |
| Observed capability | `invoke` |
| Mode | `design` |
| Target artifact | Operations V1 architecture bundle |
| Lifecycle owner | `projects/ide-extension` |
| Source design | `session-content-canvas-design/ARCHITECTURE-BUNDLE.md` |
| Review authority | `html-builder-architecture-review/findings.md` |
| Runtime mutation | none |

## Source Contracts

- Existing V0 complete-file behavior remains unchanged.
- Compatibility is achieved through a separately derived surface identity.
- Whole-document operations precede declared regions.
- CAS, operation idempotency, and durable request/result binding are mandatory.
- Navigation and display refresh do not create content revisions.
- Trusted-local value remains distinct from hostile HTML or production claims.

## Dispatch Technique Trace

| Technique | Effect on design |
| --- | --- |
| `sequence` | V0 design and accepted review feed the Operations V1 bundle, then validation and plan handoff. |
| `concrete_path_evidence` | Source contracts are cited by repository path. |
| `artifact_contract_bridge` | Review obligations become explicit interfaces, decisions, and validation expectations. |
| `state_namespace_boundary` | Workspace V0 bytes, immutable blobs, event metadata, projection, and browser DOM have distinct owners. |
| `owner_boundary_check` | Invoke authors design; later plan and Task Session own implementation. |
| `authority_split_gate` | Preview/display operations do not grant protected-effect authority. |
| `validation_loop` | Dispatch validation and six-view/Distill checks gate handoff. |
| `residue_ledger` | Parser choice, size limits, GC, navigation durability, and regions remain named. |
| `handle_handoff` | Planning consumes artifact paths rather than copied source bodies. |
| `observability_grouping` | This design run has one Invoke observability group. |

Full dispatch: [operations-v1-design.dispatch.json](operations-v1-design.dispatch.json).

## Design Gates

- Six required views: `pass`.
- Glossary consistency: `pass`.
- Compatibility with original V0 API: `pass` by separate identity.
- Design-unit Distill: `pass`.
- Runtime implementation authority: not granted.

## Gap Ledger

| Gap | Owner | Required route |
| --- | --- | --- |
| Parser package/version and serialization fixtures | Operations V1 plan | Resolve before parser SWU. |
| Request/body limits | Operations V1 plan | Bind to server/body-store constraints. |
| Blob GC policy | Operations V1 plan | Define retention or explicit deferral. |
| Navigation durability | Operations V1 plan | Select ephemeral ack or durable command record. |
| Region mutation semantics | Future design | Keep outside current plan. |

## Next Route

`invoke plan operations_v1` after the operator accepts this design. The current
requested second route is instead the independent V0 issue-repair plan.
