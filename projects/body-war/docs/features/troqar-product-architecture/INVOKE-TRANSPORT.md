# Invoke Transport

Status: `pass`
Mode: `define+design`
Target artifact: `troqar-product-architecture`

## Template/Profile Selection

| Selection | Why |
| --- | --- |
| DomainSpec feature spec family | User requested DomainSpec domains, operations, UI/UX, and backend definitions. |
| Architecture bundle profile | User requested architecture for all TROQAR pages and backend surfaces. |
| UX/UI companion | Page inventory and visual guide materially affect architecture. |
| Refinement/gap review companion | User requested `/refine` for gaps/blockers after design. |

## Dispatch Technique Trace

| Technique | Applied To | Validation Expectation |
| --- | --- | --- |
| `sequence` | Operations/capabilities first, then domain, then UI/backend. | Artifact order is explicit in `README.md`. |
| `artifact_contract_bridge` | DomainSpec templates to project-local docs. | Aspect docs match template families. |
| `owner_boundary_check` | Body War consumes DomainSpec, does not promote DomainSpec methods. | Architecture states source-authority boundary. |
| `concrete_path_evidence` | Source docs, visual notes, auth package, previous MVP packet. | Every artifact cites local sources. |
| `residue_ledger` | Active Strava and geometry gaps. | `GAP-BLOCKER-REVIEW.md` preserves gaps. |
| `validation_loop` | Syntax/link/path checks. | Final validation commands recorded in the run response. |

## Design Views

| View | Artifact |
| --- | --- |
| Context | `ARCHITECTURE.md#1-context-view` |
| High-level structure | `ARCHITECTURE.md#2-high-level-structure-view` |
| Low-level components | `ARCHITECTURE.md#3-low-level-components-view` |
| Workflow process | `ARCHITECTURE.md#4-workflow-process-view` |
| Decision flow | `ARCHITECTURE.md#5-decision-flow-view` |
| Dependency interface | `ARCHITECTURE.md#6-dependency-interface-view` |

## Glossary Consistency

Status: `flag`

Reason: project seed definitions exist in `docs/INITIAL-DEFINITIONS.md`, but
this app-wide packet introduces product architecture definitions that are not
yet promoted into a canonical glossary. They should remain local candidate
definitions until a definitions-governance route promotes them.

## Next Route

Preferred next route is not app mutation. Use one of:

1. Formal Refine confirmation for the prepared gap/blocker strategy.
2. Invoke plan to turn this app-wide packet into an implementation-layered
   work-pack.
3. Task Session for a bounded W0 spec/page slice selected from this packet.
